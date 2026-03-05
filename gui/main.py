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

from socket_client import send_command
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
        self._sessions_tab = SessionsTab(on_session_selected=self._on_session_selected)
        self._context_tab = ContextTab()

        self._notebook = None
        self._findings_label = None
        self._FINDINGS_PAGE = 2  # 0=Status,1=Rules,2=Findings,3=Sessions
        self._refresh_interval = 5
        self._refresh_in_flight = False  # Guard against overlapping requests

        # Session picker state
        self._session_combo = None
        self._selected_session_id = None  # None = "All"
        self._session_detail_in_flight = False

        self._build_ui()

        # Initial data load
        GLib.idle_add(self._refresh_all)

        # Auto-refresh every 5 seconds
        self.start_refresh(5, self._refresh_all)

    def _build_ui(self):
        # Session picker in header (left side)
        picker_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        picker_label = Gtk.Label(label="Session:")
        picker_box.pack_start(picker_label, False, False, 0)

        self._session_combo = Gtk.ComboBoxText()
        self._session_combo.append("__all__", "All Sessions")
        self._session_combo.set_active_id("__all__")
        self._session_combo.connect("changed", self._on_session_combo_changed)
        picker_box.pack_start(self._session_combo, False, False, 0)
        self.add_header_widget(picker_box, end=False)

        # Reload button in header
        reload_btn = Gtk.Button(label="Reload")
        reload_btn.get_style_context().add_class("shortcut-btn")
        reload_btn.connect("clicked", self._on_reload)
        self.add_header_widget(reload_btn)

        # Notebook with 5 tabs
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
        """Single dashboard call — error callback handles disconnected state."""
        # Skip if previous request hasn't returned yet
        if self._refresh_in_flight:
            return True

        self._refresh_in_flight = True
        send_command({"cmd": "dashboard"}, self._on_dashboard, self._on_dashboard_error)
        return True  # keep timer

    def _on_dashboard(self, data):
        """Handle combined dashboard response — update all tabs at once."""
        self._refresh_in_flight = False

        # Sync session picker
        sessions = data.get("sessions", [])
        self._update_session_combo(sessions)

        # If a specific session is selected, fetch its detail instead of global
        if self._selected_session_id:
            self._fetch_session_detail(self._selected_session_id)
            # Still update global-only tabs (rules, sessions list)
            self._rules_tab.update({"rules": data.get("rules", [])})
            self._sessions_tab.update({"sessions": sessions})

            self._findings_tab.update({"findings": data.get("findings", [])})
            if self._findings_tab.had_new_findings:
                self._findings_label.set_markup('<b>Findings</b> <span foreground="#a6e3a1">●</span>')
                GLib.timeout_add(3000, self._reset_findings_label)
            else:
                self._reset_findings_label()
            return

        # Global view (no session selected)
        # Status
        status_data = data.get("status", {})
        self._status_tab.update(status_data)
        rules = status_data.get("rule_count", 0)
        findings = status_data.get("total_findings", 0)
        self.set_status(f"Connected — {rules} rules, {findings} findings", "status-saved")
        self.set_subtitle("")

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
        self._sessions_tab.update({"sessions": sessions})

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

    def _on_session_combo_changed(self, combo):
        """Session picker changed — fetch detail or go back to global view."""
        active_id = combo.get_active_id()
        if active_id == "__all__" or active_id is None:
            self._selected_session_id = None
            self.set_subtitle("")
            self._session_combo.get_style_context().remove_class("base-badge-ok")
            # Restore global view on next refresh
            self._refresh_all()
        else:
            self._selected_session_id = active_id
            self._session_combo.get_style_context().add_class("base-badge-ok")
            self._fetch_session_detail(active_id)

    def _on_session_selected(self, session_id: str):
        """Called from Sessions tab when a row is double-clicked."""
        # Set the combo to this session
        if self._session_combo.get_active_id() != session_id:
            self._session_combo.set_active_id(session_id)

    def _update_session_combo(self, sessions: list):
        """Sync combo entries with current sessions list."""
        current_id = self._session_combo.get_active_id()
        known_ids = {s.get("id", "") for s in sessions}

        # Build set of existing combo entries
        existing_ids = set()
        model = self._session_combo.get_model()
        if model:
            for row in model:
                existing_ids.add(row[1])  # column 1 = id

        # Add new sessions
        for s in sessions:
            sid = s.get("id", "")
            if sid and sid not in existing_ids:
                project = s.get("project", "–")
                phase = s.get("phase", "")
                label = f"{project} — {phase} ({sid[:8]})"
                self._session_combo.append(sid, label)

        # Remove stale sessions (except __all__)
        if model:
            to_remove = []
            for i, row in enumerate(model):
                rid = row[1]
                if rid != "__all__" and rid not in known_ids:
                    to_remove.append(i)
            for offset, idx in enumerate(to_remove):
                model.remove(model.get_iter_from_string(str(idx - offset)))

        # Restore selection
        if current_id and self._session_combo.get_active_id() != current_id:
            self._session_combo.set_active_id(current_id)

    def _fetch_session_detail(self, session_id: str):
        """Fetch detailed data for a specific session."""
        if self._session_detail_in_flight:
            return
        self._session_detail_in_flight = True
        send_command(
            {"cmd": "session", "id": session_id},
            self._on_session_detail,
            self._on_session_detail_error,
        )

    def _on_session_detail(self, data):
        """Handle session detail response — update tabs with session-specific data."""
        self._session_detail_in_flight = False
        if "error" in data:
            self.set_status(f"Session error: {data['error']}", "status-error")
            return

        sid = data.get("session_id", "?")
        project = data.get("project_name", "")
        phase = data.get("phase", "")
        self.set_subtitle(f"{project} — {phase} — {sid[:8]}")

        # Update context tab with session-specific injections
        self._context_tab.update({"injections": data.get("injection_history", [])})

        # Update status tab with session-specific info
        self._status_tab.update_session(data)

        calls = data.get("total_calls", 0)
        files = len(data.get("files_touched", []))
        self.set_status(f"Session {sid[:8]}: {calls} calls, {files} files, phase={phase}", "status-saved")

    def _on_session_detail_error(self, msg):
        self._session_detail_in_flight = False
        self.set_status(f"Session detail error: {msg}", "status-error")

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
