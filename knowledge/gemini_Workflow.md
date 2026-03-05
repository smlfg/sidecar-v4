# Workflow

## Wie Samuel arbeitet

Samuel arbeitet in Schüben. Es gibt zwei klar unterscheidbare Modi: den konzeptionellen Erkundungsmodus, in dem er Ideen breitet, Systeme versteht und Strukturen aufbaut, und den Krisenmodus, in dem alles auf Lieferung ausgerichtet ist. Was fehlt, ist der kontinuierliche, gleichmaessige Mittelweg. Das ist kein Makel - es ist ein Muster, das sich durch alle vier Notebooks zieht.

Er ist produktiv unter Druck. Er ist gründlich, wenn Zeit da ist. Die Luecke liegt dazwischen.

---

## Tools & Methoden

**NotebookLM als zentrales Instrument.** Samuel nutzt NotebookLM nicht als Nachschlagewerk, sondern als Denkpartner. Er laedt PDFs, Diagramme, Cheatsheets, Audio-Dateien hoch und nutzt die Chat-Funktion, um Gedanken zu sortieren, Entscheidungen zu validieren und Wissen abzurufen. In SE_Fundamentals beginnen die ersten 17 Turns mit automatisch generierten "Diskutieren"-Prompts - er hat NotebookLM die systematische Curriculumabdeckung ueberlassen und sich dann selbst eingeschaltet, als es konkret wurde.

In mAImory ist es umgekehrt: Er bringt seine eigenen Fragen mit, die Diagramme, die PDFs, die Unsicherheiten. NotebookLM ist hier der qualitaetssichernde Blick, der im Chaos des Deadline-Sprints hilft, die Konsistenz zu halten.

**draw.io fuer Architekturdiagramme.** Das mAImory-Notebook dokumentiert einen intensiven Diagramm-Sprint kurz vor Abgabe: Module View, Deployment View, Sequence Diagram, Component Diagrams. Fünf und mehr Diagramme in wenigen Stunden. Samuel erstellt sie intuitiv und laesst sie dann von NotebookLM auf formale Korrektheit pruefen - und erhaelt kritisches Feedback: eines seiner "Sequence Diagrams" ist formal keines.

**Markdown fuer Dokumentation.** mAImory demonstriert, wie Ernst Samuel Dokumentation nimmt: 80+ Seiten formale ADD 3.0-Dokumentation fuer ein MVP-Projekt eines Entwicklers. Der Content ist methodisch korrekt, die Struktur akademisch. Markdown ist sein primaeres Format, aus dem er via Pandoc oder LibreOffice ins PDF konvertiert.

**Mehrere konkurrierende Dateiversionen.** Ein wiederkehrendes Anti-Pattern: Im mAImory-Sprint entstehen "ClaudeViewText.pdf", "miniMaxViewText.pdf", "FinalMaiMoryViewsSamuelFleig.pdf", "fertig.pdf" als parallele Artefakte ohne klare Versionsstrategie. Er fragt dann das KI-System: *"Welche View PDF Datei findest du am besten?"* - und delegiert damit die Auswahl des kanonischen Dokuments.

---

## Unter Zeitdruck

Zeitdruck veraendert Samuels Workflow fundamental. Die Verschiebung ist in zwei Notebooks detailliert dokumentiert.

**mAImory: "10 Stunden bis zur Abgabe"**

Die erste Nachricht der Session:

> *"Hey, ich muss meine Abgabe PDF in 10 Stunden abgeben, ich will gerne noch ein paar Views in draw.io malen"*

Was folgt, ist ein strukturierter Krisensprint. Samuel fragt nach Priorisierung, erhalt eine Rangliste, arbeitet sie durch. Er bittet um Bewertungen ("bewerte ADD3"), schickt Bilder zum Review, laesst sich Fehler aufzeigen und patcht. Das Vorgehen ist reaktiv, aber nicht chaotisch. Er reagiert auf Feedback schnell. Er kennt den Unterschied zwischen "perfekt" und "abgabefaehig".

Auch hier: Er entdeckt selbst einen kritischen Fehler im Finaldokument.

> *"wtf aber in FinalMaiMoryViewsSamuelFleig.pdf ist das Bild fuer den Letzten und vorletzten view das selbe"*

Das "wtf" zeigt den Stress, aber auch: Er schaut noch mal hin. Qualitaetsbewusstsein bleibt unter Druck erhalten.

