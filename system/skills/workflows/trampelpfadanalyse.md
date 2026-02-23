# Trampelpfadanalyse & Schwarm-Verfahren (Elephant Path / Swarm Ops)

**Version:** 2.0
**Stand:** 2026-02-15
**Quelle:** Pilotversuch (10 Proben) + Grossversuch (100 Proben) auf BACH-Dateisystem

---

## Uebersicht

Die Trampelpfadanalyse ist eine Methode, um zu beobachten wie naive LLMs ein unbekanntes System navigieren. Ziel: Herausfinden wo "Schilder" (READMEs, Guardrails, Leitplanken) fehlen.

Darauf aufbauend: **Schwarm-Verfahren (Swarm Ops)** - Muster fuer die parallele Ausfuehrung von LLM-Agenten fuer verschiedene Zwecke.

```
TRAMPELPFADANALYSE - 4 PHASEN               SCHWARM-VERFAHREN
+--------------------------------------+    +---------------------------+
| 1. PROBEN DEFINIEREN                 |    | A. Echolot (Exploration)  |
| 2. AGENTEN LOSLASSEN (naiv)          |    | B. Single Op (Race)       |
| 3. PFADE AUSWERTEN (Heatmap)        |    | C. Ralphing (Pipeline)    |
| 4. SCHILDER AUFSTELLEN              |    | D. Nano-Swarm (Emergent)  |
+--------------------------------------+    | E. Schatzsuche (Health)   |
                                            +---------------------------+
```

**Dauer:** 20-40 Minuten (100 Proben parallel)
**Kosten:** ~$3-5 (100 Haiku-Proben)
**Analogie:** Elephant Path - LLMs sind grosse, kraftvolle "Tiere" die sichtbare Spuren im Dateisystem hinterlassen.

---

## Teil 1: Trampelpfadanalyse

### Phase 1: Proben definieren

#### 1.1 Auftraege waehlen

| Typ | Beispiel | Prueft |
|-----|----------|--------|
| Lesen | "Wo sind die Logs?" | Dateisystem-Navigation |
| Schreiben | "Erstelle einen Task" | API-Discovery |
| Suchen | "Finde alle Python-Tools" | Such-Strategien |
| Verstehen | "Was ist der System-Status?" | Architektur-Verstaendnis |
| Ausfuehren | "Starte BACH" | Startpunkt-Finding |

**Empfehlung:** 20 verschiedene Auftraege, jeder 5x wiederholt = 100 Proben.

#### 1.2 Test-Modi

| Modus | MEMORY.md | Skills | Hooks | Misst |
|-------|-----------|--------|-------|-------|
| **Naiv** | Leer | Deaktiviert | Aktiv | Reine Navigation ohne Vorwissen |
| **Informiert** | Normal | Aktiv | Aktiv | Navigation mit BACH-Kontext |
| **Post-Schilder** | Leer | Deaktiviert | Aktiv | Wirkung der neuen READMEs |

**Empfohlene Reihenfolge:**
1. Naiv-Test (Baseline) → Schilder-Bedarf identifizieren
2. Schilder aufstellen (READMEs, ARCHITECTURE.md Updates)
3. Post-Schilder-Test → Verbesserung messen
4. Optional: Informiert-Test → Maximale Leistung mit vollem Kontext

**Vergleichs-Metriken:**

| Metrik | Naiv | Post-Schilder | Informiert |
|--------|------|---------------|------------|
| Fehler/Probe | ? | ? | ? |
| Pfade bis Ziel | ? | ? | ? |
| Erfolgsquote | ? | ? | ? |
| Blind Spots | ? | ? | ? |

#### 1.3 Technische Parameter

| Parameter | Empfehlung |
|-----------|-----------|
| Proben | 100 (20 Tasks x 5) |
| Modell | Haiku (guenstig, naiv) |
| Timeout | 120 Sekunden |
| Max parallel | 5 (Semaphore) |
| Tools | Bash, Glob, Grep, Read |
| Skills | Deaktiviert (--disable-slash-commands) |
| Verbose | Ja (--verbose, noetig fuer stream-json) |

