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
BACH Prompt-Manager v2.0 [LEGACY]
===================================
HINWEIS: Prompt-Manager ist LEGACY (weiterhin nutzbar, nicht weiterentwickelt).
Empfohlen: Claude Code CLI Sessions oder Telegram Bridge.
Siehe: gui/MODERNIZATION.md

PyQt6-basierter Manager fuer Claude-Sessions, Prompt-Templates und Daemon-Steuerung.

Funktionsbereiche:
1. STARTUP & LIFECYCLE - System Tray, Single Instance
2. DAEMON-STEUERUNG - Start/Stop, Intervalle, Ruhezeiten
3. TEMPLATE-VERWALTUNG - System/Agents/Custom Templates
4. PROMPT-EDITOR - Variablen-Substitution, Editor
5. PROFIL-MANAGEMENT - Profile laden/speichern
6. CLI-INTERFACE - Kommandozeilen-Parameter
7. PROMPT-GENERIERUNG - Kontextbasierte Prompts
8. API-ENDPOINTS - Interne Service-Methoden
9. EINSTELLUNGEN
10. HILFSFUNKTIONEN

Autor: Claude + User
Version: 2.0
"""

import sys
import os
import re
import json
import signal
import subprocess
import time
import threading
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

# PyQt6 Imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QSpinBox, QCheckBox, QLineEdit,
    QTextEdit, QGroupBox, QGridLayout, QComboBox, QSlider, QFrame,
    QSystemTrayIcon, QMenu, QMessageBox, QScrollArea, QSplitter,
    QProgressBar, QStatusBar, QListWidget, QListWidgetItem, QPlainTextEdit,
    QTreeWidget, QTreeWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QFont, QAction, QColor, QPalette, QPixmap, QTextCharFormat, QSyntaxHighlighter

# ============ PFADE ============

SCRIPT_DIR = Path(__file__).parent.resolve()
BACH_DIR = SCRIPT_DIR.parent
HUB_DIR = BACH_DIR / "hub"
DAEMON_DIR = HUB_DIR / "_services" / "daemon"
PROMPT_GEN_DIR = HUB_DIR / "_services" / "prompt_generator"

# Konfigurationsdateien
CONFIG_FILE = DAEMON_DIR / "config.json"
PID_FILE = DAEMON_DIR / "daemon.pid"
LOG_FILE = BACH_DIR / "data" / "logs" / "session_daemon.log"
PROMPT_GEN_CONFIG = PROMPT_GEN_DIR / "config.json"

# Templates
TEMPLATES_DIR = PROMPT_GEN_DIR / "templates"
SYSTEM_TEMPLATES_DIR = DAEMON_DIR / "prompts"
AGENT_TEMPLATES_DIR = DAEMON_DIR / "prompts" / "agents"
CUSTOM_TEMPLATES_DIR = BACH_DIR / "user" / "templates"
PROFILES_DIR = DAEMON_DIR / "profiles"

# Scripts
DAEMON_SCRIPT = DAEMON_DIR / "session_daemon.py"
AUTO_SESSION_SCRIPT = DAEMON_DIR / "auto_session.py"
SKILL_FILE = BACH_DIR / "SKILL.md"

# Datenbanken
USER_DB = BACH_DIR / "data" / "bach.db"
BACH_DB = BACH_DIR / "data" / "bach.db"

# Icon
ICON_FILE = BACH_DIR / "gui" / "static" / "favicon.ico"

# Lock-File fuer Single-Instance
LOCK_FILE = BACH_DIR / "data" / ".prompt_manager.lock"


# ============ FARBEN (Dark Theme) ============

COLORS = {
    "bg_dark": "#1a1a2e",
    "bg_card": "#16213e",
    "bg_input": "#0f3460",
    "accent": "#e94560",
    "accent_hover": "#ff6b6b",
    "success": "#4ecca3",
    "warning": "#fbbf24",
    "text": "#eaeaea",
    "text_dim": "#888888",
    "text_muted": "#666666",
    "primary": "#3498db",
    "sidebar_bg": "#0d1b2a",
    "editor_bg": "#1b2838"
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text']};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}}

QGroupBox {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['bg_input']};
    border-radius: 8px;
    margin-top: 12px;
    padding: 15px;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
    color: {COLORS['accent']};
}}

QPushButton {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text']};
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {COLORS['primary']};
}}

QPushButton:pressed {{
    background-color: {COLORS['accent']};
}}

QPushButton:disabled {{
    background-color: {COLORS['text_muted']};
    color: {COLORS['text_dim']};
}}

QPushButton#startBtn {{
    background-color: {COLORS['success']};
    color: white;
}}

QPushButton#startBtn:hover {{
    background-color: #5fd9b3;
}}

QPushButton#stopBtn {{
    background-color: {COLORS['accent']};
    color: white;
}}

QPushButton#stopBtn:hover {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton#sendBtn {{
    background-color: {COLORS['success']};
    color: white;
    padding: 12px 24px;
    font-size: 11pt;
}}

QPushButton#copyBtn {{
    background-color: {COLORS['primary']};
    color: white;
}}

QLineEdit, QSpinBox, QComboBox {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['text_muted']};
    border-radius: 4px;
    padding: 6px;
}}

QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border-color: {COLORS['accent']};
}}

QTextEdit, QPlainTextEdit {{
    background-color: {COLORS['editor_bg']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['text_muted']};
    border-radius: 4px;
    padding: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 10pt;
}}

QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {COLORS['accent']};
}}

QCheckBox {{
    color: {COLORS['text']};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {COLORS['text_muted']};
    background-color: {COLORS['bg_input']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

QTabWidget::pane {{
    border: 1px solid {COLORS['bg_input']};
    border-radius: 8px;
    background-color: {COLORS['bg_dark']};
}}

QTabBar::tab {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text']};
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['accent']};
    color: white;
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS['bg_input']};
}}

QProgressBar {{
    border: none;
    border-radius: 4px;
    background-color: {COLORS['bg_input']};
    text-align: center;
    color: white;
}}

QProgressBar::chunk {{
    background-color: {COLORS['primary']};
    border-radius: 4px;
}}

QStatusBar {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_dim']};
}}

QScrollArea {{
    border: none;
}}

QListWidget {{
    background-color: {COLORS['sidebar_bg']};
    border: none;
    border-radius: 4px;
    padding: 5px;
}}

QListWidget::item {{
    padding: 8px 12px;
    border-radius: 4px;
    margin: 2px 0;
}}

QListWidget::item:selected {{
    background-color: {COLORS['accent']};
    color: white;
}}

QListWidget::item:hover:!selected {{
    background-color: {COLORS['bg_input']};
}}

QTreeWidget {{
    background-color: {COLORS['sidebar_bg']};
    border: none;
    border-radius: 4px;
}}

QTreeWidget::item {{
    padding: 6px;
}}

QTreeWidget::item:selected {{
    background-color: {COLORS['accent']};
}}

QTreeWidget::item:hover:!selected {{
    background-color: {COLORS['bg_input']};
}}

QLabel#statusDot {{
    font-size: 24pt;
}}

QLabel#countdownLabel {{
    font-size: 18pt;
    font-weight: bold;
    color: {COLORS['warning']};
}}

QLabel#sessionCounter {{
    font-size: 14pt;
    font-weight: bold;
    color: {COLORS['primary']};
}}

QLabel#charCount {{
    color: {COLORS['text_dim']};
    font-size: 9pt;
}}

QSplitter::handle {{
    background-color: {COLORS['bg_input']};
}}

QSplitter::handle:horizontal {{
    width: 3px;
}}
"""


# ============ 8. API-ENDPOINTS / HILFSFUNKTIONEN ============

def load_config() -> dict:
    """Laedt Daemon-Konfiguration."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except:
            pass
    return get_default_config()


def save_config(config: dict):
    """Speichert Daemon-Konfiguration."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def get_default_config() -> dict:
    """Standard-Konfiguration."""
    return {
        "enabled": True,
        "quiet_start": "22:00",
        "quiet_end": "08:00",
        "ignore_quiet": False,
        "jobs": [
            {
                "profile": "ati",
                "interval_minutes": 30,
                "enabled": True,
                "last_run": None
            }
        ]
    }


