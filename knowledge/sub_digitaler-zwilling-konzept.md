# Digitaler Zwilling — Konzept-Dokument

**Date:** 2026-03-02
**Agent:** digital-twin-agent
**Status:** Entwurf v1

---

## 1. Was existiert bereits — Marktüberblick

### Moltbot / OpenClaw (ehem. Clawdbot)
- **Was:** Self-hosted AI Agent, "Claude with hands" — nicht nur Chat, sondern Aktionen
- **Persistenz:** `~/.clawdbot/` mit `USER.md` (was er über dich weiss), `SOUL.md` (Persönlichkeit), `memory/` Ordner
- **Prinzip:** Plain Markdown als Source of Truth — lesbar, versionierbar, lokal
- **Heartbeat Engine:** Cron-basiert, proaktiv (Morning Briefings, Erinnerungen ohne Prompt)
- **Problem:** ~60k GitHub Stars, viel Hype, aber: Fokus auf Task-Execution, NICHT auf Lernprozesse aus digitalen Aufzeichnungen
- **GitHub:** [OpenClaw](https://openclaw.ai/)

### Mem0 / Letta (MemGPT)
- **Mem0:** Hybrid Vector DB + Graph DB, automatische Fakt/Präferenz-Extraktion
- **Letta:** OS-inspirierte Memory-Hierarchie (Core Memory / Archival / Recall)
- **Problem:** Reaktiv — warten auf Prompts, kein proaktives Lernen aus bestehenden Artefakten

### Stanford Generative Agents (Smallville)
- **Drei-Tier-Memory:** Stream → Reflection → Planning
- **Reflection-Trigger:** wenn `sum(recent_importance_scores) > THRESHOLD` → Synthese, höhere Insights
- **Direkte Analogie:** REM-Schlaf-Konsolidierung
- **Problem:** Simulation, nicht auf echte User-Daten angewendet

### Was ALLE gemeinsam fehlen

> **Kein existierendes System lernt proaktiv aus deinen eigenen digitalen Artefakten.**
> Alle Systeme sind reaktiv: sie warten auf Prompts oder neue Inputs.
> Niemand schaut sich deine Claude Sessions, Git Commits, Usage Logs an und synthesiert daraus ein Bild von dir.

---

## 2. Samuels System — Was es anders macht

### Der entscheidende Unterschied: Die Datenbasis

Samuel trackt bereits ALLES:

| Artefakt | Wo | Was drin steckt |
|---|---|---|
| Claude Sessions | `~/.claude/` (intern) | Entscheidungsmuster, Frustrationspunkte, Workarounds |
| Usage Logs | `~/.claude/usage/YYYY-MM-DD.jsonl` | Welche Tools wann, Kosten, Häufigkeiten |
| Git Commits | `~/Projekte/*/` | Was wirklich gebaut wurde vs. was geplant war |
| Coaching Hooks | `~/.claude/hooks/coaching/` | Micro-Learnings im Moment |
| MEMORY.md | `~/.claude/projects/*/memory/` | Explizit gespeichertes Wissen |
| SESSION_LOG.md | In Projekten | Recap + Learn Einträge |
| Produktivitätsmuster | Usage + Zeit-Stamps | Morgens schärfer, abends kreativer |

**Kein anderes Personal AI Tool hat diese Datenbasis.**
Moltbot kennt deinen Namen und bevorzugten Kaffee. Samuels Zwilling könnte deine ADHS-Muster erkennen.

### Das Oktopus-Modell als Architektur

Samuels eigene Metapher gibt die Architektur vor:

```
KOPF (Samuel)
    ↕ bewusste Steuerung
UNTERBEWUSSTSEIN (Zwilling)
    ↕ automatische Verarbeitung
ARME (Agents)
    ↕ Ausführung + Reporting
```

Der Zwilling LEBT zwischen Samuel und den Agents.
Er beobachtet, lernt, antizipiert — ohne gefragt zu werden.

---

## 3. Wie der Zwilling aus Samuels digitalen Aufzeichnungen lernt

### Schicht 1 — Rohdaten-Ingestion (täglich)

```python
# Crawler läuft als systemd service oder cron
sources = [
    UsageLogCrawler("~/.claude/usage/*.jsonl"),      # Tool-Nutzung
    GitCommitCrawler("~/Projekte/**/.git/"),          # Was gebaut wurde
    MemoryCrawler("~/.claude/projects/*/memory/"),    # Explizites Wissen
    SessionLogCrawler("~/Projekte/*/SESSION_LOG.md"), # Recap/Learn Einträge
    CoachingLogCrawler("~/.claude/hooks/coaching/"),  # Micro-Learnings
]
```

### Schicht 2 — Importance Scoring (Stanford-Modell)

Jedes Artefakt bekommt einen Score 1-10:
- **10:** "Ich habe erkannt dass ich Session-Sprawl betreibe" (Selbsterkenntnis)
- **7:** Neues Muster in Tool-Nutzung
- **4:** Routine-Commit
- **1:** Dupliziertes Memory

### Schicht 3 — Nacht-Konsolidierung ("Träumen")

Wenn `sum(recent_scores) > THRESHOLD`:
```
Trigger: täglich 3 Uhr morgens
Input: letzte 24h high-score Artefakte + bestehende Profile
Prozess: LLM synthesiert → findet Muster → aktualisiert samuel-profil.md
Output:
  - samuel-profil.md Diff (was sich geändert hat)
  - neue Insights in MEMORY.md
  - optional: Morning Briefing für Samuel
```

### Schicht 4 — Proaktive Surfacing (ReLU-Filter)

Samuels eigenes ReLU-Prinzip anwenden:
- Insights unter Threshold → verwerfen
- Insights über Threshold → Samuel in nächster Session proaktiv zeigen
- Beispiel: "Gestern hast du 3 Sessions gestartet ohne vorher /learn zu machen. Ist dir das aufgefallen?"

### Konkrete Lernbeispiele

**ADHS-Pattern-Erkennung:**
- Usage Logs: 23 Uhr Session-Start, viele kurze Tool-Calls, kein /recap
- Git: Commits enthalten "WIP", "fix", "test" aber selten strukturierte Messages
- Zwilling lernt: Abend-Sessions = kreativ aber incomplete

**Kompetenz-Tracking:**
- Git Commits über 3 Monate: mehr spezifische `git add` statt `-A`?
- Dann: "Du machst Fortschritte mit Git — du nutzt jetzt 40% öfter spezifische Pfade"

**Session-Sprawl-Früherkennung:**
- Usage Logs: heute bereits 4 Sessions, keine mit /recap abgeschlossen
- Zwilling: "Warning: Session-Sprawl-Pattern erkannt. Soll ich /recap starten?"

---

## 4. Verbindung zum Unterbewusstsein-Framework

Das Subconsciousness Framework (laut RESEARCH_subconsciousness_framework.md) definiert:

| Unterbewusstseins-Prozess | Zwilling-Entsprechung |
|---|---|
| Mustererkennung | Vector-Embeddings auf Usage Logs + Git |
| Background Processing | systemd daemon, läuft 24/7 |
| Trainierte Intuition | Profil wächst durch Konsolidierung |
| Traum-Konsolidierung | Nacht-Batch (3 Uhr), Stanford-Reflection |
| Priming/Assoziation | Morning Briefing mit relevantem Kontext |
| Salienz/Aufmerksamkeit | Importance Scoring 1-10 |
| ReLU-Filter (Samuel) | Threshold-basierte Proaktivität |

**Der Zwilling IST das Unterbewusstsein.**
Er macht die impliziten Muster explizit — genau wie das Unterbewusstsein unbewusste Prozesse ins Bewusstsein hebt.

### LIDA-Global-Workspace-Analogie

Das Subconsciousness Framework nennt LIDA als Referenz: Viele parallele Codelets konkurrieren um Aufmerksamkeit, der Gewinner wird "bewusst".

Im Zwilling:
```
Codelets = spezialisierte Analyzer (Git-Analyzer, Usage-Analyzer, Memory-Analyzer)
Global Workspace = samuel-profil.md + MEMORY.md
Bewusstsein = Morning Briefing / proaktive Hinweise in Sessions
```

---

## 5. Build vs. Buy — Empfehlung

### Buy/Adopt (sofort nutzbar)

| Tool | Für was | Kosten |
|---|---|---|
| **Moltbot/OpenClaw** | Basis-Infrastruktur: Gateway, Heartbeat, Markdown-Persistenz | Open Source |
| **Mem0** | Automatische Fakt-Extraktion aus neuen Inputs | Open Source + Cloud |
| **mcp-memory-service** | MCP-Integration für Claude + Knowledge Graph | Open Source |

**mcp-memory-service** ist besonders relevant: "Open-source persistent memory for AI agent pipelines + Claude. REST API + knowledge graph + autonomous consolidation."
→ [GitHub](https://github.com/doobidoo/mcp-memory-service)

### Build (Samuels Unique Value)

Was es NICHT gibt und Samuel bauen muss:

1. **Claude-Session-Crawler** — kein Tool liest und analysiert Claude-interne Logs
2. **Usage-Pattern-Analyzer** — `~/.claude/usage/YYYY-MM-DD.jsonl` → Verhaltensprofile
3. **Git-Commitment-Tracker** — `git log` → Kompetenz-Entwicklung über Zeit
4. **Nacht-Konsolidierungs-Agent** — systemd + LLM → `samuel-profil.md` Update
5. **ReLU-Filter** für proaktive Hinweise — Samuels eigenes Prinzip

### Empfehlung: Hybrid-Ansatz

```
Phase 1 (MVP, 1 Woche):
  → mcp-memory-service als MCP-Server konfigurieren
  → Usage-Log-Crawler schreiben (Python, ~100 Zeilen)
  → Nacht-Cron der samuel-profil.md aktualisiert

Phase 2 (2-3 Wochen):
  → Git-Analyzer integrieren
  → Importance-Scoring implementieren
  → Morning Briefing via claude hook

Phase 3 (Monat 2):
  → Moltbot/OpenClaw als Gateway
  → Mobile-Access via Telegram
  → Vollständige Konsolidierungsschleife
```

**Build > Buy für den Kern.**
Niemand sonst hat Samuels Datenbasis. Die Infrastruktur (Memory-Service, Gateway) kaufen/adopten — die Seele selbst bauen.

---

## 6. Nächste konkrete Schritte

1. `mcp-memory-service` evaluieren und als MCP-Server einrichten
2. Python-Skript: `~/.claude/usage/*.jsonl` → Tages-Profil generieren
3. Erster Nacht-Cron: `samuel-profil.md` mit Usage-Daten anreichern
4. Pilot-Session: Zwilling in Morning-Hook einbauen → "Gestern: X Sessions, Y /learn-Einträge"

---

## Quellen

- [From Clawdbot to Moltbot: C&D and the Chaos](https://dev.to/sivarampg/from-clawdbot-to-moltbot-how-a-cd-crypto-scammers-and-10-seconds-of-chaos-took-down-the-4eck)
- [Moltbot Persistent Memory Architecture](https://openclaw.ninja/blog/persistent-memory)
- [Falling in and out of love with Moltbot](https://www.platformer.news/moltbot-clawdbot-review-ai-agent/)
- [Moltbot Memory Architecture - Daily Notes and Long-Term Memory](https://zenvanriel.nl/ai-engineer-blog/moltbot-memory-architecture-guide/)
- [Agentic AI: OpenClaw/MoltBot Memory Architecture Explained](https://medium.com/@shivam.agarwal.in/agentic-ai-openclaw-moltbot-clawdbots-memory-architecture-explained-61c3b9697488)
- [mcp-memory-service GitHub](https://github.com/doobidoo/mcp-memory-service)
- RESEARCH_subconsciousness_framework.md (lokal, 2026-03-02)
- samuel-profil.md (lokal, aktuell)
