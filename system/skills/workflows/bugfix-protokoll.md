# Bugfix-Protokoll für Python/PyQt6 Projekte

> **Ziel:** Systematisches Vorgehen bei Bugs, um Zeit zu sparen und bekannte Probleme schnell zu erkennen.

---

## Phase 1: Schnell-Checks (< 2 Minuten)

### 1.1 Fehlermeldung analysieren
```
Fehlertyp              | Wahrscheinliche Ursache
-----------------------|------------------------------------------
ModuleNotFoundError    | Import-Pfad, fehlende Dependency
AttributeError         | Tippfehler, fehlende Initialisierung
ImportError            | Circular Import, falscher Modulname
Access Violation       | PyQt6: QObject vor QApplication
Silent Crash (kein Output) | PyQt6: QObject/Signal Problem
TypeError              | Falsche Argumente, Signatur-Mismatch
```

### 1.2 Exit-Code prüfen (Windows)
```
Exit-Code          | Bedeutung
-------------------|------------------------------------------
0                  | Erfolg
1                  | Allgemeiner Fehler
-1073740791        | Access Violation (0xC0000005) → PyQt6!
-1073741819        | Access Violation (0xC0000005) → PyQt6!
```

**Bei Access Violation → Direkt zu Phase 2.2 (c_method_analyzer)**

---

## Phase 2: DEV_TOOLS einsetzen (2-10 Minuten)

### 2.1 Import-Diagnose
```bash
python c_import_diagnose.py "<projekt>/src"
```
**Prüft:** Circular Imports, fehlende Module, __init__.py Probleme

### 2.2 Code-Analyse (WICHTIG bei PyQt6!)
```bash
python c_method_analyzer.py "<datei>.py"
```
**Prüft:**
- ✅ Attribut vor Definition (`self.x` verwendet bevor `self.x = ...`)
- ✅ Signal-Callbacks (`.connect(self.x)` → existiert x?)
- ✅ Underscore-Mismatches (`_show_x` vs `show_x`)
- ✅ Ungenutzte/fehlende Definitionen

**Typische Findings die auf PyQt6-Bugs hinweisen:**
```
[KRITISCH] ATTRIBUT VOR DEFINITION VERWENDET
  self._initialized (Zeile X): Erst in Zeile Y definiert
```
→ **Singleton-Pattern mit QObject ist fehlerhaft!**

### 2.3 Weitere Tools je nach Bedarf
| Tool | Anwendungsfall |
|------|----------------|
| `c_code_search.py` | String/Pattern in Projekt suchen |
| `c_dependency_check.py` | Fehlende pip-Pakete |
| `c_syntax_check.py` | Syntax-Fehler vor Ausführung |

---

## Phase 3: Isoliertes Testen (5-15 Minuten)

### 3.1 Minimales Reproduktions-Script
```python
# test_minimal.py
import sys
sys.path.insert(0, r"<projekt_pfad>")

print("[1] Import X...", flush=True)
from module import X
print("    OK", flush=True)

print("[2] Instanziieren...", flush=True)
obj = X()
print("    OK", flush=True)
```

### 3.2 Bei PyQt6: QApplication zuerst!
```python
from PyQt6.QtWidgets import QApplication
app = QApplication(sys.argv)  # MUSS vor allen QObject-Imports!

# Dann erst eigene Module
from myapp.gui import MainWindow
```

### 3.3 Schrittweise Eingrenzung
1. Modul-für-Modul testen
2. Methode-für-Methode in __init__ testen
3. Zeile-für-Zeile wenn nötig

**Log in Datei schreiben** bei Silent Crashes:
```python
def log(msg):
    print(msg, flush=True)
    with open("debug.log", "a") as f:
        f.write(msg + "\n")
```

---

## Phase 4: Websuche (nur wenn Phase 1-3 nicht helfen)

### 4.1 Wann Websuche?
- ✅ Unbekannte Fehlermeldung
- ✅ Framework-spezifisches Problem (PyQt6, asyncio, etc.)
- ✅ Plattform-spezifisch (Windows vs Linux)
- ❌ Nicht bei offensichtlichen Tippfehlern
- ❌ Nicht bei Logik-Fehlern im eigenen Code

### 4.2 Effektive Suchbegriffe
```
"<Fehlermeldung>" site:stackoverflow.com
"<Fehlermeldung>" site:github.com/issues
PyQt6 "<Symptom>" crash
Python "<Modul>" "<Fehlertyp>"
```

