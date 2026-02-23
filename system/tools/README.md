# BACH Tools-Verzeichnis

Übersicht aller 199 Tools im BACH-System (Stand: 2026-02-14)

---

## 📊 Status Quo

- **Gesamt:** 199 Python-Dateien
- **Aktiv genutzt:** ~159 Tools (80%)
- **Archiviert:** 42 Tools (21%)
- **Ungenutzt:** 21 Tools (11%)
- **Durchschnitt:** 268 Zeilen pro Tool

**⚠️ Achtung:** Aktuell befindet sich der Tools-Ordner in einem unstrukturierten Zustand.
Eine umfassende Reorganisation ist in Planung. Siehe: `docs/TOOLS_CLEANUP_KONZEPT.md`

---

## 🗂️ Aktuelle Struktur

### Root-Level (81 Tools)
Hauptsächlich allgemeine Utilities und ältere Tools ohne klare Zuordnung.

**Wichtigste Tools:**
- `backup_manager.py` - System-Backups
- `injectors.py` - Dependency Injection
- `autolog.py` - Automatisches Logging
- `encoding_fix.py` - Encoding-Reparatur
- `token_monitor.py` - Token-Überwachung

### _archive/ (42 Tools)
Veraltete oder obsolete Tools. Werden für Referenz aufbewahrt.

### _policies/ (5 Tools)
Code-Policies und Standards.
- `policy_control.py` - Policy-Verwaltung
- `policy_applier.py` - Policy-Anwendung
- `emoji_safe.py` - Emoji-Handling
- `encoding_header.py` - Header-Management
- `json_safe.py` - JSON-Utilities

### agents/ (6 Tools)
Agent-Framework und Implementierungen.
- `agent_framework.py` - Basis-Framework
- `agent_cli.py` - CLI-Interface
- `entwickler_agent.py` - Entwickler-Agent ⚠️ UNGENUTZT
- `production_agent.py` - Produktions-Agent
- `research_agent.py` - Research-Agent

### code_quality/ (29 Tools mit `c_` Prefix)
Tools für Code-Qualität, Analyse und Transformationen.

**⚠️ Wird reorganisiert:** Prefix `c_` wird entfernt, Tools werden in Unterkategorien gruppiert.

**Wichtigste:**
- `c_code_analyzer.py` - Code-Analyse
- `c_encoding_fixer.py` - Encoding-Fixes
- `c_file_cleaner.py` - Datei-Bereinigung
- `c_duplicate_detector.py` - Duplikat-Erkennung
- `c_json_fixer.py` - JSON-Reparatur

### testing/ (29 Tools)
Test-Framework und Test-Suites.

**Unterverzeichnisse:**
- `b_tests/` - Build/BACH Tests (B001-B008)
- `o_tests/` - Operational Tests (O001-O006)
- `playwright/` - Browser-Automation

**Test-Runner:**
- `run_b_tests.py` - Build-Tests ausführen
- `run_o_tests.py` - Operational-Tests ausführen

### maintenance/ (12 Tools)
System-Wartung und Administration.
- `sync_skills.py` - Skill-Synchronisation
- `skill_health_monitor.py` - Health-Checks
- `registry_watcher.py` - Registry-Überwachung
- `task_statistics.py` - Task-Statistiken
- `archive_done_tasks.py` - Task-Archivierung

### generators/ (4 Tools)
Code- und Content-Generierung.
- `skill_generator.py` - Skill-Generierung
- `exporter.py` - Export-Funktionen
- `os_generator.py` - OS-Generierung
- `distribution_system.py` - Distributions-System

### integrations/ (11 Tools)

#### ocr/ (3 Tools)
OCR-Integration (Tesseract).
- `cli.py` - CLI-Interface (37x verwendet!)
- `engine.py` - OCR-Engine (13x verwendet)

#### rag/ (3 Tools)
Retrieval-Augmented Generation.
- `search.py` - RAG-Suche (10x verwendet)
- `ingest.py` - Daten-Ingestion

#### ollama/ (5 Tools)
Ollama LLM Integration.
- `ollama_client.py` - Client-Bibliothek
- `ollama_worker.py` - Worker-Prozesse
- `ollama_summarize.py` - Zusammenfassungen

### partner_communication/ (8 Tools)
Kommunikation mit externen Systemen.
- `interaction_protocol.py` - Kommunikations-Protokoll
- `communication.py` - Kommunikations-Handler
- `ai_compatible.py` - AI-Kompatibilität
- `real_tools.py` - Tool-Integration

### analysis/ (8 Tools)
Analyse-Tools für verschiedene Zwecke.
- `autolog_analyzer.py` - Log-Analyse
- `session_analyzer.py` - Session-Analyse
- `db_check.py` - Datenbank-Checks
- `forensic_db_scan.py` - Forensische DB-Analyse
- `folder_diff_scanner.py` - Ordner-Vergleich

---

## 🔥 Meist-genutzte Tools (Top 10)

1. **ocr/cli.py** (37x) - OCR-CLI
2. **injectors.py** (13x) - Dependency Injection
3. **ocr/engine.py** (13x) - OCR-Engine
4. **generators/exporter.py** (11x) - Export
5. **rag/search.py** (10x) - RAG-Suche
6. **backup_manager.py** (7x) - Backups
7. **encoding_fix.py** (7x) - Encoding-Fixes
8. **autolog.py** (6x) - Auto-Logging
9. **tool_discovery.py** (6x) - Tool-Discovery
10. **nulcleaner.py** (5x) - NUL-Char Bereinigung

