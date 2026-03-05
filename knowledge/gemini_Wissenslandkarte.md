# Wissenslandkarte — Samuels Wissens-Archipel

*Eine Kartierung von 9 NotebookLM-Notebooks, 744.306 Tokens, einem Kopf*

---

## Die 9 Wissensinseln

Stell dir neun Inseln vor, jede mit eigenem Klima und Vegetation — aber alle im selben Meer. Zusammen ergeben sie ein Bild davon, wer Samuel Fleig als Denker und Baumeister ist. Grosse und Dichte variieren stark.

---

**Insel 1: AI_NPU_Agent** — Die Expedition (258.870 Tokens, grosste Insel)
Das bei weitem volumenstarkste Notebook. Fast die Halfte des gesamten Korpus. Der Grund: Samuel hat den vollstandigen Hexagon V73 Programmer's Reference Manual gesammelt — das ISA-Handbuch (Instruction Set Architecture) fur Qualcomms Neural Processing Unit, in seiner ganzen technischen Tiefe. Die Insel ist eine Expedition in feindliches Gelande: WSL-Umgebungsinstabilitaten, Black-Box-APIs, 0-Byte-Modelldateien, ein ARM64/x64-Widerspruch, der die gesamte Strategie in Frage stellt. Das Projekt hat sein Hauptziel verfehlt — kein LLM lauft auf dem NPU — aber die Lessons Learned sind von aussergewohnlicher Qualitat. *"Das Projekt war von Natur aus kein reines Software-Implementierungsprojekt, sondern ein Forschungs- und Entwicklungsvorhaben (R&D), das sich mit unbekanntem Terrain auseinandersetzte."*

**Insel 2: mAImory** — Das Architekturburo (170.463 Tokens)
Die zweitgroste Insel ist eine Konstruktionszeichnung. mAImory ist Samuels Software-Architecture-Semesterprojekt an der Hochschule Worms, dokumentiert nach ADD 3.0-Methodik mit 7 Architecture Decision Records, drei vollstandigen Iterationen und einem mathematisch beweisbaren Verfugbarkeitsversprechen (99,9975% via Drei-Provider-Fallback-Kette). Die Insel hat zwei Gesichter: akademische Strenge und echter Startup-Pragmatismus. *"Dein Projekt ist kein Over-Engineered Monster, sondern ein chirurgisch prazises MVP."* Die Architektur ist fertig entworfen — ob der Code dahinter vollstandig implementiert ist, bleibt offen.

**Insel 3: Software_Architecture** — Die Bibliothek (106.956 Tokens)
Der Kurs-Kontext fur mAImory. Hier lagern Vorlesungsfolien (Lect 1-9), Ubungsblatter, ADD-Cheat-Sheets, Systemfragen mit Musterantworten und Samuels eigene Freitextnotizen — darunter die ehrlichste Aussage uber akademische Frustration: *"Ich kotze im Strahl wegen ADD, es kommt mir so unnötig vor, ich wünsche mir mein System so — wo sind die Haken meines Wishful Thinkings?"* Die Bibliothek enthalt alle zehn Architekturmuster mit Qualitatsattribut-Analyse, samtliche ADD-3.0-Schritte und einen direkten Einblick in Samuels Denken als Student und als Praktiker zugleich.

**Insel 4: SE_Fundamentals** — Die Klausurstation (88.796 Tokens)
Software Engineering mit Prof. Dr. Kohler an der HS Worms. Diese Insel ist ein Echtzeit-Lerndokument — man kann Samuels emotionalen Zustand buchstablich an der Grammatik ablesen. Turns 0-32: prazises Hochdeutsch, akademischer Ton. Turn 60: *"Ich 8 Stunden ist die Klausur / ich bin im 2. Versuch"* — Syntax-Fehler als Stressindikator. Das Notebook dokumentiert UML-Diagrammtypen, Scrum, Cloud Computing und Big Data, zeigt aber vor allem, wie ein Lernender unter Druck mit AI als Lernpartner arbeitet.

**Insel 5: Keeper_System** — Die Maschinenhalle (36.677 Tokens)
Die technische Systemdokumentation des Keeper-Projekts: Architekturentscheidungen, Datenbankschemas, Kafka-Konfiguration, Code-Analyse, Fehlerdiagnosen. Hier findet sich der systematische Code-Review mit Bewertungs-Rubrik (8/10 Architektur, 4/10 Performance), die Identifikation des dualen Datenbank-Stacks als kritischstes Problem und die Berechnung, dass Batch-Optimierung den Token-Verbrauch um 90% senken wurde. *"Mit den Top-5-Verbesserungen konnte das System 10x schneller werden."*

