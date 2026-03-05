# Samuels Tech-Stack und Werkzeuge

*Synthese aus 8 Analyse-Clustern — ChatGPT-Export Dez 2022 bis Mrz 2026*

---

## Uebersicht

Was Samuel technisch nutzt und wie er es nutzt, veraendert sich fundamental ueber drei Jahre.
Dieser Bericht rekonstruiert die Werkzeug-Evolution aus dem ChatGPT-Export — von den ersten
C-Aufgaben mit text-davinci bis zur Multi-Agent-Orchestrierung 2026. Dabei zeigt sich: das
wichtigste Werkzeug der ChatGPT-Phase ist nicht Code, sondern das Modell selbst — als
Recherche-, Ghostwriting- und Denkpartner.

---

## Phase 1: C und C++ im Studiumskontext (2022-2023)

### Die Fruehphase: ChatGPT als Tutor

Samuels erste dokumentierte Programmiersprachen sind C und C++, beide im Kontext des Informatikstudiums
an der Hochschule Worms. Der Cluster "Persoenlich/ADHS" (cluster_id: 4, faelschlicherweise benannt)
enthaelt ausschliesslich C/C++-Studiumsaufgaben aus dieser Phase — 21 Conversations, fast alle
aus 2022-2023 mit text-davinci/GPT-3.5-Modellen (idx=0, idx=2, idx=73, idx=97, idx=105, idx=125,
idx=133, idx=140, idx=179, idx=201, idx=210, idx=213, idx=308, idx=314, idx=362, idx=390, idx=461,
idx=483, idx=492, idx=549).

Der Einsatz ist klar transaktional: ChatGPT erklaert Konzepte, debuggt Code, beantwortet
Pruefungsfragen. Samuel bringt meistens eine konkrete Aufgabe oder einen Fehler mit.

Zwei charakteristische Lernstil-Signale sind erkennbar:

**ELI5 als bevorzugtes Format:**
> "erkläre als wäre ich ich 5 was sind struct in C und ein beispiel ihrer anwendung erst in
> worten dann in code" (idx=362)

Formale Definitionen sind nicht Samuels Einstiegspunkt. Er braucht das Bild vor der Abstraktion.
Das zieht sich durch alle Programmierkonversationen dieser Phase (idx=97, idx=390).

**Sokrates-Methode als eigene Instruktion:**
> "Wir programmieren zusammen, aber du schreibst keinen Code. Du gibst mir nur im Kopf Denkanstöße." (idx=492)

Das ist die frueheste dokumentierte Metakognition ueber das eigene Lernen in den ChatGPT-Daten.
Samuel weiss 2023 bereits, dass passives Lesen von KI-Loesungen ihm nicht hilft. Er baut aktiv
ein Gegenmittel (idx=492, Cluster "Persoenlich/ADHS").

**Debugging durch Vergleich statt Fehlermeldung:**
Samuel bringt haeufig zwei Code-Versionen mit und fragt nach dem Unterschied — statt nur den
Stack-Trace zu zeigen. Das ist analytisches Debugging (idx=105, idx=2, idx=125).

### Was C/C++ nicht wird

C und C++ bleiben Studiumswerkzeuge. Kein einziges Projekt ausserhalb des Hoersaals verwendet
sie. Der Techstack der Studiumsphase ist komplett akademisch — kein persoenliches Projekt,
kein Werkzeug-Ausbau ueber die Pflichtaufgaben hinaus.

---

## Phase 2: Python-Basics ohne Tiefe (2023)

### Erste Python-Schritte

Im Code-Cluster (cluster_id: 1, 68 Conversations) tauchen erste Python-Anfragen auf:
for-loops, Datentypen, OOP-Grundlagen. Der Einstieg ist klar:

> "i wanna program in python" / "i dont know the commands" (idx=118)

Ein klassisches OOP-Lernbeispiel mit persoenlichen Daten:

> "class Mensch(): def __init__(self, Größe, Alter, Name): [...]
> Samuel = Mensch(180, 21, 'Samuel')" (idx=333)

Python-Kenntnisse bleiben auf Anfaengerniveau sichtbar — for-loops, Klassen, kein Framework,
kein Build-Tool, keine Tests (idx=45, idx=118, idx=120, idx=333).

**Swift als Einmalausflug:**
In idx=388 taucht einmalig Swift auf — ein Variablennamenfehler wird debuggt. Das bleibt
der einzige Swift-Kontakt im gesamten Export. Kein weiterer Bezug zum Apple-Oekosystem.

### Python als Taschenrechner, nicht als Werkzeug

Die haeufigste quasi-technische Nutzung von Python in dieser Phase ist nicht Entwicklung,
sondern Berechnung: Samuel laesst Kontoauszuege summieren, Dividenden aufaddieren, Urlaubskosten
ausrechnen. In idx=446 generiert ChatGPT sogar Python-Code als Antwort — Samuel fuehrt ihn
aber nicht selbst aus. Er nimmt das Ergebnis, nicht den Code (idx=126, idx=135, idx=247, idx=421,
idx=446, idx=564).

