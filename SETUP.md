# Sidecar + Voice Bridge Setup

## Voraussetzungen

```bash
# wtype (Wayland text injection — primaerer Ansatz)
sudo apt install wtype

# ydotool (Fallback falls wtype auf COSMIC nicht geht)
sudo apt install ydotool

# Whisper STT (fuer Voice Bridge)
pip3 install openai-whisper sounddevice numpy

# watchdog (fuer Sidecar Daemon — optional, inotify ist besser)
# pip3 install watchdog
```

## Installation

### 1. Sidecar Daemon

```bash
# Service installieren
mkdir -p ~/.config/systemd/user/
cp sidecar.service ~/.config/systemd/user/claude-sidecar.service
systemctl --user daemon-reload
systemctl --user enable claude-sidecar.service
systemctl --user start claude-sidecar.service

# Status pruefen
systemctl --user status claude-sidecar.service
journalctl --user -u claude-sidecar.service -f
```

### 2. Voice Bridge

```bash
# Service installieren
cp voice-bridge.service ~/.config/systemd/user/voice-bridge.service
systemctl --user daemon-reload
systemctl --user enable voice-bridge.service
systemctl --user start voice-bridge.service

# Trigger-Pipe erstellen
mkfifo /tmp/voice-bridge-trigger

# Test: Aufnahme triggern
echo "start" > /tmp/voice-bridge-trigger
```

### 3. Hook Migration (settings.json)

In `~/.claude/settings.json` den minimax_watcher Hook durch sidecar_bridge ersetzen:

**Vorher:**
```json
{
  "matcher": "Bash|Edit|Write",
  "hooks": [{
    "type": "command",
    "command": "python3 /home/smlflg/Dokumente/Pläne/ClaudeCodeWorks/plugins/claude-hook/hooks/minimax_watcher.py",
    "timeout": 15
  }]
}
```

**Nachher:**
```json
{
  "matcher": "Bash|Edit|Write",
  "hooks": [{
    "type": "command",
    "command": "python3 /home/smlflg/Dokumente/Pläne/ClaudeCodeWorks/plugins/claude-hook/hooks/sidecar_bridge.py",
    "timeout": 5
  }]
}
```

### 4. COSMIC Shortcut fuer Voice (optional)

COSMIC Settings → Keyboard → Custom Shortcuts:
- Name: "Voice Bridge Toggle"
- Command: `bash -c 'echo start > /tmp/voice-bridge-trigger'`
- Shortcut: F5 oder Super+V

## Validation

```bash
# Sidecar laeuft?
ls -la /tmp/claude-sidecar.sock
tail -f /tmp/claude-sidecar.log

# Voice Bridge laeuft?
tail -f /tmp/voice-bridge.log

# wtype funktioniert?
wtype "hello world"

# Trigger testen
echo "start" > /tmp/voice-bridge-trigger
# → Sprechen → Text erscheint im Terminal
```

## Rollback

```bash
# Sidecar zurueck zu minimax_watcher
# In settings.json: sidecar_bridge.py → minimax_watcher.py
systemctl --user stop claude-sidecar.service
systemctl --user disable claude-sidecar.service

# Voice Bridge stoppen
systemctl --user stop voice-bridge.service
systemctl --user disable voice-bridge.service
```
