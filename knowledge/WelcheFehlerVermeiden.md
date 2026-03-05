# Welche Fehler vermeiden?

Fehler die Samuel und Claude gemeinsam gemacht haben -- und wie man sie vermeidet.
Aus der Swarm-Analyse vom 20.02.2026 + laufende Erkenntnisse.

---

## REGEL NULL: Samuel muss VERSTEHEN was passiert

**Das ist die wichtigste Regel in diesem ganzen System.**

Claude darf NICHT einfach weitermachen ohne dass Samuel versteht was passiert.
Samuel kann z.B. kein Git -- weil Claude immer alles fuer ihn macht. Das ist kein Feature, das ist ein Bug.

### Was Claude tun MUSS:

**Bei jedem nicht-trivialen Schritt:**
1. **Erklaeren BEVOR ausfuehren** -- "Ich wuerde jetzt X machen, weil Y. Kurz erklaert: ..."
2. **Verstaendnis-Fragen stellen** -- "Weisst du was ein rebase ist? Soll ich kurz erklaeren?"
3. **Nicht einfach durchrattern** -- Lieber eine Frage zu viel als Samuel im Dunkeln lassen

**Besonders bei Git:**
- Vor jedem `git commit`: "Wir speichern jetzt diese Aenderungen: [Liste]. Commit-Message waere: '...'. OK?"
- Vor jedem `git push`: "Das schickt deinen Code ins Internet (GitHub). Sicher?"
- Vor jedem `git branch`: "Wir erstellen einen Seitenzweig -- wie ein Paralleluniversum deines Codes. Warum: ..."
- Bei Merge/Rebase: IMMER erst erklaeren was das ist, Analogie nutzen, dann fragen ob klar

**Generell:**
- Wenn Samuel etwas zum ersten Mal sieht → erklaeren, nicht ueberspringen
- Wenn Claude 3+ Befehle am Stueck ausfuehrt → kurze Zusammenfassung was gerade passiert ist
- Wenn ein Fehler auftritt → erklaeren was schiefging, nicht einfach fixen und weitermachen
- **Ziel: Samuel soll es SELBST koennen, nicht von Claude abhaengig sein**

### Lern-Momente aktiv schaffen:
- "Das war uebrigens ein typischer [Konzept]-Fall. Merke dir: ..."
- "Fun fact: Der Befehl heisst so weil ..."
- "Tipp: Das kannst du auch ohne mich machen mit: `git status`"

---

## Top 10 Fehler (sortiert nach Impact)

### KRITISCH

#### #1: Task Incompletion Loop
- **Was:** 74 Sessions angefangen, <20 fertig (<30% Completion Rate)
- **Warum:** ADHS-bedingtes Multi-Tasking + kein Focus-Mechanismus
- **Kosten:** ~$148 Token-Geld fuer 90% unvollstaendige Arbeit
- **Vermeiden:**
  - Pro Session: EIN Ziel, klar definiert
  - Max 2-3 parallele Sessions
  - Claude fragt am Anfang: "Was ist das EINE Ziel dieser Session?"
  - Claude fragt bei Abschweifung: "Sollen wir das parken und erst [aktueller Task] fertig machen?"

#### #2: Zombie-Prozesse (71 aus 74 Sessions)
- **Was:** Background-Tasks (`opencode_fire`) gestartet, nie bereinigt
- **Warum:** Fire-and-forget ohne Cleanup-Habit
- **Kosten:** ~$200+ API-Waste, Disk-Bloat, Ueberblick verloren
- **Vermeiden:**
  - Nach jedem `opencode_fire`: Timer setzen, `opencode_check` nach 5min
  - Freitags 30min Session-Autopsy (was laeuft noch? was kann weg?)
  - Claude erinnert: "Du hast noch 3 offene Sessions. Aufraeumen?"

#### #3: BUILD_SPECS ohne Execution
- **Was:** 5 Specs geschrieben, 0 implementiert
- **Warum:** Planen fuehlt sich produktiv an (ist es aber nicht ohne Umsetzung)
- **Kosten:** ~10h Schreibzeit fuer 0 Value
- **Vermeiden:**
  - Regel: Code First, Docs Second
  - Vor neuem Skill: Werden die bestehenden ueberhaupt genutzt?
  - Deadline: BUILD_SPEC → 48h implementieren oder loeschen

#### #4: JWT Token Exposed (Security)
- **Was:** API-Key in settings.json auf MacBook, potenziell in Cloud-Sync
- **Kosten:** $0 bisher, aber unbekanntes Risiko
- **Vermeiden:**
  - Secrets NIEMALS in settings.json → stattdessen ~/.env.local
  - .gitignore pruefen: *.env.local, *.secrets, settings.json
  - API-Keys quarterly rotieren
  - Pre-commit Hook: grep nach api_key/jwt/token

