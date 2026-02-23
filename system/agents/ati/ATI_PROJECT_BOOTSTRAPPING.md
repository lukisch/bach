---
name: ati-project-bootstrapping
metadata:
  version: 1.0.0
  last_updated: 2026-01-21
  type: concept
  status: approved
  parent: ati-agent
description: >
  ATI Projekt-Bootstrapping-System: Automatisches Onboarding neuer
  Softwareprojekte mit BACH-Policies, Git-Strukturvorlagen und
  wiederverwendbaren Modulen (Selbstheilung, Distribution, etc.)
---

# ATI - Projekt-Bootstrapping-Konzept

> Neue Softwareprojekte automatisch mit BACH-Policies und -Strukturen ausstatten

## 1. Uebersicht

### 1.1 Problem

Neue Softwareprojekte starten oft ohne:
- Konsistente Ordnerstruktur
- Pfad-Management und Selbstheilung
- Distribution-Vorbereitung (Tier-System)
- Standard-Policies (Naming, Encoding, etc.)
- Wiederverwendbare Module

### 1.2 Loesung

ATI bietet ein **Project Bootstrapping System**, das:
- BACH-konforme Git-Strukturen generiert
- Wiederverwendbare Module injiziert (Pfadheilung, etc.)
- Bestehende Projekte auf Strukturvorgaben umbauen kann
- Policies automatisch anwendet

### 1.3 Bestehende Tools (Integration)

| Tool | Pfad | Funktion | Integration |
|------|------|----------|-------------|
| `structure_generator.py` | `skills/tools/` | Skill/Agent-Strukturen | Als Template-Engine |
| `skill_generator.py` | `skills/tools/generators/` | Skill-Profile | Template-Bibliothek |
| `distribution_system.py` | `skills/tools/` | Tier-System, Siegel | Dist-Policies |
| `unified_path_healer.py` | `skills/tools/_FUTURES/maintain/` | Pfad-Korrektur | Selbstheilungsmodul |
| `exporter.py` | `skills/tools/generators/` | Export-Funktion | Release-Pipeline |
| `builder.md` | `skills/_services/` | Build-Skill | Orchestrierung |

---

## 2. Architektur

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ATI PROJECT BOOTSTRAPPING SYSTEM                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      BOOTSTRAP CORE                              │   │
│  │                                                                   │   │
│  │   project_bootstrapper.py                                         │   │
│  │   ├── TemplateEngine (nutzt structure_generator.py)               │   │
│  │   ├── PolicyApplier (wendet BACH-Policies an)                     │   │
│  │   ├── ModuleInjector (injiziert wiederverwendbare Module)         │   │
│  │   └── StructureMigrator (baut bestehende Projekte um)             │   │
│  │                                                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                │                                        │
│                                ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    WIEDERVERWENDBARE MODULE                      │   │
│  │                                                                   │   │
│  │   modules/                                                        │   │
│  │   ├── path_healer/         # Pfad-Selbstheilung (von RecludOS)    │   │
│  │   ├── distribution/        # Tier-System, Siegel                  │   │
│  │   ├── encoding/            # UTF-8, BOM-Handling                  │   │
│  │   ├── backup/              # Snapshot, Restore                    │   │
│  │   └── validation/          # Schema-Validierung                   │   │
│  │                                                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                │                                        │
│                                ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    GIT-STRUKTUR-TEMPLATES                        │   │
│  │                                                                   │   │
│  │   templates/                                                      │   │
│  │   ├── python-cli/          # Python CLI-Projekt                   │   │
│  │   ├── python-api/          # Python API-Projekt                   │   │
│  │   ├── llm-skill/           # LLM Skill-Projekt                    │   │
│  │   ├── llm-agent/           # LLM Agent-Projekt                    │   │
│  │   ├── llm-os/              # LLM OS-Projekt                       │   │
│  │   └── generic/             # Universelles Projekt                 │   │
│  │                                                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Git-Struktur-Templates

### 3.1 Template: python-cli

