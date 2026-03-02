#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
PortableAgent Base Class v1.0.0

Abstrakte Basisklasse fuer BACH-Agenten mit Portabilitaet.
Agenten koennen sowohl mit als auch ohne BACH-Installation arbeiten.

Wenn BACH verfuegbar ist:
  - Config aus DB, Logging via BACH, Service-Binding
Wenn BACH nicht verfuegbar ist:
  - Config aus lokaler JSON, Standard-Python-Logging, Standalone-Betrieb
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

# --- BACH Detection ---
BACH_ROOT = Path(os.environ.get("BACH_ROOT", Path(__file__).parents[3]))
BACH_AVAILABLE = False

try:
    import sys
    _bach_core = BACH_ROOT / "system" / "core"
    if _bach_core.exists() and str(_bach_core) not in sys.path:
        sys.path.insert(0, str(_bach_core))
    from bach_api import BachAPI  # type: ignore
    BACH_AVAILABLE = True
except ImportError:
    BACH_AVAILABLE = False


def _get_fallback_logger(name: str) -> logging.Logger:
    """Erstellt Standard-Python-Logger als Fallback."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


class BACHAdapter:
    """Optionaler Wrapper fuer BACH-DB-Registrierung und Service-Binding."""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self._api = None
        if BACH_AVAILABLE:
            try:
                self._api = BachAPI()
            except Exception:
                pass

    @property
    def connected(self) -> bool:
        return self._api is not None

    def load_config(self, section: str = "agents") -> Dict:
        """Laedt Config aus BACH DB."""
        if not self.connected:
            return {}
        try:
            return self._api.get_config(section, self.agent_name) or {}
        except Exception:
            return {}

    def register_agent(self, metadata: Dict) -> bool:
        """Registriert Agent in BACH DB."""
        if not self.connected:
            return False
        try:
            self._api.register_agent(self.agent_name, metadata)
            return True
        except Exception:
            return False

    def get_logger(self, name: str) -> logging.Logger:
        """Holt BACH-Logger oder Fallback."""
        if self.connected:
            try:
                return self._api.get_logger(name)
            except Exception:
                pass
        return _get_fallback_logger(name)


class PortableAgent(ABC):
    """Abstrakte Basisklasse fuer portable BACH-Agenten.

    Unterklassen muessen implementieren:
      - run()
      - status()
      - config()
      - standalone_config_template()
    """

    AGENT_NAME: str = "PortableAgent"
    VERSION: str = "0.0.0"

    def __init__(self, config_path: Optional[str] = None):
        self._bach = BACHAdapter(self.AGENT_NAME)
        self.logger = self._bach.get_logger(self.AGENT_NAME)
        self._config = self._load_config(config_path)
        self.logger.info(
            f"{self.AGENT_NAME} v{self.VERSION} gestartet "
            f"(BACH={'ja' if BACH_AVAILABLE else 'nein'})"
        )

    # --- Config Loading ---

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Laedt Config: BACH DB -> lokale JSON -> Defaults."""
        # 1. BACH DB
        if self._bach.connected:
            cfg = self._bach.load_config()
            if cfg:
                return cfg

        # 2. Lokale JSON
        if config_path:
            path = Path(config_path)
        else:
            path = Path(__file__).parent / f"{self.AGENT_NAME.lower()}_config.json"

        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                self.logger.warning(f"Config-Fehler ({path}): {e}")

        # 3. Defaults aus Template
        return self.standalone_config_template()

    def save_config(self, path: Optional[str] = None):
        """Speichert aktuelle Config als JSON."""
        out = Path(path) if path else (
            Path(__file__).parent / f"{self.AGENT_NAME.lower()}_config.json"
        )
        with open(out, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Config gespeichert: {out}")

    # --- Abstract Interface ---

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """Hauptfunktion des Agenten."""

    @abstractmethod
    def status(self) -> Dict:
        """Gibt aktuellen Agent-Status zurueck."""

    @abstractmethod
    def config(self) -> Dict:
        """Gibt aktuelle Konfiguration zurueck."""

    @abstractmethod
    def standalone_config_template(self) -> Dict:
        """Gibt Standard-Config-Template fuer Standalone-Betrieb zurueck."""

    # --- Utility ---

    @property
    def bach_available(self) -> bool:
        return BACH_AVAILABLE

    @property
    def bach_root(self) -> Path:
        return BACH_ROOT

    @property
    def data_dir(self) -> Path:
        """Standard-Datenverzeichnis (BACH oder ~/.bach/)."""
        if BACH_AVAILABLE and (BACH_ROOT / "system" / "data").exists():
            return BACH_ROOT / "system" / "data"
        fallback = Path.home() / ".bach" / "data"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback
