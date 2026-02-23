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
Agent Runtime - Instanziierbare Agenten für BACH
=================================================

Analog zum Connector-System: Agenten werden zu laufzeitfähigen Objekten.

Basis-Architektur:
  - AgentConfig: Konfiguration (wie ConnectorConfig)
  - BaseAgent: Abstrakte Basis-Klasse (wie BaseConnector)
  - AgentRegistry: Factory + Discovery
  - Agent-Instanzen: SteuerAgent, ResearchAgent, etc.

Usage:
    from core.agent_runtime import get_agent

    agent = get_agent("steuer-agent")
    if agent and agent.connect():
        success, msg = agent.execute("status", [])
        print(msg)

Autor: Claude Worker-Agent
Datum: 2026-02-14
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

# UTF-8 Encoding fix
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# ═══════════════════════════════════════════════════════════════
# Status & Config
# ═══════════════════════════════════════════════════════════════

class AgentStatus(Enum):
    """Agent-Status (analog zu ConnectorStatus)."""
    IDLE = "idle"
    CONNECTING = "connecting"
    READY = "ready"
    EXECUTING = "executing"
    ERROR = "error"
    DISCONNECTED = "disconnected"


@dataclass
class AgentConfig:
    """Agent-Konfiguration (analog zu ConnectorConfig)."""
    name: str
    agent_type: str  # 'expert', 'worker', 'boss', 'specialist'
    capabilities: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    base_path: Optional[Path] = None
    is_active: bool = True


# ═══════════════════════════════════════════════════════════════
# BaseAgent - Abstrakte Basis-Klasse
# ═══════════════════════════════════════════════════════════════

