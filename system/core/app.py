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
App Container - Lightweight DI fuer BACH
=========================================
Kein Startup noetig - sofort einsatzbereit fuer CLI und Library.
Nutzt hub/bach_paths.py fuer Pfade (Single Source of Truth).
"""

import sys
from pathlib import Path
from typing import Optional

from .db import Database
from .hooks import hooks
from .registry import HandlerRegistry
from .aliases import COMMAND_ALIASES


class App:
    """Zentraler Container fuer BACH - CLI und Library."""

    def __init__(self, base_path: Path = None):
        """Initialisiert App mit Pfaden und Lazy-DB.

        Args:
            base_path: system/ Verzeichnis. Falls None, wird automatisch ermittelt.
        """
        if base_path is None:
            # Automatisch: Diese Datei liegt in system/core/app.py
            base_path = Path(__file__).parent.parent

        self.base_path = base_path
        self._db: Optional[Database] = None
        self._registry: Optional[HandlerRegistry] = None
        self._paths_loaded = False
        self.hooks = hooks  # Globale Hook-Registry

        # sys.path sicherstellen fuer Handler-Imports
        if str(base_path) not in sys.path:
            sys.path.insert(0, str(base_path))

    @property
    def db(self) -> Database:
        """Lazy-Initialisierte Datenbank."""
        if self._db is None:
            from hub.bach_paths import BACH_DB
            schema_dir = self.base_path / "db"
            self._db = Database(BACH_DB, schema_dir)
            # Schema anwenden (IF NOT EXISTS - sicher fuer bestehende DB)
            if schema_dir.exists() and (schema_dir / "schema.sql").exists():
                self._db.init_schema()
                self._db.run_migrations()
        return self._db

    @property
    def registry(self) -> HandlerRegistry:
        """Lazy-Initialisierte Handler-Registry."""
        if self._registry is None:
            self._registry = HandlerRegistry()
            hub_dir = self.base_path / "hub"
            self._registry.discover(hub_dir, aliases=COMMAND_ALIASES)
        return self._registry

    @property
    def paths(self):
        """Zugriff auf bach_paths Modul."""
        if not self._paths_loaded:
            hub_dir = str(self.base_path / "hub")
            if hub_dir not in sys.path:
                sys.path.insert(0, hub_dir)
            self._paths_loaded = True

        import hub.bach_paths as bp
        return bp

    def reload_registry(self) -> int:
        """Hot-Reload der Handler-Registry.

        Cleared alle Handler und entdeckt neu.
        Ermoeglicht das Hinzufuegen neuer Handler ohne Neustart.

        Returns:
            Anzahl gefundener Handler
        """
        hub_dir = self.base_path / "hub"
        if self._registry is None:
            self._registry = HandlerRegistry()
        return self._registry.reload(hub_dir, aliases=COMMAND_ALIASES)

    def get_handler(self, name: str):
        """Holt Handler-Instanz (Legacy oder New-Style).

        Args:
            name: Handler-Name (z.B. "task", "memory", "mem")

        Returns:
            Handler-Instanz oder None
        """
        return self.registry.get(name, base_path=self.base_path, app=self)

    def execute(self, command: str, operation: str = "", args: list = None) -> tuple:
        """Fuehrt Handler-Befehl aus.

        Args:
            command: Handler-Name (z.B. "task")
            operation: Operation (z.B. "list")
            args: Zusaetzliche Argumente

        Returns:
            (success, message) Tuple
        """
        handler = self.get_handler(command)
        if not handler:
            return (False, f"Unbekannter Befehl: {command}")

        # Hook: before_command
        self.hooks.emit('before_command', {
            'handler': command, 'operation': operation, 'args': args or []
        })

        try:
            success, message = handler.handle(operation, args or [])
        except Exception as e:
            success, message = False, f"Fehler in {command} {operation}: {e}"

        # Hook: after_command
        self.hooks.emit('after_command', {
            'handler': command, 'operation': operation,
            'success': success, 'args': args or []
        })

        return (success, message)
