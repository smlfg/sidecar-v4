#!/usr/bin/env python3
"""Status Tab — Daemon status overview with key-value grid."""

import shutil
import subprocess

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "Projekte" / "ClaudeCodePanel"))
from theme import get_palette


class StatusTab(Gtk.Box):
    """Daemon status display with key-value pairs."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_margin_top(12)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self._fields: dict[str, Gtk.Label] = {}
        self._session_fields: dict[str, Gtk.Label] = {}
        self._status_dot = None
        self._stack = None

        self._build_ui()

    def _build_ui(self):
        p = get_palette()

        # Connection status header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self._status_dot = Gtk.Label()
        self._status_dot.set_markup(f'<span foreground="{p["dim"]}">●</span>')
        header_box.pack_start(self._status_dot, False, False, 0)

        header_lbl = Gtk.Label()
        header_lbl.set_markup(f'<b>Daemon Status</b>')
        header_lbl.get_style_context().add_class("section-title")
        header_box.pack_start(header_lbl, False, False, 0)
        self.pack_start(header_box, False, False, 0)

        # Stack: "daemon" view and "session" view
        self._stack = Gtk.Stack()
        self._stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self._stack.set_transition_duration(150)

        # --- Daemon grid (child "daemon") ---
        daemon_grid = Gtk.Grid()
        daemon_grid.set_column_spacing(16)
        daemon_grid.set_row_spacing(6)
        daemon_grid.set_margin_top(8)
        daemon_grid.get_style_context().add_class("base-card")

        daemon_fields = [
            ("status", "Status"),
            ("pid", "PID"),
            ("uptime", "Uptime"),
            ("rule_count", "Rules"),
            ("total_findings", "Findings"),
            ("plugins", "Plugins"),
            ("patterns", "Patterns"),
            ("skill_triggers", "Skills"),
            ("judge", "Judge"),
            ("judge_evals", "Judge Evals"),
            ("judge_budget", "Judge Budget"),
        ]

        for row, (key, label_text) in enumerate(daemon_fields):
            key_lbl = Gtk.Label(label=label_text)
            key_lbl.set_xalign(0)
            key_lbl.set_markup(
                f'<span foreground="{p["overlay"]}">{label_text}</span>'
            )
            daemon_grid.attach(key_lbl, 0, row, 1, 1)

            val_lbl = Gtk.Label(label="--")
            val_lbl.set_xalign(0)
            val_lbl.get_style_context().add_class("monitor-value")
            daemon_grid.attach(val_lbl, 1, row, 1, 1)
            self._fields[key] = val_lbl

        self._stack.add_named(daemon_grid, "daemon")

        # --- Session grid (child "session") ---
        session_grid = Gtk.Grid()
        session_grid.set_column_spacing(16)
        session_grid.set_row_spacing(6)
        session_grid.set_margin_top(8)
        session_grid.get_style_context().add_class("base-card")

        session_fields = [
            ("session_id", "Session ID"),
            ("project", "Project"),
            ("phase", "Phase"),
            ("total_calls", "Total Calls"),
            ("files_touched", "Files Touched"),
            ("recap_done", "Recap Done"),
            ("history_length", "History Length"),
            ("started", "Started"),
        ]

        for row, (key, label_text) in enumerate(session_fields):
            key_lbl = Gtk.Label(label=label_text)
            key_lbl.set_xalign(0)
            key_lbl.set_markup(
                f'<span foreground="{p["overlay"]}">{label_text}</span>'
            )
            session_grid.attach(key_lbl, 0, row, 1, 1)

            val_lbl = Gtk.Label(label="--")
            val_lbl.set_xalign(0)
            val_lbl.get_style_context().add_class("monitor-value")
            session_grid.attach(val_lbl, 1, row, 1, 1)
            self._session_fields[key] = val_lbl

        self._stack.add_named(session_grid, "session")

        self.pack_start(self._stack, False, False, 0)

        # Action buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        btn_box.set_margin_top(12)

        stop_btn = Gtk.Button(label="Stop Daemon")
        stop_btn.connect("clicked", self._on_stop)
        btn_box.pack_start(stop_btn, False, False, 0)

        log_btn = Gtk.Button(label="View Log")
        log_btn.connect("clicked", self._on_view_log)
        btn_box.pack_start(log_btn, False, False, 0)

        self.pack_start(btn_box, False, False, 0)

    def _on_stop(self, _btn):
        try:
            subprocess.Popen(["systemctl", "--user", "stop", "sidecar"])
        except FileNotFoundError:
            self._show_error("systemctl not found")
        except OSError as e:
            self._show_error(str(e))

    def _on_view_log(self, _btn):
        log_path = "/tmp/claude-sidecar.log"
        terminals = ["cosmic-term", "kitty", "xterm", "gnome-terminal"]
        for term in terminals:
            if shutil.which(term):
                try:
                    subprocess.Popen([term, "--", "tail", "-f", log_path])
                    return
                except OSError:
                    continue
        self._show_error("No terminal emulator found")

    def _show_error(self, msg: str) -> None:
        """Show error in status field."""
        p = get_palette()
        self._fields["status"].set_markup(
            f'<span foreground="{p["red"]}" font_family="monospace">{msg}</span>'
        )

    def update(self, data: dict) -> None:
        """Update status display from daemon response."""
        p = get_palette()

        self._stack.set_visible_child_name("daemon")

        status = data.get("status", "unknown")
        color = p["green"] if status == "running" else p["red"]
        self._status_dot.set_markup(f'<span foreground="{color}">●</span>')

        self._fields["status"].set_markup(
            f'<span foreground="{color}" font_family="monospace">{status}</span>'
        )

        for key in ("pid", "rule_count", "total_findings", "plugins", "patterns", "skill_triggers"):
            val = data.get(key, "--")
            if key in self._fields:
                self._fields[key].set_text(str(val))

        # Judge status
        judge_data = data.get("llm_judge", {})
        if judge_data and "judge" in self._fields:
            judge_enabled = judge_data.get("enabled", False)
            judge_provider = judge_data.get("provider", "?")
            judge_color = p["green"] if judge_enabled else p["dim"]
            judge_label = f"{judge_provider}" if judge_enabled else "disabled"
            self._fields["judge"].set_markup(
                f'<span foreground="{judge_color}" font_family="monospace">{judge_label}</span>'
            )

            budget = judge_data.get("budget", {})
            evals = budget.get("calls", 0)
            self._fields["judge_evals"].set_text(f"{evals} calls")

            spent = budget.get("spent", 0)
            limit = budget.get("limit", 0)
            pct = budget.get("pct", 0)
            budget_color = p["green"] if pct < 60 else (p["yellow"] if pct < 90 else p["red"])
            self._fields["judge_budget"].set_markup(
                f'<span foreground="{budget_color}" font_family="monospace">'
                f'${spent:.4f} / ${limit:.2f} ({pct:.0f}%)</span>'
            )

        # Format uptime
        uptime_s = data.get("uptime_s", 0)
        if uptime_s:
            mins, secs = divmod(int(uptime_s), 60)
            hrs, mins = divmod(mins, 60)
            self._fields["uptime"].set_text(f"{hrs}h {mins}m {secs}s")
        else:
            self._fields["uptime"].set_text("--")

    def update_session(self, data: dict) -> None:
        """Update session detail view with honest session-specific data."""
        import time as _time

        p = get_palette()

        self._status_dot.set_markup(f'<span foreground="{p["accent"]}">●</span>')

        session_id = data.get("session_id", "?")
        self._session_fields["session_id"].set_markup(
            f'<span font_family="monospace">{session_id}</span>'
        )

        project = data.get("project_name") or "--"
        self._session_fields["project"].set_text(project)

        phase = data.get("phase", "unknown")
        phase_color = p["accent"]
        self._session_fields["phase"].set_markup(
            f'<span foreground="{phase_color}" font_family="monospace">{phase}</span>'
        )

        total_calls = data.get("total_calls", 0)
        self._session_fields["total_calls"].set_text(str(total_calls))

        files_touched = data.get("files_touched", [])
        self._session_fields["files_touched"].set_text(str(len(files_touched)))

        recap_done = data.get("recap_done", False)
        recap_color = p["green"] if recap_done else p["yellow"]
        recap_label = "yes" if recap_done else "no"
        self._session_fields["recap_done"].set_markup(
            f'<span foreground="{recap_color}" font_family="monospace">{recap_label}</span>'
        )

        history = data.get("history", [])
        self._session_fields["history_length"].set_text(str(len(history)))

        start_ts = data.get("session_start_ts", 0)
        if start_ts:
            mins = int((_time.time() - start_ts) / 60)
            self._session_fields["started"].set_text(f"{mins} min ago")
        else:
            self._session_fields["started"].set_text("--")

        self._stack.set_visible_child_name("session")

    def show_disconnected(self) -> None:
        """Show disconnected state."""
        p = get_palette()
        self._stack.set_visible_child_name("daemon")
        self._status_dot.set_markup(f'<span foreground="{p["red"]}">●</span>')
        self._fields["status"].set_markup(
            f'<span foreground="{p["red"]}" font_family="monospace">disconnected</span>'
        )
        for key in ("pid", "uptime", "rule_count", "total_findings", "plugins", "patterns", "skill_triggers", "judge", "judge_evals", "judge_budget"):
            if key in self._fields:
                self._fields[key].set_text("--")
