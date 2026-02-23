#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
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
"""

import os
import json
from datetime import datetime
from pathlib import Path
import sys

# =============================================================================
# KONFIGURATION
# =============================================================================

VERSION = "3.0.0"
GENERATED_DATE = datetime.now().strftime("%Y-%m-%d")

# =============================================================================
# STRUKTUR-DEFINITION v3.0
# =============================================================================

STRUCTURE = {
    # Root-Dateien
    "_files": [
        "SKILL.md",
        "README.md", 
        "CHANGELOG.md",
        "identity.json"
    ],
    
    # ══════════════════════════════════════════════════════════════════
    # KERN-INFRASTRUKTUR (mit _ Prefix = laden beim Boot)
    # ══════════════════════════════════════════════════════════════════
    
    # _boot/ - Lifecycle-Management
    "_boot": {
        "_files": [
            "SKILL.md",
            "boot-config.json",
            "boot-sequence.json",
            "micro-routines.json",
            "shutdown-protocol.json",
            "triggers.json"
        ]
    },
    
    # _registry/ - Zentrale Wahrheitsquellen
    "_registry": {
        "_files": [
            "SKILL.md",
            "master.json",
            "skills.json",
            "tools.json",
            "configs.json"
        ],
        "schema": {}
    },
    
    # _config/ - System-Konfiguration
    "_config": {
        "_files": [
            "SKILL.md",
            "system.json",
            "user.json",
            "integrations.json"
        ]
    },
    
    # _memory/ - Kognitive Memory-Architektur
    "_memory": {
        "_files": ["SKILL.md"],
        
        "_meta": {
            "_files": [
                "confidence.json",
                "conflicts.json",
                "blind_spots.json",
                "hallucination_log.json",
                "introspection.md"
            ],
            "consciousness": {
                "_files": [
                    "self_concept.json",
                    "theory_of_mind.json",
                    "time_awareness.json"
                ]
            }
        },
        
        "working": {
            "_files": [
                "scratchpad.md",
                "active_context.json",
                "open_loops.json",
                "current_intent.json"
            ]
        },
        
        "episodic": {
            "_files": ["_index.json"],
            "timeline": {},
            "sessions": {},
            "decisions": {},
            "outcomes": {}
        },
        
        "semantic": {
            "_files": ["_index.json"],
            "facts": {},
            "concepts": {},
            "relationships": {},
            "lessons": {}
        },
        
        "procedural": {
            "_files": ["_index.json"],
            "skills": {},
            "workflows": {},
            "patterns": {},
            "heuristics": {}
        },
        
        "emotional": {
            "_files": [
                "importance_weights.json",
                "sentiment_history.json",
                "engagement_patterns.json"
            ]
        },
        
        "consolidation": {
            "_files": [
                "pending_episodic.json",
                "merge_candidates.json",
                "ttl_expiring.json",
                "archive_queue.json"
            ]
        },
        
        "config": {
            "_files": [
                "memory_config.json",
                "retention_policy.json",
                "consolidation_rules.json"
            ]
        }
    },
    
    # 🆕 v3.0: _backup/ - Backup & Recovery System
    "_backup": {
        "_files": ["SKILL.md", "backup_log.json"],
        "trash": {
            "_files": [".gitkeep"]
        },
        "snapshots": {
            "_files": [".gitkeep"]
        }
    },
    
    # _communication/ - Bidirektionale Kommunikation
    "_communication": {
        "_files": [
            "SKILL.md",
            "async_queue.json"
        ],
        
        "channels": {
            "inbox": {
                "pending": {},
                "processed": {}
            },
            "outbox": {
                "pending": {},
                "delivered": {}
            }
        },
        
        "protocols": {
            "_files": [
                "message_schema.json",
                "routing_rules.json"
            ]
        },
        
        "history": {
            "_files": ["index.json"],
            "archive": {}
        }
    },
    
    # ══════════════════════════════════════════════════════════════════
    # AKTEUR-SCHICHT
    # ══════════════════════════════════════════════════════════════════
    
    "actors": {
        "_files": [
            "SKILL.md",
            "delegation_matrix.json"
        ],
        
        "user": {
            "_files": ["profile.json"]
        },
        
        "ai": {
            "_files": ["profile.json"]
        },
        
        "external_ais": {
            "_files": ["registry.json"],
            "delegation_templates": {
                "_files": [
                    "gemini_template.md",
                    "ollama_template.md"
                ]
            }
        }
    },
    
    # ══════════════════════════════════════════════════════════════════
    # AKTIONS-SCHICHT
    # ══════════════════════════════════════════════════════════════════
    
    "skills": {
        "_files": ["SKILL.md"],
        
        "code": {"_files": ["SKILL.md"]},
        "communicate": {"_files": ["SKILL.md"]},
        "analyze": {"_files": ["SKILL.md"]},
        "create": {"_files": ["SKILL.md"]},
        "delegate": {"_files": ["SKILL.md"]}
    },
    
    "tools": {
        "_files": [
            "SKILL.md",
            "annotations.json"
        ],
        
        "mcp-servers": {
            "_files": ["SKILL.md", "registry.json"],
            "templates": {
                "_files": ["server_template.ts"]
            }
        },
        
        "services": {
            "_files": ["registry.json"],
            
            "memory_router": {
                "_files": ["SKILL.md", "router.py", "config.json"]
            },
            
            "success_watcher": {
                "_files": ["SKILL.md", "tracker.py", "fitness_formula.json"],
                "data": {"_files": ["metrics.json"]}
            },
            
            "token_watcher": {
                "_files": ["SKILL.md", "monitor.py", "budget_zones.json"],
                "data": {"_files": ["usage.json"]}
            },
            
            "process_watcher": {
                "_files": ["SKILL.md", "observer.py"],
                "data": {"_files": ["active_tasks.json"]}
            },
            
            # 🆕 v3.0: Backup Service
            "backup_service": {
                "_files": ["SKILL.md", "backup_manager.py", "config.json"],
                "data": {"_files": ["backup_history.json"]}
            }
        },
        
        "patterns": {
            "_files": [
                "SKILL.md",
                "sync_pattern.md",
                "async_pattern.md",
                "batch_pattern.md",
                "session_pattern.md",
                "safe_pattern.md"
            ]
        },
        
        "utilities": {
            "_files": ["registry.json"]
        }
    },
    
    "connections": {
        "_files": ["SKILL.md"],
        
        "external_ais": {
            "gemini": {"inbox": {}, "outbox": {}},
            "ollama": {"_files": ["queue.json"]}
        },
        
        "apis": {"_files": ["registry.json"]},
        "services": {"_files": ["registry.json"]}
    },
    
    # ══════════════════════════════════════════════════════════════════
    # INTERFACE-SCHICHT
    # ══════════════════════════════════════════════════════════════════
    
    "gui": {
        "_files": ["SKILL.md"],
        
        "dashboards": {
            "_files": [
                "boot-dashboard.html",
                "memory-dashboard.html",
                "token-dashboard.html",
                "success-dashboard.html",
                "backup-dashboard.html"  # 🆕 v3.0
            ]
        },
        
        "modules": {}
    },
    
    "reports": {
        "_files": ["SKILL.md"],
        "current": {},
        "archive": {},
        "templates": {}
    },
    
    "exports": {
        "_files": ["SKILL.md"],
        "packages": {},
        "installer": {}
    },
    
    # 🆕 v3.0: _data/ für einfache Tasks (aus Skill-Builder)
    "_data": {
        "_files": ["tasks.json", "tasks_done.json"]
    }
}


# =============================================================================
# DATEI-TEMPLATES v3.0
# =============================================================================

def get_templates(name: str) -> dict:
    """Gibt alle Templates zurück"""
    
    return {
        # ═══════════════════════════════════════════════════════════════════════
        # ROOT FILES
        # ═══════════════════════════════════════════════════════════════════════
        
        "SKILL.md": f'''# {name} - Universal LLM OS v3.0
## Entry Point - Einziger Upload-Skill

**Version:** {VERSION}
**Generiert:** {GENERATED_DATE}

---

## 📋 Übersicht

{name} ist ein textbasiertes Betriebssystem für AI-Assistenten.

### Die drei Säulen

```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│     MEMORY      │ │     TOOLS       │ │  COMMUNICATION  │
│   (Gedächtnis)  │ │    (Hände)      │ │    (Dialog)     │
│                 │ │                 │ │                 │
│   _memory/      │ │  tools/         │ │ _communication/ │
│                 │ │  skills/        │ │  actors/        │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┴───────────────────┘
                             │
              Handlungsfähiges + Kooperatives + Lernendes System
```

### Die drei Kernprinzipien

1. **"Der Geist in der Flasche"** - Die AI ist austauschbar
2. **"Give Them the Power to Act"** - Tools sind die Hände
3. **"Ich, Du, Wir"** - Geteilter Raum für User und AI

## 🚀 Quick Start

1. **Lies diese Datei** - Du bist hier richtig!
2. **Prüfe Inbox** - `_communication/channels/inbox/pending/`
3. **Prüfe Tasks** - `_data/tasks.json`
4. **Lade Memory** - `_memory/working/scratchpad.md`

## 🚀 Bootstrap-Sequenz

1. Version-Check (lokal vs. Kontext)
2. Actor-Profile laden
3. Memory-Retrieval
4. Communication-Queue prüfen
5. **Backup-Status prüfen** (🆕 v3.0)
6. Micro-Routines ausführen
7. Bereit für Interaktion

## 📁 Struktur

```
{name}/
│
├── KERN-INFRASTRUKTUR
│   ├── _boot/              # Lifecycle
│   ├── _registry/          # Wahrheitsquellen
│   ├── _config/            # Konfiguration
│   ├── _memory/            # Gedächtnis
│   ├── _communication/     # Kommunikation
│   ├── _backup/            # 🆕 v3.0 Backup & Recovery
│   └── _data/              # 🆕 v3.0 Einfache Tasks
│
├── AKTEUR-SCHICHT
│   └── actors/             # User, AI, External
│
├── AKTIONS-SCHICHT
│   ├── skills/             # Ausführbare Skills
│   ├── tools/              # Werkzeuge & Services
│   └── connections/        # Externe Verbindungen
│
└── INTERFACE-SCHICHT
    ├── gui/                # Dashboards
    ├── reports/            # Dokumentation
    └── system/system/system/system/exports/            # Deployment
```

## 💾 Backup-System (🆕 v3.0)

| Pfad | Zweck |
|------|-------|
| `_backup/trash/` | Papierkorb (vor destruktiven Operationen) |
| `_backup/snapshots/` | Manuelle Snapshots |
| `_backup/backup_log.json` | Backup-Historie |

**Vor dem Löschen:** Immer zuerst nach `_backup/trash/` verschieben!

## ⚙️ Konfiguration

- System: `_config/system.json`
- User-Präferenzen: `actors/user/profile.json`
- AI-Capabilities: `actors/ai/profile.json`

## 🆕 Neu in v3.0

- **_backup/** - Backup & Recovery System mit Papierkorb
- **_data/** - Einfaches Task-System (zusätzlich zu Communication)
- **backup_service** - Aktiver Backup-Service
- **Erweiterte Boot-Sequenz** - Mit Backup-Status-Check
- **Shutdown mit Backup** - Automatische Sicherung bei Session-Ende
''',

        "README.md": f'''# {name} - Universal LLM OS v3.0

Ein textbasiertes Betriebssystem für AI-Assistenten.

## Die drei Säulen

| Säule | Ordner | Funktion |
|-------|--------|----------|
| **MEMORY** | `_memory/` | Gedächtnis (Episodisch, Semantisch, Prozedural) |
| **TOOLS** | `tools/`, `skills/` | Handlungsfähigkeit (MCP, Services, Patterns) |
| **COMMUNICATION** | `_communication/`, `actors/` | Dialog (Bidirektional, Asynchron) |

## Features v3.0

- 🧠 **Memory System** - Kognitive Architektur mit Consciousness-Erweiterung
- 🛠️ **Tool Framework** - MCP-Standard, Design-Patterns, Watcher-Services
- 💬 **Communication** - Bidirektionale Inbox/Outbox, Akteur-Profile
- 🔄 **Lifecycle** - Boot, Routinen, Shutdown mit aktiver Überwachung
- 📊 **Dashboards** - Memory, Token, Success Monitoring
- 💾 **Backup System** - Papierkorb, Snapshots, Recovery (🆕 v3.0)
- ✅ **Task System** - Einfaches tasks.json (🆕 v3.0)

## Quick Start

1. Lade `SKILL.md` als Skill in Claude hoch
2. Das System bootstrappt sich selbst
3. Interagiere natürlich

## Version

{VERSION} ({GENERATED_DATE})

## Generator

os_generator_v3 (BACH_STREAM)
''',

        "CHANGELOG.md": f'''# Changelog

## [{VERSION}] - {GENERATED_DATE}

### Added (Neu in v3.0)
- **_backup/** - Backup & Recovery System
  - `_backup/trash/` - Papierkorb für destruktive Operationen
  - `_backup/snapshots/` - Manuelle Snapshots
  - `_backup/backup_log.json` - Backup-Historie
- **_data/** - Einfaches Task-System (tasks.json, tasks_done.json)
- **tools/services/backup_service/** - Backup-Management-Service
- **gui/dashboards/backup-dashboard.html** - Backup-Status-Dashboard
- Erweiterte Boot-Sequenz mit Backup-Check
- Shutdown-Protocol mit Backup-Phase

### Based On
- Universal LLM OS v2.0
- BACH_STREAM Potentialanalyse
- recludOS v3.3.0 Backup-Konzepte

## [2.0.0] - 2026-01-06

### Added
- _communication/ - Bidirektionale Kommunikation
- actors/ - Akteur-Profile
- tools/services/*_watcher/ - Aktive Überwachung
- tools/patterns/ - Tool-Design-Patterns
- _memory/_meta/consciousness/ - Bewusstseins-Modell
''',

        "identity.json": json.dumps({
            "name": name,
            "version": VERSION,
            "created": GENERATED_DATE,
            "description": "Textbasiertes Betriebssystem für AI-Assistenten",
            "generator": "os_generator_v3 (BACH_STREAM)",
            "pillars": ["Memory", "Tools", "Communication"],
            "principles": [
                "Der Geist in der Flasche - AI ist austauschbar",
                "Give Them the Power to Act - Tools sind die Hände",
                "Ich, Du, Wir - Geteilter Raum für User und AI"
            ]
        }, indent=2, ensure_ascii=False),

        # ═══════════════════════════════════════════════════════════════════════
        # _boot/ FILES
        # ═══════════════════════════════════════════════════════════════════════
        
        "_boot/SKILL.md": '''# Boot System

## 📋 Übersicht
Lifecycle-Management für das Universal LLM OS.

## Dateien
- `boot-config.json` - Haupt-Konfiguration
- `boot-sequence.json` - Reihenfolge der Boot-Schritte
- `micro-routines.json` - Automatische Routinen
- `shutdown-protocol.json` - Shutdown-Prozess
- `triggers.json` - Event-Trigger

## Boot-Sequenz v3.0

1. Version-Check
2. Actor-Profile laden
3. Memory-Retrieval
4. Communication-Queue prüfen
5. **Backup-Status prüfen** (🆕)
6. Watcher-Services initialisieren
7. Micro-Routines ausführen
8. Bereit
''',

        "_boot/boot-config.json": json.dumps({
            "version": "3.0.0",
            "boot_phases": {
                "phase_0": "Version Check",
                "phase_1": "Load Actor Profiles",
                "phase_2": "Memory Retrieval",
                "phase_3": "Check Communication Queue",
                "phase_4": "Check Backup Status",
                "phase_5": "Initialize Watchers",
                "phase_6": "Execute Micro-Routines",
                "phase_7": "Ready"
            },
            "settings": {
                "auto_memory_retrieval": True,
                "check_inbox_on_boot": True,
                "check_backup_on_boot": True,
                "initialize_watchers": True,
                "max_memory_snippets": 5
            }
        }, indent=2, ensure_ascii=False),

        "_boot/boot-sequence.json": json.dumps({
            "version": "3.0.0",
            "sequence": [
                {"step": 1, "action": "load_identity", "path": "identity.json"},
                {"step": 2, "action": "load_actor_profiles", "path": "actors/"},
                {"step": 3, "action": "retrieve_memory", "service": "memory_router"},
                {"step": 4, "action": "check_inbox", "path": "_communication/channels/inbox/pending/"},
                {"step": 5, "action": "check_backup_status", "path": "_backup/backup_log.json"},
                {"step": 6, "action": "check_tasks", "path": "_data/tasks.json"},
                {"step": 7, "action": "init_watchers", "services": ["success_watcher", "token_watcher", "process_watcher", "backup_service"]},
                {"step": 8, "action": "run_routines", "path": "_boot/micro-routines.json"},
                {"step": 9, "action": "ready", "status": "operational"}
            ]
        }, indent=2, ensure_ascii=False),

        "_boot/micro-routines.json": json.dumps({
            "version": "3.0.0",
            "enabled": True,
            "pre_prompt_checks": [
                {"id": "check-001", "name": "Memory Retrieval", "priority": 1, "enabled": True},
                {"id": "check-002", "name": "Inbox Check", "priority": 2, "enabled": True},
                {"id": "check-003", "name": "Token Budget Check", "priority": 3, "enabled": True},
                {"id": "check-004", "name": "Backup Status", "priority": 4, "enabled": True}
            ],
            "post_response_actions": [
                {"id": "action-001", "name": "Store Episode", "condition": "significant_interaction", "enabled": True},
                {"id": "action-002", "name": "Update Success Metrics", "condition": "task_completed", "enabled": True},
                {"id": "action-003", "name": "Track Token Usage", "condition": "always", "enabled": True},
                {"id": "action-004", "name": "Auto-Backup Check", "condition": "destructive_operation", "enabled": True}
            ]
        }, indent=2, ensure_ascii=False),

        "_boot/shutdown-protocol.json": json.dumps({
            "version": "3.0.0",
            "max_duration_minutes": 5,
            "phases": {
                "phase_1": {"name": "Working Memory Save", "duration": "30s"},
                "phase_2": {"name": "Task Management", "duration": "1min"},
                "phase_3": {"name": "Create Backup Snapshot", "duration": "1min", "new_in_v3": True},
                "phase_4": {"name": "Memory Consolidation", "duration": "1min"},
                "phase_5": {"name": "Registry Update", "duration": "30s"},
                "phase_6": {"name": "Finalization", "duration": "30s", "optional_if_timeout": True}
            }
        }, indent=2, ensure_ascii=False),

        "_boot/triggers.json": json.dumps({
            "version": "3.0.0",
            "triggers": {
                "memory": {"phrases": ["Erinnerst du dich", "Weißt du noch"], "action": "memory_router.retrieve"},
                "code": {"phrases": ["Erstelle Code", "Programmiere"], "skill": "skills/code"},
                "delegate": {"phrases": ["Delegiere", "Gib ab an"], "skill": "skills/delegate"},
                "communicate": {"phrases": ["Sende Nachricht", "Schreib an"], "skill": "skills/communicate"},
                "backup": {"phrases": ["Sichere", "Backup erstellen"], "service": "backup_service"}
            }
        }, indent=2, ensure_ascii=False),

        # ═══════════════════════════════════════════════════════════════════════
        # _backup/ FILES (🆕 v3.0)
        # ═══════════════════════════════════════════════════════════════════════
        
        "_backup/SKILL.md": '''# Backup System (🆕 v3.0)

## 📋 Übersicht
Backup & Recovery System für sichere Operationen.

## Struktur

| Pfad | Zweck |
|------|-------|
| `trash/` | Papierkorb - Dateien vor Löschung |
| `snapshots/` | Manuelle Snapshots des Systems |
| `backup_log.json` | Historie aller Backup-Operationen |

## Verwendung

### Vor destruktiven Operationen
```
1. Datei nach _backup/trash/ kopieren
2. Operation durchführen
3. backup_log.json aktualisieren
```

### Snapshot erstellen
```
1. Wichtige Dateien nach _backup/snapshots/YYYYMMDD_HHMMSS/ kopieren
2. backup_log.json aktualisieren
```

### Recovery
```
1. backup_log.json prüfen
2. Datei aus trash/ oder snapshots/ wiederherstellen
```

## Regeln

- **Papierkorb leeren:** Nach 30 Tagen automatisch (cleanup_config)
- **Snapshots behalten:** Manuell verwaltet
- **Wichtig:** Vor jeder Löschoperation zuerst sichern!
''',

        "_backup/backup_log.json": json.dumps({
            "version": "3.0.0",
            "entries": [],
            "summary": {
                "total_backups": 0,
                "trash_items": 0,
                "snapshots": 0,
                "last_backup": None
            }
        }, indent=2, ensure_ascii=False),

        # ═══════════════════════════════════════════════════════════════════════
        # _data/ FILES (🆕 v3.0)
        # ═══════════════════════════════════════════════════════════════════════
        
        "_data/tasks.json": json.dumps([
            {
                "_schema": "BEISPIEL - Diese Task löschen und eigene erstellen",
                "id": "task_001",
                "title": "System konfigurieren",
                "status": "open",
                "priority": "normal",
                "created": GENERATED_DATE,
                "description": "SKILL.md anpassen und System personalisieren"
            }
        ], indent=2, ensure_ascii=False),

        "_data/tasks_done.json": "[]",

        # ═══════════════════════════════════════════════════════════════════════
        # Weitere Standard-Templates
        # ═══════════════════════════════════════════════════════════════════════
        
        "_registry/SKILL.md": '''# Registry System

## 📋 Übersicht
Zentrale Wahrheitsquellen für das System.

## Registries
- `master.json` - Master-Registry mit allen Verweisen
- `skills.json` - Skill-Registry
- `tools.json` - Tool-Registry
- `configs.json` - Config-Registry
''',

        "_memory/SKILL.md": '''# Memory System

## 📋 Übersicht
Kognitive Memory-Architektur basierend auf Kognitionspsychologie.

## Subsysteme

| Subsystem | Funktion |
|-----------|----------|
| `_meta/` | Metagedächtnis (Konfidenz, Blind Spots, Consciousness) |
| `working/` | Arbeitsgedächtnis (Scratchpad, Context) |
| `episodic/` | Episodisches Gedächtnis (Timeline, Sessions) |
| `semantic/` | Semantisches Gedächtnis (Facts, Concepts) |
| `procedural/` | Prozedurales Gedächtnis (Skills, Patterns) |
| `emotional/` | Emotionale Modulation (Importance) |
| `consolidation/` | Konsolidierung (EP → SEM) |
| `config/` | Memory-Konfiguration |
''',

        "_communication/SKILL.md": '''# Communication System

## 📋 Übersicht
Bidirektionale Kommunikation zwischen User und AI.

## Konzept: Ich, Du, Wir

```
┌─────────────────┐                    ┌─────────────────┐
│      USER       │                    │       AI        │
│                 │                    │                 │
│  (sendet via    │──── inbox/ ───────►│  (empfängt)     │
│   outbox)       │                    │                 │
│                 │◄─── outbox/ ───────│  (sendet)       │
│  (empfängt)     │                    │                 │
└─────────────────┘                    └─────────────────┘
```

## Struktur
- `channels/inbox/` - AI empfängt
- `channels/outbox/` - AI sendet
- `async_queue.json` - Asynchrone Warteschlange
''',

        "actors/SKILL.md": '''# Actors System

## 📋 Übersicht
Akteur-Profile für das 6-Akteure-Modell.

## Die Akteure

| Akteur | Ordner | Beschreibung |
|--------|--------|--------------|
| User | `user/` | Der Mensch (Entscheider) |
| AI | `ai/` | Der Geist (Operierende AI) |
| External AIs | `external_ais/` | Gemini, Ollama, Copilot... |

## Konzept: "Ich, Du, Wir"
- **ICH** (AI) - Austauschbar, nicht hardcoded
- **DU** (User) - Aktiver Teilnehmer mit Profil
- **WIR** (System) - Geteilter Workspace
''',

        "tools/SKILL.md": '''# Tools

## 📋 Übersicht
Werkzeuge und Services des Systems.

## Struktur v3.0

```
tools/
├── mcp-servers/      # MCP-Server-Definitionen
├── services/         # Interne Services
│   ├── memory_router/
│   ├── success_watcher/
│   ├── token_watcher/
│   ├── process_watcher/
│   └── backup_service/    # 🆕 v3.0
├── patterns/         # Tool-Design-Patterns
└── utilities/
```
''',

        "skills/SKILL.md": '''# Skills

## 📋 Übersicht
Ausführbare Skills des Systems.

## Kategorien

| Skill | Funktion |
|-------|----------|
| `code/` | Code-Erstellung und -Analyse |
| `communicate/` | Kommunikation mit Akteuren |
| `analyze/` | Analyse und Research |
| `create/` | Kreative Erstellung |
| `delegate/` | Delegation an andere Akteure |
''',

        "gui/SKILL.md": '''# GUI

## 📋 Übersicht
Dashboards und Module für das System.

## Dashboards v3.0
- `boot-dashboard.html` - Boot-Status
- `memory-dashboard.html` - Memory-Übersicht
- `token-dashboard.html` - Token-Tracking
- `success-dashboard.html` - Erfolgs-Metriken
- `backup-dashboard.html` - Backup-Status (🆕)
''',

        "reports/SKILL.md": '''# Reports

## 📋 Übersicht
Dokumentation und Berichte.

## Struktur
- `current/` - Aktuelle Berichte
- `archive/` - Archivierte Berichte
- `templates/` - Berichts-Vorlagen
''',

        "system/system/system/system/exports/SKILL.md": '''# Exports

## 📋 Übersicht
Deployment und Paketierung.

## Struktur
- `packages/` - Exportierte Pakete
- `installer/` - Installations-Scripts
''',

        "connections/SKILL.md": '''# Connections

## 📋 Übersicht
Externe Verbindungen zu anderen Akteuren und APIs.
''',

        "_config/SKILL.md": '''# Configuration

## 📋 Übersicht
System-Konfigurationen.

## Dateien
- `system.json` - System-Einstellungen
- `user.json` - User-Einstellungen
- `integrations.json` - Externe Integrationen
''',
    }


# =============================================================================
# GENERATOR-FUNKTIONEN
# =============================================================================

def create_structure(base_path: Path, structure: dict, templates: dict, parent_path: str = ""):
    """Erstellt die Ordnerstruktur rekursiv."""
    
    for key, value in structure.items():
        if key == "_files":
            for filename in value:
                file_path = base_path / filename
                
                # Template-Key ermitteln
                template_key = f"{parent_path}/{filename}" if parent_path else filename
                
                # Suche nach Template
                content = ""
                if template_key in templates:
                    content = templates[template_key]
                elif filename in templates:
                    content = templates[filename]
                else:
                    # Generisches Template
                    if filename.endswith('.json'):
                        content = json.dumps({"version": "3.0.0"}, indent=2)
                    elif filename.endswith('.md'):
                        content = f"# {filename}\n\nPlaceholder.\n"
                    elif filename.endswith('.py'):
                        content = f"#!/usr/bin/env python3\n# {filename}\n\npass\n"
                    elif filename.endswith('.html'):
                        content = f"<!DOCTYPE html>\n<html><head><title>{filename}</title></head><body></body></html>\n"
                    elif filename == ".gitkeep":
                        content = "# Placeholder\n"
                    else:
                        content = ""
                
                file_path.write_text(content, encoding='utf-8')
                rel_path = f"{parent_path}/{filename}" if parent_path else filename
                print(f"  📄 {rel_path}")
        else:
            folder_path = base_path / key
            folder_path.mkdir(parents=True, exist_ok=True)
            
            new_parent = f"{parent_path}/{key}" if parent_path else key
            print(f"  📁 {new_parent}/")
            
            if isinstance(value, dict):
                create_structure(folder_path, value, templates, new_parent)


def print_banner():
    """Zeigt Banner"""
    print("=" * 70)
    print("  UNIVERSAL LLM OS GENERATOR v3.0 - BACH_STREAM BUILD TOOL")
    print("=" * 70)
    print()
    print("  Die drei Säulen: MEMORY + TOOLS + COMMUNICATION")
    print("  Neu in v3.0: Backup-System, einfache Tasks")
    print()


def generate(name: str, target_path: str):
    """Hauptfunktion: Generiert die komplette Struktur."""
    
    base = Path(target_path) / name
    
    print(f"\n📍 Zielverzeichnis: {base}\n")
    
    # Prüfe ob bereits existiert
    if base.exists():
        print(f"⚠️  Ordner existiert bereits: {base}")
        response = input("   Überschreiben? (j/n): ").strip().lower()
        if response != 'j':
            print("   Abgebrochen.\n")
            return False
        import shutil
        shutil.rmtree(base)
        print("   Alter Ordner gelöscht.\n")
    
    # Erstelle Basis-Ordner
    base.mkdir(parents=True, exist_ok=True)
    print(f"✅ Basis-Ordner erstellt\n")
    
    # Templates laden
    templates = get_templates(name)
    
    # Erstelle Struktur
    print("📂 Erstelle Struktur:\n")
    create_structure(base, STRUCTURE, templates)
    
    # Statistiken
    file_count = sum(1 for _ in base.rglob("*") if _.is_file())
    dir_count = sum(1 for _ in base.rglob("*") if _.is_dir())
    
    print(f"\n{'='*70}")
    print(f"  ✅ Universal LLM OS '{name}' erfolgreich erstellt!")
    print(f"  📍 Pfad: {base}")
    print(f"  📁 Ordner: {dir_count}")
    print(f"  📄 Dateien: {file_count}")
    print(f"{'='*70}")
    print(f"\n  🆕 Neue Komponenten in v3.0:")
    print(f"     • _backup/ - Backup & Recovery System")
    print(f"     • _data/ - Einfaches Task-System")
    print(f"     • backup_service - Aktiver Backup-Service")
    print(f"     • Erweiterte Boot-Sequenz mit Backup-Check")
    print(f"\n")
    
    return True


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print_banner()
    
    if len(sys.argv) < 2:
        print("Verwendung:")
        print("  python os_generator_v3.py <name> [zielordner]")
        print()
        print("Beispiele:")
        print('  python os_generator_v3.py mein-os')
        print('  python os_generator_v3.py mein-os "C:\Projekte"')
        sys.exit(1)
    
    name = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    
    generate(name, target)
