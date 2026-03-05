# Ideen — Offene Baustellen, Feature-Wunsche und Zukunftsplane

*Destilliert aus 9 NotebookLM-Notebooks, Stand 2026-03-02*

---

## Offene Baustellen

### Keeper — Das Preismonitoring-System mit Luft nach oben

Keeper ist das technisch ambitionierteste Projekt in Samuels Portfolio — eine Drei-Saulen-Architektur aus Apache Kafka, PostgreSQL und Elasticsearch, die Amazon-Preise alle 6 Stunden automatisch pruft und Deals findet. Die Architektur bekommt 8/10, die Performance aber nur 4/10. Das Fundament ist solid, der Ausbau fehlt noch.

**Kritische offene Punkte (Keeper_Amazon, Keeper_System):**

- **Batch-Optimierung fehlt komplett.** Die Keepa-API erlaubt bis zu 10 ASINs pro Request — Keeper ruft sie einzeln ab. Ergebnis: 100 Produkte brauchen 75 Minuten statt 8 Minuten, und der Token-Verbrauch ist 10x hoher als notig. *"Die aktuelle Implementierung ruft die Keepa API fur jedes uberwachte Produkt einzeln auf, anstatt die von Keepa angebotenen Batch-Abfragen (bis zu 10 ASINs pro Request) zu nutzen."* Geschatzter Aufwand zur Behebung: 8-12 Stunden.
- **Duale Datenbank-Schemas.** Es existieren zwei parallele Datenbank-Stacks: ein asynchroner (services/database.py) und ein synchroner (core/database.py), mit abweichenden Tabellennamen und Datentypen. Das ist die Wurzel vieler Instabilitaten. *"Das grosste identifizierte Problem ist die Existenz von zwei parallelen Datenbank-Stacks (asynchron vs. synchron)."* Aufwand: 20-30 Stunden.
- **Telegram und Discord — gebaut aber nicht fertig.** Die Architektur sieht drei Benachrichtigungskanale vor: E-Mail (funktioniert), Telegram Bot (Platzhalter), Discord Webhook (Platzhalter). Nutzer sehen in der Dokumentation drei Kanale, konnen aber nur einen nutzen. Aufwand: 6-10 Stunden.
- **Async-Bug im Deal-Search-Endpoint.** In `/api/v1/deals/search` fehlt ein einzelnes `await` vor `client.search_deals()`. Das Resultat: HTTP 500 bei jeder Deal-Suche. *"[Das] verursacht einen HTTP-500-Fehler, wenn nach Deals gesucht wird."* Aufwand: 1-2 Stunden — der einfachste Fix mit dem hochsten Impact.
- **Memory-Leak im Alert-Deduplicator.** Das Dict `sent_alerts` wachst unbegrenzt, ohne je aufgeraumt zu werden. Bei langem Betrieb ein stilles Problem, das irgendwann zu Speicherproblemen fuhrt.
- **Das Delete-Endpoint ist eine Attrappe.** `DELETE /api/v1/watches/{id}` loggt Erfolg, ohne etwas in der Datenbank zu andern. Produkte konnen de facto nicht geloscht werden.

**Mittelfristige Wishlist (aus Keeper_Amazon):**
- ML-basiertes Deal-Scoring (momentan regelbasiert: Discount x Rating x SalesRank)
- React-Frontend als Kibana-Ersatz fur normale Nutzer
- Prometheus + Grafana fur System-Health-Monitoring
- Elasticsearch-Cluster mit mehr als einem Node fur den Produktionsbetrieb

---

### mAImory — Architektur fertig, Implementierung offen

mAImory ist Samuels Uni-Abgabe fur das Software Architecture-Modul an der Hochschule Worms — und gleichzeitig eine echte Startup-Idee. Die ADD-3.0-Dokumentation ist abgeschlossen, aber ob der Code hinter der Architektur tatsachlich vollstandig implementiert wurde, bleibt offen.

**Explizit aufgeschobene Features (mAImory):**

- **F-3: Pattern Recognition.** Das ML-basierte Feature, das aus historischen Terminen Verhaltensmuster erkennt und proaktiv Erinnerungen vorschlagt. Samuel selbst nennt es *"Wunschfunktionalitat"* — zu komplex fur den MVP, braucht mindestens 3 Monate Betriebsdaten und eine eigene ML-Pipeline. *"F-3 (Pattern Recognition): POST-MVP Feature (ML-basierte Verhaltensvorhersagen). Zu komplex fur initiales MVP."*
- **Gmail API Auto-Fetch.** Momentan muss der Nutzer E-Mails manuell hochladen oder einfugen. Die automatische Gmail-Integration wurde `gmail.readonly` OAuth-Scope brauchen — 3-4 Tage Aufwand, die Samuel bewusst verschoben hat.
- **CalendarAdapter fur Google und Outlook.** Momentan gibt es nur ICS-Download zum manuellen Import. Direkte Sync wurde 5-7 Tage Entwicklung kosten.
- **Web-Queue-Worker-Upgrade.** Die synchrone Pipeline-Architektur hat eine Skalierungsgrenze bei ca. 100 gleichzeitigen Nutzern. Der Upgrade-Trigger ist definiert (100 MAU, Fallback-Rate >50%, Response Time >5s), aber der eigentliche Umbau auf Redis + Celery fehlt noch.
- **Circuit Breaker.** *"Rejected for MVP — Too complex for 1 developer, violates BG-4 (MVP Speed). Professors love such deliberate non-decisions."* Geplant fur den 1000-MAU-Meilenstein.
- **Browser Extension.** Im Frontend-Plan erwaht, aber nicht entworfen.
- **ADD4-Iteration (optional, nicht abgeschlossen):** Drei mogliche Themen — A) Datenbankdesign + Pattern Recognition, B) Monitoring mit Prometheus/Grafana, C) Security & Rate Limiting per Nutzer.

