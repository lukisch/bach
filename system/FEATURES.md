# Feature-Analyse: BACH v2 Vanilla

## Projektübersicht

**Projektname:** BACH v2 Vanilla (Best-of BATCH + CHIAH)
**Version:** 2.1.0
**Status:** Development
**Typ:** Personal Agentic Operating System

BACH ist ein persönliches, portables Betriebssystem für KI-Agenten, das als Orchestrierungs- und Verwaltungsschicht für große Sprachmodelle (Claude, Gemini, Ollama) fungiert.

---

## Kernfeatures

### 1. Kognitives Memory-Modell (5-Typen)

- **Working Memory:** Kurzzeit/Session-Notizen
- **Episodic Memory:** Abgeschlossene Sessions, Tagebuch
- **Semantic Memory:** Fakten, Wiki, Help-Inhalte
- **Procedural Memory:** Tools, Skills, Workflows
- **Associative Memory:** Konsolidierung, Trigger

### 2. Aktive Konsolidierung

- KI-Gedächtnis mit automatischem "Vergessen" und "Lernen"
- Lernvorgänge explizit speichern (Lessons Learned)
- Session-Tracking und Konsolidierungs-Pipeline

### 3. Multi-Partner Delegation

- Netzwerk von Partner-Modellen (Claude, Gemini, lokale LLMs)
- Chat-System für Multi-LLM Kommunikation
- Automatisches Lock-System für Datei-Koordination
- Partner-Awareness und Presence-Tracking

### 4. CLI-First + GUI

- Nahtlose Terminal-Steuerung (Hauptfokus)
- Optional: FastAPI-basiertes Web-Dashboard
- Seitenloses Design, komplette Terminal-Bedienbarkeit

### 5. Portable und Lokal

- SQLite-Datenbank, keine Cloud-Abhängigkeiten
- 100% Kontrolle über Daten
- Plug-and-Play Installation
- Selbstheilung durch automatische Pfad-Korrektur

### 6. Domain-Agenten (15+ Spezialisten)

- Autonomous Agents für spezialisierte Aufgaben
- Experten für Fachbereiche
- Services für Cross-Domain Funktionen

### 7. Self-Healing

- Automatische Pfad-Korrektur
- System-Registry und Verifikation
- Integritätsprüfung (Identity Seal)

---

## Technologie-Stack

### Programmiersprachen
- **Python 3.x** (100%)

### Frameworks und Bibliotheken
- **FastAPI** - Web-Framework für Dashboard/API
- **SQLite3** - Datenbank-Engine
- **Pathlib** - Cross-Platform Dateisystem
- **Pydantic** - Datenvalidierung
- **Uvicorn** - ASGI-Server
- **Anthropic SDK** - Claude API Integration

### Datenbank
- **bach.db** (SQLite) mit 27+ Tabellen
- Kategorien: System, Tasks, Memory, Tools, Skills, Agents, Files, Automation, Monitoring, Connections, Languages

### Externe Integrationen
- Claude API (Anthropic)
- Gemini API (Google)
- Ollama (lokale Modelle)
- OCR Tools (Tesseract)
- ELSTER (deutsche Steuerverwaltung)
- Banking APIs (CAMT-Parser)

---

## Architektur

### Schichtenmodell

```
USER INTERFACES
  ├── CLI/Terminal (bach.py)
  ├── GUI/Browser (server.py)
  └── MCP/IDE (mcp_server.py)
       │
HUB LAYER (~62 Handler-Module)
  ├── System: startup, shutdown, status
  ├── Domain: steuer, abo, haushalt, gesundheit
  ├── Data: task, memory, db, session, logs
  └── Multi-AI: agents, partner, ati, daemon
       │
SKILLS LAYER
  ├── _agents/ (Autonome Agenten)
  ├── _experts/ (Domain-Experten)
  ├── _services/ (Allgemeine Services)
  └── _workflows/ (~25 Prozessabläufe)
       │
DATA LAYER
  ├── bach.db (SQLite)
  └── FileSystem
```

### Verzeichnisstruktur

```
BACH_ROOT/
├── system/
│   ├── bach.py (CLI Entry Point)
│   ├── data/ (Datenbanken, Logs)
│   ├── gui/ (FastAPI Dashboard)
│   ├── hub/ (~62 Handler-Module)
│   └── skills/ (Tools, Agents, Experts)
├── docs/ (Dokumentation)
├── system/system/system/system/exports/ (Generierte Exporte)
├── extensions/ (Third-Party Tools)
└── user/ (User-Daten)
```

---

## Handler-Module (Hub-Layer)

### System-Handler (~10)
startup.py, shutdown.py, status.py, backup.py, tokens.py, db.py, logs.py

### Domain-Handler (~8)
steuer.py, abo.py, haushalt.py, gesundheit.py, contact.py, doc.py, bericht.py