```
{project_name}/
├── .git/
├── .gitignore
├── README.md
├── CHANGELOG.md
├── LICENSE
├── setup.py / pyproject.toml
│
├── src/{project_name}/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py              # CLI Entry-Point
│   └── core/
│       └── __init__.py
│
├── tests/
│   ├── __init__.py
│   └── test_core.py
│
├── ../docs/
│   └── README.md
│
├── _policies/              # BACH-Policies [INJIZIERT]
│   ├── naming_convention.md
│   ├── encoding_policy.md
│   └── path_rules.json
│
└── _modules/               # Wiederverwendbare Module [INJIZIERT]
    ├── path_healer.py
    └── distribution.py
```

### 3.2 Template: llm-skill (BACH-konform)

```
{skill_name}/
├── SKILL.md               # Einstiegspunkt (Pflicht)
├── README.md
├── CHANGELOG.md
│
├── _config/
│   ├── config.json
│   └── tools.json
│
├── _data/
│   └── tasks.json
│
├── _memory/
│   ├── lessons_learned.md
│   ├── preferences.json
│   └── context/
│
├── _modules/              # Wiederverwendbare Module [INJIZIERT]
│   ├── path_healer.py
│   └── validation.py
│
└── _policies/             # BACH-Policies [INJIZIERT]
    └── skill_policy.md
```

### 3.3 Template: llm-agent (BACH-konform)

```
{agent_name}/
├── SKILL.md               # Einstiegspunkt (Pflicht)
├── README.md
├── CHANGELOG.md
│
├── _config/
│   ├── config.json
│   ├── skills.json
│   └── workflow_config.json
│
├── _data/
│   ├── tasks.json
│   ├── projekte/
│   └── outputs/
│
├── _memory/
│   ├── session/
│   ├── global/
│   └── projekte/
│
├── _workflows/
│   └── _index.md
│
├── _skills/
│   └── _registry.json
│
├── _modules/              # Wiederverwendbare Module [INJIZIERT]
│   ├── path_healer.py
│   ├── distribution.py
│   └── backup.py
│
└── _policies/             # BACH-Policies [INJIZIERT]
    ├── agent_policy.md
    └── tier_classification.json
```

---

## 4. Wiederverwendbare Module

### 4.1 path_healer (von RecludOS/VFDistiller)

**Quelle:** `skills/tools/_FUTURES/maintain/unified_path_healer.py`

**Funktion:**
- Automatische Pfad-Korrektur bei Umbenennung/Verschiebung
- String-Ersetzung in JSON, MD, PY, TXT
- Healing-Report generieren

**Integration:**
```python
# In jedem neuen Projekt verfuegbar als:
from _modules.path_healer import PathHealer

healer = PathHealer(project_root)
healer.heal_all(dry_run=True)  # Vorschau
healer.heal_all()               # Ausfuehren
```

**Konfiguration (path_rules.json):**
```json
{
  "version": "1.0",
  "corrections": [
    {"old": "old/path/", "new": "new/path/"},
    {"old": "deprecated\name\", "new": "current\name\"}
  ],
  "healable_extensions": [".json", ".md", ".py", ".txt"],
  "ignore_dirs": ["__pycache__", ".git", "node_modules"]
}
```

### 4.2 distribution (von RecludOS)

**Quelle:** `skills/tools/distribution_system.py`

**Funktion:**
- Tier-Klassifizierung (0=Kernel, 1=Core, 2=Extension, 3=UserData)
- Siegel-System fuer Integritaet
- Release-Erstellung

**Integration:**
```python
from _modules.distribution import DistributionSystem

dist = DistributionSystem(project_root)
dist.classify_all_files()      # Tier zuweisen
dist.verify_seal()             # Integritaet pruefen
dist.create_release("v1.0.0")  # Release erstellen
```

### 4.3 encoding (UTF-8 Standard)

**Funktion:**
- UTF-8 mit BOM-Toleranz
- Encoding-Korrektur bei Read/Write
- Windows Console Support

**Integration:**
```python
from _modules.encoding import safe_read, safe_write

content = safe_read(filepath)   # Auto BOM-Handling
safe_write(filepath, content)   # UTF-8 ohne BOM
```

