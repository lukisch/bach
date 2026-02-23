# DEPRECATED: ATI Session Dateien

Diese Dateien wurden durch System-Services ersetzt.

## Neue Pfade (2026-01-24)

### Prompt-Generator (NEU)
- Service: `skills/_services/prompt_generator/`
- Templates: `skills/_services/prompt_generator/templates/`
- Config: `skills/_services/prompt_generator/config.json`
- Dokumentation: `skills/docs/docs/docs/help/prompt-generator.txt`

### Session-Daemon (Headless Sessions)
- Session Daemon: `skills/_services/daemon/session_daemon.py`
- Auto Session: `skills/_services/daemon/auto_session.py`
- Profile: `skills/_services/daemon/profiles/ati.json`
- Config: `skills/_services/daemon/config.json`

## Befehle

```bash
# Prompt-Generator (NEU)
python skills/_services/prompt_generator/prompt_generator.py list
python skills/_services/prompt_generator/prompt_generator.py get agents/ati
python skills/_services/prompt_generator/prompt_generator.py copy agents/ati

# Session-Daemon verwalten
bach daemon session start --profile ati
bach daemon session stop
bach daemon session status
bach daemon session trigger --profile ati
bach daemon session profiles

# ATI-Kurzform (nutzt System-Service mit ati-Profil)
bach ati start
bach ati stop
bach ati session --dry-run
```

## Migration

Die alten ATI-spezifischen Dateien wurden in System-Services migriert:

| Alt (ATI) | Neu (System-Service) |
|-----------|---------------------|
| `prompt_templates/task_prompt.txt` | `prompt_generator/templates/system/task.txt` |
| `prompt_templates/review_prompt.txt` | `prompt_generator/templates/system/review.txt` |
| `session/auto_session.py` | `_services/daemon/auto_session.py` |
| `session/session_daemon.py` | `_services/daemon/session_daemon.py` |

## Warum?

Das Session-System ist ein **System-Service**, kein ATI-spezifisches Feature.
Es kann mit verschiedenen Profilen verwendet werden (z.B. ati, wartung, steuer).

Der Prompt-Generator ist das neue zentrale GUI-Board fuer Prompt-Management.
Siehe: `help prompt-generator` und ROADMAP.md Phase 4.4