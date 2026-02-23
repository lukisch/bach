# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
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
Event Sources fuer den Watcher Daemon
=======================================
Jede Source pollt eine Kategorie von Events und liefert WatcherEvent-Objekte.

Version: 1.0.0
Erstellt: 2026-02-10
"""

import json
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List

try:
    from .classifier import WatcherEvent
except ImportError:
    from classifier import WatcherEvent


class BaseEventSource(ABC):
    """Gemeinsame Schnittstelle fuer alle Event-Quellen."""

    def __init__(self, base_path: Path, db_path: Path, config: dict = None):
        self.base_path = base_path
        self.db_path = db_path
        self.config = config or {}

    @abstractmethod
    def poll(self) -> List[WatcherEvent]:
        """Prueft auf neue Events. Gibt Liste von WatcherEvent zurueck."""
        pass

    @abstractmethod
    def is_enabled(self) -> bool:
        """Ob diese Quelle aktiv ist."""
        pass

    def _get_db(self) -> sqlite3.Connection:
        """Oeffnet DB-Verbindung."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn


class ConnectorEventSource(BaseEventSource):
    """
    Ueberwacht connector_messages auf unverarbeitete eingehende Nachrichten.

    Liest aus der DB statt selbst zu pollen - nutzt existierendes
    poll_and_route Daemon-Job das bereits Telegram/Discord abfragt.
    """

    def is_enabled(self) -> bool:
        return self.config.get("enabled", True)

    def poll(self) -> List[WatcherEvent]:
        events = []
        try:
            conn = self._get_db()

            # Stelle sicher dass watcher_classified Spalte existiert
            self._ensure_column(conn)

            rows = conn.execute(
                "SELECT id, connector_name, sender, content, created_at "
                "FROM connector_messages "
                "WHERE direction='in' AND watcher_classified=0 "
                "ORDER BY created_at ASC LIMIT 10"
            ).fetchall()

            for row in rows:
                events.append(WatcherEvent(
                    source="connector",
                    event_type="message",
                    content=row["content"] or "",
                    sender=row["sender"] or "unknown",
                    connector_name=row["connector_name"] or "",
                    recipient=row["sender"] or "",
                    timestamp=row["created_at"] or "",
                    source_id=row["id"],
                ))

            conn.close()
        except Exception:
            pass
        return events

    def mark_classified(self, source_id: int):
        """Markiert Nachricht als vom Watcher klassifiziert."""
        try:
            conn = self._get_db()
            conn.execute(
                "UPDATE connector_messages SET watcher_classified=1 WHERE id=?",
                (source_id,)
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _ensure_column(self, conn: sqlite3.Connection):
        """Stellt sicher dass watcher_classified Spalte existiert."""
        try:
            conn.execute("SELECT watcher_classified FROM connector_messages LIMIT 1")
        except sqlite3.OperationalError:
            try:
                conn.execute(
                    "ALTER TABLE connector_messages ADD COLUMN watcher_classified INTEGER DEFAULT 0"
                )
                conn.commit()
            except Exception:
                pass


class TaskQueueEventSource(BaseEventSource):
    """
    Ueberwacht BACH Task-Queue auf neue/dringende Tasks.

    Prueft tasks-Tabelle auf neue P1/P2 Tasks seit letztem Check.
    """

    def __init__(self, base_path: Path, db_path: Path, config: dict = None):
        super().__init__(base_path, db_path, config)
        self._last_check_id = 0

    def is_enabled(self) -> bool:
        return self.config.get("enabled", True)

    def poll(self) -> List[WatcherEvent]:
        events = []
        min_priority = self.config.get("min_priority", "P2")

        try:
            conn = self._get_db()
            rows = conn.execute(
                "SELECT id, title, priority, status, created_at "
                "FROM tasks "
                "WHERE id > ? AND status='pending' AND priority <= ? "
                "ORDER BY id ASC LIMIT 5",
                (self._last_check_id, min_priority)
            ).fetchall()

            for row in rows:
                events.append(WatcherEvent(
                    source="task_queue",
                    event_type="new_task",
                    content=f"[{row['priority']}] {row['title']}",
                    sender="bach-system",
                    timestamp=row["created_at"] or "",
                    source_id=row["id"],
                ))
                self._last_check_id = max(self._last_check_id, row["id"])

            conn.close()
        except Exception:
            pass
        return events


class FileSystemEventSource(BaseEventSource):
    """
    Ueberwacht konfigurierte Ordner auf neue Dateien.

    Einfaches Polling mit State-Tracking via JSON-Datei.
    """

    def __init__(self, base_path: Path, db_path: Path, config: dict = None):
        super().__init__(base_path, db_path, config)
        self._state_file = Path(__file__).parent / "fs_state.json"
        self._known_files = self._load_state()

    def is_enabled(self) -> bool:
        return self.config.get("enabled", False)

    def poll(self) -> List[WatcherEvent]:
        events = []
        watched_dirs = self.config.get("watched_dirs", [])
        extensions = set(self.config.get("extensions", [".pdf", ".docx", ".txt"]))

        for dir_path in watched_dirs:
            path = Path(dir_path)
            if not path.exists():
                continue

            for f in path.iterdir():
                if not f.is_file():
                    continue
                if f.suffix.lower() not in extensions:
                    continue

                file_key = str(f)
                if file_key not in self._known_files:
                    self._known_files.add(file_key)
                    events.append(WatcherEvent(
                        source="filesystem",
                        event_type="file_created",
                        content=f"Neue Datei: {f.name} ({f.suffix}, {f.stat().st_size} bytes)",
                        sender=str(path),
                        metadata={"path": str(f), "name": f.name, "size": f.stat().st_size}
                    ))

        if events:
            self._save_state()
        return events

    def _load_state(self) -> set:
        if self._state_file.exists():
            try:
                data = json.loads(self._state_file.read_text(encoding="utf-8"))
                return set(data.get("known_files", []))
            except Exception:
                pass
        return set()

    def _save_state(self):
        try:
            self._state_file.write_text(
                json.dumps({"known_files": list(self._known_files)}, indent=2),
                encoding="utf-8"
            )
        except Exception:
            pass


class ScheduledEventSource(BaseEventSource):
    """
    Feuert Events basierend auf Zeitplaenen.

    V1: Einfacher Intervall-Check. Cron kommt spaeter.
    """

    def __init__(self, base_path: Path, db_path: Path, config: dict = None):
        super().__init__(base_path, db_path, config)
        self._last_fired = {}

    def is_enabled(self) -> bool:
        return self.config.get("enabled", False)

    def poll(self) -> List[WatcherEvent]:
        events = []
        scheduled_events = self.config.get("events", [])
        now = datetime.now()

        for ev in scheduled_events:
            name = ev.get("name", "unknown")
            cron = ev.get("cron", "")
            if not cron:
                continue

            # V1: Einfacher Stunden-Match (Format "0 8 * * *" = 08:00)
            parts = cron.split()
            if len(parts) >= 2:
                try:
                    minute = int(parts[0])
                    hour = int(parts[1])
                    if now.hour == hour and now.minute == minute:
                        if name not in self._last_fired or \
                           self._last_fired[name].date() < now.date():
                            self._last_fired[name] = now
                            events.append(WatcherEvent(
                                source="scheduled",
                                event_type="cron",
                                content=f"Scheduled: {name}",
                                sender="scheduler",
                                metadata=ev,
                            ))
                except (ValueError, IndexError):
                    pass

        return events
