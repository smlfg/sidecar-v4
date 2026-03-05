# Lernreise: Samuel Fleigs Weg vom Student zum Systembauer

*Ein chronologischer Bericht, September 2025 bis Februar 2026*

---

## Der Anfang: Ein Student mit grossen Ambitionen

Samuel Fleig ist kein Student, der sich mit Pflichtstoff begnuegt. Schon bevor die ersten Zeilen dieser Aufzeichnungen entstehen, hat er monatelang an eigenen KI-Systemen gearbeitet. Er formuliert es selbst so, in seiner charakteristisch direkten Art:

> *"Da ich jetzt schon 6 Monate an einem eigenen KI System mit generativer KI arbeite kenne ich aus der Praxis ein paar der Tücken die über ein solches System auftreten können."*
> — Software Architecture Notebook (SWA)

Das ist der Samuel, der im Herbst 2025 in diese Periode eintritt: jung, technisch hungrig, ungeduldig mit Theorie, aber instinktiv stark in praktischem Denken. Er baut Systeme, bevor er deren akademischen Rahmen kennt. Er findet Fragen interessanter als Antworten. Und er scheitert produktiv — was sich als seine wertvollste Eigenschaft herausstellen wird.

---

## Fruehjahr 2025: Das NPU-Abenteuer — In die Wand gefahren

Die erste grosse Lektion kommt nicht aus dem Hoersaal, sondern aus einem technischen Fiasko.

Samuel will ein LLM direkt auf der NPU (Neural Processing Unit) seines Dell Latitude 7455 mit Snapdragon X Elite laufen lassen. Kein Cloud-Zugriff, keine Latenz, echte Privatsphere. Die Idee ist mutig. Die Ausfuehrung trifft auf eine brutale Realitaet.

Zwei Strategien, beide scheitern. Die Qualcomm-Bibliothek `qai_hub_models` gibt bei `from_pretrained()` still und leise `None` zurueck — kein Fehler, keine Erklaerung, kein Signal. Das nachfolgende Debugging ist wie Stochern im Nebel. Strategie 2 mit `llama-cpp-python` und NPU-Backends kompiliert scheinbar erfolgreich:

> *"pip install kann eine erfolgreiche Installation melden, auch wenn die Kompilierung für spezifische Hardware-Backends nicht erfolgreich war oder die CMAKE_ARGS ignoriert wurden."*
> — AI NPU Agent Notebook (Lessons Learned)

Am Ende landet das Projekt im "Demo-Modus" — fest verdrahtete Antworten statt echter NPU-Inferenz. Das Notebook, das diese Erfahrung dokumentiert, traegt bezeichnenderweise den Titel: "Lessons Learned and Strategic Realignment".

Die wichtigste Erkenntnis aus dieser Phase ist eine Meta-Einsicht, die Samuel sauber benennt:

> *"Das Projekt war von Natur aus kein reines Software-Implementierungsprojekt, sondern ein Forschungs- und Entwicklungsvorhaben (R&D), das sich mit unbekanntem Terrain auseinandersetzte."*
> — AI NPU Agent Notebook

Er hat einen Implementierungsauftrag angenommen, der in Wirklichkeit ein Forschungsauftrag war. Diese Unterscheidung wird ihn nicht mehr loslassen.

Parallel entsteht im Juni 2025 das Digital_Anonym-Notebook — eine tiefe Auseinandersetzung mit Privatsphare, Tor-Netzwerken und digitaler Sicherheit. Der Satz, der dabei herausdestilliert wird, koennte als Lebensphilosophie stehen: *"Anonymität beginnt nicht im Netz – sie beginnt im Kopf."*

---

## September 2025: Keeper — Das erste echte System

Nach dem NPU-Debakel macht Samuel etwas Kluges: Er baut etwas, das funktioniert.

Keeper ist ein Amazon-Preisbeobachtungs-System mit vollstandiger Data-Engineering-Pipeline. Keepa API als Datenquelle, Apache Kafka fuer Event-Streaming, PostgreSQL als zuverlassige Datenbank, Elasticsearch fuer schnelle Suche, LangGraph fuer Agenten-Orchestrierung — acht Docker-Services, koordiniert in einem Compose-File. Die Architektur-Bewertung: 8 von 10. Die Performance-Bewertung: 4 von 10.

