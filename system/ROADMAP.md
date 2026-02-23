# BACH ROADMAP - Strategische Vision

**Stand:** 2026-02-13 | **Version:** 3.7.0

> Die ROADMAP definiert Vision und Phasen. Konkrete Tasks siehe: `bach task list`

---

## Vision

BACH definiert sich als **Personal Agentic Operating System**. Es entwickelt sich zu einem autonomen, lernfähigen System mit:

- **Kognitives Memory-System** (menschliches Gedächtnis als Vorbild)
- **Selbstständige Sessions** (Headless AI ohne User-Interaktion)
- **Aktive Konsolidierung** (Lernen, Vergessen, Zusammenfassen)
- **Multi-Partner Delegation** (Claude, Gemini, Ollama, lokale Modelle)

---

## Entwicklungsprinzip: Systemisch First

> **BACH wird als wiederverwendbares System entwickelt, nicht fuer einen einzelnen User.**

Jede Funktion muss fuer ALLE zukuenftigen User funktionieren. Die Entwicklung
folgt der Reihenfolge:

1. **Systemisch** - Wiederverwendbare Services, Agents, Workflows
2. **CLI First** - Alles ueber CLI steuerbar
3. **User-Daten** - Import/Test mit echten Daten (z.B. Lukas' Daten)

Der aktuelle Entwickler (Lukas) nutzt BACH aktiv und testet mit seinen
eigenen Daten. Aber alle Workflows (Versicherungs-Import, Arztbericht-Scan,
Steuer-Export) muessen generisch sein und fuer jeden neuen User funktionieren.

**dist_type System** trennt System- von User-Daten:

- `0` = User-Daten (nicht mitgeliefert bei Installation)
- `1` = Template (zuruecksetzbar, Basis-Konfiguration)
- `2` = Core (System-intern, immer dabei)

Siehe: `../docs/WICHTIG_SYSTEMISCH_FIRST.md`

---

## Aktuelle Fokus-Bereiche

### 0. Adaptionsfaehigkeit & Self-Extension (In Progress)

BACH wird zu einem sich selbst erweiternden System. AI-Partner sollen
aktiv neue Faehigkeiten erstellen, statt nur bestehende zu nutzen.

**Phase 1: Quick Wins (KOMPLETT)**
- Registry Hot-Reload (`core/registry.py` reload-Methode)
- `bach skills create <name> --type <typ>` (5 Typen: tool, agent, expert, handler, service)
- `bach skills reload` (Hot-Reload ohne Neustart)
- Self-Extension Workflow (`skills/workflows/self-extension.md`)

**Phase 2: Hook-Framework (KOMPLETT)**
- `core/hooks.py` - HookRegistry mit 14 Events
- `hub/hooks.py` - CLI-Handler (`bach hooks status/events/log/test`)
- Hooks in Startup, Shutdown, Task, Memory, Lesson, Skills, App
- Hooks != Injektoren: Technisches Framework vs. kognitives Subsystem

**Phase 3: Plugin-API (KOMPLETT)**
- `core/plugin_api.py` - PluginRegistry-Singleton
- `hub/plugins.py` - CLI-Handler (`bach plugins list/load/unload/tools/info/create`)
- `plugins.register_tool(name, handler)` - Dynamisch Tools registrieren
- `plugins.register_hook(event, callback)` - Hooks ueber API registrieren
- `plugins.register_workflow(name, steps)` - Workflows programmatisch erstellen
- `plugins.register_handler(name, class)` - Handler zur Laufzeit hinzufuegen
- `plugins.load_plugin(path)` - Deklarativ via plugin.json Manifest
- `plugins.unload_plugin(name)` - Plugin sauber entladen

**Phase 4: Sandbox & Security - Stufe 1 Capability System (KOMPLETT)**
- `core/capabilities.py` - CapabilityManager mit 11 definierten Capabilities
- Trust-Level Enforcement: goldstandard/trusted/untrusted/blacklist
- Capability-Profile in `data/skill_sources.json` integriert
- Enforcement in allen `register_*()` Methoden der Plugin-API
- Statische Code-Analyse (eval, exec, subprocess, os.system, requests)
- Audit-Log (`data/logs/capability_audit.log`) mit Rotation
- CLI: `bach plugins caps/trust/audit`
- Hook: `after_capability_denied` bei Verweigerung

**Phase 4: Sandbox - Stufe 2+3 (GEPLANT)**
- Stufe 2: Subprocess-Isolation (timeout, memory-limit)
- Stufe 3: Container-Isolation (Docker/chroot)
- Rollback bei fehlerhaften Erweiterungen

Analyse: `docs/openclaw_architektur_analyse.md`
Vergleich: `docs/vergleich_bach_vs_openclaw.md`
Plan: `docs/adaptions_plan_bach.md`

### 0b. Phase 19: Directory Restructuring (v2.5 - KOMPLETT)

Vereinheitlichung der Verzeichnisstruktur unter `system/` fuer Standards-Compliance
und klarere Trennung von Agents, Connectors und Partners.

**Aenderungen:**
- `agents/` -> `agents/` (top-level unter system/)
- `agents/_experts/` -> `agents/_experts/` (Experts gehoeren zu Agents)
- `skills/workflows/` -> `skills/workflows/` (Umbenennung, praeziserer Begriff)
- `connectors/` -> `connectors/` (top-level unter system/)
- `partners/` -> `partners/` (top-level unter system/)

**Ergebnis:**
- Agents, Connectors und Partners sind eigenstaendige Top-Level-Verzeichnisse
- Skills-Verzeichnis enthaelt nur noch `_services/`, `workflows/` und `docs/docs/docs/help/`
- Klarere Architektur-Schichten sichtbar in der Verzeichnisstruktur

### 1. Zeit-System (v1.1.83 - KOMPLETT)

Unified Zeit-Management fuer LLM-Sessions.

- `bach clock` - Uhrzeit-Anzeige mit Intervall
- `bach timer` - Stoppuhr (mehrere parallel)
- `bach countdown` - Countdown mit Trigger
- `bach between` - Profile-basierte Zwischen-Checks
- `bach beat` - Unified Zeit-Anzeige

Konzept: `skills/docs/docs/docs/help/beat.txt`, `skills/docs/docs/docs/help/clock.txt`, `skills/docs/docs/docs/help/timer.txt`, `skills/docs/docs/docs/help/countdown.txt`, `skills/docs/docs/docs/help/between.txt`

### 2. Workflow-TUeV (v1.1.83 - KOMPLETT)

Qualitaetssicherung fuer Workflows.

- `bach tuev status` - TUeV-Status aller Workflows
- `bach tuev check` - Einzelnen Workflow pruefen
- `bach usecase list` - Testfaelle anzeigen
- `bach usecase run` - Testfall ausfuehren

Konzept: `skills/docs/docs/docs/help/workflow-tuev.txt`

### 3. Memory-Konsolidierung (In Progress)

Aktives Lernen und Vergessen wie beim Menschen.

- Tasks: CONSOL_001 - CONSOL_007
- Konzept: `skills/docs/docs/docs/help/consolidation.txt`

### 4. GUI-Erweiterungen

Dashboard, Tools, Inbox, Help/Wiki Trennung.

- Diverse GUI-Tasks (P1-P2)

### 5. Steuer-Banking Integration

CAMT.053, Bank-Beleg-Matching, Watch-Ordner.

- Tasks: STEUER_007 - STEUER_010

### 6. Data-Import-Framework

Generisches Import-System fuer alle DB-Tabellen.

- `tools/data_importer.py` - CSV/JSON Import, Schema-Erkennung, Duplikaterkennung
- `tools/folder_diff_scanner.py` - Verzeichnis-Ueberwachung, Datei-Tracking
- Workflow: Ordner scannen -> neue Dateien -> OCR/Parse -> DB-Import
- Alle Imports protokolliert, rollback-faehig, idempotent

### 7. CLI-Handler Erweiterungen

Vollstaendige CLI-Steuerung aller Lebensbereiche.

- `bach contact` - Kontaktverwaltung (CRUD, Suche, Geburtstage)
- `bach gesundheit` - Gesundheitsmanagement (Diagnosen, Medis, Labor, Termine)
- `bach haushalt` - Haushalt (Routinen, Kalender, Fixkosten, Einkaufsliste)
- `bach steuer export --format vorsorge` - Steuer-Export Vorsorgeaufwand

### 8. Connector & Message-System (v2.1.0 - KOMPLETT)

Zuverlaessige Nachrichtenzustellung auch ohne aktive CLI-Session.

- Queue-Processor mit Retry/Backoff und Circuit Breaker
- Daemon-Integration (2 automatische Jobs: poll_and_route, dispatch)
- REST-API (4 Endpoints: send, queue, inbox, route)
- ContextInjector + context_triggers Integration beim Routing
- 3 Runtime-Adapter: Telegram, Discord, HomeAssistant

Konzept: `../docs/PLAN_MESSAGE_SYSTEM_UPGRADE.md`

### 9. bach.py v2.0 Registry-Architecture (KOMPLETT)

Refactoring von 1.636 auf 563 Zeilen mit Auto-Discovery.

- Registry-basiertes Routing via `core/registry.py`
- Library-API `bach_api.py` fuer LLM/Script-Zugriff
- Dual-Init BaseHandler (Path und App)
- 50 Tests bestanden

### 10. MCP-Server Integration (v2.2.0 - KOMPLETT)

Model Context Protocol fuer IDE-Integration (Claude Code, Cursor, etc.).

- MCP Server v2.2.0 (`tools/mcp_server.py`) - 610 Zeilen
- 23 Tools, 8 Resources, 3 Prompts (alle drei MCP-Primitives)
- Backend: bach_api (Handler-basiert, kein direkter SQLite)
- Session-Tools: session_startup, session_shutdown
- Partner-Tools: partner_list, partner_status
- db_query mit 110-Table Whitelist (Credentials geschuetzt)
- Konformitaet: 95% (fehlend: Pagination, Events - bewusst deferred)
- Doku: `../docs/_archive/con4_MCP_CONFORMITY_60.md`

---

## Langfristige Ziele (P4)

### Headless AI-Sessions

Autonomer Betrieb ohne User-Interaktion.

- Tasks: AI_001 - AI_004 (KOMPLETT)
- Multi-Job Daemon, Zeitbudget, Reporting integriert.

### Filesystem-Schutz

Backup, Critical-Check, Mode-Switch.

- Tasks: FS_001 - FS_004
- Konzept: `../docs/CONCEPT_filesystem_protection.md`

### DB-Content-Sync

Automatische Synchronisation Skills/Tools.

- Task: SYNC_004 (in Progress)
- Konzept: `../docs/CONCEPT_db_content_sync.md`

---

## Abgeschlossene Meilensteine

| Phase | Bereich | Abschluss |
|-------|---------|-----------|
| 1-3 | Autonomie, Funktionalität, Dashboard | 2026-01 |
| 4 | Session, Token, GUI, Prompt-Generator | 2026-01 |
| 5 | Integration Services | 2026-01 |
| 6.1-6.2 | Steuer Phase 1-2, Workflows | 2026-01 |
| 8 | Mail-Profil-System | 2026-01 |
| 10 | Dokumenten-Scanner/Inbox | 2026-01 |
| 11 | JSON-zu-DB Migration | 2026-01 |
| 12 | bach.py v2.0 Registry-Architecture | 2026-02 |
| 13 | Connector Runtime + Voice Service | 2026-02 |
| 14 | Message-System Upgrade (Queue, Retry, API) | 2026-02 |
| 15 | MCP-Server v2.2 (23 Tools, 8 Resources, 3 Prompts) | 2026-02 |
| 16 | BachFliege/BachForelle Analyse + Archivierung | 2026-02 |
| 17 | Email-Handler (Gmail API, Draft-Safety) | 2026-02 |
| 18.1 | Self-Extension Quick Wins (skills create/reload, hot-reload) | 2026-02 |
| 18.2 | Hook-Framework (14→16 Events, CLI-Handler, Kern-Integration) | 2026-02 |
| 18.3 | Plugin-API (register_tool/hook/workflow/handler, plugin.json) | 2026-02 |
| 18.4 | Capability System Stufe 1 (11 Caps, Trust-Enforcement, Audit-Log) | 2026-02 |
| 19 | Directory Restructuring v2.5 (agents/, connectors/, partners/ top-level, workflows/) | 2026-02 |

~100+ Tasks abgeschlossen in Phase 1-19.

---

## Architektur-Übersicht

```
                        BACH v2.5 GESAMTARCHITEKTUR
  ========================================================================

  USER-INTERFACES
    CLI (bach.py)  |  GUI (gui/server.py)  |  API (headless:8001)  |  MCP
  ========================================================================
                                |
  HUB LAYER (hub/*.py)
    System: startup, shutdown, status, backup, tokens, inject, scan
    Domain: steuer, abo, haushalt, gesundheit, contact, calendar, routine
    Data:   task, memory, db, session, logs, wiki, docs, inbox
    AI:     agents, partner, daemon, ollama, ati
    Comm:   connector, messages (Queue, Retry, Circuit Breaker)
  ========================================================================
              |                     |                      |
  AGENTS LAYER            TOOLS LAYER              DATA LAYER
    agents/ (ATI, 4+)      c_ocr_engine.py          bach.db (Unified DB)
    agents/_experts/ (14)  data_importer.py          Dateisystem
    skills/_services/      folder_diff_scanner.py     (../user/, memory/,
     (daemon, connector,   doc_search.py               logs/, skills/docs/docs/docs/help/)
     document, voice,      mcp_server.py             Externe Ordner/Inbox
     mail, market)         injectors.py
    skills/workflows/
     (.md)
  ========================================================================
              |                                        |
  PARTNER LAYER                             CONNECTOR LAYER
    partners/claude/                          connectors/ (3+)
    partners/gemini/                          Telegram, Discord
    partners/ollama/                          HomeAssistant
                                              (Signal, WhatsApp geplant)
  ========================================================================

  DATENFLUSS:  CLI/GUI/API --> Hub --> Agents/Skills/Tools --> DB/Files/Partners
  PRINZIPIEN:  CLI First | Systemisch | dist_type | Idempotent
```

> Detaillierte Architektur-Diagramme: `../docs/ARCHITECTURE_DIAGRAMS.md`

---

## Konzept-Index

| Bereich | Konzept-Datei |
|---------|---------------|
| Memory-Konsolidierung | `skills/docs/docs/docs/help/consolidation.txt` |
| Strategische Dokumente | `skills/docs/docs/docs/help/strategic.txt` |
| Drei Handler-Systeme | `../docs/CONCEPT_three_handlers.md` |
| DB-Content-Sync | `../docs/CONCEPT_db_content_sync.md` |
| Filesystem-Schutz | `../docs/CONCEPT_filesystem_protection.md` |
| Inbox-Scanner | `../docs/CONCEPT_inbox_folders_format.md` |
| Message-System Upgrade | `../docs/PLAN_MESSAGE_SYSTEM_UPGRADE.md` |
| Systemisch-First | `../docs/WICHTIG_SYSTEMISCH_FIRST.md` |
| Distribution-System | `data/schema_distribution.sql` |
| Architektur-Diagramme | `../docs/ARCHITECTURE_DIAGRAMS.md` |

---

## Changelog (komprimiert)

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.0-1.5 | 2026-01 | Phase 1-3 (Autonomie, Funktionalität) |
| 2.0 | 2026-01-24 | Phase 4-11 konsolidiert |
| 2.1 | 2026-01-25 | Erledigte Phasen zusammengefasst |
| 3.0 | 2026-01-25 | Transformation zu strategischem Dokument |
| 3.1 | 2026-01-28 | Systemisch-First Prinzip, Import-Framework, CLI-Handler |
| **3.2** | 2026-01-30 | **Zeit-System (Clock/Timer/Countdown/Between/Beat), Workflow-TUeV** |
| **3.3** | 2026-02-08 | **bach.py v2.0 Registry, Connector Runtime, Message-System v2.0** |
| **3.4** | 2026-02-08 | **MCP v2.2 (23 Tools), Email-Adapter, BachFliege/BachForelle archiviert** |
| **3.5** | 2026-02-13 | **Self-Extension: Skills Create/Reload, Hook-Framework (14 Events), Email-Handler** |
| **3.6** | 2026-02-13 | **Capability System Stufe 1: 11 Caps, Trust-Enforcement, Audit-Log, Plugin-API Security** |
| **3.7** | 2026-02-13 | **Directory Restructuring v2.5: agents/, connectors/, partners/ top-level; _workflows/ -> workflows/** |

Detaillierte Historie: `CHANGELOG.md`
Archivierte Versionen: `../docs/_archive/ROADMAP_*.md`

---

---

## Verwandte Dokumente

- **MASTERPLAN (Release-Pipeline):** `../../BACH_Dev/MASTERPLAN.txt`
  Beschreibt den Weg von Vanilla -> Strawberry -> GitHub-Veroeffentlichung.
  Enthaelt: 11 Hauptquests, 29 Sidequests, 7 Cluster, Abhaengigkeitskarte.
  Die ROADMAP beschreibt WAS BACH kann, der MASTERPLAN beschreibt WIE wir releasen.

- **SKILL.md (Einstiegspunkt):** `../../SKILL.md`

---

*BACH Session 2026-02-13, Querverweise ergaenzt 2026-02-16*