---

### AI NPU Agent / Self AI V2 — Gescheitertes Experiment mit offenem Ausgang

Das NPU-Projekt ist das ehrlichste Notebook in Samuels Sammlung: ein dokumentiertes Scheitern. Das Ziel — ein LLM auf dem Snapdragon X Elite NPU laufen lassen, ohne Cloud — wurde nicht erreicht. Beide technische Strategien schlugen fehl. Aber das Notebook ist kein Endpunkt, sondern ein Startpunkt.

**Was offen geblieben ist (AI_NPU_Agent, Self_AI_V2):**

- **NPU-Integration ist ungelost.** Die Hardware ist vorhanden (Dell Latitude 7455, Snapdragon X Elite), aber die Software-Toolchain ist noch nicht reif. *"Das Ziel 'LLM auf NPU zum Laufen bringen' war in diesem Kontext nicht ein Endpunkt, sondern ein ganzes Forschungsgebiet."* Die Frage ist, ob sich das 2025/2026 mit besseren SDKs anders anfuhlt.
- **SelfAI-Agent-Framework.** `selfai.py` und `agent_manager.py` existieren als Gerust — mit Fallback-Kette NPU > CPU > Demo-Modus. Das Demo-Fallback (hartcodierte Antworten) ist der aktuelle Zustand. Der Rest wartet auf eine funktionierende LLM-Integration.
- **Konkrete nachste Schritte aus den Lessons Learned:**
  - Dev Container, der die gesamte Entwicklungsumgebung kapselt (Python-Version, CMake, QNN-SDK)
  - Automatische Integritatsprufung fur heruntergeladene Model-Dateien (SHA256-Checksum)
  - `BUILD.md` mit allen CMAKE_ARGS fur Hardware-Backends
  - Spike-basierte Architekturentscheidungen: zeitboxed Experimente mit klaren Erfolgskriterien

---

## Feature-Wunsche

Uber alle Notebooks hinweg tauchen wiederkehrende Feature-Ideen auf, die Samuel noch nicht gebaut hat:

**AI & Automatisierung:**
- Lokales LLM ohne Cloud — der Kern des NPU-Projekts, noch ungelost
- Strukturiertes personliches Wissenssystem mit Kategorien "personlich" und "arbeit" (Self_AI_V2) — mehr als nur NotebookLM
- LLM-Response-Caching in mAImory via Redis (Hash des E-Mail-Textes als Cache-Key, TTL 24h)
- ML-basiertes Deal-Scoring fur Keeper statt regelbasiertem Ansatz

**Infrastruktur & DevOps:**
- Prometheus + Grafana fur alle Projekte als einheitliches Monitoring-Dashboard
- CI/CD-Pipeline fur Keeper (war fur mAImory geplant, dort aber auch nur erwaht)
- Chaos-Engineering-Tests fur Keeper's Failure-Scenarios

**Privatsphare & Sicherheit:**
- DSGVO-Compliance fur mAImory (explizit auf Post-MVP verschoben, nur relevant fur EU-Markterweiterung)
- Rate Limiting pro Nutzer in mAImory (Anti-Abuse)

---

## Zukunftsplane — Wohin steuert Samuel?

Die Notebooks zeigen eine klare Richtung, auch wenn Samuel sie nicht explizit ausgesprochen hat:

**Das Startup-Modell:** mAImory ist nicht nur ein Uni-Projekt. Samuel hat es mit echten Business Goals dokumentiert — 10 MAU → 100 MAU → 1000 MAU, geografische Expansionsstrategie fur LATAM und Sudostasien, VC-Investor-Persona. *"Wir haben keine Architektur fur Google gebaut (Microservices), sondern fur ein Startup mit einem Entwickler (Monolith). Aber wir haben die Sollbruchstellen so designed, dass wir wachsen konnen, wenn der Erfolg eintritt."* Das ist kein akademischer Text — das ist ein Pitch.

