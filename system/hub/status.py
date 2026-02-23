# SPDX-License-Identifier: MIT
"""
Status Handler - Schnelle System-Uebersicht
"""
from datetime import datetime
from pathlib import Path
import json
from .base import BaseHandler
from .lang import t


class StatusHandler(BaseHandler):
    """Handler fuer --status"""
    
    def __init__(self, base_path: Path):
        super().__init__(base_path)
    
    @property
    def profile_name(self) -> str:
        return "status"
    
    @property
    def target_file(self) -> Path:
        return self.base_path
    
    def get_operations(self) -> dict:
        return {"show": t("status_show_desc", default="Systemstatus anzeigen (Standard)")}
    
    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        return self._show_status()
    
    def _show_status(self) -> tuple:
        """Sammelt und zeigt Systemstatus."""
        now = datetime.now()
        results = []

        results.append(f"BACH Status @ {now.strftime('%Y-%m-%d %H:%M')}")
        results.append("=" * 45)

        # Memory Status
        memory_file = self.base_path / "memory" / "current.md"
        if memory_file.exists():
            content = memory_file.read_text(encoding="utf-8")
            lines = len(content.splitlines())

            if "BEREIT" in content.upper():
                mem_status = t("bereit", default="BEREIT")
            elif "AKTIV" in content.upper():
                mem_status = t("aktiv", default="AKTIV")
            elif "UNTERBROCHEN" in content.upper():
                mem_status = t("unterbrochen", default="UNTERBROCHEN") + " (!)"
            else:
                mem_status = "?"

            lines_label = t("zeilen", default="Zeilen")
            results.append(f"Memory:   {mem_status} ({lines} {lines_label})")
        else:
            results.append(f"Memory:   {t('keine_aktive_session', default='Keine aktive Session')}")

        # Chat
        chat_file = self.base_path / "memory" / "chat.json"
        if chat_file.exists():
            try:
                with open(chat_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                unresolved = len([m for m in data.get("messages", []) if not m.get("resolved")])
                results.append(f"Chat:     {unresolved} {t('offen', default='offen')}")
            except:
                results.append(f"Chat:     {t('fehler', default='Fehler')}")
        else:
            results.append(f"Chat:     0 {t('offen', default='offen')}")

        # Tasks
        tasks_file = self.base_path / "memory" / "tasks.json"
        if tasks_file.exists():
            try:
                with open(tasks_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                task_list = data.get("tasks", [])
                open_count = len([tk for tk in task_list if tk.get("status") == "open"])
                high_prio = len([tk for tk in task_list if tk.get("status") == "open" and tk.get("priority") in ["high", "critical"]])
                results.append(f"Tasks:    {open_count} open ({high_prio} high/critical)")
            except:
                results.append(f"Tasks:    {t('fehler', default='Fehler')}")
        else:
            results.append(f"Tasks:    {t('keine_datei', default='Keine Datei')}")

        # Tools
        tools_file = self.base_path / "tools" / "tools.json"
        if tools_file.exists():
            try:
                with open(tools_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                tool_count = len(data.get("tools", []))
                results.append(f"Tools:    {tool_count} {t('registriert', default='registriert')}")
            except:
                results.append(f"Tools:    {t('fehler', default='Fehler')}")

        # Health (JSONs pruefen)
        json_files = [
            self.base_path / "memory" / "chat.json",
            self.base_path / "memory" / "tasks.json",
            self.base_path / "tools" / "tools.json"
        ]

        all_valid = True
        for jf in json_files:
            if jf.exists():
                try:
                    with open(jf, "r", encoding="utf-8") as f:
                        json.load(f)
                except:
                    all_valid = False
                    break

        if all_valid:
            results.append("Health:   OK")
        else:
            results.append(f"Health:   {t('fehler', default='FEHLER')} (JSON {t('korrupt', default='korrupt')})")

        return True, "\n".join(results)
