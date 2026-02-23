# BACH ATI Policies

**Version:** 1.0.0  
**Erstellt:** 2026-01-22

## Übersicht

Dieses Verzeichnis enthält Policy-Templates für das ATI Projekt-Bootstrapping-System.
Die Policies definieren Standards und Regeln, die auf neue oder bestehende Projekte angewendet werden.

## Verfügbare Policies

| Policy | Datei | Beschreibung |
|--------|-------|--------------|
| **Naming** | `naming_policy.json` | Namenskonventionen für Dateien, Klassen, Funktionen |
| **Encoding** | `encoding_policy.json` | UTF-8 Standards, BOM-Handling, Line-Endings |
| **Path Rules** | `path_rules_policy.json` | Pfadnormalisierung, Variablen, Heilungsstrategien |

## Verwendung

### Python-Import

```python
from agents.ati._policies import load_policy, get_all_policies

# Einzelne Policy laden
naming = load_policy('naming')

# Alle Policies laden
all_policies = get_all_policies()
```

### Mit PolicyApplier (geplant - BOOTSTRAP_010)

```python
from agents.ati.tools.policy_applier import PolicyApplier

applier = PolicyApplier()
applier.validate_project("/path/to/project")
applier.apply_policies("/path/to/project", fix=True)
```

## Policy-Struktur

Jede Policy-JSON hat folgende Grundstruktur:

```json
{
  "policy_name": "Name der Policy",
  "version": "1.0.0",
  "description": "Kurzbeschreibung",
  
  / Policy-spezifische Regeln...
  
  "validation": {
    "strict_mode": false,
    "warn_on_violation": true
  }
}
```

## Erweiterung

Neue Policies können einfach hinzugefügt werden:

1. Neue `<name>_policy.json` erstellen
2. Grundstruktur mit `policy_name`, `version`, `description` 
3. Policy-spezifische Regeln definieren
4. `validation` Block hinzufügen

## Roadmap

- [ ] BOOTSTRAP_010: PolicyApplier Klasse implementieren
- [ ] Validation-Checks für jede Policy
- [ ] Auto-Fix Funktionen
- [ ] CLI: `bach ati policy check <project>`

---

*Teil des ATI Projekt-Bootstrapping-Systems (BACH v1.1)*
