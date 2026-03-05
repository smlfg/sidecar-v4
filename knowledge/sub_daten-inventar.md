# Datenquellen-Inventar — Digitaler Zwilling Samuel
Stand: 2026-03-02 (aktualisiert von Scout-Agent)

---

## 1. Claude Code Sessions

**Pfad:** `~/.claude/`

| Datei/Verzeichnis | Groesse | Eintraege | Format |
|---|---|---|---|
| `history.jsonl` | 572 KB | 2.326 Zeilen | JSONL — user-Prompts mit sessionId, timestamp, project |
| `projects/*/` | 553 MB | 1.265 JSONL-Dateien | JSONL — vollstaendige Sessions incl. Tool-Calls, AI-Antworten |
| `usage/` | 176 KB | 3.538 Eintraege | JSONL — Tool-Events mit Timestamp (2 Tage) |
| `session-logs/` | 80 KB | 10 Markdown-Dateien | Manuell geschriebene Session-Rueckblicke |
| `file-history/` | — | 307 Dateien | Datei-Versionshistorie |
| `todos/` | — | 125 Eintraege | Todo-Listen aus Sessions |

**Bewertung:** Goldgrube. `history.jsonl` = Samuels eigene Worte uber Monate. Projects = vollstaendige Denkprozesse. Usage = Verhaltensmuster (welche Tools wann). Maschinenlesbar, strukturiert.

**Analyse-Aufwand:** Niedrig — direkt parsebar, kein Preprocessing noetig.

---

## 2. Gemini / NotebookLM Takeout

**Pfad:** `~/Downloads/Sessions_GEMINI/extracted/Takeout/`

| Quelle | Groesse | Eintraege | Format |
|---|---|---|---|
| `Gemini/` | minimal | 2 HTML-Dateien | HTML — Gems + Scheduled Actions (kein Chat-History!) |
| `NotebookLM/` | 868 MB | 248 JSON-Dateien | JSON — Notebooks, Sources, Artifacts, Chat-History |

**Wichtiger Befund:** Der Gemini Takeout enthaelt **keine Chat-Konversationen** — nur Gems-Konfiguration und Scheduled Actions. Die echten Gespraeche fehlen (typisches Google Takeout Limit). NotebookLM dagegen hat strukturierte Projektkontexte mit Artefakten aus echten Projekten (Keeper System, mAImory, Self AI V2, ADHS-Notebook).

**Analyse-Aufwand:** Mittel — NotebookLM JSON-Format muss erst geprueft werden, Bulk ist Sources (HTML), nicht Chat.

---

## 3. WhatsApp — MoltBot Credentials

**Pfad:** `~/.moltbot/`

| Datei | Groesse | Inhalt |
|---|---|---|
| `credentials/whatsapp/default/` | 7,6 MB gesamt | 1.752 JSON-Dateien — Crypto-Keys, Session-Keys, LID-Mappings |
| `agents/main/sessions/*.jsonl` | 340 KB | 124 Zeilen — MoltBot-interne Chat-Sessions |

**Wichtiger Befund:** Das ist **kein WhatsApp-Nachrichtenarchiv**. Es sind die Krypto-Credentials des MoltBot-WhatsApp-Bots (pre-keys, sender-keys, session-keys fuer E2E-Verschluesselung). Keine lesbaren Nachrichten vorhanden.

**Echte WhatsApp-Chatverlaeufe:** Nicht gefunden auf dem System. Muessen vom Handy exportiert werden (Android: Chat > ... > Chat exportieren > .txt/.zip) oder via WhatsApp Web.

**Analyse-Aufwand:** N/A — falsche Quelle. Echte Backups fehlen noch.

---

## 4. ChatGPT Export

**Pfad:** `~/Downloads/Sessions_ChatGPT/`

| Datei | Groesse | Inhalt |
|---|---|---|
| Ordner leer (kein `conversations.json`) | 4 KB (Ordner) | Nur leerer Ordner mit FOR_SMLFLG.md |

**Befund:** Kein ChatGPT-Export vorhanden. Muss frisch unter https://chatgpt.com/settings → Datenkontrollen → Alle Daten exportieren angefordert werden. Format wenn vorhanden: `conversations.json` (~100MB+), maschinenlesbar.

**Analyse-Aufwand:** Erst nach Export beurteilbar.

---

## 5. Bonus: Claude T450s Archiv

**Pfad:** `~/Downloads/Claude T450s-20260209T160919Z-1-001.zip`
**Groesse:** 34 MB
**Inhalt:** Vermutlich Claude Code History vom alten Laptop (T450s), importiert am 09.02.2026.

**Analyse-Aufwand:** Niedrig — gleicher JSONL-Format wie aktuelle sessions.

---

## Prioritaets-Reihenfolge

| Prio | Quelle | Begruendung |
|---|---|---|
| **1** | `~/.claude/history.jsonl` + `projects/` | Groesste Dichte an Samuels eigener Sprache, Denkweise, Projekten. Maschinenlesbar. Sofort verfuegbar. |
| **2** | `~/.claude/usage/*.jsonl` | Verhaltens-Pattern (Tools, Timing, Frequenz). Schnell parsebar, hohes Signal fuer Arbeitsrhythmus. |
| **3** | NotebookLM Takeout | Projektstrukturierung, Themen-Clustering. Zeigt was Samuel als wichtig genug empfand, um Notebooks anzulegen. |
| **4** | Claude T450s ZIP | Entpacken + mergen mit aktueller History = laengere Zeitreihe. |
| **5** | WhatsApp (erst beschaffen) | Persoenlichster Datenschatz — aber erst vom Handy exportieren. |
| **6** | ChatGPT Export (erst anfordern) | Export anfordern → ca. 24h Wartezeit. |