### Phase 2: Agenten loslassen

**Launcher-Script:** `data/elephant_path_launcher.py` (v6.0)

```bash
cd system/ && python data/elephant_path_launcher.py
```

Das Script:
- Sichert MEMORY.md automatisch (Backup + atexit-Sicherheitsnetz)
- Startet alle Threads sofort (Semaphore regelt Parallelitaet)
- Stellt MEMORY.md wieder her sobald alle Proben gestartet sind
- Speichert stream-json + geparste Ergebnisse pro Probe

**Prompt-Template:**

```
Du erkundet das [SYSTEM].
[SYSTEM] liegt unter: [PFAD]

AUFTRAG: [Spezifischer Auftrag]

REGELN:
1. Du weisst NUR den Pfad oben, sonst NICHTS
2. Erkunde das System um den Auftrag zu erfuellen
3. Maximal 8 Schritte
4. Am Ende: BESUCHTE_VERZEICHNISSE, GELESENE_DATEIEN,
   AUFTRAG_ERFUELLT, HILFREICHSTE_DATEI
```

### Phase 3: Pfade auswerten

#### 3.1 Heatmap erstellen

```
HITZE-SKALA: ████ HOT (30+)  ░░░░ WARM (10-29)  ···· COOL (1-9)  ---- COLD (0)

system/                          ████████████████████ 97/100
├── data/                        ████████████████     37/100
├── hub/                         ░░░░░░░░░░░░        27/100
├── tools/                       ░░░░                 14/100
├── skills/                      ░░░░                 13/100
├── agents/                      ░░░░                 11/100
├── core/                        ····                  8/100
├── partners/                    ····                  8/100
├── docs/                        ····                  8/100
├── wiki/                        ····                  6/100
├── connectors/                  ····                  6/100
├── _templates/                  ····                  3/100
├── gui/                         ····                  1/100
├── help/                        ----                  0/100  ← BLIND SPOT!
└── start/                       ····                  4/100
```

#### 3.2 Schilder-Bedarf identifizieren

| Befund | Bedeutung | Massnahme |
|--------|-----------|-----------|
| HOT + kein README | Viel Traffic, keine Orientierung | README dringend noetig |
| WARM + Fehler | Agenten kommen hin, straucheln | Bessere Doku/Beispiele |
| COLD | Nicht gefunden | Verlinkung in ARCHITECTURE.md |
| Sackgasse | Agent dreht Schleifen | Wegweiser hinzufuegen |
| Direktzugriff DB | Agent umgeht API | Teaching-Hook installieren |

### Phase 4: Schilder aufstellen

1. **ARCHITECTURE.md**: Schnellnavigation-Tabelle am Anfang (Top-Datei: 43/100 lesen sie)
2. **READMEs**: In jedem HOT-Verzeichnis ohne README
3. **Teaching-Hooks**: PreToolUse fuer gefaehrliche Aktionen
4. **Pfad-Hinweise**: Forward-Slashes empfehlen (56% nutzen Backslashes)

---

## Teil 2: Schwarm-Verfahren (Swarm Ops)

### Grundlagen: Schwarm-Robotik fuer LLMs

Inspiriert von Schwarm-Robotik und Ameisen-Algorithmen. Kernkonzepte:

| Konzept | Biologisch | LLM-Adaption |
|---------|-----------|--------------|
| **Stigmergy** | Ameisen hinterlassen Pheromone | Agenten hinterlassen Dateien/Marker in Verzeichnissen |
| **Einfache Regeln** | Jede Ameise folgt 3-4 Regeln | Jeder Agent hat minimalen Prompt mit klaren Regeln |
| **Emergenz** | Globale Strukturen aus lokalen Aktionen | Wissensrekonstruktion aus vielen Pfad-Fragmenten |
| **Keine direkte Kommunikation** | Ameisen "sprechen" nicht | Agenten arbeiten unabhaengig, Ergebnisse werden aggregiert |
| **Parallelitaet** | Tausende gleichzeitig | Semaphore-gesteuerte Parallelausfuehrung |

