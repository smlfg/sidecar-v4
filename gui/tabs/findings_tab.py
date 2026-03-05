#!/usr/bin/env python3
"""Findings Tab — Scrollable list of sidecar findings with severity colors."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path.home() / "Projekte" / "ClaudeCodePanel"))
from theme import get_palette


class FindingsTab(Gtk.Box):
    """Findings display as colored cards in a scrolled list."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_margin_top(8)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self._count_label = None
        self._scrolled = None
        self._last_seen_ts: float = 0.0
        self.had_new_findings: bool = False
        self._build_ui()

    def _build_ui(self):
        p = get_palette()

        # Header with count
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self._count_label = Gtk.Label()
        self._count_label.set_markup(
            f'<b>Findings</b>  <span foreground="{p["overlay"]}">0 total</span>'
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
        self._scrolled.add(self._listbox)
        self.pack_start(self._scrolled, True, True, 0)

    def update(self, data: dict) -> None:
        """Update findings list from daemon response."""
        p = get_palette()
        findings = data.get("findings", [])

        self._count_label.set_markup(
            f'<b>Findings</b>  <span foreground="{p["overlay"]}">{len(findings)} total</span>'
        )

        # Detect new findings (timestamp > last seen)
        new_ts = 0.0
        new_finding_indices: set[int] = set()
        for i, f in enumerate(findings):
            ts_raw = f.get("timestamp", "")
            try:
                ts = datetime.fromisoformat(ts_raw).timestamp()
            except (ValueError, TypeError):
                ts = 0.0
            if ts > self._last_seen_ts:
                new_finding_indices.add(i)
            new_ts = max(new_ts, ts)

        self.had_new_findings = bool(new_finding_indices)
        if new_ts > self._last_seen_ts:
            self._last_seen_ts = new_ts

        # Remove old rows
        for child in self._listbox.get_children():
            self._listbox.remove(child)

        if not findings:
            row = Gtk.ListBoxRow()
            lbl = Gtk.Label()
            lbl.set_markup(f'<span foreground="{p["dim"]}">No findings recorded.</span>')
            lbl.set_margin_top(20)
            row.add(lbl)
            self._listbox.add(row)
            self._listbox.show_all()
            return

        for i, f in enumerate(findings):
            card = self._build_finding_card(f, p, is_new=(i in new_finding_indices))
            row = Gtk.ListBoxRow()
            row.add(card)
            self._listbox.add(row)

        self._listbox.show_all()

        # Auto-scroll to bottom when new findings arrived
        if self.had_new_findings:
            GLib.idle_add(self._scroll_to_bottom)

    def _scroll_to_bottom(self) -> bool:
        adj = self._scrolled.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
        return False  # one-shot idle

    def _build_finding_card(self, finding: dict, p: dict, is_new: bool = False) -> Gtk.Box:
        """Build a single finding card widget."""
        severity = finding.get("severity", "info").lower()
        border_color = {
            "critical": p["red"],
            "warning": p["yellow"],
            "info": p["accent"],
        }.get(severity, p["dim"])

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        card.get_style_context().add_class("base-card")
        # Override border-left via inline approach: use a horizontal box with a colored bar
        outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        if is_new:
            outer.get_style_context().add_class("base-badge-warn")
            # Remove highlight after 3 seconds
            GLib.timeout_add(3000, lambda: (
                outer.get_style_context().remove_class("base-badge-warn"), False
            )[-1])

        # Colored bar
        bar = Gtk.DrawingArea()
        bar.set_size_request(3, -1)
        bar.connect("draw", self._draw_bar, border_color)
        outer.pack_start(bar, False, False, 0)

        # Content
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        content.set_margin_start(8)
        content.set_margin_top(6)
        content.set_margin_bottom(6)

        # Top row: time + rule + severity badge
        top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        ts = finding.get("timestamp", "")
        time_str = "--:--"
        try:
            dt = datetime.fromisoformat(ts)
            time_str = dt.strftime("%H:%M")
        except (ValueError, TypeError):
            if ts:
                time_str = str(ts)[:5]

        time_lbl = Gtk.Label()
        time_lbl.set_markup(f'<span foreground="{p["dim"]}" font_family="monospace" size="small">{time_str}</span>')
        top_row.pack_start(time_lbl, False, False, 0)

        rule_name = finding.get("rule", "")
        rule_lbl = Gtk.Label()
        rule_lbl.set_markup(f'<tt><b>{GLib.markup_escape_text(rule_name)}</b></tt>')
        top_row.pack_start(rule_lbl, False, False, 0)

        sev_lbl = Gtk.Label(label=severity)
        css_cls = {
            "critical": "base-badge-error",
            "warning": "base-badge-warn",
            "info": "base-badge-ok",
        }.get(severity, "base-badge-ok")
        sev_lbl.get_style_context().add_class("base-badge")
        sev_lbl.get_style_context().add_class(css_cls)
        top_row.pack_end(sev_lbl, False, False, 0)

        content.pack_start(top_row, False, False, 0)

        # Message
        msg = finding.get("message", "")
        msg_lbl = Gtk.Label()
        msg_lbl.set_markup(f'<span foreground="{p["subtext1"]}" size="small">{GLib.markup_escape_text(msg)}</span>')
        msg_lbl.set_xalign(0)
        msg_lbl.set_line_wrap(True)
        msg_lbl.set_max_width_chars(80)
        content.pack_start(msg_lbl, False, False, 0)

        outer.pack_start(content, True, True, 0)
        return outer

    @staticmethod
    def _draw_bar(widget, cr, color_hex):
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
