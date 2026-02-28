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
ATI Session Daemon v1.0
=======================
Laeuft im Hintergrund und startet Claude-Sessions in Intervallen.

Portiert von: _BATCH/session_daemon.py
Angepasst fuer: BACH v1.1 ATI Agent

Usage:
  python session_daemon.py                # Startet mit config
  python session_daemon.py --interval 30  # Alle 30 Minuten
  python session_daemon.py --stop         # Beendet laufenden Daemon
  python session_daemon.py --status       # Zeigt Status

Features:
  - Stoppt automatisch alte Instanz beim Start
  - Laedt Config bei jedem Intervall neu (live-aenderbar)
  - Ruhezeiten (z.B. nachts keine Sessions)
  - Integration mit BACH Memory und ATI Tasks
"""

import time
import sys
import os
import json
import subprocess
import signal
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread, Event

# ============ PFADE (relativ zu BACH) ============

# ATI Session-Ordner
ATI_SESSION_DIR = Path(__file__).parent.resolve()
ATI_DIR = ATI_SESSION_DIR.parent
BACH_DIR = ATI_DIR.parent.parent.parent

# Konfiguration
CONFIG_FILE = ATI_DIR / "data" / "config.json"
PID_FILE = ATI_SESSION_DIR / "daemon.pid"
LOG_FILE = BACH_DIR / "data" / "logs" / "ati_daemon.log"

# Datenbanken
USER_DB = BACH_DIR / "data" / "bach.db"
BACH_DB = BACH_DIR / "data" / "bach.db"

# Defaults
DEFAULT_INTERVAL = 30
DEFAULT_QUIET_START = "22:00"
DEFAULT_QUIET_END = "08:00"

# ============ LOGGING ============

def log(msg: str, level: str = "INFO"):
    """Logging in Datei und Console."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

# ============ CONFIG ============

def load_config() -> dict:
    """Laedt ATI-Konfiguration."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except:
            pass

    # Default-Config
    return {
        "enabled": True,
        "session": {
            "interval_minutes": DEFAULT_INTERVAL,
            "quiet_start": DEFAULT_QUIET_START,
            "quiet_end": DEFAULT_QUIET_END,
            "ignore_quiet": False,
            "timeout_minutes": 15,
            "max_tasks_per_session": 3
        }
    }

def save_config(config: dict):
    """Speichert Config."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

# ============ DAEMON CONTROL ============

def get_running_pid() -> int:
    """Gibt PID des laufenden Daemons zurueck, oder 0."""
    if not PID_FILE.exists():
        return 0
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)  # Prueft ob Prozess existiert
        return pid
    except (ProcessLookupError, ValueError, PermissionError):
        try:
            PID_FILE.unlink()
        except:
            pass
        return 0

def stop_old_daemon() -> bool:
    """Stoppt alte Instanz falls vorhanden."""
    pid = get_running_pid()
    if pid == 0:
        return True

    if pid == os.getpid():
        return True  # Das sind wir selbst

    log(f"Stoppe alte Instanz (PID {pid})...")
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        try:
            os.kill(pid, 0)
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        log("Alte Instanz gestoppt")
        return True
    except Exception as e:
        log(f"Fehler beim Stoppen: {e}", "ERROR")
        return False

def write_pid():
    """Schreibt PID-Datei."""
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()))

def show_status():
    """Zeigt Daemon-Status."""
    pid = get_running_pid()
    config = load_config()
    session_cfg = config.get("session", {})

    print("\n" + "=" * 50)
    print("ATI SESSION DAEMON STATUS")
    print("=" * 50)

    if pid:
        print(f"[OK] Daemon laeuft (PID {pid})")
    else:
        print("[--] Daemon laeuft nicht")

    print(f"\nConfig:")
    print(f"  Enabled: {config.get('enabled', True)}")
    print(f"  Intervall: {session_cfg.get('interval_minutes', DEFAULT_INTERVAL)} Min")
    print(f"  Ruhezeit: {session_cfg.get('quiet_start', DEFAULT_QUIET_START)} - {session_cfg.get('quiet_end', DEFAULT_QUIET_END)}")
    print(f"  Max Tasks/Session: {session_cfg.get('max_tasks_per_session', 3)}")

    # Offene Tasks zaehlen
    try:
        import sqlite3
        conn = sqlite3.connect(USER_DB)
        open_tasks = conn.execute(
            "SELECT COUNT(*) FROM ati_tasks WHERE status = 'offen'"
        ).fetchone()[0]
        conn.close()
        print(f"\nOffene ATI-Tasks: {open_tasks}")
    except Exception as e:
        print(f"\nATI-Tasks: Fehler ({e})")

    if LOG_FILE.exists():
        print(f"\nLetzte Log-Eintraege:")
        lines = LOG_FILE.read_text(encoding="utf-8").strip().split("\n")
        for line in lines[-5:]:
            print(f"  {line}")

    print("=" * 50)

# ============ QUIET HOURS ============

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

# ============ TASK LOGIC ============

