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
Tool: [tool_name]
Version: 1.0.0
Author: [author]
Created: [YYYY-MM-DD]
Updated: [YYYY-MM-DD]
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version [tool_name]
Verwende immer die höchste Versionsnummer.

Description:
    [Was macht dieses Tool?]

Usage:
    python [tool_name].py [args]
    bach [tool_name] [args]

Arguments:
    [arg1]      [Beschreibung]
    [arg2]      [Beschreibung]
    --option    [Beschreibung]

Examples:
    python [tool_name].py input.txt
    python [tool_name].py input.txt --option value

Dependencies:
    - [module1]
    - [module2]

Exit Codes:
    0 - Erfolg
    1 - Fehler
"""

__version__ = "1.0.0"
__author__ = "[author]"

import argparse
import sys
from pathlib import Path


def main():
    """Hauptfunktion."""
    parser = argparse.ArgumentParser(
        description="[Tool-Beschreibung]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python %(prog)s input.txt
  python %(prog)s input.txt --option value
        """
    )

    parser.add_argument(
        "input",
        help="[Input-Beschreibung]"
    )

    parser.add_argument(
        "--option",
        default="default_value",
        help="[Option-Beschreibung] (default: %(default)s)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    # Tool-Logik hier
    try:
        # [Implementierung]
        print(f"[OK] Tool erfolgreich ausgeführt")
        return 0
    except Exception as e:
        print(f"[FEHLER] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