def is_quiet_time(quiet_start: str, quiet_end: str) -> bool:
    """Prueft ob Ruhezeit aktiv ist."""
    if not quiet_start or not quiet_end:
        return False
    try:
        now = datetime.now()
        start_h, start_m = map(int, quiet_start.split(":"))
        end_h, end_m = map(int, quiet_end.split(":"))

        start = now.replace(hour=start_h, minute=start_m, second=0)
        end = now.replace(hour=end_h, minute=end_m, second=0)

        if start > end:  # Ueber Mitternacht
            return now >= start or now < end
        return start <= now < end
    except:
        return False


def get_daemon_pid() -> int:
    """Gibt PID des laufenden Daemons zurueck, oder 0."""
    if not PID_FILE.exists():
        return 0
    try:
        pid = int(PID_FILE.read_text().strip())
        # Pruefen ob Prozess existiert
        os.kill(pid, 0)
        return pid
    except (ProcessLookupError, ValueError, PermissionError, OSError):
        return 0


def kill_all_daemons():
    """Killt alle session_daemon.py Prozesse."""
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ['wmic', 'process', 'where',
                 "commandline like '%session_daemon.py%'",
                 'get', 'processid'],
                capture_output=True, text=True, timeout=5,
                creationflags=0x08000000
            )
            for line in result.stdout.strip().split('\n'):
                line = line.strip()
                if line.isdigit():
                    pid = int(line)
                    if pid != os.getpid():
                        try:
                            os.kill(pid, signal.SIGTERM)
                        except:
                            pass
    except:
        pass

    # PID-File loeschen
    if PID_FILE.exists():
        try:
            PID_FILE.unlink()
        except:
            pass


def count_open_tasks(source: str = "ati_tasks") -> int:
    """Zaehlt offene Tasks."""
    try:
        import sqlite3
        if source == "ati_tasks":
            db = USER_DB
            query = "SELECT COUNT(*) FROM ati_tasks WHERE status = 'offen'"
        else:
            db = BACH_DB
            query = "SELECT COUNT(*) FROM tasks WHERE status = 'open'"

        if db.exists():
            conn = sqlite3.connect(str(db))
            count = conn.execute(query).fetchone()[0]
            conn.close()
            return count
    except:
        pass
    return 0


def is_process_running(pid: int) -> bool:
    """Prueft ob ein Prozess mit gegebener PID laeuft (Windows-kompatibel)."""
    if pid <= 0:
        return False
    try:
        if sys.platform == "win32":
            # Windows: tasklist verwenden
            import subprocess
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                capture_output=True, text=True, creationflags=0x08000000  # CREATE_NO_WINDOW
            )
            # Wenn PID gefunden, steht sie in der Ausgabe
            return str(pid) in result.stdout
        else:
            # Unix: kill mit Signal 0
            os.kill(pid, 0)
            return True
    except (subprocess.SubprocessError, OSError, PermissionError):
        return False


def check_single_instance() -> bool:
    """Prueft ob bereits eine Instanz laeuft (Windows-kompatibel)."""
    import subprocess as sp  # Import am Anfang der Funktion
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)

    if LOCK_FILE.exists():
        try:
            stored_pid = int(LOCK_FILE.read_text().strip())
            if stored_pid != os.getpid():
                # Pruefen ob Prozess noch laeuft
                if is_process_running(stored_pid):
                    # Zusaetzlich pruefen ob es wirklich prompt_manager ist
                    if sys.platform == "win32":
                        result = sp.run(
                            ["wmic", "process", "where", f"ProcessId={stored_pid}", "get", "CommandLine"],
                            capture_output=True, text=True, creationflags=0x08000000, encoding='utf-8', errors='ignore'
                        )
                        if result.stdout and "prompt_manager" in result.stdout.lower():
                            return False  # Instanz laeuft bereits
                        # Anderer Prozess hat die PID wiederverwendet
                    else:
                        return False  # Unix: Prozess laeuft
        except (ValueError, FileNotFoundError, sp.SubprocessError, TypeError):
            pass  # Alte/korrupte Lock-Datei

    # Lock-Datei erstellen
    LOCK_FILE.write_text(str(os.getpid()))
    return True


def cleanup_lock():
    """Entfernt Lock-Datei beim Beenden."""
    try:
        LOCK_FILE.unlink(missing_ok=True)
    except:
        pass


# ============ 5. PROFIL-MANAGEMENT ============

def load_profile(name: str) -> dict:
    """Laedt ein Prompt-Profil aus JSON."""
    profile_file = PROFILES_DIR / f"{name}.json"
    if profile_file.exists():
        try:
            return json.loads(profile_file.read_text(encoding="utf-8"))
        except:
            pass

    # Fallback-Profil
    return {
        "name": name,
        "description": f"Profil: {name}",
        "task_source": "ati_tasks",
        "task_filter": {"status": "offen"},
        "max_tasks": 3,
        "timeout_minutes": 15,
        "prompt_template": "default",
        "instruction": f"Arbeite als {name} Agent."
    }


def list_profiles() -> List[str]:
    """Listet alle verfuegbaren Profile."""
    profiles = ["ati", "wartung", "custom"]  # Defaults

    if PROFILES_DIR.exists():
        for f in PROFILES_DIR.glob("*.json"):
            name = f.stem
            if name not in profiles:
                profiles.append(name)

    return profiles


# ============ 1. TEMPLATE-VERWALTUNG ============

def list_templates() -> Dict[str, List[dict]]:
    """Listet alle verfuegbaren Templates nach Kategorie."""
    result = {"system": [], "agents": [], "custom": []}

    # System-Templates
    if SYSTEM_TEMPLATES_DIR.exists():
        for f in SYSTEM_TEMPLATES_DIR.glob("*.md"):
            if f.name != "agents":
                result["system"].append({
                    "name": f.stem,
                    "path": f"system/{f.stem}",
                    "file": str(f),
                    "editable": False,
                    "description": get_template_description(f)
                })
        for f in SYSTEM_TEMPLATES_DIR.glob("*.txt"):
            result["system"].append({
                "name": f.stem,
                "path": f"system/{f.stem}",
                "file": str(f),
                "editable": False,
                "description": get_template_description(f)
            })

    # Templates aus prompt_generator
    if TEMPLATES_DIR.exists():
        for subdir in ["system", "agents", "custom"]:
            sub_path = TEMPLATES_DIR / subdir
            if sub_path.exists():
                for f in sub_path.glob("*.txt"):
                    cat = "system" if subdir == "system" else ("agents" if subdir == "agents" else "custom")
                    result[cat].append({
                        "name": f.stem,
                        "path": f"{subdir}/{f.stem}",
                        "file": str(f),
                        "editable": cat != "system",
                        "description": get_template_description(f)
                    })

    # Agent-Templates
    if AGENT_TEMPLATES_DIR.exists():
        for f in AGENT_TEMPLATES_DIR.glob("*.md"):
            result["agents"].append({
                "name": f.stem,
                "path": f"agents/{f.stem}",
                "file": str(f),
                "editable": True,
                "description": get_template_description(f)
            })
        for f in AGENT_TEMPLATES_DIR.glob("*.txt"):
            result["agents"].append({
                "name": f.stem,
                "path": f"agents/{f.stem}",
                "file": str(f),
                "editable": True,
                "description": get_template_description(f)
            })

    # Custom-Templates
    if CUSTOM_TEMPLATES_DIR.exists():
        for f in CUSTOM_TEMPLATES_DIR.glob("*.md"):
            result["custom"].append({
                "name": f.stem,
                "path": f"custom/{f.stem}",
                "file": str(f),
                "editable": True,
                "description": get_template_description(f)
            })
        for f in CUSTOM_TEMPLATES_DIR.glob("*.txt"):
            result["custom"].append({
                "name": f.stem,
                "path": f"custom/{f.stem}",
                "file": str(f),
                "editable": True,
                "description": get_template_description(f)
            })

    return result


def get_template_description(file_path: Path) -> str:
    """Extrahiert Beschreibung aus Template-Header."""
    try:
        lines = file_path.read_text(encoding='utf-8').split('\n')
        for line in lines[:5]:
            if line.startswith('#') and not line.startswith('# '):
                continue
            if line.startswith('# '):
                return line[2:].strip()
        return ""
    except:
        return ""


