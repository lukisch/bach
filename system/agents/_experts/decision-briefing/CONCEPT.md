# EXPERTE: Decision-Briefing

## Status: AKTIV
Version: 1.0.0
Erstellt: 2026-02-18
Parent-Agent: persoenlicher-assistent

---

## 1. Ueberblick

Der Decision-Briefing-Experte ist das zentrale System für ausstehende Entscheidungen und User-Aufgaben in BACH. Er:

- **Scannt** alle registrierten Ordner und Dateien nach Entscheidungs- und Aufgaben-Markern
- **Konsolidiert** Treffer in einem zentralen Briefing-Dokument
- **Legt** Entscheidungen dem User strukturiert vor (interaktive Session)
- **Verteilt** getroffene Entscheidungen zurück an die Ursprungsdateien

**Zweiteilung:**
- `DECISION_BRIEFING.txt` — offene Entscheidungen die eine Wahl erfordern
- `AUFGABEN.txt` — Dinge die der User selbst tun muss (Aktionen, Deadlines)

**Abgrenzung zu `user-decide.md`:**
`user-decide.md` bietet Entscheidungs-Frameworks (Pro/Con, Weighted Scoring) für eine einzelne Frage im Gespräch.
Decision-Briefing sammelt **systemweit alle offenen Entscheidungen** und koordiniert ihre Bearbeitung.
Beide ergänzen sich: Decision-Briefing kann `user-decide.md` für komplexe Einzelfälle einsetzen.

---

## 2. Marker-Konvention

Dateien im System kennzeichnen Entscheidungen und Aufgaben mit folgenden Markern:

### Entscheidungs-Marker

```
ENTSCHEIDUNG: Welchen Server für den nächsten MCMC-Run buchen?
DECISION: Which journal to target for Paper 3?
[ENTSCHEIDUNG] Soll die Funktion intern oder als Modul ausgelagert werden?
```

### Aufgaben-Marker

```
AUFGABE: Steuererklärung bis 31.03. abgeben
TODO: Termin mit Dr. Müller vereinbaren
TASK: GitHub-Repo für CFM auf öffentlich stellen nach DOI-Vergabe
ACTION: E-Mail an Konferenz-Komitee senden
```

### Optionale Zusatzinformationen (direkt nach Marker)

```
ENTSCHEIDUNG: Server-Provider auswählen
  Optionen: Hetzner / AWS / DigitalOcean
  Fälligkeit: vor 25.02.
  Kontext: Für laufende MCMC-Runs gebraucht
```

---

## 3. Scan-Quellen (Registrierung)

Welche Ordner und Dateien durchsucht werden, ist konfigurierbar:

### Konfigurationsdatei

```json
// user/decision_briefing/sources.json
{
  "sources": [
    {
      "path": "user/persoenlicher_assistent/",
      "patterns": ["*.md", "*.txt"],
      "recursive": true
    },
    {
      "path": "C:/Users/User/OneDrive/Forschung/",
      "patterns": ["Plan.txt", "AUFGABEN.txt", "*.md"],
      "recursive": true
    },
    {
      "path": "C:/Users/User/OneDrive/KI&AI/BACH_v2_vanilla/",
      "patterns": ["MASTERPLAN.txt", "TODO.txt"],
      "recursive": false
    },
    {
      "path": "user/notizblock/",
      "patterns": ["*.txt"],
      "recursive": true
    }
  ]
}
```

Neue Quellen über CLI registrieren (siehe Abschnitt 6).

---

## 4. Briefing-Dokument-Format

### DECISION_BRIEFING.txt

```
# Decision Briefing — 2026-02-18
# Generiert: 14:30 | Quellen: 12 Dateien durchsucht
# Offen: 5 Entscheidungen, 3 Aufgaben

============================================================
ENTSCHEIDUNGEN — OFFEN (5)
============================================================

[E001] Welchen Server für den nächsten MCMC-Run buchen?
  Quelle: /Forschung/Natur&Technik/Spieltheorie Urknall/Plan.txt:45
  Kontext: Aktueller Run endet ~19.02., Nachfolger nötig
  Optionen: Hetzner CCX33 / Hetzner CCX53 / AWS c5.4xlarge
  Fälligkeit: 20.02.2026
  Entscheidung: _______________

[E002] Zielzeitschrift für Paper 3?
  Quelle: /Forschung/Natur&Technik/Spieltheorie Urknall/Plan.txt:78
  Kontext: PRD hat höheren Impact, JCAP ist thematisch passender
  Optionen: PRD / JCAP / Andere
  Entscheidung: _______________

[E003] ...

============================================================
AUFGABEN — OFFEN (3)
============================================================

[A001] Steuererklärung abgeben
  Quelle: /Dokumente/_Versicherungen&Finanzen/Steuer/TODO.txt:3
  Fälligkeit: 31.03.2026
  Status: offen

[A002] GitHub-Repo cfm-cosmology auf öffentlich stellen
  Quelle: /Forschung/Plan.txt:102
  Fälligkeit: nach DOI-Vergabe
  Status: offen

[A003] ...

============================================================
GETROFFEN (letzte 30 Tage): 8 Entscheidungen
→ Details: user/decision_briefing/entschieden/ENTSCHIEDEN.md
============================================================
```

---

## 5. Workflow

### 5.1 Scan-Phase

```
1. bach entscheidung scan
   ↓
2. Alle registrierten Quellen lesen (sources.json)
   ↓
3. Regex-Suche nach Markern (ENTSCHEIDUNG, AUFGABE, TODO, TASK...)
   ↓
4. Einträge extrahieren: Text, Quelle, Zeile, Kontext (umliegende Zeilen)
   ↓
5. Deduplizierung (gleiche Entscheidung in mehreren Dateien)
   ↓
6. DECISION_BRIEFING.txt + AUFGABEN.txt generieren
   ↓
7. User-Meldung: "5 neue Entscheidungen, 3 neue Aufgaben gefunden"
```

