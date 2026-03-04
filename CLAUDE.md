# BACH Projekt-Anweisungen

<!-- BACH:START - Automatisch generiert, nicht manuell bearbeiten -->

*Generiert: 2026-02-21 23:29 | Quelle: BACH Memory (Legacy)*

## System-Einstellungen

**SECURITY**
- `secrets_file_path`: ~/.bach/bach_secrets.json

**BEHAVIOR**
- `auto_backup_days`: 30
- `default_retention_days`: 30
- `healing.adaptation_rules`: directory_truth.json
- `healing.auto_detect_moves`: 1
- `healing.mode`: ask
- `timeout_checkpoint_minutes`: 10

**INTEGRATION**
- `integration.claude-code.claude_md_path`: 

## BACH Lessons (Top-10)

- 🔴 Fernet Salt-Format: Feste 16 Bytes statt Newline-Delimiter
- 🟠 Ein CLI Einstiegspunkt
- 🟠 SQLite statt JSON
- 🟠 PID-Tracking
- 🟠 dist_type Dreischritt
- 🟠 Keine versteckten Pfade
- 🟠 PyQt6 Access Violation
- 🟠 PyMuPDF: Save-to-Original erfordert Temp-Datei
- 🟠 Word vMerge: Zusammengefuegte Zellen beim Loeschen beachten
- 🟠 OCR-Tools existieren bereits

<!-- BACH:END -->

## Entwicklungs-Workflow (Single Installation Model, ab v3.3.0)

### Code aendern
```bash
# Direkt im Git-Repo entwickeln
cd /c/Users/User/OneDrive/KI\&AI/BACH
# CORE-Aenderungen: git add + commit + push
git add system/hub/neuer_handler.py
git commit -m "feat: neuer Handler"
git push origin main
```

### User-Daten sind geschuetzt
- `.gitignore` schuetzt: `bach.db`, `data/config/`, `_dev/`, persoenliche Experten, Credentials
- `git status` darf KEINE User-Dateien zeigen — sonst `.gitignore` erweitern

### Neue Tabellen anlegen
1. SQL-Schema in `system/data/schema/migrations/XXX_beschreibung.sql` erstellen
2. Migration ausfuehren: `bach upgrade` oder manuell via `python -c "import sqlite3..."`
3. Tracking in `_migrations`-Tabelle eintragen

### Verzeichnisstruktur
```
KI&AI/BACH/                    ← Git-Repo (github.com/lukisch/bach)
KI&AI/BACH_Dev/                ← Companion-Toolbox (Release-Doku, Tests, Scripts)
KI&AI/_ARCHIVED_BACH_vanilla_20260301/  ← Read-only Archiv
```

## Arbeitsprinzipien & Knowledge Capture

Diese Prinzipien gelten für alle Arbeiten mit BACH. Beachte sie IMMER:

1. **Tasks strukturieren** — Komplexe Aufgaben in Schritte zerlegen (`bach task add`)
2. **Fortschritt dokumentieren** — Status aktualisieren (`bach task status <id> in-progress|done`)
3. **Kontext speichern** — Wichtiges in memory_working schreiben (`bach mem write`)
4. **Tools nutzen** — BACH-Werkzeuge vor manuellen Lösungen bevorzugen
5. **Fehler protokollieren** — Probleme als Lessons festhalten (`bach lesson add`)
6. **Wissen sichern** — **KRITISCH**: Erkenntnisse ins Gedächtnis schreiben BEVOR der Kontext verloren geht

### Knowledge Capture (SQ015)

**Regel:** Wenn du während der Arbeit wichtige Erkenntnisse gewinnst, speichere sie SOFORT:

- **Facts** (Fakten, Definitionen, Wissen): `bach mem fact "API-Endpoint: /api/v2/users"`
- **Lessons** (Gelerntes, Erfahrungen): `bach lesson add "PyQt6 Access Violation: Immer Temp-Datei nutzen"`
- **Working Memory** (Session-Kontext): `bach mem write "Aktuell: Migration von PyMuPDF zu pypdf"`

**Wann?**
- Nach jedem wichtigen Fehler und dessen Lösung
- Bei Entdeckung von Best Practices
- Wenn du API-Details, Pfade, Konfigurationen findest
- Vor dem Ende einer langen Session (Kontext-Sicherung)

**Beispiele:**
```bash
# Fehler gelöst → Lesson
bach lesson add "Windows: UTF-8 Encoding mit PYTHONIOENCODING=utf-8 setzen" --severity high

# API-Detail gefunden → Fact
bach mem fact "GitHub API Rate-Limit: 5000/h für authenticated requests"

# Session-Kontext → Working Memory
bach mem write "Migration Status: 12/15 Dateien auf pypdf umgestellt, Tests laufen"
```

**Wichtig:** Diese Daten stehen dir in der nächsten Session wieder zur Verfügung!
