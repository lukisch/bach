#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Reminder Injector -- SQ040
Injiziert Erinnerungen in den LLM-Prompt vor jedem Call.
Quellen: Offene Tasks, User-definierte Reminders, Zeitbasierte Trigger.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class ReminderInjector:
    """Injiziert aktive Reminders in LLM-Prompts."""

    TRIGGER_TYPES = ("always", "on_task", "time_based", "keyword_match")

    def __init__(self, base_path: Path, db=None):
        self.base_path = Path(base_path)
        self.db = db
        self._fallback_file = self.base_path / "data" / "reminders.json"

    # ── CRUD ──────────────────────────────────────────────────────────

    def list_reminders(self, active_only: bool = True) -> list[dict]:
        """Alle Reminders laden (DB oder JSON Fallback)."""
        if self.db:
            return self._list_from_db(active_only)
        return self._list_from_json(active_only)

    def add_reminder(self, message: str, trigger_condition: str = "always",
                     trigger_value: str = None, priority: int = 5) -> dict:
        """Neuen Reminder anlegen."""
        if trigger_condition not in self.TRIGGER_TYPES:
            raise ValueError(f"Ungueltiger Trigger: {trigger_condition}. "
                             f"Erlaubt: {self.TRIGGER_TYPES}")
        now = datetime.now().isoformat()
        reminder = {
            "trigger_condition": trigger_condition,
            "trigger_value": trigger_value,
            "message": message,
            "active": 1,
            "priority": priority,
            "last_triggered": None,
            "created_at": now,
            "updated_at": now,
        }
        if self.db:
            return self._add_to_db(reminder)
        return self._add_to_json(reminder)

    def update_reminder(self, reminder_id: int, **kwargs) -> bool:
        """Reminder aktualisieren."""
        allowed = {"message", "trigger_condition", "trigger_value",
                    "active", "priority"}
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return False
        updates["updated_at"] = datetime.now().isoformat()
        if self.db:
            return self._update_in_db(reminder_id, updates)
        return self._update_in_json(reminder_id, updates)

    def delete_reminder(self, reminder_id: int) -> bool:
        """Reminder loeschen."""
        if self.db:
            return self._delete_from_db(reminder_id)
        return self._delete_from_json(reminder_id)

    # ── Core Logic ────────────────────────────────────────────────────

    def get_active_reminders(self, context: dict) -> list[str]:
        """Gibt Reminder-Texte zurueck, die zum aktuellen Kontext passen."""
        reminders = self.list_reminders(active_only=True)
        matched = []

        for r in reminders:
            if self._matches_context(r, context):
                matched.append(r)

        # Nach Prioritaet sortieren (niedrig = wichtiger)
        matched.sort(key=lambda x: x.get("priority", 5))
        return [r["message"] for r in matched]

    def inject(self, prompt: str, context: dict) -> str:
        """Haengt Reminder-Block vor den Prompt."""
        messages = self.get_active_reminders(context)
        if not messages:
            return prompt

        block_lines = ["[BACH-REMINDERS]"]
        for i, msg in enumerate(messages, 1):
            block_lines.append(f"  {i}. {msg}")
        block_lines.append("[/BACH-REMINDERS]")
        block_lines.append("")

        return "\n".join(block_lines) + prompt

    # ── Matching ──────────────────────────────────────────────────────

    def _matches_context(self, reminder: dict, context: dict) -> bool:
        """Prueft ob ein Reminder zum Kontext passt."""
        trigger = reminder.get("trigger_condition", "always")
        value = reminder.get("trigger_value")

        if trigger == "always":
            return True

        if trigger == "on_task":
            # Aktiv wenn ein Task laeuft
            return bool(context.get("active_task"))

        if trigger == "time_based":
            # value = "HH:MM-HH:MM" Zeitfenster
            if not value:
                return False
            return self._in_time_window(value)

        if trigger == "keyword_match":
            # value = komma-separierte Keywords
            if not value:
                return False
            text = context.get("user_input", "").lower()
            keywords = [kw.strip().lower() for kw in value.split(",")]
            return any(kw in text for kw in keywords)

        return False

    @staticmethod
    def _in_time_window(window: str) -> bool:
        """Prueft ob aktuelle Uhrzeit im Fenster liegt. Format: 'HH:MM-HH:MM'."""
        try:
            parts = window.split("-")
            if len(parts) != 2:
                return False
            start = datetime.strptime(parts[0].strip(), "%H:%M").time()
            end = datetime.strptime(parts[1].strip(), "%H:%M").time()
            now = datetime.now().time()
            if start <= end:
                return start <= now <= end
            # Ueber Mitternacht
            return now >= start or now <= end
        except (ValueError, IndexError):
            return False

    # ── DB Backend ────────────────────────────────────────────────────

    def _list_from_db(self, active_only: bool) -> list[dict]:
        query = "SELECT * FROM reminders"
        if active_only:
            query += " WHERE active = 1"
        query += " ORDER BY priority ASC"
        try:
            rows = self.db.execute(query).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return self._list_from_json(active_only)

    def _add_to_db(self, reminder: dict) -> dict:
        try:
            cursor = self.db.execute(
                """INSERT INTO reminders
                   (trigger_condition, trigger_value, message, active, priority,
                    last_triggered, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (reminder["trigger_condition"], reminder["trigger_value"],
                 reminder["message"], reminder["active"], reminder["priority"],
                 reminder["last_triggered"], reminder["created_at"],
                 reminder["updated_at"]))
            self.db.commit()
            reminder["id"] = cursor.lastrowid
            return reminder
        except Exception:
            return self._add_to_json(reminder)

    def _update_in_db(self, reminder_id: int, updates: dict) -> bool:
        try:
            sets = ", ".join(f"{k} = ?" for k in updates)
            vals = list(updates.values()) + [reminder_id]
            self.db.execute(
                f"UPDATE reminders SET {sets} WHERE id = ?", vals)
            self.db.commit()
            return True
        except Exception:
            return False

    def _delete_from_db(self, reminder_id: int) -> bool:
        try:
            self.db.execute("DELETE FROM reminders WHERE id = ?",
                            (reminder_id,))
            self.db.commit()
            return True
        except Exception:
            return False

    # ── JSON Fallback ─────────────────────────────────────────────────

    def _load_json(self) -> list[dict]:
        if self._fallback_file.exists():
            try:
                with open(self._fallback_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return []

    def _save_json(self, data: list[dict]):
        self._fallback_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._fallback_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _list_from_json(self, active_only: bool) -> list[dict]:
        data = self._load_json()
        if active_only:
            data = [r for r in data if r.get("active", 1)]
        return sorted(data, key=lambda x: x.get("priority", 5))

    def _add_to_json(self, reminder: dict) -> dict:
        data = self._load_json()
        max_id = max((r.get("id", 0) for r in data), default=0)
        reminder["id"] = max_id + 1
        data.append(reminder)
        self._save_json(data)
        return reminder

    def _update_in_json(self, reminder_id: int, updates: dict) -> bool:
        data = self._load_json()
        for r in data:
            if r.get("id") == reminder_id:
                r.update(updates)
                self._save_json(data)
                return True
        return False

    def _delete_from_json(self, reminder_id: int) -> bool:
        data = self._load_json()
        new_data = [r for r in data if r.get("id") != reminder_id]
        if len(new_data) == len(data):
            return False
        self._save_json(new_data)
        return True
