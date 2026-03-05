#!/usr/bin/env python3
"""Deep Judge Agent — autonomer Coach mit Wissensbasis-Navigation.

Schicht 3 im Sidecar Stack:
  1. Deterministisch ($0, <1ms, SYNC) — Gates + Detektoren
  2. Quick Judge (~$0.0002, <2s, SYNC) — LLMJudge in llm_judge.py
  3. Deep Judge (~$0.005, 5-15s, ASYNC) — dieser Agent

Der Deep Judge navigiert Samuels Wissensbasis autonom via Function Calling
(MiniMax M2.5) und gibt personalisiertes Coaching-Feedback.

Laeuft als asyncio.Task im Daemon. Ergebnis wird gecacht und beim
naechsten UserPromptSubmit als [DEEP-JUDGE] injiziert.
"""

import asyncio
import json
import os
import time

_LOG_PATH = "/tmp/claude-sidecar.log"
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_KNOWLEDGE_DIR = os.path.join(_BASE_DIR, "knowledge")
_INDEX_PATH = os.path.join(_KNOWLEDGE_DIR, "knowledge_index.json")


def _log(msg: str) -> None:
    try:
        with open(_LOG_PATH, "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [deep-judge] {msg}\n")
    except Exception:
        pass


# --- Knowledge Tools (executed locally, no API cost) ---

def _load_index() -> dict:
    """Load knowledge_index.json. Cached after first load."""
    try:
        with open(_INDEX_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        _log(f"Failed to load index: {e}")
        return {"topics": {}, "files": {}}


_cached_index: dict | None = None


def _get_index() -> dict:
    global _cached_index
    if _cached_index is None:
        _cached_index = _load_index()
    return _cached_index


def reload_index():
    """Force reload of knowledge index (called by sidecar-ctl reindex)."""
    global _cached_index
    _cached_index = None
    _get_index()
    _log("Knowledge index reloaded")


def tool_read_file(path: str, section: str = "") -> str:
    """Read a file from knowledge/. Optionally extract a ## section."""
    safe_path = os.path.basename(path)  # prevent directory traversal
    full_path = os.path.join(_KNOWLEDGE_DIR, safe_path)

    if not os.path.exists(full_path):
        return f"Error: File '{safe_path}' not found in knowledge base."

    try:
        with open(full_path, "r") as f:
            content = f.read()
    except Exception as e:
        return f"Error reading '{safe_path}': {e}"

    if not section:
        # Limit to ~4000 chars to stay within token budget
        if len(content) > 4000:
            return content[:4000] + f"\n\n[... truncated, {len(content)} chars total]"
        return content

    # Extract section by ## heading
    lines = content.split("\n")
    in_section = False
    section_lines = []
    section_lower = section.lower().strip("# ")

    for line in lines:
        if line.startswith("## ") or line.startswith("# "):
            if in_section:
                break  # next section starts
            heading = line.lstrip("# ").strip().lower()
            if section_lower in heading:
                in_section = True
                section_lines.append(line)
                continue
        if in_section:
            section_lines.append(line)

    if not section_lines:
        return f"Section '{section}' not found in '{safe_path}'. Available headings: " + \
               ", ".join(l.lstrip("# ").strip() for l in lines if l.startswith("## "))[:500]

    result = "\n".join(section_lines)
    if len(result) > 4000:
        return result[:4000] + f"\n\n[... truncated, {len(result)} chars total]"
    return result


def tool_search_knowledge(query: str) -> str:
    """Search knowledge index for relevant topics. Returns top 3 matches."""
    index = _get_index()
    topics = index.get("topics", {})
    query_lower = query.lower()
    query_words = query_lower.split()

    scored = []
    for topic_name, topic_data in topics.items():
        score = 0
        keywords = topic_data.get("keywords", [])
        description = topic_data.get("description", "").lower()

        for word in query_words:
            # Exact keyword match
            if word in keywords:
                score += 3
            # Partial keyword match
            elif any(word in kw for kw in keywords):
                score += 1
            # Description match
            if word in description:
                score += 1
            # Topic name match
            if word in topic_name:
                score += 2

        if score > 0:
            scored.append((topic_name, score, topic_data))

    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:3]

    if not top:
        return f"No matching topics for '{query}'. Use list_topics() to see available topics."

    results = []
    for name, score, data in top:
        files_str = ", ".join(data.get("files", [])[:5])
        results.append(
            f"Topic: {name} (score={score})\n"
            f"  Description: {data.get('description', '')}\n"
            f"  Files: {files_str}"
        )
    return "\n\n".join(results)


