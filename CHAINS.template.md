# BACH Toolchains

Automatisch generiert aus der Datenbank (toolchains).

**Total:** (wird automatisch befuellt)

## Trigger-Typen

- **event**: Reagiert auf System-Events (z.B. task_completed)
- **schedule**: Zeitgesteuerte Ausfuehrung
- **manual**: Manuell ausgeloest

## Beispiel

### after_task_done

**Trigger:** task_completed
**Steps:**
```json
[
  {"tool": "task", "args": ["list", "--status", "open"]},
  {"tool": "--memory", "args": ["store", "--type", "lesson", "--auto"]}
]
```

---

<!--
  HINWEIS: Diese Datei ist ein Template.
  BACH generiert die vollstaendige Liste automatisch aus bach.db.
-->