### 4.3 Gute Quellen
1. **StackOverflow** - Konkrete Lösungen
2. **GitHub Issues** - Bekannte Bugs in Libraries
3. **Qt Forum** - PyQt6-spezifisch
4. **Python Docs** - Offizielle Dokumentation

---

## Phase 5: Eigenes Diagnose-Tool (nur bei wiederkehrenden Problemen)

### 5.1 Wann eigenes Tool?
- ✅ Problem tritt in mehreren Projekten auf
- ✅ Manuelle Prüfung dauert > 5 Minuten
- ✅ Prüfung kann automatisiert werden
- ❌ Einmaliges, projekt-spezifisches Problem

### 5.2 Tool-Entwicklung
1. **Minimal starten** - Nur das Nötigste
2. **In DEV_TOOLS speichern** - `c_<name>.py`
3. **In python_tools.json registrieren**
4. **README/Docstring** - Wann/wie verwenden

### 5.3 Registrierung
```json
/ python_tools.json
{
  "name": "c_mein_tool",
  "description": "...",
  "usage": "python c_mein_tool.py <args>",
  "category": "diagnose"
}
```

---

## Phase 6: Exit-Strategie (20-Minuten-Regel)

> **Kernregel:** Nach 20 Minuten ohne Fortschritt → STOPPEN und DOKUMENTIEREN

### 6.1 Wann aufhören?

| Situation | Aktion |
|-----------|--------|
| Bug gelöst | ✅ Kurze Dokumentation, weiterarbeiten |
| Fortschritt erkennbar | ⏳ Weitermachen, aber Zeitlimit beachten |
| 20 Min ohne Fortschritt | 🛑 STOP → Bug-Report erstellen |
| Hartnäckiger Bug | 📝 Detaillierten Report, später fortsetzen |

### 6.2 Warum dokumentieren statt weitermachen?

- **Negative Ergebnisse sind Ergebnisse** - "X ist nicht die Ursache" ist wertvoll
- **Verhindert Doppelarbeit** - Nächste Session fängt nicht bei 0 an
- **Ermöglicht Tool-Entwicklung** - Aus Report kann Diagnose-Tool entstehen
- **Frische Perspektive** - Nach Pause sieht man oft die Lösung

### 6.3 Was dokumentieren?

```
✅ WAS GETESTET WURDE
✅ WAS AUSGESCHLOSSEN WURDE (negative Ergebnisse!)
✅ WO DER CRASH-PUNKT LIEGT (falls bekannt)
✅ WELCHE TOOLS VERWENDET WURDEN + OUTPUT
✅ HYPOTHESEN die noch zu prüfen sind
```

---

## Bug-Report Template (für ungelöste/komplexe Bugs)

```markdown
# Bug-Report: [Projekt] - [Kurzbeschreibung]

**Status:** 🔴 OFFEN | 🟡 IN ARBEIT | 🟢 GELÖST
**Priorität:** KRITISCH | HOCH | MITTEL | NIEDRIG
**Erstellt:** YYYY-MM-DD
**Zuletzt bearbeitet:** YYYY-MM-DD

---

## 1. Symptom

**Fehlermeldung:**
```
[Exakte Fehlermeldung hier einfügen]
```

**Exit-Code:** [z.B. -1073740791]
**Wann tritt es auf:** [Start / Bei Aktion X / Zufällig]
**Reproduzierbar:** JA / MANCHMAL / NEIN

---

## 2. Durchgeführte Tests

### 2.1 DEV_TOOLS Ergebnisse

**c_import_diagnose.py:**
```
[Output hier]
```
**Ergebnis:** ✅ OK / ❌ Probleme gefunden

**c_method_analyzer.py:**
```
[Output hier]
```
**Ergebnis:** ✅ OK / ❌ Probleme gefunden

### 2.2 Isolierte Tests

| Test | Ergebnis | Erkenntnis |
|------|----------|------------|
| Import Module X | ✅ OK | Nicht die Ursache |
| Import Module Y | ❌ CRASH | Hier liegt Problem |
| QApplication zuerst | ❌ CRASH | Nicht ausreichend |

### 2.3 Minimales Reproduktions-Script

```python
# Datei: test_bug_xyz.py
# Reproduziert den Bug zuverlässig
[Code hier]
```

**Crash-Punkt lokalisiert:** JA / NEIN
**Crash passiert bei:** [Zeile/Methode/Modul]

---

## 3. Ausgeschlossene Ursachen

> ⚠️ WICHTIG: Diese Liste verhindert Doppelarbeit!

- [ ] ~~Circular Import~~ - c_import_diagnose zeigt keine Zyklen
- [ ] ~~Fehlende Dependency~~ - Alle pip-Pakete installiert
- [ ] ~~Syntax-Fehler~~ - Datei lässt sich importieren
- [ ] ~~Falscher Pfad~~ - sys.path korrekt gesetzt
- [?] QObject Singleton - Noch nicht geprüft

---

## 4. Aktuelle Hypothesen

| Hypothese | Wahrscheinlichkeit | Nächster Test |
|-----------|-------------------|---------------|
| QObject vor QApplication | HOCH | c_method_analyzer auf event_bus.py |
| Race Condition in __init__ | MITTEL | Schrittweises Logging |
| Externe Library Bug | NIEDRIG | GitHub Issues prüfen |

---

## 5. Nächste Schritte

1. [ ] [Konkreter nächster Schritt]
2. [ ] [Weiterer Schritt]
3. [ ] [Falls nötig: Spezifisches Diagnose-Tool entwickeln]

---

## 6. Kontext für Tool-Entwicklung

> Falls aus diesem Bug ein Diagnose-Tool entstehen soll:

**Wiederholbares Muster:** [Beschreibung]
**Automatisierbar:** JA / NEIN
**Geschätzter Aufwand:** [Zeit]
**Potentieller Nutzen:** [Wie oft könnte das Tool helfen?]

---

## 7. Lösung (wenn gefunden)

**Ursache:**
[Was war das eigentliche Problem?]

**Fix:**
```python
# Vorher (fehlerhaft):
[Code]

