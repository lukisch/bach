# BACH Standard-Templates

**Version:** 1.0.0
**Erstellt:** 2026-02-04
**Basierend auf:** CONCEPT_Skill_Architecture_v2.md

---

## Übersicht

Diese Templates definieren die Standard-Header und Strukturen für alle BACH-Komponenten gemäß der Skill-Architektur v2.0.

## Verfügbare Templates

| Template | Verwendung |
|----------|------------|
| `TEMPLATE_SKILL.md` | Allgemeine Skills |
| `TEMPLATE_AGENT.md` | Boss-Agenten (orchestrieren Experten) |
| `TEMPLATE_EXPERT.md` | Domänen-Experten (tiefes Fachwissen) |
| `TEMPLATE_SERVICE.md` | System-Services (Handler-nah) |
| `TEMPLATE_WORKFLOW.md` | Workflow-Anleitungen |
| `TEMPLATE_TOOL.py` | Python-Tools |
| `TEMPLATE_HELP.txt` | Help-Dateien |

## Versions-Check-Prinzip

Alle Templates enthalten den **VERSIONS-HINWEIS**:

```
# Prüfe ob eine neuere Version existiert (lokal oder zentral).
# Verwende IMMER die Version mit der höchsten Versionsnummer.
```

## Pflichtfelder im Header

### Für Markdown-Dateien (YAML-Frontmatter)

```yaml
---
name: [name]
version: X.Y.Z
type: skill | agent | expert | service | workflow
author: [author]
created: YYYY-MM-DD
updated: YYYY-MM-DD
anthropic_compatible: true
dependencies:
  tools: []
  services: []
  workflows: []
description: >
  [Beschreibung]
---
```

### Für Python-Tools (Docstring)

```python
"""
Tool: [name]
Version: X.Y.Z
Author: [author]
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Anthropic-Compatible: True

VERSIONS-HINWEIS: ...
"""

__version__ = "X.Y.Z"
__author__ = "[author]"
```

### Für Help-Dateien (Kommentar-Header)

```
# Portabilitaet: UNIVERSAL | SYSTEM | PRIVAT
# Version: X.Y.Z
# Zuletzt validiert: YYYY-MM-DD (Author)
# Naechste Pruefung: YYYY-MM-DD
# Ressourcen: [...]
```

## Ordnerstruktur

### Flat (Standard, < 5 Dateien)

```
skill-name/
├── SKILL.md
├── tool.py
└── workflow.md
```

### Mit Unterordnern (>= 5 Dateien)

```
skill-name/
├── SKILL.md
├── tools/
├── workflows/
└── data/
```

## Verwendung

1. Template kopieren
2. Platzhalter `[...]` ersetzen
3. Datums-Platzhalter `YYYY-MM-DD` ausfüllen
4. Nicht benötigte Abschnitte entfernen

## Siehe auch

- `docs/CONCEPT_Skill_Architecture_v2.md` - Vollständiges Konzept
- `docs/docs/docs/help/skills.txt` - Skill-System Dokumentation
- `docs/docs/docs/help/naming.txt` - Namenskonventionen
