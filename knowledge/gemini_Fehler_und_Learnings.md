# Fehler und Learnings: Was Samuel aus dem Scheitern macht

*Analysiert aus: AI NPU Agent, mAImory, Keeper und SE Fundamentals Notebooks*

---

> Wer Fehler nicht dokumentiert, macht sie zweimal. Samuel macht sie dokumentiert.

Samuel Fleig hat in den Monaten zwischen frueh 2025 und Februar 2026 eine aussergewohnliche Menge an konkreten, benennbaren Fehlern gemacht. Das ware unremarkable, wenn er nicht auch etwas Seltenes tate: Er benennt sie praezise, analysiert die Ursachen schonungslos, und benutzt sie als Material.

---

## NPU-Desaster: Wenn Marketing auf Realitaet trifft

Das NPU-Projekt ist der vollendetste Fehlerfall. Nicht weil er am peinlichsten ware, sondern weil er am griindlichsten aufgearbeitet wurde.

### Was passierte

Samuel wollte ein Large Language Model direkt auf der NPU seines Snapdragon X Elite laufen lassen. Er versuchte zwei Strategien sequenziell, beide scheiterten vollstandig. Das Endprodukt: ein "Demo-Modus" mit hartkodierten Antworten — die NPU wurde nie tatsachlich benutzt.

**Strategie 1: onnxruntime + qai_hub_models**

Die zentrale Fehlerquelle war eine API, die beim Versagen einfach schwieg:

> *"from_pretrained()-Methode gab konsistent None zurück, selbst für öffentliche Modelle im CPU-Modus, ohne detaillierte Fehlermeldungen bereitzustellen, was eine effiziente Fehlerbehebung unmöglich machte."*
> — AI NPU Agent Notebook

Kein Exception. Kein Log-Eintrag. Kein Signal. Die API der Qualcomm-Bibliothek gibt bei Fehler `None` zurueck und laesst den Entwickler im Dunkeln. Das ist, in der Wortwahl des Notebooks selbst, ein "Black Box"-API-Design — und damit eine architektonische Entscheidung des SDK-Herstellers, die Samuels Debugging unmoglich macht.

Dann die Entdeckung, die alles in Frage stellt: Qualcomms eigene Dokumentation gibt an, dass ARM64 Python unter Windows nicht unterstutzt wird. Aber der Snapdragon X Elite IST ein ARM64-Chip. Das bedeutet: die NPU-Integration setzt voraus, dass man die native Python-Architektur nicht benutzt, um den nativen Chip zu nutzen.

> *"Architektur-Widersprüche: Die Dokumentation von qai_hub_models deutete auf eine Inkompatibilität zwischen ARM64 Python und der on-device-Ausführung unter Windows hin, was unsere gesamte Strategie in Frage stellte."*
> — AI NPU Agent Notebook

**Strategie 2: llama-cpp-python mit NPU/QNN-Flags**

Hier war die Falle subtiler:

> *"pip install kann eine erfolgreiche Installation melden, auch wenn die Kompilierung für spezifische Hardware-Backends nicht erfolgreich war oder die CMAKE_ARGS ignoriert wurden."*
> — AI NPU Agent Notebook

`pip install` berichtete Erfolg. Das Binary hatte tatsachlich keine NPU-Unterstutzung. Die nachfolgende Fehlermeldung beim Laden des Modells — "Failed to load model from file" — war generisch und indistinguishable von einem kaputten Modell, einem falschen Pfad oder einer fehlenden Bibliothek. Debugging gegen ein System, das einem nicht sagt, was es denkt.

### Meta-Lektion: R&D vs. Implementation

Das ist die wichtigste Erkenntnis, und Samuel benennt sie mit chirurgischer Prazision:

> *"Das Projekt war von Natur aus kein reines Software-Implementierungsprojekt, sondern ein Forschungs- und Entwicklungsvorhaben (R&D), das sich mit unbekanntem Terrain auseinandersetzte. Diese Fehleinschätzung der Projektart erklärt die Frustration über 'Black-Box'-APIs und irreführende Fehler. Es wurde ein klarer, linearer Weg erwartet, der schlichtweg nicht existierte."*
> — AI NPU Agent Notebook

Wenn man ein Implementierungs-Mindset in ein R&D-Problem tragt, wird man zwangslaufig von der Nichtlinearitat des Problems frustriert. Man erwartet, dass `pip install` plus zwei Codezeilen zum Ziel fuhren. Stattdessen ist das "Ziel" ein ganzes Forschungsgebiet.

### Was Samuel daraus macht