### Muster A: Echolot / Swarm Inspection

**Zweck:** Unbekannte Ordnerstruktur kartieren und Wissen rekonstruieren.

```
100 Erkunder → unbekannter Ordner → jeder sammelt Daten
                                         ↓
                              Aggregation: Pfade + Fakten
                                         ↓
                              Mehrfach bestaetigt = validiert
```

**Regeln pro Agent:**
1. Starte am Root, erkunde so viele Verzeichnisse wie moeglich
2. Lies jede Datei die du findest (mindestens Anfang)
3. Notiere: Pfad, Dateiname, Inhaltszusammenfassung, Groesse
4. Maximal N Schritte, dann Bericht

**Auswertung:**
- Pfade die von 5+ Agenten besucht wurden = Hauptstruktur
- Fakten die von 3+ Agenten bestaetigt werden = validiert
- Dateien die nur 1 Agent fand = Randgebiet, manuell pruefen

**Anwendung:** Onboarding auf fremdes Projekt, Legacy-Code verstehen, Audit.

### Muster B: Single Op / Race

**Zweck:** Schnellstmoegliche Ausfuehrung einer einzelnen Operation.

```
100 Agenten → selbe Aufgabe → Erster Erfolg → ALLE STOPPEN
```

**Ablauf:**
1. Alle Agenten bekommen identische Aufgabe
2. Sobald ein Agent "ERFUELLT" meldet: Signal an alle
3. Laufende Agenten werden terminiert (subprocess.kill)
4. Ergebnis des Siegers wird verwendet

**Technisch:**
- Shared `threading.Event()` als Abbruchsignal
- Jeder Agent prueft das Event vor jedem Schritt
- Alternativ: Polling auf eine "done"-Datei

**Anwendung:** Zeitkritische Operationen, Bugfix-Race, First-Response.

### Muster C: Ralphing / Review-Pipeline

**Zweck:** Qualitaetsgesicherte Bearbeitung vieler Minitasks.

```
100 Minitasks → Worker (Haiku) → Reviewer (Haiku) → Senior (Sonnet/Opus)
                    ↓                  ↓                    ↓
               Bearbeitung       OK? → weiter         OK? → FERTIG
                                Nein → zurueck       Nein → zurueck
```

**Pipeline pro Task-Line:**
1. **Worker** (Haiku): Bearbeitet den Minitask
2. **Reviewer** (Haiku): Prueft das Ergebnis. OK → Senior. Nicht OK → Worker nochmal.
3. **Senior Reviewer** (Sonnet/Opus): Finale Qualitaetspruefung. OK → Fertig. Nicht OK → Worker.

**Parallelitaet:**
- Alle 100 Lines laufen gleichzeitig (Semaphore ueber alle Lines)
- Jede Line ist unabhaengig
- Global-Semaphore: Max N gleichzeitige API-Calls ueber alle Lines

**Anwendung:** Batch-Uebersetzungen, Code-Reviews, Dokumentation, Daten-Bereinigung.

### Muster D: Nano-Swarm / Emergent Behavior

**Zweck:** Komplexe Aufgabe loesen durch Agenten mit einfachen lokalen Regeln, ohne direkte Kommunikation.

**Inspiration:** Schwarm-Robotik (Kilobots, Ant Colony Optimization, Boids)

**Biologische Vorbilder und ihre LLM-Uebersetzung:**

