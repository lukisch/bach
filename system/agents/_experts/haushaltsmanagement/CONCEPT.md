# EXPERTE: Haushaltsmanagement

## Status: AKTIV
Version: 2.0.0
Erstellt: 2026-01-20
Aktualisiert: 2026-03-01 (INT02: HausLagerist V4 Integration)
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

### Tabellen in bach.db

| Tabelle | Beschreibung |
|---------|--------------|
| `household_inventory` | Lagerbestaende mit Pull-Einstellungen (priority, pull_threshold, learning_alpha) |
| `household_orders` | Bedarfs-Orders (routine, period, oneshot, project) |
| `household_suppliers` | Lieferanten (Supermarkt, Drogerie, Online) |
| `household_stock_transactions` | Bestandsbuchungen (Eingang, Verbrauch) |
| `household_shopping_lists` | Einkaufslisten |
| `household_shopping_items` | Items pro Liste |
| `household_finances` | Haushaltsbuch |
| `household_routines` | Wiederkehrende Aufgaben |

### Pull-System (HausLagerist V4)

Das Vorratsmanagement basiert auf dem **Pull-Quotient-Verfahren**:

- **Pull-Quotient:** Q = Bestand / (Tagesbedarf * Planungstage)
- **Dringlichkeit:** D = (Prioritaet / min(Q, 10)) * max(0, 1 - Q)
- **Ampel:** ROT (leer+Bedarf), GELB (<7 Tage), GRUEN (OK), GRAU (kein Bedarf)
- **Exponentielles Glaetten:** V_new = alpha * V_gemessen + (1-alpha) * V_alt

### Beispiel-Queries

```sql
-- Pull-Kandidaten (Bestand unter Bedarf)
SELECT i.name, i.quantity, i.min_quantity, i.priority,
       o.quantity_value / o.cycle_interval_days as daily_demand
FROM household_inventory i
JOIN household_orders o ON o.article_id = i.id
WHERE o.status = 'active' AND o.order_type = 'routine'
AND i.quantity < (o.quantity_value / o.cycle_interval_days * 7);

-- Letzte Bestandsbewegungen
SELECT i.name, t.transaction_type, t.amount, t.stock_after, t.timestamp
FROM household_stock_transactions t
JOIN household_inventory i ON i.id = t.article_id
ORDER BY t.timestamp DESC LIMIT 10;

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
# Uebersicht
bach haushalt status             # Dashboard mit Ampel
bach haushalt today              # Was steht heute an?
bach haushalt due 14             # Faellige Aufgaben

# Vorratsmanagement (Pull-System)
bach haushalt inventory          # Bestand mit Ampelfarben
bach haushalt add-item "Milch" --cat Lebensmittel --unit Liter --min 2
bach haushalt stock-in 1 6 --price 1.29   # Eingang buchen
bach haushalt stock-out 1 2               # Verbrauch buchen
bach haushalt pull-check         # Automatische Einkaufsliste
bach haushalt ampel              # ROT/GELB/GRUEN Uebersicht
bach haushalt order 1 --type routine --qty 6 --cycle 14

# Lieferanten
bach haushalt supplier           # Alle Lieferanten
bach haushalt add-supplier "REWE" --type supermarket

# Einkaufsliste (manuell)
bach haushalt shopping
bach haushalt add-shopping "Milch" --cat Lebensmittel

# Finanzen
bach haushalt costs              # Fixkosten-Uebersicht
bach haushalt kosten-monat 3     # Irregulare Kosten Maerz
bach haushalt insurance-check    # Versicherungs-Check
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

### Phase 2 (DONE — INT02, v3.3.0)
- [x] Pull-basiertes Vorratsmanagement (HausLagerist V4 Port)
- [x] 9 neue CLI-Operationen (inventory, stock-in/out, pull-check, ampel, order, supplier)
- [x] Inventory Engine (Pull-Quotient, Dringlichkeit, Exponentielles Glaetten)
- [x] DB-Migration 025 (household_orders, household_suppliers, household_stock_transactions)

### Phase 3 (PLANNED)
- [ ] GUI-Integration
- [ ] Automatische Bestandswarnungen (Proaktive Meldungen)
- [ ] Kassenbon-Scanner (OCR)
- [ ] Intelligence: Auto-Routine-Vorschlaege basierend auf Verbrauchshistorie