# KONZEPT: Aboservice Expert Agent

## Status: GEPLANT (nicht umgesetzt)
Erstellt: 2026-01-18

---

## 1. Idee

Ein Expert Agent der Steuerdaten analysiert um aktive Abonnements zu identifizieren.
Zeigt monatliche Kosten und ermoeglicht einfache Kuendigung.

---

## 2. Datenquellen

### Primaer: steuer_posten (user.db)

```sql
-- Wiederkehrende Zahlungen identifizieren
SELECT
    rechnungssteller,
    COUNT(*) as anzahl,
    AVG(brutto) as durchschnitt,
    SUM(brutto) as gesamt
FROM steuer_posten
WHERE steuerjahr = 2025
GROUP BY rechnungssteller
HAVING anzahl >= 3  -- Mind. 3x = wahrscheinlich Abo
ORDER BY gesamt DESC;
```

### Bekannte Abo-Anbieter (Pattern-Matching)

| Anbieter | Kategorie | Kuendigungslink |
|----------|-----------|-----------------|
| Netflix | Streaming | netflix.com/cancelplan |
| Spotify | Musik | spotify.com/account |
| Microsoft 365 | Software | account.microsoft.com/services |
| Adobe | Software | account.adobe.com |
| Amazon Prime | Shopping | amazon.de/prime |
| Disney+ | Streaming | disneyplus.com/account |
| Apple One | Service | appleid.apple.com |
| YouTube Premium | Streaming | youtube.com/paid_memberships |
| Dropbox | Cloud | dropbox.com/account |
| iCloud | Cloud | appleid.apple.com |

---

## 3. Architektur

### Neue Tabellen (user.db)

```sql
-- Abo-Definitionen
CREATE TABLE abo_subscriptions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,           -- "Netflix Standard"
    anbieter TEXT NOT NULL,       -- "Netflix"
    kategorie TEXT,               -- "Streaming"
    betrag_monatlich REAL,        -- 12.99
    zahlungsintervall TEXT,       -- "monatlich", "jaehrlich"
    kuendigungslink TEXT,         -- URL
    erkannt_am TEXT,              -- Automatische Erkennung
    bestaetigt INTEGER DEFAULT 0, -- Manuell bestaetigt
    aktiv INTEGER DEFAULT 1,
    created_at TEXT,
    updated_at TEXT
);

-- Abo-Zahlungen (Verknuepfung zu steuer_posten)
CREATE TABLE abo_payments (
    id INTEGER PRIMARY KEY,
    subscription_id INTEGER REFERENCES abo_subscriptions(id),
    posten_id INTEGER REFERENCES steuer_posten(id),
    betrag REAL,
    datum TEXT,
    created_at TEXT
);

-- Bekannte Anbieter-Patterns
CREATE TABLE abo_patterns (
    id INTEGER PRIMARY KEY,
    pattern TEXT NOT NULL,        -- Regex oder LIKE Pattern
    anbieter TEXT NOT NULL,
    kategorie TEXT,
    kuendigungslink TEXT,
    dist_type INTEGER DEFAULT 2   -- CORE = mitgeliefert
);
```

### CLI-Befehle

```bash
bach abo scan           # Analysiert steuer_posten, erkennt Abos
bach abo list           # Zeigt alle erkannten Abos
bach abo confirm 1      # Bestaetigt Abo-Erkennung
bach abo dismiss 2      # Entfernt Fehlererkennung
bach abo costs          # Monatliche Kostenaufstellung
bach abo export         # Export fuer Haushaltsplanung
```

### GUI-Dashboard (/abo)

