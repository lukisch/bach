# BACH Maintenance Tools

Interne Tools für System-Wartung, Synchronisation und Monitoring.

## Enthaltene Tools

| Tool | Zweck |
|------|-------|
| `archive_done_tasks.py` | Erledigte Tasks archivieren |
| `create_boot_checks.py` | Boot-Checks erstellen |
| `generate_skills_report.py` | Skills-Report generieren |
| `register_skills.py` | Skills in DB registrieren |
| `registry_watcher.py` | Registry überwachen |
| `skill_health_monitor.py` | Skill-Gesundheit prüfen |
| `sync_skills.py` | Skills synchronisieren |
| `sync_utils.py` | Sync-Hilfsfunktionen |
| `task_statistics.py` | Task-Statistiken |
| `tool_discovery.py` | Tools automatisch entdecken |
| `tool_registry_boot.py` | Tool-Registry beim Boot |

## Nutzung via CLI

Die meisten Tools sind über `bach --maintain` erreichbar:

```bash
bach --maintain scan
bach --maintain list
```

---

*BACH v1.1 - Maintenance Tools*