| Biologie / Robotik | LLM-Schwarm Aequivalent |
|---|---|
| Boids-Separation (Abstand halten) | "Vermeide Redundanz" - pruefe ob Task bereits bearbeitet wird |
| Boids-Alignment (Richtung angleichen) | "Folge dem Konsens" - orientiere dich an Entscheidungen anderer |
| Boids-Cohesion (zur Mitte bewegen) | "Bleib im Kontext" - halte Verbindung zum gemeinsamen Ziel |
| ACO-Pheromone (Spur hinterlassen) | Marker-Dateien mit Timestamps, Success-Counter |
| ACO-Verdunstung (alte Spuren verblassen) | TTL-basiertes Loeschen alter Marker nach N Stunden |
| ACO-Verstaerkung (gute Wege breiter) | Counter-Dateien inkrementieren bei wiederholtem Erfolg |
| Territoriales Verhalten (Revier markieren) | `.claimed_by_agent_X.lock` verhindert doppelte Arbeit |

**Schluesselprinzip:** Jedes Individuum kennt nur seine lokale Nachbarschaft, keine globale Sicht. Emergenz entsteht durch Interaktion simpler lokaler Regeln.

**Einfache Regeln (max 3-5 pro Agent):**
1. Wenn du eine Datei siehst die ein Problem hat → fixe es
2. Wenn du eine Datei siehst die bereits gefixt ist → gehe weiter
3. Wenn du nicht weiterkommst → wechsle das Verzeichnis
4. Hinterlasse einen Marker (Datei) wenn du fertig bist
5. Folge Verzeichnissen mit hohem `.visit_count` zuerst

**Indirekte Kommunikation (Stigmergy):**
- **Gaestebuch-Dateien**: Jeder Agent schreibt seinen Namen in `.visitors.log` im aktuellen Verzeichnis
- **Aenderungs-Erkennung**: `git status` oder Datei-Timestamps pruefen → sehen was andere geaendert haben
- **Marker-Dateien**: `.done`, `.in_progress`, `.needs_review` als Signale
- **Pheromon-Dateien**: Zaehler in `.visit_count` → haeufig besuchte Pfade werden bevorzugt
- **Gradient-Navigation**: Verzeichnistiefe = Pheromondichte (flachere Struktur = hoehere Prioritaet)

**Pheromon-Space (konkreter Vorschlag):**
```
data/swarm/                    # Zentrale Pheromon-Ablage
├── .visitors.log              # Wer war hier?
├── task_123.done              # Ergebnis-Marker
├── task_456.in_progress       # Territorium-Marker
├── path_explored.counter      # Besuchs-Zaehler (Verstaerkung)
└── needs_review.flag          # Signal-Datei (indirekte Kommunikation)
```

**Technische Fragen:**
- Weiss ein Verzeichnis wer es liest? → Ja, ueber Gaestebuch-Dateien (Agent schreibt bei Eintritt)
- Weiss ein Verzeichnis was geaendert wurde? → Ja, ueber git diff oder File-Watcher
- Koennen Agenten ohne Kommunikation zusammenarbeiten? → Ja, ueber Stigmergy (Umgebungs-Signale)
- Wie verhindern wir lokale Optima? → Pheromon-Verdunstung (alte Marker per Cron/TTL loeschen)

**Anwendung:** Grossflaechige Code-Bereinigung, Dokumentations-Vervollstaendigung, System-Heilung.

### Muster E: Schatzsuche / Swarm Health

**Zweck:** Systemgesundheit testen durch simulierte "physische" Navigation.

**Grundregel:** Agenten "gehen" durch Verzeichnisse wie durch Raeume. Sie muessen alle Dateien eines Raums lesen bevor sie den naechsten betreten.

```
Agent betritt Verzeichnis (Raum)
    → Liest ALLE Dateien im Raum
    → Prueft auf Fallen/Fehler (konfigurierbar)
    → Loest Pruefung oder meldet Fehler
    → Geht zum naechsten Raum
    → Findet Codewort? → ALLE STOPPEN
```

**Varianten:**

| Variante | Beschreibung |
|----------|-------------|
| **Schatzsuche** | Codewort in einer Systemdatei versteckt, wer es findet gewinnt |
| **Punkt-zu-Punkt** | Alle starten am selben Ort, muessen zum Zielverzeichnis kommen |
| **Zeitlimit** | Wie weit kommt jeder Agent in N Sekunden? |
| **Zangen-Maneuver** | Gruppe A startet von aussen (Root), Gruppe B von innen (Tiefe) |
| **Fallen-Parcours** | Auf jedem Weg Pruefungen (z.B. "Korrigiere diesen Fehler um weiterzugehen") |

