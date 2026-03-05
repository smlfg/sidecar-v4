#!/usr/bin/env python3
"""Context Tab — Live injection history from the Sidecar daemon."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path.home() / "Projekte" / "ClaudeCodePanel"))
from theme import get_palette


class ContextTab(Gtk.Box):
    """Scrollable list of context injections with expandable text."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_margin_top(8)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self._count_label = None
        self._scrolled = None
        self._listbox = None
        self._last_seen_ts: float = 0.0
        self.had_new_injections: bool = False
        self._build_ui()

    def _build_ui(self):
        p = get_palette()

        # Header with count
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self._count_label = Gtk.Label()
        self._count_label.set_markup(
            f'<b>Context</b>  <span foreground="{p["overlay"]}">0 injections</span>'
        )
        self._count_label.set_halign(Gtk.Align.START)
        header.pack_start(self._count_label, False, False, 0)
        self.pack_start(header, False, False, 0)

        # Scrolled list
        self._scrolled = Gtk.ScrolledWindow()
        self._scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._scrolled.set_vexpand(True)

        self._listbox = Gtk.ListBox()
        self._listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self._listbox.connect("row-activated", self._on_row_activated)
        self._scrolled.add(self._listbox)
        self.pack_start(self._scrolled, True, True, 0)

    def update(self, data: dict) -> None:
        """Update injections list from daemon response."""
        p = get_palette()
        injections = data.get("injections", [])

        self._count_label.set_markup(
            f'<b>Context</b>  <span foreground="{p["overlay"]}">{len(injections)} injections</span>'
        )

        # Detect new entries by unix timestamp
        new_ts = 0.0
        new_indices: set[int] = set()
        for i, inj in enumerate(injections):
            ts = float(inj.get("ts", 0.0))
            if ts > self._last_seen_ts:
                new_indices.add(i)
            new_ts = max(new_ts, ts)

        self.had_new_injections = bool(new_indices)
        if new_ts > self._last_seen_ts:
            self._last_seen_ts = new_ts

        # Rebuild rows
        for child in self._listbox.get_children():
            self._listbox.remove(child)

        if not injections:
            row = Gtk.ListBoxRow()
            lbl = Gtk.Label()
            lbl.set_markup(f'<span foreground="{p["dim"]}">No injections recorded.</span>')
            lbl.set_margin_top(20)
            row.add(lbl)
            self._listbox.add(row)
            self._listbox.show_all()
            return

        for i, inj in enumerate(injections):
            card = self._build_card(inj, p)
            row = Gtk.ListBoxRow()
            row.add(card)
            self._listbox.add(row)

        self._listbox.show_all()

        if self.had_new_injections:
            GLib.idle_add(self._scroll_to_bottom)

    def _scroll_to_bottom(self) -> bool:
        adj = self._scrolled.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
        return False

    def _on_row_activated(self, listbox, row) -> None:
        """Toggle expand/collapse of the clicked card's full text."""
        card = row.get_child()
        revealer = getattr(card, "_revealer", None)
        if revealer is not None:
            revealer.set_reveal_child(not revealer.get_reveal_child())

    def _build_card(self, inj: dict, p: dict) -> Gtk.Box:
        """Build a single injection card widget."""
        hook = inj.get("hook", "prompt")
        bar_color = p["accent"] if hook == "prompt" else p["yellow"]
        hook_badge_cls = "base-badge-ok" if hook == "prompt" else "base-badge-warn"

        outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # Colored left bar
        bar = Gtk.DrawingArea()
        bar.set_size_request(3, -1)
        bar.connect("draw", self._draw_bar, bar_color)
        outer.pack_start(bar, False, False, 0)

        # Content area
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        content.set_margin_start(8)
        content.set_margin_top(6)
        content.set_margin_bottom(6)
        content.set_margin_end(6)

        # Top row: time, hook badge, char count, source badges
        top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        ts_raw = float(inj.get("ts", 0.0))
        try:
            time_str = datetime.fromtimestamp(ts_raw).strftime("%H:%M:%S")
        except (OSError, OverflowError, ValueError):
            time_str = "--:--:--"

        time_lbl = Gtk.Label()
        time_lbl.set_markup(
            f'<span foreground="{p["dim"]}" font_family="monospace" size="small">{time_str}</span>'
        )
        top_row.pack_start(time_lbl, False, False, 0)

        hook_lbl = Gtk.Label(label=hook)
        hook_lbl.get_style_context().add_class("base-badge")
        hook_lbl.get_style_context().add_class(hook_badge_cls)
        top_row.pack_start(hook_lbl, False, False, 0)

        chars = inj.get("chars", 0)
        chars_lbl = Gtk.Label()
        chars_lbl.set_markup(
            f'<span foreground="{p["subtext1"]}" size="small">{chars} chars</span>'
        )
        top_row.pack_start(chars_lbl, False, False, 0)

        for src in inj.get("sources", []):
            src_lbl = Gtk.Label(label=GLib.markup_escape_text(str(src)))
            src_lbl.get_style_context().add_class("base-badge")
            top_row.pack_start(src_lbl, False, False, 0)

        content.pack_start(top_row, False, False, 0)

        # Preview: first 2 lines
        text = inj.get("text", "")
        lines = text.splitlines()
        preview_text = "\n".join(lines[:2])
        if len(lines) > 2:
            preview_text += f"\n…  ({len(lines) - 2} more lines)"

        preview_lbl = Gtk.Label()
        preview_lbl.set_markup(
            f'<span foreground="{p["subtext1"]}" font_family="monospace" size="small">'
            f"{GLib.markup_escape_text(preview_text)}</span>"
        )
        preview_lbl.set_xalign(0)
        preview_lbl.set_line_wrap(True)
        preview_lbl.set_max_width_chars(100)
        content.pack_start(preview_lbl, False, False, 0)

        # Revealer for full text (hidden by default)
        revealer = Gtk.Revealer()
        revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        revealer.set_reveal_child(False)

        full_lbl = Gtk.Label()
        full_lbl.set_markup(
            f'<span foreground="{p["overlay"]}" font_family="monospace" size="small">'
            f"{GLib.markup_escape_text(text)}</span>"
        )
        full_lbl.set_xalign(0)
        full_lbl.set_line_wrap(True)
        full_lbl.set_max_width_chars(100)
        full_lbl.set_margin_top(4)
        revealer.add(full_lbl)
        content.pack_start(revealer, False, False, 0)

        outer.pack_start(content, True, True, 0)

        # Attach revealer so _on_row_activated can find it
        outer._revealer = revealer
        return outer

    @staticmethod
    def _draw_bar(widget, cr, color_hex: str) -> bool:
        """Draw a colored vertical bar."""
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        r = int(color_hex[1:3], 16) / 255
        g = int(color_hex[3:5], 16) / 255
        b = int(color_hex[5:7], 16) / 255
        cr.set_source_rgb(r, g, b)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        return False