def tool_list_topics() -> str:
    """List all available knowledge topics."""
    index = _get_index()
    topics = index.get("topics", {})

    if not topics:
        return "No topics in knowledge index."

    lines = []
    for name, data in sorted(topics.items()):
        file_count = len(data.get("files", []))
        lines.append(f"- {name}: {data.get('description', '')} ({file_count} files)")
    return "\n".join(lines)


def _handle_tool_call(name: str, arguments: dict) -> str:
    """Route tool calls to local functions."""
    if name == "read_file":
        return tool_read_file(arguments.get("path", ""), arguments.get("section", ""))
    elif name == "search_knowledge":
        return tool_search_knowledge(arguments.get("query", ""))
    elif name == "list_topics":
        return tool_list_topics()
    else:
        return f"Unknown tool: {name}"


# --- Tier 1 System Prompt (always loaded) ---

def _build_system_prompt() -> str:
    """Build system prompt from Tier 1 files (always loaded, ~8K tokens)."""
    parts = [
        "Du bist Samuels persoenlicher Coach-Agent. Du kennst seine Arbeitsweise, "
        "ADHS-Muster, Staerken und Schwaechen aus seiner Wissensbasis.\n\n"
        "Du hast Tools um in seiner Wissensbasis zu suchen und Dateien zu lesen. "
        "Nutze sie um dein Feedback zu personalisieren.\n\n"
        "REGELN:\n"
        "- Antworte auf Deutsch, 2-4 Saetze, konkret und actionable\n"
        "- Bezieh dich auf Samuels bekannte Muster (ADHS, Scope Creep, Session-Sprawl)\n"
        "- Wenn du unsicher bist, nutze search_knowledge() oder read_file()\n"
        "- Kein Smalltalk, kein Lob ohne Grund\n"
        "- Wenn alles gut laeuft: antworte mit genau 'OK'\n"
    ]

    # Load Tier 1 files inline
    tier1_files = [
        ("samuel-kontext.md", "Samuels Profil (Kurzfassung):"),
        ("coaching_rules.txt", "Arbeitsregeln:"),
    ]

    for filename, header in tier1_files:
        path = os.path.join(_KNOWLEDGE_DIR, filename)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    content = f.read()
                if len(content) > 3000:
                    content = content[:3000] + "\n[...]"
                parts.append(f"\n{header}\n{content}")
            except Exception:
                pass

    return "\n".join(parts)


# --- Deep Judge Budget ---

class DeepBudget:
    """Separate budget for Deep Judge. Cap: $0.03/session."""

    def __init__(self, session_cap: float = 0.03):
        self.session_cap = session_cap
        self._sessions: dict[str, float] = {}  # session_id -> spent
        self._total_spent = 0.0
        self._total_calls = 0

    def can_spend(self, session_id: str) -> bool:
        spent = self._sessions.get(session_id, 0.0)
        return spent < self.session_cap

    def record(self, session_id: str, input_tokens: int = 6000, output_tokens: int = 300):
        """Record estimated cost. MiniMax M2.5: ~$0.001/1K input, ~$0.002/1K output."""
        cost = (input_tokens / 1000) * 0.001 + (output_tokens / 1000) * 0.002
        self._sessions[session_id] = self._sessions.get(session_id, 0.0) + cost
        self._total_spent += cost
        self._total_calls += 1

    def status(self) -> dict:
        return {
            "total_spent": round(self._total_spent, 6),
            "total_calls": self._total_calls,
            "session_cap": self.session_cap,
            "active_sessions": len(self._sessions),
        }


# --- Deep Judge Agent ---

