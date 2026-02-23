# Self-Extension Workflow

> **Ziel:** BACH autonome Selbsterweiterung durch KI-Partner (Claude, Gemini, etc.)
> **Version:** 1.0.0
> **Erstellt:** 2026-02-13

---

## Wann nutzen?

Wenn der KI-Partner eine Faehigkeit benoetigt, die BACH noch nicht hat:
- User fragt nach etwas, das kein Handler/Tool abdeckt
- Ein Workflow erfordert ein fehlendes Tool
- Eine Domain braucht einen neuen Experten

---

## Self-Extension Loop (4 Schritte)

```
ERKENNEN -> ERSTELLEN -> REGISTRIEREN -> NUTZEN
    |                                       |
    +----------- REFLEKTIEREN <-------------+
```

### Schritt 1: ERKENNEN (Luecke identifizieren)

Pruefe ob die Faehigkeit wirklich fehlt:

```bash
bach skills search "<keyword>"
bach tools search "<keyword>"
bach --help <thema>
```

Wenn nichts gefunden: Weiter zu Schritt 2.

### Schritt 2: ERSTELLEN (Skill scaffolden + implementieren)

**Entscheide den Typ:**

| Situation | Typ | Befehl |
|-----------|-----|--------|
| Neuer CLI-Befehl noetig | handler | `bach skills create <name> --type handler` |
| Standalone-Script noetig | tool | `bach skills create <name> --type tool` |
| Neuer KI-Agent noetig | agent | `bach skills create <name> --type agent` |
| Fachexperte noetig | expert | `bach skills create <name> --type expert` |
| Hintergrund-Service noetig | service | `bach skills create <name> --type service` |

**Erstellen:**

```bash
bach skills create voice-processor --type tool
```

**Implementieren:**
- Oeffne die erstellte Datei
- Fuege die Logik ein
- Teste isoliert: `python tools/voice-processor.py`

### Schritt 3: REGISTRIEREN (Hot-Reload)

```bash
bach skills reload
```

Dies macht:
1. Handler-Registry neu laden (neue Handler sofort verfuegbar)
2. Tool-Auto-Discovery (neue Tools in DB + Trigger)
3. Skills-Verzeichnis scannen (Statistik aktualisieren)

### Schritt 4: NUTZEN (Testen und verwenden)

```bash
# Handler testen:
bach <name> list

# Tool testen:
bach tools run <name>

# Skill pruefen:
bach skills show <name>
```

### Bonus: REFLEKTIEREN

Nach erfolgreicher Nutzung:

```bash
bach lesson add "Self-Extension: <name> erstellt fuer <zweck>"
```

---

## Typ-spezifische Details

### Handler erstellen

```bash
bach skills create email-parser --type handler
```

Ergebnis: `hub/email-parser.py` mit BaseHandler-Skelett.
Danach: Implementierung ergaenzen, `bach skills reload`, `bach email-parser list`.

### Tool erstellen

```bash
bach skills create voice-processor --type tool
```

Ergebnis: `tools/voice-processor.py` mit Standard-Skelett.
Danach: main() implementieren, `bach skills reload`, `bach tools run voice-processor`.

### Agent erstellen

```bash
bach skills create medien-agent --type agent
```

Ergebnis:
```
agents/medien-agent/
  SKILL.md         (Agenten-Definition)
  manifest.json    (Metadaten)
  tools/           (Agent-spezifische Tools)
```

Danach: SKILL.md mit Rolle/Regeln fuellen, optional Tools in tools/ erstellen.

### Expert erstellen

```bash
bach skills create datenschutz-experte --type expert
```

Ergebnis:
```
agents/_experts/datenschutz-experte/
  SKILL.md         (Experten-Wissen)
  manifest.json    (Metadaten)
```

Danach: SKILL.md mit Fachwissen fuellen.

---

## Beispiel: Kompletter Self-Extension-Zyklus

**User:** "Kannst du meine Sprachnachrichten transkribieren?"

**KI-Partner (Claude):**

```
1. Pruefen: bach tools search "sprach"
   -> Nichts gefunden.

2. Erstellen: bach skills create speech-transcriber --type tool
   -> tools/speech-transcriber.py erstellt

3. Implementieren: [Code in die Datei schreiben]
   - whisper/openai API einbinden
   - Audio-Datei lesen
   - Transkription zurueckgeben

4. Registrieren: bach skills reload
   -> Tool in DB registriert, Trigger gesetzt

5. Nutzen: bach tools run speech-transcriber "audio.wav"
   -> Transkription ausgeben

6. Reflektieren: bach lesson add "speech-transcriber Tool erstellt fuer Sprachnachrichten"
```

---

## Sicherheitshinweise

- **Kein Ueberschreiben:** Create verweigert wenn Skill bereits existiert
- **DB-Registration:** Ist optional, BACH funktioniert auch ohne
- **Testen:** Immer isoliert testen bevor im Produktivbetrieb nutzen
- **Versionierung:** manifest.json enthaelt Version, spaeter per `bach skills version` pruefbar

---

## Fortgeschritten: Batch-Erstellung

Mehrere Skills auf einmal:

```bash
bach skills create api-connector --type handler
bach skills create data-validator --type tool
bach skills create security-expert --type expert
bach skills reload
```

---

*Workflow-Version: 1.0.0 | BACH Self-Extension System v2.1*
