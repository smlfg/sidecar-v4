# Samuels Projekt-Portfolio

Wer Samuel verstehen will, schaut sich seine Projekte an. Vier Systeme, vier verschiedene Stadien, vier verschiedene Lektionen. Kein Projekt ist perfekt — aber jedes erzählt etwas Wahres darüber, wie jemand denkt, wenn er baut.

---

## Keeper: Amazon Price Monitoring System

*Notebooks: Keeper_Amazon, Keeper_System*

### Was ist das?

Keeper ist eine vollständige Data-Engineering-Pipeline, die automatisch Amazon-Preise überwacht, Deals findet und Nutzer benachrichtigt, wenn ein Preis unter einen Zielpreis fällt. Die Idee ist simpel und bestechend: "Statt manuell Preise zu vergleichen, übernimmt unsere Pipeline das — periodisch, automatisiert, mit Notifications."

Das Ergebnis ist ein System, das man als "ambitioniert realistisch" bezeichnen könnte: architektonisch gut durchdacht, in der Umsetzung noch nicht fertig, aber funktional genug für eine Beta.

### Tech-Stack

| Schicht | Technologien |
|---------|-------------|
| Backend | Python 3.11, FastAPI, asyncio, asyncpg |
| Datenbanken | PostgreSQL 15, Elasticsearch 8.11.0 |
| Messaging | Apache Kafka 7.5.0, Zookeeper |
| Orchestrierung | LangGraph (Agents), APScheduler |
| Infrastruktur | Docker Compose (8 Services) |
| Validierung | Pydantic, SQLAlchemy 2.0+ |

### Die Three-Pillars-Architektur

Keeper ist um drei klare Säulen gebaut:

1. **Scraping/Ingestion Layer** — Keepa API + APScheduler (alle 6 Stunden)
2. **Processing/Event-Streaming Layer** — Apache Kafka + LangGraph Agents
3. **Storage Layer** — PostgreSQL (ACID, Source of Truth) + Elasticsearch (Volltext-Suche) + Kibana (Dashboards)

Die Entscheidung für zwei Datenbanken war bewusst: *"Jedes System hat eine klare Aufgabe. PostgreSQL garantiert ACID-Transaktionen für die Preis-History — wenn ein Preis gespeichert wird, ist er da. Elasticsearch ist für schnelle Suche und Aggregationen optimiert — 'Zeige mir alle Deals unter 50€ mit Rating > 4.0 sortiert nach Discount' ist eine Zeile in ES, aber ein komplexer Join in SQL."*

Kafka sitzt in der Mitte und entkoppelt alles: *"Kafka entkoppelt die Produzenten (den Scheduler) von den Konsumenten (die in die Datenbanken schreiben). Wenn die nachgelagerte Datenbank ausfällt, gehen keine Daten verloren, da Kafka die Nachrichten über Offsets und eine siebentägige Speicherdauer (Retention) puffert."*

### Ein echtes Highlight: Token Bucket Rate Limiting

Der Keepa-API-Client implementiert ein Token-Bucket-Algorithmus, der die verbleibenden API-Tokens pro Request trackt. Jede Operation hat ihren Preis: Queries kosten 15 Token, Deals 5, Best-Sellers 3. *"Keepa gibt mit jeder Response die verbleibenden Tokens zurück. Unser Client wartet automatisch, wenn Tokens unter den Schwellwert fallen."*

Das ist kein Copy-Paste aus einem Tutorial. Das ist Verständnis.

### Das kritische Problem: Zwei Datenbank-Schemas

Die größte Schwachstelle von Keeper ist gleichzeitig die lehrreichste: Zwei parallele Datenbank-Stacks existieren nebeneinander — ein asynchroner (`services/database.py`) und ein synchroner (`core/database.py`). Tabellennamen und Datentypen weichen voneinander ab.

*"Das größte identifizierte Problem ist die Existenz von zwei parallelen Datenbank-Stacks (asynchron vs. synchron). Tabellennamen und Datentypen weichen voneinander ab, was zu Divergenzen und Fehlern zwischen der API und den Background-Schedulern führt."*

Die Entstehung ist klassisch: Das System begann synchron, wurde später auf async umgestellt — aber nicht vollständig. Zwei Code-Pfade. Ein Wartungs-Albtraum.