def get_template(file_path: str) -> Optional[str]:
    """Laedt ein Template."""
    try:
        path = Path(file_path)
        if path.exists():
            return path.read_text(encoding='utf-8')
    except:
        pass
    return None


def extract_variables(template: str) -> List[str]:
    """Extrahiert {{VAR_NAME}} Variablen aus Template."""
    pattern = r'\{\{([A-Z_][A-Z0-9_]*)\}\}'
    return list(set(re.findall(pattern, template)))


def substitute_variables(template: str, variables: Dict[str, str]) -> str:
    """Ersetzt {{VAR_NAME}} mit Werten."""
    result = template
    for key, value in variables.items():
        result = result.replace(f"{{{{{key}}}}}", str(value))
    # Nicht ersetzte markieren
    result = re.sub(r'\{\{[A-Z_][A-Z0-9_]*\}\}', '[NICHT DEFINIERT]', result)
    return result


# ============ 7. PROMPT-GENERIERUNG ============

def get_tasks(profile: dict, limit: int = 5) -> list:
    """Holt Tasks basierend auf Profil."""
    import sqlite3
    task_source = profile.get("task_source", "ati_tasks")

    try:
        if task_source == "ati_tasks":
            conn = sqlite3.connect(str(USER_DB))
            tasks = conn.execute("""
                SELECT tool_name, task_text, aufwand, priority_score
                FROM ati_tasks
                WHERE status = 'offen'
                ORDER BY priority_score DESC
                LIMIT ?
            """, (limit,)).fetchall()
        else:
            conn = sqlite3.connect(str(BACH_DB))
            tasks = conn.execute("""
                SELECT category, title, priority, id
                FROM tasks
                WHERE status = 'open'
                ORDER BY
                    CASE priority
                        WHEN 'P1' THEN 1
                        WHEN 'P2' THEN 2
                        WHEN 'P3' THEN 3
                        ELSE 4
                    END
                LIMIT ?
            """, (limit,)).fetchall()

        conn.close()
        return tasks
    except Exception as e:
        return []


def get_recent_memory() -> str:
    """Holt letzte Memory-Eintraege."""
    import sqlite3
    try:
        conn = sqlite3.connect(str(BACH_DB))
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


def generate_session_prompt(profile: dict, include_startup: bool = True,
                            include_skill_ref: bool = True, include_session_end: bool = True,
                            work_time_minutes: int = None) -> str:
    """Generiert kontextbasierten Session-Prompt.

    Args:
        profile: Profil-Dictionary mit agent_prompt, start_command, etc.
        include_startup: ERSTE AKTION Block einfuegen
        include_skill_ref: SKILL.md Referenz einfuegen
        include_session_end: SESSION-ENDE Block einfuegen
        work_time_minutes: Explizite Arbeitszeit (ueberschreibt Profil-timeout)

    Returns:
        Formatierter Prompt-String
    """
    profile_name = profile.get("name", "default")
    # Arbeitszeit: Explizit uebergeben oder aus Profil
    timeout = work_time_minutes if work_time_minutes else profile.get("timeout_minutes", 15)

    # Session-Start-Zeit generieren
    session_start = datetime.now().strftime("%H:%M")

    # Prompt-Teile zusammenbauen
    parts = []

    # ═══════════════════════════════════════════════════════════════
    # 1. AGENT-PROMPT (aus Profil oder generisch)
    # ═══════════════════════════════════════════════════════════════
    agent_prompt = profile.get("agent_prompt")
    if agent_prompt:
        parts.append(agent_prompt)
    else:
        # Generischer Agent-Header
        parts.append(f"# {profile_name.upper()} Agent Prompt")
        instruction = profile.get("instruction", f"Du bist der {profile_name} Agent im BACH-System.")
        parts.append(f"\n{instruction}")

    # ═══════════════════════════════════════════════════════════════
    # 2. ERSTE AKTION (optional)
    # ═══════════════════════════════════════════════════════════════
    if include_startup:
        startup_block = f"""
## 1. ERSTE AKTION (Automatischer Modus)

```bash
cd "{BACH_DIR}"
python bach.py --startup --partner=claude --mode=silent
bach countdown {timeout} --name="Session-Ende" --notify
```"""
        parts.append(startup_block)

    # ═══════════════════════════════════════════════════════════════
    # 3. SKILL.md REFERENZ (optional)
    # ═══════════════════════════════════════════════════════════════
    if include_skill_ref:
        skill_block = f"""
## 2. SKILL.md (ab Abschnitt 2)

Lies {SKILL_FILE} und springe direkt zu Abschnitt **(2) SYSTEM**."""
        parts.append(skill_block)

    # ═══════════════════════════════════════════════════════════════
    # 4. START-COMMAND (aus Profil)
    # ═══════════════════════════════════════════════════════════════
    start_command = profile.get("start_command")
    if start_command:
        parts.append(f"\n{start_command}")

    # ═══════════════════════════════════════════════════════════════
    # 5. AUFGABEN-WORKFLOW
    # ═══════════════════════════════════════════════════════════════
    workflow_block = """
### AUFGABEN-WORKFLOW:
```
(A) bach beat           # Startzeit merken
(B) Aufgabe erledigen
(C) bach beat           # Endzeit = Dauer berechnen
```"""
    parts.append(workflow_block)

    # ═══════════════════════════════════════════════════════════════
    # 6. SESSION-ENDE (optional)
    # ═══════════════════════════════════════════════════════════════
    if include_session_end:
        end_block = """
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
```"""
        parts.append(end_block)

    return "\n".join(parts)


def generate_minimal_prompt(profile: dict) -> str:
    """Generiert minimalen Prompt nur mit Agent-Info (ohne Zusaetze)."""
    return generate_session_prompt(profile,
                                   include_startup=False,
                                   include_skill_ref=False,
                                   include_session_end=False)


# ============ SCREEN LOCK CHECK ============

def is_screen_locked() -> bool:
    """Prueft ob Windows-Bildschirm gesperrt ist."""
    if sys.platform != "win32":
        return False

    try:
        import ctypes
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

    except Exception:
        return False


# ============ WORKER THREADS ============

class DaemonStartWorker(QThread):
    """Worker zum Starten des Daemons."""
    finished = pyqtSignal(bool, str)

    def __init__(self, interval_minutes: int):
        super().__init__()
        self.interval = interval_minutes

    def run(self):
        try:
            kill_all_daemons()
            time.sleep(0.3)

            # Config updaten
            config = load_config()
            if config.get("jobs"):
                config["jobs"][0]["interval_minutes"] = self.interval
                config["jobs"][0]["enabled"] = True
                config["jobs"][0]["last_run"] = None  # Reset fuer sofortigen Start
            save_config(config)

            # Daemon starten
            python_exe = sys.executable
            if sys.platform == "win32":
                creation_flags = 0x08000000  # CREATE_NO_WINDOW
            else:
                creation_flags = 0

            subprocess.Popen(
                [python_exe, str(DAEMON_SCRIPT)],
                cwd=str(DAEMON_DIR),
                creationflags=creation_flags,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            time.sleep(1)

            if get_daemon_pid() > 0:
                self.finished.emit(True, "Daemon gestartet")
            else:
                self.finished.emit(False, "Daemon-Start fehlgeschlagen")

        except Exception as e:
            self.finished.emit(False, str(e))


class SessionTriggerWorker(QThread):
    """Worker zum Starten einer Session."""
    finished = pyqtSignal(bool, str)

    def __init__(self, prompt: str = None, profile_name: str = "ati", force: bool = False,
                 work_time_minutes: int = None):
        super().__init__()
        self.prompt = prompt
        self.profile_name = profile_name
        self.force = force
        self.work_time_minutes = work_time_minutes

    def run(self):
        try:
            # Screen-Lock-Check
            if not self.force and is_screen_locked():
                self.finished.emit(False, "Bildschirm gesperrt")
                return

            # Prompt generieren falls nicht gegeben
            if not self.prompt:
                profile = load_profile(self.profile_name)
                self.prompt = generate_session_prompt(profile, work_time_minutes=self.work_time_minutes)

            # Claude Quick-Entry triggern
            import pyautogui
            import pyperclip

            # In Zwischenablage
            pyperclip.copy(self.prompt)

            # Quick-Entry oeffnen
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'alt', 'space')
            time.sleep(1.0)

            # Einfuegen
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)

            # Absenden
            pyautogui.press('enter')

            self.finished.emit(True, f"Session gestartet ({len(self.prompt)} Zeichen)")

        except ImportError:
            self.finished.emit(False, "pyautogui/pyperclip nicht installiert")
        except Exception as e:
            self.finished.emit(False, str(e))


