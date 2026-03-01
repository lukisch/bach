# BACH ROADMAP - Strategische Vision

**Stand:** 2026-03-01 | **Version:** 4.0.0

Copyright (c) 2026 Lukas Geiger. Alle Rechte vorbehalten.

> Die ROADMAP definiert Vision und Phasen. Konkrete Tasks siehe: `bach task list`
> Post-Release-Details (SQ-Nummern): ehemals `BACH_Dev/ROADMAP.md` — jetzt hier konsolidiert.

---

## Vision

BACH definiert sich als **Personal Agentic Operating System**. Es entwickelt sich zu einem autonomen, lernfaehigen System mit:

- **Kognitives Memory-System** (menschliches Gedaechtnis als Vorbild)
- **Selbststaendige Sessions** (Headless AI ohne User-Interaktion)
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

## GitHub-Veroeffentlichung

Alle technischen Go-Kriterien sind erfuellt. Der Release wartet auf den manuellen Push.

| Schritt | Status |
|---------|--------|
| Privates Repo erstellen & Push | Ausstehend |
| Repo auf Public stellen | Ausstehend (nach Pruefung) |
| Tag `v3.1.6-strawberry` setzen | Ausstehend |
| Release-Announcement | Ausstehend |
| Manuelle PII-Stichproben Prio 4-5 (optional, ~30 min) | Optional |

> Checkliste: `../../BACH_Dev/archive/reports/ENDABNAHME_CHECKLISTE.md` | PII-Scan: `../docs/HQ9_PUBLIC_RELEASE_CHECKLIST.md`

---

## Aktuelle Fokus-Bereiche

### Prioritaet 1 — Kern-Architektur vervollstaendigen

**SQ073: Scheduler-Migration abschliessen** (ENT-43)
- DB-Tabellen `daemon_jobs`/`daemon_runs` -> `scheduler_jobs`/`scheduler_runs` umbenennen
- `hub/chain.py` (ChainHandler) erstellen: `bach chain start/stop/status/list/log`
- llmauto als `tools/llmauto/` in BACH einbinden
- SessionDaemon + ATI SessionDaemon -> llmauto-Ketten konvertieren
- GUI: Scheduler-Tab + Chain-Tab im FastAPI-Dashboard
- Ref: `../../BACH_Dev/archive/reports/SQ073_DAEMON_SCHEDULER_PLANUNG.md`

**SQ074: marble_run vollstaendig nach llmauto portieren** (ENT-43)
- active_chain.md Generierung (dynamisches Worker-Briefing)
- 6 Selection-Strategien portieren
- 4 Original-Prompts uebernehmen
- marble_run/ -> `_archive/` verschieben (nach Abschluss)
- Chain-Config-Dateien: `SQ074_CHAIN_PORTS/` (9 JSONs bereits portiert)

**SQ043: Memory-Migration Stufe D**
- Sessions migrieren: `memory_sessions` -> `shared_memory_sessions` (1504 Eintraege)
- context_triggers migrieren: 1024 Eintraege -> `shared_context_triggers`
- Auto-expires Trigger implementieren
- Ref: `../../BACH_Dev/archive/reports/SQ043_STUFE_C_MEMORY_MIGRATION_KONZEPT.md`

**HQ8/ENT-45: Installer CLI-Interface (Phase 3)**
- Non-interaktiver CLI-Modus mit Validierung
- Integrations-Level-Wahl in Installer einbauen (SQ038)

---

### Prioritaet 2 — Features & Qualitaet

**SQ014: 7 verbleibende PARTIAL Usecases verbessern** (B27)
- UC6/7/8 (Versicherung): Retest empfohlen
- UC26/UC27 (Location/Reiseroute): Web-Features
- UC43 (FinancialProof Dashboard): Externe App-Integration
- UC46 (MediaBrain DB): Externe DB-Anbindung

**SQ017: GUI aktualisieren** (B28, ENT-33)
- Scheduler-Tab implementieren (Schicht 1 dockt an)
- Chain-Tab implementieren (Schicht 2 dockt an)
- Ref: `../../BACH_Dev/archive/reports/SQ017_GUI_STATUS.md`

