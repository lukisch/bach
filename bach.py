#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
BACH CLI Wrapper - Root-Level Entry Point
==========================================

Dieses Script liegt im BACH-Root und ruft system/bach.py auf.

Usage:
    python bach.py <command> [args]
    ./bach.py --startup

Referenz: SQ013, SQ015 (Build-Fix)
Datum: 2026-02-20
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    """Wrapper-Einstiegspunkt für BACH CLI."""
    # BACH Root (wo dieses Script liegt)
    bach_root = Path(__file__).parent
    system_bach = bach_root / "system" / "bach.py"

    # Verifizieren dass system/bach.py existiert
    if not system_bach.exists():
        print(f"ERROR: system/bach.py nicht gefunden in {bach_root}", file=sys.stderr)
        print(f"       Erwartet: {system_bach}", file=sys.stderr)
        sys.exit(1)

    # UTF-8 Encoding setzen (Windows)
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

    # system/bach.py mit allen Argumenten aufrufen
    # CWD muss system/ sein, damit relative Pfade (data/bach.db) funktionieren
    result = subprocess.run(
        [sys.executable, str(system_bach)] + sys.argv[1:],
        cwd=str(bach_root / "system")
    )

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