class CopyWorker(QThread):
    """Worker zum Kopieren in Zwischenablage."""
    finished = pyqtSignal(bool, str)

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def run(self):
        try:
            import pyperclip
            pyperclip.copy(self.text)
            self.finished.emit(True, f"Kopiert ({len(self.text)} Zeichen)")
        except ImportError:
            try:
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(self.text)
                root.update()
                root.destroy()
                self.finished.emit(True, f"Kopiert ({len(self.text)} Zeichen)")
            except:
                self.finished.emit(False, "Clipboard nicht verfuegbar")


# ============ HAUPTFENSTER ============

class PromptManagerWindow(QMainWindow):
    """Hauptfenster des BACH Prompt-Managers."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("BACH Prompt-Manager v2.0")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)

        # Icon setzen
        if ICON_FILE.exists():
            self.setWindowIcon(QIcon(str(ICON_FILE)))

        # State
        self.daemon_running = False
        self.daemon_started_at = None
        self.daemon_interval_sec = 0
        self.daemon_max_sessions = 0
        self.config = load_config()
        self.current_template = None
        self.current_variables = {}

        # Tray Icon
        self.tray_icon = None
        self.setup_tray_icon()

        # UI aufbauen
        self.setup_ui()

        # Timer fuer Updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.periodic_update)
        self.update_timer.start(1000)  # Jede Sekunde

        # Initial-Status
        self.update_daemon_status()
        self.load_templates()
        self.log("Prompt-Manager v2.0 gestartet")

    # ==================== 1. STARTUP & LIFECYCLE ====================

    def setup_tray_icon(self):
        """System Tray Integration"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        self.tray_icon = QSystemTrayIcon(self)

        # Icon
        if ICON_FILE.exists():
            self.tray_icon.setIcon(QIcon(str(ICON_FILE)))
        else:
            pixmap = QPixmap(64, 64)
            pixmap.fill(QColor(COLORS["accent"]))
            self.tray_icon.setIcon(QIcon(pixmap))

        # Menue
        tray_menu = QMenu()

        show_action = QAction("Dashboard oeffnen", self)
        show_action.triggered.connect(self.show_from_tray)
        tray_menu.addAction(show_action)

        tray_menu.addSeparator()

        session_action = QAction("Session starten", self)
        session_action.triggered.connect(self.start_session_now)
        tray_menu.addAction(session_action)

        tray_menu.addSeparator()

        start_daemon_action = QAction("Daemon starten", self)
        start_daemon_action.triggered.connect(self.start_daemon)
        tray_menu.addAction(start_daemon_action)

        stop_daemon_action = QAction("Daemon stoppen", self)
        stop_daemon_action.triggered.connect(self.stop_daemon)
        tray_menu.addAction(stop_daemon_action)

        tray_menu.addSeparator()

        quit_action = QAction("Beenden", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_activated)
        self.tray_icon.show()
        self.tray_icon.setToolTip("BACH Prompt-Manager")

    def tray_activated(self, reason):
        """Tray-Icon Doppelklick."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_from_tray()

    def show_from_tray(self):
        """Fenster aus Tray wiederherstellen."""
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def closeEvent(self, event):
        """Bei Schliessen: Minimiert zu Tray statt Beenden."""
        if self.tray_icon and self.tray_icon.isVisible():
            self.hide()
            self.tray_icon.showMessage(
                "BACH Prompt-Manager",
                "Laeuft im Hintergrund weiter",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
            event.ignore()
        else:
            self.quit_app()
            event.accept()

    def quit_app(self):
        """Anwendung komplett beenden - inkl. Kill Switch fuer Daemons."""
        # Kill Switch: Alle laufenden Daemons beenden
        kill_all_daemons()
        self.log("Alle Daemons beendet (Kill Switch)")

        cleanup_lock()
        if self.tray_icon:
            self.tray_icon.hide()
        QApplication.quit()

    # ==================== UI SETUP ====================

    def setup_ui(self):
        """Baut die UI auf."""
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Tab 1: Prompt-Editor (NEU)
        self.create_prompt_editor_tab()

        # Tab 2: Dashboard (Daemon + Quick Actions)
        self.create_dashboard_tab()

        # Tab 3: Einstellungen
        self.create_settings_tab()

        # Tab 4: Log
        self.create_log_tab()

        # Statusbar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Bereit")

    # ==================== 2. PROMPT-EDITOR TAB ====================

    def create_prompt_editor_tab(self):
        """Prompt-Editor mit Template-Sidebar."""
        tab = QWidget()
        self.tabs.addTab(tab, "Prompt-Editor")

        layout = QHBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Splitter fuer Sidebar/Editor
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        # ==================== 1. TEMPLATE-SIDEBAR ====================
        sidebar = QWidget()
        sidebar.setMaximumWidth(300)
        sidebar.setMinimumWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)

        # Template-Header
        sidebar_header = QLabel("Templates")
        sidebar_header.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        sidebar_header.setStyleSheet(f"color: {COLORS['accent']};")
        sidebar_layout.addWidget(sidebar_header)

        # Template-Tree
        self.template_tree = QTreeWidget()
        self.template_tree.setHeaderHidden(True)
        self.template_tree.itemClicked.connect(self.on_template_selected)
        sidebar_layout.addWidget(self.template_tree)

        # Refresh-Button
        refresh_btn = QPushButton("Templates neu laden")
        refresh_btn.clicked.connect(self.load_templates)
        sidebar_layout.addWidget(refresh_btn)

        splitter.addWidget(sidebar)

        # ==================== 2. EDITOR-BEREICH ====================
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(10, 10, 10, 10)
        editor_layout.setSpacing(10)

        # Editor-Header mit Template-Info
        header_layout = QHBoxLayout()

        self.template_name_label = QLabel("Kein Template geladen")
        self.template_name_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        header_layout.addWidget(self.template_name_label)

        header_layout.addStretch()

        self.char_count_label = QLabel("0 Zeichen")
        self.char_count_label.setObjectName("charCount")
        header_layout.addWidget(self.char_count_label)

        editor_layout.addLayout(header_layout)

        # Variablen-Bereich
        self.variables_group = QGroupBox("Variablen")
        self.variables_layout = QGridLayout(self.variables_group)
        self.variables_group.setVisible(False)
        editor_layout.addWidget(self.variables_group)

        # Editor
        self.prompt_editor = QPlainTextEdit()
        self.prompt_editor.setPlaceholderText(
            "Waehle ein Template aus der Sidebar oder schreibe direkt hier...\n\n"
            "Variablen-Syntax: {{VAR_NAME}}"
        )
        self.prompt_editor.textChanged.connect(self.on_editor_changed)
        editor_layout.addWidget(self.prompt_editor, 1)

        # ==================== 3. PROMPT-OPTIONEN ====================
        options_group = QGroupBox("Prompt-Optionen")
        options_layout = QHBoxLayout(options_group)

        # Profil-Auswahl
        options_layout.addWidget(QLabel("Profil:"))
        self.send_profile_combo = QComboBox()
        self.send_profile_combo.addItems(list_profiles())
        self.send_profile_combo.setFixedWidth(120)
        options_layout.addWidget(self.send_profile_combo)

        options_layout.addSpacing(15)

        # Checkboxen fuer optionale Teile
        self.include_startup_check = QCheckBox("Startup-Block")
        self.include_startup_check.setChecked(True)
        self.include_startup_check.setToolTip("ERSTE AKTION mit bash-Befehlen")
        options_layout.addWidget(self.include_startup_check)

        self.include_skill_check = QCheckBox("SKILL.md")
        self.include_skill_check.setChecked(True)
        self.include_skill_check.setToolTip("Referenz auf SKILL.md")
        options_layout.addWidget(self.include_skill_check)

        self.include_end_check = QCheckBox("Session-Ende")
        self.include_end_check.setChecked(True)
        self.include_end_check.setToolTip("Kontinuitaetstests und Abschluss")
        options_layout.addWidget(self.include_end_check)

        options_layout.addStretch()

        editor_layout.addWidget(options_group)

        # ==================== 4. SEND-AKTIONEN ====================
        send_group = QGroupBox("Aktionen")
        send_layout = QHBoxLayout(send_group)

        # Generate Session Prompt Button
        generate_btn = QPushButton("Session-Prompt generieren")
        generate_btn.clicked.connect(self.generate_session_prompt_ui)
        send_layout.addWidget(generate_btn)

        # Copy Button
        copy_btn = QPushButton("In Zwischenablage")
        copy_btn.setObjectName("copyBtn")
        copy_btn.clicked.connect(self.copy_prompt)
        send_layout.addWidget(copy_btn)

        # Save Custom Prompt Button
        save_prompt_btn = QPushButton("Als Vorlage speichern")
        save_prompt_btn.setToolTip("Aktuellen Prompt als Custom-Template speichern")
        save_prompt_btn.clicked.connect(self.save_custom_prompt)
        send_layout.addWidget(save_prompt_btn)

        send_layout.addStretch()

        # Send Button
        send_btn = QPushButton("Direkt starten")
        send_btn.setObjectName("sendBtn")
        send_btn.clicked.connect(self.send_direct_session)
        send_layout.addWidget(send_btn)

        editor_layout.addWidget(send_group)

        splitter.addWidget(editor_widget)

        # Splitter-Proportionen
        splitter.setSizes([250, 750])

    def load_templates(self):
        """Laedt Templates in Tree."""
        self.template_tree.clear()

        templates = list_templates()

        for category, items in templates.items():
            if not items:
                continue

            # Kategorie-Node
            cat_item = QTreeWidgetItem([category.upper()])
            cat_item.setFont(0, QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.template_tree.addTopLevelItem(cat_item)

            # Templates
            for tmpl in items:
                item = QTreeWidgetItem([tmpl["name"]])
                item.setData(0, Qt.ItemDataRole.UserRole, tmpl)
                if tmpl.get("description"):
                    item.setToolTip(0, tmpl["description"])
                cat_item.addChild(item)

            cat_item.setExpanded(True)

        self.log(f"Templates geladen: {sum(len(v) for v in templates.values())} gefunden")

    def on_template_selected(self, item: QTreeWidgetItem, column: int):
        """Template aus Tree ausgewaehlt."""
        tmpl = item.data(0, Qt.ItemDataRole.UserRole)
        if not tmpl:
            return  # Kategorie-Node

        # Template laden
        content = get_template(tmpl["file"])
        if content:
            self.current_template = tmpl
            self.prompt_editor.setPlainText(content)
            self.template_name_label.setText(f"{tmpl['path']}")

            # Variablen extrahieren und anzeigen
            self.setup_variable_inputs(content)

            self.log(f"Template geladen: {tmpl['path']}")

    def setup_variable_inputs(self, template: str):
        """Erstellt Input-Felder fuer Template-Variablen."""
        # Alte Inputs entfernen
        while self.variables_layout.count():
            child = self.variables_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Variablen extrahieren
        variables = extract_variables(template)

        if not variables:
            self.variables_group.setVisible(False)
            return

        self.variables_group.setVisible(True)
        self.current_variables = {}

        row = 0
        col = 0
        for var in sorted(variables):
            label = QLabel(f"{var}:")
            self.variables_layout.addWidget(label, row, col * 2)

            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Wert fuer {var}")
            input_field.textChanged.connect(self.on_variable_changed)
            self.variables_layout.addWidget(input_field, row, col * 2 + 1)

            self.current_variables[var] = input_field

            col += 1
            if col >= 2:
                col = 0
                row += 1

    def on_variable_changed(self):
        """Variable geaendert - Prompt aktualisieren."""
        if not self.current_template:
            return

        # Original-Template laden
        content = get_template(self.current_template["file"])
        if not content:
            return

        # Variablen substituieren
        variables = {}
        for var, input_field in self.current_variables.items():
            value = input_field.text()
            if value:
                variables[var] = value

        if variables:
            content = substitute_variables(content, variables)

        # Editor aktualisieren (ohne Signal-Loop)
        self.prompt_editor.blockSignals(True)
        self.prompt_editor.setPlainText(content)
        self.prompt_editor.blockSignals(False)

        self.update_char_count()

    def on_editor_changed(self):
        """Editor-Text geaendert."""
        self.update_char_count()

    def update_char_count(self):
        """Aktualisiert Zeichenzaehler."""
        count = len(self.prompt_editor.toPlainText())
        self.char_count_label.setText(f"{count:,} Zeichen".replace(",", "."))

    def copy_prompt(self):
        """Prompt in Zwischenablage kopieren."""
        text = self.prompt_editor.toPlainText()
        if not text:
            self.statusbar.showMessage("Kein Text zum Kopieren", 3000)
            return

        self.copy_worker = CopyWorker(text)
        self.copy_worker.finished.connect(self.on_copy_finished)
        self.copy_worker.start()

    def on_copy_finished(self, success: bool, message: str):
        """Callback nach Copy."""
        if success:
            self.log(f"Prompt kopiert: {message}")
        else:
            self.log(f"Copy-Fehler: {message}")
        self.statusbar.showMessage(message, 3000)

    def save_custom_prompt(self):
        """Speichert aktuellen Prompt als Custom-Template."""
        from PyQt6.QtWidgets import QInputDialog

        text = self.prompt_editor.toPlainText()
        if not text:
            self.statusbar.showMessage("Kein Prompt zum Speichern", 3000)
            return

        # Namen abfragen
        name, ok = QInputDialog.getText(
            self,
            "Prompt speichern",
            "Name fuer die Vorlage (ohne Erweiterung):",
            QLineEdit.EchoMode.Normal,
            f"custom_{datetime.now().strftime('%Y%m%d_%H%M')}"
        )

        if not ok or not name:
            return

        # Unerlaubte Zeichen entfernen
        name = re.sub(r'[<>:"/\\|?*]', '_', name)

        # Speicherpfad: user/templates/
        CUSTOM_TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        file_path = CUSTOM_TEMPLATES_DIR / f"{name}.txt"

        # Beschreibung als Header hinzufuegen
        description, ok2 = QInputDialog.getText(
            self,
            "Beschreibung",
            "Kurze Beschreibung (optional):",
            QLineEdit.EchoMode.Normal,
            ""
        )

        # Template mit Header speichern
        header = f"# {description if description else name}\n# Erstellt: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        content = header + text

        try:
            file_path.write_text(content, encoding='utf-8')
            self.log(f"Prompt gespeichert: {file_path.name}")
            self.statusbar.showMessage(f"Vorlage gespeichert: {name}", 3000)

            # Templates neu laden
            self.load_templates()

        except Exception as e:
            self.log(f"Speichern fehlgeschlagen: {e}")
            self.statusbar.showMessage(f"Fehler: {e}", 5000)

    def generate_session_prompt_ui(self):
        """Generiert Session-Prompt und zeigt im Editor."""
        profile_name = self.send_profile_combo.currentText()
        profile = load_profile(profile_name)

        # Optionen aus Checkboxen
        include_startup = self.include_startup_check.isChecked()
        include_skill = self.include_skill_check.isChecked()
        include_end = self.include_end_check.isChecked()

        # Arbeitszeit aus Einstellungen holen (Session-Dauer)
        work_time = self.session_duration.value() if hasattr(self, 'session_duration') else 15

        prompt = generate_session_prompt(
            profile,
            include_startup=include_startup,
            include_skill_ref=include_skill,
            include_session_end=include_end,
            work_time_minutes=work_time
        )

        self.prompt_editor.setPlainText(prompt)

        # Label mit Optionen
        opts = []
        if include_startup:
            opts.append("Startup")
        if include_skill:
            opts.append("SKILL")
        if include_end:
            opts.append("Ende")
        opts_str = " + ".join(opts) if opts else "Minimal"

        self.template_name_label.setText(f"Session-Prompt ({profile_name}) [{opts_str}]")
        self.variables_group.setVisible(False)

        self.log(f"Session-Prompt generiert: {profile_name} [{opts_str}]")

    def send_direct_session(self):
        """Startet Claude-Session mit aktuellem Prompt."""
        text = self.prompt_editor.toPlainText()
        if not text:
            self.statusbar.showMessage("Kein Prompt zum Senden", 3000)
            return

        profile_name = self.send_profile_combo.currentText()

        self.statusbar.showMessage("Starte Session...")
        self.session_worker = SessionTriggerWorker(prompt=text, profile_name=profile_name)
        self.session_worker.finished.connect(self.on_session_finished)
        self.session_worker.start()

    # ==================== 2. DASHBOARD TAB ====================

    def create_dashboard_tab(self):
        """Dashboard mit Daemon-Steuerung und Quick Actions."""
        tab = QWidget()
        self.tabs.addTab(tab, "Dashboard")

        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # Daemon Status & Control
        daemon_group = QGroupBox("Daemon-Steuerung")
        daemon_layout = QGridLayout(daemon_group)
        daemon_layout.setSpacing(10)

        # Status-Anzeige
        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("statusDot")
        self.status_dot.setStyleSheet(f"color: {COLORS['text_muted']};")
        daemon_layout.addWidget(self.status_dot, 0, 0)

        self.status_label = QLabel("Daemon gestoppt")
        self.status_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        daemon_layout.addWidget(self.status_label, 0, 1, 1, 2)

        # Start/Stop Buttons
        self.start_btn = QPushButton("Start")
        self.start_btn.setObjectName("startBtn")
        self.start_btn.setFixedWidth(100)
        self.start_btn.clicked.connect(self.start_daemon)
        daemon_layout.addWidget(self.start_btn, 0, 3)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setFixedWidth(100)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_daemon)
        daemon_layout.addWidget(self.stop_btn, 0, 4)

        # Intervall-Einstellung
        daemon_layout.addWidget(QLabel("Intervall:"), 1, 0)

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(5, 480)
        self.interval_spin.setValue(30)
        self.interval_spin.setSuffix(" Min")
        daemon_layout.addWidget(self.interval_spin, 1, 1)

        # Quick-Select Buttons
        quick_frame = QWidget()
        quick_layout = QHBoxLayout(quick_frame)
        quick_layout.setContentsMargins(0, 0, 0, 0)
        quick_layout.setSpacing(5)

        for text, mins in [("15 Min", 15), ("30 Min", 30), ("1 Std", 60), ("2 Std", 120)]:
            btn = QPushButton(text)
            btn.setFixedWidth(60)
            btn.clicked.connect(lambda checked, m=mins: self.interval_spin.setValue(m))
            quick_layout.addWidget(btn)

        daemon_layout.addWidget(quick_frame, 1, 2, 1, 3)

        # Session-Counter & Countdown
        daemon_layout.addWidget(QLabel("Sessions:"), 2, 0)

        self.session_counter = QLabel("0 / ∞")
        self.session_counter.setObjectName("sessionCounter")
        daemon_layout.addWidget(self.session_counter, 2, 1)

        daemon_layout.addWidget(QLabel("Naechste:"), 2, 2)

        self.countdown_label = QLabel("--:--")
        self.countdown_label.setObjectName("countdownLabel")
        daemon_layout.addWidget(self.countdown_label, 2, 3, 1, 2)

        # Auto-Stop
        daemon_layout.addWidget(QLabel("Max Sessions:"), 3, 0)

        self.max_sessions_spin = QSpinBox()
        self.max_sessions_spin.setRange(0, 100)
        self.max_sessions_spin.setValue(0)
        self.max_sessions_spin.setSpecialValueText("Unbegrenzt")
        daemon_layout.addWidget(self.max_sessions_spin, 3, 1)

        self.unlimited_check = QCheckBox("Unbegrenzt")
        self.unlimited_check.setChecked(True)
        self.unlimited_check.stateChanged.connect(self.toggle_max_sessions)
        daemon_layout.addWidget(self.unlimited_check, 3, 2)

        layout.addWidget(daemon_group)

        # Ruhezeiten
        quiet_group = QGroupBox("Ruhezeiten (keine Sessions)")
        quiet_layout = QHBoxLayout(quiet_group)

        quiet_layout.addWidget(QLabel("Von:"))
        self.quiet_start = QLineEdit("22:00")
        self.quiet_start.setFixedWidth(60)
        quiet_layout.addWidget(self.quiet_start)

        quiet_layout.addWidget(QLabel("Bis:"))
        self.quiet_end = QLineEdit("08:00")
        self.quiet_end.setFixedWidth(60)
        quiet_layout.addWidget(self.quiet_end)

        self.ignore_quiet = QCheckBox("Ruhezeit ignorieren")
        quiet_layout.addWidget(self.ignore_quiet)

        quiet_layout.addStretch()

        layout.addWidget(quiet_group)

        # Quick Actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QHBoxLayout(actions_group)

        session_btn = QPushButton("Session starten")
        session_btn.setStyleSheet(f"background-color: {COLORS['success']}; color: white;")
        session_btn.clicked.connect(self.start_session_now)
        actions_layout.addWidget(session_btn)

        folder_btn = QPushButton("BACH Ordner")
        folder_btn.clicked.connect(lambda: os.startfile(str(BACH_DIR)) if sys.platform == "win32" else None)
        actions_layout.addWidget(folder_btn)

        skill_btn = QPushButton("SKILL.md")
        skill_btn.clicked.connect(lambda: os.startfile(str(SKILL_FILE)) if SKILL_FILE.exists() else None)
        actions_layout.addWidget(skill_btn)

        log_btn = QPushButton("Daemon Log")
        log_btn.clicked.connect(lambda: os.startfile(str(LOG_FILE)) if LOG_FILE.exists() else None)
        actions_layout.addWidget(log_btn)

        layout.addWidget(actions_group)

        # Status-Info
        info_group = QGroupBox("System-Status")
        info_layout = QGridLayout(info_group)

        info_layout.addWidget(QLabel("Offene Tasks:"), 0, 0)
        self.tasks_label = QLabel("0")
        self.tasks_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        info_layout.addWidget(self.tasks_label, 0, 1)

        info_layout.addWidget(QLabel("Daemon PID:"), 0, 2)
        self.pid_label = QLabel("-")
        info_layout.addWidget(self.pid_label, 0, 3)

        info_layout.addWidget(QLabel("Letzte Session:"), 1, 0)
        self.last_session_label = QLabel("-")
        info_layout.addWidget(self.last_session_label, 1, 1, 1, 3)

        layout.addWidget(info_group)

        layout.addStretch()

    # ==================== 3. SETTINGS TAB ====================

    def create_settings_tab(self):
        """Einstellungen-Tab."""
        tab = QWidget()
        self.tabs.addTab(tab, "Einstellungen")

        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # Session-Einstellungen
        session_group = QGroupBox("Session-Einstellungen")
        session_layout = QGridLayout(session_group)

        session_layout.addWidget(QLabel("Session-Dauer (Min):"), 0, 0)
        self.session_duration = QSpinBox()
        self.session_duration.setRange(5, 60)
        self.session_duration.setValue(15)
        session_layout.addWidget(self.session_duration, 0, 1)

        session_layout.addWidget(QLabel("Max Tasks/Session:"), 1, 0)
        self.max_tasks = QSpinBox()
        self.max_tasks.setRange(1, 20)
        self.max_tasks.setValue(3)
        session_layout.addWidget(self.max_tasks, 1, 1)

        layout.addWidget(session_group)

        # Profil-Auswahl
        profile_group = QGroupBox("Daemon-Profil")
        profile_layout = QGridLayout(profile_group)

        profile_layout.addWidget(QLabel("Aktives Profil:"), 0, 0)
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(list_profiles())
        profile_layout.addWidget(self.profile_combo, 0, 1)

        layout.addWidget(profile_group)

        # System-Info
        info_group = QGroupBox("System-Info")
        info_layout = QVBoxLayout(info_group)

        info_text = f"""BACH-Ordner: {BACH_DIR}
