#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Meta-Feedback Injector -- SQ042
Erkennt wiederkehrende LLM-Ticks und injiziert Korrektur-Feedback.
Auto-Deaktivierung wenn Pattern nicht mehr auftritt.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional


# Standard-Patterns fuer haeufige LLM-Ticks
DEFAULT_PATTERNS = [
    {
        "id": 1,
        "pattern": r"(?i)\b(here|let me|I'll|sure|certainly)\b",
        "pattern_type": "regex",
        "correction": "Antworte IMMER auf Deutsch. Keine englischen Fuellwoerter.",
        "frequency": 0,
        "max_inactive_count": 10,
        "inactive_count": 0,
        "active": 1,
    },
    {
        "id": 2,
        "pattern": r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\u2600-\u26FF\u2700-\u27BF]",
        "pattern_type": "regex",
        "correction": "Verwende KEINE Emojis in Antworten.",
        "frequency": 0,
        "max_inactive_count": 10,
        "inactive_count": 0,
        "active": 1,
    },
    {
        "id": 3,
        "pattern": r"(?i)(entschuldigung|tut mir leid|sorry|ich entschuldige|verzeih)",
        "pattern_type": "regex",
        "correction": "Keine uebertriebenen Entschuldigungen. Direkt zur Sache kommen.",
        "frequency": 0,
        "max_inactive_count": 10,
        "inactive_count": 0,
        "active": 1,
    },
]


