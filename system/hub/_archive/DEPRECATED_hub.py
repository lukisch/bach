# SPDX-License-Identifier: MIT
"""
hub.py - DEPRECATED
====================

ACHTUNG: Diese Datei ist DEPRECATED!

hub.py (CHIAH) wurde vollstaendig in bach.py integriert.
Alle Funktionen sind ueber bach.py verfuegbar.

Statt:  python hub/hub.py --startup
Nutze:  python bach.py --startup

Diese Datei leitet alle Aufrufe an bach.py weiter und wird
in einer zukuenftigen Version entfernt.

Migration: Ersetze alle Aufrufe von hub.py/chiah.py durch bach.py
Siehe:     docs/docs/docs/help/hub.txt fuer Details

Version: 3.1.0 (DEPRECATED)
Deprecated seit: 2026-01-23
"""

import sys
import os
import subprocess
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# DEPRECATION WARNING
# ═══════════════════════════════════════════════════════════════

def show_deprecation_warning():
    """Zeigt Deprecation-Warnung an."""
    warning = """
╔═══════════════════════════════════════════════════════════════╗
║  ⚠️  DEPRECATED: hub.py / chiah.py                            ║
╠═══════════════════════════════════════════════════════════════╣
║  hub.py wurde in bach.py integriert.                          ║
║                                                               ║
║  Bitte nutze stattdessen:                                     ║
║    python bach.py [befehl]                                    ║
║                                                               ║
║  Dieser Wrapper wird in einer zukuenftigen Version entfernt.  ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(warning, file=sys.stderr)


# ═══════════════════════════════════════════════════════════════
# REDIRECT TO BACH.PY
# ═══════════════════════════════════════════════════════════════

def main():
    """Leitet alle Aufrufe an bach.py weiter."""
    # Deprecation-Warnung anzeigen
    show_deprecation_warning()
    
    # Pfad zu bach.py
    bach_dir = Path(__file__).parent.parent
    bach_py = bach_dir / "bach.py"
    
    if not bach_py.exists():
        print(f"[ERROR] bach.py nicht gefunden: {bach_py}", file=sys.stderr)
        return 1
    
    # Alle Argumente an bach.py weiterleiten
    args = sys.argv[1:]
    
    # Aufruf konstruieren
    cmd = [sys.executable, str(bach_py)] + args
    
    # Ausfuehren und Exit-Code uebernehmen
    try:
        result = subprocess.run(cmd, cwd=str(bach_dir))
        return result.returncode
    except KeyboardInterrupt:
        return 130
    except Exception as e:
        print(f"[ERROR] Weiterleitung fehlgeschlagen: {e}", file=sys.stderr)
        return 1


# ═══════════════════════════════════════════════════════════════
# LEGACY EXPORTS (fuer Imports aus anderen Modulen)
# ═══════════════════════════════════════════════════════════════

# Diese werden noch von einigen Modulen importiert
# und muessen vorerst erhalten bleiben

BACH_DIR = Path(__file__).parent.parent
TOOLS_DIR = BACH_DIR / "tools"

def get_handler(profile_name: str):
    """DEPRECATED: Importiere direkt aus bach.py oder hub.handlers."""
    import warnings
    warnings.warn(
        "hub.get_handler() ist deprecated. "
        "Nutze den Import aus bach.py oder hub.handlers direkt.",
        DeprecationWarning,
        stacklevel=2
    )
    
    # Fallback zur alten Implementierung
    from .handlers.base import BaseHandler
    
    handlers = {
        "help": lambda: _import_handler("help", "HelpHandler"),
        "memory": lambda: _import_handler("memory", "MemoryHandler"),
        "startup": lambda: _import_handler("startup", "StartupHandler"),
        "shutdown": lambda: _import_handler("shutdown", "ShutdownHandler"),
        "status": lambda: _import_handler("status", "StatusHandler"),
        "context": lambda: _import_handler("context", "ContextHandler"),
        "inject": lambda: _import_handler("inject", "InjectHandler"),
        "sources": lambda: _import_handler("sources", "SourcesHandler"),
        "test": lambda: _import_handler("test", "TestHandler"),
        "maintain": lambda: _import_handler("maintain", "MaintainHandler"),
        "data": lambda: _import_handler("data_analysis", "DataAnalysisHandler"),
        "recurring": lambda: _import_handler("recurring", "RecurringHandler"),
    }
    
    if profile_name in handlers:
        return handlers[profile_name]()
    return None


def _import_handler(module_name: str, class_name: str):
    """Importiert Handler dynamisch."""
    import importlib
    module = importlib.import_module(f".handlers.{module_name}", package="hub")
    handler_class = getattr(module, class_name)
    return handler_class(BACH_DIR)


if __name__ == "__main__":
    sys.exit(main())
