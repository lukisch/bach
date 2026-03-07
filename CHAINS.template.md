# BACH Toolchains

Automatically generated from the database (toolchains).

**Total:** (automatically populated)

## Trigger Types

- **event**: Reacts to system events (e.g. task_completed)
- **schedule**: Time-based execution
- **manual**: Manually triggered

## Example

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
  NOTE: This file is a template.
  BACH generates the complete list automatically from bach.db.
-->

---
🇩🇪 [Deutsche Version](CHAINS.template.de.md)
