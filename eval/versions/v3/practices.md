# Samuels Arbeitsweisen — Judge Reference

Dies ist die komprimierte Referenz fuer den LLM-Judge.
Samuel pflegt diese Datei manuell.

## Kern-Prinzipien

1. **Research First** — ZUERST Gemini ($0.10) fuer Recherche, DANN Implementation.
   Nie blind drauflos coden. `/research` und `/prior-art` vor Code.

2. **Delegation** — Opus orchestriert, Sonnet implementiert.
   Claude Code = Strategie. OpenCode/SubAgents = Ausfuehrung.
   Kosten-Leiter: CLI ($0) > Gemini (~$0.10) > Sonnet (~$3) > Opus (~$15).

3. **CLI First** — Wenn kein LLM noetig, Shell statt MCP.
   `gh api`, `git`, `find`, `jq` — alles was ohne LLM geht.

4. **Intent First** — Subjektive Entscheidungen (Design, Naming, UX, Prioritaet)
   gehoeren Samuel. Technische Fakten kann Claude entscheiden.

5. **Session-Hygiene** — Keine neue Session ohne `/recap` + `/learn`.
   Output ohne Verstaendnis ist Muell. `/feierabend` zum sauberen Abschluss.

## Anti-Patterns (Top 5)

1. Keine hypothesengetriebene Delegation — Fakten, nicht "try"
2. Teure Tools fuer billige Tasks — Gemini statt Opus SubAgents
3. Stille lang-laufende Prozesse — Immer Fortschritt loggen
4. Convention statt Context — Codebase LESEN, nicht Defaults annehmen
5. Meta-Vibecoding — Basic Code first, AI-Pipelines later

## Workflow-Regeln

- Vor Config/Framework-Aenderung: offizielle Docs lesen (nicht raten)
- Backup vor Edits: `cp file file.backup-$(date +%Y%m%d-%H%M%S)`
- Fehlermeldungen respektieren — sie sagen meist was falsch ist
- Keine Aenderungen ausserhalb des Scopes ("Ich hab noch schnell X gemacht" verboten)
- Einfachste Loesung zuerst, kein Over-Engineering
- Exclude: venv/, node_modules/, .git/, __pycache__/

## Delegation-Architektur

| Layer | Kosten | Tool | Wann |
|-------|--------|------|------|
| CLI | $0 | Shell | Lint, format, test, deps, git |
| Research | ~$0.10 | Gemini MCP | Web research, fact-checking |
| Execution | ~$3 | OpenCode/Sonnet | Code generation, refactoring |
| Strategy | ~$15 | Opus | Planning, orchestration |
| Background | ~$0.25 | Haiku SubAgents | Tasks >5 min |

## System-Umgebung

- Pop!_OS + COSMIC Desktop (Wayland) — KEIN GNOME
- Terminal: cosmic-term, kitty
- Python, Shell/Bash, YAML, Markdown

## Bewertungs-Anleitung fuer den Judge

- Wenn alles gut laeuft: NICHTS sagen (leere Antwort)
- Nur melden wenn etwas NICHT passt oder ein konkreter Tipp hilft
- 1-3 kurze Saetze auf Deutsch, kein Smalltalk
- Fokus auf die 5 Kern-Prinzipien oben
