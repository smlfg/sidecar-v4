# Samuels Technologie-Landkarte

Technologie-Kompetenz lässt sich nicht aus Lebensläufen ablesen. Sie zeigt sich darin, welche Fehler jemand macht — und wie präzise er sie beschreibt. Diese Karte basiert auf dem, was in sechs Notebook-Analysen sichtbar wurde: durch Code, durch Fehlschläge, durch Fragen, durch Erklärungen.

---

## Kernkompetenzen (Advanced)

### Python — Die Muttersprache

Python läuft durch alle vier Projekte wie ein roter Faden. Nicht als Werkzeug, das man benutzt, weil es verfügbar ist — sondern als Sprache, in der man denkt.

**Async/Concurrency:** Keeper zeigt, was "advanced" hier bedeutet. `asyncio.gather()` mit Semaphores für parallele API-Calls, Event-Loop-Management, der Unterschied zwischen `asyncpg` und `psycopg2` als bewusste Architekturentscheidung: *"asyncpg ist ein asynchroner PostgreSQL-Treiber. Im Gegensatz zu psycopg2 (synchron) blockiert asyncpg nicht den Event Loop während einer Datenbankabfrage. Das heißt: Während eine DB-Query auf Antwort wartet, kann unser Server andere HTTP-Requests bearbeiten."*

Gleichzeitig zeigt das fehlende `await` auf einem async API-Call in Keeper, dass selbst gute async-Kenntnisse gegen subtile Bugs nicht immun sind. Das ist ehrlich — kein gecasteter Skill, sondern ein lebendiger.

**Einsatz in:** Keeper (async pipeline), mAImory (FastAPI backend), NPU Agent (selfai.py, agent_manager.py), Self AI V2 (inference integration), SE-Studium (UML exercise scripts)

### FastAPI — Produktiv ohne Boilerplate

FastAPI ist Samuels bevorzugtes Backend-Framework für neue Projekte — wegen Python-Vertrautheit, Pydantic-Integration und der automatischen OpenAPI-Dokumentation.

In Keeper wurde eine vollständige REST-API mit Swagger UI, Pydantic-Validierung, async-Endpoints und 8 Microservices aufgebaut. In mAImory war FastAPI explizit als Constraint definiert: *"YES known tech stack (Python/FastAPI)"* — weil Vertrautheit im 4-Wochen-MVP-Sprint wichtiger ist als technische Neuheit.

Reifer Einsatz: Modular routing, startup configuration, error handling. Noch offen: Missing-`await`-Bugs zeigen, dass async FastAPI Tücken hat, die auch Erfahrene treffen.

### Docker und Docker Compose — Infrastruktur als Code

8 Services in einem `docker-compose.yml` orchestriert, mit named volumes, internem Networking (`db:5432`, `kafka:29092`, `elasticsearch:9200`), environment variables und health checks. Das ist nicht "ich habe Docker mal ausprobiert" — das ist produktiver Umgang mit Container-Orchestrierung auf mittlerem Komplexitätsniveau.

Cloud-Agnostizismus in mAImory: *"Docker container macht den Provider irrelevant architektonisch. Flexibilität, auf Startup-Credits zu reagieren."*

### LLM und AI-Integration — Multi-Provider-Denken

Nicht ein LLM-Provider — mehrere, hinter Abstraktionsschichten. In mAImory wurden drei konkrete Adapter implementiert (OpenAI, Claude, MiniMax) hinter einer abstrakten `LLMAdapter`-Schnittstelle. In Keeper übernimmt LangGraph die Orchestrierung (Price Monitor Agent, Deal Finder Agent, Alert Dispatcher).

Das Wichtigste: Samuel denkt nicht in einzelnen API-Calls. Er denkt in Provider-Unabhängigkeit, Fallback-Ketten, Timeout-Budgets. *"LLM market changes rapidly. System must support OpenAI, Claude, and MiniMax without vendor lock-in."*

Aus der Praxis: *"Da ich jetzt schon 6 Monate an einem eigenen KI System mit generativer KI arbeite, kenne ich aus der Praxis ein paar der Tücken die über ein solches System auftreten können."*

### Software-Architektur und Design Patterns — Das akademische Fundament mit Praxisankern

Das ist vielleicht die stärkste Kompetenz — und die am wenigsten offensichtliche. ADD 3.0, Adapter Pattern, Repository Pattern, Chain of Responsibility, Strategy Pattern: Diese werden nicht nur benannt, sondern angewendet und begründet.

