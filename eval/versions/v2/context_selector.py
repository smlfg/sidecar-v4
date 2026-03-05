#!/usr/bin/env python3
"""ContextSelector — Sidecar v2.0 targeted context injection.

Replaces bulk-loading ~900 lines of context with ~20 focused lines
based on current session phase, tool history, and prompt intent.

Runs on every UserPromptSubmit — must be fast, no file I/O at selection time.
"""

import time

# ---------------------------------------------------------------------------
# Phase → context mapping (all in-memory constants)
# ---------------------------------------------------------------------------

PHASE_CONTEXTS: dict[str, dict] = {
    "exploration": {
        "rules": [
            "RESEARCH FIRST: Gemini MCP ($0.10) vor WebSearch. /research Skill nutzen.",
            "EXPLORE: /explore-first fuer parallele Codebase-Erkundung.",
            "Context beats convention: Codebase LESEN, nicht Defaults annehmen.",
        ],
        "intent_keywords": ["research", "gemini", "exploration", "explore", "read", "understand"],
    },
    "implementation": {
        "rules": [
            "DELEGATION: Opus orchestriert, Sonnet implementiert. OpenCode MCP (~$3) oder /chef.",
            "CLI FIRST: Shell ($0) vor MCP wenn kein LLM noetig.",
            "SCOPE: Keine Aenderungen ausserhalb des Requests. Samuel entscheidet.",
            "INTENT FIRST: Subjektive Entscheidungen (Design, Naming, UX) → Samuel fragen.",
        ],
        "intent_keywords": ["delegation", "implement", "build", "create", "refactor", "architecture"],
    },
    "testing": {
        "rules": [
            "TEST: /cli test ($0) oder /test Skill. ISTQB-Klassifikation.",
            "Nach JEDEM Fix: Wo gilt das gleiche Prinzip noch?",
            "Keine Edits ohne Tests. postwrite_test_runner Hook aktiv.",
        ],
        "intent_keywords": ["testing", "test", "quality", "verify", "validate"],
    },
    "debugging": {
        "rules": [
            "DEBUG: /debug-loop Skill (max 5 Iterationen). Hypothesengetrieben.",
            "Error Messages LESEN — sie sagen meist genau was falsch ist.",
            "MCP-Fehler MELDEN, nicht still selbst machen.",
            "Kein Brute-Force: Alternative Ansaetze statt Retry-Loop.",
        ],
        "intent_keywords": ["debugging", "debug", "errors", "fix", "broken"],
    },
}

# Intent keywords that map to a phase regardless of PhaseTracker
INTENT_PHASE_OVERRIDE: dict[str, str] = {
    "debug": "debugging",
    "fix": "debugging",
    "fehler": "debugging",
    "kaputt": "debugging",
    "error": "debugging",
    "test": "testing",
    "pytest": "testing",
    "verify": "testing",
    "build": "implementation",
    "implement": "implementation",
    "create": "implementation",
    "schreib": "implementation",
    "explore": "exploration",
    "research": "exploration",
    "recherche": "exploration",
    "understand": "exploration",
}

# Anti-pattern detection thresholds
STALL_READ_THRESHOLD = 5       # reads without edit/write
ERROR_LOOP_THRESHOLD = 3       # same tool errors in a row
COMMIT_GAP_THRESHOLD = 20      # calls without a git commit
MCP_WITHOUT_CLI_TOOLS = {"mcp__opencode__run", "mcp__gemini__ask-gemini", "WebFetch", "WebSearch"}
CLI_TOOLS = {"Bash"}


def _log(msg: str) -> None:
    try:
        with open("/tmp/claude-sidecar.log", "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [context_selector] {msg}\n")
    except Exception:
        pass