**Insel 6: Keeper_Amazon** — Das Missionskontrollzentrum (35.890 Tokens)
Die operationelle Seite des gleichen Projekts: Q&A-Sessions, Erklarungen der Architektur, tiefes Einsteigen in einzelne Komponenten. Keeper_Amazon und Keeper_System sind die engst verbundenen Inseln im gesamten Archipel (TF-IDF-Ahnlichkeit: 0.906 — quasi Zwillinge). Gemeinsame Begriffe: asin, await, elasticsearch, kafka, keepa, kibana, postgres, scheduler.

**Insel 7: Self_AI_V2** — Das Hauptquartier (23.818 Tokens)
Die organisatorische und reflexive Zusammenfassung des Self-AI-Projekts. Hier wohnen die drei wichtigsten technischen und prozessualen Erkenntnisse aus dem NPU-Abenteuer, der Entwurf des SelfAI-Agent-Frameworks (selfai.py, agent_manager.py) und die strukturierten Lernmomente. Kleinste der "Projekt-Inseln", aber sehr dicht.

**Insel 8: Digital_Anonym** — Die Bunkeranlage (9.921 Tokens)
Ein detailliertes Handbuch zu Anonymitat im Netz: 7-Schichten-Anonymitatskette, Tails OS, VeraCrypt, KeePassXC, DNS-over-HTTPS, MAC-Adressen-Spoofing, Tor vor VPN, Kryptographie-Wallet-Hygiene, Verhaltensrisiken ("Tippmuster konnen Identitat verraten"). Die Insel ist klein aber philosophisch dicht. *"Anonymitat ist wie ein Schatten: Du siehst ihn nur, solange du das Licht richtig einsetzt."*

**Insel 9: ADHS** — Das Archiv (13.915 Tokens)
Die personalste Insel. Medizinische Dokumentation fur die ADHS-Erstdiagnose aus dem Jahr 2010 (Dr. Karl C. Mayer, Heidelberg) und die Nachdiagnose als Erwachsener 2025. BDI-II, WURS-K, Grundschulzeugnisse als objektive Belege fur Kindheitssymptome. *"Ich wurde 8 Jahre meiner Jugend mit Ritalin behandelt."* Keine Scham, kein Euphemismus — reine Sachlichkeit uber sich selbst.

---

## Brucken zwischen den Inseln

Welche Inseln sind miteinander verbunden? Das Wissens-Graph zeigt klare Starken und Muster.

```
ADHS (13K)
  |
  | 0.289 ─────────────────────────────────────────────────────────
  |                                                                |
  v                                                               v
SE_Fundamentals (88K) ──── 0.402 ──── Software_Architecture ─── 0.685 ──── mAImory (170K)
      |                                     (107K)                              |
      | 0.248                                 |                                 | 0.380
      v                                       | 0.404                           v
Keeper_Amazon ──── 0.906 ──── Keeper_System   |                         AI_NPU_Agent (259K)
   (35K)                         (36K)        |                               |
                                              v                               | 0.362
                                         Self_AI_V2 (23K) ──────────────────-+
                                              |
Digital_Anonym (9K) ─── 0.262 ─── SE_Fundamentals
```

*Kantenwerte = TF-IDF-Kosinusahnlichkeit (Wertebereich 0-1)*

---

**Brucke 1: Keeper_Amazon ↔ Keeper_System (0.906 — starkste Verbindung)**
Zwei Notebooks fur ein Projekt. Sie teilen 17 Fachbegriffe: asin, await, current_price, deals, discount_percent, docker-compose, elasticsearch, kafka, keepa, keeper, kibana, postgres, price, scheduler, watches. Diese Zwillings-Inseln sind im Grunde eine einzige Wissensbasis, die in zwei NotebookLM-Projekten gepflegt wurde — vermutlich wegen Grossenbeschrangungen oder thematischer Trennung zwischen Systemarchitektur und operationellem Betrieb.

**Brucke 2: Software_Architecture ↔ mAImory (0.685 — zweitstarkste)**
mAImory IST das Kurs-Projekt. Die Vorlesungsinhalte (Adapter Pattern, Repository Pattern, ADD 3.0, Quality Attribute Scenarios) sind direkt in mAImorys Architekturentscheidungen eingeflossen. Gemeinsame Begriffe: "architectural" und "modifiability" — kein Zufall, das sind die Kernbegriffe der ADD-Methodik. Samuel hat die Theorie benutzt, um seine eigene Praxis zu strukturieren. *"Es geht nicht um die PERFEKTE Architektur. Es geht darum zu ZEIGEN, WIE du zu deiner Architektur gekommen bist!"*

**Brucke 3: Software_Architecture ↔ AI_NPU_Agent (0.404)**
Stark genug, um bemerkenswert zu sein. Die NPU-Arbeit hat Samuel tief in Software-Architektur-Fragen hineingezogen: Wie entkoppelt man eine Anwendung von der LLM-Schnittstelle? (Antwort in mAImory: Adapter Pattern.) Wie verwaltet man fehlerhafte Hardware-Backends? (Antwort im NPU-Postmortem: abstrakte `load_model()`-Factory.) Die akademische Architekturlehre und das praktische Scheitern haben denselben Losungsraum.

