# BACH Agenten-System

## Ueberblick

Das BACH Agenten-System organisiert KI-Assistenten in einer hierarchischen Struktur:

```
Boss-Agenten (koordinieren)
    |
    +-- Experten (spezialisiert)
```

## Hierarchie

### Privat

**Persoenlicher Assistent** (`persoenlicher-assistent`)
- Terminverwaltung, Recherche, Kommunikation
- Experten:
  - Haushaltsmanagement

**Gesundheitsassistent** (`gesundheitsassistent`)
- Medizinische Dokumentation und Gesundheitsverwaltung
- Experten:
  - Gesundheitsverwalter (Arztberichte, Labor, Medikamente)
  - Psycho-Berater (therapeutische Unterstuetzung)

### Beruflich

**Bueroassistent** (`bueroassistent`)
- Steuern, Foerderplanung, Dokumentation
- Experten:
  - Steuer-Agent (Werbungskosten, Belege)
  - Foerderplaner (ICF, Materialrecherche)

## Verzeichnisstruktur

```
skills/
+-- _agents/                    # Boss-Agenten
|   +-- persoenlicher-assistent.txt
|   +-- gesundheitsassistent.txt
|   +-- bueroassistent.txt
|   +-- README.md
|
+-- _experts/                   # Experten
    +-- haushaltsmanagement/
    |   +-- CONCEPT.md
    |   +-- aufgaben.txt
    |
    +-- gesundheitsverwalter/
    |   +-- CONCEPT.md
    |
    +-- psycho-berater/
    |   +-- CONCEPT.md
    |   +-- rolle.txt
    |
    +-- steuer/
    |   +-- steuer-agent.txt
    |
    +-- foerderplaner/
        +-- foerderplaner.txt
```

## User-Datenordner

Jeder Agent hat einen dedizierten Ordner unter `../user/`:

```
../user/
+-- persoenlicher_assistent/    # Persoenlicher Assistent
|   +-- dokumente/
|   +-- briefings/
|   +-- dossiers/
|   +-- haushalt/               # Haushaltsmanagement
|
+-- gesundheit/                 # Gesundheitsassistent
|   +-- dokumente/
|   +-- wissen/
|   +-- auswertungen/
|   +-- psycho/                 # Psycho-Berater
|
+-- buero/                      # Bueroassistent
    +-- steuer/                 # Steuer-Agent
    +-- foerderplanung/         # Foerderplaner
```

## Datenbank-Integration

### bach.db

- `bach_agents` - Registrierte Boss-Agenten
- `bach_experts` - Registrierte Experten
- `agent_expert_mapping` - Zuordnungen

### user.db

Jeder Experte kann eigene Tabellen haben:

**Haushaltsmanagement:**
- `household_inventory`
- `household_shopping_lists`
- `household_finances`
- `household_routines`

**Gesundheitsverwalter:**
- `health_contacts`
- `health_diagnoses`
- `health_medications`
- `health_lab_values`
- `health_documents`
- `health_appointments`

**Psycho-Berater:**
- `psycho_sessions`
- `psycho_observations`

**Persoenlicher Assistent:**
- `assistant_contacts`
- `assistant_calendar`
- `assistant_briefings`
- `assistant_user_profile`

## CLI-Befehle

```bash
# Agenten anzeigen
python skills/tools/agent_cli.py list
python skills/tools/agent_cli.py experts

# Agent-Details
python skills/tools/agent_cli.py info gesundheitsassistent

# User-Ordner initialisieren
python skills/tools/agent_cli.py init all
python skills/tools/agent_cli.py init bueroassistent

# Datenbank einrichten
python skills/tools/agent_cli.py setup-db

# System-Status
python skills/tools/agent_cli.py status
```

## Neuen Agenten hinzufuegen

1. **Agent-Datei erstellen** unter `agents/name.txt`
2. **In Datenbank registrieren** (in `agent_cli.py` oder manuell)
3. **User-Ordner definieren** unter `../user/`
4. **Experten zuordnen** falls vorhanden

## Neuen Experten hinzufuegen

1. **Ordner erstellen** unter `agents/_experts/name/`
2. **CONCEPT.md** mit Dokumentation
3. **Schema** in `data/schema_agents.sql` falls DB-Tabellen benoetigt
4. **Dem Boss-Agent zuordnen**

## Workflow

1. **Agent aktivieren**: Entweder direkt oder ueber CLI
2. **Kontext laden**: Agent laedt Skill-Datei und User-Daten
3. **Anfrage analysieren**: Agent entscheidet ob selbst oder Experte
4. **Delegation**: Bei Spezialthemen an Experten delegieren
5. **Ergebnisse sammeln**: Boss-Agent fasst zusammen