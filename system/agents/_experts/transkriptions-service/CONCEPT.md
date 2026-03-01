# EXPERTE: Transkriptions-Service

## Status: AKTIV
Version: 1.0.0
Erstellt: 2026-02-18
Parent-Agent: persoenlicher-assistent

---

## 1. Ueberblick

Der Transkriptions-Service wandelt Audiodateien und Gespräche in strukturierte Textdokumente um:
- **Wörtliches Rohtransskript** mit Pausennotation und Artikulationsmarkierungen
- **Sprecher-Erkennung** und -zuordnung (vor- oder nachträglich)
- **Bereinigung** zum sauberen Leseprotokoll
- **Export** als TXT, Markdown oder PDF
- **Übergabe** an BACH-Notizblöcke

Bestehender Ansatz aus dem Forschungsprojekt:
`Forschung/Methoden/HOLD__Podcast_Concept_Politik/prototype/srt_to_transcript.py`
(SRT→Transkript-Konverter; kann als Basis-Tool für SRT-Quellen genutzt werden)

---

## 2. Transkriptions-Notation

### Standardmarkierungen

| Markierung | Bedeutung |
|---|---|
| (Pause) | Kurze Sprechpause (< 3 Sek.) |
| (lange Pause) | Pause > 3 Sekunden |
| ähm / äh | Gefüllte Pause, wörtlich transkribiert |
| (räuspert sich) | Nicht-verbale Lautäußerung |
| (lacht) | Lachen |
| (unverständlich) | Nicht transkribierbar |
| (überlappend) | Gleichzeitiges Sprechen zweier Sprecher |
| [Hintergrundgeräusch] | Kontextueller Hinweis |
| SV1: | Sprecher 1 — vorläufig, vor Zuordnung |
| A: | Zugewiesener Sprecher nach Zuordnung |
| // | Abrupter Abbruch oder Unterbrechung |

### Zeitstempel-Format (optional)

```
[00:03:45] SV1: Text der Äußerung...
```

---

## 3. Workflow

### 3.1 Schritt 1 — Rohtransskript erstellen

**Quellen:** Audiodatei, Diktat, handschriftliche Mitschrift, SRT-Datei

**Prozess:**
1. Sprecher vorab festlegen (wenn bekannt) oder vorläufig nummerieren (SV1, SV2...)
2. Alle gesprochenen Wörter wörtlich notieren — auch Füllwörter, Wiederholungen
3. Pausennotation und Artikulationen nach Konvention einfügen (Abschnitt 2)
4. Sprecher-Wechsel markieren

**Ergebnis:** `transkript_roh_DATUM.txt`

### 3.2 Schritt 2 — Sprecher-Zuordnung

**Vorab (wenn Teilnehmer bekannt):**
Direkt als `A:`, `B:`, `Lukas:`, `Dr. Müller:` transkribieren.

**Nachträglich (unbekannte Sprecher):**
1. Rohtransskript mit SV1, SV2, ... erstellen
2. Charakteristika notieren (Themen, Redeanteil, Stil)
3. User ordnet zu: "SV1 = ich, SV2 = Interviewer"
4. Claude führt Bulk-Ersatz im Dokument durch

**Externe Tools (via production-agent):**
- **Whisper (OpenAI):** Lokale Transkription mit Sprechertrennung
- **Gemini 1.5 Pro:** Direkte Audio-Transkription langer Dateien
- **Descript:** Professionelle Sprecher-Erkennung und Editing

### 3.3 Schritt 3 — Bereinigung

Aus dem Rohtranskript wird ein **sauberes Leseprotokoll** erzeugt:
- Füllwörter entfernen (ähm, äh, halt, irgendwie, sozusagen)
- Selbstkorrekturen auflösen (Hauptversion behalten)
- Pausennotation und Artikulationen entfernen
- Satzstruktur glätten — **ohne Sinnänderung**
- Sprecher bleiben erhalten

**Ergebnis:** `transkript_bereinigt_DATUM.txt`

### 3.4 Schritt 4 — Export

| Format | Dateiname | Inhalt |
|---|---|---|
| TXT | `transkript_roh_DATUM.txt` | Rohtranskript mit Notation |
| TXT | `transkript_bereinigt_DATUM.txt` | Bereinigtes Protokoll |
| Markdown | `transkript_DATUM.md` | Mit Formatierung und Metadaten |
| PDF | `transkript_DATUM.pdf` | Druckfertig (via cc_md_to_html MCP) |

---

## 4. Notizblock-Integration

Transkripte können direkt in BACH-Notizblöcke übergeben werden:
- Rohtranskript → Notizblock `interviews`
- Bereinigtes Transkript → Notizblock `protokolle`
- Einzelne Passagen per Markierung `#NB: <ziel>` in spezifische Notizbücher

---

## 5. User-Datenordner

```
user/transkriptionen/
├── roh/           # Rohtranskripte mit Notation
├── bereinigt/     # Bereinigte Leseprotokolle
├── audio/         # Originaldateien (falls lokal gespeichert)
└── export/        # PDF- und MD-Exporte
```

---

## 6. Datenbank-Integration (optional)

### Tabellen in user.db

| Tabelle | Beschreibung |
|---|---|
| `transcript_sessions` | Transkriptions-Sessions (Datum, Titel, Quelle, Status) |
| `transcript_speakers` | Sprecher-Profile je Session |
| `transcript_segments` | Zeitgestempelte Blöcke (wenn Timestamps vorhanden) |

---

## 7. CLI-Befehle

```bash
# Neue Transkription starten
bach transkript new "Interview_Mueller" --sprecher "A:Lukas,B:Müller"
bach transkript new "Diktat_20260218"  # ohne Sprecher

# Sprecher nachträglich zuordnen
bach transkript speaker-map roh.txt --sv1 "Lukas" --sv2 "Interviewer"

# Bereinigen
bach transkript clean roh.txt --output bereinigt.txt

# Export
bach transkript export roh.txt --format md
bach transkript export roh.txt --format pdf

# In Notizblock senden
bach transkript to-notizblock roh.txt --buch "interviews"

# Übersicht
bach transkript list
bach transkript status "Interview_Mueller"
```

---

## 8. Abhaengigkeiten

Standard (keine zusätzlichen Abhängigkeiten):
- Python stdlib (pathlib, re, json)

Optional für Audio-Transkription:
- **openai-whisper** (pip) — lokale Transkription
- **gemini API** — lange Audio-Dateien
- **bach-codecommander-mcp** `cc_md_to_html` — PDF-Export

---

## 9. Roadmap

### Phase 1 — DONE (Konzept)
- [x] CONCEPT.md erstellt
- [x] Notations-Konvention definiert
- [x] Workflow dokumentiert
- [x] Integration Notizblock und production-agent beschrieben

### Phase 2 — TODO
- [ ] Basis-Transkriptions-Template (TXT-Vorlage)
- [ ] Bereinigungsprotokoll als Claude-Prompt
- [ ] Whisper-Integration (lokal)
- [ ] SRT-Import via srt_to_transcript.py Basis

### Phase 3 — PLANNED
- [ ] Automatische Sprechertrennung via Whisper
- [ ] Zeitstempel-synchronisierte Ansicht
- [ ] DB-Integration mit Volltextsuche