**SQ038: Claude Code Integration — offene Punkte** (B29)
- Inter-Instanz-Messaging via Hooks
- System-Injection-Log als Standard
- Ref: `../../BACH_Dev/archive/reports/SQ038_MEMO_DEDUP_BERICHT.md`

**SQ051: Stigmergy-API implementieren** (B33)
- `hub/_services/stigmergy/stigmergy_api.py` vollstaendig (STUB vorhanden)
- Abhaengig von: SQ073 (Scheduler) + SQ074 (llmauto)

**SQ075: USER.md** (B34, ENT-41)
- Installer-Integration: USER.md beim Setup generieren
- Bidirektionaler SYNC fertigstellen

**SQ036: Vernunftstests** (B36)
- Ergebnisse in Forschung rueckfuehren

---

### Prioritaet 3 — Modulare Agenten & externe Tools

**SQ080: ApiProber** (B36)
- Timeout-Bug im Smoke-Test fixen (60s statt 10s)
- Veraltete Import-Tests korrigieren
- Sync mit `api_book`-Tabelle

**SQ081: n8n Workflow Manager** (B37)
- BACH-Handler vollstaendig implementieren (list, sync)
- Smoke-Test gegen lokale n8n-Instanz
- Sync mit `api_book`-Tabelle

**SQ011: Pipeline-Framework** (B39)
- Generischer Entscheidungsbaum fuer alle Pipelines
- ATI Scan-Roots konfigurierbar machen

---

### Prioritaet 4 — Visionen & Experimente (nach Release)

| SQ | Thema | Notiz |
|----|-------|-------|
| SQ016 | Schwarm-LLM-Haiku-Experimente | Multi-Agent-Forschung |
| SQ018 | Plan-Agent & Planungsprotokoll | Formalisierung |
| SQ028 | Multi-BACH (benannte Instanzen) | Ein Ordner = eine Instanz (ENT-11) |
| SQ040 | Reminder-Injektor | LLM-Selbsterinnerung |
| SQ042 | Meta-Feedback-Injektor | BACH korrigiert LLM-Ticks |
| SQ044 | BACH-in-a-Database (Vision) | Alles lebt in DB, on-demand entpackt |
| SQ048 | Arbeitsmodi & 24h-Agent | Persistenter Tages-Kontext |
| SQ052 | Bridge Antwort-Modus & Server-Betrieb | Headless/Remote |
| SQ054 | ResearchAgent BACH-Re-Integration | v0.3.0 Ziel |
| SQ055 | devSoftAgent fertigstellen | 12 Module, 1244 LOC |
| SQ056 | llmauto Standalone finalisieren | ENT-43 Schicht 2 |
| ENT-25 | _CHIAH + recludOS als Legacy veroeffentlichen | Bereinigung noetig |

---

## Softwareprojekt-Integrationen (KOMPLETT - 2026-03-01)

6 Integrations-Aufgaben aus der Analyse aller 11 Tools vs. BACH (73 Handler, 23 Experten, 25+ Services).

| Integration | Beschreibung | Status |
|-------------|-------------|--------|
| INT01 | LitZentrum -> `literatur.py` + Expert `literaturverwalter` | KOMPLETT |
| INT02 | HausLagerist V4 -> `haushalt.py` erweitern + Expert | KOMPLETT |
| INT03 | MediaBrain -> `media.py` + Expert `mediaverwalter` | KOMPLETT |
| INT04 | MasterRoutine -> Routine-Export-Skill | KOMPLETT |
| INT05 | UpToday -> Dashboard-Aggregator `bach today` | KOMPLETT |
| INT06 | ProFiler -> Dedup + Datenschutz-Ampel | KOMPLETT |

---

## Weitere abgeschlossene Bloecke (ehemals Prio 2-3)

| Block | SQ | Aufgabe | Status |
|-------|-----|---------|--------|
| B31 | SQ047/SQ059 | Wissensindexierung / KnowledgeDigest | KOMPLETT |
| B35 | SQ076 | Secrets-Management Installer-Integration | KOMPLETT |
| B38 | SQ010 | Foerderplaner-Extraktion (pdf_processor, ocr_service) | KOMPLETT |
| B40 | SQ027 | Alt-Tests in pytest portieren | KOMPLETT |
| — | SQ033 | BACH Mini (USMC-basiert) | KOMPLETT |
| B30 | SQ046 | Therapie-Skills: Trauma + Systemisch | Verschoben -> `THE_RELEASE_AFTER.md` |
| B32 | SQ049 | Agenten autonomer machen | Verschoben -> `THE_RELEASE_AFTER.md` |

