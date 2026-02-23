#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2026 Lukas Geiger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Tool: c_structure_generator
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version c_structure_generator

Description:
    [Beschreibung hinzufügen]

Usage:
    python c_structure_generator.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

# -*- coding: utf-8 -*-
"""
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
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# =============================================================================
# PROFIL-DEFINITIONEN
# =============================================================================

# MICRO = Absolute Teilfähigkeit - nur Datei(en)
PROFILE_MICRO = {
    "_files": ["SKILL.md"],
    "_type": "micro"
}

# LIGHT = Minimale Struktur
PROFILE_LIGHT = {
    "_files": ["SKILL.md", "README.md"],
    "_config": {"_files": ["config.json"]},
    "_data": {"_files": ["tasks.json"]}
}

# STANDARD = Skill mit einfachem Memory
PROFILE_STANDARD = {
    "_files": ["SKILL.md", "README.md", "CHANGELOG.md"],
    "_docs": {"_files": ["USAGE.md"]},
    "_config": {"_files": ["config.json"]},
    "_data": {"_files": ["tasks.json"]},
    "_memory": {"_files": ["usage_log.json", "lessons_learned.md", "preferences.json"]},
    "_templates": {"_files": [".gitkeep"]}
}

# EXTENDED = Skill mit Mikro-Skills
PROFILE_EXTENDED = {
    "_files": ["SKILL.md", "README.md", "CHANGELOG.md"],
    "_docs": {"_files": ["USAGE.md", "ARCHITECTURE.md"]},
    "_config": {"_files": ["config.json", "tools.json"]},
    "_data": {"_files": ["tasks.json", "tasks_done.json"]},
    "_memory": {
        "_files": ["usage_log.json", "lessons_learned.md", "preferences.json"],
        "context": {"_files": ["current.json"]}
    },
    "_micro_skills": {"_files": ["registry.json"]},
    "_templates": {"_files": [".gitkeep"]},
    "_backup": {"_files": [".gitkeep"]}
}

# AGENT = Orchestriert Skills zu Workflows
PROFILE_AGENT = {
    "_files": ["SKILL.md", "README.md", "CHANGELOG.md"],
    "_docs": {"_files": ["ARCHITECTURE.md", "WORKFLOWS.md", "SKILLS_OVERVIEW.md"]},
    "_config": {"_files": ["config.json", "skills.json", "workflow_config.json"]},
    "_data": {
        "_files": ["tasks.json", "tasks_done.json"],
        "projekte": {"_files": [".gitkeep"]},
        "inputs": {"_files": [".gitkeep"]},
        "outputs": {"_files": [".gitkeep"]}
    },
    "_memory": {
        "_files": ["context.md", "preferences.json"],
        "session": {"_files": [".gitkeep"]},
        "global": {"_files": ["lessons_learned.md", "entscheidungen.md"]},
        "projekte": {"_files": [".gitkeep"]}
    },
    "_workflows": {"_files": ["_index.md", "beispiel_workflow.md"]},
    "_skills": {
        "_files": ["_registry.json"],
        "_templates": {"_files": ["skill_template.md"]}
    },
    "_backup": {"_files": [".gitkeep"]},
    "_reports": {
        "sessions": {"_files": [".gitkeep"]},
        "projekte": {"_files": [".gitkeep"]}
    }
}

# AGENT_FULL = Vollständiger Agent
PROFILE_AGENT_FULL = {
    "_files": ["SKILL.md", "README.md", "CHANGELOG.md"],
    "_docs": {
        "_files": ["ARCHITECTURE.md", "WORKFLOWS.md", "SKILLS_OVERVIEW.md", 
                   "LIFECYCLE.md", "PATTERNS.md"]
    },
    "_config": {
        "_files": ["config.json", "skills.json", "workflow_config.json", 
                   "tools.json", "routines.json"]
    },
    "_data": {
        "_files": ["tasks.json", "tasks_done.json"],
        "projekte": {"_files": [".gitkeep"]},
        "inputs": {"_files": [".gitkeep"]},
        "outputs": {"_files": [".gitkeep"]},
        "cache": {"_files": [".gitkeep"]}
    },
    "_memory": {
        "_files": ["context.md", "preferences.json"],
        "session": {"_files": [".gitkeep"]},
        "global": {"_files": ["lessons_learned.md", "entscheidungen.md", "expertise.md"]},
        "projekte": {"_files": [".gitkeep"]},
        "episodic": {"_files": ["_index.json"]}
    },
    "_workflows": {
        "_files": ["_index.md", "beispiel_workflow.md"],
        "templates": {"_files": [".gitkeep"]},
        "active": {"_files": [".gitkeep"]}
    },
    "_skills": {
        "_files": ["_registry.json"],
        "_templates": {"_files": ["skill_template.md", "micro_skill_template.md"]}
    },
    "_tools": {
        "_files": ["registry.json"],
        "utilities": {"_files": [".gitkeep"]}
    },
    "_backup": {
        "trash": {"_files": [".gitkeep"]},
        "snapshots": {"_files": [".gitkeep"]}
    },
    "_reports": {
        "sessions": {"_files": [".gitkeep"]},
        "projekte": {"_files": [".gitkeep"]},
        "analysis": {"_files": [".gitkeep"]}
    },
    "_concepts": {
        "inbox": {"_files": [".gitkeep"]},
        "approved": {"_files": [".gitkeep"]}
    }
}

# Embedded-Versionen (für Nutzung im OS)
PROFILE_EMBEDDED_SKILL = {
    "_files": ["SKILL.md"],
    "_type": "embedded"
}

PROFILE_EMBEDDED_AGENT = {
    "_files": ["SKILL.md", "workflows.md", "skills_used.md"],
    "_type": "embedded"
}

PROFILES = {
    "MICRO": PROFILE_MICRO,
    "LIGHT": PROFILE_LIGHT,
    "STANDARD": PROFILE_STANDARD,
    "EXTENDED": PROFILE_EXTENDED,
    "AGENT": PROFILE_AGENT,
    "AGENT_FULL": PROFILE_AGENT_FULL,
    # Embedded
    "EMBEDDED_SKILL": PROFILE_EMBEDDED_SKILL,
    "EMBEDDED_AGENT": PROFILE_EMBEDDED_AGENT
}

PROFILE_INFO = {
    "MICRO": ("Skill", "Nur Datei(en), kein Ordner", "1 Datei"),
    "LIGHT": ("Skill", "Minimale Struktur", "~5 Dateien"),
    "STANDARD": ("Skill", "Mit Memory und Lessons", "~12 Dateien"),
    "EXTENDED": ("Skill", "Mit Mikro-Skills", "~20 Dateien"),
    "AGENT": ("Agent", "Orchestriert Skills", "~30 Dateien"),
    "AGENT_FULL": ("Agent", "Vollständig, näher am OS", "~50 Dateien"),
    "EMBEDDED_SKILL": ("Embedded", "Skill für OS", "1 Datei"),
    "EMBEDDED_AGENT": ("Embedded", "Agent für OS", "3 Dateien")
}

# =============================================================================
# DATEI-TEMPLATES
# =============================================================================

def get_skill_md(name: str, profile: str, embedded: bool = False) -> str:
    """Generiert SKILL.md basierend auf Profil"""
    
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Für MICRO und Embedded: kompakte Version
    if profile == "MICRO" or embedded:
        return f'''---
name: {name}
type: {"embedded-" if embedded else ""}{"agent" if "AGENT" in profile else "skill"}
profile: {profile}
version: 0.1.0
created: {date}
---

# {name}

> [BESCHREIBUNG]

## Wann nutzen?

- [Trigger 1]
- [Trigger 2]

## Vorgehen

### 1. [Schritt]
[Beschreibung]

### 2. [Schritt]
[Beschreibung]

## Beispiel

**Input:** [Beispiel]
**Output:** [Ergebnis]

---
*Generiert mit structure_generator (BACH_STREAM)*
'''
    
    # Für Skills (LIGHT bis EXTENDED)
    if profile in ["LIGHT", "STANDARD", "EXTENDED"]:
        memory_section = ""
        if profile in ["STANDARD", "EXTENDED"]:
            memory_section = """
