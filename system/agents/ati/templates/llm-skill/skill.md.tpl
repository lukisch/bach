---
name: ${project_name}
version: 0.1.0
description: ${description}
last_updated: ${date}
---

# ${project_name}

> ${description}

## Quick Start

```bash
# In BACH integriert
bach skill use ${project_name}
```

## Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `...` | ... |

## Konfiguration

Siehe `_config/config.json`:

```json
{
  "name": "${project_name}",
  "version": "0.1.0",
  "enabled": true
}
```

## Architektur

```
${project_name}/
├── SKILL.md ........... Du bist hier
├── README.md .......... Allgemeine Dokumentation
├── CHANGELOG.md ....... Versionshistorie
├── _config/
│   ├── config.json .... Hauptkonfiguration
│   └── tools.json ..... Tool-Definitionen
├── _data/
│   └── tasks.json ..... Task-Storage
├── _memory/
│   ├── context/ ....... Kontext-Dateien
│   ├── lessons_learned.md
│   └── preferences.json
├── _modules/ .......... BACH wiederverwendbare Module
└── _policies/ ......... BACH Policies
```

## Usage

*Beschreibe hier die Nutzung des Skills.*

---
*Generated with ATI Project Bootstrapper*