---

## Abgeschlossene Phasen (BACH-internes Entwicklungsprotokoll)

### 0b.2 Release v3.2.0-butternut (KOMPLETT - 2026-02-28)

Grosse BUTTERNUT-Release mit Scheduler-Refactoring, Prompt-System, neuen Handlern und Portierungen.

**DB-Schema:**
- `daemon_jobs` -> `scheduler_jobs`, `daemon_runs` -> `scheduler_runs`
- 4 neue Tabellen: `prompt_templates`, `prompt_versions`, `prompt_boards`, `prompt_board_items`
- 8 Migrationen (012-020) nachgezogen

**Neue Handler:**
- `AgentLauncherHandler` (`bach agent`) - Agent-Ausfuehrung via CLI
- `PromptHandler` (`bach prompt`) - Prompt-CRUD mit Board-System

**SharedMemory-Erweiterungen:**
- `current-task`, `generate-context`, `conflict-resolution`, `decay`, `changes-since`

**Neue Infrastruktur:**
- `hub/_services/usmc_bridge.py` - USMC Bridge fuer Cross-Agent-Kommunikation
- bach:// URL-Resolution in llmauto-Prompts (`hub/url_resolver.py`)
- `tools/migrate_prompts.py` - 3-Quellen-Migration in DB

**Portierungen aus vanilla:**
- SharedMemoryHandler, ApiProberHandler, N8nManagerHandler, UserSyncHandler
- Stigmergy-Service

**Archivierungen:**
- marble_run -> `_archive/marble_run/`
- ATI SessionDaemon -> Ersetzt durch SchedulerService

### 0. Adaptionsfaehigkeit & Self-Extension (Phase 1-3 KOMPLETT, Phase 4 Stufe 2+3 GEPLANT)

**Phase 1: Quick Wins (KOMPLETT)**
- Registry Hot-Reload (`core/registry.py` reload-Methode)
- `bach skills create <name> --type <typ>` (5 Typen: tool, agent, expert, handler, service)
- `bach skills reload` (Hot-Reload ohne Neustart)

**Phase 2: Hook-Framework (KOMPLETT)**
- `core/hooks.py` - HookRegistry mit 14 Events
- `hub/hooks.py` - CLI-Handler (`bach hooks status/events/log/test`)

**Phase 3: Plugin-API (KOMPLETT)**
- `core/plugin_api.py` - PluginRegistry-Singleton
- `hub/plugins.py` - CLI-Handler (`bach plugins list/load/unload/tools/info/create`)

**Phase 4: Sandbox & Security - Stufe 1 Capability System (KOMPLETT)**
- `core/capabilities.py` - CapabilityManager mit 11 definierten Capabilities
- Trust-Level Enforcement: goldstandard/trusted/untrusted/blacklist

**Phase 4: Sandbox - Stufe 2+3 (GEPLANT)**
- Stufe 2: Subprocess-Isolation (timeout, memory-limit)
- Stufe 3: Container-Isolation (Docker/chroot)
- Rollback bei fehlerhaften Erweiterungen

### Weitere abgeschlossene Phasen

| # | Phase | Bereich | Status |
|---|-------|---------|--------|
| 19 | Directory Restructuring v2.5 | agents/, connectors/, partners/ top-level | KOMPLETT |
| 1 | Zeit-System v1.1.83 | clock, timer, countdown, between, beat | KOMPLETT |
| 2 | Workflow-TUeV v1.1.83 | tuev status/check, usecase list/run | KOMPLETT |
| 3 | Memory-Konsolidierung | CONSOL_001-007 | In Progress |
| 4 | GUI-Erweiterungen | Dashboard, Tools, Inbox | Offen |
| 5 | Steuer-Banking Integration | CAMT.053, Bank-Beleg-Matching | Offen |
| 6 | Data-Import-Framework | CSV/JSON Import, Schema-Erkennung | KOMPLETT |
| 7 | CLI-Handler Erweiterungen | contact, gesundheit, haushalt, steuer | KOMPLETT |
| 8 | Connector & Message-System v2.1 | Queue, Retry, Circuit Breaker, 3 Adapter | KOMPLETT |
| 9 | bach.py v2.0 Registry-Architecture | 1636->563 Zeilen, Auto-Discovery | KOMPLETT |
| 10 | MCP-Server v2.2.0 | 23 Tools, 8 Resources, 3 Prompts | KOMPLETT |

