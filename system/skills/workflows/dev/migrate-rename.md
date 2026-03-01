# Workflow: Datei-Umbenennung mit Wrapper (Evolutionaere Migration)

**Version:** 1.0.0
**Erstellt:** 2026-01-24
**Kategorie:** System-Wartung

---

## Zweck

Dieses Verfahren ermoeglicht Datei-Umbenennungen OHNE harte Brueche.
Statt alle Verweise auf einmal zu korrigieren, werden sie organisch
durch die taegliche Nutzung aktualisiert.

---

## Prinzip: Evolutionaere Migration

```
VORHER:                          NACHHER:
alte_datei.md                    neue_datei.md (umbenannt)
   |                                |
   +-- Verweis A                    +-- alte_datei.md (Wrapper)
   +-- Verweis B                           |
   +-- Verweis C                           +-- Log-Tabelle
                                           +-- Anleitung
                                           +-- Link zu neue_datei.md
```

Wer den alten Pfad aufruft:
1. Landet bei der Wrapper-Datei
2. Traegt sich ins Log ein
3. Korrigiert den Verweis der ihn herschickte
4. Geht zur eigentlichen Datei

---

## Schritt-fuer-Schritt

### 1. Datei umbenennen

```bash
mv alte_datei.md neue_datei.md
```

### 2. Wrapper-Datei erstellen

Erstelle `alte_datei.md` mit folgendem Inhalt:

```markdown
# ALTE_DATEI.md - UMGELEITET

**Status:** Diese Datei wurde umbenannt zu `neue_datei.md`

---

## Migration-Log

Wenn du diese Datei liest, hinterlasse einen Eintrag:

| Datum | Wer | Herkunft | Verweis korrigiert? |
|-------|-----|----------|---------------------|
| YYYY-MM-DD | [Name] | Initiale Migration | n/a (Wrapper erstellt) |
| | | | |

---

## Anleitung fuer KI-Partner

1. **Log-Eintrag hinterlassen** (oben in Tabelle)
2. **Herkunft pruefen**: Was hat dich hierher geschickt?
3. **Verweis korrigieren**: Aendere `alte_datei.md` → `neue_datei.md`
4. **Zur eigentlichen Datei gehen**: [neue_datei.md](neue_datei.md)

---

**Zieldatei:** [neue_datei.md](neue_datei.md)
```

### 3. Kritische Verweise sofort korrigieren

Einige Verweise sollten SOFORT korrigiert werden:
- Help-Dateien (primaere Dokumentation)
- System-Prompt Referenzen
- CLI-Code der den Pfad direkt verwendet

### 4. Uebrige Verweise evolutionaer migrieren

Der Rest wird automatisch korrigiert wenn:
- Ein Partner die Wrapper-Datei findet
- Der Path Healer (`bach --maintain heal`) laeuft
- Die Datei manuell gefunden wird

---

## Wann Wrapper-Methode verwenden?

**JA - Wrapper sinnvoll:**
- Viele potenzielle Verweise
- Datei wird von verschiedenen Partnern/Tools referenziert
- Keine kritische System-Datei

**NEIN - Direkt alle aendern:**
- Wenige, bekannte Verweise
- Kritische System-Dateien (config, DB-Schema)
- Performance-kritische Pfade

---

## Beispiel: ROADMAP_ADVANCED.md → ROADMAP.md

Durchgefuehrt 2026-01-24:

1. `mv ROADMAP_ADVANCED.md ROADMAP.md`
2. Wrapper erstellt mit Log-Tabelle
3. Help-Dateien sofort korrigiert
4. Uebrige 20+ Verweise werden evolutionaer migriert

---

## Cleanup

Nach ca. 30 Tagen oder wenn Log zeigt dass keine neuen Eintraege:
1. Wrapper-Datei nach `_archive/deprecated/` verschieben
2. Oder komplett loeschen (wenn keine Eintraege mehr)

---

## Siehe auch

- `skills/docs/docs/docs/docs/help/migrate.txt` - CLI-Dokumentation
- `bach --maintain heal` - Automatische Pfadkorrektur
- `skills/docs/docs/docs/docs/help/practices.txt` - Architekturprinzip #3: Evolutionaere Migration