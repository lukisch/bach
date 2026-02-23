AUTOMATISIERUNG MIT LLMs - UEBERSICHT
=====================================

Stand: 2026-01-24

Dieser Ordner enthaelt Wiki-Eintraege zu verschiedenen
Automatisierungsmoeglichkeiten mit Large Language Models.

INHALT
======

KOMMUNIKATION & TERMINE
-----------------------
  terminverwaltung.txt      Kalender & Scheduling automatisieren
  mail_automation.txt       Email-Antworten automatisieren
  kundensupport.txt         Customer Support Chatbots
  telefon_service.txt       Voice Bots fuer Telefonie

AUDIO & VIDEO
-------------
  voice_cloning.txt         Eigene Stimme fuer Anrufe
  avatar_videocalls.txt     Digital Twin fuer Videocalls

WISSENSMANAGEMENT
-----------------
  briefings_dossiers.txt    Briefings und Reports automatisieren
  listenfuehrung.txt        Task-Listen mit LLMs fuehren
  dokumentation.txt         Technical Writing automatisieren

ENTWICKLUNG & TESTING
---------------------
  code_testing.txt          Unit Tests automatisch generieren

SPEZIALANWENDUNGEN
------------------
  psychologische_diagnostik.txt   AI in Mental Health (Forschung)

SCHNELLREFERENZ
===============

| Thema               | Datei                        | Reifegrad     |
|---------------------|------------------------------|---------------|
| Termine             | terminverwaltung.txt         | Production    |
| Kundensupport       | kundensupport.txt            | Production    |
| Email               | mail_automation.txt          | Production    |
| Telefon             | telefon_service.txt          | Production    |
| Voice Cloning       | voice_cloning.txt            | Production    |
| Video Avatar        | avatar_videocalls.txt        | Early Adopt   |
| Briefings           | briefings_dossiers.txt       | Production    |
| Listen              | listenfuehrung.txt           | Production    |
| Code Testing        | code_testing.txt             | Production    |
| Dokumentation       | dokumentation.txt            | Production    |
| Psych. Diagnostik   | psychologische_diagnostik.txt| Research      |

EMPFOHLENE LESEPFADE
====================

FUER EINSTEIGER:
  1. terminverwaltung.txt (einfachster Einstieg)
  2. mail_automation.txt (direkter Nutzen)
  3. listenfuehrung.txt (persoenliche Produktivitaet)

FUER ENTWICKLER:
  1. code_testing.txt
  2. dokumentation.txt
  3. kundensupport.txt (RAG-Implementierung)

FUER UNTERNEHMEN:
  1. kundensupport.txt
  2. telefon_service.txt
  3. briefings_dossiers.txt

FUER SPEZIALANWENDUNGEN:
  1. psychologische_diagnostik.txt (mit Vorsicht!)
  2. avatar_videocalls.txt
  3. voice_cloning.txt

BACH-INTEGRATION
================
  Alle Themen koennen mit BACH integriert werden:
  - Partner-System fuer LLM-Auswahl
  - Tools in tools/ Ordner
  - Workflows in _inbox/ → _outbox/

  Typische Partner-Zuweisung:
  - Claude: Komplexe, nuancierte Aufgaben
  - Gemini: Lange Dokumente (40+ Seiten), Kosteneffizienz
  - Ollama: Datenschutz-kritische Daten (lokal)
  - Antigravity: Agent-driven Development, Tests

  Was BACH intern loesen kann:
  - Mail/Termine: Ollama (Drafts) + n8n + Scripts
  - Dokumentation: Gemini (grosses Context Window)
  - Coding Tests: Antigravity (Agent fuehrt Tests selbst aus)
  - Briefings: Gemini (1-2 Mio Token Context)
  - Psych. Diagnostik: PubMed (Wissen) + Ollama (Privacy)

  Was EXTERNE Tools braucht:
  - Telefonie: Vapi.ai (Orchestrierung) + ElevenLabs (Voice)
  - Video Avatar: HeyGen (Interactive Avatar API)

SICHERHEITSHINWEISE
===================
  Generell fuer alle Automatisierungen:
  - Sensible Daten NICHT an Cloud-LLMs
  - Human-in-the-Loop wo kritisch
  - Ergebnisse validieren
  - Audit Trails fuehren
  - DSGVO/Datenschutz beachten

MODULARES FRAMEWORK (VISION)
============================
  Potentielle Architektur fuer LLM-Betriebssystem:

  Layer 1 - ERKENNUNG & EXTRAKTION
    - Mails, Anrufe, Texte → strukturierte Events
    - (Terminwunsch, Supportanfrage, Task, etc.)

  Layer 2 - REGELN & PROFILE
    - Harte Logik, Rollen, Rechte
    - Zeitregeln, Diagnostik-Standards

  Layer 3 - LLM-FORMULIERUNG
    - Antworten, Dossiers, Berichte
    - Gespraechsfuehrung (Text/Voice/Avatar)

  Layer 4 - PERSISTENZ & UI
    - BACH, Sheets, DMS, Kalender
    - Ticket-System, schlanke Oberflaechen

WEITERENTWICKLUNG
=================
  Geplante Ergaenzungen:
  - Workflow-Automatisierung
  - RPA + LLM Kombinationen
  - Multi-Agent Systems
  - Branchen-spezifische Guides
  - Einheitliches Event-Schema

SIEHE AUCH
==========
  wiki/ki_preise.txt       Kostenueberblick LLMs
  wiki/mcp.txt             Model Context Protocol
  docs/docs/docs/help/partners.txt             BACH Partner-System
  wiki/rag.txt             Retrieval-Augmented Generation
  wiki/n8n.txt             Workflow-Automatisierung (zu erstellen)