### Der Performance-Krater: 75 Minuten statt 8

Für 100 überwachte Produkte braucht Keeper 75 Minuten, wenn es die Keepa-API einzeln aufruft. Mit Batch-Queries (bis zu 10 ASINs pro Request) würden es 8 Minuten sein. Die Optimierung existiert in der API — wird aber nicht genutzt. Das kostet 90% mehr Tokens und macht das System in der Praxis schwerfällig.

*"Die aktuelle Implementierung ruft die Keepa API für jedes überwachte Produkt einzeln auf, anstatt die von Keepa angebotenen Batch-Abfragen (bis zu 10 ASINs pro Request) zu nutzen."*

### Das Scorecard

| Dimension | Score |
|-----------|-------|
| Architektur | 8/10 |
| Performance | 4/10 |
| Maintainability | 7/10 |
| **Gesamt** | **6.2/10** |

Ehrlich, datengetrieben, nicht beschönigt.

### Fehler mit Lehrwert

- **Async-Bug:** `client.search_deals` wird in einem API-Endpoint aufgerufen, aber nicht `await`et. Ergebnis: HTTP-500-Fehler bei jedem Deal-Search-Request.
- **Memory Leak:** Das `sent_alerts`-Dict im Alert Dispatcher wächst ohne TTL oder Cleanup unbegrenzt — über lange Laufzeit ein echtes Problem.
- **Geisterfunktionen:** Telegram- und Discord-Notifikationen sind in der Architektur dokumentiert, im Code aber Platzhalter. Nur E-Mail funktioniert.

---

## mAImory: AI-Powered Email-to-Reminder Pipeline

*Notebooks: mAImory, Software_Architecture*

### Was ist das?

mAImory ist gleichzeitig ein Uni-Projekt (Software Architecture, HS Worms, WS 2025/2026) und ein echtes Startup-Konzept. Nutzer laden eine E-Mail hoch, ein LLM extrahiert Termine und Fristen, generiert eine ICS-Datei, und der Nutzer bestätigt per Y/N-Gate, bevor er den Termin in seinen Kalender importiert.

Das Ziel: ein MVP in 4 Wochen mit einem Entwickler, das von 10 auf 1000 Monthly Active Users skalieren kann, ohne dass die Architektur neu gebaut werden muss.

### Tech-Stack

- **Backend:** Python, FastAPI (synchron für MVP, async-upgrade geplant)
- **Datenbank:** PostgreSQL (2 Tabellen: users + reminders)
- **LLM-Provider:** OpenAI GPT-4, Anthropic Claude 3.5, MiniMax (Fallback-Kette)
- **Auth:** Google OAuth2 (authlib, python-jose/JWT)
- **Output:** Python `icalendar` Library (ICS-Generierung)
- **Deployment:** Docker, GitHub Actions CI/CD

### Die Architektur: ADD 3.0, 7 ADRs, Adapter Pattern

Das Herzstück ist eine dreiteilige Entwurfsstrategie:

**1. Pipeline Architecture** — Synchroner Monolith für das MVP, mit definiertem Upgrade-Trigger: "Sobald 100 concurrent users, Fallback-Rate >50%, oder Response Time >5s — dann Web-Queue-Worker mit Redis + Celery." Das Besondere: Der Upgrade-Pfad ist konkret geplant, nicht vage versprochen. *"Upgrade Pfad: Sobald die Metriken zeigen, dass der Server blockiert, tauschen wir die synchrone Implementierung des AIService gegen einen AsyncQueueService aus. Die restliche App merkt davon nichts."*

**2. Adapter Pattern für LLM-Unabhängigkeit** — Drei konkrete Adapter (OpenAIAdapter, ClaudeAdapter, MiniMaxAdapter) hinter einer abstrakten Schnittstelle. Provider-Wechsel in unter 8 Entwicklungsstunden — garantiert durch Architektur, nicht durch Hoffnung.

**3. Fallback-Kette mit Mathematik** — Drei unabhängige Provider ergeben rechnerisch 99,9975% Verfügbarkeit: `1-(1-0.995)^3`. Ohne einen einzigen Redundanz-Server. *"Durch die Verkettung von drei unabhängigen Providern mit je 99,5% Uptime erreichen wir rein rechnerisch ca. 99,99% Verfügbarkeit, ohne einen Cent für Redundanz-Server auszugeben."*

