---
name: [skill-name]
version: 1.0.0
type: skill
author: [author]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
anthropic_compatible: true

dependencies:
  tools: []
  services: []
  workflows: []

metadata:
  inputs: ""
  outputs: ""

description: >
  [Kurze Beschreibung der Funktion]
---

# VERSIONS-HINWEIS
# Prüfe ob eine neuere Version dieses Skills existiert (lokal oder zentral).
# Verwende IMMER die Version mit der höchsten Versionsnummer.
# Versions-Check: bach skills version [skill-name]

# [Skill-Name]

## Übersicht

[Was macht dieser Skill?]

## Verwendung

```bash
# Beispiel-Befehle
bach [skill] [command]
```

## Abhängigkeiten

- Tools: [Liste oder "keine"]
- Services: [Liste oder "keine"]
- Workflows: [Liste oder "keine"]

## Dateien

```
[skill-name]/
├── SKILL.md          # Diese Datei
├── [tool].py         # Spezifische Tools (optional)
├── [workflow].md     # Spezifische Workflows (optional)
└── config.json       # Konfiguration (optional)
```

## Changelog

### v1.0.0 ([YYYY-MM-DD])
- Initiale Version

---
BACH Skill-Architektur v2.0