class DeepJudge:
    """Autonomer Judge-Agent mit Wissensbasis-Navigation."""

    def __init__(self):
        self.enabled = False
        self.budget = DeepBudget()
        self._api_key = ""
        self._system_prompt = ""
        self._cached_results: dict[str, dict] = {}  # session_id -> {result, ts}
        self._pending: set[str] = set()  # session_ids currently being evaluated
        self._cache_ttl = 180  # seconds

        # Check for API key
        self._api_key = self._find_api_key()
        if not self._api_key:
            _log("Deep Judge disabled: no MINIMAX_API_KEY")
            return

        # Check for knowledge directory
        if not os.path.isdir(_KNOWLEDGE_DIR):
            _log(f"Deep Judge disabled: {_KNOWLEDGE_DIR} not found")
            return

        # Build system prompt
        self._system_prompt = _build_system_prompt()
        if not self._system_prompt:
            _log("Deep Judge disabled: empty system prompt")
            return

        self.enabled = True
        _log("Deep Judge enabled")

    def _find_api_key(self) -> str:
        key = os.environ.get("MINIMAX_API_KEY", "")
        if not key:
            for path in ["~/.config/minimax-key", "~/.minimax-key"]:
                expanded = os.path.expanduser(path)
                if os.path.exists(expanded):
                    try:
                        with open(expanded) as f:
                            key = f.read().strip()
                    except Exception:
                        pass
                    if key:
                        break
        return key

    def _build_user_prompt(self, session_ctx: dict, trigger: str) -> str:
        """Build user prompt from session context."""
        phase = session_ctx.get("phase", "unknown")
        total_calls = session_ctx.get("total_calls", 0)
        history = session_ctx.get("history", [])

        recent = history[-8:] if history else []
        tool_summary = "\n".join(
            f"  {e.get('summary', e.get('tool', '?'))}" for e in recent
        )

        prompt = session_ctx.get("prompt", "")
        prompt_excerpt = prompt[:200] if prompt else ""

        parts = [
            f"Trigger: {trigger}",
            f"Phase: {phase} | Turn: {total_calls}",
        ]
        if tool_summary:
            parts.append(f"Letzte Tools:\n{tool_summary}")
        if prompt_excerpt:
            parts.append(f"Aktueller Prompt: {prompt_excerpt}")
        parts.append(
            "\nAnalysiere den Session-Kontext. Nutze deine Tools um in Samuels "
            "Wissensbasis relevante Muster nachzuschlagen. Gib personalisiertes Feedback."
        )
        return "\n".join(parts)

    def evaluate_async(self, session_id: str, session_ctx: dict, trigger: str,
                       loop: asyncio.AbstractEventLoop | None = None):
        """Start async evaluation. Result available via get_cached_result()."""
        if not self.enabled:
            return
        if not self.budget.can_spend(session_id):
            _log(f"Deep Judge budget exhausted for session {session_id[:8]}")
            return
        if session_id in self._pending:
            _log(f"Deep Judge already running for session {session_id[:8]}")
            return

        self._pending.add(session_id)

        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                _log("No event loop for Deep Judge async evaluation")
                self._pending.discard(session_id)
                return

        loop.create_task(self._evaluate(session_id, session_ctx, trigger))

    async def _evaluate(self, session_id: str, session_ctx: dict, trigger: str):
        """Run the agent loop in background."""
        start = time.monotonic()
        try:
            user_prompt = self._build_user_prompt(session_ctx, trigger)

            # Import here to avoid circular imports
            from llm_providers.minimax import call_minimax_agent, KNOWLEDGE_TOOLS

            # Run the blocking agent call in a thread
            result = await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: call_minimax_agent(
                    system_prompt=self._system_prompt,
                    user_prompt=user_prompt,
                    api_key=self._api_key,
                    tools=KNOWLEDGE_TOOLS,
                    tool_handler=_handle_tool_call,
                    max_rounds=3,
                    timeout=15.0,
                )
            )

            elapsed = time.monotonic() - start
            self.budget.record(session_id)

            if result and result.strip().upper() != "OK":
                self._cached_results[session_id] = {
                    "result": result,
                    "ts": time.time(),
                    "trigger": trigger,
                    "elapsed": round(elapsed, 1),
                }
                _log(f"Deep Judge result for {session_id[:8]} ({elapsed:.1f}s): {result[:80]}")
            else:
                _log(f"Deep Judge for {session_id[:8]}: OK ({elapsed:.1f}s)")

        except Exception as e:
            _log(f"Deep Judge error for {session_id[:8]}: {e}")
        finally:
            self._pending.discard(session_id)

    def get_cached_result(self, session_id: str) -> str | None:
        """Get and consume cached result for a session."""
        entry = self._cached_results.pop(session_id, None)
        if entry is None:
            return None
        # Check TTL
        if time.time() - entry["ts"] > self._cache_ttl:
            _log(f"Deep Judge result expired for {session_id[:8]}")
            return None
        return entry["result"]

    def should_trigger(self, session_ctx: dict, concern_score: int = 0,
                       phase_changed: bool = False) -> str | None:
        """Decide if Deep Judge should run. Returns trigger reason or None."""
        total_calls = session_ctx.get("total_calls", 0)

        # Priority 1: High concern score (multiple detectors fired)
        if concern_score >= 3:
            return f"high_concern_score={concern_score}"

        # Priority 2: Phase change
        if phase_changed:
            return "phase_change"

        # Priority 3: Every ~15 turns
        if total_calls > 0 and total_calls % 15 == 0:
            return f"periodic_turn={total_calls}"

        # Priority 4: Session start (first 3 turns)
        if total_calls <= 3:
            return f"session_start_turn={total_calls}"

        return None

    def status(self) -> dict:
        return {
            "enabled": self.enabled,
            "budget": self.budget.status(),
            "cached_results": len(self._cached_results),
            "pending": len(self._pending),
            "cache_ttl": self._cache_ttl,
        }