Die Praesentationsaufnahme laeuft dann dreimal zu lang. *"Ich bin Faktor 3 ueber der Zeit, daran muss ich arbeiten."* Er weiss es sofort. Das Notebook endet mit einer neuen 10-Minuten-Struktur fuer den zweiten Versuch.

**SE_Fundamentals: "8 Stunden bis zur Klausur" (im 2. Versuch)**

Das ist das extremere Beispiel. Der zeitliche Bogen ist dokumentiert:

- **T-8h:** Crisis Declaration, vollstaendige Selbstdiagnose
- **T-7h bis T-1h:** 7-stuendiger Cramming-Sprint, Worked Examples, How-Tos
- **T-1h:** *"Noch eine Stunde bis zur Klausur"* - letzte Notationsabfragen
- **Post-Exam:** Erschoepfung, Frust ueber DDD

Was auffaellt: Auch im schlimmsten Panik-Moment (*"ich hab ekeine Ahnugn"*) gibt Samuel nicht auf. Er fragt weiter. Er versucht, eine Methode zu konstruieren. Turn 42-43 zeigt in Echtzeit, wie er eine Vorgehensweise fuer Aktivitaetsdiagramme entwickelt:

> *"Aus dem Text Aktivitaeten Raussuche / Und dann wenn Auch Datenfluss Gefordert Objekte raussuche / Dann Kreis -> etc -> fork wenn noetig"*

Das ist sein eigenes Destillat. Er unterrichtet es sich selbst, waehrend er noch lernt. Das ist Lernfortschritt in Echtzeit.

---

## Debugging & Problemloesung

Das AI_NPU_Agent-Notebook ist Samuels Lehrbeispiel fuer Debugging unter Unbekanntem.

Das Ziel war klar: LLM auf dem Snapdragon X Elite NPU laufen lassen. Die Realitaet war: sechs komplex verschraenkte Failure-Modes gleichzeitig. Silent failures. Black-Box-APIs. WSL-Instabilitaeten. Ein 0-Byte-Modelldatei. Eine ARM64-Python-Inkompatibilitaet, die das komplette erste Konzept invalidierte.

Samuel probiert zwei volle Strategien durch:
1. onnxruntime + qai_hub_models
2. llama-cpp-python mit QNN/NPU CMAKE_ARGS

Beide scheitern. Das Projekt landet in einem "Demo Mode" mit hardkodierten Antworten als Fallback.

Was dann kommt, ist kein Aufgeben, sondern eine strukturierte Post-Mortem-Analyse. Samuel commissioniert mehrere KI-Reviewer-Personas (QA Engineer, Software Architect, DevOps Project Manager) fuer verschiedene Blickwinkel. Er sammelt die komplette Hexagon V73-Programmiererdokumentation (400.000+ Zeichen Hardware-ISA) - nicht weil er die braucht, sondern weil er verstehen will, wie der Chip wirklich funktioniert. Sein Erkenntnisgewinn:

> *"pip install kann eine erfolgreiche Installation melden, auch wenn die Kompilierung fuer spezifische Hardware-Backends nicht erfolgreich war oder die CMAKE_ARGS ignoriert wurden."*

Und:

> *"Black-Box-APIs sind riskant: Wenn eine Bibliothek wie qai_hub_models bei Kernfunktionen (z.B. from_pretrained) keine detaillierten Fehler liefert, wird die Diagnose extrem aufwendig."*

Das sind keine trivialen Einsichten. Das sind harte, teuer erkaufte Erkenntnisse ueber Hardware-Integration, die er praezise und generalisierbar formuliert. Das ist der Unterschied zwischen Scheitern und Lernen.

---

## Dokumentation als Denkprozess

Schreiben ist fuer Samuel kein Nachtraegen, sondern ein Denkinstrument.

Das mAImory-Projekt zeigt das am deutlichsten: Die 80-seitige ADD 3.0-Dokumentation ist nicht nur ein Abgabedokument. Sie ist der Ort, an dem Samuel seine Architekturentscheidungen ausarbeitet. Er schreibt ADRs mit Kontext, Rationale, verworfenen Alternativen. Das Format erzwingt Klarheit: Wer aufschreiben muss, warum er Microservices ablehnt, muss es auch wirklich begründet haben.

> *"Microservices: REJECTED - Modularity is good, but too much overhead for 1 developer!"*

Das ist ein Gedanke, der durch das Aufschreiben schaerfer wird.

