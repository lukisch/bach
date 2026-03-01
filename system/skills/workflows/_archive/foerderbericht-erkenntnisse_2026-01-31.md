# Förderbericht-Workflow: Erkenntnisse & Verbesserungen

**Stand:** 2026-01-31
**Basierend auf:** Erster Praxistest mit echter Akte

---

## 1. Probleme beim ersten Durchlauf

### 1.1 Word-Template
- [ ] Neue Platzhalter wurden nicht erkannt/ausgefüllt
- [ ] Tabelle (Förderziele) wurde nicht befüllt
- [ ] Checkboxen nicht bearbeitet
- **TODO:** Template-Parser verbessern, Tabellen-Logik implementieren

### 1.2 Anonymisierung
- [ ] Sachbearbeiter wurde anonymisiert, aber NICHT de-anonymisiert
- [ ] Sachbearbeiter sollte NICHT anonymisiert werden (sind Amtspersonen)
- **TODO:** Whitelist für Amtspersonen/Sachbearbeiter

### 1.3 Fehlende Formate
- [ ] Mail-Dateien (.msg, .eml) werden nicht unterstützt
- **TODO:** Mail-Extraktion implementieren (wichtig für Elternarbeit, Umfeldarbeit, Bewilligungen)

---

## 2. Dokumenten-Korset (Zwei-Stufen-Modell)

### 📋 CORE (Stufe 1) - IMMER an LLM senden

| Dokumentart | Typische Namen | Welches nehmen? | Extrahierbare Daten |
|-------------|----------------|-----------------|---------------------|
| **Protokolle** | `Protokolle Einzel_XY.docx`, `[Name].docx` | Aus Bewilligungszeitraum (meist im `/root` oder `/Dokumentation`) | **Beobachtungen, Ist-Stand**, konkrete Fortschritte |
| **Aktendeckblatt** | `Aktendeckblatt.doc`, `Anmeldung.pdf` | Das eine vorhandene | Name, Geburtsdatum, Förderungsbeginn bei proAutismus |
| **Hilfeplan** | `Hilfeplan_2024.pdf`, `Kostenzusage*.pdf`, `Bewilligung*.pdf` | **Aktuellsten!** | **ZIELE übernehmen!**, Sachbearbeiter, Landkreis, Aktenzeichen |
| **Letzter proAutismus-Bericht** | `Entwicklungsbericht_2024.docx`, `ICF-Bericht_*.docx` | Nur **aktuellsten** | Kontinuität, frühere Ziele/Ist-Stände |

### 📄 STUFE 2 - Ebenfalls mitsenden (nach CORE im Dokument)

| Dokumentart | Typische Namen | Welches nehmen? | Extrahierbare Daten |
|-------------|----------------|-----------------|---------------------|
| **Mails** | `*.msg`, `*.eml` | Aus aktuellem Berichtszeitraum (~1 Jahr) | Elternarbeit, Umfeldarbeit, Amt-Kommunikation |
| **Aktuellster Arztbericht** | `Bericht_Dr_*.pdf`, `Entlassbericht_*.pdf` | Nur **aktuellsten** | Diagnosen (ICD-Code, Diagnostiker, Datum) |
| **Aktuellster Schulbericht** | `Schulbericht_*.pdf`, `SB_Bericht_*.docx` | Nur **letzten** | Schulkontext, Verhalten, Nachteilsausgleich |

### 🗄️ EXTENDED - Eigene Datei, nur bei User-Anfrage

| Dokumentart | Inhalt |
|-------------|--------|
| Ältere Mails | Vor dem Berichtszeitraum |
| Ältere Arztberichte | Diagnose-Historie |
| Ältere Schulberichte | Historischer Schulkontext |
| Alte proAutismus-Berichte | Verlaufsdokumentation |
| Archiv-Material | Selten relevant |

### 📦 Bundle-Struktur

```
CORE + STUFE 2 → Ein anonymisiertes Dokument
                 CORE-Dateien am Anfang
                 STUFE 2 danach

EXTENDED      → Separate Text-Datei
                Nur bei Bedarf/User-Anfrage einbeziehen
```

### 🎯 Ziel-Logik