### Die Ironie: Anti-Over-Engineering im über-dokumentierten Format

Das auffälligste an mAImory ist der Widerspruch zwischen Form und Inhalt. Constraint CON-5 lautet explizit: "Keine Over-Engineering, YES known tech stack (Python/FastAPI)." Microservices werden abgelehnt ("Modularity is good, but too much overhead for 1 developer!"), Circuit Breaker für das MVP verworfen, layered architecture als over-engineered abgestempelt.

Und doch: Ein Solo-Uni-Projekt mit ~700 Zeilen Code ist in einem 40+ Seiten formalen ADD-3.0-Dokument mit 7 ADRs, 3 ADD-Iterationen, einem kompletten 8-Schritt-QAW-Prozess, Kanban-Boards und 5+ draw.io-Diagrammen dokumentiert.

Der Anti-Over-Engineering-Standpunkt ist selbst über-dokumentiert. Das nennt man produktive Ironie — und es spiegelt die Realität eines Uni-Projekts, das gleichzeitig ein echtes Startup-Konzept ist.

*"Dein Projekt ist kein Over-Engineered Monster, sondern ein chirurgisch präzises MVP."* — So das Feedback, das Samuel besonders traf.

### "Progress > Perfection" als Architekturprinzip

Der klarste Satz im ganzen Projekt: *"BWL: Wir opfern jetzt QAS-1 (perfekte Skalierbarkeit) zugunsten von QAS-3 (MVP-Speed), weil wir ohne MVP gar keine User haben werden."*

Das ist kein Kompromiss aus Unwissenheit. Es ist eine bewusste Entscheidung mit geschriebener Begründung.

### Der echte Schwachpunkt: Angst vor Datenbanken

*"erkläre mir die Rolle von Postgres und DB in mAImory, ich habe Angst vor diesen beiden sachen, deswegen habe ich es auch noch nie eingezeichnet in den Views"*

Selten ist eine Lücke so direkt und ehrlich benannt. ADD-Iteration 3 wurde bewusst auf Resilience und Error Handling gelenkt — weil Samuel zu dem Zeitpunkt DB-Schema-Design noch nicht sicher beherrschte. Eine echte Einschränkung, die transparent kommuniziert wurde. *"Leider kenne ich mich nicht mit Datenbanken aus und habe das Modul dazu nie geschrieben, auch wenn es eine denkbares ADD3 wäre, muss es leider ausfallen."*

---

## AI NPU Agent: Der groesste Failure — und die wertvollste Lektion

*Notebook: AI_NPU_Agent*

### Was sollte es werden?

Das Ziel war ambitioniert: Ein Large Language Model direkt auf der Snapdragon X Elite NPU (Neural Processing Unit) eines Dell Latitude 7455 zum Laufen bringen. Privat, latenzarm, kein Cloud-Aufruf. Der lokale KI-Assistent "SelfAI" sollte auf echter Hardware inferieren.

### Zwei Strategien. Beide gescheitert.

**Strategie 1: onnxruntime + qai_hub_models**
Die offizielle Qualcomm-Bibliothek `qai_hub_models` sollte via ONNX Runtime mit dem QNN Execution Provider auf der NPU laufen. Ergebnis: Der QnnExecutionProvider konnte von ONNX Runtime nicht gefunden werden. Schlimmer: *"from_pretrained()-Methode gab konsistent None zurück, selbst für öffentliche Modelle im CPU-Modus, ohne detaillierte Fehlermeldungen bereitzustellen, was eine effiziente Fehlerbehebung unmöglich machte."*

Eine Black-Box-API, die bei Fehlern schweigt, ist in Hardware-Integrationsarbeiten das Schlimmste, was passieren kann.

**Strategie 2: llama-cpp-python mit NPU/QNN-Flags**
Kompilierung von llama-cpp-python aus dem Quellcode mit `CMAKE_ARGS='-DGGML_QNN=ON'`. Ergebnis: *"pip install kann eine erfolgreiche Installation melden, auch wenn die Kompilierung für spezifische Hardware-Backends nicht erfolgreich war oder die CMAKE_ARGS ignoriert wurden."*

