#!/usr/bin/env python3
"""Non-blocking Unix Socket client for Sidecar daemon.

Uses GLib.io_add_watch for async I/O — no threading needed.
Protocol: Send JSON command, receive JSON response, close.
"""

import json
import socket
from pathlib import Path

from gi.repository import GLib

SOCKET_PATH = "/tmp/claude-sidecar.sock"


def send_command(cmd_data: dict, callback, error_callback=None) -> None:
    """Send a command to the sidecar daemon asynchronously.

    Args:
        cmd_data: Dict with at least {"cmd": "..."}.
        callback: Called with parsed JSON response dict.
        error_callback: Called with error message string on failure.
    """
    cmd_data["_type"] = "cmd"
    raw = json.dumps(cmd_data).encode()

    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.setblocking(False)
    except OSError as e:
        if error_callback:
            error_callback(f"Socket creation failed: {e}")
        return

    try:
        sock.connect(SOCKET_PATH)
    except BlockingIOError:
        pass  # connect in progress — normal for non-blocking
    except (FileNotFoundError, ConnectionRefusedError) as e:
        sock.close()
        if error_callback:
            error_callback("Daemon not running")
        return
    except OSError as e:
        sock.close()
        if error_callback:
            error_callback(str(e))
        return

    chunks = []
    sent = [False]

    def _on_io(fd, condition):
        if condition & GLib.IO_OUT and not sent[0]:
            try:
                sock.sendall(raw)
                sent[0] = True
            except OSError as e:
                sock.close()
                if error_callback:
                    GLib.idle_add(error_callback, str(e))
                return False
            # Now watch for incoming data
            GLib.io_add_watch(sock.fileno(), GLib.IO_IN | GLib.IO_HUP | GLib.IO_ERR, _on_read)
            return False  # remove OUT watch
        return False

    def _on_read(fd, condition):
        if condition & (GLib.IO_HUP | GLib.IO_ERR):
            _finish()
            return False
        try:
            chunk = sock.recv(65536)
            if not chunk:
                _finish()
                return False
            chunks.append(chunk)
            return True  # keep reading
        except BlockingIOError:
            return True
        except OSError:
            _finish()
            return False

    def _finish():
        sock.close()
        raw_resp = b"".join(chunks).decode()
        if not raw_resp:
            if error_callback:
                GLib.idle_add(error_callback, "Empty response")
            return
        try:
            data = json.loads(raw_resp)
            GLib.idle_add(callback, data)
        except json.JSONDecodeError as e:
            if error_callback:
                GLib.idle_add(error_callback, f"Invalid JSON: {e}")

    GLib.io_add_watch(sock.fileno(), GLib.IO_OUT, _on_io)


def is_daemon_reachable() -> bool:
    """Synchronous check if the socket file exists."""
    return Path(SOCKET_PATH).exists()