```
┌─────────────────────────────────────────────────────────────┐
│  IDEALFALL: Aktueller Hilfeplan vorhanden                   │
│  ─────────────────────────────────────────────────────────  │
│  1. Ziele aus aktuellem Hilfeplan übernehmen                │
│  2. Beobachtungen aus Protokollen den Zielen zuordnen       │
│  3. Zielerreichung bewerten (1/2/3)                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  FALLBACK: Kein aktueller Hilfeplan                         │
│  ─────────────────────────────────────────────────────────  │
│  1. Aus Protokollen EX POST ableiten was gearbeitet wurde   │
│  2. Daraus plausible Ziele formulieren (wie bei Leon)       │
│  3. Beobachtungen eintragen                                 │
└─────────────────────────────────────────────────────────────┘
```

### 📁 Ordner-Zuordnung

| Ordner | Erwarteter Inhalt | Stufe |
|--------|-------------------|-------|
| `/root` | Aktuelle Protokolle | CORE |
| `/Anmeldeunterlagen` | Aktendeckblatt | CORE |
| `/Dokumentation`, `/Protokolle` | Protokolle im Zeitraum | CORE |
| `/Hilfeplan&Amt` | Hilfepläne, Kostenzusagen | CORE (aktuellster) |
| `/Berichte/intern` | proAutismus-Berichte | CORE (aktuellster) |
| `/Familie&Umfeld` | Mails, Elterngespräche | STUFE 2 (im Zeitraum) |
| `/Berichte/extern` | Arzt/Schule | STUFE 2 (aktuellste) |
| Rest | Historisches | EXTENDED |

---

## 3. Sachbearbeiter-Handling

### Zwei Typen beim Amt:
1. **Wirtschaftliche Jugendhilfe** - Kostenzusagen, Bewilligungen
2. **ASD/Pädagogisch** - Hilfepläne, Fallführung

### Regel:
- Sachbearbeiter-Namen NICHT anonymisieren
- Im Profil als `whitelist` führen
- Bei Bericht: Empfänger = pädagogischer Sachbearbeiter

---

## 4. Technische TODOs

### Erledigt (2026-01-31):
- [x] Platzhalter erweitert: `{{Weiterbewilligung oder Beendigung}}`, `{{Empfehlung}}`, `{{AKTUELLE_ENTWICKLUNGEN}}`, `{{BEDINGUNGSMODELL}}`
- [x] Empfehlungs-Checkboxen implementiert (Verlängerung/Beendigung + Gründe)
- [x] Anonymizer: `whitelist` Parameter für create_profile() hinzugefügt
- [x] word_template_service.py: `fill_table_rows()` und `fill_foerderziele_table()` Methoden
- [x] ICF-Tabelle: Neue Platzhalter-Methode implementiert (siehe unten)
- [x] Landkreis-Adresse: Automatische Ermittlung aus `landkreis` Feld (Lörrach/Waldshut)
- [x] Diagnosen: Erweitertes Format mit Diagnostiker, Datum, Quelle
- [x] Mail-Extraktion (.msg, .eml) - `extract_text_from_msg()`, `extract_text_from_eml()`

### Kurzfristig:
- [ ] Dokumenten-Collector mit CORE/STUFE2/EXTENDED Kategorisierung
- [ ] PDF-OCR-Integration (nutze existierendes `skills/tools/c_ocr_engine.py`)
- [ ] Anonymisiertes Bundle erstellen VOR Text-Extraktion

### Mittelfristig:
- [ ] Automatische Hilfeplan-Ziel-Extraktion
- [ ] GUI für Dokumenten-Zuordnung (manuell nachbessern)

---

## 5. ICF-Tabellen-Methoden

### Option A: Platzhalter-Template (EMPFOHLEN)

Das Template enthält Zeilen mit Platzhaltern pro ICF-Code:

```
| ICF-Code | Kapitel                | Zielformulierung | Ist-Stand    | Erreicht | Grund |
|----------|------------------------|------------------|--------------|----------|-------|
| D350     | Konversation           | {D350-Ziel}      | {D350-Ist}   | {D350-E} | {D350-G} |
| D7503    | Mit Gleichaltrigen     | {D7503-Ziel}     | {D7503-Ist}  | {D7503-E}| {D7503-G}|
| D250     | Verhaltensregulation   | {D250-Ziel}      | {D250-Ist}   | {D250-E} | {D250-G} |
```

**Vorteile:**
- Nur die gewünschten ICF-Codes im Template
- Zeilen ohne Daten werden automatisch gelöscht
- Flexible Reihenfolge

**Platzhalter-Format:**
- `{CODE-Ziel}` → Zielformulierung
- `{CODE-Ist}` → Ist-Stand/Beschreibung
- `{CODE-E}` → Zielerreichung (1)/(2)/(3)
- `{CODE-G}` → Grund bei Nichterreichung (1)/(2)/(3)/(4)

