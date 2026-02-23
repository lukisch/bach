# 📋 Gemini Delegations-Vorlage

> Diese Datei zeigt das Format für Aufgaben, die an Gemini delegiert werden.

## Template

```markdown
# 🔷 Gemini-Aufgabe: [Kurztitel]

**Erstellt:** [Datum]
**Priorität:** [Hoch/Mittel/Niedrig]
**Erwartet bis:** [optional]

## Aufgabe

[Klare Beschreibung was Gemini tun soll]

## Kontext

[Relevante Hintergrundinformationen]
[Ggf. Dateien die beigefügt werden sollen]

## Erwartetes Ergebnis

- [ ] [Konkretes Ergebnis 1]
- [ ] [Konkretes Ergebnis 2]

## Format der Antwort

[Wie soll Gemini antworten? Text, Liste, Tabelle, etc.]

---

**Ergebnis hier einfügen oder als .txt in outbox/ ablegen**
```

## Beispiel-Aufgaben für Gemini

### Deep Research
```markdown
# 🔷 Gemini-Aufgabe: Recherche zu [Thema]

Nutze Gemini Deep Research um folgendes zu untersuchen:
- [Aspekt 1]
- [Aspekt 2]

Erwartetes Ergebnis: Zusammenfassung mit Quellen
```

### Faktencheck
```markdown
# 🔷 Gemini-Aufgabe: Faktencheck

Prüfe folgende Behauptung auf Korrektheit:
"[Behauptung]"

Erwartetes Ergebnis: Bestätigung/Widerlegung mit Quellen
```

### Lange Dokument-Analyse
```markdown
# 🔷 Gemini-Aufgabe: Dokument analysieren

Analysiere beigefügtes Dokument (nutze Geminis 1M Context):
- Kernaussagen extrahieren
- Widersprüche identifizieren
- Zusammenfassung erstellen

Datei: [Dateipfad oder Inhalt]
```

### Alternative Perspektive
```markdown
# 🔷 Gemini-Aufgabe: Zweite Meinung

Claude hat folgende Analyse erstellt:
[Claude's Analyse]

Bitte Gemini um:
- Kritische Prüfung
- Ergänzungen
- Alternative Sichtweisen
```

## Workflow

1. Claude erstellt Task nach diesem Template
2. Task wird in `inbox/` gespeichert
3. User öffnet Task, führt in Gemini aus
4. Ergebnis in `outbox/` ablegen oder direkt in Chat einfügen
5. Claude verarbeitet Ergebnis
