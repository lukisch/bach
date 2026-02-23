---
name: [expert-name]
version: 1.0.0
type: expert
author: [author]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
anthropic_compatible: true

domain: [Domäne/Fachgebiet]
parent_agents: []

dependencies:
  tools: []
  services: []
  workflows: []

description: >
  [Kurze Beschreibung des Experten]
---

# VERSIONS-HINWEIS
# Prüfe ob eine neuere Version dieses Experten existiert (lokal oder zentral).
# Verwende IMMER die Version mit der höchsten Versionsnummer.
# Versions-Check: bach experts version [expert-name]

# [Expert-Name]

## Domäne

[Welches Fachgebiet deckt dieser Experte ab? Tiefes Domänenwissen.]

## Zugehörige Agenten

Dieser Experte wird koordiniert von:

- [Agent 1]
- [Agent 2]

## Fähigkeiten

- [Spezialisierte Fähigkeit 1]
- [Spezialisierte Fähigkeit 2]
- [Spezialisierte Fähigkeit 3]

## Tools

| Tool | Beschreibung |
|------|--------------|
| [tool_name.py] | [Was es tut] |

## Workflows

| Workflow | Beschreibung |
|----------|--------------|
| [workflow.md] | [Wann anwenden] |

## Datenstrukturen

[Welche Tabellen/Daten nutzt dieser Experte?]

## Verwendung

```bash
# Experte direkt aufrufen (selten)
bach expert [name] [command]

# Typisch: Via Agent
bach agent [parent-agent] --expert [name]
```

## Dateien

```
[expert-name]/
├── SKILL.md              # Diese Datei (Expert-Definition)
├── [expert]_[tool].py    # Spezifische Tools
├── [expert]-[workflow].md # Spezifische Workflows
├── data/                 # Spezifische Daten/Templates (optional)
└── config.json           # Konfiguration (optional)
```

## Changelog

### v1.0.0 ([YYYY-MM-DD])
- Initiale Version

---
BACH Skill-Architektur v2.0