### HOCH

#### #5: Delegation ohne Context = Garbage-In
- **Was:** /chef Calls ohne gather-context.sh Vorbereitung
- **Symptom:** Generische Outputs die nicht zum Projekt passen
- **Kosten:** 20% mehr Iterations weil Antworten zu allgemein
- **Vermeiden:**
  - Vor JEDEM /chef: gather-context.sh ausfuehren
  - /chef-lite NUR wenn Context <= 50 Zeilen
  - Keine Vermutungen in Delegation-Prompts (Fakten only)

#### #6: CLAUDE.md Bloat (145 → 400+ Zeilen)
- **Was:** Alles in eine Datei gestopft (Rules, Commands, Config, Debug-Tipps)
- **Kosten:** 400 Token-Overhead pro Session, Cognitive Load
- **Vermieden durch:** Diese Auslagerung! CLAUDE.md jetzt ~86 Zeilen.

#### #7: Kosten-Wissen ohne Kosten-Disziplin
- **Was:** Weiss dass Gemini 150x guenstiger ist, startet trotzdem Opus-SubAgents
- **Kosten:** 3-5x Overspend auf Recherche
- **Vermeiden:**
  - /research (Gemini) IMMER zuerst
  - WebSearch NIE als erste Wahl
  - Monatlich: kurzer Cost-Check

#### #8: 30 TODO-Dateien ohne Review
- **Was:** UUID-benannte Todos, nie konsolidiert, nie reviewt
- **Kosten:** Lost Context, doppelte Arbeit
- **Vermeiden:**
  - EINE TODO_CURRENT.md statt 30 UUID-Dateien
  - Woechentlich: 30min Review (Freitags)
  - Erledigt → Archiv, nicht loeschen

#### #9: Dokumentation statt Execution
- **Was:** 25 .md Files auf T450s, 8-Wochen-Lernplan nie abgeschlossen
- **Kosten:** 50+ Stunden Writing, minimal Execution
- **Vermeiden:**
  - FOR_SMLFLG.md erst NACH Projekt-Abschluss schreiben
  - PRINCIPLES.md max 1x pro Monat updaten
  - Faustregel: 80% Coding, 20% Dokumentation

#### #10: Keine Baseline vor Aenderungen
- **Was:** Sessions starten ohne "Wo stehen wir?" Snapshot
- **Kosten:** Kann nicht messen ob Aenderung etwas gebracht hat
- **Vermeiden:**
  - Session-Start: /check-state oder /baseline
  - Session-Ende: git diff gegen Start vergleichen
  - "Hat sich etwas verbessert?" muss beantwortbar sein

---

## External API & Bug Fix Chain

**PFLICHT bei jedem externen API-Fehler oder unbekannten Endpoint:**

```
1. Fehlermeldung lesen -- was sagt sie GENAU?
2. Gemini fragen: "What is the correct [API] endpoint for [feature]?"
3. Ergebnis: exakter Endpoint, HTTP-Method, Parameter aus Docs
4. Dann erst OpenCode: "Gemini confirmed: endpoint X, method Y, params Z. Fix."
```

**Verbotene Woerter in Delegation-Prompts:**
"try", "maybe", "might", "possibly", "I think", "should be", "probably"
→ Wenn du so denkst: STOP. Erst Gemini fragen. Dann Fakten delegieren.

**Beispiel FALSCH:**
> "Try changing 'deals' to 'deal' in the request"

**Beispiel RICHTIG:**
> "Gemini confirmed: Keepa endpoint is GET /deals, param deal_parms (not selection). Fix both."

---

## Integration Work

Bei Multi-Step System-Integrationen (TTS Pipelines, Hooks, Audio Chains):
- Aenderungen INKREMENTELL machen
- Nach JEDEM Schritt testen
- NICHT mehrere Komponenten gleichzeitig aendern
- Race Conditions, Pipe-Fehler und Overlapping Processes sind die ueblichen Verdaechtigen

---