### Option B: 72-Zeilen-Vollständiges Template

Das Universal-Template enthält alle 72 ICF-Codes. Der Generator:
1. Filtert auf die aktiven Codes
2. Füllt Zielformulierung, Ist-Stand, Erreicht, Grund in die entsprechenden Spalten

**Nachteil:** Komplexe Merge-Cell-Struktur kann zu Problemen führen.

### Fallback-Logik im Generator

Der Generator versucht zuerst die Platzhalter-Methode. Wenn keine `{xxx}` Platzhalter gefunden werden, fällt er auf die 72-Zeilen-Filterung zurück.

---

## 6. Neue Stammdaten-Felder

### Landkreis & Amt-Adresse
Der Generator ermittelt automatisch die Amt-Adresse basierend auf dem Landkreis:

| landkreis | Adresse |
|-----------|---------|
| `Lörrach` | Landratsamt Lörrach, Jugend & Familie SD IV, Hebelstraße 11, 79650 Schopfheim |
| `Waldshut` | Landratsamt Waldshut, Jugendamt, Kaiserstraße 110, 79761 Waldshut-Tiengen |

**Platzhalter:** `{{AMT_ADRESSE}}`, `{{LANDKREIS}}`

### Diagnosen (erweitertes Format)
Diagnosen werden jetzt strukturiert erfasst:

```json
{
  "diagnosen": [
    {
      "icd_code": "F84.5",
      "bezeichnung": "Asperger-Syndrom",
      "diagnostiker": "Dr. Ritter-Gekeler",
      "datum": "2019",
      "quelle": "Bericht vom 12.03.2019"
    },
    {
      "icd_code": "F90.1",
      "bezeichnung": "Hyperkinetische Störung des Sozialverhaltens",
      "diagnostiker": "Kreiskrankenhaus Lörrach",
      "datum": "2018",
      "quelle": "Entlassbericht"
    }
  ]
}
```

**Ausgabe:** `F84.5 Asperger-Syndrom (Diagnose Dr. Ritter-Gekeler, 2019)`

---

---

## 7. Verbesserter Workflow (Soll-Zustand)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DATEIEN EINSAMMELN                                       │
│    Tool: DocumentCollector (neu zu implementieren)          │
│    - Alle Dateien scannen                                   │
│    - In CORE / STUFE2 / EXTENDED kategorisieren             │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. PDF-VORVERARBEITUNG                                      │
│    Tool: c_ocr_engine.py (existiert!)                       │
│    - PDF ohne Text erkennen (Bild-PDF)                      │
│    - OCR durchführen → Text extrahieren                     │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. TEXT EINSAMMELN                                          │
│    Tool: generator.py extract_all_sources()                 │
│    - Alle Dokumente: .docx, .pdf, .msg, .eml, .xlsx → Text  │
│    - CORE + STUFE2 in ein Bundle                            │
│    - EXTENDED in separates Bundle                           │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. ANONYMISIEREN                                            │
│    Tool: anonymizer_service.py                              │
│    - Text-Bundle anonymisieren (Namen → Tarnnamen)          │
│    - Anonymisiertes Bundle speichern                        │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. BERICHT GENERIEREN                                       │
│    Tool: generator.py + LLM                                 │
│    - Anonymisiertes CORE+STUFE2 Bundle an LLM               │
│    - JSON generieren                                        │
│    - Word-Template befüllen                                 │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. DE-ANONYMISIEREN (Export)                                │
│    Tool: anonymizer_service.py DocumentDeanonymizer         │
│    - Tarnnamen → echte Namen                                │
│    - Fertiger Bericht                                       │
└─────────────────────────────────────────────────────────────┘
```

### Existierende Tools

| Tool | Pfad | Funktion |
|------|------|----------|
| OCR Engine | `skills/tools/c_ocr_engine.py` | PDF → Text via Tesseract |
| Anonymizer | `skills/_services/document/anonymizer_service.py` | Namen ersetzen |
| Generator | `agents/_experts/report_generator/generator.py` | Text-Extraktion, Bericht |
| Word Service | `skills/_services/document/word_template_service.py` | Template befüllen |

---

*Erstellt nach erstem Praxistest, 2026-01-31*
*Aktualisiert: 2026-01-31 (ICF-Platzhalter, Landkreis-Adresse, Diagnosen-Format, Mail-Extraktion, Workflow)*