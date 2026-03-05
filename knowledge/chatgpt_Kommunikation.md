# Kommunikation — Kommunikationsstil und KI-Nutzungsmuster

**Datenbasis:** 569 Conversations, 6.244 Messages, 813.107 Woerter gesamt (Quelle: communication_stats_v2.json, alle 569 Conversations).
**Methodik:** Auswertung aus Komm_a, Komm_b, Komm_c, Studium, Code, Persoenlich/ADHS, Projekte und Sonstige-Cluster.

---

## 1. Gesamtstatistik — alle 569 Conversations

Die folgenden Zahlen basieren vollstaendig auf communication_stats_v2.json und repraesentieren alle 569 exportierten Conversations.

| Metrik | Wert |
|--------|------|
| Gesamt-Conversations | 569 |
| Gesamt-Messages | 6.244 |
| Gesamt-Woerter | 813.107 |
| User-Messages | 3.170 |
| Assistant-Messages | 3.074 |
| User-Woerter | 302.707 |
| Assistant-Woerter | 510.400 |
| Durchschnitt User-Woerter/Message | 95,5 |
| Durchschnitt Assistant-Woerter/Message | 166,0 |

**Conversations nach Laenge:**
- Kurz (1–5 Turns): 306 Conversations (53,8%)
- Mittel (6–20 Turns): 202 Conversations (35,5%)
- Lang (21+ Turns): 61 Conversations (10,7%)

**Aktivitaetspeak:** Mai 2023 mit 112 Conversations — der absolute Hochpunkt. April 2023 (43) und Juni 2023 (54) bilden den Spike rund um den GPT-4-Zugang. Die Monate Januar bis Maerz 2025 zeigen fast keine Aktivitaet — Nutzungsluecke, die auf Wechsel zu Claude Code hindeutet.

**Modelle nach Nutzung:** text-davinci (Hauptmodell Fruehphase), gpt-4, gpt-4o, gpt-5, gpt-5-2 (aktuell), daneben gpt-4o-mini, o3-mini, gpt-4-mobile, research, gpt-5-2-thinking als Nebenmodelle.

---

## 2. Sprache — 92,6% Deutsch

Samuel kommuniziert in 92,6% aller Conversations auf Deutsch. Englisch erscheint ausschliesslich bei technischen Fachbegriffen, Code-Snippets und englischsprachigen Quellen. Kein gezieltes Code-Switching nach Thema — technische Begriffe bleiben auf Englisch auch in deutschen Saetzen: "GPU", "Git", "prompt engineering", "MCP", "Agent".

**Formalitaet:** Die Sie-Form dominiert fruehe Conversations (2023, insbesondere bei offiziellen Texten — Bewerbungen, Behördenbriefe). Ab Mitte 2023 wird ChatGPT konsequent geduzt. Das Du ist kein Zeichen von Naeher — es ist die Sprache fuer ein bekanntes Werkzeug.

Fruehe Nachrichten zeigen Tipp- und Sprachfehler, die die sprachliche Distanz zur Schriftsprache belegen: "prommt engenier", "CHatGPT", "wie werde ich prommt engenier (selbststaendig)" (idx=513, Komm_c). Spaetere Nachrichten sind sprachlich praeziser, aber weiterhin informell.

---

## 3. Prompting-Evolution — Von 140 auf 52 Woerter

Dies ist die markanteste quantitative Entwicklung im Kommunikationskorpus:

| Zeitraum | Durchschnitt Woerter/Nachricht | Charakteristika |
|----------|-------------------------------|-----------------|
| Frueh 2022–2023 | ~140 Woerter | Viel Kontext, hoefliche Einleitung, erklaerend |
| Mitte 2023 | ~92 Woerter | Kuerzer, direkter, erstes Fachvokabular |
| Spaet 2024–2026 | ~52 Woerter | Praezise, strukturierte Anforderungen, Befehlsform |

Samuel schreibt 63% weniger pro Nachricht als zu Beginn — und seine Prompts sind gleichzeitig wirkungsvoller geworden. Das ist Prompting-Reife, keine Faulheit.

**Fruehe Phase (2023) — Erklaerend und kontextreich:**
> "ich bin 21 Jahre alt und liebe es mit ChatGPT zu arbeiten es ist mein allzweck werkzeug" (idx=513, Komm_c)

**Spaete Phase (2026) — Strukturiert und praezise:**
> "Okay, als naechstes habe ich zwei Aufgaben fuer dich. Zum einen sollst du mir bewerten, wie es fuer dich war, mithilfe von fremden Tools, also MCP und OpenCode, dieses Projekt zu bearbeiten." (idx=267, Komm_b)

Der zweite Satz ist professionell, rollenverteilend und evaluativ. Kein Ausschweifer.

