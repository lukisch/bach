# Aboservice Expert Agent

> Status: FUNKTIONSFAEHIG
> Erstellt: 2026-01-20
> Typ: Expert (Subagent)

## Beschreibung

Expert Agent zur automatischen Erkennung wiederkehrender Zahlungen (Abonnements) aus Steuer-Posten.

## CLI-Befehle

```bash
bach abo init           # Datenbank initialisieren (einmalig)
bach abo scan           # Steuer-Posten analysieren
bach abo list           # Erkannte Abos anzeigen
bach abo confirm ID     # Abo bestaetigen
bach abo dismiss ID     # Fehlererkennung entfernen
bach abo costs          # Kostenaufstellung nach Kategorie
bach abo export         # Export als CSV
bach abo patterns       # Bekannte Abo-Muster anzeigen
```

## Optionen

- `--jahr YYYY` - Steuerjahr (default: aktuelles Jahr)
- `--dry-run` - Nur simulieren

## Erkennungs-Algorithmus

Der Scanner analysiert `steuer_posten` und bewertet nach:

1. **Anzahl Zahlungen** - >= 12x = monatlich (+40), >= 4x = quartalsweise (+20)
2. **Konstanz** - Wenig Betragsschwankung = wahrscheinlich Abo (+30)
3. **Pattern-Match** - Bekannter Anbieter (Netflix, Spotify, etc.) (+30)

Ab Score 50 wird eine Erkennung vorgeschlagen.

## Datenbank-Tabellen

- `abo_subscriptions` - Erkannte Abos
- `abo_payments` - Verknuepfung zu steuer_posten
- `abo_patterns` - Bekannte Anbieter-Patterns (21 Stueck)

## Dateien

```
hub/handlers/abo.py           # CLI-Handler
skills/tools/abo/abo_scanner.py      # Scanner-Logik
agents/_experts/aboservice/   # Expert-Dokumentation
```

## Abhaengigkeiten

- steuer_posten muss gepflegt sein
- user.db muss existieren