## Memory

- `_memory/usage_log.json` - Nutzungsverlauf
- `_memory/lessons_learned.md` - Was funktioniert
- `_memory/preferences.json` - Präferenzen
"""
        
        micro_skills = ""
        if profile == "EXTENDED":
            micro_skills = """
## Mikro-Skills

| Mikro-Skill | Zweck |
|-------------|-------|
| [name] | [beschreibung] |

Registry: `_micro_skills/registry.json`
"""
        
        return f'''---
name: {name}
type: skill
profile: {profile}
version: 0.1.0
created: {date}
generator: structure_generator
---

# {name}

> Skill ({profile}) - [BESCHREIBUNG]

## Quick Start

1. Lies diese Datei
2. Prüfe `_data/tasks.json`
3. Konfiguration in `_config/config.json`

## Wann nutzen?

- [Trigger 1]
- [Trigger 2]

## Vorgehen

### 1. [Schritt]
[Beschreibung]

### 2. [Schritt]
[Beschreibung]
{memory_section}{micro_skills}
## Beispiel

**Input:** [Beispiel]
**Output:** [Ergebnis]

---
*Generiert mit structure_generator (BACH_STREAM)*
'''
    
    # Für Agents (AGENT, AGENT_FULL)
    return f'''---
name: {name}
type: agent
profile: {profile}
version: 0.1.0
created: {date}
generator: structure_generator
---

# {name}

> Agent ({profile}) - Orchestriert Skills zu Workflows

## Quick Start

1. Lies diese Datei
2. Prüfe Projekte: `_data/projekte/`
3. Lade Memory: `_memory/context.md`
4. Prüfe Tasks: `_data/tasks.json`

## Was macht dieser Agent?

[BESCHREIBUNG]

## Wann nutzen?

- [Trigger 1: Komplexe Aufgabe]
- [Trigger 2: Projekt über Zeit]

## Workflows

| Workflow | Beschreibung | Skills |
|----------|--------------|--------|
| [name] | [beschreibung] | [skills] |

Details: `_workflows/_index.md`

## Skills

| Skill | Zweck |
|-------|-------|
| [name] | [beschreibung] |

Registry: `_skills/_registry.json`

## Memory

| Typ | Pfad | Zweck |
|-----|------|-------|
| Session | `_memory/session/` | Kurzzeit |
| Global | `_memory/global/` | Langzeit |
| Projekte | `_memory/projekte/` | Pro-Projekt |

---
*Generiert mit structure_generator (BACH_STREAM)*
'''


def get_readme(name: str, profile: str) -> str:
    """README.md"""
    ptype, desc, size = PROFILE_INFO.get(profile, ("", "", ""))
    return f'''# {name}

> {ptype} - Profil: {profile}
> {desc} ({size})

## Für Claude

**Einstiegspunkt:** `SKILL.md`

## Generiert mit

structure_generator.py (BACH_STREAM)

---
*Erstellt: {datetime.now().strftime("%Y-%m-%d")}*
'''


def get_changelog(name: str) -> str:
    return f'''# Changelog - {name}

## [0.1.0] - {datetime.now().strftime("%Y-%m-%d")}

### Hinzugefügt
- Initiale Struktur erstellt
'''


def get_config_json(name: str, profile: str) -> str:
    config = {
        "name": name,
        "type": "agent" if "AGENT" in profile else "skill",
        "profile": profile,
        "version": "0.1.0",
        "generator": "structure_generator",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "settings": {}
    }
    
    if profile in ["STANDARD", "EXTENDED", "AGENT", "AGENT_FULL"]:
        config["settings"]["memory_enabled"] = True
    
    if profile in ["AGENT", "AGENT_FULL"]:
        config["settings"]["workflows_enabled"] = True
        config["settings"]["track_projects"] = True
    
    if profile == "AGENT_FULL":
        config["settings"]["routines_enabled"] = True
    
    return json.dumps(config, indent=4, ensure_ascii=False)


def get_generic_json(template_type: str) -> str:
    """Generiert verschiedene JSON-Dateien"""
    templates = {
        "tasks": [{"_example": True, "id": "task_001", "title": "Konfigurieren", 
                   "status": "open", "created": datetime.now().strftime("%Y-%m-%d")}],
        "tasks_done": [],
        "usage_log": {"version": "1.0", "entries": [], "summary": {"total_uses": 0}},
        "preferences": {"version": "1.0", "user_preferences": {}, "learned_defaults": {}},
        "registry": {"version": "1.0", "items": []},
        "skills_registry": {"version": "1.0", "skills": [], "note": "Registrierte Skills"},
        "tools": {"version": "1.0", "tools": []},
        "routines": {"version": "1.0", "enabled": False, 
                     "pre_session": [{"name": "load_context", "enabled": True}],
                     "post_session": [{"name": "save_lessons", "enabled": True}]},
        "workflow_config": {"version": "1.0", "workflow_path": "_workflows/", 
                            "settings": {"auto_memory_update": True}},
        "skills_config": {"version": "1.0", "skill_paths": ["_skills/"], "auto_discover": True},
        "index": {"version": "1.0", "entries": []},
        "current": {"version": "1.0", "current_task": None, "active_context": {}}
    }
    return json.dumps(templates.get(template_type, {}), indent=4, ensure_ascii=False)


def get_generic_md(template_type: str, name: str) -> str:
    """Generiert verschiedene MD-Dateien"""
    templates = {
        "usage": f"# Verwendung: {name}\n\n## Grundlegende Nutzung\n\n[TODO]\n",
        "architecture": f"# Architektur: {name}\n\n## Struktur\n\n[TODO]\n",
        "workflows": f"# Workflows: {name}\n\n## Übersicht\n\n[TODO]\n",
        "skills_overview": f"# Skills: {name}\n\n## Registrierte Skills\n\n[TODO]\n",
        "lifecycle": f"# Lifecycle: {name}\n\n## Session-Start\n\n[TODO]\n",
        "patterns": f"# Patterns: {name}\n\n## Workflow-Patterns\n\n[TODO]\n",
        "lessons": f"# Lessons Learned: {name}\n\n## Was funktioniert\n\n- [TODO]\n",
        "entscheidungen": f"# Entscheidungen: {name}\n\n## Log\n\n[TODO]\n",
        "expertise": f"# Expertise: {name}\n\n[TODO]\n",
        "context": f"# Kontext: {name}\n\n## Aktueller Fokus\n\n[TODO]\n",
        "workflow_index": f"# Workflows Index\n\n| Workflow | Status |\n|----------|--------|\n| beispiel | Aktiv |\n",
        "beispiel_workflow": "# Workflow: Beispiel\n\n## Trigger\n\n- [TODO]\n\n## Phasen\n\n### Phase 1\n- Skill: [name]\n",
        "skill_template": "---\nname: [NAME]\ntype: skill\n---\n\n# [NAME]\n\n[TODO]\n",
        "micro_skill_template": "---\nname: [NAME]\ntype: micro-skill\n---\n\n# [NAME]\n\n[TODO]\n",
        "workflows_used": "# Workflows\n\n## Diesen Agent\n\n[TODO]\n",
        "skills_used": "# Genutzte Skills\n\n| Skill | Pfad |\n|-------|------|\n| [name] | [pfad] |\n"
    }
    return templates.get(template_type, f"# {template_type}\n\n[TODO]\n")


# =============================================================================
# FILE CONTENT RESOLVER
# =============================================================================

def get_file_content(filename: str, name: str, profile: str) -> str:
    """Gibt Inhalt für eine Datei zurück"""
    
    # Haupt-Dateien
    if filename == "SKILL.md":
        return get_skill_md(name, profile)
    if filename == "README.md":
        return get_readme(name, profile)
    if filename == "CHANGELOG.md":
        return get_changelog(name)
    
    # Config JSONs
    if filename == "config.json":
        return get_config_json(name, profile)
    if filename == "tasks.json":
        return get_generic_json("tasks")
    if filename == "tasks_done.json":
        return get_generic_json("tasks_done")
    if filename == "usage_log.json":
        return get_generic_json("usage_log")
    if filename == "preferences.json":
        return get_generic_json("preferences")
    if filename == "tools.json":
        return get_generic_json("tools")
    if filename == "routines.json":
        return get_generic_json("routines")
    if filename == "workflow_config.json":
        return get_generic_json("workflow_config")
    if filename == "skills.json":
        return get_generic_json("skills_config")
    if filename == "_registry.json":
        return get_generic_json("skills_registry")
    if filename == "registry.json":
        return get_generic_json("registry")
    if filename == "_index.json":
        return get_generic_json("index")
    if filename == "current.json":
        return get_generic_json("current")
    
    # Docs MDs
    if filename == "USAGE.md":
        return get_generic_md("usage", name)
    if filename == "ARCHITECTURE.md":
        return get_generic_md("architecture", name)
    if filename == "WORKFLOWS.md":
        return get_generic_md("workflows", name)
    if filename == "SKILLS_OVERVIEW.md":
        return get_generic_md("skills_overview", name)
    if filename == "LIFECYCLE.md":
        return get_generic_md("lifecycle", name)
    if filename == "PATTERNS.md":
        return get_generic_md("patterns", name)
    
    # Memory MDs
    if filename == "lessons_learned.md":
        return get_generic_md("lessons", name)
    if filename == "entscheidungen.md":
        return get_generic_md("entscheidungen", name)
    if filename == "expertise.md":
        return get_generic_md("expertise", name)
    if filename == "context.md":
        return get_generic_md("context", name)
    
    # Workflow MDs
    if filename == "_index.md":
        return get_generic_md("workflow_index", name)
    if filename == "beispiel_workflow.md":
        return get_generic_md("beispiel_workflow", name)
    
    # Skill Templates
    if filename == "skill_template.md":
        return get_generic_md("skill_template", name)
    if filename == "micro_skill_template.md":
        return get_generic_md("micro_skill_template", name)
    
    # Embedded Agent
    if filename == "workflows.md":
        return get_generic_md("workflows_used", name)
    if filename == "skills_used.md":
        return get_generic_md("skills_used", name)
    
    # Fallback
    if filename == ".gitkeep":
        return "# Placeholder\n"
    
    return f"# {filename}\n\n[TODO]\n"


# =============================================================================
# GENERATOR
# =============================================================================

def create_structure(base_path: Path, structure: dict, name: str, profile: str, indent: int = 0):
    """Erstellt rekursiv die Ordnerstruktur"""
    prefix = "  " * indent
    
    for key, value in structure.items():
        if key == "_files":
            for filename in value:
                file_path = base_path / filename
                content = get_file_content(filename, name, profile)
                file_path.write_text(content, encoding='utf-8')
                print(f"{prefix}📄 {filename}")
        elif key == "_type":
            continue
        else:
            folder_path = base_path / key
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"{prefix}📁 {key}/")
            if isinstance(value, dict):
                create_structure(folder_path, value, name, profile, indent + 1)


def generate_micro(name: str, target: Path, profile: str) -> bool:
    """Generiert MICRO/EMBEDDED - nur Datei(en)"""
    
    if profile in ["MICRO", "EMBEDDED_SKILL"]:
        file_path = target / f"{name}.md"
        content = get_skill_md(name, profile, embedded=(profile == "EMBEDDED_SKILL"))
        file_path.write_text(content, encoding='utf-8')
        print(f"\n  📄 {name}.md")
    
    elif profile == "EMBEDDED_AGENT":
        # Mehrere Dateien für embedded Agent
        for filename in ["SKILL.md", "workflows.md", "skills_used.md"]:
            file_path = target / f"{name}_{filename}" if filename != "SKILL.md" else target / f"{name}.md"
            content = get_file_content(filename, name, profile)
            file_path.write_text(content, encoding='utf-8')
            print(f"  📄 {file_path.name}")
    
    print(f"\n{'='*60}")
    print(f"  ✅ '{name}' erstellt! (Profil: {profile})")
    print(f"  📍 Pfad: {target}")
    print(f"{'='*60}\n")
    return True


def generate(name: str, profile: str, target: Path) -> bool:
    """Hauptgenerator"""
    
    # MICRO und EMBEDDED: Nur Dateien
    if profile in ["MICRO", "EMBEDDED_SKILL", "EMBEDDED_AGENT"]:
        return generate_micro(name, target, profile)
    
    # Andere Profile: Ordnerstruktur
    output_path = target / name
    
    if output_path.exists():
        print(f"\n[!] Ordner existiert: {output_path}")
        response = input("    Überschreiben? (j/N): ").strip().lower()
        if response != 'j':
            print("    Abgebrochen.")
            return False
        import shutil
        shutil.rmtree(output_path)
    
    print(f"\n[+] Erstelle {profile}-Struktur...\n")
    
    output_path.mkdir(parents=True)
    structure = PROFILES[profile]
    
    # Root-Dateien
    if "_files" in structure:
        for filename in structure["_files"]:
            file_path = output_path / filename
            content = get_file_content(filename, name, profile)
            file_path.write_text(content, encoding='utf-8')
            print(f"  📄 {filename}")
    
    # Ordner
    for key, value in structure.items():
        if key not in ["_files", "_type"]:
            folder_path = output_path / key
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"  📁 {key}/")
            if isinstance(value, dict):
                create_structure(folder_path, value, name, profile, 1)
    
    # Statistik
    file_count = sum(1 for _ in output_path.rglob("*") if _.is_file())
    dir_count = sum(1 for _ in output_path.rglob("*") if _.is_dir())
    
    print(f"\n{'='*60}")
    print(f"  ✅ '{name}' erstellt!")
    print(f"  📍 Pfad: {output_path}")
    print(f"  📁 {dir_count} Ordner | 📄 {file_count} Dateien")
    print(f"{'='*60}\n")
    
    return True


# =============================================================================
# CLI
# =============================================================================

def print_banner():
    print("=" * 65)
    print("  STRUCTURE GENERATOR v1.0 - BACH_STREAM BUILD TOOL")
    print("=" * 65)
    print()
    print("  Skill ←──────── Spektrum ────────→ Agent")
    print()
    print("  Profile:")
    print("    MICRO        Nur Datei (Skill)")
    print("    LIGHT        Minimal (Skill)")
    print("    STANDARD     Mit Memory (Skill)")
    print("    EXTENDED     Mit Mikro-Skills (Skill)")
    print("    AGENT        Mit Workflows (Agent)")
    print("    AGENT_FULL   Vollständig (Agent)")
    print()
    print("  Embedded (für OS-Nutzung):")
    print("    --embedded skill  → 1 Datei")
    print("    --embedded agent  → 3 Dateien")
    print()


def main():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(
        description='Generiert Skill- und Agent-Strukturen',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('name', nargs='?', help='Name der Struktur')
    parser.add_argument('profile', nargs='?', default='STANDARD',
                        help='Profil: MICRO|LIGHT|STANDARD|EXTENDED|AGENT|AGENT_FULL')
    parser.add_argument('target', nargs='?', default='.', help='Zielordner')
    parser.add_argument('--embedded', choices=['skill', 'agent'],
                        help='Embedded-Modus für OS-Nutzung')
    parser.add_argument('--list', action='store_true', help='Zeigt alle Profile')
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.list:
        print("  Verfügbare Profile:\n")
        for p, (ptype, desc, size) in PROFILE_INFO.items():
            print(f"    {p:15} {ptype:8} {desc:30} {size}")
        print()
        return 0
    
    if not args.name:
        parser.print_help()
        print("\n[!] Name ist erforderlich\n")
        return 1
    
    # Embedded-Modus
    if args.embedded:
        profile = f"EMBEDDED_{args.embedded.upper()}"
    else:
        profile = args.profile.upper()
    
    if profile not in PROFILES:
        print(f"[!] Unbekanntes Profil: {profile}")
        print(f"    Verfügbar: {', '.join(PROFILES.keys())}")
        return 1
    
    ptype, desc, size = PROFILE_INFO.get(profile, ("", "", ""))
    target = Path(args.target)
    
    print(f"[+] Name:    {args.name}")
    print(f"[+] Profil:  {profile} ({ptype})")
    print(f"[+] Info:    {desc} ({size})")
    print(f"[+] Ziel:    {target.absolute()}")
    
    success = generate(args.name, profile, target)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
