---
name: [workflow-name]
version: 1.0.0
type: workflow
author: [author]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
anthropic_compatible: true

trigger: [Wann diesen Workflow starten?]
duration: [geschätzte Dauer]
complexity: low | medium | high

dependencies:
  tools: []
  skills: []

description: >
  [Kurze Beschreibung des Workflows]
---

# VERSIONS-HINWEIS
# Prüfe ob eine neuere Version dieses Workflows existiert (lokal oder zentral).
# Verwende IMMER die Version mit der höchsten Versionsnummer.
# Versions-Check: bach workflows version [workflow-name]

# [Workflow-Name]

## Wann anwenden?

[Trigger-Situationen beschreiben]

## Voraussetzungen

- [ ] [Voraussetzung 1]
- [ ] [Voraussetzung 2]

## Schritte

### 1. [Schritt-Titel]

[Beschreibung]

```bash
# Befehl falls nötig
```

### 2. [Schritt-Titel]

[Beschreibung]

### 3. [Schritt-Titel]

[Beschreibung]

## Entscheidungspunkte

| Situation | Aktion |
|-----------|--------|
| [Wenn X] | [Dann Y] |
| [Wenn A] | [Dann B] |

## Abschluss

- [ ] [Abschluss-Check 1]
- [ ] [Abschluss-Check 2]

## Siehe auch

- [Verwandter Workflow 1]
- [Verwandtes Tool 1]

## Changelog

### v1.0.0 ([YYYY-MM-DD])
- Initiale Version

---
BACH Skill-Architektur v2.0
