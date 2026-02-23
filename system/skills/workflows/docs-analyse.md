# Workflow: Dokumenten-Anforderungsanalyse

**Version:** 1.2.0
**Erstellt:** 2026-01-20
**Aktualisiert:** 2026-01-20

---

## Zweck

Analysiert alle Konzept- und Anforderungsdokumente im ../docs/ Ordner, prueft deren Anforderungen gegen den aktuellen Code und erstellt einen konsolidierten Differenz-Bericht.

---

## Namenskonvention

### Praefix und Suffix
Alle analysierten Dokumente erhalten:
- **Praefix:** `conN_` wobei N = Analyse-Version (1, 2, 3, ...)
- **Suffix:** `_XX` wobei XX = Erfuellungsgrad in Prozent (gerundet auf 10er)

### Versionierung
Bei jeder neuen Analyse wird die Versionsnummer hochgezaehlt:

```
Erste Analyse:
  KONZEPT_GUI.md              -> con1_KONZEPT_GUI_90.md
  ANFORDERUNGSANALYSE.md      -> con1_ANFORDERUNGSANALYSE.md
  consense_diff.md            -> consense_diff_1.md

Zweite Analyse (alle Dokumente bekommen con2_):
  con1_KONZEPT_GUI_90.md      -> con2_KONZEPT_GUI_95.md
  NEUES_DOC.md                -> con2_NEUES_DOC_60.md
  ANFORDERUNGSANALYSE.md      -> con2_ANFORDERUNGSANALYSE.md
  consense_diff.md            -> consense_diff_2.md

Dritte Analyse:
  con2_KONZEPT_GUI_95.md      -> con3_KONZEPT_GUI_100.md
  con2_NEUES_DOC_60.md        -> con3_NEUES_DOC_80.md
  ...
```

### Versions-Ermittlung
```
1. Suche nach hoechstem conN_ Praefix in ../docs/ und ../docs/_archive/
2. Falls keine con_ Dateien: N = 1
3. Falls con_ ohne Zahl: N = 1 (Legacy, wird zu con1_)
4. Sonst: N = hoechste gefundene Zahl + 1
```

### Archivierungs-Schwelle
- **>= 75% erfuellt:** Dokument wird nach `../docs/_archive/` verschoben
- **< 75% erfuellt:** Dokument bleibt in `../docs/` mit Praefix/Suffix
- **Schwelle konfigurierbar** (Default: 75)

### Ordner-Erstellung
Falls `../docs/_archive/` nicht existiert, wird er automatisch angelegt.

---

## Trigger

- Manuell: `bach workflow run docs-analyse`
- Empfohlen: Vor Major-Releases oder nach Feature-Sprints

---

## Eingabe

- **Quellordner:** `../docs/` (root, ohne Unterordner wie _archive, _ideas)
- **Dateitypen:** `*.md`, `*.txt`
- **Ausnahmen:** `README.txt`, bereits archivierte Dokumente

---

## Ablauf

### Phase 1: Dokumente sammeln
```
1. Liste alle *.md und *.txt Dateien in ../docs/ (root)
2. Filtere README.txt aus
3. Erstelle Arbeitsliste
```

### Phase 2: Anforderungen extrahieren
```
Fuer jedes Dokument:
1. Lese Inhalt
2. Identifiziere Anforderungen (Checklisten, Tabellen, FEHLT/TODO Marker)
3. Kategorisiere: Struktur, Code, API, DB-Schema, CLI, Feature
```

### Phase 3: Code-Pruefung
```
Fuer jede Anforderung:
1. Bestimme Pruefmethode:
   - Struktur: Glob/Dateisystem-Check
   - DB-Schema: SQLite PRAGMA table_info
   - API: Grep in server.py
   - CLI: Grep in handlers/
   - Code: Grep/Read spezifische Dateien
2. Fuehre Pruefung durch
3. Markiere als: ERFUELLT, TEILWEISE, FEHLT
4. Dokumentiere Proof (Pfad:Zeile oder Befehl)
```

### Phase 4: Bewertung
```
Fuer jedes Dokument:
1. Zaehle erfuellte vs. offene Anforderungen
2. Berechne Erfuellungsgrad (%)
3. Runde auf 10er (67% -> 70, 83% -> 80)
4. Entscheide:
   - >= 75% erfuellt: ARCHIVIEREN
   - < 75%: IN DOCS BELASSEN
```

