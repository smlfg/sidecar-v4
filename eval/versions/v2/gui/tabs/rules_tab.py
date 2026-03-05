#!/usr/bin/env python3
"""Rules Tab — ListBox with search filter and enable/disable/snooze controls."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "Projekte" / "ClaudeCodePanel"))
from theme import get_palette


class RulesTab(Gtk.Box):
    """Rules list with filter and action buttons."""

    def __init__(self, on_action_callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_margin_top(8)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self._on_action = on_action_callback
        self._rules_data: list[dict] = []
        self._filter_text = ""
        self._selected_rule: str | None = None

        self._build_ui()

    def _build_ui(self):
        p = get_palette()

        # Search bar
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.get_style_context().add_class("base-toolbar")

        self._search = Gtk.SearchEntry()
        self._search.set_placeholder_text("Filter rules...")
        self._search.connect("search-changed", self._on_filter_changed)
        toolbar.pack_start(self._search, True, True, 0)

        self.pack_start(toolbar, False, False, 0)

        # Scrolled list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)

        self._listbox = Gtk.ListBox()
        self._listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self._listbox.connect("row-selected", self._on_row_selected)
        scrolled.add(self._listbox)
        self.pack_start(scrolled, True, True, 0)

        # Action buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_box.set_margin_top(4)

        self._btn_enable = Gtk.Button(label="Enable")
        self._btn_enable.get_style_context().add_class("shortcut-btn")
        self._btn_enable.set_sensitive(False)
        self._btn_enable.connect("clicked", lambda _: self._do_action("enable"))
        btn_box.pack_start(self._btn_enable, False, False, 0)

        self._btn_disable = Gtk.Button(label="Disable")
        self._btn_disable.get_style_context().add_class("shortcut-btn")
        self._btn_disable.set_sensitive(False)
        self._btn_disable.connect("clicked", lambda _: self._do_action("disable"))
        btn_box.pack_start(self._btn_disable, False, False, 0)

        self._btn_snooze = Gtk.Button(label="Snooze 30m")
        self._btn_snooze.get_style_context().add_class("shortcut-btn")
        self._btn_snooze.set_sensitive(False)
        self._btn_snooze.connect("clicked", lambda _: self._do_action("snooze"))
        btn_box.pack_start(self._btn_snooze, False, False, 0)

        self.pack_start(btn_box, False, False, 0)

    def update(self, data: dict) -> None:
        """Update rules list from daemon response."""
        self._rules_data = data.get("rules", [])
        self._rebuild_list()

    def _rebuild_list(self):
        """Rebuild the ListBox rows from current data + filter."""
        p = get_palette()

        # Remove old rows
        for child in self._listbox.get_children():
            self._listbox.remove(child)

        for rule in self._rules_data:
            name = rule.get("name", "")
            if self._filter_text and self._filter_text.lower() not in name.lower():
                group = rule.get("group", "")
                if self._filter_text.lower() not in group.lower():
                    continue

            row = Gtk.ListBoxRow()
            row._rule_name = name

            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            hbox.set_margin_top(4)
            hbox.set_margin_bottom(4)
            hbox.set_margin_start(6)
            hbox.set_margin_end(6)

            # Name (monospace)
            name_lbl = Gtk.Label()
            name_lbl.set_markup(f'<tt>{GLib.markup_escape_text(name)}</tt>')
            name_lbl.set_xalign(0)
            name_lbl.set_width_chars(22)
            hbox.pack_start(name_lbl, False, False, 0)

            # Group badge
            group = rule.get("group", "")
            group_lbl = Gtk.Label()
            group_lbl.set_markup(
                f'<span foreground="{p["overlay"]}" size="small">{GLib.markup_escape_text(group)}</span>'
            )
            group_lbl.set_width_chars(12)
            group_lbl.set_xalign(0)
            hbox.pack_start(group_lbl, False, False, 0)

            # Enabled status
            enabled = rule.get("enabled", True)
            snoozed = rule.get("snoozed", False)
            if snoozed:
                status_text = "Snoozed"
                css_cls = "base-badge-warn"
            elif enabled:
                status_text = "On"
                css_cls = "base-badge-ok"
            else:
                status_text = "Off"
                css_cls = "base-badge-error"

            status_lbl = Gtk.Label(label=status_text)
            status_lbl.get_style_context().add_class("base-badge")
            status_lbl.get_style_context().add_class(css_cls)
            hbox.pack_start(status_lbl, False, False, 0)

            # Fire count
            fires = rule.get("fires", 0)
            fires_lbl = Gtk.Label()
            fires_lbl.set_markup(
                f'<span foreground="{p["dim"]}" size="small">{fires}x</span>'
            )
            fires_lbl.set_halign(Gtk.Align.END)
            hbox.pack_end(fires_lbl, False, False, 0)

            row.add(hbox)
            self._listbox.add(row)

        self._listbox.show_all()

    def _on_filter_changed(self, entry):
        self._filter_text = entry.get_text()
        self._rebuild_list()

    def _on_row_selected(self, listbox, row):
        if row and hasattr(row, "_rule_name"):
            self._selected_rule = row._rule_name
            self._btn_enable.set_sensitive(True)
            self._btn_disable.set_sensitive(True)
            self._btn_snooze.set_sensitive(True)
        else:
            self._selected_rule = None
            self._btn_enable.set_sensitive(False)
            self._btn_disable.set_sensitive(False)
            self._btn_snooze.set_sensitive(False)

    def _do_action(self, action: str):
        if not self._selected_rule or not self._on_action:
            return
        self._on_action(action, self._selected_rule)