**Brucke 4: Software_Architecture ↔ SE_Fundamentals (0.402)**
Beide kommen aus HS Worms, beide decken Software-Engineering-Konzepte ab, beide enthalten UML. SE_Fundamentals liefert das Fundament (UML-Syntax, Scrum, Komplexitat), Software_Architecture baut darauf auf (ADD, Qualitatsattribute, Architekturmuster). Im mAImory-Notebook tauchen auch SE-Fundamentals-Vorlesungsfolien auf — Samuel hat beide Kurse mit demselben Werkzeug (NotebookLM) und teilweise im gleichen Notebook studiert.

**Brucke 5: AI_NPU_Agent ↔ Self_AI_V2 (0.362 — geteilt: "qualcomm")**
Identisches Vokabular, identische Problemstellung. Self_AI_V2 ist das Uber-Projekt, AI_NPU_Agent ist die Hardware-Expedition dazu. Die selfai.py-Architektur wollte NPU als prima Inferenz-Backend nutzen — ist aber im Demo-Fallback steckengeblieben. Das gemeinsame Schlusselbegriff "qualcomm" verrart die Hardware-Abhangigkeit beider Notebooks.

**Brucke 6: AI_NPU_Agent ↔ mAImory (0.380)**
Beide arbeiten mit LLMs. Beide haben Fallback-Konzepte (NPU > CPU > Demo in Self_AI; OpenAI > Claude > MiniMax in mAImory). Die Lektion aus dem NPU-Projekt — "Black-Box-APIs sind riskant: Wenn eine Bibliothek bei Kernfunktionen keine detaillierten Fehler liefert, wird die Diagnose extrem aufwendig" — hatte direkt mAImory's Adapter-Architektur begrunden konnen.

**Brucke 7: ADHS ↔ SE_Fundamentals (0.289)**
Die starkste Verbindung des ADHS-Notebooks — und sie geht zu SE_Fundamentals. Beide teilen zwar keine Fachbegriffe, aber viel sprachliche Struktur: emotionale Authentizitat, Druck, das Navigieren eines Systems (medizinisch vs. akademisch). Der Krisenmodus ("Ich 8 Stunden ist die Klausur / ich bin im 2. Versuch") und die ADHS-Appointment-Panik ("Okay morgen ist der Termin, ich muss heute noch alle Sachen ausfüllen") haben denselben menschlichen Tenor. ADHS erklart das Verhaltensmuster, das in fast allen anderen Notebooks sichtbar ist: Hyperfokus, Last-Minute-Sprints, diagnostische Prazision uber sich selbst.

---

## Themen-Cluster

**Cluster "Projekte" — Der Maschinenraum**
- Keeper_Amazon + Keeper_System (ein Projekt, zwei Notebooks)
- mAImory (Startup-Idee und Uni-Abgabe zugleich)
- AI_NPU_Agent + Self_AI_V2 (ein Ziel, eine Hardware, viel Lehrgeld)

Diese funf Notebooks teilen einen gemeinsamen Nenner: Samuel baut Systeme fur sich selbst, die er auch anderen verkaufen konnte. Keeper spart Geld beim Online-Shopping. mAImory spart Zeit bei der Terminverwaltung. SelfAI gibt Datenprivatsphare beim LLM-Einsatz.

**Cluster "Akademisch" — Das Gerippe**
- Software_Architecture (SWA 506, Prof. Schwarzer, HS Worms)
- SE_Fundamentals (SE mit Cloud/Big Data/UML, Prof. Kohler, HS Worms)

Beide Kurse sind an der Hochschule Worms, beide praxisorientiert. Software_Architecture liefert den Rahmen (ADD-Methodik, Architekturmuster), SE_Fundamentals das Handwerk (UML, Scrum, Cloud-Grundlagen). Das Akademische ist nicht abstrakt — es wird direkt in den Projekten angewendet.

**Cluster "Personlich" — Die Grundlage**
- ADHS (Selbstkenntnis und medizinische Navigation)
- Digital_Anonym (Werte und Verhaltensregeln)

Diese beiden Notebooks erklaren den Menschen hinter den Projekten. ADHS erklart den Lernstil (Hyperfokus, Systemdenken, Last-Minute-Mobilisierung). Digital_Anonym erklart die Design-Philosophie (Privacy by Default, Datensparsamkeit, Misstrauen gegenuber Single Points of Trust).

---

## Zentrale Begriffe — Was durch alle Inseln wandert

Einige Konzepte tauchen in mehreren Notebooks auf, ohne explizit verlinkt zu sein:

