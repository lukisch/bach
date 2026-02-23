# EXPERTE: Haushaltsmanagement

## Status: AKTIV
Version: 1.0.0
Erstellt: 2026-01-20
Parent-Agent: persoenlicher-assistent

---

## 1. Ueberblick

Der Haushaltsmanagement-Experte unterstuetzt bei der Organisation des Alltags:
- **Haushaltsbuch** - Einnahmen und Ausgaben tracken
- **Lagerbestaende** - Medikamente, Hygieneartikel, wichtige Vorraete
- **Einkaufslisten** - Automatisch aus Bestaenden generieren
- **Haushaltsplaene** - Putzplaene, Routinen, wiederkehrende Aufgaben
- **Bestellungen** - Online-Bestellungen tracken

---

## 2. Datenbank-Integration

### Tabellen in user.db

| Tabelle | Beschreibung |
|---------|--------------|
| `household_inventory` | Lagerbestaende mit Mindestmengen |
| `household_shopping_lists` | Einkaufslisten |
| `household_shopping_items` | Items pro Liste |
| `household_finances` | Haushaltsbuch |
| `household_routines` | Wiederkehrende Aufgaben |

### Beispiel-Queries

```sql
-- Artikel mit niedrigem Bestand
SELECT * FROM household_inventory
WHERE quantity <= min_quantity;

-- Monatliche Ausgaben nach Kategorie
SELECT category, SUM(amount) as total
FROM household_finances
WHERE entry_type = 'ausgabe'
AND entry_date >= date('now', 'start of month')
GROUP BY category;

-- Ueberfaellige Routinen
SELECT * FROM household_routines
WHERE is_active = 1 AND next_due <= datetime('now');
```

---

## 3. User-Datenordner

Pfad: `../user/persoenlicher_assistent/haushalt/`

```
haushalt/
+-- inventar/           # Export-Listen, Bestandsberichte
+-- finanzen/           # Monatsberichte, Jahresuebersichten
+-- plaene/             # Putzplaene, Wochenplaene
+-- belege/             # Gescannte Kassenbons (optional)
```

---

## 4. Kernfunktionen

### 4.1 Bestandsverwaltung

```python
# Bestand aktualisieren
def update_inventory(item_name: str, quantity: int):
    """Aktualisiert Bestand und prueft Mindestmenge"""

# Einkaufsliste aus Bestaenden generieren
def generate_shopping_list() -> List[dict]:
    """Erstellt Liste aus allen Artikeln unter Mindestmenge"""
```

### 4.2 Haushaltsbuch

```python
# Ausgabe erfassen
def add_expense(amount: float, category: str, description: str):
    """Erfasst Ausgabe im Haushaltsbuch"""

# Monatsreport
def monthly_report(year: int, month: int) -> dict:
    """Erstellt Monatsueberblick"""
```

### 4.3 Routinen

```python
# Routine als erledigt markieren
def complete_routine(routine_id: int):
    """Markiert Routine und berechnet naechsten Termin"""
```

---

## 5. CLI-Befehle

```bash
# Inventar
bach haushalt inventar list
bach haushalt inventar add "Klopapier" --quantity 24 --min 6
bach haushalt inventar update "Klopapier" --quantity 12

# Einkaufsliste
bach haushalt liste show
bach haushalt liste add "Milch" --quantity 2
bach haushalt liste generate  # Aus niedrigen Bestaenden

# Finanzen
bach haushalt ausgabe 45.99 --kategorie "Lebensmittel" --beschreibung "Wocheneinkauf"
bach haushalt report --monat 1 --jahr 2026

# Routinen
bach haushalt routine list
bach haushalt routine done "Waesche waschen"
```

---

## 6. Integration mit Parent-Agent

Der Persoenliche Assistent kann:
- Einkaufslisten beim Morgenbriefing erwaehnen
- Niedrige Bestaende proaktiv melden
- Routinen in den Tagesplan integrieren
- Finanzuebersichten bei Bedarf erstellen

---

## 7. Kategorien

### Inventar-Kategorien
- Medikamente
- Hygiene
- Reinigung
- Lebensmittel (haltbar)
- Buero
- Technik

### Ausgaben-Kategorien
- Lebensmittel
- Haushalt
- Gesundheit
- Transport
- Freizeit
- Abos
- Sonstiges

---

## 8. Abhaengigkeiten

```
sqlite3 (stdlib)
```

Keine externen Dependencies erforderlich.

---

## 9. Roadmap

### Phase 1 (DONE)
- [x] Datenbank-Schema
- [x] CONCEPT.md

### Phase 2 (TODO)
- [ ] CLI-Implementierung
- [ ] Basis-CRUD-Operationen
- [ ] Einkaufslisten-Generator

### Phase 3 (PLANNED)
- [ ] GUI-Integration
- [ ] Automatische Bestandswarnungen
- [ ] Kassenbon-Scanner (OCR)