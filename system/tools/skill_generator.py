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
skill_generator_v3.py
=====================
Generiert Skill-Strukturen von MICRO bis EXTENDED.

Version: 3.0.0
Erstellt: 2026-01-14
Basis: skill_generator_v2.py + SKILL_AGENT_OS_DEFINITIONS.md

PROFILE:
  MICRO    = Nur Datei(en), kein Ordnersystem (absolute Teilfähigkeit)
  LIGHT    = Minimale Struktur (SKILL.md + _config + _data)
  STANDARD = Standard-Skill mit einfachem Memory
  EXTENDED = Komplexer Skill mit Mikro-Skills (näher am Agent)

Verwendung:
    python skill_generator_v3.py [name] [profil] [zielordner]
    
    profil: MICRO | LIGHT | STANDARD | EXTENDED (default: STANDARD)
    
Beispiele:
    python skill_generator_v3.py analyse-workflow MICRO .
    python skill_generator_v3.py mein-skill LIGHT .
    python skill_generator_v3.py mein-skill STANDARD .
    python skill_generator_v3.py komplexer-skill EXTENDED .

Für Agents → agent_generator_v1.py
Für OS → os_generator_v3.py
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# =============================================================================
# PROFIL-DEFINITIONEN
# =============================================================================

# MICRO = Absolute Teilfähigkeit - nur Datei(en), kein Ordnersystem
# Ausgabe: Eine oder mehrere .md/.txt Dateien direkt
PROFILE_MICRO = {
    "_files": ["SKILL.md"],
    "_type": "micro"  # Marker für Spezialbehandlung
}

# LIGHT = Minimale Struktur für einfache Skills
PROFILE_LIGHT = {
    "_files": ["SKILL.md", "README.md"],
    "_config": {
        "_files": ["config.json"]
    },
    "_data": {
        "_files": ["tasks.json"]
    }
}

# STANDARD = Standard-Skill mit einfachem Memory und Lessons
PROFILE_STANDARD = {
    "_files": ["SKILL.md", "README.md", "CHANGELOG.md"],
    "_docs": {
        "_files": ["USAGE.md"]
    },
    "_config": {
        "_files": ["config.json"]
    },
    "_data": {
        "_files": ["tasks.json"]
    },
    "_memory": {
        "_files": ["usage_log.json", "lessons_learned.md", "preferences.json"]
    },
    "_templates": {
        "_files": [".gitkeep"]
    }
}

# EXTENDED = Komplexer Skill mit Mikro-Skills (näher am Agent)
PROFILE_EXTENDED = {
    "_files": ["SKILL.md", "README.md", "CHANGELOG.md"],
    "_docs": {
        "_files": ["USAGE.md", "ARCHITECTURE.md"]
    },
    "_config": {
        "_files": ["config.json", "tools.json"]
    },
    "_data": {
        "_files": ["tasks.json", "tasks_done.json"]
    },
    "_memory": {
        "_files": ["usage_log.json", "lessons_learned.md", "preferences.json"],
        "context": {
            "_files": ["current.json"]
        }
    },
    "_micro_skills": {
        "_files": ["registry.json"]
    },
    "_templates": {
        "_files": [".gitkeep"]
    },
    "_backup": {
        "_files": [".gitkeep"]
    }
}

PROFILES = {
    "MICRO": PROFILE_MICRO,
    "LIGHT": PROFILE_LIGHT,
    "STANDARD": PROFILE_STANDARD,
    "EXTENDED": PROFILE_EXTENDED
}

PROFILE_DESCRIPTIONS = {
    "MICRO": "Absolute Teilfähigkeit - nur Datei(en)",
    "LIGHT": "Minimale Struktur (4 Dateien, 2 Ordner)",
    "STANDARD": "Standard-Skill mit Memory (~15 Dateien)",
    "EXTENDED": "Komplexer Skill mit Mikro-Skills (~25 Dateien)"
}

# =============================================================================
# DATEI-TEMPLATES
# =============================================================================

def get_micro_skill_md(name: str) -> str:
    """MICRO: Alles in einer Datei"""
    return f'''---
name: {name}
type: micro-skill
version: 0.1.0
created: {datetime.now().strftime("%Y-%m-%d")}
---

# {name}

> Eine fokussierte Teilfähigkeit

## Wann nutzen?

- [Trigger 1]
- [Trigger 2]

## Vorgehen

### Schritt 1: [Name]
[Beschreibung]

### Schritt 2: [Name]
[Beschreibung]

### Schritt 3: [Name]
[Beschreibung]

## Beispiel

**Input:**
```
[Beispiel-Input]
```

**Output:**
```
[Beispiel-Output]
```

## Notizen & Lessons Learned

- [Erkenntnis 1]
- [Erkenntnis 2]

---
*Micro-Skill generiert mit skill_generator_v3 (BACH_STREAM)*
'''


def get_skill_md(name: str, profile: str) -> str:
    """SKILL.md für LIGHT/STANDARD/EXTENDED"""
    
    profile_badge = {
        "LIGHT": "🟢 Light",
        "STANDARD": "🔵 Standard", 
        "EXTENDED": "🟣 Extended"
    }
    
    memory_section = ""
    if profile in ["STANDARD", "EXTENDED"]:
        memory_section = """
## Memory

Dieser Skill speichert:
- `_memory/usage_log.json` - Nutzungsverlauf
- `_memory/lessons_learned.md` - Was funktioniert hat
- `_memory/preferences.json` - Deine Präferenzen
"""

    micro_skills_section = ""
    if profile == "EXTENDED":
        micro_skills_section = """
## Mikro-Skills

Dieser Skill enthält spezialisierte Unter-Skills:

| Mikro-Skill | Zweck |
|-------------|-------|
| [name] | [beschreibung] |

Registriert in: `_micro_skills/registry.json`
"""

    return f'''---
name: {name}
type: skill
profile: {profile}
version: 0.1.0
created: {datetime.now().strftime("%Y-%m-%d")}
generator: skill_generator_v3
---

# {name}

> {profile_badge.get(profile, "")} Skill - [BESCHREIBUNG]

## Quick Start

1. **Lies diese Datei** - Du bist hier richtig!
2. **Prüfe Tasks** - `_data/tasks.json`
3. **Konfiguration** - `_config/config.json`

## Wann diesen Skill nutzen?

- [Trigger 1: Wann aktiviert sich dieser Skill?]
- [Trigger 2: Welche Schlüsselwörter?]
- [Trigger 3: Welcher Kontext?]

## Vorgehen

### 1. [Erster Schritt]
[Beschreibung]

### 2. [Zweiter Schritt]
[Beschreibung]

### 3. [Dritter Schritt]
[Beschreibung]
{memory_section}{micro_skills_section}
## Beispiel

**Input:**
```
[Beispiel-Anfrage]
```

**Vorgehen:**
1. [Schritt]
2. [Schritt]
3. [Schritt]

**Output:**
[Ergebnis]

---
*Skill generiert mit skill_generator_v3 (BACH_STREAM)*
'''


def get_readme(name: str, profile: str) -> str:
    """README.md"""
    return f'''# {name}

> Generiert mit skill_generator_v3 (Profil: {profile})

## Übersicht

[Was macht dieser Skill?]

## Für Claude

**Einstiegspunkt:** `SKILL.md`

## Profil: {profile}

{PROFILE_DESCRIPTIONS.get(profile, "")}

---
*Erstellt am {datetime.now().strftime("%Y-%m-%d")}*
'''


def get_changelog(name: str) -> str:
    """CHANGELOG.md"""
    return f'''# Changelog - {name}

## [0.1.0] - {datetime.now().strftime("%Y-%m-%d")}

### Hinzugefügt
- Initiale Struktur erstellt
'''


def get_usage_md(name: str) -> str:
    """USAGE.md für _docs/"""
    return f'''# Verwendung: {name}

## Grundlegende Nutzung

1. SKILL.md lesen
2. [Weitere Schritte]

## Häufige Anwendungsfälle

### Fall 1: [Name]
[Beschreibung]

### Fall 2: [Name]
[Beschreibung]

## Tipps

- [Tipp 1]
- [Tipp 2]
'''


def get_architecture_md(name: str) -> str:
    """ARCHITECTURE.md für EXTENDED"""
    return f'''# Architektur: {name}

## Struktur

```
{name}/
├── SKILL.md              # Einstiegspunkt
├── _config/              # Konfiguration
├── _data/                # Arbeitsdaten
├── _memory/              # Skill-Gedächtnis
├── _micro_skills/        # Unter-Skills
├── _templates/           # Vorlagen
└── _backup/              # Sicherungen
```

## Mikro-Skills

Dieser Skill kann spezialisierte Unter-Skills enthalten.

## Datenfluss

```
Input → [Verarbeitung] → Output
          ↓
       _memory/
```
'''


def get_config_json(name: str, profile: str) -> str:
    """config.json"""
    config = {
        "name": name,
        "version": "0.1.0",
        "profile": profile,
        "generator": "skill_generator_v3",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "settings": {}
    }
    
    if profile in ["STANDARD", "EXTENDED"]:
        config["settings"]["memory_enabled"] = True
        config["settings"]["track_usage"] = True
    
    if profile == "EXTENDED":
        config["settings"]["micro_skills_enabled"] = True
    
    return json.dumps(config, indent=4, ensure_ascii=False)


def get_tools_json() -> str:
    """tools.json für EXTENDED"""
    return json.dumps({
        "version": "1.0",
        "tools": []
    }, indent=4, ensure_ascii=False)


def get_tasks_json() -> str:
    """tasks.json"""
    return json.dumps([{
        "_example": True,
        "id": "task_001",
        "title": "Skill konfigurieren",
        "status": "open",
        "created": datetime.now().strftime("%Y-%m-%d")
    }], indent=4, ensure_ascii=False)


def get_usage_log_json() -> str:
    """usage_log.json für Memory"""
    return json.dumps({
        "version": "1.0",
        "entries": [],
        "summary": {
            "total_uses": 0,
            "last_used": None
        }
    }, indent=4, ensure_ascii=False)


def get_lessons_learned_md(name: str) -> str:
    """lessons_learned.md"""
    return f'''# Lessons Learned: {name}

## Was funktioniert gut

- [Erkenntnis]

## Was vermeiden

- [Anti-Pattern]

## Optimierungen

- [Verbesserung]

---
*Wird automatisch ergänzt durch Nutzung*
'''


def get_preferences_json() -> str:
    """preferences.json"""
    return json.dumps({
        "version": "1.0",
        "user_preferences": {},
        "learned_defaults": {}
    }, indent=4, ensure_ascii=False)


def get_micro_skills_registry() -> str:
    """registry.json für _micro_skills/"""
    return json.dumps({
        "version": "1.0",
        "micro_skills": [],
        "note": "Registriere hier eingebettete Mikro-Skills"
    }, indent=4, ensure_ascii=False)


def get_current_context_json() -> str:
    """current.json für _memory/context/"""
    return json.dumps({
        "version": "1.0",
        "current_task": None,
        "active_context": {}
    }, indent=4, ensure_ascii=False)


# =============================================================================
# GENERATOR-FUNKTIONEN
# =============================================================================

def get_file_content(filename: str, name: str, profile: str) -> str:
    """Gibt den Inhalt für eine Datei zurück"""
    
    if filename == "SKILL.md":
        if profile == "MICRO":
            return get_micro_skill_md(name)
        return get_skill_md(name, profile)
    elif filename == "README.md":
        return get_readme(name, profile)
    elif filename == "CHANGELOG.md":
        return get_changelog(name)
    elif filename == "USAGE.md":
        return get_usage_md(name)
    elif filename == "ARCHITECTURE.md":
        return get_architecture_md(name)
    elif filename == "config.json":
        return get_config_json(name, profile)
    elif filename == "tools.json":
        return get_tools_json()
    elif filename == "tasks.json":
        return get_tasks_json()
    elif filename == "tasks_done.json":
        return "[]"
    elif filename == "usage_log.json":
        return get_usage_log_json()
    elif filename == "lessons_learned.md":
        return get_lessons_learned_md(name)
    elif filename == "preferences.json":
        return get_preferences_json()
    elif filename == "registry.json":
        return get_micro_skills_registry()
    elif filename == "current.json":
        return get_current_context_json()
    elif filename == ".gitkeep":
        return "# Placeholder\n"
    else:
        return f"# {filename}\n\n[TODO]\n"


def create_structure(base_path: Path, structure: dict, name: str, profile: str, indent: int = 0):
    """Erstellt rekursiv die Ordnerstruktur"""
    
    prefix = "  " * indent
    
    for key, value in structure.items():
        if key == "_files":
            for filename in value:
                file_path = base_path / filename
                content = get_file_content(filename, name, profile)
                file_path.write_text(content, encoding='utf-8')
                print(f"{prefix}  📄 {filename}")
        elif key == "_type":
            continue  # Marker ignorieren
        else:
            folder_path = base_path / key
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"{prefix}  📁 {key}/")
            
            if isinstance(value, dict):
                create_structure(folder_path, value, name, profile, indent + 1)


