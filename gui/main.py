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


class SidecarApp(BaseApp):
    """Main Sidecar Control Panel application."""

    def __init__(self):
        super().__init__("Sidecar Control Panel", 750, 550, icon_name="preferences-system")

        self._status_tab = StatusTab()
        self._rules_tab = RulesTab(on_action_callback=self._on_rule_action)
        self._findings_tab = FindingsTab()

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

        # Notebook with 3 tabs
        notebook = Gtk.Notebook()
        notebook.append_page(self._status_tab, Gtk.Label(label="Status"))
        notebook.append_page(self._rules_tab, Gtk.Label(label="Rules"))
        notebook.append_page(self._findings_tab, Gtk.Label(label="Findings"))

        self.content_box.pack_start(notebook, True, True, 0)

    def _refresh_all(self) -> bool:
        """Fetch status, rules, and findings from daemon."""
        if not is_daemon_reachable():
            self._status_tab.show_disconnected()
            self.set_status("Disconnected — daemon not running", "status-error")
            return True  # keep timer

        send_command({"cmd": "status"}, self._on_status_response, self._on_error)
        send_command({"cmd": "rules"}, self._on_rules_response, self._on_error)
        send_command({"cmd": "findings"}, self._on_findings_response, self._on_error)
        return True  # keep timer

    def _on_status_response(self, data):
        self._status_tab.update(data)
        status = data.get("status", "unknown")
        rules = data.get("rule_count", 0)
        findings = data.get("total_findings", 0)
        self.set_status(f"Connected — {rules} rules, {findings} findings", "status-saved")

    def _on_rules_response(self, data):
        self._rules_tab.update(data)

    def _on_findings_response(self, data):
        self._findings_tab.update(data)

    def _on_error(self, msg):
        self._status_tab.show_disconnected()
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
            # Refresh rules after action
            send_command({"cmd": "rules"}, self._on_rules_response, self._on_error)

        send_command(cmd, _after_action, self._on_error)


def main():
    app = SidecarApp()
    app.run()


if __name__ == "__main__":
    main()
