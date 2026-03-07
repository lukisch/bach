# BACH Quickstart Guide

**Version:** v3.1.6

## In 5 Minuten zu Ihrem ersten BACH-Workflow

### 1. Installation (2 Minuten)

```bash
# Repository klonen
git clone https://github.com/lukisch/bach.git
cd bach

# Abhaengigkeiten installieren
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
python bach.py wiki write "bash-tricks" "Nuetzliche Bash-Befehle sammeln"

# Wissen suchen
python bach.py wiki search "bash"
```

#### Memory-System nutzen

```bash
# Wichtigen Fakt speichern
python bach.py mem write fact "Projekt-Deadline: 2024-12-31"

# Facts abrufen
python bach.py mem read facts
```

#### BACH beenden

```bash
python bach.py --shutdown
```

---

## Wichtigste Kommandos

---

## Naechste Schritte

1. **Dokumentation erkunden**
   ```bash
   python bach.py docs list
   ```

2. **Agenten kennenlernen**
   ```bash
   python bach.py agent list
   ```

3. **Skills durchsuchen**
   ```bash
   cat SKILLS.md
   ```

4. **Eigenen Workflow erstellen**
   - Siehe: [Skills/_workflows/](skills/_workflows/)
   - Beispiele fuer wiederkehrende Aufgaben

---

## Konfiguration

BACH passt sich automatisch an, aber Sie koennen anpassen:

- **Partner konfigurieren:** `python bach.py partner register claude`
- **Settings aendern:** `python bach.py config list`
- **Connector einrichten:** `python bach.py connector list`

---

## Weiterfuehrende Dokumentation

- **[README.md](README.md)** - Vollstaendige Uebersicht
- **[API-Referenz](docs/reference/api.md)** - Programmier-Interface
- **[Skills-Katalog](SKILLS.md)** - Alle verfuegbaren Skills
- **[Agenten-Katalog](AGENTS.md)** - Alle verfuegbaren Agenten

---

## Tipps

1. **Kontextuelles Arbeiten:** BACH merkt sich, woran Sie arbeiten
2. **Automatisierung:** Nutzen Sie Workflows fuer wiederkehrende Aufgaben
3. **Integration:** Verbinden Sie BACH mit Claude, Gemini oder Ollama
4. **Backup:** Regelmaessig `python bach.py backup create`

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

English version: [QUICKSTART.md](QUICKSTART.md)

*Generiert mit `bach docs generate quickstart --lang de`*
