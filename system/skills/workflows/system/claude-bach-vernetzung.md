---
name: claude-bach-vernetzung
version: 1.0.0
type: workflow
author: Lukas Geiger + Claude Opus 4.6
created: 2026-02-21
updated: 2026-02-21
anthropic_compatible: true

trigger: Neues System einrichten, Claude Code mit BACH verbinden, Silo-Problem loesen
duration: 30-60 Minuten (Ersteinrichtung)
complexity: medium

dependencies:
  tools: []
  skills: []
  external: [Claude Code, OneDrive, npm]

description: >
  Anleitung zur vollstaendigen Integration von Claude Code mit dem BACH-System.
  Loest das Memory-Silo-Problem und richtet MCP-Server, Home-Memory-Hub
  und globale CLAUDE.md ein.
---

# Claude Code + BACH Vernetzung

## Wann anwenden?

- Neues System wird eingerichtet und Claude Code soll mit BACH arbeiten
- Silo-Problem tritt auf (Wissen geht zwischen Projekten verloren)
- MCP-Server muessen installiert werden
- Home-Memory-Hub wird erstellt

## Das Silo-Problem

### Problem

Claude Code speichert Memory **projekt-basiert** unter:
```
~/.claude/projects/<pfad-hash>/memory/MEMORY.md
```

Jedes Projekt hat ein isoliertes Memory. Konsequenzen:
- Gleiche Fehler werden in verschiedenen Projekten wiederholt
- Lessons Learned aus Projekt A sind in Projekt B unsichtbar
- Kein projektuebergreifendes Wissensmanagement moeglich

### Loesung: Hub-Architektur

```
~/.claude/projects/C--Users-User/memory/    <-- HOME-MEMORY (Hub)
  MEMORY.md                                  <-- Zentrales Wissen
  mcmc-server.md                             <-- Detail-Datei
  weitere-details.md                         <-- Detail-Datei
  ...

~/CLAUDE.md                                  <-- Globale Regeln (JEDES Projekt)

~/.claude/projects/<projekt-hash>/memory/    <-- Projekt-Memory (Silo)
  MEMORY.md                                  <-- Nur projektspezifisches Wissen
```

**Prinzip:**
1. `~/CLAUDE.md` wird von JEDER Claude Code Instanz geladen (globale Regeln)
2. Home-Memory (`C--Users-User`) wird geladen wenn man im Home-Verzeichnis startet
3. Projekt-Memories enthalten nur projektspezifisches Wissen
4. Cross-Projekt-Wissen wird im Home-Memory gesammelt

## Voraussetzungen

- [ ] Claude Code installiert (`claude --version`)
- [ ] Git Bash verfuegbar
- [ ] Node.js >= 18 (`node --version`)
- [ ] npm eingeloggt (`npm whoami`)
- [ ] OneDrive synchron (fuer BACH-Zugriff)

## Schritt 1: Globale CLAUDE.md erstellen

Erstelle `~/CLAUDE.md` (Home-Verzeichnis) mit:

```markdown
# Globale Regeln fuer alle Claude Code Instanzen

## Sprache
- Antworte IMMER auf Deutsch
- Technische Terme und Code-Identifier bleiben englisch

## User
- Name: Lukas Geiger
- Standort: Bernau
- GitHub: github.com/lukisch

## System: Windows 11 + Git Bash
- PYTHONIOENCODING=utf-8 bei JEDEM Python-Aufruf
- Bash-Pfade: /c/Users/User/ (nicht C:\Users\User\)
- Python-Pfade: C:\Users\User\... (Windows-nativ)
- NUL-Dateien vermeiden (Windows-reservierte Namen)
- & in Pfaden: Immer in Anfuehrungszeichen setzen
- sqlite3 CLI nicht verfuegbar -- python -c "import sqlite3..." nutzen

## OneDrive
- File-Locking: Retry bei Fehlern
- .venv NIEMALS in OneDrive-Ordnern

## Arbeitsweise
- ZUERST bestehenden Code lesen, dann aendern
- Keine Duplikate erzeugen
- User korrigiert aktiv -- flexibel reagieren

## BACH System
- BACH-Pfad: /c/Users/User/OneDrive/KI&AI/BACH_v2_vanilla/system/
- bach_api (Library) bevorzugen, nicht bach.py (CLI)
- Nie direkt auf bach.db zugreifen

## Memory-System
- Home-Memory als zentraler Hub
- Detail-Dateien in Memory-Ordner, Referenz in MEMORY.md
- MEMORY.md max 200 Zeilen
```

## Schritt 2: Home-Memory einrichten

