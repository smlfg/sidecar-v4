# Agent Swarm Kanban — GUI Entwurf

## Ziel

Samuel will seine Agents bei der Arbeit SEHEN. Nicht in einer Log-Datei suchen, nicht
blind vertrauen — ein echter Kontrollraum. Wie NASA Mission Control, aber fuer AI Agents.

Der neue Tab "Swarm" im ClaudeCodePanel zeigt in Echtzeit:
- Welche Agents gerade laufen (mit Teamzugehoerigkeit)
- Was jeder Agent gerade tut (aktuelle Task oder letzter Schritt)
- Welche Tasks abhaengig voneinander sind (Kanban-Board)
- Wie Daten zwischen Agents fliessen

---

## Datenquellen

### 1. Team-Config: `~/.claude/teams/<team-name>/config.json`

Liefert: Agent-Namen, Farben, Modelle, Typen (orchestrator / general-purpose).

```json
{
  "name": "subconsciousness",
  "members": [
    {
      "name": "team-lead",
      "agentType": "orchestrator",
      "model": "claude-opus-4-6",
      "color": null
    },
    {
      "name": "architect",
      "agentType": "general-purpose",
      "model": "sonnet",
      "color": "blue"
    }
  ]
}
```

### 2. Task-Files: `~/.claude/tasks/<team-name>/<id>.json`

Liefert: Task-ID, Titel, Status (pending / in_progress / completed / deleted),
Abhaengigkeiten (blocks / blockedBy), Owner.

```json
{
  "id": "3",
  "subject": "kanban-designer",
  "status": "in_progress",
  "blocks": [],
  "blockedBy": [],
  "owner": "kanban-designer"
}
```

### 3. Session-Files: `~/.claude/projects/<project-id>/<session-id>.jsonl`

Liefert: Was ein Agent zuletzt getan hat — letzte Tool-Calls, letzter Text-Output.
Jede Zeile ist ein JSON-Objekt. Relevante Typen: `"assistant"` (mit `toolUse`-Blocks).

**Mapping Agent -> Session:** Der Lead-Session-ID steht in `config.json` als `leadSessionId`.
Fuer Team-Mitglieder: `~/.claude/projects/<leadSessionId>/` als Projektordner verwenden,
dann `.jsonl`-Dateien nach Aktivitaet sortieren.

### 4. Process-Scan: `ps aux` (wie process_manager.py)

Liefert: Welche `claude`-Prozesse laufen, mit welchen Verzeichnissen (CWD via `/proc/<pid>/cwd`).
Damit kann man aktive vs. tote Agents erkennen.

### 5. Lock-File: `~/.claude/tasks/<team-name>/.lock`

Wenn die Datei existiert und nicht leer ist, laeuft gerade eine Task-Operation.

---

## Daten-Abfrage Strategie

Der neue `agent_swarm.py` folgt dem Muster von `process_manager.py`:

```
_scan_swarm() -> list[AgentState]
  ├── lies alle teams/ Ordner
  ├── lies alle tasks/ Dateien pro Team
  ├── bestimme Session-Aktivitaet via stat() auf .jsonl Dateien
  └── korreliere mit ps-aux Scan (optional, teuer)
```

TTL-Cache: 10 Sekunden (Agents aendern sich schneller als Sessions).
Refresh-Timer: 10 Sekunden (wie Logs-Tab).

---

## UI-Mockup: Swarm Tab

