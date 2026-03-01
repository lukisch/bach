---
name: cross-system-sync
version: 1.0.0
type: workflow
author: Lukas Geiger + Claude Opus 4.6
created: 2026-02-21
updated: 2026-02-21
anthropic_compatible: true

trigger: Neues System einrichten, Wissen zwischen Systemen synchronisieren
duration: 15-30 Minuten (Ersteinrichtung), 2 Minuten (laufender Sync)
complexity: low

dependencies:
  tools: []
  skills: []
  external: [OneDrive]

description: >
  Synchronisiert Claude Code Wissen (MEMORY.md, CLAUDE.md, Lessons Learned)
  zwischen mehreren Systemen ueber einen gemeinsamen OneDrive-Ordner.
  Loest das Problem isolierter Wissenssilos bei Multi-System-Setups.
---

# Cross-System Sync Workflow

## Wann anwenden?

- Neues System wird eingerichtet und soll bestehendes Wissen erhalten
- Zwei oder mehr Systeme sollen Lessons Learned austauschen
- Nach laengerer Arbeit auf einem System soll das andere aktualisiert werden

## Problemstellung

Claude Code speichert Memory projekt- und system-basiert. Wissen von
System A ist auf System B nicht verfuegbar, selbst wenn beide via
OneDrive verbunden sind. Dieser Workflow loest das durch einen
bidirektionalen Sync-Mechanismus.

## Architektur

```
SYSTEM A (z.B. Laptop)              SYSTEM B (z.B. Workstation)
  ~/.claude/.../MEMORY.md              ~/.claude/.../MEMORY.md
  ~/CLAUDE.md                          ~/CLAUDE.md
       |                                    |
       v                                    v
  OneDrive/claude-sync/              OneDrive/claude-sync/
    system-a/                          system-b/
      MEMORY_EXPORT.md                   MEMORY_EXPORT.md
      CLAUDE_EXPORT.md                   CLAUDE_EXPORT.md
      LESSONS_NEW.md                     LESSONS_NEW.md
      last_sync.txt                      last_sync.txt
    SYNC_PROTOCOL.md (gemeinsam)
```

## Voraussetzungen

- [ ] OneDrive auf beiden Systemen aktiv und synchron
- [ ] Claude Code auf beiden Systemen installiert
- [ ] Home-Memory als Hub eingerichtet (siehe `claude-bach-vernetzung.md`)

## Schritte: Ersteinrichtung

### 1. Sync-Ordner anlegen

```bash
mkdir -p "/c/Users/User/OneDrive/claude-sync/system-a"
mkdir -p "/c/Users/User/OneDrive/claude-sync/system-b"
```

Systembezeichnung frei waehlbar (z.B. `laptop`, `workstation`, `desktop`).

### 2. SYNC_PROTOCOL.md erstellen

Erstelle `OneDrive/claude-sync/SYNC_PROTOCOL.md` mit:
- Ordnerstruktur-Erklaerung
- Workflow-Beschreibung (Export + Import)
- Regeln (nur eigenen Ordner beschreiben, Merge statt Ueberschreiben)
- Systemliste mit Identifikatoren

### 3. Initialen Export erstellen

```bash
# Eigenes Wissen exportieren
cp ~/.claude/projects/C--Users-User/memory/MEMORY.md \
   "/c/Users/User/OneDrive/claude-sync/<system>/MEMORY_EXPORT.md"

cp ~/CLAUDE.md \
   "/c/Users/User/OneDrive/claude-sync/<system>/CLAUDE_EXPORT.md"

date "+%Y-%m-%d %H:%M:%S" > \
   "/c/Users/User/OneDrive/claude-sync/<system>/last_sync.txt"
```

### 4. LESSONS_NEW.md anlegen

Erstelle `OneDrive/claude-sync/<system>/LESSONS_NEW.md`:

```markdown
# Neue Lessons -- <SYSTEM>
# Kumulatives Log neuer Erkenntnisse

## YYYY-MM-DD -- <Thema>
- Erkenntnis 1
- Erkenntnis 2
```

### 5. CLAUDE.md und MEMORY.md ergaenzen

In beide Dateien einfuegen:

```markdown
## Cross-System Sync
- **Sync-Ordner:** `C:\Users\User\OneDrive\claude-sync\`
- **Eigener Slot:** `<system>/`
- **Protokoll:** Siehe `OneDrive/claude-sync/SYNC_PROTOCOL.md`
- **Bei Session-Start:** Eigene Exports aktualisieren, Exports des anderen lesen
```

### 6. Uebergabedokument fuer neues System

Erstelle eine `CLAUDE_UEBERGABE_<SYSTEM>.md` auf dem Desktop mit:
- Uebergabeprompt an die neue Instanz
- Kopie der CLAUDE.md
- Wichtigste MEMORY.md-Inhalte
- Anleitung fuer Silo-Problem-Patch
- Sync-Workflow-Anleitung

## Schritte: Laufender Sync (bei Session-Start)

### 1. Eigene Exports aktualisieren

```
Lese eigene MEMORY.md und CLAUDE.md
Schreibe nach: OneDrive/claude-sync/<eigenes-system>/MEMORY_EXPORT.md
Schreibe nach: OneDrive/claude-sync/<eigenes-system>/CLAUDE_EXPORT.md
Aktualisiere: last_sync.txt
```

### 2. Exports des anderen Systems lesen

```
Lese: OneDrive/claude-sync/<anderes-system>/MEMORY_EXPORT.md
Lese: OneDrive/claude-sync/<anderes-system>/LESSONS_NEW.md
Vergleiche mit eigenem Wissen
```

### 3. Neue Infos uebernehmen

```
Relevante neue Erkenntnisse in eigene MEMORY.md eintragen
Keine Duplikate erzeugen
Kompakt halten (200-Zeilen-Limit)
```

## Regeln

| Regel | Beschreibung |
|-------|-------------|
| Nur eigenen Ordner beschreiben | Nie in den Ordner des anderen Systems schreiben |
| Merge statt Ueberschreiben | Neue Infos ergaenzen, bestehende nicht loeschen |
| Keine Duplikate | Vor dem Eintragen pruefen ob die Info schon existiert |
| Kompakt bleiben | MEMORY.md hat 200-Zeilen-Limit |
| Datierte Eintraege | Jeder LESSONS_NEW.md Eintrag bekommt ein Datum |

## Entscheidungspunkte

| Situation | Aktion |
|-----------|--------|
| Anderes System hat neue Lessons | In eigene MEMORY.md uebernehmen |
| Widerspruch zwischen Systemen | Neueres Datum gewinnt, im Zweifel User fragen |
| MEMORY.md wird zu lang | Detail-Dateien auslagern, in MEMORY.md referenzieren |
| Neues drittes System | Neuen Ordner in claude-sync anlegen, Uebergabedokument erstellen |

## Abschluss-Checkliste

```
[ ] Sync-Ordner in OneDrive angelegt
[ ] SYNC_PROTOCOL.md erstellt
[ ] Initialer Export fuer alle Systeme
[ ] CLAUDE.md + MEMORY.md mit Sync-Abschnitt
[ ] Uebergabedokument fuer neue Systeme
[ ] Erster erfolgreicher bidirektionaler Sync
```

## Siehe auch

- `claude-bach-vernetzung.md` -- Silo-Problem loesen, BACH integrieren
- `system-synopse.md` -- Systemvergleich

## Changelog

### v1.0.0 (2026-02-21)
- Initiale Version: OneDrive-basierter bidirektionaler Sync

---
BACH Skill-Architektur v2.0
