# Studium: Samuels akademisches Profil an der Hochschule Worms

*Basierend auf: SE Fundamentals, Software Architecture und mAImory Notebooks*

---

## Hochschule Worms — Der Rahmen

Samuel Fleig studiert Informatik an der Hochschule Worms (HS Worms), einer Fachhochschule in Rheinland-Pfalz. Der Wintersemester 2025/26 zeigt ihn in einer der dichtesten akademischen Perioden seiner bisherigen Laufbahn: zwei anspruchsvolle Kurse gleichzeitig, ein echtes Projekt als Universitatsabgabe, und eine Prufung im zweiten Versuch — alles in einem Zeitfenster von drei Monaten.

Was Samuel von einem typischen Informatikstudenten unterscheidet: Er kommt nicht als Theoretiker zum praktischen Anwendungsfall. Er kommt als Praktiker, der lernt, seinen Instinkten einen formalen Rahmen zu geben. Das macht sein Lernprofil sowohl starker als auch ungewohnlicher.

---

## Software Architecture 506 — Theorie als Spiegel

**Kurs:** Software Architecture 506 (SWA 506) — Attribute-Driven Design
**Dozent:** Prof. Volker Schwarzer
**Sprache:** Englisch (Vorlesung und Prufung)
**Lehrbuch:** *Software Architecture in Practice*, Bass/Clements/Kazman, 4. Auflage 2021
**Quellen im Notebook:** 55

Dieser Kurs trifft Samuel an einer interessanten Stelle: Er hat bereits sechs Monate an eigenen KI-Systemen gearbeitet. Er kennt Trade-offs aus Erfahrung, nicht aus dem Lehrbuch. Das fuehrt zu einem charakteristischen Lernweg — er nutzt die akademische Methodik als Diagnosewerkzeug fuer sein eigenes Denken, nicht als externe Vorschrift.

Der erste Kontakt mit ADD ist ehrlich frustrierend:

> *"ich kotze im strahl wegen ADD, es kommt mir so unnötig vor, ich wünsche mir mein system so, wo sind die haken meines wishfull thinkings"*
> — SWA Notebook, Freewriting

Aber die zweite Halfte dieses Satzes ist entscheidend: Samuel fragt sofort, wo sein Wunschdenken bricht. Er kapituliert nicht vor der Methodik — er benutzt sie.

### Was er wirklich gelernt hat

Das SWA-Notebook dokumentiert 15 Konzepte auf Anwendungs- oder Verstandnisebene. Besonders bemerkenswert:

**ADD 3.0 auf Anwendungsebene:** Samuel fuhrte drei vollstandige ADD-Iterationen fur mAImory durch — einschliesslich des 8-schrittigen Quality Attribute Workshops, vollstandiger Architectural Decision Records (ADRs) und eines expliciten Upgrade-Pfads.

**Quality Attribute Scenarios (QAS):** Er schrieb drei vollstandige, korrekte QAS fur mAImory:
- Skalierbarkeit: 1000 gleichzeitige Nutzer in unter 2 Sekunden
- Modifizierbarkeit: LLM-Anbieterwechsel in weniger als 8 Entwicklerstunden
- Deployability: git push bis Production in weniger als 15 Minuten

Er versteht den Unterschied, den die meisten Studierenden nicht begreifen: dass ein Business Goal kein Quality Attribute ist.

> *"Falsch: Business Goal: Das System soll skalierbar sein. Richtig: Business Goal: Erreiche 1000 MAU in 6 Monaten → daraus folgt QA: Scalability."*
> — SWA Notebook

**Trade-off-Denken:** Jede Entscheidung in mAImory dokumentiert, was geopfert wird:

> *"BWL: Wir opfern jetzt QAS-1 (perfekte Skalierbarkeit) zugunsten von QAS-3 (MVP-Speed), weil wir ohne MVP gar keine User haben werden."*
> — SWA Notebook

**Evolutionare Architektur:** Der Upgrade-Pfad (Pipeline jetzt → Web-Queue-Worker bei 100 gleichzeitigen Nutzern) mit messbaren Triggerbedingungen ist laut Kursbewertern ungewohnlich anspruchsvoll fur ein Studierendenprojekt.

> *"Architekt: Upgrade Pfad — Sobald die Metriken zeigen, dass der Server blockiert, tauschen wir die synchrone Implementierung des AIService gegen einen AsyncQueueService aus. Die restliche App merkt davon nichts."*
> — SWA Notebook

Die Kursbenotung: 60% Dokumentation, 40% Prasentation. Samuel hat das korrekt internalisiert und entsprechend priorisiert.

---

## Software Engineering Fundamentals — Unter Prufungsdruck