```
+------------------------------------------------------------------+
| SWARM  [Team: subconsciousness v]  [Refresh]  Aktualisiert: 10s |
+------------------------------------------------------------------+

 TEAM-LEAD (Opus)                                           [live]
 +---------------------------------------------------------+
 | team-lead   orchestrator   claude-opus-4-6             |
 | Letzte Aktion: Nachrichten an Teammates gesendet        |
 | Sessions: 1 aktiv | Tasks: 5 vergeben                   |
 +---------------------------------------------------------+

 AGENTS ──────────────────────────────────────────────────────────

 [blue] architect          [green] twin-designer
 +------------------------+  +------------------------+
 | STATUS: in_progress    |  | STATUS: in_progress    |
 |                        |  |                        |
 | Task: "architect"      |  | Task: "twin-designer"  |
 | Letzter Schritt:       |  | Letzter Schritt:       |
 | Read architektur.md    |  | WebSearch: ClaudeBot   |
 |                        |  |                        |
 | Aktiv seit: 8 min      |  | Aktiv seit: 6 min      |
 | Session: 3f8477f8      |  | Session: --            |
 +------------------------+  +------------------------+

 [yellow] kanban-designer   [purple] profiler
 +------------------------+  +------------------------+
 | STATUS: in_progress    |  | STATUS: in_progress    |
 |                        |  |                        |
 | Task: "kanban-gui"     |  | Task: "profiler"       |
 | Letzter Schritt:       |  | Letzter Schritt:       |
 | Write entwurf.md       |  | Read samuel-profil.md  |
 |                        |  |                        |
 | Aktiv seit: 5 min      |  | Aktiv seit: 4 min      |
 | Session: --            |  | Session: --            |
 +------------------------+  +------------------------+

 [orange] researcher
 +------------------------+
 | STATUS: pending        |
 |                        |
 | Task: "prior-art"      |
 | Wartet auf: --         |
 |                        |
 | Aktiv seit: --         |
 +------------------------+

 KANBAN ──────────────────────────────────────────────────────────

   PENDING          IN PROGRESS         COMPLETED
 +------------+  +---------------+  +---------------+
 |            |  | architect   1 |  |               |
 |            |  | twin-desig  2 |  |               |
 |            |  | kanban-des  3 |  |               |
 |            |  | profiler    4 |  |               |
 |            |  |               |  |               |
 +------------+  +---------------+  +---------------+

 DATENFLUSS ──────────────────────────────────────────────────────

  team-lead ──[Aufgabe]──> architect
  team-lead ──[Aufgabe]──> twin-designer
  team-lead ──[Aufgabe]──> kanban-designer
  team-lead ──[Aufgabe]──> profiler
  team-lead ──[Aufgabe]──> researcher

  (Pfeile werden statisch aus config.json blocks/blockedBy generiert)

+------------------------------------------------------------------+
```

---

## Statusfarben (Catppuccin)

| Status      | Farbe (dark)  | Hex       |
|-------------|---------------|-----------|
| pending     | dim/overlay   | `#6c7086` |
| in_progress | yellow/peach  | `#f9e2af` |
| completed   | green         | `#a6e3a1` |
| idle (kein Prozess) | dim  | `#6c7086` |
| error       | red           | `#f38ba8` |

Agent-Karten bekommen farbige linke Border gemaess `color`-Feld in config.json:

| Farbe-Name | Catppuccin Mocha |
|------------|------------------|
| blue       | `#89b4fa`        |
| green      | `#a6e3a1`        |
| yellow     | `#f9e2af`        |
| purple     | `#cba6f7`        |
| orange     | `#fab387`        |
| teal       | `#94e2d5`        |

---

## Letzter-Schritt Erkennung

Aus den Session-JSONL-Dateien den letzten `toolUse`-Block extrahieren:

```python
def _get_last_action(session_path: Path) -> str:
    """Read last tool call from session .jsonl — letzte Zeile rueckwaerts lesen."""
    try:
        with open(session_path, 'rb') as f:
            # Effizient: letzte Bytes lesen statt ganze Datei
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 4096))
            tail = f.read().decode('utf-8', errors='ignore')

        for line in reversed(tail.splitlines()):
            if not line.strip():
                continue
            entry = json.loads(line)
            if entry.get('type') == 'assistant':
                content = entry.get('message', {}).get('content', [])
                for block in reversed(content) if isinstance(content, list) else []:
                    if block.get('type') == 'tool_use':
                        name = block.get('name', '?')
                        # Kuerzen und lesbar machen
                        inp = block.get('input', {})
                        path = inp.get('file_path', inp.get('path', inp.get('command', '')))
                        if path:
                            return f"{name}: {Path(path).name}"
                        return name
    except Exception:
        pass
    return "(keine Info)"
```

