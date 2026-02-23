# SPDX-License-Identifier: MIT
"""
base.py - Basis-Handler-Klasse
==============================
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple, List


class BaseHandler(ABC):
    """Basisklasse fuer alle CHIAH Handler."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
    
    @property
    @abstractmethod
    def profile_name(self) -> str:
        """Name des Profils."""
        pass
    
    @property
    @abstractmethod
    def target_file(self) -> Path:
        """Hauptdatei/Ordner des Handlers."""
        pass
    
    @abstractmethod
    def get_operations(self) -> dict:
        """Verfuegbare Operationen mit Beschreibung."""
        pass
    
    @abstractmethod
    def handle(self, operation: str, args: List[str], dry_run: bool = False) -> Tuple[bool, str]:
        """
        Fuehrt Operation aus.
        
        Returns:
            (success, message)
        """
        pass