### 4.4 backup (Snapshot-System)

**Quelle:** `skills/_services/builder.md` (Konzept)

**Funktion:**
- Snapshot vor kritischen Operationen
- Restore auf vorherigen Stand
- Backup-Rotation

### 4.5 validation (Schema-Pruefung)

**Funktion:**
- JSON-Schema-Validierung
- Frontmatter-Check fuer MD-Dateien
- Struktur-Validierung

---

## 5. BACH-Policies

### 5.1 Naming Convention

**Datei:** `_policies/naming_convention.md`

```markdown
# Naming Convention

## Dateien
- kebab-case fuer alle Dateien: `my-file.md`
- Keine Leerzeichen, keine Umlaute
- Lowercase (Ausnahme: SKILL.md, README.md, etc.)

## Ordner
- Underscore-Prefix fuer System: `_config/`, `_data/`
- Lowercase ohne Prefix fuer User-Ordner

## Python
- snake_case fuer Module und Funktionen
- PascalCase fuer Klassen
```

### 5.2 Encoding Policy

**Datei:** `_policies/encoding_policy.md`

```markdown
# Encoding Policy

## Standard
- UTF-8 ohne BOM (Pflicht)
- LF Line Endings (empfohlen)

## Ausnahmen
- Windows Batch (.bat): CP1252 erlaubt
- Legacy-Dateien: UTF-8 mit BOM toleriert

## Validation
- Bei --startup: Encoding-Check
- Bei --shutdown: Auto-Fix Option
```

### 5.3 Path Rules

**Datei:** `_policies/path_rules.json`

```json
{
  "version": "1.0",
  "rules": {
    "max_depth": 5,
    "max_name_length": 50,
    "forbidden_chars": ["<", ">", ":", "\"", "|", "?", "*"],
    "reserved_names": ["CON", "PRN", "AUX", "NUL"]
  },
  "aliases": {
    "~": "{USER_HOME}",
    "@": "{PROJECT_ROOT}"
  }
}
```

### 5.4 Tier Classification

**Datei:** `_policies/tier_classification.json`

```json
{
  "version": "1.0",
  "tiers": {
    "0": {"name": "Kernel", "mutable": false, "backup": "distribution"},
    "1": {"name": "Core", "mutable": false, "backup": "distribution"},
    "2": {"name": "Extension", "mutable": true, "backup": "snapshot"},
    "3": {"name": "UserData", "mutable": true, "backup": "rotation"}
  },
  "path_patterns": {
    "SKILL.md": 0,
    "_config/*": 1,
    "_data/*": 3,
    "_memory/*": 3
  }
}
```

---

## 6. CLI-Befehle

### 6.1 Neues Projekt erstellen

```bash
# Python CLI-Projekt
bach ati bootstrap my-tool --template python-cli

# LLM Skill (BACH-konform)
bach ati bootstrap my-skill --template llm-skill

# LLM Agent (BACH-konform)
bach ati bootstrap my-agent --template llm-agent

# Mit Optionen
bach ati bootstrap my-project --template python-cli \
    --modules path_healer,distribution \
    --policies naming,encoding
```

### 6.2 Bestehendes Projekt migrieren

```bash
# Analyse: Was fehlt?
bach ati migrate my-project --analyze

# Dry-Run: Was wuerde passieren?
bach ati migrate my-project --dry-run

# Migration ausfuehren
bach ati migrate my-project --execute

# Nur Module hinzufuegen
bach ati migrate my-project --add-modules path_healer
```

### 6.3 Module verwalten

```bash
# Verfuegbare Module anzeigen
bach ati modules list

# Modul zu Projekt hinzufuegen
bach ati modules add path_healer --project my-project

# Modul aktualisieren
bach ati modules update path_healer --project my-project
```

### 6.4 Policies anwenden

```bash
# Policies pruefen
bach ati policies check my-project

# Policies anwenden
bach ati policies apply my-project --policy naming
bach ati policies apply my-project --all
```

---