```
+------------------------------------------------------------------+
| ABOSERVICE - Deine aktiven Abonnements                           |
+------------------------------------------------------------------+
| Monatliche Kosten: 78,45 EUR                                     |
| Jaehrliche Kosten: 941,40 EUR                                    |
+------------------------------------------------------------------+

+------------------+----------+----------+--------+----------------+
| Anbieter         | Kategorie| Betrag   | Letzte | Aktion         |
+------------------+----------+----------+--------+----------------+
| Netflix          | Stream   | 12,99/Mo | Jan 18 | [Kuendigen]    |
| Spotify Family   | Musik    | 17,99/Mo | Jan 15 | [Kuendigen]    |
| Microsoft 365    | Software | 7,00/Mo  | Jan 10 | [Kuendigen]    |
| Disney+          | Stream   | 8,99/Mo  | Jan 05 | [Kuendigen]    |
| iCloud 200GB     | Cloud    | 2,99/Mo  | Jan 01 | [Kuendigen]    |
+------------------+----------+----------+--------+----------------+

+------------------------------------------------------------------+
| UNBESTAETIGTE ERKENNUNGEN                                         |
+------------------------------------------------------------------+
| ? Amazon (12x Zahlungen, 156 EUR) - Abo oder Einzelkaeufe?       |
|   [Ja, ist Abo]  [Nein, Einzelkaeufe]                            |
+------------------------------------------------------------------+
```

---

## 4. Erkennungs-Algorithmus

```python
def detect_subscriptions(username: str, steuerjahr: int):
    """Erkennt potenzielle Abos aus steuer_posten."""

    # 1. Gruppiere nach Rechnungssteller
    groups = db.execute("""
        SELECT rechnungssteller,
               COUNT(*) as cnt,
               AVG(brutto) as avg_betrag,
               MIN(datum) as erste,
               MAX(datum) as letzte
        FROM steuer_posten
        WHERE username = ? AND steuerjahr = ?
        GROUP BY rechnungssteller
    """)

    for group in groups:
        score = 0

        # 2. Heuristiken anwenden
        if group.cnt >= 12:  # Monatlich
            score += 50
        elif group.cnt >= 4:  # Quartalsweise
            score += 30

        # Konstanter Betrag?
        stddev = calculate_stddev(group.rechnungssteller)
        if stddev < 1.0:  # Wenig Varianz
            score += 30

        # Bekanntes Pattern?
        if matches_known_pattern(group.rechnungssteller):
            score += 40

        # 3. Bei Score > 60: Als Abo vorschlagen
        if score > 60:
            create_subscription_suggestion(group)
```

---

## 5. Implementierungsplan

### Phase 1: Grundstruktur
- [ ] Tabellen in user.db erstellen
- [ ] abo_patterns mit Basiswerten fuellen
- [ ] CLI-Handler `hub/handlers/abo.py`
- [ ] Erkennungs-Algorithmus implementieren

### Phase 2: CLI
- [ ] `bach abo scan` - Erkennung starten
- [ ] `bach abo list` - Abos anzeigen
- [ ] `bach abo confirm/dismiss` - Bestaetigung

### Phase 3: GUI
- [ ] Route `/abo` in server.py
- [ ] Template `templates/abo.html`
- [ ] API-Endpunkte `/api/abo/*`
- [ ] Kuendigungslinks als externe Links

### Phase 4: Erweiterungen
- [ ] Benachrichtigung bei neuen Erkennungen
- [ ] Export als CSV/PDF
- [ ] Integration in Startup-Protokoll
- [ ] Jaehrliche Kostenprognose

---

## 6. Dateien (geplant)

```
hub/handlers/abo.py           CLI-Handler
skills/tools/abo/abo_scanner.py      Erkennungs-Logik
gui/templates/abo.html        Dashboard-Template
skills/docs/docs/docs/help/abo.txt                  Hilfe-Dokumentation
data/abo_patterns.json        Bekannte Abo-Anbieter
```

---

## 7. Abhaengigkeiten

- steuer_posten muss gepflegt sein
- GUI-Server muss laufen fuer Dashboard
- Keine externen APIs noetig (offline-faehig)

---

## 8. Offene Fragen

1. Sollen Kuendigungslinks direkt oeffnen oder nur anzeigen?
2. Integration mit Haushaltsbudget-Tools?
3. Benachrichtigungen bei Preiserhoehungen?
4. Historische Daten (mehrere Steuerjahre)?