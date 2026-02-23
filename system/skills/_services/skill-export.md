---
name: skill-export
metadata:
  version: 4.0.0
  last_updated: 2026-01-14
  parent: builder
description: >
  Spezialisiert auf Anthropic/Claude.ai Skill-Upload.
  Für allgemeine Exports siehe builder.md
---

# Skill Export v4.0 - Anthropic Upload

Erstellt upload-kompatible `.zip` Dateien für claude.ai.

> **Hinweis:** Für allgemeine Skill/Agent-Exports siehe `builder.md`  
> Dieser Skill ist spezialisiert auf **Anthropic-Upload-Anforderungen**.

---

## ⚠️ KRITISCHE FORMAT-REGELN (Stand: 2026-01-14)

### 1. Dateiformat
- **Erweiterung:** `.zip` (NICHT .skill!)
- **Struktur:** SKILL.md **direkt im Root** (kein Unterordner!)

```
✅ RICHTIG:
skill-name.zip
└── SKILL.md

❌ FALSCH:
skill-name.zip
└── skill-name/
    └── SKILL.md
```

### 2. Frontmatter-Regeln
- `name:` darf NICHT "claude" enthalten (reserviertes Wort)
- Eigene Felder unter `metadata:` verschachteln
- Max 64 Zeichen für name, max 1024 für description

---

## Upload-Workflow

```bash
# 1. Skill für Anthropic exportieren
python exporter.py skill <n> --from-os . --anthropic

# 2. Validieren
python exporter.py validate <skill.zip>

# 3. Upload unter claude.ai/settings/skills
```

---

## Unterschied zu builder.md

| Aspekt | builder.md | skill-export.md |
|--------|------------|-----------------|
| Zweck | Allgemeine Erstellung & Export | Anthropic-Upload |
| Format | Standalone-Pakete | Minimal (nur SKILL.md) |
| Ziel | Lokale Nutzung, Weitergabe | claude.ai Skill-System |
| Struktur | Vollständig | Nur Root-Datei |

---

## Verwandte Skills

- `builder.md` - Hauptskill für Erstellung & Export
- `handle_files.md` - Datei-Sicherheitsregeln
