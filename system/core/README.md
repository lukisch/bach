# core/ - BACH Kern-Infrastruktur

Low-Level Infrastruktur die von allen anderen BACH-Komponenten genutzt wird. Diese Dateien nur mit Vorsicht aendern.

## Module

| Datei | Zweck |
|-------|-------|
| `db.py` | Datenbank-Verwaltung (SQLite Connection, Schema-Loading) |
| `registry.py` | Tool/Skill-Registry (Auto-Discovery, Registrierung) |
| `adapter.py` | Adapter-Pattern fuer externe Systeme |
| `agent_runtime.py` | Agent-Laufzeitumgebung |
| `aliases.py` | Befehlskuerzel (z.B. `t` -> `task`) |
| `app.py` | App-Initialisierung |
| `base.py` | Basis-Klassen und Utilities |
| `capabilities.py` | Capability-System (Feature-Flags) |
| `hooks.py` | Hook-System (Pre/Post-Execution) |
| `launcher.py` | BACH Launcher (Startup-Sequenz) |
| `plugin_api.py` | Plugin-API fuer Erweiterungen |

## Verwendung

```python
# Datenbank-Zugriff (intern)
from core.db import get_connection

# Registry
from core.registry import ToolRegistry

# Aliases
from core.aliases import resolve_alias
```

## Wichtig

- `db.py` verwaltet die Verbindung zu `data/bach.db`
- Fuer normalen Zugriff auf Tasks/Memory/Lessons: `bach_api` verwenden, nicht `core.db`
- `registry.py` wird beim Startup automatisch geladen

---
*Kern-Infrastruktur, selten direkt genutzt*