Keeper ist kein perfektes System. Es hat ein kritisches Problem: zwei parallele Datenbankschemas — ein asynchrones und ein synchrones — die nebeneinander existieren und Inkonsistenzen erzeugen. Und eine Performance-Bombe:

> *"Die aktuelle Implementierung ruft die Keepa API für jedes überwachte Produkt einzeln auf, anstatt die von Keepa angebotenen Batch-Abfragen zu nutzen. Für 100 Watches: 75 Minuten vs. 8 Minuten mit korrektem Batching."*
> — Keeper Amazon Notebook

Aber Keeper lehrt Samuel etwas Fundamentales: wie man technische Entscheidungen begruendet. Er weiss, warum er asyncpg statt psycopg2 verwendet. Er weiss, warum Kafka siebentagige Message-Retention hat. Er weiss, warum Elasticsearch eine separate Rolle von PostgreSQL uebernimmt. Das ist kein zufalliges Zusammenfuegen von Tools — das ist Systemdenken.

Das Keeper-Notebook entsteht erst im Februar 2026 (Erstellungsdatum: 20. Februar 2026), aber das System selbst laeuft schon lange. Samuel dokumentiert es retrospektiv — ein Zeichen, dass er gelernt hat, dass Dokumentation kein Afterthought sein darf.

---

## Dezember 2025 bis Januar 2026: mAImory — Theorie trifft Praxis

Dann kommt der Moment, wo Universitat und reale Projekte kollidieren. Prof. Volker Schwarzer an der Hochschule Worms verlangt im Kurs "Software Architecture 506" die Anwendung der ADD-Methodik (Attribute-Driven Design) auf ein echtes Projekt.

Samuel waehlt mAImory — ein System, das aus E-Mails automatisch Termine und Erinnerungen extrahiert und in Kalender-Events umwandelt. Es ist gleichzeitig sein Universitaetsprojekt und eine echte Startup-Idee.

Der erste Kontakt mit der akademischen ADD-Methodik provoziert eine ehrliche Reaktion:

> *"ich kotze im strahl wegen ADD, es kommt mir so unnötig vor, ich wünsche mir mein system so, wo sind die haken meines wishfull thinkings"*
> — Software Architecture Notebook (SWA), Freewriting-Notizen

Aber genau darin steckt der Wendepunkt. Samuel fragt die richtige Frage: Wo sind die Haken meines Wunschdenkens? Das ist nicht Kapitulation vor der Theorie — das ist Nutzung der Theorie als Diagnosewerkzeug.

Er arbeitet sich durch alle sieben ADD-Schritte. Er schreibt drei vollstandige Quality Attribute Scenarios (QAS). Er fuhrt einen formellen QAW-Workshop durch — mit vier erfundenen Stakeholder-Personas (Entwickler, BWL, Investor, Architekt), von denen alle er selbst sind. Er entscheidet bewusst GEGEN Microservices:

> *"Microservices: REJECTED — Modularity is good, but too much overhead for 1 developer!"*
> — mAImory Notebook

Und er entscheidet GEGEN Over-Engineering — in einem Dokument, das selbst 40+ Seiten umfasst. Die Ironie ist ihm nicht entgangen. Das KI-Feedback, das er bekommt und behaelt, trifft es:

> *"Dein Projekt ist kein Over-Engineered Monster, sondern ein chirurgisch präzises MVP."*
> — mAImory Notebook, Modell-Feedback

Die Abgabe war der 9. Januar 2026. Die letzte aktive Session im mAImory-Notebook: zehn Stunden vor Deadline. Danach: Zufall und Chaos, aber strukturiert.

---

## Januar 2026: SE Fundamentals — Unter Feuer

Gleichzeitig laeuft die zweite Prufung: Software Engineering Fundamentals bei Prof. Dr. Jens Kohler. 6 CP, 90-Minuten-Klausur. Samuel ist im zweiten Versuch.

