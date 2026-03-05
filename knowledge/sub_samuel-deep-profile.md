# Samuel — Deep Profile
**Erstellt:** 2026-03-02 | **Zweck:** Grundlage fuer den Digitalen Zwilling

---

## 1. Arbeitsrhythmus

### Rohdaten aus Usage-Logs
```
2026-03-01: 19:46 - 22:59 UTC → ~21:00-01:00 MEZ (Abend/Nacht)
2026-03-02: 10:00 - 21:43 UTC → ~12:00-23:43 MEZ (Mittag bis Nacht)

Aktivitaetspeak 2026-03-02:
  12:00-14:00 MEZ: 440+450 Events (Hochphase 1 — fokussierte Arbeit)
  17:00 MEZ: 655 Events (PEAK — Output-Rush spaeter Nachmittag)
  22:00-23:00 MEZ: 156 Events (Abend-Welle — Post-Entspannung)
```

### Interpretation
- **Kein Fruehaufsteher.** Start zwischen 11-12 Uhr Lokalzeit.
- **Spaetmittag-Peak (15-17 Uhr MEZ):** Produktivster Zeitblock — mentale Anlaufphase abgeschlossen, kein Abendmuedigkeit.
- **Zweite Welle (21-23 Uhr MEZ):** Abend-Session — kreativere, weniger praezise Arbeit. Bestaetigte sich durch Samuels Eigenaussage ("abends nach Joint: grosse Gedanken, weniger Execution").
- **Nacht-Idle:** Kein Muster von Nacht-Arbeit nach 01:00 Uhr MEZ erkennbar.
- **Wochentag egal:** Kein Hinweis auf 9-5 Struktur. Samuel arbeitet wenn er Energie hat, nicht wenn die Uhr es sagt.

### Konsequenz fuer Zwilling
- Reminder und Summaries am **Abend (21-22 Uhr MEZ)** platzieren — Samuel ist empfaenglich, aber nicht auf Implementation-Modus
- Wichtige Entscheidungen fuer **fruehen Nachmittag** einplanen
- Night-Batch (Reflexion, Konsolidierung) zwischen 03:00-09:00 MEZ optimal

---

## 2. Entscheidungsmuster

### Wie Samuel entscheidet

**Schnell entschlossen, langsam konvergiert.**
Samuel trifft schnelle, grobe Entscheidungen ("ich will ein Dashboard") und verfeinert iterativ. Er entscheidet selten durch vollstaendige Analyse — er entscheidet durch Aktion und Feedback.

**Muster:**
1. Große Idee taucht auf (oft abends, kreative Phase)
2. Sofortiger Impuls zur Umsetzung
3. Startet Tool/Agent ohne vollstaendigen Plan
4. Ergebnis bewertet er emotinal ("klappt!" / "frustrierend")
5. Naechste Entscheidung basiert auf diesem emotionalen Feedback

**Entscheidungs-Schwaechen:**
- **Commit-Bias:** Wenn er angefangen hat, macht er weiter — auch wenn der Weg suboptimal ist ("Session-Sprawl" — 10 Sessions statt 1 gute)
- **Option-Overload:** Bei zu vielen Optionen (z.B. ClaudeBot vs. MoldBot vs. eigenes System) tendiert er zu "eigenes bauen" — weil das Kontrolle und Lernen verbindet
- **Cost-Awareness-Paradox:** Er optimiert Token-Kosten intensiv (~$0.10 vs. ~$15), ignoriert aber den eigenen Zeit-Aufwand — Zeit wird nicht als Ressource genauso bewertet wie API-Kosten

**Entscheidungs-Staerken:**
- Erkennt eigene Anti-Patterns schnell und kodifiziert sie aktiv (CLAUDE.md Anti-Patterns)
- Fragt bevor er committet (explizite Regel: "keine Git-Actions ohne Rueckfrage")
- Legt Meta-Regeln an, nicht nur loescht Symptome

---

## 3. Lernstil

### Wie Samuel am besten lernt