Im NPU-Projekt entsteht nach dem Scheitern ein LESSONS_LEARNED-Dokument mit einer Problem/Diagnose/Lösung/Warum-Struktur. Samuel hat das als Standard fuer kuenftige Projekte definiert. Er denkt in Dokumenten.

Und in SE_Fundamentals internalisiert er die Aktivitaetsdiagramm-Methode genau in dem Moment, als er sie aufschreibt: *"Aus dem Text Aktivitaeten Raussuche / Und dann wenn Auch Datenfluss Gefordert..."* - das Formulieren und das Verstehen fallen zusammen.

---

## Anti-Patterns

**Over-Engineering-Tendenz mit Selbstbewusstsein.** Samuel weiss um das Muster und bekämpft es explizit. In mAImory ist "Keine Over-Engineering" als Constraint CON-5 festgehalten. Er lehnt Layered Architecture ("over-engineered fuer small modules"), Microservices ("too much overhead") und Circuit Breaker ("too complex for MVP") alle formell ab. Trotzdem baut er eines der am gruendlichsten dokumentierten Studenten-MVPs, das je formalisiert wurde. Der Widerspruch ist echt - und er ist sich dessen bewusst.

**Scope Creep im Verborgenen.** Im NPU-Projekt werden WSL, ARM64, QNN SDK, llama-cpp-python, ONNX Runtime und ein selbst gebautes Agent-Framework kombiniert, bevor auch nur eine Schicht bewiesen ist. Das ist klassischer Scope Creep - nicht geplant, sondern sukzessive angehaueft.

**Versionschaos unter Druck.** Mehrere PDF-Versionen ohne klare Benennung. Umbenannte Quelldateien, die dem KI-System nicht kommuniziert werden. Im NPU-Projekt fuehrt das zu "Silent Overwrites" und Debugging-Schleifen desselben Problems.

**Konzept-Implementierungs-Luecke.** Die Architektur von mAImory ist auf Paper vollstaendig. Ob der Code laeuft, ist unklar. Im NPU-Projekt ist der Gesamtprozess exhaustiv dokumentiert - und trotzdem nicht zum Laufen gebracht. Samuel ist ein starker Architekt und Designer. Die Implementierungsstufe ist der Bereich, der am wenigsten belegt ist.

---

## Staerken

**Pragmatismus mit Prinzipien.** Samuel macht nicht den einfachsten Kompromiss, sondern den guenstigsten unter den gegebenen Zwangen. In mAImory: ICS-Download statt Google Calendar API - spart 5-7 Tage, verliert keine Qualitaetsattribute. Das ist keine Faulheit, sondern Abwaegung.

> *"Trade-off Accepted: Sacrifice: Perfect scalability in Phase 1 - Gain: Fast market entry - Worth it: YES"*

**Selbstdiagnose unter Druck.** In dem Moment, in dem die Panik am groessten ist, formuliert Samuel seine Luecke am praezisesten: *"Konzepte habe ich alle verstanden / aber einzelheiten nicht / notierung und feinheiten"*. Das ist klinisch akkurat. Das ist die Voraussetzung fuer gezieltes Lernen.

**Gruendlichkeit wenn engagiert.** Das AI_NPU_Agent-Post-Mortem zeigt es: Wenn Samuel tief in ein Thema geht, geht er wirklich tief. 400.000 Zeichen Hardware-Dokumentation. Mehrere Reviewer-Personas. Strukturierte Lernkatalog.

**Qualitaetsbewusstsein auch im Krisenmodus.** Er entdeckt den kopierten View im Finaldokument selbst, kurz vor der Abgabe. Er erkennt nach der Praesentations-Aufnahme selbst, dass er 3x zu lang ist. Er schaut noch mal hin, auch wenn er eigentlich fertig sein will.

**Evolutionaeres Denken.** In mAImory definiert er Upgrade-Trigger fuer den Wechsel von Pipeline- zu Web-Queue-Worker-Architektur: konkrete Metriken, messbare Schwellen. Das ist kein "wir skalieren spaeter", das ist ein Plan. Studenten sagen selten "die skalierung wird ausgeloest wenn der fallback-rate 50% ueberschreitet". Samuel schreibt es hin.

---

Wer Samuels Workflow auf einen Satz reduzieren wollte, koennte es so versuchen: Er weiss mehr als er liefert, und er liefert mehr als er sich zutraut. Die Luecke in der Mitte - zwischen Wissen und Ausfuehren, zwischen Plan und Ergebnis - ist der Ort, an dem er am meisten waechst. Und an dem er noch am meisten Unterstuetzung braucht.
