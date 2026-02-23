# Service/Agent Validator Workflow

## Zweck
Qualitätsprüfung für neue Services, Agents und Experts im BACH-System.

## Wann anwenden
- Bei Erstellung eines neuen Agents/Experts/Services
- Bei größeren Änderungen an bestehenden Komponenten
- Als Teil des Code-Review Prozesses

## Checkliste

### 1. Unabhängigkeit (Funktioniert ohne User-Daten)
```bash
# Test: Komponente mit leerer DB starten
bach --db reset --test
bach <component> --dry-run
```
**Kriterium:** Keine Fehler bei fehlenden User-Daten

### 2. CLI-Integration
```bash
# Prüfen: Gibt es einen CLI-Befehl?
bach help <component>
bach <component> --help
```
**Kriterium:** Mindestens ein CLI-Einstiegspunkt vorhanden

### 3. Input-Flexibilität
```
[ ] Kann Dateien als Input verarbeiten
[ ] Kann Ordner als Input verarbeiten
[ ] Kann DB-Einträge als Input verarbeiten
```
**Kriterium:** Mindestens 2 von 3 erfüllt

### 4. Strukturierte Ausgabe
```
[ ] Output geht in DB-Tabelle
[ ] Oder: Output als strukturiertes JSON
[ ] Oder: Output als definiertes Dateiformat
```
**Kriterium:** Keine unstrukturierten Print-Ausgaben als Hauptoutput

### 5. dist_type Handling
```python
# Prüfen im Code:
grep -n "dist_type" <component_file>
```
**Kriterium:** dist_type wird bei Datenoperationen gesetzt
- 0 = System
- 1 = Template
- 2 = User

### 6. Idempotenz
```bash
# Test: Zweimal ausführen
bach <component> <input>
bach <component> <input>
# Ergebnis sollte identisch sein
```
**Kriterium:** Wiederholte Ausführung ändert nichts / keine Duplikate

### 7. Pfad-Handling
```python
# Prüfen im Code:
grep -n "C:\\\\Users" <component_file>
grep -n "hardcoded" <component_file>
# Sollte KEINE Treffer haben

# Stattdessen:
from bach_paths import BACH_ROOT, DATA_DIR
```
**Kriterium:** Alle Pfade über bach_paths.py oder relativ

## Bewertung

| Punkte | Status |
|--------|--------|
| 7/7    | ✅ Production-Ready |
| 5-6/7  | ⚠️ Mit Einschränkungen nutzbar |
| 3-4/7  | 🔧 Nacharbeit erforderlich |
| <3/7   | ❌ Nicht bereit für Integration |

## CLI-Befehl (geplant)

```bash
# Zukünftige Implementierung
bach validate agent <name>
bach validate service <name>
bach validate expert <name>

# Output:
# [✓] Unabhängigkeit: OK
# [✓] CLI-Integration: OK
# [!] Input-Flexibilität: Nur Dateien (2/3)
# [✓] Strukturierte Ausgabe: OK
# [✓] dist_type: OK
# [!] Idempotenz: Nicht getestet
# [✓] Pfad-Handling: OK
#
# Ergebnis: 5/7 - Mit Einschränkungen nutzbar
```

## Siehe auch
- `bach help skills` - Skills-System
- `bach help agents` - Agenten-Übersicht
- `bach help naming` - Namenskonventionen
- `skills/docs/docs/docs/help/practices.txt` - Best Practices