Daemon-Script: {DAEMON_SCRIPT}
Config: {CONFIG_FILE}
Templates: {TEMPLATES_DIR}
Profile: {PROFILES_DIR}
System Tray: {'Verfuegbar' if QSystemTrayIcon.isSystemTrayAvailable() else 'Nicht verfuegbar'}"""

        info_label = QLabel(info_text)
        info_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-family: Consolas;")
        info_layout.addWidget(info_label)

        layout.addWidget(info_group)

        # Speichern-Button
        save_btn = QPushButton("Einstellungen speichern")
        save_btn.setStyleSheet(f"background-color: {COLORS['success']}; color: white;")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        layout.addStretch()

    # ==================== 4. LOG TAB ====================

    def create_log_tab(self):
        """Log-Tab."""
        tab = QWidget()
        self.tabs.addTab(tab, "Log")

        layout = QVBoxLayout(tab)

        # Log-Anzeige
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Consolas", 9))
        self.log_display.setStyleSheet(f"background-color: {COLORS['bg_input']};")
        layout.addWidget(self.log_display)

        # Buttons
        btn_layout = QHBoxLayout()

        refresh_btn = QPushButton("Aktualisieren")
        refresh_btn.clicked.connect(self.refresh_log)
        btn_layout.addWidget(refresh_btn)

        clear_btn = QPushButton("Leeren")
        clear_btn.clicked.connect(self.log_display.clear)
        btn_layout.addWidget(clear_btn)

        btn_layout.addStretch()

        layout.addLayout(btn_layout)

    # ==================== 2. DAEMON-STEUERUNG ====================

    def start_daemon(self):
        """Daemon Start."""
        interval = self.interval_spin.value()

        self.start_btn.setEnabled(False)
        self.statusbar.showMessage("Starte Daemon...")

        self.daemon_worker = DaemonStartWorker(interval)
        self.daemon_worker.finished.connect(self.on_daemon_started)
        self.daemon_worker.start()

    def on_daemon_started(self, success: bool, message: str):
        """Callback nach Daemon-Start."""
        if success:
            self.daemon_running = True
            self.daemon_started_at = time.time()
            self.daemon_interval_sec = self.interval_spin.value() * 60
            self.daemon_max_sessions = 0 if self.unlimited_check.isChecked() else self.max_sessions_spin.value()

            self.status_dot.setStyleSheet(f"color: {COLORS['success']};")
            self.status_label.setText(f"Daemon laeuft ({self.interval_spin.value()} Min)")
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)

            self.log(f"Daemon gestartet (Intervall: {self.interval_spin.value()} Min)")
        else:
            self.start_btn.setEnabled(True)
            self.log(f"Daemon-Start fehlgeschlagen: {message}")

        self.statusbar.showMessage(message, 3000)

    def stop_daemon(self):
        """Daemon Stop."""
        kill_all_daemons()

        self.daemon_running = False
        self.daemon_started_at = None
        self.daemon_interval_sec = 0

        self.status_dot.setStyleSheet(f"color: {COLORS['text_muted']};")
        self.status_label.setText("Daemon gestoppt")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.countdown_label.setText("--:--")
        self.session_counter.setText("0 / ∞")

        self.log("Daemon gestoppt")
        self.statusbar.showMessage("Daemon gestoppt", 3000)

    def toggle_max_sessions(self, state):
        """Auto-Stop Toggle."""
        self.max_sessions_spin.setEnabled(state != Qt.CheckState.Checked.value)
        if state == Qt.CheckState.Checked.value:
            self.max_sessions_spin.setValue(0)

    def get_extrapolated_session_count(self) -> int:
        """Session-Counter aus Laufzeit."""
        if not self.daemon_started_at or not self.daemon_running:
            return 0

        elapsed_sec = time.time() - self.daemon_started_at
        elapsed_min = elapsed_sec / 60
        safety_min = 0.75

        if elapsed_min < safety_min:
            return 0

        interval_min = self.daemon_interval_sec / 60
        if interval_min <= 0:
            return 0

        return int((elapsed_min - safety_min) / interval_min)

    def get_time_to_next_session(self) -> int:
        """Sekunden bis zur naechsten Session."""
        if not self.daemon_started_at or not self.daemon_running:
            return 0

        elapsed = time.time() - self.daemon_started_at
        if self.daemon_interval_sec <= 0:
            return 0

        return int(self.daemon_interval_sec - (elapsed % self.daemon_interval_sec))

    # ==================== HILFSFUNKTIONEN ====================

    def start_session_now(self):
        """Session-Trigger."""
        self.statusbar.showMessage("Starte Session...")
        profile_name = self.profile_combo.currentText() if hasattr(self, 'profile_combo') else "ati"

        # Arbeitszeit aus Einstellungen holen
        work_time = self.session_duration.value() if hasattr(self, 'session_duration') else 15

        self.session_worker = SessionTriggerWorker(
            profile_name=profile_name,
            work_time_minutes=work_time
        )
        self.session_worker.finished.connect(self.on_session_finished)
        self.session_worker.start()

    def on_session_finished(self, success: bool, message: str):
        """Callback nach Session-Start."""
        if success:
            self.log(f"Session gestartet: {message}")
            self.last_session_label.setText(datetime.now().strftime("%H:%M:%S"))
        else:
            self.log(f"Session-Fehler: {message}")

        self.statusbar.showMessage(message, 3000)

    def update_daemon_status(self):
        """Daemon-Status aktualisieren."""
        pid = get_daemon_pid()

        if pid > 0:
            if not self.daemon_running:
                self.daemon_running = True
                self.daemon_started_at = time.time()

                config = load_config()
                if config.get("jobs"):
                    self.daemon_interval_sec = config["jobs"][0].get("interval_minutes", 30) * 60

            self.status_dot.setStyleSheet(f"color: {COLORS['success']};")

            config = load_config()
            if is_quiet_time(config.get("quiet_start", "22:00"), config.get("quiet_end", "08:00")):
                self.status_label.setText("RUHEZEIT - wartend")
                self.status_dot.setStyleSheet(f"color: {COLORS['warning']};")
            else:
                interval = self.daemon_interval_sec / 60
                self.status_label.setText(f"Daemon laeuft ({interval} Min)")

            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.pid_label.setText(str(pid))
        else:
            if self.daemon_running:
                self.daemon_running = False
                self.daemon_started_at = None

            self.status_dot.setStyleSheet(f"color: {COLORS['text_muted']};")
            self.status_label.setText("Daemon gestoppt")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.pid_label.setText("-")

    def periodic_update(self):
        """Periodisches Update (jede Sekunde)."""
        self.update_daemon_status()

        if self.daemon_running:
            current = self.get_extrapolated_session_count()
            max_sess = self.daemon_max_sessions

            if max_sess > 0:
                self.session_counter.setText(f"{current} / {max_sess}")
            else:
                self.session_counter.setText(f"{current} / ∞")

            remaining = self.get_time_to_next_session()
            if remaining > 0:
                mins = remaining / 60
                secs = remaining % 60
                self.countdown_label.setText(f"{mins:02d}:{secs:02d}")
            else:
                self.countdown_label.setText("Jetzt!")

        # Task-Count (alle 5 Sekunden)
        if int(time.time()) % 5 == 0:
            self.tasks_label.setText(str(count_open_tasks()))

    # ==================== EINSTELLUNGEN ====================

    def save_settings(self):
        """Einstellungen speichern."""
        config = load_config()

        config["quiet_start"] = self.quiet_start.text()
        config["quiet_end"] = self.quiet_end.text()
        config["ignore_quiet"] = self.ignore_quiet.isChecked()

        if config.get("jobs"):
            config["jobs"][0]["profile"] = self.profile_combo.currentText()
            config["jobs"][0]["interval_minutes"] = self.interval_spin.value()

        save_config(config)

        self.log("Einstellungen gespeichert")
        self.statusbar.showMessage("Einstellungen gespeichert", 3000)

    def load_settings(self):
        """Einstellungen laden."""
        config = load_config()

        self.quiet_start.setText(config.get("quiet_start", "22:00"))
        self.quiet_end.setText(config.get("quiet_end", "08:00"))
        self.ignore_quiet.setChecked(config.get("ignore_quiet", False))

        if config.get("jobs"):
            job = config["jobs"][0]
            self.interval_spin.setValue(job.get("interval_minutes", 30))

            profile = job.get("profile", "ati")
            idx = self.profile_combo.findText(profile)
            if idx >= 0:
                self.profile_combo.setCurrentIndex(idx)

    # ==================== LOG ====================

    def log(self, message: str):
        """Nachricht ins Log schreiben."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_display.append(f"[{timestamp}] {message}")

    def refresh_log(self):
        """Daemon-Log laden."""
        if LOG_FILE.exists():
            try:
                content = LOG_FILE.read_text(encoding="utf-8")
                lines = content.strip().split("\n")[-50:]
                self.log_display.setPlainText("\n".join(lines))
            except Exception as e:
                self.log_display.setPlainText(f"Fehler beim Laden: {e}")
        else:
            self.log_display.setPlainText("Keine Log-Datei gefunden")