- **"Adapter"** — In mAImory als Architekturmuster (LLM-Provider-Adapter), in Software_Architecture als Theorie, im NPU-Projekt als dringend benotigtes abstraktes Interface (`load_model()` Factory). Drei Notebooks, ein Losungsgedanke.
- **"Fallback"** — NPU > CPU > Demo (AI_NPU_Agent), OpenAI > Claude > MiniMax (mAImory), PostgreSQL als source-of-truth wenn Elasticsearch ausfault (Keeper). Resilience durch Fallback-Ketten ist Samuels Lieblings-Architekturmuster.
- **"MVP"** — mAImory explizit als Startup-Metrik (4 Wochen, 1 Entwickler, kein Over-Engineering), Keeper implizit im Beta-Zustand (6.2/10, funktional aber nicht produktionsreif), NPU-Projekt mit Demo-Fallback als ehrlichstem MVP aller Zeiten.
- **"LLM"** — Verbindet AI_NPU_Agent, Self_AI_V2, mAImory, und uber die Adapter-Pattern-Diskussion auch Software_Architecture. LLM-Integration ist das rote Faden, der Samuels technisches Schaffen zusammenhalt.
- **"Anonymitat / Datensparsamkeit"** — Digital_Anonym als Handbuch, mAImory als Designprinzip (keine E-Mail-Inhalte in der DB), NPU-Projekt als ultimative Konsequenz (kein Cloud-LLM, alles lokal).

---

## Blinde Flecken — Was fehlt auf der Karte

Kein Atlas ist vollstandig. Die Wissenslandkarte zeigt auch, was fehlt:

- **Testing** — Kein Notebook uber automatisiertes Testen. Keeper hat explizit keine Unit-Tests fur Kafka-Consumer und keine Integration-Tests fur Elasticsearch. mAImory erwahnt Load-Testing als Validierungsschritt, aber nirgendwo ist ein Test-Notebook.
- **Frontend** — Samuels gesamte Arbeit ist Backend und Infrastruktur. mAImory erwaht eine Browser Extension, Keeper eine React-Dashboard-Alternative zu Kibana — aber weder gebaut noch dokumentiert. UI/UX ist ein blinder Fleck.
- **DevOps & CI/CD** — Docker wird genutzt, aber oberflachlich. CI/CD ist in mAImory als Qualitatsattribut-Ziel definiert ("<15 Minuten git push to production"), aber die Pipeline selbst ist nicht dokumentiert.
- **Teamarbeit & Collaboration** — Alle Projekte sind Solo-Projekte (CON-1: "1 Developer"). Wie Samuel in Teams arbeitet, Wissensubergaben gestaltet oder Code Reviews durchfuhrt — kein Notebook.
- **Datenbankdesign** — Samuel hat das selbst bemerkt: *"Leider kenne ich mich nicht mit Datenbanken aus."* Kein Notebook zu SQL-Optimierung, Indexing, Migrations-Strategien oder Datenbanktheorie.

---

## Die grosse Verbindung — Was alles zusammenhalt

Betrachtet man die neun Inseln aus der Vogelperspektive, wird ein ubergeordnetes Muster sichtbar:

Samuel baut an einer personlichen KI-Infrastruktur — lokale, private, autonome Werkzeuge, die sein Leben effizienter machen. Wahrend er baut, studiert er gleichzeitig die Theorie dahinter. Und er dokumentiert das Scheitern mit derselben Prazision wie den Erfolg.

Die akademischen Kurse (Software_Architecture, SE_Fundamentals) liefern nicht Theorie um der Theorie willen — sie liefern Vokabular und Methodik fur Entscheidungen, die Samuel sowieso trifft. ADD 3.0 ist nicht burokratischer Overhead, sondern ein Spiegel, der zeigt, wo das eigene "Wishful Thinking" bricht. *"Ich kotze im Strahl wegen ADD, es kommt mir so unnötig vor — wo sind die Haken meines Wishful Thinkings?"* Die Frustration wird zur richtigen Frage.

Die personlichen Notebooks (ADHS, Digital_Anonym) sind nicht Randnotizen — sie sind die Betriebssystem-Ebene. ADHS erklart, warum manche Notebooks in Last-Minute-Krisen entstehen und trotzdem brillante Selbstanalysen enthalten. Digital_Anonym erklart, warum mAImory keine E-Mails speichert und warum das NPU-Projekt die Cloud vermeiden wollte.

Der rote Faden durch alle neun Inseln: *Autonomie durch Verstandnis.* Nicht "jemanden fragen" — verstehen. Nicht "Cloud-Service nutzen" — lokale Kontrolle behalten. Nicht "Fehler verstecken" — Postmortem schreiben.

*"Wissen ist kein Schutz. Verhalten ist Schutz."* — Digital_Anonym

Das gilt nicht nur fur Anonymitat. Es gilt fur alles, was Samuel baut.
