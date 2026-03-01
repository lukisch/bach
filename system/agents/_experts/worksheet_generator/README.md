# Worksheet Generator (Expert)

**Task:** FOERD-01
**Status:** V1.0 Implemented

## Beschreibung

Dieser Expert erstellt Prompts für die Generierung von personalisierten Arbeitsblättern.
Er liest Daten aus den Klienten-Ordnern (`../user/buero/foerderplanung/klienten/`) bzw. den dort liegenden `bericht_data.json` Dateien.

## Nutzung

```bash
# Verfügbare Klienten auflisten
python agents/_experts/worksheet_generator/generator.py list

# Prompt generieren (z.B. für Mathe)
python agents/_experts/worksheet_generator/generator.py generate <KlientenID> mathe
```

## Ordnerstruktur

- `generator.py`: Hauptskript
- `templates/`: Prompt-Vorlagen (txt)
- `output/`: Generierte Prompts

## Neue Templates erstellen

Erstelle eine .txt Datei in `templates/`.
Verfügbare Platzhalter:

- `{{NAME}}`
- `{{DIAGNOSE}}`
- `{{INTERESSEN}}`
- `{{ZIELE}}`