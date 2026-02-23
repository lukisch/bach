# EXPERTE: Data Analysis

## Status: ENTWURF
Version: 0.1.0
Erstellt: 2026-01-21
Parent-Agent: -

---

## 1. Ueberblick

Der Data Analysis Expert bietet strukturierte Datenanalyse-Faehigkeiten:
- **CSV/Excel Import** - Dateien laden und inspizieren
- **Statistik** - Deskriptive Statistik, Korrelationen
- **Transformation** - Filter, Gruppierung, Pivot
- **Visualisierung** - Charts als PNG/SVG generieren
- **Export** - Aufbereitete Daten speichern

**SKILL_ANALYSE Koeffizient:** 20% -> Ziel 60%

---

## 2. Kernfunktionen

### 2.1 Daten laden

```python
def load_data(path: str, format: str = 'auto') -> DataFrame:
    """Laedt CSV, Excel, JSON in DataFrame"""
    
def inspect_data(df: DataFrame) -> dict:
    """Gibt Spalten, Typen, Nullwerte, Zeilen zurueck"""
```

### 2.2 Deskriptive Statistik

```python
def describe(df: DataFrame, columns: list = None) -> dict:
    """Mean, Median, Std, Min, Max pro Spalte"""
    
def correlations(df: DataFrame) -> DataFrame:
    """Korrelationsmatrix numerischer Spalten"""
```

### 2.3 Transformation

```python
def filter_rows(df: DataFrame, condition: str) -> DataFrame:
    """Filtert Zeilen nach Bedingung"""
    
def group_by(df: DataFrame, by: list, agg: dict) -> DataFrame:
    """Gruppiert und aggregiert"""

def pivot(df: DataFrame, index: str, columns: str, values: str) -> DataFrame:
    """Erstellt Pivot-Tabelle"""
```

### 2.4 Visualisierung

```python
def create_chart(df: DataFrame, chart_type: str, 
                 x: str, y: str, output: str) -> str:
    """Erstellt Chart und speichert als PNG"""
    # chart_type: bar, line, scatter, pie, heatmap

def save_chart(fig, path: str, format: str = 'png') -> str:
    """Speichert Figure in Datei"""
```

---

## 3. CLI-Befehle (geplant)

```bash
# Daten laden und inspizieren
bach data load "data.csv"
bach data inspect "data.csv"
bach data head "data.csv" --rows 10

# Statistik
bach data describe "data.csv"
bach data corr "data.csv"

# Filter und Transformation
bach data filter "data.csv" "age > 30" --output "filtered.csv"
bach data groupby "data.csv" --by category --agg "sum:amount,count:id"

# Visualisierung
bach data chart "data.csv" --type bar --x category --y amount --output "chart.png"
bach data chart "data.csv" --type line --x date --y value --output "trend.png"
```

---

## 4. User-Datenordner

Pfad: `../user/data-analysis/`

```
data-analysis/
+-- input/          # Hochgeladene Dateien
+-- output/         # Transformierte Dateien
+-- charts/         # Generierte Visualisierungen
+-- reports/        # Analyse-Berichte
```

---

## 5. Abhaengigkeiten

```
pandas>=2.0.0
openpyxl>=3.0.0     # Excel-Support
matplotlib>=3.5.0   # Charts
seaborn>=0.12.0     # Erweiterte Charts (optional)
```

---

## 6. Roadmap

### Phase 1: Basis (aktuell)
- [x] CONCEPT.md erstellt
- [x] Verzeichnisstruktur angelegt (../user/data-analysis/input|output|charts)
- [x] CLI-Handler data_analysis.py (v1.0.0)
- [x] load, describe, head, corr, list Befehle

### Phase 2: Analyse
- [ ] Korrelationsanalyse
- [ ] Filter und Gruppierung
- [ ] Pivot-Tabellen

### Phase 3: Visualisierung
- [ ] Bar/Line Charts
- [ ] Scatter/Heatmap
- [ ] Export-Optionen

### Phase 4: Integration
- [ ] CLI-Befehle implementieren
- [ ] In andere Agenten integrieren (Steuer, Gesundheit)
- [ ] Automatische Reports

---

## 7. Anwendungsfaelle

### 7.1 Finanzanalyse
```bash
bach data load "kontoauszug.csv"
bach data groupby --by kategorie --agg "sum:betrag"
bach data chart --type pie --x kategorie --y betrag
```

### 7.2 Gesundheitsdaten
```bash
bach data load "blutwerte.csv"
bach data chart --type line --x datum --y tsh_wert
```

### 7.3 Projekt-Metriken
```bash
bach data load "tasks.csv"
bach data describe  # Bearbeitungszeiten
bach data groupby --by status --agg "count:id"
```

---

## 8. Notizen zur Implementierung

**Prioritaet 1:** CSV-Import + describe() 
- Einfachster Quick-Win
- Nutzt bestehende Pandas-Installation

**Prioritaet 2:** Einfache Charts (bar, line)
- Matplotlib ist ueberall verfuegbar
- Speichern als PNG im charts/ Ordner

**Spaeter:** Integration mit anderen BACH-Komponenten
- Steuer: Ausgaben-Analyse
- Gesundheit: Labor-Trends
- ATI: Code-Metriken