# ATI Wiederverwendbare Module

> Standalone-faehige Module fuer Projekt-Bootstrapping

## Verfuegbare Module

| Modul | Funktion | Quelle |
|-------|----------|--------|
| `distribution.py` | Tier-System, Siegel, Versionierung | BACH skills/tools/distribution_system.py |
| `path_healer.py` | Pfad-Selbstheilung | *(planned - Task BOOTSTRAP_005)* |
| `encoding.py` | UTF-8, BOM-Handling | BACH Best-Practices (Task BOOTSTRAP_007 ✓) |

## Verwendung

```python
# Tier-Klassifizierung
from modules.distribution import classify_file
tier = classify_file(Path("src/core/main.py"))  # -> 'kernel'

# Siegel erstellen
from modules.distribution import SiegelManager
siegel = SiegelManager(project_root)
hashes = siegel.create_siegel([file1, file2])
siegel.save_siegel(hashes)

# Version erhoehen
from modules.distribution import bump_version
new_version = bump_version("1.2.3", "minor")  # -> "1.3.0"
```

## Design-Prinzipien

1. **Standalone**: Keine Abhaengigkeiten zu BACH-Core
2. **Minimal**: Nur wesentliche Funktionen
3. **Injizierbar**: Kann in beliebige Projekte kopiert werden
4. **Dokumentiert**: Docstrings und Beispiele

## Erstellt

- **Datum**: 2026-01-22
- **Von**: ATI Project Bootstrapping System
- **Task**: BOOTSTRAP_006