#!/usr/bin/env python3
"""Sidecar Control Panel — GTK3 standalone GUI.

Visualizes sidecar daemon status, rules, and findings.
Data source: Unix socket at /tmp/claude-sidecar.sock (JSON protocol).
"""

import sys
from pathlib import Path

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

# Import shared base
sys.path.insert(0, str(Path.home() / "Projekte" / "shared-gui"))
from gui_base import BaseApp

from socket_client import send_command, is_daemon_reachable
from tabs.status_tab import StatusTab
from tabs.rules_tab import RulesTab
from tabs.findings_tab import FindingsTab
from tabs.sessions_tab import SessionsTab
from tabs.context_tab import ContextTab


class SidecarApp(BaseApp):
    """Main Sidecar Control Panel application."""

    def __init__(self):
        super().__init__("Sidecar Control Panel", 750, 550, icon_name="preferences-system")

        self._status_tab = StatusTab()
        self._rules_tab = RulesTab(on_action_callback=self._on_rule_action)
        self._findings_tab = FindingsTab()
        self._sessions_tab = SessionsTab()
        self._context_tab = ContextTab()

        self._notebook = None
        self._findings_label = None
        self._FINDINGS_PAGE = 2  # 0=Status,1=Rules,2=Findings,3=Sessions
        self._refresh_interval = 5
        self._refresh_in_flight = False  # Guard against overlapping requests

        self._build_ui()

        # Initial data load
        GLib.idle_add(self._refresh_all)

        # Auto-refresh every 5 seconds
        self.start_refresh(5, self._refresh_all)

    def _build_ui(self):
        # Reload button in header
        reload_btn = Gtk.Button(label="Reload")
        reload_btn.get_style_context().add_class("shortcut-btn")
        reload_btn.connect("clicked", self._on_reload)
        self.add_header_widget(reload_btn)

        # Notebook with 4 tabs
        self._notebook = Gtk.Notebook()
        self._findings_label = Gtk.Label(label="Findings")
        self._notebook.append_page(self._status_tab, Gtk.Label(label="Status"))
        self._notebook.append_page(self._rules_tab, Gtk.Label(label="Rules"))
        self._notebook.append_page(self._findings_tab, self._findings_label)
        self._notebook.append_page(self._sessions_tab, Gtk.Label(label="Sessions"))
        self._context_label = Gtk.Label(label="Context")
        self._notebook.append_page(self._context_tab, self._context_label)
        self._notebook.connect("switch-page", self._on_tab_switch)

        self.content_box.pack_start(self._notebook, True, True, 0)

    def _refresh_all(self) -> bool:
        """Single dashboard call — one socket connection, no race conditions."""
        if not is_daemon_reachable():
            self._refresh_in_flight = False
            self._status_tab.show_disconnected()
            self.set_status("Disconnected — daemon not running", "status-error")
            return True  # keep timer

        # Skip if previous request hasn't returned yet
        if self._refresh_in_flight:
            return True

        self._refresh_in_flight = True
        send_command({"cmd": "dashboard"}, self._on_dashboard, self._on_dashboard_error)
        return True  # keep timer

    def _on_dashboard(self, data):
        """Handle combined dashboard response — update all tabs at once."""
        self._refresh_in_flight = False

        # Status
        status_data = data.get("status", {})
        self._status_tab.update(status_data)
        rules = status_data.get("rule_count", 0)
        findings = status_data.get("total_findings", 0)
        self.set_status(f"Connected — {rules} rules, {findings} findings", "status-saved")

        # Rules
        self._rules_tab.update({"rules": data.get("rules", [])})

        # Findings
        self._findings_tab.update({"findings": data.get("findings", [])})
        if self._findings_tab.had_new_findings:
            self._findings_label.set_markup('<b>Findings</b> <span foreground="#a6e3a1">●</span>')
            GLib.timeout_add(3000, self._reset_findings_label)
        else:
            self._reset_findings_label()

        # Sessions
        self._sessions_tab.update({"sessions": data.get("sessions", [])})

        # Context (injections)
        self._context_tab.update({"injections": data.get("injections", [])})

    def _on_dashboard_error(self, msg):
        """Dashboard failed — show disconnected. No flicker: guard prevents overlap."""
        self._refresh_in_flight = False
        self._status_tab.show_disconnected()
        self.set_status(f"Error: {msg}", "status-error")

    def _reset_findings_label(self) -> bool:
        self._findings_label.set_text("Findings")
        return False  # one-shot

    def _on_tab_switch(self, _notebook, _page, page_num):
        """Speed up polling when Findings tab is active."""
        if page_num == self._FINDINGS_PAGE:
            if self._refresh_interval != 3:
                self._refresh_interval = 3
                self.stop_all_refresh()
                self.start_refresh(3, self._refresh_all)
        else:
            if self._refresh_interval != 5:
                self._refresh_interval = 5
                self.stop_all_refresh()
                self.start_refresh(5, self._refresh_all)

    def _on_error(self, msg):
        """Error handler for one-off commands (reload, rule actions)."""
        self.set_status(f"Error: {msg}", "status-error")

    def _on_reload(self, _btn):
        send_command({"cmd": "reload"}, lambda d: self._refresh_all(), self._on_error)

    def _on_rule_action(self, action: str, rule_name: str):
        """Handle enable/disable/snooze from rules tab."""
        cmd = {"cmd": action, "name": rule_name}
        if action == "snooze":
            cmd["minutes"] = 30

        def _after_action(data):
            msg = data.get("message", f"{action}: {rule_name}")
            self.set_status(msg, "status-saved")
            # Refresh after action
            self._refresh_all()

        send_command(cmd, _after_action, self._on_error)


def main():
    app = SidecarApp()
    app.run()


if __name__ == "__main__":
    main()