### Langfristige Ziele (P4)

**Headless AI-Sessions** — Tasks AI_001-AI_004 (KOMPLETT)
**Filesystem-Schutz** — Tasks FS_001-FS_004, Konzept: `../docs/CONCEPT_filesystem_protection.md`
**DB-Content-Sync** — Task SYNC_004 (in Progress), Konzept: `../docs/CONCEPT_db_content_sync.md`

---

## Abgeschlossene Meilensteine

| Phase | Bereich | Abschluss |
|-------|---------|-----------|
| 1-3 | Autonomie, Funktionalitaet, Dashboard | 2026-01 |
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
| 18.1 | Self-Extension Quick Wins | 2026-02 |
| 18.2 | Hook-Framework (14->16 Events) | 2026-02 |
| 18.3 | Plugin-API | 2026-02 |
| 18.4 | Capability System Stufe 1 | 2026-02 |
| 19 | Directory Restructuring v2.5 | 2026-02 |
| 20 | BUTTERNUT v3.2.0 | 2026-02 |
| INT01-06 | Softwareprojekt-Integrationen (6 Tools) | 2026-03 |
| B31 | KnowledgeDigest / Wissensindexierung | 2026-03 |
| B35 | Secrets-Management | 2026-03 |
| B38 | Foerderplaner-Extraktion | 2026-03 |
| B40 | Alt-Tests pytest-Portierung | 2026-03 |
| — | BACH Mini (USMC-basiert) | 2026-03 |

~140+ Tasks abgeschlossen in Phase 1-20 + Post-Release-Bloecke.

### Abgeschlossene Release-Meilensteine (Strawberry v3.1.6)

| Meilenstein | Version | Status |
|-------------|---------|--------|
| HQ0 DB-Konsolidierung | — | 142 Tabellen |
| HQ1 Dateizuordnung (dist_type) | — | CORE/TEMPLATE/USER |
| HQ2 Distribution-System | — | distribution.py v1.0.0 |
| HQ3 Strawberry Build | v3.1.6 | 669 Dateien, 99.0% pytest |
| HQ4 Integritaet & PII | — | 0 PII-Leaks |
| HQ5 Nutzertest | — | 83.3% EXCELLENT |
| HQ6 Reset/Restore | — | 3 Varianten, 15/15 Tests |
| HQ7 Neuinstallation | — | 3 Varianten definiert & getestet |
| HQ8 Installer-Workflow | — | ENT-45 3D-Modell (Phase 1-2+4) |
| HQ9 GitHub-Vorbereitung | — | 7/7 Go-Kriterien erfuellt |
| SQ027 Testabdeckung | — | 390/391 (99.7%) |
| SQ014 Usecase-Coverage | — | 50/50 (100%), Score 80.0% |

> Vollstaendige Erledigungsliste: `../../BACH_Dev/archive/masterplan/MASTERPLAN_DONE.txt`

---

## Architektur-Uebersicht