def count_open_tasks() -> int:
    """Zaehlt offene ATI-Tasks in bach.db."""
    try:
        import sqlite3
        conn = sqlite3.connect(USER_DB)
        count = conn.execute(
            "SELECT COUNT(*) FROM ati_tasks WHERE status = 'offen'"
        ).fetchone()[0]
        conn.close()
        return count
    except:
        return 0

def get_top_tasks(limit: int = 3) -> list:
    """Holt die Top-Tasks nach Prioritaet."""
    try:
        import sqlite3
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
    except:
        return []

# ============ SESSION TRIGGER ============

def trigger_session() -> bool:
    """Triggert Claude-Session via auto_session.py."""
    auto_session = ATI_SESSION_DIR / "auto_session.py"

    if not auto_session.exists():
        log("auto_session.py nicht gefunden!", "ERROR")
        return False

    log("Starte auto_session.py...")
    try:
        creation_flags = 0x08000000 if sys.platform == "win32" else 0

        result = subprocess.run(
            [sys.executable, str(auto_session)],
            cwd=str(ATI_SESSION_DIR),
            capture_output=True,
            text=True,
            timeout=60,
            creationflags=creation_flags
        )

        if result.returncode == 0:
            log("Session erfolgreich gestartet")
            for line in result.stdout.strip().split('\n')[-5:]:
                if line.strip():
                    log(f"  {line.strip()}")
            return True
        else:
            log(f"auto_session.py Fehler: {result.stderr}", "ERROR")
            return False

    except subprocess.TimeoutExpired:
        log("auto_session.py Timeout (>60s)", "ERROR")
        return False
    except Exception as e:
        log(f"Trigger-Fehler: {e}", "ERROR")
        return False

# ============ MAIN LOOP ============

def daemon_loop(stop_event: Event):
    """Hauptschleife - laedt Config bei jedem Durchlauf neu."""

    first_run = True

    while not stop_event.is_set():
        try:
            # Config NEU laden
            config = load_config()
            session_cfg = config.get("session", {})

            interval = session_cfg.get("interval_minutes", DEFAULT_INTERVAL)
            quiet_start = session_cfg.get("quiet_start", DEFAULT_QUIET_START)
            quiet_end = session_cfg.get("quiet_end", DEFAULT_QUIET_END)
            ignore_quiet = session_cfg.get("ignore_quiet", False)

            # Deaktiviert?
            if not config.get("enabled", True):
                log("Daemon deaktiviert in config - warte 60s")
                stop_event.wait(60)
                continue

            # Ruhezeit?
            if not ignore_quiet and is_quiet_time(quiet_start, quiet_end):
                log(f"Ruhezeit ({quiet_start}-{quiet_end}) - warte 60s")
                stop_event.wait(60)
                continue

            # Erste Ausfuehrung: Kurzes Delay
            if first_run:
                log("Erste Ausfuehrung in 30 Sekunden...")
                stop_event.wait(30)
                if stop_event.is_set():
                    break
                first_run = False

            # Aufgaben pruefen
            tasks = count_open_tasks()
            log(f"Offene ATI-Tasks: {tasks}")

            if tasks > 0:
                # Top Tasks anzeigen
                top = get_top_tasks(3)
                for tool, text, aufwand, prio in top:
                    short = text[:40] + "..." if len(text) > 40 else text
                    log(f"  [{tool}] {short}")

                trigger_session()
            else:
                log("Keine offenen Tasks")

            # Warten
            next_run = datetime.now() + timedelta(minutes=interval)
            log(f"Naechste Pruefung: {next_run.strftime('%H:%M')} (in {interval} Min)")
            stop_event.wait(interval * 60)

        except Exception as e:
            log(f"Fehler: {e}", "ERROR")
            stop_event.wait(60)

# ============ MAIN ============

def main():
    # Status?
    if "--status" in sys.argv:
        show_status()
        return

    # Stop?
    if "--stop" in sys.argv:
        pid = get_running_pid()
        if pid:
            try:
                os.kill(pid, signal.SIGTERM)
                print(f"[OK] Daemon (PID {pid}) gestoppt")
                PID_FILE.unlink()
            except Exception as e:
                print(f"[!!] Fehler: {e}")
        else:
            print("Kein Daemon laeuft")
        return

    # Alte Instanz stoppen
    stop_old_daemon()

    # PID schreiben
    write_pid()

    # Config laden
    config = load_config()
    session_cfg = config.get("session", {})

    # CLI Override fuer Intervall
    interval = session_cfg.get("interval_minutes", DEFAULT_INTERVAL)
    for i, arg in enumerate(sys.argv):
        if arg == "--interval" and i + 1 < len(sys.argv):
            interval = int(sys.argv[i + 1])
            config.setdefault("session", {})["interval_minutes"] = interval
            save_config(config)

    log("=" * 50)
    log("ATI SESSION DAEMON")
    log(f"Intervall: {interval} Min")
    log(f"BACH: {BACH_DIR}")
    log("=" * 50)

    stop_event = Event()

    def signal_handler(sig, frame):
        log("Stop-Signal empfangen")
        stop_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    daemon_loop(stop_event)

    # Aufraeumen
    if PID_FILE.exists():
        try:
            PID_FILE.unlink()
        except:
            pass

    log("Daemon beendet")

if __name__ == "__main__":
    main()
