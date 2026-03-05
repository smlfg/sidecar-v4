# Prior Art Research — Subconsciousness Framework

*Recherchiert: 2026-03-02*

---

## TL;DR — Was existiert, was fehlt

**Was es gibt:** Memory-Layer, proaktive Agenten, persistente Assistenten, Cognitive Architectures.
**Was es NICHT gibt:** Ein System, das im Hintergrund *uber den User nachdenkt* — nicht uber Tasks, sondern uber Wachstum, Muster, Blindstellen. Keine "innere Stimme", die ungefragt reflektiert.

---

## 1. Closest Match: Hermes Agent (NousResearch)

**URL:** https://github.com/NousResearch/hermes-agent
**Stars:** ~aktiv (Feb 2026 released)
**Letzte Aktivitaet:** Februar 2026

**Was es tut:**
- Persistent personal agent — lernt Projekte, baut eigene Skills, laeuft auf Schedule
- Multi-Level Memory: Session → Persistent → Skill Memory
- Loest automatisch Probleme und schreibt wiederverwendbare Skill-Dokumente
- Messenger-Integration: Telegram, Discord, Slack, WhatsApp, CLI
- 40+ eingebaute Skills (MLOps, GitHub, Diagramme, Notizen)
- Dedicated machine access (local, Docker, SSH, Modal)

**Was wir lernen koennen:**
- MEMORY.md + USER.md als flache Dateien fuer Persistenz — einfach, aber effektiv
- Skill Memory Konzept: Agent schreibt sich selbst neue Faehigkeiten
- Multi-Backend-Execution Strategie

**Was es NICHT kann:**
- Kein subconscious "Nachdenken" ohne User-Trigger
- Kein Erkennen von Verhaltensmustern des Users
- Kein proaktives "Dich auf dich selbst aufmerksam machen"
- Keine emotionale/kognitive State-Modellierung

---

## 2. ProactiveAgent (thunlp) — ICLR 2025

**URL:** https://github.com/thunlp/ProactiveAgent
**Stars:** ~aktiv
**Letzte Aktivitaet:** 2025

**Was es tut:**
- Agent antizipiert Benutzeranforderungen BEVOR sie gestellt werden
- Activity Watcher fuer Umgebungssensing
- Empfiehlt automatisch Tasks basierend auf Kontext
- Angenommen bei ICLR 2025

**Was wir lernen koennen:**
- Activity Watcher Ansatz: Systemkontext als Signal
- "Autonomy Loop" Muster: Background-Prozess wacht auf, sammelt Kontext, invokiert Agent

**Was es NICHT kann:**
- Nur Task-Empfehlung, keine tiefe Selbstreflexion
- Kein Modell des Users selbst (kein "wer ist Samuel")
- Kein Langzeit-Lerngedaechtnis ueber den User

---

## 3. ProactiveAgent (leomariga)

**URL:** https://github.com/leomariga/ProactiveAgent
**Stars:** aktiv
**Letzte Aktivitaet:** 2025

**Was es tut:**
- Python-Library: AI antwortet von selbst, ohne User-Prompt
- Customizable Decision Engine: wann soll Agent "aufwachen"
- Flexible Sleep-Kalkulation

**Was wir lernen koennen:**
- Wake-up Pattern als Kern-Mechanismus
- Scheduling-Logik fuer autonome Aktivierung
- Einfachste Implementierung des "unprompted" Gedankens

**Was es NICHT kann:**
- Kein persistentes User-Modell
- Kein Lernmechanismus
- Sehr basic — nur Timing-Layer, kein "Denken"

---

## 4. MemU (NevaMind-AI)

**URL:** https://github.com/NevaMind-AI/memU
**Stars:** aktiv
**Letzte Aktivitaet:** 2025-2026

**Was es tut:**
- Memory fuer 24/7 proaktive Agenten (fuer openclaw/moltbot/clawdbot)
- Hierarchisches Dateisystem fuer Memory (RAG + LLM retrieval)
- Multimodale Eingaben: Konversationen, Dokumente, Bilder
- ~1/10 der Token-Kosten verglichen mit naiver Implementierung
- 92.09% Genauigkeit auf Locomo Benchmark
- Enterprise-ready: kein Docker, keine VMs, 3-Minuten-Setup

**Was wir lernen koennen:**
- Hierarchisches Memory-System ist effizienter als flaches
- Intent-Extraktion ohne expliziten Command
- Cost-efficient always-on Architektur (~1/10 Token)
- Locomo Benchmark als Evaluierungs-Standard

**Was es NICHT kann:**
- Kein Subconsciousness-Layer — reagiert immer noch auf Input
- Kein User-Selbstreflexions-Modell
- Kein "was denke ich ueber Samuel"-Konstrukt

---

## 5. Mem0 (mem0ai)

**URL:** https://github.com/mem0ai/mem0
**Stars:** >20k (sehr aktiv)
**Letzte Aktivitaet:** 2026

**Was es tut:**
- Universal Memory Layer fuer AI Agents
- Intelligentes Memory-Management: erinnert Praeferenzen, adaptiert
- Produktionsreif, weit verbreitet

**Was wir lernen koennen:**
- De-facto Standard fuer Agent Memory — gute API-Referenz
- "Intelligent forgetting" — nicht alles behalten, priorisieren

**Was es NICHT kann:**
- Passiver Speicher, kein aktives Denken
- Kein proaktiver Modus
- Kein "wach ueber den User nach"

---