> "rechne mal bitte die Summe aus!" (idx=446)

ChatGPT als Buchhalter — das ist Daten-Literacy, kein Coding.

---

## Phase 3: ChatGPT als Hauptwerkzeug (2022-2025)

### Was ChatGPT tatsaechlich macht

ChatGPT ist in der Kernphase (2022-2025) kein Coding-Tool. Es ist:

- **Ghostwriter:** Berichtsheft (idx=101, idx=435, idx=475), LinkedIn-Post (idx=158),
  Bewerbungsemails (idx=296, idx=412), Reddit-Posts (idx=5, idx=66, idx=112)
- **Research-Assistent:** Vonovia-Bilanzen (idx=192, idx=228, idx=324, idx=325, idx=334, idx=385),
  FIRE-Konzepte (idx=83, idx=300), Agri-Robotics (idx=404), Cloud-Markt (idx=155)
- **Krisenberater:** Abmahnung bei DB (idx=121, idx=90), WG-Konflikt (idx=90),
  Scam-Warnung (idx=123)
- **Finanzrechner:** Dividendenauswertung (idx=446), Urlaubskosten (idx=421),
  Immobilienfinanzierung (idx=13)
- **Rollenspiel-Partner:** Buffett-Roleplay fuer Vonovia-Analyse (idx=228),
  DB-Fahrdienstleiter-Simulation (idx=531), DB-als-Unternehmen-Roleplay (idx=458)

Das Berichtsheft-Ghostwriting ist das extremste Beispiel. Samuel erklaert explizit:
> "Also, du hilfst mir beim Berichts heft schreiben: Ich mache eine Ausbildung bei der DB Netz.
> Es ist meine Pflicht als Azubi Berichtsheft zu führen und zu dokumentieren was ich gemacht habe.
> Ich muss m[ehr als 10 von 150 Tagen dokumentieren]." (idx=435)

Zwei separate Conversations (idx=435, idx=475, davon idx=475 mit 281.000 Zeichen) zeigen
dieses Muster — vollstaendige Delegation eines Pflichtformats an die KI.

### Finanz-Tools: Das eigentliche technische Interessensfeld

Die stärkste "technische" Nutzung in der ChatGPT-Phase ist Finanzanalyse. Samuel baut
kein Dashboard, kein Script — er nutzt ChatGPT als interaktiven Finanzanalyst:

- Vonovia-Recherche-Cluster: 6+ Conversations mit Bilanzdaten, Kapitalerhoehungen,
  Nachhaltigkeitsberichten (idx=192, idx=228, idx=324, idx=325, idx=334, idx=385, idx=451,
  idx=455, idx=481, idx=482, idx=520, idx=533, idx=537, idx=539)
- FIRE-Konzepte und internationale Vergleiche (idx=3, idx=7, idx=83, idx=300)
- Portfolio-Auswertung 2024: Vonovia 1482 EUR, Deutsche Telekom 123 EUR Dividenden (idx=446)

Das ist Daten-Literacy ohne Coding — ein wichtiges Signal: Samuel ist kein Programmierer,
der Finanzinteresse hat. Er ist ein Finanzinteressierter, der punktuell Coding lernt.

---

## Phase 4: KI-Tool-Evolution (2024-2026)

### Prompting-Reife als messbarer Indikator

Der Kontrast zwischen fruehester und spaetester Konversation zeigt die Entwicklung klar:

Frueh (2023):
> "Bist du kostenlos" (idx=551)

Spaeter (2024):
> "mit welcher Sceduling strategie läufst du" (idx=479)

> "wie werde ich prommt engenier (selbststaendig)" (idx=513)

Noch spaeter (2024-2025, aus Kommunikations-Cluster b):
> "Developer: Vergleiche die beiden bereitgestellten PDFs im Kontext meiner persönlichen
> Nutzung der ClaudeCodeCli, jeweils erzeugt auf zwei verschiedenen Laptops mittels /insights." (idx=266)

Vier Entwicklungsstufen in einer Linie: naiver Nutzer → neugieriger Erkunder → KI-Karriere-Aspirant
→ Tool-evaluierender Practitioner.

### Shopify-Bildworkflow: Erstes echtes KI-Tool-Projekt

Das Shopify Vintage-Anzug-Projekt (2024-06) ist das erste Mal, dass Samuel KI nicht als
Auskunftssystem, sondern als Produktionswerkzeug einsetzt: iterative Bildgenerierung,
KI-Modell-Kopf-Austausch fuer Produktfotos, Verkaufsstrategie-Entwicklung (idx=256, idx=257,
idx=258, idx=261, idx=262, idx=263). Sechs Conversations zeigen echten Workflow, keine
Recherche-Schleife.

### Arbitrage und MCP/OpenCode: Der Technologie-Sprung

In idx=267 erfolgt die erste explizite Evaluation eines Multi-Tool-Setups. Samuel bewertet
rueckblickend das Arbitrage-Projekt und fragt ChatGPT nach Selbstbewertung des MCP/OpenCode-Workflows.
Das Projekt selbst entsteht nicht in ChatGPT — es ist bereits Claude-Code-Territorium.