**Fallen/Pruefungen (konfigurierbar per Prompt):**
- Syntax-Fehler in einer Datei → Agent muss korrekten Code erkennen
- Fehlende Import-Anweisung → Agent muss ergaenzen
- Falsche Konfiguration → Agent muss korrekten Wert nennen
- Quiz-Frage zum gelesenen Inhalt → Agent muss antworten

**Anwendung:** System-Audit, Onboarding-Test, Dokumentations-Qualitaet, Gamification.

---

## Referenzergebnisse

### Pilotversuch (2026-02-15)
- 10 Proben: 5 Haiku + 5 Sonnet
- **Erfolgsquote:** 100%
- **Meistbesuchte Datei:** hub/bach_paths.py (4/10)
- **Blind Spots:** connectors/ (0/10), partners/ (0/10)
- **Massnahmen:** 4 READMEs, 1 Teaching-Hook

### Grossversuch (2026-02-15)
- 100 Proben: 100 Haiku (naiv, ohne MEMORY.md/Skills)
- **53 completed, 47 timeout** (alle mit Pfaddaten)
- **966 Pfade erfasst, 894 Tool-Aufrufe, $3.54 Gesamtkosten**
- **Top-Datei:** ARCHITECTURE.md (43/100 lesen sie!)
- **Tool-Verteilung:** Bash 54%, Read 35%, Glob 9%, Grep 3%
- **Groesster Blind Spot:** help/ (0/100 trotz 93 Help-Dateien!)
- **0%-Task:** "Neuen Skill erstellen" (niemand findet _templates/)
- **100%-Tasks:** BACH starten, Logs finden, Agenten auflisten, Nachricht senden

**Massnahmen nach Grossversuch:**
- Schnellnavigation in ARCHITECTURE.md (help/, _templates/, workflows/)
- Self-Extension-Hinweis in _templates/README.md
- Script v6.0: Kein Delay, atexit-Schutz, fruehe MEMORY-Restore

### Dateien
- Launcher: `data/elephant_path_launcher.py`
- Rohdaten: `data/elephant_path_100/probe_*.json`
- Bericht: `data/elephant_path_100/report.md`
- Pilotdaten: `data/pilot_probe_results.json`

---

## Wann anwenden?

- Nach groesseren Umstrukturierungen (neue Verzeichnisse, Umbenennungen)
- Vor Onboarding neuer LLM-Partner
- Nach Hinzufuegen neuer Module/Handler
- Als Qualitaetssicherung fuer System-Dokumentation
- Regelmaessig (z.B. quartalsweise) als "UX-Audit fuer LLMs"
- Fuer Erkundung unbekannter Ordnerstrukturen (Echolot-Muster)
- Fuer zeitkritische Operationen (Single-Op-Muster)

---

## Siehe auch

- `skills/workflows/system-testverfahren.md` - B/O/E-Tests
- `skills/workflows/system-mapping.md` - System-Kartierung
- `wiki/trampelpfadanalyse.txt` - Hintergrundwissen zum Konzept
- `data/elephant_path_launcher.py` - Ausfuehrbares Experiment-Script
- `data/elephant_path_100/report.md` - Ergebnis des Grossversuchs

## Schwarm-Robotik Quellen

- Automatic design of stigmergy-based behaviours for robot swarms (Nature, 2024)
- From animal collective behaviors to swarm robotic cooperation (National Science Review, 2023)
- Ant Colony Optimization - Wikipedia
- Boids (Reynolds, 1986) - Wikipedia
- Micro/Nanorobotic Swarms: From Fundamentals to Functionalities (ACS Nano, 2023)

---
BACH Protocol v2.0 - Trampelpfadanalyse & Schwarm-Verfahren
