# Gemini Partner Workspace

## Ordnerstruktur
```
partners/gemini/
├── prompts/              # Prompt-Vorlagen fuer verschiedene Modi
│   ├── auto.txt          # Auto-Modus (DEFAULT)
│   ├── default.txt       # Interaktiv-Modus
│   ├── analyse.txt       # Analyse-Scripts ausfuehren
│   ├── bulk.txt          # Alle Tasks ohne Limit
│   └── research.txt      # Recherche-Modus
├── startprompt_gemini.txt  # Individueller User-Prompt
├── start_gemini.bat      # Interaktiver Starter
├── inbox/                # Auftraege an Gemini
├── outbox/               # Berichte von Gemini
└── workspace/            # Arbeitsdateien
```

## Schnellstart

**Doppelklick auf `start_gemini.bat`** - zeigt Menue:

| Taste | Modus | Backend |
|-------|-------|---------|
| Enter | Auto (2 Tasks) | CLI |
| 1 | Auto (5 Tasks) | CLI |
| 2 | Bulk (alle Tasks) | CLI |
| 3 | Bulk | GUI |
| 4 | Interaktiv | GUI |
| 5 | Individual-Prompt | GUI |
| 6 | Analyse | GUI |
| 7 | Research | GUI |
| 8 | Docs-Update | GUI |
| 9 | Wiki-Update | GUI |
| X | Help-Update | GUI |
| L | Vorlagen auflisten | - |

## Kommandozeile

```bash
# Auto-Modus (DEFAULT) - 2 Tasks abarbeiten
python skills/tools/gemini_start.py

# Auto-Modus mit mehr Tasks
python skills/tools/gemini_start.py --tasks 5

# Interaktiv (wartet auf Eingabe)
python skills/tools/gemini_start.py --default

# Individueller User-Prompt
python skills/tools/gemini_start.py --individual

# Spezifischer Modus
python skills/tools/gemini_start.py --mode analyse
python skills/tools/gemini_start.py --mode bulk
python skills/tools/gemini_start.py --mode research

# Vorlagen auflisten
python skills/tools/gemini_start.py --list

# Nur Befehl anzeigen
python skills/tools/gemini_start.py --dry-run
```

## Prompt-Vorlagen (prompts/)

| Datei | Beschreibung |
|-------|--------------|
| auto.txt | Auto-Modus: Tasks sofort abarbeiten (DEFAULT) |
| default.txt | Interaktiv: Wartet auf Anweisungen |
| analyse.txt | Fuehrt alle Analyse-Scripts aus |
| bulk.txt | Bearbeitet ALLE Tasks ohne Limit |
| research.txt | Recherche-Modus fuer Themenanalyse |
| docs-update.txt | Help+Wiki mit Skills abgleichen |
| wiki-update.txt | Zufaelligen Wiki-Eintrag aktualisieren |
| help-update.txt | Zufaellige Help-Datei aktualisieren |

## Workflows (skills/workflows/)

Die Update-Modi verweisen auf detaillierte Workflows:
- `wiki-author.md` - Vollstaendiger Wiki-Autor Workflow
- `help-forensic.md` - Help-Forensik Workflow

## Individueller Prompt

Bearbeite `startprompt_gemini.txt` fuer eigene Anweisungen.
Nutze mit `--individual` oder Menue-Option 5.

## Task-Workflow (CLI-basiert)

Gemini kann Tasks direkt ueber die CLI bearbeiten:

```bash
# Offene Tasks anzeigen
python bach.py task list

# Nur Gemini-Tasks anzeigen
python bach.py task list | grep gemini

# Task als erledigt markieren
python bach.py task done <id>
python bach.py task done <id> "Abschluss-Notiz"

# Task-Details anzeigen
python bach.py task show <id>
```

**WICHTIG:** Gemini muss Tasks NICHT mehr ueber `_TASKS.md` abgleichen.
Die CLI ist die primaere Schnittstelle zum Task-System.

## Kommunikation
```bash
bach msg send user "Nachricht" --from gemini
```

## Pfade (Self-Healing)

Alle Pfade werden relativ ermittelt. Zentrale Konfiguration:
- `bach_paths.py` im BACH-Root

```python
from bach_paths import BACH_ROOT, DATA_DIR, get_db
```

## Metaprompt
Gemini liest: `~/.gemini/GEMINI.md`

## Antigravity Workflow (optional)
Falls `.agent/workflows/bach-task.md` existiert:
- Trigger mit `/bach-task` in Antigravity
- Nutzt `/ turbo-all` fuer automatische Ausfuehrung