class ContextSelector:
    """Selects targeted context lines based on phase, history, and prompt intent."""

    def __init__(self, phase_tracker=None):
        """phase_tracker: PhaseTracker instance for current phase."""
        self.phase_tracker = phase_tracker

    def select(self, prompt: str, tool_history: list, phase: str = None) -> str:
        """Select relevant context based on phase + prompt intent.

        Returns a string of max ~20 lines for additionalContext injection.
        tool_history: list of dicts with keys 'tool', 'had_error', optional 'input'.
        """
        # Resolve phase: explicit arg > intent override from prompt > phase_tracker > default
        resolved_phase = phase
        if not resolved_phase:
            resolved_phase = self._detect_intent_phase(prompt)
        if not resolved_phase and self.phase_tracker:
            resolved_phase = self.phase_tracker.current_phase
        if not resolved_phase:
            resolved_phase = "exploration"

        lines: list[str] = []

        # Phase context
        phase_lines = self._get_phase_context(resolved_phase)
        lines.extend(phase_lines)

        # History-derived hints
        history_lines = self._get_history_context(tool_history)
        lines.extend(history_lines)

        # Anti-pattern warnings
        warning_lines = self._get_anti_pattern_warnings(tool_history)
        lines.extend(warning_lines)

        # Build output — hard cap at 20 lines / ~500 chars
        output_lines = lines[:20]
        header = f"[SIDECAR-CONTEXT] Phase: {resolved_phase}"
        body = "\n".join(f"- {l}" for l in output_lines)
        result = f"{header}\n{body}"

        # Truncate to ~500 chars to stay within budget
        if len(result) > 500:
            result = result[:497] + "..."

        _log(f"select() phase={resolved_phase} rules={len(phase_lines)} "
             f"history={len(history_lines)} warnings={len(warning_lines)}")

        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _detect_intent_phase(self, prompt: str) -> str | None:
        """Check if prompt keywords directly override the phase."""
        lower = prompt.lower()
        for keyword, phase in INTENT_PHASE_OVERRIDE.items():
            if keyword in lower:
                return phase
        return None

    def _extract_intent(self, prompt: str) -> list[str]:
        """Extract intent keywords from user prompt."""
        lower = prompt.lower()
        found = []
        for phase_data in PHASE_CONTEXTS.values():
            for kw in phase_data["intent_keywords"]:
                if kw in lower and kw not in found:
                    found.append(kw)
        return found

    def _get_phase_context(self, phase: str) -> list[str]:
        """Get context lines for a given phase."""
        data = PHASE_CONTEXTS.get(phase)
        if not data:
            _log(f"Unknown phase '{phase}', falling back to exploration")
            data = PHASE_CONTEXTS["exploration"]
        return list(data["rules"])

    def _get_history_context(self, tool_history: list) -> list[str]:
        """Derive additional hints from recent tool history patterns."""
        if not tool_history:
            return []

        lines = []
        recent = tool_history[-10:]
        tools_used = [e.get("tool", "") for e in recent]

        # Bash usage without test commands → nudge toward verification
        bash_calls = [e for e in recent if e.get("tool") == "Bash"]
        if len(bash_calls) >= 3:
            cmds = " ".join(e.get("input", {}).get("command", "") for e in bash_calls).lower()
            if not any(t in cmds for t in ["test", "pytest", "check"]):
                lines.append("VERIFY: Bash-Calls ohne Tests. /test oder pytest ausfuehren?")

        # Multiple Write/Edit calls → suggest checkpoint
        write_calls = sum(1 for t in tools_used if t in {"Edit", "Write"})
        if write_calls >= 4:
            lines.append("CHECKPOINT: Viele Edits. /checkpoint oder git commit erwaeagen.")

        return lines

    def _get_anti_pattern_warnings(self, tool_history: list) -> list[str]:
        """Check for anti-patterns in recent tool history."""
        if not tool_history:
            return []

        warnings = []
        tools = [e.get("tool", "") for e in tool_history]

        # 1. Stall: 5+ reads without any edit/write
        read_tools = {"Read", "Grep", "Glob", "Agent", "WebSearch", "WebFetch"}
        write_tools = {"Edit", "Write"}

        streak = 0
        for t in reversed(tools):
            if t in write_tools:
                break
            if t in read_tools:
                streak += 1
        if streak >= STALL_READ_THRESHOLD:
            warnings.append(
                f"STALL WARNING: {streak} Reads ohne Action. Plan machen oder /explore-first."
            )

        # 2. Error loop: 3+ errors on the same tool consecutively
        if len(tool_history) >= ERROR_LOOP_THRESHOLD:
            recent = tool_history[-ERROR_LOOP_THRESHOLD:]
            all_same_tool = len({e.get("tool") for e in recent}) == 1
            all_errors = all(e.get("had_error", False) for e in recent)
            if all_same_tool and all_errors:
                tool_name = recent[-1].get("tool", "?")
                warnings.append(
                    f"ERROR LOOP: {ERROR_LOOP_THRESHOLD}x Fehler mit '{tool_name}'. "
                    "Anderen Ansatz waehlen."
                )

        # 3. Long session without commit
        if len(tools) >= COMMIT_GAP_THRESHOLD:
            last_n = tools[-COMMIT_GAP_THRESHOLD:]
            has_commit = any(
                "commit" in tool_history[-(COMMIT_GAP_THRESHOLD - i)].get("input", {}).get("command", "")
                for i, t in enumerate(last_n)
                if t == "Bash"
            )
            if not has_commit:
                warnings.append(
                    f"CHECKPOINT: {len(tools)}+ Calls ohne Commit. /checkpoint erwaeagen."
                )

        # 4. MCP called without prior CLI attempt
        if len(tool_history) >= 2:
            last = tool_history[-1]
            prev = tool_history[-2]
            if last.get("tool") in MCP_WITHOUT_CLI_TOOLS and prev.get("tool") not in CLI_TOOLS:
                warnings.append("CLI FIRST: Shell ($0) zuerst probieren vor MCP-Call.")

        return warnings
