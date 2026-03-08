# SPDX-License-Identifier: MIT
"""
schwarm - Schwarm-basierte LLM-Ausfuehrungsmuster
==================================================
Epstein-Methode, Konsensus, Hierarchie, Stigmergy, Spezialist.

Ref: BACH v3.8.0-SUGAR
"""

from .runner import ClaudeRunner
from .consensus import ConsensusPattern

__all__ = ["ClaudeRunner", "ConsensusPattern"]
