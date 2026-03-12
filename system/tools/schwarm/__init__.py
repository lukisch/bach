# SPDX-License-Identifier: MIT
"""
schwarm - Schwarm-basierte LLM-Ausfuehrungsmuster
==================================================
Epstein-Methode, Konsensus, Hierarchie, Stigmergy, Spezialist.

Ref: BACH v3.8.0-SUGAR
"""

from .runner import ClaudeRunner, calculate_dynamic_workers
from .consensus import ConsensusPattern
from .hierarchy import HierarchyPattern
from .stigmergy_pattern import StigmergyPattern
from .specialist import SpecialistPattern

__all__ = [
    "ClaudeRunner",
    "calculate_dynamic_workers",
    "ConsensusPattern",
    "HierarchyPattern",
    "StigmergyPattern",
    "SpecialistPattern",
]