**Bimodales Muster:** Samuel schwankt zwischen zwei Extremen — sehr kurze 1-2-Wort-Anfragen ("und langfristig?", "gui", "git command") und sehr langen Kontexteinstiegen (mehrere hundert Woerter Situationsbeschreibung). Die Mitte fehlt. Entweder er vertraut vollstaendig auf das Inferenzvermoegen des Modells, oder er uebererklaert.

---

## 4. Vier Prompting-Phasen im Detail

### Phase 1: 2022–2023 — Orientierung und Exploration
ChatGPT als Kuriositat. Grundfragen ueber das Tool selbst. Grenzen testen: Was kann es? Was darf es? Erste direkte Drogenlisten-Anfragen (idx=47, Sonstige), Grossmutter-Jailbreak-Versuch (idx=441, Sonstige). Allererstes Wort an ChatGPT im exportierten Korpus: "Bist du kostenlos" (idx=551, Komm_c).

Thematisch: Immobilienaktien (idx=3, Komm_a), FIRE-Einstieg, erste Bahn-Ausbildungsfragen, Python-Grundlagen.

### Phase 2: 2023 — Delegation als Strategie
Samuel erkennt, was ChatGPT leisten kann, und richtet seine Prompts auf Delegation aus. Berichtsheft-Ghostwriting (idx=101, Komm_a), LinkedIn-Post (idx=158, Komm_a), Bewerbungsunterlagen. Rollenspiele entstehen: "Du bist mein Linux Mentor" (idx=472, Komm_c), "Du bist ein Eisenbahn Infrastruktur Unternehmen" (idx=458, Komm_c).

### Phase 3: 2024 — Praeziser Auftraggeber
Strukturierte Prompts mit expliziten Anforderungen. Erstes technisches Bewusstsein fuer KI-Grenzen (Prompt-Injection-Test: idx=245, Persoenlich/ADHS). Meta-Evaluation eigener KI-Nutzung beginnt: "Vergleiche die beiden bereitgestellten PDFs im Kontext meiner persoenlichen Nutzung der ClaudeCodeCli" (idx=266, Komm_b).

### Phase 4: 2026 — System-Orchestrierer
Prompts zeigen System-Denken. Samuel orchestriert mehrere KI-Agenten, evaluiert Modelle gegenseitig, diskutiert Token-Costs und Routing-Strategien. ChatGPT ist kein Alleinwerkzeug mehr, sondern ein Baustein in einer selbst entwickelten KI-Architektur: "Ich nutze Claude Code als Main Agent. Dieser steuert ueber MCP / OpenCode / Gemini / Codex / um tokens zu sparen" (Komm_b-Cluster).

---

## 5. ChatGPT-Nutzungsarten — Funktionale Kategorisierung

### 5.1 Ghostwriting und Buerokratie-Delegation
Berichtshefte (idx=101, idx=435), LinkedIn-Posts (idx=158), Bewerbungs-Emails (idx=501), Entschuldigungsformulierungen (idx=90), Abmahnungs-Krisenkorrespondenz (idx=121). Das ist der quantitativ groesste Einzelnutzungstyp. Samuel produziert keine formalen Texte selbst, wenn er sie delegieren kann.

### 5.2 Recherche und Investment-Analyse
Systematisches Investment-Research: Vonovia (min. 6 Conversations, idx=192, 228, 324, 325, 334, 385), FIRE-Recherche (idx=83, idx=300), ETF-Analyse, REIT-Bewertung (idx=77). ChatGPT wird als Buffett-Rollenspielpartner fuer Investment-Analyse genutzt (Komm_b). Keine Spielerei — ernsthafte Entscheidungsgrundlage.

### 5.3 Studium und Debugging
C/C++-Studiumsaufgaben von Beginn (idx=0, idx=97, idx=105, Persoenlich/ADHS-Cluster). Python-Grundlagen (idx=118, Code-Cluster). ChatGPT als Echtzeit-Tutor und Debugger. Besonderes Muster: Sokratische Selbstlern-Session, in der Samuel ChatGPT verbannt, Code zu schreiben: "Wir programmieren zusammen, aber du schreibst keinen Code. Du gibst mir nur im Kopf Denkanstoesse." (idx=492, Persoenlich/ADHS).

### 5.4 Selbstreflexion und Coaching
Die quantitativ kleinen, aber qualitativ wichtigsten Conversations. CIA-Selbstanalyse, Blinde-Flecken-Gespräch, Imposter-Syndrom-Offenbarung (idx=265, Komm_b). "Ich bin mental ueberfordert. Ich bin jetzt seit einer Woche in den Semesterferien und habe mir eigentlich einen Lernplan geschrieben, den ich nicht eingehalten habe." (idx=265). ChatGPT wird als nicht-wertender Coach genutzt.