## 7. Workflow: Neues Projekt

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BOOTSTRAP WORKFLOW                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. TEMPLATE AUSWAHL                                                    │
│     bach ati bootstrap {name} --template {type}                         │
│     │                                                                   │
│     ▼                                                                   │
│  2. STRUKTUR GENERIEREN                                                 │
│     ├── Git-Repository initialisieren                                   │
│     ├── Ordnerstruktur aus Template erstellen                           │
│     └── Basis-Dateien generieren                                        │
│     │                                                                   │
│     ▼                                                                   │
│  3. MODULE INJIZIEREN                                                   │
│     ├── path_healer.py → _modules/                                      │
│     ├── distribution.py → _modules/                                     │
│     └── weitere nach --modules Parameter                                │
│     │                                                                   │
│     ▼                                                                   │
│  4. POLICIES ANWENDEN                                                   │
│     ├── naming_convention.md → _policies/                               │
│     ├── encoding_policy.md → _policies/                                 │
│     └── path_rules.json → _policies/                                    │
│     │                                                                   │
│     ▼                                                                   │
│  5. INITIALISIERUNG                                                     │
│     ├── Tier-Klassifizierung durchfuehren                               │
│     ├── Siegel erstellen (wenn distribution Modul)                      │
│     └── README mit Quick-Start aktualisieren                            │
│     │                                                                   │
│     ▼                                                                   │
│  6. ONBOARDING-TASKS ERSTELLEN                                          │
│     ├── "SKILL.md anpassen"                                             │
│     ├── "config.json konfigurieren"                                     │
│     └── "Erste Funktion implementieren"                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Workflow: Bestehendes Projekt migrieren

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MIGRATION WORKFLOW                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. ANALYSE (--analyze)                                                 │
│     ├── Aktuelle Struktur scannen                                       │
│     ├── Vergleich mit Ziel-Template                                     │
│     └── Report: Was fehlt, was umbenannt werden muss                    │
│     │                                                                   │
│     ▼                                                                   │
│  2. BACKUP ERSTELLEN                                                    │
│     └── Snapshot vor Migration (Pflicht)                                │
│     │                                                                   │
│     ▼                                                                   │
│  3. STRUKTUR ANPASSEN                                                   │
│     ├── Fehlende Ordner erstellen                                       │
│     ├── Dateien nach Konvention umbenennen                              │
│     └── Pfade in Dateien anpassen (path_healer)                         │
│     │                                                                   │
│     ▼                                                                   │
│  4. MODULE HINZUFUEGEN                                                  │
│     ├── _modules/ Ordner erstellen                                      │
│     └── Gewaehlte Module kopieren                                       │
│     │                                                                   │
│     ▼                                                                   │
│  5. POLICIES EINFUEGEN                                                  │
│     ├── _policies/ Ordner erstellen                                     │
│     └── Policy-Dateien kopieren                                         │
│     │                                                                   │
│     ▼                                                                   │
│  6. VALIDIERUNG                                                         │
│     ├── Struktur-Check                                                  │
│     ├── Encoding-Check                                                  │
│     └── Policy-Compliance-Check                                         │
│     │                                                                   │
│     ▼                                                                   │
│  7. REPORT                                                              │
│     └── Migration-Report mit allen Aenderungen                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Implementierungs-Roadmap

### Phase 1: Core (4h)
```
[ ] project_bootstrapper.py erstellen
[ ] TemplateEngine implementieren (nutzt structure_generator.py)
[ ] CLI-Handler hub/handlers/ati_bootstrap.py
[ ] Basis-Templates: python-cli, llm-skill
```

### Phase 2: Module (4h)
```
[ ] _modules/ Ordner in ATI erstellen
[ ] path_healer.py von _FUTURES portieren
[ ] distribution.py Minimal-Version extrahieren
[ ] encoding.py erstellen
[ ] ModuleInjector implementieren
```

### Phase 3: Policies (2h)
```
[ ] _policies/ Templates erstellen
[ ] PolicyApplier implementieren
[ ] Validation-Checks
```

### Phase 4: Migration (4h)
```
[ ] StructureMigrator implementieren
[ ] --analyze Funktion
[ ] --dry-run Funktion
[ ] --execute Funktion mit Rollback
```

