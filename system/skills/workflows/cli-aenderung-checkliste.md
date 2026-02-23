# CLI-Änderungs-Checkliste

**Version:** 1.0  
**Stand:** 2026-01-22  
**Kategorie:** Wartung, Entwicklung

---

## Übersicht

Dieser Workflow beschreibt alle Schritte die nötig sind wenn ein neuer CLI-Befehl eingeführt oder ein bestehender geändert wird.

```
┌─────────────────────────────────────────────────────────┐
│  NEUER CLI-BEFEHL: CHECKLISTE (6 Schritte)              │
├─────────────────────────────────────────────────────────┤
│  1. Handler implementieren (hub/handlers/)              │
│  2. In bach.py registrieren                             │
│  3. Help-Datei erstellen (skills/docs/docs/docs/help/*.txt)                   │
│  4. KNOWN_COMMANDS aktualisieren                        │
│  5. SKILL.md Befehlsübersicht aktualisieren             │
│  6. Test: --help und Funktion prüfen                    │
└─────────────────────────────────────────────────────────┘
```

**Dauer:** 10-30 Minuten je nach Komplexität

---

## Schritt 1: Handler implementieren

**Ort:** `hub/handlers/<name>.py`

### Vorlage

```python
"""Handler für <name> Funktionen."""
from hub.handlers.base import BaseHandler

class <Name>Handler(BaseHandler):
    def handle(self, args: list) -> tuple:
        if not args:
            return self._show_help()
        
        operation = args[0].lower()
        
        if operation == "list":
            return self._list(args[1:])
        elif operation == "add":
            return self._add(args[1:])
        else:
            return False, f"Unbekannte Operation: {operation}"
    
    def _show_help(self) -> tuple:
        return True, "Nutzung: bach <name> [operation]"
    
    def _list(self, args: list) -> tuple:
        # Implementierung
        return True, "Liste..."
```

### Checkliste

```
□ Klasse von BaseHandler ableiten
□ handle() Methode implementiert
□ Operationen als Untermethoden
□ Hilfe bei leeren Args
□ Fehlerbehandlung
```

---

## Schritt 2: In bach.py registrieren

**Ort:** `bach.py` (zwei Stellen!)

### A) Handler-Import (get_handler Funktion)

```python
# In get_handler() ca. Zeile 800-900:
handler_imports = {
    # ... bestehende ...
    "<name>": lambda: _import_handler("<name>", "<Name>Handler"),
}
```

### B) Subcommand elif-Block

```python
# In main() ca. Zeile 1000-1100:
elif command == "<name>":
    handler = get_handler("<name>")
    if handler:
        return handler.handle(args[2:])
```

### Checkliste

```
□ Handler in handler_imports registriert
□ elif-Block für Subcommand ohne --
□ Beide Varianten funktionieren: bach <name> UND bach --<name>
```

---

## Schritt 3: Help-Datei erstellen

**Ort:** `skills/docs/docs/docs/help/<name>.txt`

### Vorlage

```
<NAME> - <Kurzbeschreibung>
============================

BESCHREIBUNG
------------
<Was macht dieser Befehl?>

BEFEHLE
-------
  bach <name> list          <Beschreibung>
  bach <name> add <args>    <Beschreibung>
  bach <name> status        <Beschreibung>

BEISPIELE
---------
  # Beispiel 1
  bach <name> list

  # Beispiel 2
  bach <name> add "Etwas"

TECHNISCHE DETAILS
------------------
  Handler: hub/handlers/<name>.py
  DB-Tabelle: (falls relevant)
  Config: (falls relevant)

SIEHE AUCH
----------
  bach --help <verwandt>
  bach --help tasks
```

### Checkliste

```
□ Datei in skills/docs/docs/docs/help/<name>.txt erstellt
□ Alle Operationen dokumentiert
□ Beispiele vorhanden
□ SIEHE AUCH verweist auf relevante Themen
```

---

## Schritt 4: KNOWN_COMMANDS aktualisieren

**Ort:** `bach.py` ca. Zeile 855

```python
KNOWN_COMMANDS = [
    # Subcommands (ohne --)
    "task", "mem", "backup", "restore", "dist", "partner",
    "gui", "daemon", "scan", "lesson", "wiki", "tools",
    "msg", "steuer", "ati", "abo", "ocr", "data",
    "<name>",  # NEU HINZUFÜGEN
    
    # Handler (mit --)
    "--help", "--startup", "--shutdown", ...
]
```

### Zweck

- Did-you-mean Funktion findet ähnliche Befehle
- Vollständige Befehlsliste für Dokumentation

---

## Schritt 5: SKILL.md aktualisieren

**Ort:** `SKILL.md` Befehlsübersicht

### Relevante Sektionen

1. **Hauptübersicht** (ca. Zeile 50-150):
   ```markdown
   ## <Kategorie>
   ```bash
   bach <name> list     # Beschreibung
   bach <name> add      # Beschreibung
   ```

2. **Version erhöhen** (Header):
   ```markdown
   **Version:** 1.1.XX (was +1)
   ```

### Checkliste

```
□ Befehl in passende Kategorie eingetragen
□ Version in SKILL.md erhöht
□ Changelog in SKILL.md ergänzt (falls major)
```

---

## Schritt 6: Test

### Manuelle Tests

```bash
# Help funktioniert?
bach --help <name>

# Beide Varianten?
bach <name> list
bach --<name> list

# Did-you-mean bei Tippfehler?
bach <nam> list  # Sollte "<name>" vorschlagen

# Operationen funktionieren?
bach <name> add "Test"
bach <name> status
```

### Automatischer Test (optional)

```bash
# Konsistenz-Check
bach --maintain registry check
```

---

## Schnell-Checkliste (Kopiervorlage)

```
NEUER CLI-BEFEHL: <name>
========================

□ hub/handlers/<name>.py erstellt
□ bach.py: handler_imports erweitert
□ bach.py: elif-Block für Subcommand
□ skills/docs/docs/docs/help/<name>.txt erstellt
□ KNOWN_COMMANDS in bach.py ergänzt
□ SKILL.md Befehlsübersicht aktualisiert
□ SKILL.md Version erhöht
□ Test: bach --help <name>
□ Test: bach <name> [operation]
□ Test: bach --<name> [operation]
□ Test: Tippfehler -> Did-you-mean
```

---

## Automatisierung

### Mögliche Verbesserungen

1. **Generator-Script:**
   ```bash
   bach --maintain generate handler <name>
   ```
   → Erstellt Boilerplate für Handler + Help

2. **Konsistenz-Check:**
   ```bash
   bach --maintain integration
   ```
   → Prüft Help ↔ Handler Abgleich

3. **Pre-Commit Hook:**
   → Warnt wenn Handler ohne Help commited wird

---

## Siehe auch

- `skills/workflows/system-anschlussanalyse.md` - Allgemeine Konsistenz
- `skills/docs/docs/docs/help/cli.txt` - CLI-Konventionen
- `skills/docs/docs/docs/help/coding.txt` - Coding-Standards
- `skills/docs/docs/docs/help/naming.txt` - Namenskonventionen

---

*Erstellt: 2026-01-22 | Anlass: Standardisierung CLI-Entwicklung*