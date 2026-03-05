#!/usr/bin/env python3
"""SkillRecommender — Dynamic skill suggestions based on prompt + session phase.

Replaces the static 258-line Skilluebersicht.md with max 3 context-aware
recommendations per prompt. Implements RulePlugin so it plugs into the
existing Sidecar plugin system.
"""

import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rule_plugin import RulePlugin


SKILL_CATALOG = [
    {"name": "/research",     "keywords": ["research", "recherche", "investigate", "explore", "understand", "was ist", "how does"], "phases": ["exploration"],                                       "description": "Gemini Research ($0.10)"},
    {"name": "/prior-art",    "keywords": ["prior-art", "existing", "library", "package", "github", "alternative"],                  "phases": ["exploration"],                                       "description": "GitHub Prior Art Search"},
    {"name": "/explore-first","keywords": ["codebase", "structure", "architecture", "wo ist", "find", "suche"],                      "phases": ["exploration"],                                       "description": "Parallel Codebase Exploration"},
    {"name": "/auto",         "keywords": ["implement", "build", "create", "bauen", "erstell", "code", "feature"],                   "phases": ["implementation"],                                    "description": "Smart Auto-Delegation"},
    {"name": "/test",         "keywords": ["test", "verify", "check", "validate", "pytest", "pruefen"],                              "phases": ["testing"],                                           "description": "Cascading Test Pipeline"},
    {"name": "/debug-loop",   "keywords": ["debug", "fix", "error", "bug", "broken", "fehler", "crash"],                            "phases": ["debugging"],                                         "description": "Autonomous Debug Loop (max 5 iter)"},
    {"name": "/review",       "keywords": ["review", "quality", "security", "check code", "pruefe"],                                 "phases": ["testing", "implementation"],                         "description": "Thorough Code Review"},
    {"name": "/commit",       "keywords": ["commit", "save", "checkpoint", "git"],                                                   "phases": ["implementation", "testing"],                         "description": "Smart Git Commit"},
    {"name": "/simplify",     "keywords": ["simplify", "refactor", "clean", "vereinfach", "aufraeum"],                              "phases": ["implementation"],                                    "description": "Code Simplification"},
    {"name": "/control",      "keywords": ["review", "cross-model", "zweitmeinung", "check"],                                        "phases": ["testing"],                                           "description": "Cross-Model Review"},
    {"name": "/focus",        "keywords": ["focus", "ein ziel", "konzentrier", "ablenkung"],                                         "phases": ["exploration", "implementation"],                     "description": "Focus Mode — 1 Goal, 1 Session"},
    {"name": "/recap",        "keywords": ["recap", "zusammenfass", "session end", "fertig", "done"],                               "phases": ["exploration", "implementation", "testing", "debugging"], "description": "Session Summary"},
    {"name": "/learn",        "keywords": ["learn", "explain", "versteh", "erklaer", "was macht"],                                  "phases": ["exploration"],                                       "description": "Post-Session Learning"},
    {"name": "/quickwin",     "keywords": ["stuck", "blocked", "keine ahnung", "anfang", "start", "paralysis"],                     "phases": ["exploration"],                                       "description": "3 Quick Wins gegen Task Paralysis"},
]


def _log(msg: str) -> None:
    try:
        with open("/tmp/claude-sidecar.log", "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [skill_recommender] {msg}\n")
    except Exception:
        pass


class SkillRecommender(RulePlugin):
    name = "skill_recommender"
    description = "Recommends max 3 relevant skills based on prompt + phase"

    def __init__(self):
        self._current_phase = "exploration"
        self._last_recommendations: list[str] = []

    def set_phase(self, phase: str) -> None:
        """Update current phase (called by sidecar before match)."""
        self._current_phase = phase

    def match(self, prompt: str, session_state: dict) -> bool:
        """Rank skills and cache results. Returns True when recommendations exist."""
        self._current_phase = session_state.get("phase", self._current_phase)
        self._last_recommendations = self._rank_skills(prompt)
        result = len(self._last_recommendations) > 0
        _log(
            f"match=>{result} phase={self._current_phase} "
            f"suggestions={[s['name'] for s in self._last_recommendations]}"
        )
        return result

    def inject(self) -> str:
        """Return compact 3-line skill recommendation block."""
        if not self._last_recommendations:
            return ""
        lines = [f"[SKILL-SUGGEST] Phase: {self._current_phase}"]
        for skill in self._last_recommendations:
            lines.append(f"  {skill['name']} — {skill['description']}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _rank_skills(self, prompt: str) -> list:
        """Score every skill; return top 3 with minimum score of 2."""
        lower = prompt.lower()
        scored = []

        for skill in SKILL_CATALOG:
            score = 0

            # +2 per keyword match
            for kw in skill["keywords"]:
                if kw in lower:
                    score += 2

            # +3 if phase matches current session phase
            if self._current_phase in skill["phases"]:
                score += 3

            # +1 variety bonus if skill was NOT in the last recommendations
            if skill["name"] not in self._last_recommendations:
                score += 1

            if score >= 2:
                scored.append((score, skill))

        # Sort descending by score, take top 3
        scored.sort(key=lambda x: x[0], reverse=True)
        return [skill for _, skill in scored[:3]]