```
                        BACH v2.5 GESAMTARCHITEKTUR
  ========================================================================

  USER-INTERFACES
    CLI (bach.py)  |  GUI (gui/server.py)  |  API (headless:8001)  |  MCP
  ========================================================================
                                |
  HUB LAYER (hub/*.py)
    System:    startup, shutdown, status, backup, tokens, inject, scan
    Domain:    steuer, abo, haushalt, gesundheit, contact, calendar, routine
    Data:      task, memory, db, session, logs, wiki, docs, inbox
    AI:        agent (launcher), partner, scheduler, ollama, ati
    Comm:      connector, messages (Queue, Retry, Circuit Breaker)
    Prompts:   prompt (templates, versions, boards) [NEU v3.2]
    Memory:    shared_memory + USMC Bridge [NEU v3.2]
  ========================================================================
              |                     |                      |
  AGENTS LAYER            TOOLS LAYER              DATA LAYER
    agents/ (ATI, 4+)      c_ocr_engine.py          bach.db (Unified DB)
    agents/_experts/ (14)  data_importer.py          prompt_templates [NEU]
    skills/_services/      folder_diff_scanner.py    scheduler_jobs [NEU]
     (daemon, connector,   doc_search.py             Dateisystem
     document, voice,      mcp_server.py             (../user/, memory/,
     mail, market,         migrate_prompts.py [NEU]   logs/, help/)
     stigmergy [NEU])      url_resolver.py [NEU]     Externe Ordner/Inbox
    skills/workflows/
     (.md)
  ========================================================================
              |                                        |
  PARTNER LAYER                             CONNECTOR LAYER
    partners/claude/                          connectors/ (3+)
    partners/gemini/                          Telegram, Discord
    partners/ollama/                          HomeAssistant
    USMC Bridge [NEU]                         (Signal, WhatsApp geplant)
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
| Policy-Entscheidungen | `../../BACH_Dev/POLICY.md` (alle 44 ENTs) |

---

## Changelog (komprimiert)

| Version | Datum | Aenderung |
|---------|-------|----------|
| 1.0-1.5 | 2026-01 | Phase 1-3 (Autonomie, Funktionalitaet) |
| 2.0 | 2026-01-24 | Phase 4-11 konsolidiert |
| 2.1 | 2026-01-25 | Erledigte Phasen zusammengefasst |
| 3.0 | 2026-01-25 | Transformation zu strategischem Dokument |
| 3.1 | 2026-01-28 | Systemisch-First Prinzip, Import-Framework, CLI-Handler |
| **3.2** | 2026-01-30 | **Zeit-System (Clock/Timer/Countdown/Between/Beat), Workflow-TUeV** |
| **3.3** | 2026-02-08 | **bach.py v2.0 Registry, Connector Runtime, Message-System v2.0** |
| **3.4** | 2026-02-08 | **MCP v2.2 (23 Tools), Email-Adapter, BachFliege/BachForelle archiviert** |
| **3.5** | 2026-02-13 | **Self-Extension: Skills Create/Reload, Hook-Framework (14 Events), Email-Handler** |
| **3.6** | 2026-02-13 | **Capability System Stufe 1: 11 Caps, Trust-Enforcement, Audit-Log** |
| **3.7** | 2026-02-13 | **Directory Restructuring v2.5** |
| **3.8** | 2026-02-28 | **BUTTERNUT v3.2.0: Scheduler, Prompt-System, USMC Bridge** |
| **4.0** | 2026-03-01 | **Konsolidierung: BACH_Dev/ROADMAP.md + Post-Release-Prios integriert, INT01-06 + B31/B35/B38/B40/BACH Mini als KOMPLETT markiert** |

Detaillierte Historie: `CHANGELOG.md`
Archivierte Versionen: `../docs/_archive/ROADMAP_*.md`

---

## Verwandte Dokumente

- **MASTERPLAN (Release-Pipeline):** `../../BACH_Dev/MASTERPLAN.txt`
  Beschreibt den Weg von Vanilla -> Strawberry -> GitHub-Veroeffentlichung.
  Enthaelt: 11 Hauptquests, 29 Sidequests, 7 Cluster, Abhaengigkeitskarte.
  Die ROADMAP beschreibt WAS BACH kann, der MASTERPLAN beschreibt WIE wir releasen.

- **NEXT_RELEASE (naechste Tasks):** `../../BACH_Dev/NEXT_RELEASE.md`
  Konkrete Aufgaben fuer das naechste Release.

- **THE_RELEASE_AFTER (verschoben):** `../../BACH_Dev/THE_RELEASE_AFTER.md`
  Items die nicht release-kritisch sind (B30/SQ046, B32/SQ049).

- **POLICY (Entscheidungen):** `../../BACH_Dev/POLICY.md`
  Alle 44 ENT-Entscheidungen.

- **SKILL.md (Einstiegspunkt):** `../../SKILL.md`

---

*Konsolidiert am 2026-03-01 — BACH_Dev/ROADMAP.md und BACH/ROADMAP.md zu einem Dokument zusammengefuehrt*
