# Konzept: Anonymisierter LLM-Workflow

## Status Quo

### Vorhandene Infrastruktur
- `anonymizer_service.py` - vollständiger Service mit:
  - Profilerstellung mit Tarnnamen
  - AES-256 Verschlüsselung der Schlüssel
  - Schlüssel LOKAL gespeichert (`%LOCALAPPDATA%\BACH\keys\`)
  - Anonymisierung von DOCX, TXT, PDF, Excel
  - De-Anonymisierung
  - Dateinamen-Anonymisierung
- `bundles/` Ordner existiert (core, extended)
- `.profil.json` speichert Tarnname und Client-ID

### Problem
Das LLM (und der Chatbot) sehen aktuell die **echten Namen** in den Quelldokumenten.
Der Anonymisierungsschritt erfolgt nicht automatisch vor der LLM-Verarbeitung.

---

## Ziel-Architektur

```
┌─────────────────────────────────────────────────────────────────┐
│  data/                        │  bundles/                       │
│  (Nur Nutzer sieht das)       │  (LLM sieht nur das)            │
├───────────────────────────────┼─────────────────────────────────┤
│  Forman, Jaden Hannington/    │  K_A7B3C9/                      │
│    ├── Dokumentation/         │    ├── core/                    │
│    ├── Amt&Hilfeplan/         │    │   ├── beobachtungen.txt    │
│    └── Berichte/              │    │   └── stammdaten.json      │
│                               │    └── extended/                │
│                               │        ├── externe_berichte/    │
│                               │        └── amt_korrespondenz/   │
└───────────────────────────────┴─────────────────────────────────┘
                    ▲                           │
                    │                           ▼
              ┌─────┴─────┐              ┌──────────────┐
              │ Schlüssel │              │     LLM      │
              │  (lokal)  │              │  (sieht nur  │
              │ .enc      │              │   Tarnname)  │
              └───────────┘              └──────┬───────┘
                    ▲                           │
                    │                           ▼
              ┌─────┴───────────────────────────────────┐
              │  output/                                 │
              │  (De-anonymisiert beim Speichern)        │
              │  Foerderbericht_Jaden_Forman_2026-02.docx│
              └─────────────────────────────────────────┘
```

---

## Workflow

### Phase 1: Akte anlegen (einmalig)
```
Nutzer: "Neue Akte für Jaden Forman"

System:
1. Quelldokumente in data/Forman, Jaden Hannington/ ablegen
2. Automatisch Profil erstellen:
   - Client-ID generieren (K_A7B3C9)
   - Tarnname generieren (Felix Bergmann)
   - Alle Namen in Dokumenten scannen
   - Mappings erstellen (echte Namen → Tarnnamen)
3. Schlüssel verschlüsselt LOKAL speichern
4. Bundle erstellen in bundles/K_A7B3C9/:
   - Alle Dokumente anonymisiert kopieren
   - Ordnerstruktur: core/ (wichtig) + extended/ (optional)
5. .profil.json in data-Ordner speichern (nur ID + Tarnname)
```

### Phase 2: Bericht generieren
```
Nutzer: "Bitte Förderbericht für Jaden"

System:
1. Profil aus data/.profil.json laden
2. Client-ID ermitteln → Bundle-Pfad finden
3. LLM-Prompt NUR mit Bundle-Inhalt erstellen
   → LLM sieht nur "Felix Bergmann"
4. LLM generiert JSON mit Tarnnamen
5. JSON in bundles/K_A7B3C9/output/ speichern (anonymisiert)
```

### Phase 3: Bericht speichern/exportieren
```
Nutzer: "Bericht speichern" oder automatisch nach Generierung

System:
1. Schlüssel aus lokalem Speicher laden (Passwort abfragen)
2. Bericht de-anonymisieren:
   - "Felix Bergmann" → "Jaden Forman"
   - Alle Mappings umkehren
3. In data/.../output/ speichern (echte Namen)
4. Optional: Direkt in _ready_for_export/ kopieren
```

---

## Implementierung

### Neue Klasse: `AnonymizedWorkflow`

```python
class AnonymizedWorkflow:
    """Orchestriert den anonymisierten Berichts-Workflow."""

    def __init__(self, data_dir: Path, bundles_dir: Path):
        self.data_dir = data_dir
        self.bundles_dir = bundles_dir
        self.anonymizer = DocumentAnonymizer()

    def create_or_load_profile(self, klient_ordner: str) -> Tuple[AnonymProfile, str]:
        """
        Lädt existierendes Profil oder erstellt neues.
        Returns: (profile, bundle_path)
        """
        pass

    def create_bundle(self, klient_ordner: str, profile: AnonymProfile) -> Path:
        """
        Erstellt anonymisiertes Bundle aus Quelldokumenten.
        """
        pass

    def get_bundle_content(self, client_id: str) -> str:
        """
        Extrahiert Text aus Bundle für LLM-Prompt.
        LLM sieht NUR diesen anonymisierten Text.
        """
        pass

    def save_report_deanonymized(
        self,
        report_path: Path,
        profile: AnonymProfile,
        password: str
    ) -> Path:
        """
        De-anonymisiert Bericht und speichert in data/output/.
        """
        pass
```

### Integration in Generator

```python
# In generator.py

def generate_report_anonymized(
    klient_ordner: str,
    password: str,
    template_path: str = None
) -> GeneratorResult:
    """
    Vollständiger anonymisierter Workflow.

    1. Bundle laden/erstellen
    2. Prompt aus Bundle erstellen (anonymisiert)
    3. LLM aufrufen
    4. Template füllen (mit Tarnnamen)
    5. De-anonymisieren beim Speichern
    """
    workflow = AnonymizedWorkflow(DATA_DIR, BUNDLES_DIR)

    # Profil laden/erstellen
    profile, bundle_path = workflow.create_or_load_profile(klient_ordner)

    # Quelltexte aus Bundle (anonymisiert!)
    source_text = workflow.get_bundle_content(profile.client_id)

    # LLM-Prompt (sieht nur Tarnnamen)
    prompt = build_llm_prompt(source_text, schema)

    # ... LLM-Aufruf ...

    # Template füllen (mit Tarnnamen)
    temp_output = BUNDLES_DIR / profile.client_id / "output" / "bericht_temp.docx"
    fill_template(template_path, report_data, temp_output)

    # De-anonymisieren
    final_output = workflow.save_report_deanonymized(temp_output, profile, password)

    return GeneratorResult(success=True, output_path=str(final_output))
```

---

## Ordnerstruktur (Ziel)

```
user/documents/foerderplaner/
├── Berichte/
│   ├── data/                          # Echte Daten (nur Nutzer)
│   │   └── Forman, Jaden Hannington/
│   │       ├── Dokumentation/
│   │       ├── Amt&Hilfeplan/
│   │       ├── output/                # Fertige Berichte (de-anonymisiert)
│   │       └── .profil.json           # Client-ID + Tarnname
│   │
│   ├── bundles/                       # Anonymisiert (für LLM)
│   │   └── K_A7B3C9/
│   │       ├── core/                  # Kerndokumente
│   │       │   ├── beobachtungen.txt
│   │       │   └── stammdaten.json
│   │       ├── extended/              # Zusätzliche Dokumente
│   │       └── output/                # LLM-Output (anonymisiert)
│   │
│   └── output/                        # Legacy (kann weg)
│
└── _archive/                          # Archivierte Klienten
```

---

## Sicherheitsaspekte

### Was das LLM sieht:
- Nur Tarnnamen ("Felix Bergmann")
- Anonymisierte Daten (verschobene Daten, falsche Adressen)
- Client-ID (K_A7B3C9) statt Ordnername

### Was das LLM NICHT sieht:
- Echte Namen
- Echte Adressen
- Echte Telefonnummern
- Mapping-Tabelle (Schlüssel)

### Schlüssel-Sicherheit:
- AES-256 verschlüsselt
- LOKAL gespeichert (`%LOCALAPPDATA%\BACH\keys\`)
- NICHT in OneDrive/Cloud
- Passwort nur beim De-Anonymisieren nötig

---

## Offene Fragen

1. **Bundle-Update**: Wie werden Bundles aktualisiert wenn neue Dokumente hinzukommen?
   - Option A: Bundle komplett neu erstellen
   - Option B: Inkrementelles Update

2. **Passwort-Handling**: Wann wird das Passwort abgefragt?
   - Option A: Nur beim De-Anonymisieren (Export)
   - Option B: Bei jedem Workflow-Start (sicherer)

3. **Chatbot-Integration**: Wie bekommt der Chatbot nur das Bundle?
   - Option A: Separate Funktion `read_bundle()` statt `read_file()`
   - Option B: Pfad-Umleitung in den Hooks

4. **Bestehende Akten**: Migration der Akte "Forman, Jaden" ins neue System?

---

## Nächste Schritte

1. [ ] `AnonymizedWorkflow` Klasse implementieren
2. [ ] Bundle-Erstellung automatisieren
3. [ ] Generator-Integration
4. [ ] CLI-Befehle hinzufügen:
   - `report create-bundle <klient_ordner>`
   - `report generate --anonymized <klient_ordner>`
5. [ ] Migration bestehender Akten
6. [ ] Dokumentation aktualisieren

---

## Beispiel-Session (Ziel)

```
Nutzer: Neue Akte für Jaden Forman anlegen

BACH: Profil erstellt:
  - Client-ID: K_A7B3C9
  - Tarnname: Felix Bergmann
  - Bundle erstellt in bundles/K_A7B3C9/
  - Schlüssel gespeichert (lokal)

Nutzer: Bitte Förderbericht erstellen

BACH: [Lädt Bundle für K_A7B3C9]
      [LLM sieht nur "Felix Bergmann"]
      [Bericht generiert]

Nutzer: Bericht speichern

BACH: Passwort für Entschlüsselung: ****
      Bericht de-anonymisiert und gespeichert:
      → data/Forman, Jaden Hannington/output/Foerderbericht_2026-02.docx
```