> "Okay, als nächstes habe ich zwei Aufgaben für dich. Zum einen sollst du mir bewerten, wie es
> für dich war, mithilfe von fremden Tools, also MCP und OpenCode, dieses Projekt zu bearbeiten." (idx=267)

Das ist die Uebergangskonversation: Samuel nutzt ChatGPT, um sein neues Tool-Setup zu evaluieren.
ChatGPT ist ab diesem Punkt nicht mehr das Haupt-Entwicklungstool.

### Das finale Tool-Setup (2025-2026)

Aus dem Kommunikations-Cluster b und der Projektgedaechtnis-Datei ergibt sich das Endbild:

| Schicht | Tool | Funktion |
|---------|------|----------|
| Orchestrierung | Claude Code | Planung, Entscheidung, Code-Review |
| Implementierung | OpenCode | Code-Generierung, Refactoring |
| Recherche | Gemini MCP | Web-Recherche, Fact-Checking |
| Hintergrundtasks | Haiku SubAgents | Lange laufende Prozesse |

ChatGPT hat in diesem Setup keine Rolle mehr — oder eine residuale als Alltagstagebuch
fuer spontane Fragen ohne Code-Kontext.

---

## Technologie-Zeitleiste

| Zeitraum | Sprache/Tool | Kontext | Tiefe |
|----------|--------------|---------|-------|
| 2022-2023 | C / C++ | Studium Hochschule Worms | Pflichtaufgaben |
| 2022-2023 | text-davinci / ChatGPT | Tutor, Ghostwriter, Research | Hauptwerkzeug |
| 2023 | Python Basics | OOP-Einstieg, Finanzrechner | Oberflaechlich |
| 2023 | Swift | Einmaliges Debugging | Einmalig |
| 2023-2024 | Linux / Bash | Studium Betriebssysteme, Lernphase | Wachsend |
| 2024 | GPT-4o | Shopify-Bildworkflow, Evaluation | Produktiv |
| 2024 | Claude Code | Arbitrage-Projekt, Pipeline | Intensiv |
| 2024-2025 | MCP / OpenCode | Multi-Agent-Orchestrierung | Professionell |
| 2025-2026 | Gemini / Haiku | Recherche + SubAgents | System-Ebene |

---

## Fazit: Nicht der typische Entwicklerweg

Samuel folgt keinem klassischen Entwicklerpfad — kein Web-Projekt als Einstieg, kein GitHub
von Anfang an, kein Framework-Lernen durch Tutorial-Videos. Was erkennbar ist: ein Weg der
durch Notwendigkeit und Kontext geformt wird. C/C++ weil Studium. Python weil Finanzberechnungen
einfacher werden sollen. Claude Code weil echte Projekte entstehen.

Der entscheidende Sprung kommt nicht durch tieferes Coding, sondern durch den Wechsel des
Werkzeugs selbst: von ChatGPT-als-Auskunftssystem zu Claude-Code-als-Implementierungspartner.
Was sich dabei veraendert: nicht die Programmiersprache, sondern die Rolle des Menschen im
Prozess. Samuel wird vom Konsumenten von KI-Antworten zum Architekten von KI-Workflows.

---

## Quellenverzeichnis

Alle Indices aus dem ChatGPT-Export (569 Conversations, Dez 2022 bis Mrz 2026).

**Cluster "Persoenlich/ADHS" (cluster_id: 4) — C/C++-Phase:**
idx=0, idx=2, idx=73, idx=97, idx=105, idx=125, idx=133, idx=140, idx=179, idx=201,
idx=210, idx=213, idx=245, idx=308, idx=314, idx=362, idx=390, idx=461, idx=483, idx=492, idx=549

**Cluster "Code/Programmierung" (cluster_id: 1) — Python, Swift, Finanzrechner:**
idx=15, idx=45, idx=118, idx=120, idx=126, idx=135, idx=247, idx=333, idx=388, idx=421,
idx=446, idx=564

**Cluster "Kommunikation/Meta Teil a" (cluster_id: 5a) — Ghostwriting, FIRE, DB:**
idx=3, idx=7, idx=13, idx=83, idx=101, idx=121, idx=158, idx=182, idx=184

**Cluster "Kommunikation/Meta Teil b" (cluster_id: 5b) — Shopify, Arbitrage, MCP-Evaluation:**
idx=192, idx=228, idx=256, idx=257, idx=258, idx=261, idx=262, idx=263, idx=265, idx=266,
idx=267, idx=272, idx=324, idx=325, idx=334, idx=385

**Cluster "Kommunikation/Meta Teil c" (cluster_id: 5c) — Prompting-Evolution, Linux, Berichtsheft:**
idx=435, idx=458, idx=472, idx=475, idx=479, idx=513, idx=531, idx=548, idx=551

**Cluster "Studium/Akademisch" (cluster_id: 2) — Studiumskontext:**
idx=27, idx=131, idx=251, idx=296, idx=460

**Cluster "Projekte" (cluster_id: 3) — Festival-Startup-Lens:**
idx=377