`pip install` meldet Erfolg. Das Backend wurde trotzdem nicht gebaut. Der einzige Hinweis: "Failed to load model from file" — ohne weitere Information.

### Die Marketing-vs-Reality-Kluft

Qualcomm vermarktet NPU-Inference als schlüsselfertige Lösung. Die technische Realität war eine andere: ARM64-Python wird von `qai_hub_models` unter Windows nicht unterstützt — auf einem ARM64-Chip. Das ist kein Randproblem. Das ist ein fundamentaler Architektur-Widerspruch.

*"Architektur-Widersprüche: Die Dokumentation von qai_hub_models deutete auf eine Inkompatibilität zwischen ARM64 Python und der on-device-Ausführung unter Windows hin, was unsere gesamte Strategie in Frage stellte."*

### Die Meta-Lektion

Die wichtigste Erkenntnis formuliert der Lessons-Learned-Bericht selbst: *"Das Projekt war von Natur aus kein reines Software-Implementierungsprojekt, sondern ein Forschungs- und Entwicklungsvorhaben (R&D), das sich mit unbekanntem Terrain auseinandersetzte. Diese Fehleinschätzung der Projektart erklärt die Frustration über 'Black-Box'-APIs und irreführende Fehler. Es wurde ein klarer, linearer Weg erwartet, der schlichtweg nicht existierte."*

Ein Implementations-Task behandelt wie einen R&D-Task — ohne die Methoden des R&D zu kennen. Das Projekt scheiterte nicht an Dummheit. Es scheiterte an einer falschen Projektkategorie-Einschätzung.

### Was blieb

Trotz allem: Das komplette Hexagon V73 Programmer's Reference Manual (400K+ Zeichen Hardware-ISA-Dokumentation) wurde durchgearbeitet. Nicht weil es für den MVP gebraucht wurde — sondern weil Samuel verstehen wollte, wie die Hardware wirklich funktioniert.

---

## Self AI V2: Strukturiertes LLM-Fundament

*Notebook: Self_AI_V2 (in group1_personal)*

### Was ist das?

Self AI V2 ist das infrastrukturelle Fundament, auf dem der NPU Agent aufbauen sollte — und von dem mAImory konzeptionell abgeleitet ist. Ein strukturiertes LLM-System mit optimierter Inference, Multi-Provider-Architektur und einem Gedächtnissystem, das zwischen "persoenlich" und "arbeit" unterscheidet.

Das Projekt befindet sich in einem aktiven Review-Stadium: Technische und organisatorische Erkenntnisse wurden herausgearbeitet, Verbesserungsvorschläge dokumentiert, ein API-Test war erfolgreich.

### Verbindung zu mAImory

Self AI V2 ist der konzeptionelle Vorläufer von mAImory: Die Multi-Provider-Logik, die in Self AI V2 als Idee existiert, wurde in mAImory als Adapter Pattern formalisiert. Das Gedächtnissystem aus Self AI V2 ist die informelle Vorstufe des strukturierten Datenmodells in mAImory.

---

## Verbindungen zwischen den Projekten

Die vier Projekte sind keine isolierten Experimente. Sie bilden eine Lernkurve:

```
Self AI V2  →  NPU Agent  →  Keeper  →  mAImory
(Fundament)    (Failure)    (System)    (Architektur)
```

- **Self AI V2** etablierte das Interesse an lokalem LLM-Inference.
- **NPU Agent** testete die Hardware-Grenze — und scheiterte, aber mit Dokumentation.
- **Keeper** baute die erste vollständige Data-Engineering-Pipeline mit echten Systemen.
- **mAImory** brachte das akademische Framework (ADD 3.0) auf ein reales Startup-Konzept.

Was alle vier verbindet: LangGraph-Workflows, das Adapter-Pattern als Architekturprinzip, und Python als einheitliche Sprache. Und ein Entwickler, der lieber ehrlich einen Score von 6.2/10 vergibt als eine 10/10 zu behaupten.

---

*Quellen: Notebooks Keeper_Amazon, Keeper_System, AI_NPU_Agent, mAImory, Software_Architecture, Self_AI_V2 — analysiert am 2026-03-02.*