class BaseAgent:
    """Basis-Klasse für alle BACH-Agenten (analog zu BaseConnector)."""

    def __init__(self, config: AgentConfig):
        """
        Args:
            config: Agent-Konfiguration
        """
        self.config = config
        self.name = config.name
        self.agent_type = config.agent_type
        self.capabilities = config.capabilities
        self.status = AgentStatus.IDLE
        self.base_path = config.base_path or Path.cwd()

    def connect(self) -> bool:
        """
        Initialisiert den Agent (lädt Dependencies, prüft Verfügbarkeit).

        Returns:
            True wenn erfolgreich, False bei Fehler
        """
        raise NotImplementedError("Subclass must implement connect()")

    def disconnect(self) -> bool:
        """
        Räumt Ressourcen auf.

        Returns:
            True wenn erfolgreich
        """
        self.status = AgentStatus.DISCONNECTED
        return True

    def execute(self, operation: str, args: List[str]) -> Tuple[bool, str]:
        """
        Führt eine Agent-Operation aus.

        Args:
            operation: Operation-Name (z.B. "status", "scan")
            args: Argumente

        Returns:
            (success, message) Tuple
        """
        raise NotImplementedError("Subclass must implement execute()")

    def get_operations(self) -> Dict[str, str]:
        """
        Gibt verfügbare Operationen zurück.

        Returns:
            Dict {operation: description}
        """
        return {
            "status": "Agent-Status anzeigen",
            "help": "Hilfe anzeigen"
        }

    def _update_status(self, status: AgentStatus):
        """Interner Status-Update."""
        self.status = status

    def _log(self, message: str, level: str = "INFO"):
        """Einfaches Logging."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{self.name}] [{level}] {message}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════
# AgentRegistry - Factory + Discovery
# ═══════════════════════════════════════════════════════════════

class AgentRegistry:
    """Registry für Agent-Discovery und Instanziierung."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.db_path = base_path / "data" / "bach.db"
        self._cache: Dict[str, BaseAgent] = {}

    def get(self, name: str) -> Optional[BaseAgent]:
        """
        Holt oder erstellt eine Agent-Instanz.

        Args:
            name: Agent-Name (z.B. "steuer-agent")

        Returns:
            Agent-Instanz oder None
        """
        # Cache-Check
        if name in self._cache:
            return self._cache[name]

        # Aus DB laden
        config = self._load_config(name)
        if not config:
            return None

        # Instanz erstellen
        instance = self._instantiate(config)
        if instance:
            self._cache[name] = instance
            return instance

        return None

    def list_agents(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """
        Listet alle registrierten Agenten auf.

        Args:
            active_only: Nur aktive Agenten

        Returns:
            List von Agent-Info-Dicts
        """
        if not self.db_path.exists():
            return []

        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row

        try:
            if active_only:
                rows = conn.execute("""
                    SELECT name, agent_type, capabilities, is_active, last_used
                    FROM agent_instances
                    WHERE is_active = 1
                    ORDER BY name
                """).fetchall()
            else:
                rows = conn.execute("""
                    SELECT name, agent_type, capabilities, is_active, last_used
                    FROM agent_instances
                    ORDER BY name
                """).fetchall()

            return [dict(row) for row in rows]
        finally:
            conn.close()

    def register(self, config: AgentConfig) -> bool:
        """
        Registriert einen neuen Agent in der DB.

        Args:
            config: Agent-Konfiguration

        Returns:
            True wenn erfolgreich
        """
        if not self.db_path.exists():
            return False

        conn = sqlite3.connect(str(self.db_path))
        try:
            now = datetime.now().isoformat()
            conn.execute("""
                INSERT OR REPLACE INTO agent_instances
                (name, agent_type, capabilities, config, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                config.name,
                config.agent_type,
                json.dumps(config.capabilities, ensure_ascii=False),
                json.dumps(config.config, ensure_ascii=False),
                1 if config.is_active else 0,
                now
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"[AgentRegistry] Registration error: {e}", file=sys.stderr)
            return False
        finally:
            conn.close()

    def _load_config(self, name: str) -> Optional[AgentConfig]:
        """Lädt Agent-Config aus DB."""
        if not self.db_path.exists():
            return None

        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row

        try:
            row = conn.execute("""
                SELECT name, agent_type, capabilities, config, is_active
                FROM agent_instances
                WHERE name = ? OR name LIKE ?
            """, (name, f"%{name}%")).fetchone()

            if not row:
                return None

            capabilities = json.loads(row['capabilities']) if row['capabilities'] else []
            config_data = json.loads(row['config']) if row['config'] else {}

            return AgentConfig(
                name=row['name'],
                agent_type=row['agent_type'],
                capabilities=capabilities,
                config=config_data,
                base_path=self.base_path,
                is_active=bool(row['is_active'])
            )
        finally:
            conn.close()

    def _instantiate(self, config: AgentConfig) -> Optional[BaseAgent]:
        """
        Erstellt Agent-Instanz basierend auf agent_type.

        Sucht nach:
          1. agents/{name}_agent.py
          2. agents/_experts/{name}/{name}_agent.py
          3. Fallback: DummyAgent
        """
        agent_type = config.agent_type
        name_base = config.name.replace("-agent", "").replace("_agent", "")

        # Versuch 1: agents/{name}_agent.py
        try:
            module_name = f"{name_base}_agent"
            agents_dir = self.base_path / "agents"

            if str(agents_dir) not in sys.path:
                sys.path.insert(0, str(agents_dir))

            # Dynamischer Import
            module = __import__(module_name)

            # Suche nach Klasse (z.B. SteuerAgent)
            class_name = ''.join(word.capitalize() for word in name_base.split('_')) + 'Agent'

            if hasattr(module, class_name):
                agent_class = getattr(module, class_name)
                return agent_class(config)
        except ImportError:
            pass

        # Versuch 2: agents/_experts/{name}/
        try:
            expert_dir = self.base_path / "agents" / "_experts" / name_base
            if expert_dir.exists() and str(expert_dir) not in sys.path:
                sys.path.insert(0, str(expert_dir))

            module_name = f"{name_base}_agent"
            module = __import__(module_name)

            class_name = ''.join(word.capitalize() for word in name_base.split('_')) + 'Agent'
            if hasattr(module, class_name):
                agent_class = getattr(module, class_name)
                return agent_class(config)
        except ImportError:
            pass

        # Fallback: DummyAgent
        print(f"[AgentRegistry] No implementation found for '{config.name}', using DummyAgent",
              file=sys.stderr)
        return DummyAgent(config)


# ═══════════════════════════════════════════════════════════════
# DummyAgent - Fallback für nicht-implementierte Agenten
# ═══════════════════════════════════════════════════════════════

class DummyAgent(BaseAgent):
    """Dummy-Agent als Fallback."""

    def connect(self) -> bool:
        self.status = AgentStatus.READY
        return True

    def execute(self, operation: str, args: List[str]) -> Tuple[bool, str]:
        if operation == "status":
            return True, f"[DUMMY] Agent '{self.name}' ist bereit (keine echte Implementierung)."
        elif operation == "help":
            return True, f"[DUMMY] Agent '{self.name}' - Keine Operationen verfügbar."
        else:
            return False, f"[DUMMY] Operation '{operation}' nicht implementiert."


# ═══════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════

_registry: Optional[AgentRegistry] = None

def get_registry(base_path: Optional[Path] = None) -> AgentRegistry:
    """Holt oder erstellt die globale Agent-Registry."""
    global _registry
    if _registry is None:
        if base_path is None:
            # Auto-detect: Dieses Modul liegt in system/core/agent_runtime.py
            base_path = Path(__file__).parent.parent
        _registry = AgentRegistry(base_path)
    return _registry


def get_agent(name: str, base_path: Optional[Path] = None) -> Optional[BaseAgent]:
    """
    Haupteinstiegspunkt: Holt Agent-Instanz.

    Args:
        name: Agent-Name (z.B. "steuer-agent")
        base_path: Optional base path

    Returns:
        Agent-Instanz oder None

    Example:
        agent = get_agent("steuer-agent")
        if agent and agent.connect():
            success, msg = agent.execute("status", [])
    """
    registry = get_registry(base_path)
    return registry.get(name)


def list_agents(active_only: bool = False, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Listet alle Agenten auf.

    Args:
        active_only: Nur aktive Agenten
        base_path: Optional base path

    Returns:
        List von Agent-Info-Dicts
    """
    registry = get_registry(base_path)
    return registry.list_agents(active_only)


def register_agent(config: AgentConfig, base_path: Optional[Path] = None) -> bool:
    """
    Registriert einen Agent.

    Args:
        config: Agent-Konfiguration
        base_path: Optional base path

    Returns:
        True wenn erfolgreich
    """
    registry = get_registry(base_path)
    return registry.register(config)