# --- Smoke Test ---

if __name__ == "__main__":
    print("=== Deep Judge Smoke Test ===\n")

    judge = DeepJudge()
    print(f"Enabled: {judge.enabled}")
    print(f"Status: {json.dumps(judge.status(), indent=2)}")

    # Test knowledge tools
    print("\n--- Tool: list_topics ---")
    print(tool_list_topics())

    print("\n--- Tool: search_knowledge('adhs session') ---")
    print(tool_search_knowledge("adhs session"))

    print("\n--- Tool: read_file('coaching_rules.txt') ---")
    result = tool_read_file("coaching_rules.txt")
    print(result[:200] + "..." if len(result) > 200 else result)

    # Test trigger logic
    print("\n--- Trigger Logic ---")
    ctx = {"total_calls": 0, "phase": "exploration", "history": []}
    print(f"Turn 0: {judge.should_trigger(ctx)}")
    ctx["total_calls"] = 5
    print(f"Turn 5: {judge.should_trigger(ctx)}")
    ctx["total_calls"] = 15
    print(f"Turn 15: {judge.should_trigger(ctx)}")
    print(f"High score: {judge.should_trigger(ctx, concern_score=4)}")
    print(f"Phase change: {judge.should_trigger(ctx, phase_changed=True)}")

    if judge.enabled:
        print("\n--- Live Agent Test (async) ---")
        async def test():
            ctx = {
                "phase": "implementation",
                "total_calls": 12,
                "history": [
                    {"tool": "Read", "summary": "[Read] sidecar.py"},
                    {"tool": "Read", "summary": "[Read] sidecar.py"},
                    {"tool": "Read", "summary": "[Read] sidecar.py"},
                    {"tool": "Read", "summary": "[Read] sidecar.py"},
                    {"tool": "Edit", "summary": "[Edit] judge_agent.py"},
                ],
                "prompt": "Implement the deep judge feature",
            }
            judge.evaluate_async("test-session-001", ctx, "smoke_test")
            # Wait for result
            for _ in range(20):
                await asyncio.sleep(1)
                result = judge.get_cached_result("test-session-001")
                if result:
                    print(f"Result: {result}")
                    break
            else:
                print("No result after 20s (timeout or OK response)")
        asyncio.run(test())
    else:
        print("\nDeep Judge disabled — set MINIMAX_API_KEY to test live agent loop")
