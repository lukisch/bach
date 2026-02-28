#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2026 Lukas Geiger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
ATI Auto-Session v1.0
=====================
Startet automatisch eine Claude-Session mit ATI-Tasks.

Portiert von: _BATCH/auto_session.py
Angepasst fuer: BACH v1.1 ATI Agent

Usage:
  python auto_session.py                # Normale Session
  python auto_session.py --dry-run      # Nur Prompt anzeigen
  python auto_session.py --force        # Auch bei gesperrtem Screen

Abhaengigkeiten:
  pip install pyautogui pyperclip

Features:
  - Screen-Lock-Detection (Windows)
  - Intelligente Prompt-Generierung mit ATI-Tasks
  - Integration mit BACH Memory
"""

import time
import sys
import os
import json
import ctypes
import sqlite3
from datetime import datetime
from pathlib import Path

# ============ PFADE (relativ zu BACH) ============

ATI_SESSION_DIR = Path(__file__).parent.resolve()
ATI_DIR = ATI_SESSION_DIR.parent
BACH_DIR = ATI_DIR.parent.parent.parent

# Konfiguration und Daten
CONFIG_FILE = ATI_DIR / "data" / "config.json"
LOG_FILE = BACH_DIR / "data" / "logs" / "ati_session.log"
USER_DB = BACH_DIR / "data" / "bach.db"
BACH_DB = BACH_DIR / "data" / "bach.db"
SKILL_FILE = BACH_DIR / "SKILL.md"

# Wartezeiten (Sekunden)
WAIT_AFTER_HOTKEY = 1.0
WAIT_AFTER_PASTE = 0.3
STARTUP_DELAY = 3

# ============ LOGGING ============

def log(msg: str):
    """Logging in Datei und Console."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} - {msg}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

# ============ SCREEN LOCK CHECK ============

def is_screen_locked() -> bool:
    """Prueft ob Windows-Bildschirm gesperrt ist."""
    if sys.platform != "win32":
        return False

    try:
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()

        if hwnd == 0:
            return True

        try:
            import pyautogui
            pos = pyautogui.position()
            return False
        except:
            return True

    except Exception as e:
        log(f"Screen-Lock-Check Fehler: {e}")
        return False

# ============ CONFIG ============

def load_config() -> dict:
    """Laedt ATI-Konfiguration."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except:
            pass

    return {
        "enabled": True,
        "session": {
            "interval_minutes": 30,
            "timeout_minutes": 15,
            "max_tasks_per_session": 3
        }
    }

# ============ TASK LOADING ============

def get_top_tasks(limit: int = 5) -> list:
    """Holt die Top-Tasks aus bach.db/ati_tasks."""
    try:
        conn = sqlite3.connect(USER_DB)
        tasks = conn.execute("""
            SELECT tool_name, task_text, aufwand, priority_score
            FROM ati_tasks
            WHERE status = 'offen'
            ORDER BY priority_score DESC
            LIMIT ?
        """, (limit,)).fetchall()
        conn.close()
        return tasks
    except Exception as e:
        log(f"Task-Laden Fehler: {e}")
        return []

def count_open_tasks() -> int:
    """Zaehlt offene ATI-Tasks."""
    try:
        conn = sqlite3.connect(USER_DB)
        count = conn.execute(
            "SELECT COUNT(*) FROM ati_tasks WHERE status = 'offen'"
        ).fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def get_recent_memory() -> str:
    """Holt letzte Memory-Eintraege aus bach.db."""
    try:
        conn = sqlite3.connect(BACH_DB)
        notes = conn.execute("""
            SELECT content FROM memory_working
            ORDER BY created_at DESC LIMIT 3
        """).fetchall()
        conn.close()

        if notes:
            return "\n".join(f"- {n[0][:100]}" for n in notes)
        return "(keine)"
    except:
        return "(Fehler)"

# ============ PROMPT GENERATION ============

def create_session_prompt() -> str:
    """Erstellt intelligenten Prompt fuer Claude."""
    config = load_config()
    session_cfg = config.get("session", {})
    timeout = session_cfg.get("timeout_minutes", 15)
    max_tasks = session_cfg.get("max_tasks_per_session", 3)

    # Tasks laden
    tasks = get_top_tasks(max_tasks + 2)
    task_count = count_open_tasks()

    # Task-Liste formatieren
    task_lines = []
    for i, (tool, text, aufwand, prio) in enumerate(tasks[:max_tasks], 1):
        short = text[:60] + "..." if len(text) > 60 else text
        task_lines.append(f"{i}. [{tool}] {short} (Aufwand: {aufwand or 'mittel'})")

    tasks_text = "\n".join(task_lines) if task_lines else "(keine offenen Tasks)"

    # Memory laden
    memory_text = get_recent_memory()

    prompt = f"""# BACH AUTO-SESSION [ATI]