def generate_micro(name: str, target: Path):
    """Spezialfall: MICRO generiert nur Datei(en), keinen Ordner"""
    
    # Nur eine SKILL.md Datei erstellen
    file_path = target / f"{name}.md"
    content = get_micro_skill_md(name)
    file_path.write_text(content, encoding='utf-8')
    
    print(f"\n  📄 {name}.md")
    print(f"\n{'='*60}")
    print(f"  ✅ Micro-Skill '{name}' erstellt!")
    print(f"  📄 Datei: {file_path}")
    print(f"{'='*60}")
    print(f"\n  💡 MICRO = Alles in einer Datei, kein Ordner nötig")
    print()
    
    return True


def print_banner():
    """Zeigt Banner"""
    print("=" * 60)
    print("  SKILL GENERATOR v3.0 - BACH_STREAM BUILD TOOL")
    print("=" * 60)
    print()
    print("  Profile:")
    print("    MICRO    = Nur Datei(en), kein Ordner")
    print("    LIGHT    = Minimal (SKILL.md + _config + _data)")
    print("    STANDARD = Mit Memory und Lessons")
    print("    EXTENDED = Mit Mikro-Skills (näher am Agent)")
    print()


def print_usage():
    """Zeigt Verwendung"""
    print("Verwendung:")
    print("  python skill_generator_v3.py <name> [profil] [ziel]")
    print()
    print("  profil: MICRO | LIGHT | STANDARD | EXTENDED")
    print("          (default: STANDARD)")
    print()
    print("  Policy-Aliase (empfohlen):")
    print("    EMBEDDED   = MICRO     (fuer Nutzung im OS, nur .md)")
    print("    STANDALONE = STANDARD  (fuer externe Nutzung, volle Struktur)")
    print()
    print("Beispiele:")
    print('  python skill_generator_v3.py analyse EMBEDDED     # OS-Skill')
    print('  python skill_generator_v3.py mein-skill STANDALONE # Export-faehig')
    print('  python skill_generator_v3.py mein-skill MICRO')
    print('  python skill_generator_v3.py komplex EXTENDED')
    print()


def main():
    """Hauptfunktion"""
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print_banner()
    
    if len(sys.argv) < 2:
        print_usage()
        print("[!] Fehler: Name ist erforderlich")
        return 1
    
    name = sys.argv[1]
    profile_input = sys.argv[2].upper() if len(sys.argv) > 2 else "STANDARD"
    target = Path(sys.argv[3]) if len(sys.argv) > 3 else Path.cwd()
    
    # Policy-konforme Aliase (siehe SKILL_AGENT_OS_DEFINITIONS.md)
    PROFILE_ALIASES = {
        "EMBEDDED": "MICRO",      # --embedded = fuer Nutzung im OS
        "STANDALONE": "STANDARD", # --standalone = fuer externe Nutzung
    }
    profile = PROFILE_ALIASES.get(profile_input, profile_input)
    
    if profile not in PROFILES:
        print(f"[!] Unbekanntes Profil: {profile}")
        print(f"    Verfügbar: {', '.join(PROFILES.keys())}")
        return 1
    
    print(f"[+] Name:    {name}")
    print(f"[+] Profil:  {profile} - {PROFILE_DESCRIPTIONS[profile]}")
    print(f"[+] Ziel:    {target}")
    
    # MICRO: Spezialbehandlung - nur Datei, kein Ordner
    if profile == "MICRO":
        return 0 if generate_micro(name, target) else 1
    
    # Andere Profile: Ordnerstruktur
    output_path = target / name
    
    if output_path.exists():
        print(f"\n[!] Ordner existiert bereits: {output_path}")
        response = input("    Überschreiben? (j/N): ").strip().lower()
        if response != 'j':
            print("    Abgebrochen.")
            return 0
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
    print(f"  ✅ Skill '{name}' erstellt!")
    print(f"  📍 Pfad: {output_path}")
    print(f"  📁 Ordner: {dir_count} | 📄 Dateien: {file_count}")
    print(f"{'='*60}")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
