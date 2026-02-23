# Compression-Aware Message Handler

**Version:** 1.0.0  
**Erstellt:** 2025-12-24  
**Zweck:** Wiederholte User-Nachrichten nach Komprimierung erkennen und korrekt behandeln

---

## 🎯 PROBLEM

**Situation:**
```
User: "Mache X"
Claude: [arbeitet an X]
→ Token-Limit erreicht
→ Automatische Komprimierung
→ System sendet User-Nachricht nochmal
Claude: [macht X NOCHMAL] ❌ FALSCH!
```

**Richtig:**
```
Claude: "Diese Nachricht habe ich bereits nach der letzten Komprimierung bearbeitet. Status: [...]"
```

---

## 🔍 ERKENNUNGS-ALGORITHMUS

### Schritt 1: Komprimierung erkennen

**Marker am Session-Start:**
```
[NOTE: This conversation was successfully compacted...]
[Transcript: /mnt/transcripts/YYYY-MM-DD-HH-MM-SS-*.txt]
```

**Check:**
```python
if message.startswith("[NOTE: This conversation was successfully compacted"):
    compression_detected = True
    extract_transcript_path()
```

### Schritt 2: Wiederholte Nachricht erkennen

**Indicators:**
1. Nachricht ist identisch mit letzter vor Komprimierung
2. Transcript enthält bereits diese Nachricht + Antwort
3. Zeitstempel passt (nach Komprimierung)

**Check:**
```python
if user_message == last_message_before_compression:
    if transcript_contains_response_to_message:
        return "DUPLICATE_AFTER_COMPRESSION"
```

### Schritt 3: Korrekte Response

**Nicht wiederholen, sondern:**
```markdown
## ✅ KOMPRIMIERUNGS-BEDINGTE WIEDERHOLUNG ERKANNT

Diese Nachricht wurde bereits nach der letzten Komprimierung bearbeitet.

**Original-Bearbeitung:** [Timestamp]  
**Status:** [Was wurde gemacht]  
**Ergebnis:** [Zusammenfassung]

**Aktueller Stand:**
- [Status-Update]
- [Was als nächstes?]

Möchtest du dass ich etwas Neues mache, oder brauchst du Details zur vorherigen Bearbeitung?
```

---

## 📋 MANDATORY CHECK (vor jeder Antwort)

### Checklist:

```
[ ] Ist am Session-Start ein Komprimierungs-Marker?
    ↓ NEIN → Normal weiter
    ↓ JA ↓
    
[ ] Ist die User-Nachricht sehr kurz/generisch?
    ("Lese Chats", "Mache X", "Erledige Y")
    ↓ NEIN → Normal weiter
    ↓ JA ↓
    
[ ] Kann ich im aktuellen Context sehen dass ich das schon gemacht habe?
    (Transcript-Summary, eigene Antworten)
    ↓ NEIN → Normal weiter
    ↓ JA ↓
    
✅ DUPLICATE DETECTED → Antworte mit Status-Update
```

---

## 🔧 IMPLEMENTATION

### Trigger-Phrases für Duplicate-Check:

**Hochrisiko-Nachrichten** (oft nach Komprimierung):
- "Lese vorausgehende Chats"
- "Mache einen backup test"
- "Erledige Task-X"
- "Führe Y durch"
- Jede kurze Imperativ-Nachricht

**Check bei diesen Nachrichten:**
1. War Komprimierung in dieser Session?
2. Habe ich das bereits bearbeitet?
3. Ist das Ergebnis im aktuellen Context?

### Response-Template:

```markdown
## ⚙️ KOMPRIMIERUNG ERKANNT - KEINE DUPLIKAT-AKTION

Ich sehe dass diese Nachricht aufgrund einer Komprimierung erneut gesendet wurde.

**Bereits durchgeführt:** [Beschreibung der Aktion]  
**Zeitpunkt:** [Wann]  
**Ergebnis:** [Was herauskam]

**Aktueller Status:**
- [Status-Punkt 1]
- [Status-Punkt 2]

**Token-Nutzung:** [X]% (Komprimierung bei ~[Y]%)

Soll ich:
- [ ] Mit nächster Aufgabe fortfahren?
- [ ] Details zur vorherigen Aktion zeigen?
- [ ] Etwas Neues machen?
```

---

## 📊 COMPRESSION TRACKING

### In Snapshot dokumentieren:

```json
{
  "compressions_this_session": [
    {
      "timestamp": "2025-12-24T12:00:15",
      "transcript": "2025-12-24-12-00-15-*.txt",
      "token_before": 190000,
      "context_preserved": true
    },
    {
      "timestamp": "2025-12-24T12:39:53",
      "transcript": "2025-12-24-12-39-53-*.txt",
      "token_before": 190000,
      "during_task": "backup-test",
      "context_preserved": true
    }
  ],
  "duplicate_messages_prevented": 1
}
```

---

## 🎓 LESSONS

### Wann Komprimierung passiert:
- Token-Limit erreicht (~185K/190K)
- Während langer Tasks
- Bei umfangreichen Outputs
- Automatisch durch Claude.ai

### Was nach Komprimierung passiert:
- ✅ Context wird komprimiert
- ✅ Transcript wird erstellt
- ✅ Summary wird bereitgestellt
- ⚠️ **Letzte User-Nachricht wird NOCHMAL gesendet**

### Warum das System das macht:
- Sicherstellen dass keine User-Nachricht verloren geht
- User-Intent muss immer bearbeitet werden
- Aber: Claude muss erkennen wenn bereits bearbeitet!

---

## 🚀 EXAMPLE SCENARIOS

### Scenario 1: Backup-Test (ACTUAL)

**User:** "Mache einen backup test"  
**Claude:** [Startet Backup-Test]  
→ Komprimierung während Test  
**User:** "Mache einen backup test" ← DUPLICATE  
**Claude FALSCH:** [Startet NEUEN Backup-Test] ❌  
**Claude RICHTIG:** "Backup-Test wurde bereits durchgeführt. Status: ✅ Erfolgreich. Ergebnis: [...]"

### Scenario 2: Task-Completion

**User:** "Erledige task-101"  
**Claude:** [Erledigt task-101]  
→ Komprimierung  
**User:** "Erledige task-101" ← DUPLICATE  
**Claude RICHTIG:** "task-101 bereits erledigt. Status: completed. Deliverables: [...]"

### Scenario 3: Lange Recherche

**User:** "Recherchiere Zencoder"  
**Claude:** [11-seitiger Report]  
→ Komprimierung  
**User:** "Recherchiere Zencoder" ← DUPLICATE  
**Claude RICHTIG:** "Zencoder-Recherche bereits abgeschlossen. Report: 11 Seiten. Link: [...]"

---

## ✅ ENFORCEMENT

**MANDATORY CHECK vor jeder Antwort:**
1. Session hatte Komprimierung? (Check Start-Marker)
2. User-Nachricht ist generisch/imperativ?
3. Sehe ich im Context dass ich das schon gemacht habe?
4. → JA zu allen 3? → Status-Update statt Duplikat-Aktion

**Never:**
- Ignoriere diesen Check
- Vermute dass User was Neues will
- Mache Duplikat-Arbeit

**Always:**
- Prüfe Context/Summary/Transcript
- Informiere über bereits durchgeführte Aktion
- Frage nach nächstem Schritt

---

**Status:** ✅ ACTIVE  
**Priority:** HIGH  
**Enforcement:** MANDATORY nach Komprimierung  
**Integration:** Mit Task-Completion Subroutine