**⚠️ Diese Tools NICHT löschen oder verschieben ohne gründliche Impact-Analyse!**

---

## ⚠️ Kritische Befunde

### Duplikate (müssen konsolidiert werden)
```
1. run_b_tests.py       - 2x (testing/ und testing/b_tests/)
2. run_o_tests.py       - 2x (testing/ und testing/o_tests/)
3. doc_update_checker   - 2x (root und _archive/)
4. cleanup.py           - 2x (_archive/)
```

### Ungenutzte Tools (21)
Tools ohne erkennbare Nutzung. Kandidaten für Archivierung:
- `_policies/encoding_header.py`
- `_policies/json_safe.py`
- `agents/entwickler_agent.py` ⚠️ **Warum ungenutzt?**
- `c_skill_init.py`
- `c_skill_package.py`
- `c_skill_validate.py`
- Weitere in `docs/TOOLS_ANALYSIS_SUMMARY.md`

### Unkategorisiert (37)
Tools ohne klare Kategorie-Zuordnung. Müssen eingeordnet werden.

---

## 📚 Dokumentation

- **Vollständige Analyse:** `docs/TOOLS_ANALYSIS_SUMMARY.md`
- **Aufräumkonzept:** `docs/TOOLS_CLEANUP_KONZEPT.md`
- **Analyse-Daten:** `tools/analysis_results.json`

---

## 🔧 Analyse-Tools

Folgende Tools wurden für diese Analyse verwendet:

```bash
# Tiefenanalyse mit Kategorisierung
python tools/deep_analysis.py

# Abhängigkeits- und Nutzungsanalyse
python tools/dependency_analysis.py
```

**Ergebnisse:** `tools/analysis_results.json`

---

## 🚀 Geplante Reorganisation

Eine vollständige Reorganisation ist in Planung mit folgenden Zielen:

1. **Klare Kategorien** - 12 Hauptkategorien mit Unterverzeichnissen
2. **Bessere Namen** - `c_*` Prefix entfernen
3. **Duplikate weg** - Konsolidierung identischer Tools
4. **Dokumentiert** - README in jeder Kategorie
5. **Getestet** - Alle Imports aktualisiert

**Geschätzter Aufwand:** 15-22 Arbeitstage
**Details:** Siehe `docs/TOOLS_CLEANUP_KONZEPT.md`

---

## 🔍 Tool finden

### Nach Kategorie
```bash
# Code-Quality
ls tools/c_*.py

# Testing
ls tools/testing/

# OCR
ls tools/ocr/

# Maintenance
ls tools/maintenance/
```

### Nach Nutzung
```bash
# Wo wird ein Tool verwendet?
grep -r "from tools.TOOLNAME import" .
grep -r "import tools.TOOLNAME" .
```

### Nach Funktion
```bash
# Alle Analyse-Tools
ls tools/*analyz*.py

# Alle Scanner
ls tools/*scan*.py

# Alle Generatoren
ls tools/*generat*.py
```

---

## ⚡ Schnellstart

### Tool ausführen
```bash
# Mit Python direkt
python tools/TOOLNAME.py --help

# Über BACH CLI (wenn registriert)
python bach.py TOOLNAME --help
```

### Tool importieren
```python
# In eigenem Code
from tools.TOOLNAME import function_name

# Oder ganzes Modul
import tools.TOOLNAME as tool
```

### Neues Tool hinzufügen
```bash
# Template nutzen (wenn vorhanden)
cp _templates/tool_template.py tools/my_new_tool.py

# Oder von Grund auf
touch tools/my_new_tool.py
# Mindestanforderungen:
# - Docstring
# - if __name__ == "__main__": Guard
# - Error Handling
# - ArgParse (für CLI-Tools)
```

---

## 📝 Best Practices

### Tool-Entwicklung
1. **Docstring** - Immer erklären was das Tool macht
2. **Main Guard** - `if __name__ == "__main__":`
3. **Error Handling** - Try/Except für robuste Tools
4. **Logging** - `autolog.py` nutzen
5. **Encoding** - UTF-8 explizit setzen
6. **Tests** - Mindestens ein B-Test oder O-Test

### Naming Conventions
- **Klare Namen** - `code_analyzer.py` statt `ca.py`
- **Snake Case** - `my_tool.py` nicht `MyTool.py`
- **Keine Prefixes** - Außer bei klarer Konvention
- **Beschreibend** - Name zeigt Funktion

### Kategorisierung
- **Ein Zweck** - Tool macht eine Sache gut
- **Richtige Kategorie** - Ins passende Verzeichnis
- **Dependencies klar** - Imports dokumentieren
- **CLI oder Library** - Entweder/oder, nicht beides

---

## 🐛 Probleme melden

Bei Problemen mit Tools:

1. **Check Logs:** `data/logs/`
2. **Encoding-Probleme:** `python tools/encoding_fix.py`
3. **Import-Fehler:** Pfade prüfen
4. **Tool fehlt:** Eventuell archiviert? Check `_archive/`

---

## 📞 Support

- **Dokumentation:** `docs/`
- **Analyse-Ergebnisse:** `tools/analysis_results.json`
- **Code-Review:** BACH Development Team
- **Fragen:** Siehe Hauptdokumentation

---

**Letzte Aktualisierung:** 2026-02-14
**Verantwortlich:** BACH Worker-Agent
**Nächste Review:** Nach Reorganisation (geplant in 3-4 Wochen)