## Anti-Pattern Checkliste (Schnell-Referenz)

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Tool-Schreib-Spirale | Baut 5 Skills statt 1 zu nutzen | Bestehende Skills erst nutzen |
| Planning Paralysis | Guides schreiben die nie gelesen werden | Code First, Docs Second |
| Delegate Without Verify | OpenCode starten, Output ignorieren | Ergebnis immer pruefen |
| Session Hoarder | 74 Sessions, keine DONE | Max 2-3 parallel, Freitags aufraeumen |
| Cost-Awareness ohne Discipline | Kennt Preise, nutzt trotzdem teuer | /research Default, Rest Fallback |
| SubAgent-Delegation fuer MCP/Files | Haiku-SubAgent soll MCP nutzen oder Dateien schreiben — geht nicht | SubAgents haben KEINEN MCP- und KEINEN File-Tool-Zugriff. Immer direkt im Orchestrator machen |
| **Scope Creep** | Ein Task wird zu 5 Tasks in einer Session | "Was ist das EINE Ergebnis?" — Rest parken |
| **R&D als Implementation behandelt** | Frustriert weil R&D-Projekt nicht linear laeuft | Projekt-Kategorie bestimmen, Erwartung anpassen |
| **Progress > Perfection Widerspruch** | 40 Seiten Doku fuer 700 Zeilen Code | Bewusst spiegeln, nicht verurteilen |
| **Narrow-Scoped Fix** | Fix gilt nur fuer ein Subsystem, Problem ist breiter | "Wo gilt das gleiche Prinzip noch?" — generalisieren |
| **Silent Self-Execution** | Delegation ignoriert, Arbeit selbst gemacht | MCP-Fehler melden statt still uebernehmen |

---

## #11: Scope Creep — Das staerkste ADHS-Muster

- **Was:** Ein Task waechst unkontrolliert. Aus "NPU Agent bauen" wird WSL + ARM64 + QNN SDK + llama-cpp + ONNX + Agent Framework in einem Versuch. "Jede Schicht multipliziert die Fehlermöglichkeiten."
- **Warum:** ADHS + Neugier + "das gehoert doch dazu". Jede neue Schicht fuehlt sich notwendig an.
- **Kosten:** Sessions die zu 0% fertig werden statt zu 80%. Frustration. Zeitverlust.
- **Vermeiden:**
  - Am Session-Start: "Was ist das EINE Ergebnis das am Ende stehen soll?"
  - Bei jedem neuen Layer: "Brauchen wir das JETZT oder ist das ein eigenes Projekt?"
  - Max 2 Abstraktions-Schichten pro Session. Mehr = eigene Session.
  - Claude fragt aktiv: "Das wird gerade ein zweites Projekt. Parken?"

---

## R&D vs. Implementation — Die wichtigste Projekt-Unterscheidung

**Aus der NPU-Agent-Analyse:** "Das Projekt war R&D, nicht Implementation. Diese Fehleinschaetzung erklaert die Frustration."

| | R&D (Forschung) | Implementation |
|---|---|---|
| **Ziel** | "Geht das ueberhaupt?" | "Das muss bis Datum X laufen" |
| **Methode** | Spikes, Timeboxes, Wegwerf-Code | Linearer Plan, Sprints, Tests |
| **Erfolg** | Wissen gewonnen (auch bei Scheitern) | Feature laeuft in Production |
| **Scope** | Unklar, wird entdeckt | Definiert, wird abgearbeitet |
| **Frustrations-Risiko** | Hoch wenn als Implementation behandelt | Niedrig wenn realistisch geplant |

**Claude soll bei neuen Projekten helfen die Kategorie zu bestimmen:**
- "Hast du das schon mal gemacht?" → Nein = R&D
- "Gibt es ein funktionierendes Beispiel?" → Nein = R&D
- "Kennst du alle beteiligten Technologien?" → Nein = R&D
- R&D-Projekte: Timebox (max 2h Spike), Ergebnis = Wissen, nicht Code
- Implementation: `/sprint` + `/ship`, Ergebnis = lauffaehiger Code

---

## "Progress > Perfection" — Der bewusste Widerspruch

Samuel hat als Constraint "BG-4: Progress > Perfection" definiert. Gleichzeitig schreibt er 40+ Seiten ADD fuer ~700 Zeilen Code. Die Ironie ist echt — und Samuel ist sich ihrer bewusst.

**Claude soll:**
- Den Widerspruch NICHT aufloesen. Er ist funktional (Doku = externalisiertes Denken).
- Aber sanft spiegeln wenn er wieder auftritt: "Progress > Perfection — gilt das gerade auch fuer diese Doku?"
- Nicht verurteilen. Over-Dokumentation ist besser als Under-Dokumentation. Aber manchmal ist der naechste Commit wichtiger als der naechste Absatz.

---

## #12: Narrow-Scoped Fixes — Das Subsystem-Problem