Das SE-Notebook zeigt den vollstandigen Arc eines Lernenden unter Druck. Die ersten 32 Chat-Turns sind makellos strukturiert — formale, akademische Fragen zu jedem Kursthema, sauber wie ein Lehrplan. Dann, in Turn 34, erscheint Samuel selbst: er verbindet O-Notation mit der Software-Architektur seiner Projekte.

Und dann, Turn 60:

> *"ich 8 stunden ist die Klausur / ich bin im 2. Versuch / Konzepte habe ich alle verstanden / aber einzelheiten nicht / notierung und feinheiten"*
> — SE Fundamentals Notebook, Turn 60

Die Syntax bricht zusammen. Das ist kein Faulheit — das ist kognitiver Overload, der sich in der Grammatik niederschlaegt. Acht Stunden bis zur Klausur, 2. Versuch, und er weiss genau was er nicht kann: Notationsprazision. Nicht das Konzept. Die Details.

Er arbeitet sieben Stunden durch. Dann, eine Stunde vor der Klausur:

> *"Noch eine Stunde bis zur Klausur"*
> — SE Fundamentals Notebook, Turn 72

Nach der Klausur, Turn 82:

> *"Ja so ist vorbei warum haben wir Domain driven Design nicht besprochen erklärt geübt"*
> — SE Fundamentals Notebook, Turn 82

DDD war auf der Prufung. Er hatte es nicht hinreichend vorbereitet. Der Vorwurf richtet sich an "wir" — Samuel betrachtet NotebookLM als Lernpartner mit geteilter Verantwortung. Das ist bemerkenswert ehrlich und ein bisschen ruhrend.

---

## Februar 2026: ADHS-Re-Diagnose — Die persoenliche Ebene

Waehrend der akademische Druck laeuft, oeffnet Samuel am 3. Februar 2026 ein neues Notebook: ADHS. Er sucht im Erwachsenenalter eine formale Wiederholung seiner Kindheitsdiagnose von 2010.

> *"ich wurde 8 Jahre meiner Jugend mit Ritalin behandelt"*
> — ADHS Notebook

Er hat als Kind freiwillig die 3. Klasse wiederholt. Er hatte Konzentrationsprobleme, war "leicht ablenkbar", "träumt vor sich hin". Jetzt, als junger Erwachsener, navigiert er das medizinische System mit derselben Pragmatik, mit der er technische Systeme debuggt: Er sammelt Grundschulzeugnisse als objektive Evidenz, fuellt BDI-II und WURS-K Frageboegen aus, schreibt professionelle E-Mails an die Praxis.

> *"Warum brauchen die Für eine Diagnose im Erwachsenen Alter meine Grundschul zeugniss"*
> — ADHS Notebook

Die Frage dahinter ist nicht Widerstand — es ist Neugier. Er will das System verstehen, nicht nur navigieren.

---

## Wendepunkte: Die Momente, wo etwas klickte

Aus all diesen Daten treten drei echte Wendepunkte hervor:

**1. NPU als R&D-Erkenntnis (frueh 2025)**
Der Moment, wo Samuel versteht, dass "LLM auf NPU laufen lassen" kein Implementierungs-Task war, sondern ein Forschungsprojekt. Diese Unterscheidung — R&D vs. Execution — wird seinen gesamten spateren Ansatz formt. Er fragt seitdem zuerst: Was ist das eigentlich fur eine Aufgabe?

**2. ADD-Frustration als Diagnosefrage (Dezember 2025)**
*"wo sind die haken meines wishfull thinkings"* — der Moment, wo Samuels naturliche Ungeduld mit akademischer Methodik umschlagt in genuine Nutzung. Die Theorie wird zum Spiegel, nicht zur Bremse.

**3. Selbstdiagnose in der Prufungs-Nacht (Januar 2026)**
*"Konzepte habe ich alle verstanden / aber einzelheiten nicht / notierung und feinheiten"* — einer der prazisesten Selbstbefunde, die ein Lernender in Echtzeit formulieren kann. Wer weiss, was er nicht weiss, kann es lernen.

Was diese sechs Monate zusammenhalt: Samuel baut schnell, scheitert konkret, und dokumentiert beides mit bemerkenswerter Ehrlichkeit. Das ist die seltenste Kombination.
