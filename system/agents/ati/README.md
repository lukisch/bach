# ATI - Advanced Tool Integration Agent

> Software-Entwickler-Agent fuer BACH

## Konzept

```
BATCHI = _BATCH + _CHIAH (Best-of Synopse)
ATI    = BATCHI - BACH (Delta zu BACH-Core)
BACH + ATI = BATCHI (vollstaendiger Software-Entwickler)
```

## Wichtig: Eigene Task-Verwaltung

ATI verwaltet **eigene** Software-Entwicklungs-Tasks:
- Scanner fuer AUFGABEN.txt = ATI Feature
- user.db/ati_tasks = ATI Tasks (nicht BACH)
- Onboarding neue Projekte = ATI Feature

BACH System-Tasks (bach.db/tasks) sind separat!

## Ordnerstruktur

```
agents/ati/
├── ATI.md              Haupt-Dokumentation
├── README.md           Diese Datei
├── data/
│   ├── config.json     ATI Konfiguration
│   └── tasks.db        (geplant) ATI-eigene Tasks
├── prompt_templates/   Prompt-Vorlagen fuer Headless
└── (geplant)
    ├── task_scanner.py     AUFGABEN.txt Scanner
    ├── session_daemon.py   Headless Sessions
    ├── onboarding.py       Projekt-Erkennung
    └── cli.py              ATI CLI
```

## CLI (geplant)

```bash
bach ati start           # Headless-Daemon starten
bach ati stop            # Daemon stoppen
bach ati status          # Status anzeigen
bach ati task list       # ATI-Tasks (Software-Dev)
bach ati scan            # AUFGABEN.txt scannen
bach ati onboard PATH    # Neues Projekt
bach ati export          # Als BATCHI exportieren
```

## Export: BATCHI

ATI kann als "BATCHI" exportiert werden:
```bash
bach ati export          # -> batchi.zip
```

Das Paket enthaelt alles was ein standalone Software-Entwickler-Agent braucht.

## Status

- [x] Konzept dokumentiert
- [x] Ordnerstruktur angelegt
- [x] config.json erstellt
- [x] Prompt-Templates erstellt (task, review, analysis)
- [ ] CLI-Handler (hub/handlers/ati.py)
- [ ] Scanner-Migration
- [ ] Headless Sessions
- [ ] Export-System