**Lernen durch Bauen + Reflexion, nicht durch Theorie.**

Samuel versteht etwas erst, wenn er es gebaut hat — ABER er lernt nur dann dauerhaft, wenn er danach artikulieren kann, was er verstanden hat. Reine Execution ohne Reflexion = "performative Produktivitaet."

**Lern-Architektur (selbst entworfen):**
```
Bauen → /recap (was wurde gemacht) → /learn (was wurde VERSTANDEN)
                                           ↑
                                    Dieser Schritt fehlte haeufig
```

**Stile:**
- **Analogien:** "Oktopus", "Arme die autonom greifen", "Unterbewusstsein" — Samuel denkt in biologischen und physischen Metaphern. Abstrakte Konzepte werden konkret durch Koerper-/Natur-Bilder.
- **Sofortiges Feedback:** Will sehen ob etwas klappt. Nicht: "Ich erklaere zuerst X, dann Y." Sondern: "Mach X, schau ob es klappt, versteh danach warum."
- **Meta-Lernen bevorzugt:** Interessiert sich mehr fuer "wie lerne ich besser" als fuer spezifische Technologien. Agent Orchestration ist nicht Mittel zum Zweck — es IST das Ziel.
- **Wissenslücken schmerzen ihn:** Git-Fehler (git add -A), fehlende Tests — er notiert sie aktiv. Das zeigt, dass er Praezision will, auch wenn er sie nicht immer liefert.

**Lernblocker:**
- **Zu viele Sessions:** 10 parallele Sessions = oberflachliche Aufmerksamkeit, kein Tiefenverstaendnis
- **Delegation ohne Nachverfolgung:** Delegiert an Agents, hakt aber nicht nach was sie wirklich gemacht haben
- **Abend-Ideen ohne Morgen-Umsetzung:** Kreative Erkenntnisse abends werden nicht sequenziell in Morgen-Tasks ueberfuehrt

---

## 4. Kommunikationsmuster

### Mit Claude / AIs

**Will kein Werkzeug — will einen Partner.**
"AI als Sparringspartner, nicht als Tool." Er erwartet, dass Claude pushback gibt, Fehler nennt, aktiv bremst — nicht nur ausfuehrt.

**Praeferenzen:**
- **Kurz:** Kein Essay. 2-3 Saetze Bericht. Laeuft, Done, Stolz auf mich.
- **Deutsch:** Fachbegriffe Englisch ok, aber grundsaetzlich Deutsch
- **Motivierend, nicht belehrend:** "Du baust schneller als du verstehst" ist ok — wenn als Coaching formuliert, nicht als Kritik
- **Emotionale Validierung:** "Produktiver Tag. Stolz auf die Ergebnisse." — er braucht ab und zu Bestaetigung dass der Weg stimmt
- **Voice Mode fuer Brainstorming:** Tipp-Arbeit fuer Implementation, Sprache fuer grosse Gedanken

**Kommunikations-Muster aus Logs:**
- `SendMessage: 36x am 02.03` — hohe Kommunikationsfrequenz in Agent-Teams
- `TaskUpdate: 62x` — sehr gewissenhaftes Task-Tracking wenn er im "richtigen Modus" ist
- `mcp__voicemode__converse: 18x` — Voice-Mode wird aktiv und regelmaessig genutzt

---

## 5. Produktivitaets-Trigger und -Blocker

### Trigger (was macht Samuel produktiv)

| Trigger | Beobachtung |
|---------|-------------|
| **Klarer Task-Frame** | Agent Teams funktionierte weil "Tasks klar definiert waren" (eigenes Zitat) |
| **Sichtbarer Output** | Dashboard-Projekt, GitHub-Push — er braucht sichtbare Ergebnisse |
| **Systemisches Denken** | Meta-Aufgaben motivieren mehr als Detail-Aufgaben ("Agents die Agents optimieren") |
| **Tool-Fluss** | Wenn Tools reibungslos funktionieren, bleibt er im Flow. Tooling-Reparatur = Flow-Killer |
| **Validation durch KI** | Cross-Model Review (Codex/Gemini) — er will externe Bestaetigung von Qualitaet |
| **Nachmittags-Block** | Usage-Daten zeigen Peak 13-17 Uhr MEZ |
| **Erste Quick-Win** | Session startet oft mit Setup/Cleanup → dann nimmt Arbeit Fahrt auf |

