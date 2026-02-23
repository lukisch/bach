# BACH System Architecture

> Design-Manifest und Architektur-Dokumentation

**Version:** 1.1.73
**Stand:** 2026-01-29
**Zielgruppe:** Entwickler, Kontributoren, fortgeschrittene Nutzer

---

## Inhaltsverzeichnis

1. [Vision & Philosophie](#vision--philosophie)
2. [Systemuebersicht](#systemuebersicht)
3. [Kernprinzipien](#kernprinzipien)
4. [Architektur-Diagramme](#architektur-diagramme)
5. [Komponenten](#komponenten)
6. [Datenfluss](#datenfluss)
7. [Erweiterbarkeit](#erweiterbarkeit)
8. [Konventionen](#konventionen)

---

## Schnellnavigation (fuer LLMs)

> **Tipp:** Wenn du eine Aufgabe in BACH loesen willst, schaue ZUERST hier:

| Was suchst du? | Wo findest du es? | Dateien |
|---|---|---|
| **Befehls-Hilfe** | `help/*.txt` | 93 Help-Dateien zu allen BACH-Befehlen |
| **Hintergrundwissen** | `wiki/*.txt` | Artikel zu Konzepten und Methoden |
| **Arbeitsablaeufe** | `skills/workflows/*.md` | 24 Schritt-fuer-Schritt Anleitungen |
| **Neue Skills erstellen** | `_templates/` | Vorlagen fuer Handler, Tools, Agents |
| **Python-API** | `hub/*.py` | 73 Handler (CLI-Module) |
| **Daten & DB** | `data/` | bach.db, Configs, Exporte |
| **KI-Agenten** | `agents/` | 11 Boss-Agenten, 17 Experten |
| **Tools** | `skills/tools/*.py` | Standalone Python-Tools |

**WICHTIG:** Nutze immer Forward-Slashes (`C:/Users/...`) oder Unix-Pfade (`/c/Users/...`) in Bash-Befehlen. Windows-Backslashes (`C:\Users\...`) fuehren zu Fehlern!

---

## Vision & Philosophie

### Was ist BACH?

BACH ist ein **textbasiertes Betriebssystem fuer KI-Agenten**.
Es fungiert als Middleware zwischen Mensch und KI.

```
+-----------------------------------------------------------------+
|                                                                 |
|    "BACH = OS/Framework | Agenten = Plugins"                   |
|                                                                 |
|    Wie ein Betriebssystem fuer KI-Assistenten:                 |
|    - Dateisystem-Abstraktion                                   |
|    - Speicherverwaltung (Memory)                               |
|    - Prozess-Koordination (Tasks, Partner)                     |
|    - Konfiguration & Persistenz (DB)                           |
|                                                                 |
+-----------------------------------------------------------------+
```

### Herkunft

BACH ist das "Best-of" aus drei Vorgaengersystemen:

```
  +-------------+     +-------------+     +-------------+
  |    BATCH    |     |    CHIAH    |     |  RecludOS   |
  |  (Hub,      |     |  (CLI,      |     |  (Agenten,  |
  |   Sessions) |     |   Help)     |     |   Healing)  |
  +------+------+     +------+------+     +------+------+
         |                   |                   |
         +-------------------+-------------------+
                             |
                             v
                    +-----------------+
                    |      BACH       |
                    |   (Best-of)     |
                    +-----------------+
```

### Design-Philosophie

```
+-----------------------------------------------------------------+
|  PRINZIP                 |  BEDEUTUNG                           |
|-----------------------------------------------------------------|
|  Database-First          |  Alles in SQLite, keine JSONs       |
|  Text-basiert            |  .txt Dateien fuer Transparenz      |
|  Hub & Handler           |  Zentrale CLI, modulare Handler     |
|  Selbstheilung          |  Automatische Konsistenzpruefung     |
|  Partner-faehig          |  Multi-Agent Zusammenarbeit         |
+-----------------------------------------------------------------+
```

---

## Systemuebersicht

### High-Level Architektur

```
                        +--------------------------------+
                        |           NUTZER               |
                        |     (Mensch oder KI-Agent)     |
                        +---------------+----------------+
                                        |
                                        v
+-----------------------------------------------------------------------+
|                              CLI LAYER                                 |
|  +------------------------------------------------------------------+ |
|  |                        bach.py (Hub)                             | |
|  |  - Argument Parsing                                              | |
|  |  - Handler Routing                                               | |
|  |  - Error Handling                                                | |
|  +------------------------------------------------------------------+ |
+-----------------------------------------------------------------------+
                                        |
                    +-------------------+-------------------+
                    |                   |                   |
                    v                   v                   v
+------------------------+ +------------------------+ +------------------------+
|   HANDLER LAYER        | |   HANDLER LAYER        | |   HANDLER LAYER        |
|  +------------------+  | |  +------------------+  | |  +------------------+  |
|  |  TaskHandler     |  | |  |  MemoryHandler   |  | |  |  HelpHandler     |  |
|  |  StartupHandler  |  | |  |  BackupHandler   |  | |  |  WikiHandler     |  |
|  |  ShutdownHandler |  | |  |  SnapshotHandler |  | |  |  PartnerHandler  |  |
|  |  ...             |  | |  |  ...             |  | |  |  ...             |  |
|  +------------------+  | |  +------------------+  | |  +------------------+  |
+------------------------+ +------------------------+ +------------------------+
                    |                   |                   |
                    +-------------------+-------------------+
                                        |
                                        v
+-----------------------------------------------------------------------+
|                           DATA LAYER                                   |
|  +------------------------------------------------------------------+ |
|  |                      data/bach.db (SQLite)                       | |
|  |                                                                   | |
|  |  +----------+ +----------+ +----------+ +----------+             | |
|  |  |  tasks   | |  memory_ | |  tools   | |  files_  |             | |
|  |  |          | |  working | |          | |  trash   |             | |
|  |  +----------+ +----------+ +----------+ +----------+             | |
|  |  +----------+ +----------+ +----------+ +----------+             | |
|  |  | lessons_ | | memory_  | | partner_ | | boot_    |             | |
|  |  | learned  | | sessions | | recogni..| | checks   |             | |
|  |  +----------+ +----------+ +----------+ +----------+             | |
|  |                        (32+ Tabellen)                            | |
|  +------------------------------------------------------------------+ |
+-----------------------------------------------------------------------+
```

---

## Kernprinzipien

### 1. Database-First (DATENBANK VOR JSON)

```
+-----------------------------------------------------------------+
|  REGEL: Daten gehoeren in die Datenbank, nicht in JSON.         |
|                                                                  |
|  AUSNAHMEN (alle muessen zutreffen):                            |
|  - Nutzer-spezifisch (wird bei Neuinstallation neu erstellt)    |
|  - Transparenz wichtig (Nutzer soll editieren koennen)          |
|  - Prozess-Charakter (Import/Export, temporaer)                 |
|  - Schema-Validierung (wenn vorhanden)                          |
|                                                                  |
|  GRUND: RecludOS-Lesson - JSON-Wildwuchs = Inkonsistenz         |
+-----------------------------------------------------------------+
```

### 2. Hub & Handler Pattern

```
                        +-------------+
                        |   bach.py   |
                        |    (Hub)    |
                        +------+------+
                               |
         +---------------------+---------------------+
         |                     |                     |
         v                     v                     v
+-----------------+  +-----------------+  +-----------------+
|  TaskHandler    |  |  MemoryHandler  |  |  BackupHandler  |
|  (task.py)      |  |  (memory.py)    |  |  (backup.py)    |
+-----------------+  +-----------------+  +-----------------+

Jeder Handler:
- Erbt von BaseHandler
- Hat profile_name Property
- Implementiert handle(operation, args)
- Ist fuer genau einen Befehlsbereich zustaendig
```

### 3. Textbasierte Transparenz

```
+-----------------------------------------------------------------+
|  FORMAT       |  VERWENDUNG              |  BEISPIEL            |
|-----------------------------------------------------------------|
|  .txt         |  Dokumentation, Help     |  skills/docs/docs/docs/help/tasks.txt      |
|  .md          |  Navigation, Skills      |  SKILL.md            |
|  .py          |  Code                    |  bach.py             |
|  .sql         |  Schema                  |  SCHEMA.sql          |
|  .json        |  NUR Ausnahmen!          |  config.json         |
|  .db          |  Alle Daten              |  bach.db             |
+-----------------------------------------------------------------+
```

### 4. Selbstheilungs-Module

```
+-----------------------------------------------------------------+
|                    SELBSTHEILUNG                                 |
|                                                                  |
|  +-----------------+     +-----------------+                    |
|  | Registry Watcher|     | Skill Health    |                    |
|  | (DB-Tabellen)   |     | Monitor         |                    |
|  +--------+--------+     +--------+--------+                    |
|           |                       |                              |
|           +-----------+-----------+                              |
|                       v                                          |
|              +-----------------+                                |
|              |   --startup     |                                |
|              |  (Auto-Check)   |                                |
|              +-----------------+                                |
|                                                                  |
|  Bei Session-Start werden automatisch geprueft:                 |
|  - DB-Tabellen vorhanden?                                       |
|  - Skills konsistent?                                           |
|  - Pfade korrekt?                                               |
+-----------------------------------------------------------------+
```

---

## Architektur-Diagramme

### DIAGRAMM 1: Backend-Architektur
Technische Ebene: Handler, Tools, Datenbanken, Delegation

```
                        BACH BACKEND ARCHITEKTUR
  ========================================================================

  +--------------------------+          +---------------------------+
  |    bach.py (CLI Entry)   |          |   gui/server.py (FastAPI) |
  |   37 Befehle registriert |          |   REST API + WebSocket    |
  +-----------+--------------+          +------------+--------------+
              |                                      |
              +------------------+-------------------+
                                 |
                    +------------v-------------+
                    |     HUB / HANDLERS       |
                    |     (hub/*.py)            |
                    +--------------------------+
                    | System:                  |
                    |   startup, shutdown,     |
                    |   status, context,       |
                    |   backup, tokens, sync   |
                    +--------------------------+
                    | Domain:                  |
                    |   steuer, abo, haushalt,  |
                    |   gesundheit, contact,   |
                    |   calendar, routine      |
                    +--------------------------+
                    | Data:                    |
                    |   task, memory, db,      |
                    |   session, logs, wiki    |
                    +--------------------------+
                    | Multi-AI:                |
                    |   agents, partner,       |
                    |   daemon, ollama, ati    |
                    +-----+----------+---------+
                          |          |
              +-----------+          +----------+
              |                                 |
  +-----------v-----------+      +--------------v--------------+
  |    TOOLS (skills/tools/*.py) |      |   DATENBANKEN               |
  +-----------------------+      +-----------------------------+
  | c_ocr_engine.py       |      | bach.db (System)            |
  | data_importer.py      |      |   tasks, memory_lessons,    |
  | folder_diff_scanner.py|      |   skills, tools, config,    |
  | doc_search.py         |      |   automation_triggers       |
  | cv_generator.py       |      +-----------------------------+
  | mcp_server.py         |      | bach.db (Unified seit v1.1.84)|
  | autolog.py            |      |   fin_insurances,           |
  | backup_manager.py     |      |   fin_contracts,            |
  | injectors.py          |      |   health_*, household_*,    |
  +-----------------------+      |   assistant_contacts,       |
                                 |   steuer_*, abo_*           |
  +-----------------------+      +-----------------------------+
  |  PARTNER / DELEGATION |
  +-----------------------+      +-----------------------------+
  | partners/claude/       |      | DATEISYSTEM                 |
  | partners/gemini/       |      |   ../user/ (User-Ordner)       |
  |   inbox/ outbox/      |      |   memory/ (Archiv)          |
  | partners/ollama/       |      |   logs/ (Sessions)          |
  | MCP Server (extern)   |      |   skills/docs/docs/docs/help/ (Wiki)              |
  +-----------------------+      +-----------------------------+
```

---

### DIAGRAMM 2: Frontend-Architektur (Inhaltliche Ebene)
Agenten, Experten, Services, Skills, Workflows, Usecases

```
                      BACH FRONTEND ARCHITEKTUR
                      (Inhaltliche/Funktionale Ebene)
  ========================================================================

  USER / USECASE
  +---------------------------------------------------------------+
  | "Importiere meine Arztberichte"                                |
  | "Zeige meine Versicherungskosten"                              |
  | "Erstelle Steuer-Export Vorsorgeaufwand"                       |
  +-------------------------------+-------------------------------+
                                  |
                                  v
  AGENTEN (agents/)
  +---------------------------------------------------------------+
  | Persoenlicher Assistent | Gesundheitsassistent                 |
  | Bueroassistent          | Finanz-Assistent                     |
  | ATI (Autonomer Agent)   | (erweiterbar)                        |
  +-------------------------------+-------------------------------+
                                  |
                    steuern & delegieren
                                  |
                                  v
  EXPERTEN (agents/_experts/)
  +---------------------------------------------------------------+
  | steuer/            | gesundheitsverwalter/ | aboservice/        |
  | financial_mail/    | health_import/        | report_generator/  |
  | haushaltsmanagement/| foerderplaner/       | data-analysis/     |
  | psycho-berater/    | wikiquizzer/          | (14 Experten)      |
  +-------------------------------+-------------------------------+
                                  |
                    nutzen & ueberwachen
                                  |
                                  v
  WORKFLOWS (skills/workflows/)        METAKOGNITION
  +----------------------------------+  +-------------------------+
  | steuer_workflow.md               |  | ROADMAP.md (Vision)     |
  | health_import_workflow.md        |  | CHANGELOG.md (Historie) |
  | abo_detection_workflow.md        |  | BUGLOG.md (Probleme)    |
  | document_scan_workflow.md        |  | Memory-System (Lernen)  |
  | mail_analysis_workflow.md        |  +-------------------------+
  +----------------------------------+
                  |
                  v
  SERVICES (skills/_services/)     +    TOOLS (skills/tools/*.py)
  +----------------------------------+  +-------------------------+
  | daemon/ (Hintergrund-Sessions)   |  | c_ocr_engine.py (OCR)   |
  | document/ (PDF, OCR, Scanner)    |  | data_importer.py        |
  | mail/ (E-Mail-Verwaltung)        |  | folder_diff_scanner.py  |
  | market/ (Analyse)                |  | doc_search.py           |
  | prompt_generator/                |  | cv_generator.py         |
  | recurring/ (Wiederkehrend)       |  | mcp_server.py           |
  +----------------------------------+  +-------------------------+
                  |                                |
                  +--------------------------------+
                  |
                  v
  DATEN (Quellen & Ziele)
  +---------------------------------------------------------------+
  | LESEN:                                                         |
  |   bach.db (Unified DB), JSON-Configs                            |
  |   User-Ordner in BACH (../user/steuer/, ../user/gesundheit/)         |
  |   Definierte Ordner ausserhalb BACH (Dokumente/, Arztsachen/)  |
  +---------------------------------------------------------------+
  | SCHREIBEN:                                                     |
  |   bach.db (strukturierte Daten)                                |
  |   User-Ordner in BACH (Exporte, Berichte)                      |
  |   Export-Ordner (../user/steuer/2025/export/)                     |
  |   Definierte Ordner ausserhalb BACH                            |
  +---------------------------------------------------------------+
  | ERGEBNISSE:                                                    |
  |   .txt Berichte (cleaner look, CLI-freundlich)                 |
  |   .csv Exporte (Steuer, Daten)                                 |
  |   DB-Eintraege (strukturierte Speicherung)                     |
  |   GUI-Praesentation (Dashboard, Charts)                        |
  +---------------------------------------------------------------+
```

---

### DIAGRAMM 3: Gesamtarchitektur (Backend + Frontend + GUI)
Alle Ebenen zusammen mit Verknuepfungen

```
                        BACH v1.1 GESAMTARCHITEKTUR
  ========================================================================

  +=====================================================================+
  |                         USER-INTERFACES                              |
  |                                                                      |
  |  +-------------------+    +-------------------+    +---------------+ |
  |  |   CLI (Terminal)  |    | GUI (Browser)     |    | MCP (IDE)     | |
  |  |   bach.py         |    | gui/server.py     |    | mcp_server.py | |
  |  |   "bach task list"|    | localhost:5000     |    | bach://tasks  | |
  |  +--------+----------+    +--------+----------+    +-------+-------+ |
  +===========|========================|========================|========+
              |                        |                        |
              +------------------------+------------------------+
                                       |
  +====================================v====================================+
  |                          HUB LAYER (hub/*.py)                           |
  |                                                                         |
  |  System        Domain          Data            Multi-AI                 |
  |  --------      --------        --------        --------                 |
  |  startup       steuer          task            agents                   |
  |  shutdown      abo             memory          partner                  |
  |  status        haushalt        db              daemon                   |
  |  context       gesundheit      session         ollama                   |
  |  backup        contact         logs            ati                      |
  |  tokens        calendar        wiki                                     |
  |  inject        routine         docs                                     |
  |  scan          bericht         inbox                                    |
  +====================================+====================================+
                                       |
          +----------------------------+----------------------------+
          |                            |                            |
  +-------v--------+     +------------v------------+     +---------v--------+
  | SKILLS LAYER   |     |     TOOLS LAYER         |     |   DATA LAYER     |
  |                |     |                          |     |                  |
  | agents/        |     | c_ocr_engine.py          |     | bach.db          |
  |   ATI          |     | data_importer.py          |     |   tasks          |
  |   4 Agenten    |     | folder_diff_scanner.py    |     |   memory         |
  |   _experts/    |     | doc_search.py              |     |   skills/tools   |
  |   14 Experten  |     | cv_generator.py            |     |   config         |
  |                |     | scanner_service.py         |     |                  |
  | _services/     |     | autolog.py                  |     | bach.db (Unified)|
  |   daemon       |     | backup_manager.py           |     |   fin_*          |
  |   document     |     | injectors.py                |     |   health_*       |
  |   mail         |     |                             |     |   household_*    |
  |                |     +-----------------------------+     |   steuer_*       |
  | workflows/     |                                         |   assistant_*    |
  |   .md Dateien  |     +-----------------------------+     |   abo_*          |
  |   Anleitungen  |     |   PARTNER LAYER             |     |                  |
  +----------------+     |                             |     | Dateisystem      |
                          | partners/claude/            |     |   ../user/          |
                          |   inbox/ outbox/            |     |   memory/        |
                          | partners/gemini/            |     |   logs/          |
                          |   inbox/ outbox/ prompts/   |     |   skills/wiki/     |
                          | partners/ollama/            |     |                  |
                          +-----------------------------+     | Externe Ordner   |
                                                              |   Dokumente/     |
                                                              |   Arztsachen/    |
                                                              |   Versicherungen/|
                                                              +------------------+

  DATENFLUSS:
  ===========
  CLI/GUI/MCP --> Hub Handler --> Skills/Tools --> Datenbanken
                                              --> Dateisystem
                                              --> Partner-LLMs

  PRINZIPIEN:
  ===========
  1. CLI First   - Alles ueber Terminal steuerbar
  2. Systemisch  - Wiederverwendbar fuer jeden User
  3. dist_type   - 0=User, 1=Template, 2=Core (Daten-Isolation)
  4. Idempotent  - Importe wiederholbar ohne Duplikate
```

---

### DIAGRAMM 4: Memory-System (Kognitives Modell)

```
  VERGLEICH: Menschliches Gedaechtnis  <-->  BACH Memory-System
  ================================================================

  MENSCH                              BACH / LLM
  ------                              ----------

  +---------------------+             +-------------------------+
  |  ARBEITSGEDAECHTNIS  |             |  memory_working (47)    |
  |  "Was tue ich gerade"|             |  Scratchpad, Notizen    |
  |  ~7 Einheiten,       |             |  bach mem write "..."   |
  |  Sekunden-Minuten    |  <------->  |  Fluechttig, pro Session|
  |                      |             |  Typ: scratchpad/note   |
  +----------+-----------+             +----------+--------------+
             | Konsolidierung                      | bach mem archive
             v                                     v
  +---------------------+             +-------------------------+
  |  EPISODISCHES        |             |  memory_sessions (354)  |
  |  GEDAECHTNIS         |             |  Session-Berichte       |
  |  "Was habe ich       |             |  bach --memory session  |
  |   erlebt"            |  <------->  |  Wer/Was/Wann/Ergebnis  |
  |  Autobiografisch     |             |  continuation_context   |
  +----------+-----------+             +----------+--------------+
             | Abstraktion                         | Lessons Learned
             v                                     v
  +---------------------+             +-------------------------+
  |  SEMANTISCHES        |             |  memory_facts (174)     |
  |  GEDAECHTNIS         |             |  + memory_lessons (68)  |
  |  "Was weiss ich"     |             |  + skills/docs/docs/docs/help/, wiki/         |
  |  Fakten, Konzepte,   |  <------->  |  Fakten, Erkenntnisse,  |
  |  Weltwissen          |             |  Dokumentation          |
  +----------+-----------+             +----------+--------------+
             |                                     |
             v                                     v
  +---------------------+             +-------------------------+
  |  PROZEDURALES        |             |  skills/tools/ (77 Scripts)    |
  |  GEDAECHTNIS         |             |  skills/ (255 Eintraege)|
  |  "Wie mache ich es"  |             |  workflows/ (24)        |
  |  Automatismen,       |  <------->  |  _services/ (25+)       |
  |  Fertigkeiten        |             |  hub/ (CLI-Handler)     |
  +----------+-----------+             +----------+--------------+
             |                                     |
             v                                     v
  +---------------------+             +-------------------------+
  |  ASSOZIATIVES        |             |  memory_consolidation   |
  |  GEDAECHTNIS         |             |  (357 Eintraege)        |
  |  "Was gehoert        |             |  + Injektoren           |
  |   zusammen"          |  <------->  |  + trigger_words        |
  |  Verknuepfungen      |             |  + Kontext-Suche        |
  +----------------------+             +-------------------------+


  AKTIVE PROZESSE (wie beim Menschen)
  ====================================

  MENSCH                              BACH
  ------                              ----

  Vergessen (Decay)         <-->      Konsolidierung: Alte Working-Memory
                                      Eintraege verlieren Gewicht, werden
                                      archiviert oder geloescht.

  Erinnern (Retrieval)      <-->      Injektoren: Keywords triggern
                                      automatisch relevantes Wissen.
                                      bach --memory search "..."

  Lernen (Encoding)         <-->      memory_lessons: Erkenntnisse aus
                                      Sessions werden als Lessons gespeichert.
                                      bach lesson add "Titel: Erkenntnis"

  Aufmerksamkeit (Focus)    <-->      memory_context: Gereifter Kontext
                                      wird bei Session-Start injiziert.
                                      Fokussiert auf Relevantes.

  Schlaf-Konsolidierung     <-->      bach --shutdown: Session-Bericht
                                      wird gespeichert, Working Memory
                                      archiviert, Kontext konsolidiert.

  Metakognition             <-->      Workflows + Strategien: "Weiss ich
  ("Weiss ich, was ich                genug?" -> skills/docs/docs/docs/help/ nachschlagen.
   nicht weiss?")                     "Welches Tool?" -> bach tools search


  DATENFLUSS (Memory-Lifecycle)
  ==============================

  Eingabe --> Working Memory --> Konsolidierung --> Facts/Lessons
                    |                                     |
                    | (Session-Ende)                       | (Permanent)
                    v                                     v
              Session-Bericht                     Injektoren/Kontext
              (Episodisch)                        (Semantisch)
                    |                                     |
                    +--------> Suche <--------------------+
                                  |
                                  v
                          Relevanter Kontext
                          fuer naechste Session
```

---

### Datenbankschema (Auszug)

```
+---------------------------------------------------------------------+
|                          bach.db SCHEMA                              |
|---------------------------------------------------------------------|
|                                                                      |
|  CORE TABLES                           MEMORY TABLES                |
|  ------------                          -------------                |
|  +------------------+                  +------------------+         |
|  |      tasks       |                  |  memory_working  |         |
|  |------------------|                  |------------------|         |
|  | id INTEGER PK    |                  | id INTEGER PK    |         |
|  | title TEXT       |                  | content TEXT     |         |
|  | status TEXT      |                  | timestamp TEXT   |         |
|  | priority TEXT    |                  | session_id TEXT  |         |
|  | project TEXT     |                  +------------------+         |
|  | assigned_to TEXT |                                               |
|  | depends_on TEXT  |                  +------------------+         |
|  +------------------+                  |  memory_facts    |         |
|                                        |------------------|         |
|  +------------------+                  | id INTEGER PK    |         |
|  |      tools       |                  | key TEXT UNIQUE  |         |
|  |------------------|                  | value TEXT       |         |
|  | id INTEGER PK    |                  | category TEXT    |         |
|  | name TEXT UNIQUE |                  +------------------+         |
|  | type TEXT        |                                               |
|  | category TEXT    |                  +------------------+         |
|  | path TEXT        |                  | lessons_learned  |         |
|  | capabilities TEXT|                  |------------------|         |
|  +------------------+                  | id INTEGER PK    |         |
|                                        | title TEXT       |         |
|  PARTNER TABLES                        | content TEXT     |         |
|  --------------                        | category TEXT    |         |
|  +------------------+                  | created_at TEXT  |         |
|  |partner_recognition|                  +------------------+         |
|  |------------------|                                               |
|  | id INTEGER PK    |                  +------------------+         |
|  | name TEXT        |                  | memory_sessions  |         |
|  | type TEXT        |                  |------------------|         |
|  | capabilities TEXT|                  | id INTEGER PK    |         |
|  | allowed_zones TXT|                  | session_id TEXT  |         |
|  +------------------+                  | summary TEXT     |         |
|                                        | tasks_created INT|         |
|  +------------------+                  | tasks_completed  |         |
|  | delegation_rules |                  +------------------+         |
|  |------------------|                                               |
|  | id INTEGER PK    |                                               |
|  | zone INTEGER     |                                               |
|  | partner TEXT     |                                               |
|  | allowed BOOLEAN  |                                               |
|  +------------------+                                               |
|                                                                      |
+---------------------------------------------------------------------+
```

---

### Handler-Hierarchie

```
                    BaseHandler (base.py)
                          |
        +-----------------+-----------------+
        |                 |                 |
        v                 v                 v
  SessionHandlers    DataHandlers      SystemHandlers
        |                 |                 |
   +----+----+      +----+----+      +----+----+
   |         |      |         |      |         |
Startup  Shutdown  Memory  Task   Backup  Maintain
Handler  Handler   Handler Handler Handler Handler
```

---

### Skills & Agents Struktur

```
agents/                          # KI-Agenten (Top-Level)
+-- ati/                         # Software-Entwicklung
|   +-- SKILL.md
|   +-- manifest.json
|   +-- skills/tools/
+-- foerderplaner/               # Paedagogik
+-- haushalt/                    # Haushalts-Verwaltung
+-- _experts/                    # Domain-Experten
    +-- steuer-experte.txt
    +-- datev-experte.txt

skills/
+-- _services/                   # Hintergrund-Services
|   +-- wiki/                    # Wiki-Autoren Service
|   +-- skills/docs/docs/docs/help/                    # Help-Forensik Service
|   +-- recurring/               # Recurring Tasks
|
+-- workflows/                   # Arbeitsablaeufe (ehem. _workflows/_protocols)
    +-- wiki-author.md
    +-- help-forensic.md
    +-- bugfix-protokoll.md

connectors/                      # Konnektoren (Top-Level)

partners/                        # Partner-LLMs (Top-Level)
+-- claude/
+-- gemini/
+-- ollama/
```

---

## Datenfluss

### Session-Lifecycle

```
+---------------------------------------------------------------------+
|                         SESSION LIFECYCLE                            |
|---------------------------------------------------------------------|
|                                                                      |
|  1. STARTUP                                                         |
|  +----------------------------------------------------------------+ |
|  |  bach --startup                                                 | |
|  |                                                                 | |
|  |  -> Selbstheilungs-Checks (Registry, Skills)                   | |
|  |  -> Token-Zone ermitteln                                       | |
|  |  -> Nachrichten pruefen                                        | |
|  |  -> Offene Tasks laden                                         | |
|  |  -> Recurring Tasks pruefen                                    | |
|  |  -> Session-ID generieren                                      | |
|  +----------------------------------------------------------------+ |
|                              |                                       |
|                              v                                       |
|  2. ARBEITEN                                                        |
|  +----------------------------------------------------------------+ |
|  |  Tasks erstellen/bearbeiten                                     | |
|  |  Memory schreiben/lesen                                         | |
|  |  Help konsultieren                                              | |
|  |  Partner delegieren                                             | |
|  |  ...                                                            | |
|  +----------------------------------------------------------------+ |
|                              |                                       |
|                              v                                       |
|  3. SHUTDOWN                                                        |
|  +----------------------------------------------------------------+ |
|  |  bach --shutdown "Summary"                                      | |
|  |                                                                 | |
|  |  -> Dir-Scan (Aenderungen erfassen)                            | |
|  |  -> Task-Statistik berechnen                                   | |
|  |  -> Session-Bericht speichern                                  | |
|  |  -> Auto-Snapshot (wenn >= 3 Aenderungen)                      | |
|  |  -> Autolog schreiben                                          | |
|  +----------------------------------------------------------------+ |
|                                                                      |
+---------------------------------------------------------------------+
```

---

### Token-Zone System

```
+---------------------------------------------------------------------+
|                      TOKEN-ZONE DELEGATION                           |
|---------------------------------------------------------------------|
|                                                                      |
|  Token-Verbrauch    Zone    Erlaubte Partner                        |
|  ---------------    ----    -----------------                       |
|      0 - 70%        1       Alle (Gemini, Ollama, Copilot, ...)    |
|     70 - 85%        2       Mittel (Ollama, lokale LLMs)           |
|     85 - 95%        3       Nur lokal (Ollama)                     |
|     95 - 100%       4       NOTFALL (nur kritische Ops)            |
|                                                                      |
|                                                                      |
|   Token-Budget                                                       |
|   ------------                                                       |
|   ##########..........  50% -> Zone 1 (alle Partner)               |
|   ##############......  75% -> Zone 2 (eingeschraenkt)             |
|   ##################..  90% -> Zone 3 (nur lokal)                  |
|   ####################  100% -> Zone 4 (Notfall)                   |
|                                                                      |
+---------------------------------------------------------------------+
```

---

## Erweiterbarkeit

### Neuen Handler erstellen

```python
# hub/handlers/my_handler.py

from pathlib import Path
from .base import BaseHandler

class MyHandler(BaseHandler):
    """Handler fuer meinen Befehl"""

    def __init__(self, base_path: Path):
        super().__init__(base_path)

    @property
    def profile_name(self) -> str:
        return "mycommand"

    @property
    def target_file(self) -> Path:
        return self.base_path / "data"

    def get_operations(self) -> dict:
        return {
            "list": "Alle anzeigen",
            "add": "Neuen Eintrag erstellen",
        }

    def handle(self, operation: str, args: list, dry_run: bool = False):
        if operation == "list":
            return self._list()
        elif operation == "add":
            return self._add(args)
        return False, f"Unbekannte Operation: {operation}"
```

### Neuen Agent erstellen

```
agents/mein_agent/
+-- SKILL.md              # Dokumentation (PFLICHT)
+-- manifest.json         # Metadaten
+-- skills/tools/
    +-- main_tool.py
```

---

## Konventionen

### Namenskonventionen

```
+-----------------------------------------------------------------+
|  TYP              |  PRAEFIX     |  BEISPIEL                    |
|-----------------------------------------------------------------|
|  Handler          |  *Handler    |  TaskHandler                 |
|  Service          |  *_service   |  wiki_author                 |
|  Tool             |  <kategorie>_|  c_method_analyzer           |
|  Help-Datei       |  <thema>.txt |  tasks.txt                   |
|  Wiki-Artikel     |  <thema>.txt |  icf.txt                     |
|  Konzept          |  CONCEPT_*   |  CONCEPT_delegation.md       |
|  Protocol         |  <name>.md   |  wiki-author.md              |
+-----------------------------------------------------------------+
```

### Ordnerstruktur-Regeln

```
BACH_ROOT/
+-- hub/handlers/      # CLI-Handler (NICHT woanders)
+-- agents/            # KI-Agenten (Top-Level)
|   +-- _experts/      # Domain-Experten (unter agents/)
+-- skills/            # Services, Protocols, Tools
|   +-- tools/         # Standalone-Tools
|   +-- _services/     # Hintergrund-Services
|   +-- workflows/     # Arbeitsablaeufe (ehem. _workflows/_protocols)
+-- connectors/        # Konnektoren (Top-Level)
+-- partners/          # Partner-LLMs (Top-Level)
+-- skills/docs/docs/docs/help/              # Dokumentation (KI-optimiert)
|   +-- wiki/          # Hintergrundwissen
+-- ../docs/              # Entwickler-Dokumentation (Menschen)
+-- ../user/              # Nutzer-spezifische Daten
+-- data/              # Datenbanken
+-- logs/              # Protokolle
+-- gui/               # Web-Interface
```

---

## Verteilung der Diagramme

| Diagramm | Einsatzort |
|----------|-----------|
| Diagramm 3 (Gesamt) | SKILL.md, ROADMAP.md, README |
| Diagramm 1 (Backend) | ../docs/ Entwicklerdoku |
| Diagramm 2 (Frontend) | skills/docs/docs/docs/help/bach.txt, Einstiegs-Hilfe |
| Diagramm 4 (Memory) | skills/docs/docs/docs/help/memory.txt, ../docs/ Konzeptdoku |

---

## Weiterfuehrende Dokumentation

| Ressource | Beschreibung | Zugriff |
|-----------|--------------|---------|
| SKILL.md | KI-Referenz | Root-Verzeichnis |
| skills/docs/docs/docs/help/*.txt | Befehls-Dokumentation | `bach --help <thema>` |
| skills/wiki/*.txt | Hintergrundwissen | `bach wiki <artikel>` |
| ../user/README.md | Nutzer-Einstieg | ../user/ Ordner |
| ROADMAP.md | Entwicklungsplan | Root-Verzeichnis |

---

## Versionierung

| Version | Datum | Beschreibung |
|---------|-------|--------------|
| 1.0.0 | 2026-01-11 | Initial Release |
| 1.1.0 | 2026-01-14 | Backup/Restore/Distribution |
| 1.1.50 | 2026-01-24 | Wiki-Service, Help-Forensik |
| 1.1.73 | 2026-01-29 | Architektur-Diagramme zusammengefuehrt |

---

*Dieses Dokument ist Teil der BACH-Entwicklerdokumentation.*
*Fuer operative Befehle siehe: `bach --help`*
*Erstellt: 2026-01-29 | Zusammengefuehrt aus ../docs/ARCHITECTURE.md und ../docs/ARCHITECTURE_DIAGRAMS.md*