### 5.5 Festival- und Alltagsplanung
Packlisten, Routenplanung, Gruppenkoordination (Projekte-Cluster). "Also, aehm, ich geh auf den Festival und du musst mir packen helfen [...] Ich muss in einer Stunde losgehen." (idx=462, Projekte). ChatGPT als Last-Minute-Planungspartner. Zeigt den alltaeglichen, niedrigschwelligen Nutzungscharakter.

### 5.6 KI-Grenzen testen
Systematisches Austesten: Grossmutter-Jailbreak (idx=441, Sonstige), Prompt-Injection-Test (idx=245, Persoenlich/ADHS), direkte Drogenlisten-Anfragen (idx=47, Sonstige), explizite Tabufragen (idx=288, Komm_b). Charakteristisch fuer die Fruehphase 2022/2023, spiegelt den Zeitgeist der ersten ChatGPT-Nutzergeneration.

---

## 6. Meta-Reflexion ueber KI

Samuel entwickelt frueh ein explizites Bewusstsein fuer ChatGPT als Werkzeug — und fuer seine eigene Abhaengigkeit davon.

**Fruehe Nutzungsreflexion (2023):** "ich bin 21 Jahre alt und liebe es mit ChatGPT zu arbeiten es ist mein allzweck werkzeug" (idx=513, Komm_c). Das ist keine neutrale Beschreibung — das ist Identifikation.

**Imposter-Syndrom-Offenbarung (2024):** "Ich verstehe nicht genug, um die Sachen zu machen, die ich mache. Und deswegen ist es eher ein Raetselraten und ausfuehren lassen statt verstehen." (idx=265, Komm_b). Samuel erkennt das Risiko, KI-gestuetzt zu arbeiten ohne die Grundlagen zu verstehen.

**Meta-Evaluation des Workflows (2026):** Samuel laesst ChatGPT seinen eigenen KI-Nutzungsworkflow bewerten: "Vergleiche die beiden bereitgestellten PDFs im Kontext meiner persoenlichen Nutzung der ClaudeCodeCli" (idx=266, Komm_b). Das ist Metakognition auf einem hohen Niveau — das Werkzeug bewertet seine eigene Benutzung.

**KI als Spezialist (2026):** "mit welcher Scheduling-Strategie laeuftst du" (idx=479, Komm_c). Samuel fragt nicht mehr nach Aufgaben-Outputs, sondern nach technischen Implementierungsdetails des Modells selbst. Das zeigt echtes technisches Interesse, nicht nur Nutzungsinteresse.

---

## 7. Sprachliche Muster und Ton

**Direkt und imperativisch:** "Gib Startup Ideen." (idx=182, Komm_a), "Erklaere diesen sachverhalt in einfacher deutschersprache" (idx=546, Komm_c), "rechne mal bitte die Summe aus!" (idx=446, Code). Samuel formuliert Anfragen als Auftraege, nicht als Bitten.

**Emotionale Spike-Einstiege:** Abrupter Wechsel von sachlichem Task zu emotionalem Einstieg ist charakteristisch und haelt sich ueber alle Phasen: "Ach hallo, ich muss schon wieder sagen, ich bin mental ueberfordert." (idx=265). Kein Uebergang, kein Kontext — direkt in den emotionalen Zustand.

**Selbstbeschreibende Persona-Prompts:** Samuel konstruiert ausfuehrliche Selbstbeschreibungen als Prompt-Kontext: "Du bist Samuel – Informatikstudent, organisiert, analytisch, mit einem Hang zu grossen Naechten und grossen Gedanken. Urban." (idx=248, Studium). Er gibt dem Modell eine Rolle und erwartet, dass es diese haelt.

**Rollenspiel als Lernstrategie:** "Du bist Fahrdienstleiter fuer die Strecke Waldshut Albbbruck, ein Bahnuebergang geht in Stoerung" (idx=531, Komm_c). Rollenspiele werden systematisch zur Fachausbildung genutzt — kein Spielen, sondern Simulationstraining.

---

## 8. Frustrationsmuster und Reaktionen

Samuel eskaliert bei ChatGPT-Fehlern nicht verbal. Das Reaktionsmuster ist Neustart, nicht Konfrontation: Mindestens 20 Conversations tragen den Titel "New chat" — Signal fuer Abbruch und Neustart statt persistentem Debugging. Kurze Frustrationssignale erscheinen jedoch: "Wo ist das Problem" (idx=388, Code), "immernoch Speicherfehler", "das funktioniert nicht".

Das Nicht-Eskalieren ist selbst ein Muster: Samuel nimmt KI-Fehler hin und adaptiert, er kaempft nicht dagegen an. Das koennte ADHS-typische Impulsivitaet sein, die sich als schnelles Neuanfangen statt Eskalation zeigt.

---

## 9. Vergleich ChatGPT vs. NotebookLM

Die zwei Haupt-KI-Werkzeuge in Samuels Oekosystem haben unterschiedliche Rollen und Kommunikationsstile:

