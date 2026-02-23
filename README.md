# BACH - Textbasiertes Betriebssystem für LLMs

**Version:** v3.1.6
**Status:** Production-Ready
**Lizenz:** MIT

## Überblick

BACH ist ein textbasiertes Betriebssystem, das Large Language Models (LLMs) befähigt, eigenständig zu arbeiten, zu lernen und sich zu organisieren. Es bietet eine umfassende Infrastruktur für Task-Management, Wissensmanagement, Automatisierung und LLM-Orchestrierung.

### Kernfunktionen

- **🤖 5 KI-Agenten** - Spezialisierte Agenten für verschiedene Aufgabenbereiche
- **🛠️ 262 Tools** - Umfangreiche Tool-Bibliothek für Dateiverarbeitung, Analyse, Automation
- **📚 945 Skills** - Wiederverwendbare Workflows und Templates
- **🔄 10 Workflows** - Vorgefertigte Prozess-Workflows
- **💾 Wissensspeicher** - 147 Lessons + 249 Facts

## Installation

```bash
# Repository klonen
git clone https://github.com/YOUR_USERNAME/bach.git
cd bach

# Abhängigkeiten installieren
pip install -r requirements.txt

# BACH initialisieren
python system/setup.py
```

## Quick Start

```bash
# BACH starten
python bach.py --startup

# Task erstellen
python bach.py task add "Analysiere Projektstruktur"

# Wissen abrufen
python bach.py wiki search "Task Management"

# BACH beenden
python bach.py --shutdown
```

## Hauptkomponenten

### 1. Task-Management
Vollständiges GTD-System mit Priorisierung, Deadlines, Tags und Context-Tracking.

### 2. Wissenssystem
Strukturiertes Memory-System mit Facts, Lessons und automatischer Konsolidierung.

### 3. Agenten-Framework
Boss-Agenten orchestrieren Experten für komplexe Aufgaben (Büro, Gesundheit, Produktion, etc.).

### 4. Bridge-System
Connector-Framework für externe Services (Telegram, Email, WhatsApp, etc.).

### 5. Automatisierung
Scheduler für wiederkehrende Tasks und Event-basierte Workflows.

## Dokumentation

- **[Getting Started](docs/getting-started.md)** - Erste Schritte mit BACH
- **[API Reference](docs/reference/)** - Vollständige API-Dokumentation
- **[Skills Katalog](SKILLS.md)** - Alle verfügbaren Skills
- **[Agents Katalog](AGENTS.md)** - Alle verfügbaren Agenten

## Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/bach/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/bach/discussions)

---

*Generiert mit `bach docs generate readme`*
