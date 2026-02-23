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
Tool: c_header_migrate
Version: 1.0.0
Author: BACH Team
Created: 2026-02-08
Updated: 2026-02-08
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version c_header_migrate

Description:
    Migriert fehlende Standard-Header in Help- und Tool-Dateien.
    Prueft alle docs/docs/docs/help/*.txt und tools/*.py auf Standard-Header
    und fuegt fehlende Header hinzu.

Usage:
    python tools/c_header_migrate.py [--dry-run] [--verbose]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

SYSTEM_DIR = Path(__file__).parent.parent

# Standard Help-File Header
HELP_HEADER_TEMPLATE = """# Portabilitaet: UNIVERSAL
# Version: 1.0.0
# Zuletzt validiert: {date} (Migration)
# Naechste Pruefung: {next_date}

"""

# Standard Tool-File Header (inserted into existing docstring)
TOOL_HEADER_TEMPLATE = '''Tool: {name}
Version: 1.0.0
Author: BACH Team
Created: {date}
Updated: {date}
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version {name}

'''


def has_help_header(content: str) -> bool:
    """Prueft ob Help-Datei den Standard-Header hat."""
    return content.strip().startswith("# Portabilitaet:")


def has_tool_header(content: str) -> bool:
    """Prueft ob Tool-Datei den Standard-Header hat."""
    return "Tool:" in content[:500] and "Version:" in content[:500]


def add_help_header(filepath: Path, dry_run: bool = False) -> bool:
    """Fuegt Standard-Header zu Help-Datei hinzu."""
    content = filepath.read_text(encoding="utf-8")
    if has_help_header(content):
        return False

    now = datetime.now()
    header = HELP_HEADER_TEMPLATE.format(
        date=now.strftime("%Y-%m-%d"),
        next_date=(now + timedelta(days=180)).strftime("%Y-%m-%d")
    )

    if dry_run:
        print(f"  [DRY] {filepath.name}: Wuerde Header hinzufuegen")
        return True

    filepath.write_text(header + content, encoding="utf-8")
    print(f"  [OK] {filepath.name}: Header hinzugefuegt")
    return True


def add_tool_header(filepath: Path, dry_run: bool = False) -> bool:
    """Fuegt Standard-Header zu Tool-Datei hinzu."""
    content = filepath.read_text(encoding="utf-8")
    if has_tool_header(content):
        return False

    name = filepath.stem
    now = datetime.now().strftime("%Y-%m-%d")
    header_block = TOOL_HEADER_TEMPLATE.format(name=name, date=now)

    # Suche existierendes Docstring-Pattern und fuege Header ein
    # Pattern: """ oder ''' am Anfang (nach shebang/encoding)
    patterns = [
        (r'(""")\n', '"""\n' + header_block),
        (r"(''')\n", "'''\n" + header_block),
    ]

    modified = False
    for pattern, replacement in patterns:
        match = re.search(pattern, content[:300])
        if match:
            pos = match.end()
            new_content = content[:pos] + header_block + content[pos:]
            content = new_content
            modified = True
            break

    if not modified:
        # Kein Docstring gefunden - Header als Kommentar einfuegen
        lines = content.split("\n")
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.startswith("#!") or line.startswith("# -*-"):
                insert_pos = i + 1
            else:
                break

        header_comment = f'"""\n{header_block}"""\n\n'
        lines.insert(insert_pos, header_comment)
        content = "\n".join(lines)

    if dry_run:
        print(f"  [DRY] {filepath.name}: Wuerde Header hinzufuegen")
        return True

    filepath.write_text(content, encoding="utf-8")
    print(f"  [OK] {filepath.name}: Header hinzugefuegt")
    return True


def migrate(dry_run: bool = False, verbose: bool = False):
    """Hauptfunktion: Alle Dateien pruefen und migrieren."""
    help_dir = SYSTEM_DIR / "help"
    tools_dir = SYSTEM_DIR / "tools"

    print("BACH Header Migration")
    print("=" * 50)
    print(f"  Modus: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    # Help-Dateien
    help_files = sorted(help_dir.glob("*.txt"))
    help_missing = 0
    help_migrated = 0

    print(f"Help-Dateien ({len(help_files)} gesamt):")
    for f in help_files:
        content = f.read_text(encoding="utf-8")
        if not has_help_header(content):
            help_missing += 1
            if add_help_header(f, dry_run):
                help_migrated += 1
        elif verbose:
            print(f"  [OK] {f.name}: Header vorhanden")

    if help_missing == 0:
        print("  Alle Help-Dateien haben Header.")
    print()

    # Tool-Dateien
    tool_files = sorted(tools_dir.glob("*.py"))
    tool_missing = 0
    tool_migrated = 0

    print(f"Tool-Dateien ({len(tool_files)} gesamt):")
    for f in tool_files:
        if f.name == "__init__.py" or f.name == "__pycache__":
            continue
        content = f.read_text(encoding="utf-8")
        if not has_tool_header(content):
            tool_missing += 1
            if add_tool_header(f, dry_run):
                tool_migrated += 1
        elif verbose:
            print(f"  [OK] {f.name}: Header vorhanden")

    if tool_missing == 0:
        print("  Alle Tool-Dateien haben Header.")

    # Zusammenfassung
    print()
    print("Zusammenfassung:")
    print(f"  Help: {help_migrated}/{help_missing} migriert (von {len(help_files)} gesamt)")
    print(f"  Tools: {tool_migrated}/{tool_missing} migriert (von {len(tool_files)} gesamt)")
    total = help_migrated + tool_migrated
    print(f"  Gesamt: {total} Dateien aktualisiert")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv
    migrate(dry_run=dry_run, verbose=verbose)
