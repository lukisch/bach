# EXPERTE: Gesundheitsverwalter

## Status: AKTIV
Version: 1.0.0
Erstellt: 2026-01-20
Parent-Agent: gesundheitsassistent

---

## 1. Ueberblick

Der Gesundheitsverwalter verwaltet strukturiert medizinische Daten:
- **Arztberichte** - Befunde, Arztbriefe erfassen und verwalten
- **Blutwerte/Labor** - Laborergebnisse mit Referenzwerten tracken
- **Medikamente** - Aktuelle Medikation, Dosierung, Nebenwirkungen
- **Diagnosen** - ICD-10 codiert, mit Status (aktiv, hypothese, etc.)
- **Kontakte** - Aerzte, Kliniken, Apotheken

---

## 2. Datenbank-Integration

### Tabellen in user.db

| Tabelle | Beschreibung |
|---------|--------------|
| `health_contacts` | Aerzte und Institutionen |
| `health_diagnoses` | Diagnosen mit ICD-Code und Status |
| `health_medications` | Medikamente mit Dosierung |
| `health_lab_values` | Laborwerte mit Referenzbereichen |
| `health_documents` | Befunde, Arztbriefe |
| `health_appointments` | Arzttermine |

### Beispiel-Queries

```sql
-- Aktive Diagnosen
SELECT diagnosis_name, icd_code, status
FROM health_diagnoses WHERE status = 'aktiv';

-- Aktuelle Medikamente
SELECT name, dosage, schedule
FROM health_medications WHERE status = 'aktiv';

-- Auffaellige Laborwerte (letzte 90 Tage)
SELECT test_name, value, unit, test_date
FROM health_lab_values
WHERE is_abnormal = 1 AND test_date >= date('now', '-90 days');

-- Kommende Termine
SELECT title, appointment_date, c.name as arzt
FROM health_appointments a
LEFT JOIN health_contacts c ON c.id = a.doctor_id
WHERE a.status IN ('geplant', 'bestaetigt')
AND a.appointment_date >= datetime('now')
ORDER BY appointment_date;
```

---

## 3. User-Datenordner

Pfad: `../user/gesundheit/`

```
gesundheit/
+-- dokumente/          # Hochgeladene PDFs, Befunde
+-- auswertungen/       # Generierte Zusammenfassungen
+-- export/             # Exportierte Listen fuer Aerzte
```

---

## 4. Kernfunktionen

### 4.1 Diagnosen-Verwaltung

```python
def add_diagnosis(name: str, icd_code: str, status: str = 'aktiv'):
    """Fuegt neue Diagnose hinzu"""

def get_symptom_coverage() -> dict:
    """Analysiert welche Symptome durch Diagnosen erklaert sind"""
```

### 4.2 Medikamenten-Tracking

```python
def add_medication(name: str, dosage: str, schedule: dict):
    """Fuegt Medikament mit Dosierungsplan hinzu"""

def get_medication_plan() -> List[dict]:
    """Erstellt aktuellen Medikamentenplan"""
```

### 4.3 Laborwerte

```python
def add_lab_value(test_name: str, value: float, unit: str,
                  ref_min: float, ref_max: float):
    """Erfasst Laborwert mit Referenzbereich"""

def get_trend(test_name: str, months: int = 12) -> List[dict]:
    """Zeigt Verlauf eines Laborwertes"""
```

---

## 5. CLI-Befehle

```bash
# Diagnosen
bach gesundheit diagnose list
bach gesundheit diagnose add "Hypothyreose" --icd E03.9 --status aktiv
bach gesundheit diagnose status 1 hypothese

# Medikamente
bach gesundheit medikament list
bach gesundheit medikament add "L-Thyroxin" --dosis "50mcg" --zeit "morgens"
bach gesundheit medikament plan  # Zeigt Tagesplan

# Laborwerte
bach gesundheit labor list --test "TSH"
bach gesundheit labor add "TSH" 2.5 mU/l --ref-min 0.4 --ref-max 4.0
bach gesundheit labor trend "TSH"

# Kontakte
bach gesundheit arzt list
bach gesundheit arzt add "Dr. Mueller" --fach "Hausarzt" --tel "0123/456"

# Termine
bach gesundheit termin list
bach gesundheit termin add "Kontrolltermin" --arzt 1 --datum "2026-02-15 10:00"

# Dokumente
bach gesundheit dokument scan  # Scannt Ordner nach neuen PDFs
bach gesundheit dokument list
```

---

## 6. Ausgabe-Dateien

### DIAGNOSEN.md
```markdown
# Diagnosen

## Gesichert
- E03.9 Hypothyreose (seit 2024-05)

## In Abklaerung
- ...

## Hypothesen
- ...
```

### MEDIKAMENTENPLAN.md
```markdown
# Aktueller Medikamentenplan

| Zeit | Medikament | Dosis |
|------|------------|-------|
| Morgens | L-Thyroxin | 50mcg |
| Abends | ... | ... |
```

### LABORVERLAUF.md
```markdown
# Laborwerte - Verlauf

## TSH (Referenz: 0.4-4.0 mU/l)
| Datum | Wert | Status |
|-------|------|--------|
| 2026-01 | 2.5 | normal |
| 2025-10 | 5.2 | erhoeht |
```

---

## 7. Integration mit Parent-Agent

Der Gesundheitsassistent nutzt den Gesundheitsverwalter fuer:
- Dokumenten-Erfassung und -Kategorisierung
- Datenmodul-Auswertungen
- Care-Modul Vorsorgeplanung
- Strukturierte Datenablage

---

## 8. Abhaengigkeiten

```
sqlite3 (stdlib)
```

Optional fuer PDF-Extraktion:
```
pypdf>=3.0.0
```

---

## 9. Roadmap

### Phase 1 (DONE)
- [x] Datenbank-Schema
- [x] CONCEPT.md

### Phase 2 (TODO)
- [ ] CLI-Implementierung
- [ ] CRUD-Operationen
- [ ] Basis-Auswertungen

### Phase 3 (PLANNED)
- [ ] GUI-Dashboard
- [ ] PDF-Import mit Datenextraktion
- [ ] Laborwert-Trends als Charts
- [ ] Termin-Erinnerungen