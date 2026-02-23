# BACH Project Templates

Vorlagen für strategische Projekt-Dokumente.

## Verfügbare Templates

| Template | Zweck | Beschreibung |
|----------|-------|--------------|
| `SKILL.md` | Projekt-Identität | Hauptdokumentation, Quick Start, Architektur |
| `CHANGELOG.md` | Versionshistorie | Semantic Versioning, Keep a Changelog Format |
| `BUGLOG.md` | Bekannte Probleme | Dokumentierte Bugs, Workarounds, Status |
| `ROADMAP.md` | Strategische Vision | Langfristige Ziele, Phasen, Meilensteine |

## Verwendung

### Für neue BACH-Projekte

```bash
# Template kopieren und anpassen
cp _templates/SKILL.md mein-projekt/SKILL.md
cp _templates/CHANGELOG.md mein-projekt/CHANGELOG.md
cp _templates/ROADMAP.md mein-projekt/ROADMAP.md
```

### Für ATI-Bootstrapping

Die Templates werden von `bach ati bootstrap` verwendet:

```bash
bach ati bootstrap mein-tool --template python-cli
# Erstellt automatisch SKILL.md, CHANGELOG.md, ROADMAP.md
```

## Template-Hierarchie

```
_templates/              # Projekt-weite Templates (hier)
├── SKILL.md
├── CHANGELOG.md
├── BUGLOG.md
└── ROADMAP.md

skills/_templates/       # Skills-spezifische Templates
├── GEMINI.md           # Partner-Kommunikation
├── COPILOT.md
└── delegation_task_template.md
```

## Neue Skills/Tools/Handler erstellen

Fuer das Erstellen neuer BACH-Komponenten gibt es den Self-Extension Workflow:

```bash
bach skills create mein-skill --type service    # Neuer Service-Skill
bach skills create mein-tool --type tool        # Neues Python-Tool
bach skills create mein-handler --type handler  # Neuer CLI-Handler
bach skills create mein-agent --type agent      # Neuer Agent
bach skills create mein-experte --type expert   # Neuer Domain-Experte
```

Detaillierte Anleitung: `skills/workflows/self-extension.md`

## Anpassung

Die Templates enthalten Platzhalter:
- `YYYY-MM-DD` → Aktuelles Datum
- `projekt-name` → Projektname
- `PREFIX_` → Task-Prefix (z.B. CONSOL_, AI_, FS_)

## Teil des Konsolidierungs-Systems

Diese Templates sind Teil der Metakognition:

```
ROADMAP (Vision) → Tasks (Konkret) → Memory (Operativ)
     ↑                                      │
     └──────── Konsolidierung ──────────────┘
```

Siehe: `skills/help/strategic.txt`, `skills/help/consolidation.txt`

---

*BACH v1.1 - Template System*