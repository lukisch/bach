---
name: [agent-name]
version: 1.0.0
type: agent
author: [author]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
anthropic_compatible: true

orchestrates:
  experts: []
  services: []

dependencies:
  tools: []
  workflows: []

description: >
  [Kurze Beschreibung des Agenten]
---

# VERSIONS-HINWEIS
# Prüfe ob eine neuere Version dieses Agenten existiert (lokal oder zentral).
# Verwende IMMER die Version mit der höchsten Versionsnummer.
# Versions-Check: bach agents version [agent-name]

# [Agent-Name]

## Rolle

[Was orchestriert dieser Agent? Welche Bereiche koordiniert er?]

## Experten

Dieser Agent koordiniert folgende Experten:

| Experte | Bereich | Pfad |
|---------|---------|------|
| [name] | [Bereich] | agents/_experts/[name]/ |

## Fähigkeiten

- [Fähigkeit 1]
- [Fähigkeit 2]
- [Fähigkeit 3]

## Verwendung

```bash
# Agent aktivieren
bach agent [name] [command]

# Status prüfen
bach agent [name] status
```

## Workflow

1. [Schritt 1]
2. [Schritt 2]
3. Bei Spezialthema: Delegation an Experten
4. [Schritt 4]

## Dateien

```
[agent-name]/
├── SKILL.md          # Diese Datei (Agent-Definition)
├── [tool].py         # Spezifische Tools (optional)
├── [workflow].md     # Spezifische Workflows (optional)
└── config.json       # Konfiguration (optional)
```

## User-Daten

Pfad: `user/[agent-name]/`

## Changelog

### v1.0.0 ([YYYY-MM-DD])
- Initiale Version

---
BACH Skill-Architektur v2.0