## 1. ERSTE AKTION (Automatischer Modus)

```bash
cd "{BACH_DIR}"
python bach.py --startup --partner=claude --mode=silent
bach countdown {timeout} --name="Session-Ende" --notify
bach between use autosession
```

## 2. SKILL.md (ab Abschnitt 2)

Lies {SKILL_FILE} und springe direkt zu Abschnitt **(2) SYSTEM**.
Nur Punkt (1) EINLEITUNG wurde bereits durchgefuehrt.

## 3. ARBEITSPHASE

ATI (Advanced Tool Integration) - Software-Entwicklung und Tool-Management.

**Top-Tasks ({task_count} offen):**
{tasks_text}

**Memory-Kontext:**
{memory_text}

### AUFGABEN-WORKFLOW:
```
(A) bach beat           # Startzeit merken
(B) Aufgabe erledigen
(C) bach beat           # Endzeit = Dauer berechnen
```

### BETWEEN-TASK CHECK (nach jeder Aufgabe):
1. ZEIT-CHECK: `bach countdown status` - Restzeit pruefen
2. ENTSCHEIDUNG:
   - Restzeit > Aufgabendauer + 3min Sicherheit? -> Naechste Aufgabe
   - Sonst -> Weiter zu SESSION-ENDE

**DENKANSTOSS:**
- Planen und Zerlegen kann deine Aufgabe sein!
- Du musst nicht fertig werden, nur dokumentieren wo du warst!

## 4. SESSION-ENDE

### Kontinuitaetstests (max. 2 Min):
- Lessons learned? -> `bach memory add "..."`
- Tasks erledigt? -> Im Taskmanager dokumentieren
- Neue Folgeaufgaben? -> Als neue Tasks anlegen
- Grosse Aenderung? -> CHANGELOG.md + help aktualisieren

### Meta-Plan (max. 2 Min):
- ROADMAP-Aufgabe erledigt? -> ROADMAP.md aktualisieren
- Bug entdeckt? -> BUGLOG.md

### Abschliessen:
```bash
bach --memory session
bach --shutdown "Zusammenfassung der erledigten Arbeit"
```
"""
    return prompt

# ============ CLAUDE TRIGGER ============

def start_claude_session(prompt: str) -> bool:
    """Oeffnet Claude Quick-Entry und sendet Prompt."""
    try:
        import pyautogui
        import pyperclip
    except ImportError:
        log("FEHLER: pip install pyautogui pyperclip")
        return False

    log("Claude Quick-Entry oeffnen (Ctrl+Alt+Space)...")
    pyautogui.hotkey('ctrl', 'alt', 'space')
    time.sleep(WAIT_AFTER_HOTKEY)

    log(f"Prompt einfuegen ({len(prompt)} Zeichen)...")
    pyperclip.copy(prompt)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(WAIT_AFTER_PASTE)

    log("Absenden (Enter)...")
    pyautogui.press('enter')

    log("Session gestartet!")
    return True

# ============ MAIN ============

def main():
    dry_run = '--dry-run' in sys.argv
    force = '--force' in sys.argv

    log("=" * 50)
    log("ATI AUTO-SESSION START")

    # Screen-Lock-Check
    if not force and is_screen_locked():
        log("ABBRUCH: Bildschirm ist gesperrt!")
        log("Verwende --force um trotzdem fortzufahren.")
        return

    # Config laden
    config = load_config()

    # Tasks pruefen
    task_count = count_open_tasks()
    log(f"Offene ATI-Tasks: {task_count}")

    if task_count == 0:
        log("Keine offenen Tasks - Session uebersprungen")
        return

    # Prompt generieren
    prompt = create_session_prompt()

    # Claude starten
    if dry_run:
        log("DRY-RUN: Claude-Start uebersprungen")
        log("-" * 40)
        log("Prompt Preview:")
        log("-" * 40)
        try:
            print(prompt[:2000])
        except UnicodeEncodeError:
            safe = prompt[:2000].encode('ascii', 'ignore').decode('ascii')
            print(safe)
        if len(prompt) > 2000:
            print(f"\n... ({len(prompt) - 2000} weitere Zeichen)")
    else:
        log(f"Starte in {STARTUP_DELAY} Sekunden...")
        time.sleep(STARTUP_DELAY)
        start_claude_session(prompt)

    log("ATI AUTO-SESSION ENDE")
    log("=" * 50)

if __name__ == "__main__":
    main()