### Phase 5: Ausgabe generieren
```
1. Erstelle ANFORDERUNGSANALYSE.md
   - Zusammenfassungstabelle
   - Pro Dokument: Erfuellte + Offene Anforderungen

2. Erstelle consense_diff.md
   - Nur offene Anforderungen
   - Gruppiert nach Prioritaet (P1-P4)
   - Kontext aus Quelldokumenten
```

### Phase 6: Versionsnummer ermitteln
```
1. Scanne ../docs/ und ../docs/_archive/ nach conN_ Praefix
2. Extrahiere hoechste Zahl N aus gefundenen Dateien
3. Falls con_ ohne Zahl (Legacy): behandle als con1_
4. Neue Version = hoechste gefundene + 1
5. Falls keine con_ Dateien: Version = 1
```

### Phase 7: Dokumente umbenennen und verschieben
```
1. Stelle sicher dass ../docs/_archive/ existiert
   - Falls nicht: Ordner anlegen

2. Fuer jedes analysierte Dokument:
   a. Entferne altes conN_ Praefix falls vorhanden
   b. Entferne altes _XX Suffix falls vorhanden
   c. Berechne gerundeten Prozentsatz (auf 10er)
   d. Erstelle neuen Namen: conN_BASISNAME_XX.ext
   e. Falls >= Schwelle: Verschiebe nach ../docs/_archive/
   f. Falls < Schwelle: Verschiebe/Benenne um in ../docs/

3. Spezielle Dateien:
   a. ANFORDERUNGSANALYSE.md -> conN_ANFORDERUNGSANALYSE.md
   b. consense_diff.md -> consense_diff_N.md
```

---

## Ausgabe

| Datei | Beschreibung |
|-------|--------------|
| `../docs/conN_ANFORDERUNGSANALYSE.md` | Vollstaendige Analyse (Version N) |
| `../docs/consense_diff_N.md` | Konsolidierte offene Anforderungen (Version N) |
| `../docs/_archive/conN_*_XX.*` | Archivierte (>=Schwelle) Dokumente |
| `../docs/conN_*_XX.*` | Verbleibende (<Schwelle) Dokumente |

### Beispiel nach 3 Analysen
```
../docs/
├── con3_ANFORDERUNGSANALYSE.md      # Aktuelle Analyse
├── consense_diff_3.md               # Aktuelle offene Punkte
├── con3_SKILL_EXPORT_20.md          # Noch nicht erfuellt
├── con3_SERVICE_ORDNER_40.md        # Noch nicht erfuellt
│
../docs/_archive/
├── con1_ANFORDERUNGSANALYSE.md      # Historisch
├── consense_diff_1.md               # Historisch
├── con3_KONZEPT_GUI_100.md          # Vollstaendig erfuellt
├── con3_SCANNER_MIGRATION_100.md    # Vollstaendig erfuellt
├── con2_DAEMON_DASHBOARD_80.md      # Bei Analyse 2 archiviert
```

---

## Pruefmethoden-Referenz

### Struktur-Check
```bash
# Ordner existiert?
Glob: path/to/folder/**/*

# Datei existiert?
Read: path/to/file.py
```

### DB-Schema-Check
```python
import sqlite3
db = sqlite3.connect('data/bach.db')
# Tabelle existiert?
tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
# Spalte existiert?
cols = db.execute("PRAGMA table_info(tablename)")
```

### API-Check
```bash
# Endpoint implementiert?
Grep: "@app.get.*\/api\/endpoint" in gui/server.py
```

### CLI-Check
```bash
# Handler existiert?
Glob: hub/handlers/handlername.py
# Befehl implementiert?
Grep: "def cmd_befehlname" in bach.py
```

---

## Prioritaets-Klassifizierung

| Prioritaet | Kriterien |
|:----------:|-----------|
| P1 | Kernfunktionalitaet fehlt, System nicht nutzbar |
| P2 | Wichtige Feature fehlt, Workaround moeglich |
| P3 | Nice-to-have, verbessert UX |
| P4 | Kosmetisch, Dokumentation, Code-Qualitaet |

---

## Beispiel-Aufruf

```bash
# Vollstaendige Analyse
bach workflow run docs-analyse

# Nur Pruefung ohne Archivierung
bach workflow run docs-analyse --dry-run

# Spezifisches Dokument
bach workflow run docs-analyse --file KONZEPT_XY.md
```

---

## Changelog

| Version | Datum | Aenderung |
|---------|-------|-----------|
| 1.0.0 | 2026-01-20 | Initial erstellt |