# ============ 6. CLI-INTERFACE ============

def run_cli():
    """CLI-Interface fuer Prompt-Manager."""
    parser = argparse.ArgumentParser(
        description="BACH Prompt-Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python prompt_manager.py                     # GUI starten
  python prompt_manager.py --list              # Templates auflisten
  python prompt_manager.py --generate ati      # Session-Prompt generieren
  python prompt_manager.py --start ati         # Session direkt starten
  python prompt_manager.py --copy ati          # Prompt in Zwischenablage
  python prompt_manager.py --dry-run ati       # Prompt nur anzeigen
  python prompt_manager.py --daemon start      # Daemon starten
  python prompt_manager.py --daemon stop       # Daemon stoppen
  python prompt_manager.py --status            # Daemon-Status
        """
    )

    parser.add_argument("--list", "-l", action="store_true", help="Templates auflisten")
    parser.add_argument("--generate", "-g", metavar="PROFILE", help="Session-Prompt generieren")
    parser.add_argument("--start", "-s", metavar="PROFILE", help="Session direkt starten")
    parser.add_argument("--copy", "-c", metavar="PROFILE", help="Prompt in Zwischenablage")
    parser.add_argument("--dry-run", "-n", metavar="PROFILE", help="Prompt nur anzeigen (kein Start)")
    parser.add_argument("--daemon", "-d", choices=["start", "stop", "status"], help="Daemon steuern")
    parser.add_argument("--status", action="store_true", help="Daemon-Status anzeigen")
    parser.add_argument("--force", "-f", action="store_true", help="Screen-Lock ignorieren")
    parser.add_argument("--interval", "-i", type=int, default=30, help="Daemon-Intervall (Minuten)")
    parser.add_argument("--gui", action="store_true", help="GUI starten (Default)")

    args = parser.parse_args()

    # Wenn keine CLI-Argumente, GUI starten
    if len(sys.argv) == 1 or args.gui:
        return None  # Signal fuer GUI-Start

    # Templates auflisten
    if args.list:
        templates = list_templates()
        print("BACH Prompt-Manager - Templates")
        print("=" * 40)
        for category, items in templates.items():
            if items:
                print(f"\n{category.upper()}:")
                for item in items:
                    edit = "" if not item["editable"] else " (editable)"
                    print(f"  {item['path']}{edit}")
                    if item["description"]:
                        print(f"    {item['description']}")
        return True

    # Prompt generieren
    if args.generate:
        profile = load_profile(args.generate)
        prompt = generate_session_prompt(profile)
        print(prompt)
        return True

    # Prompt anzeigen (dry-run)
    if args.dry_run:
        profile = load_profile(args.dry_run)
        prompt = generate_session_prompt(profile)
        print("=" * 50)
        print(f"DRY-RUN: Profil '{args.dry_run}'")
        print("=" * 50)
        try:
            print(prompt[:2000])
        except UnicodeEncodeError:
            safe = prompt[:2000].encode('ascii', 'ignore').decode('ascii')
            print(safe)
        if len(prompt) > 2000:
            print(f"\n... ({len(prompt) - 2000} weitere Zeichen)")
        return True

    # Prompt in Zwischenablage
    if args.copy:
        profile = load_profile(args.copy)
        prompt = generate_session_prompt(profile)
        try:
            import pyperclip
            pyperclip.copy(prompt)
            print(f"Prompt kopiert ({len(prompt)} Zeichen)")
        except ImportError:
            print("FEHLER: pyperclip nicht installiert")
            return False
        return True

    # Session starten
    if args.start:
        if not args.force and is_screen_locked():
            print("ABBRUCH: Bildschirm ist gesperrt!")
            print("Verwende --force um trotzdem fortzufahren.")
            return False

        profile = load_profile(args.start)
        prompt = generate_session_prompt(profile)

        try:
            import pyautogui
            import pyperclip

            print(f"Starte Session mit Profil '{args.start}'...")
            time.sleep(3)

            pyperclip.copy(prompt)
            pyautogui.hotkey('ctrl', 'alt', 'space')
            time.sleep(1.0)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            pyautogui.press('enter')

            print(f"Session gestartet ({len(prompt)} Zeichen)")
        except ImportError:
            print("FEHLER: pyautogui/pyperclip nicht installiert")
            return False
        return True

    # Daemon-Status
    if args.status or args.daemon == "status":
        pid = get_daemon_pid()
        config = load_config()

        print("BACH Daemon-Status")
        print("=" * 40)
        print(f"Laeuft: {'Ja' if pid > 0 else 'Nein'}")
        if pid > 0:
            print(f"PID: {pid}")
        if config.get("jobs"):
            job = config["jobs"][0]
            print(f"Profil: {job.get('profile', 'ati')}")
            print(f"Intervall: {job.get('interval_minutes', 30)} Min")
        print(f"Ruhezeit: {config.get('quiet_start', '22:00')} - {config.get('quiet_end', '08:00')}")
        print(f"Ruhezeit aktiv: {'Ja' if is_quiet_time(config.get('quiet_start'), config.get('quiet_end')) else 'Nein'}")
        print(f"Offene Tasks: {count_open_tasks()}")
        return True

    # Daemon starten
    if args.daemon == "start":
        kill_all_daemons()
        time.sleep(0.3)

        config = load_config()
        if config.get("jobs"):
            config["jobs"][0]["interval_minutes"] = args.interval
            config["jobs"][0]["enabled"] = True
            config["jobs"][0]["last_run"] = None
        save_config(config)

        python_exe = sys.executable
        creation_flags = 0x08000000 if sys.platform == "win32" else 0

        subprocess.Popen(
            [python_exe, str(DAEMON_SCRIPT)],
            cwd=str(DAEMON_DIR),
            creationflags=creation_flags,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(1)
        if get_daemon_pid() > 0:
            print(f"Daemon gestartet (Intervall: {args.interval} Min)")
        else:
            print("Daemon-Start fehlgeschlagen")
            return False
        return True

    # Daemon stoppen
    if args.daemon == "stop":
        kill_all_daemons()
        print("Daemon gestoppt")
        return True

    return None


# ============ MAIN ============

def main():
    # CLI zuerst pruefen
    cli_result = run_cli()
    if cli_result is not None:
        sys.exit(0 if cli_result else 1)

    # Single-Instance Check
    if not check_single_instance():
        print("Prompt-Manager laeuft bereits!")
        # Versuche bestehendes Fenster in Vordergrund zu bringen
        if sys.platform == "win32":
            try:
                import subprocess
                # Finde Fenster und bringe in Vordergrund
                subprocess.run([
                    "powershell", "-Command",
                    "(Get-Process | Where-Object {$_.MainWindowTitle -like '*Prompt*Manager*'}).MainWindowHandle | ForEach-Object { [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject([System.Runtime.InteropServices.Marshal]::GetActiveObject('Shell.Application')) }"
                ], capture_output=True, creationflags=0x08000000)
            except:
                pass
        sys.exit(0)

    # Qt App
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)

    # Cleanup bei Beenden
    import atexit
    atexit.register(cleanup_lock)

    # Hauptfenster
    window = PromptManagerWindow()
    window.load_settings()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