# Nachher (korrekt):
[Code]
```

**Betroffene Dateien:**
- `path/to/file.py` - [Was wurde geändert]

**Lessons Learned:**
- [Was kann man für die Zukunft mitnehmen?]
```

---

## Speicherort für Bug-Reports

```
Projekt/
├── BUGREPORT_[datum]_[kurzname].md    # Im Projekt-Root
└── ../docs/
    └── bugs/                           # Oder in ../docs/bugs/
        └── BUGREPORT_[datum]_[kurzname].md
```

**Naming Convention:** `BUGREPORT_20260108_startup_crash.md`

---

## Bekannte PyQt6-Fallen

### 1. QObject Singleton
**Symptom:** Access Violation beim Import/Start
**Ursache:** QObject in `__new__` erstellt
**Lösung:** Lazy Initialization mit Funktion
```python
# FALSCH:
class MySingleton(QObject):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # CRASH!
        return cls._instance

# RICHTIG:
_instance = None
def get_instance():
    global _instance
    if _instance is None:
        _instance = MySingleton()
    return _instance
```

### 2. Signal vor QApplication
**Symptom:** Silent Crash bei pyqtSignal
**Ursache:** pyqtSignal-Klassenvariable wird vor QApplication evaluiert
**Lösung:** QApplication IMMER zuerst erstellen

### 3. Event-Handler Race Condition
**Symptom:** AttributeError in Callback
**Ursache:** Signal.connect() vor Widget-Erstellung
**Lösung:** Guard-Clause in Handler
```python
def _on_changed(self, index):
    if not hasattr(self, 'my_widget'):
        return
    # ... rest
```

---

## Checkliste für Bug-Reports

```markdown
## Bug: [Kurzbeschreibung]

### Symptom
- Fehlermeldung: ...
- Exit-Code: ...
- Wann: Beim Start / Bei Aktion X / ...

### Analyse
- [ ] c_import_diagnose.py ausgeführt
- [ ] c_method_analyzer.py ausgeführt
- [ ] Minimales Reproduktions-Script erstellt
- [ ] Crash-Punkt lokalisiert

### Ursache
...

### Lösung
...

### Betroffene Dateien
- `path/to/file.py` - Beschreibung der Änderung
```

---

## Quick Reference

```
Bug-Typ                    | Erste Aktion
---------------------------|----------------------------------
Import-Fehler              | c_import_diagnose.py
AttributeError             | c_method_analyzer.py
Silent Crash / Access Viol.| c_method_analyzer.py → QObject?
Unerwartetes Verhalten     | Minimales Test-Script
Performance                | cProfile, line_profiler
Memory Leak                | tracemalloc, objgraph
```

---

*Erstellt: 2026-01-08 | Basierend auf ExplorerPro & DevCenter Bug-Sessions*