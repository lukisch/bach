# System-Anschlussanalyse: Integration & Konsistenz

**Version:** 1.0  
**Stand:** 2026-01-22  
**Kategorie:** Wartung, Qualitätssicherung

---

## Übersicht

Dieser Workflow prüft BACH auf unverbundene Systembereiche, Inkonsistenzen und Integrationslücken. Ziel ist es, parallele/doppelte Strukturen zu erkennen und zu konsolidieren.

```
┌─────────────────────────────────────────────────────────┐
│         ANSCHLUSSANALYSE (5 Schritte)                   │
├─────────────────────────────────────────────────────────┤
│  1. Dokumentations-Scan (Help vs. Code vs. DB)          │
│  2. Handler-Vollständigkeit prüfen                      │
│  3. Cross-Referenzen validieren                         │
│  4. Doppelstrukturen identifizieren                     │
│  5. Integrations-Tasks erstellen                        │
└─────────────────────────────────────────────────────────┘
```

**Dauer:** 15-30 Minuten  
**Empfohlene Häufigkeit:** Monatlich oder nach größeren Änderungen

---

## Schritt 1: Dokumentations-Scan

**Zweck:** Prüfen ob Help-Texte, Code und DB konsistent sind

### Prüfpunkte

| Quelle | Prüfung | Befehl |
|--------|---------|--------|
| skills/docs/docs/docs/help/*.txt | Alle Handler dokumentiert? | `dir docs\docs\docs\help\*.txt` |
| hub/handlers/*.py | Alle Handler haben Help? | `dir hub\handlers\*.py` |
| bach.py | Alle Subcommands in KNOWN_COMMANDS? | Zeile ~855 |
| practices.txt | REGELWERK-INDEX vollständig? | `--help practices` |

### Checkliste

```
□ Jeder Handler hat eine skills/docs/docs/docs/help/*.txt Datei
□ REGELWERK-INDEX verweist auf alle relevanten Themen
□ Keine verwaisten Help-Dateien ohne Handler
```

---

## Schritt 2: Handler-Vollständigkeit

**Zweck:** CLI-Routing auf Lücken prüfen

### Bekannte Patterns

```python
# In bach.py gibt es zwei Routing-Pfade:

# 1. Mit -- (Handler-basiert)
if arg.startswith('--'):
    handler = get_handler(profile_name)

# 2. Ohne -- (Subcommand)
elif command == "partner":
    handler = get_handler("partner")
```

### Prüfung

```bash
# Handler in get_handler() registriert?
grep -n "lambda.*_import_handler" bach.py

# Subcommand elif-Block vorhanden?
grep -n "elif command ==" bach.py
```

### Ziel

Alle Handler sollten BEIDE Wege unterstützen (mit und ohne --).

---

## Schritt 3: Cross-Referenzen validieren

**Zweck:** Verweise zwischen Systemen prüfen

### Typische Inkonsistenzen

| Problem | Beispiel | Lösung |
|---------|----------|--------|
| Alter Pfad | `recludOS/` statt `BACH_v2_vanilla/` | `--maintain heal` |
| Fehlende Referenz | skills/docs/docs/docs/help/x.txt erwähnt nicht existierende Datei | Korrigieren |
| Doppelte Doku | Info in skills/docs/docs/docs/help/*.txt UND in DB | Konsolidieren |

### Befehle

```bash
# Pfad-Konsistenz
bach --maintain heal --dry-run

# Registry-Konsistenz
bach --maintain registry check

# Skill-Konsistenz
bach --maintain skills check
```

---

## Schritt 4: Doppelstrukturen identifizieren

**Zweck:** Parallele Systeme erkennen und zusammenführen

### Bekannte Doppelstrukturen

| Bereich | Struktur A | Struktur B | Empfehlung |
|---------|------------|------------|------------|
| Lessons | skills/docs/docs/docs/help/lessons.txt (statisch) | memory_lessons DB (dynamisch) | Help verweist auf DB |
| Facts | memory_facts DB | config.json | DB für dynamisch, JSON für statisch |
| Befehle | `mem` Kurzform | `--memory` Handler | Beide behalten, dokumentieren |

### Prüffragen

```
□ Gibt es zwei Orte für die gleiche Information?
□ Welcher ist die "Single Source of Truth"?
□ Kann einer auf den anderen verweisen statt duplizieren?
```

---

## Schritt 5: Integrations-Tasks erstellen

**Zweck:** Gefundene Lücken als Tasks erfassen

### Task-Kategorien

| Kategorie | Präfix | Beispiel |
|-----------|--------|----------|
| Dokumentation | DOC_ | DOC_007: Help-Datei fehlt |
| Integration | INTEG_ | INTEG_001: Handler nicht verknüpft |
| Migration | MIG_ | MIG_003: Alte Pfade korrigieren |

### Befehl

```bash
bach task add "[INTEG] Handler X braucht elif-Block in bach.py" --priority P3
```

---

## Automatisierung

### Option A: Als Recurring Task

```bash
bach --recurring add integration_check \
    --interval 30d \
    --action "bach --maintain registry && bach --maintain skills" \
    --assignee BACH
```

### Option B: In Startup integrieren (Quick-Check)

Bereits implementiert in `--startup`:
- Directory Scan ✅
- Registry Watcher ✅
- Skill Health ✅

### Option C: Dedizierter Maintain-Befehl

```bash
# NEU: Vollständige Anschlussanalyse
bach --maintain integration [--dry-run]
```

---

## Ergebnisse dieser Session (2026-01-22)

### Gefundene Inkonsistenzen

1. **CLI-Syntax:** `--partner` funktionierte, `partner` nicht → **GELÖST** (elif-Block hinzugefügt)
2. **Did-you-mean:** Fehlte bei unbekannten Befehlen → **GELÖST** (`_suggest_command()`)
3. **CLI-Dokumentation:** skills/docs/docs/docs/help/cli.txt fehlte → **GELÖST** (erstellt)
4. **REGELWERK-INDEX:** CLI-Syntax fehlte → **GELÖST** (ergänzt)

### Erstellte Artefakte

- `skills/docs/docs/docs/help/cli.txt` - CLI-Konventionen
- `_suggest_command()` in bach.py - Did-you-mean Funktion
- Lesson #34, #35 - CLI-Dokumentation
- Dieser Workflow

---

## Schnell-Checkliste

```
□ skills/docs/docs/docs/help/*.txt ↔ hub/handlers/*.py Abgleich
□ bach.py KNOWN_COMMANDS aktuell
□ practices.txt REGELWERK-INDEX vollständig
□ --maintain heal --dry-run ohne Fehler
□ --maintain registry check OK
□ Keine Doppelstrukturen oder dokumentiert
□ Integrations-Tasks erstellt
```

---

## Siehe auch

- `skills/workflows/system-mapping.md` - Feature-Erfassung
- `skills/workflows/system-synopse.md` - System-Übersicht
- `skills/docs/docs/docs/help/maintain.txt` - Wartungs-Tools
- `skills/docs/docs/docs/help/practices.txt` - Best Practices Index

---

*Erstellt: 2026-01-22 | Anlass: Partner-System Integration*