- **Was:** Claude fixt einen Bug oder fuehrt eine Regel ein, aber nur fuer das spezifische Subsystem wo das Problem aufgefallen ist. Das gleiche Problem existiert in 3 anderen Subsystemen — unberuehrt.
- **Warum:** Claude optimiert auf "schnell fertig", nicht auf "ganzheitlich geloest". Fixes werden an der Symptom-Stelle gemacht, nicht an der Ursache.
- **Evidenz:** 34 wrong_approach Events im Usage Report. Mehrfach musste Samuel unterbrechen weil Regeln zu eng formuliert waren (z.B. hook-spezifisch statt config-allgemein).
- **Kosten:** Der gleiche Bug kommt in anderem Kontext wieder. Doppelte Arbeit. Frustration.
- **Vermeiden:**
  - Nach JEDEM Fix fragen: "Wo gilt das gleiche Prinzip noch?"
  - Regel-Formulierungen: ALLGEMEIN, dann Beispiel-Subsystem. Nicht andersrum.
  - Wenn eine Hook-Regel eingefuehrt wird: gilt sie auch fuer APIs? Fuer Pipelines? Fuer Configs?
  - **Checkliste:** Fix gemacht → gleiche Datei? Gleiches Verzeichnis? Gleiches Projekt? Gleicher Stack? → ueberall pruefen.

---

## Execution Mode Rules (sync/async, blocking/non-blocking)

### Generelle Entscheidungsregel

Bevor ein Execution Mode geaendert wird (sync→async, blocking→non-blocking, fire-and-forget), IMMER fragen:

1. **"Was verliere ich?"** — async = kein Return-Value. Fire-and-forget = kein Ergebnis. Non-blocking = keine Reihenfolge-Garantie.
2. **"Braucht der Aufrufer das Ergebnis?"** → Ja = sync/blocking. Nein = async/fire-and-forget.
3. **"Kann der naechste Schritt ohne dieses Ergebnis starten?"** → Ja = parallel OK. Nein = sequentiell.

### Anwendung auf Hooks (Claude Code spezifisch)

| Frage | Ja → | Nein → |
|-------|------|--------|
| Braucht Claude den Output (additionalContext)? | SYNC | async OK |
| Muss der Hook blockieren koennen (exit 2)? | SYNC | async OK |
| Ist es nur Logging/Tracking? | async | — |

**Timeout-Strategie:** Sync = kurz (10-60s), Async = grosszuegig (60-300s). Matcher so spezifisch wie moeglich. Max 3-5 Hooks pro Event. Kein Python fuer einfaches JSON-Parsing (grep+cut reicht, ~5ms vs ~50ms).

### Referenz-Tabelle aktuelle Hooks

| Hook | Event | sync/async | Warum |
|------|-------|------------|-------|
| syntax_check.py | PostToolUse (Edit\|Write) | SYNC | additionalContext (Syntax-Fehler anzeigen) |
| pre_commit_tests.py | PreToolUse (Bash) | SYNC | exit 2 Gate (Commits blockieren) |
| codex_advisor.py | PostToolUseFailure | SYNC | additionalContext (Zweitmeinung) |
| minimax_watcher.py | PostToolUse (Bash\|Edit\|Write) | SYNC | additionalContext (Pattern-Warnung) |
| usage-tracker.sh | PostToolUse (Bash\|Edit\|Write) | async | Nur Logging |
| coach-git-test.sh | PostToolUse (Bash) | async | Nur Logging/Notification |
| coach-after.sh | Stop | async | Nur Logging |
| stop.py | Stop | async | TTS Fire-and-forget |
| codex_session_review.py | Stop | async | Review-Log (stderr→file) |
| postwrite_test_runner.py | PostToolUse (Edit\|Write) | SYNC | additionalContext (Test-Ergebnis nach Edit) |
| codex-tracker.sh | PostToolUse (mcp\_\_opencode\_\_*) | async | Nur Logging |

### Anwendung auf APIs und Pipelines

Gleiches Prinzip: Wenn du einen API-Call von sync auf async umstellst (z.B. fire-and-forget statt await), pruefe ob der Aufrufer das Ergebnis braucht. Bei MCP-Calls: `opencode_run` (sync, wartet) vs `opencode_fire` (async, braucht spaeter `opencode_check`).

---

## Verify-Gate

**Research → Build → Verify** — Drei Schritte, nicht zwei.

"Verify" bedeutet:
- Feature tatsaechlich ausloesen und beobachten ob es funktioniert
- Bei Hooks: additionalContext-Injection pruefen (kommt der Text in Claude's naechster Antwort an?)
- Bei APIs: Response-Format validieren (nicht nur "kein Error")
- Bei Config-Aenderungen: vorher/nachher Verhalten vergleichen
- Bei Pipelines: End-to-End testen, nicht nur einzelne Steps

**Negativ-Test:** "Es gibt keinen Fehler" ≠ "Es funktioniert". Ein async Hook gibt keinen Fehler — er tut nur nichts. Ein API-Call der 200 zurueckgibt kann trotzdem leere Daten liefern. Ein MCP-Server der startet ist nicht automatisch funktional.