**Problem:** Team-Mitglieder haben keine eigene Session-ID in config.json.
Workaround: Alle `.jsonl`-Dateien in `~/.claude/projects/<leadSessionId>/` nach `st_mtime` sortieren.
Die neuesten N Dateien (ausser der Lead-Session) koennen Team-Member sein.

Alternativ: Reines Activity-Signal via `st_mtime` — wenn eine Datei sich in den letzten
30 Sekunden geaendert hat, ist der zugehoerige Agent "aktiv".

---

## Modul-Struktur: `agent_swarm.py`

Folgt dem Muster von `process_manager.py` (eigenstaendig, public API: build + refresh):

```python
# Public API
def build_swarm_tab() -> Gtk.ScrolledWindow: ...
def refresh_swarm() -> bool: ...  # returns True (GLib timer)

# Interne Funktionen
def _scan_teams() -> list[dict]: ...          # liest teams/ + tasks/
def _get_agent_activity(agent) -> dict: ...   # session activity
def _build_agent_card(agent) -> Gtk.Frame: ... # eine Agent-Karte
def _build_kanban_section(tasks) -> Gtk.Box: ...
def _build_flow_section(members) -> Gtk.Box: ...
```

### Neue Daten-Funktionen in `monitor.py`

```python
def get_team_configs() -> list[dict]: ...     # alle teams/ Ordner
def get_team_tasks(team_name: str) -> list[dict]: ...  # tasks/<team>/
```

---

## Integration in panel.py

1. Import: `from agent_swarm import build_swarm_tab, refresh_swarm`
2. Neuer Tab nach "Prozesse":
   ```python
   notebook.append_page(build_swarm_tab(), Gtk.Label(label="Swarm"))
   ```
3. Timer in `_start_all_timers()`:
   ```python
   GLib.timeout_add_seconds(10, refresh_swarm)
   ```

---

## Was NICHT gebaut wird (Scope)

- Kein Echtzeit-Streaming von Agent-Output (zu teuer, GTK nicht dafuer gebaut)
- Kein Eingriff in Agents (kein Kill/Pause via GUI — das ist Prozesse-Tab)
- Keine Visualisierung von Token-Kosten pro Agent (Phase 2)
- Kein Dependency-Graph mit Pfeilen (nur Text-Datenfluss)

---

## Offene Fragen / Risiken

1. **Session-zu-Agent Mapping:** Team-Mitglieder schreiben ihre Sessions nicht in
   `config.json`. Die Zuordnung "welche JSONL gehoert zu welchem Agent" ist implizit.
   Einzige Chance: Timestamp-Korrelation (Agent gestartet um T, Session erstellt um T+delta).
   **Vorschlag fuer Phase 2:** Claude Code soll Session-ID in tasks/ schreiben.

2. **Refresh-Frequenz:** 10s ist gut fuer Status, aber "letzter Schritt" kann veraltet sein.
   Bei schnellen Agents (viele Tool-Calls) koennte man auf 5s gehen.

3. **GTK-Threading:** `_get_last_action()` liest Disk — muss via `GLib.idle_add` oder
   in einem Thread (mit `GLib.idle_add` fuer UI-Updates) laufen. Nicht im Main-Thread!

4. **Keine Session fuer neue Agents:** Agents die noch nie gestartet wurden haben
   keine Session-Datei. Die Karte zeigt dann nur config.json-Daten (Status: pending).

---

## Naexter Schritt

Wenn dieser Entwurf genehmigt ist:
1. `agent_swarm.py` als neues Modul erstellen (~300 Zeilen)
2. `monitor.py` um `get_team_configs()` + `get_team_tasks()` erweitern
3. `panel.py` Tab + Timer hinzufuegen (~15 Zeilen)

Gesamt-Aufwand: ~350 neue Zeilen. Kein bestehender Code veraendert ausser 2 kleine Ergaenzungen.