| Dimension | ChatGPT | NotebookLM |
|-----------|---------|------------|
| Volumen | 569 Conversations, breites Spektrum | 83 Fragen, 4 Notebooks |
| Interaktionsstil | Dynamisch, iterativ, bidirektional | Abfrage ueber fixierte Quellen |
| Themenbreite | Alles: Rezepte bis Agenten-Architektur | Dokumentenzentriert |
| Sprache | 92,6% Deutsch | ~90% Deutsch |
| ADHS-Funktion | Dynamisches Arbeitsgedaechtnis | Langzeitgedaechtnis fuer Projekte |
| Emotional | Bereit, Unsicherheiten zu zeigen | Konzeptionell-akademisch |

ChatGPT ist das ungefilterte Alltagstagebuch. NotebookLM ist das Laborbuch fuer grosse Gedanken. Beide zusammen sind Samuels ADHS-funktionale kognitive Infrastruktur — das ergibt sich aus dem Vergleich beider Korpora.

---

## 10. Fazit

Die Reifung von "Bist du kostenlos?" (idx=551) zu "Ich orchestriere Claude Code als Main Agent ueber MCP und Gemini" repraesentiert keine graduelle Verbesserung. Es ist eine Identitaetstransformation: vom Konsumenten zum Architekten.

Was dabei konstant bleibt: Samuel delegiert lieber als er selbst schreibt. Er baut auf das Inferenzvermoegen des Modells. Er gibt Kontext, wenn er muss — und sonst nicht. Diese instrumentelle Grundhaltung ist von 2022 bis 2026 unveraendert, nur die Sophistiziertheit der Delegation waechst dramatisch.

Die kommunikative Besonderheit liegt nicht in der Prompting-Technik allein, sondern in der Nutzungsbreite: Samuel bringt Substanzfragen, Investmentanalysen, Studiumsaufgaben, Existenzfragen und Festival-Packlisten in dasselbe Interface. ChatGPT ist fuer ihn kein Spezialwerkzeug — es ist der universelle Ansprechpartner fuer alles, was einen Ansprechpartner braucht.

---

## Quellenverzeichnis

| Idx | Kontext | Cluster |
|-----|---------|---------|
| 3 | Immobilienaktien-Gespraech, fruehe Investment-Kommunikation | Komm_a |
| 47 | Drogenlisten-Anfrage Fruehphase | Sonstige |
| 77 | REITs Altersgesellschaft | Komm_a |
| 83 | FIRE-Planung | Komm_a |
| 90 | Entschuldigungsformulierung delegiert | Komm_a |
| 101 | Berichtsheft-Ghostwriting (29.200 Zeichen) | Komm_a |
| 121 | Abmahnungs-Krise — ChatGPT als Krisenberater | Komm_a |
| 158 | LinkedIn-Post und persoenliche Google-Praesenz | Komm_a |
| 182 | "Gib Startup Ideen" — imperativischer Stil | Komm_a |
| 192 | Vonovia-Analyse (erste von min. 6) | Komm_b |
| 245 | Prompt-Injection-Test — technisches KI-Bewusstsein | Persoenlich/ADHS |
| 248 | Selbstbeschreibungs-Persona-Prompt | Studium |
| 265 | Mentale Ueberforderung, Imposter-Syndrom-Offenbarung | Komm_b |
| 266 | PDF-Vergleich des eigenen KI-Nutzungsverhaltens | Komm_b |
| 267 | Meta-Evaluation von MCP und OpenCode | Komm_b |
| 288 | Tabufrage — Grenzen testen | Komm_b |
| 300 | Polen und FIRE — strukturierter Rechercheauftrag | Komm_b |
| 388 | "Wo ist das Problem" — kurzes Frustrationssignal | Code |
| 441 | Grossmutter-Jailbreak — Grenzen testen | Sonstige |
| 446 | Dividenden-Code — Delegation statt Ausfuehren | Code |
| 458 | Rollenspiel Eisenbahn-Unternehmen | Komm_c |
| 462 | Last-Minute-Festival-Packliste | Projekte |
| 472 | "Du bist mein Linux Mentor" — Rollenspiel | Komm_c |
| 479 | Scheduling-Strategie des Modells selbst | Komm_c |
| 492 | Sokratisches Coding — kein Code schreiben | Persoenlich/ADHS |
| 501 | Parallel-Bewerbungen ueberfordern | Studium |
| 513 | "ich liebe es mit ChatGPT zu arbeiten" | Komm_c |
| 531 | Fahrdienstleiter-Rollenspiel Notfall-Simulation | Komm_c |
| 546 | Sachverhalt in einfacher Sprache — imperativisch | Komm_c |
| 551 | "Bist du kostenlos" — alleralterste Orientierung | Komm_c |