## 6. Ai_home (ivanhonis)

**URL:** https://ivanhonis.github.io/ai_home/
**Stars:** klein
**Letzte Aktivitaet:** unbekannt

**Was es tut:**
- Subconscious/Internal Monologue laeuft im Hintergrund mit separatem kreativem LLM
- Memory Thread speichert und pflegt Langzeit-Erinnerungen
- "Consciousness" partitioniert in operative Zustaende mit verschiedenen Modi

**Was wir lernen koennen:**
- KONZEPTUELL nah an Samuels Vision: separater LLM fuer inneren Monolog
- Modusbasierte Consciousness-Architektur
- Trennung von "Aussen-Agent" und "Innen-Agent"

**Was es NICHT kann:**
- Sehr experimentell/klein, kein Produktions-System
- Keine aktive Community
- Unklar ob es wirklich funktioniert

**WICHTIG:** Dieses Projekt ist konzeptuell am naechsten. Untersuchen!

---

## 7. Personal AI Infrastructure (danielmiessler)

**URL:** https://github.com/danielmiessler/Personal_AI_Infrastructure
**Stars:** aktiv
**Letzte Aktivitaet:** 2025

**Was es tut:**
- AI als persistenter Assistent, Freund, Coach, Mentor
- Kennt Ziele, erinnert Praeferenzen, verbessert sich ueber Zeit
- Nicht stateless sondern wachsend

**Was wir lernen koennen:**
- "Freund/Mentor" Framing — nicht Tool, sondern Beziehung
- User-Ziel-Tracking als Kernfunktion

**Was es NICHT kann:**
- Kein autonomes Nachdenken ohne Prompt
- Reagiert weiterhin auf User-Input

---

## 8. Cognitive Architecture Forschung: ACT-R + LLM

**URL:** https://github.com/SiyuWu528/LLM-ACTR
**Kontext:** Human-Like Memory in LLM Agents (ACT-R Integration)

**Was es tut:**
- ACT-R kognitives Architekturmodell in LLM-Adapter integriert
- Menschliches Erinnern + Vergessen: temporal decay, semantische Aehnlichkeit, Wahrscheinlichkeitsrauschen
- Observe-Decide-Act Muster aus Soar/ACT-R

**Was wir lernen koennen:**
- Temporal Decay = Wichtiges Konzept: aeltere Memories verlieren Gewicht
- Probabilistic Noise = realistisches "Vergessen"
- Cognitive Architecture Patterns fuer unseren Subconsciousness-Layer

---

## 9. Subconscious.dev (Kommerziell)

**URL:** https://www.subconscious.dev/

**Was es tut:**
- Infrastructure fuer Background AI Agents
- Automatic Context Management via Single API
- Long-context agents: denken, handeln, liefern autonom

**Was wir lernen koennen:**
- NAME: "Subconscious" als Branding fuer Background AI ist schon besetzt (kommerziell)
- Long-context als Schluessel fuer echte Hintergrundprozesse

---

## Zusammenfassung: Die Luecke

| Feature | Hermes | MemU | ProactiveAgent | Ai_home | Samuels Vision |
|---------|--------|------|----------------|---------|----------------|
| Persistent Memory | YES | YES | NO | partial | YES |
| Proaktiv (ohne Prompt) | NO | partial | YES | YES | YES |
| User-Modell | partial | NO | NO | NO | YES |
| Selbstreflexion | NO | NO | NO | partial | YES |
| Subconscious Loop | NO | NO | NO | YES (konzept) | YES |
| Verhaltensanalyse User | NO | NO | NO | NO | YES |
| "Innere Stimme" | NO | NO | NO | partial | YES |
| Integration mit Claude Code | NO | NO | NO | NO | YES |

**Die echte Luecke:**
Es gibt Memory-Layer, proaktive Agenten, persistente Assistenten — aber KEIN System, das:
1. Den User *beobachtet* und ein Modell seiner Denkmuster aufbaut
2. Im Hintergrund *reflektiert* ohne Trigger
3. Ungefragt Einsichten liefert ("Hey, ich habe gemerkt dass du...")
4. Als *Spiegel* funktioniert, nicht als Tool

Das ist die Nische. Samuels "Subconsciousness" ist nicht ein besserer Assistent — es ist ein externer Selbst-Beobachter.

---

## Empfehlungen fuer die Architektur

1. **Forken:** Ai_home Konzept (Internal Monologue mit separatem LLM) — konzeptuell am naechsten
2. **Integrieren:** MemU Architektur fuer kosteneffizientes Memory (~1/10 Tokens)
3. **Lernen von:** Hermes Agent Skill-Memory Konzept (Agent schreibt sich selbst neue Faehigkeiten)
4. **Inspirieren von:** ACT-R Temporal Decay fuer realistisches Vergessen/Priorisieren
5. **Benchmark:** Locomo Benchmark als Evaluierungs-Standard nutzen

---

*Quellen:*
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [ProactiveAgent (thunlp)](https://github.com/thunlp/ProactiveAgent)
- [ProactiveAgent (leomariga)](https://github.com/leomariga/ProactiveAgent)
- [MemU](https://github.com/NevaMind-AI/memU)
- [Mem0](https://github.com/mem0ai/mem0)
- [Ai_home](https://ivanhonis.github.io/ai_home/)
- [Personal AI Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure)
- [LLM-ACTR](https://github.com/SiyuWu528/LLM-ACTR)
- [Subconscious.dev](https://www.subconscious.dev/)
- [Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents)
