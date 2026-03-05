#!/usr/bin/env python3
"""session_limit — Warn when too many sessions have been started today.

Counts top-level session .jsonl files in ~/.claude/projects/ modified today.
Fires when count >= 5 to encourage longer focused sessions over many short ones.
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rule_plugin import RulePlugin

SESSION_LIMIT = 5
PROJECTS_DIR = Path.home() / ".claude" / "projects"


def _count_sessions_today() -> int:
    """Count top-level session .jsonl files modified today (excludes subagents)."""
    today_start = time.mktime(time.strptime(
        time.strftime("%Y-%m-%d"), "%Y-%m-%d"
    ))
    count = 0
    try:
        for project_dir in PROJECTS_DIR.iterdir():
            if not project_dir.is_dir():
                continue
            for f in project_dir.glob("*.jsonl"):
                if f.stat().st_mtime >= today_start:
                    count += 1
    except Exception:
        return 0
    return count


class SessionLimitRule(RulePlugin):
    name = "session_limit"
    description = "Warns when too many sessions have been started today"

    def match(self, prompt: str, session_state: dict) -> bool:
        # Run on every prompt — only inject when limit is reached
        try:
            return _count_sessions_today() >= SESSION_LIMIT
        except Exception:
            return False  # fail-open: never block on error

    def inject(self) -> str:
        try:
            count = _count_sessions_today()
        except Exception:
            return None
        return (
            f"[SESSION-LIMIT] Du hast heute schon {count} Sessions. "
            "Laengere Sessions > viele kurze. Fokus behalten!"
        )
