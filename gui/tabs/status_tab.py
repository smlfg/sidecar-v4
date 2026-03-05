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
        self._status_dot = None

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

        # Key-value grid
        grid = Gtk.Grid()
        grid.set_column_spacing(16)
        grid.set_row_spacing(6)
        grid.set_margin_top(8)
        grid.get_style_context().add_class("base-card")

        fields = [
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

        for row, (key, label_text) in enumerate(fields):
            key_lbl = Gtk.Label(label=label_text)
            key_lbl.set_xalign(0)
            key_lbl.set_markup(
                f'<span foreground="{p["overlay"]}">{label_text}</span>'
            )
            grid.attach(key_lbl, 0, row, 1, 1)

            val_lbl = Gtk.Label(label="--")
            val_lbl.set_xalign(0)
            val_lbl.get_style_context().add_class("monitor-value")
            grid.attach(val_lbl, 1, row, 1, 1)
            self._fields[key] = val_lbl

        self.pack_start(grid, False, False, 0)

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
            errors = judge_data.get("error_count", 0) if "error_count" in judge_data else 0
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

    def show_disconnected(self) -> None:
        """Show disconnected state."""
        p = get_palette()
        self._status_dot.set_markup(f'<span foreground="{p["red"]}">●</span>')
        self._fields["status"].set_markup(
            f'<span foreground="{p["red"]}" font_family="monospace">disconnected</span>'
        )
        for key in ("pid", "uptime", "rule_count", "total_findings", "plugins", "patterns", "skill_triggers", "judge", "judge_evals", "judge_budget"):
            if key in self._fields:
                self._fields[key].set_text("--")
