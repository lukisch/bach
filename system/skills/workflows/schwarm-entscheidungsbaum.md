# Schwarm-Entscheidungsbaum: Wann welches Muster?

**Version:** 1.0 | **Stand:** 2026-02-22 | **Bezug:** MASTERPLAN SQ051

## Entscheidungsbaum

```
Aufgabe gegeben
    |
    +-- Ist die Aufgabe parallelisierbar?
    |       |
    |       +-- NEIN --> Einzelagent (kein Schwarm)
    |       |            Einsatz: Kreatives Schreiben, komplexe Analyse,
    |       |            Aufgaben mit starken Abhaengigkeiten
    |       |
    |       +-- JA --> Sind alle Teilaufgaben gleich (homogen)?
    |                   |
    |                   +-- JA --> Epstein-Methode (Chunk-Schwarm)
    |                   |         Chunk-Groesse: 20-30 Aufgaben/Agent
    |                   |
    |                   +-- NEIN --> Braucht es Koordination zwischen Agenten?
    |                               |
    |                               +-- NEIN --> Stigmergy-Schwarm
    |                               |           (Pheromon-basiert, dezentral)
    |                               |
    |                               +-- JA --> Hierarchie-Schwarm (Boss+Worker)
    |                                         Boss koordiniert, Worker spezialisiert
    |
    +-- Qualitaetssicherung besonders wichtig?
            |
            +-- JA --> Konsensus-Schwarm (3 Agenten, Mehrheit)
            |          ACHTUNG: 3x Kosten
            |
            +-- Verschiedene Fachgebiete benoetigt?
                    |
                    +-- JA --> Spezialist-Schwarm (BACH Boss-System)
                               Routing via Aufgaben-Analyse
```

## Entscheidungs-Checkliste

Bevor du einen Schwarm startest, beantworte:

1. **Parallelisierbar?** Koennen Teilaufgaben unabhaengig voneinander bearbeitet werden?
2. **Homogen?** Sind alle Teilaufgaben vom gleichen Typ?
3. **Koordination noetig?** Muessen Zwischenergebnisse aufeinander abgestimmt werden?
4. **Kritikalitaet?** Wie schlimm ist ein Fehler in einem Teilergebnis?
5. **Budget?** Konsensus-Schwarm kostet 3x — lohnt es sich?

## Kostenmatrix

| Muster | Kosten-Faktor | Qualitaets-Gewinn | Empfehlung |
|--------|--------------|------------------|------------|
| Epstein | 1x (pro Task) | Gleichwertig | Fuer repetitive Tasks (Uebersetzung, Review) |
| Hierarchie | 1.5x | +20% | Fuer komplexe Projekte mit Abhaengigkeiten |
| Stigmergy | 1x (selbst-regulierend) | +10% | Exploration, Optimierung |
| Konsensus | 3x | +30% | Kritische Entscheidungen (Release, Diagnose) |
| Spezialist | 1x | +25% | Standard-BACH (Boss-System bereits implementiert) |

## Praktische Heuristiken

### Wann Epstein?
- Mehr als 10 gleichartige Aufgaben
- Keine Abhaengigkeiten zwischen Teilaufgaben
- Zeitdruck (parallele Ausfuehrung spart Zeit)

### Wann Hierarchie?
- Komplexes Projekt mit Meilensteinen
- Einige Tasks haengen von anderen ab
- Mensch-in-der-Schleife gewuenscht (Boss als Checkpoint)

### Wann Stigmergy?
- Unbekanntes Terrain (Exploration)
- Kein klarer Algorithmus bekannt
- System soll sich selbst optimieren

### Wann Konsensus?
- Medizinische oder rechtliche Entscheidungen
- Release-Entscheidungen (funktioniert es wirklich?)
- Wenn ein einzelner Agent bekannt unkonsistent ist

### Wann Spezialist?
- Fast immer die beste Wahl fuer BACH
- Boss-Agenten kennen ihr Fachgebiet besser als Generalisten
- Routing ist automatisch via BACH-Registry

## BACH-Integration

```bash
# Epstein-Schwarm starten (konzeptuell):
bach task add "Schwarm: Uebersetzung 100 Dokumente" --type epstein --chunk-size 20

# Hierarchie-Schwarm:
bach agent run "Projektleiter-Aufgabe" --mode hierarchical

# Spezialist-Routing (automatisch):
bach task add "Steuerfrage bearbeiten"
# -> BACH routet automatisch an STEUER-Boss
```

---

*Erstellt: SQ051 Schwarm-Protokolle | Begleit-Datei: schwarm-operationen.md*