**Edge AI als langfristiges Ziel:** Die Investition in das NPU-Projekt (Lesen des vollstandigen Hexagon V73 Programmer's Reference Manual, 400.000+ Zeichen Hardware-ISA-Dokumentation) zeigt, dass Samuel auf-device AI nicht aufgegeben hat. Der Markt (Qualcomm Whitepaper vom Februar 2025: *"AI disruption is driving innovation in on-device inference"*, DeepSeek R1) bewegt sich in seine Richtung.

**Privatsphare als Designprinzip:** Digital_Anonym zeigt, dass Privacy fur Samuel kein Add-on ist, sondern eine Grundhaltung. *"Anonymitat beginnt nicht im Netz — sie beginnt im Kopf."* In mAImory taucht das als konkretes Designprinzip auf: keine E-Mail-Inhalte in der Datenbank gespeichert, stateless Processing-Pipeline. Das sind keine zufalligen Entscheidungen.

---

## Verbindungen — Ideen, die mehrere Projekte verbinden

```
Self_AI_V2 ──────────────────────────────────────────────────── AI_NPU_Agent
     |                    (gleicher LLM-Stack, gleiche Hardware)        |
     |                                                                   |
     v                                                                   v
mAImory ──────────────────────────── Software_Architecture (Kurs)   NPU Lessons
(LLM-Adapter-Architektur)              (ADD Methodik)              (futern Keeper?)
     |
     v
Keeper_Amazon/System
(LangGraph Agents — gleiche Toolchain)
```

**mAImory + Self AI V2:** Beide arbeiten mit LLM-Integration und Adapter-Patterns. Self_AI_V2 wollte lokales Inference, mAImory nutzt Cloud-APIs mit Fallback-Kette. Die Lessons Learned aus dem NPU-Projekt — "Black-Box-APIs sind riskant", "Hardware-Integration ist R&D, nicht Implementation" — hatten mAImory's Fallback-Design direkt begrunden konnen.

**Keeper + AI-Verbesserungen:** Keeper verwendet bereits LangGraph fur Agent-Orchestration (Price Monitor Agent, Deal Finder Agent, Alert Dispatcher Agent). Der logische nachste Schritt ware, Keeper's Deal-Scoring von regelbasiert auf LLM-gestutztes Modell umzustellen — ein Feature, das Samuel auf der Wishlist hat.

**NPU-Lessons + Alle Projekte:** Die organisatorischen Erkenntnisse aus dem NPU-Projekt sind universal: "Reproduzierbarkeit ist Konig", "Documentation in Echtzeit", "requirements.txt und setup.sh sind Voraussetzungen, keine Nachgedanken." Diese Standards fehlen auch bei Keeper.

---

## Was Samuel antreibt

Hinter allen Projekten steckt ein konsistentes Motivationsbild:

**Autonomie durch Automatisierung.** Statt Preise manuell zu vergleichen — Keeper. Statt Termine manuell aus E-Mails herauszulesen — mAImory. Statt von Cloud-Diensten abhangig zu sein — lokales LLM auf dem NPU. Der Grundantrieb ist immer derselbe: ein Problem losbar machen und dann nie wieder manuell erledigen mussen.

**Systeme verstehen, nicht nur benutzen.** Der Hexagon V73 ISA wurde nicht fur ein Praktikum gelesen — Samuel wollte verstehen, was die Hardware wirklich kann. Die ADHS-Diagnostik wurde nicht einfach abgenickt — er fragte: *"Warum brauchen die fur eine Diagnose im Erwachsenen Alter meine Grundschulzeugnisse?"* Das ist die Haltung eines Ingenieurs.

**Privatsphare als Wert, nicht als Feature.** Digital_Anonym zeigt, dass Samuel nicht nur uber Privacy nachdenkt, sondern sie lebt. *"Wissen ist kein Schutz. Verhalten ist Schutz."* In mAImory schlagt sich das direkt in Architekturentscheidungen nieder.

**Startup-Pragmatismus gegenuber akademischer Perfektion.** *"Progress > Perfection (BG-4)"* steht in mAImory, und es gilt fur alle Projekte. Keeper ist 6.2/10 und trotzdem wertvoller als ein perfektes Toy-Projekt.

---

## Priorisierung — Was ware der kluge nachste Schritt?

| Prioritat | Idee | Aufwand | Warum jetzt |
|-----------|------|---------|-------------|
| 1 | Keeper: Async-Bug fixen (`await` in Deal-Search) | 1-2h | Groste Impact/Aufwand-Ratio |
| 2 | Keeper: Batch-Optimierung Keepa API | 8-12h | 90% Token-Ersparnis, 10x Performance |
| 3 | Keeper: Duale DB-Schemas zusammenfuhren | 20-30h | Wurzel aller Instabilitaten |
| 4 | mAImory: Implementierung starten | variabel | Architektur ist fertig — jetzt bauen |
| 5 | NPU revisit mit reiferer Toolchain | variabel | Markt hat sich weiterentwickelt |

*Die gunstigsten Fixes (1 und 2) liegen in Keeper. Der strategisch wichtigste Schritt ist mAImory vom Dokument zum laufenden System zu machen.*
