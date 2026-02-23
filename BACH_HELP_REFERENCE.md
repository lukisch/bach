# BACH Befehlsreferenz

*Generiert: 2026-02-22*

---


*113 Help-Dateien*


## Abo

ABO - Abonnement- und Vertragsverwaltung
=========================================

BESCHREIBUNG:
  Verwaltet laufende Abonnements und Vertraege (Streaming, Software,
  Internet, Mobilfunk etc.). Erkennt Abos automatisch aus Steuer-Posten
  und berechnet monatliche/jaehrliche Kosten.

CLI-BEFEHLE:
  bach abo help              Hilfe anzeigen
  bach abo init              Datenbank-Tabellen erstellen (einmalig)
  bach abo scan              Steuer-Posten nach Abos durchsuchen
  bach abo list              Alle erkannten Abos anzeigen
  bach abo list --alle       Inkl. deaktivierte
  bach abo list --bestaetigt Nur bestaetigte
  bach abo confirm <id>      Abo-Erkennung bestaetigen
  bach abo dismiss <id>      Fehlererkennung entfernen
  bach abo costs             Kostenaufstellung nach Kategorie
  bach abo export            CSV-Export (data/abo_export.csv)
  bach abo patterns          Bekannte Abo-Muster anzeigen
  bach abo sync-mail         Abos aus E-Mails synchronisieren

OPTIONEN:
  --jahr YYYY    Steuerjahr fuer Scan (Default: aktuelles Jahr)
  --dry-run      Scan nur simulieren

DATENBANK:
  Tabellen in bach.db:

  abo_subscriptions - Erkannte/verwaltete Abos
    id, name, anbieter, kategorie, betrag_monatlich,
    zahlungsintervall, kuendigungslink, erkannt_am,
    bestaetigt (0/1), aktiv (0/1)

  abo_payments - Zahlungsverknuepfungen zu Steuer-Posten
    id, subscription_id, posten_id, betrag, datum

  abo_patterns - Bekannte Anbieter-Erkennungsmuster
    id, pattern, anbieter, kategorie, kuendigungslink

  fin_contracts - Manuelle Vertragsverwaltung (parallel)
    id, name, kategorie, anbieter, kundennummer, vertragsnummer,
    betrag, intervall, kuendigungsfrist_tage, ablauf_datum, ...

WORKFLOW:
  1. bach abo init           (einmalig: Tabellen + Default-Patterns)
  2. bach abo scan           (durchsucht steuer_posten)
  3. bach abo list           (zeigt Ergebnisse)
  4. bach abo confirm <id>   (bestaetige echte Abos)
  5. bach abo dismiss <id>   (entferne Fehlerkennungen)
  6. bach abo costs          (Kostenueberblick)
  7. bach abo sync-mail      (E-Mail-Abos importieren, optional)

BEKANNTE PATTERNS (Auswahl):
  Netflix, Spotify, Microsoft 365, Adobe, Amazon Prime, Disney+,
  Apple/iCloud, YouTube Premium, Dropbox, Google One, ChatGPT/OpenAI,
  Anthropic/Claude, GitHub, JetBrains, 1Password, NordVPN, ExpressVPN

ZUSAMMENSPIEL:
  - bach steuer: Steuer-Posten als Datenquelle fuer Abo-Scan
  - GUI: Abos CRUD (#573, von Gemini implementiert)
  - fin_contracts: Manuelle Vertraege (ergaenzt automatische Erkennung)
  - financial_emails: E-Mails mit Abo-Bezug (category = 'abo')

BEISPIELE:
  # Erstmalige Einrichtung:
  bach abo init

  # Abos aus Steuer-Daten erkennen:
  bach abo scan --jahr 2025

  # Alle Abos auflisten (inkl. deaktivierte):
  bach abo list --alle

  # Nur bestaetigte Abos:
  bach abo list --bestaetigt

  # Kostenueberblick nach Kategorie:
  bach abo costs

  # Abo bestaetigen:
  bach abo confirm 8

  # Fehlererkennung entfernen:
  bach abo dismiss 3

  # E-Mail-Abos importieren:
  bach abo sync-mail

  # Export fuer Haushaltsplanung:
  bach abo export

  # Bekannte Patterns anzeigen:
  bach abo patterns


## Actors

ACTORS MODEL - 6-Kategorien Akteure-System
==========================================

BESCHREIBUNG
Das Actors-Model beschreibt die 6 Akteur-Kategorien die in BACH
zusammenarbeiten. Es ersetzt das alte 4-Akteure-Modell.

Version: 2.0.0

DIE 6 AKTEURE
=============

1. USER (Einer oder Mehrere)
----------------------------
Rolle: Entscheider, Auftraggeber, Feedback-Geber

Schnittstellen:
  - MessageBox/       Primaere Kommunikation
  - User/             Persoenlicher Bereich
  - Workspace/        Aktiver Arbeitsbereich

Modi:
  - Single-User       Standard (aktuell)
  - Multi-User        Zukunft (Admin, Standard, Gast)

Interaktion:
  - Direkt via Chat (Claude.ai / API)
  - Asynchron via MessageBox (.txt/.md Dateien)
  - Manuell via Dateisystem


2. OPERATING AI - "Geist in der Flasche"
----------------------------------------
Rolle: Zentrale Intelligenz, Reasoning, Orchestrierung

Aktuell:      Claude (Anthropic)
Austauschbar: Ja - System ist AI-agnostisch designed

Aufgaben:
  - Reasoning und Entscheidungsfindung
  - Task-Orchestrierung und Delegation
  - Code-Generierung und Review
  - Dokumentation und Analyse
  - User-Kommunikation

Eigenschaften:
  - Token-Limit: ~190.000 pro Session
  - Kein persistentes Gedaechtnis
  - Zugriff auf Tools via MCP/Desktop Commander


3. WEITERE AIs/LLMs
-------------------
Rolle: Spezialisierte Aufgaben, Delegation, Token-Ersparnis

Verfuegbar:
  - Ollama (lokal)    llama3.2, mistral, codellama
  - Gemini (extern)   Deep Research, lange Dokumente
  - Copilot           Office-Integration
  - GPT               Alternative (inaktiv)

Delegations-Trigger:
  - Token-Knappheit (>70%)
  - Bulk-Verarbeitung
  - Spezialisierte Tasks
  - Parallel-Verarbeitung


4. OPERATING SYSTEM
-------------------
Rolle: Grundlegende Infrastruktur und lokale Ausfuehrung

Umfasst:
  - Windows/Linux OS
  - Installierte Software
  - Ollama Runtime
  - Python/Node.js
  - Dateisystem

Zugriff via:
  - Desktop Commander (MCP)
  - FileCommander (MCP)
  - Direkte Shell-Befehle


5. INTEGRIERTE TOOLS & SCRIPTE
------------------------------
Rolle: Eigenentwicklungen, Automatisierung, Spezialaufgaben

Kategorien:
  - Coding-Tools      c_encoding_fixer, c_json_repair, etc.
  - Steuer-Tools      steuer_scanner, steuer_sync, etc.
  - Agent-Scripts     agent_framework, entwickler_agent
  - Backup-Tools      backup_manager
  - Migration         migrate_connections

Verwaltung:
  bach tools list     Python-Scripts auflisten (Dateisystem)
  bach tools db       DB-registrierte Tools (CLI + externe KI)


6. ONLINE-TOOLS (ohne AI)
-------------------------
Rolle: Spezialisierte Web-Dienste

Kategorien:
  - Generatoren       PDF, QR-Codes, etc.
  - Datenbanken       APIs, Registries
  - Konverter         Format-Umwandlung
  - Recherche         Nicht-AI Suchmaschinen

Hinweis: Unterschied zu AI-Tools wie ChatGPT/Midjourney!


INTERAKTIONS-PRINZIPIEN
=======================

Hierarchie der Entscheidungen:
  1. User entscheidet bei kritischen Fragen
  2. Claude koordiniert und orchestriert
  3. Tools fuehren aus
  4. Andere AIs unterstuetzen bei Bedarf

Token-Bewusstsein:
  - Claude ist Token-limitiert
  - Delegation spart Tokens
  - Bulk-Ops an Ollama
  - Research an Gemini

Kommunikations-Kanaele:
  - Direkt:    Claude <-> User (Chat)
  - Async:     MessageBox (Dateien)
  - API:       MCP-Server, REST
  - Delegation: Inbox/Outbox System


VERBINDUNGS-MATRIX
==================

Operating AI (Claude):
  -> User (direkt, MessageBox)
  -> Ollama (API, Queue)
  -> Gemini (Drive Delegation)
  -> OS (Desktop Commander)
  -> Tools (direkte Ausfuehrung)
  -> MCP-Server (PubMed, Canva, Drive)

User:
  -> Claude (Chat, MessageBox)
  -> OS (direkte Nutzung)
  -> Tools (manuelle Ausfuehrung)

Ollama:
  <- Claude (Delegation)
  -> OS (lokale Ausfuehrung)

Gemini:
  <- Claude (Drive Delegation)
  -> Cloud (externe Verarbeitung)


CLI-ZUGRIFF
===========
bach --connections list          Connections anzeigen
bach --connections db            Alias fuer list
bach --connections db --type ai  AI-Partner
bach --connections actors        Actors-Model anzeigen
bach --connections partners      Partner-Profile anzeigen
bach --help actors               Diese Hilfe


AGENTEN-SYSTEM
==============

Neben den 6 Akteuren gibt es ein hierarchisches Agenten-System:

Boss-Agenten (koordinieren):
  - Persoenlicher Assistent (privat)
  - Gesundheitsassistent (privat)
  - Bueroassistent (beruflich)

Experten (spezialisiert):
  - Haushaltsmanagement
  - Gesundheitsverwalter, Psycho-Berater
  - Steuer-Agent, Foerderplaner

Mehr Infos: bach --help agents


SIEHE AUCH
----------
bach --connections list    Connections-Verwaltung
bach --connections actors  Actors-Model
bach --connections partners Partner-Profile
bach tools list            Tool-Verwaltung (Dateisystem)
bach tools db              Tool-Verwaltung (Datenbank)
bach --help agents         Agenten-System


## Agents

BACH AGENTEN-SYSTEM
==================

Hierarchisches System aus Boss-Agenten und Experten.

STRUKTUR
--------

Boss-Agenten koordinieren, Experten sind spezialisiert:

  [Boss-Agent]
       |
       +-- [Experte 1]
       +-- [Experte 2]


VERFUEGBARE AGENTEN (agents/)
-------------------------------------

[BERUFLICH]

  ATI (ati/)
    Software-Entwickler-Agent mit Scanner, Sessions
    Features: Task-Scanner, Headless Sessions, Tool Discovery

  Entwickler (entwickler)
    Allgemeiner Entwickler-Agent

  Production (production)
    Produktions-Workflow-Agent

  Research (research)
    Wissenschaftliche Recherche (PubMed, Perplexity, Consensus)

  Bueroassistent (bueroassistent)
    Steuern, Foerderplanung, Dokumentation
    Experten: Steuer, Foerderplaner

  Reflection (reflection)
    Selbstreflexion und Meta-Analyse


[PRIVAT]

  Persoenlicher Assistent (persoenlicher-assistent)
    Terminverwaltung, Recherche, Kommunikation, Transkription, Notizen
    Experten: Haushaltsmanagement, Transkriptions-Service, Decision-Briefing
    Services:  Notizblock

  Gesundheitsassistent (gesundheitsassistent)
    Medizinische Dokumentation und Verwaltung
    Experten: Gesundheitsverwalter, Psycho-Berater

  Versicherungen (versicherungen)
    Versicherungs-Verwaltung


[TEST]

  Test-Agent (test-agent)
    Fuer Tests und Experimente


CLI-BEFEHLE
-----------

  # Agenten auflisten
  bach --agents list
  python tools/agent_cli.py list

  # Experten anzeigen
  python tools/agent_cli.py experts

  # Agent-Details
  python tools/agent_cli.py info <agent-name>

  # User-Ordner initialisieren
  python tools/agent_cli.py init all
  python tools/agent_cli.py init <agent-name>

  # Datenbank einrichten
  python tools/agent_cli.py setup-db

  # System-Status
  python tools/agent_cli.py status


VERZEICHNISSE
-------------

  agents/     Boss-Agenten Definitionen (11 Agenten)
  agents/_experts/    Experten-Ordner mit CONCEPT.md (17 Experten)
  user/<agent>/       User-Datenordner pro Agent

WICHTIG: Agenten und Experten sind unterschiedliche Konzepte!
  - Agenten (Boss): Koordinieren und delegieren (_agents/)
  - Experten: Spezialisierte Ausfuehrung (_experts/)
  - Einige in Help gelistete "Agenten" sind eigentlich Experten:
    * steuer-agent → _experts/steuer/
    * foerderplaner → _experts/foerderplaner/
    * haushaltsmanagement → _experts/haushaltsmanagement/
    * psycho-berater → _experts/psycho-berater/
    * transkriptions-service → _experts/transkriptions-service/
    * decision-briefing → _experts/decision-briefing/
    * notizblock → skills/_services/notizblock.md (Service, kein Experte)


DATENBANKEN
-----------

  bach.db:
    - agents (Agenten-Registry)
    - agent_synergies (Synergien zwischen Agenten)

  bach.db:
    - Tabellen je Experte (health_*, household_*, etc.)


WORKFLOW
--------

1. Agent aktivieren (ueber Skill oder CLI)
2. Agent laedt Skill-Definition und User-Daten
3. Bei Spezialthema: Delegation an Experten
4. Experte fuehrt aus, Boss-Agent fasst zusammen


GUI
---

  http://127.0.0.1:8000/agents     Agenten-Uebersicht
  http://127.0.0.1:8000/ati        ATI-Agent Details
  http://127.0.0.1:8000/steuer     Steuer-Agent Details


DATEIEN
-------

  agents/ati/              ATI-Agent Ordner
  agents/ati/ATI.md        ATI Definition
  agents/persoenlicher-assistent.txt
  agents/gesundheitsassistent.txt
  agents/bueroassistent.txt
  agents/steuer-agent.txt
  agents/research.txt
  agents/entwickler.txt
  agents/production.txt
  agents/README.md


SIEHE AUCH
----------

  bach --help actors      Ueberblick ueber Akteure
  bach --help bach_paths        Verzeichnisstruktur
  bach --help practices   Architektur-Prinzipien
  bach --help ati         ATI Software-Entwickler Details


## Anbieter

ANBIETER - Anbieterspezifische Regeln
=====================================

BESCHREIBUNG
Regeln fuer die Verarbeitung von Rechnungen und Belegen
verschiedener Online-Anbieter.

WICHTIG: Dies ist eine reine Dokumentationsdatei ohne zugehoerigen
Handler. Die Regeln sind in Steuer-Expert-Scripts implementiert:
- system/agents/_experts/steuer/temu_ocr_batch.py
- system/agents/_experts/steuer/steuer_batch.py
- system/agents/_experts/steuer/beleg_vorfilter.py
- system/agents/_experts/steuer/beleg_parser.py

Belege werden in Unterordnern gespeichert:
user/documents/persoenlicher_assistent/steuer/YYYY/Werbungskosten/belege/[Anbieter]/

TEMU
====

Kontext:
TEMU-Rechnungen werden aus E-Mail-Bestellbestaetigungen importiert,
nicht aus Originalquittungen. Dies ist ein Workaround, da
automatisches Abrufen der Originalquittungen sehr aufwaendig ist.

Erfassungsregeln:

1. PREISE
   Immer aus den Mail-PDFs extrahieren
   (Preise sind volatil auf der Website)

2. PRODUKTNAMEN
   Falls Text fehlt oder unvollstaendig:
   - Logisch herleiten aus Kontext
   - Besser: Produkt auf temu.com suchen fuer korrekte Bezeichnung

3. DOKUMENTTYP
   Als "Bestellbestaetigung (ersatzweise Rechnung)" markieren

4. NACHTRAEGLICHE VALIDIERUNG
   Falls spaeter Originalquittungen hochgeladen werden,
   Daten abgleichen und aktualisieren

Hinweis fuer Finanzamt:
Originalquittungen werden nur auf Nachfrage bereitgestellt.
Bestellbestaetigungen dienen als Erstnachweis.


AMAZON
======
(Platzhalter fuer zukuenftige Regeln)

Bei Bedarf ergaenzen:
- Rechnungsformat
- Besonderheiten bei Marketplace-Verkaeufen
- Prime-Mitgliedschaftsbelege


EBAY
====
(Platzhalter fuer zukuenftige Regeln)

Bei Bedarf ergaenzen:
- PayPal-Verkuepfung
- Privatverkaeufe vs. gewerbliche


WEITERE ANBIETER
================
Bei Bedarf hier ergaenzen:
- Aliexpress
- Wish
- Shein
- Andere Online-Haendler mit speziellen Rechnungsformaten


IMPLEMENTIERTE ANBIETER IN BELEG_VORFILTER.PY
==============================================
- Temu (temu.com, Whaleco)
- Amazon (amazon.de, amazon.com)
- eBay (ebay.de, ebay.com)
- PayPal (paypal.com)
- Google Play
- Apple
- Medimops


SIEHE AUCH
----------
bach steuer help       Steuer-Handler Hilfe
bach steuer tools      Verfuegbare Steuer-Tools anzeigen

TOOLS
-----
temu_ocr_batch.py      Batch-OCR fuer Temu-Belege (Bild-basierte PDFs)
steuer_batch.py        Anbieter-Parser fuer Amazon, Temu, eBay
beleg_vorfilter.py     Automatisches Sortieren von Belegen
beleg_parser.py        LLM-basierte Beleg-Extraktion


## Antigravity

ANTIGRAVITY - SCHNELLREFERENZ
=============================

Google Antigravity ist eine Agent-first Development Platform.
Ausfuehrliche Dokumentation: wiki/antigravity.txt

KURZUEBERSICHT
--------------
  Was:        VS Code Fork mit autonomen KI-Agenten
  Download:   https:/antigravity.google/download
  Pfad:       C:\Users\User\AppData\Local\Programs\Antigravity\

CLI-BEFEHLE
-----------
  antigravity [pfad]              Editor oeffnen
  antigravity chat "Prompt"       Chat starten (GUI!)
  antigravity chat -m agent       Agent-Modus
  antigravity --add-mcp {...}     MCP-Server hinzufuegen

TASTENKUERZEL
-------------
  Cmd+L   Agent-Panel toggle
  Cmd+I   Inline-Completion
  Cmd+E   Editor/Manager wechseln

ENTWICKLUNGSMODI
----------------
  Agent-driven    Autopilot (autonom)
  Review-driven   Mit Genehmigung (empfohlen)
  Agent-assisted  User in Kontrolle

WICHTIGE PFADE
--------------
  .gemini\antigravity\brain\     Task-Listen (LESBAR!)
  .gemini\antigravity\skills\    Globale Skills
  .agent\skills\                 Workspace-Skills
  .agent\workflows\              Workflows (/slash-commands)

BACH-INTEGRATION
----------------
  Start:    start/start_gemini.bat (Interaktiv)
  Script:   python tools/partner_communication/gemini_start.py
  Inbox:    system/partners/gemini/inbox/
  Outbox:   system/partners/gemini/outbox/

SIEHE AUCH
----------
  wiki/antigravity.txt   Vollstaendige Dokumentation
  wiki/gemini.txt        Gemini KI-Modelle
  docs/docs/docs/help/partners.txt           KI-Partner System


## Api

API-BUCH
========

Zentrale API-Dokumentation in BACH.
Registriert APIs mit Base-URL, Auth-Typ, Endpoints und Beispielen.

BEFEHLE
-------

  # API registrieren
  bach api add <name> <base_url> [--auth key|oauth|none] [--desc "..."]
  bach api add openai https://api.openai.com --auth key --desc "OpenAI API"
  bach api add github https://api.github.com --auth oauth --provider GitHub

  # Endpoints verwalten
  bach api endpoint add <api_name> <METHOD> <path> [--desc "..."]
  bach api endpoint add openai POST /v1/chat/completions --desc "Chat Completion"

  # Anzeigen
  bach api list                    Alle registrierten APIs
  bach api show <name>             API-Details mit Endpoints
  bach api search <keyword>        APIs durchsuchen

  # Testen
  bach api verify                  Alle aktiven APIs pruefen (HTTP HEAD)
  bach api verify <name>           Einzelne API pruefen

  # Entfernen
  bach api remove <name>           API aus der DB loeschen

AUTH-TYPEN
----------
  none    - Kein Auth erforderlich
  key     - API-Key (Bearer Token / X-API-Key)
  oauth   - OAuth2 Flow

DATENBANK
---------
  Tabelle: api_book
  Felder: name, base_url, auth_type, provider, description, endpoints_json, tags


## Architecture

BACH ARCHITEKTUR (Personal Agentic OS)
======================================

DEFINITION
BACH ist ein hierarchisches System zur Orchestrierung von KI-Modellen.
Es sitzt als "Nervensystem" zwischen Infrastruktur (Compute) und Anwendung.

SCHICHTEN-MODELL
----------------

0. CORE LAYER (core/, bach_api.py)
   Registry-Based Auto-Discovery: Automatisches Laden aller Handler aus hub/
   App Container: Lightweight DI mit lazy-initialized DB + Registry
   Library-API: Programmatischer Zugriff ohne CLI (bach_api.py)
   Base Types: Result, ParsedArgs, OpDef - einheitliche Contracts

1. ORCHESTRATION LAYER (bach.py, Partner-System, Headless API)
   Koordiniert Multi-LLM Zusammenarbeit (Claude, Gemini, Ollama).
   Verwaltet Tasks, Rollen und Delegation via Message-System.
   REST-API: Port 8001 für programmatischen Zugriff (headless.py)

2. COGNITIVE MEMORY LAYER (memory_*, Consolidation-Engine)
   5 Memory-Typen (Working, Episodisch, Semantisch, Prozedural, Assoziativ).
   Aktive Konsolidierung (Decay, Boost, nächtliche Komprimierung).

3. LOGIC & SKILL LAYER (hub/, skills/, Hierarchy-JSON)
   60+ Auto-Discovered Handler (hub/) und dynamische Skills-Hierarchie.
   Das Skills Board (GUI) steuert die Zuweisung von Experten zu Agenten.
   Queue-Processor: hub/_services/connector/ für asynchrone Verarbeitung

4. EXECUTION LAYER (tools/)
   290+ spezialisierte Python-Scripts für Dateisystem, Steuer, Analyse etc.
   Standardisiertes Interface (c_ prefix) für AI-Kompatibilität.

5. DATA & PERSISTENCE (bach.db, data/logs/)
   SQLite-Grundlage mit 116+ Tabellen (Zentralisierte Datenhaltung).
   Tracking von Tokens, Sessions, Erfolg und Directory Truth.
   Logs konsolidiert in data/logs/ (system/logs/ DEPRECATED)

PROJEKTSTRUKTUR
---------------

system/
├── bach.py .................... CLI-Zentrale (Orchestrator)
├── bach_api.py ................ Library-API (Programmatischer Zugriff)
├── bach_legacy.py ............. Backup (vor Registry-Refactor)
├── core/ ...................... Foundation Layer
│   ├── base.py ................ Result, ParsedArgs, OpDef
│   ├── registry.py ............ Auto-Discovery + Command Routing
│   ├── app.py ................. App Container (DI)
│   ├── db.py .................. Database Wrapper
│   ├── adapter.py ............. Legacy Bridge
│   └── aliases.py ............. Command Aliases (mem -> memory)
├── data/
│   ├── bach.db ................ SQLite (116+ Tabellen) - "Das Gedächtnis"
│   └── logs/ .................. Konsolidierte Logs (NUR HIER)
├── db/
│   └── schema.sql ............. Single Source of Truth (DDL)
├── hub/ ....................... Handler-Module (Auto-Discovered)
│   ├── bach_paths.py .......... Pfad-Management (Governance)
│   └── _services/ ............. Hintergrund-Services
│       ├── connector/ ......... Queue-Processor (async)
│       └── document/ .......... Report-Workflows
├── tools/ ..................... Python-Scripts (290+ Werkzeuge)
├── docs/docs/docs/help/ ...................... Hilfe-System (.txt)
├── agents/ ............ Agenten-Profile (Rollen)
├── partners/ .......... LLM-Konfigurationen (KONSOLIDIERT)
├── docs/ ...................... Dokumentation & Konzepte
├── gui/ ....................... Web-Dashboard (FastAPI)
│   └── api/ ................... REST-APIs
│       ├── headless.py ........ Port 8001 (Pure JSON API)
│       └── messages_api.py .... Message-Router
└── user/ ...................... User-Daten & Exporte

ARCHITEKTUR-DIAGRAMM (Registry v2.0)
------------------------------------

┌─────────────────────────────────────────────────────────────────┐
│ ZUGRIFFS-LAYER                                                  │
├───────────────────┬─────────────────────┬───────────────────────┤
│ CLI (bach.py)     │ Library (bach_api)  │ REST (headless.py)    │
│ sys.argv routing  │ Direct function     │ Port 8001 JSON API    │
└───────────────────┴─────────────────────┴───────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ CORE LAYER (core/)                                              │
├───────────────────┬─────────────────────┬───────────────────────┤
│ App Container     │ HandlerRegistry     │ Database (db.py)      │
│ DI + Lazy Init    │ Auto-Discovery      │ Schema + Migrations   │
└───────────────────┴─────────────────────┴───────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ HANDLER LAYER (hub/)                                            │
│ 60+ BaseHandler Subklassen - Automatisch Registriert           │
├───────────────────┬─────────────────────┬───────────────────────┤
│ task.py           │ memory.py           │ partner.py            │
│ steuer.py         │ backup.py           │ lesson.py             │
│ ...               │ ...                 │ ...                   │
└───────────────────┴─────────────────────┴───────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ SERVICE LAYER (hub/_services/)                                  │
├───────────────────┬─────────────────────┬───────────────────────┤
│ connector/        │ document/           │ daemon/               │
│ Queue-Processor   │ Report-Workflows    │ Background Tasks      │
└───────────────────┴─────────────────────┴───────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ EXECUTION LAYER (tools/)                                        │
│ 290+ Python-Scripts mit standardisiertem c_ Interface          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PERSISTENCE LAYER                                               │
├───────────────────┬─────────────────────┬───────────────────────┤
│ bach.db           │ data/logs/          │ user/                 │
│ 116+ Tabellen     │ Konsolidierte Logs  │ Exports & Berichte    │
└───────────────────┴─────────────────────┴───────────────────────┘

CORE KONZEPTE
-------------

* REGISTRY-BASED: Auto-Discovery statt hardcodierter Handler-Map.
  Neue Handler brauchen NUR eine Datei in hub/ (keine Registrierung).

* DUAL-ACCESS: CLI (python bach.py task list) UND Library-API (bach_api.task.list()).
  Beide nutzen dieselben Handler + DB - Zero Overhead.

* MULTI-PARTNER: Nicht ein Agent, sondern ein Netzwerk mit specialized roles.

* KOGNITIVES GEDÄCHTNIS: Informationen werden nicht nur gespeichert, sondern
  aktiv gewichtet und "verdaut" (Konsolidierung).

* PORTABLE & LOKAL: Das gesamte System ist in einem Ordner gekapselt und
  funktioniert ohne Cloud-Zwang (z.B. mit Ollama).

* SELF-HEALING: Automatische Korrektur von Pfaden und Registry-Einträgen.

* HEADLESS API: REST-Interface auf Port 8001 für externe Integration
  (getrennt vom GUI-Server Port 8000).

SIEHE AUCH
----------
docs/docs/docs/help/bach_info.txt       Was ist BACH?
docs/docs/docs/help/memory.txt          Das Gedaechtnis-System
docs/docs/docs/help/partner.txt         Zusammenarbeit der KIs
wiki/was_ist_bach.txt  Ausfuehrliche Synopse


## Arrow

Diese Datei beschreibt **BachForelle**, ein SEPARATES Projekt ausserhalb von BACH v2 Vanilla.

**Korrekte Pfade:**
- BachForelle: `C:\Users\User\OneDrive\KI&AI\BachForelle\`
- BachFliege: `C:\Users\User\OneDrive\KI&AI\BachFliege\`

## Was ist BachForelle?
BachForelle ist eine leichtgewichtige, LLM-First Variante von BACH.
Es handelt sich um ein EIGENSTAENDIGES Projekt mit separatem Codebase.

**Philosophie:**
*   LLM ist Orchestrator (nicht nur Nutzer)
*   Kein Boot-Prozess nötig
*   Modulare Skills statt Hub-Routing
*   Fokus: Memory + Multi-LLM

## Für BACH v2 Vanilla User
**BachForelle ist NICHT Teil von BACH v2 Vanilla.**

Wenn du BachForelle nutzen möchtest:
1. Wechsle in den BachForelle-Ordner
2. Lies `C:\Users\User\OneDrive\KI&AI\BachForelle\README.md`
3. Lies `C:\Users\User\OneDrive\KI&AI\BachForelle\SKILL.md`

## BACH v2 Vanilla hat KEINEN "arrow" Befehl
Diese Help-Datei existiert nur als Cross-Reference für Nutzer, die beide Systeme verwenden.

Für BACH v2 Vanilla Features siehe:
```bash
python bach.py help
python bach.py help <command>
```


## Ati

ATI - Advanced Tool Integration Agent

ATI (Agent fuer Technische Implementierung) ist der Tool-Integrations-Agent
von BACH. ATI = BATCHI - BACH (das Delta, was BACH noch fehlt).
Er bietet Daemon-Steuerung, Session-Management, Task-Verwaltung, Scanner,
Projekt-Bootstrapping, Code-Analyse und Build-Automatisierung.

BEFEHLE - DAEMON & SESSIONS
===========================

bach ati status                   ATI-Status und Daemon-Info anzeigen
bach ati start                    Headless Session-Daemon starten
bach ati stop                     Session-Daemon stoppen
bach ati session                  Manuelle Session starten
bach ati session --dry-run        Session-Trockenlauf (keine Aenderungen)

BEFEHLE - TASK MANAGEMENT
=========================

bach ati task list                ATI-Tasks anzeigen
bach ati task add "TITEL"         Neuen ATI-Task hinzufuegen
bach ati task done ID             Task als erledigt markieren
bach ati task depends ID DEP      Abhaengigkeit zwischen Tasks setzen
bach ati task blocked             Blockierte Tasks anzeigen
bach ati check                    Between-Task-Checkliste anzeigen
bach ati problems                 Problems First - Fehler priorisiert anzeigen
bach ati context KEYWORD          Kontext-Trigger testen

BEFEHLE - SCANNER
=================

bach ati scan                     Software-Projekte scannen
bach ati scan status              Letzten Scan-Status anzeigen
bach ati scan tasks               Gescannte Tasks anzeigen
bach ati onboard PATH             Neues Projekt onboarden

BEFEHLE - TOOLS & PFADE
=======================

bach ati path NAME                Pfad zu einem Tool anzeigen
bach ati path --list              Alle Tool-Pfade auflisten

BEFEHLE - EXPORT & INSTALL
==========================

bach ati export                   ATI-Agent als ZIP exportieren
bach ati export --dry-run         Export-Trockenlauf (zeigt was exportiert wird)
bach ati install PFAD.zip         ATI-Export installieren

BEFEHLE - PROJEKT-BOOTSTRAPPING
===============================

bach ati bootstrap NAME --template TYPE  Neues Projekt mit Template erstellen
bach ati bootstrap my-tool --template python-cli
bach ati bootstrap my-skill --template llm-skill

BEFEHLE - PROJEKT-MIGRATION
===========================

bach ati migrate PATH --analyze           Bestehendes Projekt analysieren
bach ati migrate PATH --template TYPE     Projekt auf Template migrieren
bach ati migrate my-project --dry-run     Trockenlauf (keine Aenderungen)

BEFEHLE - MODULE
================

bach ati modules list             Verfuegbare Module auflisten

TEMPLATES
=========

python-cli     Python CLI-Anwendung mit setuptools/pyproject.toml
               Struktur: src/, tests/, docs/, _modules/, _policies/

llm-skill      LLM Skill fuer BACH/Claude
               Struktur: SKILL.md, _config/, _data/, _docs/

llm-agent      LLM Agent
               Struktur: AGENT.md, _skills/, _tools/

WIEDERVERWENDBARE MODULE
========================

_modules/ und modules/
├── path_healer.py       Pfad-Selbstheilung (von RecludOS/VFDistiller)
├── distribution.py      Tier-System, Siegel, Release-Management (modules/)
├── encoding.py          UTF-8, BOM-Handling, Encoding-Korrektur (modules/)
└── validation.py        Schema-Validierung (geplant)

BACH-POLICIES
=============

_policies/
├── naming_convention.md    Dateinamen-Konventionen
├── encoding_policy.md      UTF-8 Standard, keine BOM
└── path_rules.json         Relative Pfade, keine Hardcoded-Pfade

BEISPIELE
=========

# Daemon starten und Status pruefen
bach ati start
bach ati status

# Tasks verwalten
bach ati task list
bach ati task add "Feature X implementieren"
bach ati task done 1

# Projekt scannen und onboarden
bach ati scan
bach ati onboard C:\Projekte\neues-tool

# Neues Python-CLI-Projekt erstellen
bach ati bootstrap rechnungs-tool --template python-cli

# Bestehendes Projekt analysieren
bach ati migrate C:\Projekte\altes-tool --analyze

# Projekt auf BACH-Struktur migrieren (Dry-Run)
bach ati migrate C:\Projekte\altes-tool --template python-cli --dry-run

# ATI exportieren und woanders installieren
bach ati export
bach ati install C:\Downloads\ati_export.zip

MIGRATION-WORKFLOW
==================

1. Analyse:   bach ati migrate PATH --analyze
              Zeigt: Compliance-Score, fehlende Verzeichnisse, Probleme

2. Dry-Run:   bach ati migrate PATH --template TYPE --dry-run
              Zeigt was passieren wuerde ohne Aenderungen

3. Migration: bach ati migrate PATH --template TYPE
              Fuehrt Migration aus (erstellt Backup automatisch)

4. Verify:    bach ati migrate PATH --analyze
              Prueft neuen Compliance-Score

HINWEISE
========

- ATI nutzt project_bootstrapper.py (agents/ati/tools/)
- Templates liegen in agents/ati/templates/
- Module liegen in agents/ati/_modules/ und modules/
- Policies liegen in agents/ati/_policies/
- Scanner liegen in agents/ati/scanner/
- Session-Daemon liegt in agents/ati/session/
- Export liegt in agents/ati/export/
- Onboarding liegt in agents/ati/onboarding/
- Daten liegen in data/ati/ und data/bach.db
- Dokumentation: agents/ati/ATI.md
- Bootstrapping-Konzept: agents/ati/ATI_PROJECT_BOOTSTRAPPING.md

VERWANDT
========

bach --help builder        Build-Skill fuer Projekte
bach --help distribution   Distribution-System
bach --help coding         Coding-Konventionen
bach --help maintain       Wartungs-Tools (Pfadheilung)


## Bach Info

BACH INFO
=========

DEFINITION
BACH (Best-of BATCH + CHIAH) ist ein lokales, portables "Agentic Operating System" - 
eine Arbeitsumgebung für LLM-basierte KI-Assistenten. Es kombiniert Agenten-Frameworks, 
RAG-Systeme und kognitive Psychologie zu einem persönlichen "Nervensystem" für KIs.

KERNFEATURES (Die 7 Säulen)
1. Kognitives Memory-Modell: 5 Typen analog zum menschlichen Gedächtnis
   (Working, Episodisch, Semantisch, Prozedural, Assoziativ).
2. Aktive Konsolidierung: Das System lernt, vergisst und gewichtet Informationen
   via Decay, Boost und nächtliche Komprimierung.
3. Multi-Partner Delegation: Orchestrierung von Claude, Gemini und Ollama.
4. CLI-First + GUI: Volle Kontrolle via Terminal oder Web-Dashboard (8+ spezialisierte Boards).
5. Portable & Lokal: SQLite-basiert, kein Cloud-Zwang, volle Datenhoheit.
6. Domain-Agenten: 20+ Spezialisten (ATI, Steuer, Finanzassistent, Health, etc.).
7. Self-Healing: Automatische Wartung, Pfad-Heilung und Dokumentations-Forensik.

VERWENDUNG
Das System wird primär über dieses CLI (`bach.py`) oder das Web-Dashboard gesteuert.

BEFEHLE
bach --help             Uebersicht aller Themen
bach status             Aktueller Systemstatus
bach task list          Offene Aufgaben anzeigen
bach mem read           Aktuelles Gedaechtnis abrufen

ARCHITEKTUR
CLI/GUI/MCP --> Hub Handler --> Skills/Tools --> Datenbanken/Dateisystem/Partner

SIEHE AUCH
wiki/was_ist_bach.txt      Ausfuehrliche Definition & Vergleich
system/ARCHITECTURE.md     Architektur-Dokumentation (Schichten-Modell)
docs/help/architecture.txt Technische Details
docs/help/features.txt     Feature-Liste


## Bach Paths

BACH PATHS - Zentrale Pfadverwaltung
=====================================

bach_paths.py ist die "Single Source of Truth" fuer alle Pfade in BACH.
Keine hartcodierten Pfade mehr - alles zentral an einem Ort.

STANDORT
--------
system/hub/bach_paths.py

HAUPTFUNKTION: get_path(name)
-----------------------------
Die wichtigste Funktion - gibt den Pfad zu einem benannten Verzeichnis zurueck.

Beispiele:
    from bach_paths import get_path

    tools_dir = get_path("tools")           # system/tools/
    template = get_path("bericht_template") # Vorlage fuer Berichte
    db = get_path("db")                     # bach.db Datenbank
    berichte = get_path("berichte")         # Berichte-Verzeichnis

IMPORT VON UEBERALL
-------------------
Methode 1 - Wenn hub/ im sys.path (z.B. in hub/_services/):
    from bach_paths import BACH_ROOT, get_path

Methode 2 - Universal (funktioniert von ueberall):
    import sys
    from pathlib import Path

    # Finde bach_paths.py automatisch
    _current = Path(__file__).resolve()
    for _parent in [_current] + list(_current.parents):
        _hub = _parent / "system" / "hub"
        if _hub.exists():
            if str(_hub) not in sys.path:
                sys.path.insert(0, str(_hub))
            break

    from bach_paths import BACH_ROOT, get_path

VERFUEGBARE PFADE
-----------------
Hierarchie:     root, bach, system, hub
System:         data, gui, skills, dist
Skills:         tools, help, agents, experts, workflows, partners, services, templates
Data:           logs, backups, archive, trash, messages
Root:           user, docs, exports, extensions
Datenbanken:    db, bach_db, archive_db
User:           user_documents, persoenlich
Steuer:         steuer, steuer_2025, belege, bundles
Partner:        gemini, claude, ollama
Berichte:       foerderplanung, berichte, berichte_output, berichte_klienten, berichte_data, berichte_bundles, klienten, quarantine
Templates:      bericht_template
Extern:         wissensdatenbank

BEISPIEL: Tool-Import
---------------------
Problem: Tools liegen in system/tools/
Loesung mit bach_paths:

    try:
        from c_ocr_engine import ocr_pdf
    except ImportError:
        from bach_paths import get_path
        tools_dir = get_path("tools")
        if str(tools_dir) not in sys.path:
            sys.path.insert(0, str(tools_dir))
        from c_ocr_engine import ocr_pdf

BEISPIEL: Template-Pfad
-----------------------
    from bach_paths import get_path

    template_path = get_path("bericht_template")
    # -> C:/Users/.../BACH_v2_vanilla/system/skills/_templates/bericht_template_geiger_universal.docx

WEITERE FUNKTIONEN
------------------
list_paths()              - Alle verfuegbaren Pfade als Dict
get_tool_path(name)       - Findet Tool in tools/ oder Unterordnern
get_partner_dir(partner)  - Partner-Verzeichnis (gemini, claude, ollama)
get_belege_path(anbieter) - Belege-Pfad mit optionalem Anbieter
resolve(relpath)          - Relativen Pfad aufloesen
validate()                - Alle kritischen Pfade pruefen

DB-OVERRIDES
------------
Pfade koennen in der DB ueberschrieben werden:

    from bach_paths import set_path_override, get_path_with_override

    # Override setzen
    set_path_override("wissensdatenbank", "D:/Meine/Datenbank")

    # Override nutzen
    path = get_path_with_override("wissensdatenbank")

CLI NUTZUNG
-----------
    python bach_paths.py templates           # Einzelnen Pfad abrufen
    python bach_paths.py --list              # Alle Pfade auflisten
    python bach_paths.py --validate          # Pfade validieren
    python bach_paths.py --set PATH name     # Override setzen (mit name)
    python bach_paths.py --overrides         # DB-Overrides anzeigen
    python bach_paths.py --json              # Ausgabe als JSON

VARIABLEN (fuer direkten Import)
--------------------------------
    from bach_paths import (
        BACH_ROOT,      # Repository-Root
        SYSTEM_ROOT,    # system/
        HUB_DIR,        # system/hub/
        DATA_DIR,       # system/data/
        SKILLS_DIR,     # system/skills/
        TOOLS_DIR,      # system/tools/
        BACH_DB,        # system/data/bach.db
        USER_DIR,       # user/
        BERICHTE_DIR,   # user/documents/foerderplaner/Berichte/
    )

SELF-HEALING
------------
bach_paths berechnet alle Pfade relativ zum eigenen Standort.
Wenn BACH verschoben wird, funktioniert alles weiterhin -
keine manuellen Anpassungen noetig.

SIEHE AUCH
----------
- c_path_healer.py  - Pfad-Korrekturen in Dateien
- maintain heal     - CLI-Befehl zum Heilen von Pfaden


## Bach User Mounts

BACH USER-MOUNTS (KONZEPT)
==========================

Stand: 2026-02-08

WAS SIND USER-MOUNTS?
---------------------
User-Mounts sind eine implementierte Funktion (seit 2026-01-28, Task SYS_001), um externe Speicherorte (z.B. NAS, externe Festplatten, Cloud-Ordner wie Google Drive) transparent in das BACH-Dateisystem einzubinden. Anstatt Daten in den BACH-Ordner zu kopieren, werden sie virtuell verknuepft.

FUNKTIONSWEISE
--------------
Das System nutzt "Directory Junctions" oder "Symlinks", um externe Pfade als Unterordner im `user/`-Verzeichnis bereitzustellen.
Der `filesystem_scanner` und `dirscan` koennen diese Pfade dann wie lokale Ordner durchsuchen, indizieren und Dateien verarbeiten (z.B. fuer OCR oder Extraktion).

ZIELSETZUNG
-----------
*   **Keine Redundanz**: Originaldaten bleiben an ihrem Ort.
*   **Transparenz**: Alle BACH-Tools koennen auf die Daten zugreifen.
*   **Persistenz**: Verbindungen werden in der Datenbank (`connections`-Tabelle) gespeichert und bei Bedarf (nach Neustart) wiederhergestellt.

BEISPIEL
--------
Ein User hat Steuerunterlagen auf `E:\Archiv\Steuer`.
Via User-Mount wird dies eingebunden als: `user/mounts/archiv_steuer/`.
Der Steuer-Agent kann nun auf `user/mounts/archiv_steuer/2025/` zugreifen, als waere es lokal.

TECHNISCHE DETAILS
------------------
*   **DB-Tabelle**: `connections` (type='mount', name='alias', endpoint='source_path')
*   **Handler**: `system/hub/mount.py` (verwaltet mklink Befehle)
*   **CLI-Befehle**:
    - `bach mount add <pfad> <alias>` - Ordner anbinden
    - `bach mount remove <alias>` - Anbindung entfernen
    - `bach mount list` - Aktive Mounts anzeigen
    - `bach mount restore` - Mounts nach Neustart wiederherstellen

STATUS
------
IMPLEMENTIERT (seit 2026-01-28). Vollstaendig funktionsfaehig. CLI-Befehle verfuegbar. GUI-Integration geplant fuer spaetere Phase.

SIEHE AUCH
----------
wiki/it_tools/filecommander.txt           Datei-Operationen
docs/_archive/CONCEPT_user_folder_attachment.md  Technisches Konzept (archiviert)


## Backup

BACKUP & RESTORE
================

Das Backup-System basiert auf dem dist_type Konzept:

  dist_type = 2 (CORE)      → Distribution IST das Backup
  dist_type = 1 (TEMPLATE)  → 1x Snapshot bei Installation
  dist_type = 0 (USER_DATA) → Normale Backup-Rotation

BEFEHLE
-------

  # Backup erstellen
  bach backup create                  Lokales Backup
  bach backup create --to-nas         Auch auf NAS kopieren

  # Backups anzeigen
  bach backup list                    Lokale Backups
  bach backup list --nas              NAS-Backups
  bach backup info <name>             Backup-Details

  # Wiederherstellen (NUR userdata_*.zip Backups)
  bach restore backup <name>          Bestimmtes Backup
  bach restore backup latest          Neuestes Backup

  # Template zurücksetzen (NUR via backup_manager.py)
  python system/tools/backup_manager.py restore template SKILL.md

WAS WIRD GESICHERT?
-------------------

  dist_type = 0 (USER_DATA):
    ├── tasks (alle Tasks, Status, History)
    ├── memory/ (Sessions, Longterm, Archive)
    ├── data/logs/ (Session-Logs, konsolidierter Pfad)
    └── user/ (Inbox, Nachrichten, Agenda)

  NICHT gesichert (dist_type >= 1):
    ├── bach.py, schema.sql, hub/
    ├── tools/, skills/, docs/help/
    └── (sind Teil der Distribution)

BACKUP-ROTATION
---------------

  Lokal (system/data/backups/):  7 Backups behalten
  NAS:                           30 Backups behalten
  OneDrive:                      Automatisch (Versionsverlauf)

SPEICHERORTE
------------

  Lokal:   system/data/backups/
  NAS:     \\YOUR_NAS_IP\fritz.nas\Extreme_SSD\BACKUP\BACH_Backups
  Logs:    system/data/logs/ (konsolidiert)

TOOLS
-----

  system/tools/backup_manager.py     Direkter Aufruf möglich:
    python system/tools/backup_manager.py create [--to-nas]
    python system/tools/backup_manager.py list [--nas]
    python system/tools/backup_manager.py info <name>
    python system/tools/backup_manager.py restore backup <name>
    python system/tools/backup_manager.py restore template <file>
    python system/tools/backup_manager.py snapshot <file>

API
---

  POST /api/v1/backup         Backup erstellen (Headless)
  GET  /api/v1/backup/list    Backups auflisten

VERWANDTE SKILLS
----------------

  skills/_service/builder.md  → CREATE, EXPORT, DISTRIBUTE, BACKUP, RESTORE
  docs/BACKUP_SYSTEM.md       → Ursprüngliches Konzept aus _BATCH


## Beat

BEAT - Unified Zeit-Anzeige
===========================

Zentrale Steuerung aller Zeit-Funktionen (Clock, Timer, Countdown, Between).

CLI-BEFEHLE
-----------

  bach beat                 Alle Zeit-Infos anzeigen
  bach beat on              Alle Zeit-Anzeigen aktivieren
  bach beat off             Alle Zeit-Anzeigen deaktivieren
  bach beat interval <sek>  Globales Intervall setzen

AUSGABE-FORMAT
--------------

  [BEAT] 14:35
    Timer:     Session 45:12 | Recherche 05:23
    Countdown: focus 19:45 verbleibend
    Between:   Profil "Algebra" aktiv

KOMPONENTEN
-----------

  1. CLOCK - Uhrzeit
     Zeigt aktuelle Uhrzeit
     -> bach clock on|off|interval

  2. TIMER - Stoppuhr
     Zeigt laufende Timer
     -> bach timer start|stop|list

  3. COUNTDOWN - Countdown
     Zeigt aktive Countdowns
     -> bach countdown start|stop|list

  4. BETWEEN - Zwischen-Checks
     Zeigt aktives Profil
     -> bach between on|off|use

BEISPIELE
---------

  # Alle Zeit-Infos auf einen Blick
  bach beat
  -> [BEAT] 14:35
  ->   Timer:     Session 45:12
  ->   Countdown: -
  ->   Between:   default

  # Alles ausschalten (fokussiertes Arbeiten)
  bach beat off

  # Alles einschalten mit 2-Min Intervall
  bach beat on
  bach beat interval 120

ZUSAMMENSPIEL MIT INJEKTOREN
----------------------------

Die Zeit-Anzeigen werden ueber das Injektor-System ausgegeben.
`bach beat` ist die einheitliche Steuerung dafuer.

Alte Befehle (deprecated):
  --inject toggle timebeat     -> bach beat on|off
  --inject toggle between      -> bach between on|off

Neue Struktur:
  TimeManager verwaltet Clock, Timer, Countdown
  BetweenManager verwaltet Profile und Checks

ARCHITEKTUR
-----------

  ┌─────────────────────────────────────┐
  │           TimeManager               │
  ├─────────────────────────────────────┤
  │  ┌─────────┐ ┌─────────┐ ┌────────┐ │
  │  │ Clock   │ │ Timer   │ │Countdown│ │
  │  └─────────┘ └─────────┘ └────────┘ │
  └─────────────────────────────────────┘
               │
               v
  ┌─────────────────────────────────────┐
  │         BetweenManager              │
  │  (Profile-basierte Between-Checks)  │
  └─────────────────────────────────────┘
               │
               v
  ┌─────────────────────────────────────┐
  │         InjectorSystem              │
  │    (Ausgabe bei CLI-Befehlen)       │
  └─────────────────────────────────────┘

SIEHE AUCH
----------

  --help clock      Uhrzeit-Anzeige
  --help timer      Stoppuhr
  --help countdown  Countdown mit Trigger
  --help between    Between-Checks mit Profilen

---
Version: 1.0 | Status: Implementiert (v1.1.83)
Siehe: docs/_archive/con4_CONCEPT_time_system_90.md


## Bericht

FOERDERBERICHT
==============

ICF-basierte Entwicklungsberichte erstellen, exportieren und archivieren.
Alle Klientendaten werden automatisch anonymisiert.

WICHTIG: Der Handler (system/hub/bericht.py) nutzt FALSCHE Pfade!
         Er verweist auf user/buero/foerderplanung (existiert nicht).
         Tatsaechlicher Pfad: user/documents/foerderplaner/
         Generator (generator.py) nutzt korrekte Pfade via bach_paths.py.

BEFEHLE
-------

  bach bericht help
    Zeigt diese Hilfe an.

  bach bericht list
    Listet alle Klienten-Ordner mit Status (JSON/DOCX vorhanden).

  bach bericht status
    Zeigt Pipeline-Status aller Ordner (Berichte/data, bundles, output, _archive).

  bach bericht extract <klient-ordner> [-o output]
    Extrahiert Text aus .docx, .txt, .pdf im Klienten-Ordner.
    Ohne -o wird der Text auf stdout ausgegeben.

  bach bericht prompt <klient-ordner> [-o output]
    Erstellt den vollstaendigen LLM-Prompt inkl. ICF-Referenz
    und JSON-Schema-Anforderungen.

  bach bericht generate <json-datei> -o <output> [-t vorlage]
    Fuellt die Word-Vorlage mit Daten aus der JSON-Datei.
    -t: Vorlage (Standard: bericht_template_geiger_universal.docx)
    -o: Ausgabedatei (erforderlich)

  bach bericht export <klient-ordner> -p <passwort>
    De-anonymisiert den Bericht und legt ihn in
    Berichte/output/<Echter_Name>/ ab.

  bach bericht archive [name]
    Verschiebt einen fertigen Bericht aus Berichte/output/
    nach _archive/<Name>_YYYY-MM/.

BEISPIELE
---------

  # Uebersicht
  bach bericht list
  bach bericht status

  # Workflow (mit anonymisierten Bundles)
  bach bericht extract Berichte/bundles/K_CE2E70
  bach bericht prompt Berichte/bundles/K_CE2E70 -o Berichte/bundles/K_CE2E70/core/_prompt.txt
  bach bericht generate Berichte/bundles/K_CE2E70/output/bericht_data.json \
    -o Berichte/bundles/K_CE2E70/output/bericht_2026-02.docx
  bach bericht export Berichte/bundles/K_CE2E70 -p bach2026
  bach bericht archive Mustermann_Max

PIPELINE (user/documents/foerderplaner/)
-----------------------------------------

  Berichte/data/<Echter_Name>/     Echte Akten (nur User-Zugriff)
         ↓
  Berichte/bundles/K_xxxx/         Anonymisierte Bundles (LLM/Chatbot)
         ↓
  Berichte/output/<Echter_Name>/   De-anonymisierte Berichte
         ↓
  _archive/<Name>_YYYY-MM/         Abgeschlossene Berichte

VERWANDTE SKILLS
----------------

  agents/_experts/report_generator/generator.py      Report Generator
  hub/_services/document/anonymizer_service.py       Anonymisierung
  skills/_templates/bericht_template_geiger_universal.docx  Word-Vorlage
  user/documents/foerderplaner/                      Klientendaten & Output


## Between Tasks

# Portabilitaet: UNIVERSAL
# Version: 1.0.0
# Zuletzt validiert: 2026-02-08
# Naechste Pruefung: 2026-08-08

# HINWEIS: Dieser Eintrag wurde nach between.txt migriert
#
# Siehe: bach help between
#
# Die Between-Tasks Funktionalitaet wurde erweitert und unterstuetzt jetzt:
# - Anpassbare Profile (DEFAULT, FOCUS, REVIEW, LEARNING, AUTOSESSION)
# - CLI-Befehle: bach between on/off/status/use
# - Profil-Verwaltung: bach between profile list/show (add/edit/delete noch nicht implementiert)
#
# Vollstaendige Dokumentation: docs/docs/docs/help/between.txt


## Between

BETWEEN - Zwischen-Checks mit Profilen
======================================

Erinnerungen zwischen Tasks. Anpassbar durch Profile.

CLI-BEFEHLE
-----------

  An/Aus:
  bach between on                  Between-Checks aktivieren
  bach between off                 Deaktivieren
  bach between status              Status zeigen

  Profile verwalten:
  bach between profile add "Name"     Neues Profil erstellen
  bach between profile edit "Name"    Profil bearbeiten
  bach between profile delete "Name"  Profil loeschen
  bach between profile list           Alle Profile anzeigen
  bach between profile show "Name"    Profil-Details

  Profil aktivieren:
  bach between use "Name"          Profil fuer Session aktivieren
  bach between use default         Zurueck zum Standard-Profil (nutzt "default" als Name)

PROFIL-STRUKTUR
---------------

  {
    "name": "Algebra",
    "description": "Mathematik-Aufgaben mit Verifikation",
    "message": "ZWISCHEN-CHECK:\n1. Kontrolliere Ergebnis\n2. Pruefe Rechenweg\n3. Dokumentiere",
    "trigger_on": ["task done", "task complete"],
    "is_default": false
  }

STANDARD-PROFILE
----------------

  1. DEFAULT
     Generischer Between-Check (aktuelles Verhalten)
     "1. Zeit-Check  2. Memory OK?  3. Naechste Aufgabe?"

  2. FOCUS
     Minimaler Check fuer fokussierte Arbeit
     "Weitermachen oder Pause?"

  3. REVIEW
     Ausfuehrlicher Check mit Code-Review Hinweisen
     "1. Code reviewen  2. Tests laufen?  3. Dokumentiert?"

  4. LEARNING
     Check mit Reflexionsfragen
     "1. Was gelernt?  2. Lesson anlegen?  3. Verstanden?"

  5. AUTOSESSION
     Auto-Session Workflow mit Zeitkontrolle
     "1. Zeit-Check  2. Dauer letzte Aufgabe?  3. Weiter oder Session-Ende?"

BEISPIELE
---------

  # Neues Profil fuer Mathe-Aufgaben
  bach between profile add "Mathe"
  -> Profil 'Mathe' erstellt (bearbeiten mit: between profile edit)

  # Profil anzeigen
  bach between profile show "Mathe"
  -> Zeigt Details des Profils (edit noch nicht implementiert)

  # Profil aktivieren
  bach between use "Mathe"
  -> Profil 'Mathe' fuer diese Session aktiviert

  # Zurueck zu Standard
  bach between use default

AUSGABE-FORMAT
--------------

  [BETWEEN-TASKS]
  1. Kontrolliere das Ergebnis der letzten Aufgabe
  2. Pruefe Rechenweg auf Fehler
  3. Dokumentiere Zwischenschritte

  Tipp: --status fuer Uebersicht

PERSISTENZ
----------

  Tabelle: between_profiles (bach.db)
  Aktives Profil: data/.between_state

HINWEIS
-------

  Profile add/edit/delete sind noch nicht implementiert.
  Verwende DB direkt oder warte auf zukuenftige Version.

USECASES
--------

  1. PROJEKT-SPEZIFISCH
     Jedes Projekt hat eigenes Between-Profil
     -> Wechseln bei Projekt-Wechsel

  2. LERN-SESSIONS
     Profil "Learning" mit Reflexionsfragen
     -> Foerdert bewusstes Lernen

  3. CODE-REVIEW
     Profil "Review" mit Review-Checkliste
     -> Qualitaetssicherung

  4. FOKUS-MODUS
     Profil "Focus" mit minimalem Check
     -> Weniger Unterbrechung

ZUSAMMENSPIEL
-------------

Between ist Teil des Zeit-Systems:
  --help clock      Uhrzeit-Anzeige
  --help timer      Stoppuhr
  --help countdown  Countdown mit Trigger
  --help beat       Unified Zeit-Anzeige

---
Version: 1.0 | Status: Implementiert (v1.1.83)
Handler: system/hub/time.py (BetweenHandler)
Tool: system/tools/time_system.py (BetweenManager)


## Bugfix

BUGFIX PROTOKOLL - SCHNELLREFERENZ
===================================

Bei Fehlern IMMER diese Reihenfolge:

1. STANDARD-FIXER ZUERST
   python system/tools/c_standard_fixer.py <datei>
   Behebt: BOM, Encoding, Umlaute, JSON-Probleme
   -> Problem geloest? Arbeit gespart!

2. IMPORT-DIAGNOSE
   python system/tools/c_import_diagnose.py <ordner>
   Prueft: Circular Imports, fehlende Module

3. CODE-ANALYSE
   python system/tools/c_method_analyzer.py <datei>
   Prueft: Attribut vor Definition, Signal-Callbacks

4. ISOLIERTES TESTEN
   Minimales Test-Script erstellen
   Schrittweise eingrenzen

5. 20-MINUTEN-REGEL
   Nach 20 Min ohne Fortschritt: STOP
   Bug-Report erstellen, spaeter fortsetzen

SCHNELL-CHECK:

| Fehlertyp           | Erste Aktion              |
|---------------------|---------------------------|
| Import-Fehler       | c_import_diagnose.py      |
| AttributeError      | c_method_analyzer.py      |
| Silent Crash        | c_method_analyzer.py      |
| Encoding/BOM        | c_standard_fixer.py       |

HINWEIS: Diese Datei dokumentiert standalone Tools, keinen Handler.
         Detaillierte Bugfix-Workflows: skills/workflows/bugfix-protokoll.md


## Builder

BUILDER - Skill/Agent Erstellung & Export
==========================================

BACH COMMAND (bevorzugt)
-------------------------
bach skills export <name>               Skill exportieren (v2.0)
bach skills list                        Alle Skills auflisten
bach skills version <name>              Versions-Check


WERKZEUGE IN system/tools/
---------------------------
c_structure_generator.py <n> <profil>   Skill/Agent erstellen
c_structure_generator.py <n> --embedded Für BACH (leichtgewichtig)

generators/os_generator.py <n> [ziel]   Neues OS erstellen
generators/exporter.py skill <n>        Skill exportieren
generators/distribution_system.py       Distribution-System


PROFILE-SPEKTRUM
----------------
MICRO      Nur SKILL.md (1 Datei)
LIGHT      Minimale Struktur (~5 Dateien)
STANDARD   Mit Memory (~12 Dateien)
EXTENDED   Mit Mikro-Skills (~20 Dateien)
AGENT      Mit Workflows (~30 Dateien)
AGENT_FULL Vollständig (~50 Dateien)


DIST_TYPE SYSTEM
----------------
2 = CORE      Immer mitverpacken
1 = TEMPLATE  Auf Original zurücksetzen
0 = USER      Nicht exportieren


SCHNELLBEFEHLE
--------------
Skill exportieren:     bach skills export analyse
Skills auflisten:      bach skills list
Versions-Check:        bach skills version analyse


ZUGEHOERIGE HANDLER
-------------------
system/hub/skills.py                    SkillsHandler (v2.0)


Siehe auch: builder.md (hub/_services/)


## Calendar

CALENDAR - Termin- und Kalenderverwaltung
=========================================

STAND: 2026-02-08

Das Kalender-System (Schicht 3) bündelt zeitkritische Informationen aus 
verschiedenen Quellen (Termine, Erinnerungen, Routinen).

KERNKONZEPTE
------------
- KOMBINATION: Zeigt Assistenten-Kalender UND faellige Haushaltsroutinen an.
- ANSICHTEN: Optimiert für CLI (Today, Week, Month).
- PERSISTENZ: Speicherung in der zentralen `bach.db`.

CLI-BEFEHLE (bach calendar)
---------------------------
  today         Termine und fällige Routinen für heute.
  week          Wochenübersicht (Mo-So) mit Wochentag-Namen.
  month         Alle Einträge des aktuellen Monats.
  list          Alle kommenden Termine (Standard: 30 Tage).
  add "Titel"   Erstellt einen neuen Termin (assistant_calendar).
  show <ID>     Zeigt Termin-Details an.
  done <ID>     Markiert einen Termin als erledigt.
  delete <ID>   Löscht einen Termin.
  help          Zeigt Hilfe an.

ANZEIGE-FORMAT
--------------
  [Mo 28.01.] ----------------------------------------
    09:00 Zahnarzt Dr. Müller
    [R04] ---- Küche aufräumen (täglich, Haushalt)

DATENBANK (Schicht 1)
---------------------
- `assistant_calendar`: Manuelle Termine des Users.
- `household_routines`: Wiederkehrende Aufgaben (nur Anzeige).
- `calendar_events`: (Optional) System-Events.

GUI & INTEGRATION
-----------------
Das **Assistant-Dashboard** in der GUI bietet eine grafische Wochen- und 
Monatsansicht. Der Kalender dient als zeitliche Schiene für Schicht 5 Automation.

SIEHE AUCH
----------
  bach routine         Verwaltung der Haushaltsroutinen
  bach --help clock    Zeit- und Zeitstempel-Tools
  docs/docs/docs/help/memory.txt      Zeitliche Einordnung von Sessions


## Claude Code Automatisierung

CLAUDE CODE AUTOMATISIERUNG
============================

Anleitung zur Automatisierung von Claude Code über die Kommandozeile (CLI).


ÜBERSICHT
---------
Claude Code kann im non-interaktiven Modus betrieben werden, was die
Integration in Skripte, CI/CD-Pipelines und automatisierte Workflows ermöglicht.


1. NON-INTERAKTIVER MODUS (-p / --print)
----------------------------------------
Der wichtigste Parameter für Automatisierung. Claude gibt die Antwort aus
und beendet sich.

    # Einfache Anfrage
    claude -p "Erkläre mir was diese Funktion macht"

    # Mit Datei-Input über Pipe
    cat mycode.py | claude -p "Analysiere diesen Code"

    # Über stdin
    echo "Was ist 2+2?" | claude -p


2. AUSGABEFORMATE FÜR SCRIPTING
-------------------------------
Text (Standard):
    claude -p "Deine Anfrage"

JSON (einzelnes Ergebnis):
    claude -p "Liste 5 Programmiersprachen" --output-format json

Stream-JSON (Echtzeit-Streaming):
    claude -p "Schreibe einen Test" --output-format stream-json


3. BERECHTIGUNGEN UND SICHERHEIT
--------------------------------
Vollautomatisch ohne Bestätigungen:
    # ACHTUNG: Nur in sicheren/isolierten Umgebungen verwenden!
    claude -p "Erstelle eine index.html" --dangerously-skip-permissions

Permission Mode wählen:
    # Plan-Modus: Claude plant Änderungen vor Ausführung
    claude -p "Refactor Code" --permission-mode plan

    # DontAsk-Modus: Keine Rückfragen während Ausführung
    claude -p "Update dependencies" --permission-mode dontAsk

Mit eingeschränkten Tools:
    # Nur bestimmte Tools erlauben
    claude -p "Zeige git status" --allowedTools "Bash(git:*)"

    # Bestimmte Tools verbieten
    claude -p "Analysiere Code" --disallowedTools "Edit Write"

    # Alle Tools deaktivieren außer spezifische
    claude -p "Nur lesen" --tools "Read"


4. SESSION-MANAGEMENT
---------------------
Letzte Session fortsetzen:
    claude --continue

Bestimmte Session per ID fortsetzen:
    claude --resume SESSION_ID

Neue Session-ID bei Fortsetzung erstellen:
    claude --continue --fork-session


5. BUDGET UND MODELL-KONTROLLE
------------------------------
    # Budget-Limit setzen (in USD)
    claude -p "Komplexe Analyse" --max-budget-usd 1.00

    # Modell wählen
    claude -p "Schnelle Frage" --model sonnet
    claude -p "Komplexe Aufgabe" --model opus

    # Fallback-Modell bei Überlastung
    claude -p "Anfrage" --fallback-model sonnet


6. SYSTEM-PROMPT ANPASSEN
-------------------------
    # Eigenen System-Prompt setzen
    claude -p "Anfrage" --system-prompt "Du bist ein Python-Experte"

    # System-Prompt erweitern
    claude -p "Anfrage" --append-system-prompt "Antworte immer auf Deutsch"


7. CI/CD INTEGRATION
--------------------
Beispiel: Code-Review in Pipeline

    #!/bin/bash
    # code_review.sh
    claude -p "Review diesen Code auf Sicherheitsprobleme und Best Practices" \
      --output-format json \
      --dangerously-skip-permissions \
      --max-budget-usd 1.00 \
      --model sonnet

Beispiel: Automatische Dokumentation

    #!/bin/bash
    # generate_docs.sh
    cat src/main.py | claude -p "Erstelle eine API-Dokumentation im Markdown-Format" \
      --output-format text \
      --dangerously-skip-permissions > docs/API.md

Beispiel: Test-Generierung

    #!/bin/bash
    # generate_tests.sh
    claude -p "Generiere Unit-Tests für die Funktion in src/utils.py" \
      --dangerously-skip-permissions \
      --allowedTools "Read Write" \
      --max-budget-usd 0.50


8. BIDIREKTIONALES STREAMING
----------------------------
Für komplexe Integrationen mit Echtzeit-Kommunikation:

    claude -p "..." \
      --input-format stream-json \
      --output-format stream-json \
      --include-partial-messages


9. MCP SERVER INTEGRATION
-------------------------
    # MCP-Konfiguration laden (JSON-Datei oder String)
    claude -p "Anfrage" --mcp-config ./mcp-config.json

    # Mehrere Configs laden
    claude -p "Anfrage" --mcp-config ./config1.json ./config2.json

    # Nur MCP-Server aus Config verwenden
    claude -p "Anfrage" --mcp-config ./mcp-config.json --strict-mcp-config

    # MCP-Server verwalten
    claude mcp                    # Interaktives Management
    claude mcp --help             # MCP-Befehle anzeigen


10. ERWEITERTE FEATURES
-----------------------
Strukturierte JSON-Ausgabe:
    # JSON Schema validieren
    claude -p "Gib mir User-Daten" --json-schema '{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}'

Agenten verwenden:
    # Vorkonfigurierte Agenten
    claude -p "Review Code" --agent reviewer

    # Eigene Agenten definieren
    claude -p "Anfrage" --agents '{"tester": {"description": "Testet Code", "prompt": "Du bist ein QA-Experte"}}'

Plugin-Integration:
    # Plugins aus Verzeichnis laden
    claude -p "Anfrage" --plugin-dir ./my-plugins

Zusätzliche Verzeichnisse erlauben:
    # Erweitert Tool-Zugriff
    claude -p "Analysiere mehrere Projekte" --add-dir /path/to/project1 /path/to/project2

Debug-Modus:
    # Mit Filter
    claude -p "Anfrage" --debug "api,hooks"

    # Ohne bestimmte Kategorien
    claude -p "Anfrage" --debug "!1p,!file"

    # Debug-Log in Datei schreiben
    claude -p "Anfrage" --debug-file ./debug.log


WICHTIGE PARAMETER-REFERENZ
---------------------------
Parameter                       Beschreibung
---------                       ------------
-p, --print                     Non-interaktiver Modus (Pflicht für Automatisierung)
--output-format                 text, json, stream-json
--input-format                  text, stream-json
--dangerously-skip-permissions  Keine Bestätigungsdialoge
--permission-mode               acceptEdits, bypassPermissions, default, delegate, dontAsk, plan
--allowedTools                  Erlaubte Tools (z.B. "Bash(git:*) Read")
--disallowedTools               Verbotene Tools
--tools                         Tool-Liste oder "" für keine, "default" für alle
--max-budget-usd                Budget-Limit in USD
--model                         Modell (sonnet, opus, oder vollständiger Name)
--fallback-model                Fallback bei Überlastung
--system-prompt                 Eigener System-Prompt
--append-system-prompt          System-Prompt erweitern
--continue                      Letzte Session fortsetzen
--resume                        Session per ID fortsetzen
--fork-session                  Neue Session-ID bei Fortsetzung
--session-id                    Spezifische Session-ID setzen (UUID)
--mcp-config                    MCP-Server-Konfiguration(en)
--strict-mcp-config             Nur MCP aus Config verwenden
--json-schema                   JSON Schema für validierte Ausgabe
--agent                         Vorkonfigurierter Agent
--agents                        Eigene Agenten als JSON
--plugin-dir                    Plugin-Verzeichnisse
--add-dir                       Zusätzliche Verzeichnisse erlauben
--debug                         Debug-Modus mit optionalem Filter
--debug-file                    Debug-Logs in Datei schreiben
--no-session-persistence        Session nicht speichern (nur mit --print)


SICHERHEITSHINWEISE
-------------------
1. --dangerously-skip-permissions nur in isolierten Umgebungen
   (Sandboxes, Container) verwenden
2. Budget-Limits setzen um unerwartete Kosten zu vermeiden
3. Tools einschränken mit --allowedTools wenn möglich
4. Keine sensiblen Daten über Pipes an Claude senden


SIEHE AUCH
----------
- claude --help               Vollständige Hilfe
- claude doctor               Installations-Check
- claude mcp                  MCP-Server verwalten
- claude plugin               Plugin-Management
- claude setup-token          Langlebiges Auth-Token einrichten
- claude install [target]     Native Build installieren (stable/latest/version)
- claude update               Auf Updates prüfen
- claude-code.txt             Allgemeine Claude Code Informationen


## Claude Code Injections

CLAUDE CODE INJEKTIONS-SYSTEM -- ANATOMIE
==========================================

Stand: 2026-02-17
Quelle: Reverse-Engineering aus cli.js v2.1.44 (minifiziert)
Methode: Regex-Analyse + systematische Prompt-Tests

UEBERBLICK
----------
Claude Code injiziert sogenannte "System-Reminders" in den Nachrichtenstrom
zwischen User und LLM. Das LLM (Claude) sieht diese als Teil der Konversation,
kann aber nicht unterscheiden ob sie vom User oder vom System stammen --
ausser am <system-reminder> XML-Tag.

Anders als BACHs Injektor-System (siehe: injectors.txt) hat der User bei
Claude Code KEINE direkte Kontrolle ueber die Injektionen. Das LLM kann
sie weder an- noch abschalten.

ARCHITEKTUR
-----------
  User-Nachricht
      |
      v
  Claude Code CLI (Node.js, cli.js)
      |
      +--> d6() -- erzeugt User-Message-Objekt
      |      Felder: content, isMeta, isVisibleInTranscriptOnly,
      |      isCompactSummary, uuid, timestamp, todos, ...
      |      isMeta:true = unsichtbar im User-Transcript
      |
      +--> Px() -- System-Reminder Wrapper
      |      function Px(A) { return `<system-reminder>\n${A}\n</system-reminder>` }
      |
      +--> s5() -- Bulk-Wrapper
      |      Wendet Px() auf alle Text-Inhalte in Message-Arrays an
      |
      v
  API-Call an Anthropic (Messages mit injizierten system-reminders)
      |
      v
  LLM (Claude) -- sieht system-reminders im Nachrichtenstrom

KERN-FUNKTIONEN (deobfusciert)
------------------------------
  d6({content, isMeta, ...})
    Erstellt ein Message-Objekt vom Typ "user" mit role:"user".
    isMeta:true bedeutet: Nachricht ist im Transcript nicht sichtbar,
    wird aber ans LLM gesendet.

  Px(text)
    Wrapped Text in <system-reminder> Tags.
    Einfachste Funktion im System.

  s5(messages)
    Iteriert ueber Message-Array und wendet Px() auf alle
    Text-Inhalte an. Bulk-Operation.

ALLE 52 INJEKTIONS-TYPEN
-------------------------

Datei-Operationen (12):
  file                    Datei gelesen (mit Inhalt)
  already_read_file       Datei wurde schon gelesen (no-op)
  edited_text_file        Textdatei wurde editiert
  edited_image_file       Bilddatei editiert (no-op)
  pdf                     PDF gelesen
  pdf_reference           PDF-Referenz
  image                   Bild gelesen
  notebook                Jupyter Notebook
  directory               Verzeichnis-Listing (via ls)
  compact_file_reference  Kompakte Datei-Referenz
  selected_lines_in_ide   User hat Zeilen in IDE selektiert
  opened_file_in_ide      User hat Datei in IDE geoeffnet

Memory/Kontext (4):
  nested_memory           Inhalt von Memory-Unterfiles
                          Format: "Contents of {path}:\n{content}"
  ultramemory             Ultra-Memory Injektion (generisch)
  compaction_reminder     "Auto-compact enabled, older messages will be summarized"
  date_change             "The date has changed. DO NOT mention this to the user"

Task/Todo-Management (5):
  task_reminder           "Task tools haven't been used recently" (Nudge)
  task_progress           Task-Fortschrittsmeldung (generisch)
  task_status             Task-Status: killed/stopped + Details
  todo                    Todo-Eintrag
  todo_reminder           Todo-Nudge (aelteres System, gleicher Mechanismus)

Plan-Modus (5):
  plan_mode               Plan-Modus aktiviert
  plan_mode_exit          Plan-Modus verlassen
  plan_mode_reentry       Zurueck in Plan-Modus (liest existierenden Plan)
  plan_file_reference     Referenz auf Plan-Datei
  verify_plan_reminder    "Plan implementiert, bitte verifizieren"

Team/Agenten (5):
  agent_mention           "User wants to invoke agent X"
  delegate_mode           Delegate-Modus: nur Team-Tools erlaubt
  delegate_mode_exit      Delegate-Modus verlassen
  team_context            Team-Kontext-Injektion
  teammate_mailbox        Nachrichten von Teammates (nur im Team-Modus)

Hooks (10):
  hook_blocking_error     Hook hat Aktion blockiert (mit Fehlermeldung)
  hook_success            Hook erfolgreich (nur SessionStart/UserPromptSubmit)
  hook_additional_context Hook liefert zusaetzlichen Kontext
  hook_error_during_execution  Hook-Fehler waehrend Ausfuehrung (no-op)
  hook_non_blocking_error Nicht-blockierender Hook-Fehler (no-op)
  hook_cancelled          Hook abgebrochen (no-op)
  hook_stopped_continuation   Hook hat Fortsetzung gestoppt
  hook_system_message     Hook-Systemnachricht
  hook_permission_decision    Hook-Permission-Entscheidung
  async_hook_response     Asynchrone Hook-Antwort

Ressourcen/Budget (2):
  token_usage             "Token usage: X/Y; Z remaining"
  budget_usd              "USD budget: $X/$Y; $Z remaining"

Skills/MCP (4):
  skill_listing           Liste verfuegbarer Skills
  invoked_skills          Aufgerufene Skills
  dynamic_skill           Dynamischer Skill (no-op, returns [])
  mcp_resource            MCP-Ressource geladen

Sonstige (5):
  text                    Einfacher Text
  queued_command           Wartender Slash-Command
  structured_output       Strukturierter Output
  diagnostics             IDE-Diagnose (neue Fehler/Warnungen)
  output_style            Output-Style aktiv (z.B. "explanatory")
  critical_system_reminder    Kritische System-Erinnerung (generisch)
  command_permissions     Command-Permissions (no-op)

NO-OP TYPEN (erzeugen keine Injektion):
  already_read_file, command_permissions, edited_image_file,
  hook_cancelled, hook_error_during_execution, hook_non_blocking_error,
  dynamic_skill

TIMING-KONSTANTEN
-----------------
  Xf6 = {
      TURNS_SINCE_WRITE: 10          Task-Nudge nach 10 Turns ohne Task-Tool
      TURNS_BETWEEN_REMINDERS: 10    Min. 10 Turns zwischen Task-Nudges
  }

  qt4 = {
      TURNS_BETWEEN_ATTACHMENTS: 5          Attachment-Reminder alle 5 Turns
      FULL_REMINDER_EVERY_N_ATTACHMENTS: 5  Voller Reminder alle 5 Attachments
  }

  aQY = {
      TOKEN_COOLDOWN: 5000           Token-Cooldown (nach 5000 Tokens)
  }

  sQY = {
      TURNS_BETWEEN_REMINDERS: 10    Allgemeiner Reminder-Intervall
  }

  Hinweis: "Turns" zaehlt alle LLM-Interaktionen inkl. Tool-Aufrufe,
  nicht nur User-Nachrichten. Deshalb erscheinen Nudges unregelmaessig
  aus User-Perspektive.

TRIGGER-LOGIK (Task-Reminder, deobfusciert)
-------------------------------------------
  function shouldInjectTaskReminder(messages) {
      // Nur wenn Task-Tools verfuegbar
      if (!taskToolsEnabled()) return false;
      if (messages.length === 0) return false;

      // Zaehle Turns seit letzter Task-Tool-Nutzung
      let turnsSinceLastUse = 0;
      let turnsSinceLastReminder = 0;

      for (msg in messages.reverse()) {
          if (msg.type === "assistant" && msg.usedTool("TaskCreate" || "TaskUpdate"))
              break;  // Letzte Task-Tool-Nutzung gefunden
          turnsSinceLastUse++;
      }

      // Pruefe ob Reminder faellig
      if (turnsSinceLastUse >= 10 && turnsSinceLastReminder >= 10) {
          let tasks = getAllTasks();
          return { type: "task_reminder", content: tasks };
      }
      return false;
  }

GEHEIMHALTUNGS-ANWEISUNGEN
---------------------------
Folgende Typen enthalten explizite "NEVER mention"-Anweisungen:

  task_reminder:     "Make sure that you NEVER mention this reminder to the user"
  todo_reminder:     "Make sure that you NEVER mention this reminder to the user"
  date_change:       "DO NOT mention this to the user explicitly"
  nested_memory:     "Don't tell the user this, since they are already aware"
    (bei CLAUDE.md/MEMORY.md Aenderungen)

VERGLEICH: CLAUDE CODE vs. BACH INJEKTOREN
------------------------------------------

  Eigenschaft           | Claude Code            | BACH
  ----------------------|------------------------|-------------------------
  Architektur           | System-zentrisch       | LLM-zentrisch
  Kontrolle             | CLI steuert LLM        | LLM steuert Injektoren
  User-Kontrolle        | Keine (ausser Hooks)   | Voll (toggle on/off)
  LLM-Kontrolle         | Keine                  | Voll (an/abschalten)
  Cooldown-Management   | Turn-basiert (starr)   | Zeit-basiert (flexibel)
  Anzahl Typen          | 52                     | 5 (mit Teilfunktionen)
  Geheimhaltung         | 4 Typen mit "NEVER"    | Keine (transparent)
  Trigger               | Turn-Count             | Keywords + Zeit + Events
  DB-Integration        | Keine                  | 900+ dynamische Trigger
  Self-Extension        | Nicht moeglich         | Via context_triggers DB
  Open Source            | cli.js (minifiziert)   | Voll lesbar (Python)

WESENTLICHE UNTERSCHIEDE:

  1. TRANSPARENZ: BACH informiert offen, Claude Code versteckt aktiv
  2. KONTROLLE: BACH-Injektoren sind vom LLM steuerbar, Claude Codes nicht
  3. FLEXIBILITAET: BACH hat dynamische DB-Trigger, Claude Code hat Hardcoded-Konstanten
  4. COOLDOWNS: BACH nutzt Zeitbasiert (min), Claude Code nutzt Turns (starr)

POTENTIAL: MESSAGING-SYSTEM
----------------------------
Die Injektions-Infrastruktur koennte fuer Inter-Instanz-Kommunikation
genutzt werden:

  1. HOOKS (einfachster Weg):
     hook_additional_context bei UserPromptSubmit --
     liest Nachricht aus Datei und injiziert als Kontext.
     Kein Source-Patching noetig.

  2. NESTED MEMORY:
     Dateien im Memory-Ordner werden automatisch injiziert.
     Aenderung von aussen = Nachricht ans LLM.
     Einschraenkung: Nur bei Session-Start oder CLAUDE.md/MEMORY.md Aenderungen.

  3. CRITICAL_SYSTEM_REMINDER:
     Generischer Typ fuer beliebige Nachrichten.
     Muesste programmatisch getriggert werden (Source-Patch).

  4. TEAM MAILBOX:
     Bereits vorhandenes Messaging fuer Teams.
     Nur im Team-Modus aktiv (l8() Check).

EMPFEHLUNG: Hook-basierter Ansatz ist am praktikabelsten.
Ein UserPromptSubmit-Hook koennte eine "Inbox"-Datei pruefen und
Nachrichten als hook_additional_context injizieren.

EXPERIMENTELLE ERGEBNISSE (Session 2026-02-17)
-----------------------------------------------
Systematischer Test mit 14+ Nachrichten:

  - Task-Nudge erscheint nicht strikt alle 10 Nachrichten, weil
    Tool-Calls als eigene Turns zaehlen
  - Keyword-Trigger fuer Task-Nudge: WIDERLEGT (reines Turn-Counting)
  - User-Nachrichtenlaenge: kein Einfluss auf Trigger
  - Eigene (LLM) Outputs triggern keine Nudges
  - Muster: Nudges haeufen sich nach Tool-intensiven Runden
    (weil mehr Turns = schneller bei 10)

DATEIEN
-------
  Reverse-Engineering Quelle:
    C:\Users\User\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\cli.js
    (11.5 MB, minifiziert, Version 2.1.44)

  Analyse-Ergebnisse:
    ~/.claude/projects/C--Users-User/memory/claude-code-injections-anatomy.md
    ~/.claude/projects/C--Users-User/memory/system-injections.log

SIEHE AUCH
----------
  injectors.txt                BACH Injektor-System (5 Injektoren)
  claude-code.txt              Claude Code Kurzreferenz
  claude-code-automatisierung.txt  Claude Code Automatisierung
  memory.txt                   Memory-System
  partner.txt                  Partner-Infrastruktur


## Claude Code

CLAUDE CODE - KURZREFERENZ
==========================

Claude Code ist das offizielle CLI-Tool von Anthropic fuer Claude.
Aktuell: Version 2.1.37+ (Stand Feb 2026)

INSTALLATION (EMPFOHLEN: Native, NICHT npm!)
---------------------------------------------
  # Windows PowerShell
  irm https://claude.ai/install.ps1 | iex

  # macOS/Linux/WSL
  curl -fsSL https://claude.ai/install.sh | bash

  # Alternativ: Homebrew
  brew install --cask claude-code

  # Alternativ: WinGet
  winget install Anthropic.ClaudeCode

  # VERALTET (nicht empfohlen):
  npm install -g @anthropic-ai/claude-code

STARTEN
-------
  claude                   # Interaktive Session starten
  claude .                 # Im aktuellen Verzeichnis starten
  claude "Prompt"          # Mit Prompt starten
  claude -c                # Letzte Session fortsetzen
  claude -r                # Session auswaehlen zum Fortsetzen
  claude -p "query"        # Non-interaktiv (SDK-Mode, dann Exit)

WICHTIGE KOMMANDOS
------------------
  claude update            Updates installieren
  claude doctor            Installation pruefen
  claude mcp               MCP-Server konfigurieren
  claude install           Zu Native-Installation migrieren
  claude setup-token       Auth-Token einrichten

MODELLE (Stand 2026)
--------------------
  --model default          Je nach Account (Pro/Max/Teams: Opus 4.6)
  --model sonnet           Claude Sonnet 4.5 (schnell, taegliche Tasks)
  --model opus             Claude Opus 4.6 (komplex, beste Reasoning)
  --model haiku            Claude Haiku (schnellstes, guenstigstes)
  --model sonnet[1m]       Sonnet mit 1M Token Context
  --model opusplan         Opus fuer Plan-Mode, Sonnet fuer Execution

  Effort Level (Opus 4.6): low, medium, high (Standard)
  Env: CLAUDE_CODE_EFFORT_LEVEL=low|medium|high

WICHTIGE OPTIONEN (Auswahl - 50+ verfuegbar!)
----------------------------------------------
  -c, --continue           Letzte Session fortsetzen
  -r, --resume [id]        Session per ID/Name fortsetzen
  -p, --print              Ausgabe drucken und beenden (fuer Pipes)
  --model <alias|name>     Modell waehlen
  --add-dir <dir>          Zusaetzliche Verzeichnisse erlauben
  --system-prompt "..."    System-Prompt ERSETZEN
  --append-system-prompt "..." System-Prompt ERWEITERN (empfohlen!)
  --tools "Bash,Edit,Read" Nur bestimmte Tools aktivieren
  --allowedTools "..."     Tools ohne Permission-Prompt
  --disallowedTools "..."  Tools verbieten
  --permission-mode <mode> Plan/acceptEdits/default
  --dangerously-skip-permissions  Alle Prompts ueberspringen (ACHTUNG!)
  --output-format json     JSON Output (text/json/stream-json)
  --max-turns N            Max. agentic Turns (print mode)
  --max-budget-usd N       Max. Dollar fuer API Calls
  --chrome                 Chrome Browser Integration
  --ide                    Auto-Connect zu IDE
  --verbose                Verbose Logging
  --debug "api,mcp"        Debug-Mode mit Kategorien
  --mcp-config <file>      MCP-Server aus JSON laden
  --agents '{...}'         Custom Subagents definieren
  --fork-session           Neue Session-ID beim Resume
  --from-pr N              Sessions von GitHub PR N
  --remote "task"          Web-Session auf claude.ai starten
  --teleport               Web-Session lokal fortsetzen

PERMISSIONS
-----------
  --permission-mode <mode>
    default                Standard (fragt nach)
    acceptEdits            Edits automatisch akzeptieren
    plan                   Nur Plan-Modus

  --dangerously-skip-permissions  ALLE Prompts umgehen (Vorsicht!)
  --allow-dangerously-skip-permissions  Bypass erlauben (nicht aktivieren)

AUSGABEFORMATE (mit -p)
-----------------------
  --output-format text           Text (Standard)
  --output-format json           JSON (einzelnes Ergebnis)
  --output-format stream-json    Echtzeit-Streaming
  --include-partial-messages     Partial Events (mit stream-json)

SYSTEM-PROMPT FLAGS
-------------------
  --system-prompt "..."              ERSETZT gesamten Default-Prompt
  --system-prompt-file <file>        ERSETZT mit Datei (print mode only)
  --append-system-prompt "..."       ERWEITERT Default-Prompt (empfohlen!)
  --append-system-prompt-file <file> ERWEITERT mit Datei (print mode)

  Faustregel: --append-* bevorzugen (behaelt Claude Code Faehigkeiten)

SUBAGENTS (--agents Flag)
-------------------------
  JSON-Format fuer Custom Subagents:
  --agents '{
    "reviewer": {
      "description": "Code reviewer",
      "prompt": "You are a senior code reviewer...",
      "tools": ["Read", "Grep", "Glob"],
      "model": "sonnet"
    }
  }'

UMGEBUNGSVARIABLEN (Auswahl)
-----------------------------
  ANTHROPIC_MODEL=<alias|name>       Default-Modell
  ANTHROPIC_DEFAULT_OPUS_MODEL=...   Opus Alias Mapping
  ANTHROPIC_DEFAULT_SONNET_MODEL=... Sonnet Alias Mapping
  ANTHROPIC_DEFAULT_HAIKU_MODEL=...  Haiku Alias Mapping
  CLAUDE_CODE_SUBAGENT_MODEL=...     Subagent-Modell
  CLAUDE_CODE_EFFORT_LEVEL=low|med|high  Opus Effort
  DISABLE_PROMPT_CACHING=1           Prompt Caching global aus
  DISABLE_AUTOUPDATER=1              Auto-Updates deaktivieren
  CLAUDE_CODE_GIT_BASH_PATH=...      Git Bash Pfad (Windows)

BEISPIELE
---------
  # Interaktiv im BACH-Verzeichnis
  cd "C:\Users\User\OneDrive\KI&AI\BACH_v2_vanilla"
  claude

  # Mit Opus 4.6 und Extended Context
  claude --model opus[1m]

  # Letzte Session fortsetzen
  claude -c

  # Non-interaktiv (fuer Scripts)
  claude -p "Liste alle Python-Dateien auf"

  # Mit zusaetzlichem Verzeichnis
  claude --add-dir "C:\MeinProjekt"

  # Custom System Prompt (erweitert, nicht ersetzt)
  claude --append-system-prompt "Nutze TypeScript, keine any-Types"

  # Opus fuer Planning, Sonnet fuer Execution
  claude --model opusplan

  # JSON Output fuer Scripting
  claude -p --output-format json "Finde alle TODOs"

  # Mit MCP-Server Config
  claude --mcp-config ./mcp.json

  # Chrome-Integration
  claude --chrome

  # Max Budget limitieren
  claude -p --max-budget-usd 5.00 "Grosse Analyse"

AUTHENTICATION
--------------
  1. Claude Pro/Max (empfohlen): Login via claude.ai Account
  2. Claude Console: OAuth via console.anthropic.com
  3. Teams/Enterprise: Team-Login via claude.ai
  4. Cloud Provider: Bedrock/Vertex/Foundry Config

AUTO-UPDATES
------------
  Native Installation: Auto-Update alle paar Stunden (im Hintergrund)
  Homebrew/WinGet: Manuell mit `brew upgrade` / `winget upgrade`

  Release Channels:
    - latest (Standard, neue Features sofort)
    - stable (~1 Woche alt, Skip bei Regressions)

  Config: /config → Auto-update channel
  Oder: settings.json → "autoUpdatesChannel": "stable"

SIEHE AUCH
----------
  https://code.claude.com/docs/en/cli-reference  Vollstaendige CLI-Referenz
  https://code.claude.com/docs/en/setup          Setup & Installation
  wiki/claude-code.txt                      BACH Wiki (falls vorhanden)
  wiki/gemini.txt                           Gemini CLI/Antigravity
  wiki/ollama.txt                           Lokale LLMs

QUELLEN (Stand 2026-02-08)
--------------------------
  - https://code.claude.com/docs/en/cli-reference
  - https://code.claude.com/docs/en/setup
  - https://code.claude.com/docs/en/model-config
  - https://www.npmjs.com/package/@anthropic-ai/claude-code
  - https://github.com/anthropics/claude-code


## Cli

CLI-KONVENTIONEN (v2.0 Registry-Based)
=======================================

ARCHITEKTUR:
----------------------------------------
BACH nutzt Auto-Discovery via core/registry.py:
- Handler in hub/*.py werden automatisch gefunden
- Keine statische Handler-Map mehr (wie in v1.x)
- Routing-Reihenfolge: --handler → Inline Commands → skill export →
  restore backup → Registry → Tool-Fallback

STANDARD-PATTERN (wie git, npm, docker):
  bach SUBCOMMAND [args]     Aktion ausfuehren
  bach --HANDLER [args]      Handler mit -- Prefix

ZWEI ZUGRIFFSWEGE:
----------------------------------------
1. CLI (fuer Menschen):
   python bach.py task list

2. Library-API (fuer LLM/Scripts - BEVORZUGT):
   from bach_api import task
   task.list()

KERN-SUBCOMMANDS (Verwaltung):
----------------------------------------
  task      Task-Verwaltung (add, list, done, block, next)
  mem       Working Memory (write, read, status, archive)
  memory    Erweiterter Memory-Handler (facts, lessons, archive)
  msg       Nachrichtensystem (send, list, read, ping)
  lesson    Lessons Learned (add, list, search, archive)
  backup    Sicherung der Datenbanken
  restore   Wiederherstellung aus Backup
  dist      Distributionen & Release-Management
  partner   Partner-Netzwerk (Koordination Claude/Gemini/Ollama)
  session   Session-Management & Zusammenfassungen

AGENTEN & EXPERTEN (Fachgebiete):
----------------------------------------
  steuer        Steuer-Experte (Finanzamt, Fristen, Belege)
  ati           ATI-Agent (Konzept-Entwicklung)
  abo           Abo-Service (Kuendigungen, Vertraege)
  bericht       Bericht-Generator (Foerderberichte ICF)
  gesundheit    Gesundheits-Assistent
  haushalt      Haushalts-Management
  versicherung  Versicherungs-Management

SERVICES & INFRASTRUKTUR:
----------------------------------------
  gui           Dashboard Steuerung (start, stop, status)
  daemon        Hintergrund-Service fuer Wartung
  scan          Input-Scanner (Inbox, OCR)
  connector     Connector-Verwaltung (poll, dispatch, setup-daemon)
  mount         Einbinden externer Ressourcen
  chain         Toolchain-Engine (Automatisierung)
  routine       Routine-Management (Morgen/Abend/Projekt-Start)
  recurring     Wiederkehrende Aufgaben

SELBSTERWEITERUNG & HOOKS:
----------------------------------------
  skills create <name> --type <typ>   Neue Faehigkeit scaffolden
                                       Typen: tool, agent, expert, handler, service
  skills reload                        Hot-Reload (Registry + Tools + Skills)
  hooks status                         Status aller Hooks und Listener
  hooks events                         Alle Events auflisten
  hooks log                            Letzte Hook-Ausfuehrungen
  hooks test <event>                   Test-Event emittieren
  plugins list                         Geladene Plugins anzeigen
  plugins load <pfad>                  Plugin aus plugin.json laden
  plugins unload <name>                Plugin entladen
  plugins create <name>                Plugin-Manifest scaffolden
  plugins tools                        Alle Plugin-Tools anzeigen

SYSTEM-WERKZEUGE:
----------------------------------------
  wiki          Wissensdatenbank (wiki/)
  tools         Management interner Skripte
  tuev          Validierungs- & Test-System
  usecase       Test-Cases (Teil von tuev)
  clock         Zeit-System (now, format, parse)
  timer         Timer starten/stoppen
  countdown     Countdown erstellen
  beat          Unified Zeit-Anzeige (Clock, Timer, Countdown, Between)
  between       Zeit zwischen zwei Zeitpunkten
  maintain      Wartungs-Funktionen (db optimize, logs clean)
  test          Test-Runner (smoke, integration, full)

HANDLER MIT -- (erweiterte Funktionen):
----------------------------------------
  --startup         Session starten (Initialisierung, --watch fuer Polling)
  --shutdown        Session beenden (Cleanup)
  --status          Gesamt-Status des Systems
  --help [topic]    Hilfe zu Themen/Modulen anzeigen
  --memory          Detaillierter Memory-Handler (facts, lessons)
  --db              Datenbank-Analyse (bach.db Schema/Stats)
  --tokens          Token-Kosten Kontrolle
  --inject          Injektor-System fuer Tools
  --context         Kontext-Loader fuer Sessions
  --logs            System-Log Analyse (data/logs/)
  --docs            Doku-Integrity-Check
  --snapshot        Systemzustand einfrieren
  --trash           Papierkorb & Wiederherstellung
  --fs              Filesystem-Protection (check, heal, status)
  --connections     Connections & Actors-Model

INLINE COMMANDS (tools-basiert, kein Handler):
----------------------------------------
  fs            Filesystem-Protection (check, heal, classify, scan)
  file          File-Manager (read, write, copy, move, delete)
  ocr           OCR-Engine (Beleg-ID oder PDF-Pfad)
  llm           Multi-LLM Protocol (--partner=<name>)
  map           Call-Graph / Dependency-Mapper

SPEZIALFAELLE:
----------------------------------------
  skill export  Skill-Export mit Dependency Resolution
  restore backup <file>  Backup wiederherstellen

BEIDE VARIANTEN AKZEPTIERT:
----------------------------------------
Aus historischen Gruenden funktionieren diese oft hybrid:
  bach partner list     = bach --partner list
  bach gui start        = bach --gui start

DID-YOU-MEAN (Fuzzy-Matching):
----------------------------------------
Bei Tippfehlern schlaegt BACH aehnliche Befehle vor (Levenshtein ≤2):
  $ bach parner list → "Meintest du: partner?"
  $ bach taks add    → "Meintest du: task?"

TOOL-FALLBACK:
----------------------------------------
Wenn kein Handler gefunden wird, versucht BACH ein Tool aus tools/:
  bach skill_export  → tools/skill_export.py
  bach backup_manager → tools/backup_manager.py

REGISTRIERTE HANDLER (Stand 2026-02-13):
----------------------------------------
75+ Handler via Auto-Discovery (hub/*.py):
abo, agents, ati, backup, beat, bericht, between, calendar, chain, clock,
connections, connector, consolidation, contact, context, countdown, cv,
daemon, data, db, dist, doc, docs, email, extensions, fs, gesundheit, gui,
haushalt, healthcheck, help, hooks, inject, lang, lesson, logs, maintain,
mem, memory, mount, msg, notify, obsidian, ollama, partner, path, profile,
profiler, recurring, reflection, routine, scan, session, shutdown, skill,
skills, smarthome, snapshot, sources, startup, status, steuer, sync, task,
test, timer, tokens, tool, tools, trash, tuev, update, usecase,
versicherung, wiki

SIEHE AUCH:
----------------------------------------
  help practices      Regelwerk-Index
  help naming         Namenskonventionen
  help coding         Coding-Standards
  help actors         Actors-Model (Connections)
  help partners       Partner-Profile
  help hooks          Hook-Framework (14 Events)
  help self-extension Selbsterweiterungs-System


## Clock

CLOCK - Uhrzeit-Anzeige
=======================

Zeigt die aktuelle Uhrzeit bei CLI-Ausgaben an.

CLI-BEFEHLE
-----------

  bach clock on              Uhrzeit-Anzeige aktivieren
  bach clock off             Uhrzeit-Anzeige deaktivieren
  bach clock status          Aktuellen Status zeigen
  bach clock interval <sek>  Intervall in Sekunden setzen

INTERVALL
---------

  interval 0    Uhrzeit bei JEDER Ausgabe
  interval 60   Uhrzeit nur wenn >= 60 Sekunden seit letzter Anzeige
  interval 300  Uhrzeit alle 5 Minuten

AUSGABE-FORMAT
--------------

  [CLOCK] 14:35

PERSISTENZ
----------

  Datei: data/.clock_state

  Inhalt:
  {
    "enabled": true,
    "interval": 60,
    "last_shown": "2026-01-30T14:35:00"
  }

BEISPIELE
---------

  # Uhrzeit bei jeder Ausgabe
  bach clock on
  bach clock interval 0

  # Uhrzeit alle 5 Minuten
  bach clock interval 300

  # Status pruefen
  bach clock status
  -> Clock: AN | Intervall: 60s | Letzte: 14:35

ZUSAMMENSPIEL
-------------

Clock ist Teil des Zeit-Systems:
  --help timer      Stoppuhr
  --help countdown  Countdown mit Trigger
  --help between    Between-Checks
  --help beat       Unified Zeit-Anzeige

Alle Zeit-Funktionen werden via `bach beat` zusammengefasst.

---
Version: 1.0 | Status: Implementiert (v1.1.83)
Siehe: docs/CONCEPT_time_system.md


## Coding

CODING-STANDARDS
================

1. PFADE
   - Relative Pfade sind Goldstandard
   - Keine hardcoded C:\Users\...
   - Path(__file__).parent nutzen
   - Bei Pfad-Fragen: --help bach_paths

2. ENCODING
   - UTF-8 EVERYWHERE
   - IMMER encoding='utf-8' angeben
   - Nie auf System-Default verlassen
   
   Richtig:
     content = Path("file.txt").read_text(encoding="utf-8")
     with open("file.txt", "w", encoding="utf-8") as f:

3. CONSOLE
   - Keine Emojis in print()
   - Stattdessen: [INFO], [OK], [ERROR], [WARN]
   - Console-Fix wenn noetig:
     sys.stdout.reconfigure(encoding='utf-8', errors='replace')

4. EMOJIS
   - Erlaubt in Dateien, aber nur registrierte!
   - Registry: system/tools/c_emoji_scanner.py (ASCII_OVERRIDES)
   - Scanner: bach c_emoji_scanner <datei>

5. JSON-BEARBEITUNG
   - ERSTE WAHL: bach.py oder Python-Script
   - NIE fc_str_replace fuer JSON
   - NIE PowerShell fuer JSON
   - Bei Problemen: bach c_json_repair <datei>

6. IMPORTS
   - Standard-Library zuerst
   - Dann Third-Party
   - Dann lokale Module
   - Tool: bach c_import_organizer <datei>


## Communicate

COMMUNICATE - Partner-Kommunikationssystem
==========================================

STAND: 2026-02-08

Das Kommunikationssystem (Schicht 4) verwaltet den Informationsaustausch
zwischen allen Instanzen (Mensch & KIs).

KERNKONZEPTE
------------
1. MESSAGING: Persistentes Nachrichten-Routing in der DB.
2. PROTOKOLLE: Standardisierte Abläufe (Handshake, Request, Transfer).
3. WORKSPACES: Physische Verzeichnisse für Dateiaustausch (system/partners/).
4. PRESENCE: Aktiver Online-Status und Watch-Mechanismen.

REGISTRIERTE PARTNER (10)
-------------------------
Internal System:
  user      User (Lukas)           [✓ Active]
  claude    Claude (Opus 4.6)      [✓ Active]
  bach      BACH Core System       [✓ Active]

Local AI:
  ollama    Mistral 7B             [✓ Active]
  llama     Llama 3 8B             [✓ Active]

External AI:
  gemini    Google Gemini          [✓ Active]
  gpt       OpenAI GPT             [○ Inactive]

APIs:
  pubmed    PubMed MCP             [✓ Active]

Services:
  drive     Google Drive           [✓ Active]

Tools:
  canva     Canva MCP              [✓ Active]

PARTNER-ERKENNUNG
-----------------
Keywords loesen automatisch Partner-Auswahl aus:

  ollama:       bulk, embedding, token-free, draft email
  pubmed:       gene, protein, disease, clinical, biomedical
  google_drive: google drive, find document, search drive
  canva:        design, presentation, poster, infographic
  gemini:       deep research, long document, concept analysis

ROUTING-KANAELE
---------------
| Partner | Kanaele | Status |
|---------|---------|--------|
| ollama | Direct API, Queue | ✓ |
| user | MessageBox | ✓ |
| pubmed | MCP Server | ✓ |
| canva | MCP Server | ✓ |
| google_drive | API | ✓ |
| gemini | partners/gemini/ | ✓ |

HEALTH-CHECKS
-------------
Ollama:       curl http://127.0.0.1:11434/api/tags
Google Drive: API Token-Check
PubMed:       MCP Connection Test
Canva:        MCP Connection Test

TOKEN-ZONEN (Delegation)
------------------------
Zone 1 (0-30%):   Alle Partner verfuegbar
Zone 2 (30-60%):  Guenstige Partner (Ollama bevorzugt)
Zone 3 (60-80%):  Nur lokale Partner
Zone 4 (80-100%): Nur Notfall (Human + Ollama)

CLI-BEFEHLE (bach msg)
----------------------
  list [--inbox/--outbox] [--limit N]  Alle Nachrichten anzeigen.
  unread                               Nur ungelesene Nachrichten.
  send <NAME> <TEXT> [--from SENDER]   Nachricht senden.
  read <ID> [--ack]                    Nachricht lesen und optional bestätigen.
  ping [--from NAME]                   Ungelesene AN Partner anzeigen.
  watch [--from NAME]                  Live-Polling (alle 10s prüfen).
  count                                Nachrichtenzähler anzeigen.
  delete <ID> [ID2...]                 Nachricht(en) löschen.
  archive <ID> [ID2...]                Nachricht(en) archivieren.

NACHRICHTEN-TYPEN
-----------------
- TASK: Aufträge an Partner (via `_TASKS.md` + `msg send`).
- INFO: Status-Updates und Reports (`outbox/`).
- ALERT: Fehler-Meldungen und Eskalationen (Problem-Monitor).

INTERAKTIONSPROTOKOLLE
----------------------
1. HANDSHAKE: Gegenseitige Erkennung und Funktions-Check (Health).
2. REQUEST: Formelle Anfrage für Daten oder Dienstleistung.
3. TRANSFER: Physische Übertragung via Workspace oder DB.
4. CONFIRM: Bestätigung des Empfangs und der Verarbeitung (Receipt).

DATENBANK-TABELLEN
------------------
connections         Partner-Endpoints und Tools
partner_recognition Partner-Capabilities und Zonen
delegation_rules    Token-basierte Delegation
messages            Nachrichtenprotokoll (genutzt von hub/messages.py)
comm_messages       Alternative Nachrichten-Tabelle (nicht aktiv genutzt)

PARTNER-WORKSPACES
------------------
Jeder Partner hat eine genormte Ordnerstruktur unter `system/partners/`:
  - inbox/      Eingehende Daten/Anfragen.
  - outbox/     Ergebnisse/Berichte.
  - workspace/  Temporärer Arbeitsbereich.

DAEMON & AUTOMATION
-------------------
Der Daemon-Job `msg-cleanup` archiviert gelesene Nachrichten nach 30 Tagen.
Partner wie Gemini nutzen `bach msg watch`, um in Echtzeit auf Claude zu reagieren.

HANDLER & TOOLS
---------------
hub/messages.py              Nachrichtensystem-CLI (542 Zeilen)
hub/partner.py               Partner-Verwaltung (514 Zeilen)
tools/partner_communication/ Tools für Partner-Interaktion:
  - interaction_protocol.py  Instanz-Kommunikation
  - system_explorer.py       Software-Erkennung
  - ai_compatible.py         AI-Kompatibilitätsschicht
  - communication.py         Kommunikations-Utilities

SIEHE AUCH
----------
  bach partner --help    Partner-Verwaltung und Delegation
  bach msg --help        Nachrichtensystem-Befehle
  docs/docs/docs/help/maintain.txt      Partner-Health Checks


## Connections

CONNECTIONS - Verbindungen & Integrationen (Uebersicht)
=======================================================

STAND: 2026-02-08

Das Connections-System ist die zentrale Datenbank-Tabelle fuer ALLE
technischen Verbindungen in BACH. Es gibt ZWEI verschiedene Subsysteme
mit unterschiedlichen Zwecken:

1. CONNECTOR-SYSTEM (NEU, v2.0)
--------------------------------
Externe Kommunikationsverbindungen (Telegram, Discord, HomeAssistant).
Vollstaendiges Message-System mit Queue, Retry, Circuit Breaker.

**DETAILS → siehe docs/docs/docs/help/connector.txt**

CLI: bach connector <operation>
Operationen: list, status, add, remove, poll, dispatch, setup-daemon, etc.

Handler: hub/connector.py
Services: hub/_services/connector/queue_processor.py
API: gui/api/messages_api.py (4 REST-Endpoints)

2. AI/MCP-CONNECTIONS (LEGACY)
-------------------------------
Technische Infrastruktur fuer AI-Partner und MCP-Server.
Verwaltet Endpoints, API-Keys, OAuth-Tokens.

CLI: bach --connections list/show
Handler: hub/connections.py (?)

Typen:
  - AI-Partner: claude, ollama, gemini (Anthropic, Local, Google)
  - MCP-Server: pubmed, canva, gdrive (Model Context Protocol)

WICHTIG: CONNECTIONS vs PARTNER vs CONNECTOR
--------------------------------------------
- CONNECTIONS (Tabelle):  Zentrale Registry ALLER Verbindungen
- CONNECTOR   (Subsystem): Externe Kommunikation (Telegram, Discord, ...)
- PARTNER     (Logik):     Delegation & Expertise (WER macht WAS?)

DATENBANK-TABELLE
-----------------
Tabelle: connections
Felder:
  - name, type, category, endpoint, is_active
  - auth_type, auth_config (JSON mit Credentials)
  - success_count, error_count, last_used
  - consecutive_failures, disabled_until (Circuit Breaker, nur Connectors)

Kategorien (category):
  - 'connector':  Externe Kommunikation (Telegram, Discord, ...)
  - 'ai':         AI-Partner (Claude, Ollama, Gemini)
  - 'mcp':        MCP-Server (PubMed, Canva, ...)
  - 'api':        Sonstige APIs

VERWENDUNG
----------
Die meisten Nutzer benoetigen NUR das **Connector-System**.

Fuer externe Kommunikation (Telegram, Discord, HomeAssistant):
  → bach connector --help
  → docs/docs/docs/help/connector.txt (dedizierte Dokumentation)

Fuer AI-Partner und MCP-Server:
  → bach --connections list
  → bach --help partner

SIEHE AUCH
----------
  docs/docs/docs/help/connector.txt     Connector-System (Telegram, Discord, HA)
  bach --help partner    Logische Delegation & Zonen
  bach --help messages   Internes Nachrichtensystem
  bach --help daemon     Hintergrund-Jobs (poll_and_route, dispatch)


## Connector

CONNECTOR - Externe Kommunikationsverbindungen
===============================================

BESCHREIBUNG
Verwaltet externe Kommunikationsverbindungen (Telegram, Discord,
HomeAssistant, etc.) und fuehrt sie aus. Unterstuetzt automatisches
Polling, Queue-Versand mit Retry/Backoff und Circuit Breaker.

UNTERSTUETZTE TYPEN
-------------------
  telegram        Telegram Bot API (getUpdates Polling)
  discord         Discord Bot (REST API)
  homeassistant   Home Assistant (REST API)
  webhook         Eingehende Webhooks (Push-basiert)
  signal          Signal Messenger (geplant, signal-cli)
  whatsapp        WhatsApp (geplant, Baileys)

Runtime-Adapter verfuegbar: telegram, discord, homeassistant

CLI-BEFEHLE
-----------

Verwaltung:
  bach connector list                    Alle Connectors anzeigen
  bach connector status                  Status + Statistiken
  bach connector add <type> <name> [url] Neuen Connector registrieren
  bach connector remove <name>           Connector entfernen
  bach connector enable <name>           Aktivieren
  bach connector disable <name>          Deaktivieren

Nachrichten:
  bach connector messages [name]         Nachrichten anzeigen
  bach connector unprocessed             Unverarbeitete Nachrichten
  bach connector route                   Nachrichten routen (inbox)
  bach connector send <name> <to> <text> In ausgehende Queue einreihen

Runtime:
  bach connector poll <name>             Einmal pollen (Nachrichten holen + speichern)
  bach connector dispatch <name>         Ausgehende Queue versenden

Queue-Management:
  bach connector setup-daemon            Daemon-Jobs registrieren (einmalig)
  bach connector queue-status            Queue-Statistiken (pending/failed/dead)
  bach connector retry <id|all>          Dead-Letter zuruecksetzen

ZUVERLAESSIGE ZUSTELLUNG (v2.0)
-------------------------------
Das Message-System arbeitet mit dem Daemon zusammen fuer
automatische Zustellung auch ohne aktive CLI-Session.

Einrichtung:
  1. bach connector setup-daemon       # Einmalig: 2 Daemon-Jobs anlegen
  2. bach daemon start --bg            # Daemon im Hintergrund starten

Ab jetzt automatisch:
  - Telegram/Discord alle 1-2 Min gepollt
  - Eingehende Nachrichten in Inbox (mit Kontext-Hints)
  - Ausgehende Queue jede Minute abgearbeitet
  - Fehlgeschlagene Sends bis 5x mit Backoff wiederholt

Daemon-Jobs:
  connector_poll_and_route   (2 Min Intervall) Pollt und routet
  connector_dispatch         (1 Min Intervall) Versendet Queue

RETRY UND BACKOFF
-----------------
Fehlgeschlagene Nachrichten werden mit exponentiellem Backoff
wiederholt: 30s, 60s, 120s, 240s, 480s (~15 Minuten gesamt).

Nach 5 Fehlversuchen (konfigurierbar) wird die Nachricht als
"Dead Letter" markiert. Dead Letters koennen manuell
zurueckgesetzt werden:

  bach connector retry all             Alle Dead Letters zuruecksetzen
  bach connector retry 42              Einzelne Nachricht zuruecksetzen

CIRCUIT BREAKER
---------------
Nach 5 aufeinanderfolgenden Fehlern wird ein Connector fuer
5 Minuten gesperrt (disabled_until). Weitere Sende-/Poll-Versuche
werden uebersprungen bis der Cooldown abgelaufen ist. Danach
wird der Zaehler automatisch zurueckgesetzt.

KONTEXT-INTEGRATION
-------------------
Eingehende Nachrichten werden beim Routing durch zwei
Trigger-Systeme gefiltert (Assoziatives Gedaechtnis):

  a) ContextInjector (hardcoded, ~100 Trigger)
     → injector_hint in messages.metadata

  b) context_triggers Tabelle (dynamisch, 900+ Trigger)
     → context_triggers in messages.metadata

Ergebnis in messages.metadata (JSON):
  {
    "source": "telegram:123456",
    "injector_hint": "[KONTEXT] Backup: bach backup create ...",
    "context_triggers": ["backup", "sicherung"],
    "routed_at": "2026-02-08T22:00:00"
  }

REST-API
--------
Verfuegbar wenn Headless API laeuft (Port 8001):

  POST /api/v1/messages/send      Nachricht in Queue einreihen
  GET  /api/v1/messages/queue     Queue-Status (pending/failed/dead)
  GET  /api/v1/messages/inbox     Inbox lesen (Paginierung, Filter)
  POST /api/v1/messages/route     Routing manuell ausloesen

Beispiele:
  curl localhost:8001/api/v1/messages/queue
  curl -X POST localhost:8001/api/v1/messages/send \
    -H "Content-Type: application/json" \
    -d '{"connector":"telegram_main","recipient":"123","content":"Hallo"}'

POLL-INTERVALLE (Default)
-------------------------
  Typ              Intervall   Rationale
  telegram         60s         getUpdates ist guenstig
  discord          120s        REST-Polling, Rate-Limits
  homeassistant    300s        Events, weniger dringend
  webhook          N/A         Push-basiert, kein Polling

Ueberschreibbar per auth_config JSON: {"poll_interval": 30}

DATENBANK
---------
Tabellen:
  connections         Connector-Konfiguration + Circuit-Breaker-Status
  connector_messages  Nachrichten-Queue (ein-/ausgehend, Retry-Tracking)
  messages            Inbox/Outbox (geroutete Nachrichten)
  daemon_jobs         Automatische Poll/Dispatch-Jobs

Relevante Spalten connector_messages:
  status          TEXT (pending/sent/failed/dead)
  retry_count     INTEGER (aktuelle Versuchsnummer)
  max_retries     INTEGER (Default 5)
  next_retry_at   TEXT (naechster Retry-Zeitpunkt)

Relevante Spalten connections:
  consecutive_failures  INTEGER (Circuit-Breaker-Zaehler)
  disabled_until        TEXT (Sperre bis Timestamp)

DATEIEN
-------
  hub/connector.py                           CLI-Handler
  hub/_services/connector/queue_processor.py Queue-Processor (Kern)
  gui/api/messages_api.py                    REST-API Router
  connectors/base.py                 Abstrakte Basisklasse
  connectors/telegram_connector.py   Telegram-Adapter
  connectors/discord_connector.py    Discord-Adapter
  connectors/homeassistant_connector.py  HA-Adapter
  db/migrations/001_connector_queue_upgrade.sql  Schema-Migration

SIEHE AUCH
----------
  bach --help messages        Internes Nachrichtensystem
  bach --help daemon          Hintergrund-Jobs
  bach --help injectors       Kontext-Injektoren


## Consolidation

MEMORY-KONSOLIDIERUNG
=====================

STAND: 2026-02-08

WAS IST KONSOLIDIERUNG?
-----------------------
Konsolidierung ist der aktive Prozess, der aus Rohdaten (Sessions, Lessons,
Working Memory) Sinnstrukturen schafft und in Kontext überführt. 

Analog zum menschlichen Schlaf:
- Erlebnisse werden verarbeitet, Wichtiges behalten.
- Wiederholung stärkt Verbindungen (Boost), Ungenutztes verblasst (Decay).
- Zusammenfassung reduziert Details, behält die Essenz.

KONSOLIDIERUNGS-EBENEN (Pipeline)
---------------------------------

  ROHDATEN (Sessions, Working Mem) --[Analyse]--> ASM (Metadaten)
  ASM (Metadaten) --[KI-Review]--> ESSENZ (Lessons, Context)
  ESSENZ --[Indexierung]--> TRIGGER-DB (Assoziatives Gedächtnis)

TABELLEN (v1.1.80+ Aktiv)
-------------------------
  memory_sessions      Rohdaten (360+ Einträge)
  memory_lessons       Gereinigte Erkenntnisse (70+ Einträge)
  memory_consolidation Tracking & Scores (350+ Einträge)
  context_triggers     Assoziative Brücken (900+ Triggers)

CLI-BEFEHLE (bach consolidate)
------------------------------
  status       Zeigt Statistiken und fällige Konsolidierungen.
  run          Führt alle verfügbaren Konsolidierungs-Schritte aus (weight, archive, index, sync-triggers, forget).
  compress     Kompression von Sessions zu Context-Einträgen.
               --cleanup: Leere Sessions aufräumen
               --batch: Sessions nach Tag gruppieren
               --run: Vollständige Komprimierung mit Regelwerk
  weight       Aktualisierung der Relevanz-Scores (Decay/Boost).
  archive      Verschieben von veraltetem Wissen in das Langzeit-Archiv.
  index        Abgleich zwischen Fakten, Help und Wiki.
  review       Erstellt Review-Tasks für manuelle Validierung.
  init         Tracking für existierende Einträge initialisieren.
  sync-triggers Dynamische Kontext-Trigger aktualisieren (NEU v1.1.80).
  forget       Ungenutzte Einträge löschen (weight < threshold).
  reclassify   Falsch kategorisierte Einträge korrigieren (NEU v1.1.81).

DAEMON-INTEGRATION
------------------
Die Konsolidierung kann als Hintergrund-Job laufen (daemon_jobs):
- `consolidate-weight`: Täglich (Decay-Simulation).
- `consolidate-archive`: Wöchentlich (Archiv-Prüfung).
- `consolidate-index`: Facts-Index aktualisieren.

(Hinweis: Daemon-Jobs müssen konfiguriert werden - siehe docs/docs/docs/help/daemon.txt)

TRUTHFULNESS:
Jeder Konsolidierungslauf erzeugt Log-Einträge und bei Zweifeln 
Review-Tasks (#category: maintenance).

SIEHE AUCH
----------
  docs/docs/docs/help/memory.txt          Kognitives Gedaechtnis Modell
  docs/docs/docs/help/lessons.txt         Best Practices & Erkenntnisse
  docs/docs/docs/help/daemon.txt          Daemon-Jobs
  hub/consolidation.py     Implementation der Logik
  ARCHITECTURE.md          System-Architektur (Memory-Modell)

TEILPROZESSE (BEREITS VORHANDEN)
--------------------------------
Diese existierenden Tools sind Teil der Konsolidierung:

  tools/autolog_analyzer.py     Session-Analyse (ASM_003)
  tools/context_compressor.py   Komprimierung (ASM_004/005)
  skills/workflows/wiki-*      Wiki-Autoren
  skills/workflows/help-*      Help-Autoren

DATENBANK-SCHEMA
----------------
memory_consolidation (AKTIV, 350+ Eintraege):

  id                INTEGER PRIMARY KEY
  source_table      TEXT        -- memory_sessions, memory_lessons, etc.
  source_id         INTEGER     -- ID in Quelltabelle
  times_accessed    INTEGER     -- Abruf-Zaehler
  last_accessed     TIMESTAMP   -- Letzter Abruf
  weight            REAL        -- Relevanz-Score (0.0-1.0)
  decay_rate        REAL        -- Verfalls-Rate
  threshold         REAL        -- Archivierungs-Schwelle
  status            TEXT        -- active, archived, deleted
  consolidated_to   INTEGER     -- ID in memory_context (wenn konsolidiert)
  created_at        TIMESTAMP
  updated_at        TIMESTAMP

WORKFLOW: SESSION -> KONTEXT
----------------------------
1. Session endet (--shutdown)
2. autolog_analyzer.py extrahiert Aktivitaeten
3. context_compressor.py erstellt Zusammenfassung
4. Zusammenfassung in memory_sessions gespeichert
5. [DAEMON] Nach X Sessions: Komprimierung zu Context
6. [KI-REVIEW] Prueft Sinnstruktur, korrigiert
7. Ergebnis in memory_context mit Triggern

WORKFLOW: FACT -> WIKI/HELP
---------------------------
1. Neuer Fact wird erstellt: bach --memory fact "thema:wert"
2. consolidate-index prueft: Existiert Help/Wiki zu "thema"?
3. Falls nein: Task erstellen "Wiki-Eintrag zu [thema] erstellen"
4. Wiki-Autor erstellt Eintrag
5. Fact wird aktualisiert mit Pfad-Verweis

WORKFLOW: WIKI/HELP -> FACTS INDEX
----------------------------------
1. consolidate-index scannt docs/docs/docs/help/*.txt und wiki/*.txt
2. Fuer jeden Eintrag: Existiert Fact?
3. Falls nein: Fact erstellen als Index
   HELP.memory -> "Memory-System Dokumentation"
   WIKI.gemini -> "Google Gemini KI-Modelle"
4. Facts dienen als schneller Lookup

SCHWELLENWERTE (KONFIGURIERBAR)
-------------------------------
  weight_threshold_archive: 0.2   Unter diesem Wert: Archivieren
  weight_threshold_delete:  0.05  Unter diesem Wert: Loeschen
  decay_rate_default:       0.95  Taeglicher Verfall (5%)
  boost_on_access:          0.1   Gewichts-Erhoehung bei Abruf
  sessions_before_compress: 10    Sessions bis Komprimierung
  days_before_archive:      90    Tage bis Archivierung

NEUE OPERATIONEN (v1.1.80+)
---------------------------
  sync-triggers    Aktualisiert dynamische Trigger aus:
                   - workflow_trigger_generator.py
                   - lesson_trigger_generator.py
                   - tool_auto_discovery.py
                   - theme_packet_generator.py
                   - trigger_maintainer.py

  forget           Deaktiviert/loescht Eintraege mit weight < 0.05
                   - memory_lessons: is_active = 0
                   - memory_working: is_active = 0
                   - memory_facts: DELETE

  reclassify       Korrigiert falsche Kategorisierungen:
                   - Lesson -> Context (bei hoher Nutzung)
                   - Working -> Lesson (bei Lesson-Pattern)
                   - Working -> Fact (bei Key:Value Format)
                   - Fact ohne Wiki -> Task erstellen

                   Manuelle Konvertierung:
                     bach consolidate reclassify lesson 42 context

                   Automatische Analyse:
                     bach consolidate reclassify
                     bach consolidate reclassify --fix


## Contact

CONTACT - Kontaktverwaltung
===========================

BESCHREIBUNG:
  Verwaltet persoenliche und geschaeftliche Kontakte mit Freitextsuche,
  Kontext-Filterung und Geburtstags-Uebersicht. Kontakte werden per
  Soft-Delete deaktiviert (nicht geloescht).

BEFEHLE:
  bach contact list              Alle aktiven Kontakte anzeigen
  bach contact list --all        Inkl. inaktive Kontakte
  bach contact list -c privat    Nach Kontext filtern
  bach contact search <term>     Freitextsuche (Name, Email, Telefon, Firma, Notizen, Tags)
  bach contact add "Name"        Neuen Kontakt anlegen
  bach contact show <id>         Kontakt-Details anzeigen
  bach contact edit <id>         Kontakt bearbeiten
  bach contact delete <id>       Kontakt deaktivieren (Soft-Delete)
  bach contact birthday          Geburtstage (naechste 30 Tage)
  bach contact birthday 90       Geburtstage (naechste 90 Tage)
  bach contact export            Alle Kontakte exportieren (Text/CSV/vCard)
  bach contact export --type arzt --format csv  Arzt-Kontakte als CSV
  bach contact export --format vcard --file out.vcf  vCard-Export in Datei
  bach contact help              Diese Hilfe

OPTIONEN FUER ADD/EDIT:
  --context, -c   Kontext (privat|beruflich|versicherung|finanzen|arzt|sonstige)
  --email, -e     E-Mail-Adresse
  --phone, -p     Telefon (Festnetz)
  --mobile, -m    Mobilnummer
  --address, -a   Adresse
  --birthday, -b  Geburtstag (DD.MM.YYYY oder YYYY-MM-DD)
  --company       Firma/Organisation
  --position      Position/Rolle im Unternehmen
  --tags          Tags kommagetrennt (z.B. "dev,it,freelance")
  --note          Notiz (bei edit: wird an bestehende Notizen angehaengt)
  --name          Name aendern (nur bei edit)

OPTIONEN FUER EXPORT:
  --type, -t      Nur bestimmten Kontext exportieren (arzt, privat, etc.)
  --format, -f    Exportformat: txt (default), csv, vcard
  --file, -o      Ausgabedatei (sonst Konsolen-Output)

KONTEXTE:
  privat        Freunde, Familie, Bekannte
  beruflich     Arbeitskollegen, Geschaeftskontakte
  versicherung  Versicherungsberater, Agenturen
  finanzen      Steuerberater, Bankberater
  arzt          Aerzte, Therapeuten, Apotheken
  sonstige      Alles andere

DATENBANK:
  Haupttabelle: bach.db / assistant_contacts
  Felder: id, name, context, email, phone, mobile, address, birthday,
          company, position, tags, notes, is_active, created_at, updated_at

  HINWEIS: vCard-Export nutzt zusaetzlich "contacts" Tabelle (Unified Schema)
           mit erweiterten Feldern (first_name, last_name, organization, etc.)

BEISPIELE:
  # Kontakt mit allen Details anlegen:
  bach contact add "Dr. Mueller" --context arzt --phone 030-12345 --email mueller@example.de --address "Hauptstr. 1, 10115 Berlin"

  # Beruflichen Kontakt mit Firma und Position:
  bach contact add "Lisa Schmidt" --context beruflich --company "Beispiel GmbH" --position "Teamlead" --tags "dev,it" --email lisa@example.com

  # Kontakt suchen:
  bach contact search Mueller

  # Telefonnummer und Firma aendern:
  bach contact edit 5 --phone 030-99999 --company "Neue GmbH" --note "Gewechselt ab Jan 2026"

  # Alle Versicherungskontakte:
  bach contact list -c versicherung

  # Wer hat bald Geburtstag?
  bach contact birthday 60

  # Export-Beispiele:
  bach contact export                              # Text-Format in Konsole
  bach contact export --format csv                 # CSV in Konsole
  bach contact export --type arzt --format csv     # Nur Arzt-Kontakte als CSV
  bach contact export --format vcard --file kontakte.vcf  # vCard in Datei
  bach contact export --file export.csv            # CSV in Datei

ZUSAMMENSPIEL:
  - Getrennt von health_contacts (Arzt-Kontakte im Gesundheitsmodul)
  - assistant_contacts = persoenliche Kontaktdatenbank (Standard-Operationen)
  - contacts = Unified-Tabelle (nur fuer vCard-Export)
  - GUI: Kontakte-Tab (wenn verfuegbar)

BEKANNTE EINSCHRAENKUNGEN:
  - "bach contact list --all" zeigt inaktive Kontakte OHNE visuelle Markierung
  - vCard-Export greift auf separate "contacts" Tabelle zu (nicht assistant_contacts)
  - Tags werden bei Search durchsucht, aber nicht in List-Ansicht angezeigt


## Cookbooks

COOKBOOKS - Anthropic Referenz-Material
========================================

STAND: 2026-02-06

BESCHREIBUNG
------------
Ausgewaehlte Notebooks und Scripts aus dem offiziellen Anthropic
claude-cookbooks Repository. Dienen als Referenz und Inspiration
fuer BACH-Weiterentwicklungen -- nicht als direkt ausfuehrbarer Code.

SPEICHERORT
-----------
docs/reference/anthropic_cookbooks/

VERFUEGBARE COOKBOOKS
---------------------

  memory/
    memory_tool.py                        Tool-basiertes LLM-Memory
    BACH-Vergleich: bach --memory ist deutlich ausgereifter
                    (SQLite, Sessions, Confidence, 10 Ops)
    Nuetzlich fuer: Tool-Definition-Pattern, Prompt-Engineering

  compaction/
    session_memory_compaction.ipynb        Session-Zusammenfassung
    automatic-context-compaction.ipynb     Token-basiertes Auto-Compact
    BACH-Vergleich: prompt_manager.py mit Kontext-Kompression
    Nuetzlich fuer: Token-Zaehlung, Komprimierungs-Prompts

  text_to_sql/
    guide.ipynb                           Natural Language → SQL
    BACH-Relevanz: Integrationsplan fuer "bach --db query"
    Nuetzlich fuer: Schema-Kontext, SQL-Validierung, Retry-Loop

  orchestrator/
    orchestrator_workers.ipynb            Orchestrator-Worker Pattern
    prompts/                              3 Agent-Prompt-Templates
      citations_agent.md                  Quellenverweise
      research_lead_agent.md              Recherche-Steuerung
      research_subagent.md                Recherche-Ausfuehrung
    BACH-Vergleich: agents/_experts/ + hub/_services/
    Nuetzlich fuer: Agent-Prompt-Vorlagen, Ergebnis-Synthese

  tool_search/
    tool_search_with_embeddings.ipynb     Semantische Tool-Suche
    BACH-Vergleich: _try_run_tool() nutzt Prefix-Match
    Nuetzlich fuer: Embedding-basierte Tool-Discovery

INTEGRATION IN BACH
-------------------

  Prioritaet 1 (kurzfristig):
    - text_to_sql → neuer "bach --db query" Handler
    - compaction → Token-Zaehlung in prompt_manager.py

  Prioritaet 2 (mittelfristig):
    - orchestrator → Refactoring der Agent-Orchestrierung
    - tool_search → Upgrade fuer tool_discovery.py

  Prioritaet 3 (langfristig):
    - memory → Vergleich fuer Quality-Checks

QUELLEN
-------

  Repository:  github.com/anthropics/claude-cookbooks
  Commit:      7cb72a9
  Datum:       2026-02-06
  Lizenz:      Apache 2.0

WEITERE REFERENZEN
------------------

  docs/reference/mcp-builder/             MCP Server Best Practices
    SKILL.md                              Skill-Definition
    reference/mcp_best_practices.md       MCP Patterns
    reference/python_mcp_server.md        Python MCP Server
    reference/node_mcp_server.md          Node MCP Server
    reference/evaluation.md               MCP Evaluation

  tools/testing/playwright/               Browser-Test-Referenz
    with_server.py                        Server-Management
    examples/                             3 Beispiel-Scripts

SIEHE AUCH
----------
bach --help vendor              Vendor-Code (anthropic_docx/pdf/xlsx)
bach --help tools               Tool-Uebersicht
docs/reference/analyse_anthropic_skills_cookbooks.md   Vollstaendige Analyse


## Core

BACH KERN-KONZEPT
=================

"Der Agent ist die Rolle und die zielorientierte Absicht darin.
Workflows sind das Gehirn zur Ausfuehrung.
Skills, Tools und Services sind die Werkzeuge zur Ausfuehrung.
Zusammen sind sie der Kern."

DIE VIER SAEULEN
----------------

```
┌─────────────────────────────────────────────────────────────────┐
│                        DER KERN                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │   AGENT     │    │  WORKFLOW   │    │  SKILLS/TOOLS/SVC   │  │
│  │             │    │             │    │                     │  │
│  │  Rolle +    │───>│  Gehirn     │───>│  Werkzeuge          │  │
│  │  Absicht    │    │  Steuerung  │    │  Ausfuehrung        │  │
│  │             │    │             │    │                     │  │
│  │  WER + WARUM│    │  WIE        │    │  WOMIT              │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

AGENT = Rolle + zielorientierte Absicht
---------------------------------------

- WER bin ich in dieser Aufgabe?
- WARUM tue ich das? (Ziel, Motivation)
- Definiert Perspektive und Entscheidungsrahmen

Beispiele:
  - Entwickler-Agent: Schreibt Code, debuggt, testet
  - Persoenlicher Assistent: Hilft User bei Alltag
  - Recherche-Experte: Sucht und bewertet Informationen

Speicherort: agents/*.txt

WORKFLOW = Gehirn zur Ausfuehrung
---------------------------------

- WIE wird die Aufgabe ausgefuehrt?
- Steuert den Ablauf, die Reihenfolge, die Entscheidungen
- Prozedurales Wissen: Schritt-fuer-Schritt Anleitung

Beispiele:
  - Bugfix-Workflow: Reproduzieren -> Analysieren -> Fixen -> Testen
  - Review-Workflow: Lesen -> Bewerten -> Kommentieren -> Entscheiden
  - Startup-Workflow: Pruefen -> Laden -> Initialisieren -> Bereit

Speicherort: skills/workflows/*.md

Workflows sind ZENTRAL weil:
  1. Sie die eigentliche Steuerung uebernehmen
  2. Sie Skills, Tools und Services orchestrieren
  3. Sie testbar sind (Usecase-Tests)
  4. Sie wiederverwendbar sind

SKILLS / TOOLS / SERVICES = Werkzeuge
-------------------------------------

- WOMIT wird die Aufgabe ausgefuehrt?
- Konkrete Faehigkeiten und Funktionen
- Werden von Workflows aufgerufen

| Typ     | Beschreibung              | Speicherort           |
|---------|---------------------------|-----------------------|
| Skills  | Wissen + Anleitung (.txt) | skills/*.txt          |
| Tools   | Python-Scripts (.py)      | tools/*.py            |
| Services| Externe Dienste           | via API/CLI           |

ZUSAMMENSPIEL
-------------

```
User-Anfrage
     │
     v
┌─────────────┐
│   AGENT     │  "Ich bin Entwickler, Ziel: Bug fixen"
└─────────────┘
     │
     v
┌─────────────┐
│  WORKFLOW   │  "1. Reproduzieren 2. Analysieren 3. Fixen"
└─────────────┘
     │
     v
┌─────────────────────────────────────┐
│  SKILLS / TOOLS / SERVICES          │
│  - debugger.py (Tool)               │
│  - git-workflow.txt (Skill)         │
│  - test-runner (Service)            │
└─────────────────────────────────────┘
     │
     v
Ergebnis
```

BEWUSSTSEIN DES LLM
-------------------

Das operierende LLM muss wissen:
1. WELCHE Agents existieren (agents/)
2. WELCHE Workflows verfuegbar sind (skills/workflows/)
3. WELCHE Skills/Tools/Services es gibt (skills/, tools/)

Dies wird erreicht durch:
- Handler-Registry (system/core/registry.py) - Auto-Discovery von Handlern
- Tool-Auto-Discovery (tools/tool_auto_discovery.py) - Scannt Tools in DB
- DB-Eintraege (tools-Tabelle, hierarchy_items)
- Startup-Uebersicht zeigt Session-Kontext

Siehe: --help startup, --help tools

QUALITAETSSICHERUNG (WORKFLOW-TUEV)
-----------------------------------

Workflows sind so wichtig, dass sie geprueft werden muessen:

1. USECASE-TESTS
   - Sammlung von Testfaellen in DB
   - Automatische Durchfuehrung
   - Bewertung: sehr gut / gut / befriedigend / ausreichend / durchgefallen

2. TUEV-ABLAUF
   - Workflows haben Ablaufdatum
   - Bei Ablauf: Wartungs-Task automatisch erstellen
   - Nach Pruefung: Neues Ablaufdatum setzen

3. CHECKLISTE fuer neue Komponenten
   [ ] Funktioniert ohne User-Daten?
   [ ] CLI-Befehl vorhanden?
   [ ] Input aus Dateien/Ordnern moeglich?
   [ ] Output in strukturierte DB?
   [ ] Scan/Import wiederholbar (idempotent)?
   [ ] Keine Hardcoded-Pfade?

Siehe: WF-TUEV Tasks (in Entwicklung)

VERWANDTE KONZEPTE
------------------

- docs/docs/docs/help/memory.txt        - Memory als kognitives Modell
- docs/docs/docs/help/agents.txt        - Agent-System Details
- docs/docs/docs/help/workflow.txt      - Workflow-System Details
- docs/docs/docs/help/skills.txt        - Skills-Hierarchie
- docs/docs/docs/help/tools.txt         - Tool-System Details
- system/ARCHITECTURE.md - Gesamtarchitektur

---
Version: 1.0.1 | Erstellt: 2026-01-30 | Aktualisiert: 2026-02-08
(Kern-Konzept: Agent/Workflow/Skills/Tools)


## Countdown

COUNTDOWN - Countdown mit Trigger
==================================

Countdown-Timer der bei Ablauf optional einen Befehl ausfuehrt.

CLI-BEFEHLE
-----------

  bach countdown start <name> HH:MM:SS              Countdown starten
  bach countdown start <name> HH:MM:SS --after "cmd" Mit Trigger-Befehl
  bach countdown stop <name>                         Countdown abbrechen
  bach countdown list                                Aktive Countdowns
  bach countdown pause <name>                        Pausieren
  bach countdown resume <name>                       Fortsetzen

AUSGABE-FORMAT
--------------

  Normal:  [COUNTDOWN] session: 45:12 verbleibend
  Warnung: [!] session: Nur noch 04:58!

Warnung erscheint bei < 5 Minuten verbleibend.

PERSISTENZ
----------

  Datei: data/.countdown_state

  Inhalt:
  {
    "countdowns": {
      "session": {
        "end_time": "2026-01-30T15:00:00",
        "after_command": "shutdown 'Zeit um'",
        "paused": false,
        "remaining_on_pause": null
      }
    }
  }

BEISPIELE
---------

  # 1-Stunde Session-Countdown
  bach countdown start session 01:00:00
  -> Countdown 'session' gestartet: 01:00:00

  # Mit automatischem Shutdown
  bach countdown start session 01:00:00 --after "shutdown 'Session beendet'"
  -> Bei Ablauf wird "bach --shutdown 'Session beendet'" ausgefuehrt

  # Pomodoro-Timer (25 Min)
  bach countdown start focus 00:25:00
  -> Countdown 'focus' gestartet: 00:25:00

  # Pausieren und Fortsetzen
  bach countdown pause focus
  bach countdown resume focus

  # Status pruefen
  bach countdown list
  -> session: 45:12 verbleibend
  -> focus:   19:45 verbleibend (PAUSIERT)

TRIGGER (--after)
-----------------

Der --after Befehl wird bei Ablauf ausgefuehrt:

  --after "shutdown 'Zeit um'"     Session beenden
  --after "msg send user 'Pause!'" Nachricht senden
  --after "task done 123"          Task als erledigt markieren

Bei Ablauf wird der Befehl in eine Queue geschrieben.
Der naechste CLI-Aufruf fuehrt ihn aus (oder der Daemon).

USECASES
--------

  1. SESSION-LIMIT
     bach countdown start session 02:00:00 --after "shutdown 'Limit erreicht'"
     -> Automatisches Session-Ende nach 2 Stunden

  2. POMODORO-TECHNIK
     bach countdown start focus 00:25:00 --after "msg send user 'Pause machen!'"
     -> Nach 25 Min Erinnerung an Pause

  3. DEADLINE-REMINDER
     bach countdown start deadline 04:00:00
     -> Warnung bei < 5 Min, dann manuell handeln

ZUSAMMENSPIEL
-------------

Countdown ist Teil des Zeit-Systems:
  --help clock    Uhrzeit-Anzeige
  --help timer    Stoppuhr
  --help between  Between-Checks
  --help beat     Unified Zeit-Anzeige

---
Version: 1.0 | Status: Implementiert (v1.1.83)
Siehe: docs/CONCEPT_time_system.md


## Daemon

DAEMON - Hintergrund-Jobs und Scheduler
=======================================

STAND: 2026-02-08

WICHTIGE POLICY
---------------
**ALLE DAEMON-JOBS SIND STANDARDMAESSIG DEAKTIVIERT.**

Grund: Automatische Prozesse koennen mit aktiven Chat-Sessions
und dem Prompt Generator kollidieren. Jobs werden nur manuell
aktiviert wenn benoetigt.

Der Daemon pausiert automatisch OneDrive-Sync waehrend des Betriebs
um Sync-Konflikte zu vermeiden.

Siehe: docs/CONCEPT_daemon_policy.md

CLI-BEFEHLE
-----------
  bach daemon jobs              Alle Jobs anzeigen
  bach daemon status            Daemon-Status
  bach daemon start [--bg]      Scheduler starten (--bg fuer Hintergrund)
  bach daemon stop              Scheduler stoppen
  bach daemon run <ID>          Einzelnen Job manuell ausfuehren
  bach daemon logs [N]          Letzte Log-Eintraege anzeigen (Standard: 20)

SESSION-SYSTEM
--------------
  bach daemon session start [--profile NAME]   Session-Daemon starten
  bach daemon session stop                     Session-Daemon stoppen
  bach daemon session status                   Session-Status anzeigen
  bach daemon session trigger [--profile NAME] Session manuell ausloesen
  bach daemon session profiles                 Verfuegbare Profile auflisten

  Beispiel mit Dry-Run:
    bach daemon session trigger --profile wartung --dry-run

JOB-TYPEN
---------
  interval    Wiederholung nach Zeitspanne (z.B. 24h, 30m)
  cron        Zeitplan-basiert (z.B. "0 2 * * *" = taeglich 2 Uhr)
  event       Event-basierter Trigger (extern ausgeloest)
  manual      Nur manuell ausfuehrbar
  chain       Verkettete Job-Ausfuehrung (Chain-System)

Der Daemon prueft automatisch alle 5 Minuten auf faellige Recurring Tasks.

VERFUEGBARE JOBS (alle standardmaessig AUS)
-------------------------------------------
Hinweis: Job-Liste ist dynamisch. Aktuelle Jobs via: bach daemon jobs

Beispiel-Jobs:
  ID  Name                      Schedule    Funktion
  --  ------------------------  ----------  --------------------------------
  1   scanner                   60m         Software-Ordner nach Tasks scannen
  2   backup                    24h         Automatisches Backup
  3   inbox-scan                30m         Inbox-Ordner verarbeiten
  4   consolidate-weight        24h         Memory-Gewichtungen (Decay)
  5   consolidate-archive       24h         Alte Eintraege archivieren
  6   consolidate-index         7d          Help/Wiki Index aktualisieren
  7   consolidate-compress      24h         Sessions komprimieren
  8   consolidate-we            7d          Woechentliche Konsolidierung
  9   Nightly Maintenance       cron 0 2    Naechliche Wartungskette
  10  Weekly Backup             cron 0 3 0  Woechentliches Backup

Connector-Jobs (v2.0, via bach connector setup-daemon):
  --  connector_poll_and_route  2m          Connectors pollen + Inbox-Routing
  --  connector_dispatch        1m          Ausgehende Queue mit Retry versenden

JOB MANUELL AUSFUEHREN
----------------------
Empfohlene Methode statt automatischem Scheduler:

  # Job einmalig ausfuehren
  bach daemon run 1         # Scanner einmal laufen lassen
  bach daemon run 2         # Backup einmal erstellen

  # Oder direkt den Befehl
  bach scan run             # Scanner
  bach backup create        # Backup
  bach consolidate run      # Konsolidierung

GUI
---
  http://127.0.0.1:8000/daemon    Daemon-Dashboard

  - Jobs aktivieren/deaktivieren
  - Manuell ausfuehren
  - Letzte Ausfuehrungen sehen

SIEHE AUCH
----------
  docs/CONCEPT_daemon_policy.md   Daemon-Richtlinien
  docs/docs/docs/help/connector.txt              Connector-System (Queue, Retry)
  docs/docs/docs/help/maintain.txt               Wartungs-Tools
  docs/docs/docs/help/backup.txt                 Backup-System
  docs/docs/docs/help/consolidation.txt          Memory-Konsolidierung


## Data

DATA ANALYSIS - BACH Datenanalyse-Befehle
==========================================

BACH bietet einfache Datenanalyse-Funktionen fuer CSV, Excel und JSON.

INSTALLATION
------------
Benoetigt: pip install pandas matplotlib

BEFEHLE
-------

bach data list
  Zeigt alle Dateien im input/ Ordner an.

bach data load <pfad>
  Laedt Datei und zeigt Basisinfos (Zeilen, Spalten, Datentypen).
  Unterstuetzte Formate: CSV, Excel (.xlsx/.xls), JSON

bach data describe <pfad>
  Zeigt deskriptive Statistik (mean, std, min, max, quartile).
  Nur fuer numerische Spalten.

bach data head <pfad> [--rows N]
  Zeigt die ersten N Zeilen (Standard: 10).

bach data corr <pfad>
  Zeigt Korrelationsmatrix aller numerischen Spalten.

bach data chart <pfad> --type TYPE --x COL [--y COL] [--output NAME]
  Erstellt ein Diagramm und speichert es in charts/.
  X-Spalte erforderlich, Y-Spalte optional (wird automatisch gewaehlt).

  Chart-Typen:
    bar     - Balkendiagramm (benoetigt X und Y)
    line    - Liniendiagramm (benoetigt X und Y)
    pie     - Kreisdiagramm (benoetigt X, Y optional fuer Werte)
    scatter - Streudiagramm (benoetigt X und Y)
    hist    - Histogramm (benoetigt nur X)

VERZEICHNISSE
-------------
user/data-analysis/
├── input/    # Quelldateien hier ablegen
├── output/   # Verarbeitete Ergebnisse
└── charts/   # Generierte Diagramme

BEISPIELE
---------

# Datei laden und analysieren
bach data load user/data-analysis/input/sales.csv
bach data describe user/data-analysis/input/sales.csv
bach data head user/data-analysis/input/sales.csv --rows 20

# Korrelation pruefen
bach data corr user/data-analysis/input/metrics.xlsx

# Charts erstellen
bach data chart input/sales.csv --type bar --x monat --y umsatz
bach data chart metrics.xlsx --type line --x date --y value --output trend
bach data chart input/survey.csv --type pie --x kategorie --y anzahl
bach data chart input/metrics.xlsx --type scatter --x x_wert --y y_wert
bach data chart input/data.csv --type hist --x alter

TIPPS
-----
- Dateien im input/ Ordner koennen mit kurzem Namen referenziert werden
- Charts werden automatisch in charts/ gespeichert (PNG, 150 DPI)
- Bei grossen Dateien: erst head, dann describe
- Chart-Befehle erfordern matplotlib: pip install matplotlib
- Y-Spalte wird bei bar/line/scatter automatisch gewaehlt wenn nicht angegeben

SIEHE AUCH
----------
bach --help tools     # Alle verfuegbaren Tools
bach --help features  # BACH Features-Uebersicht

VERSION
-------
Eingefuehrt in BACH v1.1.25 (2026-01-21)
Chart-Befehle vollstaendig implementiert (bar, line, pie, scatter, hist)
Handler: system/hub/data_analysis.py


## Delegate

BACH PARTNER-DELEGATION
=======================

STAND: 2026-02-08

Die Delegation ermöglicht die Verteilung von Aufgaben innerhalb
des Partner-Netzwerks basierend auf Expertise und Token-Ökonomie.

Handler: system/hub/partner.py (DB-basiert seit JSON_001 Migration)

KERNAUFGABEN
------------
- Task-Delegation via CLI oder MessageBox (data/messages/message_box.md)
- Monitoring des Fortschritts über `bach partner status`
- Token-bewusste Auswahl basierend auf Zonen (monitor_tokens DB-Tabelle)
- Offline-Fallback zu lokalen Partnern (--fallback-local Flag)

CLI-BEFEHLE (bach partner)
--------------------------
  list          Zeigt alle registrierten Partner und ihren Status
  status        Zusammenfassung aktiver Partner und Delegation-Zonen
  info <name>   Details zu einem spezifischen Partner
  active        Nur aktive Partner auflisten
  delegate      Überträgt einen Task an Partner (Token-aware)
                --to=NAME         Spezifischer Partner
                --zone=N          Zone erzwingen (1-4)
                --fallback-local  Bei Offline auf lokale AI (Ollama) ausweichen

GEMINI WORKFLOW
---------------
Gemini ist der primäre Partner für Deep-Analysis und Long-Form Content:

1. ZUWEISUNG:
   `bach partner delegate "Task Text" --to=gemini`
   Alternativ: Delegation via MessageBox (data/messages/message_box.md)

2. START:
   Über `partners/gemini/start_gemini.bat`
   Antigravity lädt automatisch Kontext aus .gemini/GEMINI.md

3. BEARBEITUNG:
   Partner arbeitet autark in `partners/gemini/workspace/`

4. ABSCHLUSS:
   Bericht in `partners/gemini/outbox/` ablegen
   Task als erledigt markieren: `bach task done ID`

TOKEN-ZONEN & STRATEGIE
-----------------------
Basierend auf monitor_tokens.budget_percent aus bach.db:

- Zone 1 (0-30%):   Alle Partner verfügbar (Claude, Gemini, etc.)
- Zone 2 (30-60%):  Kostengünstige Partner bevorzugt (Gemini, Ollama)
- Zone 3 (60-80%):  Nur lokale AI (Ollama)
- Zone 4 (80-100%): Nur Human (Intervention erforderlich)

ARCHITEKTUR-HINWEIS
-------------------
Delegation ist DB-basiert (seit JSON_001 Migration):
- Partner in partner_recognition Tabelle
- Zonen-Regeln in delegation_rules Tabelle
- Token-Budget in monitor_tokens Tabelle
- Delegation-Messages in data/messages/message_box.md

SIEHE AUCH
----------
docs/docs/docs/help/partner.txt                 Partner-Konzept (Zonen, Routing)
wiki/gemini.txt             Gemini-Details
wiki/antigravity.txt        Antigravity-Editor
hub/partner.py                   Partner Handler Implementation
data/bach.db                     Partner-Registry (partner_recognition, delegation_rules)


## Denkstrategien

DENKSTRATEGIEN
==============
Kognitive und metakognitive Strategien fuer Informationsverarbeitung.

Bezug: Lernsystem-Analyse, docs/docs/docs/help/operatoren.txt, docs/docs/docs/help/rhetorik.txt


1. KOGNITIVE STRATEGIEN (Informationsverarbeitung)
===================================================
Steuern WIE man Informationen verarbeitet.

1.1 Chunking (Buendeln)
-----------------------
Komplexe Informationen in kleinere Einheiten zerlegen.
  - grosse Aufgabe in 5 Schritte teilen
  - Text in Abschnitte gliedern
BACH: Task-Breakdown, Workflow-Phasen

1.2 Mustererkennung
-------------------
Wiederkehrende Strukturen erkennen.
  - aehnliche Fehler in Logs
  - wiederkehrende Dokumenttypen
BACH: Lessons-Learned Pattern-Matching

1.3 Analogiebildung
-------------------
Neues durch Vergleich mit Bekanntem verstehen.
  - "Mail-Routing ist wie Netzwerk-Routing"
  - "Operatoren sind wie Lego-Bausteine"

1.4 Hypothesenbildung
---------------------
Annahmen formulieren, bevor man prueft.
  - "Wenn Score niedrig, fehlt vermutlich ein Pflichtfeld"

1.5 Deduktives Denken
---------------------
Vom Allgemeinen auf den Einzelfall schliessen.
  - "Alle Rechnungen haben Rechnungsnummer -> dieses Dokument
     hat keine -> vermutlich keine Rechnung"

1.6 Induktives Denken
---------------------
Vom Einzelfall auf Regeln schliessen.
  - "In 90% der Faelle enthaelt 'Rechnung' im Betreff
     eine echte Rechnung"
BACH: Lessons-Learned Ableitung

1.7 Kausales Denken
-------------------
Ursache-Wirkungs-Beziehungen erkennen.
  - "Fehler steigt -> CPU-Last steigt -> vermutlich Engpass"

1.8 Perspektivwechsel
---------------------
Problem aus anderer Sicht betrachten.
  - Nutzerperspektive vs. Entwicklerperspektive

1.9 Szenariodenken
------------------
"Was waere wenn"-Varianten durchspielen.
  - "Was passiert, wenn API ausfaellt"
  - "Was, wenn Klassifikation falsch liegt"
BACH: Modus (2) Nachdenken

1.10 Priorisieren
-----------------
Wichtige Informationen zuerst verarbeiten.
  - kritische Fehler vor Warnungen
  - Rechnungen vor Newslettern
BACH: Task-Prioritaeten (P1 > P2 > P3)


2. METAKOGNITIVE STRATEGIEN (Denken ueber Denken)
==================================================
Steuern WIE man sein eigenes Denken steuert.

2.1 Selbstueberwachung (Monitoring)
-----------------------------------
Eigenes Denken beobachten.
  - "Verstehe ich das Problem wirklich"
  - "Welche Annahmen mache ich gerade"

2.2 Selbstregulation
--------------------
Den Denkprozess aktiv anpassen.
  - Tempo reduzieren
  - Strategie wechseln (z.B. von Hypothese -> Test)

2.3 Fehleranalyse
-----------------
Eigene Denkfehler erkennen.
  - Bestaetigungsfehler
  - vorschnelle Schlussfolgerungen
BACH: Lessons-Learned (Bug-Kategorie)

2.4 Meta-Fragen stellen
-----------------------
Fragen ueber den Denkprozess selbst.
  - "Welche Informationen fehlen mir"
  - "Welche Operatoren brauche ich hier"

2.5 Strategiewahl
-----------------
Bewusst entscheiden, welche Denkstrategie passt.
  - "Brauche ich Mustererkennung oder Hypothesenbildung"

2.6 Reflexion
-------------
Nachtraegliches Bewerten des Denkprozesses.
  - "Warum hat diese Loesung funktioniert"
  - "Was wuerde ich naechstes Mal anders machen"
BACH: Session-Summary, Konsolidierung

2.7 Metamodellierung
--------------------
Das Problem in ein abstrakteres Modell ueberfuehren.
  - "Das ist ein Klassifikationsproblem"
  - "Das ist ein Routing-Problem"

2.8 Meta-Abstraktion
--------------------
Komplexitaet reduzieren, indem man auf die Essenz schaut.
  - "Eigentlich geht es nur um drei Variablen"

2.9 Meta-Vergleiche
-------------------
Vergleich zwischen Denkstrategien.
  - "Hypothesenbildung war ineffektiv -> besser Daten-Driven"

2.10 Meta-Planung
-----------------
Planen, wie man denkt, bevor man denkt.
BACH: Modus (2) Nachdenken = Injektoren bewusst provozieren


3. BEZUG ZU BACH MODI
=====================

Modus (1) Energiesparen:
  - Mustererkennung (automatisch)
  - Priorisieren (Regeln abrufen)
  - Deduktion (schnelle Schlussfolgerungen)

Modus (2) Nachdenken:
  - Szenariodenken
  - Perspektivwechsel
  - Hypothesenbildung
  - Meta-Fragen stellen
  - Strategiewahl

Modus (3) Konsolidierung:
  - Induktives Denken (Regeln ableiten)
  - Reflexion
  - Fehleranalyse
  - Meta-Abstraktion


4. BEZUG ZU RHETORIK
====================
Denkstrategien haben direkte rhetorische Entsprechungen:

  Chunking           -> Gliederung, 3-Punkte-Regel
  Mustererkennung    -> Topoi (Argumentmuster), Story-Archetypen
  Analogiebildung    -> Metaphern, Vergleiche
  Hypothesenbildung  -> Argumente vorbereiten, Gegenargumente antizipieren
  Deduktion/Induktion-> Logische Argumentation
  Szenariodenken     -> "Was waere wenn"-Argumente
  Priorisieren       -> Kernbotschaft, Elevator Pitch

Rhetorik = Kognitive Strategie + Sprachliche Verpackung

Siehe: --help rhetorik


VERWANDTE HELP-DATEIEN
======================
  --help operatoren   Basis-Operatoren und Patterns
  --help strategien   Kategorisieren, Bewerten, Testen, etc.
  --help rhetorik     Rhetorische Operatoren und Patterns
  --help metakognition Wiki-Eintrag zur Metakognition


## Dev

ENTWICKLUNGSMODUS (Dev-Zyklus)
==============================

BESCHREIBUNG
------------
BACH wird in einem 8-Phasen-Zyklus entwickelt. Jedes Feature durchlaeuft
den gleichen Ablauf: Von der Anforderung bis zum validierten Usecase.

DER ZYKLUS
----------

  Phase 1: Feature-Wuensche     Anforderungen funktional formulieren
  Phase 2: Ist-Stand pruefen    Was gibt es schon? Duplikate vermeiden
  Phase 3: Funktionale Planung  Workflows, Agenten, Experten, Skills, Services
  Phase 4: Functional Frontend  Skill-Dateien, Workflows, Agent-Profile erstellen
  Phase 5: Backend planen       CLI-Handler, DB-Schema, API-Endpoints
  Phase 6: Backend umsetzen     Python-Code, Tools, DB-Migrationen
  Phase 7: Technische Tests     B/O/E-Tests, Bugfix-Protokoll
  Phase 8: Usecases             End-to-End Validierung aus Nutzersicht

GRUNDPRINZIPIEN
---------------
  1. Systemisch First     Wiederverwendbar fuer jeden User
  2. CLI First            Alles ueber Terminal steuerbar
  3. dist_type Isolation  User-Daten getrennt (0/1/2/3)
  4. Functional First     Erst beschreiben, dann implementieren
  5. Usecases als Tests   Validierung UND Anforderungsquelle

DER KREISLAUF
-------------

  Usecases (Phase 8) generieren neue Anforderungen (Phase 1).
  Fehlgeschlagene Usecases werden zu Bugs oder Feature-Requests.
  Erfolgreiche Usecases validieren das System.

  Phase 8 -> Phase 1 -> Phase 2 -> ... -> Phase 8 (Kreislauf)

EBENEN DER PLANUNG (Phase 3)
-----------------------------

  Ebene      Frage                        Ort
  ---------  ---------------------------  -------------------------
  Workflow   WANN/WIE koordinieren?       skills/workflows/*.md
  Agent      WER fuehrt aus?              agents/*.txt
  Experte    WER hat Fachwissen?          agents/_experts/*/
  Skill      WAS wird getan?              skills/_services/*.md
  Service    WIE technisch?               skills/_services/*/
  Tool       WOMIT wird gearbeitet?       tools/*.py

CHECKLISTE NEUER SERVICE (Phase 6)
-----------------------------------
  [ ] Funktioniert ohne User-Daten (leere DB)?
  [ ] CLI-Befehl vorhanden?
  [ ] Input aus Dateien/Ordnern?
  [ ] Output in strukturierte DB?
  [ ] dist_type automatisch gesetzt?
  [ ] Scan/Import wiederholbar (idempotent)?
  [ ] Kein Hardcoded-Pfad?
  [ ] Tool registriert?
  [ ] Help-Datei erstellt?

WORKFLOW-DATEI
--------------
  Detaillierter Ablauf: skills/workflows/dev-zyklus.md

SIEHE AUCH
----------
  bach --help usecase           Usecase-Dokumentation (Phase 8)
  bach --help test              Testverfahren (Phase 7)
  bach --help practices         Architektur-Prinzipien
  docs/_archive/WICHTIG_SYSTEMISCH_FIRST.md   Kernprinzip

---
Version: 1.0.0 | Erstellt: 2026-01-28


## Dirscan

DIRECTORY TRUTH
===============

Automatische Verzeichnis-Zustandsverwaltung.

KONZEPT:
  - Startup: IST-Zustand erfassen, mit SOLL vergleichen
  - Shutdown: Aktueller Zustand wird neuer SOLL
  - Heuristik: Claude-Aenderungen sind gewollt

ABLAUF:

1. Erster Start
   - Aktueller Zustand = SOLL-Zustand
   - Gespeichert in data/directory_truth.json

2. Folgende Starts
   - IST-Zustand scannen
   - Vergleich mit SOLL
   - Externe Aenderungen anzeigen (User hat was geaendert)

3. Shutdown
   - Aktueller Zustand wird neuer SOLL
   - Claudes Aenderungen sind jetzt "Standard"

IGNORIERT:
  - __pycache__
  - .pyc Dateien
  - .git, .idea, .vscode
  - auto_log.txt (aendert sich staendig)
  - current.md (Memory)

AUSGABE BEI AENDERUNGEN:
  + Neue Ordner/Dateien
  - Geloeschte Ordner/Dateien
  ~ Modifizierte Dateien

VORTEILE:
  - Claude muss nicht manuell tracken was sich geaendert hat
  - Externe Aenderungen (User) werden erkannt
  - Eigene Aenderungen automatisch uebernommen

INTEGRATION:
  - Automatisch in hub/startup.py (DirectoryScanner bei Startup)
  - Automatisch in hub/shutdown.py (Zustand bei Shutdown speichern)
  - Kein eigener Handler, Tool-basiert (tools/c_dirscan.py)

CLI (MANUELL):
  python c_dirscan.py                    # Status anzeigen
  python c_dirscan.py --scan             # Aktuellen Zustand scannen
  python c_dirscan.py --compare          # Vergleich IST vs SOLL
  python c_dirscan.py --update           # SOLL-Zustand aktualisieren
  python c_dirscan.py --path /pfad       # Anderes Verzeichnis
  python c_dirscan.py --json             # JSON-Ausgabe

DATEIEN:
  - Tool: system/tools/c_dirscan.py (DirectoryScanner-Klasse)
  - Daten: system/data/directory_truth.json
  - Struktur: {timestamp, directories[], files{path: {hash, size}}}


## Distribution

DISTRIBUTION-SYSTEM
===================

Stand: 2026-02-08

Das Distribution-System trennt System-Kern von User-Daten und Release-Templates.

4-TIER MODELL (dist_type):
  dist_type = 0  KERNEL     Absolut unveränderlich (Basis-System)
  dist_type = 1  CORE       Systemdatei (readonly / distribution backup)
  dist_type = 2  EXTENSION  Release-Template (1x Snapshot für Reset)
  dist_type = 3  USER_DATA  Individuelle Userdaten (nicht im Repo)

CLI-BEFEHLE
-----------
  bach --dist status              System-Status (Siegel, Mode, Dateien)
  bach --dist verify              Siegel-Integrität prüfen
  bach --dist scan                Dateien scannen und registrieren
  bach --dist snapshot NAME       Snapshot erstellen
  bach --dist release NAME        Release erstellen
  bach --dist restore ZIP         Aus Distribution-ZIP wiederherstellen
  bach --dist install ZIP ZIEL    Distribution in neuem Ordner installieren
  bach --dist list [snapshots]    Snapshots auflisten

RELEASE-WORKFLOW
----------------
  1. Snapshot erstellen: `bach --dist snapshot "pre-release"`
  2. Release erstellen: `bach --dist release "v1.2.0"`
  3. Distribution-ZIP wird in dist/ erstellt
  4. Reset: `bach fs heal --all` stellt Dateien aus Snapshots wieder her
  5. Restore: `bach --dist restore bach_vanilla_1.2.0.zip`

DATENBANK & FILESYSTEM INTEGRATION
----------------------------------
  - Skills & Tools werden bidirektional synchronisiert (`bach --sync skills`).
  - `dist_type` Spalten finden sich in ca. 60 Tabellen (siehe db/schema.sql).
  - Datei-Manifest in `distribution_manifest` Tabelle.
  - OneDrive/Git sichern die Distribution, BACH sichert die Integrität.

HINWEIS ZUR DATENBANK
---------------------
Es gibt nur eine zentrale `data/bach.db` (seit v2.0 in system/db/schema.sql).
Viele Tabellen nutzen `dist_type` für logische Trennung:
  - dist_type=0: Kernel-Daten (absolut unveränderlich)
  - dist_type=1: Core-Daten (systemkritisch)
  - dist_type=2: Extension-Daten (zurücksetzbar)
  - dist_type=3: User-Daten (nicht im Installer)

SIEHE AUCH
----------
  bach --sync help         Skills- und Tools-Synchronisation
  bach fs help             Filesystem-Operationen (heal, verify)
  docs/docs/docs/help/guidelines.txt      Dokumentations-Standards
  system/db/schema.sql     Vollständiges DB-Schema (114 Tabellen)


## Docs

DOCS - Menschenlesbare Dokumentation
=====================================

BESCHREIBUNG
------------
Neben dem help-System (fuer KI optimiert) gibt es zwei menschenlesbare
Dokumentationen mit ASCII-Grafiken und Uebersichten.

DOKUMENTATIONSEBENEN
--------------------
BACH hat drei Dokumentationsebenen:

  ┌────────────────────────────────────────────────────────────────┐
  │  EBENE              │  ZIELGRUPPE    │  ORT                   │
  ├────────────────────────────────────────────────────────────────┤
  │  docs/README.txt    │  Entwickler    │  docs/                 │
  │  (Entwicklung)      │  Kontributoren │                        │
  ├────────────────────────────────────────────────────────────────┤
  │  ARCHITECTURE.md    │  Entwickler    │  system/               │
  │  (Architektur)      │  Tiefgehend    │                        │
  ├────────────────────────────────────────────────────────────────┤
  │  docs/help/*.txt    │  KI-Agenten    │  system/docs/help/     │
  │  (Operativ)         │  Claude, etc.  │                        │
  ├────────────────────────────────────────────────────────────────┤
  │  wiki/*.txt         │  Alle          │  system/wiki/          │
  │  (Fachwissen)       │                │                        │
  └────────────────────────────────────────────────────────────────┘

DOKUMENTE
---------

  docs/README.txt
  ---------------
  Entwicklungsdokumentation - Uebersicht ueber docs/ Ordnerstruktur.
  - Konzepte (CONCEPT_*.md)
  - Analysen und Reports
  - Archivierte Altkonzepte (_archive/)
  - Langfristige Ideen (_ideas/)
  - Tests und Reports (_test_and_reports/)

  Zielgruppe: Entwickler, Kontributoren
  Format: Plain Text mit Verweisen

  system/ARCHITECTURE.md
  ----------------------
  System-Architektur fuer Entwickler.
  - Vision & Design-Philosophie
  - High-Level Architektur-Diagramme
  - Hub & Handler Pattern erklaert
  - Datenbankschema visualisiert
  - Datenfluss-Diagramme
  - Erweiterungsanleitungen
  - Konventionen

  Zielgruppe: Entwickler, Kontributoren, fortgeschrittene Nutzer
  Format: Markdown mit ASCII-Diagrammen

ABGRENZUNG
----------
  docs/help/*.txt        Operative Referenz, maschinenlesbar, konsistent
  docs/README.txt        Entwickler-Uebersicht, Ordnerstruktur
  system/ARCHITECTURE.md Technisches Verstaendnis, Architektur, Design

  help ist die PRIMAERE Dokumentation.
  docs/README.txt und ARCHITECTURE.md verweisen auf help fuer Details.

AKTUALISIERUNG
--------------
Bei groesseren Aenderungen am System sollten alle Ebenen
aktualisiert werden:

  1. docs/help/*.txt        - Befehle, Operationen (IMMER aktuell halten)
  2. docs/README.txt        - Bei Konzept-/Ordner-Aenderungen
  3. system/ARCHITECTURE.md - Bei Architektur-Aenderungen

GITHUB-VEROEFFENTLICHUNG
------------------------
Bei Veroeffentlichung auf GitHub:

  - system/ARCHITECTURE.md als Haupteinstieg verlinken
  - docs/README.txt fuer Entwickler-Uebersicht
  - help-System als integrierte Dokumentation erwaehnen

DATEIPFADE
----------
  docs/README.txt          Entwickler-Uebersicht
  system/ARCHITECTURE.md   Architektur-Dokumentation
  system/docs/help/*.txt   Operative Hilfe (diese Dateien)
  system/wiki/*.txt        Hintergrundwissen

SIEHE AUCH
----------
  bach --help list         Alle Help-Themen
  bach wiki list           Alle Wiki-Artikel
  docs/help/practices.txt  Architektur-Prinzipien
  docs/help/naming.txt     Namenskonventionen


## Documentation

BACH DOKUMENTATION - Uebersicht
================================

Zentrale Anlaufstelle fuer alle BACH-Dokumentation.

KERN-DOKUMENTE
--------------

Root-Ebene:
  SKILL.md              Master-Kontext, Identitaet, Verhaltensregeln
  README.md             Projekt-Uebersicht

system/:
  ARCHITECTURE.md       Technische Architektur, Komponenten
  ROADMAP.md            Entwicklungsplan, Meilensteine
  CHANGELOG.md          Versionshistorie, Aenderungen
  BUGLOG.md             Bekannte Bugs, Fixes

HELP-SYSTEM (system/docs/docs/docs/docs/help/)
--------------------------

Aufruf: python bach.py --help <topic>

KONZEPTE:
  --help core            Kern-Konzept (Agent/Workflow/Skills/Tools)
  --help memory          Memory-System (5 kognitive Typen + Lernkreislauf)
  --help injectors       Injektor-System (automatische Hinweise)
  --help consolidation   Konsolidierung (Komprimierung, Decay, Boost)
  --help startup         Startup-Protokoll

SYSTEM:
  --help tasks           Task-Management
  --help lessons         Lessons Learned System
  --help partner         Partner-System (Multi-LLM)
  --help daemon          Daemon-Service

ZEIT:
  --help clock           Uhrzeit-Anzeige
  --help timer           Stoppuhr
  --help countdown       Countdown mit Trigger
  --help between         Between-Checks
  --help beat            Unified Zeit-System

ENTWICKLUNG:
  --help dev             Entwicklungs-Workflow
  --help usecase         Usecase-Tests
  --help bugfix          Bugfix-Protokoll
  --help coding          Coding-Standards

VERZEICHNISSE:
  --help list            Alle verfuegbaren Themen

FEATURES (seit v1.1.85):
  --help agent/<name>    Agent-Dokumente (z.B. --help agent/ati)
  --help workflow/<name> Workflow-Dokumente
  --help expert/<name>   Experten-Dokumente
  --help <tool_name>     Tool-Informationen aus DB

SKILLS-HIERARCHIE (system/skills/)
-----------------------------------

  agents/        Agent-Profile (Rollen)
  skills/workflows/     Workflow-Definitionen (22 Workflows)
  agents/_experts/       Experten-Konfigurationen
  skills/_services/      Service-Beschreibungen
  skills/_templates/     Vorlagen
  partners/      Partner-LLM Konfigurationen
  connectors/    Externe Verbindungen
  skills/_os/            OS-spezifische Konfigurationen

DOCS-ORDNER (docs/)
-------------------

  docs/                  Aktuelle Konzepte und Analysen
  docs/_archive/         Archivierte/erledigte Konzepte
  docs/_ideas/           Ideen fuer die Zukunft
  docs/_test_and_reports/ Test-Ergebnisse und Berichte
  docs/analyse/          Analytische Dokumente
  docs/reference/        Externe Referenzen (cookbooks, etc.)

CODE-DOKUMENTATION
------------------

  system/bach.py         Haupt-Entry-Point (v2.0 Registry-Based)
  system/bach_api.py     Library-API (task, memory, backup, etc.)
  system/core/           Kern-Module (registry, app, db, base)
  system/hub/*.py        Handler-Implementierungen (Auto-Discovery)
  system/tools/*.py      Tool-Scripts

DATENBANK-SCHEMA
----------------

  system/db/schema.sql   Vollstaendiges DB-Schema (114 Tabellen)
  system/data/bach.db    SQLite-Datenbank

CLI-Zugriff:
  python bach.py --db schema       Zeigt DB-Schema
  python bach.py --db tables       Zeigt alle Tabellen

QUICK REFERENCE
---------------

  Was ist BACH?          --help wiki/was_ist_bach
  Wie starte ich?        --help startup
  Wie beende ich?        --help shutdown
  Task erstellen?        --help tasks
  Lesson speichern?      --help lessons
  Memory nutzen?         --help memory

DOKUMENTATIONS-HIERARCHIE
-------------------------

```
SKILL.md                 <- Master-Kontext (liest LLM immer)
    │
    ├── ARCHITECTURE.md  <- Technische Details
    │
    ├── docs/docs/docs/help/            <- Operative Anleitungen
    │   ├── core.txt     <- Kern-Konzept
    │   ├── memory.txt   <- Memory-System
    │   └── ...
    │
    ├── skills/          <- Funktionale Definitionen
    │   ├── _agents/
    │   ├── _workflows/
    │   └── ...
    │
    └── docs/            <- Konzepte, Analysen
        ├── CONCEPT_*.md
        └── archive/
```

HANDLER-ARCHITEKTUR
-------------------

Help Handler:      system/hub/help.py
  - Zeigt .txt Dateien aus system/docs/docs/docs/docs/help/
  - Unterstuetzt Unterordner (tools/, wiki/)
  - Alias-System fuer agents, workflows, _experts
  - Tool-Direktzugriff aus DB (v1.1.38+)

Docs Handler:      system/hub/docs.py
  - Listet/durchsucht docs/ Ordner
  - Gruppiert nach KONZEPTE, ANALYSEN, SCHEMATA, SONSTIGE
  - Operationen: list, show, search

---
Version: 1.0.1 | Erstellt: 2026-01-30 | Aktualisiert: 2026-02-08


## Downgrade

BACH DOWNGRADE - VERSION ZURÜCKSETZEN
======================================

Setzt BACH auf eine frühere Version zurück. Verwendet historische
Versionen aus dist_file_versions (SQ020).


VERWENDUNG
----------

  # Verfügbare Versionen einer Datei anzeigen
  bach downgrade list <datei-pfad>

  # Einzelne Datei auf Version zurücksetzen
  bach downgrade <datei-pfad> --version <version>

  # Gesamtes System auf Release zurücksetzen
  bach downgrade --release <release-id>

  # Dry-Run (nur anzeigen, nicht ausführen)
  bach downgrade --dry-run <datei-pfad> --version <version>


VERSIONEN
---------

Versionsnummern: v1, v2, v3, ...
  - Hash-basiert (SHA256 erkennt Änderungen automatisch)
  - Auto-Increment gibt menschenlesbare Reihenfolge


WICHTIG
-------

- Downgrade funktioniert NUR für CORE + TEMPLATE Dateien
- Alte Versionen werden in dist_file_versions gespeichert
- USER_DATA hat keine Versionierung (gehört dem User)
- Backup wird empfohlen vor Downgrade


BEISPIELE
---------

  # Versionen von bach.py anzeigen
  bach downgrade list system/bach.py

  # bach.py auf Version 3 zurücksetzen
  bach downgrade system/bach.py --version v3

  # Prüfen welche Dateien geändert würden
  bach downgrade --dry-run --release r2


KOMBINIERT MIT UPGRADE
-----------------------

Upgrade und Downgrade arbeiten zusammen:
  - Upgrade speichert alte Version automatisch
  - Downgrade greift auf gespeicherte Versionen zurück
  - Bidirektionales System (vor + zurück)


SIEHE AUCH
----------

  bach --help upgrade       Upgrade auf neuere Version
  bach --help restore       Template-Wiederherstellung
  bach --help seal          Integritätsprüfung


## Emoji

EMOJI-SYSTEM (KONZEPT-DOKU)
============================

Policy-Module und Tools zur Emoji-Handhabung.
HINWEIS: Keine automatische System-weite Konvertierung -
Policy-Funktionen muessen manuell aufgerufen werden.

VERFUEGBARE MODULE:

1. Policy-Modul (system/tools/_policies/emoji_safe.py)
   - emoji_to_safe(text): Emoji → ASCII-Tags via emoji.demojize()
   - emoji_to_display(text): ASCII-Tags → Emoji via emoji.emojize()

2. Scanner-Tool (system/tools/c_emoji_scanner.py)
   - CLI: python c_emoji_scanner.py --status
   - CLI: python c_emoji_scanner.py --scan-batch
   - CLI: python c_emoji_scanner.py <datei/ordner>
   - Nicht als BACH-Befehl integriert

3. JSON-Repair (system/tools/c_json_repair.py)
   - Nutzt Emoji-Konvertierung beim Repair-Prozess

KONVERTIERUNGS-BEISPIELE:
  ✅ → :check_mark_button:
  ❌ → :cross_mark:
  ⚠️ → :warning:
  📁 → :file_folder:
  📄 → :page_facing_up:
  🔧 → :wrench:
  💡 → :light_bulb:

ASCII-OVERRIDES (custom, in Tools definiert):
  🟢 → [GRUEN]
  🟡 → [GELB]
  🔴 → [ROT]
  ✅ → [OK]
  ❌ → [X]
  ⚠ → [WARN]
  → → ->
  ← → <-
  ↔ → <->

ANWENDUNG:
  - JSON-Dateien: ASCII-Tags bevorzugt (manuell konvertieren)
  - Markdown: Emojis erlaubt
  - Logs: ASCII-Tags bevorzugt

WARUM?
  - UTF-8 Encoding-Probleme vermeiden
  - Mojibake verhindern
  - Konsistenz ueber alle Systeme


## Entscheidung

ENTSCHEIDUNG - Decision-Briefing
=================================

BESCHREIBUNG:
  Experte unter dem Persoenlichen Assistenten. Sammelt systemweit alle
  offenen Entscheidungen und User-Aufgaben aus registrierten Dateien,
  konsolidiert sie in einem zentralen Briefing-Dokument, fuehrt den User
  durch die Entscheidungen und verteilt Ergebnisse zurueck an die Quellen.

  Skill-Datei: agents/_experts/decision-briefing/CONCEPT.md
  User-Daten:  user/decision_briefing/

  ABGRENZUNG:
    - decision-briefing (dieser Service): Systemweites Sammeln + Verteilen
    - user-decide (skill): Frameworks fuer Einzel-Entscheidungen (Pro/Con etc.)

MARKER-KONVENTION:
  Dateien im System kennzeichnen Entscheidungen mit diesen Markern:

  ENTSCHEIDUNG: Welchen Server buchen?
    Optionen: Hetzner / AWS / DigitalOcean
    Faelligkeit: vor 25.02.

  AUFGABE: Steuererkaerung bis 31.03. abgeben

  TODO: Termin mit Dr. Mueller vereinbaren

  DECISION: Which journal to target for Paper 3?

  TASK: GitHub-Repo auf oeffentlich stellen nach DOI-Vergabe

BRIEFING-FORMAT (user/decision_briefing/DECISION_BRIEFING.txt):
  # Decision Briefing - 2026-02-18
  ====================================
  ENTSCHEIDUNGEN (offen: 5)
  ====================================

  [E001] Welchen Server buchen?
    Quelle: /Forschung/CFM/Plan.txt:45
    Optionen: Hetzner / AWS / DigitalOcean
    Entscheidung: _______________

  [E002] Zielzeitschrift fuer Paper 3?
    Quelle: /Forschung/CFM/Plan.txt:78
    Entscheidung: _______________

  ====================================
  AUFGABEN (offen: 3)
  ====================================

  [A001] Steuererklarung abgeben
    Quelle: /Dokumente/TODO.txt:3
    Faelligkeit: 31.03.2026

QUELLEN REGISTRIEREN (sources.json):
  user/decision_briefing/sources.json konfiguriert welche Ordner gescannt werden:

  {
    "sources": [
      {"path": "user/persoenlicher_assistent/", "patterns": ["*.md","*.txt"], "recursive": true},
      {"path": "C:/Users/User/OneDrive/Forschung/", "patterns": ["Plan.txt","*.md"], "recursive": true}
    ]
  }

CLI-BEFEHLE (PLAN):
  bach entscheidung scan                  Alle Quellen scannen, Briefing generieren
  bach entscheidung scan --quelle "/Forschung/"

  bach entscheidung briefing              Offene Entscheidungen anzeigen
  bach entscheidung aufgaben              Offene User-Aufgaben anzeigen
  bach entscheidung log                   Getroffene Entscheidungen

  bach entscheidung session               Interaktive Session (Claude fuehrt durch)
  bach entscheidung decide E001 "Hetzner" Entscheidung direkt eintragen
  bach entscheidung aufgabe-erledigt A001

  bach entscheidung distribute            Alle getroffenen Entscheidungen zurueckverteilen
  bach entscheidung distribute E001       Nur eine Entscheidung

  bach entscheidung source add "/Forschung/" --pattern "Plan.txt" --recursive
  bach entscheidung source list
  bach entscheidung source remove 3

RUECKVERTEILUNG:
  Nach getroffener Entscheidung wird die Quelldatei aktualisiert:

  Vorher:
    ENTSCHEIDUNG: Welchen Server buchen?
    Optionen: Hetzner / AWS

  Nachher:
    ENTSCHEIDUNG: Welchen Server buchen?
    Optionen: Hetzner / AWS
    -> GETROFFEN 2026-02-18: Hetzner CCX33

DATEIEN:
  user/decision_briefing/DECISION_BRIEFING.txt  Aktives Briefing
  user/decision_briefing/AUFGABEN.txt           Offene User-Aufgaben
  user/decision_briefing/sources.json           Scan-Quellen
  user/decision_briefing/entschieden/           Log getroffener Entscheidungen
  user/decision_briefing/archiv/                Monatliche Archiv-Briefings

DATENBANK:
  Optional: decision_items Tabelle in bach.db
  Primaer: Flachdatei-Betrieb (DECISION_BRIEFING.txt)

STATUS:
  Konzept definiert (CONCEPT.md). CLI-Implementierung ausstehend (Phase 2).
  In bach_experts eingetragen (Migration 012).

ZUSAMMENSPIEL:
  user-decide.md:     Fuer komplexe Einzel-Entscheidungen im Briefing
  Notizblock:         Entscheidungs-Kontext und Notizen
  Persoenl. Assistent: Uebergeordneter Boss-Agent

SIEHE AUCH:
  bach help notizblock    Notizen und Notizbuecher
  bach help transkription Transkriptions-Service
  bach help agents        Agenten-Uebersicht
  bach help planning      Planung und Aufgaben


## Features

BACH v2.0 - FEATURES
====================

Uebersicht aller implementierten Features und deren Status.

ARCHITEKTUR v2.0 (NEU)
----------------------
Registry-Based Handler-System mit Auto-Discovery:
- 64+ Handler in hub/ automatisch erkannt
- Library-API (bach_api.py) fuer programmatischen Zugriff
- Dual-Init Handler (Path + App Support)
- Multi-Handler-Dateien (time.py, tuev.py)
- Kognitive Injektoren integriert

Zwei Zugriffswege:
1. CLI:         python bach.py task add "..." --priority P4
2. Library-API: from bach_api import task; task.add("...", "--priority", "P4")

CLI-BEFEHLE (Kern)
------------------
bach --startup              Session starten (mit DirScan, GUI)
bach --shutdown             Session beenden (Memory archivieren)
bach --status               System-Status anzeigen
bach --help [thema]         Hilfe (60+ Themen)

TASK-MANAGEMENT
---------------
bach task add "..."         Neue Aufgabe erstellen
bach task list              Aufgaben anzeigen
bach task done T001         Aufgabe abschliessen
bach task edit T001 "..."   Aufgabe bearbeiten

MEMORY-SYSTEM
-------------
bach mem write "..."        In Memory schreiben
bach mem read               Memory lesen
bach mem context            Kontext anzeigen
bach mem archive            Session archivieren

NACHRICHTEN
-----------
bach msg send "..."         Nachricht senden
bach msg list               Nachrichten anzeigen
bach msg read M001          Nachricht lesen
bach msg unread             Ungelesene anzeigen

SCANNER
-------
bach scan run               Tools scannen
bach scan status            Scan-Status
bach scan tasks             Gescannte Tasks anzeigen

WARTUNG (Daemon)
----------------
bach daemon jobs            Jobs anzeigen
bach daemon run J001        Job ausfuehren
bach daemon toggle J001     Job aktivieren/deaktivieren

GUI & REST-API
--------------
bach gui start              Web-Dashboard starten (Port 8000)
bach gui start-bg           Im Hintergrund starten
bach gui status             Server-Status

REST-API (Headless Server):
  python gui/api/headless.py --port 8001
  Endpoints:
    GET  /api/v1/tasks             Tasks auflisten
    POST /api/v1/tasks             Task erstellen
    GET  /api/v1/memory/facts      Fakten abrufen
    POST /api/v1/messages/send     Nachricht in Queue einreihen
    GET  /api/v1/messages/inbox    Inbox lesen
    GET  /api/v1/status            System-Status
  Swagger Docs: http://localhost:8001/api/docs

INJEKTOREN
----------
bach --inject status        Injektor-Status
bach --inject toggle X      Injektor an/aus
bach --inject task 5        Zeitbudget-Task

BACKUP
------
bach backup create          Backup erstellen
bach backup list            Backups anzeigen
bach backup restore X       Backup wiederherstellen

DATENBANK
---------
bach --db status            DB-Status
bach --db query "SQL"       SQL ausfuehren

CONNECTOR-SYSTEM v2.0 (NEU)
---------------------------
Zuverlaessige Nachrichtenzustellung mit Queue, Retry/Backoff, Circuit Breaker.
Runtime-Adapter: Telegram, Discord, HomeAssistant

bach connector list         Connectors anzeigen
bach connector status       Status aktiver Connectors
bach connector add <type>   Neuen Connector registrieren
bach connector messages     Nachrichten anzeigen
bach connector poll <name>  Einmal pollen (Nachrichten holen)
bach connector dispatch     Queue abarbeiten (Nachrichten versenden)
bach connector queue-status Queue-Statistiken (pending/failed/dead)
bach connector retry [id]   Dead-Letter zuruecksetzen

Daemon-Integration:
  poll_and_route (alle 2min) - Pollen + Routing
  dispatch (alle 1min)        - Queue abarbeiten

Features:
- Retry mit exponentiellen Backoff (30s bis 480s)
- Circuit Breaker (nach 5 Fehlern 5min Cooldown)
- Dead-Letter Queue fuer fehlgeschlagene Nachrichten
- Kontext-Trigger fuer Injektoren beim Routing

VOICE SERVICE (NEU)
-------------------
STT (Speech-to-Text): Whisper (online), Vosk (offline)
TTS (Text-to-Speech): pyttsx3 (Windows SAPI5 / espeak)
Wake-Word: openwakeword (optional), Keyboard-Fallback

Tool-Pfad: system/hub/_services/voice/voice_stt.py
Integration: Kann in Connector-System eingebunden werden

FEATURE-MATRIX
--------------

| Bereich           | Soll | Ist  | Status |
|-------------------|------|------|--------|
| CLI-Befehle       | 20   | 60+  | OK     |
| Help-Themen       | 21   | 60+  | OK     |
| Handler (Registry)| 12   | 64+  | OK     |
| Skills (Datei)    | 30   | 50+  | OK     |
| Skills (JSON)     | 50   | 0    | JSON*  |
| Tools (Datei)     | 30   | 90+  | OK     |
| Tools (Registry)  | 60   | 85   | OK     |
| GUI Endpunkte     | 30   | 80+  | OK     |
| REST-API Endpoints| 10   | 12   | OK     |
| DB Tabellen       | 25   | 114  | OK     |
| Connectors        | 3    | 3+   | OK     |

*) Skills & Experten werden primär über skills_hierarchy.json verwaltet.

Handler (Auto-Discovery in hub/):
  abo, agents, ati, backup, bericht, calendar, chain, connections,
  connector, consolidation, contact, context, cv, daemon, data_analysis,
  db, dist, doc, docs, extensions, fs, gesundheit, gui, haushalt, health,
  help, inbox, inject, lang, lesson, logs, maintain, memory, messages,
  mount, multi_llm_protocol, notify, obsidian, ollama, partner, path,
  profile, profiler, recurring, reflection, routine, scan, session,
  shutdown, skills, smarthome, snapshot, sources, startup, status,
  steuer, sync, task, test, time, tokens, tools, trash, tuev, update,
  versicherung, wiki

IMPLEMENTIERTE GUI DASHBOARDS
-----------------------------
- Startseite (Overview, Tokens, Inbox)
- Skills Board (Agents, Experts, Skills, Tools)
- Memory Board (Working, Facts, Lessons, Sessions)
- Financial (Finanzassistent / Insurance)
- Foerderplaner (Client Pipeline)
- Gesundheit (Gesundheitsassistent - Beta)
- ATI (Konzept-Entwicklung)

GEPLANTE FEATURES
-----------------
- Skill-Sync          Automatischer Abgleich Dateien <-> Hierarchy
- Multi-LLM Shared    Echter Shared Context über verschiedene Modelle
- Autonomous Mode     Agenten können selbstständig Tasks ausführen (Loop)
- Voice Full-Stack    Vollständige Voice-Interface-Integration (STT/TTS/Wake)
- Signal Connector    Erweiterung Connector-System um Signal-Messenger
- WhatsApp Connector  Erweiterung Connector-System um WhatsApp

CHANGELOG v2.0 (2026-02-06 bis 2026-02-08)
-------------------------------------------
[v2.0.0 - 2026-02-08] Registry-Based + Connector v2.0 + Voice
+ Registry-Based Handler-System (Auto-Discovery, 64+ Handler)
+ Library-API (bach_api.py) fuer programmatischen Zugriff
+ Connector-System v2.0: Queue, Retry/Backoff, Circuit Breaker
+ Runtime-Adapter: Telegram, Discord, HomeAssistant
+ Voice Service: STT (Whisper/Vosk), TTS (pyttsx3), Wake-Word
+ REST-API Headless Server (Port 8001, 12 Endpoints)
+ Daemon-Integration (poll_and_route + dispatch Jobs)
+ Schema-Migration mit Retry-Tracking und Circuit Breaker
+ DB-Schema: 114 Tabellen (Single Source of Truth)
+ 50 Tests (test_core + test_smoke) - alle gruen
+ Log-Pfade konsolidiert (nur noch system/data/logs/)
+ _partners Ordner konsolidiert (nur noch system/partners/)

SIEHE AUCH
----------
bach --help gui         Web-Dashboard Details
bach --help tasks       Task-Management
bach --help wartung     Wartung (Jobs/Daemon)
bach --help dirscan     Scanner-System
bach --help connector   Connector-System Details

WEITERE RESSOURCEN
------------------
- Architektur-Doku: docs/con3_ANFORDERUNGSANALYSE.md
- Changelog: memory/MEMORY.md (Abschnitt bach.py v2.0)
- Tests: system/tests/ (test_core.py, test_smoke.py)
- REST-API Swagger: http://localhost:8001/api/docs (wenn Server laeuft)
- Library-API Beispiele: system/bach_api.py (Docstring)


## Formats

DATENFORMATE
============

STAND: 2026-02-08

GRUNDREGEL: DATENBANK VOR JSON
------------------------------
BACH nutzt SQLite (`bach.db`) als primäre Datenhaltung (aktuell 116 Tabellen).
JSON-Dateien sind NUR in begründeten Ausnahmefällen erlaubt.

WANN DATENBANK (STANDARD)?
--------------------------
  - Persistente Systemdaten (Tools, Tasks, Config)
  - Historische Daten (Logs, Sessions, Lessons Learned)
  - Große Datensätze (Wiki, Med-Research)
  - Integrität (Hash-basierte Validierung)

WANN JSON ERLAUBT (AUSNAHMEN)?
------------------------------
1. KOMPLEXE HIERARCHIEN: `system/data/skills_hierarchy.json` (Interaktive Bäume).
2. LOCAL CONFIG: Falls individuell benötigt (z.B. UI-Präferenzen).
3. MCP-CONFIG: Falls Claude Desktop Integration gewünscht.
4. Kurzlebige Prozess-Daten: Temporäre Snapshots bei Bedarf.

ANDERE FORMATE
--------------
  - TOON:   Token-optimierte Datensätze für LLM-Injektion.
  - MD:     Dokumentation und Berichts-Ausgabe (`outbox/`).

MIGRATION JSON -> DB (Erfolgreich durchgeführt)
-----------------------------------------------
- `partner_registry.json` -> `partner_recognition` (Tabelle)
- `connections.json`      -> `connections` (Tabelle)
- `injectors.txt`         -> `automation_injectors` (Tabelle)
- `inbox_folders.txt`     -> `folder_scans` (Tabelle)

KONVERTIERUNG
-------------
  python system/tools/c_universal_converter.py <file> --to [json|yaml|toml|xml|toon]

SIEHE AUCH
----------
  docs/docs/docs/help/maintain.txt    Integritäts-Check und Seal-Mechanismus
  bach --db status     Aktueller Stand der 116 Tabellen


## Gesundheit

GESUNDHEIT - Gesundheitsassistent
=================================

BESCHREIBUNG:
  Der Gesundheitsassistent verwaltet medizinische Daten (Diagnosen,
  Medikamente, Laborwerte, Dokumente, Termine) und Arztkontakte.
  Er dient als zentrales medizinisches Journal.

CLI-BEFEHLE (UEBERSICHT):
  bach gesundheit status             Dashboard anzeigen (Termine, Auffaelligkeiten)
  bach gesundheit contacts           Arzt-Kontakte anzeigen
  bach gesundheit contacts -s <fach> Nach Fachgebiet filtern
  bach gesundheit diagnoses          Aktive Diagnosen
  bach gesundheit diagnoses --all    Alle Diagnosen (inkl. geheilt/widerlegt)
  bach gesundheit meds               Aktive Medikamente
  bach gesundheit meds --all         Alle Medikamente (inkl. abgesetzt)
  bach gesundheit labs               Laborwerte (letzte 50)
  bach gesundheit labs --abnormal    Nur auffaellige Werte
  bach gesundheit labs -t <test>     Nach Test filtern (z.B. -t TSH)
  bach gesundheit docs               Medizinische Dokumente/Befunde
  bach gesundheit docs --type <typ>  Nach Typ filtern (befund|labor|rezept)
  bach gesundheit appointments       Kommende Arzttermine
  bach gesundheit appointments --past Vergangene Termine
  bach gesundheit help               Detaillierte Befehls-Hilfe

VORSORGEUNTERSUCHUNGEN:
  bach gesundheit vorsorge           Alle Vorsorgeuntersuchungen anzeigen
  bach gesundheit vorsorge-faellig   Nur faellige Untersuchungen
  bach gesundheit add-vorsorge "Name" --turnus <monate> --kategorie <typ>
  bach gesundheit vorsorge-done <id> Als erledigt markieren (heute)
  bach gesundheit vorsorge-done <id> --date DD.MM.YYYY

  Beispiele:
    bach gesundheit add-vorsorge "Darmspiegelung" --turnus 120 --kategorie Krebs
    bach gesundheit add-vorsorge "Hautkrebsscreening" --turnus 24 --ab-alter 35
    bach gesundheit vorsorge-done 1 --date 15.01.2026

EXPORT-FUNKTIONEN:
  bach gesundheit export                      Arzt-Kontakte (default)
  bach gesundheit export --entity diagnoses   Diagnosen exportieren
  bach gesundheit export --entity meds        Medikamente exportieren
  bach gesundheit export --entity labs        Laborwerte exportieren
  bach gesundheit export --entity all         Gesundheitspass (alles)
  bach gesundheit export --format csv         Als CSV exportieren
  bach gesundheit export --format vcard       Als vCard 3.0 exportieren
  bach gesundheit export --file <pfad>        In Datei speichern
  bach gesundheit export -s <fach>            Nur bestimmtes Fachgebiet

  Beispiel: bach gesundheit export --entity all --file gesundheitspass.txt

PROAKTIVE FUNKTIONEN:
  bach gesundheit reminders          Erinnerungen (Medikamente, Vorsorge, Termine)
  bach gesundheit interactions       Wechselwirkungs-Check aktiver Medikamente

DATENERFASSUNG (ADD):
  bach gesundheit add-diagnosis "Name" [Optionen]
    Optionen: --icd, --date, --status, --severity, --doctor, --note

  bach gesundheit add-med "Name" [Optionen]
    Optionen: --ingredient, --dosage, --schedule, --diagnosis, --start, --note

  bach gesundheit add-lab "Test" [Optionen]
    Optionen: --value, --unit, --ref-min, --ref-max, --date, --abnormal, --doctor

  bach gesundheit add-doc "Titel" [Optionen]
    Optionen: --type, --file, --summary, --date, --doctor, --diagnosis

  bach gesundheit add-appointment "Titel" [Optionen]
    Optionen: --doctor, --date, --time, --duration, --type, --note

  Tipp: Nutze `bach gesundheit add-... --help` fuer detaillierte Optionen.

  Beispiele:
    bach gesundheit add-diagnosis "Hypothyreose" --icd E03.9 --status aktiv
    bach gesundheit add-med "L-Thyroxin" --dosage 75mcg --schedule morgens
    bach gesundheit add-lab "TSH" --value 2.5 --unit mU/L --ref-min 0.4 --ref-max 4.0
    bach gesundheit add-doc "Blutwerte Jan 2026" --type labor --file /pfad/datei.pdf
    bach gesundheit add-appointment "Kontrolle" --doctor 1 --date 15.02.2026 --time 10:00

DETAILS ANZEIGEN:
  bach gesundheit show <typ> <id>

  Verfuegbare Typen:
    - contact / arzt
    - diagnosis / diagnose
    - med / medication / medikament
    - lab / laborwert
    - doc / dokument
    - appointment / termin
    - vorsorge / checkup

  Beispiele:
    bach gesundheit show contact 1
    bach gesundheit show diagnosis 1
    bach gesundheit show med 1
    bach gesundheit show lab 1
    bach gesundheit show vorsorge 1

DATENBANK:
  Tabellen in bach.db (Unified DB seit v1.1.84):
  - health_contacts (Aerzte)
  - health_diagnoses (Diagnosen, ICD-Codes)
  - health_medications (Medikamente, Dosierung, Einnahmeplan)
  - health_lab_values (Laborwerte, Referenzbereiche)
  - health_documents (Befunde, Arztbriefe)
  - health_appointments (Arzttermine)
  - vorsorge_checks (Vorsorgeuntersuchungen)

INTEGRATION:
  - LifeAssistant: Liest Termine fuer das Daily Briefing.
  - Dokumente: Verknuepft mit Dateien in `user/documents/medical/`.
  - Wechselwirkungs-Check: Basis-Datenbank mit 12 haeufigen Interaktionen.

SIEHE AUCH:
  bach --help abo            (Fuer Fitness-Abos etc.)
  bach --help contact        (Allgemeine Kontakte)


## Git Github

GIT & GITHUB - KURZREFERENZ
============================

STAND: 2026-02-20

Kurzreferenz fuer die wichtigsten Git- und GitHub-Befehle.
Ausfuehrliche Anleitung: BACH_Dev/GITHUB_GUIDE.md

GRUNDBEFEHLE
------------
  git init                         Neues Repository
  git clone <url>                  Repository kopieren
  git status                       Aenderungen anzeigen
  git add <datei>                  Datei stagen
  git add .                        Alles stagen
  git commit -m "Nachricht"        Commit erstellen
  git log --oneline --graph        Historie anzeigen

REMOTE
------
  git remote -v                    Remotes anzeigen
  git push                         Commits hochladen
  git push -u origin <branch>      Branch erstmals hochladen
  git pull                         Aenderungen herunterladen
  git fetch                        Aenderungen holen (ohne Merge)

BRANCHES
--------
  git branch                       Branches auflisten
  git checkout -b <name>           Neuen Branch erstellen + wechseln
  git switch -c <name>             Modern: Erstellen + Wechseln
  git merge <branch>               Branch zusammenfuehren
  git branch -d <name>             Branch loeschen (wenn gemergt)

RUECKGAENGIG
------------
  git restore <datei>              Aenderung verwerfen
  git restore --staged <datei>     Aus Staging entfernen
  git stash                        Aenderungen zwischenspeichern
  git stash pop                    Zwischenspeicher wiederherstellen
  git revert <commit>              Commit rueckgaengig (neuer Commit)

TAGS
----
  git tag -a v1.0.0 -m "Release"  Tag erstellen
  git push origin --tags           Tags hochladen

GITHUB CLI (GH)
---------------
  gh repo clone user/repo          Klonen
  gh pr create                     Pull Request erstellen
  gh pr list                       PRs auflisten
  gh issue create                  Issue erstellen
  gh release create v1.0.0         Release erstellen

STANDARD-WORKFLOW
-----------------
  1. git pull                      Aktuellen Stand holen
  2. git checkout -b feature/xyz   Feature-Branch erstellen
  3. (Dateien bearbeiten)
  4. git add . && git commit -m "feat: ..."
  5. git push -u origin feature/xyz
  6. Pull Request auf GitHub erstellen
  7. Code-Review + Merge
  8. git checkout main && git pull

COMMIT-MESSAGE-FORMAT
---------------------
  feat:     Neues Feature
  fix:      Bugfix
  docs:     Dokumentation
  refactor: Code-Umbau
  test:     Tests
  chore:    Build, Dependencies

HAEUFIGE PROBLEME
-----------------
  Merge-Konflikt:
    1. Datei oeffnen, <<<< / ==== / >>>> Markierungen loesen
    2. git add <datei> && git commit

  Versehentlich auf main committed:
    git branch feature/xyz         # Branch erstellen (Commits bleiben)
    git checkout main
    git reset --hard origin/main   # main zuruecksetzen (VORSICHT!)

  Datei aus Git entfernen (lokal behalten):
    git rm --cached <datei>
    echo "<datei>" >> .gitignore

SIEHE AUCH
----------
  wiki/github_einfuehrung.txt     Ausfuehrliche Grundlagen
  wiki/github_konventionen.txt    Standard-Dateien und Namensregeln
  BACH_Dev/GITHUB_GUIDE.md        Umfassender Guide mit Glossar


## Gui

GUI - Web-Dashboard
===================

BESCHREIBUNG
Das GUI-Modul stellt ein Web-Dashboard fuer BACH bereit.
Basiert auf FastAPI mit HTML/CSS/JS Frontend.
Wird automatisch mit --startup im Hintergrund gestartet.

ZWEI SERVER:
  - GUI Server (Port 8000):    Web-Dashboard mit HTML-Templates
  - Headless API (Port 8001):  Pure REST-API fuer Programme

BEFEHLE
-------
bach gui start              Server starten (blockierend, Port 8000)
bach gui start --port 9000  Server auf anderem Port
bach gui start-bg           Server im Hintergrund starten
bach gui start-bg --port 9000  Hintergrund mit anderem Port
bach gui status             Server-Status pruefen
bach gui info               GUI-Informationen anzeigen

MANUELLER START
---------------
user/start_gui.bat          Batch-Datei fuer Windows (oeffnet Browser)

AUTOMATISCHER START
-------------------
bach --startup              Startet GUI automatisch im Hintergrund
                            (siehe [GUI SERVER] Sektion im Output)

VORAUSSETZUNGEN
---------------
pip install fastapi uvicorn

DASHBOARDS (Basis)
------------------
/              Startseite mit Status-Cards und Quick-Actions
/tasks         Task-Management (Filter, CRUD, Status-Wechsel)
/messages      Nachrichten (Inbox/Outbox, Compose)
/daemon        Wartung (Jobs, Runs, Toggle)
/docs          API-Dokumentation (Swagger)

DASHBOARDS (Erweitert)
----------------------
/agents        Agent-Verwaltung
/memory        Memory/Wissensbasis
/tools         Tool-Verwaltung
/tokens        Token-Statistik
/steuer        Steuer-Workflows
/financial     Finanz-Uebersicht
/gesundheit    Gesundheits-Tracking
/kontakte      Kontaktverwaltung
/routinen      Routinen-Editor
/skills-board  Skills-Board
/tasks_board   Kanban Task-Board
/logs          Log-Viewer
/help          Help-System
/wiki          Wiki-Seiten
/inbox         Inbox-Ansicht
/inbox_editor  Inbox-Editor
/maintenance   Wartungs-Dashboard
/partners      Partner-Verwaltung
/persoenlich   Persoenliche Einstellungen
/ati           ATI-System
/usecases      Use-Cases
/workflow_tuev Workflow-Pruefung
/prompt-generator  Prompt-Generator
/foerderplaner Foerderplaner
/anonymization Anonymisierung

FEATURES
--------
- Dashboard mit System-Status
- Task-Uebersicht (User + Gescannte)
- Message-System (CLI-Anbindung: bach msg)
- Wartungs-Jobs
- REST-API mit automatischer Dokumentation (/docs)

CLI <-> GUI VERKNUEPFUNG
------------------------
Nachrichten:
  CLI: bach msg send/list/read/unread
  GUI: /messages (Inbox/Outbox, Compose)
  DB:  bach.db -> messages Tabelle
  Startup: Ungelesene werden bei --startup angezeigt

Tasks:
  CLI: bach task add/list/done
  GUI: /tasks (CRUD, Filter, Status)
  DB:  bach.db -> tasks Tabelle

Wartung:
  CLI: bach daemon list/run/toggle
  GUI: /daemon (Jobs, Runs, Toggle)
  DB:  bach.db -> daemon_jobs, daemon_runs


STRUKTUR
--------
gui/
├── server.py          FastAPI Backend (alle APIs integriert)
├── daemon_service.py  Hintergrund-Service
├── prompt_manager.py  Prompt-Verwaltung
├── file_watcher.py    Datei-Ueberwachung
├── sync_service.py    Synchronisation
├── api_webhook.py     Webhook-Handler
├── __init__.py        Modul-Init
├── static/
│   ├── css/main.css   Styling
│   └── js/
│       ├── api.js     API-Client
│       ├── app.js     Haupt-Logik
│       ├── nav.js     Navigation
│       └── skills-board.js  Skills-Board Logik
└── templates/
    ├── index.html     Startseite
    ├── tasks.html     Task-Management
    ├── messages.html  Nachrichten
    ├── daemon.html    Daemon-Manager
    └── ... (30+ weitere Templates)

API-ENDPUNKTE (GUI SERVER - Port 8000)
---------------------------------------
Status:
GET  /api/status              System-Status

Tasks:
GET  /api/tasks               User-Tasks
POST /api/tasks               Task erstellen
POST /api/tasks/export        Tasks exportieren
GET  /api/tasks/{id}          Task Details
PUT  /api/tasks/{id}          Task aktualisieren
DELETE /api/tasks/{id}        Task loeschen
GET  /api/scanned-tasks       Gescannte Tasks
GET  /api/assignees           Task-Zuweisungen

Nachrichten (CLI-Verwaltung):
GET  /api/messages            Nachrichten (messages Tabelle)
POST /api/messages            Nachricht erstellen
PUT  /api/messages/{id}/read  Als gelesen markieren
PUT  /api/messages/{id}/archive  Nachricht archivieren
PUT  /api/messages/{id}/delete   Nachricht loeschen

Daemon:
GET  /api/daemon/jobs         Daemon-Jobs
POST /api/daemon/jobs         Job erstellen
PUT  /api/daemon/jobs/{id}/toggle  Job aktivieren/deaktivieren
POST /api/daemon/jobs/{id}/run     Job manuell ausfuehren
GET  /api/daemon/runs         Job-Ausfuehrungen
GET  /api/daemon/status       Daemon-Status
POST /api/daemon/start        Daemon starten
POST /api/daemon/stop         Daemon stoppen
POST /api/daemon/kill-all     Alle Jobs beenden
PUT  /api/daemon/config       Daemon-Konfiguration aendern

Memory:
GET  /api/memory/overview     Memory-Uebersicht
GET  /api/memory/working      Working Memory
GET  /api/memory/lessons      Lessons
GET  /api/memory/facts        Fakten
GET  /api/memory/sessions     Sessions
POST /api/memory/working      Working Memory Entry erstellen
POST /api/memory/lessons      Lesson erstellen
POST /api/memory/facts        Fakt erstellen
DELETE /api/memory/facts/{id}       Fakt loeschen
DELETE /api/memory/working/{id}     Working Entry loeschen
DELETE /api/memory/lessons/{id}     Lesson loeschen
GET  /api/memory/stats/db     DB-Statistiken
POST /api/memory/maintenance/cleanup  Memory-Cleanup
GET  /api/memory/sessions/{id}       Session-Details

Skills:
GET  /api/skills              Skills auflisten
GET  /api/skills/categories   Skill-Kategorien
GET  /api/skills/{id}         Skill-Details

Tools:
GET  /api/tools               Tools auflisten
GET  /api/tools/{name}        Tool-Details
POST /api/tools/{name}/run    Tool ausfuehren

Agents:
GET  /api/agents              Agent-Liste
PUT  /api/agents/{id}/toggle  Agent aktivieren/deaktivieren

ATI:
GET  /api/ati/stats           ATI-Statistiken
GET  /api/ati/tasks           ATI-Tasks
GET  /api/ati/tasks/{id}      ATI-Task-Details
GET  /api/ati/sessions        ATI-Sessions
POST /api/ati/session/start   ATI-Session starten
POST /api/ati/session/start-cli  ATI CLI-Session
POST /api/ati/tasks           ATI-Task erstellen
PUT  /api/ati/tasks/{id}      ATI-Task aktualisieren
DELETE /api/ati/tasks/{id}    ATI-Task loeschen

Financial:
GET  /api/financial/status    Financial-Status
GET  /api/financial/emails    Financial-Emails
GET  /api/financial/emails/{id}  Email-Details
GET  /api/financial/subscriptions  Abonnements
GET  /api/financial/subscriptions-unified  Vereinigte Abos
DELETE /api/financial/subscriptions/{id}  Abo loeschen
GET  /api/financial/categories  Kategorien
POST /api/financial/sync      Financial-Sync
POST /api/financial/save-json  JSON speichern
GET  /api/financial/config    Financial-Config
PUT  /api/financial/config    Config aktualisieren
PUT  /api/financial/emails/{id}/status  Email-Status aendern
GET  /api/financial/export    Financial exportieren
GET  /api/financial/accounts  Email-Accounts
POST /api/financial/accounts  Account erstellen
PUT  /api/financial/accounts/{id}/toggle  Account aktivieren
POST /api/financial/accounts/{id}/test  Account testen
DELETE /api/financial/accounts/{id}  Account loeschen
GET  /api/financial/imap-presets  IMAP-Presets
GET  /api/financial/gmail/find-credentials  Gmail-Credentials
POST /api/financial/gmail/setup  Gmail-Setup
GET  /api/financial/gmail/status  Gmail-Status
GET  /api/financial/profiles  Profile
POST /api/financial/profiles  Profil erstellen
PUT  /api/financial/profiles/{id}  Profil aktualisieren
DELETE /api/financial/profiles/{id}  Profil loeschen
GET  /api/financial/false-positives  False-Positives
POST /api/financial/false-positives  False-Positive erstellen
DELETE /api/financial/false-positives/{id}  False-Positive loeschen
POST /api/financial/profiles/test  Profil testen
POST /api/financial/profiles/import  Profile importieren
GET  /api/financial/contracts  Vertraege
POST /api/financial/contracts  Vertrag erstellen
PUT  /api/financial/contracts/{id}  Vertrag aktualisieren
DELETE /api/financial/contracts/{id}  Vertrag loeschen
GET  /api/financial/insurances  Versicherungen
GET  /api/financial/deadlines  Deadlines
POST /api/financial/insurances  Versicherung erstellen
PUT  /api/financial/insurances/{id}  Versicherung aktualisieren
DELETE /api/financial/insurances/{id}  Versicherung loeschen
GET  /api/financial/bank-accounts  Bank-Accounts
POST /api/financial/bank-accounts  Bank-Account erstellen
PUT  /api/financial/bank-accounts/{id}  Bank-Account aktualisieren
DELETE /api/financial/bank-accounts/{id}  Bank-Account loeschen
GET  /api/financial/credits  Kredite
POST /api/financial/credits  Kredit erstellen
PUT  /api/financial/credits/{id}  Kredit aktualisieren
DELETE /api/financial/credits/{id}  Kredit loeschen

Steuer:
GET  /api/steuer/dokumente/unlinked  Unverlinkte Steuer-Dokumente
POST /api/steuer/posten/{id}/link  Dokument verlinken
POST /api/steuer/match-bank  Bank-Matching

Bericht (Foerderplaner):
GET  /api/bericht/status      Bericht-Status
GET  /api/bericht/clients     Klienten
POST /api/bericht/export      Bericht exportieren
POST /api/bericht/generate    Bericht generieren

Mounts:
GET  /api/mounts              Mounts auflisten
POST /api/mounts              Mount erstellen
DELETE /api/mounts/{alias}    Mount loeschen
POST /api/mounts/restore      Mounts wiederherstellen

Scanner:
POST /api/scanner/trigger     Scanner ausloesen
POST /api/scanner/run         Scanner starten
GET  /api/scanner/status      Scanner-Status
GET  /api/scanner/tools       Scanner-Tools
GET  /api/scanner/config      Scanner-Config

Wartung:
POST /api/wartung/trigger     Wartung ausloesen
GET  /api/wartung/status      Wartungs-Status

Tokens:
GET  /api/tokens/usage        Token-Nutzung

Logs:
GET  /api/system/logs         Log-Dateien
GET  /api/system/logs/{name}  Log-Datei lesen

Inbox:
GET  /api/inbox/status        Inbox-Status
GET  /api/inbox/config        Inbox-Config
POST /api/inbox/config        Config aktualisieren
GET  /api/inbox/folders       Ordner
POST /api/inbox/folders       Ordner erstellen
PUT  /api/inbox/folders       Ordner aktualisieren
DELETE /api/inbox/folders     Ordner loeschen
GET  /api/inbox/rules         Regeln
POST /api/inbox/rules         Regel erstellen
PUT  /api/inbox/rules/{id}    Regel aktualisieren
DELETE /api/inbox/rules/{id}  Regel loeschen
POST /api/inbox/scan          Inbox scannen
GET  /api/inbox/unsorted      Unsortierte Elemente
POST /api/inbox/sort          Elemente sortieren
GET  /api/inbox/preview/{file}  Datei-Vorschau
GET  /api/inbox/analyze/{file}  Datei analysieren
PUT  /api/inbox/settings      Settings aktualisieren

Skills-Board:
GET  /api/skills-board/item-file  Item-Datei lesen
PUT  /api/skills-board/item-file  Item-Datei speichern
GET  /api/skills-board/hierarchy  Hierarchie lesen
PUT  /api/skills-board/hierarchy  Hierarchie speichern

Help-System:
GET  /api/help               Help-Dateien auflisten
GET  /api/docs/docs/docs/help/{name}        Help-Datei lesen
PUT  /api/docs/docs/docs/help/{name}        Help-Datei aktualisieren
POST /api/help               Help-Datei erstellen
DELETE /api/docs/docs/docs/help/{name}      Help-Datei loeschen
GET  /api/docs/docs/docs/help/search/{term} Help durchsuchen

Anonymization (Foerderplaner):
GET  /api/anonymization/clients  Klienten
POST /api/anonymization/profile  Profil erstellen
POST /api/anonymization/upload  Dokument hochladen
POST /api/report/session/start  Bericht-Session starten
POST /api/report/session/{id}/import  Import
POST /api/report/session/{id}/profile  Profil
POST /api/report/session/{id}/anonymize  Anonymisieren
POST /api/report/session/{id}/prompt  Prompt
POST /api/report/session/{id}/generate  Generieren
POST /api/report/session/{id}/cleanup  Cleanup
GET  /api/report/session/{id}  Session-Details
GET  /api/report/pending      Pending Reports

Prompt-Generator:
GET  /api/prompt-generator/templates  Templates
GET  /api/prompt-generator/template/{path}  Template lesen
POST /api/prompt-generator/send/task  Als Task senden
POST /api/prompt-generator/send/session  In Session senden
POST /api/prompt-generator/send/copy  In Zwischenablage
GET  /api/prompt-generator/daemon/status  Daemon-Status
PUT  /api/prompt-generator/daemon/config  Daemon-Config
POST /api/prompt-generator/start-desktop  Desktop starten
POST /api/prompt-generator/daemon/toggle  Daemon-Toggle
POST /api/prompt-generator/templates/save  Template speichern

Auto-Sessions:
POST /api/auto-sessions/launch  Session starten

Session:
GET  /api/session/activities  Aktivitaeten
POST /api/session/generate-summary  Summary generieren
POST /api/session/end        Session beenden

Recurring:
GET  /api/recurring           Wiederkehrende Tasks
POST /api/recurring/check    Check ausfuehren
POST /api/recurring/trigger/{id}  Task ausloesen

Use-Cases:
GET  /api/usecases            Use-Cases
GET  /api/usecases/{id}       Use-Case-Details
POST /api/usecases            Use-Case erstellen
PUT  /api/usecases/{id}       Use-Case aktualisieren
DELETE /api/usecases/{id}     Use-Case loeschen
POST /api/usecases/{id}/test  Use-Case testen
POST /api/usecases/test-all   Alle testen
POST /api/usecases/{id}/execute  Use-Case ausfuehren

Kontakte:
GET  /api/contacts            Kontakte
GET  /api/contacts/{id}       Kontakt-Details
POST /api/contacts            Kontakt erstellen
PUT  /api/contacts/{id}       Kontakt aktualisieren
DELETE /api/contacts/{id}     Kontakt loeschen
GET  /api/contacts/export     Kontakte exportieren

Routinen:
GET  /api/routines            Routinen
GET  /api/routines/{id}       Routinen-Details
POST /api/routines            Routine erstellen
PUT  /api/routines/{id}       Routine aktualisieren
POST /api/routines/{id}/complete  Routine abschliessen
DELETE /api/routines/{id}     Routine loeschen
GET  /api/routines/export     Routinen exportieren

WebSockets:
GET  /api/ws/status           WebSocket-Status

Workflow-TÜV:
GET  /api/workflow-tuev       Workflows
POST /api/workflow-tuev/{id}/check  Workflow pruefen
POST /api/workflow-tuev/check-all  Alle pruefen
POST /api/workflow-tuev/sync  Workflows synchronisieren
GET  /api/workflow-tuev/content  Workflow-Content

AI Headless:
POST /api/ai/headless/run     AI-Task ausfuehren

Bach-Agents:
GET  /api/bach-agents         Bach-Agents auflisten


HEADLESS API (Port 8001) - Programmatischer Zugriff
-----------------------------------------------------
Zweck: Pure REST-API ohne HTML, fuer Skripte/Programme

Auth:
  - Localhost (127.0.0.1, ::1, localhost): Kein Auth noetig (Trust-Modus)
  - Remote: X-BACH-Key Header ODER ?api_key= Parameter
  - Key: Auto-generiert beim ersten Start → data/.api_key

Start:
  python gui/api/headless.py [--port 8001] [--key YOUR_KEY]

Dokumentation:
  http://localhost:8001/api/docs (Swagger)
  http://localhost:8001/api/redoc (ReDoc)

Endpoints (Prefix: /api/v1):

Tasks:
GET  /api/v1/tasks             Tasks auflisten (Filter: status, priority, limit)
POST /api/v1/tasks             Task erstellen
GET  /api/v1/tasks/{id}        Task-Details
PUT  /api/v1/tasks/{id}        Task aktualisieren

Memory:
GET  /api/v1/memory/facts      Fakten (Filter: category, min_confidence)
GET  /api/v1/memory/lessons    Lessons (Filter: category, limit)
GET  /api/v1/memory/search     Memory durchsuchen (Parameter: q)
POST /api/v1/memory            Memory-Eintrag erstellen

Messages (Queue + Inbox):
POST /api/v1/messages/send     Nachricht in Queue einreihen (connector_messages)
GET  /api/v1/messages/queue    Queue-Status (pending/failed/dead pro Connector)
GET  /api/v1/messages/inbox    Inbox lesen (Filter: status, sender, Paginierung)
POST /api/v1/messages/route    Routing manuell ausloesen (in → inbox)

System:
GET  /api/v1/status            System-Status (Tasks, Memory, DB-Size)
POST /api/v1/backup            Backup erstellen
GET  /api/v1/skills            Skills auflisten (Filter: type, limit)
GET  /api/v1/health            Health-Check (oeffentlich, kein Auth)

BEISPIELE
---------
GUI Server (Port 8000):
  # Server im Hintergrund starten
  bach gui start-bg

  # Oder: Server starten (blockierend)
  bach gui start

  # Browser oeffnen
  http://127.0.0.1:8000

  # API-Dokumentation
  http://127.0.0.1:8000/docs

  # Server auf anderem Port
  bach gui start --port 9000

  # Status pruefen
  bach gui status

Headless API (Port 8001):
  # Server starten
  python gui/api/headless.py --port 8001

  # Mit Custom API-Key
  python gui/api/headless.py --key MEIN_KEY

  # API-Docs
  http://localhost:8001/api/docs

  # Task erstellen (localhost = kein Auth)
  curl -X POST http://localhost:8001/api/v1/tasks \
       -H "Content-Type: application/json" \
       -d '{"title": "Test", "priority": "P2"}'

  # Von Remote mit API-Key
  curl -X GET http://REMOTE:8001/api/v1/status \
       -H "X-BACH-Key: YOUR_KEY"

  # Nachricht senden
  curl -X POST http://localhost:8001/api/v1/messages/send \
       -H "Content-Type: application/json" \
       -d '{"connector": "signal", "recipient": "+49...", "content": "Test"}'

  # Queue-Status
  curl http://localhost:8001/api/v1/messages/queue

  # Inbox lesen
  curl "http://localhost:8001/api/v1/messages/inbox?status=unread&limit=20"

SIEHE AUCH
----------
bach --help wartung         Wartungs-Jobs
bach --help tasks           Task-Verwaltung
bach --help messages        Nachrichten-CLI
bach --help connector       Connector-System
gui/api/headless.py         Headless API Source
gui/api/messages_api.py     Messages-API Router


## Guidelines

GUIDELINES - Dokumentations-Standards
=====================================

STAND: 2026-02-08

DREISTUFIGES SYSTEM
-------------------
1. OPERATIV (docs/docs/docs/help/*.txt)
   - WIE benutze ich BACH?
   - Fokus: CLI-Befehle, Anleitungen, Referenzen.
   - Format: TXT (ASCII-kompatibel, max. 250 Zeilen).

2. WISSEN (wiki/*.txt)
   - WAS ist X?
   - Fokus: Hintergrundwissen, Domänen-Wissen, KI-Theorie.
   - Format: TXT (ASCII-kompatibel).

3. KONZEPTIONELL (skills/**/*.md, docs/*.md)
   - WARUM & WIE ist es gebaut?
   - Fokus: Architekturen, Workflows, tiefere Analysen.
   - Format: MarkDown (reich bebildert/strukturiert).

METADATEN-PFLICHT (NEU 2026-01)
-------------------------------
Jede Dokumentationsdatei MUSS folgenden Header haben:

  # Portabilitaet: UNIVERSAL | SYSTEM | USER
  # Zuletzt validiert: YYYY-MM-DD
  # Naechste Pruefung: YYYY-MM-DD
  # Quellen: [Optional]

Pruefungs-Intervalle:
  SYSTEM:    +3 Monate  (code-gekoppelt, aendert sich haeufig)
  UNIVERSAL: +6 Monate  (allgemein gueltig, stabil)
  USER:      +12 Monate (nutzer-spezifisch, langlebig)

TX/TXT-STRUKTUR (Klassisch)
---------------------------
  TITEL IN GROSSBUCHSTABEN
  ========================
  [Metadaten-Header]

  BESCHREIBUNG
  [Was macht dieses Feature]

  BEFEHLE
  bach [befehl] [argumente]

  BEISPIELE
  [Konkrete Anwendungsfälle]

  SIEHE AUCH
  [Links zu anderen docs/docs/docs/help/ oder wiki/ Dateien]

LEBENSZYKLUS ANALYSEN
---------------------
1. ERSTELLUNG: user/ANALYSE_Thema.md
2. AUSWERTUNG: Erkenntnisse → docs/docs/docs/help/ ODER wiki/. Aufgaben → Tasksystem.
3. ARCHIVIERUNG: Verschieben nach user/_archive/ nach Abschluss.

NAMING CONVENTIONS
------------------
docs/docs/docs/help/<thema>.txt          Einfaches Thema
docs/docs/docs/help/<befehl>.txt         CLI-Befehl-Dokumentation
wiki/<spezial>.txt   Externes Wissen

SKILL_<n>.md              Skill-Dokumentation
KONZEPT_<n>.md            Konzept-Dokument
<n>_ANALYSE.md            Analyse-Bericht
<Thema>_Vorschlag.md      Vorschlaege (awaiting approval)

QUALITAETSKRITERIEN
-------------------
docs/docs/docs/help/*.txt Dateien:
- Max. 250 Zeilen (empfohlen unter 150)
- Keine Markdown-Syntax (ASCII-kompatibel)
- Alle Befehle dokumentiert
- Mindestens 1 Beispiel
- SIEHE AUCH Verweis

SIEHE AUCH
----------
user/_archive/Guidelines_Vorschlag.md    Vollstaendiges Konzept (archiviert)
bach --help practices                    Architektur-Prinzipien
bach --help naming                       Naming Conventions


## Help

HELP - Das BACH Hilfe-System
=============================

BESCHREIBUNG
Das help-System bietet kontextbezogene Dokumentation fuer alle BACH-Komponenten.
Jedes Thema hat eine eigene .txt Datei im docs/help/-Verzeichnis.

CLI-BEFEHLE
-----------
bach --help                 Alle verfuegbaren Themen anzeigen
bach --help [thema]         Hilfe zu einem bestimmten Thema
bach --help tasks           Beispiel: Hilfe zum Task-System
bach --help steuer          Beispiel: Hilfe zum Steuer-Agenten
bach --help tools/name      Beispiel: Hilfe aus Unterordner
bach --help tool_name       Beispiel: Tool-Info aus Datenbank

VERFUEGBARE THEMEN
------------------
System:         startup, shutdown, architecture, features
Tasks:          tasks, between-tasks, planning, workflow
Memory:         memory, lessons, logs, sources
Agenten:        agents, actors, communicate, partners
Tools:          tools, maintain, backup, distribution
Daten:          dirscan, trash
GUI:            gui, wartung, prompt-generator, recurring
Spezial:        steuer, coding, bugfix, injectors
Extern:         vendor, cookbooks
Sonstiges:      identity, naming, practices, formats, emoji

STRUKTUR EINER HELP-DATEI
-------------------------
1. TITEL - Name in Grossbuchstaben
2. BESCHREIBUNG - Was macht diese Komponente?
3. CLI-BEFEHLE - Welche Befehle gibt es?
4. WEITERE SEKTIONEN - Konzepte, Beispiele, Tipps

NEUE HELP-DATEI ERSTELLEN
-------------------------
1. Datei unter docs/help/[thema].txt anlegen
2. Format von bestehender Datei uebernehmen
3. Mindestens: Titel, Beschreibung, CLI-Befehle
4. Registrierung in bach --help automatisch

HELP-DATEIEN VS ANDERE DOCS
---------------------------
docs/help/*.txt CLI-Referenz, schnelle Nachschau
skills/*.md     Agenten-Profile, komplexe Konzepte
docs/*.md       Entwickler-Dokumentation, Konzepte
SKILL.md        Haupt-Einstiegspunkt

BEST PRACTICES
--------------
- Kurz und praegnant halten (unter 100 Zeilen)
- CLI-Befehle immer zuerst dokumentieren
- Beispiele sind hilfreicher als Theorie
- Bei Aenderungen: help-Datei mitaktualisieren

WIKI & ERWEITERUNGEN
--------------------
Das wiki/-Unterverzeichnis enthaelt erweiterte Dokumentation:
wiki/*.txt

Unterordner-Zugriff:
  bach --help tools/python_cli_editor
  bach --help wiki/antigravity

Tool-Datenbank-Zugriff (NEU v1.1.38):
  bach --help path_healer     Tool-Info aus bach.db
  bach --help tool_scanner    Zeigt Typ, Pfad, Capabilities

Skill-Aliase (NEU v1.1.85):
  bach --help agent/ati       Zeigt agents/ati/ATI.md
  bach --help workflow/bugfix Zeigt skills/workflows/bugfix-protokoll.md
  bach --help expert/steuer   Zeigt agents/_experts/steuer/STEUER.md

SIEHE AUCH
----------
bach --help tasks           Task-System
bach --help memory          Memory-System
bach --help agents          Agenten-System
SKILL.md                    Hauptdokumentation


## Hooks

BACH HOOK-FRAMEWORK
===================

Stand: 2026-02-13

Hooks sind ein erweiterbares Event-System fuer BACHs Lifecycle.
Sie erlauben es, eigene Logik an zentrale System-Events anzuhaengen,
OHNE bestehenden Code zu aendern.

WICHTIG: HOOKS != INJEKTOREN
-----------------------------
  Hooks     = Technisches Framework (Lifecycle-Events, Plugin-Integration)
  Injektoren = Kognitives Subsystem (Denksimulation, kognitive Entlastung)

Hooks und Injektoren arbeiten unabhaengig voneinander.
Injektoren bleiben als eigenstaendiges Subsystem erhalten.

VERFUEGBARE EVENTS (17)
------------------------
  Event                    Wann                            Kontext-Keys
  ----------------------   ----------------------------    -------------------------
  before_startup           Vor dem Startup-Protokoll       partner, mode, quick
  after_startup            Nach erfolgreichem Startup      partner, mode, success
  before_shutdown          Vor dem Shutdown-Protokoll       partner, mode
  after_shutdown           Nach dem Shutdown                partner, mode, success
  before_command           Vor jedem CLI-Befehl            handler, operation, args
  after_command            Nach jedem CLI-Befehl           handler, operation, success, args
  after_task_create        Nach Task-Erstellung            task_id, title
  after_task_done          Nach Task-Abschluss             task_id, title
  after_task_delete        Nach Task-Loeschung             task_id
  after_memory_write       Nach Memory-Eintrag             type, content
  after_lesson_add         Nach Lesson-Erstellung          lesson_id, title, category, severity
  after_skill_create       Nach Skill-Erstellung           name, type, path
  after_skill_reload       Nach Hot-Reload                 handler_count
  after_plugin_load        Nach Plugin-Laden               name, version, hooks, handlers
  after_plugin_unload      Nach Plugin-Entladen            name
  after_capability_denied  Nach verweigerter Capability    plugin, capability, reason
  after_email_send         Nach E-Mail-Versand             draft_id, recipient

CLI-BEFEHLE
-----------
  bach hooks status            Status aller Hooks und Listener
  bach hooks events            Alle Events mit Beschreibung auflisten
  bach hooks log               Letzte Hook-Ausfuehrungen anzeigen
  bach hooks test <event>      Test-Event emittieren (Debugging)

  Kurzform:
  bach hook status             (Alias: hook -> hooks)

API-NUTZUNG
-----------
  from core.hooks import hooks

  # Listener registrieren
  def mein_handler(context):
      print(f"Task erstellt: {context['task_id']}")
      return "verarbeitet"  # Optional

  hooks.on('after_task_create', mein_handler, name='mein_plugin')

  # Listener mit Prioritaet (niedriger = frueher, default=50)
  hooks.on('after_startup', check_updates, priority=10, name='updater')

  # Listener entfernen
  hooks.off('after_task_create', name='mein_plugin')

  # Event manuell emittieren
  results = hooks.emit('after_task_create', {'task_id': 42, 'title': 'Test'})

  # Status abfragen
  print(hooks.status())

  # Pruefen ob Event Listener hat
  if hooks.has_listeners('after_startup'):
      print("Startup wird ueberwacht")

EIGENE HOOKS REGISTRIEREN
--------------------------
AI-Partner koennen eigene Hooks registrieren um BACH zu erweitern:

  from core.hooks import hooks

  # Beispiel: Auto-Backup nach jedem Task-Abschluss
  def auto_backup_nach_task(ctx):
      from bach_api import backup
      backup.create()
      return f"Backup nach Task #{ctx['task_id']}"

  hooks.on('after_task_done', auto_backup_nach_task, name='auto_backup')

  # Beispiel: Benachrichtigung bei Startup
  def startup_notification(ctx):
      from bach_api import msg
      msg.send("user", f"Session gestartet ({ctx['partner']})")

  hooks.on('after_startup', startup_notification, name='notify')

SICHERHEIT
----------
  - Hooks sind in try/except gekapselt: Ein fehlerhafter Listener
    blockiert NIEMALS die eigentliche Operation
  - Listener erhalten nur Lese-Kontext (dict), keinen Schreibzugriff
  - Priorisierung verhindert Reihenfolge-Konflikte
  - Hook-Log (bach hooks log) fuer Debugging

ARCHITEKTUR
-----------
  core/hooks.py        HookRegistry-Singleton (Framework)
  hub/hooks.py         CLI-Handler (bach hooks ...)
  core/app.py          Emittiert before/after_command
  hub/startup.py       Emittiert before/after_startup
  hub/shutdown.py      Emittiert before/after_shutdown
  hub/task.py          Emittiert after_task_create/done
  hub/memory.py        Emittiert after_memory_write
  hub/lesson.py        Emittiert after_lesson_add
  hub/skills.py        Emittiert after_skill_create/reload
  core/plugin_api.py   Emittiert after_plugin_load/unload
  core/capabilities.py Emittiert after_capability_denied

SIEHE AUCH
----------
  bach help cli              CLI-Konventionen
  bach help skills           Skill-System
  bach help self-extension   Selbsterweiterungs-Workflow
  bach --inject status       Injektor-System (separates Subsystem)


## Identity

IDENTITY-SYSTEM
===============

Stand: 2026-02-08

Das Identity-System gewaehrleistet die Integritaet und Identifikation der BACH-Instanz.
Funktionen sind im Distribution-Handler implementiert, aber das CLI-Routing ist defekt.

TABELLE: system_identity (Zentrales Singleton)
----------------------------------------------
  - id:               Primary Key (MUSS 1 sein - Singleton)
  - instance_id:      Eindeutige UUID der Installation
  - instance_name:    Individueller Name (z.B. "BACH_Alpha")
  - version:          Aktuelle BACH-Version (z.B. v1.1.83)
  - created_at:       Erstellungsdatum
  - seal_status:      Integritaets-Status ('intact' | 'broken')
  - kernel_hash:      SHA256 der System-Kern-Dateien
  - last_verified:    Letzter Verifizierungs-Zeitpunkt
  - current_mode:     Betriebsmodus (default: 'developer')
  - last_boot:        Letzter Boot-Zeitpunkt
  - boot_count:       Anzahl Boots (default: 0)

SIEGEL-MECHANISMUS
------------------
  1. Boot-Check: Bei jedem Startup wird der Kernel-Hash berechnet
  2. Vergleich: Stimmt der Hash mit der DB ueberein?
  3. Status: Bei Abweichung wird das Siegel "gebrochen" (broken)
  4. Warnung: Ein gebrochenes Siegel weist auf manuelle Eingriffe hin

CLI-BEFEHLE (DOKUMENTIERT, aber DEFEKT)
----------------------------------------
  bach --dist status         System-Status mit Siegel-Info anzeigen
  bach --dist verify         Siegel-Integritaet pruefen

PROBLEM: Der dist-Handler (hub/dist.py) existiert und implementiert diese
Funktionen, aber das CLI-Routing in bach.py ruft ihn nicht korrekt auf.
Nur "bach dist list" funktioniert.

NICHT IMPLEMENTIERT
-------------------
  bach --dist reseal         (EXISTIERT NICHT - keine Reseal-Funktion)

Bei gebrochenem Siegel gibt es keinen automatischen Repair. Man muss manuell
via distribution_system.py ein neues Siegel setzen.

IMPLEMENTATION
--------------
  Handler:        system/hub/dist.py (DistHandler)
  Backend:        system/tools/generators/distribution_system.py
  Operations:     status, verify, scan, snapshot, release, restore, install, list
  Funktioniert:   Nur "list" - alle anderen Operationen werden nicht geroutet

KONTEXT
-------
Identity ist Teil des Distribution-Systems (ehemals Governance-Schicht 5).
Sie stellt sicher dass das "Gedaechtnis" (DB) zur "Hardware" (Dateisystem) passt.

SIEHE AUCH
----------
  docs/docs/docs/help/maintain.txt        Wartungs-Tools (keine Identity-Funktion)
  docs/docs/docs/help/distribution.txt    Distribution & Releases
  docs/docs/docs/help/bach_info.txt       System-Uebersicht


## Inbox

BACH INBOX-SYSTEM
=================

Automatisierte Dokumenten-Sortierung mit Watchdog-Ueberwachung.

KONZEPT
-------

Das Inbox-System ueberwacht Eingangsordner (Downloads, Scans) und
sortiert Dateien automatisch nach Regeln in Zielordner.

KONFIGURATION
-------------

Zwei Dateien steuern das System:

  data/inbox_folders.txt     Watch-Ordner (Quellen)
  data/inbox_config.json     Sortier-Regeln

INBOX_FOLDERS.TXT FORMAT
------------------------

  # Format: PFAD | MODUS | FILTER | ZIEL
  C:\Users\User\Downloads | auto | pdf | inbox
  C:\Users\User\Scans | manual | pdf,jpg | inbox

  MODUS: auto (automatisch sortieren) oder manual (nur sammeln)
  FILTER: Dateiendungen (kommasepariert) oder * fuer alle
  ZIEL: inbox (Transfer-Zone) oder relativer BACH-Pfad

INBOX_CONFIG.JSON
-----------------

  settings:
    enabled: true/false
    interval_seconds: 60
    transfer_zone: user/inbox/unsortiert
    ocr_enabled: false
    auto_task_on_unknown: true

  rules:
    - id: steuer_rechnung
      pattern: rechnung|invoice|beleg
      pattern_type: filename|content|ocr
      target: user/steuer/{year}/belege/Weitere
      priority: 1

ORDNER
------

  user/inbox/           Transfer-Zone (Eingang)
  user/inbox/unsortiert Nicht zuordenbare Dateien

CLI-BEFEHLE
-----------

  bach inbox status      Status anzeigen
  bach inbox start       Inbox-Watcher starten (Hintergrund)
  bach inbox stop        Inbox-Watcher stoppen
  bach inbox scan        Einmaliger Dry-Run Scan
  bach inbox config      Konfiguration anzeigen

DAEMON-INTEGRATION
------------------

Das Inbox-System ist als Daemon-Job integriert:

  Job-ID: 3 (inbox-scan)
  Typ:    interval
  Zyklus: 30 Minuten (standardmäßig OFF)
  Modus:  --process (einmaliger Scan pro Durchlauf)

Befehle:
  bach daemon jobs               Alle Jobs auflisten
  bach daemon run 3              Inbox-Scan manuell starten
  bach daemon toggle 3           Job aktivieren/deaktivieren
  bach daemon reschedule 3 15m   Intervall ändern (z.B. 15 Minuten)

WICHTIG: Der Daemon-Job ruft `inbox_watcher.py --process` auf, NICHT
         den dauerhaften Watchdog-Modus. Für Echtzeit-Überwachung:
         `bach inbox start` (startet watchdog direkt)

GUI
---

  /inbox                 Inbox-Dashboard
  /inbox/rules           Regeln verwalten (Task #443)

  API-Endpunkte:
    POST /api/inbox/scan     Scan manuell triggern (GUI + index.html)

WORKFLOW
--------

ZWEI MODI:

A. WATCHDOG-MODUS (bach inbox start):
   - Echtzeit-Überwachung mit watchdog-Library
   - Reagiert sofort auf neue Dateien
   - Läuft dauerhaft im Hintergrund

B. DAEMON-MODUS (bach daemon run 3):
   - Periodischer Scan alle 30 Minuten (konfigurierbar)
   - Ruft `inbox_watcher.py --process` auf
   - Integriert in Daemon-System

Verarbeitungsablauf (beide Modi):
1. Datei erscheint in Watch-Ordner (z.B. Downloads)
2. Scanner wartet bis Datei stabil (keine Schreibzugriffe)
3. Datei wird nach Transfer-Zone verschoben
4. Regel-Engine prueft Muster (Dateiname, Inhalt, OCR)
5. Treffer: Datei wird in Zielordner verschoben
6. Kein Treffer: Bleibt in unsortiert, Task wird erstellt

CONNECTOR-INTEGRATION
---------------------

Ab v1.1.0 werden Connector-Nachrichten (E-Mails, Slack, etc.) automatisch
in die messages-Inbox geroutet. Siehe:

  system/hub/_services/connector/queue_processor.py
  bach --help messages
  bach --help connector

KONZEPT-DOKUMENTE
-----------------

  docs/CONCEPT_INBOX_SCANNER.md         Architektur (aktiv)
  docs/_archive/CONCEPT_inbox_*.md      Format-Specs (archiviert)

IMPLEMENTATION
--------------

  system/tools/inbox_watcher.py         Hauptscript (watchdog + --process)
  system/hub/inbox.py                   CLI-Handler
  system/gui/server.py                  GUI-API (POST /api/inbox/scan)
  system/hub/_services/document/scanner_service.py  Dokumenten-Scanner

SIEHE AUCH
----------

  bach --help dirscan       Dokumenten-Scanner
  bach --help daemon        Hintergrund-Dienste
  bach --help steuer        Steuer-Integration
  bach --help messages      Nachrichten-System
  bach --help connector     Connector-System

VERSION: 1.1.0 (2026-02-08)


## Injectors

INJEKTOR-SYSTEM (Kognitive Orchestrierung)
==========================================

Stand: 2026-02-08

Injektoren simulieren DENKEN und ASSOZIATIONEN als ZENTRALE EXEKUTIVE.
Sie orchestrieren die kognitive Verarbeitung in drei Ebenen:
- STATISCH: Wissensbasis (Wiki, Help, Kontext)
- PROZESSBEGLEITEND: Aktive Steuerung waehrend der Arbeit
- PROAKTIV: Memory-Abrufe und System-Logs

Default: Alle AN (koennen jederzeit abgeschaltet werden).

COOLDOWN-MANAGEMENT (v1.1.75)
-----------------------------
Injektoren werden nach Anzeige fuer X Minuten stumm geschaltet:
- Strategy:  2 Minuten
- Context:   1 Minute
- Between:   3 Minuten
- Tool-Warn: 5 Minuten

Verhindert nervige Wiederholungen, ohne Funktion zu verlieren.

DIE 5 INJEKTOREN MIT TEILFUNKTIONEN
-----------------------------------

1. STRATEGY-INJEKTOR (Metakognition)
   Teilfunktionen:
   - Metakognition: Was, wann, wie machen?
   - Entscheidungshilfe bei Verzweigungen
   - Fehleranalyse ("Fehler sind wertvolle Informationen")

   Trigger-Woerter: fehler, komplex, blockiert, schwierig, problem
   Beispiel: "Fehler" -> "Fehler sind wertvolle Informationen"
   Cooldown: 2 Minuten

2. CONTEXT-INJEKTOR (Arbeitsgedaechtnis)
   Teilfunktionen:
   - Aufgabenbeschreibung in Erinnerung rufen
   - Tool-Empfehlungen basierend auf Kontext
   - Memory-Abruf (Kurzzeit, Langzeit, Session)
   - Anforderungsanalyse
   - Integration mit Connector-Routing (siehe unten)

   Trigger: Stichwoerter im Text (siehe TOOL-TRIGGER unten)
   Nicht aggressiv - nur Hinweise
   Cooldown: 1 Minute

3. TIME-INJEKTOR (Zeitgefuehl)
   Teilfunktionen:
   - Timebeat: Regelmaessige Zeit-Updates
   - Zeitbudget-Awareness

   Default-Intervall: 60 Sekunden
   Hilft beim Zeitgefuehl und Session-Management
   Kein Cooldown (eigener Intervall-Mechanismus)

4. BETWEEN-INJEKTOR (Qualitaetskontrolle)
   Teilfunktionen:
   - Qualitaetskontrolle nach Task-Done
   - Uebergang zur naechsten Aufgabe regeln
   - Ergebnis-Check: Validierung gegen Anforderungen

   Trigger: Nach "bach task done"
   NICHT bei Session-Ende (erkennt das)
   Cooldown: 3 Minuten

5. TOOL-INJEKTOR (Tool-Awareness)
   Teilfunktionen:
   - Tool-Erinnerung bei Session-Start (einmalig)
   - Warnung vor Tool-Duplikaten beim Erstellen
   - Kategorisierte Tool-Uebersicht

   Kategorien: OCR, Daten-Import, Domain-Handler, Code-Analyse,
               Encoding, Import-Handling, Konvertierung
   Trigger: Text enthaelt "neues tool", "tool erstellen" etc.
   Cooldown: 5 Minuten

KOGNITIVE ORCHESTRIERUNG (Diagramm)
-----------------------------------

  +-------------------------------------------------------------+
  |                INJEKTOR-ORCHESTRIERUNG                      |
  |                (Zentrale Exekutive)                         |
  +-------------------------------------------------------------+
  |                                                             |
  |  STATISCH (Wissensbasis)                                    |
  |  +-- Meta-Skills, Meta-Workflows                            |
  |  +-- Wiki (wiki/)                                      |
  |  +-- Help (docs/docs/docs/help/*.txt)                                      |
  |  +-- Kontext (memory_context)                               |
  |                                                             |
  |  PROZESSBEGLEITEND (via Injektoren)                         |
  |  +-- strategy_injector (Cooldown: 2min)                     |
  |  |   +-- Metakognition: Was, wann, wie?                     |
  |  |   +-- Entscheidungshilfe                                 |
  |  |   +-- Fehleranalyse                                      |
  |  +-- context_injector (Cooldown: 1min)                      |
  |  |   +-- Aufgaben-Erinnerung                                |
  |  |   +-- Tool-Empfehlungen                                  |
  |  |   +-- Anforderungsanalyse                                |
  |  |   +-- Connector-Routing Integration (siehe unten)        |
  |  +-- between_injector (Cooldown: 3min)                      |
  |  |   +-- Qualitaetskontrolle                                |
  |  |   +-- Task-Uebergang                                     |
  |  |   +-- Ergebnis-Validierung                               |
  |  +-- time_injector (kein Cooldown)                          |
  |  |   +-- Zeitgefuehl (Timebeat)                             |
  |  +-- tool_injector (Cooldown: 5min)                         |
  |      +-- Tool-Awareness (Session-Start)                     |
  |      +-- Duplikat-Warnung                                   |
  |                                                             |
  |  PROAKTIV (Memory-Abrufe via context_injector)              |
  |  +-- Kurzzeit-Memory (working_memory)                       |
  |  +-- Langzeit-Memory (facts, lessons)                       |
  |  +-- Session-Memory (sessions)                              |
  |  +-- System-Logs (Changelog, Buglog, Roadmap)               |
  |                                                             |
  +-------------------------------------------------------------+

BEFEHLE
-------
  bach --inject status         Zeigt Status aller Injektoren (inkl. Cooldown)
  bach --inject toggle <name>  Schaltet an/aus
  bach --inject task <min>     Aufgabe fuer X Minuten
  bach --inject decompose <id> Zerlegt Aufgabe

TOGGLE-NAMEN:
  strategy   (oder strategy_injector)
  context    (oder context_injector)
  time       (oder time_injector)
  between    (oder between_injector)

COOLDOWN-STATUS ANZEIGEN:
  bach --inject status zeigt verbleibende Cooldown-Zeit in Sekunden

TOOL-TRIGGER (Context-Injektor)
-------------------------------
Der Context-Injektor erkennt Stichwoerter und empfiehlt Tools:

  PYTHON-BEARBEITUNG
  ------------------
  "python bearbeiten"     -> bach python_cli_editor <datei> --show-all
  "klasse bearbeiten"     -> bach python_cli_editor <datei> --show-all
  "methode bearbeiten"    -> bach python_cli_editor <datei> --show-all
  "code struktur"         -> bach python_cli_editor <datei> --show-all
  "imports anzeigen"      -> bach python_cli_editor <datei> --show-imports

  CODE-ANALYSE
  ------------
  "code analysieren"      -> bach code_analyzer <datei>
  "dead code"             -> bach code_analyzer <datei>

  ENCODING & FORMATIERUNG
  -----------------------
  "encoding problem"      -> bach c_encoding_fixer <datei>
  "umlaute kaputt"        -> bach c_encoding_fixer <datei>
  "utf-8"                 -> bach c_encoding_fixer <datei>
  "emoji"                 -> bach c_emoji_scanner <datei>
  "einrueckung"           -> bach c_indent_checker <datei>

  IMPORT-HANDLING
  ---------------
  "imports sortieren"     -> bach c_import_organizer <datei>
  "import problem"        -> bach c_import_diagnose <datei>
  "import fehlt"          -> bach c_import_diagnose <datei>

  DATEI-OPERATIONEN
  -----------------
  "datei aufteilen"       -> bach c_pycutter <datei>
  "zu gross"              -> bach c_pycutter <datei>
  "sqlite anzeigen"       -> bach c_sqlite_viewer <db>
  "json problem"          -> bach c_json_repair <datei>

  KONVERTIERUNG
  -------------
  "markdown zu pdf"       -> bach c_md_to_pdf <datei>
  "format konvertieren"   -> bach c_universal_converter <datei>

  TOOL-SUCHE
  ----------
  "tool finden"           -> bach tool suggest 'beschreibung'
  "welches tool"          -> bach tool suggest 'beschreibung'
  "tool suchen"           -> bach tools search <begriff>

  HILFE & KONVENTIONEN
  --------------------
  "neues tool"            -> --help naming (Tool-Praefixe)
  "konzept"               -> --help practices
  "architektur"           -> --help practices
  "memory"                -> --help memory
  "task"                  -> --help tasks
  "pfad"                  -> --help bach_paths
  "skill"                 -> --help skills
  "version"               -> bach --skills version <name>

BEISPIEL-AUSGABE
----------------
Wenn Claude "python bearbeiten" liest:

  [KONTEXT] Python-Editor: bach python_cli_editor <datei> --show-all

Wenn Claude "encoding problem" liest:

  [KONTEXT] Encoding-Fix: bach c_encoding_fixer <datei>

CONNECTOR-ROUTING INTEGRATION (NEU v1.1.75)
-------------------------------------------
ContextInjector ist jetzt in den Connector-Message-Flow integriert:

ROUTING-PIPELINE (queue_processor.py):
  Eingehende Nachricht (connector_messages)
    |
    v
  route_incoming() wendet an:
    1. ContextInjector.check(text) - 100+ hardcoded Trigger + DB cache
    2. context_triggers Tabelle - 900+ dynamische Trigger aus DB
    |
    v
  Nachricht mit Metadata-Hints (messages.inbox)
    -> metadata["context_hints"] = [hint1, hint2, ...]
    -> metadata["context_triggers"] = [trigger1, trigger2, ...]

VORTEIL:
- Eingehende Nachrichten bekommen SOFORT Kontext-Hinweise
- LLM sieht bereits relevante Tool-Empfehlungen
- Keine manuelle Suche nach Tools noetig
- Kontext wird als Metadata mitgeliefert (nicht im Text)

BEISPIEL:
  User schreibt: "encoding problem mit Datei X"
  -> ContextInjector erkennt "encoding problem"
  -> Metadata: {"context_hints": "bach c_encoding_fixer <datei>"}
  -> LLM bekommt Hint als System-Info, nicht als User-Text

DATENBANK-TRIGGER:
  Tabelle context_triggers (900+ Eintraege):
  - trigger_phrase: Suchbegriff (z.B. "python bearbeiten")
  - hint_text: Empfehlung (z.B. "bach python_cli_editor <datei>")
  - Automatisch beim Routing abgefragt
  - Dynamisch erweiterbar ohne Code-Aenderung

KONFIGURATION
-------------
In config.json unter "injectors":

  {
    "injectors": {
      "strategy_injector": true,
      "context_injector": true,
      "time_injector": true,
      "between_injector": true,
      "timebeat_interval": 60
    }
  }

WICHTIG
-------
- Injektoren koennen auch nerven/ablenken!
- Jederzeit abschaltbar: bach --inject toggle context (oder strategy, time, between)
- Hinweis bei jeder Strategie-Injection wie man abschaltet
- KEINE neuen Injektoren noetig - die 5 decken alle Funktionen ab
- Cooldowns verhindern nervige Wiederholungen automatisch

CODE-REFERENZ
-------------
  tools/injectors.py                    Injector-Implementierung
  hub/inject.py                         CLI-Handler
  hub/_services/connector/queue_processor.py  Connector-Integration

KLASSEN & KOMPONENTEN:
  InjectorSystem        - Haupt-Interface, orchestriert alle Injektoren
  StrategyInjector      - Metakognition, Trigger-basiert
  ContextInjector       - Tool-Empfehlungen, DB-Cache (~100 Trigger)
  TimeInjector          - Timebeat (60s Intervall)
  BetweenInjector       - Qualitaetskontrolle nach Task-Done
  ToolInjector          - Tool-Awareness, Duplikat-Warnung
  CooldownManager       - Cooldown-Verwaltung (strategy=2min, context=1min, between=3min)
  TaskAssigner          - Task-Zuweisung basierend auf Zeitbudget

DATENBANK-TABELLEN:
  context_triggers      - 900+ dynamische Trigger (trigger_phrase, hint_text)
  injector_cooldowns    - Cooldown-Timestamps (injector_name, last_shown)

SIEHE AUCH
----------
  bach --help tools                      Tool-Uebersicht
  bach --help tools/python_cli_editor    Detaillierte Tool-Doku
  bach --help memory                     Memory-System
  bach --help connector                  Connector-System & Message-Routing
  bach tools search                      Tool-Suche
  bach tool suggest                      Tool-Empfehlung


## Lernen

LERNEN - Memory als Lernprozess
================================

BESCHREIBUNG
Philosophische Betrachtung von Lernen als Memory-Prozess.
Entstanden aus der Analyse, wie BACH-Agenten lernen.

KERN-THESE
----------
"Lernen ist eigentlich eine Form von Memory."

DER PROZESS-ABLAUF
------------------
1. JETZTZUSTAND (Status Quo)
   Ausgangslage des Systems/Wissens.

2. EREIGNIS / ERFAHRUNG (Event)
   Interaktion, neuer Input, Erfolg oder Fehler.

3. SPEICHERN (Storage)
   Rohdaten des Ereignisses festhalten.

4. KONSOLIDIEREN (Consolidation)
   Der eigentliche Lernschritt:
   - Erkenntnisse ziehen
   - Regeln ableiten (Abstraktion)
   - Erfahrung zusammenfassen (Komprimierung)

FAZIT
-----
Lernen ist nicht das Ansammeln von Daten, sondern die
Konsolidierung von Erfahrungen zu neuen Strukturen
(Regeln/Wissen) im Gedaechtnis.

UMSETZUNG IN BACH
-----------------
Das Memory-System bildet diesen Prozess ab:

  Eingabe --> Working Memory --> Konsolidierung --> Facts/Lessons
                    |                                     |
                    | (Session-Ende)                       | (Permanent)
                    v                                     v
              Session-Bericht                     Injektoren/Kontext
              (Episodisch)                        (Semantisch)

PRAKTISCHE ANWENDUNG
--------------------
1. Erfahrung machen
   bach memory write "Beobachtung: XYZ funktioniert nicht"

2. Erkenntnis ableiten
   Was ist der Kern? Was ist die Regel?

3. Als Lesson speichern
   bach lesson add "Titel: Erkenntnis/Loesung"

4. Im Kontext verfuegbar
   Lesson wird bei relevantem Kontext injiziert

SIEHE AUCH
----------
bach memory status         Memory-System Uebersicht
bach lesson list           Lessons Learned System
bach shutdown              Konsolidierung bei Session-Ende


## Lessons

LESSONS LEARNED - Wissensmanagement
====================================

STAND: 2026-02-08

System zum Erfassen und Abrufen von Erkenntnissen, Bug-Fixes und Best Practices.
Lessons sind der Kern des "Rueckflusses" in das Systemverhalten.

CLI-BEFEHLE
-----------
  bach lesson add "Titel: Loesung"     Neue Lesson hinzufügen
  bach lesson edit ID [Optionen]       Lesson bearbeiten (v1.1.70)
  bach lesson deactivate ID [-r REASON] Deaktivieren (v1.1.70)
  bach lesson last [n]                 Letzte n Lessons (Standard: 5)
  bach lesson search "keyword"         Durchsuchen
  bach lesson show ID                  Details & Metadaten anzeigen

LIBRARY API
-----------
  from bach_api import lesson
  lesson.add("Titel: Loesung", "--category", "bug")
  lesson.list("bug")
  lesson.edit(42, "--title", "Neuer Titel")
  lesson.deactivate(42, "--reason", "Obsolet")
  lesson.show(42)

KATEGORIEN (Aktuell)
--------------------
  bug           Bug-Fixes und Workarounds
  workflow      Erweiterte Arbeitsabläufe (z.B. Multi-LLM)
  tool          Tool-spezifisches Wissen
  integration   Integration mit externen Systemen
  performance   Performance-Optimierungen
  general       Allgemeine Architektur-Entscheidungen

SCHWEREGRADE
------------
  low           Nur zur Info
  medium        Empfohlener Standard
  high          Wichtige Regel (Injektor-Prio)
  critical      Kritisches Systemwissen (Schutzregeln)

BEISPIELE
=========

  # Bug-Fix dokumentieren
  bach lesson add "SQLite Lock: WAL-Mode aktivieren" --category bug --severity high

  # Workflow dokumentieren
  bach lesson add "Multi-LLM: Immer llm lock vor Schreibzugriff" --category workflow

  # Performance-Optimierung
  bach lesson add "DB-Queries: Index auf created_at" --category performance

  # Integration-Wissen
  bach lesson add "OCR: Tesseract braucht PATH-Variable" --category integration

  # Lesson bearbeiten
  bach lesson edit 42 --title "Neuer Titel" --severity critical

  # Lesson deaktivieren
  bach lesson deactivate 42 --reason "Durch bessere Loesung ersetzt"

BEKANNTE PROBLEME & LOESUNGEN (Auszug)
=====================================

1. MULTI-LLM SHARED FILES (workflow)
   Problem: Race Conditions bei gleichzeitiger Bearbeitung.
   Loesung: IMMER `bach llm lock <datei>` vor Schreibzugriff nutzen.

2. CLI-FIRST PRINZIP (workflow)
   Problem: Manuelle Datei-Edits umgehen Injektoren/Monitoring.
   Loesung: Alles was via CLI geht (task, lesson, mem) IMMER via CLI tun.

3. WINDOWS ENCODING (bug)
   Problem: Emojis crashen oft die Standard-Windows-Konsole.
   Loesung: In Python `io.TextIOWrapper` mit UTF-8 Fallback für stdout nutzen.

4. DB-DATEI SPERREN (performance)
   Problem: Lock-Fehler bei parallelem Zugriff vieler Prozesse.
   Loesung: Kurze Transaktionen und WAL-Mode (Write-Ahead Logging).

5. DOCS-UPDATE (bug)
   Problem: Veraltete Versionen in SKILL.md blockieren Sessions.
   Loesung: `python tools/doc_update_checker.py` regelmäßig laufen lassen.

INTEGRATION
-----------
Lessons fließen automatisch in das **Dynamic Learning System** ein:
- Trigger-Generierung: Keywords in Titeln erzeugen Injektor-Hinweise.
- Aktivierung: `is_active=1` steuert, welche Regeln dem LLM präsentiert werden.

SIEHE AUCH
----------
  docs/docs/docs/help/memory.txt            Cognitive Memory Model
  docs/docs/docs/help/consolidation.txt     Vom Ereignis zur Lektion
  ROADMAP.md                 Phasen der Entwicklung


## Llm Kommunikation

LLM-KOMMUNIKATION -- UEBERBLICK ALLER METHODEN
================================================

Stand: 2026-02-17
Kontext: Wie koennen LLM-Instanzen (Claude, Gemini, Ollama) miteinander
         und mit der Aussenwelt kommunizieren? Katalog aller bekannten
         Methoden, bewertet nach Eignung fuer verschiedene Szenarien.

21 KOMMUNIKATIONSFORMEN
========================

HINWEIS: 15 generische Methoden (1-15) + 6 BACH-spezifische (16-21).
Die generischen Methoden sind auf jedes LLM-System uebertragbar.
Die BACH-spezifischen nutzen BACHs eigene Infrastruktur.

1. DATEIEN HINTERLASSEN (Drop-File)
-----------------------------------
   Methode:    LLM schreibt Datei, anderes LLM liest sie spaeter
   Richtung:   Unidirektional (Schreiber -> Leser)
   Latenz:     Hoch (Leser muss aktiv pruefen)
   Beispiel:   Agent schreibt ergebnis.txt, naechster Agent liest sie
   Staerke:    Einfachst moegliche Methode, keine Infrastruktur noetig
   Schwaeche:  Kein Benachrichtigungsmechanismus, Timing-Probleme
   BACH:       Grundlegende Methode in vielen Workflows

2. MEMORY.md (Gemeinsam geteilte Datei)
----------------------------------------
   Methode:    Alle LLM-Partner lesen/schreiben dieselbe MEMORY.md
   Richtung:   Bidirektional (alle lesen und schreiben)
   Latenz:     Session-basiert (Aenderungen wirken ab naechster Session)
   Beispiel:   Claude schreibt Lesson Learned, Gemini liest es naechste Session
   Staerke:    Automatisch injiziert bei Session-Start (Claude Code)
   Schwaeche:  200-Zeilen-Limit, keine Echtzeit, manuell gepflegt
   BACH:       Aktuell je eine pro Partner; SQ043 plant gemeinsame Memory-DB

3. GEMEINSAMES GEDAECHTNIS (Datenbank)
---------------------------------------
   Methode:    Zentrale DB (bach.db) in die alle schreiben/lesen
   Richtung:   Bidirektional, Multi-Party
   Latenz:     Sofort (bei DB-Zugriff innerhalb einer Session)
   Beispiel:   Agent speichert Fact, anderer Agent fragt Facts ab
   Staerke:    Strukturiert, durchsuchbar, gewichtet, persistent
   Schwaeche:  Braucht DB-Zugriffs-Handler, nicht automatisch injiziert
   BACH:       facts, lessons, context_triggers in bach.db (890+ Eintraege)

4. INJEKTOREN ALS KOMMUNIKATION
---------------------------------
   Methode:    System-Reminders werden in den Nachrichtenstrom injiziert
   Richtung:   System -> LLM (unidirektional)
   Latenz:     Sofort (bei naechster Nachricht)
   Beispiel:   Hook injiziert Nachricht via hook_additional_context
   Varianten:
     a) Claude Code Injektoren (52 Typen, nicht steuerbar)
     b) BACH Injektoren (5 Typen, LLM-steuerbar)
     c) Hook-basiert (UserPromptSubmit liest "Inbox"-Datei)
   Staerke:    Erscheint im Kontext ohne aktives Abrufen
   Schwaeche:  CC-Injektoren nicht vom User/LLM kontrollierbar
   BACH:       ContextInjector, SessionInjector, PartnerInjector,
               HealthInjector, SpendenInjector
   Siehe auch: claude-code-injections.txt, injectors.txt

5. STIGMERGY / KARTE DES RUMTREIBERS
--------------------------------------
   Methode:    Agenten hinterlassen Marker-Dateien (Pheromone)
               Andere Agenten lesen die Marker und passen Verhalten an
   Richtung:   Indirekt bidirektional (ueber Umgebung)
   Latenz:     Sofort (File-System)
   Beispiel:   Bot schreibt .visited.log, andere meiden besuchte Bereiche
   Marker:     .done, .in_progress, .visited.log, .counter, .flag
   Staerke:    Keine direkte Kommunikation noetig, skaliert gut
   Schwaeche:  Keine Garantie dass Marker gelesen wird, Verdunstung noetig
   BACH:       data/swarm/map/, maintenance_swarm.py, marauders_map.py
   Siehe auch: trampelpfadanalyse.md (Kapitel 2: Schwarm-Verfahren)

6. HANDOFF-DATEIEN (Explizite Uebergabe)
------------------------------------------
   Methode:    Strukturiertes Uebergabedokument zwischen Instanzen
   Richtung:   Unidirektional (Vorgaenger -> Nachfolger)
   Latenz:     Sofort (Datei wird vor Start des Nachfolgers geschrieben)
   Beispiel:   Marble-Run: handoff.md mit Task, Status, Ergebnis, Feedback
   Staerke:    Volle Kontextweitergabe, strukturiert, nachvollziehbar
   Schwaeche:  Nur fuer serielle Ketten, nicht fuer parallele Kommunikation
   BACH:       marble_run/state/handoff.md (Murmelbahn-Pipeline)

7. BRIDGE / CONNECTORS (Externe Kanaele)
------------------------------------------
   Methode:    BACH sendet/empfaengt Nachrichten ueber externe Dienste
   Richtung:   Bidirektional (BACH <-> Mensch/anderes System)
   Latenz:     Sekunden (abhaengig vom Dienst)
   Beispiel:   User schreibt Telegram-Nachricht, BACH antwortet
   Kanaele:    Telegram (Beta), Discord (Beta), HomeAssistant (Beta),
               Signal (geplant), WhatsApp (geplant)
   Staerke:    Kommunikation mit der realen Welt, nicht nur LLM-zu-LLM
   Schwaeche:  Abhaengig von externen APIs, Scraping-basiert bei manchen
   BACH:       connectors/, hub/connector.py, Bridge-System
   Siehe auch: bridge.txt, connectors.txt

8. CLAUDE CODE TEAM-MODUS
---------------------------
   Methode:    Eingebaute Team-Koordination in Claude Code CLI
   Richtung:   Bidirektional (Leader <-> Teammates)
   Latenz:     Sofort (Message-Queue innerhalb der Session)
   Beispiel:   Team-Lead sendet Aufgabe an Researcher, bekommt Ergebnis
   Features:   SendMessage, TaskList, TaskCreate, TaskUpdate, Broadcast
   Staerke:    Anthropic-native, gut integriert, parallele Arbeit
   Schwaeche:  Nur innerhalb einer Claude Code Session, kein Opus/Sonnet-Mix
   BACH:       Nicht direkt integriert (Claude Code Feature, nicht BACH)

9. GIT ALS KOMMUNIKATION
--------------------------
   Methode:    Commits + Commit-Messages als Nachrichten zwischen Instanzen
   Richtung:   Bidirektional (Push/Pull)
   Latenz:     Minuten (Commit + Push + Pull)
   Beispiel:   Worker committed Aenderung, Reviewer liest git diff + Message
   Staerke:    Versioniert, nachvollziehbar, Standard-Tooling
   Schwaeche:  Overhead fuer kleine Nachrichten, braucht Repo
   BACH:       Nicht systematisch genutzt, aber moeglich (SQ020 Versionierung)

10. DB-TABELLEN ALS KANAL
---------------------------
    Methode:    Agenten schreiben in gemeinsame DB-Tabelle, andere lesen
    Richtung:   Bidirektional, Multi-Party
    Latenz:     Sofort (innerhalb einer Session bei DB-Zugriff)
    Beispiel:   Agent schreibt Nachricht in messages-Tabelle, Empfaenger pollt
    Staerke:    Strukturiert, persistent, durchsuchbar, bereits vorhanden
    Schwaeche:  Polling noetig (kein Push), braucht Handler
    BACH:       bach.db hat Infrastruktur, aber kein explizites Message-System

11. HOOKS (Event-basierte Injektion)
--------------------------------------
    Methode:    Shell-Kommando wird bei Event ausgefuehrt, Ergebnis injiziert
    Richtung:   Extern -> LLM (unidirektional pro Hook-Aufruf)
    Latenz:     Sofort (bei jedem User-Prompt oder Tool-Call)
    Beispiel:   UserPromptSubmit-Hook liest "Inbox"-Datei und injiziert Inhalt
    Hook-Typen: PreToolUse, PostToolUse, SessionStart, UserPromptSubmit, etc.
    Staerke:    Einfachster Weg fuer Inter-Instanz-Messaging ohne Source-Patch
    Schwaeche:  Nur bei Events (nicht on-demand), Hook-Konfiguration noetig
    BACH:       Empfohlener Ansatz fuer Claude Code Integration
    Siehe auch: claude-code-injections.txt (Abschnitt "Messaging-System")

12. MCP-SERVER ALS VERMITTLER
-------------------------------
    Methode:    Gemeinsamer MCP-Server den mehrere LLM-Instanzen nutzen
    Richtung:   Bidirektional (alle Instanzen rufen gleichen Server auf)
    Latenz:     Sofort (Tool-Call)
    Beispiel:   bach-codecommander-mcp als Shared-Service fuer alle Claude-Instanzen
    Staerke:    Standardisiert (MCP-Protokoll), tool-basiert, erweiterbar
    Schwaeche:  Server muss laufen, kein Push-Mechanismus
    BACH:       bach-codecommander-mcp (14 Tools), bach-filecommander-mcp (38 Tools)

13. PROCESS-CHAINING (.bat als Signal)
----------------------------------------
    Methode:    Ein Prozess startet den naechsten via Batch-Datei
    Richtung:   Unidirektional (Vorgaenger -> Nachfolger)
    Latenz:     Sofort (Prozess-Start)
    Beispiel:   Marble-Run: Opus Worker beendet sich, .bat startet Sonnet Reviewer
    Staerke:    Deterministisch, keine Infrastruktur, BS-nativ
    Schwaeche:  Nur serielle Ketten, kein Feedback-Kanal (braucht Handoff-Datei)
    BACH:       marble_run/launchers/ (Murmelbahn-System)

14. SHARED FILESYSTEM (File-Watcher)
--------------------------------------
    Methode:    Agenten ueberwachen gemeinsames Verzeichnis auf Aenderungen
    Richtung:   Bidirektional (alle koennen schreiben/lesen)
    Latenz:     Sekunden (Polling-Intervall des Watchers)
    Beispiel:   Agent schreibt neue_aufgabe.json, Watcher erkennt und reagiert
    Staerke:    Einfach, keine spezielle Infrastruktur
    Schwaeche:  Polling-basiert, Race Conditions moeglich, OneDrive-Sync-Probleme
    BACH:       Grundsaetzlich moeglich, nicht systematisch implementiert

15. STDOUT/STDIN-PIPING
-------------------------
    Methode:    Ausgabe eines Prozesses wird direkt zur Eingabe des naechsten
    Richtung:   Unidirektional (Producer -> Consumer)
    Latenz:     Sofort (Pipe)
    Beispiel:   claude --print "Analysiere X" | claude --print "Bewerte: $(cat -)"
    Staerke:    Unix-Philosophie, minimaler Overhead, kein Dateisystem noetig
    Schwaeche:  Nur Text, kein strukturierter Kontext, keine Persistenz
    BACH:       Nicht genutzt (Claude Code unterstuetzt --print aber kein stdin-Pipe)

BACH-SPEZIFISCHE KOMMUNIKATIONSFORMEN (16-21)
===============================================

16. MULTI-LLM-PROTOKOLL V3 (Presence + Locking)
-------------------------------------------------
    Methode:    Presence-Dateien + Lock-Dateien + Handshake im Dateisystem
    Richtung:   Bidirektional, Multi-Party
    Latenz:     Sekunden (Heartbeat alle 30s, Timeout 120s)
    Beispiel:   Claude erkennt dass Gemini online ist via .gemini_presence
    Features:   Presence, Locking, Handshake, Heartbeat, Agent-Detection
    Bekannte:   claude, gemini, copilot, ollama, perplexity, mistral-watcher
    Staerke:    Koordination ohne zentrale Instanz, Race-Condition-sicher
    Schwaeche:  Dateisystem-basiert (langsamer als DB), Stale-Presence moeglich
    BACH:       hub/multi_llm_protocol.py (V3), CLI: bach llm presence/check/lock

17. PARTNER-PRESENCE DB (Stempelkarten)
----------------------------------------
    Methode:    SQLite-Tabelle partner_presence mit clock_in/out/heartbeat
    Richtung:   Bidirektional (jeder meldet sich an/ab)
    Latenz:     Sofort (DB-Abfrage)
    Beispiel:   bach llm status -> zeigt wer online ist und was er tut
    Features:   clock_in(), clock_out(), heartbeat(), get_online_partners()
    Staerke:    Zuverlaessiger als Dateien, persistenter Status
    Schwaeche:  Braucht DB-Zugriff, nicht dateisystem-kompatibel
    BACH:       hub/multi_llm_protocol.py (PartnerPresenceDB Klasse)

18. NACHRICHTEN-SYSTEM (INBOX/OUTBOX)
--------------------------------------
    Methode:    DB-basiertes Messaging mit sender, recipient, body, status
    Richtung:   Bidirektional, gerichtet (Empfaenger bestimmt)
    Latenz:     Sofort (bei Abfrage) oder Polling (Watch-Modus alle 10s)
    Beispiel:   bach msg send gemini "Analysiere dieses Bild"
    Features:   Send, Read, Watch (Polling), Ping, Lesebestaetigung (--ack)
    Status:     unread, read, archived
    Staerke:    Strukturiert, persistent, durchsuchbar, Lesebestaetigung
    Schwaeche:  Pull-basiert (kein Push), braucht aktives Polling
    BACH:       hub/messages.py, DB-Tabelle: messages

19. BENACHRICHTIGUNGS-SYSTEM (Multi-Channel Push)
--------------------------------------------------
    Methode:    Ausgehende Benachrichtigungen ueber externe Kanaele
    Richtung:   Unidirektional (BACH -> Extern)
    Latenz:     Sekunden
    Kanaele:    Discord (Webhook), Telegram (Bot API), Slack (Webhook),
                Email (SMTP/SSL), Signal (Direct), Generic Webhook
    Beispiel:   bach notify send telegram "Task erledigt"
    Staerke:    Multi-Channel, konfigurierbar
    Schwaeche:  Nur ausgehend (kein Empfang ueber notify)
    BACH:       hub/notify.py, CLI: bach notify setup/send/test/list

20. QUEUE PROCESSOR & SMART ROUTER
------------------------------------
    Methode:    Zuverlaessiges Routing von Connector-Nachrichten
    Richtung:   Bidirektional (Connector <-> BACH intern)
    Latenz:     Sekunden (Poll-Intervalle: Telegram 15s, Discord 60s)
    Features:   Retry/Backoff (5 Stufen: 30s-480s), Circuit Breaker (5 Fehler)
    Smart:      Parst Commands aus Nachrichten ("/task add Test")
    Staerke:    Zuverlaessig, selbstheilend, Command-Erkennung
    Schwaeche:  Komplex, braucht laufenden Daemon
    BACH:       hub/_services/connector/queue_processor.py, smart_router.py

21. GEMINI DELEGATION PROTOCOL
--------------------------------
    Methode:    Task-Dateien in gemini/inbox/, Ergebnisse in gemini/outbox/
    Richtung:   Bidirektional (Claude -> Gemini und zurueck)
    Latenz:     Minuten bis Stunden (manuell oder via Google Drive Sync)
    Trigger:    Keyword, Token-Budget, Dokument-Laenge, explizit
    Beispiel:   Claude erstellt Research-Task, Gemini arbeitet ab, Ergebnis zurueck
    Staerke:    Nutzt Geminis Staerken (grosse Dokumente, Bilder)
    Schwaeche:  Manueller Transfer noetig (oder Google Drive Sync)
    BACH:       skills/workflows/gemini-delegation.md

VERGLEICHSMATRIX
=================

  Methode              | Richtung | Latenz   | Persistenz | Skalierung | Komplexitaet
  ---------------------|----------|----------|------------|------------|-------------
  GENERISCH (uebertragbar auf jedes LLM-System):
  1  Drop-File         | Uni      | Hoch     | Ja         | Gut        | Minimal
  2  MEMORY.md         | Bi       | Session  | Ja         | Begrenzt   | Gering
  3  Gemeinsame DB     | Multi    | Sofort   | Ja         | Sehr gut   | Mittel
  4  Injektoren        | Uni      | Sofort   | Nein       | Begrenzt   | Mittel
  5  Stigmergy         | Indirekt | Sofort   | Ja (TTL)   | Sehr gut   | Mittel
  6  Handoff-Dateien   | Uni      | Sofort   | Ja         | Seriell    | Gering
  7  Bridge/Connectors | Bi       | Sekunden | Ja         | Gut        | Hoch
  8  Team-Modus        | Bi       | Sofort   | Session    | Parallel   | Mittel
  9  Git               | Bi       | Minuten  | Ja         | Gut        | Mittel
  10 DB-Tabellen       | Multi    | Sofort   | Ja         | Sehr gut   | Mittel
  11 Hooks             | Uni      | Event    | Nein       | Begrenzt   | Gering
  12 MCP-Server        | Bi       | Sofort   | Variabel   | Gut        | Hoch
  13 Process-Chaining  | Uni      | Sofort   | Nein       | Seriell    | Gering
  14 File-Watcher      | Bi       | Sekunden | Ja         | Gut        | Mittel
  15 Stdout-Piping     | Uni      | Sofort   | Nein       | Seriell    | Minimal

  BACH-SPEZIFISCH (nutzt BACH-Infrastruktur):
  16 Multi-LLM-Prot.   | Multi    | 30s      | Ja         | Gut        | Mittel
  17 Partner-Presence   | Multi    | Sofort   | Ja         | Gut        | Mittel
  18 Nachrichten-Sys.   | Bi       | Sofort   | Ja         | Gut        | Mittel
  19 Notify (Push)      | Uni      | Sekunden | Ja         | Multi-Ch.  | Mittel
  20 Queue/Router       | Bi       | Sekunden | Ja         | Gut        | Hoch
  21 Gemini-Delegation  | Bi       | Minuten  | Ja         | Begrenzt   | Gering

EMPFEHLUNGEN NACH ANWENDUNGSFALL
==================================

  Anwendungsfall                    | Empfohlene Methode(n)
  ----------------------------------|---------------------------------------
  Schwarm (viele parallele Agenten) | 5 (Stigmergy) + 3 (DB) + 14 (Watcher)
  Serielle Pipeline (Marble-Run)    | 6 (Handoff) + 13 (Process-Chain)
  Team-Arbeit (2-5 Agenten)         | 8 (Team-Modus) oder 10 (DB-Tabellen)
  Langzeit-Wissenstransfer          | 2 (MEMORY.md) + 3 (DB)
  Echtzeit-Benachrichtigung         | 4 (Injektoren) + 11 (Hooks)
  Kommunikation mit Aussenwelt      | 7 (Bridge/Connectors)
  Asynchrone Zusammenarbeit         | 1 (Drop-File) + 9 (Git)
  Toolbasierte Integration          | 12 (MCP-Server)

BACH-SPEZIFISCHE ARCHITEKTUR
==============================

BACHs Staerke ist die Kombination mehrerer Methoden:
- Bridge (7) fuer die Aussenwelt
- DB (3+10) als zentraler Wissensspeicher
- Injektoren (4) fuer proaktive Kontext-Anreicherung
- Stigmergy (5) fuer Schwarm-Operationen
- Handoff (6) + Process-Chaining (13) fuer Marble-Run-Pipelines

Im Gegensatz dazu ist Claude Code auf eine Methode pro Szenario beschraenkt:
Team-Modus (8) ODER Injektoren (4), nicht kombinierbar.

BACH kann alle 15 Methoden gleichzeitig nutzen und dynamisch wechseln --
das ist der architektonische Vorteil eines LLM-zentrierten Systems.

SIEHE AUCH
===========
  bridge.txt                    Bridge/Connector-System
  connectors.txt                Connector-Typen im Detail
  injectors.txt                 BACH Injektor-System
  claude-code-injections.txt    Claude Code Injektions-Anatomie
  multi-llm.txt                 Multi-LLM-Protokoll
  schwarm.txt                   Schwarm-Operationen (falls vorhanden)


## Logs

LOGS - Auto-Logging System
==========================

BESCHREIBUNG
BACH protokolliert automatisch alle Aktionen.
Zweistufiges System fuer effiziente Speicherung.

ARCHITEKTUR
-----------
system/data/logs/auto_log.txt          Letzte 300 Eintraege (Kurzzeitgedaechtnis)
system/data/logs/auto_log_extended.txt Aeltere Eintraege, max 30 Tage

Nach 30 Tagen werden Eintraege automatisch geloescht.

CLI-BEFEHLE
-----------
bach --logs tail [n]         Letzte n Eintraege (Standard: 20)
bach --logs extended         Extended-Archiv anzeigen
bach --logs count            Anzahl Eintraege

python tools/autolog.py --tail 50      Letzte 50 Eintraege
python tools/autolog.py --extended     Extended-Archiv
python tools/autolog.py --count        Statistik
python tools/autolog.py --log "Text"   Manueller Eintrag

LOG-FORMAT
----------
[YYYY-MM-DD HH:MM:SS] TYP: Nachricht

Typen:
  CMD      Ausgefuehrter Befehl
  TOOL     Tool-Aufruf
  SESSION  Session-Start/Ende

BEISPIEL-OUTPUT
---------------
[2026-01-19 12:29:34] SESSION START
[2026-01-19 12:29:35] CMD: startup
[2026-01-19 12:30:00] TOOL: autolog --count
[2026-01-19 12:35:00] SESSION END: Steuer-Agent Tasks

INTEGRATION
-----------
Auto-Logging ist in bach.py integriert (via tools/autolog.py) und loggt automatisch:
- Session-Start und -Ende
- Alle CLI-Befehle
- Tool-Aufrufe

SPEICHERORTE
------------
Hauptlog:    system/data/logs/auto_log.txt
Extended:    system/data/logs/auto_log_extended.txt

HINWEIS: Der Pfad system/logs/ ist DEPRECATED.
EINZIGER Log-Ordner ist jetzt system/data/logs/ (konsolidiert 2026-02-06).

KONFIGURATION
-------------
MAX_LINES = 300        Maximale Zeilen im Hauptlog
ARCHIVE_DAYS = 30      Tage im Extended-Archiv

Werte in tools/autolog.py anpassbar.

SIEHE AUCH
----------
bach --help startup    Zeigt Autolog-Status bei Session-Start
bach --help shutdown   Session-Ende Logging


## Maintain

MAINTAIN - BACH Wartungs-Tools
==============================

UEBERSICHT
----------
Sammlung von Wartungs- und Analyse-Tools fuer BACH.
Alle Tools sind CLI-zugaenglich via bach --maintain

BEFEHLE (16)
------------
  bach --maintain docs          Dokumentations-Update-Check
  bach --maintain duplicates    Duplikat-Erkennung Info
  bach --maintain generate      Skill/Agent Generator
  bach --maintain export        Export-Tools
  bach --maintain pattern       Dateinamen-Pattern kuerzen
  bach --maintain scan          System nach CLI-Tools scannen
  bach --maintain clean         Dateien nach Alter/Muster loeschen
  bach --maintain json          JSON-Dateien reparieren
  bach --maintain heal          Pfad-Korrektur und Selbstheilung
  bach --maintain registry      Registry-Konsistenz pruefen
  bach --maintain skills        Skill-Gesundheit pruefen
  bach --maintain sync          Skills mit Datenbank synchronisieren
  bach --maintain headers       SKILL.md YAML-Header generieren/validieren
  bach --maintain skill-help    Help-Dateien aus SKILL.md generieren
  bach --maintain workflows     Workflow-Format validieren
  bach --maintain nul           Windows NUL-Dateien entfernen
  bach --maintain list          Alle Tools anzeigen

DOKUMENTATIONS-CHECK
--------------------
  bach --maintain docs [--dry-run]
  
  Erkennt veraltete Dokumentationen:
  - Aelter als 60 Tage
  - Ungueltige Pfade
  - Fehlende Referenzen

SKILL GENERATOR
---------------
  bach --maintain generate <n> [profil] [zielordner]
  
  Profile:
    MICRO    - Nur Datei(en)
    LIGHT    - Minimal (SKILL.md + config + data)
    STANDARD - Standard mit Memory
    EXTENDED - Komplex mit Mikro-Skills

  Beispiele:
    bach --maintain generate mein-skill STANDARD skills/
    bach --maintain generate analyse MICRO skills/workflows/

EXPORT TOOLS
------------
  bach --maintain export skill <n> --from-os <path>
  bach --maintain export agent <n> --from-os <path>
  bach --maintain export os-fresh <path> --output <zip>
  bach --maintain export os-reset <path> --backup

PATTERN TOOL
------------
  bach --maintain pattern <ordner> [optionen]
  
  Optionen:
    --dry-run       Nur anzeigen (default)
    --execute       Umbenennungen durchfuehren
    --prefix-only   Nur Prefix-Patterns
    --suffix-only   Nur Suffix-Patterns
    -m <n>          Minimale Pattern-Laenge

TOOL SCANNER
------------
  bach --maintain scan [--json]
  bach --maintain scan compare
  
  Findet installierte CLI-Tools und vergleicht mit Registry.

FILE CLEANER
------------
  bach --maintain clean <ordner> [optionen]
  
  Optionen:
    --age <tage>    Dateien aelter als X Tage
    --keep <n>      Nur N neueste behalten
    --pattern <p>   Datei-Pattern (z.B. "*.log")
    -r              Rekursiv suchen
    --execute       Tatsaechlich loeschen

  Beispiele:
    bach --maintain clean ./logs --age 30
    bach --maintain clean ./backups --keep 5 --execute

JSON FIXER
----------
  bach --maintain json <datei/ordner> [optionen]
  
  Optionen:
    --dry-run    Nur pruefen (default)
    --execute    Tatsaechlich reparieren
    --backup     Backup vor Aenderung

  Repariert:
    - UTF-8 BOM
    - Trailing Commas
    - Single-Quotes
    - PowerShell Newlines

PATH HEALER (NEU)
-----------------
  bach --maintain heal [optionen]
  
  Korrigiert veraltete Pfade in BACH-Dateien.
  
  Optionen:
    --dry-run       Nur pruefen, nichts aendern (default)
    --execute       Tatsaechlich korrigieren
    --target <p>    Nur bestimmte Datei pruefen
    --report        Detaillierten Report generieren
    
  Korrigiert:
    - Alte recludOS-Pfade -> BACH_v2_vanilla
    - Alte Skill-Pfade
    - Hub/Handler-Pfade
    - Tools-Verweise
    
  Beispiele:
    bach --maintain heal                   # Dry-run fuer alle
    bach --maintain heal --execute         # Alle korrigieren
    bach --maintain heal --target config.py

  Basiert auf: RecludOS Unified Path Healer v2.3.0

REGISTRY WATCHER (NEU)
----------------------
  bach --maintain registry [optionen]
  
  Ueberwacht und validiert alle BACH-Registries.
  
  Optionen:
    check           Vollstaendiger Check (default)
    check --db      Nur Datenbank pruefen
    check --json    Nur JSON-Configs pruefen
    partners        Partner-Registry Check (NEU)
    report          Detaillierter Report
    
  Prueft:
    - Existenz der Registry-relevanten DB-Tabellen (tools, skills, agents, partners)
    - JSON-Konfigurationsdateien (nur noch begruendete Ausnahmen)
    - Cross-Referenzen zwischen Tabellen
    - partner_recognition + delegation_rules Konsistenz

  Hinweis: partner_registry.json ist DEPRECATED (siehe docs/docs/docs/help/formats.txt)
    
  Beispiele:
    bach --maintain registry               # Quick-Check
    bach --maintain registry report        # Detaillierter Report
    bach --maintain registry check --db    # Nur Datenbank
    
  Hinweis: Laeuft automatisch bei --startup (Quick-Check)

SKILL HEALTH MONITOR (NEU)
--------------------------
  bach --maintain skills [optionen]
  
  Ueberwacht und validiert alle BACH-Skills und Agenten.
  
  Optionen:
    check            Vollstaendiger Check (default)
    check --skills   Nur Skills pruefen
    check --agents   Nur Agenten pruefen
    report           Detaillierter Report
    
  Prueft:
    - Skill-Verzeichnisse (_agents, _experts, _services)
    - SKILL.md Vollstaendigkeit (name, version, description)
    - Agent-Definitionen validieren
    - Verwaiste oder fehlerhafte Skills finden
    
  Beispiele:
    bach --maintain skills                 # Quick-Check
    bach --maintain skills report          # Detaillierter Report
    bach --maintain skills check --agents  # Nur Agenten
    
  Hinweis: Laeuft automatisch bei --startup (Quick-Check)

SYNC TOOL (NEU)
---------------
  bach --maintain sync [optionen]

  Synchronisiert skills/ Dateien mit der Datenbank.

  Optionen:
    --dry-run    Nur anzeigen, nichts aendern (default)
    --verbose    Ausfuehrliche Ausgabe
    -v           Kurz fuer --verbose

  Synchronisiert:
    - SKILL.md Metadaten (Name, Version, Beschreibung)
    - Skill-Status und Abhaengigkeiten
    - Agent-Definitionen

  Beispiele:
    bach --maintain sync               # Dry-run
    bach --maintain sync --verbose     # Mit Details
    bach --maintain sync --dry-run -v  # Dry-run ausfuehrlich

HEADERS TOOL (NEU)
------------------
  bach --maintain headers [optionen]

  Generiert und validiert YAML-Header fuer SKILL.md Dateien.

  Optionen:
    --all           Alle Skill-Verzeichnisse scannen (default)
    --path <p>      Bestimmtes Verzeichnis scannen
    --file <f>      Einzelne SKILL.md verarbeiten
    --dry-run       Nur anzeigen (default)
    --fix           Aenderungen schreiben
    --update-db     DB-Versionen aus YAML-Headern aktualisieren
    -v              Ausfuehrlich

  Gescannte Verzeichnisse:
    - agents/*/SKILL.md
    - agents/_experts/*/SKILL.md
    - hub/_services/*/SKILL.md
    - partners/*/SKILL.md

  Beispiele:
    bach --maintain headers                      # Trockenlauf
    bach --maintain headers --fix                # Alle Header normalisieren
    bach --maintain headers --fix --update-db    # Header + DB aktualisieren
    bach --maintain headers --path agents -v

SKILL-HELP TOOL (NEU)
---------------------
  bach --maintain skill-help [optionen]

  Generiert docs/docs/docs/help/*.txt Dateien aus SKILL.md.

  Optionen:
    <name>       Einzelner Skill-Name
    --all        Alle Skills verarbeiten
    -a           Kurz fuer --all
    --dry-run    Nur anzeigen, nichts schreiben
    -n           Kurz fuer --dry-run

  Beispiele:
    bach --maintain skill-help ati              # Help fuer ATI-Agent
    bach --maintain skill-help --all            # Alle Skills
    bach --maintain skill-help --all --dry-run  # Trockenlauf

WORKFLOWS TOOL (NEU)
--------------------
  bach --maintain workflows [optionen]

  Validiert Workflow-Dateien auf konsistentes Format.

  Prueft:
    - H1-Titel vorhanden
    - Beschreibung (> Blockquote, **Zweck:**, ## Uebersicht)
    - Schritte/Phasen-Struktur
    - Versions-Angabe (optional)

  Erwartet in: skills/workflows/*.md

  Beispiele:
    bach --maintain workflows        # Alle Workflows validieren
    bach --maintain workflows help   # Hilfe anzeigen

NUL-CLEANER (NEU)
-----------------
  bach --maintain nul [optionen]

  Entfernt Windows NUL-Dateien (reservierter Dateiname).

  Optionen:
    scan            Nur NUL-Dateien auflisten (default)
    delete          NUL-Dateien loeschen
    clean/remove    Alias fuer delete
    <pfad>          Bestimmtes Verzeichnis scannen

  Beispiele:
    bach --maintain nul                        # Scan BACH-Verzeichnis
    bach --maintain nul scan                   # Nur scannen
    bach --maintain nul delete                 # Scannen und loeschen
    bach --maintain nul delete C:\Pfad         # Bestimmtes Verzeichnis

  Hinweis: NUL-Dateien entstehen auf Windows, wenn versehentlich
           nach 'NUL' geschrieben wird (Windows Device-Name).

TOOLS
-----
  tools/doc_update_checker.py        Dokumentations-Pruefung
  tools/duplicate_detector.py        Duplikat-Erkennung
  tools/generators/                  Generator-Scripts
    skill_generator.py               Skill-Strukturen
    exporter.py                      Export-Funktionen
  tools/pattern_tool.py              Pattern-Erkennung
  tools/tool_scanner.py              CLI-Tool Discovery
  tools/file_cleaner.py              Datei-Cleanup
  tools/json_fixer.py                JSON-Reparatur
  tools/c_path_healer.py             Pfad-Korrektur (WICHTIG: c_path_healer!)
  tools/nulcleaner.py                NUL-Dateien entfernen
  tools/skill_header_gen.py          YAML-Header Generator
  tools/skill_help_gen.py            Help-Generator + Workflow-Validator
  tools/maintenance/
    registry_watcher.py              Registry-Konsistenz
    skill_health_monitor.py          Skill-Gesundheit
    sync_skills.py                   Skills-DB Synchronisierung

AUTOMATISCHE CHECKS BEI --startup
---------------------------------
Die folgenden Wartungs-Checks laufen automatisch bei Session-Start:

  1. Directory Scan     - Aenderungen seit letzter Session
  2. Path Healer        - Dry-run Pfadkorrektur
  3. Registry Watcher   - Quick-Check DB/JSON Konsistenz
  4. Skill Health       - Quick-Check Skills/Agenten

Fuer detaillierte Reports: bach --maintain <tool> report

AKTUELLE TOOL-UBERSICHT (16 Befehle)
-------------------------------------
1.  docs          - Dokumentations-Update-Check
2.  duplicates    - Duplikat-Erkennung Info
3.  generate      - Skill/Agent Generator
4.  export        - Export-Tools
5.  pattern       - Dateinamen-Pattern kuerzen
6.  scan          - System nach CLI-Tools scannen
7.  clean         - Dateien nach Alter/Muster loeschen
8.  json          - JSON-Dateien reparieren
9.  heal          - Pfad-Korrektur und Selbstheilung
10. registry      - Registry-Konsistenz pruefen
11. skills        - Skill-Gesundheit pruefen
12. sync          - Skills mit Datenbank synchronisieren
13. headers       - SKILL.md YAML-Header generieren/validieren
14. skill-help    - Help-Dateien aus SKILL.md generieren
15. workflows     - Workflow-Format validieren
16. nul           - Windows NUL-Dateien entfernen

SIEHE AUCH
----------
  docs/docs/docs/help/backup.txt   Backup-System
  docs/docs/docs/help/test.txt     Test-System
  docs/docs/docs/help/tools.txt    Tool-Inventar
  docs/docs/docs/help/formats.txt  Datenbank-Formate


## Memory

MEMORY-SYSTEM (Cognitive Model)
================================

STAND: 2026-01-30

Definition: BACH nutzt ein kognitives Memory-System, das dem menschlichen 
Gedächtnis nachempfunden ist. Es geht über reines Speichern hinaus und 
integriert aktive Gewichtung, Decay (Vergessen) und Boost (Erinnern).

DIE 5 KOGNITIVEN TYPEN:
-----------------------

1. WORKING MEMORY (memory_working)
   - "Das Kurzzeitgedächtnis"
   - Fokus: Aktuelle Session, flüchtig.
   - Befehl: `bach mem write "..."`

2. EPISODISCHES GEDÄCHTNIS (memory_sessions)
   - "Das Erlebnistagebuch"
   - Speichert abgeschlossene Sessions (360+).
   - Befehl: `bach --memory session "..."`

3. SEMANTISCHES GEDÄCHTNIS (memory_facts, docs/help/, wiki/)
   - "Das Weltwissen"
   - Fakten, Definitionen, Architektur (230+ Fakten).
   - Befehl: `bach --memory fact "..."`

4. PROZEDURALES GEDÄCHTNIS (memory_lessons, tools/, skills/)
   - "Das Können" / "Best Practices"
   - Wie Dinge getan werden (Workflows, Tools).
   - Befehl: `bach lesson add "..."`

5. ASSOZIATIVES GEDÄCHTNIS (memory_context, context_triggers)
   - "Die Brücke"
   - Verknüpft Wissen via Triggern mit der aktuellen Situation.
   - Befehl: `bach --memory search "..."`
   - Integration: context_triggers feuern auch beim Connector-Routing

DYNAMISCHES LERNSYSTEM (NEU v1.1.80)
------------------------------------
Im Gegensatz zu traditionellen Systemen sind die Injektoren bei BACH nun DYNAMISCH:
- TRIGGER-DB: 900+ Trigger aus Lessons, Workflows und Tools werden automatisch generiert.
- KOGNITIVE LAST: Nur relevanter Kontext wird in die Session geladen.
- RUECKFLUSS: Erledigte Tasks und gelernte Lektionen verändern das Systemverhalten sofort.

CONNECTOR-INTEGRATION (NEU v2.0 - 2026-02-08)
---------------------------------------------
context_triggers werden jetzt auch beim Connector-Routing genutzt:
- Eingehende Telegram/Discord/HomeAssistant-Nachrichten durchlaufen context_triggers
- Erkannte Trigger werden als Metadata an messages.metadata angefügt
- LLM bekommt automatisch relevanten Kontext (z.B. "Steuer" → Steuer-Facts)
- Siehe: --help connector (Kontext-Integration Abschnitt)

DATENBANK-TABELLEN:
  memory_working       Temporäre Notizen (is_active Flag)
  memory_facts         Globale Fakten (cat: user, project, system, domain)
  memory_lessons       Erkenntnisse (severity: info, warn, critical)
  memory_sessions      Session-Historie (mit Summary & Context)
  memory_consolidation Tracking-Metadaten (weight, last_accessed)
  memory_context       Source-Pfade mit Triggern (legacy)
  context_triggers     900+ dynamische Trigger (Lessons/Workflows/Tools)
                       → Feuern in Injektoren + Connector-Routing

KONFIDENZ-SYSTEM:
=================

Das Memory-System verwendet Konfidenz-Werte zur Qualitaetsbewertung von Fakten.

KONFIDENZ-SKALA (0.0 - 1.0):
  1.0       Absolut sicher (verifiziert, mehrfach bestaetigt)
  0.8-0.9   Sehr sicher (aus zuverlaessiger Quelle)
  0.5-0.7   Moderat (Annahme oder Beobachtung)
  0.3-0.4   Unsicher (Vermutung)
  0.0-0.2   Sehr unsicher (zu pruefen)

VISUELLE DARSTELLUNG:
  Konfidenz wird als Balken angezeigt: [*****] = 1.0, [***  ] = 0.6, [*    ] = 0.2

QUELLEN-TRACKING:
  Jeder Fakt kann eine Quelle haben (--source), z.B. "user", "system", "observation"

BEFEHLE (Vollstaendig):
=======================

GRUNDBEFEHLE:
  bach mem write "..."              Arbeitsgedächtnis füllen
  bach --memory facts               Semantisches Wissen abrufen
  bach --memory fact "key:value"    Neuen Fakt speichern
  bach --memory session "..."       Session-Bericht speichern
  bach --memory search "..."        Assoziative Suche
  bach --memory status              Detaillierter Memory-Status
  bach --status                     Memory-Status im Header sehen

LIBRARY API (bach_api.py):
  from bach_api import memory
  memory.write("Notiz")             Working Memory
  memory.facts()                    Alle Fakten
  memory.fact("key:value")          Fakt speichern
  memory.search("query")            Assoziativ suchen
  memory.status()                   Status
  memory.session("Summary")         Session beenden

KONFIDENZ-BEFEHLE:
  bach --memory certain             Nur sichere Fakten anzeigen (>=0.8)
  bach --memory uncertain           Unsichere Fakten zur Pruefung (<0.5)
  bach --memory confidence KEY 0.9  Konfidenz eines Fakts aktualisieren

SESSION-BEFEHLE:
  bach --memory sessions            Alle Sessions anzeigen
  bach --memory sessions N          Letzte N Sessions anzeigen

FAKT MIT KONFIDENZ SPEICHERN:
  bach --memory fact "key:value" --conf=0.8 --source="user"

  Parameter:
    --conf=X      Konfidenz-Wert (0.0-1.0), Standard: 0.5
    --source=X    Quelle des Fakts (z.B. "user", "system", "observation")

KONSOLIDIERUNG:
  bach consolidate run              Lernprozesse starten (Decay/Boost)

HEADLESS API (GUI-Server):
  GET  /api/memory/facts?limit=50         Alle Fakten (JSON)
  POST /api/memory/facts                  Neuen Fakt erstellen
  DEL  /api/memory/facts/<id>             Fakt löschen
  GET  /api/memory/lessons?limit=50       Alle Lessons
  POST /api/memory/lessons                Neue Lesson erstellen
  DEL  /api/memory/lessons/<id>           Lesson deaktivieren

SIEHE AUCH:
  --help injectors      Das Injektor-System
  --help consolidation  Konsolidierungs-Engine
  --help connector      Connector-Integration (context_triggers)
  docs/help/lessons.txt      Umgang mit Lektionen
  bach_api.py           Library API (memory Modul)
  SKILL.md              System-Initialisierung

SHUTDOWN-WORKFLOW:
==================

RICHTIG (neu):
  1. bach --shutdown                  Directory-Scan + Hinweis
  2. bach --memory session "..."      Session-Bericht in DB speichern
  
  Oder alles in einem:
  bach --memory session "THEMA: Was gemacht wurde. NAECHSTE: Was noch kommt."

FALSCH (veraltet):
  - Markdown-Dateien in memory/archive/ erstellen
  - Session-Berichte als .md Dateien speichern

SESSION-BERICHT FORMAT:
=======================

Empfohlenes Format fuer den Summary-Text:

  "THEMA: Kurzbeschreibung.
   
   ERLEDIGT:
   - Aufgabe 1
   - Aufgabe 2
   
   ERSTELLT: X neue Tasks
   
   NAECHSTE SCHRITTE:
   1. Prioritaet 1
   2. Prioritaet 2"

Alternativ kompakt:
  "ATI-Architektur, 9 Tasks erstellt. Naechste: ati.py Handler"

BEST PRACTICES:
===============

1. Session-Start:
   - bach --startup ausfuehren
   - Liest letzte Session aus memory_sessions

2. Waehrend Session:
   - bach mem write "wichtige Erkenntnis"
   - bach --memory fact "projekt.name:BACH"

3. Session-Ende:
   - bach --shutdown
   - bach --memory session "Zusammenfassung"

4. Lessons Learned:
   - bach lesson add "Titel: Loesung"
   - Eigener Handler, nicht --memory!

DATENBANK-SCHEMA:
=================

memory_sessions:
  - session_id          Eindeutige ID (session_YYYYMMDD_HHMMSS)
  - started_at          Startzeit
  - ended_at            Endzeit (NULL wenn aktiv)
  - summary             Session-Bericht
  - tasks_created       Anzahl erstellter Tasks
  - tasks_completed     Anzahl erledigter Tasks
  - continuation_context  Fuer naechste Session

ARCHITEKTUR-DIAGRAMM
====================

Visueller Vergleich Mensch <-> BACH Memory:
  docs/ARCHITECTURE_DIAGRAMS.md  -> Diagramm 4: Memory-System

Zeigt alle 5 kognitiven Typen mit menschlicher Entsprechung
und aktive Prozesse (Vergessen, Erinnern, Lernen, Aufmerksamkeit,
Schlaf-Konsolidierung, Metakognition).

KOGNITIVES MODELL: LERNEN ALS MEMORY-KREISLAUF
===============================================

These: "Lernen ist eine Form von Memory."
(Erarbeitet: User + Claude + Gemini, Januar 2026)

DER LERNPROZESS ALS KREISLAUF:

```
┌─────────────────────────────────────────────────────────────────────┐
│  MEMORY / ERFAHRUNGSSCHATZ (Langzeitspeicher)                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ Lessons      - Was hat funktioniert? Was nicht?               │  │
│  │ Workflows    - WIE geht es? (Prozedurales Gedaechtnis)        │  │
│  │ Sessions     - Was war mein Ziel? (Ausrichtung auf Zukunft)   │  │
│  │ Fakten       - docs/help/ + wiki/ + facts (Weltwissen)        │  │
│  │ Best Pract.  - Zu Regeln gemachte Erfahrungen                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│        │                                                            │
│        │ ABRUF ──> automatisch: Injektoren                          │
│        │      ──> bewusst: Nachdenken                               │
│        v                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  JETZT-EBENE                                                  │  │
│  │  (1) ENERGIESPAREN: Regeln abrufen, automatisch handeln       │  │
│  │  (2) NACHDENKEN: Injektoren provozieren, Szenarien spielen    │  │
│  │  -> HANDELN -> Ergebnis (= neues EREIGNIS)                    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│        │                                                            │
│        v EREIGNIS                                                   │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  SPEICHERN -> lessons, facts, sessions                        │  │
│  └───────────────────────────────────────────────────────────────┘  │
│        │                                                            │
│        v                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  KONSOLIDIERUNG (= Schlaf)                                    │  │
│  │  Komprimieren, Best Practices bilden, Lessons ableiten        │  │
│  └───────────────────────────────────────────────────────────────┘  │
│        │                                                            │
│        v                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  RUECKFLUSS -> Injektoren aktualisieren                       │  │
│  │  System verhaelt sich ANDERS = echtes Lernen                  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│        │                                                            │
│        └──────> zurueck zu MEMORY (neuer Zustand)                   │
└─────────────────────────────────────────────────────────────────────┘
```

ZUORDNUNG: MENSCHLICHES GEDAECHTNIS <-> BACH
--------------------------------------------

| Menschlich               | BACH-Entsprechung              | Funktion                    |
|--------------------------|--------------------------------|-----------------------------|
| Zentrale Exekutive       | Injektoren                     | Aufmerksamkeit steuern      |
| Arbeitsgedaechtnis       | memory_working                 | Aktuelle Session            |
| Prozedurales Gedaechtnis | Workflows, tools/, skills/     | WIE man etwas tut           |
| Episodisches Gedaechtnis | memory_lessons, memory_sessions| WAS passiert ist            |
| Semantisches Gedaechtnis | docs/help/, wiki/, memory_facts | Weltwissen (fast leer*)     |
| Regelwissen              | Best Practices, SKILL.md       | Bewaehrte Erfahrungen       |

*) Semantisches Gedaechtnis ist bei BACH fast leer, weil das Weltwissen
   bereits in den Trainingsdaten des LLM enthalten ist.

INJEKTOREN ALS "GEDANKEN"
-------------------------

Injektoren entsprechen Gedanken im menschlichen Denken:
- AUTOMATISCH: Feuern bei Keyword-Match (wie unbewusste Assoziationen)
- BEWUSST: Gezielt provozieren durch Nachfragen (wie Nachdenken)

Zwei Modi der Verarbeitung:
  (1) ENERGIESPAREN - Schnell, regelbasiert, automatisch
      -> Injektoren feuern, direkte Aktion
  (2) NACHDENKEN - Langsam, assoziativ, bewusst
      -> Injektoren reflektieren, Szenarien durchspielen
  (3) KONSOLIDIERUNG - Offline, komprimierend (= Schlaf)
      -> bach consolidate (Daemon-Job)

AKTUELLER STAND & ZIEL
----------------------

IST-Zustand (seit v1.1.80 teilweise dynamisch):
  Wissen -> Memory (DB) -> Trigger-DB (900+ dynamische Trigger)
  Injektoren sind teilweise dynamisch (Trigger-DB + Python-Dicts)

SOLL-Zustand (in Arbeit):
  Wissen -> Memory (DB) -> Injektoren -> Verhalten aendert sich
                       -> Workflows -> Automation
                       -> Patterns -> Delegation

Der "Rueckfluss" von konsolidiertem Wissen in die Injektoren
ist das fehlende Stueck fuer echtes Lernen.

Siehe auch:
  --help injectors     (Injektor-System)
  --help consolidation (Konsolidierungs-Engine)
  docs/archive/ANALYSE_Lernsysteme_BACH_vs_recludOS.md (Vollanalyse)

---
Version: 1.3.0 | Aktualisiert: 2026-02-08
(Connector-Integration dokumentiert, Library API + Headless API ergaenzt)


## Messagebox

MESSAGEBOX-SYSTEM (VERALTET)
=============================

HINWEIS: Dieses dateibasierte System ist VERALTET und archiviert.
         Aktuelles System: MessagesHandler (system/hub/messages.py)

Das alte Themen-basierte Nachrichtensystem (wie Email, aber dateibasiert)
wurde durch ein SQLite-basiertes System ersetzt.

AKTUELLER ERSATZ:
  Handler:  system/hub/messages.py (MessagesHandler)
  Backend:  system/data/bach.db (messages Tabelle)
  CLI:      bach msg <operation>

SIEHE:
  bach msg --help           Aktuelle Befehle
  system/docs/docs/docs/docs/help/messages.txt  Neue Dokumentation

ARCHIVIERTER CODE:
  system/data/_archive/gui_Entwuerfe/inbox/
    - messagebox_backend.py
    - messagebox.html
    - inbox_index.json

-----------------------------------------------------------------------
ALTE DOKUMENTATION (nur noch historisch)
-----------------------------------------------------------------------

KONZEPT (alt):
  - Ein Thema = eine TXT-Datei
  - Nachrichten werden Themen zugeordnet
  - Index (JSON) fuer schnellen Zugriff
  - Auto-Archivierung bei Groessenlimit

ORDNER (alt):
  DATA/inbox/               Aktive Themen (existiert nicht mehr)
  DATA/inbox/archive/       Archivierte Themen (existiert nicht mehr)
  DATA/inbox/agenda/        Agenda-Referenzen (existiert nicht mehr)

CLI-BEFEHLE (alt, nicht mehr funktional):
  python messagebox_backend.py list [--all]
  python messagebox_backend.py new <titel>
  python messagebox_backend.py add <id> <text>
  python messagebox_backend.py show <id>
  python messagebox_backend.py archive <id>
  python messagebox_backend.py restore <id>

MIGRATION:
  Das alte System wurde nicht migriert. Bei Bedarf koennen alte
  Themen-Dateien aus Backups wiederhergestellt werden.


## Messages

MESSAGES - Nachrichtensystem
============================

BESCHREIBUNG
Internes Nachrichtensystem fuer Kommunikation zwischen User,
System und Agenten. Erreichbar ueber CLI und Web-GUI.

Ohne --from wird automatisch der eingestempelte Partner verwendet.

CLI-BEFEHLE
-----------
bach msg list              Alle Nachrichten anzeigen
bach msg list --inbox      Nur Inbox
bach msg list --outbox     Nur Gesendete
bach msg list --limit 20   Mit Limit (Standard: 10)

bach msg inbox             Inbox anzeigen (Kurzform)
bach msg outbox            Outbox anzeigen (Kurzform)

bach msg unread            Ungelesene Nachrichten anzeigen
bach msg count             Nachrichtenzaehler

bach msg send <to> <text>  Nachricht senden (als user/aktiver Partner)
bach msg send <to> <text> --from <partner>  Von Partner senden

bach msg read <id>         Nachricht lesen (markiert als gelesen)
bach msg read <id> --ack   Lesen mit automatischer Lesebestaetigung

bach msg ping              Ungelesene Nachrichten AN mich anzeigen
bach msg ping --from <p>   Nachrichten an spezifischen Partner

bach msg watch             Polling-Modus: Auf neue Nachrichten warten (Ctrl+C)
bach msg watch --from <p>  Polling fuer spezifischen Partner

bach msg delete <id>       Nachricht(en) loeschen
bach msg delete 1 2 3      Mehrere Nachrichten loeschen
bach msg delete <id> --dry-run  Vorschau (ohne Aenderung)

bach msg archive <id>      Nachricht(en) archivieren
bach msg archive 1 2 3     Mehrere Nachrichten archivieren
bach msg archive <id> --dry-run  Vorschau (ohne Aenderung)

bach msg help              Hilfe anzeigen

MULTI-PARTNER-SUPPORT
---------------------
Partner senden mit eigener Identitaet:

  bach msg send user "Bericht fertig" --from gemini
  bach msg send user "Task erledigt" --from claude
  bach msg send user "Verarbeitung abgeschlossen" --from ollama

Logik:
  --from user    -> Nachricht in User OUTBOX (Standard)
  --from <other> -> Nachricht in User INBOX (unread)

Partner-Identitaeten:
  user      User (Mensch)
  claude    Claude (Operating AI)
  gemini    Gemini (External AI via Antigravity)
  ollama    Ollama (Local AI)
  system    System-Nachrichten

EMPFAENGER
----------
system                     System-Nachrichten
user                       User-Nachrichten
agent:<name>               Spezifischer Agent (z.B. agent:coder)

STATUS-WERTE
------------
unread                     Ungelesen
read                       Gelesen
archived                   Archiviert
deleted                    Geloescht

WEB-GUI
-------
http://127.0.0.1:8000/messages

Features:
- Inbox/Outbox/Archiv Ansicht
- Neue Nachricht verfassen
- Als gelesen markieren
- Nachricht-Detail anzeigen

DATENBANK
---------
Tabelle: messages (in data/bach.db)

Felder:
- id             INTEGER PRIMARY KEY
- direction      TEXT (inbox/outbox)
- sender         TEXT
- recipient      TEXT
- subject        TEXT (geplant - derzeit nicht verwendet)
- body           TEXT
- status         TEXT (unread/read/archived/deleted)
- priority       INTEGER
- created_at     TIMESTAMP
- read_at        TIMESTAMP
- archived_at    TIMESTAMP

BEISPIELE
---------
# Nachricht senden
bach msg send system "Backup abgeschlossen"

# Ungelesene anzeigen
bach msg unread

# Nachricht lesen
bach msg read 5

# Nachricht lesen mit Bestaetigung
bach msg read 5 --ack

# Alle Outbox-Nachrichten
bach msg list --outbox

# Auf neue Nachrichten warten
bach msg watch

# Status pruefen
bach msg count

CONNECTOR-INTEGRATION (v1.1.0)
------------------------------
Nachrichten von externen Connectors (Telegram, Discord, etc.)
werden automatisch in die Inbox geroutet:

  connector_messages (in) → route_incoming() → messages (inbox)

Sender-Format: "connector:sender_id" (z.B. "telegram:123456")
Kontext-Hints werden automatisch als metadata gespeichert.

Ausgehende Nachrichten werden ueber die Queue versendet:

  bach connector send <name> <empfaenger> <text>

Zuverlaessige Zustellung mit Retry/Backoff via Daemon:

  bach connector setup-daemon    # Jobs registrieren
  bach daemon start --bg         # Daemon starten

Siehe: bach --help connector

REST-API (Port 8001)
--------------------
Verfuegbar wenn Headless API laeuft:

  POST /api/v1/messages/send      Nachricht in Queue einreihen
  GET  /api/v1/messages/queue     Queue-Status
  GET  /api/v1/messages/inbox     Inbox lesen (Paginierung, Filter)
  POST /api/v1/messages/route     Routing manuell ausloesen

Beispiel:
  curl localhost:8001/api/v1/messages/inbox?status=unread&limit=10

HANDLER
-------
hub/messages.py            CLI-Handler (Inbox/Outbox)
hub/connector.py           Connector-Handler (Queue, Routing)
gui/api/messages_api.py    REST-API Endpoints
gui/server.py              GUI-Endpunkte (/api/messages)

SIEHE AUCH
----------
bach --help connector      Connector-System (Queue, Retry, Circuit Breaker)
bach --help gui            Web-Dashboard
bach --help daemon         Hintergrund-Jobs
bach --help injectors      Kontext-Injektoren
bach --help wartung        Wartungs-Jobs (automatische Aufgaben)


## Migrate

MIGRATE - Evolutionaere Datei-Migration
=======================================

KONZEPT
-------
Bei Datei-Umbenennungen oder Pfadaenderungen:
Statt alle Verweise auf einmal zu aendern, nutze eine Wrapper-Datei.
Verweise werden organisch korrigiert durch taegliche Nutzung.

WARUM?
------
- Keine harten Brueche
- Verweise werden schrittweise aktualisiert
- Jeder Partner korrigiert was ihn herschickte
- Keine vergessenen Verweise

VORGEHEN
--------
1. Datei umbenennen:
   mv alte_datei.md neue_datei.md

2. Wrapper erstellen (alte_datei.md):
   - Status-Hinweis "umgeleitet"
   - Log-Tabelle fuer Besucher
   - Anleitung: Herkunft pruefen + korrigieren
   - Link zur neuen Datei

3. Kritische Verweise SOFORT korrigieren:
   - docs/docs/docs/help/*.txt (primaere Dokumentation)
   - System-Code der Pfad direkt nutzt
   - CLI-Handler

4. Uebrige evolutionaer migrieren:
   - Partner korrigieren bei Nutzung
   - Path Healer findet automatisch
   - Manual discovery

WRAPPER-TEMPLATE
----------------
# ALTE_DATEI - UMGELEITET

Status: Diese Datei wurde umbenannt zu `neue_datei.md`

## Migration-Log

| Datum | Wer | Herkunft | Verweis korrigiert? |
|-------|-----|----------|---------------------|
| | | | |

## Anleitung

1. Log-Eintrag hinterlassen
2. Herkunft pruefen (was hat dich hergeschickt?)
3. Verweis dort korrigieren
4. Zur eigentlichen Datei gehen

**Zieldatei:** [neue_datei.md](neue_datei.md)

WANN WRAPPER?
-------------
JA (Wrapper sinnvoll):
  - Viele potenzielle Verweise
  - Von verschiedenen Partnern referenziert
  - Keine kritische System-Datei

NEIN (direkt alle aendern):
  - Wenige, bekannte Verweise
  - Kritische System-Dateien
  - Performance-kritische Pfade

CLEANUP
-------
Nach 30 Tagen oder wenn Log leer:
  bach trash delete <wrapper>

AUTOMATISCHE UNTERSTUETZUNG
---------------------------
  bach --maintain heal       Findet veraltete Pfade automatisch
  bach --maintain docs       Erkennt veraltete Dokumentation

BEISPIEL
--------
ROADMAP_ADVANCED.md → ROADMAP.md (2026-01-24):

  1. mv ROADMAP_ADVANCED.md ROADMAP.md
  2. Wrapper ROADMAP_ADVANCED.md erstellt
  3. docs/docs/docs/help/formats.txt korrigiert (kritisch)
  4. 20+ andere Verweise → evolutionaer

SIEHE AUCH
----------
  skills/workflows/migrate-rename.md   Detaillierter Workflow
  docs/docs/docs/help/practices.txt                    Prinzip #3: Evolutionaere Migration
  bach --maintain heal                  Automatische Pfadkorrektur
  bach --maintain docs                  Erkennt veraltete Dokumentation


## Modes

BACH NUTZERMODI (v1.1.37)
=========================

BACH unterstuetzt 4 verschiedene Startup-Modi, die bestimmen,
welche Komponenten beim Start automatisch gestartet werden.

VERFUEGBARE MODI
----------------
  gui      GUI-Modus (Standard)
           - Startet GUI Dashboard im Browser
           - Oeffnet http://127.0.0.1:8000
           - Ideal fuer interaktive Nutzung

  text     Text-Modus
           - Startet nur Konsole mit bach.py
           - Kein Browser wird geoeffnet
           - Ideal fuer Terminal-fokussierte Arbeit

  dual     Dual-Modus
           - Startet GUI + separate Konsole
           - Beide Interfaces parallel nutzbar
           - Ideal fuer Power-User

  silent   Silent-Modus
           - Nichts wird automatisch gestartet
           - Nur Startup-Bericht ausgegeben
           - Ideal fuer Scripts und Automatisierung

MODUS AENDERN
-------------
Dauerhaft (in Config speichern):
  bach --startup mode gui
  bach --startup mode text
  bach --startup mode dual
  bach --startup mode silent

Einmalig (nur diesen Start):
  bach --startup --mode=gui
  bach --startup --mode=text

KONFIGURATION
-------------
Der aktuelle Modus wird in system/data/user_config.json gespeichert:

  {
    "startup_mode": "gui",
    "startup_modes": {
      "gui":    {"gui": true,  "console": false},
      "text":   {"gui": false, "console": true},
      "dual":   {"gui": true,  "console": true},
      "silent": {"gui": false, "console": false}
    }
  }

BEISPIELE
---------
# Normal starten (verwendet gespeicherten Modus)
bach --startup

# Modus dauerhaft auf Text aendern
bach --startup mode text

# Einmalig im Silent-Modus starten
bach --startup --mode=silent

# Quick-Start ohne Dir-Scan im GUI-Modus
bach --startup quick --mode=gui

HINWEISE
--------
- Der Modus wird bei --startup automatisch angezeigt
- GUI-Server bleibt im Hintergrund aktiv bis zum Shutdown
- Im Text-Modus oeffnet sich ein neues Konsolenfenster
- Silent-Modus eignet sich fuer Cron-Jobs und Automations

SIEHE AUCH
----------
  help startup    - Startup-Protokoll Details
  help gui        - GUI Dashboard Dokumentation
  help shutdown   - Session beenden


## Multi Llm

MULTI-LLM PROTOCOL - Koordination paralleler Agenten
=====================================================

Stand: 2026-01-28 v1.1.71

Protokoll V3 fuer sichere parallele Arbeit mehrerer LLMs
(Claude, Gemini, Copilot, Ollama, Perplexity) im selben
Dateisystem. Entwickelt durch Claude + Gemini Experiment
am 2026-01-28.

WICHTIG: RICHTIG STARTEN
========================
ALLE Partner muessen mit Stempelkarte starten!

  # Claude startet
  bach --startup --partner=claude --mode=silent

  # Gemini startet
  bach --startup --partner=gemini --mode=silent

  # Neuer Partner (mit eigenem Namen)
  bach --startup --partner=simonAI --mode=silent

  # Neuer Partner (ohne Namen)
  bach --startup --partner=new --mode=silent

WARUM?
- Automatisches Ein-/Ausstempeln in partner_presence DB
- Partner-Awareness: Erkennt wer noch online ist
- Protokoll V3 wird bei mehreren Partnern automatisch empfohlen
- Between-Task Check erinnert an Partner-Pruefung

CLI-BEFEHLE
-----------
bach llm presence [dir] [task]  Presence erstellen/aktualisieren
bach llm check [dir]            Andere Agenten erkennen
bach llm lock <datei>           Lock erwerben
bach llm unlock [datei]         Lock freigeben
bach llm handshake [dir]        Handshake-Protokoll starten
bach llm status [dir]           Status anzeigen

PROTOKOLL V3 KOMPONENTEN
========================

1. PRESENCE-SYSTEM
------------------
Jeder Agent erstellt eine Presence-Datei im Arbeitsverzeichnis:

Datei:   .<agent>_presence (z.B. .claude_presence)

Inhalt:
  agent: claude
  status: ACTIVE|FINISHED
  started: 2026-01-28T01:00:00
  heartbeat: 2026-01-28T01:05:00
  working_on: TASK_BESCHREIBUNG
  current_file: datei.txt
  lock_status: FREE|LOCKED|WAITING

Regeln:
- Heartbeat alle 30-60 Sekunden aktualisieren
- Heartbeat aelter als 2 Minuten = Agent inaktiv
- Bei Session-Ende: status auf FINISHED setzen

2. LOCKING-SYSTEM
-----------------
Vor Schreibzugriff auf geteilte Dateien:

Lock-Datei: <datei>.lock.<agent>
Beispiel:   PROTOKOL.md.lock.claude

Workflow:
  1. list_directory - Pruefen ob fremder .lock.* existiert
  2. Falls ja -> WARTEN (5 Sek Backoff, dann erneut)
  3. Falls nein -> Lock erstellen
  4. Backup erstellen (<datei>.bak)
  5. Datei bearbeiten
  6. Lock SOFORT loeschen

Lock-Inhalt:
  agent: claude
  locked_at: 2026-01-28T01:00:00
  file: PROTOKOL.md

Timeout: Lock aelter als 5 Minuten gilt als "stale"
         und kann von anderem Agent geloescht werden.

3. BACKUP-SYSTEM
----------------
VOR jeder Aenderung an geteilten Dateien:
- Backup erstellen: <datei>.bak
- Erst danach schreiben
- Backup bleibt fuer Recovery

4. HANDSHAKE-PROTOKOLL
----------------------
Auto-Detection wenn sich Agenten begegnen:

Ablauf:
  1. Agent A erstellt Presence
  2. Agent A erkennt Agent B (via detect_other_agents)
  3. Agent A erstellt: .handshake_<agent_a>
  4. Agent B erkennt Handshake-Anfrage
  5. Agent B antwortet: .handshake_<agent_b> mit ACCEPTED
  6. Beide aktivieren Protokoll V3

Handshake-Datei:
  from: claude
  to: gemini
  time: 2026-01-28T01:00:00
  status: ACCEPTED
  protocol: V3

KOMMUNIKATION
=============

Meta-Ebene (asynchron):
  bach msg send <partner> "Nachricht"
  bach msg list
  bach msg read <id>

Echtzeit (im Arbeitsordner):
  Presence-Dateien fuer Status
  In-File-Kommunikation (Eintraege mit Timestamp)

In-File-Format:
  [HH:MM] [Agent] Nachricht oder Aktion

WORKFLOW: GEMEINSAME DATEI BEARBEITEN
=====================================

1. Presence pruefen:
   bach llm check

2. Lock erwerben:
   bach llm lock DATEI.md

3. Backup erstellen:
   (automatisch bei safe_write)

4. Datei bearbeiten

5. Lock freigeben:
   bach llm unlock DATEI.md

6. Presence aktualisieren:
   bach llm presence . "Fertig"

BEISPIEL SESSION
================

# Agent A startet
bach llm presence . "Task_123"
bach llm check              # -> "Keine anderen Agenten"

# Agent B startet
bach llm presence . "Task_456"
bach llm check              # -> "claude: AKTIV"

# Agent A will SHARED.txt bearbeiten
bach llm lock SHARED.txt    # -> "Lock erworben"
# ... bearbeitet ...
bach llm unlock SHARED.txt

# Agent B wartet automatisch wenn Lock existiert
bach llm lock SHARED.txt    # -> Wartet bis A fertig

BEKANNTE AGENTEN
================

- claude      Claude (Anthropic)
- gemini      Gemini (Google)
- copilot     GitHub Copilot
- ollama      Lokale LLMs
- perplexity  Perplexity AI

DATEIEN IM ARBEITSORDNER
========================

.claude_presence       Presence Claude
.gemini_presence       Presence Gemini
DATEI.lock.claude      Lock von Claude
DATEI.lock.gemini      Lock von Gemini
DATEI.bak              Backup vor Aenderung
.handshake_claude      Handshake-Signal
.handshake_gemini      Handshake-Antwort

TROUBLESHOOTING
===============

Problem: Lock bleibt haengen
Loesung: Lock aelter als 5 Min wird als stale betrachtet
         und automatisch ignoriert. Manuell loeschen OK.

Problem: Agent erkennt anderen nicht
Loesung: Presence-Datei pruefen. Heartbeat aktuell?

Problem: Race Condition trotz Lock
Loesung: Pruefen ob list_directory VOR Lock-Erstellung
         ausgefuehrt wird. Timing-Problem?

HANDLER
-------
hub/multi_llm_protocol.py   Protokoll-Implementation

LESSONS
-------
Lesson #62: Multi-LLM Parallelarbeit Grundlagen
Lesson #63: Multi-LLM Protokoll V3

SIEHE AUCH
----------
bach --help partner   Partner-System
bach --help messages       Nachrichten


STEMPELKARTEN-SYSTEM (v1.1.71)
==============================
DB-basierte Partner-Praesenz fuer automatische Awareness.

TABELLE: partner_presence
  id               INTEGER PRIMARY KEY
  partner_name     TEXT     Partner-ID (claude, gemini, user, ...)
  status           TEXT     online|offline|crashed
  clocked_in       TEXT     Einstempel-Zeitpunkt
  clocked_out      TEXT     Ausstempel-Zeitpunkt
  last_heartbeat   TEXT     Letzte Aktivitaet
  current_task     TEXT     Aktuelle Aufgabe
  session_id       TEXT     Zugehoerige Session

AUTOMATISCH:
- Bei --startup: Clock-In (alte crashed Sessions markiert)
- Bei --shutdown: Clock-Out
- Partner-Awareness im Startup-Output

MANUELL (optional):
- Heartbeat: bach llm presence . "Task_XYZ"
- Status: bach llm status

TIMEOUT:
- Heartbeat aelter als 5 Minuten = Partner inaktiv
- Crashed Sessions werden bei naechstem Startup bereinigt


## Naming

NAMENSKONVENTIONEN
==================

Stand: 2026-02-08

ZEITSTEMPEL-FORMATE
-------------------
  Session-ID:   YYYYMMDD_HHMM         (20260111_0315)
  Chat-ID:      msg_YYYYMMDD_HHMMSS   (msg_20260111_031504)
  Dokument:     DD.MM.YYYY            (11.01.2026)
  JSON-Felder:  ISO 8601              (2026-01-11T03:15:04)

DATEIEN
-------
  Bericht:      Bericht_YYYYMMDD_HHMM.md
  Forensik:     REPORT_YYYY-MM-DD_Thema.md
  Konzept:      KONZEPT_Name.md oder CONCEPT_Name.md
  Analyse:      ANALYSE_Name.md
  Recherche:    RECHERCHE_Name.md
  Schema:       *_schema.md
  Template:     TEMPLATE_Name.md

TOOL-PRAEFIXE (tools/*.py)
--------------------------
Praefixe kennzeichnen den Typ und Einsatzzweck eines Tools.

  PRAEFIX   BEDEUTUNG                BEISPIELE
  -------   ----------------------   ---------------------------
  c_        CLI-optimiert fuer AI    c_encoding_fixer.py
            (Claude/recludOS)        c_json_repair.py
            - Klare, parsbare Outputs
            - Encoding-sicher (UTF-8)

  m_        Maintain/Wartung         m_migrate_triggers.py
            - Aufraeum-Tools         m_cleanup_logs.py
            - Migrations-Scripts

  b_        BACH-Kern (System)       backup_manager.py
            - Von bach.py genutzt    bach_auto_discovery.py
            - Kritische Funktionen

  check_    Validatoren              check_my_tasks.py
            - Einmalige Pruefungen

  fix_      Quick-Fixes              fix_injectors.py
            - Repariert spezifische Bugs

SKILL-SPEZIFISCHE TOOLS (NEU)
-----------------------------
Tools die nur fuer einen Skill relevant sind:

  Namenskonvention: <skill>_<funktion>.py

  Beispiele:
    steuer_scanner.py       # Steuer-Expert spezifisch
    steuer_sync.py          # Steuer-Expert spezifisch
    task_scanner.py         # ATI-Agent spezifisch (in agents/ati/scanner/)

  Speicherort:
    - Allgemein:  tools/c_ocr_engine.py
    - Spezifisch: agents/_experts/steuer/steuer_scanner.py
    - Agent-Tool: agents/ati/scanner/task_scanner.py

  REGEL: Im Zweifel doppelt halten!
  Skill-spezifische Tools MUESSEN beim Export inkludiert werden.

PYTHON-TOOL-HEADER (NEU - Pflicht)
----------------------------------
Jedes Tool braucht einen Standard-Header:

  """
  Tool: tool_name
  Version: X.Y.Z
  Author: [author]
  Created: YYYY-MM-DD
  Updated: YYYY-MM-DD
  Anthropic-Compatible: True

  VERSIONS-HINWEIS: Pruefe auf neuere Versionen

  Description:
      Was das Tool tut.
  """

  __version__ = "X.Y.Z"
  __author__ = "[author]"

Template: system/skills/_templates/TEMPLATE_TOOL.py

SKILL-ORDNER-NAMEN
------------------
  Format: lowercase-mit-bindestrich

  Beispiele:
    agents/entwickler/
    agents/persoenlicher-assistent/
    agents/_experts/steuer/
    agents/_experts/foerderplaner/

SKILL-DATEIEN
-------------
  SKILL.md        Hauptdefinition (Pflicht)
  config.json     Konfiguration (Optional)
  README.md       Nur fuer Navigation (Nicht fuer Konzepte!)

TASK-IDS & PROJEKTE
-------------------
  IDs:         Numerisch (1, 2, 712) - Automatisch vergeben.
  Labels/Pfx:  Fuer die Beschreibung genutzte Gruppen:
               SYS_    System-Kern
               WF_     Workflow-Entwicklung
               GUI_    Frontend-Themen
               FIN_    Finanz-Modul
               HEALTH_ Forensik & Wartung
               SKILL_  Skill-Architektur (NEU)
               LANG_   Internationalisierung

VERBOTEN
--------
  Dateinamen:  / \ : * ? " < > | Umlaute

SIEHE AUCH
----------
  bach --help tools            Tool-Verwaltung und Ausfuehrung
  bach --help skills           Skill-System
  system/tools/_policies/      Policy-Validatoren
  system/skills/_templates/    Standard-Templates


## News

NEWS-AGGREGATION
================

Sammelt News aus verschiedenen Quellen (RSS, Web, YouTube).
Typ-Erkennung: /feed, /rss, .xml -> RSS, youtube.com -> YouTube, sonst Web.

BEFEHLE
-------

  # Quellen verwalten
  bach news add <url> [--type rss|web|youtube] [--category X] [--name "..."]
  bach news list                    Alle Quellen anzeigen
  bach news remove <id>             Quelle entfernen
  bach news categories              Kategorien-Uebersicht
  bach news stats                   Statistiken

  # News abrufen
  bach news fetch                   Alle aktiven Quellen abrufen
  bach news fetch --source <id>     Einzelne Quelle abrufen

  # News lesen
  bach news items                   Neueste Artikel
  bach news items --unread          Nur ungelesene
  bach news items --category technik  Nach Kategorie filtern
  bach news items --limit 50        Mehr Ergebnisse

  # Gelesen-Status
  bach news read <id>               Einzelnen Artikel als gelesen markieren
  bach news read all                Alle als gelesen markieren

BEISPIELE
---------

  bach news add https://feeds.feedburner.com/TechCrunch --category technik
  bach news add https://youtube.com/channel/UC... --name "Kanal"
  bach news fetch
  bach news items --unread --limit 10

ABHAENGIGKEIT
-------------
  pip install feedparser     (Pflicht fuer RSS)


## Newspaper

NEWSPAPER (TAEGLICHE ZEITUNG)
============================

Generiert eine taegliche PDF-Zeitung aus gesammelten News-Items.

WORKFLOW
--------
  1. bach news fetch              News aus allen Quellen abrufen
  2. bach newspaper generate      Zeitung generieren (HTML + PDF)
  3. bach newspaper deliver       Zeitung zustellen (Desktop/Telegram)

BEFEHLE
-------

  # Generieren
  bach newspaper generate                    Zeitung fuer heute
  bach newspaper generate --date 2026-02-18  Bestimmtes Datum

  # Zustellen
  bach newspaper deliver                     Alle konfigurierten Kanaele
  bach newspaper deliver --channel telegram  Nur Telegram
  bach newspaper deliver --channel desktop   Nur Desktop-Kopie

  # Verwaltung
  bach newspaper config                      Konfiguration anzeigen
  bach newspaper history                     Bisherige Ausgaben

KONFIGURATION
-------------
  Datei: hub/_services/newspaper/config.json

  title                 Zeitungstitel
  categories            Kategorien-Reihenfolge
  max_items_per_category  Max. Artikel pro Kategorie
  delivery.desktop_copy   Kopie auf Desktop (true/false)
  delivery.telegram       Via Telegram senden (true/false)
  delivery.email          Via Email senden (true/false)

AUSGABE
-------
  HTML + PDF in: user/newspaper/
  PDF via Edge Headless (automatisch)


## Notizblock

NOTIZBLOCK - Freie Notizen und Themen-Notizbuecher
===================================================

BESCHREIBUNG:
  Dateibasierter Service fuer freie Notizen. Alles landet im Standard-
  Notizblock wenn kein anderes Ziel angegeben ist. Beliebig viele
  thematische Notizbuecher und Themenordner anlegbar.

  Skill-Datei: skills/_services/notizblock.md
  User-Daten:  user/notizen/

DATEISTRUKTUR:
  user/notizen/
  +-- Notizblock.txt          Standard-Inbox (immer vorhanden)
  +-- Einkaufsliste.txt       Weiterer Notizblock (gleiche Ebene)
  +-- Thema A/
  |   +-- Formeln.txt         Notizblock im Themenordner
  +-- Thema B/
  |   +-- Ideen.txt
  +-- Archiv/
      +-- Notizblock_2026-01.txt

ANLEGEN:
  "Lege neuen Notizblock an namens Einkaufsliste"
    -> user/notizen/Einkaufsliste.txt

  "Lege Thema an namens Physik"
    -> Ordner user/notizen/Physik/

  "Lege Notizblock in Thema Physik namens Formeln an"
    -> user/notizen/Physik/Formeln.txt

  Ohne Angabe -> immer in Notizblock.txt

EINTRAG-FORMAT (Notizblock.txt):
  ---
  [2026-02-18 14:30]
  Schnelle Notiz ohne Zuweisung.

  ---
  [2026-02-18 15:00]
  Interviewidee mit Prof. Wagner.
  #NB: interviews

TRANSFER-MARKIERUNG (#NB:):
  Eintraege mit #NB: werden auf Befehl in das Zielnotizbuch verschoben:
    #NB: Einkaufsliste        -> nach user/notizen/Einkaufsliste.txt
    #NB: Physik/Formeln       -> nach user/notizen/Physik/Formeln.txt

  Ausfuehren: "Fuehre alle #NB-Transfers durch"
  Claude entfernt die Markierung nach dem Transfer.

CLI-BEFEHLE (PLAN):
  bach notiz "Meine Notiz"                Schnell in Notizblock.txt
  bach notiz "Text" --in Einkaufsliste    In bestimmtes Notizbuch
  bach notiz "Text" --in "Physik/Formeln"

  bach notiz neu Einkaufsliste            Neues Notizbuch anlegen (Datei)
  bach notiz neu "Physik"                 Neues Thema anlegen (Ordner)
  bach notiz neu "Physik/Formeln"         Notizbuch im Thema anlegen

  bach notiz show                         Standard-Notizblock (letzte 20)
  bach notiz show Einkaufsliste           Bestimmtes Notizbuch
  bach notiz show --alle                  Alle Notizbuecher

  bach notiz transfer                     #NB: Transfers ausfuehren
  bach notiz transfer --preview           Vorschau ohne Ausfuehren
  bach notiz archiv                       Block archivieren, neu starten
  bach notiz suche "Wagner"               Volltextsuche

INTEGRATION:
  Transkriptions-Service:   bach transkript to-notizblock <datei>
  Persoenlicher Assistent:  Schnellnotizen im Gespraech
  Research-Agent:           Recherche-Fragmente sammeln
  Decision-Briefing:        Entscheidungs-Kontext notieren

STATUS:
  Service aktiv (notizblock.md). CLI-Implementierung ausstehend (Phase 2).
  Dateibasiert, kein DB-Eintrag noetig.

SIEHE AUCH:
  bach help transkription   Transkriptions-Service
  bach help entscheidung    Decision-Briefing
  bach help agents          Agenten-Uebersicht


## Npm Publish

NPM PUBLISH - MCP Server Veroeffentlichung
============================================

STAND: 2026-02-15

Workflow zum Veroeffentlichen der BACH MCP Server auf NPM und GitHub.

PAKETE
------
  bach-filecommander-mcp    39 Tools, Filesystem/Prozesse/Sessions/i18n
  bach-codecommander-mcp    15 Tools, Code-Analyse/JSON/Encoding/i18n

GITHUB REPOS
-------------
  https://github.com/lukisch/bach-filecommander-mcp
  https://github.com/lukisch/bach-codecommander-mcp

NPM AUTHENTIFIZIERUNG
----------------------
  Methode: Granular Access Token mit "Bypass 2FA"
  Token-Name: bach-publisher 2
  Erstellt: 2026-02-15
  Laeuft ab: 2026-05-16
  Gespeichert in: ~/.npmrc

  WICHTIG: Classic Automation Tokens funktionieren NICHT mehr (EOTP-Fehler).
  Nur Granular Access Tokens mit "Bypass 2FA" umgehen die OTP-Abfrage.

  Token erneuern (wenn abgelaufen):
    1. https://www.npmjs.com/settings/~/tokens -> "Generate New Token"
    2. "Granular Access Token" waehlen (NICHT Classic!)
    3. Permissions: Read and Write, alle Packages
    4. "Bypass 2FA" Checkbox aktivieren
    5. Token in ~/.npmrc eintragen:
       //registry.npmjs.org/:_authToken=<neuer-token>

NPM PUBLISH WORKFLOW
---------------------
  1. Token pruefen:
     npm whoami    -> muss "lukisch" ausgeben

  2. Build manuell ausfuehren (wegen & im Pfad KI&AI):
     node "<pfad>/node_modules/typescript/bin/tsc" --project "<pfad>/tsconfig.json"

  3. npm publish ausfuehren (kein OTP, kein Browser noetig):
     cd <projektverzeichnis>
     npm publish --ignore-scripts

BEKANNTE PROBLEME
------------------
  - & im Pfad "KI&AI" stoert npm scripts (prepublishOnly)
    -> Workaround: --ignore-scripts (Build vorher manuell)
  - npm run build schlaegt fehl im Projektverzeichnis
    -> Workaround: tsc direkt ueber node aufrufen
  - Classic Automation Tokens loesen EOTP-Fehler aus
    -> Workaround: Granular Access Token mit "Bypass 2FA"

GITHUB WORKFLOW
----------------
  1. git add <dateien> && git commit -m "message"
  2. git tag vX.Y.Z
  3. git push origin master --tags

VERSION BUMP CHECKLISTE
------------------------
  [ ] package.json version
  [ ] src/index.ts version (server config)
  [ ] CHANGELOG.md neuer Eintrag
  [ ] README.md falls Features sich aendern
  [ ] Build testen
  [ ] Git commit + tag + push
  [ ] npm publish --ignore-scripts

SIEHE AUCH
----------
  docs/help/tools.txt         Tool-Uebersicht
  docs/help/coding.txt        Coding-Standards
  skills/workflows/npm-mcp-publish.md  Ausfuehrliches Protokoll


## Ollama

BACH OLLAMA-INTEGRATION
=======================
Lokaler LLM-Server fuer Token-Sparmodus und Offline-Nutzung.

BEFEHLE
-------
bach ollama status           Verbindung pruefen, installierte Modelle
bach ollama ask "prompt"     Direkte Anfrage an Ollama
bach ollama embed "text"     Embedding generieren
bach ollama models           Verfuegbare Modelle auflisten

OPTIONEN
--------
--model=NAME              Modell waehlen (default: llama3.2)

BEISPIELE
---------
# Status pruefen
bach ollama status

# Einfache Frage
bach ollama ask "Was ist BACH?" --model=llama3.2

# Code-Review delegieren
bach ollama ask "Review diesen Code: def add(a,b): return a+b"

# Embedding fuer Suche
bach ollama embed "Suchtext fuer RAG"

INTEGRATION MIT PARTNER-SYSTEM
------------------------------
Ollama ist als lokaler Partner registriert und wird automatisch
bei hohem Token-Verbrauch bevorzugt:

Zone 3 (60-80% Tokens):  Ollama wird bevorzugt
Zone 4 (80-100%):        Nur Human/Notfall (Ollama noch moeglich)

Automatische Delegation:
  bach partner delegate "Task" --to=ollama

Fallback bei Netzwerkproblemen:
  bach ollama ask "Task"   (direkte lokale Ausfuehrung)

VORAUSSETZUNGEN
---------------
- Ollama muss lokal installiert sein
- Standard-Port: http://localhost:11434
- Mindestens ein Modell muss gepullt sein

Installation pruefen:
  ollama --version
  ollama list

Modell installieren:
  ollama pull llama3.2
  ollama pull codellama

TROUBLESHOOTING
---------------
Fehler: "Connection refused"
  → Ollama-Server starten: ollama serve
  → Port pruefen: http://localhost:11434

Fehler: "Model not found"
  → Modell pullen: ollama pull llama3.2
  → Modellnamen pruefen: ollama list

Langsame Antworten:
  → Kleineres Modell waehlen (llama3.2 statt llama3.1:70b)
  → GPU-Nutzung pruefen (CUDA/Metal)

Speicherprobleme:
  → Kleineres Modell verwenden
  → Andere Modelle entladen: ollama stop

KONFIGURATION
-------------
Ollama-Einstellungen in BACH:
  - Partner-ID: ollama
  - Typ: local
  - Standardmodell: llama3.2 (konfigurierbar)
  - Timeout: 120 Sekunden

Anpassung via:
  bach partner info ollama

SIEHE AUCH
----------
bach help partner          Partner-System Uebersicht
bach help delegate         Task-Delegation
bach help tools            Tool-Inventar (ollama_client.py)


## Operatoren

OPERATOREN-TAXONOMIE
====================
Vollstaendige Klassifikation der Datenverarbeitungs-Operatoren
fuer Watcher, Toolchains, Injektoren und Automatisierung.

Bezug: Lernsystem-Analyse (user/_archive/ANALYSE_Lernsysteme_BACH_vs_recludOS.md)


1. ERKENNUNGS-OPERATOREN ("Sinne")
===================================
Wie das System Veraenderungen in der Umwelt wahrnimmt.

1.1 Polling (periodisches Abfragen)
------------------------------------
Regelmaessiges Pruefen eines Zustands.
  - Verzeichnisinhalt bei t0 und t1 vergleichen
  - API alle 5 Minuten abfragen
  - Cron-Jobs fuer Systemmetriken
BACH: TimeInjector, Daemon-Checks, Session-Start-Scan

1.2 Event-Driven (Push-basiert)
-------------------------------
Reaktion auf externe Ereignisse.
  - Filesystem-Events (inotify)
  - Webhooks (GitHub, Stripe)
  - Message-Queues (Kafka, RabbitMQ)
BACH: Noch nicht implementiert. Toolchain-Events als erster Schritt.

1.3 Snapshot-Diffing
--------------------
Zwei Zustaende vergleichen und Abweichungen extrahieren.
  - Datei-Hashes vergleichen
  - Datenbank-Snapshot vs. Live-Daten
  - Konfigurations-Drift erkennen
BACH: RAG tools/rag/ingest.py (MD5 Change Detection), DirScan


2. ANALYSE-OPERATOREN
=====================
Wie das System Daten versteht und einordnet.

2.1 Vergleichen
---------------
Zwei oder mehr Werte gegenueberstellen.
  - Hash-Vergleich
  - Feld A == Feld B
  - Zeitstempel t0 < t1

2.2 Messen
----------
Quantitative Eigenschaften bestimmen.
  - Dateigroesse
  - Latenzzeit
  - CPU-Auslastung
  - Anzahl neuer Datensaetze

2.3 Filtern
-----------
Daten anhand von Regeln reduzieren.
  - Nur Dateien > 10 MB
  - Nur E-Mails mit Betreff "Rechnung"
  - Nur API-Antworten mit Status 200

2.4 Klassifizieren
------------------
Daten in Kategorien einordnen.
  - Spam vs. Nicht-Spam
  - Dokumenttyp erkennen (Rechnung, Vertrag, Mahnung)
  - Log-Level (INFO, WARN, ERROR)
BACH: OCR-Kategorisierung (Office Lens), Skill-Typen

2.5 Gruppieren
--------------
Daten nach Merkmalen zusammenfassen.
  - Logs nach Service gruppieren
  - Rechnungen nach Monat gruppieren
  - Dateien nach Dateityp gruppieren

2.6 Aggregieren
---------------
Gruppen zusammenfassen oder verdichten.
  - Summe aller Rechnungsbetraege
  - Durchschnittliche CPU-Last
  - Anzahl Dateien pro Ordner

2.7 Korrelieren
---------------
Beziehungen zwischen Datenpunkten erkennen.
  - Log-Events mit Request-ID verknuepfen
  - Sensorwert + Zeitstempel + Standort
  - Fehler + vorherige Systemlast
BACH: Assoziatives Memory (memory_associations)

2.8 Validieren
--------------
Pruefen, ob Daten Regeln erfuellen.
  - JSON-Schema-Validierung
  - IBAN-Pruefung
  - Pflichtfelder vorhanden?

2.9 Normalisieren
-----------------
Daten in ein einheitliches Format bringen.
  - Datumsformate vereinheitlichen
  - Gross-/Kleinschreibung angleichen
  - Waehrungsumrechnung


3. TRANSFORMATIONS-OPERATOREN
=============================
Wie das System Daten umwandelt.

3.1 Extrahieren
---------------
Informationen aus Rohdaten herausloesen.
  - OCR aus PDF
  - Regex aus Text
  - JSON-Felder aus API-Antwort
BACH: OCR-Pipeline, RAG Chunking

3.2 Transformieren
------------------
Daten in eine andere Form ueberfuehren.
  - CSV -> JSON
  - Text -> Tokens
  - Bild -> Thumbnail

3.3 Anreichern (Enrichment)
----------------------------
Daten mit zusaetzlichen Informationen ergaenzen.
  - Geo-Lookup (IP -> Land)
  - Kundendaten aus CRM ergaenzen
  - KI-basierte Klassifikation hinzufuegen
BACH: RAG Search (semantische Anreicherung)

3.4 Zusammenfuehren (Merge/Join)
---------------------------------
Mehrere Datenquellen kombinieren.
  - Tabellen per Schluessel verbinden
  - Logs aus mehreren Services zusammenfuehren
  - E-Mail + CRM-Eintrag matchen


4. ZEITBEZOGENE OPERATOREN
==========================

4.1 Sequenzieren
----------------
Reihenfolgen herstellen oder analysieren.
  - Sortieren nach Zeitstempel
  - Workflow-Schritte nacheinander ausfuehren
  - Ereignisfolgen rekonstruieren
BACH: Toolchain-Engine (hub/chain.py), Session-Reihenfolge

4.2 Fensterung (Windowing)
---------------------------
Daten in Zeitfenster einteilen.
  - 5-Minuten-Durchschnitt
  - Rolling Window fuer Sensorwerte
  - Sliding Window fuer Log-Analysen


5. KONTROLL-OPERATOREN
======================

5.1 Debouncing
--------------
Mehrere schnelle Ereignisse zu einem zusammenfassen.
  - Dateiaenderungen buendeln
  - UI-Events reduzieren
  - API-Requests throttlen

5.2 Rate-Limiting
-----------------
Begrenzen, wie oft etwas passieren darf.
  - Max. 10 API-Calls pro Minute
  - E-Mail-Benachrichtigungen drosseln
BACH: Token-Budget-Zonen (Konzept aus recludOS)

5.3 Retry-Strategien
--------------------
Wiederholungslogik bei Fehlern.
  - Exponentielles Backoff
  - Feste Retry-Intervalle
  - Retry bis Timeout


6. SPEICHER- UND ZUSTANDS-OPERATOREN
=====================================

6.1 Stateful Processing
------------------------
Vorherige Werte werden gespeichert.
  - Letzten Hash merken
  - Letzten API-Stand speichern
  - Sliding Window mit Zustand
BACH: Memory-System (alle 5 Schichten), Session-State

6.2 Stateless Processing
-------------------------
Jede Verarbeitung ist unabhaengig.
  - Hash einer Datei berechnen
  - JSON validieren
  - Regex-Match


7. META-OPERATOREN (hoehere Abstraktion)
=========================================

7.1 Orchestrieren
-----------------
Mehrere Operatoren zu einem Workflow verbinden.
  - n8n-Pipelines
  - Airflow DAGs
  - Kubernetes CronJobs + Worker
BACH: Toolchain-Engine (hub/chain.py), Workflows (skills/workflows/), Dev-Zyklus

7.2 Optimieren
--------------
Datenverarbeitung effizienter machen.
  - Caching
  - Parallelisierung
  - Indexierung

7.3 Beobachten (Observability)
-------------------------------
Systemzustaende erfassen und interpretieren.
  - Logging
  - Metriken
  - Tracing
BACH: Session-Logging, Task-Statistik, Daemon-Status


8. OPERATOR-PATTERNS (Kombinationen)
=====================================
Typische Kombinationen von Operatoren fuer wiederkehrende Aufgaben.

8.1 Scoring & Ranking Pattern (#9)
-----------------------------------
Zweck: Elemente bewerten und sortieren.
Operatoren: Messen, Bewerten, Aggregieren, Sortieren.
  - E-Mails nach Relevanz sortieren
  - Dokumente nach "Wahrscheinlichkeit Rechnung" ranken

8.2 Classification Pipeline Pattern (#10)
------------------------------------------
Zweck: Daten in Klassen einteilen.
Operatoren: Extrahieren, Normalisieren, Klassifizieren, Validieren.
  - Dokumenttyp (Rechnung/Vertrag/Mahnung)
  - Ticket-Prioritaet (Low/Medium/High)

8.3 Rule-Based Filtering Pattern (#11)
---------------------------------------
Zweck: Ausschliessen anhand fester Regeln.
Operatoren: Filtern, Validieren, Ausschliessen.
  - Absender auf Blacklist
  - Dateien ohne Anhang verwerfen

8.4 Threshold Alert Pattern (#12)
----------------------------------
Zweck: Alarm bei Grenzwertueberschreitung.
Operatoren: Messen, Vergleichen, Bewerten, Event-Trigger.
  - CPU > 80%
  - mehr als 10 Fehler in 5 Minuten

8.5 Anomaly Detection Light Pattern (#13)
------------------------------------------
Zweck: Auffaellige Werte erkennen (einfach).
Operatoren: Messen, Aggregieren, Vergleichen, Fensterung.
  - Wert > Mittelwert + Faktor
  - ploetzlicher Sprung in Dateianzahl

8.6 Deduplication Pattern (#14)
--------------------------------
Zweck: Dubletten erkennen und entfernen.
Operatoren: Vergleichen, Gruppieren, Aggregieren, Filtern.
  - doppelte Rechnungen
  - doppelte E-Mails / IDs

8.7 Canonicalization Pattern (#15)
-----------------------------------
Zweck: Daten auf kanonische Form bringen.
Operatoren: Normalisieren, Transformieren, Validieren.
  - Namen, Adressen, Datumsformate vereinheitlichen

8.8 Golden Record Pattern (#16)
--------------------------------
Zweck: "beste" Version eines Datensatzes bestimmen.
Operatoren: Zusammenfuehren, Bewerten, Aggregieren, Validieren.
  - Kundendaten aus mehreren Systemen
  - Stammdatenpflege

8.9 Multi-Stage Validation Pattern (#17)
-----------------------------------------
Zweck: Validierung in Stufen.
Operatoren: Validieren, Klassifizieren, Filtern.
  - Syntax -> Semantik -> Geschaeftsregeln
  - "weich" vs. "hart" fehlerhafte Datensaetze

8.10 Fallback Resolution Pattern (#18)
---------------------------------------
Zweck: Alternative Wege bei Fehlern.
Operatoren: Testen, Retry, Fallback, Bewerten.
  - primaere API down -> sekundaere API
  - KI-Klassifikation unsicher -> Regelwerk

8.11 A/B Testing Pattern (#19)
-------------------------------
Zweck: Zwei Strategien gegeneinander testen.
Operatoren: Testen, Vergleichen, Bewerten, Aggregieren.
  - zwei Klassifikationsmodelle
  - zwei Regelsets fuer Mailrouting

8.12 Multi-Criteria Decision Pattern (#20)
-------------------------------------------
Zweck: Entscheidung nach mehreren Kriterien.
Operatoren: Messen, Bewerten, Aggregieren, Ranking.
  - "beste" Zuordnung zu Kostenstelle
  - Priorisierung von Tickets

8.13 Routing by Category Pattern (#21)
---------------------------------------
Zweck: Weiterleitung nach Kategorie.
Operatoren: Klassifizieren, Filtern, Routing.
  - Rechnungen -> Buchhaltung
  - Bewerbungen -> HR

8.14 Confidence-Based Handling Pattern (#22)
---------------------------------------------
Zweck: Verhalten abhaengig von Sicherheit/Score.
Operatoren: Bewerten, Klassifizieren, Filtern.
  - Score > 0.9 -> auto buchen
  - Score 0.6-0.9 -> manuelle Pruefung

8.15 Progressive Refinement Pattern (#23)
------------------------------------------
Zweck: Schrittweise Verfeinerung.
Operatoren: Klassifizieren, Anreichern, Transformieren.
  - grobe Kategorie -> feine Unterkategorie
  - erst Dokumenttyp, dann Inhaltsextraktion

8.16 Sanity Check Pattern (#24)
--------------------------------
Zweck: Einfache Plausibilitaetspruefungen.
Operatoren: Testen, Validieren, Ausschliessen.
  - Betrag > 0
  - Datum nicht in der Zukunft

8.17 Cross-Source Consistency Pattern (#25)
--------------------------------------------
Zweck: Daten gegen andere Quelle testen.
Operatoren: Vergleichen, Zusammenfuehren, Validieren.
  - Rechnungsbetrag vs. ERP
  - Kundennummer vs. CRM

8.18 Error Classification Pattern (#26)
----------------------------------------
Zweck: Fehlerarten kategorisieren.
Operatoren: Klassifizieren, Gruppieren, Aggregieren.
  - Netzwerkfehler vs. Datenfehler
  - Benutzerfehler vs. Systemfehler

8.19 Recovery Strategy Pattern (#27)
-------------------------------------
Zweck: Definierte Reaktion auf Fehler.
Operatoren: Testen, Retry, Fallback, Logging.
  - Queue -> Dead Letter Queue
  - manuelle Nachbearbeitungsliste

8.20 Human-in-the-Loop Pattern (#28)
-------------------------------------
Zweck: Mensch bei Unsicherheit einbinden.
Operatoren: Bewerten, Klassifizieren, Routing.
  - Score zu niedrig -> Review-Inbox
  - Konfliktfaelle -> Freigabeprozess


BEZUG ZUM LERNPROZESS
=====================
Die Operatoren bilden das Werkzeug-Set fuer alle 3 Modi:

  (1) Energiesparen: Polling + Filtern + Regeln abrufen
  (2) Nachdenken:    Korrelieren + Klassifizieren + Szenarien
  (3) Konsolidierung: Aggregieren + Normalisieren + Gruppieren

Erkennungs-Operatoren = Sinne (Wahrnehmung)
Analyse-Operatoren    = Verarbeitung (Denken)
Transformations-Op.   = Handeln (Aktion)
Meta-Operatoren       = Steuerung (Zentrale Exekutive)
Operator-Patterns     = Kombinierte Loesungsmuster


VERWANDTE HELP-DATEIEN
======================
  --help strategien      Kategorisieren, Bewerten, Ausschliessen, Testen
  --help denkstrategien  Kognitive Strategien (Chunking, Mustererkennung, etc.)
  --help rhetorik        Rhetorische Operatoren und Patterns


## Partner

BACH PARTNER-SYSTEM (Federated Intelligence)
=============================================

STAND: 2026-02-08

Das Partner-System verwaltet die Zusammenarbeit zwischen verschiedenen KIs
und dem Menschen auf Basis von Token-Effizienz und Capabilities.

REGISTRIERTE PARTNER (bach.db)
------------------------------
**AI-Partner:**
- Claude, Gemini, Ollama (aktiv)
- ChatGPT, Copilot, Mistral, Perplexity (aktiv)
- Anthropic-Local, Custom-Agent (inaktiv)

**Human-Partner:**
- Human (User/Admin)

KERN-KOMPONENTEN
----------------
1. LOGIK (partner_recognition): Wer kann was? (Caps, Zone, Cost-Tier)
2. PHYSIK (connections): Wo sind die Endpoints? (API-Keys, URLs)
3. PRÄSENZ (partner_presence): Wer ist gerade "eingestempelt"?
4. PROTOKOLL (llm / msg): Wie arbeiten wir zusammen? (Locks, Messages)
5. CONNECTORS (hub/connector.py): Externe Kommunikation (Telegram, Discord)

CLI-BEFEHLE (--partner)
-----------------------
  bach partner list              Alle registrierten Partner auflisten
  bach partner status            Zustand des Netzwerks (Online-Status, Token-Zonen)
  bach partner info <name>       Details zu spezifischem Partner anzeigen
  bach partner active            Liste der aktuell aktiven Partner
  bach partner delegate <task>   Aufgabe an effizientesten Partner übertragen

CONNECTOR-BEFEHLE (--connector)
-------------------------------
  bach connector list            Alle Connectors (Telegram, Discord, etc.)
  bach connector status          Status aller aktiven Connectors
  bach connector send <name> <recipient> <text>  Nachricht über Connector senden
  bach connector poll <name>     Nachrichten von Connector abrufen
  bach connector messages [name] Empfangene Nachrichten anzeigen

DELEGATE-FLAGS
--------------
Der delegate-Befehl unterstützt folgende Optionen:
  --partner delegate <task>              Aufgabe automatisch routen
  --partner delegate <task> --to=NAME    An spezifischen Partner delegieren
  --partner delegate <task> --zone=N     Zone erzwingen (1-4)
  --partner delegate <task> --fallback-local
  --partner delegate <task> --fal        Offline-Fallback auf Ollama (Kurzform)

MULTI-LLM KOORDINATION (Neu v1.1.73+)
-------------------------------------
Um Konflikte in der Parallel-Arbeit zu vermeiden, gelten folgende Regeln:
- LOCKING: `bach llm lock <file>` verhindert, dass zwei KIs dieselbe Datei ändern.
- MESSAGING: `bach msg send <target> "text"` zur direkten Abstimmung.

ZONEN-SYSTEM (Token-Awareness)
------------------------------
Das Routing erfolgt automatisch basierend auf dem Token-Budget (Schicht 5):
- Zone 1 (<30% Budget): Claude (Best Quality)
- Zone 2 (30-60%): Gemini / Claude (Mixed)
- Zone 3 (60-80%): Ollama (Lokal/Kostenlos)
- Zone 4 (80-100%): Human (Notfall/Abschluss)

DATENBANK-OBJEKTE
-----------------
- partner_recognition:   Stammdaten (10 Partner: Claude, Gemini, Ollama, etc.)
- partner_presence:      Aktuelle Sessions & Stempelkarte (40+ Logs)
- connections:           Technische Profile (8+ Verbindungen)
- interactionworkflows: Protokoll der Zusammenarbeit (10+ Einträge)
- connector_messages:    Nachrichten von/zu externen Systemen (Telegram, Discord)

WF-BEISPIEL (GEMINI)
--------------------
  1. Check: `bach msg ping --from gemini`
  2. Work: `bach llm lock research.md` -> Edit -> `unlock`.
  3. Done: `bach task done ID`

MCP SERVER INTEGRATION (v2.2)
------------------------------
Der BACH MCP Server stellt Partner-Funktionen für Claude Code bereit:

**Tools:**
- partner_list    - Alle Partner auflisten
- partner_status  - Status und Token-Zonen anzeigen

**Verwendung in Claude Code:**
```python
# MCP Tool wird automatisch verfügbar wenn Server läuft
result = mcp.call_tool("partner_list")
```

PARTNER-WORKSPACE
-----------------
AKTUELL (ab 2026-02-01): system/partners/
- claude/inbox, claude/outbox
- gemini/inbox, gemini/outbox
- ollama/inbox, ollama/outbox

VERALTET (vor 2026-02-01): system/partners/
- Nur noch gemini/outbox/ mit alten Reports (2026-02-06)
- Neue Reports gehen nach partners/gemini/outbox/

SIEHE AUCH
----------
  bach connector --help     Connector-System (Telegram, Discord)
  bach llm --help           Multi-LLM Protokoll (Locks)
  bach msg --help           Messaging System
  bach tokens --help        Token-Monitor & Quotas
  docs/docs/docs/help/maintain.txt         Integritäts-Check des Netzwerks

VERSION: v1.2.0 (2026-02-08)
Quelle: hub/partner.py, tools/mcp_server.py, partners/


## Partners

PARTNERS - Kommunikations-Partner Profile
=========================================

STAND: 2026-02-08

Das Partner-System (Schicht 5) orchestriert die Zusammenarbeit zwischen 
menschlichen Usern, lokalen Modellen (Ollama) und externen Agenten (Claude, Gemini).

PARTNER-UEBERSICHT (Snapshot)
-----------------------------
| ID  | Partner        | Typ          | Workspace / Backend            |
|-----|----------------|--------------|--------------------------------|
| 001 | User           | Human        | User/MessageBox/               |
| 002 | Claude         | AI           | partners/claude/       |
| 003 | Ollama         | Local AI     | 127.0.0.1:11434                |
| 004 | Gemini         | Agent        | Antigravity (Local)            |
| 006 | PubMed         | MCP API      | Research-Server                |

PARTNER-FOKUS: GEMINI
---------------------
- BACKEND: Antigravity (Google DeepMind Toolchain).
- STARTER: `system/partners/gemini/start_gemini.bat`
- WORKSPACE: `system/partners/gemini/` (Inbox/Outbox Modell).
- REGELN: Siehe `system/partners/gemini/GEMINI.md`

PARTNER-FOKUS: CLAUDE
---------------------
- BACKEND: Anthropic Sonnet (via Claude Desktop/MCP).
- ROLE: Operating AI (Orchestrator).
- WORKSPACE: `system/partners/claude/`

KOORDINATION via MESSAGES
-------------------------
Partner kommunizieren über das `messages` System (bach.db).
Befehle:
  bach msg send <recipient> "text" --from <sender>
  bach msg list --inbox     (Inbox anzeigen)
  bach msg unread           (Ungelesene anzeigen)
  bach msg read <id>        (Nachricht lesen)

DIENSTE & TABELLEN (bach.db)
----------------------------
- `partner_recognition`: Partner-Profile (Tools, Capabilities, Zonen)
- `connections`: Technische Endpunkte (API Keys, URLs)
- `messages`: Persistent Chat-Historie (Inbox/Outbox)
- `delegation_rules`: Token-basierte Delegations-Zonen

KOMMUNIKATIONS-HYGIENE
----------------------
1. Jede Session beginnt mit `bach --startup`
2. Tasks prüfen: `bach task list --assigned <partner>`
3. Ergebnisse in `outbox/` ablegen (z.B. REPORT_*.md)
4. Tasks erledigen: `bach task done <id> "Notiz"`
5. Nachrichten senden: `bach msg send <to> "text" --from <sender>`

SIEHE AUCH
----------
  docs/docs/docs/help/partner.txt                     Delegations-Logik und Rollen
  docs/docs/docs/help/communicate.txt                 Interaktions-Protokoll
  docs/docs/docs/help/messages.txt                    Nachrichten-Syntax
  system/partners/_README.md   Struktur des Partner-Ordners

CLI-ZUGRIFF
-----------
  bach --partner list                  Alle Partner auflisten
  bach --partner status                Status-Übersicht
  bach --partner info <name>           Partner-Details
  bach --partner delegate <task>       Task delegieren (Token-aware)
  bach --connections list              Connection-Registry
  bach msg list                        Nachrichten anzeigen


## Planning

PLANUNGSVERFAHREN
=================

WANN PLANEN?
  < 15 Min    Direkt bearbeiten
  15-30 Min   Optional strukturieren
  > 30 Min    MUSS strukturiert werden

PLANUNG ERSTELLEN (MANUELL):

  1. Konzept-Dokument erstellen in docs/ oder docs/_ideas/
  2. Struktur (Empfohlen):
     - Hintergrund (Warum?)
     - Ziel (Was soll erreicht werden?)
     - Technische Analyse (Komponenten, Dateien, Abhaengigkeiten)
     - Umsetzungsplan mit Task-Zerlegung

  3. Tasks in BACH-Datenbank anlegen:
     bach task add "Teil 1" --category development --priority P2
     bach task add "Teil 2" --category development --priority P3

  4. Abhaengigkeiten setzen (falls erforderlich):
     bach task depends <id> --on <andere_id>

ZEITBUDGET-REGELN (Empfehlungen):
  Sehr selten:  1-2 Min   (Konstante umbenennen)
  Selten:       2-3 Min   (Import hinzufuegen)
  OFT:          3-6 Min   (Funktion implementieren)
  Manchmal:     8-11 Min  (Komplexere Logik)
  Selten:       12 Min    (Groesseres Refactoring)
  NIE:          >15 Min   (Technisch nicht moeglich)

TASK-BEFEHLE:
  bach task add <titel>              Task hinzufuegen
  bach task add <titel> --category development --priority P2
  bach task list pending             Offene Tasks anzeigen
  bach task depends <id>             Abhaengigkeiten anzeigen
  bach task depends <id> --on <id2>  Abhaengigkeit setzen
  bach task show <id>                Task-Details anzeigen
  bach task done <id>                Task als erledigt markieren

  Siehe auch: bach task help

WORKFLOW-BEISPIEL:
  1. Konzept in docs/_ideas/mein_feature.md schreiben
  2. Tasks anlegen:
     bach task add "Schema erweitern" --category development --priority P2
     bach task add "Handler implementieren" --category development --priority P2
     bach task add "Tests schreiben" --category development --priority P3
  3. Abhaengigkeiten setzen:
     bach task depends 302 --on 301  # Handler haengt von Schema ab
     bach task depends 303 --on 302  # Tests haengen von Handler ab
  4. Schrittweise abarbeiten:
     bach task done 301
     bach task list pending  # 302 ist jetzt nicht mehr blocked


## Plugins

BACH PLUGIN-API
===============

Stand: 2026-02-13

Die Plugin-API ermoeglicht dynamische Erweiterung von BACH zur Laufzeit.
Plugins koennen Tools, Hooks, Workflows und Handler registrieren --
imperativ (via Code) oder deklarativ (via plugin.json).

CLI-BEFEHLE
-----------
  bach plugins list              Alle geladenen Plugins anzeigen
  bach plugins load <pfad>       Plugin aus plugin.json laden
  bach plugins unload <name>     Plugin entladen
  bach plugins tools             Alle Plugin-Tools anzeigen
  bach plugins info <name>       Details zu einem Plugin
  bach plugins create <name>     Plugin-Manifest erstellen (Scaffolding)
  bach plugins caps              Capability-Profile anzeigen
  bach plugins trust <name> <l>  Trust-Level eines Plugins aendern
  bach plugins audit [limit]     Letzte Capability-Pruefungen anzeigen

  Kurzform:
  bach plugin list               (Alias: plugin -> plugins)

API-NUTZUNG (Imperativ)
------------------------
  from core.plugin_api import plugins
  # Oder: from bach_api import plugins

  # Tool registrieren
  def mein_tool(text):
      return f"Verarbeitet: {text}"

  plugins.register_tool("mein_tool", mein_tool, "Beschreibung")
  result = plugins.call_tool("mein_tool", "Eingabe")

  # Hook registrieren
  def on_task(ctx):
      print(f"Task erstellt: {ctx['task_id']}")

  plugins.register_hook("after_task_create", on_task, plugin="mein-plugin")

  # Handler registrieren (neuer CLI-Befehl!)
  from hub.base import BaseHandler
  class MeinHandler(BaseHandler):
      ...

  plugins.register_handler("mein_cmd", MeinHandler, plugin="mein-plugin")

  # Workflow erstellen
  plugins.register_workflow("mein-workflow", "# Workflow\n...", plugin="mein-plugin")

  # Verwaltung
  print(plugins.list_plugins())
  plugins.unload_plugin("mein-plugin")

PLUGIN-MANIFEST (Deklarativ)
-----------------------------
Erstelle ein `plugin.json` fuer automatisches Laden:

  bach plugins create mein-plugin

Manifest-Format (plugin.json):
  {
    "name": "mein-plugin",
    "version": "1.0.0",
    "description": "Was das Plugin tut",
    "author": "claude",
    "source": "goldstandard",
    "capabilities": ["db_read", "hook_listen"],
    "hooks": [
      {
        "event": "after_task_done",
        "module": "handlers.py",
        "handler": "on_task_done",
        "priority": 50
      }
    ],
    "handlers": [
      {"name": "mein_cmd", "file": "mein_handler.py"}
    ],
    "workflows": [
      {"name": "mein-workflow", "file": "workflow.md"}
    ]
  }

Laden:
  bach plugins load plugins/mein-plugin/plugin.json

REGISTRIERUNGS-TYPEN
---------------------
  Typ          API-Methode              Beschreibung
  ---------    ----------------------   ---------------------------------
  Tool         register_tool()          Callable als Werkzeug registrieren
  Hook         register_hook()          Event-Listener registrieren
  Workflow     register_workflow()      Markdown-Datei erstellen
  Handler      register_handler()       Neuer CLI-Befehl zur Laufzeit

PLUGIN-LIFECYCLE
-----------------
  1. Erstellen:  bach plugins create <name>
  2. Entwickeln: plugin.json + handlers.py bearbeiten
  3. Laden:      bach plugins load <pfad/plugin.json>
  4. Nutzen:     Hooks feuern, Tools aufrufen, CLI-Befehle nutzen
  5. Entladen:   bach plugins unload <name>

CAPABILITY-SYSTEM (Stufe 1 Sandbox)
-------------------------------------
Plugins deklarieren benoetigte Faehigkeiten. BACH prueft und
durchsetzt basierend auf dem Trust-Level der Quelle.

  Definierte Capabilities:
    db_read          Datenbank lesen
    db_write         Datenbank schreiben
    file_read        Dateien lesen
    file_write       Dateien schreiben
    hook_listen      Auf Events lauschen
    hook_emit        Events emittieren
    tool_register    Neue Tools registrieren
    handler_register Neue CLI-Handler registrieren
    workflow_create  Workflows erstellen
    network          Netzwerk-Zugriff (HTTP/API)
    shell            Shell-Befehle ausfuehren

  Trust-Profile (verknuepft mit data/skill_sources.json):
    goldstandard     trust=100  Alle Capabilities
    trusted          trust=80   Alles ausser shell + network
    untrusted        trust=20   Nur db_read, file_read, hook_listen
    blacklist        trust=0    Nichts erlaubt

  Enforcement:
    - register_tool()     prueft 'tool_register'
    - register_hook()     prueft 'hook_listen'
    - register_handler()  prueft 'handler_register'
    - register_workflow() prueft 'workflow_create'
    - load_plugin()       prueft alle angeforderten Capabilities

  Audit:
    - Jede Pruefung wird in data/logs/capability_audit.log geschrieben
    - In-Memory Log (letzte 200 Eintraege): bach plugins audit
    - Hook 'after_capability_denied' feuert bei Verweigerung

SICHERHEIT
----------
  - Capability-Enforcement in allen register_*() Methoden
  - Trust-Level aus skill_sources.json (4-Stufen-System)
  - Statische Code-Analyse: eval, exec, subprocess, os.system
  - Audit-Log fuer Nachvollziehbarkeit
  - Fehlerhafte Hooks werden gefangen, brechen nichts ab
  - Plugin-Entladen entfernt alle Registrierungen sauber
  - Audit via: bach plugins audit, bach plugins info <name>

ARCHITEKTUR
-----------
  core/capabilities.py  CapabilityManager-Singleton (Enforcement)
  core/plugin_api.py    PluginRegistry-Singleton (Plugin-Verwaltung)
  hub/plugins.py        CLI-Handler (bach plugins ...)
  core/hooks.py         Hook-Framework (17 Events)
  data/skill_sources.json  Trust-Profile und Capability-Zuordnung

SIEHE AUCH
----------
  bach help hooks              Hook-Framework (16 Events)
  bach help skills             Skill-System
  bach help self-extension     Selbsterweiterungs-System
  bach help cli                CLI-Konventionen


## Practices

BEST PRACTICES
==============

BACH CLI ERSTE WAHL:
  Fuer alle Operationen IMMER bach.py nutzen
  - Tasks           --> bach task add/list/done
  - Memory          --> bach mem write/read
  - Skills          --> bach --skills list/search
  - Tools           --> bach tools list/run

WARUM?
  - Encoding-sicher (UTF-8)
  - Validiert Struktur
  - Keine Korruption
  - Atomare Operationen
  - Einheitliche Schnittstelle

ALTERNATIVEN (NUR WENN CLI NICHT GEHT):
  1. Python-Script mit bach_paths.py
  2. Direkte DB-Abfrage (nur lesen!)
  3. Niemals manuelle JSON-Bearbeitung!

REGELWERK-INDEX:
  Was?                      Wo?
  CLI-Syntax                --help cli
  Memory-Regeln             --help memory
  Task-System               --help tasks
  Coding-Standards          --help coding
  Ordnerstruktur            --help bach_paths
  Namenskonventionen        --help naming
  Datenformate              --help formats
  Bekannte Probleme         --help lessons
  Tool-Uebersicht           --help tools
  Tool-Praefixe             --help naming (Abschnitt TOOL-PRAEFIXE)
  Policy-Validatoren        tools/_policies/

ARCHITEKTUR-PRINZIPIEN:
-----------------------
Diese Regeln gelten systemweit:

1. KONZEPTE ZENTRAL IN DOCS/ ABLEGEN
   Alle CONCEPT_*.md gehoeren nach docs/ (Root-Verzeichnis).
   EIN Ort fuer alle Plaene = bessere Uebersicht.

   Nach Umsetzung: Konzept nach docs/_archive verschieben.

   MARKDOWN-DATEIEN IM SYSTEM:
   - docs/CONCEPT_*.md  = Konzepte und Plaene (zentral!)
   - */README.md        = Ordner-Wegweiser, Index
   - skills/SKILL.md    = Agent/Skill-Dokumentation
   - skills/*.md        = Agent-Hauptdokument (ATI.md, STEUER.md)

   REGEL: Dezentrale .md sind NUR fuer Navigation und Skill-Doku,
          NICHT fuer Konzepte oder Plaene.

2. DOCS/ ORDNERSTRUKTUR
   docs/ betrifft die ENTWICKLUNG des Systems:

   _archive/          Archivierte Altkonzepte (umgesetzt/obsolet)
   _ideas/            Langfristige Konzepte (noch nicht approved)
   _test_and_reports/ Entwickler-Analysen, Jetztstände, Tests
   analyse/           Analyse-Ergebnisse und Berichte
   reference/         Referenz-Dokumentation
   (root)             CONCEPT_*.md - Alle Konzepte zentral
                      EIN Ort fuer alle Plaene zur Umsetzung

   user/ betrifft die NUTZUNG des Systems:
   - Reports die durch Nutzung entstehen
   - Nicht fuer System-Entwicklung

3. EVOLUTIONAERE MIGRATION
   Keine harten Brueche bei Umbenennungen/Umstrukturierungen.
   Alte Strukturen schrittweise migrieren, nicht auf einmal.

4. EINE UNIFIED DATENBANK
   bach.db      = Einzige Haupt-DB (123 Tabellen, alles drin)

   Hinweis: user.db wurde in v1.1.84 in bach.db zusammengefuehrt.
   registry.db (Distribution) und archive.db (Archiv) sind
   Spezial-DBs, nicht Teil des Kern-Systems.

5. DATENBANK VOR JSON (RecludOS-Lehre!)
   JSON-Dateien nur in begruendeten Ausnahmefaellen.
   Standard ist IMMER die Datenbank.

   JSON erlaubt nur wenn:
   - Nutzer-spezifisch (frisch erstellt, nicht migriert)
   - Transparenz wichtig (Nutzer soll direkt editieren)
   - Prozess-Charakter (kurzlebig, Verarbeitung)
   - Import/Export Austauschformat

   Details: docs/docs/docs/help/formats.txt

6. DIST_TYPE DREISCHRITT
   2 = CORE (Systemdatei, Distribution ist Backup)
   1 = TEMPLATE (1x Snapshot fuer Reset)
   0 = USER (Userdaten, normale Rotation)

7. HELP ALS WAHRHEIT
   docs/docs/docs/help/*.txt ist die primaere Dokumentation.
   Bei Widerspruch: docs/docs/docs/help/ gewinnt.


## Press

PRESSEMITTEILUNGEN & POSITIONSPAPIERE
=====================================

Erstellt professionelle Dokumente via LaTeX.

BEFEHLE
-------

  # Erstellen
  bach press create --type pressemitteilung --title "Titel" [--body "Text"]
  bach press create --type positionspapier --title "Titel" [--body "Text"]

  # Verwalten
  bach press list                    Alle Dokumente
  bach press show <id>               Dokument-Details
  bach press templates               Verfuegbare LaTeX-Templates

  # Versenden
  bach press send <id> --to <email>  Per Email versenden

  # Konfiguration
  bach press config                  Aktuelle Config anzeigen
  bach press config --author "Name"  Autor setzen
  bach press config --logo /pfad     Logo-Pfad setzen

TYPEN
-----
  pressemitteilung  - Fuer Medien und Oeffentlichkeit
  positionspapier   - Akademisch/politisch, mit Inhaltsverzeichnis

VORAUSSETZUNGEN
---------------
  MiKTeX mit pdflatex/xelatex muss installiert sein.
  Benoetigte Pakete: geometry, fancyhdr, graphicx, hyperref, babel

KONFIGURATION
-------------
  Datei: agents/_experts/press/config.json
  Felder: author, organization, contact_email, logo_path, latex_compiler


## Problemloesung

PROBLEMLOESUNG - Strukturiertes Denken
======================================

BESCHREIBUNG
------------
Problemloesungs- und Analyse-Strategien fuer komplexe Aufgaben.
Strukturierte Denkprozesse fuer schwierige Situationen.

PROBLEMLOESUNGS-ANSAETZE
------------------------

1. DIVIDE & CONQUER
   Problem -> Teilprobleme -> Loese einzeln -> Kombiniere
   
   Wann nutzen: Grosse, komplexe Probleme die sich zerlegen lassen.

2. ROOT CAUSE ANALYSIS (5 Whys)
   Symptom -> Warum? -> Warum? -> Warum? -> Ursache -> Loesung
   
   Wann nutzen: Wenn unklar ist, was das eigentliche Problem ist.

3. CONSTRAINT RELAXATION
   Unloesbar -> Constraints lockern -> Loesen -> Constraints anziehen
   
   Wann nutzen: Wenn Anforderungen zu restriktiv sind.

4. ANALOGIE-SUCHE
   Neues Problem -> Aehnliches bekanntes Problem -> Loesung adaptieren
   
   Wann nutzen: Bei neuartigen Problemen ohne offensichtliche Loesung.

ANALYSE-METHODEN
----------------

  Methode      Anwendung
  ----------   -----------------------------------------
  SWOT         Staerken/Schwaechen/Chancen/Risiken
  Pro/Contra   Entscheidungsfindung
  Pareto       80/20 Priorisierung (wichtigste 20% finden)
  Fishbone     Ursachenanalyse (Ishikawa-Diagramm)

ENTSCHEIDUNGS-HEURISTIKEN
-------------------------

Bei Unsicherheit:
  1. Was ist das Worst-Case-Szenario?
  2. Ist es reversibel?
  3. Was kostet Nicht-Handeln?

Bei Komplexitaet:
  1. Was ist der einfachste erste Schritt?
  2. Was wuerde ein Experte tun?
  3. Was waere die 80%-Loesung?

PRAKTISCHE TIPPS
----------------
- Beginne immer mit dem einfachsten Schritt
- Dokumentiere Denkprozesse fuer spaetere Referenz
- Bei Blockade: Pause machen, Problem neu formulieren
- 80%-Loesungen sind oft besser als 100%-Plaene

SIEHE AUCH
----------
docs/docs/docs/help/denkstrategien.txt       Kognitive und metakognitive Strategien
docs/docs/docs/help/strategien.txt           Kategorisieren, Bewerten, Testen
docs/docs/docs/help/operatoren.txt           Basis-Operatoren und Patterns


## Prompt Generator

BACH PROMPT-GENERATOR
=====================

Der Prompt-Generator ist ein GUI-Board zum Erstellen, Verwalten und
Senden von Prompts an Claude-Sessions - manuell oder automatisiert.

STATUS:   FUNKTIONAL (Service implementiert, Handler fehlt)
HANDLER:  NICHT REGISTRIERT (kein bach.py Integration)
SERVICE:  hub/_services/prompt_generator/
GUI:      gui/prompt_manager.py (PyQt6, eigenstaendig)


KONZEPT
-------

Das Board bietet systemweites Prompt-Management mit folgenden Features:

  1. Texteditor fuer Startprompt (mit Reset-Funktion)
  2. Vorlagen-Auswahl (System/Agenten/Eigene)
  3. Vier Sendeoptionen
  4. Daemon-Steuerung (Zeitplanung)


SENDEOPTIONEN (4 Modi)
----------------------

  1. ALS TASK
     - Prompt wird als Task in die Warteschlange gestellt
     - Asynchrone Abarbeitung durch naechste Claude-Session
     - Keine sofortige Ausfuehrung

  2. DIREKT SESSION
     - Startet sofort eine neue Claude-Session
     - Prompt wird via Quick-Entry (Ctrl+Alt+Space) gesendet
     - Blockierend bis Session-Ende

  3. TEXT KOPIEREN
     - Kopiert den Prompt in die Zwischenablage
     - User fuegt manuell in Claude ein
     - Fuer Anpassungen vor dem Senden

  4. DAEMON-STEUERUNG
     - Automatisierte Prompt-Ausfuehrung
     - Konfigurierbar: Intervall, Sperrzeiten, Max-Sessions
     - Single-Prompt oder Multi-Prompt Rotation


VORLAGEN-SYSTEM
---------------

  System-Vorlagen (nicht editierbar, fuer Reset):
    - minimal.txt      Basis: Lies SKILL.md, fuehre bach.py aus
    - task.txt         Task-Ausfuehrung mit JSON-Output
    - review.txt       Code-Review mit Scoring

  Agenten-Vorlagen:
    - ati.txt          Software-Entwicklung (ATI Agent)
    - steuer.txt       Buchhaltung (Steuer Agent)
    - wartung.txt      BACH System-Wartung

  Eigene Vorlagen:
    - Vom User erstellte/angepasste Prompts
    - Gespeichert in DB (prompt_templates Tabelle)


DAEMON-STEUERUNG
----------------

Erweiterte Optionen fuer automatisierte Sessions:

  Intervall:        Minuten zwischen Sessions (default: 30)
  Max Sessions:     Limit pro Durchlauf (0 = unbegrenzt)
  Sperrzeiten:      Start/Ende der Ruhezeit (default: 22:00-08:00)
  Hoechstdauer:     Max. Minuten pro Session (default: 15)

  Modi:
    Single Prompt:  Immer derselbe Prompt
    Multi Prompt:   Rotation durch verschiedene Vorlagen

  One-Line:         Nur 1 Session gleichzeitig aktiv (Default)


GUI-LAYOUT (gui/prompt_manager.py - IMPLEMENTIERT)
---------------------------------------------------

  PyQt6-basierter Dark-Theme Manager mit:
  - Tab 1: Prompt Editor + Vorlagen (System/Agents/Custom)
  - Tab 2: Daemon-Steuerung (Intervalle, Ruhezeiten, Profilen)
  - Tab 3: Template-Verwaltung
  - Tab 4: Profil-Management
  - System Tray Icon
  - Single Instance Lock

  Aufruf: python system/gui/prompt_manager.py


CLI BEFEHLE (AKTUELL)
---------------------

DIREKTER AUFRUF (Service-Script):
  cd system/hub/_services/prompt_generator
  python prompt_generator.py list
  python prompt_generator.py get <path>
  python prompt_generator.py generate <path>
  python prompt_generator.py copy <path>
  python prompt_generator.py session [agent]
  python prompt_generator.py start [agent]
  python prompt_generator.py status

GUI STARTEN:
  python system/gui/prompt_manager.py

BACH.PY INTEGRATION:
  FEHLT - Kein Handler registriert!
  "python bach.py prompt list" funktioniert NICHT
  "python bach.py --prompt list" funktioniert NICHT


ABGRENZUNG: DREI HANDLER-SYSTEME
--------------------------------

  ┌─────────────────────────────────────────────────────────────────┐
  │  PROMPT-GENERATOR                                               │
  ├─────────────────────────────────────────────────────────────────┤
  │  Prompts erstellen, verwalten, senden                           │
  │  Manuell oder automatisiert                                     │
  │  Systemweit fuer alle Agenten                                   │
  │  Handler:  FEHLT (nicht in Registry)                            │
  │  Service:  hub/_services/prompt_generator/prompt_generator.py   │
  │  GUI:      gui/prompt_manager.py (PyQt6, eigenstaendig)         │
  │  Daemon:   JA (session_daemon.py)                               │
  │  API:      FEHLT (nicht in bach_api.py)                         │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │  WARTUNG (docs/docs/docs/help/wartung.txt)                                     │
  ├─────────────────────────────────────────────────────────────────┤
  │  Shell/Python-Befehle ausfuehren (Backup, Cleanup)              │
  │  Keine Prompts, nur Befehle                                     │
  │  Handler:  hub/daemon.py (registriert)                          │
  │  Service:  gui/api/daemon_api.py + DB                           │
  │  GUI:      /daemon (Web-Dashboard)                              │
  │  Daemon:   JA (eigener Prozess)                                 │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │  RECURRING (docs/docs/docs/help/recurring.txt)                                 │
  ├─────────────────────────────────────────────────────────────────┤
  │  Erstellt Tasks als Erinnerungen                                │
  │  Kein Prompt-Sending                                            │
  │  Handler:  hub/recurring.py (registriert)                       │
  │  Service:  hub/_services/recurring/                             │
  │  GUI:      KEINE (nur CLI)                                      │
  │  Daemon:   NEIN (Check bei Aufruf)                              │
  └─────────────────────────────────────────────────────────────────┘


TECHNISCHE BASIS
----------------

  Service-Ordner: hub/_services/prompt_generator/
    ├── README.md              Dokumentation
    ├── config.json            Konfiguration (Daemon-Einstellungen)
    ├── prompt_generator.py    Hauptlogik (CLI + API)
    ├── templates/             Template-Ordner
    │   ├── system/            Read-only Vorlagen
    │   │   ├── minimal.txt
    │   │   ├── task.txt
    │   │   └── review.txt
    │   └── agents/            Editierbare Vorlagen
    │       ├── ati.txt
    │       ├── steuer.txt
    │       └── wartung.txt
    └── profiles/              Daemon-Profile
        ├── ati.json
        └── wartung.json

  GUI: gui/prompt_manager.py (PyQt6, eigenstaendig)

  FEHLENDE INTEGRATION:
    - Kein Handler in hub/ (nicht in Registry)
    - Kein bach_api Modul (fehlt in bach_api.py)
    - Aufruf via "bach.py prompt" NICHT moeglich


BEKANNTE PROBLEME
-----------------

1. KEINE BACH.PY INTEGRATION
   - Service ist funktional, aber nicht in bach.py Registry
   - "python bach.py prompt list" → Fehler
   - Workaround: Direkter Service-Aufruf (siehe CLI BEFEHLE)

2. KEINE BACH_API INTEGRATION
   - Kein "prompt" Modul in bach_api.py
   - Library-API nicht nutzbar
   - Workaround: Service direkt importieren

3. PFAD-INKONSISTENZEN
   - Help-Datei verwies auf skills/_services/ (alt)
   - Tatsaechlich in hub/_services/ (korrekt)

MIGRATION ERFORDERLICH:
  - Handler erstellen in hub/prompt.py
  - In Registry registrieren (BaseHandler-Klasse)
  - bach_api.py erweitern um prompt = _HandlerProxy("prompt")


SIEHE AUCH
----------

  help wartung      Wartungs-Jobs (Shell-Befehle)
  help recurring    Wiederkehrende Task-Erinnerungen (keine GUI)
  help ati          ATI Software-Entwickler Agent
  help daemon       Daemon-Verwaltung (Wartung vs. Session-Daemon)


## Recurring

RECURRING TASKS - Wiederkehrende Aufgaben
=========================================

Das Recurring-System erstellt automatisch Tasks wenn sie faellig sind.
Anders als Wartung (die Jobs ausfuehrt) generiert Recurring nur
Erinnerungs-Tasks fuer Claude oder den User.

HANDLER:  hub/recurring.py
SERVICE:  hub/_services/recurring/
GUI:      KEINE (nur CLI + in /daemon Seite integriert)
DAEMON:   JA (Daemon prueft alle 5 Min - gui/daemon_service.py)


BEFEHLE
-------

  bach --recurring              Alle wiederkehrenden Tasks anzeigen
  bach --recurring list         (Alias)
  bach --recurring check        Faellige Tasks erstellen
  bach --recurring trigger ID   Task manuell ausloesen
  bach --recurring done ID      Als erledigt markieren (aktualisiert last_run)
  bach --recurring enable ID    Task aktivieren
  bach --recurring disable ID   Task deaktivieren


ABGRENZUNG: DREI HANDLER-SYSTEME
--------------------------------

  ┌─────────────────────────────────────────────────────────────────┐
  │  RECURRING                                                      │
  ├─────────────────────────────────────────────────────────────────┤
  │  Erstellt TASKS als Erinnerungen                                │
  │  Intervall-basiert (Tage)                                       │
  │  Fuer Claude/User zur Bearbeitung                               │
  │  Handler:  hub/recurring.py                            │
  │  Service:  hub/_services/recurring/                             │
  │  GUI:      KEINE (nur CLI)                                      │
  │  Daemon:   JA (prueft alle 5 Min via daemon_service.py)         │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │  WARTUNG (docs/docs/docs/help/wartung.txt)                                     │
  ├─────────────────────────────────────────────────────────────────┤
  │  Fuehrt Shell/Python-Befehle AUS                                │
  │  Zeitgesteuert (cron/interval)                                  │
  │  Ohne Claude-Beteiligung                                        │
  │  Handler:  hub/daemon.py                               │
  │  Service:  gui/api/daemon_api.py + DB                           │
  │  GUI:      /daemon (VORHANDEN)                                  │
  │  Daemon:   JA (eigener Prozess)                                 │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │  PROMPT-GENERATOR (docs/docs/docs/help/prompt-generator.txt)                   │
  ├─────────────────────────────────────────────────────────────────┤
  │  Sendet Prompts an Claude-Sessions                              │
  │  Manuell oder automatisiert                                     │
  │  Vorlagen-System mit Editor                                     │
  │  Handler:  (in Entwicklung)                                     │
  │  Service:  hub/_services/prompt_generator/                      │
  │  GUI:      /prompt-generator (GEPLANT)                          │
  │  Daemon:   JA (session_daemon.py)                               │
  └─────────────────────────────────────────────────────────────────┘

WANN WAS NUTZEN?
----------------

  Recurring verwenden wenn:
  - Claude soll erinnert werden
  - Task erfordert Intelligenz/Analyse
  - Flexibler Zeitpunkt (bei naechster Session)

  Wartung verwenden wenn:
  - Ein Script automatisch laufen soll (z.B. Backup, Scan)
  - Keine Intelligenz/Entscheidung noetig
  - Zeitpunkt wichtig (z.B. nachts um 3:00)

  Prompt-Generator verwenden wenn:
  - Claude-Session automatisch starten soll
  - Prompt-Vorlagen verwendet werden
  - Zeitgesteuerte Claude-Arbeit noetig


AKTUELLE RECURRING TASKS
------------------------

  ATI-Agent Tasks:
  ----------------
  1. self_check (14d)
     BACH SELF-CHECK: SKILL.md und Lessons pruefen

  2. onboarding_scan (7d)
     Neue Tools pruefen: bach ati onboard --check

  3. code_quality (30d)
     Code-Qualitaet pruefen: c_method_analyzer auf alle Tools

  System-Tasks:
  -------------
  4. backup_check (7d)
     BACH Backup pruefen: bach backup status

  5. memory_cleanup (30d)
     Memory-Archiv pruefen: alte Eintraege archivieren

  6. integration_check (30d)
     Anschlussanalyse durchfuehren
     Workflow: skills/workflows/system-anschlussanalyse.md

  Dokumentations-Tasks:
  ---------------------
  7. roadmap_review (14d)
     ROADMAP.md Review: Erledigte Tasks markieren, Prioritaeten pruefen

  8. wiki_author (21d)
     Wiki-Autoren: Agenten-Wissensluecken identifizieren + fuellen
     Workflow: skills/workflows/wiki-author.md

  9. help_forensic (14d)
     Help-Forensik: Ist vs Soll pruefen, bei Abweichung korrigieren
     Workflow: skills/workflows/help-forensic.md

  10. doc_freshness (60d)
      Dokumentations-Frische: bach --maintain docs report


KONFIGURATION
-------------

  Datei: hub/_services/recurring/config.json

  Format pro Task:
  {
    "task_name": {
      "enabled": true,
      "interval_days": 30,
      "target": "tasks",        // oder "ati_tasks"
      "priority": "P3",         // nur fuer target=tasks
      "priority_score": 50,     // nur fuer target=ati_tasks
      "aufwand": "mittel",      // nur fuer target=ati_tasks
      "task_text": "Beschreibung...",
      "last_run": "2026-01-22T21:30:00"
    }
  }


DAEMON-INTEGRATION
------------------

Der BACH Daemon-Service (gui/daemon_service.py) prueft automatisch
alle 5 Minuten auf faellige recurring Tasks.

Zusaetzlich kann manuell geprueft werden:
- `bach --startup` zeigt faellige Tasks an
- `bach --recurring check` erstellt sie sofort als echte Tasks


NEUEN RECURRING TASK HINZUFUEGEN
--------------------------------

1. config.json bearbeiten:
   hub/_services/recurring/config.json

2. Neuen Eintrag hinzufuegen:
   "mein_task": {
     "enabled": true,
     "interval_days": 14,
     "target": "tasks",
     "priority": "P3",
     "task_text": "Meine Aufgabe beschreiben"
   }

3. Testen:
   bach --recurring list


TECHNISCHE DETAILS
------------------

  Handler:       hub/recurring.py
  Service:       hub/_services/recurring/recurring_tasks.py
  Config:        hub/_services/recurring/config.json
  Daemon-Modul:  gui/daemon_service.py (prueft alle 5 Min)

WICHTIG: Recurring Tasks werden vom BACH Daemon automatisch geprueft
(alle 5 Minuten). Manuelle Checks mit `bach --recurring check` sind
jederzeit moeglich.


SIEHE AUCH
----------

  bach --help wartung           Wartungs-Jobs (Shell-Befehle, GUI vorhanden)
  bach --help prompt-generator  Prompt-Management (GUI geplant)
  bach --help tasks             Task-System
  bach --help startup           Session-Start (zeigt faellige Tasks)


## Restore

BACH RESTORE - TEMPLATE-WIEDERHERSTELLUNG
==========================================

Stellt TEMPLATE-Dateien (dist_type=1) und CORE-Dateien (dist_type=2)
aus dem Distribution-Manifest wieder her.


VERWENDUNG
----------

  # Einzelne Datei wiederherstellen
  bach restore <datei-pfad>

  # Alle TEMPLATE-Dateien wiederherstellen
  bach restore --all

  # CORE-Dateien wiederherstellen (mit Warnung)
  bach restore --core

  # Dry-Run (nur anzeigen, nicht ausführen)
  bach restore --dry-run <datei-pfad>


DIST_TYPE SYSTEM
----------------

  0 = USER_DATA    Persönliche Dateien, NICHT wiederherstellbar
  1 = TEMPLATE     Anpassbare System-Vorlagen, WIEDERHERSTELLBAR
  2 = CORE         System-Kern, wiederherstellbar (mit Warnung)


WICHTIG
-------

- USER_DATA (dist_type=0) wird NIEMALS überschrieben
- CORE-Restore zeigt Warnung, da Änderungen verloren gehen
- Backup wird empfohlen vor CORE-Restore


BEISPIELE
---------

  # SKILL.md wiederherstellen (TEMPLATE)
  bach restore SKILL.md

  # Alle Connector-Templates wiederherstellen
  bach restore system/connectors/templates/

  # Prüfen welche Dateien wiederhergestellt würden
  bach restore --dry-run --all


SIEHE AUCH
----------

  bach --help upgrade       Upgrade auf neuere BACH-Version
  bach --help downgrade     Downgrade auf ältere Version
  bach --help seal          Integritätsprüfung


## Rhetorik

RHETORIK
========
Rhetorische Operatoren und Patterns als angewandte Denkstrategien.

Kernaussage: Rhetorik ist Kognitive Strategie + Sprachliche Verpackung.


1. RHETORISCHE OPERATOREN (Grundbausteine)
==========================================

1.1 Verstaerkungs-Operatoren
-----------------------------
Erhoehen Wirkung, Intensitaet oder Wichtigkeit.
  - Amplifikation     -> etwas groesser machen
  - Emphase           -> Betonung durch Wiederholung/Struktur
  - Steigerung (Klimax) -> A -> B -> C, jeweils staerker
  - Superlativierung  -> "der wichtigste Punkt..."

1.2 Abschwächungs-Operatoren
-----------------------------
Daempfen, relativieren, entschaerfen.
  - Litotes           -> "nicht schlecht"
  - Hedging           -> "es koennte sein, dass..."
  - Relativierung     -> "im Vergleich dazu..."

1.3 Struktur-Operatoren
------------------------
Ordnen Gedanken und lenken Aufmerksamkeit.
  - Triade            -> 3-Punkte-Struktur
  - Rahmung (Framing) -> Kontext setzen
  - Signposting       -> "erstens... zweitens..."
  - Kontrastierung    -> A vs. B

1.4 Bedeutungs-Operatoren
--------------------------
Veraendern, wie etwas verstanden wird.
  - Metapher          -> Bedeutung uebertragen
  - Analogie          -> Vergleichsstruktur
  - Definition        -> Begriff festlegen
  - Reframing         -> Bedeutung umdeuten

1.5 Überzeugungs-Operatoren
----------------------------
Zielen auf Zustimmung.
  - Logos             -> logische Argumente
  - Ethos             -> Glaubwuerdigkeit
  - Pathos            -> Emotion
  - Autoritaetsbezug  -> "Studien zeigen..."

1.6 Wahrnehmungs-Operatoren
----------------------------
Steuern, worauf das Publikum achtet.
  - Fokussierung      -> "entscheidend ist..."
  - Ablenkung         -> Thema verschieben
  - Selektive Darstellung -> nur relevante Aspekte zeigen

1.7 Interaktions-Operatoren
----------------------------
Binden das Gegenueber ein.
  - Rhetorische Frage
  - Direkte Ansprache
  - Gemeinschafts-Frame -> "wir alle kennen das..."
  - Einwandvorwegnahme  -> "Sie fragen sich vielleicht..."

1.8 Glaubwürdigkeits-Operatoren
--------------------------------
Erhoehen Vertrauen.
  - Selbstoffenbarung
  - Transparenz
  - Fehler zugeben
  - Konsistenz zeigen


2. RHETORISCHE PATTERNS (Kombinationen)
========================================

2.1 Problem-Ursache-Loesung Pattern
------------------------------------
Operatoren: Framing, Kausalitaet, Strukturierung
Form: Problem benennen -> Ursache erklaeren -> Loesung praesentieren

2.2 Einwand-Vorwegnahme Pattern
--------------------------------
Operatoren: Perspektivwechsel, Reframing, Logos
Form: "Sie koennten jetzt denken... aber tatsaechlich..."

2.3 Story-Frame Pattern
------------------------
Operatoren: Metapher, Sequenzierung, Pathos
Form: Situation -> Konflikt -> Wendepunkt -> Loesung

2.4 Sandwich-Pattern
---------------------
Operatoren: Verstaerkung, Abschwaechung
Form: Positiv -> Kritik -> Positiv

2.5 Kontrast-Pattern
---------------------
Operatoren: Kontrastierung, Fokussierung
Form: "Nicht X, sondern Y."

2.6 Triaden-Pattern
--------------------
Operatoren: Strukturierung, Verstaerkung
Form: "Schnell. Klar. Effektiv."

2.7 Autoritaets-Pattern
------------------------
Operatoren: Ethos, Logos
Form: "Studien zeigen... Experten bestaetigen..."

2.8 Minimal-Widerstand Pattern
-------------------------------
Operatoren: Abschwaechung, Hedging
Form: "Vielleicht waere es sinnvoll..."

2.9 Reframing-Pattern
----------------------
Operatoren: Bedeutungsverschiebung
Form: "Das ist nicht ein Problem -- das ist eine Chance."

2.10 Socratisches Pattern
--------------------------
Operatoren: Fragen, Perspektivwechsel
Form: "Was waere, wenn...?"

2.11 Momentum-Pattern
----------------------
Operatoren: Klimax, Sequenzierung
Form: "Zuerst... dann... schliesslich..."

2.12 Reduktion-Pattern
-----------------------
Operatoren: Chunking, Fokussierung
Form: "Eigentlich geht es nur um zwei Dinge..."

2.13 Spiegelungs-Pattern
-------------------------
Operatoren: Perspektivuebernahme
Form: "Ich hoere, dass dir wichtig ist..."

2.14 Vereinfachungs-Pattern
----------------------------
Operatoren: Normalisieren, Metapher
Form: "Stell dir vor, es waere wie..."

2.15 Ueberraschungs-Pattern
----------------------------
Operatoren: Kontrast, Reframing
Form: "Die meisten denken X -- aber das Gegenteil ist wahr."

2.16 Konsistenz-Pattern
------------------------
Operatoren: Ethos, Wiederholung
Form: "Wie ich bereits sagte..."

2.17 Praezisions-Pattern
-------------------------
Operatoren: Definition, Fokussierung
Form: "Mit 'Effizienz' meine ich konkret..."

2.18 Emotional-Trigger Pattern
-------------------------------
Operatoren: Pathos, Storytelling
Form: "Stell dir vor, du stehst morgens auf und..."

2.19 Gegenbeweis-Pattern
-------------------------
Operatoren: Testen, Vergleichen
Form: "Wenn das stimmen wuerde, dann..."

2.20 Minimal-Argument Pattern
------------------------------
Operatoren: Priorisieren, Reduktion
Form: "Es gibt nur EINEN Grund, warum das wichtig ist..."


3. RHETORISCHE TRICKS (praezise Techniken)
===========================================

Cold Open       -> direkt mit starker Aussage starten
Hook            -> Aufmerksamkeit in 3 Sekunden
Call-Back       -> spaeter auf frueheren Punkt zurueckkommen
Echoing         -> Schluesselwoerter wiederholen
Contrast-Hook   -> "Die schlechte Nachricht... die gute Nachricht..."
False Start     -> bewusst unterbrechen, um Spannung zu erzeugen
Micro-Pause     -> Wirkung erhoehen
Labeling        -> Emotionen benennen ("Das wirkt frustrierend...")
Priming         -> Erwartung setzen
Anchoring       -> Vergleichspunkt setzen


4. RHETORIK UND METAKOGNITION
==============================
Metakognitive Strategien als rhetorische Selbststeuerung:

  Selbstueberwachung -> Koerpersprache, Ton, Tempo kontrollieren
  Fehleranalyse      -> Redeanalyse, Feedbackschleifen
  Meta-Fragen        -> "Was ist meine Kernbotschaft"
  Strategiewahl      -> Ethos/Pathos/Logos-Balance
  Reflexion          -> Nachbereitung einer Rede
  Meta-Planung       -> Redeaufbau, Dramaturgie

Rhetorik = nicht nur reden, sondern ueber das Reden nachdenken.


5. BEZUG ZU TECHNISCHEN PATTERNS
=================================
Viele Operator-Patterns haben rhetorische Zwillinge:

  Classification Pipeline  -> Zielgruppenanalyse
  Scoring & Ranking        -> Argumentgewichtung
  Rule-Based Filtering     -> Relevanzfilter fuer Inhalte
  Anomaly Detection        -> Widersprueche erkennen
  Progressive Refinement   -> Argument schrittweise aufbauen
  Human-in-the-Loop        -> Publikumsreaktionen einbeziehen
  Fallback Resolution      -> Umgang mit Einwaenden

Das ist kein Zufall: Rhetorik ist ein Informationsverarbeitungsprozess.


6. DIE DREI SAEULEN DER RHETORIK
=================================

Logos (logische Argumentation)
  -> Deduktion, Induktion, Vergleiche, Tests, Gegenbeweise
  -> Denkstrategien: Hypothesenbildung, Kausales Denken

Ethos (Glaubwuerdigkeit)
  -> Selbstueberwachung, Fehleranalyse, Konsistenz
  -> Metakognition: Reflexion, Meta-Fragen

Pathos (Emotionale Wirkung)
  -> Mustererkennung, Storytelling, Analogien
  -> Denkstrategien: Perspektivwechsel, Szenariodenken


7. ANWENDUNG IN BACH
====================

Rhetorische Operatoren koennen KI-Systeme verbessern:
  - Bessere Erklaerbarkeit (Vereinfachungs-Pattern)
  - Bessere Fehlermeldungen (Problem-Ursache-Loesung)
  - Bessere User-Guidance (Signposting, Strukturierung)
  - Bessere Kommunikation (Partner-System)

Denkstrategien  = interne Operatoren (Verarbeitung)
Rhetorik        = externe Operatoren (Kommunikation)


VERWANDTE HELP-DATEIEN
======================
  --help operatoren      Basis-Operatoren und Patterns
  --help denkstrategien  Kognitive und metakognitive Strategien
  --help strategien      Kategorisieren, Bewerten, Testen, etc.


## Routine

ROUTINE - Haushaltsroutinen-Verwaltung
======================================

STAND: 2026-02-08

Das Routine-System (Schicht 3) verwaltet wiederkehrende Aufgaben im Haushalt
und privaten Bereich mit automatischer Intervall-Berechnung.

KERNKONZEPTE
------------
- FREQUENZ: Von täglich bis jährlich (automatische Neu-Terminierung).
- STATUS: Überfällige Aufgaben werden mit `!!!` markiert.
- ZENTRALISIERUNG: Alle Routinen liegen in `bach.db`.

CLI-BEFEHLE (bach routine)
--------------------------
  list [--all] [-c <Kategorie>]
                Übersicht aller aktiven Routinen.
                --all zeigt auch inaktive, -c filtert nach Kategorie.
                Beispiel: bach routine list -c Kueche

  show <ID>     Zeigt Details einer einzelnen Routine an.
                Beispiel: bach routine show 3

  due [Tage]    Zeigt fällige Aufgaben für den gewählten Zeitraum.
                Standard: 7 Tage. Beispiel: bach routine due 14

  done <ID> [ID2...] [--note "Text"]
                Markiert Routine(n) als erledigt und setzt neues Datum.
                Mehrere IDs möglich, optional mit Notiz.
                Beispiel: bach routine done 3 5 --note "Grundreinigung"

  add "Name" [--freq/-f <Freq>] [--cat/-c <Kat>] [--dur/-d <Min>] [--note <Text>] [--schedule <Zeit>]
                Erstellt neue Routine mit optionalen Parametern:
                --freq/-f   Frequenz (taeglich, woechentlich, monatlich, jaehrlich, etc.)
                --cat/-c    Kategorie (Kueche, Bad, Wohnzimmer, etc.)
                --dur/-d    Dauer in Minuten
                --note      Notiz
                --schedule  Zeitplan-Details
                Beispiel: bach routine add "Staubsaugen" --freq woechentlich --cat Wohnzimmer --dur 30

  help          Zeigt diese Hilfe an.

FREQUENZEN (vollständige Liste)
-------------------------------
Unterstützte Frequenz-Werte für --freq:
  taeglich, täglich, daily
  woechentlich, wöchentlich, weekly
  2-woechentlich, 2-wöchentlich, biweekly
  monatlich, monthly
  quartal, quarterly
  halbjaehrlich, halbjährlich
  jaehrlich, jährlich, yearly

ABM-SYNTAX
----------
Marker:
  !!!  = Überfällig
  +    = Aktiv
  -    = Inaktiv

DATENBANK (Schicht 1)
---------------------
- Tabelle: `household_routines` (in `bach.db`).
- Felder: id, name, frequency, schedule, category, duration_minutes,
          last_done, next_due, is_active, notes, created_at.
- Statistik: Variable Anzahl (abhängig von DB-Inhalt).

GUI & INTEGRATION
-----------------
Das **Haushalts-Dashboard** in der GUI zeigt den Status der Routinen visuell.
Routinen sind zudem im globalen `calendar` Handler integriert.

SIEHE AUCH
----------
  bach calendar         Kombinierte Termin- und Routine-Ansicht
  bach --help gesundheit  Zusätzliche Haushalts-Tools (Inventar)
  docs/docs/docs/help/maintain.txt     DB-Verschiebungs-Historie (User->Bach)


## Seal

BACH SEAL - INTEGRITÄTSPRÜFUNG
===============================

Prüft die Integrität des BACH-Kernels (alle CORE-Dateien).
Warnt bei Änderungen, sperrt aber NICHT (ENT-13, ENT-14).


VERWENDUNG
----------

  # Kernel-Status anzeigen
  bach seal status

  # Vollständige Integritätsprüfung
  bach seal check

  # Kernel-Hash neu berechnen
  bach seal repair


KERNEL-SCOPE
------------

Alle Dateien mit dist_type=2 (CORE) = ~510 Dateien:
  - tools/ (322 Dateien)
  - hub/ (95 Dateien)
  - skills/ (89 Dateien)
  - Root (4 Dateien: bach.py, setup.py, etc.)


SIEGEL-PHILOSOPHIE
------------------

WARNUNG, KEINE SPERRE (ENT-13):
  - User hat VOLLE KONTROLLE über sein BACH
  - Siegel warnt nur, verhindert aber nichts
  - Kein DRM, kein Lockdown
  - User entscheidet ob Änderungen OK sind


AUTOMATISCHE PRÜFUNG
--------------------

Bei --startup:
  - Stichproben-Check (5 CORE-Dateien, Sektion 0.75)
  - Keine Vollprüfung (Performance)
  - Warnung bei Änderungen


KERNEL-HASH
-----------

SHA256 über alle CORE-Dateien:
  - Automatisch berechnet
  - Gespeichert in system_state Tabelle
  - Konsistent mit dist_type-System


BEISPIELE
---------

  # Aktuellen Siegel-Status prüfen
  bach seal status

  # Vollständige Integritätsprüfung
  bach seal check

  # Kernel-Hash neu berechnen (nach bewusster Änderung)
  bach seal repair


WICHTIG
-------

- Änderungen an CORE-Dateien werden erkannt
- User kann Änderungen akzeptieren (seal repair)
- Kein automatisches Rollback
- Backup empfohlen vor CORE-Änderungen


SIEHE AUCH
----------

  bach --help restore       Template-Wiederherstellung
  bach --help upgrade       System aktualisieren
  bach --help downgrade     Version zurücksetzen


## Self Extension

BACH SELF-EXTENSION (Selbsterweiterung)
=======================================

Stand: 2026-02-13

BACH ist ein sich selbst erweiterndes System. AI-Partner sollen
BACH aktiv verbessern, neue Faehigkeiten erstellen und das System
an neue Anforderungen anpassen.

KERNPRINZIP: BACH NUTZEN = BACH ERWEITERN
------------------------------------------
Jeder Zugriff ist eine Gelegenheit das System zu verbessern.
Fehlende Faehigkeiten werden NICHT gemeldet, sondern ERSTELLT.

SELF-EXTENSION LOOP
--------------------
  1. ERKENNEN  → Fehlende Faehigkeit identifizieren
  2. ERSTELLEN → Neuen Skill/Tool/Handler scaffolden
  3. REGISTRIEREN → Hot-Reload, Registry aktualisieren
  4. NUTZEN    → Sofort verwenden
  5. REFLEKTIEREN → Lesson Learned, Hook registrieren

NEUE FAEHIGKEITEN ERSTELLEN
-----------------------------
Mit `bach skills create` werden 5 Komponenten-Typen unterstuetzt:

  bach skills create voice-processor --type tool
    → Erstellt: system/tools/voice_processor.py
    → Scaffolding mit Standard-Template
    → Sofort nutzbar nach Implementierung

  bach skills create email-agent --type agent
    → Erstellt: system/agents/email-agent/SKILL.md
    → Eigener Ordner mit SKILL.md Template
    → Orchestriert andere Experten/Tools

  bach skills create tax-expert --type expert
    → Erstellt: system/agents/_experts/tax-expert/SKILL.md
    → Eigener Ordner mit SKILL.md Template
    → Tiefes Domaenenwissen

  bach skills create api-gateway --type handler
    → Erstellt: system/hub/api_gateway.py
    → Sofort als CLI-Befehl verfuegbar (bach api-gateway ...)
    → BaseHandler-Subklasse mit get_operations()

  bach skills create data-sync --type service
    → Erstellt: system/skills/_services/data-sync/
    → Service mit __init__.py und service.py
    → Handler-nah, allgemein nutzbar

NACH DER ERSTELLUNG: HOT-RELOAD
---------------------------------
  bach skills reload
    → Registry neu laden (neue Handler erkennen)
    → Tool-Discovery ausfuehren
    → Skills-DB synchronisieren
    → KEIN Neustart noetig!

ODER per API:
  from bach_api import app
  a = app()
  count = a.reload_registry()
  print(f"{count} Handler geladen")

HOOK-INTEGRATION
-----------------
Neue Faehigkeiten koennen sich in das Hook-System einhaengen:

  from core.hooks import hooks

  # Eigene Logik bei System-Events ausfuehren
  hooks.on('after_task_create', meine_logik, name='mein_plugin')
  hooks.on('after_startup', startup_check, name='mein_plugin')

  Verfuegbare Events: bach hooks events

BEISPIEL: KOMPLETTER SELF-EXTENSION WORKFLOW
----------------------------------------------

  Schritt 1: Bedarf erkennen
  -------------------------
  "Ich brauche einen Handler fuer Zeiterfassung"

  Schritt 2: Scaffolden
  ----------------------
  bach skills create zeiterfassung --type handler

  Schritt 3: Implementieren
  --------------------------
  → hub/zeiterfassung.py bearbeiten
  → Operations hinzufuegen (start, stop, list, report)
  → DB-Tabelle in db/schema.sql ergaenzen wenn noetig

  Schritt 4: Hot-Reload
  ----------------------
  bach skills reload

  Schritt 5: Sofort nutzen
  -------------------------
  bach zeiterfassung start "Projektarbeit"
  bach zeiterfassung stop
  bach zeiterfassung report --today

  Schritt 6: Hooks registrieren (optional)
  -----------------------------------------
  from core.hooks import hooks
  hooks.on('after_task_done', lambda ctx: zeiterfassung.stop())

  Schritt 7: Lesson speichern
  ----------------------------
  bach lesson add "Zeiterfassung: Handler-Pattern mit start/stop/list/report"

WAS KANN ERWEITERT WERDEN?
----------------------------
  Bereich          Wie                              Wo
  ---------------  ------------------------------   --------------------------
  CLI-Befehle      Neuen Handler in hub/ erstellen   hub/<name>.py
  Tools            Python-Script in tools/ legen     tools/<name>.py
  Agents           Agent-Ordner mit SKILL.md          agents/<name>/
  Experts          Expert-Ordner mit SKILL.md         agents/_experts/<name>/
  Services         Service-Ordner erstellen           skills/_services/<name>/
  Workflows        Markdown-Datei erstellen           skills/workflows/<name>.md
  Hooks            Listener registrieren              core/hooks.py: hooks.on()
  DB-Schema        Migration in db/ erstellen         db/migrations/
  Help-Dateien     Textdatei in docs/docs/docs/help/ erstellen       docs/docs/docs/help/<topic>.txt
  Aliases          Kurzform in aliases.py             core/aliases.py

REGELN FUER SELBSTERWEITERUNG
-------------------------------
  1. Handler First: Jede Funktion als Handler in hub/
  2. Self-Healing: Fehler sofort korrigieren
  3. Fix-or-Task: Klein = sofort fixen, gross = Task erstellen
  4. Lesson Learned: Nach jeder Erweiterung dokumentieren
  5. Hot-Reload: Immer `bach skills reload` nach Aenderungen
  6. Testen: Neue Handler mit `bach <name> help` validieren

SIEHE AUCH
----------
  bach help hooks            Hook-Framework
  bach help skills           Skill-System
  bach help cli              CLI-Konventionen
  bach help architecture     System-Architektur
  skills/workflows/self-extension.md  Detaillierter Workflow


## Selfcheck

SYSTEM-CHECKS
=============

HINWEIS: Der geplante --selfcheck Befehl wurde nicht implementiert.
Die Funktionalitaet ist VERTEILT auf existierende Handler.

ALTERNATIVEN FUER SYSTEM-CHECKS:

1. STARTUP-CHECKS (automatisch)
   bach startup run

   Fuehrt aus:
   - Directory Scan (neue/geaenderte Dateien)
   - Path Healer Check (Pfadprobleme)
   - Registry Watcher (DB/JSON-Konsistenz)
   - Skill Health Monitor (Skill/Agent-Validierung)
   - NUL Cleaner (Windows-NUL-Dateien)
   - Problems First (24h-Fehleranalyse)

2. WARTUNGS-TOOLS
   bach maintain list

   Verfuegbare Checks:
   - maintain heal      - Pfad-Korrektur
   - maintain registry  - Datenbank-Konsistenz
   - maintain skills    - Skill-Gesundheit
   - maintain json      - JSON-Reparatur
   - maintain nul       - NUL-Dateien entfernen

3. WORKFLOW-QUALITAET
   bach tuev run

   Prueft Workflows auf Struktur und Konsistenz

4. BACKUP-STATUS
   bach backup status

   Zeigt letzte Sicherungen und Alter

PERIODISCHE PRUEFUNG:
  Die automatischen Checks laufen bei JEDEM "bach startup run".
  Kein separates 30-Tage-Intervall notwendig.

LOGS:
  Startup-Logs: system/data/logs/
  Maintain-Logs: Ausgabe auf Console

EMPFEHLUNG:
  Bei Session-Start: bach startup run
  Bei Problemen: bach maintain [operation]


## Settings

BACH SETTINGS - SYSTEMEINSTELLUNGEN
====================================

Zentrale Verwaltung aller BACH-Einstellungen in der system_config Tabelle.
Ersetzt verstreute Config-Dateien durch eine einheitliche Schnittstelle.


VERWENDUNG
----------

  # Alle Einstellungen anzeigen
  bach settings list

  # Einstellungen einer Kategorie anzeigen
  bach settings list --category=integration

  # Einzelnen Wert lesen
  bach settings get integration.claude-code.level

  # Wert setzen
  bach settings set integration.claude-code.level=full

  # Wert mit Beschreibung setzen
  bach settings set backup.auto_backup=true --desc="Automatisches Backup aktiviert"

  # Wert auf Default zurücksetzen
  bach settings reset integration.claude-code.level

  # Settings als JSON exportieren
  bach settings export

  # Settings aus JSON importieren
  bach settings import settings_backup.json

  # Alle Kategorien auflisten
  bach settings categories


KATEGORIEN
----------

  backup         Backup-Einstellungen (auto_backup, retention_days, etc.)
  behavior       Systemverhalten (startup_mode, logging_level, etc.)
  integration    LLM-Partner-Integration (claude-code.level, memory_md_path, etc.)
  limits         System-Limits (max_file_size, max_tasks, etc.)
  migrations     Migrations-Status (last_migration, auto_migrate, etc.)
  security       Sicherheitseinstellungen (kernel_hash, seal_enabled, etc.)
  user           User-spezifische Einstellungen


INTEGRATION-SETTINGS (wichtigste Kategorie)
-------------------------------------------

Die integration.* Settings steuern die Verschmelzungstiefe zwischen
BACH und LLM-Partnern (Claude Code, Gemini, Ollama):

  integration.claude-code.level           off | sync | managed | full
  integration.claude-code.memory_md_path  Pfad zu MEMORY.md
  integration.claude-code.claude_md_path  Pfad zu CLAUDE.md
  integration.claude-code.hook_enabled    Hook-basierte Kontext-Injektion
  integration.claude-code.sync_on_shutdown BACH-Block bei Shutdown aktualisieren
  integration.claude-code.ingest_back     MEMORY.md -> DB Rückfluss

Stufe 0 (Off):     Kein BACH-Eingriff
Stufe 1 (Sync):    MEMORY.md aus DB generiert (-> SQ065)
Stufe 2 (Managed): BACH schreibt CLAUDE.md zwischen Markern
Stufe 3 (Full):    Hooks feuern context_triggers pro Prompt

Details: bach --help integration


KEY-FORMAT
----------

Einstellungen folgen dem Namespace-Schema:
  kategorie.bereich.eigenschaft

Beispiele:
  backup.auto_backup
  integration.claude-code.level
  limits.max_file_size


DIST_TYPE SYSTEM
----------------

Settings haben ein dist_type (0/1/2):
  0 = USER_DATA    User-spezifische Einstellung
  1 = TEMPLATE     Empfohlene Vorlage (wiederherstellbar)
  2 = CORE         System-kritische Einstellung

USER_DATA Settings werden NIEMALS überschrieben bei Restore/Upgrade.


DATENBANK
---------

Tabelle: system_config
  key          Eindeutiger Schlüssel (kategorie.bereich.eigenschaft)
  value        Wert (string, int, bool, json)
  type         Datentyp (string, int, bool, json)
  category     Kategorie (backup, behavior, integration, etc.)
  description  Beschreibung (optional)
  dist_type    0=USER, 1=TEMPLATE, 2=CORE
  updated_at   Letzte Änderung


HANDLER
-------

hub/settings.py    SettingsHandler Implementation (SQ037)


SIEHE AUCH
----------

docs/help/integration.txt    LLM-Partner-Integration
docs/help/restore.txt        Template-Wiederherstellung
bach --help memory           Memory-System


## Shutdown

SHUTDOWN - Session beenden
==========================

BESCHREIBUNG
Das Shutdown-Protokoll beendet eine BACH-Session, speichert den
Session-Bericht und aktualisiert den Directory-Zustand.

BEFEHLE
-------
bach --shutdown              Komplett-Shutdown (Standard)
bach --shutdown "Summary"    Mit Session-Zusammenfassung
bach --shutdown quick        Schnell ohne Dir-Scan
bach --shutdown emergency    Notfall - nur Zustand sichern

SHUTDOWN-TYPEN
--------------
KOMPLETT (Standard):
- Directory-Scan aktualisieren
- Auto-Snapshot bei >= 3 Aenderungen
- Session in DB speichern
- Task-Statistik zaehlen

QUICK:
- Keine Dir-Scan-Aktualisierung
- Speichert kurze Notiz
- Fuer Pausen wenn Session bald weitergeht

EMERGENCY:
- Nur Emergency-Notiz speichern (Prioritaet 10)
- Bei Abbruch/Timeout verwenden
- Minimal-Sicherung des Zustands

ABLAUF KOMPLETT (v1.1.17)
-------------------------
1. [DIRECTORY SCAN]
   - SOLL-Zustand aktualisieren
   - Aenderungen dokumentieren

2. [AUTO-SNAPSHOT] *** NEU v1.1.17 ***
   - Bei >= 3 Aenderungen: Automatischer Snapshot
   - Name: auto_YYYYMMDD_HHMMSS
   - Fortsetzen: bach snapshot load

3. [SESSION SPEICHERN]
   - Session in memory_sessions abschliessen
   - Summary wird gespeichert
   - Auto-Memory Fallback (v1.1.15):
     Wenn kein Summary gegeben -> aus Autolog generieren

4. [MEMORY STATUS]
   - Zeigt Working/Facts/Sessions Zaehler

5. [TASK-STATISTIK] *** v1.1.14 ***
   - Zaehlt erstelle/erledigte Tasks
   - Speichert in memory_sessions

OUTPUT-BEISPIEL
---------------
=======================================================
          COMPLETE SHUTDOWN
=======================================================
 Zeit: 2026-01-22 13:15
=======================================================

[DIRECTORY SCAN]
 SOLL-Zustand aktualisiert (5 Aenderungen)

[AUTO-SNAPSHOT]
 [OK] Auto-Snapshot erstellt (5 Aenderungen)

[SESSION SPEICHERN]
 [OK] Session session_20260122_1300 abgeschlossen

[MEMORY STATUS]
 Working: 3 | Facts: 5 | Sessions: 12

[TASK-STATISTIK]
 +2 erstellt, 1 erledigt (diese Session)

=======================================================
 Session BEENDET
=======================================================

SESSION-BERICHT SPEICHERN
-------------------------
VOR Shutdown den Session-Bericht speichern:

  bach --memory session "THEMA: Was gemacht. NAECHSTE: Was kommt."

Oder Summary direkt beim Shutdown angeben:

  bach --shutdown "Help-Dateien aktualisiert. NEXT: memory.txt pruefen"

WICHTIG: Session-Berichte gehoeren in memory_sessions (DB),
         NICHT in memory/archive/*.md Dateien!

AUTO-MEMORY FALLBACK (v1.1.15)
------------------------------
Wenn Claude keinen Summary angibt, wird automatisch einer
aus dem Autolog generiert. Format:

  [AUTO-FALLBACK] Befehle: 15 (8 unique) || task list, memory read, ...

Dies ist ein Sicherheitsnetz - manueller Summary ist besser!

WANN WELCHER SHUTDOWN
---------------------
| Situation | Befehl | Grund |
|-----------|--------|-------|
| Aufgabe fertig | --shutdown | Vollstaendige Dokumentation |
| Kurze Pause | --shutdown quick | Schnell, bald weiter |
| Timeout/Abbruch | --shutdown emergency | Mindest-Sicherung |

DATEN-QUELLEN
-------------
- memory_sessions:  Session-Berichte, Tasks-Zaehler
- memory_working:   Emergency-Notizen
- session_snapshots: Auto-Snapshots

HANDLER
-------
hub/shutdown.py    Shutdown-Handler (DB-basiert)

VERSIONSHISTORIE
----------------
v1.1.0   Basis-Shutdown mit Dir-Scan
v1.1.14  + Task-Statistik
v1.1.15  + Auto-Memory Fallback aus Autolog
v1.1.17  + Auto-Snapshot bei >= 3 Aenderungen

SIEHE AUCH
----------
bach --help startup        Session starten
bach --help memory         Memory-System (session, facts)
bach --help snapshot       Snapshots verwalten
bach --help tasks          Task-Management


## Skills

BACH SKILLS SYSTEM (Architektur v2.0)
=====================================

Stand: 2026-02-08

Skills sind spezialisierte Faehigkeiten, die LLMs erweitern.
Sie sind modular in Schicht 3 (Logic & Skill) organisiert.

VERSIONS-CHECK-PRINZIP (NEU)
----------------------------
IMMER die neueste Version verwenden - egal ob lokal oder zentral:

  bach --skills version <name>  # Pruefe Versionen
  bach --tools version <name>   # Pruefe Tool-Versionen

SKILL-STRUKTUR: EIN SKILL = EIN ORDNER (NEU)
--------------------------------------------
Jeder Skill, Agent, Expert ist vollstaendig autark in einem eigenen Ordner:

  FLAT (Standard, < 5 Dateien):
  ----------------------------
  agents/entwickler/
  +-- SKILL.md              # Definition mit Standard-Header
  +-- tool_xyz.py           # Spezifisches Tool (direkt im Root)
  +-- workflow_abc.md       # Spezifischer Workflow (direkt im Root)
  +-- config.json           # Optional

  KOMPLEX (>= 5 Dateien):
  -----------------------
  agents/_experts/steuer/
  +-- SKILL.md
  +-- tools/                # Unterordner bei vielen Tools
  +-- workflows/            # Unterordner bei vielen Workflows
  +-- data/                 # Spezifische Daten

HIERARCHIE & KATEGORIEN
-----------------------
skills/
+-- _agents/        Agenten (orchestrieren, eigener Ordner)
+-- _experts/       Experten (Domaenenwissen, eigener Ordner)
+-- _services/      Services (Handler-nah, eigener Ordner)
+-- _connectors/    Adapter (Telegram, Discord, HA, eigener Ordner)
+-- partners/      Partner-Integrationen (eigener Ordner)
+-- _os/            OS-spezifische Skills (eigener Ordner)
+-- _workflows/     Workflows (KEIN Ordner, 1 Datei = 1 Workflow)
+-- _templates/     Standard-Templates (TEMPLATE_*.md)

KOMPONENTEN-TYPEN
-----------------

  Typ         Ordner              Charakteristik
  ---------   -----------------   ---------------------------------
  Agent       _agents/<name>/     Orchestriert Experten, eigener Ordner
  Expert      _experts/<name>/    Tiefes Domaenenwissen, eigener Ordner
  Service     _services/<name>/   Allgemein, Handler-nah, eigener Ordner
  Connector   _connectors/<name>/ Adapter fuer externe Dienste
  Partner     partners/<name>/   Partner-Integrationen (konsolidiert)
  OS-Skill    _os/<name>/         OS-spezifische Funktionalitaet
  Workflow    _workflows/         KEIN Ordner (1 Datei = 1 Workflow)
  Tool (allg) system/tools/       Wiederverwendbar, kein Skill-Bezug
  Tool (spez) Im Skill-Ordner     Nur fuer diesen Skill

TOOL-DUPLIZIERUNG
-----------------
REGEL: Im Zweifel doppelt halten!

  system/tools/c_ocr_engine.py             # Allgemeine Version
  agents/_experts/steuer/steuer_ocr.py     # Skill-spezifische Version

Vorteile:
- Koennen unabhaengig weiterentwickelt werden
- Skill bleibt autark
- Keine Abhaengigkeitskonflikte

WICHTIG: tools/ liegt unter system/tools/ (NICHT unter skills/tools/)

CONNECTORS (NEU 2026-02)
------------------------
_connectors/ enthaelt Adapter fuer externe Dienste:
- telegram_connector.py - Telegram Bot API Integration
- discord_connector.py - Discord Bot Integration
- homeassistant_connector.py - Home Assistant Integration
- base.py - Basis-Connector-Klasse
- SKILL.md - Connector-Dokumentation

Connectors sind spezialisierte Services die externe Plattformen anbinden.
Sie nutzen meist asynchrone Kommunikation und Event-Queues.

STANDARD-HEADER (Pflicht)
-------------------------
Jede Komponente braucht einen YAML-Frontmatter Header:

  ---
  name: [name]
  version: X.Y.Z
  type: skill | agent | expert | service | connector | partner | os | workflow
  author: [author]
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  anthropic_compatible: true
  dependencies:
    tools: []
    services: []
    workflows: []
  description: >
    [Beschreibung]
  ---

Templates: skills/_templates/TEMPLATE_*.md

EXPORT-SYSTEM
-------------
Exportierte Skills muessen OHNE BACH funktionieren:

  bach --skills export <name>  # Erstellt autarkes Paket

Export enthaelt:
- SKILL.md mit Header
- manifest.json (Abhaengigkeiten, Versionen)
- Alle spezifischen Tools
- Alle spezifischen Workflows
- README.md (Standalone-Anleitung)
- Alle allgemeinen Ressourcen aus Bach, die benötigt werden

SKILL-QUELLEN & SICHERHEIT
--------------------------

  Klasse        Quellen                           Vorgehen
  -----------   -------------------------------   ----------------------
  Goldstandard  Selbst geschrieben                Beste Integration
  Trusted       anthropics/skills, cookbooks      Nach Pruefung 1:1 OK
  Untrusted     Andere GitHub-Repos               NUR neu schreiben
  Blacklist     data/skill_blacklist.json         VERBOTEN

Pruefung: data/skill_sources.json

DB-SYNCHRONISATION
------------------
Alle Skills werden bidirektional zwischen Dateisystem und DB abgeglichen:
- Tabelle: skills (aktuell 876 Eintraege)
- Felder: name, type, path, content_hash, is_active, version
- Erweiterte Felder: category, priority, trigger_phrases, dist_type, template_content, content
- Statistik: bach --skills list

CLI-BEFEHLE
-----------
  bach skills list               Alle Skills auflisten
  bach skills show <name>        Inhalt und Metadaten
  bach skills search <term>      Nach Funktionalitaet suchen
  bach skills version <name>     Versions-Check (lokal vs zentral)
  bach skills export <name>      Autarkes Paket erstellen (v2.0)
  bach skills install <path>     Skill aus ZIP/Verzeichnis importieren
  bach skills hierarchy          Hierarchie aus DB anzeigen
  bach skills hierarchy <typ>    Nur Typ anzeigen (agent/expert/skill/service/workflow)

SELBSTERWEITERUNG (NEU v2.5)
-----------------------------
  bach skills create <name> --type <typ>   Neue Faehigkeit scaffolden
  bach skills reload                        Hot-Reload ohne Neustart

  Unterstuetzte Typen fuer 'create':

    --type tool       Erstellt: system/tools/<name>.py
                       Python-Script mit Standard-Template
                       Sofort nutzbar nach Implementierung

    --type agent      Erstellt: system/agents/<name>/SKILL.md
                       Eigener Ordner, orchestriert andere Komponenten
                       Template mit Standard-Header

    --type expert     Erstellt: system/agents/_experts/<name>/SKILL.md
                       Eigener Ordner, tiefes Domaenenwissen
                       Template mit Standard-Header

    --type handler    Erstellt: system/hub/<name>.py
                       Sofort als CLI-Befehl verfuegbar!
                       BaseHandler-Subklasse mit get_operations()
                       Nach 'reload' ueber bach <name> erreichbar

    --type service    Erstellt: system/skills/_services/<name>/
                       Ordner mit __init__.py und service.py
                       Handler-nah, allgemein nutzbar

  Workflow:
    1. bach skills create mein-tool --type handler
    2. hub/mein_tool.py bearbeiten (Logik implementieren)
    3. bach skills reload
    4. bach mein-tool help  (sofort verfuegbar!)

  Hooks nach Create/Reload:
    after_skill_create → wird nach jedem 'create' emittiert
    after_skill_reload → wird nach jedem 'reload' emittiert

GUI (Skills Board)
------------------
Das interaktive Skills Board zeigt die gesamte Hierarchie,
den Sync-Status und ermoeglicht direktes Editieren.

  http://127.0.0.1:8000/skills

SIEHE AUCH
----------
  bach help agents             Agenten-Uebersicht
  bach help tools              Tool-Verwaltung
  bach help workflow           Workflow-System
  bach help naming             Namenskonventionen
  bach help hooks              Hook-Framework (14 Events)
  bach help self-extension     Selbsterweiterungs-System
  SKILL.md                     Zentrale Skill-Definition
  data/skill_sources.json      Skill-Quellen und Versionen


## Snapshot

BACH SNAPSHOT SYSTEM
====================

STAND: 2026-02-08

Session-Snapshots sichern den exakten "State of Mind" einer KI-Session. 
Dies ermöglicht das Laden eines Kontexts in eine neue Instanz oder 
das Fortsetzen nach einem Absturz/Shutdown.

BEFEHLE
-------
  bach --snapshot create [name]  Aktuellen Status sichern.
  bach --snapshot list           Verfügbare Snapshots (auto & manuell).
  bach --snapshot load [ID]      Stellt Working Memory & Tasks wieder her.
  bach --snapshot delete <ID>    Entfernt alte Snapshots.

KONZEPT: DER STATE-TREE
-----------------------
Ein Snapshot in BACH besteht aus folgenden Komponenten:
1. SESSION-ID: Aktueller Session-Kontext
2. OPEN TASKS: Welche Tasks aktiv/offen waren (bis zu 10)
3. RECENT MEMORY: Letzte Working Memory Einträge (letzte 5)
4. SNAPSHOT-METADATEN: Timestamp, Type (auto/manual), Name

UNTERSCHIED ZU ANDEREN SYSTEMEN
-------------------------------
- MEMORY: Wichtiges Wissen (langfristig).
- LOGS: Was getan wurde (historisch).
- SNAPSHOT: Wo wir gerade stehen (operativ).

AUTOMATIK
---------
Snapshots können automatisch oder manuell erstellt werden. Der snapshot_type
unterscheidet zwischen 'manual' (via --snapshot create) und 'auto' (potentiell
via --shutdown). Die Implementierung unterstützt beide Typen.

DATENBANK
---------
Tabelle: `session_snapshots` (system/db/schema.sql, Zeile 226-239)
Felder:
  - id, session_id, snapshot_type, name
  - snapshot_data (JSON: enthält open_tasks, recent_memory, created_at)
  - working_memory, open_tasks, active_files (separate JSON-Felder, optional)
  - token_usage, context_hash, notes
  - created_at (Timestamp)

BEISPIELE
---------
  bach --snapshot create "Vor Grossumbau"  # Manuelles Backup
  bach --snapshot list                     # Status prüfen
  bach --snapshot load 42                  # ID 42 wiederherstellen
  bach --snapshot delete 42                # Snapshot 42 löschen

SIEHE AUCH
----------
  docs/docs/docs/help/memory.txt      Gedächtnis-Konsolidierung
  docs/docs/docs/help/maintain.txt    Integritäts-Prüfung
  bach --help startup  Session-Start


## Sources

KONTEXTQUELLEN-SYSTEM (Dynamic Injections)
===========================================

STAND: 2026-02-08

Zentrale Registry für alle Wissensquellen mit dynamischen Triggern.

QUELLEN-KATEGORIEN:
-------------------
1. IMMER VERFUEGBAR (Injektion-Prio 8-10)
   - lessons_learned   Bekannte Fehler & Fixes
   - best_practices    Bewährte Vorgehensweisen
   - problems          Problem Monitor (kritisch/dringend)

2. AUF ANFRAGE / EVENT-BASIERT
   - strategies        Meta-kognitive Hilfen
   - meta_cognitive    Mentale Unterstützung
   - changelog         Historie
   - longterm_memory   Archivierte Sessions
   - contacts          Externe Tools/APIs
   - help              BACH Hilfedateien

DYNAMISCHE TRIGGER
------------------
Trigger sind teils in JSON (word_triggers), teils in DB (context_triggers):
- JSON: data/context_sources.json (9 Quellen, ~45 word_triggers)
- DB: context_triggers table (1012 Einträge - erweiterte Trigger-Logik)
- Typen: tool_discovery, lesson_hit, workflow_guide, theme_packet
- Gewichtung: weight 1-10, Auto-Inject Flag

CLI-BEFEHLE
-----------
  bach sources status             Status aller Quellen (Enabled/Weight)
  bach sources toggle <id>        Quelle an-/ausschalten
  bach sources inject <id>        Auto-Injektion an-/ausschalten
  bach sources get <id> [query]   Inhalt einer Quelle abrufen
  bach sources search <query>     Prüfen, welche Quelle bei Trigger feuert
  bach sources contacts [query]   Kontakte/APIs suchen
  bach sources problems           Fehler-Log prüfen

HINWEIS: "bach sources sync" ist NICHT implementiert im Handler.

KONFIGURATION
-------------
Die globale Steuerung der Quellen erfolgt über `data/context_sources.json`:
- enabled:           Quelle grundsätzlich verfügbar
- injection_enabled: Darf ohne explizite Anfrage injiziert werden
- weight:            Basis-Priorität (1-10)
- word_triggers:     Keywords für Trigger-Matching
- event_triggers:    Event-basierte Triggers (startup, error)

Handler-Pfad: system/hub/sources.py

QUELLEN-INHALTE
---------------
Der Handler kann direkte Inhalte liefern via "bach sources get <id>":
- lessons_learned:   Liefert docs/docs/docs/help/lessons.txt (existiert, aber ist lesson-Doku)
- best_practices:    Liest docs/docs/docs/help/practices.txt (existiert)
- strategies:        Hardcodierte Strategien (blockiert, komplex, unklar, müde)
- help:              Liest docs/docs/docs/help/*.txt Dateien (90+ Dateien vorhanden)
- changelog:         Extrahiert aus SKILL.md (system/SKILL.md)
- problems:          Scannt data/logs/*.log und blockierte Tasks in DB

HINWEIS: "lessons_learned" liefert docs/docs/docs/help/lessons.txt, nicht die Lessons-DB.
Für Lessons-DB verwenden: bach lesson list/search

HINWEIS ZU KONTAKTEN
--------------------
Seit v1.1.84 werden Kontakte in bach.db gespeichert (Tabellen: contacts,
assistant_contacts, health_contacts). Die alte contacts.json existiert nicht mehr.
Der "bach sources contacts" Befehl nutzt jetzt die DB-Tabellen direkt.

SIEHE AUCH
----------
  --help injectors      Das Injektor-System
  --help consolidation  Vom Ereignis zur Quelle
  docs/docs/docs/help/memory.txt        Kognitives Modell


## Startup

STARTUP - Session starten
=========================

BESCHREIBUNG
Das Startup-Protokoll initialisiert eine BACH-Session mit allen
notwendigen Checks und zeigt den Kontext der letzten Session.

BEFEHL
------
bach --startup                    Komplettes Startprotokoll
bach --startup quick              Schnellstart (ohne Directory-Scan)
bach --startup mode <m>           Startup-Modus aendern (gui|text|dual|silent)
bach --startup --mode=<m>         Einmalig mit anderem Modus starten
bach --startup --partner=NAME     Partner-spezifische Session (NEU v1.1.38)

PARTNER-SESSIONS (v1.1.38)
--------------------------
Ermoeglicht Partner-spezifisches Session-Management:

  bach --startup --partner=claude   Startet Claude-Session
  bach --startup --partner=gemini   Startet Gemini-Session
  bach --startup --partner=user     Standard (Default)
  bach --startup --partner=new      Generiert automatische ID (partner_HHMMSS)
  bach --startup --partner=simonAI  Neuer Partner mit eigenem Namen

VORTEILE:
- Vorherige Session desselben Partners wird automatisch geschlossen
- Parallele Sessions fuer verschiedene Partner moeglich
- Verhindert "verwaiste" offene Sessions bei wiederholtem Startup
- Automatische Stempelkarte (Clock-In/Out) in partner_presence Tabelle

STEMPELKARTEN-SYSTEM (v1.1.71):
- Bei Startup: Partner wird automatisch eingestempelt
- Bei Shutdown: Partner wird automatisch ausgestempelt
- Partner-Awareness: Zeigt wer noch online ist
- Multi-LLM Protokoll V3: Aktiviert bei mehreren Partnern

NEUE PARTNER:
  # Mit eigenem Namen (empfohlen)
  bach --startup --partner=simonAI

  # Ohne Namen (generiert ID)
  bach --startup --partner=new      -> partner_143052
  bach --startup --partner=nameless -> partner_143052

BEISPIEL:
  # Gemini startet Arbeit
  bach --startup --partner=gemini --mode=silent

  # Spaeter: Gemini startet neu -> alte Session wird geschlossen
  bach --startup --partner=gemini --mode=silent
  [AUTO-CLOSE] Vorherige GEMINI-Session beendet: session_20260126_...

  # Partner-Awareness zeigt:
  [PARTNER-AWARENESS]
   *** 1 ANDERE PARTNER ONLINE ***
     CLAUDE: Task_XYZ
   --> Protokoll V3 verwenden! (bach --help multi_llm)

DATENBANK:
  memory_sessions.partner_id speichert den Partner-Namen.
  partner_presence speichert Stempelkarte (online/offline/crashed).
  Default: "user" fuer manuelle Sessions.

NUTZERMODI (v1.1.37)
--------------------
BACH unterstuetzt 4 Startup-Modi:

  gui      GUI Dashboard oeffnet im Browser (Standard)
  text     Nur Konsole, kein Browser
  dual     GUI + Konsole parallel
  silent   Nichts automatisch starten

Der Modus wird in data/user_config.json gespeichert.
Details: bach --help modes

ABLAUF (v1.1.31)
----------------
Das Startup-Protokoll fuehrt folgende Schritte aus:

1. [DIRECTORY SCAN]
   - Prueft Aenderungen seit letzter Session
   - Zeigt neue/geloeschte/geaenderte Dateien
   - Wird bei "quick" uebersprungen

2. [PROBLEMS FIRST]
   - Automatische Fehlermeldung (von CHIAH)
   - Zeigt Fehler der letzten 24 Stunden

3. [PATH HEALER CHECK] *** NEU v1.1.18 ***
   - Dry-Run Pruefung auf Pfadprobleme
   - Zeigt Dateien mit fehlerhaften Pfaden
   - Reparieren: bach --maintain heal --execute

4. [REGISTRY WATCHER] *** NEU v1.1.21 ***
   - Prueft DB/JSON Konsistenz
   - Zeigt fehlende Tabellen, ungueltige JSON
   - Details: bach --maintain registry

5. [SKILL HEALTH] *** NEU v1.1.21 ***
   - Validiert Skills und Agenten
   - Zeigt Probleme mit SKILL.md Dateien
   - Details: bach --maintain skills

6. [LETZTE SESSION]
   - Zeigt die letzte abgeschlossene Session
   - Tasks erstellt/erledigt
   - WICHTIG: "NAECHSTE SCHRITTE" = continuation_context

7. [SNAPSHOT VERFUEGBAR] *** NEU v1.1.17 ***
   - Zeigt letzten Snapshot (wenn heute erstellt)
   - Anzahl offener Tasks im Snapshot
   - Fortsetzen: bach snapshot load

8. [MEMORY CHECK]
   - Zaehlt Working Memory, Facts, Lessons
   - Zeigt letzte Notiz

9. [SESSION REGISTRIEREN]
   - Neue Session-ID wird in memory_sessions erstellt

10. [NACHRICHTEN]
    - Prueft ungelesene Nachrichten in MessageBox
    - Zeigt Absender und Betreff
    - Details: bach msg unread

11. [PERIODISCHE TASKS] *** NEU v1.1.18 ***
    - Zeigt faellige Recurring Tasks
    - Erstellen: bach --recurring check

12. [BACH SYSTEM-TASKS]
    - Zeigt offene/erledigte BACH Framework-Tasks
    - Top 3 nach Prioritaet (P1 > P2 > P3)
    - Alle: bach task list

13. [ATI AGENT]
    - Prueft ob ATI-Ordner existiert
    - Software-Entwickler-Agent Status

14. [LESSONS LEARNED]
    - Zeigt gespeicherte Lessons
    - Details: bach lesson last

15. [AUTOLOG]
    - Eintraege aus system/data/logs/auto_log.txt
    - Letzte 3 Befehle
    - Mehr: bach --logs tail 20

16. [INJEKTOREN]
    - Zeigt aktive Injektoren

17. [STARTUP MODUS] *** NEU v1.1.37 ***
    - Zeigt aktuellen Modus (GUI/TEXT/DUAL/SILENT)
    - Startet GUI und/oder Konsole je nach Modus
    - GUI: http://127.0.0.1:8000 im Browser
    - Text: Neues Konsolenfenster mit bach.py

OUTPUT-BEISPIEL
---------------
=======================================================
         BACH SESSION STARTUP
=======================================================
 Zeit: 2026-01-22 13:10:15 (Thursday)
 Modus: GUI
 Partner: GEMINI
=======================================================

[AUTO-CLOSE] Vorherige GEMINI-Session beendet: session_20260122_...

[PATH HEALER]
 [!] 2 Dateien mit Pfadproblemen gefunden
   - example_file.py
 --> bach --maintain heal --execute zum Reparieren

[LETZTE SESSION]
 Session: session_20260122_1200
 Beendet: 2026-01-22 12:30
 Tasks: +3 erstellt, 2 erledigt
 Thema: Help-Dateien aktualisiert...

 *** NAECHSTE SCHRITTE ***
   P2: shutdown.txt aktualisieren
   P2: memory.txt pruefen

[SNAPSHOT VERFUEGBAR]
 Letzter: auto_shutdown_20260122_1230 (12:30)
 Tasks im Snapshot: 5
 --> bach snapshot load zum Fortsetzen

[PERIODISCHE TASKS]
 *** 1 TASK(S) FAELLIG ***
   [weekly_backup] Woechentliches Backup -> BACH
 --> bach --recurring check zum Erstellen

[BACH SYSTEM-TASKS]
 42 offen, 15 erledigt
 Top-Aufgaben:
   [93] P1 GUI: /api/skills Endpunkt...
   [94] P1 GUI: Skills-Dashboard...

=======================================================
 READY - Session gestartet

 HINWEIS: Bei Shutdown -> bach --memory session "..."
=======================================================

DATEN-QUELLEN
-------------
- memory_sessions:    Letzte Session, continuation_context
- memory_working:     Aktuelle Notizen
- memory_facts:       Persistente Fakten
- memory_lessons:     Lessons Learned
- session_snapshots:  Wiederherstellungspunkte
- tasks:              BACH System-Tasks
- messages:           MessageBox (bach.db)

HANDLER
-------
hub/startup.py    Startup-Handler (DB-basiert)

VERSIONSHISTORIE
----------------
v1.1.2   Basis-Startup mit Dir-Scan, Memory, Tasks
v1.1.17  + Snapshot-Anzeige
v1.1.18  + Path Healer, Recurring Tasks
v1.1.21  + Registry Watcher, Skill Health Monitor
v1.1.37  + Nutzermodi (gui, text, dual, silent)
v1.1.38  + Partner-Sessions (--partner=NAME, Auto-Close)

SIEHE AUCH
----------
bach --help modes          Nutzermodi (gui, text, dual, silent)
bach --help shutdown       Session beenden
bach --help memory         Memory-System
bach --help maintain       Wartungs-Tools (heal, registry, skills)
bach --help snapshot       Snapshots verwalten
bach --help tasks          Task-Management


## Steuer

STEUER-HILFE
============

Steuer-Agent fuer Werbungskosten-Erfassung.

UEBERSICHT
----------
Der Steuer-Agent hilft bei der systematischen Erfassung von
Werbungskosten fuer die Steuererklaerung. Er unterstuetzt
mehrere Nutzerprofile und Steuerjahre.

ORDNERSTRUKTUR
--------------
user/steuer/
+-- profile/              Nutzerprofile
+-- watch/                Ueberwachte Ordner (Konfiguration)
+-- templates/            Vorlagen fuer neue Jahre
+-- [JAHR]/               Pro Steuerjahr
    +-- Werbungskosten/   Werbungskosten (Hauptkategorie)
    |   +-- belege/           Beleg-Ablage
    |   |   +-- _bundles/         Text-Bundles fuer Batch-Verarbeitung
    |   |   +-- _Fahrten&Homeoffice/ Fahrtenbuch, AZN, timeGoat
    |   |   +-- _Fehlbelege/      Zur User-Pruefung (Nicht-Belege)
    |   |   +-- _Papierkorb/      Bestaetigte Nicht-Belege
    |   |   +-- Weitere/          Eingangsordner fuer neue Belege
    |   |   +-- [Anbieter]/       Pro Anbieter (amazon.de, eBay, ...)
    |   +-- export/           Erzeugte Berichte und Exporte
    |   |   +-- csv/              CSV-Exporte
    |   |   +-- POSTEN_*.txt      Posten-Listen
    |   |   +-- WERBUNGSKOSTEN_alle.txt
    |   |   +-- BELEGE_alle.txt
    |   |   +-- FAHRTKOSTEN_HOMEOFFICE_YYYY.*
    |   |   +-- FINANZAMT_YYYY.zip
    |   +-- STEUER_README.txt
    |   +-- FINANZAMT.bat
    |   +-- SYNC.bat
    +-- Außergewöhnliche Belastungen/
    +-- Haushaltsnahe Dienstleistungen & Handwerker/
    +-- Sonderausgaben/
    +-- Versicherungen und Altersvorsorge/

CLI-BEFEHLE
-----------

STATUS & UEBERSICHT:
  bach steuer status              Gesamtstatus anzeigen
  bach steuer status --jahr 2025  Status fuer ein Jahr

STEUERJAHR:
  bach steuer init 2026           Neues Steuerjahr anlegen
  bach steuer init 2026 --user X  Mit bestimmtem Profil

LISTEN:
  bach steuer list                Alle Listen zeigen
  bach steuer list --jahr 2025    Listen fuer Jahr
  bach steuer list --liste WERBUNGSKOSTEN
                                  Bestimmte Liste anzeigen

BELEG-VERWALTUNG (NEU)
----------------------
Belege sind die PDF-Dateien in belege/. Status: ERFASST, 
NICHT_ERFASST, DEPRECATED.

  bach steuer beleg list                    Alle Belege auflisten
  bach steuer beleg list --status ERFASST   Nach Status filtern
  bach steuer beleg list --status NICHT_ERFASST
  bach steuer beleg list --status DEPRECATED
  bach steuer beleg list --status ALL --limit 1000
                                            Alle mit hohem Limit

  bach steuer beleg scan                    Neue Belege finden
  bach steuer beleg scan --dry-run          Nur anzeigen

  bach steuer beleg deprecate 215 466 "Grund"
                                            Belege als ungueltig markieren
                                            (Nummern bleiben reserviert)

  bach steuer beleg sync                    TXT-Dateien aus DB regenerieren

POSTEN-VERWALTUNG (NEU)
-----------------------
Posten sind einzelne Positionen aus Belegen. Ein Beleg kann
mehrere Posten enthalten. PostenID = BelegNr-PostenNr (z.B. 151-1).

  bach steuer posten list                   Alle Posten anzeigen
  bach steuer posten list --liste W         Nach Liste filtern (W/G/V/Z)
  bach steuer posten list --belegnr 151     Nach Belegnummer filtern
  bach steuer posten list --steller NAME    Nach Rechnungssteller filtern
  bach steuer posten list --rechnungsnr NR  Nach Rechnungsnummer filtern
  bach steuer posten list --limit 100       Mit Limit

  bach steuer posten search BEGRIFF         Posten uebergreifend suchen
                                            (sucht in Bezeichnung, Steller,
                                            Bemerkung, Rechnungsnr, PostenID)

  bach steuer posten show 151-1             Einzelnen Posten anzeigen

  bach steuer posten add --belegnr 151 --bezeichnung "Produkt" --brutto 34.95 --liste W
                                            Neuen Posten erstellen
    Parameter:
    --belegnr NR       Belegnummer (erforderlich)
    --bezeichnung TXT  Produktbezeichnung (erforderlich)
    --brutto WERT      Bruttobetrag (erforderlich)
    --liste W|G|V|Z    Zielliste (default: Z)
    --anteil 0.0-1.0   Anteil bei Gemischt (default: 0.5)
    --bemerkung TXT    Optionale Bemerkung
    --datum YYYY-MM-DD Datum
    --anbieter NAME    Anbieter
    --rechnungsnr NR   Rechnungsnummer (oder --rechnr)

  bach steuer posten edit 151-1 --bezeichnung "Neuer Name"
                                            Posten bearbeiten
  bach steuer posten edit 151-1 --brutto 29.95
  bach steuer posten edit 151-1 --anteil 0.7
  bach steuer posten edit 151-1 --rechnungsnr "RE-12345"

  bach steuer posten move 151-1 W           In Liste verschieben
  bach steuer posten move 151-1 G --anteil 0.5
                                            Mit Anteil fuer Gemischte
    Listen-Kuerzel:
    W = WERBUNGSKOSTEN (100% absetzbar)
    G = GEMISCHTE (anteilig absetzbar)
    V = VERWORFEN (nicht absetzbar)
    Z = ZURUECKGESTELLT (noch zu klaeren)

  bach steuer posten delete 151-1           Loeschen (mit Bestaetigung)
  bach steuer posten delete 151-1 --force   Ohne Bestaetigung

BATCH-IMPORT (NEU v1.1.4)
-------------------------
Fuer schnelle Erfassung mehrerer Posten oder Belege.

  bach steuer batch help                    Batch-Hilfe anzeigen

  bach steuer batch posten --belegnr 42 --json '[...]'
                                            Mehrere Posten fuer einen Beleg
    JSON-Format:
    [{"bez":"Artikel","brutto":19.99,"liste":"W"},
     {"bez":"Privat","brutto":5.00,"liste":"V","bem":"privat"}]

  bach steuer batch posten --belegnr 42 --file posten.json
                                            Posten aus JSON-Datei

  bach steuer batch belege --inline "42:Artikel:19.99:W;43:Ware:5.00:V"
                                            Schnell-Erfassung mehrerer Belege
                                            Format: BELEGNR:BEZ:BRUTTO:LISTE

  bach steuer batch belege --file import.json
                                            Mehrere Belege mit Posten
    JSON-Format:
    {"belege":[
      {"belegnr":42,"posten":[{"bez":"X","brutto":10,"liste":"W"}]},
      {"belegnr":43,"posten":[{"bez":"Y","brutto":5,"liste":"V"}]}
    ]}

  bach steuer batch delete --belegnr 42 --force
                                            Alle Posten eines Belegs loeschen

  bach steuer batch delete --posten "42-1,42-2,43-1" --force
                                            Bestimmte Posten loeschen

  bach steuer batch delete --liste V --limit 100 --force
                                            Alle VERWORFEN loeschen (max 100)
                                            VORSICHT: Kann viele Posten loeschen!

  bach steuer batch move --posten "42-1,42-2" --liste W
                                            Bestimmte Posten verschieben

  bach steuer batch move --belegnr 42 --liste W
                                            Alle Posten eines Belegs verschieben

  bach steuer batch move --von V --nach W --limit 50
                                            Zwischen Listen verschieben

STEUER-TOOLS (NEU v1.1.4)
-------------------------
Eigenstaendige Python-Scripts in tools/steuer/.

  bach steuer tools list                    Alle Tools auflisten
  bach steuer tools <name> [args]           Tool ausfuehren (Kurzform)
  bach steuer tools run <name> [args]       Tool ausfuehren (explizit)
  bach steuer tools register                Tools in bach.db registrieren

Wichtige Tools:
  beleg_vorfilter   Neue Belege vorsortieren (NEU)
  make_bundle       Text-Bundles aus Belegen erstellen
  beleg_parser      Text aus PDFs extrahieren (mit OCR)
  regenerate_txt    Listen-TXTs aus DB regenerieren
  scan_new_belege   Neue Belege finden und registrieren
  temu_ocr_batch    Batch-OCR fuer Bild-PDFs

Direktaufruf:
  bach steuer tools make_bundle amazon 11 67
  bach steuer tools regenerate_txt

PROFILE:
  bach steuer profile list        Profile auflisten
  bach steuer profile show lukas  Profil anzeigen
  bach steuer profile create max  Neues Profil erstellen

WATCH-ORDNER:
  bach steuer watch list          Watch-Ordner anzeigen
  bach steuer watch add PFAD      Ordner hinzufuegen
  bach steuer watch remove PFAD   Ordner entfernen
  bach steuer scan                Watch-Ordner pruefen

EXPORT:
  bach steuer export              Export (Standard: txt)
  bach steuer export --jahr 2025 --format csv
  bach steuer export --format datev         DATEV Buchungsstapel CSV
                                            (fuer Steuerberater)
  bach steuer export --format csv           Einfaches CSV (Excel-kompatibel)
  bach steuer export --format vorsorge      Anlage Vorsorgeaufwand
                                            (Versicherungsbeitraege)

VOLLSTAENDIGKEITSPRUEFUNG:
  bach steuer check                         Pruefung durchfuehren
  bach steuer check --jahr 2025             Fuer bestimmtes Jahr
                                            Prueft: Belege ohne Posten,
                                            Posten ohne Beleg, Luecken in
                                            Belegnummern, fehlende Monate,
                                            Posten ohne MwSt-Betrag

EIGENBELEG-ERSTELLUNG:
  bach steuer eigenbeleg --bezeichnung "Parkgebuehr" --brutto 5.00
                                            Eigenbeleg erstellen
  bach steuer eigenbeleg --bezeichnung "..." --brutto 10.00 --mwst 7
                                            Mit abweichendem MwSt-Satz
  Optionen: --liste, --datum, --mwst, --grund

BANK-IMPORT:
  bach steuer import camt <pfad>            CAMT.053 XML importieren

FINANZAMT-EXPORT (geplant):
  bach steuer finanzamt           ZIP mit allen Werbungskosten erstellen
                                  Erzeugt FINANZAMT_[JAHR].zip mit:
                                  - WERBUNGSKOSTEN_alle.txt (Uebersicht)
                                  - csv/ Ordner mit CSV-Dateien
                                  - Alle referenzierten Belege (PDFs)

  Direkt via Script:
    python tools/steuer/steuer_sync.py finanzamt

CSV-EXPORT (NEU v1.3.1):
  bach steuer export --format csv CSV-Dateien in csv/ Ordner exportieren
                                  Fuer Excel/Steuersoftware-Import

  Format: Semikolon-getrennt, UTF-8 mit BOM, deutsches Zahlenformat

  CSV-Dateien werden NICHT automatisch bei sync geschrieben,
  nur bei: finanzamt (automatisch) oder export --format csv (explizit)

  Direkt via Script:
    python tools/steuer/steuer_sync.py csv

PROFILE
-------
Profile speichern nutzerspezifische Einstellungen:
- Beruflicher Kontext (Branche, Taetigkeit)
- Anbieter-Regeln (TEMU, Amazon, ...)
- Automatische Zuordnungen (Keywords)
- Standard-Anteile fuer gemischte Nutzung

Profil anlegen:
1. bach steuer profile create MEINNAME
2. Datei bearbeiten in user/steuer/profile/

LISTEN-TYPEN (ab V1.3.0)
------------------------
Neue Dateinamen in WERBUNGSKOSTEN/ Ordner:

  Code  Datei                    Beschreibung
  ----  -----------------------  ---------------------------
  W     POSTEN_reine.txt         100% absetzbar
  G     POSTEN_gemischt.txt      Anteilig absetzbar (mit Anteil)
  V     POSTEN_verworfen.txt     Nicht absetzbar (privat)
  Z     POSTEN_unsortiert.txt    Spaeter bearbeiten / unklar
  -     WERBUNGSKOSTEN_alle.txt  W + G kombiniert (fuer Finanzamt)

BELEG-STATUS
------------
ERFASST             Beleg wurde bearbeitet, Posten erstellt
NICHT_ERFASST       Beleg noch nicht bearbeitet
DEPRECATED          Beleg als ungueltig markiert (z.B. Duplikat)

BELEG-VORFILTER (NEU)
---------------------
Automatische Vorsortierung neuer Belege in Anbieter-Ordner.

  python tools/steuer/beleg_vorfilter.py [--dry-run] [--verbose]

Workflow:
1. Neue PDFs aus Email/Downloads in belege/Weitere/ legen
2. Vorfilter ausfuehren:
   python tools/steuer/beleg_vorfilter.py --dry-run   # Vorschau
   python tools/steuer/beleg_vorfilter.py             # Ausfuehren
3. Ergebnis:
   - Belege werden automatisch in Anbieter-Ordner sortiert
   - Nicht-Belege (Tracking, Versandstatus) -> _Fehlbelege/
4. User prueft _Fehlbelege/ -> echte Fehlbelege nach _Papierkorb/

Erkennungsmethoden:
- Dateiname-Muster: RG64116 -> LingoPlay, 32xxxxxx -> TimeTEX
- PDF-Inhalt: "Anthropic, PBC" -> Anthropic, "TimeTEX" -> TimeTEX
- Fehlbeleg-Marker: "Sendungsverfolgung", "Tracking" -> _Fehlbelege

Unterstuetzte Anbieter:
  Anthropic, TimeTEX, LingoPlay, Autismusverlag, PayPal,
  eBay, Temu, Amazon, Apple, Google

BIDI-SYNC (BIDIREKTIONALER TXT-SYNC)
-------------------------------------
Erweiterte Aktionen direkt in TXT-Dateien schreiben.
Der Sync parst diese und fuehrt sie in der DB aus.

AKTIONS-TYPEN:
  MOVE (Verschieben):
    42-3 -> W              In Werbungskosten verschieben
    42-3 -> G 0.5          In Gemischte mit 50% Anteil
    42-3 -> V privat       In Verworfen mit Bemerkung
    B42 -> W               Alle Posten eines Belegs verschieben

  EDIT (Bearbeiten):
    42-3 :: brutto=19.99   Bruttobetrag aendern
    42-3 :: bezeichnung=Neuer Name
    42-3 :: anteil=0.7     Anteil aendern

  DELETE (Loeschen):
    42-3 DELETE            Einzelnen Posten loeschen
    42-3 DEL               Kurzform

  DEPRECATED (Beleg ausbuchen):
    B42 DEPRECATED         Beleg als ungueltig markieren
    B42 DEPRECATED Duplikat  Mit Begruendung

EINGABE-BEREICH:
  Aktionen in TXT-Dateien im Bereich "EINGABEN" schreiben:

  === EINGABEN (werden bei Sync verarbeitet) ===
  42-3 -> W
  43-1 :: brutto=25.50
  B44 DEPRECATED Storniert
  === ENDE EINGABEN ===

SYNC AUSFUEHREN:
  python tools/steuer/steuer_sync.py sync
  oder: bach steuer beleg sync

HINWEISE:
  - Aktionen werden bei Sync verarbeitet und dann entfernt
  - Fehlerhafte Aktionen werden im Error-Log gemeldet
  - Immer erst --dry-run testen (falls verfuegbar)

TYPISCHER WORKFLOW
------------------
0. Neue Belege vorsortieren (beleg_vorfilter.py)

1. Status pruefen:
   bach steuer beleg list --status NICHT_ERFASST

2. Offene Belege nach Anbieter sehen:
   bach steuer beleg list --status NICHT_ERFASST --limit 500

3. Im Chat-Agent Belege erfassen

4. Ergebnis pruefen:
   bach steuer posten list --liste W

BATCH-VERARBEITUNG MIT BUNDLES
------------------------------
Bei vielen Belegen ist Einzelpruefung ineffizient. Stattdessen:

1. Bundle erstellen:
   python agents/_experts/steuer/make_bundle.py <quelle> <start> <ende>

   Beispiele:
     python agents/_experts/steuer/make_bundle.py paypal 171 214
     python agents/_experts/steuer/make_bundle.py ebay 77 128
     python agents/_experts/steuer/make_bundle.py google_play 129 170
   
   Quellen: paypal, ebay, google_play, amazon, weitere, temu
   Ausgabe: user/steuer/2025/bundles/<quelle>_B<start>-B<ende>.txt

2. Bundle analysieren:
   Claude liest das Bundle und klassifiziert alle Belege in:
   - W = Werbungskosten (100% absetzbar)
   - G = Gemischt (anteilig, z.B. 50%)
   - V = Verworfen (privat, Duplikate, Status-Mails)
   - Z = Zurueckgestellt (noch zu klaeren)

3. Posten batch-erfassen:
   bach steuer posten add --belegnr 195 --bezeichnung "..." --brutto 55.85 --liste W ...

4. TXT-Dateien aktualisieren:
   python agents/_experts/steuer/regenerate_txt.py

HINWEISE ZUR KLASSIFIZIERUNG
----------------------------
- PayPal: Temu-Zahlungen sind Duplikate (Originale im Temu-Ordner)
- eBay: Viele Mails pro Kauf (Bestellung, Versand, Zustellung, Rechnung)
        -> Nur die Rechnung/Bestellbestaetigung als Hauptbeleg erfassen
        -> Status-Mails als V mit 0 EUR erfassen (Vollstaendigkeit)
- Therapie-Material: LEGO, Lernspiele, Fachliteratur = W
- Software: Microsoft 365, Office = G mit 50%
- Streaming: Netflix, Disney+ = V (privat)

DATENBANK
---------
Alle Daten in: data/bach.db

Tabellen:
- steuer_dokumente     Alle Belege mit Status
- steuer_posten        Alle Posten mit Zuordnung

Profile werden als TXT-Dateien in user/steuer/profile/ gespeichert.

CHAT-AGENT
----------
Der Steuer-Agent ist als Chat-Agent unter
agents/steuer-agent.txt verfuegbar.

Er kann:
- Belege aus PDFs erfassen
- Posten automatisch kategorisieren
- Duplikate erkennen
- Mit dem Nutzer validieren
- Finanzamt-ZIP mit allen Belegen erstellen

BEREICHS-READMES (Stichwort-Nachschlagewerke)
---------------------------------------------
Jeder Steuer-Bereich hat eine README.txt mit Stichworttabelle,
benoetigten Belegen und aktuellen Pauschbetraegen (Stand 2025).

  Datei                                              Bereich / Paragraph
  ------------------------------------------------   --------------------------
  user/steuer/[JAHR]/STEUER_README.txt               Gesamtverfahren & Sync
  user/steuer/[JAHR]/Werbungskosten/README.txt       Anlage N (Paragraph 9)
  user/steuer/[JAHR]/Außergewöhnliche Belastungen/   Paragraph 33 EStG
    README.txt
  user/steuer/[JAHR]/Haushaltsnahe Dienstleistungen  Paragraph 35a EStG
    & Handwerker/README.txt
  user/steuer/[JAHR]/Sonderausgaben/README.txt       Paragraph 10 EStG
  user/steuer/[JAHR]/Versicherungen und              Anlage Vorsorgeaufwand
    Altersvorsorge/README.txt

Inhalt der READMEs:
  - Definition des Bereichs mit Rechtsgrundlage
  - Stichworttabelle: Was kann eingereicht werden + benoetigte Belege
  - Wichtige Pauschbetraege und Hoechstgrenzen
  - Praxis-Hinweise

SIEHE AUCH
----------
  bach --help tasks                    Allgemeine Aufgaben
  bach --help backup                   Backup-System
  wiki/steuer/_index.txt          Steuer-Wiki (Hintergrundwissen)
  wiki/steuer/est_bereiche.txt    EStG-Anlagen Uebersicht
  wiki/steuer/versicherungen.txt  Absetzbare Versicherungen
  wiki/steuer/sonderausgaben.txt  Sonderausgaben absetzen
  wiki/steuer/fortbildung.txt     Fortbildung und Studium
  wiki/steuer/fahrtkosten_homeoffice.txt  Fahrtkosten & Homeoffice
  agents/steuer-agent.txt      Steuer-Agent (Chat-Agent)


## Strategic

STRATEGISCHE DOKUMENTE - METAKOGNITION
=======================================

STAND: 2026-02-08

UEBERSICHT
----------
BACH verwendet drei zentrale Dokumente zur langfristigen Steuerung und Metakognition:

  system/ROADMAP.md      Vision, Phasen, langfristige Ziele
  system/CHANGELOG.md    Aenderungshistorie (Versionen, Datum, Details)
  system/BUGLOG.md       Bug-Tracking und bekannte Probleme

Ergaenzend:
- Lessons und strategische Erkenntnisse landen in memory/MEMORY.md.
- Bugs werden zusaetzlich ueber das Task-System (Kategorie: maintenance/bug) getrackt.

EINORDNUNG IM MEMORY-SYSTEM
---------------------------

  +---------------------------------------------------------------+
  |                    METAKOGNITION (Strategie)                  |
  |  +-----------------------------------------------------------+|
  |  | system/ROADMAP.md  | system/CHANGELOG.md | memory/MEMORY.md||
  |  | system/BUGLOG.md   | docs/con3_*.md      | Analysen        ||
  |  +-----------------------------------------------------------+|
  |                          |                                    |
  |                          | Ableitung                          |
  |                          v                                    |
  |  +-----------------------------------------------------------+|
  |  |                    TASK-SYSTEM (Planung)                  ||
  |  |  Konkrete, ausfuehrbare Aufgaben                           ||
  |  |  bach task list / add / done                              ||
  |  +-----------------------------------------------------------+|
  |                          |                                    |
  |                          | Ausführung                         |
  |                          v                                    |
  |  +-----------------------------------------------------------+|
  |  |              MEMORY-SYSTEM (Operativ)                     ||
  |  |  memory_sessions | memory_lessons | memory_working        ||
  |  +-----------------------------------------------------------+|
  +---------------------------------------------------------------+

KREISLAUF:
  1. Strategie definiert Ziele (system/ROADMAP.md)
  2. Ziele werden zu Tasks (Task-System)
  3. Tasks erzeugen Aktivitäten (Sessions / Log)
  4. Ereignisse werden konsolidiert (bach consolidate)
  5. Ergebnisse aktualisieren Strategie (memory/MEMORY.md)

DOKUMENT-STILE
--------------

system/ROADMAP.md:
  - Fokus: Vision, Phasen, Meilensteine.
  - Granularität: Grobe Blöcke (z.B. "Phase 12: Steuer").
  - Ziel: Orientierung für Partner-Agenten (Wo stehen wir?).

memory/MEMORY.md:
  - Fokus: Kritische Erkenntnisse und Lessons Learned.
  - Stil: Strukturierte Dokumentation von Problemen und Lösungen.
  - Kategorien: Nach Feature/Modul organisiert.

KONSOLIDIERUNG ZU STRATEGIE
---------------------------
Dieser Prozess überführt operative Daten in strategische Dokumente:

  Rohdaten ---[bach session end]---> Sessions (DB)
  Sessions ---[bach consolidate compress]---> Context (DB)
  Tasks (done) ---[Manuelle Pflege]---> memory/MEMORY.md

BEFEHLE ZUR UNTERSTUETZUNG:
  bach consolidate status                    Zeigt Konsolidierungs-Status
  bach consolidate compress --batch          Gruppiert Sessions (einfach)
  bach consolidate compress --run            Komprimiert mit Regelwerk
  bach consolidate review                    Erstellt Review-Tasks für Wiki/Doku
  bach consolidate run                       Führt alle Prozesse aus

SIEHE AUCH
----------
  docs/docs/docs/help/consolidation.txt     Memory-Konsolidierung
  docs/docs/docs/help/tasks.txt             Task-System
  docs/docs/docs/help/memory.txt            Memory-System
  system/ROADMAP.md          Aktuelle Phase & Meilensteine
  system/CHANGELOG.md        Aenderungshistorie
  system/BUGLOG.md           Bug-Tracking
  memory/MEMORY.md           Kritische Erkenntnisse & Lessons


## Strategien

STRATEGIEN
==========
Grundlegende Handlungsstrategien fuer Problemloesung und Automatisierung.

Bezug: docs/docs/docs/help/operatoren.txt, docs/docs/docs/help/denkstrategien.txt


1. KATEGORISIEREN
=================
Strategie: Regeln, Heuristiken oder Modelle ordnen Daten Klassen zu.
Operatoren: Extrahieren -> Normalisieren -> Klassifizieren -> Validieren

Beispiel (Python):
```python
def classify_doc(doc):
    text = doc["text"].lower()
    if "rechnung" in text:
        return "invoice"
    if "vertrag" in text:
        return "contract"
    return "other"
```


2. BEWERTEN (Scoring)
=====================
Strategie: Kriterien definieren, gewichten, Score berechnen.
Basis fuer Ranking, Automatisierung, Human-Review.

Beispiel (Python):
```python
def score_invoice(mail):
    score = 0
    if "rechnung" in mail["subject"].lower():
        score += 0.5
    if any(a.endswith(".pdf") for a in mail["attachments"]):
        score += 0.3
    if "iban" in mail["body"].lower():
        score += 0.2
    return score
```


3. AUSSCHLIESSEN
================
Strategie: Negativkriterien definieren (Blacklists, Muster, Grenzen).
Fruehzeitiges "Cut-off" reduziert Rauschen.

Beispiel (JavaScript):
```javascript
function isExcluded(mail) {
  const blacklist = ["noreply@", "newsletter@"];
  return blacklist.some(b => mail.from.includes(b));
}

const relevant = mails.filter(m => !isExcluded(m));
```


4. TESTEN (Validieren)
======================
Strategie: Daten gegen Regeln, Schemata, Referenzquellen pruefen.
Varianten: Schema-Tests, Business-Regeln, A/B-Vergleich, Cross-Source-Check.

Beispiel - Schema-Test (Python):
```python
def validate_invoice(d):
    tests = [
        ("amount", lambda x: x is not None and x > 0),
        ("invoice_number", lambda x: bool(x)),
        ("date", lambda x: x is not None),
    ]
    errors = []
    for field, rule in tests:
        if not rule(d.get(field)):
            errors.append(field)
    return errors
```

Beispiel - A/B-Test (Python):
```python
def classify_A(doc): ...
def classify_B(doc): ...

resA = classify_A(doc)
resB = classify_B(doc)

if resA != resB:
    # Konflikt markieren, fuer Analyse loggen
    pass
```


5. PROBLEME DEFINIEREN
======================
Strategie: Problem als Input -> gewuenschter Output -> Constraints formulieren.
In Code: klare Schnittstellen, erwartete Invarianten, Fehlerklassen.

Beispiel-Formulierung:
  Problem: "Eingehende E-Mails sollen automatisch als Rechnung,
           Vertrag oder Sonstiges klassifiziert werden."
  Input:   E-Mail (Betreff, Body, Anhaenge, Metadaten)
  Output:  Kategorie + Score + ggf. Extrakte
  Constraints: keine False-Positives bei Rechnungen ueber X EUR,
               Score-Schwellen, Logging


6. PROBLEMLOESE-STRATEGIEN
==========================
Generisches Muster fuer strategie-basierte Entscheidungen.

```python
def solve_problem(input_data, strategies):
    """
    strategies: Liste von Strategien mit:
      - name
      - condition(input_data) -> bool
      - action(input_data) -> result
    """
    for s in strategies:
        if s["condition"](input_data):
            return {
                "strategy": s["name"],
                "result": s["action"](input_data)
            }
    return {
        "strategy": None,
        "result": None
    }
```

Beispiel-Strategien (Confidence-Based):
```python
strategies = [
    {
        "name": "high_confidence_auto",
        "condition": lambda d: d["score"] >= 0.9,
        "action": lambda d: {"mode": "auto", "route": "buchhaltung"}
    },
    {
        "name": "medium_confidence_review",
        "condition": lambda d: 0.6 <= d["score"] < 0.9,
        "action": lambda d: {"mode": "review", "route": "inbox_review"}
    },
    {
        "name": "low_confidence_ignore",
        "condition": lambda d: d["score"] < 0.6,
        "action": lambda d: {"mode": "ignore", "route": None}
    },
]
```


BEZUG ZU BACH
=============
Diese Strategien sind die Basis fuer:
  - Injektoren (Kontext-basierte Entscheidungen) - system/tools/injectors.py
  - Memory-Konsolidierung (Lesson-Ableitung) - system/hub/consolidation.py
  - Workflow-Routing (Skills und Services)
  - Dokumenten-Verarbeitung (OCR, Klassifikation)

Strategien + Operatoren = wiederverwendbare Loesungsbausteine


VERWANDTE HELP-DATEIEN
======================
  --help operatoren      Basis-Operatoren und Patterns
  --help denkstrategien  Kognitive Strategien
  --help rhetorik        Rhetorische Operatoren


## Tasks

TASKS - Aufgaben-System
=======================

STAND: 2026-02-08

Das Task-System (Schicht 5) orchestriert die Arbeit zwischen User und
Partner-Agenten (Claude, Gemini, etc.).

KERNKONZEPTE
------------
- MANUELLE TASKS: Via `bach task add` (Tabelle: `tasks`).
- GESCANNTE TASKS: Aus Code-Kommentaren (Tabelle: `ati_tasks`).
- MULTI-PARTNER: Zuweisung via `--assigned` an Agenten oder User.
- DISTI-TIERS: Tasks sind via `dist_type` (User/Template/Core) getrennt.

ZWEI ZUGRIFFSWEGE (NEU ab v2.0)
-------------------------------
BACH hat ZWEI parallele Zugangswege - beide nutzen dieselben Handler + DB:

1. CLI (fuer Menschen am Terminal):
     python bach.py task add "Titel" --priority P4

2. LIBRARY-API (BEVORZUGT fuer LLM/Scripts):
     from bach_api import task
     task.add("Titel", "--priority", "P4")
     task.list()
     task.done(42, "--note", "Erledigt")

CLI-BEFEHLE (bach task)
-----------------------
  add <titel>       Erstellt Task (--priority P1-P4, --description, --category)
  list [filter]     Gefilterte Uebersicht (pending/done/blocked/all)
  list --filter     Nach Begriff im Titel filtern
  list --assigned   Tasks fuer einen bestimmten Partner
  list --unassigned Tasks ohne Zuweisung
  show <ID>         Details inkl. Beschreibung und Historie
  edit <ID>         Bearbeitet Task (--title, --description, --category, --assigned)
  done <ID>         Markiert Task als erledigt (Multi-ID, --note)
  block <ID>        Blockiert Task(s) (Multi-ID, --reason)
  unblock <ID>      Entblockt Task(s) (Multi-ID)
  reopen <ID>       Oeffnet erledigte Task(s) erneut (Multi-ID)
  delete <ID>       Loescht Task(s) permanent (Multi-ID)
  priority <ID> <P> Aendert Prioritaet (P1-P4)
  assign <ID>       Zuweisung an Partner (--to GEMINI/COPILOT/etc.)
  depends <ID>      Zeigt Abhaengigkeiten an
    --on <X>        Fuegt Abhaengigkeit hinzu (Task wartet auf X)
    --remove <X>    Entfernt Abhaengigkeit
    --clear         Loescht alle Abhaengigkeiten

LIBRARY-API BEISPIELE
---------------------
  from bach_api import task

  # Task erstellen
  task.add("Doku schreiben", "--priority", "P2", "--category", "docs")

  # Tasks auflisten
  task.list("pending")
  task.list("all", "--assigned", "GEMINI")
  task.list("--unassigned")

  # Tasks bearbeiten
  task.edit(42, "--title", "Neuer Titel")
  task.done(100, 101, 102, "--note", "Alle erledigt")
  task.assign(200, "--to", "COPILOT")

  # Abhaengigkeiten
  task.depends(306, "--on", "305")  # Task 306 wartet auf 305
  task.depends(306)                 # Abhaengigkeiten anzeigen

SCAN-TASKS (hub/ati.py)
-----------------------
  bach ati onboard --check    Scannt das Filesystem nach neuen Aufgaben.
  bach scan tasks             Listet Aufgaben aus `ati_tasks` auf.

DATENBANK (Schicht 1)
---------------------
- `tasks`: id, title, description, status, priority, assigned_to, delegated_to,
  depends_on, category, tags, created_at, completed_at, updated_at, dist_type.
- `ati_tasks`: Gescannte Aufgaben mit Source-Link (File/Line).
- DB-Pfad: system/data/bach.db

GUI & INTEGRATION (geplant)
---------------------------
Das **Task-Board** (/tasks) ist als Kanban-Ansicht geplant, die das
Verschieben von Tasks zwischen Status-Spalten ermoeglicht.

SIEHE AUCH
----------
  system/bach_api.py   Library-API Modul (bevorzugter Zugriff)
  system/hub/task.py   TaskHandler Implementation
  docs/help/delegate.txt    Delegation an Partner
  docs/help/maintain.txt    Integritaets-Pruefung und Cleanup
  docs/help/ati.txt    Der Automated Tool Incorporator


## Test

TEST - BACH Test- und QA-System
================================

UEBERSICHT
----------
Systematisches Testen von BACH und Vergleich mit anderen Systemen.
Nutzt B-Tests (automatisiert), O-Tests (funktional) und E-Tests (subjektiv).

BEFEHLE
-------
  bach --test self [PROFIL]     BACH selbst testen (default: QUICK)
  bach --test run <path>        Anderes System testen
  bach --test compare <path>    System mit BACH vergleichen
  bach --test profiles          Verfuegbare Profile anzeigen
  bach --test results [system]  Testergebnisse anzeigen

TESTPROFILE
-----------
  QUICK         Schnelltest (~5 Min) - B001, O001
  STANDARD      Standard (~20 Min) - B001-B005, O001-O003
  FULL          Vollstaendig (~40 Min) - Alle Tests
  OBSERVATION   Nur B-Tests (~15 Min)
  OUTPUT        Nur O-Tests (~20 Min)
  MEMORY_FOCUS  Memory-Fokus (~10 Min)
  TASK_FOCUS    Task-Fokus (~10 Min)

DREI TESTPERSPEKTIVEN
---------------------
  B-Tests (Beobachtung)   Extern, automatisiert, Python-Scripts
                          "Was existiert?"
  
  O-Tests (Ausgabe)       Funktional, Input->Output, Python-Scripts
                          "Funktioniert es?"
  
  E-Tests (Erfahrung)     Intern, subjektiv, Claude-gefuehrt
                          "Wie fuehlt es sich an?"

BEWERTUNGSSKALA
---------------
  5 = Exzellent
  4 = Gut
  3 = Akzeptabel
  2 = Mangelhaft
  1 = Kritisch

BEISPIELE
---------
  bach --test self              Schneller Selbsttest
  bach --test self STANDARD     Standard-Selbsttest
  bach --test compare "C:\X"    BACH mit anderem System vergleichen
  bach --test results           Alle Ergebnisse anzeigen

IMPLEMENTIERUNG
---------------
  Handler:      system/hub/test.py
  Status:       Test-Infrastruktur (tools/testing/) NICHT vorhanden
  Hinweis:      Handler existiert, aber Tools/Agent fehlen noch


## Timer

TIMER - Stoppuhr
================

Misst verstrichene Zeit. Mehrere Timer gleichzeitig moeglich.

CLI-BEFEHLE
-----------

  bach timer start              Unbenannten Timer starten
  bach timer start "Recherche"  Benannten Timer starten
  bach timer stop               Letzten/einzigen Timer stoppen
  bach timer stop "Recherche"   Benannten Timer stoppen
  bach timer list               Alle aktiven Timer anzeigen
  bach timer clear              Alle Timer loeschen

AUSGABE-FORMAT
--------------

  [TIMER] Recherche: 05:23 | Session: 45:12

Bei jeder CLI-Ausgabe werden aktive Timer angezeigt.

PERSISTENZ
----------

  Datei: data/.timer_state

  Inhalt:
  {
    "timers": {
      "Recherche": "2026-01-30T14:00:00",
      "Session": "2026-01-30T13:50:00"
    }
  }

BEISPIELE
---------

  # Session-Timer starten
  bach timer start "Session"
  -> Timer 'Session' gestartet

  # Zusaetzlichen Timer fuer Teilaufgabe
  bach timer start "Bugfix"
  -> Timer 'Bugfix' gestartet

  # Status pruefen
  bach timer list
  -> Session: 45:12
  -> Bugfix:  05:23

  # Bugfix-Timer stoppen
  bach timer stop "Bugfix"
  -> Timer 'Bugfix' gestoppt: 05:23

USECASES
--------

  1. SESSION-TRACKING
     bach timer start "Session"
     ... arbeiten ...
     bach timer stop "Session"
     -> Zeigt wie lange die Session dauerte

  2. TASK-TRACKING
     bach timer start "Task-123"
     ... Task bearbeiten ...
     bach timer stop "Task-123"
     -> Zeit kann in Task-Kommentar notiert werden

  3. PARALLEL-TRACKING
     bach timer start "Gesamt"
     bach timer start "Recherche"
     ... recherchieren ...
     bach timer stop "Recherche"
     bach timer start "Coding"
     ... coden ...
     bach timer stop "Coding"
     bach timer stop "Gesamt"
     -> Zeigt Zeitverteilung

ZUSAMMENSPIEL
-------------

Timer ist Teil des Zeit-Systems:
  --help clock      Uhrzeit-Anzeige
  --help countdown  Countdown mit Trigger
  --help between    Between-Checks
  --help beat       Unified Zeit-Anzeige

---
Version: 1.0 | Status: Implementiert (v1.1.83)
Handler: system/hub/time.py (TimerHandler)


## Tools

TOOLS - Tool-Verwaltung
=======================

BESCHREIBUNG
------------
BACH verwaltet drei Arten von Tools:
1. Python-Tools: Scripts in tools/ (Coding, Steuer, Migration)
2. CLI-Tools: Kommandozeilen-Programme (git, ffmpeg, python)
3. Externe KI-Tools: Web-basierte KI-Dienste (ChatGPT, Midjourney)

Die CLI- und externen Tools werden in der Datenbank verwaltet (bach.db/tools).

CLI-BEFEHLE
-----------
bach --tools list              Python-Tools auflisten (Dateisystem)
bach --tools db                Alle DB-Tools auflisten (CLI + extern)
bach --tools db --type cli     Nur CLI-Tools anzeigen
bach --tools db --type external Nur externe KI-Tools anzeigen
bach --tools show <n>       Tool-Details anzeigen
bach --tools run <n> [args] Python-Tool ausfuehren
bach --tools search <term>     Tools durchsuchen (Dateisystem + DB)
bach --tools migrate           Migration der Connections starten

DIREKTAUFRUF VIA BACH (empfohlen)
---------------------------------
Tools koennen direkt ueber bach.py aufgerufen werden - ohne --tools run:

  bach <toolname> [argumente]

Beispiele:
  bach python_cli_editor script.py --show-all     Struktur anzeigen
  bach c_encoding_fixer datei.py                  Encoding reparieren
  bach c_import_organizer datei.py --save         Imports sortieren
  bach c_json_repair kaputt.json                  JSON reparieren
  bach c_pycutter grosse_datei.py                 Datei aufteilen
  bach c_sqlite_viewer data/bach.db               DB anzeigen
  bach code_analyzer projekt/                     Code analysieren

Vorteile:
  - Kuerzer als: bach --tools run c_encoding_fixer datei.py
  - Tab-Completion moeglich
  - Gleiche Syntax wie direkter Python-Aufruf

Hinweis: Funktioniert fuer alle Tools in tools/*.py

TOOL-UEBERSICHTEN
-----------------
Verschiedene Wege um verfuegbare Tools zu finden:

  bach --tools list              Alle Python-Tools (tools/*.py)
  bach --tools db                Alle DB-Tools (CLI + extern)
  bach --tools search <term>     Nach Begriff suchen
  bach tool suggest "problem"    Problem-basierte Empfehlung
  bach --help tools              Diese Hilfe
  bach --help tools/_index       Index der Tool-Dokumentationen

Fuer spezifische Tool-Hilfe:
  bach <tool> --help             Argparse-Hilfe des Tools
  bach --help tools/<tool>       Ausfuehrliche Dokumentation (falls vorhanden)

TOOL-DISCOVERY (NEU v1.1.27)
----------------------------
Problem-basiertes Tool-Matching: Beschreibe ein Problem und erhalte Tool-Empfehlungen.

bach tool suggest "Encoding-Problem in Datei"  Tool-Empfehlung basierend auf Problem
bach tool suggest "JSON reparieren"            Findet json_repair_tool.py
bach tool patterns                             Alle Problem-Pattern anzeigen

Funktionsweise:
1. Keyword-Extraktion aus Problem-Beschreibung
2. Matching gegen 15+ Problem-Kategorien
3. Score-basierte Empfehlung passender Tools

Problem-Kategorien: encoding, json_repair, code_analysis, import_issues,
formatting, database, conversion, backup, cleanup, documentation,
path_issues, duplicate, emoji, german_text, steuer

Code: tools/tool_discovery.py (195 Zeilen)

PYTHON-TOOLS (tools/)
---------------------
Praefix-Konvention (siehe: bach --help naming):

  c_*        CLI-optimiert fuer AI (Claude/recludOS)
             - Klare Outputs, encoding-sicher, JSON-safe
  b_*        BACH-Kern (System-kritisch)
  a_*        Agent-Runner
  t_*        Test-Tools
  m_*        Maintain/Wartung
  g_*        Generator-Tools

Legacy-Praefixe (werden migriert):
  agent_*    -> a_*
  backup_*   -> b_* oder m_*
  migrate_*  -> m_*

Domain-Praefixe (bleiben):
  ollama_*   Ollama-Integration
  steuer_*   Steuer-Tools (in tools/steuer/)

PYTHON-TOOLS NACH FUNKTION
--------------------------

### CLI-zugaenglich (via Handler)

  Verzeichnis    Handler               Funktion
  -------------  --------------------  ----------------------------
  testing/       --test                Test-System (B/O/E-Tests)
  generators/    --maintain generate   Skill/Agent Generatoren
  mapping/       (direkt)              Feature-Mapping

### Kernfunktionen

  Tool                      Funktion
  ------------------------  ----------------------------
  autolog.py                Auto-Logging System
  autolog_analyzer.py       AutoLog-Analyse
  backup_manager.py         Backup-Verwaltung
  injectors.py              Injector-System
  c_dirscan.py              Verzeichnis-Scan
  session_analyzer.py       Session-Analyse
  time_system.py            Zeit-System
  token_monitor.py          Token-Monitoring
  success_tracker.py        Success-Tracking
  fs_protection.py          Dateisystem-Schutz

### Wartung (via --maintain Handler)

  Tool                      CLI-Befehl                  Funktion
  ------------------------  --------------------------  ----------------------------
  doc_update_checker.py     bach --maintain docs        Dokumentations-Check
  c_duplicate_detector.py   bach --maintain duplicates  Duplikat-Erkennung
  c_pattern_tool.py         bach --maintain pattern     Dateinamen-Patterns
  c_tool_scanner.py         bach --maintain scan        CLI-Tools Discovery
  c_file_cleaner.py         bach --maintain clean       Alte Dateien loeschen
  c_json_fixer.py           bach --maintain json        JSON reparieren
  c_sync_registry.py        Registry synchronisieren
  c_json_registry_cleaner.py Registry-Bereinigung
  backup_manager.py         Backup-Verwaltung
  nulcleaner.py             NUL-Character entfernen

### Generator-Tools (tools/generators/)

  Tool                      CLI-Befehl                  Funktion
  ------------------------  --------------------------  ----------------------------
  skill_generator.py        bach --maintain generate    Skill-Strukturen erstellen
  exporter.py               bach --maintain export      Skills/Agents exportieren

  Profile fuer skill_generator:
    MICRO    - Nur Datei(en), kein Ordnersystem
    LIGHT    - Minimal (SKILL.md + config + data)
    STANDARD - Standard-Skill mit einfachem Memory
    EXTENDED - Komplexer Skill mit Mikro-Skills

### Mapping-Tools (tools/mapping/)

  Tool                      Funktion
  ------------------------  ----------------------------
  query_features.py         Feature-Matrix abfragen
  populate_features.py      Datenbank befuellen
  schema.sql                DB-Schema

  Wichtig: DB_PATH Variable muss angepasst werden!

### Coding-Tools

  Tool                      Funktion
  ------------------------  ----------------------------
  c_encoding_fixer.py       Encoding reparieren
  c_emoji_scanner.py        Emoji finden/ersetzen
  c_standard_fixer.py       Code-Standards anwenden
  c_json_repair.py          JSON reparieren
  c_json_fixer.py           JSON reparieren (alt)
  c_import_organizer.py     Imports sortieren
  c_import_diagnose.py      Import-Probleme finden
  c_indent_checker.py       Einrueckung pruefen
  c_umlaut_fixer.py         Umlaute korrigieren
  c_german_scanner.py       Deutsche Woerter finden
  c_method_analyzer.py      Methoden analysieren
  c_pycutter.py             Python-Dateien aufteilen
  c_sqlite_viewer.py        SQLite-Datenbanken anzeigen
  c_license_generator.py    Lizenzdateien erstellen
  c_md_to_pdf.py            Markdown zu PDF
  c_universal_converter.py  Format-Konvertierung
  c_universal_compiler.py   Universal Compiler
  c_youtube_extractor.py    YouTube-Extraktion
  c_code_analyzer.py        Code-Analyse
  c_code_generator.py       Code-Generierung
  c_python_cli_editor.py    Python strukturiert bearbeiten
  c_structure_generator.py  Struktur-Generator
  c_header_migrate.py       Header-Migration
  call_graph.py             Call-Graph-Analyse

### Steuer-Tools

  Tool                      Funktion
  ------------------------  ----------------------------
  steuer_scanner.py         Belege scannen
  steuer_sync.py            Synchronisation
  steuer_batch.py           Batch-Verarbeitung
  steuer_apply.py           Kategorien anwenden
  setup_steuer_db.py        DB-Setup
  scan_new_belege.py        Neue Belege erkennen
  rename_belege.py          Belege umbenennen
  show_posten.py            Posten anzeigen
  temu_ocr_batch.py         Temu-OCR Batch
  ocr_engine.py             OCR-Engine

### Ollama-Tools

  Tool                      Funktion
  ------------------------  ----------------------------
  ollama_benchmark.py       Benchmarks
  ollama_summarize.py       Zusammenfassungen
  ollama_worker.py          Worker-Prozess

### Test-Tools (tools/testing/)

  Tool                      CLI-Befehl                  Funktion
  ------------------------  --------------------------  ----------------------------
  test_runner.py            bach --test run             Test-Ausfuehrung
  run_b_tests.py            bach --test self            B-Tests ausfuehren
  run_o_tests.py            bach --test ops             O-Tests ausfuehren

  Testprofile (testing/profiles/):
    QUICK.json          - Schnelle Pruefung
    STANDARD.json       - Standard-Suite
    FULL.json           - Vollstaendige Pruefung
    MEMORY_FOCUS.json   - Memory-Tests
    TASK_FOCUS.json     - Task-Tests
    OUTPUT.json         - Output-Tests
    OBSERVATION.json    - Beobachtungs-Tests

### MCP-Integration (NEU v2.2)

  Tool                      Funktion
  ------------------------  ----------------------------
  mcp_server.py             MCP Server v2.0 (654 Zeilen)
                            - 23 Tools (Task, Memory, Lesson, Backup, Steuer)
                            - 8 Resources (Tasks, Status, Memory, Skills, Contacts)
                            - 3 Prompts (Daily Briefing, Task Review, Session Summary)

  Installation:
    pip install mcp
    python tools/mcp_server.py

  Claude Code Config (~/.claude/claude_code_config.json):
    {
      "mcpServers": {
        "bach": {
          "command": "python",
          "args": ["C:/path/to/system/tools/mcp_server.py"]
        }
      }
    }

### Skill-Management (NEU)

  Tool                      Funktion
  ------------------------  ----------------------------
  c_skill_init.py           Skill-Struktur initialisieren
  c_skill_package.py        Skills paketieren
  c_skill_validate.py       Skill-Validierung
  skill_export.py           Skills exportieren
  skill_header_gen.py       Skill-Header generieren
  skill_help_gen.py         Skill-Hilfe generieren

### Projekt-Tools (NEU)

  Tool                      Funktion
  ------------------------  ----------------------------
  c_project_bundler.py      Projekt-Bundler
  c_audit_bundler.py        Audit-Bundle erstellen
  c_path_healer.py          Pfad-Reparatur
  batch_file_ops.py         Batch-Dateioperationen

### Analyse & Monitoring

  Tool                      Funktion
  ------------------------  ----------------------------
  db_check.py               Datenbank-Check
  debug_scan.py             Debug-Scan
  forensic_db_scan.py       Forensik DB-Scan
  folder_diff_scanner.py    Folder-Diff-Analyse
  custom_analysis.py        Custom-Analyse
  schema_reader.py          Schema-Reader
  problems_first.py         Problems-First Ansatz
  reports.py                Report-System

### Generator & Helper

  Tool                      Funktion
  ------------------------  ----------------------------
  c_dictionary_builder.py   Wörterbuch-Builder
  lesson_trigger_generator.py Lesson-Trigger-Generator
  theme_packet_generator.py Theme-Packet-Generator
  workflow_trigger_generator.py Workflow-Trigger-Generator
  trigger_maintainer.py     Trigger-Wartung
  context_compressor.py     Kontext-Kompression
  translate_batch.py        Batch-Übersetzung

### Integration & Import

  Tool                      Funktion
  ------------------------  ----------------------------
  gemini_llm.py             Gemini LLM Integration
  data_importer.py          Daten-Import
  document_indexer.py       Dokumenten-Indexierung
  doc_search.py             Dokumentensuche
  inbox_watcher.py          Inbox Watcher
  user_console.py           User-Console

### Agents & Auto-Discovery

  Tool                      Funktion
  ------------------------  ----------------------------
  c_headless_agent.py       Headless Agent
  bach_auto_discovery.py    Auto-Discovery System
  tool_auto_discovery.py    Tool Auto-Discovery

### User-Tools (tools/_user/)

  System-spezifische Tools (nicht fuer Distribution):
  - auto_backup_orchestrator.py   FTP-Backup
  - fritzbox_wlan_control.py      WLAN-Steuerung
  - backup_watchdog.py            Backup-Ueberwachung

  Siehe: tools/_user/README.md

CLI-TOOLS (bach.db)
-------------------
Verfuegbare Kategorien:
  archive         7z (Komprimierung)
  editor          notepad++
  ide             code (VS Code)
  multimedia      ffmpeg (Video/Audio)
  network         curl, ssh
  package_manager pip, pip3
  runtime         python, node
  text_processing grep
  version_control git

EXTERNE KI-TOOLS (bach.db)
--------------------------
Kategorien:
  llm       ChatGPT, Claude, Gemini, Copilot, Mistral, Groq
  image     Midjourney, Ideogram, Leonardo, Flux, Magnific
  video     Runway, Luma, Pika, Kling
  audio     ElevenLabs, Suno, Udio, Descript, Auphonic
  research  Perplexity, Consensus, Elicit, NotebookLM, Scite
  dev       Cursor, Bolt, Copilot Workspace, Replit, Windsurf
  edu       Gamma, Notion AI, Goblin Tools, Taskade

DATENBANK-SCHEMA
----------------
Tabelle: tools (in data/bach.db)

Wichtige Felder:
- name          TEXT UNIQUE
- type          TEXT (cli, external, internal)
- category      TEXT
- command       TEXT (fuer CLI-Tools)
- endpoint      TEXT (fuer externe Tools)
- description   TEXT
- capabilities  JSON-Array
- use_for       TEXT
- is_available  BOOLEAN

MIGRATION
---------
Die Tools wurden aus JSON-Dateien in die Datenbank migriert.
Die Quell-Dateien existieren nicht mehr (connections/ wurde aufgeloest).

Migration-Status pruefen:
  bach --tools migrate --status

Falls erneute Migration noetig (nur bei Reset):
  python tools/migrate_connections.py

BEISPIELE
---------
# Python-Tools auflisten
bach --tools list

# Alle registrierten Tools (DB)
bach --tools db

# Nur CLI-Tools
bach --tools db --type cli

# Tool-Details
bach --tools show ffmpeg
bach --tools show chatgpt

# Tool ausfuehren
bach --tools run c_encoding_fixer datei.py

# Direktaufruf (empfohlen)
bach c_encoding_fixer datei.py
bach c_skill_init neuer_skill
bach c_project_bundler ./projekt

# Suchen
bach --tools search video

# Wartungs-Tools
bach --maintain list
bach --maintain docs
bach --maintain pattern ./docs --dry-run

# Test-Tools
bach --test profiles
bach --test run QUICK

# MCP Server (NEU)
python tools/mcp_server.py
# Dann via Claude Code verfuegbar (bach:/ Resources + Tools)

TOOL-INVENTAR (~83 Tools)
-------------------------
Gesamt-Statistik nach Kategorie:

  Kategorie          Anzahl  Beschreibung
  -----------------  ------  ----------------------------
  Agent/Framework    8       Agent-System, Service-Integration, MCP
  Development        25      Code-Analyse, Testing, Projekt-Utils
  Database           8       SQLite, Migration, Schema
  Document           15      OCR, Konvertierung, Text-Verarbeitung
  Financial/Steuer   22      Komplette Steuer-Suite
  Maintenance        15      Backup, Distribution, Cleanup, Registry
  Media              2       YouTube-Extraktion, Gemini-LLM
  Utility/Helper     22      Policies, Generators, Monitoring, Sonstige
  Skill-Management   6       Skill-Init, Package, Validate, Export

Naming-Convention (Praefixe):

  c_*   CLI-optimiert fuer AI (40+ Tools)
  b_*   BACH-Kern (System-kritisch)
  a_*   Agent-Runner Tools
  t_*   Test-Tools
  m_*   Maintain-Tools
  g_*   Generator-Tools
  (-)   Domain/Utility (43+ Tools)

Synergie-Potential mit externen Suites:

  BACH-Tool               Synergie mit
  ----------------------  ----------------------------
  steuer/ Suite           Finance Suite (Budget, Expense)
  ocr_engine.py           DokuZentrum Pro
  c_md_to_pdf.py          Obsidian Export
  c_youtube_extractor.py  Media Suite

Quelle: Archiviert in user/_archive/BACH_NATIVE_TOOLS_MAPPING.md

DETAILLIERTE TOOL-DOKUMENTATION
--------------------------------
Fuer komplexe Tools gibt es ausfuehrliche Dokumentation in docs/docs/docs/help/tools/:

  Verfuegbare Dokumentationen:
  ---------------------------
  docs/docs/docs/help/tools/python_cli_editor.txt   Python-Dateien strukturiert bearbeiten
                                     (Klassen/Methoden anzeigen, einfuegen,
                                     loeschen, Edit-Workflow, Export)

  docs/docs/docs/help/tools/_index.txt              Index aller Tool-Dokumentationen

  Abruf:
  ------
  bach --help tools/python_cli_editor    Ausfuehrliche Doku lesen
  bach --help tools/_index               Uebersicht verfuegbarer Doku
  bach --help tools                      Diese allgemeine Tool-Hilfe

  Wann braucht ein Tool eigene Doku?
  ----------------------------------
  - Viele Optionen (>10 Parameter)
  - Komplexe Workflows moeglich
  - Haeufig genutzt
  - Beispiele wichtig zum Verstaendnis

  Einfache Tools nutzen nur:
  - Docstring im Python-File
  - argparse --help (bach <tool> --help)

CONTEXT-INJEKTOR (automatische Tool-Hinweise)
---------------------------------------------
Der ContextInjector erkennt Stichwoerter und empfiehlt passende Tools.
Beispiele:

  Stichwort              Tool-Empfehlung
  ---------------------  ------------------------------------------
  "encoding problem"     bach c_encoding_fixer <datei>
  "imports sortieren"    bach c_import_organizer <datei>
  "python bearbeiten"    bach c_python_cli_editor <datei> --show-all
  "datei aufteilen"      bach c_pycutter <datei>
  "sqlite anzeigen"      bach c_sqlite_viewer <db>
  "tool finden"          bach tool suggest 'beschreibung'
  "skill erstellen"      bach c_skill_init <name>
  "projekt bundlen"      bach c_project_bundler <pfad>
  "pfad reparieren"      bach c_path_healer <datei>
  "mcp starten"          python tools/mcp_server.py

Siehe: bach --help injectors (vollstaendige Trigger-Liste)

SIEHE AUCH
----------
docs/docs/docs/help/tools/_index.txt      Detaillierte Tool-Dokumentation (Index)
docs/docs/docs/help/tools/*.txt           Einzelne Tool-Dokumentationen
docs/docs/docs/help/injectors.txt         Automatische Tool-Hinweise (ContextInjector)
bach --help connections    Connections-Verwaltung
bach --help dirscan           Directory Scanner (Aenderungsueberwachung)
bach --help maintain       Wartungs-Tools
bach --help test           Test-System
bach --help naming         Namenskonventionen (Tool-Praefixe)


## Transkription

TRANSKRIPTION - Transkriptions-Service
======================================

BESCHREIBUNG:
  Experte unter dem Persoenlichen Assistenten. Wandelt Audiodateien und
  Gespraeche in strukturierte Textdokumente um: woertliche Rohtranskripte
  mit Pausennotation, Sprecher-Erkennung/-Zuordnung, Bereinigung und Export.

  Skill-Datei: agents/_experts/transkriptions-service/CONCEPT.md
  User-Daten:  user/transkriptionen/

NOTATION (Rohtranskript):
  (Pause)         Kurze Sprechpause
  (lange Pause)   Pause > 3 Sekunden
  aehm / aeh      Gefuellte Pausen, woertlich transkribiert
  (raeuspert sich) Nicht-verbale Lautaesserung
  (lacht)         Lachen
  (unverstaendlich) Nicht transkribierbar
  (ueberlappend)  Gleichzeitiges Sprechen
  SV1:            Sprecher 1 (vorlaeufig, vor Zuordnung)
  A:              Zugewiesener Sprecher nach Namenszuordnung
  //              Abrupter Abbruch oder Unterbrechung
  [00:03:45]      Optionaler Zeitstempel

WORKFLOW:
  1. Rohtranskript erstellen (woertlich, alle Marker setzen)
  2. Sprecher zuordnen (vorab oder nachtraeglich)
  3. Bereinigen (Fuellwoerter entfernen, glaetten)
  4. Exportieren (TXT / MD / PDF)
  5. Optional: In Notizblock uebertragen

CLI-BEFEHLE (PLAN):
  bach transkript new "Name"                  Neue Transkription starten
  bach transkript new "Name" --sprecher "A:Lukas,B:Interviewer"
  bach transkript speaker-map roh.txt --sv1 "Lukas" --sv2 "Interviewer"
  bach transkript clean roh.txt               Bereinigtes Transkript erstellen
  bach transkript export roh.txt --format md  Export als Markdown
  bach transkript export roh.txt --format pdf Export als PDF (via MCP)
  bach transkript to-notizblock roh.txt --buch "interviews"
  bach transkript list                        Alle Transkriptionen auflisten

DATEIEN:
  user/transkriptionen/roh/           Rohtranskripte mit Notation
  user/transkriptionen/bereinigt/     Bereinigte Leseprotokolle
  user/transkriptionen/audio/         Originaldateien
  user/transkriptionen/export/        PDF- und MD-Exporte

SPRECHER-ZUORDNUNG:
  Vorab (Teilnehmer bekannt):
    Direkt als "A:", "B:", "Lukas:", "Dr. Mueller:" transkribieren.

  Nachtraeglich (unbekannte Sprecher):
    1. Mit SV1, SV2, ... transkribieren
    2. Charakteristika notieren
    3. User ordnet zu: "SV1 = ich, SV2 = Interviewer"
    4. bach transkript speaker-map fuehrt Bulk-Ersatz durch

EXTERNE TOOLS (via production-agent):
  Whisper (OpenAI)  Lokale Transkription mit Sprechertrennung
  Gemini 1.5 Pro    Direkte Audio-Transkription langer Dateien
  Descript          Professionelle Sprecher-Erkennung und Editing

DATENBANK:
  transcript_sessions   Sessions mit Datum, Titel, Quelle, Status
  transcript_speakers   Sprecher-Profile je Session
  transcript_segments   Zeitgestempelte Bloecke (optional)

STATUS:
  Konzept definiert (CONCEPT.md). CLI-Implementierung ausstehend (Phase 2).
  Basis-Ansatz: Forschungsprojekt/srt_to_transcript.py (SRT-Import)

SIEHE AUCH:
  bach help notizblock    Notizen und Notizbuecher
  bach help agents        Agenten-Uebersicht


## Trash

BACH Trash-Handler (Papierkorb-System)
======================================

Das Trash-System ermoeglicht Soft-Delete mit Wiederherstellung.

BEFEHLE
-------
bach trash list            Alle Papierkorb-Eintraege
bach trash delete PATH     Datei in Papierkorb
bach trash restore ID      Datei wiederherstellen
bach trash purge           Abgelaufene loeschen
bach trash info ID         Details anzeigen

OPTIONEN
--------
--dry-run    Aenderungen nur simulieren

BEISPIELE
---------
# Datei loeschen
bach trash delete ./alte_datei.txt

# Inhalt anzeigen
bach trash list

# Wiederherstellen
bach trash restore 5

# Abgelaufene bereinigen (30+ Tage)
bach trash purge --dry-run
bach trash purge

TECHNISCH
---------
- Handler: system/hub/trash.py
- Dateien werden nach system/data/trash/ verschoben
- Metadaten in DB-Tabelle: files_trash
- Standard-Aufbewahrung: 30 Tage (retention_days)
- Status: active, restored, purged

DATENBANK
---------
Tabelle: files_trash (system/db/schema.sql)
- id: PRIMARY KEY
- original_path: Urspruenglicher Pfad
- trash_path: Pfad im Papierkorb
- size: Dateigroesse in Bytes
- deleted_at: Loeschzeitpunkt (ISO-8601)
- deleted_by: Benutzername (default: "claude")
- retention_days: Aufbewahrung (default: 30)
- expires_at: Ablaufdatum (ISO-8601)
- status: active/restored/purged
- restored_at: Wiederherstellungszeitpunkt
- purged_at: Endgueltige Loeschung

SIEHE AUCH
----------
bach maintain help    Wartungs-Tools
bach backup help      Backup-System
bach trash help       Inline-Hilfe


## Upgrade

BACH UPGRADE - SYSTEM-AKTUALISIERUNG
=====================================

Aktualisiert BACH auf eine neuere Version. Unterstützt selektive
Upgrades nach Kategorien (SQ020).


VERWENDUNG
----------

  # Upgrade-Status anzeigen
  bach upgrade status

  # Verfügbare Updates anzeigen
  bach upgrade check

  # Vollständiges Upgrade durchführen
  bach upgrade --all

  # Selektives Upgrade nach Kategorie
  bach upgrade --category <kategorie>

  # Dry-Run (nur anzeigen, nicht ausführen)
  bach upgrade --dry-run


KATEGORIEN
----------

  core         System-Kern (hub/, tools/, core/)
  templates    Vorlagen und Templates
  agents       Boss-Agenten und Experten
  skills       Skills und Protokolle
  connectors   Connector-System
  partners     Partner-Dateien (claude/, gemini/, ollama/)
  docs         Dokumentation
  gui          GUI-Dateien


WICHTIG
-------

- Upgrade überschreibt NUR CORE + TEMPLATE Dateien
- USER_DATA bleibt unangetastet
- Backup wird empfohlen vor Upgrade
- Versionen werden in dist_file_versions getrackt


BEISPIELE
---------

  # Nur Core-Dateien aktualisieren
  bach upgrade --category core

  # Nur Templates aktualisieren
  bach upgrade --category templates

  # Prüfen welche Dateien aktualisiert würden
  bach upgrade --dry-run --category agents


VERSIONIERUNG
-------------

- Hash + Auto-Increment System (ENT-09)
- Nur CORE + TEMPLATE werden versioniert (dist_type 1+2)
- USER_DATA ist vom User und wird nicht versioniert


SIEHE AUCH
----------

  bach --help restore       Template-Wiederherstellung
  bach --help downgrade     Downgrade auf ältere Version
  bach --help seal          Integritätsprüfung


## Usecase

USECASES - Workflow-Testfaelle und TUeV-System
===============================================

BESCHREIBUNG
------------
Usecases sind Teil des BACH-TUeV-Systems und dienen als:
  1. FEATURE-TESTS        Validiert ein Workflow funktioniert?
  2. QUALITAETSSICHERUNG  Alle Komponenten spielen zusammen?
  3. ANFORDERUNGSNACHWEIS Was ist implementiert, was fehlt noch?

Usecases werden in der SQLite-DB gespeichert (Tabelle: usecases)
und sind mit Workflows verknuepft (workflow_tuev Tabelle).

Handler: system/hub/tuev.py (TuevHandler + UsecaseHandler)

USECASE-FORMAT
--------------

  USECASE_NNN: Kurztitel

  VORBEDINGUNG:  Was muss vorhanden sein?
  EINGABE:       Was gibt der User ein / welche Daten liegen vor?
  ERWARTUNG:     Was soll herauskommen?
  PRUEFT:        Welche Komponenten werden getestet?

AKTUELLE USECASES
-----------------
Usecases sind nun in der DB (usecases Tabelle).
Anzeigen mit: bach usecase list

Historische Usecase-IDs (aus altem Task-System):
  USECASE_001   Lebenslauf-Agent
  USECASE_002   Office Lens Scanner
  USECASE_003   Dokumenten-Suche
  USECASE_004   Arzt-Berichte Schilddruese
  USECASE_005   Haushalts-Routinen
  USECASE_006   Versicherungs-Beratung

Aktuelle Usecases in DB einsehen:
  bach usecase list
  bach db query "SELECT id, title, workflow_name, test_result FROM usecases"

USECASE ALS TEST
----------------
  Ein Usecase testet den kompletten Durchstich:

  User-Eingabe -> Agent/Skill -> Tools -> DB -> Ergebnis

  Damit werden automatisch validiert:
  - CLI-Befehle funktionieren?
  - DB-Schema korrekt?
  - Tools vorhanden und aufrufbar?
  - Help-Dateien aktuell?
  - Injektoren triggern bei Keywords?
  - Ergebnis nutzbar und korrekt?

USECASE ALS ANFORDERUNG
------------------------
  Fehlgeschlagene Usecases decken Luecken auf:
  - Fehlende Tools         -> Task fuer Tool-Erstellung
  - Fehlende CLI-Befehle   -> Task fuer CLI-Handler
  - Fehlende DB-Tabellen   -> Task fuer Schema-Erweiterung
  - Fehlende Workflows     -> Task fuer Workflow-Erstellung

  Neue Usecase-Ideen sind immer willkommen:
    bach task add "USECASE_NNN Kurztitel: Beschreibung" --prio P3

RUECKKOPPLUNG IN DEN ENTWICKLUNGSZYKLUS
-----------------------------------------

  Phase 8 (Usecases)
       │
       ├── Fehlgeschlagen? -> Neuer Task in Phase 1
       ├── Erfolgreich?    -> Feature validiert
       └── Neue Idee?      -> Neuer Usecase-Task

  Usecases sind Phase 8 im Dev-Zyklus (siehe: bach --help dev)

CLI-BEFEHLE
-----------

USECASE-VERWALTUNG:
  bach usecase list [workflow]       Alle Testfaelle (optional gefiltert)
  bach usecase add <workflow>        Hinweise zum Hinzufuegen (SQL-Template)
  bach usecase show <id>             Details eines Testfalls anzeigen
  bach usecase run <id>              Einzelnen Testfall ausfuehren
  bach usecase run-all <workflow>    Alle Tests eines Workflows

TUEV-VERWALTUNG:
  bach tuev status                   TUeV-Status aller Workflows
  bach tuev check <workflow>         Einzelnen Workflow pruefen
  bach tuev run                      Alle faelligen Pruefungen
  bach tuev renew <workflow>         TUeV erneuern nach Pruefung
  bach tuev init                     Workflows aus skills/workflows/ registrieren

USECASE ERSTELLEN
-----------------
Usecases werden direkt in die DB eingefuegt:

  bach db query "INSERT INTO usecases (title, description, workflow_name, test_input, expected_output, created_by) VALUES ('Testfall-Titel', 'Beschreibung', 'workflow-name', '{}', '{}', 'user')"

Oder via GUI: /usecases (wenn GUI-Server laeuft)

KOMPONENTEN-ABDECKUNG
---------------------
  Gute Usecases decken verschiedene Bereiche ab:

  Bereich         Beispiel-Usecase
  --------------- ------------------------------------------
  OCR & Dokumente USECASE_004 (Arzt-Berichte)
  Suche           USECASE_003 (Dokumenten-Suche)
  Generierung     USECASE_001 (Lebenslauf)
  Haushalt        USECASE_005 (Routinen)
  Finanzen        USECASE_006 (Versicherungen)
  Scanner         USECASE_002 (Office Lens)

  Noch nicht abgedeckt (Ideen):
  - Steuer-Workflow (End-to-End: Beleg -> Export)
  - Partner-Delegation (Claude -> Gemini -> Ergebnis)
  - Backup & Restore (Sicherung -> Wiederherstellung)
  - Multi-LLM Koordination

DATENBANK-STRUKTUR
------------------
  Tabelle: usecases
    - id, title, description
    - workflow_name, workflow_path
    - test_input (JSON), expected_output (JSON)
    - last_tested, test_result, test_score
    - created_by, created_at, updated_at

  Tabelle: workflow_tuev
    - workflow_name, workflow_path
    - tuev_status, last_tuev_date, tuev_valid_until
    - avg_score, test_count, pass_count

SIEHE AUCH
----------
  bach tuev status                          TUeV-Dashboard
  bach --help dev                           Entwicklungszyklus (8 Phasen)
  bach --help test                          Technische Testverfahren (B/O/E)
  system/skills/workflows/dev-zyklus.md    Detaillierter Dev-Workflow
  system/hub/tuev.py                        Handler-Implementierung
  system/db/schema.sql                      DB-Schema (usecases + workflow_tuev)

---
Version: 1.1.0 | Erstellt: 2026-01-28 | Aktualisiert: 2026-02-08


## Vendor

VENDOR - Externe Code-Quellen
==============================

STAND: 2026-02-06

BESCHREIBUNG
------------
Das _vendor/-Verzeichnis enthaelt Kopien von externem Code, der in
BACH-Services integriert wird. Jeder Vendor hat ein eigenes Verzeichnis
mit PROVENANCE.md (Herkunft, Commit, Lizenz).

SPEICHERORT
-----------
system/hub/_services/document/_vendor/

VERFUEGBARE VENDORS
-------------------

  anthropic_docx/     Word XML Pack/Unpack, Validate, Tracked Changes
                      Quelle: github.com/anthropics/skills (skills/docx)
                      Nutzen: Template-Debugging, Aenderungsverfolgung

  anthropic_pdf/      PDF-Formular-Extraktion, Ausfuellung, Konvertierung
                      Quelle: github.com/anthropics/skills (skills/pdf)
                      Nutzen: Steuer-Belege, Formular-Ausfuellung
                      Integration: pdf_service.py (PDFProcessor)

  anthropic_xlsx/     Excel Recalc, Office XML Pack/Unpack/Validate
                      Quelle: github.com/anthropics/skills (skills/xlsx)
                      Nutzen: Finanz-Exports mit Formeln

  redaction_detector.py   Regex+Fuzzy+Blacklist Erkennung sensibler Daten
                          Quelle: DokuZentrum

  pdf_schwaerzer_pro.py   PDF-Schwaerzung + AES-256 Encryption
                          Quelle: PDFSchwaerzer Pro

NUTZUNG IM CODE
---------------

  # PDF-Verarbeitung (empfohlen: ueber Service-Layer)
  from hub._services.document.pdf_service import PDFProcessor

  PDFProcessor.extract_text("datei.pdf")
  PDFProcessor.get_metadata("datei.pdf")
  PDFProcessor.extract_form_fields("datei.pdf")
  PDFProcessor.fill_form("datei.pdf", {"feld": "wert"}, "out.pdf")
  PDFProcessor.to_images("datei.pdf", "output_dir/")
  PDFProcessor.check_fillable("datei.pdf")

  # Vendor-Module direkt (nur wenn Service-Layer nicht reicht)
  import sys
  sys.path.insert(0, str(vendor_dir))
  from extract_form_structure import extract_form_structure

VENDOR-KONVENTIONEN
-------------------

  1. Jeder Vendor bekommt ein eigenes Verzeichnis
  2. PROVENANCE.md ist Pflicht (Quelle, Commit, Datum, Lizenz)
  3. __init__.py als Python-Package
  4. Keine Aenderungen am Vendor-Code (Verbatim Copy)
  5. Updates: Neuen Commit kopieren, PROVENANCE.md aktualisieren

VERWANDTE TOOLS
---------------

  tools/c_skill_init.py        Neuen Skill anlegen (Anthropic-Standard)
  tools/c_skill_validate.py    SKILL.md validieren
  tools/c_skill_package.py     Skill verpacken

SIEHE AUCH
----------
bach --help cookbooks          Anthropic Cookbooks Referenz
bach --help tools              Tool-Uebersicht
_vendor/README.md              Vendor-Uebersichtstabelle


## Versicherung

VERSICHERUNG - Versicherungsverwaltung
=======================================

BESCHREIBUNG:
  Verwaltung aller Versicherungspolicen mit Fristen, Kuendigungsterminen
  und Beitraegen. Daten liegen in bach.db/fin_insurances.
  GUI-Zugriff ueber das Finanz-Modul (Versicherungen-Tab).

STATUS:
  Vollstaendiger CLI-Handler implementiert in hub/versicherung.py
  - CLI: bach versicherung <operation> (list, show, add, edit, delete, status, fristen, check, claim)
  - GUI: Finanz-Modul > Versicherungen (CRUD von Gemini implementiert)
  - Direkte DB-Abfrage (fuer Agents/Experten)

DATENBANK:
  Tabellen:
    - bach.db / fin_insurances (Versicherungen)
    - bach.db / fin_insurance_claims (Schadenfaelle)
    - bach.db / insurance_types (Referenzdaten, optional)

  Felder fin_insurances:
    id                       Auto-ID
    anbieter                 Versicherungsgesellschaft (Allianz, HUK, AXA, ...)
    tarif_name               Tarifbezeichnung
    police_nr                Policennummer (UNIQUE)
    sparte                   Haftpflicht, BU, KFZ, Hausrat, Rechtsschutz, ...
    status                   aktiv | gekuendigt | beitragsfrei | ruhend
    beginn_datum             Vertragsbeginn
    ablauf_datum             Vertragsende
    kuendigungsfrist_monate  Kuendigungsfrist in Monaten (Default: 3)
    verlaengerung_monate     Auto-Verlaengerung (Default: 12)
    naechste_kuendigung      Naechster Kuendigungstermin
    beitrag                  Beitrag als Betrag
    zahlweise                monatlich | quartalsweise | halbjaehrlich | jaehrlich
    steuer_relevant_typ      Vorsorgeaufwendungen etc.
    ordner_pfad              Pfad zu Scans/Dokumenten auf Dateisystem
    notizen                  Freitext
    created_at, updated_at   Timestamps

VERKNUEPFUNGEN:
  - financial_emails: E-Mails von Versicherungen (category = 'versicherung')
  - ordner_pfad: Echte Dokumente unter C:\Users\User\OneDrive\Dokumente\_Versicherungen&Finanzen\
  - user_data_folders: Registrierter Ordner 'user/versicherungen'

AKTUELLE DATEN:
  13 Versicherungen importiert (Stand: Session 2026-01-28)
  Sparten: Haftpflicht, BU, KFZ, Hausrat, Rechtsschutz, Zahnzusatz,
           PKV, Unfallversicherung, Auslandskrankenversicherung, u.a.

CLI-BEFEHLE:
  bach versicherung list                    Alle aktiven Versicherungen
  bach versicherung list --all              Inkl. gekuendigte
  bach versicherung list --sparte <sparte>  Nach Sparte filtern
  bach versicherung list --status <status>  Nach Status filtern

  bach versicherung show <id>               Details anzeigen

  bach versicherung add --anbieter "X" --sparte "Y" [Optionen]
    Pflicht: --anbieter, --sparte
    Optionen: --beitrag, --zahlweise, --police, --tarif, --beginn,
              --ablauf, --kuendigung, --frist, --steuer, --ordner, --note

  bach versicherung edit <id> [Felder]      Versicherung bearbeiten
  bach versicherung delete <id>             Status -> gekuendigt setzen

  bach versicherung status                  Dashboard mit Statistiken
  bach versicherung fristen [--tage N]      Kuendigungsfristen anzeigen (Default: 90 Tage)
  bach versicherung check                   Portfolio-Analyse

  bach versicherung claim add <id> --datum DD.MM.YYYY --beschreibung "Text" [--betrag X]
  bach versicherung claim list [<id>]       Schadenfaelle anzeigen

  bach versicherung help                    Hilfe anzeigen

GEPLANT:
  - Automatischer E-Mail-Abgleich mit financial_emails
  - Steuer-Export-Integration (aktuell: manuelle Steuer-Typ-Verwaltung)

ZUSAMMENSPIEL:
  - GUI: Finanz-Dashboard mit Fristen-Warnung (#575)
  - GUI: Versicherungen CRUD (#570)
  - Steuer-Export: #572 (geplant)


## Wartung

BACH WARTUNG (System-Jobs)
==========================

Der Wartungs-Handler fuehrt automatisch geplante System-Jobs aus - z.B. Backups,
Token-Checks, Datenbereinigung oder eigene Scripts.

HANDLER:  system/hub/daemon.py
SERVICE:  system/gui/daemon_service.py + DB (daemon_jobs, daemon_runs)
GUI:      /daemon (http://localhost:8000/daemon)


BEFEHLE
-------

  bach daemon start          Wartungs-Daemon im Vordergrund starten (Ctrl+C beendet)
  bach daemon start --bg     Wartungs-Daemon im Hintergrund starten
  bach daemon stop           Laufenden Daemon stoppen
  bach daemon status         Status und letzte Laeufe anzeigen
  bach daemon jobs           Alle definierten Jobs auflisten
  bach daemon run <ID>       Job manuell ausfuehren
  bach daemon logs [N]       Letzte N Log-Zeilen anzeigen (Standard: 20)


SESSION-BEFEHLE (Session-Daemon fuer automatische Claude-Sessions)
------------------------------------------------------------------

  bach daemon session start [--profile NAME]   Session-Daemon starten
  bach daemon session stop                     Session-Daemon stoppen
  bach daemon session status                   Session-Status anzeigen
  bach daemon session trigger [--profile NAME] Session manuell ausloesen
  bach daemon session profiles                 Verfuegbare Profile auflisten


JOB-TYPEN
---------

  interval    Periodisch (z.B. "30m", "1h", "24h")
  cron        Cron-Ausdruck (z.B. "0 3 * * *" = taeglich 03:00)
  manual      Nur manuell ausfuehrbar
  chain       Chain-Ausfuehrung (job.command = chain_id)
  event       Event-basiert (TODO)


BEISPIEL-JOBS
-------------

  Name           Typ        Schedule    Beschreibung
  ----------------------------------------------------------------
  backup-daily   interval   24h         Taegliches Backup erstellen
  token-check    interval   30m         Token-Verbrauch pruefen
  cleanup        cron       0 4 * * *   Alte Logs bereinigen


JOBS ERSTELLEN
--------------

Via GUI-Dashboard (http://localhost:8000/daemon):
  - Wartung > "Neuer Job"

Via API:
  POST /api/daemon/jobs
  {
    "name": "mein-job",
    "job_type": "interval",
    "schedule": "1h",
    "command": "python tools/mein_script.py"
  }


LOG-DATEIEN
-----------

  data/logs/daemon.log                     Wartungs-Aktivitaeten
  data/logs/session_daemon.log             Session-Aktivitaeten
  data/daemon.pid                          PID-Datei (wenn laufend)
  hub/_services/daemon/daemon.pid          Session-Daemon PID


TECHNISCHE DETAILS
------------------

- Jobs werden aus bach.db geladen (Tabelle: daemon_jobs)
- Ausfuehrungen in daemon_runs protokolliert
- Timeout pro Job konfigurierbar (Standard: 300s)
- Bei Fehler optional Retry (max_retries konfigurierbar)
- Alle 5 Minuten werden Jobs neu geladen
- EIGENER DAEMON-PROZESS (Python Interval-Loop)
- OneDrive wird waehrend Daemon-Betrieb pausiert (Windows)
- Verhindert Sync-Konflikte bei Datei-Operationen
- Integration mit Recurring Tasks (Check alle 5 Min)

Optional: pip install croniter (fuer erweiterte Cron-Ausdruecke)


ABGRENZUNG: DREI HANDLER-SYSTEME
--------------------------------

  ┌─────────────────────────────────────────────────────────────────┐
  │  WARTUNG                                                        │
  ├─────────────────────────────────────────────────────────────────┤
  │  Fuehrt Shell/Python-Befehle AUS                                │
  │  Zeitgesteuert (cron/interval)                                  │
  │  Ohne Claude-Beteiligung                                        │
  │  Handler:  system/hub/daemon.py                                  │
  │  Service:  system/gui/daemon_service.py + DB                    │
  │  GUI:      /daemon (vorhanden)                                  │
  │  Daemon:   JA (eigener Prozess)                                 │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │  RECURRING                                                      │
  ├─────────────────────────────────────────────────────────────────┤
  │  Erstellt TASKS als Erinnerungen                                │
  │  Intervall-basiert (Tage)                                       │
  │  Fuer Claude/User zur Bearbeitung                               │
  │  Handler:  system/hub/recurring.py                              │
  │  Service:  system/hub/_services/recurring/                      │
  │  GUI:      KEINE (nur CLI + in /daemon integriert)              │
  │  Daemon:   NEIN (Check bei Aufruf)                              │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │  PROMPT-GENERATOR                                               │
  ├─────────────────────────────────────────────────────────────────┤
  │  Sendet Prompts an Claude-Sessions                              │
  │  Manuell oder automatisiert                                     │
  │  Vorlagen-System mit Editor                                     │
  │  Handler:  (in Entwicklung)                                     │
  │  Service:  system/hub/_services/prompt_generator/                │
  │  GUI:      /prompt-generator (geplant)                          │
  │  Daemon:   JA (session_daemon.py)                               │
  └─────────────────────────────────────────────────────────────────┘

  Beispiel Wartung:          "bach backup create" taeglich um 03:00
  Beispiel Recurring:        "Self-Check faellig" -> Task fuer Claude
  Beispiel Prompt-Generator: Prompt alle 30 Min an ATI Agent senden


SIEHE AUCH
----------

  bach gui start              Web-Dashboard mit Job-Verwaltung
  bach --help backup          Backup-System
  bach --help dirscan            Directory Scanner
  bach --help recurring       Wiederkehrende Tasks (keine GUI)
  bach --help prompt-generator  Prompt-Management (GUI geplant)


## Watcher

WATCHER - Mistral Always-On Daemon
====================================

BESCHREIBUNG
------------
Der Watcher-Daemon macht BACH "always-on" - inspiriert von OpenClaw/molt.bot.
Mistral (lokal via Ollama, kostenlos) laeuft dauerhaft im Hintergrund und
klassifiziert eingehende Events. Bei Bedarf startet er Claude Code Sessions.

ARCHITEKTUR
-----------
                    Watcher Daemon (always-on)
                    |
    +---------------+---------------+
    |               |               |
  Connector     FileSystem      TaskQueue
  (Telegram,    (Inbox,         (Neue/dringende
   Discord)     Downloads)       BACH Tasks)
    |               |               |
    +-------+-------+-------+------+
            |
            v
     MistralClassifier
     (OllamaClient -> Mistral:latest)
            |
  +---------+---------+----------+
  |         |         |          |
RESPOND   ESCALATE  LOG_ONLY  IGNORE
DIRECT    CLAUDE
  |         |         |
  v         v         v
Antwort   Claude    Event-
via       Session   Log
Connector  starten

BEFEHLE
-------
  bach watcher start              Daemon im Hintergrund starten
  bach watcher stop               Daemon stoppen
  bach watcher status             Status, Events, Statistiken
  bach watcher classify "text"    Text manuell klassifizieren (Test)
  bach watcher logs [N]           Letzte N Log-Zeilen
  bach watcher events [N]         Letzte N klassifizierte Events

KLASSIFIKATION
--------------
Mistral klassifiziert jeden Event in eine von 4 Aktionen:

  Aktion           Beschreibung                          Beispiel
  ---------------  -----------------------------------   -------------------------
  RESPOND_DIRECT   Mistral antwortet selbst              "Wie gehts?" -> "Gut!"
  ESCALATE_CLAUDE  Claude-Session wird gestartet          "Refactore den Handler"
  LOG_ONLY         Nur loggen, keine Aktion               "Backup abgeschlossen"
  IGNORE           Verwerfen                              Spam, Werbung

EVENT SOURCES
-------------
  connector_messages   Telegram/Discord Nachrichten (via Connector-System)
  filesystem           Neue Dateien in ueberwachten Ordnern
  task_queue           Neue/dringende BACH Tasks (P1/P2)
  scheduled            Zeitplan-basierte Events (Cron)

SICHERHEITS-GUARDS
------------------
- Cooldown: Min. 5 Minuten zwischen Claude-Escalations
- Tages-Limit: Max 20 Escalations pro Tag
- Claude-Check: Keine Escalation wenn Claude bereits online
- Screen-Lock: Keine Escalation bei gesperrtem Bildschirm
- Quiet Hours: Konfigurierbar (Standard: 23:00-07:00)

KONFIGURATION
-------------
Datei: hub/_services/watcher/config.json

Wichtige Einstellungen:
  enabled                    Daemon an/aus
  poll_interval_seconds      Polling-Intervall (Standard: 15s)
  quiet_start/quiet_end      Ruhezeiten
  mistral_model              Ollama-Modell (Standard: Mistral:latest)
  escalation_cooldown_seconds  Min. Zeit zwischen Escalations
  max_daily_escalations      Max Escalations pro Tag
  sources.*                  Event-Quellen aktivieren/deaktivieren

VORAUSSETZUNGEN
---------------
- Ollama installiert und gestartet
- Mistral-Modell geladen (ollama pull mistral)
- Connector-System konfiguriert (fuer Message-Quellen)

DATENBANK
---------
  connector_messages.watcher_classified  Tracking ob Watcher Nachricht gesehen hat
  watcher_event_log                     Alle klassifizierten Events mit Ergebnis

LOG-DATEIEN
-----------
  data/logs/watcher_daemon.log          Daemon-Aktivitaet und Klassifikationen

SIEHE AUCH
----------
  bach help connector     Connector-System (Telegram/Discord)
  bach help partners      Partner-System
  bach help daemon        Session-Daemon
  bach help injectors     Injektor-System


## Workflow Tuev

WORKFLOW-TUEV - Qualitaetssicherung fuer Workflows
==================================================

Workflows sind das "Gehirn" des Systems. Sie muessen zuverlaessig funktionieren.
Der Workflow-TUeV stellt sicher, dass Workflows regelmaeßig getestet werden.

KONZEPT
-------

1. USECASE-TESTS
   - Sammlung von Testfaellen pro Workflow
   - Definierte Eingaben und erwartete Ausgaben
   - Automatische Durchfuehrung moeglich

2. TUEV-ABLAUF
   - Jeder Workflow hat ein Ablaufdatum (tuev_valid_until)
   - Bei Ablauf: Automatisch Wartungs-Task erstellen
   - Nach erfolgreicher Pruefung: Neues Ablaufdatum

3. BEWERTUNG
   - sehr gut (90-100%)
   - gut (70-89%)
   - befriedigend (50-69%)
   - ausreichend (30-49%)
   - durchgefallen (<30%)
   - Note bestimmt Prioritaet der Wartungs-Tasks

CLI-BEFEHLE
-----------

BACH TUEV:
  bach tuev status                    TUeV-Status aller Workflows
  bach tuev check <workflow>          Einzelnen Workflow pruefen
  bach tuev run                       Alle faelligen Pruefungen
  bach tuev renew <workflow>          TUeV erneuern nach Pruefung
  bach tuev init                      Workflows in DB registrieren

BACH USECASE:
  bach usecase list [workflow]        Testfaelle anzeigen
  bach usecase add <workflow>         Neuen Testfall hinzufuegen
  bach usecase run <id>               Testfall ausfuehren
  bach usecase run-all <workflow>     Alle Testfaelle eines Workflows
  bach usecase show <id>              Testfall-Details anzeigen

DB-SCHEMA
---------

usecases:
  id                   Primaerschluessel
  title                Testfall-Titel
  description          Beschreibung des Testfalls
  workflow_path        Pfad zum Workflow (skills/workflows/...)
  workflow_name        Name des Workflows
  test_input           JSON: Eingabedaten fuer Test
  expected_output      JSON: Erwartetes Ergebnis
  last_tested          Letzter Testlauf (Zeitstempel)
  test_result          pass/fail/error
  test_score           Punktzahl 0-100
  tuev_valid_until     Ablaufdatum dieses Testfalls
  created_by           user/system

workflow_tuev:
  id                   Primaerschluessel
  workflow_path        Pfad zum Workflow (UNIQUE)
  workflow_name        Name des Workflows
  last_tuev_date       Letzter TUeV-Termin
  tuev_valid_until     Naechster TUeV faellig
  tuev_status          pending/passed/failed/expired
  test_count           Anzahl durchgefuehrter Tests
  pass_count           Bestandene Tests
  fail_count           Fehlgeschlagene Tests
  avg_score            Durchschnittliche Punktzahl

TESTPROZESS (3 Teile)
---------------------

Teil 1: DURCHFUEHRUNG als Selbsterfahrung
  - Workflow mit Testdaten ausfuehren
  - LLM-Perspektive: "Wie war es fuer mich?"
  - Probleme, Unklarheiten, Stolpersteine notieren

Teil 2: BEWERTUNG gegen Kriterien
  - Usecase-Anforderungen pruefen
  - Festgelegte Kriterien abgleichen
  - Ergebnis vs. Expected Output vergleichen

Teil 3: BENOTUNG und Konsequenzen
  - Score berechnen (0-100)
  - Note ableiten
  - Bei Fehler: Task zur Verbesserung erstellen

CHECKLISTE fuer neue Workflows
------------------------------

[ ] Hat der Workflow mindestens 1 Usecase?
[ ] Sind Eingabe und erwartete Ausgabe definiert?
[ ] Funktioniert der Workflow ohne User-Daten?
[ ] Ist der Workflow idempotent (wiederholbar)?
[ ] Sind Abhaengigkeiten dokumentiert?
[ ] Gibt es Error-Handling?

BEISPIEL-USECASE
----------------

  Workflow: bugfix-protokoll

  Testfall: "Einfacher Syntaxfehler"
  test_input: {
    "bug_description": "SyntaxError in main.py Zeile 42",
    "file_path": "tests/sample_bug.py"
  }
  expected_output: {
    "status": "fixed",
    "changes_made": true,
    "test_passed": true
  }

AUTOMATISIERUNG
---------------

Daemon-Job (geplant):
  Name: tuev-check
  Befehl: bach tuev run
  Intervall: 7d (woechentlich)

Bei abgelaufenem TUeV:
  -> Task "Workflow X TUeV erneuern" erstellt (Prio basierend auf Score)

SIEHE AUCH
----------

  --help workflows     Workflow-System
  --help usecase       Usecase-Tests Details
  --help core          Kern-Konzept (Agent/Workflow/Skills)
  --help dev           Entwicklungs-Workflow

---
Version: 1.1 | Erstellt: 2026-01-30
Status: Implementiert (v1.1.83)
Handler: system/hub/tuev.py (TuevHandler + UsecaseHandler)


## Workflow

WORKFLOW - BACH Arbeitsablaeufe
================================

BESCHREIBUNG
------------
Workflows beschreiben WANN man WELCHEN Skill in WELCHER Reihenfolge einsetzt.
Ein Workflow ist eine Anleitung zum strategischen Einsatz von Skills.

WORKFLOW-SPEICHERORT
--------------------
  skills/workflows/          Alle BACH Workflows (22 .md Dateien)
  agents/_experts/steuer/     Steuer-Workflows (7 .md Dateien)
  DB: skills-Tabelle          type='workflow' (automatisch synchronisiert)

VERFUEGBARE WORKFLOWS
---------------------
  System-Workflows (10):
  ----------------------
  bugfix-protokoll.md            Fehlerkorrektur-Prozess
  cli-aenderung-checkliste.md    CLI-Befehl hinzufuegen
  dev-zyklus.md                  Entwicklungszyklus (8 Phasen)
  ordner-flattening.md           Ordner-Struktur abflachen
  projekt-aufnahme.md            Neues Projekt aufnehmen
  service-agent-validator.md     Service/Agent Validator
  system-anschlussanalyse.md     Integrations-Check
  system-aufraeumen.md           Aufraeumen und Archivieren
  system-mapping.md              System kartieren
  system-synopse.md              System-Uebersicht erstellen
  system-testverfahren.md        Test-Prozeduren

  Dokumentations-Workflows (4):
  -----------------------------
  docs-analyse.md                Dokumentations-Analyse
  help-forensic.md               Help Ist-Soll Pruefung (Recurring: 14d)
  wiki-author.md                 Wiki-Beitraege erstellen (Recurring: 21d)
  migrate-rename.md              Datei-Umbenennung mit Wrapper

  Partner-Workflows (2):
  ----------------------
  gemini-delegation.md           Aufgaben an Gemini delegieren
  google-drive.md                Google Drive Nutzung

  Analyse-Workflows (4):
  ----------------------
  agent-skill-finder.md          Agent-Skill Mapping Analyse
  skill-abdeckungsanalyse.md     Skill-Coverage pruefen
  synthese.md                    Dokumente zusammenfuehren
  ing-strategie.md               ING Banking Workflow

  Persoenliche-Workflows (1):
  ---------------------------
  cv-generierung.md              Lebenslauf erstellen/aktualisieren

  Steuer-Workflows (7):
  ---------------------
  HINWEIS: Diese Workflows liegen in agents/_experts/steuer/

  steuer-beleg-scan.md                  Belege scannen und erfassen
  steuer-fahrtkosten-homeoffice.md      Fahrtkosten + Homeoffice berechnen
  steuer-finanzamt-export.md            Finanzamt-Export erstellen
  steuer-sonderausgaben-erfassen.md     Sonderausgaben erfassen
  steuer-telekommunikation-eigenbeleg.md Internet/Telefon 20% Pauschale
  steuer-versicherungen-erfassen.md     Versicherungen steuerlich erfassen
  steuer-werbungskosten-erfassen.md     Werbungskosten erfassen

WANN WELCHEN WORKFLOW
---------------------
  Bug gefunden?           -> bugfix-protokoll.md
  Neuer CLI-Befehl?       -> cli-aenderung-checkliste.md
  Neues Projekt?          -> projekt-aufnahme.md
  System analysieren?     -> system-mapping.md oder system-synopse.md
  Aufraeumen?             -> system-aufraeumen.md
  Integration pruefen?    -> system-anschlussanalyse.md
  Gemini nutzen?          -> gemini-delegation.md
  Help pruefen?           -> help-forensic.md (Recurring: 14d)
  Wiki erweitern?         -> wiki-author.md (Recurring: 21d)
  Datei umbenennen?       -> migrate-rename.md
  Ordner vereinfachen?    -> ordner-flattening.md
  Fahrtkosten/Homeoffice? -> steuer-fahrtkosten-homeoffice.md
  Belege scannen?         -> steuer-beleg-scan.md
  Werbungskosten?         -> steuer-werbungskosten-erfassen.md
  Sonderausgaben?         -> steuer-sonderausgaben-erfassen.md
  Versicherungen Steuer?  -> steuer-versicherungen-erfassen.md
  Internet/Telefon?       -> steuer-telekommunikation-eigenbeleg.md
  Finanzamt Export?       -> steuer-finanzamt-export.md
  Entwicklungszyklus?     -> dev-zyklus.md (8 Phasen)

STANDARD SESSION-WORKFLOW
-------------------------
1. bach startup                # Session starten (Standard: GUI-Mode)
2. ROADMAP.md lesen            # Aufgabe waehlen
3. Aufgabe bearbeiten
4. Zwischen-Tasks: bach status # Zeit pruefen
5. bach shutdown               # Session beenden

SESSION TIMING
--------------
  Timeout-Schutz:  Claude kann nach ~13 Min abbrechen
  Empfehlung:      Alle 10 Min kurzen Status dokumentieren
  Bei langen Tasks: bach memory session "STATUS: ..."

AUFGABENGROESSE
---------------
  <5 Min     Einfach erledigen
  ~15 Min    Memory aktuell halten
  >30 Min    Vorstrukturieren (Teilaufgaben erstellen)
  >1h        Als Planungsaufgabe aufnehmen

ABGRENZUNG: WORKFLOW vs TEAM-FLOW
---------------------------------
  ┌────────────────────────────┬────────────────────────────────┐
  │  WORKFLOW                  │  TEAM-FLOW (geplant)           │
  ├────────────────────────────┼────────────────────────────────┤
  │  EIN Akteur                │  MEHRERE Akteure               │
  │  Schritt-Anleitung         │  Uebergabe-Management          │
  │  Text in .md Datei         │  Strukturiert in DB/JSON       │
  │  skills/workflows/        │  GUI Skills-Board (geplant)    │
  └────────────────────────────┴────────────────────────────────┘

CLI-BEFEHLE
-----------
  bach help workflow           Diese Hilfe
  bach help between-tasks      Zwischen-Task-Checks
  bach help startup            Session-Start
  bach help shutdown           Session-Ende

  bach startup                 Session starten (Default: GUI)
  bach startup quick           Schnellstart ohne Dir-Scan
  bach startup mode            Modus aendern: gui|text|dual|silent

  bach status                  Systemstatus anzeigen

  bach shutdown                Session beenden (mit Dir-Scan)
  bach shutdown quick          Schnell ohne Dir-Scan
  bach shutdown emergency      Notfall - nur Working Memory sichern

WORKFLOW LESEN
--------------
  # Direkt im File-System:
  skills/workflows/<name>.md
  agents/_experts/steuer/<name>.md

  # Mit Help-System (Alias-Unterstuetzung):
  bach help workflow/bugfix-protokoll
  bach help workflow/help-forensic

  # Im Chat-Client:
  Read-Tool: skills/workflows/bugfix-protokoll.md

NEUEN WORKFLOW ERSTELLEN
------------------------
1. Datei anlegen: skills/workflows/mein-workflow.md
2. Format beachten:
   - Titel mit #
   - Schritte nummeriert
   - Bedingungen klar formuliert
   - Referenzen auf andere Workflows/Skills

SIEHE AUCH
----------
  bach help tasks              Task-System
  bach help maintain           Wartungs-Tools
  bach help startup            Session-Start Protokoll
  bach help skills             Skills-System
  docs/con4_CONCEPT_Skill_Architecture_v2_70.md  Skill-Architektur


---

# BACH Tools Referenz

*81 Tool-Dokumentationen*


## Agent Cli

BACH Tool: agent_cli
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/agent_cli.py

BESCHREIBUNG
----------------------------------------
BACH Agent CLI v1.0.0
=====================

CLI-Tool zur Verwaltung von BACH Agenten und Experten.

Features:
- Agenten auflisten und aktivieren
- Experten anzeigen
- User-Ordner initialisieren
- Datenbank-Schema anwenden

Usage:
    python agent_cli.py list                    # Alle Agenten
    python agent_cli.py experts                 # Alle Experten
    python agent_cli.py info <agent>            # Agent-Details
    python agent_cli.py init <agent>            # User-Ordner erstellen
    python agent_cli.py setup-db                # Datenbank initialisieren
    python agent_cli.py status                  # System-Status

Autor: BACH System
Datum: 2026-01-20

VERWENDUNG
----------------------------------------
python bach.py tools run agent_cli [args]
oder direkt: python tools/agent_cli.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show agent_cli


## Agent Framework

BACH Tool: agent_framework
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/agent_framework.py

BESCHREIBUNG
----------------------------------------
Agent Framework v1.0.0

Zentrales Framework für RecludOS Agenten.
Verbindet Agents mit Services, externen Tools und Connections.

Features:
- Agent-Loader und Registry-Verwaltung
- Service-Integration (scheduling, media, mail, etc.)
- Externe KI-Tool-Empfehlungen
- Connection-Management (MCP, APIs, CLIs)

Usage:
  python agent_framework.py list                    # Alle Agenten
  python agent_framework.py info <agent>            # Agent-Details
  python agent_framework.py tools <agent>           # Empfohlene Tools
  python agent_framework.py services <agent>        # Verknüpfte Services
  python agent_framework.py activate <agent>        # Agent aktivieren

VERWENDUNG
----------------------------------------
python bach.py tools run agent_framework [args]
oder direkt: python tools/agent_framework.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show agent_framework


## Agent Service Integration

BACH Tool: agent_service_integration
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/agent_service_integration.py

BESCHREIBUNG
----------------------------------------
Agent-Service-Connection Integration v2.0.0 (DB-Version)

Verknüpft Agenten mit Services, Connections und externen Tools.
Zentrale Anlaufstelle für Agent-Aktivierung und Tool-Routing.

GEÄNDERT: Liest jetzt aus bach.db statt JSON-Dateien!

Usage:
  python agent_service_integration.py matrix           # Zeige Verbindungsmatrix
  python agent_service_integration.py agent <name>     # Agent-Verbindungen
  python agent_service_integration.py recommend <task> # Tool-Empfehlung
  python agent_service_integration.py status           # Gesamtstatus
  python agent_service_integration.py tools [type]     # Tools auflisten
  python agent_service_integration.py connections      # Connections auflisten

VERWENDUNG
----------------------------------------
python bach.py tools run agent_service_integration [args]
oder direkt: python tools/agent_service_integration.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show agent_service_integration


## Agents

AGENT TOOLS - Agenten-Werkzeuge
================================

UEBERSICHT
Agent-Tools in BACH verwalten und steuern AI-Agenten
und deren Interaktionen.

AGENT FRAMEWORK
---------------
agent_framework.py

Kern-Framework fuer alle BACH-Agenten.
Features:
  - Agent-Registrierung
  - Capability-Matching
  - Synergie-Management

Aufruf: Wird intern verwendet

AGENT CLI
---------
agent_cli.py

Kommandozeile fuer Agent-Interaktion.
Befehle:
  - list: Alle Agenten anzeigen
  - status: Agent-Status pruefen
  - activate: Agent aktivieren
  - deactivate: Agent deaktivieren

Aufruf: python tools/agent_cli.py <befehl>

AGENT SERVICE INTEGRATION
-------------------------
agent_service_integration.py

Verbindet Agenten mit BACH-Services.
Ermoeglicht:
  - Service-Discovery
  - Automatische Routing
  - Load-Balancing

VERFUEGBARE AGENTEN
-------------------

Verzeichnis: agents/

  ati/              Software-Entwickler (ATI)
  steuer-agent.txt  Steuer-Assistent
  research.txt      Research-Agent (Recherche)
  entwickler.txt    Allgemeiner Entwickler
  production.txt    Produktions-Agent
  foerderplaner/    Foerderplan-Assistent

AGENT-KONVENTION
----------------

Siehe: skills/AGENT_KONVENTION.md

Hierarchie:
  BOSS-Agenten:   Vollstaendige Kontrolle, langfristig
  Experts:        Spezialisiert, kurzfristig
  Services:       Automatische Hintergrund-Tasks

AGENT-BEFEHLE IN BACH
---------------------

  bach --help agents       Agent-Dokumentation
  bach --help ati          ATI-Agent Hilfe
  bach ati bootstrap       Projekt erstellen (ATI)
  bach ati migrate         Projekt migrieren (ATI)

DELEGATION AN AGENTEN
---------------------

  bach delegate "task" --to=<agent>

Verfuegbare Ziele:
  ollama, gemini, copilot, perplexity, human

ENTWICKLER-AGENT
----------------
entwickler_agent.py

Spezialisierter Agent fuer Entwicklungs-Aufgaben.
Kann:
  - Code generieren
  - Bugs analysieren
  - Tests erstellen

PRODUCTION-AGENT
----------------
production_agent.py

Fuer Produktions-Deployments.
Features:
  - Build-Prozesse
  - Deployment-Checks
  - Rollback-Support

RESEARCH-AGENT
--------------
research_agent.py

Recherche und Informationssammlung.
Quellen:
  - Web-Search
  - Dokumentation
  - Interne Wissensbasis

SIEHE AUCH
----------
bach --help delegate      Delegation-System
bach --help partner       Partner-Kommunikation
skills/AGENT_KONVENTION.md  Agent-Richtlinien


## Analysis

ANALYSIS TOOLS - Analyse-Werkzeuge
===================================

UEBERSICHT
Die Analysis-Tools in BACH helfen bei der Datenanalyse,
Code-Inspektion und Systemueberwachung.

DATEN-ANALYSE (bach data)
-------------------------
Pfad: hub/data_analysis.py
Status: Implementiert (v1.1.25)

Befehle:
  bach data load <pfad>         Datei laden und Info anzeigen
  bach data describe <pfad>     Deskriptive Statistik (mean, std, min, max)
  bach data head <pfad> [--rows N]  Erste N Zeilen (Standard: 10)
  bach data corr <pfad>         Korrelationsmatrix numerischer Spalten
  bach data chart <pfad> <typ>  Chart erstellen (bar, line, pie, scatter, hist)
  bach data list                Dateien im input/ Ordner anzeigen

Unterstuetzte Formate:
  - CSV (automatische Trennzeichen-Erkennung)
  - Excel (.xlsx, .xls)
  - JSON

Verzeichnisse:
  user/data-analysis/input/     Eingabe-Dateien
  user/data-analysis/output/    Ergebnis-Dateien
  user/data-analysis/charts/    Generierte Charts

CODE-ANALYSE
------------

code_analyzer.py
  Analysiert Python-Code auf Qualitaet und Struktur.
  Aufruf: python tools/code_analyzer.py <datei>

c_method_analyzer.py
  Analysiert Methoden und Funktionen in Python-Dateien.
  Findet lange Methoden, komplexe Funktionen.
  Aufruf: python tools/c_method_analyzer.py <datei>

STATISTIK & REPORTS
-------------------

task_statistics.py
  Erstellt Statistiken ueber Tasks (done vs pending, Prioritaeten).
  Aufruf: python tools/task_statistics.py

reports.py
  Generiert verschiedene System-Reports.
  Aufruf: python tools/reports.py

generate_skills_report.py
  Erstellt Skill-Abdeckungs-Report.
  Aufruf: python tools/generate_skills_report.py

SCANNER
-------

dirscan.py
  Scannt Verzeichnisse auf Aenderungen.
  In --startup integriert.
  Aufruf: python tools/dirscan.py <pfad>

tool_scanner.py
  Findet und registriert Tools im System.
  Aufruf: python tools/tool_scanner.py

duplicate_detector.py
  Findet doppelte Dateien nach Hash.
  Aufruf: python tools/duplicate_detector.py <pfad>

SYSTEM-INSPEKTION
-----------------

c_sqlite_viewer.py
  Inspiziert SQLite-Datenbanken (bach.db, bach.db).
  Aufruf: python tools/c_sqlite_viewer.py <db>

inspect_db_tables.py
  Zeigt Tabellen-Schema und Statistiken.
  Aufruf: python tools/inspect_db_tables.py

dump_schema.py
  Exportiert DB-Schema als SQL.
  Aufruf: python tools/dump_schema.py

SIEHE AUCH
----------
bach --help data          Data Analysis Hilfe
bach --help tools         Tool-Uebersicht
bach --help maintain      Wartungs-Tools


## Archive Done Tasks

BACH Tool: archive_done_tasks
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/archive_done_tasks.py

BESCHREIBUNG
----------------------------------------
archive_done_tasks.py - Verschiebt done-Tasks aus tasks.json nach _done.json

Verwendung:
    python archive_done_tasks.py          # Dry-run (zeigt was passieren würde)
    python archive_done_tasks.py --apply  # Wirklich ausführen

VERWENDUNG
----------------------------------------
python bach.py tools run archive_done_tasks [args]
oder direkt: python tools/archive_done_tasks.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show archive_done_tasks


## Autolog

BACH Tool: autolog
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/autolog.py

BESCHREIBUNG
----------------------------------------
Auto-Logger - Protokolliert automatisch alle Aktionen
=====================================================

Zweistufiges System:
1. auto_log.txt        - Letzte 300 Zeilen (Kurzzeitgedaechtnis)
2. auto_log_extended.txt - Aeltere Eintraege, max 30 Tage (Archiv)

Nach 30 Tagen werden Eintraege endgueltig geloescht.

VERWENDUNG
----------------------------------------
python bach.py tools run autolog [args]
oder direkt: python tools/autolog.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show autolog


## Backup

BACKUP TOOLS - Datensicherung und Wiederherstellung
===================================================

Stand: 2026-01-23
Pfad: docs/docs/docs/help/tools/backup.txt

BESCHREIBUNG
------------
Tools zur Datensicherung und Wiederherstellung von BACH-Daten:
  - Lokale Backups erstellen und verwalten
  - NAS-Backups (wenn verfuegbar)
  - Template-Restore (Originaldateien zuruecksetzen)
  - Distribution-Pakete erstellen

HAUPT-TOOL: backup_manager.py
=============================
Zentrales Tool fuer alle Backup-Operationen.
Kann direkt oder ueber CLI aufgerufen werden.

GRUNDBEFEHLE:

  # Backup erstellen
  bach backup create                  Lokales Backup
  bach backup create --to-nas         Mit NAS-Kopie

  # Backups anzeigen
  bach backup list                    Lokale Backups
  bach backup list --nas              NAS-Backups anzeigen
  bach backup info <n>                Backup-Details

  # Wiederherstellen
  bach restore backup <n>             Bestimmtes Backup
  bach restore backup latest          Neuestes Backup
  bach restore backup latest --force  Ohne Bestaetigung

  # Template zuruecksetzen
  bach restore template SKILL.md      Auf Original

DIST_TYPE KONZEPT
=================
Das Backup-System basiert auf Distribution-Typen:

  dist_type = 2 (CORE)
    -> Distribution IST das Backup
    -> bach.py, hub/, tools/, skills/, docs/docs/docs/help/
    -> NICHT separat gesichert

  dist_type = 1 (TEMPLATE)
    -> 1x Snapshot bei Installation
    -> bach restore template <datei>

  dist_type = 0 (USER_DATA)
    -> Normale Backup-Rotation
    -> Tasks, Memory, Logs, Inbox

WAS WIRD GESICHERT?
-------------------
USER_DATA (dist_type = 0):
  tasks          Alle Tasks, Status, History
  memory/        Sessions, Longterm, Archive
  logs/          Session-Logs
  user/inbox/    Nachrichten, Agenda

NICHT gesichert (CORE/TEMPLATE):
  bach.py, schema.sql, hub/
  tools/, skills/, docs/docs/docs/help/
  (sind Teil der Distribution)

BACKUP-ROTATION
===============
Automatische Rotation verhindert Speicherueberlauf:

  Lokal (system/data/system/data/system/data/system/data/backups/):     7 Backups behalten
  NAS:                  30 Backups behalten
  OneDrive:             Automatisch (Versionsverlauf)

SPEICHERORTE
============
  Lokal:    BACH_v2_vanilla/system/data/system/data/system/data/system/data/backups/
  NAS:      \\YOUR_NAS_IP\fritz.nas\Extreme_SSD\BACKUP\BACH_Backups
  Dist:     BACH_v2_vanilla/distributions/

HINWEIS:
  NAS nur im Heimnetzwerk erreichbar!
  Bei Abwesenheit --to-nas nicht verwenden.

DIREKTE TOOL-NUTZUNG
====================
backup_manager.py kann auch direkt aufgerufen werden:

  python tools/backup_manager.py create [--to-nas]
  python tools/backup_manager.py list [--nas]
  python tools/backup_manager.py restore backup <n>
  python tools/backup_manager.py restore template <file>

SNAPSHOTS (Session-basiert)
===========================
Fuer Session-Snapshots siehe Memory-System:

  bach snapshot create           Manueller Snapshot
  bach snapshot load             Letzten Snapshot laden
  bach snapshot list             Snapshots anzeigen

  -> Automatisch bei Shutdown (bei >= 3 Aenderungen)
  -> Gespeichert in session_snapshots Tabelle

DISTRIBUTION-BEFEHLE
====================
Pakete fuer Verteilung erstellen:

  bach dist create vanilla       Basis-Paket erstellen
  bach dist list                 Pakete anzeigen
  bach dist status               Verteilungsstatus
  bach dist verify               Integritaet pruefen

TYPISCHE ANWENDUNGSFAELLE
=========================

1. VOR GROESSEREN AENDERUNGEN
   Sicherheits-Backup erstellen:
   bach backup create

2. TAEGLICH (HEIMNETZWERK)
   Backup mit NAS-Kopie:
   bach backup create --to-nas

3. NACH ABSTURZ/FEHLER
   Letzte funktionierende Version:
   bach restore backup latest

4. SKILL.MD ZURUECKSETZEN
   Bei kaputten Aenderungen:
   bach restore template SKILL.md

5. PAKET FUER ANDEREN RECHNER
   Distribution erstellen:
   bach dist create vanilla

6. SESSION FORTSETZEN
   Nach Neustart/Chat-Wechsel:
   bach snapshot load

VERWANDTE SKILLS
================
  skills/_service/builder.md    CREATE, EXPORT, DISTRIBUTE, BACKUP
  docs/BACKUP_SYSTEM.md         Urspruengliches Konzept

SIEHE AUCH
----------
  bach --help backup             Vollstaendige Backup-Hilfe
  bach --help dist               Distribution-Befehle
  bach --help memory             Memory/Snapshot-System
  bach --help tools              Tool-Uebersicht


## Backup Manager

BACH Tool: backup_manager
==================================================
Generiert: 2026-02-05
Quelle: tools/backup_manager.py

BESCHREIBUNG
----------------------------------------
backup_manager.py - BACH Backup & Restore System

Verwaltet:
- User-Backup (dist_type=0) -> _system/data/system/data/system/data/system/data/backups/*.zip
- Template-Snapshots (dist_type=1) -> dist/snapshots/*.orig
- Distribution-Restore (dist_type=2) -> [NOCH NICHT IMPLEMENTIERT]

BEFEHLE
----------------------------------------
python backup_manager.py create [--to-nas]
    Erstellt vollstaendiges User-Backup
    --to-nas: Zusaetzlich auf NAS kopieren

python backup_manager.py list [--nas]
    Listet verfuegbare Backups
    --nas: NAS-Backups statt lokale anzeigen

python backup_manager.py info <name>
    Zeigt Backup-Details (Manifest) an

python backup_manager.py restore backup <name> [--force] [--no-auto-backup]
    Stellt User-Backup wieder her
    --force: Ohne Bestaetigung
    --no-auto-backup: Kein Sicherheits-Backup vor Restore

python backup_manager.py restore template <file>
    Setzt Template-Datei auf Original zurueck

python backup_manager.py restore dist <name>
    [GEPLANT] Distribution wiederherstellen - noch nicht implementiert

python backup_manager.py snapshot <file>
    Erstellt Snapshot einer Datei nach dist/snapshots/

AUTOMATISCHE FEATURES
----------------------------------------
- Auto-Backup: Vor jedem Restore wird automatisch ein Sicherheits-Backup erstellt
- Rotation lokal: Max. 7 Backups (aeltere werden automatisch geloescht)
- Rotation NAS: Max. 30 Backups (aeltere werden automatisch geloescht)

GESICHERTE DATEN
----------------------------------------
Datenbank-Tabellen:
  - tasks
  - memory_sessions
  - memory_lessons
  - memory_context
  - monitor_tokens
  - monitor_success

Verzeichnisse:
  - memory/
  - logs/
  - user/

VERWENDUNG
----------------------------------------
python bach.py tools run backup_manager [args]
oder direkt: python tools/backup_manager.py [args]

HINWEISE
----------------------------------------
- NAS-Pfad aus system_config oder Standard: \\YOUR_NAS_IP\fritz.nas\Extreme_SSD\BACKUP\BACH_Backups
- Bach-Version wird im Backup-Manifest gespeichert


## Batch File Ops

BACH Tool: batch_file_ops
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/batch_file_ops.py

BESCHREIBUNG
----------------------------------------
batch_file_ops.py - Batch-Dateioperationen

Sammelt und löscht/verschiebt/kopiert Dateien nach Pattern.

Usage:
    python batch_file_ops.py delete <ordner> --pattern "*.py"
    python batch_file_ops.py delete <ordner> --pattern "TOOLS_*.py"
    python batch_file_ops.py move <quelle> <ziel> --pattern "*.txt"
    python batch_file_ops.py copy <quelle> <ziel> --pattern "*.md"
    python batch_file_ops.py list <ordner> --pattern "*"
    python batch_file_ops.py delete <ordner> --pattern "*.py" --dry-run

Autor: Claude

VERWENDUNG
----------------------------------------
python bach.py tools run batch_file_ops [args]
oder direkt: python tools/batch_file_ops.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show batch_file_ops


## C Audit Bundler

BACH Tool: c_audit_bundler
==================================================
Generiert: 2026-01-23 10:36
Aktualisiert: 2026-02-05 (Forensik-Korrektur)
Quelle: tools/c_audit_bundler.py

BESCHREIBUNG
----------------------------------------
BACH Audit Bundler v1.0
=======================
Erstellt Audit-Pakete fuer externe Reviews.

Zwei Bundles:
1. KONZEPT-Bundle (zuerst): Dokumentation, Konzepte, Ideen
2. IMPLEMENTATION-Bundle (spaeter): Code, DB-Schemas, Scripts

Usage:
    python c_audit_bundler.py --konzept      # Bundle 1: Konzepte
    python c_audit_bundler.py --implementation  # Bundle 2: Code
    python c_audit_bundler.py --all          # Beide Bundles
    python c_audit_bundler.py --help         # Hilfe

VERWENDUNG
----------------------------------------
python bach.py tools run c_audit_bundler [args]
oder direkt: python tools/c_audit_bundler.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_audit_bundler
- Hinweis: Datei wurde von audit_bundler.py zu c_audit_bundler.py umbenannt (c_ Prefix fuer Coding-Kategorie)


## C Emoji Scanner

BACH Tool: c_emoji_scanner
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_emoji_scanner.py

BESCHREIBUNG
----------------------------------------
c_emoji_scanner.py - Emoji-Scanner mit Gemoji/emoji-Paket Integration

Scannt Dateien nach Emojis und zeigt welche automatisch aufgeloest werden koennen.
Nutzt dasselbe Backend wie c_json_repair.py (emoji-Paket oder gemoji.json Fallback).

Usage:
    python c_emoji_scanner.py <datei_oder_ordner>
    python c_emoji_scanner.py --scan-batch    # Alle _BATCH JSON-Dateien
    python c_emoji_scanner.py --status        # System-Status

Autor: Claude
Version: 3.0 - Unified mit c_json_repair.py

VERWENDUNG
----------------------------------------
python bach.py tools run c_emoji_scanner [args]
oder direkt: python tools/c_emoji_scanner.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_emoji_scanner


## C Encoding Fixer

BACH Tool: c_encoding_fixer
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_encoding_fixer.py

BESCHREIBUNG
----------------------------------------
c_encoding_fixer.py - Encoding-Probleme in Textdateien beheben

Zweck: Korrigiert Encoding-Fehler (Mojibake, falsche UTF-8 Dekodierung etc.)
       mit der ftfy-Bibliothek. Erstellt automatisch Backups.

Autor: Claude (adaptiert von EncodingFixxer.py)
Abhängigkeiten: ftfy (pip install ftfy), os, json (stdlib)

Usage:
    python c_encoding_fixer.py <file_or_folder> [--no-backup] [--recursive] [--json]
    
Beispiele:
    python c_encoding_fixer.py script.py              # Einzelne Datei
    python c_encoding_fixer.py ./src --recursive      # Ganzer Ordner
    python c_encoding_fixer.py file.py --no-backup    # Ohne Backup
    python c_encoding_fixer.py file.py --json         # JSON-Output

VERWENDUNG
----------------------------------------
python bach.py tools run c_encoding_fixer [args]
oder direkt: python tools/c_encoding_fixer.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_encoding_fixer


## C German Scanner

BACH Tool: c_german_scanner
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_german_scanner.py

BESCHREIBUNG
----------------------------------------
c_german_scanner.py - Findet deutsche Strings in Python-Projekten

Scannt Python-Dateien nach:
  - Strings mit Umlauten (ae, oe, ue, ss)
  - GUI-Texten (setText, setWindowTitle, QLabel, etc.)
  - Deutschen Keywords (Datei, Bearbeiten, Speichern, etc.)

Nuetzlich fuer:
  - Internationalisierung (i18n) vorbereiten
  - Hardcoded Strings finden
  - Uebersetzungs-Listen erstellen

Extrahiert aus: A3 Entwicklungsschleife Advanced/TranslationSystem.py

Usage:
    python c_german_scanner.py <ordner>
    python c_german_scanner.py <ordner> --json
    python c_german_scanner.py <ordner> --export translations.json

Autor: Claude (adaptiert)
Abhaengigkeiten: keine (nur stdlib)

VERWENDUNG
----------------------------------------
python bach.py tools run c_german_scanner [args]
oder direkt: python tools/c_german_scanner.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_german_scanner


## C Import Diagnose

BACH Tool: c_import_diagnose
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_import_diagnose.py

BESCHREIBUNG
----------------------------------------
Import-Diagnose-Tool für Python-Projekte
=========================================
Systematische Analyse von Import-Problemen und Access Violations.

Führt folgende Tests durch:
1. Einzelne Module isoliert importieren
2. Import-Reihenfolge variieren
3. Circular Import Detection
4. __init__.py Analyse
5. Timing-Tests mit Delays
6. Crash-Punkt lokalisieren

Verwendung:
    python c_import_diagnose.py <projekt_src_pfad> [--json] [--modules module1:Class1,module2:Class2]
    
Beispiel:
    python c_import_diagnose.py C:\MeinProjekt\src --json
    python c_import_diagnose.py . --modules core.app:App,gui.main:MainWindow

VERWENDUNG
----------------------------------------
python bach.py tools run c_import_diagnose [args]
oder direkt: python tools/c_import_diagnose.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_import_diagnose


## C Import Organizer

BACH Tool: c_import_organizer
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_import_organizer.py

BESCHREIBUNG
----------------------------------------
c_import_organizer.py - Organisiert Python-Imports nach PEP8

Funktionen:
  - Sammelt alle import/from-Statements
  - Entfernt Duplikate
  - Sortiert alphabetisch (erst import, dann from)
  - Platziert alle Imports am Dateianfang
  - Bereinigt mehrfache Leerzeilen

Extrahiert aus: A1 ProFiler/PythonBox.py (ImportOptimizer)

Usage:
    python c_import_organizer.py <datei.py>
    python c_import_organizer.py <datei.py> --dry-run
    python c_import_organizer.py <datei.py> --json
    python c_import_organizer.py --stdin < code.py

Autor: Claude (adaptiert)
Abhaengigkeiten: keine (nur stdlib)

VERWENDUNG
----------------------------------------
python bach.py tools run c_import_organizer [args]
oder direkt: python tools/c_import_organizer.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_import_organizer


## C Indent Checker

BACH Tool: c_indent_checker
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_indent_checker.py

BESCHREIBUNG
----------------------------------------
c_indent_checker.py - Python-Einrückungsprüfer

Zweck: Prüft Python-Dateien auf häufige Einrückungsfehler:
       - Fehlende Doppelpunkte nach Strukturen (def, if, class, etc.)
       - return/yield außerhalb von Blöcken
       - Mischung aus Tabs und Leerzeichen

Autor: Claude (adaptiert von indent_gui_checker.py)
Abhängigkeiten: os, re, json (stdlib)

Usage:
    python c_indent_checker.py <file_or_folder> [--recursive] [--log] [--json]
    
Beispiele:
    python c_indent_checker.py script.py          # Einzelne Datei
    python c_indent_checker.py ./src --recursive  # Ganzer Ordner
    python c_indent_checker.py ./src --log        # Log-Datei erstellen
    python c_indent_checker.py script.py --json   # JSON-Output

VERWENDUNG
----------------------------------------
python bach.py tools run c_indent_checker [args]
oder direkt: python tools/c_indent_checker.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_indent_checker


## C Json Repair

BACH Tool: c_json_repair
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_json_repair.py

BESCHREIBUNG
----------------------------------------
c_json_repair.py - Vollautomatisches JSON-Reparatur-System

Nutzt `pip install emoji` fuer beste Ergebnisse (Multi-Language, aktuell).
Fallback auf lokale gemoji.json wenn emoji-Paket nicht installiert.

Workflow:
1. Emoji gefunden -> Lookup via emoji-Paket oder gemoji.json
2. Gefunden -> Auto-ASCII aus Name (z.B. "wrench" -> "[WRENCH]")
3. Nicht gefunden -> Quarantaene [Q:XXXX] (sehr selten)

Usage:
    python c_json_repair.py <file.json>              # Reparieren
    python c_json_repair.py <file.json> --dry-run    # Nur pruefen
    python c_json_repair.py --update-gemoji          # Gemoji aktualisieren
    python c_json_repair.py --stats                  # Statistiken

Autor: Claude
Version: 3.1.0 - Mit emoji-Paket Support + Fallback

VERWENDUNG
----------------------------------------
python bach.py tools run c_json_repair [args]
oder direkt: python tools/c_json_repair.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_json_repair


## C License Generator

BACH Tool: c_license_generator
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_license_generator.py

BESCHREIBUNG
----------------------------------------
c_license_generator.py - Drittanbieter-Lizenzen Generator

Zweck: Generiert THIRD_PARTY_LICENSES.txt mit allen installierten
       pip-Paket-Lizenzen. Nutzt pip-licenses (wird bei Bedarf installiert).

Autor: Claude (adaptiert von generate_third_party_licenses.py)
Abhängigkeiten: subprocess, os, json (stdlib) + pip-licenses (wird auto-installiert)

Usage:
    python c_license_generator.py [--output <file>] [--format plain|json|csv] [--json]
    
Beispiele:
    python c_license_generator.py                           # Standard: THIRD_PARTY_LICENSES.txt
    python c_license_generator.py --output licenses.txt     # Eigener Dateiname
    python c_license_generator.py --format json             # JSON-Format
    python c_license_generator.py --json                    # Maschinenlesbarer Output

VERWENDUNG
----------------------------------------
python bach.py tools run c_license_generator [args]
oder direkt: python tools/c_license_generator.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_license_generator


## C Md To Pdf

BACH Tool: c_md_to_pdf
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_md_to_pdf.py

BESCHREIBUNG
----------------------------------------
Markdown zu PDF Converter - BACH System
==================================================

Konvertiert Markdown-Dateien zu professionellen PDFs.
Standard-Tool fuer User Reports und Dokumentation im BACH-System.

Usage:
    # Alle .md Files im Workspace
    python c_md_to_pdf.py

    # Spezifische Datei
    python c_md_to_pdf.py report.md

    # Mit custom Output
    python c_md_to_pdf.py report.md --output custom.pdf

    # Nur in Workspace speichern
    python c_md_to_pdf.py report.md --workspace-only

Version: 1.0.0
Datum: 2026-02-04
Features:
  - Universell einsetzbar (alle .md oder spezifische Files)
  - Verbessertes Markdown Parsing (Headers, Listen, Code-Bloecke, Bold/Italic)
  - Command-line Arguments (--output, --workspace-only)
  - Automatische Verzeichniserstellung
  - Professionelles PDF-Layout mit ReportLab
  - Unterstuetzt Checkboxen ([ ] und [x])

VERWENDUNG
----------------------------------------
Direkt ausfuehren:
    python tools/c_md_to_pdf.py [args]

Oder aus dem BACH-Verzeichnis:
    python system/tools/c_md_to_pdf.py [args]

ARGUMENTE
----------------------------------------
  files               Markdown-Dateien zum Konvertieren (Standard: alle *.md im Workspace)
  -o, --output        Custom Output-Pfad (nur bei einer Datei)
  --workspace-only    Nur in Workspace speichern

ABHAENGIGKEITEN
----------------------------------------
  - reportlab (pip install reportlab)

HINWEISE
----------------------------------------
- Bei Fragen: bach tools show c_md_to_pdf
- Output-Verzeichnisse werden automatisch erstellt


## C Method Analyzer

BACH Tool: c_method_analyzer
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_method_analyzer.py

BESCHREIBUNG
----------------------------------------
c_method_analyzer.py - Python Code Analyzer für Claude

Zweck: Analysiert Python-Code auf Methoden, Aufrufe, Imports und potenzielle Probleme.
       Extrahiert aus MethodenAnalyser3.py - GUI entfernt, CLI-Interface hinzugefügt.
       
Autor: Claude (adaptiert von Nutzer-Tool)
Version: 2.0 (erweitert um Signal-Check, Attribut-Check, Encoding-Fix)
Abhängigkeiten: ast, collections, difflib, datetime (alle Standard-Library)

Funktionen:
- analyze_file(path) -> AnalysisResult: Hauptanalyse
- generate_report(result) -> str: Formatierter Report
- get_summary(result) -> dict: Kompakte Zusammenfassung für weitere Verarbeitung

Neu in v2.0:
- Windows Console Encoding Fix
- Signal-Connect Prüfung (.connect(self.X) -> existiert X?)
- Attribut-vor-Init Erkennung (self.X verwendet bevor self.X = ...)
- Verbesserte Tippfehler-Erkennung (_show_X vs show_X)

VERWENDUNG
----------------------------------------
python bach.py tools run c_method_analyzer [args]
oder direkt: python tools/c_method_analyzer.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_method_analyzer


## C Pycutter

BACH Tool: c_pycutter
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_pycutter.py

BESCHREIBUNG
----------------------------------------
c_pycutter.py - Python-Klassen-Extractor

Zweck: Zerlegt Python-Dateien in separate Textdateien für jede Klasse,
       plus eine Hilfsfunktionen.txt für Imports, Funktionen und globalen Code.
       Ideal für Code-Review, Dokumentation oder LLM-Kontextmanagement.

Autor: Claude (adaptiert von pyCuttertxt.py)
Abhängigkeiten: ast, os, datetime (stdlib)

Usage:
    python c_pycutter.py <python_file> [--output-dir <dir>] [--json]
    
Beispiele:
    python c_pycutter.py main.py                    # Ausgabe im aktuellen Verzeichnis
    python c_pycutter.py main.py --output-dir ./out # Ausgabe in ./out
    python c_pycutter.py main.py --json             # JSON-Output für Weiterverarbeitung

VERWENDUNG
----------------------------------------
python bach.py tools run c_pycutter [args]
oder direkt: python tools/c_pycutter.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_pycutter


## C Sqlite Viewer

BACH Tool: c_sqlite_viewer
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_sqlite_viewer.py

BESCHREIBUNG
----------------------------------------
sqlite_viewer_cli.py - CLI-Adapter für SQLite Viewer

Zeigt und exportiert SQLite Datenbankinhalte.
Kernlogik extrahiert aus show_user_sqlite.py

Usage:
    python sqlite_viewer_cli.py <database.db> --tables
    python sqlite_viewer_cli.py <database.db> --table <name> [--limit 100]
    python sqlite_viewer_cli.py <database.db> --query "SELECT * FROM users"
    python sqlite_viewer_cli.py <database.db> --schema
    python sqlite_viewer_cli.py <database.db> --export <table> --format csv

VERWENDUNG
----------------------------------------
python bach.py tools run c_sqlite_viewer [args]
oder direkt: python tools/c_sqlite_viewer.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_sqlite_viewer


## C Standard Fixer

BACH Tool: c_standard_fixer
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_standard_fixer.py

BESCHREIBUNG
----------------------------------------
c_standard_fixer.py - Toolchain fuer haeufige Code-Probleme

Fuehrt mehrere Fixer nacheinander aus:
  1. BOM-Fix (entfernt/korrigiert Byte Order Mark)
  2. Encoding-Fix (utf-8 sicherstellen)
  3. Umlaut-Fix (kaputte deutsche Umlaute reparieren)
  4. Indent-Check (Einrueckungsprobleme erkennen)

Usage:
    python c_standard_fixer.py <datei.py>
    python c_standard_fixer.py <datei.py> --dry-run
    python c_standard_fixer.py <ordner> --recursive
    python c_standard_fixer.py <datei.py> --only bom,umlaut
    python c_standard_fixer.py --list-tools

Konfiguration:
    Die aktiven Tools koennen in STANDARD_FIXER_CONFIG angepasst werden.

Autor: Claude
Version: 1.0

VERWENDUNG
----------------------------------------
python bach.py tools run c_standard_fixer [args]
oder direkt: python tools/c_standard_fixer.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_standard_fixer


## C Umlaut Fixer

BACH Tool: c_umlaut_fixer
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_umlaut_fixer.py

BESCHREIBUNG
----------------------------------------
c_umlaut_fixer.py - Repariert kaputte deutsche Umlaute in Python-Dateien

Behebt typische Encoding-Probleme wie:
  - Lschen -> Loeschen
  - ffnen -> oeffnen
  - ber -> ueber
  
Extrahiert aus: A1 ProFiler/_Wartung/fix_profiler_complete.py

Usage:
    python c_umlaut_fixer.py <datei.py>
    python c_umlaut_fixer.py <datei.py> --dry-run
    python c_umlaut_fixer.py <datei.py> --json

Autor: Claude (adaptiert)
Abhaengigkeiten: keine (nur stdlib)

VERWENDUNG
----------------------------------------
python bach.py tools run c_umlaut_fixer [args]
oder direkt: python tools/c_umlaut_fixer.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_umlaut_fixer


## C Universal Converter

BACH Tool: c_universal_converter
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_universal_converter.py

BESCHREIBUNG
----------------------------------------
Universal Data Converter
========================
Konvertiert zwischen JSON, YAML, TOML, XML und TOON Formaten.

Nutzung:
  GUI:  python c_universal_converter.py
  CLI:  python c_universal_converter.py file1.json file2.yaml --to yaml

Unterstützte Formate:
  - JSON (.json)
  - YAML (.yaml, .yml)
  - TOML (.toml)
  - XML (.xml)
  - TOON (.toon) - Token-Oriented Object Notation (Spec-konform)

Abhängigkeiten:
  pip install pyyaml toml xmltodict tkinterdnd2

TOON Spezifikation: https:/github.com/toon-format/toon

Autor: Claude für _BATCH System
Version: 2.0.0
Datum: 2026-01-06

VERWENDUNG
----------------------------------------
python bach.py tools run c_universal_converter [args]
oder direkt: python tools/c_universal_converter.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_universal_converter


## C Youtube Extractor

BACH Tool: c_youtube_extractor
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/c_youtube_extractor.py

BESCHREIBUNG
----------------------------------------
c_youtube_extractor.py - Extrahiert YouTube Video-IDs aus URLs

Unterstuetzte Formate:
  - https:/www.youtube.com/watch?v=VIDEO_ID
  - https:/youtu.be/VIDEO_ID
  - https:/www.youtube.com/shorts/VIDEO_ID
  - https:/www.youtube.com/embed/VIDEO_ID
  - Direkte Video-ID (11 Zeichen)

Extrahiert aus: TOOLS/MEDIA/ForYou-Playlist/YouTubePlaylist.py

Usage:
    python c_youtube_extractor.py <url>
    python c_youtube_extractor.py <url1> <url2> <url3>
    python c_youtube_extractor.py --file urls.txt
    python c_youtube_extractor.py --json <url>
    echo "https:/youtu.be/dQw4w9WgXcQ" | python c_youtube_extractor.py --stdin

Autor: Claude (adaptiert)
Abhaengigkeiten: keine (nur stdlib)

VERWENDUNG
----------------------------------------
python bach.py tools run c_youtube_extractor [args]
oder direkt: python tools/c_youtube_extractor.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show c_youtube_extractor


## Code Generator

BACH Tool: code_generator
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/code_generator.py

BESCHREIBUNG
----------------------------------------
Code-Generator Modul für Entwickler-Agent
Phase 2: Core Features

Generiert Python-Code basierend auf Templates und Spezifikationen

VERWENDUNG
----------------------------------------
python bach.py tools run code_generator [args]
oder direkt: python tools/code_generator.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show code_generator


## Code Quality

CODE QUALITY TOOLS - Code-Qualitaet und Fixes
=============================================

Stand: 2026-01-23
Pfad: docs/docs/docs/help/tools/code_quality.txt

BESCHREIBUNG
------------
Tools zur Behebung haeufiger Code-Probleme:
  - Encoding-Fehler (UTF-8, BOM, Mojibake)
  - Kaputte Umlaute und Sonderzeichen
  - Emojis in Code (Windows-Console-Problem)
  - JSON-Reparatur
  - Einrueckungsprobleme

HAUPT-TOOL: c_standard_fixer
============================
Das Sammel-Tool fuehrt mehrere Fixer nacheinander aus.
Empfohlen als erste Wahl bei Code-Problemen.

ENTHALTENE FIXES:
  1. BOM-Fix        Entfernt Byte Order Mark
  2. Encoding-Fix   Stellt UTF-8 sicher
  3. JSON-Repair    Repariert JSON (bei .json Dateien)
  4. Umlaut-Fix     Repariert kaputte deutsche Umlaute
  5. Indent-Check   Prueft Einrueckung (nur Diagnose)

GRUNDBEFEHLE:

  # Einzelne Datei reparieren
  bach c_standard_fixer script.py

  # Nur pruefen ohne Aenderung
  bach c_standard_fixer script.py --dry-run

  # Ordner rekursiv verarbeiten
  bach c_standard_fixer projekt/ --recursive

  # Nur bestimmte Fixes anwenden
  bach c_standard_fixer script.py --only bom,encoding
  bach c_standard_fixer script.py --only umlaut

  # Verfuegbare Tools anzeigen
  bach c_standard_fixer --list-tools

  # Mit detaillierter Ausgabe
  bach c_standard_fixer script.py --verbose

OPTIONEN:
  --dry-run       Nur pruefen, keine Aenderungen
  --recursive     Unterordner einbeziehen
  --verbose, -v   Detaillierte Ausgabe
  --only=TOOLS    Nur bestimmte Tools (kommagetrennt)
  --list-tools    Verfuegbare Tools anzeigen

TOOL-NAMEN fuer --only:
  bom_fix, encoding_fix, json_repair, umlaut_fix, indent_check

BACKUP:
  Erstellt automatisch .standardfixer.bak Dateien

DATEI-TYPEN:
  Verarbeitet: .py, .md, .txt, .json
  Ignoriert:   __pycache__, .git, venv, node_modules, .bak

WARNUNG:
  NICHT auf batch_manager.py anwenden (bekannter Bug).
  Siehe: bach --help lessons

JSON-REPARATUR: c_json_repair
=============================
Spezialisiertes Tool fuer JSON-Probleme.

FUNKTIONEN:
  - Emoji zu ASCII konvertieren ([TOOL], [OK], etc.)
  - Mojibake reparieren (kaputte Unicode-Sequenzen)
  - Newlines in Strings korrigieren
  - BOM entfernen

GRUNDBEFEHLE:

  # JSON reparieren
  bach c_json_repair config.json

  # Nur pruefen
  bach c_json_repair config.json --dry-run

  # JSON-Ausgabe (fuer Scripts)
  bach c_json_repair config.json --json

  # Emoji-Datenbank aktualisieren
  bach c_json_repair --update-gemoji

  # Statistiken anzeigen
  bach c_json_repair --stats

OPTIONEN:
  --dry-run        Nur pruefen, keine Aenderungen
  --json           JSON-Output (maschinenlesbar)
  --update-gemoji  Emoji-Datenbank aktualisieren
  --stats          Reparatur-Statistiken anzeigen

EMOJI-KONVERTIERUNG (Beispiele):
  [WRENCH] <- Schraubenschluessel-Emoji
  [OK]     <- Gruener Haken
  [X]      <- Rotes X
  [WARN]   <- Warnung-Dreieck
  [FOLDER] <- Ordner-Emoji
  [FILE]   <- Datei-Emoji
  ->       <- Pfeil-Unicode

JSON-FIXER (Alternative): json_fixer
====================================
Einfacheres Tool fuer grundlegende JSON-Probleme.

FUNKTIONEN:
  - BOM entfernen
  - Trailing Commas entfernen
  - Einzel-Quotes zu Doppel-Quotes
  - Unescaped Strings reparieren

GRUNDBEFEHLE:

  # Einzelne Datei
  bach json_fixer config.json

  # Alle JSON in Ordner
  bach json_fixer data/

  # Nur pruefen
  bach json_fixer config.json --dry-run

  # Mit Backup
  bach json_fixer config.json --backup

WANN WELCHES TOOL?
  c_json_repair  -> Emoji-Probleme, komplexe Reparaturen
  json_fixer     -> Einfache Syntax-Fehler (Commas, Quotes)

EINZEL-TOOLS (in c_standard_fixer enthalten)
============================================
Diese Tools werden normalerweise ueber c_standard_fixer aufgerufen,
koennen aber auch einzeln genutzt werden:

c_encoding_fixer.py
  Encoding auf UTF-8 korrigieren
  bach c_encoding_fixer script.py

c_umlaut_fixer.py
  Kaputte deutsche Umlaute reparieren (ae->ä, ue->ü, etc.)
  bach c_umlaut_fixer script.py

c_indent_checker.py
  Einrueckungsprobleme finden (Tab vs Space, inkonsistent)
  bach c_indent_checker script.py

c_emoji_scanner.py
  Emojis in Dateien finden
  bach c_emoji_scanner script.py

c_german_scanner.py
  Deutsche Woerter/Umlaute finden
  bach c_german_scanner script.py

EMPFEHLUNG: Nutze c_standard_fixer statt Einzel-Tools.

TYPISCHE ANWENDUNGSFAELLE
=========================

1. NACH GIT CLONE (Windows)
   Encoding-Probleme durch unterschiedliche Systeme:
   bach c_standard_fixer projekt/ --recursive

2. NACH COPY/PASTE AUS WEB
   Kaputte Sonderzeichen:
   bach c_standard_fixer datei.py --only umlaut,encoding

3. JSON LAESST SICH NICHT LADEN
   Syntax oder Encoding-Fehler:
   bach c_json_repair config.json

4. EMOJIS CRASHEN WINDOWS-CONSOLE
   Emojis zu ASCII konvertieren:
   bach c_json_repair datei.json
   # oder fuer Python:
   bach c_standard_fixer script.py

5. VOR COMMIT
   Alle Code-Dateien pruefen:
   bach c_standard_fixer src/ --recursive --dry-run

CONTEXT-INJEKTOR
----------------
Der ContextInjector erkennt Stichwoerter und empfiehlt diese Tools:

  "encoding problem"  -> bach c_standard_fixer <datei>
  "umlaute kaputt"    -> bach c_standard_fixer <datei>
  "json problem"      -> bach c_json_repair <datei>
  "emoji"             -> bach c_emoji_scanner <datei>
  "utf-8"             -> bach c_encoding_fixer <datei>

SIEHE AUCH
----------
  bach --help tools              Tool-Uebersicht
  bach --help lessons            Bekannte Probleme (Standard-Fixer Bug)
  bach --help tools/imports      Import-Probleme
  bach --help tools/python_editing  Python-Dateien bearbeiten


## Conversion

CONVERSION TOOLS - Konvertierungs-Werkzeuge
===========================================

UEBERSICHT
Die Conversion-Tools in BACH wandeln Dateiformate um
und reparieren/standardisieren Dateien.

UNIVERSAL CONVERTER
-------------------
c_universal_converter.py

Universelles Konvertierungs-Tool fuer viele Formate.
Unterstuetzt:
  - Text -> PDF
  - Markdown -> PDF/HTML
  - JSON -> CSV
  - Excel -> CSV
  - Bilder (Resize, Format)

Aufruf: python tools/c_universal_converter.py <eingabe> <ausgabe>

MARKDOWN -> PDF
---------------
c_md_to_pdf.py

Konvertiert Markdown-Dateien in PDF mit Styling.
Features:
  - Code-Highlighting
  - Tabellen
  - Bilder einbetten

Aufruf: python tools/c_md_to_pdf.py <md-datei> [--output <pdf>]

ENCODING & TEXT
---------------

c_encoding_fixer.py
  Repariert Encoding-Probleme (UTF-8, Latin-1, etc.)
  Erkennt automatisch falsche Kodierung.
  Aufruf: python tools/c_encoding_fixer.py <datei>

c_umlaut_fixer.py
  Repariert deutsche Umlaute in Dateien.
  Ersetzt kaputte Zeichen (ae->ä, ue->ü, etc.)
  Aufruf: python tools/c_umlaut_fixer.py <datei>

c_standard_fixer.py
  Standardisiert Code-Formatierung.
  Entfernt trailing whitespace, vereinheitlicht Zeilenenden.
  Aufruf: python tools/c_standard_fixer.py <datei>

JSON TOOLS
----------

c_json_repair.py
  Repariert kaputte JSON-Dateien.
  Fixiert fehlende Kommas, Quotes, Klammern.
  Aufruf: python tools/c_json_repair.py <datei>

json_fixer.py
  Alternative JSON-Reparatur mit erweiterten Optionen.
  Aufruf: python tools/json_fixer.py <datei>

CODE TOOLS
----------

c_import_organizer.py
  Sortiert und organisiert Python-Imports.
  Gruppiert: Standard, Third-Party, Local.
  Aufruf: python tools/c_import_organizer.py <datei>

c_indent_checker.py
  Prueft und korrigiert Einrueckung.
  Optionen: --tabs, --spaces N
  Aufruf: python tools/c_indent_checker.py <datei>

EXPORT
------

export_txt.py
  Exportiert Dateien als Plain Text.
  Aufruf: python tools/export_txt.py <datei>

exporter.py
  Allgemeiner Exporter fuer verschiedene Formate.
  Aufruf: python tools/exporter.py <datei> --format <fmt>

BATCH-OPERATIONEN
-----------------

batch_file_ops.py
  Fuehrt Datei-Operationen auf mehreren Dateien aus.
  Operationen: rename, copy, move, convert
  Aufruf: python tools/batch_file_ops.py <operation> <pattern>

SIEHE AUCH
----------
bach --help tools         Tool-Uebersicht
bach --help backup        Backup-Tools
bach --help maintain      Wartungs-Tools


## Create Boot Checks

BACH Tool: create_boot_checks
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/create_boot_checks.py

BESCHREIBUNG
----------------------------------------
boot_checks Tabelle erstellen - KRITISCH für Pre-Prompt Checks
Erstellt: 2026-01-21 (BACH Session)

VERWENDUNG
----------------------------------------
python bach.py tools run create_boot_checks [args]
oder direkt: python tools/create_boot_checks.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show create_boot_checks


## Dirscan

BACH Tool: dirscan
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/dirscan.py

BESCHREIBUNG
----------------------------------------
Directory Scanner - Automatische IST/SOLL Zustand Verwaltung
============================================================

- Startup: IST-Zustand erfassen
- Shutdown: Änderungen = neuer SOLL-Zustand
- Heuristik: Claude-Änderungen sind gewollt

VERWENDUNG
----------------------------------------
python bach.py tools run dirscan [args]
oder direkt: python tools/dirscan.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show dirscan


## Distribution System

BACH Tool: distribution_system
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/distribution_system.py

BESCHREIBUNG
----------------------------------------
RecludOS Distribution & Identity System v1.1.0

Verwaltet:
- Tier-Klassifizierung (Kernel, Core, Extension, UserData)
- Siegel-System (Integritätsprüfung)
- Modi (Developer, User, Learn)
- Versionierung mit Quellen-Suffixen
- Release-Erstellung und -Export
- Snapshots & Point-in-Time Recovery
- Multi-Instanz-Erkennung

Datum: 2026-01-01

VERWENDUNG
----------------------------------------
python bach.py tools run distribution_system [args]
oder direkt: python tools/distribution_system.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show distribution_system


## Doc Update Checker

BACH Tool: doc_update_checker
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/doc_update_checker.py

BESCHREIBUNG
----------------------------------------
BACH Documentation Update Checker v1.0.1

Automatische Erkennung und Aktualisierung veralteter Dokumentationen.
Portiert von RecludOS, integriert mit BACH Memory-System.

Features:
- Erkennt veraltete Dokumente (>60 Tage, ungültige Pfade)
- Generiert Update-Vorschläge
- Erstellt Aktualisierungs-Reports
- Kann automatisch einfache Updates durchführen

Usage:
  python doc_update_checker.py check              # Prüfen
  python doc_update_checker.py report             # Report erstellen
  python doc_update_checker.py auto-update        # Auto-Update (sicher)
  python doc_update_checker.py schedule           # Für Micro-Routines

VERWENDUNG
----------------------------------------
python bach.py tools run doc_update_checker [args]
oder direkt: python tools/doc_update_checker.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show doc_update_checker


## Duplicate Detector

BACH Tool: duplicate_detector
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/duplicate_detector.py

BESCHREIBUNG
----------------------------------------
Pre-Create Check & Duplicate Detection - Phase 3
=================================================

Verhindert Duplikate durch Check vor Tool-Erstellung.

Version: 1.0.0

VERWENDUNG
----------------------------------------
python bach.py tools run duplicate_detector [args]
oder direkt: python tools/duplicate_detector.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show duplicate_detector


## Entwickler Agent

BACH Tool: entwickler_agent
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/entwickler_agent.py

BESCHREIBUNG
----------------------------------------
Entwickler-Agent v1.0.0
RecludOS Software-Entwicklungs-Agent
Vollständige Implementation (Phase 1-6)

Phase 1: ✅ Projekt- & Task-Management
Phase 2: ✅ Code-Analyse & Generation
Phase 3: ✅ Service-Integration (Editor/Compiler)
Phase 4: ✅ Intelligenz (Debugging, Patterns)
Phase 5: ✅ Kollaboration (Feedback-Loop)
Phase 6: ✅ Testing & Polish

VERWENDUNG
----------------------------------------
python bach.py tools run entwickler_agent [args]
oder direkt: python tools/entwickler_agent.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show entwickler_agent


## Export Txt

BACH Tool: export_txt
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/export_txt.py

BESCHREIBUNG
----------------------------------------
Exportiert Steuer-Posten in TXT-Dateien - alle Listen + Dokumentenverzeichnis

VERWENDUNG
----------------------------------------
python bach.py tools run export_txt [args]
oder direkt: python tools/export_txt.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show export_txt


## Exporter

BACH Tool: exporter
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/exporter.py

BESCHREIBUNG
----------------------------------------
exporter.py
===========
Export-Tool für Skills, Agents und OS.

Version: 1.0.0
Erstellt: 2026-01-14

KONZEPT:
  Im OS sind Skills/Agents leichtgewichtig (nutzen OS-Infrastruktur).
  Für externe Nutzung müssen sie "verpackt" werden mit eigener Infrastruktur.

BEFEHLE:
  skill     Exportiert einen Skill aus dem OS als Standalone
  agent     Exportiert einen Agent mit seinen Skills
  os-fresh  Erstellt ein frisches OS-Paket (ohne Userdaten)
  os-reset  Setzt ein OS zurück (löscht Userdaten)

Verwendung:
    python exporter.py skill <name> --from-os <os-path> [--output <zip>]
    python exporter.py agent <name> --from-os <os-path> [--output <zip>]
    python exporter.py os-fresh <os-path> [--output <zip>] [--version <v>]
    python exporter.py os-reset <os-path> [--backup] [--confirm]

Beispiele:
    python exporter.py skill recherche --from-os ./mein-os
    python exporter.py agent schreib-assistent --from-os ./mein-os
    python exporter.py os-fresh ./mein-os --output os-v1.0.zip
    python exporter.py os-reset ./mein-os --backup

VERWENDUNG
----------------------------------------
python bach.py tools run exporter [args]
oder direkt: python tools/exporter.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show exporter


## File Cleaner

BACH Tool: file_cleaner
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/file_cleaner.py

BESCHREIBUNG
----------------------------------------
file_cleaner.py - Dateien nach Alter/Muster bereinigen
======================================================

Findet und loescht alte Dateien oder Dateien nach Muster.
Nuetzlich fuer Backup-Ordner, Logs, temporaere Dateien.

Usage:
    python file_cleaner.py <ordner> --age 30           # Aelter als 30 Tage
    python file_cleaner.py <ordner> --pattern "*.log"  # Nach Muster
    python file_cleaner.py <ordner> --keep 5           # Behalte 5 neueste
    python file_cleaner.py <ordner> --execute          # Tatsaechlich loeschen

Autor: BACH v1.1

VERWENDUNG
----------------------------------------
python bach.py tools run file_cleaner [args]
oder direkt: python tools/file_cleaner.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show file_cleaner


## Förderplaner Cli

BACH Tool: foerderplaner_cli
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/foerderplaner_cli.py

BESCHREIBUNG
----------------------------------------
Foerderplaner CLI - Kommandozeilen-Tool für Förderplanung
Durchsucht ICF-Struktur, Wissensdatenbank und schlägt Methoden/Material vor

VERWENDUNG
----------------------------------------
python bach.py tools run foerderplaner_cli [args]
oder direkt: python tools/foerderplaner_cli.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show foerderplaner_cli


## Gemini Start

BACH Tool: gemini_start
==================================================
Generiert: 2026-01-24 (aktualisiert)
Quelle: tools/gemini_start.py

BESCHREIBUNG
----------------------------------------
BACH Gemini Starter - Startet Gemini CLI (headless) oder Antigravity (GUI).

ZWEI BACKENDS
----------------------------------------
  --cli         Gemini CLI (headless, vollautomatisch mit --yolo)
  --gui         Antigravity (Prompt wird in Zwischenablage kopiert)

WICHTIG: Antigravity hat keinen Headless-Modus! Fuer Automatisierung
         MUSS die Gemini CLI verwendet werden (--cli).

VERWENDUNG
----------------------------------------
python tools/gemini_start.py [BACKEND] [OPTIONS]

  BACKEND (erforderlich fuer nicht-Auto):
    --cli              Gemini CLI (vollautomatisch)
    --gui              Antigravity (Prompt in Clipboard)

  MODI:
    (ohne)             Auto-Modus (nur mit --cli sinnvoll)
    --bulk             Bulk-Modus ohne Task-Limit
    --default          Interaktiv (wartet auf Anweisungen)
    --individual       Nutzt startprompt_gemini.txt
    --mode NAME        Nutzt prompts/NAME.txt

  OPTIONEN:
    --tasks N          Anzahl Tasks im Auto-Modus (default: 2)
    --prompt "TEXT"    Custom Prompt direkt angeben
    --list             Verfuegbare Prompt-Vorlagen auflisten
    --dry-run          Nur Befehl anzeigen, nicht starten

CLI-BEISPIELE (vollautomatisch)
----------------------------------------
  python tools/gemini_start.py --cli                # Auto (2 Tasks)
  python tools/gemini_start.py --cli --tasks 5      # Auto (5 Tasks)
  python tools/gemini_start.py --cli --bulk         # Alle Tasks (endless)
  python tools/gemini_start.py --cli --mode analyse # Analyse-Modus

GUI-BEISPIELE (Prompt in Zwischenablage)
----------------------------------------
  python tools/gemini_start.py --gui --bulk         # Bulk-Prompt
  python tools/gemini_start.py --gui --default      # Interaktiv-Prompt
  python tools/gemini_start.py --gui --individual   # User-Prompt
  python tools/gemini_start.py --gui --mode analyse # Analyse-Prompt

GUI-WORKFLOW:
  1. Script startet Antigravity
  2. Prompt wird in Zwischenablage kopiert
  3. User klickt in Chat, drueckt Ctrl+V, Enter

PROMPT-VORLAGEN (partners/gemini/prompts/)
----------------------------------------
  auto.txt      Auto-Modus: Tasks sofort abarbeiten (nur CLI)
  bulk.txt      Bulk-Modus: ALLE Tasks ohne Limit
  default.txt   Interaktiv: Wartet auf Anweisungen
  analyse.txt   Fuehrt alle Analyse-Scripts aus
  research.txt  Recherche-Modus fuer Themenanalyse

INDIVIDUELLER PROMPT
----------------------------------------
Bearbeite partners/gemini/startprompt_gemini.txt fuer eigene Anweisungen.
Wird mit --individual geladen.

BATCH-STARTER
----------------------------------------
Alternativ: partners/gemini/start_gemini.bat
Zeigt interaktives Menue mit CLI/GUI Auswahl.

VORAUSSETZUNGEN
----------------------------------------
  CLI-Modus:   npm install -g gemini-cli
               gemini auth login
  GUI-Modus:   Antigravity installiert und im PATH

SIEHE AUCH
----------------------------------------
  wiki/gemini.txt        Gemini-Details (CLI, API, Preise)
  wiki/antigravity.txt   Antigravity IDE
  docs/docs/docs/help/partners.txt           Partner-Netzwerk
  partners/gemini/_README.md Workspace-Dokumentation


## Generate Skills Report

BACH Tool: generate_skills_report
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/generate_skills_report.py

BESCHREIBUNG
----------------------------------------
generate_skills_report.py - Generiert nutzerfreundlichen Skills-Bericht

Erstellt: user/SKILLS_REPORT.md

VERWENDUNG
----------------------------------------
python bach.py tools run generate_skills_report [args]
oder direkt: python tools/generate_skills_report.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show generate_skills_report


## Imports

IMPORT TOOLS - Python Import-Handling
======================================

Stand: 2026-01-23
Pfad: docs/docs/docs/help/tools/imports.txt

BESCHREIBUNG
------------
Tools zur Diagnose und Organisation von Python-Imports:
  - Import-Probleme finden (fehlende, zirkulaere, ungenutzte)
  - Imports sortieren und bereinigen (PEP8-konform)

Haeufige Probleme die diese Tools loesen:
  - "ModuleNotFoundError" / "ImportError"
  - Zirkulaere Imports (A importiert B, B importiert A)
  - Chaotische Import-Reihenfolge
  - Doppelte Imports
  - Imports mitten im Code statt am Anfang

IMPORT DIAGNOSE: c_import_diagnose
==================================
Systematische Analyse von Import-Problemen.

FUNKTIONEN:
  - Einzelne Module isoliert importieren
  - Import-Reihenfolge variieren
  - Zirkulaere Imports erkennen
  - __init__.py analysieren
  - Timing-Tests mit Delays
  - Crash-Punkt lokalisieren

GRUNDBEFEHLE:

  # Projekt analysieren
  bach c_import_diagnose projekt/src/

  # Mit JSON-Ausgabe
  bach c_import_diagnose projekt/src/ --json

  # Bestimmte Module testen
  bach c_import_diagnose . --modules core.app:App,gui.main:MainWindow

OPTIONEN:
  --json                 JSON-Output (maschinenlesbar)
  --modules M1:C1,M2:C2  Spezifische Module:Klassen testen

AUSGABE-BEISPIEL:
  === IMPORT DIAGNOSE ===
  
  [1/5] Einzelne Module testen...
    [OK] core.app.App
    [FAIL] gui.main.MainWindow -> ImportError: No module named 'missing'
  
  [2/5] Zirkulaere Imports pruefen...
    [WARN] core.utils -> core.app -> core.utils (Zirkel!)
  
  [3/5] __init__.py Analyse...
    [OK] core/__init__.py
    [MISSING] gui/__init__.py
  
  === EMPFEHLUNGEN ===
  1. Fehlendes Modul 'missing' installieren
  2. Zirkulaeren Import core.utils <-> core.app aufloesen
  3. gui/__init__.py erstellen

IMPORT ORGANIZER: c_import_organizer
====================================
Sortiert und bereinigt Python-Imports nach PEP8.

FUNKTIONEN:
  - Alle Imports am Dateianfang sammeln
  - Duplikate entfernen
  - Alphabetisch sortieren (erst import, dann from)
  - Mehrfache Leerzeilen bereinigen

GRUNDBEFEHLE:

  # Datei organisieren
  bach c_import_organizer script.py

  # Nur pruefen ohne Aenderung
  bach c_import_organizer script.py --dry-run

  # JSON-Ausgabe
  bach c_import_organizer script.py --json

  # Von stdin lesen
  cat script.py | bach c_import_organizer --stdin

OPTIONEN:
  --dry-run   Nur anzeigen, nicht aendern
  --json      JSON-Output
  --stdin     Code von stdin lesen

VORHER/NACHHER BEISPIEL:

  VORHER:
  ---------------------
  import os
  
  def foo():
      from pathlib import Path
      pass
  
  import sys
  from typing import List
  import os  # Duplikat!
  ---------------------

  NACHHER:
  ---------------------
  import os
  import sys
  from pathlib import Path
  from typing import List
  
  def foo():
      pass
  ---------------------

TYPISCHE WORKFLOWS
==================

1. "ImportError" DEBUGGEN
   Projekt analysieren um Crash-Punkt zu finden:
   
   bach c_import_diagnose projekt/src/ --json
   
   Dann Empfehlungen befolgen.

2. ZIRKULAERE IMPORTS FINDEN
   Wenn sich Module gegenseitig importieren:
   
   bach c_import_diagnose projekt/src/
   
   Ausgabe zeigt: A -> B -> A (Zirkel!)
   
   Loesung: Gemeinsame Abhaengigkeiten in drittes Modul auslagern.

3. VOR CODE-REVIEW
   Imports aufraumen bevor Code reviewt wird:
   
   bach c_import_organizer script.py
   
   Oder fuer ganzes Projekt:
   for f in *.py; do bach c_import_organizer "$f"; done

4. NACH REFACTORING
   Nach grossem Umbau Imports pruefen:
   
   # Erst diagnostizieren
   bach c_import_diagnose src/
   
   # Dann aufraumen
   for f in src/*.py; do bach c_import_organizer "$f"; done

5. NEUES PROJEKT EINRICHTEN
   __init__.py Dateien pruefen:
   
   bach c_import_diagnose mein_paket/
   
   Zeigt fehlende __init__.py Dateien an.

PEP8 IMPORT-REIHENFOLGE
=======================
Der c_import_organizer sortiert nach PEP8-Standard:

  1. Standard-Library (import os, import sys)
  2. Third-Party (import requests, import numpy)
  3. Lokale Imports (from . import module)

Innerhalb jeder Gruppe: alphabetisch sortiert.

CONTEXT-INJEKTOR
----------------
Der ContextInjector erkennt Stichwoerter und empfiehlt diese Tools:

  "imports sortieren"  -> bach c_import_organizer <datei>
  "import problem"     -> bach c_import_diagnose <projekt>
  "import fehlt"       -> bach c_import_diagnose <projekt>

INTEGRATION MIT ANDEREN TOOLS
=============================
Kombiniere mit python_cli_editor fuer vollstaendiges Bild:

  # Imports anzeigen (gruppiert)
  bach python_cli_editor script.py --imports
  
  # Dann organisieren
  bach c_import_organizer script.py

SIEHE AUCH
----------
  bach --help tools/python_editing   Python-Dateien bearbeiten
  bach --help tools/code_quality     Code-Qualitaet (Encoding etc.)
  bach python_cli_editor --help      Imports anzeigen mit --imports


## Injectors

BACH Tool: injectors
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/injectors.py

BESCHREIBUNG
----------------------------------------
Injector System - Automatische Hilfe und Kontext
================================================

Injektoren die Claude kognitiv entlasten:
- StrategyInjector: Hilfreiche Gedanken bei Trigger-Wörtern
- ContextInjector: Auto-Kontext bei Stichwörtern
- TimeInjector: Regelmäßige Zeit-Updates
- BetweenInjector: Auto-Erinnerungen nach Task-Done

VERWENDUNG
----------------------------------------
python bach.py tools run injectors [args]
oder direkt: python tools/injectors.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show injectors


## Json Fixer

BACH Tool: json_fixer
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/json_fixer.py

BESCHREIBUNG
----------------------------------------
json_fixer.py - JSON-Dateien reparieren
=======================================

Repariert kaputte JSON-Dateien:
- BOM entfernen
- Trailing Commas
- Einzel-Quotes
- Unescaped Strings

Usage:
    python json_fixer.py <datei>           # Einzelne Datei
    python json_fixer.py <ordner>          # Alle JSON im Ordner
    python json_fixer.py <path> --dry-run  # Nur pruefen
    python json_fixer.py <path> --backup   # Mit Backup

Autor: BACH v1.1

VERWENDUNG
----------------------------------------
python bach.py tools run json_fixer [args]
oder direkt: python tools/json_fixer.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show json_fixer


## Mapping

MAPPING-TOOLS - Feature-Vergleich zwischen Systemen
===================================================

Stand: 2026-01-23
Pfad: docs/docs/docs/help/tools/mapping.txt

BESCHREIBUNG
------------
Feature-Mapping-Tools zum Vergleichen und Analysieren
von Features ueber verschiedene Systeme hinweg.
Teil des BACH_STREAM Projekts.

Pfad: tools/mapping/

DATEIEN
-------
  query_features.py     Features abfragen und vergleichen
  populate_features.py  Datenbank mit Features befuellen
  schema.sql            Datenbank-Schema

DATENBANK
---------
Speicherort: BACH_STREAM/MAPPING/feature_mapping.db

Tabellen:
  systems            Registrierte Systeme (CHIAH, BATCH, recludOS, etc.)
  features           Feature-Definitionen
  feature_categories Kategorisierung (Memory, GUI, Tasks, etc.)
  implementations    Welches System hat welches Feature

HAUPTFUNKTIONEN
---------------

feature_matrix(category=None):
  Zeigt welches System welches Feature hat.
  
  python query_features.py matrix
  python query_features.py matrix --category "Memory"
  
  Symbole:
    +  = implemented (vollstaendig)
    ~  = partial (teilweise)
    ?  = geplant/unbekannt
    -  = nicht vorhanden

feature_synopsis(feature_name):
  Vergleicht ein einzelnes Feature ueber alle Systeme.
  Zeigt Pfade, Technologie, Notizen.
  
  python query_features.py synopsis "Working Memory"

REGISTRIERTE SYSTEME
--------------------
  _CHIAH     v3.1    Original CLI-First System
  _BATCH     v2.5    Hub-basiertes System
  recludOS   v3.3.0  Agent-Framework
  BACH       v1.1    Best-of Synopse (dieses System)
  AI-Portable        RAG-Pipeline Utility
  Templates          Projekt-Vorlagen

FEATURE-KATEGORIEN
------------------
  01 Task-Management      Aufgabenverwaltung
  02 Memory               Gedaechtnissysteme
     21 Memory-Kurzzeit   Session-basiert
     22 Memory-Langzeit   Persistent
     23 Memory-Kontext    Quellen-Gewichtung
  03 Session-Management   Startup/Shutdown
  04 GUI                  Web-Dashboards
  05 Wartung              Hintergrund-Prozesse (Daemon)
  06 Tools                Utilities
  07 Kommunikation        Messaging, Partner
  08 Dokumentation        Help-System
  09 Agenten              Boss-Agenten, Experts
  10 Backup               Sicherheit
  11 RAG/Embeddings       Retrieval Augmented
  12 Datei-Operationen    Filesystem

VERWENDUNG
----------

Feature-Matrix generieren:
  python tools/mapping/query_features.py matrix

Gefiltert nach Kategorie:
  python tools/mapping/query_features.py matrix --category "GUI"

Feature-Synopse:
  python tools/mapping/query_features.py synopsis "Injektoren"

Neue Features eintragen:
  python tools/mapping/populate_features.py

INTEGRATION MIT BACH
--------------------
Das Mapping-System hilft bei:
  - Migration von Vorgaengersystemen
  - Identifikation fehlender Features
  - Dokumentation des Implementierungsstands

Siehe auch: docs/con2_ANFORDERUNGSANALYSE.md

SIEHE AUCH
----------
  docs/docs/docs/help/architecture.txt           BACH-Systemarchitektur
  docs/consense_diff_2.md         Offene Anforderungen
  ROADMAP.md                      Roadmap mit Todos
  skills/SKILL_ANALYSE.md         Abdeckungskoeffizienten

VERSION: v1.0.0 (2026-01-23)
Zeilen: ~334 (query_features.py), ~313 (populate_features.py)


## Migrate Ati Tasks

BACH Tool: migrate_ati_tasks
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/migrate_ati_tasks.py

BESCHREIBUNG
----------------------------------------
Task 82 Phase 2: Migration scanned_tasks (bach.db) → ati_tasks (bach.db)
Erstellt: 2026-01-19

VERWENDUNG
----------------------------------------
python bach.py tools run migrate_ati_tasks [args]
oder direkt: python tools/migrate_ati_tasks.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show migrate_ati_tasks


## Migrate Connections

BACH Tool: migrate_connections
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/migrate_connections.py

BESCHREIBUNG
----------------------------------------
Migrate Connections to Database
================================

Migriert die archivierten JSON-Registries in die bach.db Tabellen:
- external_ki_tools_registry.json -> tools (type='external')
- connections_overview.json/cli_tools -> tools (type='cli')
- connections_overview.json/mcp_servers -> connections (type='mcp')
- claude_registry.json -> connections (type='ai')

Usage:
    python migrate_connections.py [--dry-run]
    python migrate_connections.py --status
    python migrate_connections.py --help

Version: 1.0.0

VERWENDUNG
----------------------------------------
python bach.py tools run migrate_connections [args]
oder direkt: python tools/migrate_connections.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show migrate_connections


## Monitoring

BACH MONITORING TOOLS
=====================

Tools zur Systemueberwachung, Konsistenzpruefung und Fehlererkennung.

SCHNELLSTART
------------
  bach --maintain registry     # DB/JSON Konsistenz pruefen
  bach --maintain skills       # Skill-Gesundheit pruefen
  bach --status               # Systemstatus anzeigen

UEBERSICHT MONITORING-TOOLS
---------------------------
tools/maintenance/
├── registry_watcher.py       # DB-JSON Konsistenzpruefung
└── skill_health_monitor.py   # Skill-Validierung

REGISTRY WATCHER
----------------
Prueft Konsistenz zwischen SQLite-Datenbank und JSON-Konfigurationen.

  python tools/maintenance/registry_watcher.py check
  python tools/maintenance/registry_watcher.py repair

Was wird geprueft:
- Tabellen-Existenz in bach.db
- JSON-Konfig-Dateien Validitaet
- Referentielle Integritaet
- Orphaned Records (Waisen-Eintraege)

SKILL HEALTH MONITOR
--------------------
Validiert alle BACH-Skills und Agenten.

  python tools/maintenance/skill_health_monitor.py check
  python tools/maintenance/skill_health_monitor.py report

Was wird geprueft:
- SKILL.md Vollstaendigkeit
- Agent-Manifeste
- Verzeichnisstruktur
- Verwaiste Skills

TOKEN MONITORING
----------------
Ueberwacht Token-Verbrauch fuer Kostenkontrolle.

Tabelle: monitor_tokens
- session_id, tokens_used, timestamp
- Token-Zonen (1-4) fuer Partner-Delegation

  bach --memory status         # Token-Zone anzeigen
  SELECT * FROM monitor_tokens; # Rohdaten

PROCESS MONITORING
------------------
Tabelle: monitor_processes
- Laufende Prozesse
- Wartungs-Daemon-Status
- Background-Jobs

  bach daemon status           # Wartungs-Daemon pruefen
  bach --status               # Gesamtstatus

SUCCESS MONITORING
------------------
Tabelle: monitor_success
- Erfolgsraten von Tools
- Fehlerhistorie
- Lernmuster fuer Verbesserungen

AUTOMATISCHE CHECKS BEI --startup
---------------------------------
Diese Checks laufen automatisch bei Session-Start:

1. Directory Scan         # Aenderungen seit letzter Session
2. Path Healer (dry-run)  # Pfadkorrektur-Vorschlaege
3. Registry Watcher       # DB/JSON Konsistenz
4. Skill Health Monitor   # Skills/Agenten Zustand

Probleme werden als Warnings in Startup-Ausgabe gemeldet.

DATENBANK-TABELLEN
------------------
27 Tabellen in bach.db, davon Monitoring-relevant:

  monitor_tokens      # Token-Tracking
  monitor_success     # Erfolgsraten
  monitor_processes   # Prozess-Status

CLI-BEFEHLE
-----------
  bach --maintain heal        # Pfad-Korrektur (dry-run)
  bach --maintain registry    # DB/JSON Konsistenz
  bach --maintain skills      # Skill-Gesundheit
  bach --maintain docs        # Dokumentations-Check
  bach --status              # Gesamtstatus

LOGS UND AUSWERTUNG
-------------------
Monitoring-Daten werden in Logs gespeichert:

  logs/auto_log_extended.txt  # Befehls-Log
  logs/errors/               # Fehler-Logs

Auswertung:
  bach --logs tail 20          # Letzte 20 Log-Eintraege
  bach --logs search "error"   # Nach Fehlern suchen

ALARME UND WARNUNGEN
--------------------
- Token-Zone 3/4: Warnung bei hohem Verbrauch
- Skill-Fehler: Warning bei --startup
- DB-Inkonsistenz: Error mit Repair-Vorschlag

TIPPS
-----
- --maintain Befehle regelmaessig ausfuehren
- Bei Problemen: bach --maintain heal --execute
- Token-Verbrauch im Auge behalten (Zone 2-3)
- Fehler-Logs bei Problemen pruefen

SIEHE AUCH
----------
  bach --help maintain         # Wartungs-Uebersicht
  bach --help startup          # Startup-Checks
  bach --help logs             # Log-System
  tools/TOOLS_CONCEPT.md       # Tool-Konzept

---
Version: 1.0.0
Erstellt: 2026-01-23
Teil von: BACH Tool-Dokumentation


## Ocr

OCR-TOOLS - Texterkennung mit Tesseract
=======================================

Stand: 2026-01-23
Pfad: docs/docs/docs/help/tools/ocr.txt

BESCHREIBUNG
------------
OCR-Engine fuer Texterkennung in Bildern und PDFs.
Verwendet Tesseract und ist von DokuZentrum Pro adaptiert.

Pfad: tools/ocr_engine.py

VORAUSSETZUNGEN
---------------
  - Tesseract installiert (tesseract-ocr)
  - Python-Pakete: pytesseract, Pillow
  - Optional: PyMuPDF (fitz) fuer PDF-Support

  Installation:
    pip install pytesseract Pillow PyMuPDF

VERWENDUNG
----------

CLI (einfach):
  python ocr_engine.py <pdf_path>
  python ocr_engine.py B0006              # Beleg-Kurzform

Python (Klasse):
  from tools.ocr_engine import OCREngine, OCRResult
  
  engine = OCREngine()
  
  # Verfuegbarkeit pruefen
  if engine.is_available:
      print("Tesseract verfuegbar!")
  
  # Bild erkennen
  result = engine.recognize_image("scan.png")
  print(result.text)
  
  # PDF erkennen
  pages = engine.recognize_pdf("dokument.pdf")
  for page in pages:
      print(f"Seite {page.page_num}: {page.text}")
  
  # Verfuegbare Sprachen
  langs = engine.get_available_languages()

HAUPTKLASSEN
------------

OCREngine:
  is_available            Tesseract verfuegbar?
  get_available_languages() Verfuegbare Sprachen auflisten
  recognize_image(path)   Text aus Bild extrahieren
  recognize_pdf(path)     Text aus PDF (auch Bild-PDFs)

OCRResult:
  success                 Erfolg (bool)
  text                    Erkannter Text
  confidence              Konfidenz-Wert (0-100)
  language                Verwendete Sprache
  error                   Fehlertext bei Misserfolg

OCRPageResult:
  page_num                Seitennummer
  text                    Seitentext
  confidence              Konfidenz
  word_count              Wortanzahl

SPRACHEN
--------
Standard: "deu+eng" (Deutsch + Englisch)

Andere Sprachen:
  engine.recognize_image("bild.png", language="fra")
  engine.recognize_pdf("doc.pdf", language="deu")

Mehrere Sprachen:
  language="deu+eng+fra"

BELEG-KURZFORM
--------------
Belegscans koennen mit Kurzform aufgerufen werden:

  python ocr_engine.py B0006

Sucht automatisch in:
  - user/steuer/belege/B0006.pdf
  - user/steuer/belege/B0006.png

INTEGRATION MIT STEUER-AGENT
----------------------------
Der Steuer-Agent nutzt die OCR-Engine um:
  - Rechnungsbetraege zu extrahieren
  - Belegdaten zu erkennen
  - Textdurchsuchbare PDFs zu erstellen

  bach steuer beleg scan B0006

FEHLERBEHEBUNG
--------------

"Tesseract nicht gefunden":
  - Tesseract installieren
  - Pfad in PATH aufnehmen
  - Oder: OCREngine(tesseract_path="C:/Program Files/...")

"pytesseract nicht installiert":
  pip install pytesseract

"PyMuPDF nicht verfuegbar":
  pip install PyMuPDF
  (Nur fuer PDF-Support noetig)

Schlechte Erkennung:
  - Bild-Qualitaet verbessern (DPI erhoehen)
  - Richtige Sprache waehlen
  - Bild vorverarbeiten (Kontrast, Skalenkorrektur)

SIEHE AUCH
----------
  docs/docs/docs/help/steuer.txt         Steuer-Agent mit OCR
  tools/steuer/           Steuer-Tools
  
  docs/MAIL_PROFILE_SYSTEM.md  E-Mail-basierte Belegerfassung

VERSION: v1.0.0 (2026-01-23)
Zeilen: ~323 (ocr_engine.py)


## Ocr Engine

BACH Tool: ocr_engine
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/ocr_engine.py

BESCHREIBUNG
----------------------------------------
BACH OCR Engine
===============
Texterkennung mit Tesseract.
Adaptiert von DokuZentrum Pro.

Usage:
    python ocr_engine.py <pdf_path>
    python ocr_engine.py B0006              # Beleg-Kurzform

VERWENDUNG
----------------------------------------
python bach.py tools run ocr_engine [args]
oder direkt: python tools/ocr_engine.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show ocr_engine


## Ollama Benchmark

BACH Tool: ollama_benchmark
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/ollama_benchmark.py

BESCHREIBUNG
----------------------------------------
Ollama Benchmark Analyse & Visualisierung

VERWENDUNG
----------------------------------------
python bach.py tools run ollama_benchmark [args]
oder direkt: python tools/ollama_benchmark.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show ollama_benchmark


## Ollama Summarize

BACH Tool: ollama_summarize
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/ollama_summarize.py

BESCHREIBUNG
----------------------------------------
Ollama Zusammenfassung von Session-Berichten

VERWENDUNG
----------------------------------------
python bach.py tools run ollama_summarize [args]
oder direkt: python tools/ollama_summarize.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show ollama_summarize


## Ollama Worker

BACH Tool: ollama_worker
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/ollama_worker.py

BESCHREIBUNG
----------------------------------------
OLLAMA WORKER - Async Job-Verarbeitung
======================================
Laueft im Hintergrund, verarbeitet Jobs aus pending/ via Ollama,
schreibt Ergebnisse nach completed/.

Usage:
  python ollama_worker.py          # Einmal alle pending Jobs verarbeiten
  python ollama_worker.py --daemon # Dauerhaft laufen

VERWENDUNG
----------------------------------------
python bach.py tools run ollama_worker [args]
oder direkt: python tools/ollama_worker.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show ollama_worker


## Os Generator

BACH Tool: os_generator
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/os_generator.py

BESCHREIBUNG
----------------------------------------
Universal LLM OS Structure Generator v3.0

Erstellt die komplette Basisstruktur für ein Universal LLM OS v3.0
basierend auf der Evolution der Erkenntnisse aus BACH_STREAM Analysen.

VERBESSERUNGEN gegenüber v2.0:
- _backup/ System (trash/, snapshots/) hinzugefügt
- Verbesserte Boot-Sequenz mit Backup-Check
- Session-Lifecycle Dokumentation erweitert
- Micro-Routines mit Backup-Integration
- Optimierte Shutdown-Protocol mit Backup-Phase

Die drei Säulen: MEMORY + TOOLS + COMMUNICATION

Autor: BACH_STREAM Generator
Datum: 2026-01-13
Version: 3.0.0

Verwendung:
    python os_generator_v3.py [name] [zielordner]
    
Beispiele:
    python os_generator_v3.py mein-os
    python os_generator_v3.py mein-os "C:\Projekte"

VERWENDUNG
----------------------------------------
python bach.py tools run os_generator [args]
oder direkt: python tools/os_generator.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show os_generator


## Partner

PARTNER-KOMMUNIKATION TOOLS - Partner-Erkennung und Message-Routing
===================================================================

Stand: 2026-01-23
Pfad: docs/docs/docs/help/tools/partner.txt

BESCHREIBUNG
------------
Diese Tools ermoeglichen die Kommunikation zwischen BACH und
externen Partnern (Ollama, Gemini, etc.), System-Analyse und 
automatisches Routing von Aufgaben.

Pfad: tools/partner_communication/

UEBERSICHT
----------

  Tool                        Zeilen   Funktion
  ─────────────────────────────────────────────────────────
  communication.py            678      Partner-Erkennung, Health-Checks
  system_explorer.py          458      OS-Software-Erkennung
  interaction_protocol.py     1225     Instanz-Handshake, DNA-Tracking
  ai_compatible.py            200      AI-kompatible Software filtern
  real_tools.py               198      Echte CLI-Tools identifizieren

  GESAMT: 5 Tools, ~2.759 Zeilen

───────────────────────────────────────────────────────────────

TOOL 1: communication.py
========================
Zentrales Tool fuer Partner-Erkennung und Message-Routing.

FUNKTIONEN:
  - Automatische Partner-Erkennung (Claude, Ollama, Gemini, etc.)
  - Health-Checks fuer Partner-Verfuegbarkeit
  - Token-aware Message-Routing
  - Partner-Status-Abfragen

VERWENDUNG (Python):
  from tools.partner_communication.communication import (
      detect_partners,
      check_health,
      route_message
  )
  
  # Partner erkennen
  partners = detect_partners()
  
  # Health pruefen
  status = check_health("ollama")
  
  # Nachricht routen
  route_message("Recherche-Aufgabe", target="gemini")

CLI (geplant):
  bach partner detect "Task-Beschreibung"
  bach partner health
  bach partner route --to gemini --message "..."

───────────────────────────────────────────────────────────────

TOOL 2: system_explorer.py
==========================
Scannt das Betriebssystem nach installierter Software.

FUNKTIONEN:
  - Windows Registry scannen
  - AI-kompatible Software identifizieren
  - Tool-Capabilities katalogisieren
  - Software-Inventar erstellen

VERWENDUNG (Python):
  from tools.partner_communication.system_explorer import (
      scan_system,
      get_ai_tools,
      list_capabilities
  )
  
  # System scannen
  software = scan_system()
  
  # Nur AI-Tools
  ai_tools = get_ai_tools()

CLI (geplant):
  bach partner scan
  bach partner scan --ai-only

───────────────────────────────────────────────────────────────

TOOL 3: interaction_protocol.py
===============================
Handshake und Protokolle zwischen BACH-Instanzen.

FUNKTIONEN:
  - Instanz-zu-Instanz Handshake
  - DNA-Tracking (Instanz-Identitaet)
  - 5 Interaktionsprotokolle:
    * Handshake - Gegenseitige Erkennung
    * Compare   - Faehigkeiten vergleichen
    * Request   - Import-Anfragen
    * Transfer  - Datenuebertragung
    * Receipt   - Empfangsbestaetigung

VERWENDUNG (Python):
  from tools.partner_communication.interaction_protocol import (
      initiate_handshake,
      execute_protocol
  )
  
  # Handshake starten
  result = initiate_handshake("gemini")
  
  # Protokoll ausfuehren
  execute_protocol("transfer", target="ollama", data=payload)

───────────────────────────────────────────────────────────────

TOOL 4: ai_compatible.py
========================
Filtert AI-kompatible Software aus dem System-Scan.

FUNKTIONEN:
  - Registry nach AI-Tools durchsuchen
  - LLM-Clients identifizieren (Ollama, LM Studio, etc.)
  - API-Endpoints erkennen
  - Capabilities extrahieren

VERWENDUNG (Python):
  from tools.partner_communication.ai_compatible import (
      scan_ai_software,
      get_llm_clients
  )
  
  ai_tools = scan_ai_software()
  llms = get_llm_clients()

───────────────────────────────────────────────────────────────

TOOL 5: real_tools.py
=====================
Identifiziert echte CLI-Tools fuer Delegation.

FUNKTIONEN:
  - EXE/CMD/BAT-Tools finden
  - Python-Scripts katalogisieren
  - Tool-Argumente analysieren
  - Delegations-Kandidaten ermitteln

VERWENDUNG (Python):
  from tools.partner_communication.real_tools import (
      find_cli_tools,
      analyze_tool
  )
  
  tools = find_cli_tools()
  info = analyze_tool("git")

───────────────────────────────────────────────────────────────

DATENBANK-INTEGRATION
---------------------
Die Tools nutzen folgende BACH-Tabellen:

  connections        Partner-Endpoints und URLs
  partner_recognition   Capabilities, Zonen, Status
  delegation_rules   Token-basierte Routing-Regeln
  comm_messages      Nachrichtenprotokoll

PARTNER-WORKSPACE
-----------------
  partners/
  ├── _TASKS.md           # Zentrale Task-Zuweisung
  ├── claude/
  │   ├── inbox/          # Eingehende Auftraege
  │   ├── outbox/         # Berichte
  │   └── workspace/      # Arbeitsdateien
  ├── gemini/
  └── ollama/

SIEHE AUCH
----------
  docs/docs/docs/help/partner.txt        Partner-System CLI-Befehle
  docs/docs/docs/help/partners.txt       Partner-Netzwerk Uebersicht
  docs/docs/docs/help/delegate.txt       Delegation-Details
  docs/docs/docs/help/communicate.txt    Kommunikationsprotokolle
  
  skills/_services/communicate.md   Skill-Definition
  tools/partner_communication/README.md   Entwickler-Doku

VERSION: v1.0.0 (2026-01-23)
Quelle: tools/partner_communication/README.md


## Path Healer

BACH Tool: path_healer
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/path_healer.py

BESCHREIBUNG
----------------------------------------
BACH Path Healer v1.0.0
Zentraler Pfad-Heilungs-Service fuer BACH

Basiert auf: RecludOS Unified Path Healer v2.3.0
Angepasst fuer BACH v1.1

Usage:
    python path_healer.py                    # Vollstaendiger Scan
    python path_healer.py --dry-run          # Nur pruefen
    python path_healer.py --target <pfad>    # Einzelne Datei
    python path_healer.py --report           # Report generieren

CLI (geplant):
    bach maintain heal                       # Vollstaendiger Scan
    bach maintain heal --dry-run             # Nur pruefen

VERWENDUNG
----------------------------------------
python bach.py tools run path_healer [args]
oder direkt: python tools/path_healer.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show path_healer


## Pattern Tool

BACH Tool: pattern_tool
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/pattern_tool.py

BESCHREIBUNG
----------------------------------------
pattern_tool.py - Dateinamen kuerzen durch Pattern-Erkennung
============================================================

Kombiniert pattern_renamer.py und pattern_trimmer.py in einem Tool.

Funktionen:
- PREFIX: Gemeinsame Prefixe bei Gruppen entfernen
- SUFFIX: Gemeinsame Suffixe bei Gruppen entfernen
- BOTH: Prefix und Suffix kombiniert

Usage:
    python pattern_tool.py <ordner> --dry-run
    python pattern_tool.py <ordner> --execute
    python pattern_tool.py <ordner> --prefix-only
    python pattern_tool.py <ordner> --suffix-only
    python pattern_tool.py <ordner> -m 5  # Min 5 Zeichen Pattern

Autor: BACH v1.1

VERWENDUNG
----------------------------------------
python bach.py tools run pattern_tool [args]
oder direkt: python tools/pattern_tool.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show pattern_tool


## Policies

POLICIES - Wiederverwendbare Code-Standards
==========================================

Stand: 2026-01-23
Pfad: docs/docs/docs/help/tools/policies.txt

BESCHREIBUNG
------------
Policies sind wiederverwendbare Code-Snippets die BACH-Standards
durchsetzen. Sie werden in neue Projekte injiziert und sorgen fuer
konsistente Handhabung von:
  - Encoding (UTF-8, Windows-Console)
  - JSON (Emoji-safe, Encoding-Fallback)
  - Dateinamen (Praefix-Konvention)

SPEICHERORT
-----------
  tools/_policies/
    encoding_header.py    UTF-8 und Console-Fix
    emoji_safe.py         Emoji-Konvertierung
    json_safe.py          Sichere JSON-Operationen
    CONCEPT_naming_convention.md   Namenskonvention (Konzept)

VERFUEGBARE POLICIES
====================

1. encoding_header (v1.0)
-------------------------
UTF-8 Encoding Header und Windows Console Fix.
Wird am Dateianfang injiziert.

INJIZIERT:
  - Shebang: #!/usr/bin/env python3
  - Encoding: # -*- coding: utf-8 -*-
  - Windows Console Encoding Fix

TYPISCHER CODE:
  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-

  import sys
  if sys.platform == 'win32':
      sys.stdout.reconfigure(encoding='utf-8', errors='replace')

2. emoji_safe (v1.0)
--------------------
Sichere Emoji-Handhabung fuer Speicherung/Transfer.

FUNKTIONEN:
  emoji_to_safe(text)      Emoji -> ASCII-safe (fuer DB/Files)
  emoji_to_display(text)   ASCII-safe -> Emoji (fuer Anzeige)

VERWENDUNG:
  from _policies.emoji_safe import emoji_to_safe
  safe_text = emoji_to_safe("Hello [TOOL]")  # -> "Hello :wrench:"

ABHAENGIGKEIT:
  Benoetigt: pip install emoji (optional, graceful fallback)

3. json_safe (v1.0)
-------------------
Sichere JSON-Operationen mit Emoji/Encoding-Handling.

FUNKTIONEN:
  json_load_safe(filepath)       Laedt mit Encoding-Fallback
  json_save_safe(data, filepath) Speichert mit Emoji-Konvertierung
  json_dumps_safe(data)          Serialisiert ensure_ascii=False

VERWENDUNG:
  from _policies.json_safe import json_load_safe, json_save_safe

  # Laden (probiert utf-8, utf-8-sig, latin-1, cp1252)
  data = json_load_safe("config.json")

  # Speichern (konvertiert Emojis zu :shortcodes:)
  json_save_safe(data, "config.json", convert_emojis=True)

POLICY-FORMAT
=============
Jede Policy hat folgenden Aufbau:

  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-
  """
  POLICY: name
  VERSION: 1.0
  SIZE: small/medium/large
  DESCRIPTION: Was macht die Policy
  """

  # === POLICY:name:version ===
  ... Code ...
  # === END:name ===

GROESENKLASSEN:
  small    -> Inline-Injection (wenige Zeilen)
  medium   -> Externe Datei (eigenes Modul)
  large    -> Mehrere Dateien

ATI PROJEKT-BOOTSTRAPPING
=========================
Policies werden vom ATI-Bootstrapper in neue Projekte injiziert:

  bach ati bootstrap my-tool --template python-cli

STANDARD-POLICIES fuer Python-CLI:
  - encoding_header (immer)
  - json_safe (wenn JSON verwendet)
  - emoji_safe (wenn Ausgabe an Console)

Siehe: agents/ati/ATI_PROJECT_BOOTSTRAPPING.md

NAMING CONVENTION (Konzept)
===========================
Geplante Namenskonvention fuer Tool-Dateien:

  c_  -> CLI-optimiert fuer AI (c_encoding_fixer.py)
  b_  -> BACH-Kern (b_backup.py)
  a_  -> Agent-Runner (a_entwickler.py)
  t_  -> Test-Tools (t_runner.py)
  m_  -> Maintain/Wartung (m_cleanup.py)
  g_  -> Generator-Tools (g_skill.py)

Status: KONZEPT - noch nicht implementiert
Siehe: tools/_policies/CONCEPT_naming_convention.md

EIGENE POLICY ERSTELLEN
=======================

1. Datei in tools/_policies/ erstellen
2. Policy-Header mit NAME, VERSION, SIZE, DESCRIPTION
3. Code zwischen # === POLICY:name:version === markieren
4. Optional: In project_bootstrapper.py registrieren

TYPISCHE ANWENDUNGSFAELLE
=========================

1. NEUES PYTHON-PROJEKT
   -> encoding_header automatisch injizieren

2. JSON-KONFIGURATION
   -> json_safe fuer sichere Speicherung

3. CONSOLE-AUSGABE MIT EMOJIS
   -> emoji_safe fuer Windows-Kompatibilitaet

4. BESTEHENDEN CODE STANDARDISIEREN
   -> c_standard_fixer nutzt Policies intern

SIEHE AUCH
----------
  bach --help tools/code_quality   Encoding/JSON-Fixer
  bach --help ati                  ATI Agent und Bootstrapping
  bach --help tools                Tool-Uebersicht


## Policy Applier

BACH Tool: policy_applier
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/policy_applier.py

BESCHREIBUNG
----------------------------------------
PolicyApplier - BACH Policy Management System
==============================================
Version: 1.0.0
Date: 2026-01-22

Task: BOOTSTRAP_010 - Phase 3.2: PolicyApplier Klasse und Validation-Checks

Funktion:
- Liest BACH-Policies aus _policies/ Ordnern
- Wendet Policies auf Projekte an
- Führt Validation-Checks durch
- Generiert Compliance-Reports

VERWENDUNG
----------------------------------------
python bach.py tools run policy_applier [args]
oder direkt: python tools/policy_applier.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show policy_applier


## Policy Control

BACH Tool: policy_control
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/policy_control.py

BESCHREIBUNG
----------------------------------------
policy_control.py - Zentrale Code-Snippet Injection

Injiziert standardisierte Code-Policies in Python-Projekte.
Unterstuetzt inline-Injection (kleine Snippets) und externe Dateien (grosse).

Usage:
    python policy_control.py <datei.py> --inject emoji_safe
    python policy_control.py <datei.py> --set standardfixer
    python policy_control.py <datei.py> --check emoji_safe
    python policy_control.py <ordner> --set standardfixer --recursive
    python policy_control.py --list
    python policy_control.py --list-sets

Autor: Claude
Version: 1.0

VERWENDUNG
----------------------------------------
python bach.py tools run policy_control [args]
oder direkt: python tools/policy_control.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show policy_control


## Problems First

BACH Tool: problems_first
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/problems_first.py

BESCHREIBUNG
----------------------------------------
Problems First - Automatische Fehler-Erkennung
==============================================

Von CHIAH nach BACH portiert.
Scannt Auto-Log und andere Quellen nach Problemen.

VERWENDUNG
----------------------------------------
python bach.py tools run problems_first [args]
oder direkt: python tools/problems_first.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show problems_first


## Production Agent

BACH Tool: production_agent
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/production_agent.py

BESCHREIBUNG
----------------------------------------
Production Agent v1.0.0

Content-Produktion: Musik, Podcast, Video, Text, Storys, PR.
Integriert externe KI-Tools und RecludOS Services.

Usage:
  python production_agent.py list
  python production_agent.py musik --prompt "Jazz instrumental"
  python production_agent.py video --prompt "Ocean waves"
  python production_agent.py recommend <category>

VERWENDUNG
----------------------------------------
python bach.py tools run production_agent [args]
oder direkt: python tools/production_agent.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show production_agent


## Python Cli Editor

BACH Tool: python_cli_editor
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/python_cli_editor.py

BESCHREIBUNG
----------------------------------------
python_cli_editor.py - Python Code Editor CLI v2.0

Analysiert und bearbeitet Python-Dateien strukturiert.
Zeigt Klassen, Methoden, Imports und ermoeglicht gezieltes Editieren.

Autor: Claude + Lukas
Version: 2.0.0
Datum: 2026-01-13

============================================================
NEUE FEATURES v2.0:
============================================================

ZEILENNUMMERN:
  --lines / --no-lines    Zeilennummern ein/aus (Default: on)

EINFUEGEN:
  --add CODE              Fuegt Code ein (aus Datei oder direkt)
  --at-start              Am Dateianfang (nach Imports)
  --at-end                Am Dateiende  
  --at-imports            Im Import-Bereich
  --in-class NAME         In Klasse NAME (am Ende)
  --before NAME           Vor Element NAME
  --after NAME            Nach Element NAME
  --at-line N             An Zeile N

LOESCHEN:
  --delete NAME           Loescht Klasse, Methode oder Funktion

ZEILEN BEARBEITEN:
  --change-line N         Zeile N bearbeiten (interaktiv oder mit --content)
  --content "CODE"        Neuer Inhalt fuer --change-line

SPEICHERN:
  --test                  Erstellt Testdatei ohne Original zu aendern
  --save                  Speichert direkt mit automatischem Backup

============================================================
BEISPIELE:
============================================================

# Struktur mit Zeilennummern anzeigen
python python_cli_editor.py script.py --show-all --lines

# Neue Funktion am Ende einfuegen
python python_cli_editor.py script.py --add new_func.py --at-end --save

# Methode in Klasse einfuegen
python python_cli_editor.py script.py --add method.py --in-class MyClass --save

# Import hinzufuegen
python python_cli_editor.py script.py --add "import os" --at-imports --save

# Klasse loeschen
python python_cli_editor.py script.py --delete MyClass --save

# Zeile aendern
python python_cli_editor.py script.py --change-line 42 --content "x = 100" --save

# Vor/Nach Element einfuegen
python python_cli_editor.py script.py --add helper.py --before MainClass --save
python python_cli_editor.py script.py --add cleanup.py --after process_data --save

============================================================

VERWENDUNG
----------------------------------------
python bach.py tools run python_cli_editor [args]
oder direkt: python tools/python_cli_editor.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show python_cli_editor


## Python Editing

PYTHON EDITING TOOLS - Python-Dateien bearbeiten
=================================================

Stand: 2026-01-23
Pfad: docs/docs/docs/help/tools/python_editing.txt

BESCHREIBUNG
------------
Tools zum Bearbeiten, Analysieren und Aufteilen von Python-Dateien.
Besonders nuetzlich fuer:
  - Grosse Python-Dateien (500+ Zeilen)
  - Code-Review und Refactoring
  - LLM-Kontextmanagement (Token sparen)
  - Strukturierte Code-Aenderungen

WICHTIG: PYTHON_CLI_EDITOR
==========================
Das Haupt-Tool fuer Python-Bearbeitung hat eine eigene, ausfuehrliche
Dokumentation wegen seiner Komplexitaet und Wichtigkeit:

  bach --help tools/python_cli_editor

Der python_cli_editor ist speziell fuer AI-Assistenten gebaut:
  - Struktur anzeigen statt ganze Datei lesen (Token sparen)
  - Gezielt Methoden/Klassen bearbeiten
  - Chirurgische Aenderungen statt komplette Rewrites

Kurzuebersicht python_cli_editor:
  bach python_cli_editor script.py --show-all      # Struktur anzeigen
  bach python_cli_editor script.py --show 50-80    # Zeilen 50-80
  bach python_cli_editor script.py --imports       # Nur Imports
  bach python_cli_editor script.py --classes       # Nur Klassen
  bach python_cli_editor script.py --add code.py --in-class MyClass --save

Fuer Details: bach --help tools/python_cli_editor

PYCUTTER: c_pycutter
====================
Zerlegt grosse Python-Dateien in separate Textdateien pro Klasse.

ANWENDUNGSFAELLE:
  - Code-Review: Jede Klasse einzeln betrachten
  - LLM-Kontext: Nur relevante Klasse laden
  - Dokumentation: Klassen-weise Doku erstellen
  - Refactoring: Uebersicht bei grossen Dateien

GRUNDBEFEHLE:

  # Datei aufteilen (erstellt Unterordner)
  bach c_pycutter main.py

  # In bestimmten Ordner ausgeben
  bach c_pycutter main.py --output-dir ./extracted

  # JSON-Output (fuer Weiterverarbeitung)
  bach c_pycutter main.py --json

OPTIONEN:
  --output-dir DIR   Ausgabe-Verzeichnis
  --json             JSON-Output statt Dateien

AUSGABE-STRUKTUR:
  main_20260123_120000/
    Hilfsfunktionen.txt    # Imports, globale Funktionen
    KlasseA.txt            # Code von class KlasseA
    KlasseB.txt            # Code von class KlasseB
    ...

BEISPIEL-WORKFLOW:
  # 1. Grosse Datei aufteilen
  bach c_pycutter riesige_app.py --output-dir ./review
  
  # 2. Einzelne Klasse bearbeiten
  # (in separatem Editor oder mit python_cli_editor)
  
  # 3. Aenderungen zurueck uebernehmen
  # (manuell oder mit Diff-Tool)

METHOD ANALYZER: c_method_analyzer
==================================
Tiefgehende Analyse von Python-Code auf Probleme und Struktur.

FUNKTIONEN:
  - Methoden-Inventar (alle Methoden mit Zeilennummern)
  - Aufruf-Analyse (welche Methode ruft welche auf)
  - Import-Pruefung (genutzt vs. ungenutzt)
  - Tippfehler-Erkennung (aehnliche Namen)
  - Signal-Connect-Pruefung (Qt/Tk)
  - Attribut-vor-Init Erkennung

GRUNDBEFEHLE:

  # Datei analysieren
  bach c_method_analyzer script.py

  # JSON-Output
  bach c_method_analyzer script.py --json

  # Nur Zusammenfassung
  bach c_method_analyzer script.py --summary

  # Bestimmte Klasse analysieren
  bach c_method_analyzer script.py --class MyClass

OPTIONEN:
  --json           JSON-Output (maschinenlesbar)
  --summary        Nur kompakte Zusammenfassung
  --class NAME     Nur bestimmte Klasse analysieren
  --verbose        Detaillierte Ausgabe

AUSGABE-BEISPIEL:
  === METHOD ANALYZER: script.py ===
  
  [KLASSEN]
    MyClass (Zeile 15-120)
      - __init__ (17)
      - process_data (35)
      - _helper (80)  <- nie aufgerufen!
  
  [POTENZIELLE PROBLEME]
    Zeile 42: self._hepler() - Tippfehler? Meinten Sie: _helper
    Zeile 67: self.button.connect(self.on_click) - on_click nicht gefunden
  
  [UNGENUTZTE IMPORTS]
    - import json (Zeile 3)
  
  [STATISTIK]
    Klassen: 2
    Methoden: 15
    Zeilen: 320

TYPISCHE WORKFLOWS
==================

1. GROSSE DATEI VERSTEHEN
   Erst Struktur, dann Details:
   
   # Ueberblick bekommen
   bach python_cli_editor grosse_datei.py --show-all
   
   # Oder aufteilen fuer Review
   bach c_pycutter grosse_datei.py

2. PROBLEME VOR COMMIT FINDEN
   Code analysieren:
   
   bach c_method_analyzer script.py
   
   Zeigt: Tippfehler, ungenutzte Methoden, fehlende Referenzen

3. REFACTORING VORBEREITEN
   Abhaengigkeiten verstehen:
   
   # Wer ruft wen auf?
   bach c_method_analyzer script.py --verbose
   
   # Klasse isoliert betrachten
   bach c_pycutter script.py

4. TOKEN SPAREN (AI-Kontext)
   Statt ganze Datei lesen:
   
   # Nur Struktur laden
   bach python_cli_editor script.py --show-all
   
   # Dann gezielt die relevante Methode
   bach python_cli_editor script.py --show 150-180

WANN WELCHES TOOL?
==================

| Aufgabe                      | Tool                |
|------------------------------|---------------------|
| Struktur anzeigen            | python_cli_editor   |
| Gezielt Code aendern         | python_cli_editor   |
| Datei in Teile zerlegen      | c_pycutter          |
| Probleme/Bugs finden         | c_method_analyzer   |
| Imports pruefen              | c_method_analyzer   |
| Tippfehler finden            | c_method_analyzer   |

CONTEXT-INJEKTOR
----------------
Der ContextInjector erkennt Stichwoerter und empfiehlt diese Tools:

  "python bearbeiten"  -> bach python_cli_editor <datei> --show-all
  "klasse bearbeiten"  -> bach python_cli_editor <datei> --show-all
  "methode bearbeiten" -> bach python_cli_editor <datei> --show-all
  "code struktur"      -> bach python_cli_editor <datei> --show-all
  "datei aufteilen"    -> bach c_pycutter <datei>
  "zu gross"           -> bach c_pycutter <datei>

SIEHE AUCH
----------
  bach --help tools/python_cli_editor  Ausfuehrliche Editor-Doku (WICHTIG!)
  bach --help tools/imports            Import-Handling
  bach --help tools/code_quality       Code-Qualitaet (Encoding etc.)
  bach --help tools/analysis           Weitere Analyse-Tools


## Register Skills

BACH Tool: register_skills
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/register_skills.py

BESCHREIBUNG
----------------------------------------
Skills in bach.db registrieren
==============================
Scannt skills/ Ordner und registriert alle Skill-Dateien in der DB.

VERWENDUNG
----------------------------------------
python bach.py tools run register_skills [args]
oder direkt: python tools/register_skills.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show register_skills


## Registry Watcher

BACH Tool: registry_watcher
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/registry_watcher.py

BESCHREIBUNG
----------------------------------------
BACH Registry Watcher v1.0.0

Automatische Ueberwachung und Konsistenzpruefung aller System-Registries.
Portiert von RecludOS, integriert mit BACH Database-System.

Features:
- Existenz-Pruefung: Registrierte Eintraege vs Dateisystem
- Syntax-Validierung: JSON-Dateien
- Cross-Reference: DB-Eintraege vs Dateien
- Health-Reports generieren
- Benachrichtigung bei Problemen

Usage:
  python registry_watcher.py check              # Alle Registries pruefen
  python registry_watcher.py report             # Health-Report erstellen
  python registry_watcher.py tools              # Nur Tools pruefen
  python registry_watcher.py skills             # Nur Skills pruefen
  python registry_watcher.py agents             # Nur Agents pruefen
  python registry_watcher.py --fix              # Probleme automatisch beheben (sicher)

VERWENDUNG
----------------------------------------
python bach.py tools run registry_watcher [args]
oder direkt: python tools/registry_watcher.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show registry_watcher


## Reports

BACH Tool: reports
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/reports.py

BESCHREIBUNG
----------------------------------------
reports.py - Erstellt Änderungsreports für andere Steuerroutinen

Generiert lesbare Markdown-Reports aus Verzeichnisänderungen.
Speichert in: reports/<alias>_changes_<datum>.md

Usage:
    python reports.py <alias>
    python reports.py skills

VERWENDUNG
----------------------------------------
python bach.py tools run reports [args]
oder direkt: python tools/reports.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show reports


## Research

RESEARCH-TOOLS - Wissenschaftliche Recherche
============================================

Stand: 2026-01-23
Pfad: docs/docs/docs/help/tools/research.txt

BESCHREIBUNG
------------
Research Agent fuer wissenschaftliche Literaturrecherche.
Integriert verschiedene externe Recherche-Tools und
strukturiert den Review-Prozess.

Pfad: tools/research_agent.py

VERFUEGBARE EXTERNE TOOLS
-------------------------
Der Research Agent empfiehlt und verlinkt:

  PubMed         Biomedizinische Literatur (NIH)
  Perplexity     AI-gestuetzte Recherche mit Quellen
  Consensus      Wissenschaftliche Evidenz-Suche
  NotebookLM     Google-Tool zum Clustern/Analysieren
  Elicit         AI-Research-Assistent
  Scite          Zitationsanalyse mit Kontext

VERWENDUNG
----------

CLI-Befehle:
  python research_agent.py search "query"
  python research_agent.py review --topic "topic" --years 5
  python research_agent.py status

Beispiele:
  python research_agent.py search "CRISPR gene therapy"
  python research_agent.py review --topic "Depression biomarkers" --years 3
  python research_agent.py status

SEARCH-BEFEHL
-------------
Fuehrt Recherche durch und empfiehlt passende Tools.

  python research_agent.py search "BRCA1 mutation breast cancer"

Ausgabe:
  - Empfohlene Tools basierend auf Keywords
  - Direkte URLs zu den Suchportalen
  - Historie wird gespeichert

Keyword-Erkennung:
  - gene, protein, disease, clinical -> PubMed
  - study, evidence, research -> Consensus
  - Allgemein -> Perplexity

REVIEW-BEFEHL
-------------
Erstellt strukturierten Literatur-Review-Plan.

  python research_agent.py review --topic "Depression vs Fatigue" --years 5

5-Phasen-Plan:
  1. Ueberblick (5 min)     - Perplexity fuer Kontext
  2. Systematische Suche    - PubMed + Consensus (15 min)
  3. Screening (10 min)     - NotebookLM fuer Clustering
  4. Volltext-Analyse       - Claude/Gemini (20 min)
  5. Synthese (10 min)      - Zusammenfassung + Gaps

Output-Verzeichnis:
  user/services_output/research/

STATUS-BEFEHL
-------------
Zeigt Agent-Status und Historie.

  python research_agent.py status

Ausgabe:
  - Version
  - Anzahl Suchen gesamt
  - Letzte Suche
  - Verfuegbare Tools

PYTHON-INTEGRATION
------------------
from tools.research_agent import ResearchAgent

agent = ResearchAgent()

# Suche starten
result = agent.search("Alzheimer biomarkers")
for rec in result["recommendations"]:
    print(f"{rec['tool']}: {rec['url']}")

# Review-Plan erstellen
plan = agent.create_review_plan("Depression", years=3)

# Status abrufen
status = agent.get_status()

WORKFLOW BEISPIEL
-----------------
Typischer Recherche-Workflow:

1. THEMA DEFINIEREN
   python research_agent.py search "depression fatigue differentiation"

2. REVIEW-PLAN ERSTELLEN
   python research_agent.py review --topic "Depression vs Fatigue" --years 5

3. TOOLS NUTZEN (manuell)
   - PubMed: Systematische Suche
   - Consensus: Evidenz-Auswertung
   - NotebookLM: PDFs clustern

4. ERGEBNISSE SPEICHERN
   Output in: user/services_output/research/

CACHE UND HISTORIE
------------------
Suchanfragen werden gespeichert:
  tools/cache/search_history.json

Letzte 100 Suchen werden aufbewahrt.

INTEGRATION MIT BACH
--------------------
Der Research Agent ist Teil des BACH-Ecosystems:

  bach tool suggest research     # Tool-Info
  bach --help tools/research     # Diese Hilfe

Zukuenftig geplant:
  bach research "query"          # Direkter CLI-Zugang
  bach research plan "topic"     # Review-Plan

SIEHE AUCH
----------
  wiki/ai_portable.txt      AI Portable RAG-Pipeline
  docs/docs/docs/help/tools/partner.txt         Partner-Tools (Perplexity-Integration)
  docs/docs/docs/help/delegate.txt              Delegation an Research-Partner

  PubMed:     https:/pubmed.ncbi.nlm.nih.gov/
  Perplexity: https:/www.perplexity.ai/
  Consensus:  https:/consensus.app/

VERSION: v1.0.0 (2026-01-23)
Zeilen: ~205 (research_agent.py)


## Research Agent

BACH Tool: research_agent
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/research_agent.py

BESCHREIBUNG
----------------------------------------
Research Agent v1.0.0

Wissenschaftliche Recherche und Literaturanalyse.
Integriert PubMed, Perplexity, Consensus und NotebookLM.

Usage:
  python research_agent.py search "query"
  python research_agent.py review --topic "topic" --years 5
  python research_agent.py status

VERWENDUNG
----------------------------------------
python bach.py tools run research_agent [args]
oder direkt: python tools/research_agent.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show research_agent


## Skills

BACH SKILLS TOOLS
=================

Tools zur Verwaltung, Ueberwachung und Validierung von BACH-Skills.

SCHNELLSTART
------------
  bach --maintain skills                    # Skill-Gesundheitscheck
  bach skill list                          # Skills auflisten
  bach skill export NAME                   # Skill exportieren

WAS SIND SKILLS?
----------------
Skills sind wiederverwendbare Faehigkeiten-Module in BACH:
- _agents/: Boss-Agenten (ATI, Steuer-Agent, etc.)
- _experts/: Experten-Skills (data-analysis, etc.)
- _services/: Service-Skills (communicate, recurring, etc.)

SKILL HEALTH MONITOR
--------------------
Ueberwacht und validiert alle Skills.

Befehle:
  python tools/maintenance/skill_health_monitor.py check
  python tools/maintenance/skill_health_monitor.py check --skills
  python tools/maintenance/skill_health_monitor.py check --agents
  python tools/maintenance/skill_health_monitor.py report

Was wird geprueft:
- SKILL.md Vollstaendigkeit (name, version, description)
- Agent-Manifest (manifest.json)
- Verzeichnisstruktur
- Verwaiste oder fehlerhafte Skills

Integration in --startup:
Der Skill Health Monitor laeuft automatisch bei Session-Start
und meldet Probleme in der Startup-Ausgabe.

SKILL EXPORT/IMPORT
-------------------
Skills koennen exportiert und auf anderen Systemen installiert werden.

Export:
  bach skill export SKILLNAME
  -> Erstellt SKILLNAME.zip mit allen Dateien + manifest.json

Import:
  bach skill install PFAD/skill.zip
  -> Entpackt und integriert in skills/

ATI EXPORT (Agent-spezifisch):
  bach ati export
  -> Exportiert ATI-Agent mit allen Abhaengigkeiten

SKILL-VERZEICHNISSTRUKTUR
-------------------------
skills/
├── SKILL.md               # Haupt-SKILL.md (BACH selbst)
├── AGENT_KONVENTION.md    # Agent-Regeln
├── SKILL_ANALYSE.md       # Abdeckungsanalyse
│
├── _agents/               # Boss-Agenten
│   ├── ati/              # Software-Entwickler-Agent
│   ├── steuer-agent.txt  # Steuer-Agent
│   └── ...
│
├── _experts/              # Experten-Module
│   └── data-analysis/    # Datenanalyse-Expert
│
└── _services/             # Hintergrunddienste
    ├── communicate.md    # Partner-Kommunikation
    └── recurring/        # Periodische Tasks

SKILL.MD FORMAT
---------------
Jede SKILL.md muss YAML-Frontmatter haben:

---
name: skill-name
version: 1.0.0
description: Kurze Beschreibung
last_updated: 2026-01-23
---

# Skill-Name

Inhalt und Dokumentation...

VALIDIERUNG
-----------
Pflichtfelder: name, version, description
Empfohlen: last_updated, author, dependencies

Agenten brauchen zusaetzlich:
- manifest.json (PFLICHT)
- README.md (empfohlen)
- CHANGELOG.md (empfohlen)

DATENBANK-INTEGRATION
---------------------
Skills werden in bach.db registriert:

  SELECT * FROM skills;                    # Alle Skills
  SELECT * FROM agents;                    # Alle Agenten
  SELECT * FROM agent_synergies;           # Agent-Beziehungen

CLI-BEFEHLE
-----------
  bach --maintain skills      # Gesundheitscheck (in --startup)
  bach skill list             # Skills aus DB auflisten
  bach skill export NAME      # Skill exportieren
  bach skill install PFAD     # Skill installieren

TIPPS
-----
- Skill Health Monitor laeuft bei jedem --startup
- Probleme werden als Warnings/Errors gemeldet
- Bei neuen Skills: SKILL.md mit korrektem Frontmatter erstellen
- Agenten immer mit manifest.json erstellen

SIEHE AUCH
----------
  bach --help agents           # Agenten-Dokumentation
  bach --help ati              # ATI-Agent Details
  bach --help maintain         # Wartungs-Tools
  skills/AGENT_KONVENTION.md   # Agent-Regeln

---
Version: 1.0.0
Erstellt: 2026-01-23
Teil von: BACH Tool-Dokumentation


## Structure Generator

BACH Tool: structure_generator
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/structure_generator.py

BESCHREIBUNG
----------------------------------------
structure_generator.py
======================
Generiert Skill- und Agent-Strukturen auf einem Spektrum.

Version: 1.0.0
Erstellt: 2026-01-14
Vereint: skill_generator_v3.py + agent_generator_v1.py

KONZEPT:
  Skill und Agent sind ein Spektrum, keine harten Kategorien.
  Von der einfachsten Teilfähigkeit bis zum vollständigen Orchestrator.

PROFILE (aufsteigend):
  MICRO       = Nur Datei(en), kein Ordnersystem (absolute Teilfähigkeit)
  LIGHT       = Minimale Struktur (SKILL.md + _config + _data)
  STANDARD    = Skill mit einfachem Memory
  EXTENDED    = Skill mit Mikro-Skills
  AGENT       = Orchestriert Skills zu Workflows
  AGENT_FULL  = Vollständiger Agent (näher am OS)

MODI:
  --embedded   = Für Nutzung innerhalb eines OS (leichtgewichtig)
  --standalone = Für externe Nutzung (vollständig, default)

Verwendung:
    python structure_generator.py <name> <profil> [zielordner] [--embedded|--standalone]
    
Beispiele:
    python structure_generator.py analyse MICRO
    python structure_generator.py recherche STANDARD
    python structure_generator.py schreib-assistent AGENT
    python structure_generator.py projekt-manager AGENT_FULL

Für OS → os_generator.py
Für Export → exporter.py

VERWENDUNG
----------------------------------------
python bach.py tools run structure_generator [args]
oder direkt: python tools/structure_generator.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show structure_generator


## Success Tracker

BACH Tool: success_tracker
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/success_tracker.py

BESCHREIBUNG
----------------------------------------
Success Tracker - Basis-Implementation
RecludOS v3.1.1

Trackt Erfolgsmetriken fuer die 6 Akteur-Kategorien.

VERWENDUNG
----------------------------------------
python bach.py tools run success_tracker [args]
oder direkt: python tools/success_tracker.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show success_tracker


## Sync Utils

BACH Tool: sync_utils
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/sync_utils.py

BESCHREIBUNG
----------------------------------------
BACH Sync Utilities v1.0
========================
Zentrale Funktionen fuer Datei-Hashing und Aenderungserkennung.

Verwendung:
  from tools.sync_utils import file_hash, content_hash, has_changed, SyncTracker

VERWENDUNG
----------------------------------------
python bach.py tools run sync_utils [args]
oder direkt: python tools/sync_utils.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show sync_utils


## Task Statistics

BACH Tool: task_statistics
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/task_statistics.py

BESCHREIBUNG
----------------------------------------
task_statistics.py - Statistik-Auswertung für _done.json

Analysiert erledigte Tasks und liefert:
- Tasks pro Woche
- Aufwand-Verteilung
- Sessions pro Tag
- Tool-Aktivität

Version: 1.0
Erstellt: 2026-01-10

VERWENDUNG
----------------------------------------
python bach.py tools run task_statistics [args]
oder direkt: python tools/task_statistics.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show task_statistics


## Token Monitor

BACH Tool: token_monitor
==================================================
Generiert: 2026-01-23 10:36
Aktualisiert: 2026-02-05 (Help-Forensik)
Quelle: tools/token_monitor.py

BESCHREIBUNG
----------------------------------------
BACH Token Monitor
==================
Funktion get_token_zone() zur Token-aware Delegation.

Zonen-Definition (aus DELEG_002):
- Zone 1: 0-70%   - Alle Partner verfuegbar
- Zone 2: 70-85%  - Mittlere Sparsamkeit
- Zone 3: 85-95%  - Nur lokale Partner (Ollama)
- Zone 4: 95-100% - Notfall-Delegation

Version: 1.0.0
Erstellt: 2026-01-23
Task: DELEG_001

VERWENDUNG
----------------------------------------
Hauptbefehl (empfohlen):
  bach --tokens status         - Zeigt Token-Statistiken und aktuelle Zone

Direktaufruf:
  python tools/token_monitor.py [args]

Hinweis: Der Befehl "bach tools run token_monitor" ist aktuell nicht
im Tool-Registry registriert. Nutze stattdessen "bach --tokens status".

VERFUEGBARE FUNKTIONEN
----------------------------------------
get_token_zone()           - Hauptfunktion fuer Zone-Ermittlung
get_current_budget_percent() - Holt aktuelles Budget aus DB
log_token_check()          - Loggt Token-Check in DB
log_ollama_usage()         - Spezialisiert fuer Ollama-Tokens
check_emergency_shutdown() - Prueft ob kritischer Verbrauch (95%+) erreicht
format_zone_status()       - Formatiert CLI-Ausgabe

HINWEISE
----------------------------------------
- Bei Fragen: bach tools show token_monitor
- Datenbank-Tabelle: monitor_tokens (17 Spalten)


## Tool Discovery

BACH Tool: tool_discovery
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/tool_discovery.py

BESCHREIBUNG
----------------------------------------
tool_discovery.py - Problem-basierte Tool-Empfehlung
=====================================================

Analysiert Problembeschreibungen und empfiehlt passende BACH-Tools.

Usage:
    python tool_discovery.py suggest "encoding problem mit umlauten"
    python tool_discovery.py list-patterns
    python tool_discovery.py --json

Autor: BACH v1.1
Version: 1.0.0
Erstellt: 2026-01-21

VERWENDUNG
----------------------------------------
python bach.py tools run tool_discovery [args]
oder direkt: python tools/tool_discovery.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show tool_discovery


## Tool Registry Boot

BACH Tool: tool_registry_boot
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/tool_registry_boot.py

BESCHREIBUNG
----------------------------------------
Boot Integration für Tool Registry
===================================

Wird beim RecludOS Boot-Prozess aufgerufen.
Lädt alle Tool-Registries in den globalen Context.

Version: 1.0.0

VERWENDUNG
----------------------------------------
python bach.py tools run tool_registry_boot [args]
oder direkt: python tools/tool_registry_boot.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show tool_registry_boot


## Tool Scanner

BACH Tool: tool_scanner
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/tool_scanner.py

BESCHREIBUNG
----------------------------------------
tool_scanner.py - Scannt System nach verfuegbaren CLI-Tools
===========================================================

Findet installierte Tools und vergleicht mit registrierten Tools.
Nuetzlich fuer Tool-Discovery und System-Inventar.

Usage:
    python tool_scanner.py scan           # System scannen
    python tool_scanner.py --json         # JSON-Output
    python tool_scanner.py compare        # Mit Registry vergleichen

Autor: BACH v1.1 (basiert auf partner_scanner.py)

VERWENDUNG
----------------------------------------
python bach.py tools run tool_scanner [args]
oder direkt: python tools/tool_scanner.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show tool_scanner


## Universal Compiler

BACH Tool: universal_compiler
==================================================
Generiert: 2026-01-23 10:36
Quelle: tools/universal_compiler.py

BESCHREIBUNG
----------------------------------------
UNIVERSAL COMPILER v2.0
Kompiliert Python-Projekte zu EXE mit PyInstaller.
Liest Konfiguration aus AUFGABEN.txt oder nutzt Auto-Detect.

Erstellt: 03.01.2026

VERWENDUNG
----------------------------------------
python bach.py tools run universal_compiler [args]
oder direkt: python tools/universal_compiler.py [args]

HINWEISE
----------------------------------------
- Automatisch generiert aus Docstring
- Bei Fragen: bach tools show universal_compiler
