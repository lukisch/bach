# SPDX-License-Identifier: MIT
"""
Boot Integration für Tool Registry
===================================

Wird beim RecludOS Boot-Prozess aufgerufen.
Lädt alle Tool-Registries in den globalen Context.

Version: 1.0.0
"""

import sys
from pathlib import Path

# Add boot-skills to path
boot_skills_path = Path(__file__).parent
if str(boot_skills_path) not in sys.path:
    sys.path.insert(0, str(boot_skills_path))

from tool_registry import ToolRegistry


# Global Registry Instance
TOOL_REGISTRY = None


def initialize_tool_registry(silent=False):
    """
    Initialisiert globale ToolRegistry beim Boot.
    
    Args:
        silent: Wenn True, keine Print-Ausgaben
    
    Returns:
        ToolRegistry Instance
    """
    global TOOL_REGISTRY
    
    if not silent:
        print("\n[BOOT] Initializing Tool Registry...")
    
    TOOL_REGISTRY = ToolRegistry()
    
    if not silent:
        print(f"[BOOT] ✅ Tool Registry ready: {TOOL_REGISTRY.stats['total_tools']} tools")
    
    return TOOL_REGISTRY


def get_registry():
    """
    Holt globale Registry Instance.
    
    Returns:
        ToolRegistry oder None wenn nicht initialisiert
    """
    return TOOL_REGISTRY


# Auto-Initialize beim Import
if __name__ != "__main__":
    # Beim Import: Automatisch initialisieren
    initialize_tool_registry(silent=True)
