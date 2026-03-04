#!/usr/bin/env python3
"""
version_bump.py - BACH Release Version Bump Tool

Aktualisiert Versionsnummern und Codenamen in allen relevanten
BACH-Dateien fuer ein neues Release.

Standalone-Script ohne BACH-Imports.

Usage:
    python version_bump.py --version 3.6.0 --codename spaghetti
    python version_bump.py -v 3.6.0 -c spaghetti --dry-run
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional

# Farbige Ausgabe (optional)
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    C_GREEN = Fore.GREEN
    C_RED = Fore.RED
    C_YELLOW = Fore.YELLOW
    C_CYAN = Fore.CYAN
    C_BOLD = Style.BRIGHT
    C_RESET = Style.RESET_ALL
except ImportError:
    C_GREEN = C_RED = C_YELLOW = C_CYAN = C_BOLD = C_RESET = ""


# --- Konfiguration ---

# BACH_ROOT: Zwei Ebenen ueber diesem Script (system/tools/ -> BACH/)
SCRIPT_DIR = Path(__file__).resolve().parent
BACH_ROOT = SCRIPT_DIR.parent.parent

# Dateien relativ zu BACH_ROOT
TARGET_FILES = [
    "README.md",
    "QUICKSTART.md",
    "SKILL.md",
    "BACH_USER_MANUAL.md",
    "system/ARCHITECTURE.md",
    "system/docs/help/features.txt",
    "system/docs/help/cli.txt",
]


def detect_current_version() -> tuple[Optional[str], Optional[str]]:
    """Erkennt aktuelle Version und Codename aus README.md."""
    readme = BACH_ROOT / "README.md"
    if not readme.exists():
        return None, None

    content = readme.read_text(encoding="utf-8")

    # Suche nach dem Badge-Muster: Version-v3.5.0--milk-orange
    match = re.search(r"Version-v(\d+\.\d+\.\d+)--(\w+)-", content)
    if match:
        return match.group(1), match.group(2)

    # Fallback: **Version:** v3.5.0-milk
    match = re.search(r"\*\*Version:\*\*\s*v(\d+\.\d+\.\d+)-(\w+)", content)
    if match:
        return match.group(1), match.group(2)

    return None, None


def build_replacements(
    old_version: str,
    old_codename: str,
    new_version: str,
    new_codename: str,
) -> list[tuple[re.Pattern, str, str]]:
    """
    Erstellt eine Liste von (regex_pattern, replacement, beschreibung) Tupeln.

    Die Reihenfolge ist wichtig: Spezifischere Muster zuerst,
    damit nicht ein generisches Muster ein spezifischeres verhindert.
    """
    old_v = re.escape(old_version)
    old_c = re.escape(old_codename)

    replacements = []

    # 1. Badge-Format: Version-v3.5.0--milk-orange (doppelter Dash vor Codename)
    replacements.append((
        re.compile(rf"Version-v{old_v}--{old_c}"),
        f"Version-v{new_version}--{new_codename}",
        "Badge-Format (shields.io)",
    ))

    # 2. Version mit v-Prefix und Codename: v3.5.0-milk
    replacements.append((
        re.compile(rf"v{old_v}-{old_c}"),
        f"v{new_version}-{new_codename}",
        "Version mit v-Prefix und Codename",
    ))

    # 3. Version ohne v-Prefix mit Codename: 3.5.0-milk
    #    (aber nicht nach einem 'v', das wird von #2 abgedeckt)
    replacements.append((
        re.compile(rf"(?<!v){old_v}-{old_c}"),
        f"{new_version}-{new_codename}",
        "Version ohne v-Prefix mit Codename",
    ))

    # 4. YAML version-Feld: version: 3.5.0
    #    Nur in YAML-Header-Kontext (nach "version:")
    replacements.append((
        re.compile(rf"(version:\s*){old_v}"),
        rf"\g<1>{new_version}",
        "YAML version-Feld",
    ))

    # 5. Kommentar-Header: # Version: 3.5.0
    replacements.append((
        re.compile(rf"(#\s*Version:\s*){old_v}"),
        rf"\g<1>{new_version}",
        "Kommentar-Header Version",
    ))

    return replacements


def process_file(
    filepath: Path,
    replacements: list[tuple[re.Pattern, str, str]],
    dry_run: bool = False,
) -> list[dict]:
    """
    Verarbeitet eine einzelne Datei und fuehrt Ersetzungen durch.

    Returns:
        Liste von Aenderungs-Dicts mit Zeilennummer, alt, neu, Beschreibung.
    """
    if not filepath.exists():
        return []

    content = filepath.read_text(encoding="utf-8")
    changes = []
    new_content = content

    for pattern, replacement, description in replacements:
        # Finde alle Matches mit Zeilennummern
        for match in pattern.finditer(new_content):
            line_num = new_content[:match.start()].count("\n") + 1
            changes.append({
                "line": line_num,
                "old": match.group(0),
                "new": pattern.sub(replacement, match.group(0)),
                "description": description,
            })

        # Ersetze im Gesamttext
        new_content = pattern.sub(replacement, new_content)

    if changes and not dry_run:
        filepath.write_text(new_content, encoding="utf-8")

    return changes


def print_file_header(rel_path: str, found: bool) -> None:
    """Gibt den Datei-Header aus."""
    if found:
        print(f"\n{C_CYAN}{C_BOLD}{rel_path}{C_RESET}")
    else:
        print(f"\n{C_YELLOW}{rel_path} -- keine Aenderungen{C_RESET}")


def print_change(change: dict) -> None:
    """Gibt eine einzelne Aenderung aus."""
    print(f"  Zeile {change['line']:>4}: {C_RED}{change['old']}{C_RESET}")
    print(f"           {C_GREEN}{change['new']}{C_RESET}")
    print(f"           ({change['description']})")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="BACH Version Bump -- Aktualisiert Versionsnummern in allen Release-Dateien.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Beispiele:\n"
            "  python version_bump.py -v 3.6.0 -c spaghetti\n"
            "  python version_bump.py -v 3.6.0 -c spaghetti --dry-run\n"
        ),
    )
    parser.add_argument(
        "-v", "--version",
        required=True,
        help="Neue Versionsnummer (z.B. 3.6.0)",
    )
    parser.add_argument(
        "-c", "--codename",
        required=True,
        help="Neuer Codename (z.B. spaghetti)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Nur anzeigen was geaendert wuerde, ohne zu schreiben",
    )

    args = parser.parse_args()

    # Validierung
    if not re.match(r"^\d+\.\d+\.\d+$", args.version):
        print(f"{C_RED}Fehler: Version muss im Format X.Y.Z sein (z.B. 3.6.0){C_RESET}")
        return 1

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", args.codename):
        print(f"{C_RED}Fehler: Codename darf nur Buchstaben, Zahlen, - und _ enthalten{C_RESET}")
        return 1

    new_version = args.version
    new_codename = args.codename.lower()

    # Aktuelle Version erkennen
    old_version, old_codename = detect_current_version()
    if not old_version or not old_codename:
        print(f"{C_RED}Fehler: Aktuelle Version konnte nicht aus README.md erkannt werden.{C_RESET}")
        print(f"Erwartet: Badge-Muster 'Version-vX.Y.Z--codename-' in README.md")
        return 1

    # Header
    mode_label = f"{C_YELLOW}DRY RUN{C_RESET}" if args.dry_run else f"{C_GREEN}LIVE{C_RESET}"
    print(f"\n{'=' * 60}")
    print(f"  BACH Version Bump [{mode_label}]")
    print(f"{'=' * 60}")
    print(f"  {old_version}-{old_codename}  -->  {C_BOLD}{new_version}-{new_codename}{C_RESET}")
    print(f"  BACH Root: {BACH_ROOT}")
    print(f"{'=' * 60}")

    if old_version == new_version and old_codename == new_codename:
        print(f"\n{C_YELLOW}Keine Aenderungen -- alte und neue Version sind identisch.{C_RESET}")
        return 0

    # Ersetzungsregeln erstellen
    replacements = build_replacements(old_version, old_codename, new_version, new_codename)

    # Dateien verarbeiten
    total_changes = 0
    files_changed = 0
    files_skipped = 0

    for rel_path in TARGET_FILES:
        filepath = BACH_ROOT / rel_path

        if not filepath.exists():
            print(f"\n{C_YELLOW}{rel_path} -- Datei nicht gefunden, uebersprungen{C_RESET}")
            files_skipped += 1
            continue

        changes = process_file(filepath, replacements, dry_run=args.dry_run)

        if changes:
            print_file_header(rel_path, found=True)
            for change in changes:
                print_change(change)
            total_changes += len(changes)
            files_changed += 1
        else:
            print_file_header(rel_path, found=False)

    # Zusammenfassung
    print(f"\n{'=' * 60}")
    print(f"  Zusammenfassung")
    print(f"{'=' * 60}")
    print(f"  Dateien geaendert:    {C_GREEN}{files_changed}{C_RESET}")
    print(f"  Ersetzungen gesamt:   {C_GREEN}{total_changes}{C_RESET}")
    if files_skipped:
        print(f"  Dateien uebersprungen: {C_YELLOW}{files_skipped}{C_RESET}")

    if args.dry_run:
        print(f"\n  {C_YELLOW}DRY RUN -- es wurden keine Dateien veraendert.{C_RESET}")
        print(f"  Fuehre ohne --dry-run aus um die Aenderungen zu schreiben.")
    else:
        print(f"\n  {C_GREEN}Alle Aenderungen wurden geschrieben.{C_RESET}")

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