class MetaFeedbackInjector:
    """Erkennt LLM-Ticks und injiziert Korrektur-Feedback."""

    def __init__(self, base_path: Path, db=None):
        self.base_path = Path(base_path)
        self.db = db
        self._fallback_file = self.base_path / "data" / "meta_feedback_patterns.json"

    # ── Core Logic ────────────────────────────────────────────────────

    def check_response(self, response: str) -> list[dict]:
        """Prueft Response auf bekannte Patterns. Gibt Treffer zurueck."""
        patterns = self._list_patterns(active_only=True)
        matches = []

        for p in patterns:
            if self._pattern_matches(p, response):
                matches.append(p)
                self._record_hit(p)
            else:
                self._record_miss(p)

        return matches

    def inject_corrections(self, prompt: str) -> str:
        """Fuegt aktive Korrektur-Anweisungen zum Prompt hinzu."""
        patterns = self._list_patterns(active_only=True)
        # Nur Patterns mit mindestens einem bisherigen Treffer injizieren
        active = [p for p in patterns if p.get("frequency", 0) > 0]

        if not active:
            return prompt

        block_lines = ["[BACH-META-FEEDBACK]"]
        for p in active:
            block_lines.append(f"  - {p['correction']}")
        block_lines.append("[/BACH-META-FEEDBACK]")
        block_lines.append("")

        return "\n".join(block_lines) + prompt

    # ── Pattern Matching ──────────────────────────────────────────────

    @staticmethod
    def _pattern_matches(pattern: dict, text: str) -> bool:
        """Prueft ob ein Pattern im Text vorkommt."""
        p = pattern.get("pattern", "")
        ptype = pattern.get("pattern_type", "substring")

        if ptype == "regex":
            try:
                return bool(re.search(p, text))
            except re.error:
                return False
        elif ptype == "substring":
            return p.lower() in text.lower()
        return False

    # ── Hit/Miss Tracking ─────────────────────────────────────────────

    def _record_hit(self, pattern: dict):
        """Pattern wurde getroffen: frequency erhoehen, inactive_count zuruecksetzen."""
        pid = pattern.get("id")
        if not pid:
            return
        updates = {
            "frequency": pattern.get("frequency", 0) + 1,
            "inactive_count": 0,
            "updated_at": datetime.now().isoformat(),
        }
        self._update_pattern(pid, updates)

    def _record_miss(self, pattern: dict):
        """Pattern nicht getroffen: inactive_count erhoehen, ggf. deaktivieren."""
        pid = pattern.get("id")
        if not pid:
            return
        new_inactive = pattern.get("inactive_count", 0) + 1
        max_inactive = pattern.get("max_inactive_count", 10)
        updates = {
            "inactive_count": new_inactive,
            "updated_at": datetime.now().isoformat(),
        }
        if new_inactive >= max_inactive:
            updates["active"] = 0
        self._update_pattern(pid, updates)

    # ── CRUD ──────────────────────────────────────────────────────────

    def add_pattern(self, pattern: str, correction: str,
                    pattern_type: str = "substring",
                    max_inactive_count: int = 10) -> dict:
        """Neues Pattern anlegen."""
        now = datetime.now().isoformat()
        entry = {
            "pattern": pattern,
            "pattern_type": pattern_type,
            "correction": correction,
            "frequency": 0,
            "max_inactive_count": max_inactive_count,
            "inactive_count": 0,
            "active": 1,
            "created_at": now,
            "updated_at": now,
        }
        if self.db:
            return self._add_to_db(entry)
        return self._add_to_json(entry)

    def remove_pattern(self, pattern_id: int) -> bool:
        """Pattern loeschen."""
        if self.db:
            return self._delete_from_db(pattern_id)
        return self._delete_from_json(pattern_id)

    def reactivate_pattern(self, pattern_id: int) -> bool:
        """Deaktiviertes Pattern wieder aktivieren."""
        return self._update_pattern(pattern_id, {
            "active": 1,
            "inactive_count": 0,
            "updated_at": datetime.now().isoformat(),
        })

    # ── DB Backend ────────────────────────────────────────────────────

    def _list_patterns(self, active_only: bool = True) -> list[dict]:
        if self.db:
            return self._list_from_db(active_only)
        return self._list_from_json(active_only)

    def _update_pattern(self, pattern_id: int, updates: dict) -> bool:
        if self.db:
            return self._update_in_db(pattern_id, updates)
        return self._update_in_json(pattern_id, updates)

    def _list_from_db(self, active_only: bool) -> list[dict]:
        query = "SELECT * FROM meta_feedback_patterns"
        if active_only:
            query += " WHERE active = 1"
        try:
            rows = self.db.execute(query).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return self._list_from_json(active_only)

    def _add_to_db(self, entry: dict) -> dict:
        try:
            cursor = self.db.execute(
                """INSERT INTO meta_feedback_patterns
                   (pattern, pattern_type, correction, frequency,
                    max_inactive_count, inactive_count, active,
                    created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (entry["pattern"], entry["pattern_type"], entry["correction"],
                 entry["frequency"], entry["max_inactive_count"],
                 entry["inactive_count"], entry["active"],
                 entry["created_at"], entry["updated_at"]))
            self.db.commit()
            entry["id"] = cursor.lastrowid
            return entry
        except Exception:
            return self._add_to_json(entry)

    def _update_in_db(self, pattern_id: int, updates: dict) -> bool:
        try:
            sets = ", ".join(f"{k} = ?" for k in updates)
            vals = list(updates.values()) + [pattern_id]
            self.db.execute(
                f"UPDATE meta_feedback_patterns SET {sets} WHERE id = ?", vals)
            self.db.commit()
            return True
        except Exception:
            return False

    def _delete_from_db(self, pattern_id: int) -> bool:
        try:
            self.db.execute(
                "DELETE FROM meta_feedback_patterns WHERE id = ?",
                (pattern_id,))
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
        return list(DEFAULT_PATTERNS)

    def _save_json(self, data: list[dict]):
        self._fallback_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._fallback_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _list_from_json(self, active_only: bool) -> list[dict]:
        data = self._load_json()
        if active_only:
            data = [p for p in data if p.get("active", 1)]
        return data

    def _add_to_json(self, entry: dict) -> dict:
        data = self._load_json()
        max_id = max((p.get("id", 0) for p in data), default=0)
        entry["id"] = max_id + 1
        data.append(entry)
        self._save_json(data)
        return entry

    def _update_in_json(self, pattern_id: int, updates: dict) -> bool:
        data = self._load_json()
        for p in data:
            if p.get("id") == pattern_id:
                p.update(updates)
                self._save_json(data)
                return True
        return False

    def _delete_from_json(self, pattern_id: int) -> bool:
        data = self._load_json()
        new_data = [p for p in data if p.get("id") != pattern_id]
        if len(new_data) == len(data):
            return False
        self._save_json(new_data)
        return True
