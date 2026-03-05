#!/usr/bin/env python3
"""SessionWatcher — Real-time monitor for Claude Code session JSONL files.

Watches ~/.claude/projects/ for JSONL file changes using watchdog.
Parses new lines as they are appended and emits structured event dicts
to a callback. Designed to run as a background thread inside the sidecar daemon.

Real JSONL format (observed from Claude Code 2.1.69):
  Each line is a JSON object with top-level "type" field:
    "user"      — user message  (obj.message.role == "user")
    "assistant" — assistant turn (obj.message.content[] may contain tool_use items)
    "progress"  — tool progress / hook notifications (skipped)
    "file-history-snapshot" — internal snapshot (skipped)

  Tool calls live inside assistant messages:
    obj.message.content[].type == "tool_use"
    obj.message.content[].name == "Read" | "Edit" | "Bash" | ...
    obj.message.content[].input == {...}

  Error detection: user messages with interrupt text, or assistant
  messages whose content contains error keywords.
"""

import json
import os
import threading
import time
from typing import Callable, Dict, Optional

# --- Logging (same pattern as all sidecar modules) ---

def _log(msg: str) -> None:
    try:
        with open("/tmp/claude-sidecar.log", "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [session_watcher] {msg}\n")
    except Exception:
        pass


# --- Watchdog import with graceful degradation ---

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent
    _WATCHDOG_AVAILABLE = True
except ImportError:
    _WATCHDOG_AVAILABLE = False
    _log("watchdog not installed — SessionWatcher will run in polling fallback mode")


# --- Constants ---

ERROR_KEYWORDS = (
    "Traceback (most recent call last)",
    "Error:", "FAILED", "SyntaxError", "TypeError",
    "NameError", "ValueError", "AttributeError",
    "ImportError", "ModuleNotFoundError", "RuntimeError",
    "fatal:", "panic:", "segfault",
)

PROJECTS_DIR_DEFAULT = os.path.expanduser("~/.claude/projects/")

POLL_INTERVAL = 2.0  # seconds, used in fallback polling mode


# --- JSONL parser helpers ---

def _extract_events(obj: dict, session_id: str) -> list[dict]:
    """Parse one JSONL object into zero or more event dicts."""
    events = []
    top_type = obj.get("type", "")
    ts_raw = obj.get("timestamp", "")

    # Parse ISO timestamp → unix float; fall back to now
    try:
        from datetime import datetime, timezone
        ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).timestamp()
    except Exception:
        ts = time.time()

    if top_type == "user":
        message = obj.get("message", {})
        content_list = message.get("content", [])
        text = " ".join(
            item.get("text", "") for item in content_list
            if isinstance(item, dict) and item.get("type") == "text"
        )
        had_error = any(kw in text for kw in ERROR_KEYWORDS)
        events.append({
            "type": "user_message",
            "session_id": session_id,
            "timestamp": ts,
            "content": text[:500],
            "had_error": had_error,
        })

    elif top_type == "assistant":
        message = obj.get("message", {})
        content_list = message.get("content", [])
        tool_uses = [item for item in content_list
                     if isinstance(item, dict) and item.get("type") == "tool_use"]
        text_parts = [item for item in content_list
                      if isinstance(item, dict) and item.get("type") == "text"]

        if tool_uses:
            for tool in tool_uses:
                events.append({
                    "type": "tool_use",
                    "session_id": session_id,
                    "timestamp": ts,
                    "tool_name": tool.get("name", ""),
                    "tool_input": tool.get("input", {}),
                    "content": "",
                    "had_error": False,
                })
        else:
            text = " ".join(p.get("text", "") for p in text_parts)
            had_error = any(kw in text for kw in ERROR_KEYWORDS)
            events.append({
                "type": "assistant_response",
                "session_id": session_id,
                "timestamp": ts,
                "content": text[:500],
                "had_error": had_error,
            })

    # "progress" and "file-history-snapshot" are intentionally skipped

    return events


# --- Core watcher ---