*"Hochgradige architektonische Reife. Studenten neigen oft dazu, einfach alles Coole einzubauen. Du machst das Gegenteil: Du lehnst komplexe Patterns ab und begründest das perfekt mit deinen Constraints."*

Besonders stark: Trade-off-Denken. Jede architektonische Entscheidung kommt mit einer Abwägung, was dabei aufgegeben wird. *"Trade-off Accepted: Sacrifice: Perfect scalability in Phase 1 — Gain: Fast market entry — Worth it: YES."*

---

## Solides Wissen (Intermediate)

### PostgreSQL — Funktional, aber mit blinden Flecken

Keeper zeigt ein solides Schema-Design: UUID Primary Keys, Foreign Keys, Indizes, Multi-Tenant-Unterstützung über eine `users`-Tabelle, ENUM-Typen für Status-Felder. Das Dual-Schema-Problem (synchroner und asynchroner Stack nebeneinander) zeigt allerdings auch, dass Datenbankentscheidungen früh und konsequent getroffen werden müssen.

Der ehrlichste Satz kommt aus mAImory: *"Leider kenne ich mich nicht mit Datenbanken aus."* Das ist keine Schwäche als Geständnis — das ist Selbstkenntnis. Und der erste Schritt, sie zu adressieren.

PostgreSQL-spezifisches Wissen ist vorhanden (Row-Level Security für Multi-Tenant-Isolation, `asyncpg` als Treiber, `pool_pre_ping` für Connection Management). Migrations, Index-Optimierung und Schema-Evolution sind als Lücken identifiziert.

### Apache Kafka — Konzeptuell stark, praktisch noch begrenzt

Kafka in Keeper: Consumer Groups, Offsets, Topic-basiertes Routing, 7-Tage-Retention konfiguriert. Das "Warum Kafka" ist gut artikuliert: *"Das ist der Vorteil von Kafkas Architektur gegenüber klassischen Message Queues: kein Message Loss."*

Was fehlt: Cluster-Erfahrung (Single-Broker-Setup), Kafka Streams, Schema Registry. Das ist One-Node-Kafka — produktiv, aber nicht Produktionsreif.

### Elasticsearch — Konzeptionell verstanden, praktisch noch Einsteiger

Keeper verwendet Elasticsearch mit eigenem Analyzer (German Stemmer + ASCII-Folding), konfigurierten Shards und Replicas. Das Verständnis der Rolle ist klar: *"'Zeige mir alle Deals unter 50€ mit Rating > 4.0 sortiert nach Discount' ist eine Zeile in ES, aber ein komplexer Join in SQL."*

Single-Node-Setup für Development — kein Cluster-Betrieb, keine Produktionserfahrung. Explizit selbst so eingestuft: "Beginner/Intermediate".

### Git und Linux — Tägliches Handwerk

Pop!_OS mit COSMIC Desktop als tägliche Arbeitsumgebung, apt-Paketverwaltung, Systemhärtung, Kommandozeile. Git als Standard-Tool für alle Projekte. Keine Besonderheiten — aber solide Grundlage.

### Privacy und Security — Eine eigene Kategorie

Ein unerwartetes, tiefes Interessensgebiet: Tor-Netzwerke, VPN-Konfiguration, VeraCrypt-Verschlüsselung, Tails OS, DNS-over-HTTPS, MAC-Adress-Randomisierung, Browser-Fingerprinting-Schutz, Kryptowährungsprivatsphäre (CoinJoin, Monero).

Das Wichtigste dabei ist eine philosophische Grundhaltung: *"Anonymität beginnt nicht im Netz — sie beginnt im Kopf."* Und: *"Wissen ist kein Schutz. Verhalten ist Schutz."*

---

## Grundlagen (Beginner / Akademisch)

### UML — Konzepte klar, Notation in Entwicklung

Software Engineering Kurs an der HS Worms: Alle 5 UML-Diagrammtypen des Kurses durchgearbeitet (Use Case, Activity, Class, Sequence, State). Konzepte verstanden — Notation noch fehleranfällig.

Der zentrale Satz: *"Konzepte habe ich alle verstanden, aber einzelheiten nicht, notierung und feinheiten."*

Ein konkreter Fehler: Ein Horizontal-Flow-Diagramm wurde als "Sequence Diagram" etikettiert, obwohl es ein Communication Diagram war. Inhalt korrekt, Label falsch. Wird mit der Zeit besser — braucht einfach mehr Übung mit Stift und Papier.