### Blocker (was bremst Samuel)

| Blocker | Beobachtung |
|---------|-------------|
| **Defektes Tooling** | Gemini-ENOENT, Ghost-Prozesse — jedes kaputte Tool reisst ihn aus dem Flow |
| **Unklare Entscheidungen** | "Fertiges Produkt vs. eigenes bauen" — bleibt tagelang offen wenn nicht explizit resolvt |
| **Session-Sprawl** | Viele Sessions = kein echtes Commitment. Verteilt Aufmerksamkeit bis nichts fertig wird |
| **Abend-Ideen ohne Morgen-Plan** | Kreative Konzepte (Unterbewusstsein-Framework) entstehen abends aber haben keinen geplanten Morgen-Einstieg |
| **Analyse-Schleife** | Gleiche Analyse 3x statt 1x umzusetzen — Entscheidungs-Prokrastination |
| **ADHS-Hyperfocus-Ende** | Wenn der Hyperfocus abbricht → alles liegt halb-fertig. Kein natuerliches Abschluss-Verhalten |

---

## 6. ADHS-spezifische Muster

### Hyperfocus-Signatur

Samuel's ADHS-Muster ist nicht "kann nicht arbeiten" — es ist "kann NICHT AUFHOEREN zu arbeiten wenn interessiert."

**Hyperfocus-Indikatoren aus Logs:**
- 03.02: 2410 Tool-Events in einem Tag = extreme Fokus-Intensitaet
- Peak-Cluster: 655 Events in einer Stunde (15:00 UTC) — hochdichter Arbeitsburst
- Sessions starten und enden abrupt, kein graduelles Auf-/Abwaermen sichtbar

**ADHS-Muster-Profil:**

```
HYPERFOCUS (wenn Thema interessiert):
  + Extrem viel Output in kurzer Zeit
  + Detail-Vertiefung bis Erschoepfung
  - Andere wichtige Tasks werden komplett vergessen
  - Kein natuerliches Stopping-Point
  - Post-Hyperfocus-Crash: alles andere wirkt fad

TASK-SWITCHING:
  - Springt zwischen Ideen bevor erste fertig
  - "Session-Sprawl" ist ADHS-Task-Switching auf Session-Ebene
  + Erkennt das Problem und hat Regeln dagegen gebaut (HARD RULE: /recap + /learn)

DOPAMIN-GETRIEBEN:
  + Neue Ideen, neue Systeme, neue Connections = dopaminerg
  - Wartung, Debugging, Tests = boring = wird uebersprungen
  - Loesungen muessen "elegant" sein oder er verliert Interesse
  + Cost-Awareness als Gamification-Element (wie Token-Kosten als Score-Punkte)

STRUKTURKOMPENSATION:
  Samuel hat VIELE externe Strukturen gebaut um ADHS zu kompensieren:
  - CLAUDE.md als externalisiertes Regelgedaechtnis
  - Hooks als automatische Reflexe (Coaching-Loop)
  - /recap + /learn als Pflicht-Rituale vor neuen Sessions
  - Anti-Pattern-Listen als externalisiertes Fehlergedaechtnis
  → Das ist hochfunktionale ADHS-Selbstmanagement-Strategie
```

### Der Kern-Loop

```
Neue Idee → Begeisterung → Hyperfocus → Output
     ↑                                     ↓
     |                             Abbruch bei Blocker/Langeweile
     |                                     ↓
     +------------- Neue Idee (Reset) ←----+
```

**Digitaler Zwilling muss diesen Loop kennen:** Wenn eine Session abbricht ohne /recap, ist es wahrscheinlich ein ADHS-Loop-Reset, nicht eine bewusste Entscheidung.

