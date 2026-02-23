# 📋 Copilot Delegations-Vorlagen

> Microsoft 365 Copilot - 60 AI-Credits/Monat

## Deine Limits

| Feature | Limit | Reset |
|---------|-------|-------|
| AI-Credits (Office) | 60/Monat | Monatsanfang |
| Deep Research | 15/Monat | Monatsanfang |
| Vision | 10 Min/Tag | Täglich |
| Voice | 30 Min/Tag | Täglich |

## Prompt-Stil für Copilot

```
✓ KURZ & DIREKT
✓ Konkrete Zahlen nennen
✓ Imperative Befehle
✗ Lange Erklärungen vermeiden
✗ Kein übermäßiger Kontext
```

## Templates nach App

### 📝 Copilot in Word

```markdown
# 🔷 Copilot Word: [Kurztitel]

**Prompt:**
"[Aktion] dieses Dokument. Erstelle [Anzahl] [Format]. 
Fokus auf [Aspekte]. Maximal [Länge] pro Punkt."

**Beispiele:**
- "Fasse zusammen in 5 Bullet Points. Fokus auf Kernaussagen."
- "Schreibe formeller um. Behalte die Struktur bei."
- "Erweitere den Abschnitt zu [Thema] um 200 Wörter."
```

### 📊 Copilot in Excel

```markdown
# 🔷 Copilot Excel: [Kurztitel]

**Prompt:**
"Erstelle eine Formel für [Berechnung] in [Bereich]."
"Analysiere diese Daten und zeige [Metrik]."
"Erstelle ein [Diagrammtyp] aus [Datenbereich]."

**Beispiele:**
- "Summiere Spalte B für alle Zeilen wo A = 'Verkauf'"
- "Erstelle Pivot-Tabelle: Umsatz nach Monat und Region"
- "Finde Ausreißer in den Verkaufszahlen"
```

### 📧 Copilot in Outlook

```markdown
# 🔷 Copilot Outlook: [Kurztitel]

**Prompt:**
"Verfasse eine [Ton] Antwort. [Kerninhalt]. Halte es [Länge]."
"Fasse diesen E-Mail-Thread zusammen. Wichtig: [Fokus]."

**Beispiele:**
- "Antworte professionell, bestätige den Termin am Freitag"
- "Fasse zusammen: Wer soll was bis wann tun?"
- "Schreibe höfliche Absage, biete Alternative nächste Woche"
```

### 📽️ Copilot in PowerPoint

```markdown
# 🔷 Copilot PowerPoint: [Kurztitel]

**Prompt:**
"Erstelle [Anzahl] Folien zu [Thema]. Stil: [Beschreibung]."
"Füge Folie hinzu: [Inhalt]. Design: [Stil]."

**Beispiele:**
- "Erstelle 5 Folien zu Q4-Ergebnissen. Professionell, mit Zahlen."
- "Füge Agenda-Folie am Anfang hinzu"
- "Vereinfache Folie 3, zu viel Text"
```

### 📓 Copilot in OneNote

```markdown
# 🔷 Copilot OneNote: [Kurztitel]

**Prompt:**
"Erstelle To-Do-Liste aus diesen Notizen."
"Strukturiere diese Informationen als [Format]."

**Beispiele:**
- "Extrahiere alle Aktionspunkte als Checkliste"
- "Fasse Meeting-Notizen in 5 Punkten zusammen"
```

## Universal-Template

```markdown
# 🔷 Copilot-Aufgabe: [Titel]

**App:** [Word/Excel/Outlook/PowerPoint/OneNote]
**Erstellt:** [Datum]

## Prompt (kopieren)

"[Fertiger Prompt hier]"

## Kontext (falls nötig)

[Zusätzliche Infos für den User]

## Ergebnis

[ ] In outbox/ ablegen oder hier einfügen
```

## Copilot vs. Gemini - Wann was?

| Aufgabe | Copilot | Gemini |
|---------|---------|--------|
| Office-Dokument bearbeiten | ✅ Nativ | ❌ |
| E-Mail-Entwurf in Outlook | ✅ | ⚠️ Copy-paste |
| Excel-Formeln | ✅ Direkt einfügen | ❌ |
| Lange Recherche | ⚠️ 15/Monat | ✅ Unbegrenzt |
| PDF analysieren | ⚠️ | ✅ 1M Context |
| Bilder verstehen | ✅ Vision | ✅ Vision |
| Code schreiben | ⚠️ | ⚠️ (Claude besser) |

## Credits sparen

1. **Bulk-Aktionen vermeiden** - Jede Aktion = 1 Credit
2. **Prompts optimieren** - Beim ersten Mal richtig
3. **Für große Aufgaben Gemini nutzen** - Kein Credit-Limit
4. **Einfaches an Ollama** - €0 Kosten
