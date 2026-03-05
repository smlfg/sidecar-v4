#!/usr/bin/env python3
"""Sessions Tab — Active Claude sessions overview with project names."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Pango

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.home() / "Projekte" / "ClaudeCodePanel"))
from theme import get_palette

# Phase colors (Catppuccin-ish)
PHASE_COLORS = {
    "exploration": "#89b4fa",   # blue
    "implementation": "#a6e3a1", # green
    "testing": "#f9e2af",       # yellow
    "debugging": "#f38ba8",     # red
}

# ListStore column indices
COL_PROJECT = 0
COL_PHASE = 1
COL_CALLS = 2
COL_FILES = 3
COL_STARTED = 4
COL_ID = 5  # hidden, for tooltip


def _relative_time(ts: float) -> str:
    """Convert timestamp to relative human-readable string."""
    if not ts:
        return "–"
    delta = int(time.time() - ts)
    if delta < 60:
        return "gerade eben"
    if delta < 3600:
        mins = delta // 60
        return f"vor {mins} Min"
    if delta < 86400:
        hours = delta // 3600
        return f"vor {hours} Std"
    days = delta // 86400
    return f"vor {days} Tag{'en' if days > 1 else ''}"


class SessionsTab(Gtk.Box):
    """Active Claude sessions as a sortable TreeView."""

    def __init__(self, on_session_selected=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_margin_top(8)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self._on_session_selected = on_session_selected
        self._count_label = None
        self._store = None
        self._tree = None
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

        # ListStore: project, phase_markup, calls, files, started, id(hidden)
        self._store = Gtk.ListStore(str, str, str, str, str, str)

        self._tree = Gtk.TreeView(model=self._store)
        self._tree.set_headers_visible(True)
        self._tree.set_tooltip_column(COL_ID)
        self._tree.get_style_context().add_class("base-card")

        # Project column (bold)
        renderer_proj = Gtk.CellRendererText()
        renderer_proj.set_property("weight", Pango.Weight.BOLD)
        col_proj = Gtk.TreeViewColumn("Project", renderer_proj, text=COL_PROJECT)
        col_proj.set_resizable(True)
        col_proj.set_min_width(150)
        col_proj.set_sort_column_id(COL_PROJECT)
        self._tree.append_column(col_proj)

        # Phase column (colored markup)
        renderer_phase = Gtk.CellRendererText()
        col_phase = Gtk.TreeViewColumn("Phase", renderer_phase, markup=COL_PHASE)
        col_phase.set_resizable(True)
        col_phase.set_min_width(110)
        self._tree.append_column(col_phase)

        # Calls, Files, Started — plain text columns
        for title, col_idx, min_w in [("Calls", COL_CALLS, 60), ("Files", COL_FILES, 60), ("Started", COL_STARTED, 100)]:
            renderer = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(title, renderer, text=col_idx)
            col.set_resizable(True)
            col.set_min_width(min_w)
            col.set_sort_column_id(col_idx)
            self._tree.append_column(col)

        # Double-click to select session
        self._tree.connect("row-activated", self._on_row_activated)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.add(self._tree)
        self.pack_start(scrolled, True, True, 0)

    def _build_row_values(self, s: dict, p: dict) -> list:
        """Build the list of column values for a session dict."""
        project = str(s.get("project", "–"))
        phase_raw = str(s.get("phase", "–"))
        calls = str(s.get("total_calls", "–"))
        files = str(s.get("files_touched", "–"))
        sid = str(s.get("id", ""))

        phase_color = PHASE_COLORS.get(phase_raw, p.get("subtext1", "#999"))
        phase_markup = f'<span foreground="{phase_color}">● {GLib.markup_escape_text(phase_raw)}</span>'

        start_ts = s.get("start_ts", 0)
        started = _relative_time(start_ts)

        return [project, phase_markup, calls, files, started, sid]

    def update(self, data: dict) -> None:
        """Update sessions list from daemon response (diff-based, no flicker)."""
        p = get_palette()
        sessions = data.get("sessions", [])

        self._count_label.set_markup(
            f'<b>Sessions</b>  <span foreground="{p["overlay"]}">{len(sessions)} active</span>'
        )

        # Build lookup: session_id → session dict
        incoming = {str(s.get("id", "")): s for s in sessions}

        # Preserve selection
        selection = self._tree.get_selection()
        selected_model, selected_iter = selection.get_selected()
        selected_sid = None
        if selected_iter is not None:
            selected_sid = self._store.get_value(selected_iter, COL_ID)

        # Walk existing rows: update in-place or mark for removal
        to_remove = []
        it = self._store.get_iter_first()
        while it is not None:
            sid = self._store.get_value(it, COL_ID)
            if sid in incoming:
                row_values = self._build_row_values(incoming[sid], p)
                for col_idx, val in enumerate(row_values):
                    self._store.set_value(it, col_idx, val)
                incoming.pop(sid)  # mark as handled
            else:
                to_remove.append(self._store.get_path(it))
            it = self._store.iter_next(it)

        # Remove stale rows (iterate paths in reverse to keep indices valid)
        for path in reversed(to_remove):
            it = self._store.get_iter(path)
            if it is not None:
                self._store.remove(it)

        # Append new sessions that weren't in the store yet
        for s in sessions:
            sid = str(s.get("id", ""))
            if sid in incoming:  # still unhandled → new
                self._store.append(self._build_row_values(s, p))

        # Restore selection if the previously selected session still exists
        if selected_sid is not None:
            it = self._store.get_iter_first()
            while it is not None:
                if self._store.get_value(it, COL_ID) == selected_sid:
                    selection.select_iter(it)
                    break
                it = self._store.iter_next(it)

    def _on_row_activated(self, tree, path, column):
        """Double-click on a session row → select it in the picker."""
        model = tree.get_model()
        it = model.get_iter(path)
        if it:
            sid = model.get_value(it, COL_ID)
            if sid and self._on_session_selected:
                self._on_session_selected(sid)
