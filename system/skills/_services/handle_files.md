---
name: handle_files
metadata:
  version: 1.0.0
  last_updated: 2025-12-22
description: >
  Datei-Operationen mit Sicherheitsregeln.
  Schützt vor versehentlichem Datenverlust.
---

# Handle Files - Datei-Management

> **📁 Sichere Datei-Operationen mit Schutzregeln**

---

## Konzept

Dieser Skill definiert:
1. **Sicherheitsregeln** für Datei-Operationen
2. **Backup-Pflicht** vor destruktiven Aktionen
3. **Berechtigungszonen** wo Claude agieren darf

---

## Sicherheitszonen

| Zone | Pfad | Berechtigung |
|------|------|--------------|
| **BACH-Ordner** | `<BACH_ROOT>/` | Volle Kontrolle |
| **Workspace** | `recludOS\Workspace\` | Frei nutzbar |
| **Extern** | Alles andere | Backup-Pflicht! |

---

## Sicherheitsregeln (security_rules/)

### Regel 1: Backup vor Löschen

```
WENN Löschung AUSSERHALB RecludOS-Ordner:
    → ERST Backup auf NAS erstellen
    → DANN löschen
```

### Regel 2: Papierkorb nutzen

```
WENN Löschen in Workspace:
    → Nach Workspace/Papierkorb verschieben
    → NICHT sofort löschen
```

### Regel 3: Bestätigung bei Masse

```
WENN mehr als 10 Dateien betroffen:
    → User um Bestätigung bitten
```

---

## Komponenten

| Komponente | Pfad | Funktion |
|------------|------|----------|
| **security_rules** | security_rules/ | Sicherheitsregeln |
| **skills** | skills/ | Datei-bezogene Sub-Skills |

---

## Befehle

| Befehl | Aktion |
|--------|--------|
| "Räume Workspace auf" | Kategorisieren, Duplikate entfernen |
| "Papierkorb leeren" | In Systempapierkorb verschieben |
| "Sichere bevor..." | Explizites Backup |

---

## Integration

- **self_backup**: Führt Backups durch
- **directory-watcher**: Überwacht Änderungen
- **security-backup**: Legacy-Kompatibilität

---

## NAS-Backup-Pfad

```
\NAS-HOST\fritz.nas\Extreme_SSD\BACKUP\Claude_Backups\
```