**Kurs:** Software Engineering: Cloud, Big Data, and UML Models
**Dozent:** Prof. Dr. Jens Kohler
**Credits:** 6 CP (ca. 150 Stunden Gesamtaufwand)
**Prufungsformat:** 90-Minuten-Klausur (kein Hilfsmittel ausser Taschenrechner)
**Samuels Versuch:** 2. Versuch (Zweitversuch)

Dieser Kurs zeigt Samuel unter maximalen Bedingungen. Im zweiten Versuch bedeutet ein weiteres Scheitern potenziell den Ausschluss vom Studiengang.

Das SE-Notebook dokumentiert 50+ abgedeckte Themen, mit UML als dominierende Pruefungskategorie (60-70% der Punkte). Der Prufungsblock ist klar: Aktivitatsdiagramme, Klassendiagramme, Use-Case-Diagramme — alle mit praziser Notationspflicht.

**Was Samuel wirklich kann:**
- Konzeptuelle Erfassung aller UML-Diagrammtypen (verstanden)
- Systemdenken — er verbindet O-Notation spontan mit seiner Projektpraxis:

> *"Die Performance bei 1000 nutzern ist ja auch abhängig von der Software Architektur"*
> — SE Fundamentals Notebook, Turn 34

- Kritisches Denken unter Druck — er hinterfragt KI-Losungen:

> *"okay warum keine route, wenn Name + passwort / wenn richtig / dann Fork 2 Faktor / wenn nein / again"*
> — SE Fundamentals Notebook, Turn 40

- Selbst-Methodisierung: Nach schwierigen Aktivitatsdiagramm-Aufgaben entwickelt er seine eigene Vorgehensweise:

> *"Aus dem Text Aktivitäten Raussuche / Und dann wenn Auch Datenfluss Gefordert Objekte raussuche / Dann Kreis -> etc -> fork wenn nötig"*
> — SE Fundamentals Notebook, Turn 42-43

**Was er nicht konnte (eigene Diagnose):**

> *"Konzepte habe ich alle verstanden / aber einzelheiten nicht / notierung und feinheiten"*
> — SE Fundamentals Notebook, Turn 60

Weisse oder schwarze Diamanten. Offene oder geschlossene Pfeilspitzen. Ob ein 1..*-Attribut als Array codiert wird. Das sind Notationsdetails, die man nur durch Praxis mit Papier und Stift verinnerlicht — nicht durch KI-Diskussionen. Das ist der Kern seiner Vorbereitungsluecke.

Ungenuegend abgedeckt blieb Domain Driven Design (DDD) — ein Thema, das in den Q&A-Sessions vom 18. Dezember 2025 und 8. Januar 2026 als pruefungsrelevant eingefuhrt wurde und dann tatsachlich auf der Klausur erschien.

---

## Lernmuster: Wie Samuel eigentlich lernt

Uber alle Notebooks hinweg ergibt sich ein konsistentes Bild.

**Practitioner-First**
Samuel denkt erst vom System, dann von der Theorie. Er entwirft mAImory mental als Datenfluss (*"Nutzer -> Mail -> LLM -> response -> parsen -> user y/n -> api -> Kalender"*), bevor er ihn formalisiert. Die Theorie legitimiert seine Intuition — sie erzeugt sie nicht.

**Zwei-Phasen-Lernen**
Im SE-Notebook ist das exemplarisch: Phase 1 (Tage oder Wochen vor der Prufung) ist ein systematischer, ruhiger Curriculum-Durchlauf — formale Fragen, vollstandige Satze, akademisches Niveau. Phase 2 ist Krisenlernen — konkrete Aufgaben, fragmentierte Sprache, aktive Problemlosung. Beide Phasen sind produktiv auf verschiedene Weisen.

**Hypothesengetriebenes Hinterfragen**
Er akzeptiert keine Antworten blind. Er pruft sie gegen seine intuitive Erwartung. Wenn die Antwort nicht passt, fragt er nach dem Warum. Das zeigt sich sowohl in akademischen Kontexten (UML-Aufgaben) als auch in technischen Projekten (NPU-Debugging).

**KI als Lernpartner, nicht als Antwortmaschine**
Seine Nutzung von NotebookLM (83 Fragen uber vier Notebooks, zwei strukturierte Studiensessions vor der SE-Prufung) zeigt ein reifes Verstandnis des Werkzeugs: er delegiert Meta-Entscheidungen ("Welche Altklausur-Aufgaben sollen wir noch besprechen?"), er nutzt es fur Synthese ("noch mal die komplette richtige Antwort"), er behandelt es als Instanz mit geteilter Verantwortung.

---

## Staerken: Was Samuel wirklich gut kann

