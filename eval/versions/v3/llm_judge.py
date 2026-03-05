#!/usr/bin/env python3
"""LLM Judge — Qualitaetskontrolle der Claude Code Arbeitsweise.

Bewertet ob Claude Code in Line mit Samuels Arbeitsregeln arbeitet.
Nutzt MiniMax M2.5 als guenstiges LLM fuer natuerlichsprachliche
Bewertung statt Keyword-Matching. Fallback: Gemini Flash.

Drei Trigger-Typen:
1. on_detector_fired() — Detektor hat Pattern erkannt, LLM formuliert besseren Hinweis
2. on_turn() — Periodischer Check alle ~6 Turns
3. on_phase_change() — Phasenwechsel-Beratung
"""

import json
import os
import time

_LOG_PATH = "/tmp/claude-sidecar.log"


def _log(msg: str) -> None:
    try:
        with open(_LOG_PATH, "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [llm_judge] {msg}\n")
    except Exception:
        pass


# --- LLM Providers (lazy-loaded from llm_providers/) ---

_provider_fns = {}


def _get_provider(name: str):
    """Lazy-load provider function from llm_providers/."""
    if name not in _provider_fns:
        try:
            if name == "gemini":
                from llm_providers.gemini import call_gemini
                _provider_fns[name] = call_gemini
            elif name == "minimax":
                from llm_providers.minimax import call_minimax
                _provider_fns[name] = call_minimax
            elif name == "ollama":
                from llm_providers.ollama import call_ollama
                _provider_fns[name] = call_ollama
            else:
                return None
        except ImportError as e:
            _log(f"Failed to import provider '{name}': {e}")
            return None
    return _provider_fns.get(name)


# --- Budget Tracker ---

class BudgetTracker:
    """Tracks estimated LLM costs per session. Resets daily."""

    def __init__(self, limit: float = 0.05):
        self.limit = limit
        self.spent = 0.0
        self.call_count = 0
        self._reset_date = time.strftime("%Y-%m-%d")

    def can_spend(self, priority: int) -> bool:
        """Check if budget allows a call. Priority: 1=detector, 2=periodic, 3=phase."""
        self._maybe_reset()
        if priority == 1:
            return self.spent < self.limit  # always if under limit
        if priority == 2:
            return self.spent < self.limit * 0.8  # throttle at 80%
        return self.spent < self.limit * 0.6  # throttle at 60%

    def record(self, input_tokens: int = 2000, output_tokens: int = 100):
        """Record estimated cost. Gemini Flash: ~$0.0001/1K input, ~$0.0004/1K output."""
        cost = (input_tokens / 1000) * 0.0001 + (output_tokens / 1000) * 0.0004
        self.spent += cost
        self.call_count += 1

    def _maybe_reset(self):
        today = time.strftime("%Y-%m-%d")
        if today != self._reset_date:
            self.spent = 0.0
            self.call_count = 0
            self._reset_date = today

    def status(self) -> dict:
        self._maybe_reset()
        return {
            "spent": round(self.spent, 6),
            "limit": self.limit,
            "calls": self.call_count,
            "pct": round(self.spent / self.limit * 100, 1) if self.limit > 0 else 0,
        }


# --- LLM Judge ---