```bash
# Memory-Ordner fuer Home-Verzeichnis (wird automatisch erstellt beim
# ersten Aufruf von Claude Code im Home-Verzeichnis)
mkdir -p ~/.claude/projects/C--Users-User/memory/
```

Erstelle `MEMORY.md` dort mit:
- User-Profil
- Master Lessons Learned (Cross-Projekt)
- BACH-System-Infos
- MCP-Server-Status
- Index der Detail-Dateien
- Index der Projekt-Silos

**WICHTIG:** Max 200 Zeilen! Groessere Bloecke in separate .md Dateien auslagern.

## Schritt 3: MCP-Server installieren

BACH hat zwei MCP-Server: FileCommander (43 Tools) und CodeCommander (17 Tools).

### Installation

```bash
# Installationsordner (KEIN & im Pfad!)
mkdir -p ~/.claude/mcp-servers/bach-filecommander-mcp
mkdir -p ~/.claude/mcp-servers/bach-codecommander-mcp

# FileCommander
cd ~/.claude/mcp-servers/bach-filecommander-mcp
npm init -y
npm install bach-filecommander-mcp

# CodeCommander
cd ~/.claude/mcp-servers/bach-codecommander-mcp
npm init -y
npm install bach-codecommander-mcp
```

### Registrierung

```bash
# WICHTIG: --scope user (NICHT project!)
# Project-Scope hat Bug: wird nicht immer geladen (GitHub #5037, #15215)

claude mcp add --scope user bach-filecommander \
  node ~/.claude/mcp-servers/bach-filecommander-mcp/node_modules/bach-filecommander-mcp/dist/index.js

claude mcp add --scope user bach-codecommander \
  node ~/.claude/mcp-servers/bach-codecommander-mcp/node_modules/bach-codecommander-mcp/dist/index.js
```

### Verifikation

```bash
# Pruefen ob registriert
claude mcp list

# In einer Claude Code Session testen
# fc_get_time sollte funktionieren
# cc_validate_json sollte funktionieren
```

### Update-Workflow

```bash
cd ~/.claude/mcp-servers/bach-filecommander-mcp && npm update bach-filecommander-mcp
cd ~/.claude/mcp-servers/bach-codecommander-mcp && npm update bach-codecommander-mcp
```

## Schritt 4: BACH-Integration testen

```bash
# BACH API starten (im BACH-Verzeichnis)
cd "/c/Users/User/OneDrive/KI&AI/BACH_v2_vanilla/system"
PYTHONIOENCODING=utf-8 python -c "
import sys; sys.path.insert(0, '.')
from bach_api import session
session.startup(partner='claude', mode='silent')
print('BACH OK:', session.version())
"
```

## Schritt 5: Cross-System Sync (optional)

Wenn mehrere Systeme synchronisiert werden sollen, siehe:
`cross-system-sync.md`

## Bekannte Fallstricke

| Problem | Loesung |
|---------|---------|
| `&` im Pfad bricht npm | `node` direkt aufrufen, nicht `npm run` |
| MCP project-scope laedt nicht | Immer `--scope user` nutzen |
| MEMORY.md > 200 Zeilen | Detail-Dateien auslagern |
| `.venv` in OneDrive | Lock-Konflikte -- venv ausserhalb OneDrive anlegen |
| NUL-Dateien entstehen | `/dev/null` vermeiden auf Windows |
| sqlite3 CLI fehlt | `python -c "import sqlite3..."` |
| OneDrive File-Locking | Retry, oder OneDrive kurz pausieren |

## Entscheidungspunkte

| Situation | Aktion |
|-----------|--------|
| Neues Projekt angelegt | Projekt-MEMORY.md minimal, Cross-Projekt-Wissen ins Home-Memory |
| Lesson Learned in Projekt | Auch ins Home-Memory uebertragen |
| MCP-Server Update verfuegbar | `npm update` in mcp-servers Ordner |
| Home-Memory wird zu gross | Detail-Dateien auslagern, Index pflegen |

## Abschluss-Checkliste

```
[ ] ~/CLAUDE.md erstellt mit globalen Regeln
[ ] Home-Memory-Hub eingerichtet
[ ] MCP-Server installiert und registriert (--scope user)
[ ] BACH API erreichbar
[ ] Erste Claude Code Session mit MCP-Tools erfolgreich
[ ] Cross-System Sync eingerichtet (falls noetig)
```

## Siehe auch

- `cross-system-sync.md` -- Multi-System Wissens-Sync
- `system-anschlussanalyse.md` -- System-Analyse
- BACH `skills/_services/builder.md` -- System-Builder

## Changelog

### v1.0.0 (2026-02-21)
- Initiale Version: Silo-Problem, MCP-Setup, Home-Memory-Hub, BACH-Integration

---
BACH Skill-Architektur v2.0
