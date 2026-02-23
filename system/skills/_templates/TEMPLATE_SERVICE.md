---
name: [service-name]
version: 1.0.0
type: service
author: [author]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
anthropic_compatible: true

handler: hub/[handler].py
scope: system

dependencies:
  tools: []
  external: []

description: >
  [Kurze Beschreibung des Services]
---

# VERSIONS-HINWEIS
# Prüfe ob eine neuere Version dieses Services existiert (lokal oder zentral).
# Verwende IMMER die Version mit der höchsten Versionsnummer.
# Versions-Check: bach services version [service-name]

# [Service-Name]

## Funktion

[Was macht dieser Service? Allgemeine, systemweite Funktion.]

## Handler-Integration

Dieser Service arbeitet eng mit `hub/[handler].py` zusammen.

## CLI-Befehle

```bash
bach [service] [command]
bach [service] status
bach [service] --help
```

## API

[Falls vorhanden: Endpoints, Funktionen]

## Konfiguration

```json
{
  "service_name": {
    "option1": "value1",
    "option2": "value2"
  }
}
```

## Dateien

```
[service-name]/
├── SKILL.md          # Diese Datei (Service-Definition)
├── [service].py      # Service-Logik (optional, wenn nicht in hub/)
└── config.json       # Konfiguration (optional)
```

## Changelog

### v1.0.0 ([YYYY-MM-DD])
- Initiale Version

---
BACH Skill-Architektur v2.0