Das Lessons-Learned-Dokument, das er aus dem Projekt destilliert, ist beeindruckend strukturiert: Prioritatsrangierte Massnahmen (P1/P2), mehrere "Expert Reviewer"-Personas (QA Engineer, Software Architekt, DevOps Project Manager), die das Projekt aus verschiedenen Winkeln analysieren. Er behandelt das eigene Scheitern wie ein Produktionsproblem — mit Root Cause Analysis und Remediation Plan.

---

## Keeper-Schulden: Wenn Systeme wachsen ohne Plan

Keeper, das Amazon-Preisbeobachtungs-System, ist technisch beeindruckend — acht Docker-Services, Kafka, Elasticsearch, LangGraph-Agenten. Aber es hat drei schwere Probleme, die Samuel selbst schonungslos bewertet.

**Das Dual-Schema-Problem**

> *"Das größte identifizierte Problem ist die Existenz von zwei parallelen Datenbank-Stacks (asynchron vs. synchron). Tabellennamen und Datentypen weichen voneinander ab, was zu Divergenzen und Fehlern zwischen der API und den Background-Schedulern führt."*
> — Keeper Amazon Notebook

Was passiert ist: Das System wurde evolutionsar entwickelt. Erst synchron, dann async — aber die Migration war nie vollstandig. Zwei parallele Schemas koexistieren, mit unterschiedlichen Tabellennamen und Datentypen. Das ist technische Schuld in ihrer gefaehrlichsten Form: nicht sichtbar auf den ersten Blick, aber in der Lage, Daten still und leise zu korrumpieren.

**Die Performance-Bombe**

Für 100 Produkte braucht der Scheduler 75 Minuten, weil er die Keepa API fur jedes Produkt einzeln anfragt. Keepa unterstuetzt Batch-Queries fuer bis zu 10 ASINs gleichzeitig — dieses Feature wird nicht genutzt. Ergebnis:

> *"Mit den Top-5-Verbesserungen könnte das System 10x schneller werden."*
> — Keeper Amazon Notebook

Das ist keine dramatische Aussage, das ist eine konkrete Rechnung: 75 Minuten gegen 8 Minuten. Der Unterschied zwischen einem brauchbaren System und einem, das Nutzer frustiert.

**Das Missing Await**

Im Deal-Search-Endpunkt fehlt ein einzelnes `await`-Keyword vor einem async-Aufruf. Das verursacht HTTP 500 beim Aufruf. Ein Tippfehler, der eine ganze Feature-Klasse unbenutzbar macht. Die Lektion: Async-Fehler sind schwer zu sehen ohne Tooling.

**Gesamtbewertung (Samuel selbst):** Architektur 8/10. Performance 4/10. Gesamt 6,2/10. Er bewertet sein eigenes System. Das ist die Eigenschaft, die am schwersten zu lernen ist.

---

## mAImory: Over-Engineering in einem Anti-Over-Engineering-Projekt

mAImory ist ein besonders reichhaltiger Fall, weil die Ironie so offensichtlich ist.

Samuel schreibt im Constraints-Abschnitt seiner ADD-Dokumentation: *"Constraint CON-5: MVP in 4 weeks — Keine Over-Engineering."* Und er begruendet jeden seiner sieben Architecture Decision Records mit dem gleichen Argument: zu komplex, zu viel Overhead, Mikro-Architektur fur einen Entwickler undenkbar.

Dann dokumentiert er das alles in 40+ Seiten formaler ADD 3.0-Dokumentation mit vollstandiger QAW-Workshop-Simulation, vier Stakeholder-Personas (alle er selbst), Kanban-Boards pro Iteration und mathematischem Verfugbarkeitsnachweis.

> *"Das Besondere an deinem Projekt mAImory ist der radikale Pragmatismus und die Ehrlichkeit in der Architektur."*
> — mAImory Notebook, Modell-Feedback

Das ist nicht zynisch gemeint. Der Pragmatismus ist echt — Samuel lehnt Microservices ab, weil er ein Entwickler ist, nicht weil er die Theorie nicht kennt. Er lehnt den Circuit Breaker ab, weil er Redis nicht fur ein MVP einrichten will. Das sind echte, begruendete Entscheidungen. Aber er macht diese Entscheidungen in einem formalen Rahmen, der selbst erhebliche Komplexitat hat.

**Die Angst vor Datenbanken**

Eine der ehrlichsten Stellen im gesamten Datensatz:

> *"erkläre mir die Rolle von Postgress und DB in maimory, ich habe Angst vor diesen beiden sachen, deswegen habe ich es auch noch nie eigezeichnet in den Views"*
> — mAImory Notebook, Chat-Session