---

## Naechste Schritte

- [ ] Claude T450s ZIP entpacken und mit `~/.claude/projects/` zusammenfuehren
- [ ] ChatGPT Export anfordern (chatgpt.com → Settings → Data controls)
- [ ] WhatsApp-Chats vom Handy exportieren (.txt Format, ohne Medien)
- [ ] NotebookLM JSON-Struktur stichprobenartig pruefen (1-2 Notebooks)
- [ ] `history.jsonl` Parser schreiben (Collector-Modul Prio 1)

---

## Scout-Ergaenzungen (2026-03-02)

### Zusaetzlich gefundene Quellen

**AI Chat Exports (Claude + OpenCode)**
- Pfad: `/home/smlflg/Orderformyaistuff/AI_Chats/exports/`
- Format: Markdown, 74 Dateien (37x Claude, 37x OpenCode — je full + prompts-only)
- Groesse: 1,1 MB
- Zeitraum: 2026-01-28 bis 2026-02-03
- Bewertung: Sauber exportiert, Zeitraum der fruehen Claude-Code-Nutzung

**Session Analysis Reports**
- Pfad: `/home/smlflg/session_analysis/`
- Groesse: 116 KB
- Enthaelt: MEGA_REPORT.md, GROW_WITH_YOUR_CODE.md, 14 Session-Batches (als .txt)
- Bewertung: Bereits vorverarbeitete Insights — schnellster Einstieg fuer Profiling

**ClaudeAnalysiertMICH (JSX-Analysen)**
- Pfad: `/home/smlflg/Dokumente/ClaudeAnalysiertMICH/`
- Format: JSX (React-Komponenten mit eingebetteten Daten)
- Groesse: 108 KB
- Dateien: blind-spots.jsx, project-evolution.jsx, style-analysis.jsx, turning-points.jsx
- Bewertung: Claude hat Samuels Muster bereits extrahiert — Prioritaet 1 fuer Persoenlichkeitsmodell

**ADHS Selbstdokumentation**
- Pfad: `/home/smlflg/Dokumente/ADHS/`
- Groesse: 21 MB
- Inhalt: Alltag (TAGESSTRUKTUR, HYPERDRIVE-FALLE, 19 NotebookLM-Uploads), Medikation, Notfallplaene
- SENSIBEL: Diagnose/ enthaelt medizinische PDFs (BDI-II, WURS-K, ADHS-Unterlagen)
- Bewertung: Hohes Signal fuer Persoenlichkeit + Arbeitsweise

**Session Logs + Lern-Notizen**
- Pfad: `/home/smlflg/SESSION_LOG.md`, `/home/smlflg/LEARN_2026-03-02.md`
- Zusaetzlich: ARCHITEKTUR_unterbewusstsein.md, RESEARCH_*.md
- Bewertung: Direkteste Quelle — Samuels eigene Reflexionen in eigenen Worten

**3-Laptops Claude Session Archiv**
- Pfad: `/home/smlflg/ClaudesReich/EveryClaudeCodeSessionfromeverydeviceever/`
- Groesse: 1,0 GB
- Inhalt: 896 JSONL-Dateien von Gen16 + MacBookPro16 + T450s, bereits extrahiert
- Bewertung: Historische Tiefe, aber Deduplizierung noetig

### Priorisierung (gesamt, neu sortiert)

| Prio | Quelle | Aufwand | Erwartetes Signal |
|------|--------|---------|-------------------|
| 1 | session_analysis/MEGA_REPORT + GROW_WITH_YOUR_CODE | Null | Fertige Insights |
| 2 | ClaudeAnalysiertMICH/*.jsx | Sehr niedrig | Persoenlichkeitsmuster bereits extrahiert |
| 3 | SESSION_LOG.md + LEARN_2026-03-02.md | Sehr niedrig | Reflexion in eigener Stimme |
| 4 | AI_Chats/exports/ (74 Markdown-Dateien) | Niedrig | Fruehes Nutzungsverhalten |
| 5 | ~/.claude/history.jsonl | Niedrig | Aktuelle Prompts + Projekte |
| 6 | ~/.claude/projects/ (1265 JSONL) | Mittel | Vollstaendige Denkprozesse |
| 7 | ADHS/Alltag/ (Markdown) | Niedrig | Strukturen + Coping-Systeme |
| 8 | ClaudesReich Archive (896 JSONL) | Hoch | Historische Entwicklung |
| 9 | ADHS/Diagnose/ (PDFs) | Hoch | Medizinisch-klinisch |
| 10 | WhatsApp (Export ausstehend) | — | Persoenlichste Quelle, noch nicht verfuegbar |

### Nicht gefunden
- **ChatGPT Export:** Kein conversations.json vorhanden — muss frisch angefordert werden
- **Telegram:** Keine Backup-Dateien gefunden
- **E-Mail-Exports:** Nicht vorhanden
- **Obsidian/Notion:** Kein Vault gefunden