### 5.2 Decision-Session (interaktiv mit Claude)

```
bach entscheidung session
   ↓
Claude liest DECISION_BRIEFING.txt
   ↓
Für jede offene Entscheidung:
  1. Entscheidung [E001] vorlegen mit vollem Kontext
  2. Optionen präsentieren (falls angegeben)
  3. Bei Bedarf: decide.md-Framework anwenden
  4. User trifft Entscheidung
  5. Entscheidung in DECISION_BRIEFING.txt eintragen
  ↓
Alle getroffen? → Rückverteilung starten
   ↓
Session-Protokoll speichern
```

### 5.3 Rückverteilung

Nach getroffenen Entscheidungen werden die Original-Dateien aktualisiert:

**Marker in Quelldatei (vorher):**
```
ENTSCHEIDUNG: Welchen Server buchen?
  Optionen: Hetzner / AWS
```

**Nach Rückverteilung:**
```
ENTSCHEIDUNG: Welchen Server buchen?
  Optionen: Hetzner / AWS
  → GETROFFEN 2026-02-18: Hetzner CCX33
  → Nächste Aktion: Server bestellen (Aufgabe A004 erstellt)
```

Optional: Automatisch eine neue Aufgabe im AUFGABEN.txt anlegen wenn die Entscheidung eine Folgeaktion impliziert.

---

## 6. User-Datenordner

```
user/decision_briefing/
├── DECISION_BRIEFING.txt   # Aktives Briefing (generiert)
├── AUFGABEN.txt            # Offene User-Aufgaben (generiert)
├── sources.json            # Registrierte Scan-Quellen
├── entschieden/
│   └── ENTSCHIEDEN.md      # Log aller getroffenen Entscheidungen
└── archiv/
    ├── BRIEFING_2026-01.txt
    └── BRIEFING_2026-02.txt
```

---

## 7. CLI-Befehle

```bash
# Scan und Briefing generieren
bach entscheidung scan
bach entscheidung scan --quelle "/Forschung/CFM/"  # Nur diese Quelle

# Briefings anzeigen
bach entscheidung briefing         # Offene Entscheidungen
bach entscheidung aufgaben         # Offene User-Aufgaben
bach entscheidung log              # Getroffene Entscheidungen (Log)

# Interaktive Session
bach entscheidung session          # Claude führt durch alle offenen Entscheidungen

# Einzelne Entscheidung
bach entscheidung decide E001 "Hetzner CCX33"
bach entscheidung aufgabe-erledigt A001

# Quellen verwalten
bach entscheidung source add "/Forschung/" --pattern "Plan.txt" --recursive
bach entscheidung source list
bach entscheidung source remove 3

# Rückverteilung
bach entscheidung distribute       # Alle getroffenen Entscheidungen zurückverteilen
bach entscheidung distribute E001  # Nur eine Entscheidung
```

---

## 8. Datenbank-Integration (optional)

### Tabellen in user.db

```sql
CREATE TABLE decision_items (
    id INTEGER PRIMARY KEY,
    type TEXT,           -- 'entscheidung' | 'aufgabe'
    ref_id TEXT,         -- E001, A001...
    title TEXT,
    source_file TEXT,
    source_line INTEGER,
    context TEXT,
    optionen TEXT,       -- JSON-Array
    faelligkeit TEXT,
    status TEXT DEFAULT 'offen',  -- offen | getroffen | verteilt | erledigt
    decision TEXT,       -- Getroffene Entscheidung
    decided_at TEXT,
    distributed_at TEXT
);
```

**Primär:** Flachdatei-Betrieb (ohne DB). DB ist optionale Erweiterung für Volltextsuche und Statistik.

---

## 9. Abgrenzung und Synergien

| Funktion | `user-decide.md` (Service) | `decision-briefing` (Experte) |
|---|---|---|
| Einzelne Entscheidung strukturieren | ✓ | — |
| Systemweiter Scan | — | ✓ |
| Zentrales Briefing-Dokument | — | ✓ |
| Rückverteilung an Quellen | — | ✓ |
| Interaktive Session | — | ✓ |
| Aufgaben-Verwaltung | — | ✓ |

**Synergie:** Decision-Briefing kann bei komplexen Einzelfällen (E001 mit vielen Kriterien) den `user-decide.md`-Service einsetzen für strukturierte Analyse vor der Entscheidung.

---

## 10. Abhaengigkeiten

Standard (keine zusätzlichen Pakete nötig):
- Python stdlib (pathlib, re, json)

Optional für erweiterte Scan-Funktionen:
- `bach-filecommander-mcp` für breite Datei-Scans
- `fc_ocr` falls gescannte Dokumente gescannt werden sollen

---

## 11. Roadmap

### Phase 1 — DONE (Konzept)
- [x] CONCEPT.md erstellt
- [x] Marker-Konvention definiert
- [x] Workflow dokumentiert
- [x] sources.json-Schema definiert
- [x] Briefing-Format festgelegt

### Phase 2 — TODO
- [ ] Scan-Script implementieren (Python)
- [ ] Briefing-Generator (Regex + Template)
- [ ] sources.json Verwaltung
- [ ] Rückverteilungs-Mechanismus
- [ ] Basis CLI-Befehle

### Phase 3 — PLANNED
- [ ] DB-Integration mit Status-Tracking
- [ ] Automatische Aufgaben-Generierung aus Entscheidungen
- [ ] Deadline-Erinnerungen
- [ ] Entscheidungs-Statistiken (Durchlaufzeit, Häufigkeit)