class LLMJudge:
    """LLM-basierte Qualitaetskontrolle der Claude Code Arbeitsweise."""

    def __init__(self, rules_path: str, provider: str = "minimax",
                 budget_limit: float = 0.05):
        self.provider = provider
        self.enabled = False
        self.budget = BudgetTracker(limit=budget_limit)
        self._turn_counter = 0
        self._periodic_interval = 6
        self._last_phase = None
        self._cache: dict[str, float] = {}  # dedup: hash -> timestamp
        self._cache_ttl = 120  # seconds

        # Load system prompt from coaching rules
        self._system_prompt = ""
        try:
            with open(rules_path, "r") as f:
                self._system_prompt = f.read().strip()
        except Exception as e:
            _log(f"Failed to load coaching rules from {rules_path}: {e}")

        # Resolve API key
        self._api_key = self._find_api_key()
        if self._api_key and self._system_prompt:
            self.enabled = True
            _log(f"LLM Judge enabled (provider={provider}, budget=${budget_limit})")
        else:
            reasons = []
            if not self._api_key:
                reasons.append("no API key")
            if not self._system_prompt:
                reasons.append("no coaching rules")
            _log(f"LLM Judge disabled: {', '.join(reasons)}")

    def _find_api_key(self) -> str:
        """Find API key from env vars or config files."""
        if self.provider == "minimax":
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
        elif self.provider == "gemini":
            key = os.environ.get("GOOGLE_API_KEY", "")
            if not key:
                for path in ["~/.config/gemini-key", "~/.gemini-key"]:
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
        return ""

    def _call_llm(self, user_prompt: str) -> str | None:
        """Call the configured LLM provider."""
        call_fn = _get_provider(self.provider)
        if call_fn is None:
            _log(f"No provider function for '{self.provider}'")
            return None
        try:
            return call_fn(self._system_prompt, user_prompt, self._api_key)
        except Exception as e:
            _log(f"Provider '{self.provider}' call failed: {e}")
            return None

    def _is_cached(self, key: str) -> bool:
        """Check if we recently evaluated the same pattern."""
        now = time.time()
        # Clean expired entries
        self._cache = {k: v for k, v in self._cache.items() if now - v < self._cache_ttl}
        return key in self._cache

    def _build_context_prompt(self, session_ctx: dict, extra: str = "") -> str:
        """Build the user prompt from session context."""
        phase = session_ctx.get("phase", "unknown")
        total_calls = session_ctx.get("total_calls", 0)
        history = session_ctx.get("history", [])

        # Last 5 tool calls as summary
        recent = history[-5:] if history else []
        tool_summary = "\n".join(
            f"  {e.get('summary', e.get('tool', '?'))}" for e in recent
        )

        parts = [
            f"Phase: {phase} | Turn: {total_calls}",
        ]
        if tool_summary:
            parts.append(f"Letzte Tools:\n{tool_summary}")
        if extra:
            parts.append(extra)
        return "\n".join(parts)

    def on_detector_fired(self, detector_type: str, hardcoded_msg: str,
                          session_ctx: dict) -> str | None:
        """Detektor hat gefeuert — LLM formuliert kontextbewussten Hinweis.
        Priority 1: always enrich if budget allows."""
        if not self.enabled:
            return None
        if not self.budget.can_spend(priority=1):
            _log("Budget exhausted for detector enrichment")
            return None

        cache_key = f"det:{detector_type}:{session_ctx.get('phase', '')}"
        if self._is_cached(cache_key):
            return None

        extra = f"Detektor '{detector_type}' hat ausgeloest: {hardcoded_msg}"
        prompt = self._build_context_prompt(session_ctx, extra)

        result = self._call_llm(prompt)
        self.budget.record()

        if result and result.strip().upper() != "OK":
            self._cache[cache_key] = time.time()
            _log(f"Judge enriched detector {detector_type}: {result[:80]}")
            return result

        return None

    def on_turn(self, session_ctx: dict) -> str | None:
        """Periodischer Check — auch wenn kein Detektor feuert.
        Priority 2: every ~6 turns, throttled at 80% budget."""
        if not self.enabled:
            return None

        self._turn_counter += 1
        if self._turn_counter % self._periodic_interval != 0:
            return None

        if not self.budget.can_spend(priority=2):
            _log("Budget throttled for periodic check")
            return None

        cache_key = f"periodic:{self._turn_counter // self._periodic_interval}"
        if self._is_cached(cache_key):
            return None

        prompt = self._build_context_prompt(session_ctx, "Periodischer Qualitaets-Check.")
        result = self._call_llm(prompt)
        self.budget.record()

        if result and result.strip().upper() != "OK":
            self._cache[cache_key] = time.time()
            _log(f"Judge periodic: {result[:80]}")
            return result

        return None

    def on_phase_change(self, old_phase: str, new_phase: str,
                        session_ctx: dict) -> str | None:
        """Phase wechselt — Empfehlung fuer neue Phase.
        Priority 3: throttled at 60% budget."""
        if not self.enabled:
            return None
        if not self.budget.can_spend(priority=3):
            return None

        cache_key = f"phase:{old_phase}->{new_phase}"
        if self._is_cached(cache_key):
            return None

        extra = f"Phasenwechsel: {old_phase} -> {new_phase}"
        prompt = self._build_context_prompt(session_ctx, extra)
        result = self._call_llm(prompt)
        self.budget.record()

        if result and result.strip().upper() != "OK":
            self._cache[cache_key] = time.time()
            _log(f"Judge phase change: {result[:80]}")
            return result

        return None

    def status(self) -> dict:
        """Status for sidecar-ctl."""
        return {
            "enabled": self.enabled,
            "provider": self.provider,
            "budget": self.budget.status(),
            "periodic_interval": self._periodic_interval,
            "cache_size": len(self._cache),
        }


# --- Smoke Test ---

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(base_dir, "coaching_rules.txt")
    judge = LLMJudge(rules_path=rules_path)
    print(f"Judge enabled: {judge.enabled}")
    print(f"Provider: {judge.provider}")
    print(f"Status: {json.dumps(judge.status(), indent=2)}")

    if judge.enabled:
        mock_ctx = {
            "phase": "implementation",
            "total_calls": 12,
            "history": [
                {"tool": "Read", "summary": "[Read] sidecar.py"},
                {"tool": "Read", "summary": "[Read] phase_tracker.py"},
                {"tool": "Read", "summary": "[Read] plugin_loader.py"},
                {"tool": "Read", "summary": "[Read] context_selector.py"},
                {"tool": "Read", "summary": "[Read] skill_recommender.py"},
            ],
        }
        print("\n--- Testing on_detector_fired (STALL) ---")
        result = judge.on_detector_fired("STALL", "10 Calls ohne Edit/Write", mock_ctx)
        print(f"Result: {result}")

        print("\n--- Testing on_turn (periodic) ---")
        judge._turn_counter = 5  # force next check
        result = judge.on_turn(mock_ctx)
        print(f"Result: {result}")
    else:
        print("\nJudge disabled — set MINIMAX_API_KEY or ~/.config/minimax-key to test")
