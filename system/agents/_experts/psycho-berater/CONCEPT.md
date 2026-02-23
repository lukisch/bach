# EXPERTE: Psycho-Berater

## Status: AKTIV (Rolle)
Version: 1.0.0
Erstellt: 2026-01-20
Parent-Agent: gesundheitsassistent

---

## 1. Ueberblick

Der Psycho-Berater ist ein experimentelles Modul fuer therapeutisch orientierte Gespraeche:
- **Gespraechsprotokolle** - Sitzungen dokumentieren
- **Hypothesen** - Verhaltens- und Erlebensmuster erfassen
- **Techniken** - Loesungsfokussiert, Systemisch, Klientenzentriert
- **Ressourcen** - Positive Aspekte und Staerken sammeln

> **Hinweis**: Dies ist eine Unterstuetzung, kein Ersatz fuer professionelle Therapie.

---

## 2. Rolle und Persona

### Fiktive Identitaet
- **Name**: Dr. Lisa Kunterbunt
- **Geschlecht**: Weiblich
- **Stil**: Warmherzig, empathisch, lösungsorientiert

### Gespraechstechniken
- Lösungsfokussierte Gesprächsführung
- Systemische Techniken
- Themenzentrierte Interaktion (TZI)
- Klientenzentrierter Ansatz (Rogers)

---

## 3. Datenbank-Integration

### Tabellen in user.db

| Tabelle | Beschreibung |
|---------|--------------|
| `psycho_sessions` | Gesprächsprotokolle |
| `psycho_observations` | Hypothesen, Beobachtungen, Muster |

### Schema

```sql
-- Sitzungen
CREATE TABLE psycho_sessions (
    id INTEGER PRIMARY KEY,
    session_date DATETIME,
    duration_minutes INTEGER,
    main_topics TEXT,           -- JSON array
    key_insights TEXT,
    mood_before TEXT,
    mood_after TEXT,
    interventions_used TEXT,    -- JSON array
    homework TEXT,
    notes TEXT
);

-- Beobachtungen
CREATE TABLE psycho_observations (
    id INTEGER PRIMARY KEY,
    session_id INTEGER,
    observation_type TEXT,      -- hypothese, beobachtung, muster, ressource
    content TEXT,
    confidence TEXT,            -- niedrig, mittel, hoch
    is_active INTEGER
);
```

---

## 4. User-Datenordner

Pfad: `../user/gesundheit/psycho/`

```
psycho/
+-- sitzungen/          # Sitzungsprotokolle als Markdown
+-- wissen/             # Methoden, Übungen, Techniken
+-- reflexionen/        # Zusammenfassungen, Entwicklungen
```

---

## 5. Dokumentation

### Sitzungsprotokoll-Format

```markdown
# Sitzung vom [DATUM]

## Stimmung
- Vorher: [beschreibung]
- Nachher: [beschreibung]

## Hauptthemen
1. [thema 1]
2. [thema 2]

## Kernerkenntnisse
- [erkenntnis]

## Verwendete Techniken
- [technik]

## Hausaufgabe
- [aufgabe]

## Beobachtungen (intern)
- [hypothese/muster]
```

---

## 6. Kernfunktionen

### 6.1 Sitzungsverwaltung

```python
def start_session() -> int:
    """Startet neue Sitzung, gibt ID zurueck"""

def end_session(session_id: int, summary: dict):
    """Beendet Sitzung mit Zusammenfassung"""

def get_session_history(limit: int = 10) -> List[dict]:
    """Holt letzte Sitzungen"""
```

### 6.2 Beobachtungen

```python
def add_observation(session_id: int, obs_type: str, content: str):
    """Fuegt Beobachtung/Hypothese hinzu"""

def get_active_hypotheses() -> List[dict]:
    """Holt alle aktiven Hypothesen"""
```

---

## 7. CLI-Befehle

```bash
# Sitzungen
bach psycho session list
bach psycho session start
bach psycho session end 1 --zusammenfassung "..."

# Beobachtungen
bach psycho observation add 1 --typ hypothese --inhalt "..."
bach psycho observation list --typ muster

# Wissen
bach psycho methode list
bach psycho uebung vorschlagen --thema "Angst"
```

---

## 8. Integration mit Parent-Agent

Der Gesundheitsassistent koordiniert:
- Zugang zum Psycho-Berater-Modus
- Verknuepfung mit medizinischen Daten (wenn relevant)
- Erinnerung an geplante Reflexionen

---

## 9. Dokument-Kategorien

### Personenbezogen
- Vom Nutzer geteilte Dokumente
- Selbstbeschreibungen

### Meta-Dokumente
- Dokumentenverzeichnis
- Sitzungsuebersicht

### Wissensdatenbank
- Methodenbeschreibungen
- Uebungsanleitungen
- Gespraechstechniken

### Protokolle
- Sitzungsprotokolle
- Hypothesensammlung
- Ressourcenliste

---

## 10. Abhaengigkeiten

```
sqlite3 (stdlib)
```

Keine externen Dependencies erforderlich.

---

## 11. Ethische Richtlinien

1. **Transparenz**: Immer klar kommunizieren, dass dies KI-Unterstuetzung ist
2. **Grenzen**: Bei akuten Krisen auf professionelle Hilfe verweisen
3. **Vertraulichkeit**: Alle Daten lokal, keine Cloud-Speicherung
4. **Selbstbestimmung**: Nutzer behaelt volle Kontrolle

---

## 12. Roadmap

### Phase 1 (DONE)
- [x] Rolle definiert
- [x] Datenbank-Schema
- [x] CONCEPT.md

### Phase 2 (TODO)
- [ ] Basis-Sitzungsverwaltung
- [ ] Protokoll-Generierung
- [ ] Hypothesen-Tracking

### Phase 3 (PLANNED)
- [ ] Methoden-Datenbank
- [ ] Uebungs-Vorschlaege
- [ ] Stimmungsverlauf-Analyse