### Cloud Computing — Akademisch solide

IaaS/PaaS/SaaS, die 5 Key Characteristics nach NIST, Public/Private/Hybrid/Community Cloud, Virtualisierung (VMs vs. Container). Korrekte Einordnung realer Dienste: Office 365 ist SaaS + Public Cloud, internes Sozialnetzwerk ist Private Cloud. Solides akademisches Fundament für praxisrelevante Architekturentscheidungen.

### NPU / Hardware-Level — Versucht, gescheitert, gelernt

Das komplette Hexagon V73 Programmer's Reference Manual (Hardware-ISA-Dokumentation, 400K+ Zeichen) durchgearbeitet. Verständnis von QNN SDK, ONNX Runtime Execution Providers, CMAKE-Build-System für Hardware-Backends, ARM64 vs. x64 Kompatibilitätsmatrizen.

Praktisch: Nichts funktioniert. Aber die Lektion ist klar: *"Hardware-Integration ist ein R&D-Task: Die Nutzung von LLM-Bibliotheken mit spezifischer, neuer Hardware sollte nicht als einfacher Implementierungsschritt betrachtet werden."*

---

## Woher gelernt?

| Quelle | Was davon |
|--------|-----------|
| Hochschule Worms (Software Architecture, SE) | ADD 3.0, UML, Cloud Computing, Scrum, Design Patterns |
| Eigene Projekte (Trial-and-Error) | Async Python, Kafka, Elasticsearch, FastAPI, Docker |
| NotebookLM als Lernpartner | Strukturierte Examen-Vorbereitung, Architektur-Coaching |
| Hardware-Dokumentation (Qualcomm) | NPU, QNN SDK, ARM64-Architektur |
| Privacy-Handbook | Tor, VPN, VeraCrypt, Krypto-Privacy |
| 6 Monate GenAI-Praxis | LLM-Integration, Provider-Abstraktion, API-Rate-Limiting |

---

## Luecken und Wachstumsfelder

**Datenbankdesign** ist die klar identifizierte Lücke. Migrations (Alembic), Index-Optimierung, Schema-Evolution, normalisiertes Design — das alles existiert als Konzept, aber noch nicht als praktische Routine. *"Ich habe Angst vor diesen beiden sachen."* — Das ist der Ausgangspunkt. Angst benennen ist der erste Schritt.

**UML-Notation** muss von konzeptuellem Verständnis zu Notations-Präzision wachsen. Das braucht Wiederholung mit echten Diagrammen, nicht nur Lesen.

**Präsentations- und Zeitmanagement** — eine Probepräsentation war 3x zu lang. *"Ich bin Faktor 3 über der Zeit, daran muss ich arbeiten."* Die Diagnose ist richtig: Der Unterschied zwischen "alles erklären" und "das Entscheidende kommunizieren."

**NPU / Hardware-Integration** — bleibt ein offenes Feld. Das Wissen ist angesammelt, die Umsetzung scheiterte an unreifer Toolchain. Wenn Qualcomm seine SDKs stabilisiert, ist der Wissensfundus vorhanden, um es erneut zu versuchen.

**Cluster-Betrieb** (Kafka, Elasticsearch) — Produktions-Deployment mit mehreren Nodes ist konzeptuell bekannt, aber nicht praktisch erfahren.

---

## Tech-Stack-Evolution

```
Anfang                          Heute
------                          -----
Python (Basics)          →      Python (Async Expert)
Einzelne API-Calls       →      Multi-Provider mit Adapter Pattern
Einzelne Skripte         →      8-Service Docker-Compose-Systeme
Kein Architektur-Framework →   ADD 3.0, ADRs, QAW, 4+1 Views
Lokaler Code             →      Event-Streaming mit Kafka
SQL-Grundlagen           →      PostgreSQL + Elasticsearch (dual)
"LLM verwenden"          →      LLM orchestrieren (LangGraph, Fallbacks)
```

Das Muster: Vom Einzeltool zum System-Denker. Von "es funktioniert" zu "warum funktioniert es, was kostet es, was passiert wenn es ausfällt."

Der nächste Schritt ist sichtbar: von der Architekturplanung zur Implementierungssicherheit — besonders bei Datenbanken und Produktions-Deployment.

---

*Quellen: Notebooks Keeper_Amazon, Keeper_System, AI_NPU_Agent, mAImory, Software_Architecture (SWA 506), SE_Fundamentals, Self_AI_V2, Digital_Anonym — analysiert am 2026-03-02.*