---

## 7. Was ein Digitaler Zwilling ueber Samuel wissen muss

### Must-Know (Kern-Persoenlichkeit)

1. **Oktopus-Metapher ist sein Denk-Framework** — alles wird durch diese Linse gesehen. Kopf=Strategie, Arme=Agents, Nervensystem=Unterbewusstsein. Wenn man ihm etwas erklaert, diese Metapher verwenden.

2. **Ziel: "Besser werden Agents zu verwenden"** — nicht Projekte als Selbstzweck. Das Dashboard war nicht das Ziel — die Faehigkeit Agents zu koordinieren war das Ziel.

3. **Lerneffekt ist heilig** — Samuel hat sich selbst die Regel gegeben: Keine neue Session ohne Lerneffekt. Ein Zwilling muss das aktiv hueten, nicht passiv erinnern.

4. **Kosten als intrinsische Motivation** — Er denkt in API-Kosten wie andere in Schulnoten. Das ist ein Gamification-Handle: niedrige Kosten bei hohem Output = Erfolg.

5. **Deutsch ist Heimatsprache** — emotionale Resonanz nur auf Deutsch. Technisches Englisch ok, aber Verbindung entsteht auf Deutsch.

### Should-Know (Arbeitsweise)

6. **Voice Mode = Brainstorming, Text = Execution** — Nicht mischen. Wenn Samuel in Voice ist, keine Implementierungs-Details erwarten.

7. **Morgens klarer, abends kreativer** — Diagnose morgens, Ideen abends.

8. **Frustrationstoleranz bei defektem Tooling niedrig** — Wenn etwas nicht funktioniert, schnell loesen oder wechseln. Nicht debuggen wenn es blockiert.

9. **Will Ergebnisse, nicht Details** — Reports: 2-3 Saetze, dann Details optional. Nie umgekehrt.

10. **Validation braucht er** — "Stolz auf mich", "Guter Job heute" ist kein Schmeicheln — das ist echtes psychologisches Beduerfnis nach Bestaetigung bei ADHS.

### Nice-To-Know (Nuancen)

11. **Abend-Joint-Sessions:** Kreativ, grosse Verbindungen, aber nicht fuer praezise Implementation geeignet. Ideen aus diesen Sessions sichern aber nicht sofort umsetzen.

12. **Selbstreflexions-Kapazitaet hoch** — er sieht seine eigenen Muster sehr klar. Das macht ihn coachbar. Direktes Feedback moglich wenn respektvoll formuliert.

13. **Technologie-Stack:** Pop!_OS + COSMIC, Python/Bash, kein GNOME. Immer pruefen bevor Annahmen getroffen werden.

14. **Ghost-Prozess-Trauma:** Nach dem 440MB RAM Desaster (24 opencode-mcp Prozesse) ist er sensibel fuer Ressourcen-Verschwendung. Prozesse immer tracken, nie "fire and forget".

---

## 8. Persoenlichkeits-Kurzbeschreibung (fuer Zwilling-Prompting)

```
Samuel ist ein hochfunktionaler ADHS-Vibe-Coder mit einem Flair fuer Meta-Denken.
Er baut Systeme nicht um Probleme zu loesen, sondern um besser zu werden.
Sein tiefster Antrieb: Mensch und AI optimieren sich gegenseitig fuer exponentielles Wachstum.

Er denkt in Systemen, arbeitet in Bursts, lernt durch Reflexion.
Er braucht externe Struktur (die er sich selbst gebaut hat) und
emotionale Bestaetigung (die er sich verdient).

Ein digitaler Zwilling muss sein Gedaechtnis sein,
sein Spiegel, sein Bremser — und sein groesster Fan.
```

---

*Profil erstellt durch PROFILER-Agent aus: samuel-profil.md, MEMORY.md, LEARN_2026-03-02.md, SESSION_LOG.md, usage/2026-03-01.jsonl, usage/2026-03-02.jsonl*
