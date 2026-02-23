---
name: cv-generierung
version: 1.0.0
type: workflow
author: BACH Team
created: 2026-02-04
updated: 2026-02-04
anthropic_compatible: true
description: >
  Workflow zur Generierung eines ASCII-Lebenslaufs aus BACH-Daten
  und Ordnerstruktur. Dokumente scannen -> CV-Daten extrahieren -> ASCII-Output.
---

# CV-GENERIERUNG WORKFLOW

> Dokumente scannen -> CV-Daten extrahieren -> ASCII-Output

## VORAUSSETZUNGEN

- [ ] Persoenliche Daten in assistant_user_profile eingetragen
- [ ] Karriere-Ordner in user_data_folders registriert
- [ ] Dokumente in erwarteter Ordnerstruktur abgelegt

## SCHRITT 1: ORDNER REGISTRIEREN

Falls noch nicht geschehen, Ordner in der DB registrieren:

```bash
bach --db query "INSERT INTO user_data_folders (folder_path, folder_type, description) VALUES ('PFAD', 'career', 'Arbeitgeber')"
```

Oder direkt in SQLite:

```sql
INSERT INTO user_data_folders (folder_path, folder_type) VALUES
  ('/pfad/zu/_Arbeitgeber', 'career'),
  ('/pfad/zu/_Abschluesse', 'education'),
  ('/pfad/zu/_Fortbildungen', 'certifications');
```

## SCHRITT 2: PERSOENLICHE DATEN EINTRAGEN

```sql
INSERT INTO assistant_user_profile (key, value) VALUES
  ('name', 'Max Mustermann'),
  ('email', 'max@example.com'),
  ('phone', '+49 123 456789'),
  ('address', 'Musterstrasse 1, 12345 Musterstadt'),
  ('birthday', '1990-01-15'),
  ('nationality', 'deutsch');
```

## SCHRITT 3: CV GENERIEREN

```bash
cd system
python agents/_experts/bewerbungsexperte/cv_generator.py --scan-folders
```

Bei manuellem Pfad:

```bash
python agents/_experts/bewerbungsexperte/cv_generator.py \
  --career-path "D:/Dokumente/_Arbeitgeber" \
  --education-path "D:/Dokumente/_Abschluesse" \
  --certs-path "D:/Dokumente/_Fortbildungen"
```

## SCHRITT 4: AUSGABE PRUEFEN

Der Generator zeigt:
- Anzahl gefundener Sektionen
- Persoenliche Daten
- Berufserfahrung mit Dokumenten
- Ausbildung mit Zeugnissen
- Fortbildungen/Zertifikate
- Referenzen

## SCHRITT 5: IN DATEI SPEICHERN

```bash
python agents/_experts/bewerbungsexperte/cv_generator.py \
  --scan-folders \
  --output ../user/bewerbung/lebenslauf.txt
```

## ERWARTETE ORDNERSTRUKTUR

```
_Arbeitgeber/
  Firma_A_2020-2023/
    Arbeitsvertrag.pdf
    Arbeitszeugnis.pdf
    Bescheinigung_xyz.pdf
  Firma_B_2018-2020/
    ...

_Abschluesse/
  01_Universitaet/
    Bachelor_Zeugnis.pdf
  02_Berufsausbildung/
    Ausbildungszeugnis.pdf

_Fortbildungen/
  Zertifikat_AWS_2024.pdf
  Seminar_Fuehrung_2023.pdf
```

## FEHLERBEHEBUNG

### Keine Daten gefunden
- Pruefen: `bach --db query "SELECT * FROM user_data_folders"`
- Pruefen: Ordnerpfade korrekt und existierend?

### Persoenliche Daten leer
- Pruefen: `bach --db query "SELECT * FROM assistant_user_profile"`
- Eintragen mit INSERT-Statement oben

### Falsches Encoding
- Windows: `python -X utf8 cv_generator.py ...`
- Ausgabedatei mit UTF-8 oeffnen

## NACHBEARBEITUNG

1. Generiertes CV pruefen
2. Fehlende Informationen manuell ergaenzen
3. Formatierung ggf. anpassen
4. Fuer spezifische Stelle: Keywords hinzufuegen

---
Letzte Aktualisierung: 2026-02-04
