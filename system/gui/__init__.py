# SPDX-License-Identifier: MIT
"""
BACH GUI Module
===============
Web-Dashboard fuer BACH v1.1
"""

from pathlib import Path

GUI_DIR = Path(__file__).parent
TEMPLATES_DIR = GUI_DIR / "templates"
STATIC_DIR = GUI_DIR / "static"

__all__ = ['GUI_DIR', 'TEMPLATES_DIR', 'STATIC_DIR']
