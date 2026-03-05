#!/usr/bin/env python3
"""Sessions Tab — Active Claude sessions overview."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "Projekte" / "ClaudeCodePanel"))
from theme import get_palette

# ListStore column indices
COL_ID = 0
COL_CALLS = 1
COL_FILES = 2
COL_HISTORY = 3


class SessionsTab(Gtk.Box):
    """Active Claude sessions as a sortable TreeView."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_margin_top(8)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self._count_label = None
        self._store = None
        self._build_ui()

    def _build_ui(self):
        p = get_palette()

        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self._count_label = Gtk.Label()
        self._count_label.set_markup(
            f'<b>Sessions</b>  <span foreground="{p["overlay"]}">0 active</span>'
        )
        self._count_label.set_halign(Gtk.Align.START)
        header.pack_start(self._count_label, False, False, 0)
        self.pack_start(header, False, False, 0)

        # ListStore: id, total_calls, files_touched, history_len
        self._store = Gtk.ListStore(str, str, str, str)

        tree = Gtk.TreeView(model=self._store)
        tree.set_headers_visible(True)
        tree.get_style_context().add_class("base-card")

        columns = [
            ("ID", COL_ID),
            ("Calls", COL_CALLS),
            ("Files", COL_FILES),
            ("History", COL_HISTORY),
        ]
        for title, col_idx in columns:
            renderer = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(title, renderer, text=col_idx)
            col.set_resizable(True)
            if col_idx == COL_ID:
                col.set_min_width(90)
            tree.append_column(col)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.add(tree)
        self.pack_start(scrolled, True, True, 0)

    def update(self, data: dict) -> None:
        """Update sessions list from daemon response."""
        p = get_palette()
        sessions = data.get("sessions", [])

        self._count_label.set_markup(
            f'<b>Sessions</b>  <span foreground="{p["overlay"]}">{len(sessions)} total</span>'
        )

        self._store.clear()
        for s in sessions:
            sid = str(s.get("id", ""))[:12]
            calls = str(s.get("total_calls", "--"))
            files = str(s.get("files_touched", "--"))
            history = str(s.get("history_len", "--"))

            self._store.append([sid, calls, files, history])
