# BACH Toolchains

Automatisch generiert aus der Datenbank (toolchains).
Letzte Aktualisierung: 2026-03-01 22:28

**Total:** 5 Toolchains

## Trigger: event

### ✓ after_task_done

**Trigger Value:** task_completed

**Last Run:** 2026-01-30 06:36:27

**Steps:**
```json
[{"tool": "task", "args": ["list", "--status", "open", "--prio", "P1"]}, {"tool": "--memory", "args": ["store", "--type", "lesson", "--auto"]}]
```

## Trigger: manual

### ✓ SafeChain

**Last Run:** 2026-01-28 09:25:59

**Steps:**
```json
[{"tool":"help","args":["cli"]}]
```

### ✓ session_start

**Last Run:** 2026-01-30 06:31:11

**Steps:**
```json
[{"tool": "msg", "args": ["ping", "--from", "claude"]}, {"tool": "msg", "args": ["ping", "--from", "gemini"]}, {"tool": "task", "args": ["list", "--prio", "P1"]}, {"tool": "--status", "args": []}]
```

## Trigger: time

### ✓ nightly_maintenance

**Trigger Value:** 02:00

**Steps:**
```json
[{"tool": "scan", "args": ["run", "--mode", "quick"]}, {"tool": "--consolidate", "args": ["run"]}, {"tool": "task", "args": ["list", "--status", "open"]}]
```

### ✓ weekly_backup

**Trigger Value:** sunday_03:00

**Steps:**
```json
[{"tool": "scan", "args": ["run", "--mode", "full"]}, {"tool": "--status", "args": ["--format", "json"]}]
```