**Selbstdiagnose in Echtzeit**
Die Formulierung "Konzepte verstanden, Notation nicht" ist keine Platitude — sie ist eine prazise klinische Selbstbeobachtung unter Prufungsdruck. Diese Fahigkeit, den eigenen Wissensstand akkurat zu kartieren, ist seltener als sie klingt.

**Architektonische Reife**
Das Feedback auf mAImory:

> *"Hochgradige architektonische Reife. Studenten neigen oft dazu, einfach alles Coole einzubauen. Du machst das Gegenteil: Du lehnst komplexe Patterns ab und begründest das perfekt mit deinen Constraints."*
> — mAImory Notebook, Modell-Bewertung

Er lehnt Microservices nicht ab weil er sie nicht kennt. Er lehnt sie ab weil er weiss, warum sie fur einen Ein-Personen-MVP falsch sind. Das ist ein grosser Unterschied.

**Kritisches Denken unter Druck**
In Turn 40 der SE-Session, acht Stunden vor einer Zweitversuchs-Klausur, hinterfragt er eine KI-Losung fuer ein Aktivitatsdiagramm. Er denkt nicht mit — er denkt gegen. Das ist keine passive Konsumhaltung.

**Multistakeholder-Perspektiven**
Im SWA-Kurs entwickelt er explizit drei Stimmen fur dasselbe Architekturproblem: den Entwickler, den BWL-Typen, den Architekten. Alle drei sind er. Das zeigt eine aussergewohnliche Fahigkeit zur Perspektivverschiebung.

**Mathematische Ingenieursdenke**
Er berechnet spontan die Composite-Availability-Formel fur seinen Fallback-Chain: 1-(1-0.995)^3 = 99,9975%. Das war nicht gefordert. Er tat es weil es ihn interessiert hat — und weil er den Unterschied zwischen einer Zahl und einem Gefuhl versteht.

---

## Schwaechen: Was noch wachsen muss

**Notationsprazision**
Das Konzept sitzt. Die Handhabung nicht. UML-Diagramme zu verstehen und sie unter Klausurbedingungen korrekt zu zeichnen sind zwei verschiedene Fahigkeiten. Die zweite erfordert Ubung mit Papier, nicht mit KI.

**Datenbankdesign**
Explizit selbst benannt in mAImory:

> *"Leider kenne ich mich nicht mit Datenbanken aus und habe das Modul dazu nie geschrieben."*
> — mAImory Notebook

Das Keeper-System zeigt dasselbe Muster: das kritischste Problem (Dual-Schema) entstand durch evolutionares Wachstum ohne fruhes Schema-Design. Die Angst vor Datenbanken ist real und hat architektonische Konsequenzen.

**Prasentationsmanagement**
Nach dem ersten Probe-Durchlauf seiner mAImory-Prasentation:

> *"Ich bin Faktor 3 über der Zeit, daran muss ich arbeiten."*
> — mAImory Notebook

Er weiss es. Aber Wissen und Konnen sind auch hier zwei verschiedene Dinge. Die Fahigkeit, komplexe Systeme auf zehn Minuten zu komprimieren, ist eine Disziplin, die sich separat uben muss.

**Zeitmanagement in der Vorbereitung**
Das SE-Notebook zeigt das Muster deutlich: solide Konzeptvorbereitung fruehzeitig, aber Notationsdetails bis in die Krisenphase aufgeschoben. Das schafft vermeidbaren Last-Minute-Stress.

---

## NotebookLM als Lernwerkzeug

Samuel nutzt NotebookLM nicht wie Google — er nutzt es wie einen Lerntutor, dem er Materialien mitbringt. Er ladt Altklausuren hoch, fragt nach Klausur-taktischen Einschatzungen ("Bei welcher Klausuraufgabe kommt Aggregation dran?"), bittet um Syntheseformulierungen ("Noch mal die komplette richtige Antwort"), und delegiert Priorisierungsentscheidungen ("Welche Altklausur-Aufgaben sollten wir noch besprechen?").

Das SWA-Notebook enthalt sogar komplett ausformulierte System-Prompts fur ADD-Coaching-Sessions mit Claude und Gemini — Samuel benutzt KI, um KI besser einsetzen zu koennen. Das ist Meta-Kompetenz.

83 Fragen uber vier Notebooks in einem Studiensemester. 55 Quellen allein im SWA-Notebook. Das sind keine zufalligen Zahlen — das ist ein Lernender, der aktiv in sein eigenes Verstandnis investiert.

Der Satz, der am Ende ubrig bleibt und am meisten uber Samuel als Studierenden aussagt:

> *"Es geht nicht um die PERFEKTE Architektur. Es geht darum zu ZEIGEN, WIE du zu deiner Architektur gekommen bist!"*
> — SWA Notebook

Er hat das internalisiert. Nicht als Strategie, um Punkte zu holen. Als Denkweise.