class SessionWatcher:
    """Watches Claude Code JSONL session files and emits structured events.

    Usage:
        watcher = SessionWatcher(on_event=my_callback)
        watcher.start()
        ...
        watcher.stop()
    """

    def __init__(
        self,
        projects_dir: Optional[str] = None,
        on_event: Optional[Callable[[dict], None]] = None,
    ):
        self._projects_dir = projects_dir or PROJECTS_DIR_DEFAULT
        self._on_event = on_event
        self._lock = threading.Lock()
        self._file_offsets: Dict[str, int] = {}   # path → last read byte offset
        self._active_session: Optional[str] = None
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._observer = None  # watchdog Observer, if available

    # --- Public API ---

    def start(self) -> None:
        """Start watching in a background thread."""
        if self._thread and self._thread.is_alive():
            _log("already running — ignoring start()")
            return

        self._stop_event.clear()

        if _WATCHDOG_AVAILABLE:
            self._start_watchdog()
        else:
            self._start_polling()

        _log(f"started (projects_dir={self._projects_dir}, watchdog={_WATCHDOG_AVAILABLE})")

    def stop(self) -> None:
        """Stop the watcher thread and observer."""
        self._stop_event.set()

        if self._observer:
            try:
                self._observer.stop()
                self._observer.join(timeout=3)
            except Exception as e:
                _log(f"error stopping observer: {e}")
            self._observer = None

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)

        _log("stopped")

    def get_active_session(self) -> Optional[str]:
        """Return the session ID of the most recently active session."""
        with self._lock:
            return self._active_session

    # --- Watchdog path ---

    def _start_watchdog(self) -> None:
        handler = _JournalEventHandler(on_modified=self._on_file_modified)
        self._observer = Observer()
        self._observer.schedule(handler, self._projects_dir, recursive=True)
        self._observer.start()

        # Also start a lightweight thread to keep the main loop alive
        # and catch any files that were missed at startup.
        self._thread = threading.Thread(
            target=self._watchdog_loop, daemon=True, name="session-watcher"
        )
        self._thread.start()

    def _watchdog_loop(self) -> None:
        """Idle loop — just keeps the thread alive so stop() can join it."""
        self._scan_existing_files()
        while not self._stop_event.is_set():
            self._stop_event.wait(timeout=30)

    def _on_file_modified(self, path: str) -> None:
        if path.endswith(".jsonl"):
            self._read_new_lines(path)

    # --- Polling fallback path ---

    def _start_polling(self) -> None:
        self._thread = threading.Thread(
            target=self._polling_loop, daemon=True, name="session-watcher-poll"
        )
        self._thread.start()

    def _polling_loop(self) -> None:
        self._scan_existing_files()
        while not self._stop_event.is_set():
            try:
                self._poll_all_files()
            except Exception as e:
                _log(f"polling error: {e}")
            self._stop_event.wait(timeout=POLL_INTERVAL)

    def _poll_all_files(self) -> None:
        for dirpath, _dirs, files in os.walk(self._projects_dir):
            for fname in files:
                if fname.endswith(".jsonl"):
                    self._read_new_lines(os.path.join(dirpath, fname))

    # --- Shared helpers ---

    def _scan_existing_files(self) -> None:
        """On startup: record current file sizes so we only read *new* lines."""
        if not os.path.isdir(self._projects_dir):
            _log(f"projects_dir not found: {self._projects_dir}")
            return

        count = 0
        for dirpath, _dirs, files in os.walk(self._projects_dir):
            for fname in files:
                if fname.endswith(".jsonl"):
                    path = os.path.join(dirpath, fname)
                    try:
                        size = os.path.getsize(path)
                    except OSError:
                        size = 0
                    with self._lock:
                        self._file_offsets[path] = size
                    count += 1

        _log(f"scan complete: {count} existing JSONL files registered")

    def _session_id_from_path(self, path: str) -> str:
        """Extract session ID from filename (UUID before .jsonl)."""
        basename = os.path.basename(path)
        return basename.removesuffix(".jsonl")

    def _read_new_lines(self, path: str) -> None:
        """Read any lines appended since last read and emit events."""
        with self._lock:
            offset = self._file_offsets.get(path, 0)

        try:
            current_size = os.path.getsize(path)
        except OSError:
            return  # file deleted/rotated

        if current_size < offset:
            # File was truncated/rotated — reset
            _log(f"file truncated, resetting offset: {os.path.basename(path)}")
            with self._lock:
                self._file_offsets[path] = 0
            offset = 0

        if current_size == offset:
            return  # nothing new

        session_id = self._session_id_from_path(path)
        new_events = []

        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                fh.seek(offset)
                for raw_line in fh:
                    line = raw_line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue  # skip malformed lines
                    events = _extract_events(obj, session_id)
                    new_events.extend(events)
                new_offset = fh.tell()
        except OSError as e:
            _log(f"read error on {os.path.basename(path)}: {e}")
            return

        with self._lock:
            self._file_offsets[path] = new_offset
            if new_events:
                self._active_session = session_id

        for event in new_events:
            self._emit(event)

    def _emit(self, event: dict) -> None:
        if not self._on_event:
            return
        try:
            self._on_event(event)
        except Exception as e:
            _log(f"on_event callback error: {e}")


# --- Watchdog event handler ---

if _WATCHDOG_AVAILABLE:
    class _JournalEventHandler(FileSystemEventHandler):
        def __init__(self, on_modified: Callable[[str], None]):
            super().__init__()
            self._on_modified = on_modified

        def on_modified(self, event):
            if not event.is_directory:
                self._on_modified(event.src_path)

        def on_created(self, event):
            # New JSONL file — treat as modification so it gets registered
            if not event.is_directory and event.src_path.endswith(".jsonl"):
                self._on_modified(event.src_path)
else:
    class _JournalEventHandler:  # type: ignore[no-redef]
        pass


# --- Smoke test ---

if __name__ == "__main__":
    print("SessionWatcher smoke test — press Ctrl+C to stop")

    def handle(event: dict) -> None:
        t = event["type"]
        sid = event["session_id"][:8]
        extra = ""
        if t == "tool_use":
            extra = f" tool={event.get('tool_name')}"
        elif t in ("user_message", "assistant_response"):
            extra = f" content={event.get('content', '')[:60]!r}"
        print(f"[{t}] session={sid}...{extra}")

    watcher = SessionWatcher(on_event=handle)
    watcher.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.stop()
        print("stopped.")
