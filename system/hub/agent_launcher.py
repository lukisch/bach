# SPDX-License-Identifier: MIT
"""
Agent Launcher Handler - Agent-Verwaltung
==========================================

bach agent list                          Verfuegbare Agents auflisten
bach agent start <name> [--mode MODE] [--model MODEL]   Agent starten
bach agent stop <name>                   Agent stoppen
bach agent status                        Laufende Agents anzeigen

Optionen:
  --mode plan|default     Modus (default: default)
  --model sonnet|opus|haiku   Modell (default: sonnet)
"""
import sys
import os
import signal
import subprocess
import json
from pathlib import Path
from datetime import datetime
from .base import BaseHandler


class AgentLauncherHandler(BaseHandler):
    """Handler fuer Agent-Operationen (list, start, stop, status)."""

    def __init__(self, base_path_or_app):
        super().__init__(base_path_or_app)
        self.agents_dir = self.base_path / "agents"
        self.experts_dir = self.base_path / "agents" / "_experts"
        self.data_dir = self.base_path / "data"
        self.pid_dir = self.data_dir / "agent_pids"
        self.temp_dir = self.data_dir / "temp"

    @property
    def profile_name(self) -> str:
        return "agent"

    @property
    def target_file(self) -> Path:
        return self.agents_dir

    def get_operations(self) -> dict:
        return {
            "list": "Verfuegbare Agents auflisten",
            "start": "Agent starten (bach agent start <name>)",
            "stop": "Agent stoppen (bach agent stop <name>)",
            "status": "Laufende Agents anzeigen"
        }

    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if operation == "list":
            return self._list_agents()
        elif operation == "start":
            if not args:
                return (False, "[ERROR] Agent-Name erforderlich: bach agent start <name>")
            name = args[0]
            return self._start_agent(name, args[1:], dry_run)
        elif operation == "stop":
            if not args:
                return (False, "[ERROR] Agent-Name erforderlich: bach agent stop <name>")
            return self._stop_agent(args[0], dry_run)
        elif operation == "status":
            return self._show_status()
        else:
            return self._list_agents()

    # ------------------------------------------------------------------
    # list
    # ------------------------------------------------------------------

    def _scan_agents(self) -> list:
        """Scannt agents/ und agents/_experts/ nach SKILL.md Dateien."""
        agents = []

        # Boss-Agents
        if self.agents_dir.exists():
            for entry in sorted(self.agents_dir.iterdir()):
                if not entry.is_dir() or entry.name.startswith("_"):
                    continue
                skill_file = entry / "SKILL.md"
                if skill_file.exists():
                    agents.append({
                        "name": entry.name,
                        "type": "boss",
                        "path": entry,
                        "skill_file": skill_file
                    })

        # Experten
        if self.experts_dir.exists():
            for entry in sorted(self.experts_dir.iterdir()):
                if not entry.is_dir() or entry.name.startswith("_"):
                    continue
                skill_file = entry / "SKILL.md"
                if skill_file.exists():
                    agents.append({
                        "name": entry.name,
                        "type": "expert",
                        "path": entry,
                        "skill_file": skill_file
                    })

        return agents

    def _is_agent_running(self, name: str) -> int:
        """Prueft ob Agent laeuft. Gibt PID oder 0 zurueck."""
        pid_file = self.pid_dir / f"{name}.pid"
        if not pid_file.exists():
            return 0
        try:
            data = json.loads(pid_file.read_text(encoding='utf-8'))
            pid = data.get("pid", 0)
            if not pid:
                return 0
            if sys.platform == 'win32':
                result = subprocess.run(
                    ['tasklist', '/FI', f'PID eq {pid}'],
                    capture_output=True, text=True
                )
                if str(pid) in result.stdout:
                    return pid
                # Prozess nicht mehr da, PID-File aufraeumen
                pid_file.unlink(missing_ok=True)
                return 0
            else:
                os.kill(pid, 0)
                return pid
        except (json.JSONDecodeError, ValueError, ProcessLookupError, PermissionError):
            return 0
        except OSError:
            pid_file.unlink(missing_ok=True)
            return 0

    def _list_agents(self) -> tuple:
        """Listet alle verfuegbaren Agents."""
        agents = self._scan_agents()

        if not agents:
            return (True, "Keine Agents mit SKILL.md gefunden.")

        output = [
            "=== VERFUEGBARE AGENTS ===",
            "",
            f"{'Name':25} {'Typ':8} {'Status':10}",
            "-" * 45
        ]

        for ag in agents:
            pid = self._is_agent_running(ag["name"])
            status = f"[RUNNING:{pid}]" if pid else "[STOPPED]"
            output.append(f"{ag['name']:25} {ag['type']:8} {status}")

        output.extend([
            "",
            "--- Befehle ---",
            "bach agent start <name>    Agent starten",
            "bach agent stop <name>     Agent stoppen",
            "bach agent status          Laufende Agents"
        ])

        return (True, "\n".join(output))

    # ------------------------------------------------------------------
    # start
    # ------------------------------------------------------------------

    def _parse_flag(self, args: list, flag: str, default: str) -> str:
        """Extrahiert --flag value aus args."""
        for i, arg in enumerate(args):
            if arg == flag and i + 1 < len(args):
                return args[i + 1]
        return default

    def _start_agent(self, name: str, args: list, dry_run: bool) -> tuple:
        """Startet einen Agent."""
        # Agent finden
        agents = self._scan_agents()
        agent = None
        for ag in agents:
            if ag["name"] == name:
                agent = ag
                break

        if not agent:
            return (False, f"[ERROR] Agent '{name}' nicht gefunden oder hat keine SKILL.md")

        # Bereits laufend?
        pid = self._is_agent_running(name)
        if pid:
            return (False, f"[WARN] Agent '{name}' laeuft bereits (PID {pid})")

        mode = self._parse_flag(args, "--mode", "default")
        model = self._parse_flag(args, "--model", "sonnet")

        if mode not in ("plan", "default"):
            return (False, f"[ERROR] Ungueltiger Modus: {mode} (erlaubt: plan, default)")
        if model not in ("sonnet", "opus", "haiku"):
            return (False, f"[ERROR] Ungueltiges Modell: {model} (erlaubt: sonnet, opus, haiku)")

        if dry_run:
            return (True, f"[DRY-RUN] Wuerde Agent '{name}' starten (mode={mode}, model={model})")

        # Verzeichnisse sicherstellen
        self.pid_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        # Temporaere CLAUDE.md erstellen
        agent_temp_dir = self.temp_dir / f"agent_{name}"
        agent_temp_dir.mkdir(parents=True, exist_ok=True)
        claude_md = agent_temp_dir / "CLAUDE.md"

        try:
            skill_content = agent["skill_file"].read_text(encoding='utf-8')
        except Exception as e:
            return (False, f"[ERROR] SKILL.md nicht lesbar: {e}")

        claude_md_content = (
            f"# BACH Agent: {name}\n\n"
            f"Du bist der BACH Agent \"{name}\". Befolge die folgende SKILL.md\n"
            f"als deine Identitaet und Arbeitsanweisung.\n\n"
            f"BACH System-Pfad: {self.base_path}\n"
            f"Nutze die Tools und Dateien im BACH-System unter diesem Pfad.\n"
            f"Antworte auf Deutsch.\n\n"
            f"---\n\n"
            f"{skill_content}"
        )

        try:
            claude_md.write_text(claude_md_content, encoding='utf-8')
        except Exception as e:
            return (False, f"[ERROR] CLAUDE.md konnte nicht geschrieben werden: {e}")

        # Claude-Prozess starten
        cmd = ["claude", "--model", model]

        if mode == "plan":
            cmd.extend(["--plan-mode", "plan"])

        try:
            if sys.platform == 'win32':
                # Windows: neues Fenster via cmd /c start
                title = f"BACH: {name}"
                # start.bat im Temp-Verzeichnis erstellen
                start_bat = agent_temp_dir / "start.bat"
                bat_content = (
                    f"@echo off\n"
                    f"title {title}\n"
                    f"cd /d \"{agent_temp_dir}\"\n"
                    f"echo === BACH Agent: {name} ===\n"
                    f"echo Modell: {model} ^| Modus: {mode}\n"
                    f"echo.\n"
                    f"{' '.join(cmd)}\n"
                    f"echo.\n"
                    f"echo Session beendet. Druecke eine Taste...\n"
                    f"pause\n"
                )
                start_bat.write_text(bat_content, encoding='utf-8')

                proc = subprocess.Popen(
                    ["cmd", "/c", "start", f"BACH: {name}", "cmd", "/c", str(start_bat)],
                    cwd=str(agent_temp_dir),
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                proc = subprocess.Popen(
                    cmd,
                    cwd=str(agent_temp_dir),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )

            # PID speichern
            pid_data = {
                "pid": proc.pid,
                "name": name,
                "type": agent["type"],
                "model": model,
                "mode": mode,
                "started": datetime.now().isoformat(),
                "temp_dir": str(agent_temp_dir)
            }
            pid_file = self.pid_dir / f"{name}.pid"
            pid_file.write_text(json.dumps(pid_data, indent=2), encoding='utf-8')

            return (True, (
                f"[OK] Agent '{name}' gestartet\n"
                f"     PID:    {proc.pid}\n"
                f"     Typ:    {agent['type']}\n"
                f"     Modell: {model}\n"
                f"     Modus:  {mode}\n"
                f"     Temp:   {agent_temp_dir}"
            ))

        except FileNotFoundError:
            return (False, "[ERROR] 'claude' CLI nicht gefunden. Ist Claude Code installiert?")
        except Exception as e:
            return (False, f"[ERROR] Start fehlgeschlagen: {e}")

    # ------------------------------------------------------------------
    # stop
    # ------------------------------------------------------------------

    def _stop_agent(self, name: str, dry_run: bool) -> tuple:
        """Stoppt einen laufenden Agent."""
        pid_file = self.pid_dir / f"{name}.pid"

        if not pid_file.exists():
            return (False, f"[WARN] Agent '{name}' hat kein PID-File (laeuft nicht)")

        try:
            data = json.loads(pid_file.read_text(encoding='utf-8'))
            pid = data.get("pid", 0)
        except (json.JSONDecodeError, ValueError):
            pid_file.unlink(missing_ok=True)
            return (False, f"[ERROR] PID-File fuer '{name}' ist ungueltig (entfernt)")

        if not pid:
            pid_file.unlink(missing_ok=True)
            return (False, f"[ERROR] Keine PID fuer Agent '{name}' (PID-File entfernt)")

        if dry_run:
            return (True, f"[DRY-RUN] Wuerde Agent '{name}' (PID {pid}) stoppen")

        try:
            if sys.platform == 'win32':
                subprocess.run(
                    ['taskkill', '/PID', str(pid), '/T', '/F'],
                    capture_output=True
                )
            else:
                os.kill(pid, signal.SIGTERM)

            # PID-File entfernen
            pid_file.unlink(missing_ok=True)

            return (True, f"[OK] Agent '{name}' (PID {pid}) gestoppt")

        except Exception as e:
            pid_file.unlink(missing_ok=True)
            return (False, f"[ERROR] Stoppen fehlgeschlagen: {e}")

    # ------------------------------------------------------------------
    # status
    # ------------------------------------------------------------------

    def _show_status(self) -> tuple:
        """Zeigt alle laufenden Agents."""
        self.pid_dir.mkdir(parents=True, exist_ok=True)

        pid_files = list(self.pid_dir.glob("*.pid"))

        if not pid_files:
            return (True, "=== AGENT STATUS ===\n\nKeine Agents registriert.")

        output = [
            "=== AGENT STATUS ===",
            "",
            f"{'Name':25} {'PID':>7}  {'Modell':8} {'Modus':8} {'Gestartet':20} {'Status':10}",
            "-" * 85
        ]

        active = 0
        for pf in sorted(pid_files):
            try:
                data = json.loads(pf.read_text(encoding='utf-8'))
                name = data.get("name", pf.stem)
                pid = data.get("pid", 0)
                model = data.get("model", "?")
                mode = data.get("mode", "?")
                started = data.get("started", "?")
                if started and started != "?":
                    started = started[:19]  # ISO ohne Microseconds

                # Pruefen ob Prozess noch laeuft
                running = False
                if pid:
                    if sys.platform == 'win32':
                        result = subprocess.run(
                            ['tasklist', '/FI', f'PID eq {pid}'],
                            capture_output=True, text=True
                        )
                        running = str(pid) in result.stdout
                    else:
                        try:
                            os.kill(pid, 0)
                            running = True
                        except OSError:
                            running = False

                status = "[RUNNING]" if running else "[DEAD]"
                if running:
                    active += 1
                else:
                    # Totes PID-File aufraeumen
                    pf.unlink(missing_ok=True)

                output.append(f"{name:25} {pid:>7}  {model:8} {mode:8} {started:20} {status}")

            except (json.JSONDecodeError, ValueError):
                output.append(f"{pf.stem:25} {'?':>7}  {'?':8} {'?':8} {'?':20} [INVALID]")
                pf.unlink(missing_ok=True)

        output.extend([
            "",
            f"Aktiv: {active} / {len(pid_files)}"
        ])

        return (True, "\n".join(output))
