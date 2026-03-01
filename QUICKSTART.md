# BACH Quickstart Guide

**Version:** v3.2.0-butternut

## In 5 Minuten zum ersten BACH-Workflow

### 1. Installation (2 Minuten)

```bash
# Repository klonen
git clone https://github.com/lukisch/bach.git
cd bach

# Abhängigkeiten installieren
pip install -r requirements.txt

# BACH initialisieren
python system/setup.py
```

### 2. Erste Schritte (3 Minuten)

#### BACH starten

```bash
python bach.py --startup
```

#### Task erstellen und verwalten

```bash
# Neue Aufgabe anlegen
python bach.py task add "Erstes BACH-Experiment"

# Aufgaben anzeigen
python bach.py task list

# Aufgabe erledigen
python bach.py task done 1
```

#### Wissen speichern und abrufen

```bash
# Notiz ins Wiki schreiben
python bach.py wiki write "bash-tricks" "Nützliche Bash-Befehle sammeln"

# Wissen suchen
python bach.py wiki search "bash"
```

#### Memory-System nutzen

```bash
# Wichtigen Fakt speichern
python bach.py mem fact "Projekt-Deadline: 2025-12-31"

# Facts abrufen
python bach.py mem read facts
```

#### Agenten verwalten

```bash
# Alle verfügbaren Agenten anzeigen
python bach.py agent list

# Agenten starten
python bach.py agent start bueroassistent

# Agenten stoppen
python bach.py agent stop bueroassistent
```

#### Prompts verwalten

```bash
# Prompt-Liste anzeigen
python bach.py prompt list

# Neuen Prompt anlegen
python bach.py prompt add "Analyse-Prompt" --content "Analysiere folgendes..."

# Prompt-Board erstellen
python bach.py prompt board-create "Meine Prompts"
```

#### Scheduler-Status prüfen

```bash
python bach.py scheduler status
```

#### BACH beenden

```bash
python bach.py --shutdown
```

---

## Wichtigste Kommandos

| Bereich | Befehl | Beschreibung |
|---------|--------|--------------|
| Task | `bach task add "..."` | Neue Aufgabe anlegen |
| Task | `bach task list` | Aufgaben anzeigen |
| Memory | `bach mem write "..."` | Notiz schreiben |
| Memory | `bach mem fact "..."` | Fakt speichern |
| Wiki | `bach wiki search "..."` | Wissen suchen |
| Agent | `bach agent list` | Agenten anzeigen |
| Agent | `bach agent start <name>` | Agenten starten |
| Agent | `bach agent stop <name>` | Agenten stoppen |
| Prompt | `bach prompt list` | Prompts anzeigen |
| Prompt | `bach prompt add <name>` | Prompt anlegen |
| Scheduler | `bach scheduler status` | Scheduler-Status |
| Chain | `bach chain list` | Ketten anzeigen |
| Chain | `bach chain create <name>` | Neue Kette erstellen |

---

## Nächste Schritte

1. **Dokumentation erkunden**
   ```bash
   python bach.py docs list
   ```

2. **Agenten kennenlernen**
   ```bash
   python bach.py agent list
   python bach.py expert list
   ```

3. **Skills durchsuchen**
   ```bash
   cat SKILLS.md
   ```

4. **Eigenen Workflow erstellen**
   - Siehe: [WORKFLOWS.md](WORKFLOWS.md)
   - Beispiele für wiederkehrende Aufgaben

---

## Konfiguration

BACH passt sich automatisch an, aber Sie können anpassen:

- **Partner konfigurieren:** `python bach.py partner register claude`
- **Settings ändern:** `python bach.py config list`
- **Connector einrichten:** `python bach.py connector list`

---

## Weiterführende Dokumentation

- **[README.md](README.md)** - Vollständige Übersicht
- **[BACH_USER_MANUAL.md](BACH_USER_MANUAL.md)** - Vollständiges Handbuch
- **[SKILL.md](SKILL.md)** - LLM-Betriebsanleitung
- **[Skills Katalog](SKILLS.md)** - Alle verfügbaren Skills
- **[Agents Katalog](AGENTS.md)** - Alle verfügbaren Agenten

---

## Tipps

1. **Kontextuelles Arbeiten:** BACH merkt sich, woran Sie arbeiten
2. **Automatisierung:** Nutzen Sie Workflows und Scheduler für wiederkehrende Aufgaben
3. **Integration:** Verbinden Sie BACH mit Claude, Gemini oder Ollama
4. **Backup:** Regelmäßig `python bach.py backup create`
5. **Prompt-System:** Verwalten Sie LLM-Prompts zentral mit `bach prompt`

---

## Hilfe bekommen

```bash
# Allgemeine Hilfe
python bach.py --help

# Handler-spezifische Hilfe
python bach.py <handler> --help

# Dokumentation durchsuchen
python bach.py docs search "keyword"
```

---

*BACH v3.2.0-butternut - Best of Agentic Cognitive Helpers*
