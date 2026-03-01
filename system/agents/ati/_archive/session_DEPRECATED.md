# DEPRECATED: ATI Session Dateien

Diese Dateien wurden durch System-Services ersetzt.

## Neue Pfade (2026-01-24)

### Prompt-Generator (NEU)
- Service: `skills/_services/prompt_generator/`
- Templates: `skills/_services/prompt_generator/templates/`
- Config: `skills/_services/prompt_generator/config.json`
- Dokumentation: `skills/docs/docs/docs/docs/help/prompt-generator.txt`

### Session-Daemon (Headless Sessions) -- DEPRECATED
- Session Daemon: `hub/_services/daemon/session_daemon.py` (legacy)
- Auto Session: `hub/_services/daemon/auto_session.py` (legacy)
- Profile: `hub/_services/daemon/profiles/ati.json` (legacy)

### llmauto Chains (NEU, empfohlen)
- ATI-Chain: `tools/llmauto/chains/session_ati.json`
- Wartungs-Chain: `tools/llmauto/chains/session_wartung.json`
- Finanz-Mail-Chain: `tools/llmauto/chains/session_financial_mail.json`

## Befehle

```bash
# llmauto Chains (NEU, empfohlen)
bach chain start session_ati
bach chain stop session_ati
bach chain status session_ati
bach chain list

# Legacy Session-Daemon (deprecated)
bach daemon session start --profile ati
bach daemon session stop
bach daemon session status
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