### Phase 5: Integration (2h)
```
[ ] Mit bestehendem Onboarding-System verbinden
[ ] Dokumentation in ATI.md aktualisieren
[ ] Tests schreiben
```

---

## 10. Konfiguration

### ATI Bootstrap Config

**Pfad:** `data/ati/bootstrap_config.json`

```json
{
  "version": "1.0",
  "default_template": "python-cli",
  "default_modules": ["path_healer", "encoding"],
  "default_policies": ["naming", "encoding"],
  "templates_path": "agents/ati/templates/",
  "modules_path": "agents/ati/modules/",
  "policies_path": "agents/ati/policies/",
  "onboarding": {
    "create_tasks": true,
    "tasks": [
      "SKILL.md anpassen",
      "config.json konfigurieren",
      "Erste Funktion implementieren",
      "README mit Projektbeschreibung ergaenzen"
    ]
  }
}
```

---

## 11. Integration mit bestehendem ATI

### Erweiterung von ATI.md

```markdown
## ATI Delta-Features (was BACH fehlt)

...bestehendes...

┌─────────────────────────────────────────────────────────────────┐
│ 9. PROJECT BOOTSTRAPPING (NEU)                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Was: Neue Projekte mit BACH-Policies und Modulen ausstatten      │
│                                                                  │
│ Komponenten:                                                     │
│   project_bootstrapper.py    Projekt-Erstellung                  │
│   templates/                 Git-Struktur-Vorlagen               │
│   modules/                   Wiederverwendbare Module            │
│   policies/                  BACH-Konventionen                   │
│                                                                  │
│ CLI:                                                             │
│   bach ati bootstrap NAME    Neues Projekt erstellen             │
│   bach ati migrate PATH      Bestehendes migrieren               │
│   bach ati modules list      Verfuegbare Module                  │
│   bach ati policies check    Policies pruefen                    │
│                                                                  │
│ Konzept: agents/ati/ATI_PROJECT_BOOTSTRAPPING.md         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. Beispiel-Nutzung

### Neues Python-Tool erstellen

```bash
# Projekt erstellen
$ bach ati bootstrap my-awesome-tool --template python-cli

[+] Template: python-cli
[+] Pfad: C:\Projekte\my-awesome-tool

Erstelle Struktur...
  📁 src/my_awesome_tool/
  📁 tests/
  📁 ../docs/
  📁 _modules/
  📁 _policies/
  📄 README.md
  📄 setup.py
  ...

Injiziere Module...
  ✓ path_healer.py
  ✓ encoding.py

Wende Policies an...
  ✓ naming_convention.md
  ✓ encoding_policy.md

Erstelle Onboarding-Tasks...
  #1 SKILL.md anpassen
  #2 config.json konfigurieren
  #3 Erste Funktion implementieren

✅ Projekt 'my-awesome-tool' erstellt!
   Naechster Schritt: cd my-awesome-tool && cat SKILL.md
```

### Bestehendes Projekt migrieren

```bash
# Analyse
$ bach ati migrate C:\alte-projekte\legacy-tool --analyze

[ANALYSE] legacy-tool

Struktur-Vergleich mit llm-skill Template:
  ❌ SKILL.md fehlt
  ❌ _config/ fehlt
  ❌ _modules/ fehlt
  ⚠️  src/ sollte umbenannt werden
  ✓ README.md vorhanden

Empfehlung: 4 Aenderungen notwendig
Ausfuehren mit: bach ati migrate ... --execute
```

---

## Verwandte Dokumente

- `ATI.md` - Hauptdokumentation ATI-Agent
- `skills/_services/builder.md` - Build-Skill v3.0
- `skills/tools/structure_generator.py` - Struktur-Generator
- `skills/tools/distribution_system.py` - Distribution-System
- `skills/tools/_FUTURES/maintain/unified_path_healer.py` - Pfad-Heilung

---

*Konzept erstellt: 2026-01-21*
*Fuer: ATI Agent - BACH v1.1*