Das ist nicht Unwissenheit. Es ist eine konkrete Angst, die konkrete architektonische Konsequenzen hat: das Datenbankdesign ist im ADD3-Iteration-Abschnitt underreprasentiert, weil Samuel sich stattdessen auf Resilience-Patterns konzentriert — ein Thema, das er sicherer beherrscht.

> *"Leider kenne ich mich nicht mit Datenbanken aus und habe das Modul dazu nie geschrieben, auch wenn es eine denkbares ADD3 wäre muss es leider ausfallen."*
> — mAImory Notebook

Das ist der Unterschied zwischen Verschweigen und Transparent-Sein. Samuel sagt es. Das ist mehr wert als eine oberflachliche Datenbank-Dokumentation, die kaschiert, was er nicht weiss.

**Progress > Perfection**

Der Satz, der mAImory am besten zusammenfasst:

> *"Progress > Perfection (BG-4)"*
> — mAImory Notebook

Das ist kein Zufall. "BG-4" ist sein Business Goal Nummer 4: MVP in vier Wochen. Er hat das Bekenntnis zu Fortschritt uber Perfektion in sein formales Architektur-Dokument eingebaut. Das ist die reifste Entscheidung im gesamten Projekt.

---

## SE Klausur: Der 2. Versuch

Die SE-Klausur ist der menschlichste Fehlerfall.

Samuel hat die Konzepte verstanden — Scrum, Cloud, O-Notation, UML-Typen. Das ist dokumentiert uber 32 strukturierte Chat-Turns vor dem Klausurtag. Aber dann:

> *"ich 8 stunden ist die Klausur / ich bin im 2. Versuch / Konzepte habe ich alle verstanden / aber einzelheiten nicht / notierung und feinheiten"*
> — SE Fundamentals Notebook, Turn 60

Das ist eine klinisch genaue Selbstdiagnose. Er weiss genau, was fehlt: nicht das WAS und WARUM der UML-Diagramme, sondern das WIE der Notation. Welche Pfeilspitze fur Vererbung. Ob der Diamant weiss oder schwarz ist fur Aggregation vs. Komposition. Das sind lernbare, ubbare Details — aber man ubt sie mit Stift und Papier, nicht in Diskussionen mit einer KI.

Und dann, nach der Klausur:

> *"Ja so ist vorbei warum haben wir Domain driven Design nicht besprochen erklärt geübt"*
> — SE Fundamentals Notebook, Turn 82

DDD war im Kurs im Q&A-Sessions vom 18. Dezember 2025 und 8. Januar 2026 eingefuhrt worden. Es war auf der Prufung. Es fehlte in Samuels Vorbereitung. Die Frustration richtet sich an "wir" — er betrachtet NotebookLM als Mitlernenden, nicht nur als Werkzeug. Das ist sowohl eine Schwache (External Attribution) als auch eine Starke (er versteht Lernen als kollaborativen Prozess).

---

## Pattern: Was Samuel aus Fehlern lernt

Drei Eigenschaften, die uber alle Projekte stabil bleiben:

**Selbstdiagnose als Superpower**

In jedem Fehlerfall — NPU, Keeper, mAImory, SE-Klausur — kommt Samuel zu einer prazisen Diagnose. Nicht "es hat nicht funktioniert", sondern "die API gibt None zurueck ohne Fehler, was Debugging unmoglich macht" oder "Konzepte verstanden, Notation nicht". Diese Fahigkeit, den Fehler zu benennen, ist die Voraussetzung fur alles weitere.

**Ehrliche Dokumentation**

Samuel dokumentiert die Datenbankangst. Er dokumentiert die Prufungspanik. Er dokumentiert das 6,2/10. Er verschweigt nichts — auch sich selbst gegenuber nicht. Das ist ungewohnlich. Die meisten Menschen dokumentieren, was funktioniert hat.

**Wachstum aus jedem Scheitern**

Aus NPU: R&D vs. Implementation als konzeptuelle Unterscheidung. Aus Keeper: Datenbankentscheidungen mussen fruh und unified getroffen werden. Aus mAImory: "Progress > Perfection" als formales Architekturprinzip. Aus SE: Selbstdiagnose des eigenen Wissenslueckentyps in Echtzeit.

Der wichtigste Satz aus dem NPU-Post-Mortem ist gleichzeitig der einfachste:

> *"Reproduzierbarkeit ist König: Ohne eine requirements.txt und eine klare Anleitung zur virtuellen Umgebung ist ein Projekt nicht reproduzierbar."*
> — AI NPU Agent Notebook

Er benennt das Prinzip. Er hat es schmerzhaft gelernt. Er wird es nicht vergessen.