### Data-Handler (~8)
task.py, memory.py, lesson.py, context.py, session.py, wiki.py, inbox.py, fs.py

### Multi-AI Handler (~6)
agents.py, ati.py, daemon.py, partner.py, chain.py, consolidation.py

### Services Layer (~13)
daemon/, financial/, household/, document/, recurring/, wiki/, mail/, market/, scheduling/

---

## CLI-Befehle (Auszug)

### System
```
python bach.py --startup [--mode=text|gui|dual]
python bach.py --shutdown
python bach.py status [detail]
python bach.py backup [create|restore|list]
```

### Aufgabenmanagement
```
bach task list
bach task add "Titel"
bach task done <id>
```

### Memory-Management
```
bach mem write "Notiz"
bach mem read [n]
bach mem fact "key:value"
bach mem search "keyword"
```

### Multi-Partner
```
bach msg send <partner> "Text"
bach msg read <id>
bach llm lock <datei>
bach llm status
```

### Domain-spezifisch
```
bach steuer scan
bach haushalt inventory
bach abo list
bach gesundheit import
```

---

## Konfiguration

### Startup-Modi
- **gui** - GUI Dashboard + Browser (Standard)
- **text** - Nur CLI/Terminal
- **dual** - GUI + Terminal
- **silent** - Nichts automatisch starten

### Path-Verwaltung (bach_paths.py)
- Single Source of Truth für alle Pfade
- Self-Healing: Pfade relativ zum Script berechnet
- get_path(name) für einfachen Zugriff

### Skill-Architektur (v2.0)
Komponenten-Typen:
| Typ | Ordner | Charakteristik |
|-----|--------|----------------|
| Agent | _agents/ | Orchestriert Experten |
| Expert | _experts/ | Tiefes Domänenwissen |
| Service | _services/ | Allgemein, Handler-nah |
| Workflow | _workflows/ | 1 Datei = 1 Workflow |
| Tool | tools/ | Wiederverwendbar |

---

## Automation und Injektoren

### 4 Kognitive Injektoren
| Injektor | Funktion |
|----------|----------|
| strategy_injector | Metakognition, Entscheidungen |
| context_injector | Aufgaben-Erinnerung, Tool-Empfehlung |
| between_injector | Qualitätskontrolle, Task-Übergänge |
| time_injector | Zeitgefühl, Nachrichten-Check |

---

## Domain-Agenten

### Aktive Agenten
| Agent | Fokus |
|-------|-------|
| ATI | Software-Entwicklung, Task Scanner |
| Persönlicher-Assistent | Briefings, Kalender |
| Büro-Assistent | Dokumente, Mails |
| Entwickler | GitHub, Code-Review |
| Gesundheits-Assistent | Import, Reports |
| Versicherungen | Verträge, Claims |
| Production | Media/Studio |
| Research | Recherche, Analyse |

### Spezialisierte Experten (~18)
- steuer (Steuererklärung)
- aboservice (Abonnements)
- foerderplaner (Förderungen)
- haushaltsmanagement (Budget)
- gesundheitsverwalter (Medical records)
- psycho-berater (Psychological support)
- report_generator (Reports)

---

## Besondere Merkmale

### Kognitive Memory-Architektur
Human-inspired 5-Teil Memory-System mit aktiver Konsolidierung

### Multi-Partner Lock-System
```
bach llm lock <datei>    # Lock VORM Schreiben
bach llm unlock [datei]  # Lock freigeben
bach llm status          # Alle Locks zeigen
```

### Self-Healing und Path Correction
- Alle Pfade relativ vom Script-Standort berechnet
- Gegen directory_truth.json validiert
- Fehlende Verzeichnisse neu erstellt

### Workflow-TÜV und Quality Assurance
```
bach tuev status        # TÜV-Status aller Workflows
bach tuev check <wf>    # Einzelnen prüfen
bach usecase run <case> # Testfall ausführen
```

### Spezialisierte Domain-Features
- **Steuer:** OCR-Scanning, ELSTER-Export
- **Haushalt:** Inventar, Einkaufslisten
- **Gesundheit:** Health-Data Import, Tracking
- **ATI:** Headless AI-Sessions, Project Bootstrapper

---

## Zusammenfassung

BACH v2 Vanilla ist ein hochmodernes, modulares KI-Betriebssystem mit:

- Professioneller Hub+Handler+Skills-Architektur
- Intelligenter 5-Teil Memory-Verwaltung
- Multi-Agent Koordination (Claude, Gemini, Ollama)
- Vollständiger Automation (Workflows, Trigger, Injektoren)
- Selbstheilendem System
- 15+ Domain-Experten
- CLI-First + Optional GUI
- 100% Lokal und Portable

**Ideal für:** Power-User und Entwickler, die ein vollständiges KI-Betriebssystem mit Hub-basierter Orchestrierung benötigen.

---

*Erstellt: 2026-02-05*
*System: BACH Feature-Analyse*
