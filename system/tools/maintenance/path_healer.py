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
Tool: c_path_healer
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version c_path_healer

Description:
    [Beschreibung hinzufügen]

Usage:
    python c_path_healer.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

# -*- coding: utf-8 -*-
"""
BACH Path Healer v2.0.0
Zentraler Pfad-Heilungs-Service fuer BACH

Nutzt bach_paths.py fuer Base-Pfad (kein hardcoded Pfad mehr!)

Usage:
    python c_path_healer.py                    # Vollstaendiger Scan
    python c_path_healer.py --dry-run          # Nur pruefen
    python c_path_healer.py --target <pfad>    # Einzelne Datei
    python c_path_healer.py --report           # Report generieren

CLI:
    bach maintain heal                       # Vollstaendiger Scan
    bach maintain heal --dry-run             # Nur pruefen
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

# ============================================================================
# BACH-SPEZIFISCHE PFAD-KORREKTUREN v2.0.0
# ============================================================================
# Format: (alter_string, neuer_string)
# Reihenfolge wichtig: Spezifischere zuerst!
# Hinweis: Backslashes muessen als \\\\ oder r-strings escaped werden

PATH_CORRECTIONS: List[Tuple[str, str]] = [
    # === Struktur-Cleanup v2.7 (2026-02-14) ===
    # Config-Move + Backups-Move + Exports-Move

    # Config → data/config (Forward-Slash)
    ("system/config/", "system/data/config/"),
    ("config/db_sync_enabled", "data/config/db_sync_enabled"),

    # Config → data/config (Backslash)
    ("system\\config\\", "system\\data\\config\\"),
    ("config\\db_sync_enabled", "data\\config\\db_sync_enabled"),

    # Backups → data/backups (Forward-Slash)
    ("backups/", "system/data/backups/"),
    ("/backups/", "/system/data/backups/"),

    # Backups → data/backups (Backslash)
    ("backups\\", "system\\data\\backups\\"),
    ("\\backups\\", "\\system\\data\\backups\\"),

    # Exports → system/exports (Forward-Slash)
    ("exports/", "system/exports/"),
    ("/exports/", "/system/exports/"),

    # Exports → system/exports (Backslash)
    ("exports\\", "system\\exports\\"),
    ("\\exports\\", "\\system\\exports\\"),

    # === Docs-Refactoring v2.6 (2026-02-14) ===
    # WICHTIG: Spezifischere Patterns ZUERST!

    # Help-Pfade (Forward-Slash)
    ("system/help/wiki/", "system/wiki/"),          # Wichtig: ZUERST
    ("help/wiki/", "wiki/"),
    ("system/help/", "system/docs/help/"),
    ("help/", "docs/help/"),

    # Help-Pfade (Backslash - Windows)
    ("system\\help\\wiki\\", "system\\wiki\\"),      # Wichtig: ZUERST
    ("help\\wiki\\", "wiki\\"),
    ("system\\help\\", "system\\docs\\help\\"),
    ("help\\", "docs\\help\\"),

    # Python-Imports (falls relevant)
    ("from help.", "from docs.help."),

    # === Directory Restructuring v2.5 (2026-02-13) ===

    # Python-Imports (Punkt-Notation)
    ("skills._connectors.", "connectors."),
    ("skills._agents.ati.", "agents.ati."),
    ("skills._agents.reflection", "agents.reflection"),
    ("skills._agents.", "agents."),

    # Pfad-Strings (Forward-Slash) - spezifischere zuerst
    ("skills/_connectors/", "connectors/"),
    ("skills/_agents/ati/", "agents/ati/"),
    ("skills/_agents/", "agents/"),
    ("skills/_experts/", "agents/_experts/"),
    ("skills/_workflows/", "skills/workflows/"),
    ("skills/_partners/", "partners/"),

    # Pfad-Strings (Backslash - Windows)
    ("skills\\_connectors\\", "connectors\\"),
    ("skills\\_agents\\ati\\", "agents\\ati\\"),
    ("skills\\_agents\\", "agents\\"),
    ("skills\\_experts\\", "agents\\_experts\\"),
    ("skills\\_workflows\\", "skills\\workflows\\"),
    ("skills\\_partners\\", "partners\\"),

    # _partners auf Root-Level (ohne skills/ Prefix)
    ("_partners/", "partners/"),
    ("_partners\\", "partners\\"),

    # === Bestehende Korrekturen (Legacy) ===
]

# Erweiterbare Liste - kann durch DB geladen werden
HEALABLE_EXTENSIONS = {'.json', '.md', '.py', '.txt', '.ps1', '.bat', '.sh', '.yaml', '.yml'}
IGNORE_DIRS = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', 'dist', 'build', '.claude'}


def _get_bach_root() -> Path:
    """
    Ermittelt BACH_ROOT dynamisch.

    Versucht bach_paths.py zu importieren, sonst berechnet relativ.
    """
    # Methode 1: bach_paths importieren
    try:
        # Diese Datei liegt in: system/tools/c_path_healer.py
        # BACH_ROOT ist: tools -> system -> BACH_ROOT
        current_dir = Path(__file__).resolve().parent
        system_dir = current_dir.parent  # tools -> system
        hub_dir = system_dir / "hub"

        if str(hub_dir) not in sys.path:
            sys.path.insert(0, str(hub_dir))

        from bach_paths import BACH_ROOT
        return BACH_ROOT
    except ImportError:
        pass

    # Methode 2: Relativ berechnen
    current_dir = Path(__file__).resolve().parent
    # tools -> system -> BACH_ROOT
    return current_dir.parent.parent


class BachPathHealer:
    """BACH Pfad-Heilungs-Service v2.0.0"""

    def __init__(self, base_path: str = None):
        if base_path is None:
            self.base_path = _get_bach_root()
        else:
            self.base_path = Path(base_path)

        self.healed_files: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.scan_count = 0
        self.start_time = None
        self.safety_backup_path = None

    def _create_safety_backup(self) -> bool:
        """Erstellt Safety-Backup des system-Ordners vor Heilung"""
        try:
            import shutil

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = self.base_path / "system" / "data" / "backups" / "safety"
            backup_dir.mkdir(parents=True, exist_ok=True)

            self.safety_backup_path = backup_dir / f"system_backup_{timestamp}"

            # Kopiere system-Ordner (ohne backups selbst - Rekursion vermeiden)
            system_src = self.base_path / "system"
            shutil.copytree(
                system_src,
                self.safety_backup_path,
                ignore=shutil.ignore_patterns('data/backups/*', '__pycache__', '*.pyc'),
                dirs_exist_ok=False
            )

            print(f"[SAFETY] Backup erstellt: {self.safety_backup_path.name}")
            return True

        except Exception as e:
            print(f"[WARN] Safety-Backup fehlgeschlagen: {e}")
            return False

    def heal_all(self, dry_run: bool = False, skip_backup: bool = False) -> Dict[str, Any]:
        """Heilt alle Dateien im BACH-System"""
        self.start_time = datetime.now()

        # Safety-Backup erstellen (nur wenn nicht Dry-Run)
        if not dry_run and not skip_backup:
            self._create_safety_backup()

        # BACH-spezifische kritische Verzeichnisse (innerhalb system/)
        system_dir = self.base_path / "system"
        critical_dirs = [
            system_dir / "hub",
            system_dir / "tools",
            system_dir / "skills",
            system_dir / "data",          # Enthält nun config/ und backups/ - v2.7
            system_dir / "gui",
            system_dir / "docs",          # Haupt-Dokumentation (inkl. help/) - v2.6
            system_dir / "wiki",          # Wiki (Top-Level) - v2.6
            system_dir / "agents",        # NEU v2.5
            system_dir / "connectors",    # NEU v2.5
            system_dir / "partners",      # NEU v2.5
            system_dir / "core",
            system_dir / "exports",       # Verschoben von Root - v2.7
            self.base_path / "docs",      # Projekt-Root-Docs
            self.base_path / "user",
        ]

        # Auch Root-Level Dateien in system/ scannen (.md, .txt)
        for root_file in system_dir.iterdir():
            if root_file.is_file() and root_file.suffix.lower() in HEALABLE_EXTENSIONS:
                self.scan_count += 1
                self.heal_file(root_file, dry_run)

        for target_dir in critical_dirs:
            if target_dir.exists():
                self._scan_directory(target_dir, dry_run)

        return self._generate_report()

    def heal_file(self, filepath: Path, dry_run: bool = False) -> Dict[str, Any]:
        """Heilt eine einzelne Datei"""
        result = {
            "file": str(filepath),
            "changes": [],
            "error": None,
            "healed": False
        }

        if filepath.suffix.lower() not in HEALABLE_EXTENSIONS:
            return result

        # Eigene Datei nicht heilen (wuerde PATH_CORRECTIONS zu No-Ops machen)
        if filepath.resolve() == Path(__file__).resolve():
            return result

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original = content

            for old_str, new_str in PATH_CORRECTIONS:
                if old_str in content and old_str != new_str:
                    count = content.count(old_str)
                    content = content.replace(old_str, new_str)
                    result["changes"].append({
                        "old": old_str,
                        "new": new_str,
                        "count": count
                    })

            if content != original:
                result["healed"] = True
                if not dry_run:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                self.healed_files.append(result)

        except UnicodeDecodeError:
            # Binaerdateien ueberspringen
            pass
        except Exception as e:
            result["error"] = str(e)
            self.errors.append(result)

        return result

    def _scan_directory(self, directory: Path, dry_run: bool):
        """Scannt Verzeichnis rekursiv"""
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                filepath = Path(root) / file
                self.scan_count += 1
                self.heal_file(filepath, dry_run)

    def _generate_report(self) -> Dict[str, Any]:
        """Generiert Heilungs-Report"""
        duration = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0

        report = {
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "system": "BACH",
            "base_path": str(self.base_path),
            "duration_seconds": duration,
            "files_scanned": self.scan_count,
            "files_healed": len(self.healed_files),
            "errors": len(self.errors),
            "healed_files": self.healed_files,
            "error_files": self.errors,
        }

        if self.safety_backup_path:
            report["safety_backup"] = str(self.safety_backup_path)

        return report

    def cleanup_safety_backup(self) -> bool:
        """Loescht Safety-Backup nach erfolgreicher Heilung"""
        if not self.safety_backup_path or not self.safety_backup_path.exists():
            return False

        try:
            import shutil
            shutil.rmtree(self.safety_backup_path)
            print(f"[CLEANUP] Safety-Backup geloescht: {self.safety_backup_path.name}")
            return True
        except Exception as e:
            print(f"[WARN] Safety-Backup-Cleanup fehlgeschlagen: {e}")
            return False

    def save_report(self, output_path: Path = None) -> Path:
        """Speichert Report als JSON"""
        if output_path is None:
            output_path = self.base_path / "system" / "data" / "healing_report.json"

        report = self._generate_report()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return output_path


def main():
    """CLI Entry Point"""
    import argparse

    parser = argparse.ArgumentParser(description="BACH Path Healer v2.0.0")
    parser.add_argument("--dry-run", action="store_true", help="Nur pruefen, keine Aenderungen")
    parser.add_argument("--target", type=str, help="Einzelne Datei heilen")
    parser.add_argument("--report", action="store_true", help="Report als JSON speichern")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    parser.add_argument("--base", type=str, help="Alternatives Base-Verzeichnis")
    parser.add_argument("--skip-backup", action="store_true", help="Safety-Backup ueberspringen")
    parser.add_argument("--cleanup", action="store_true", help="Safety-Backup nach Erfolg loeschen")

    args = parser.parse_args()

    healer = BachPathHealer(args.base)

    print("=" * 60)
    print("BACH PATH HEALER v2.0.0")
    print("=" * 60)
    print(f"[BASE] {healer.base_path}")

    if args.dry_run:
        print("[MODE] DRY RUN - Keine Aenderungen")

    if args.target:
        result = healer.heal_file(Path(args.target), args.dry_run)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["healed"]:
                print(f"[OK] Geheilt: {result['file']}")
                for change in result["changes"]:
                    print(f"     '{change['old']}' -> '{change['new']}' ({change['count']}x)")
            else:
                print(f"[INFO] Keine Aenderungen: {result['file']}")
    else:
        report = healer.heal_all(args.dry_run, args.skip_backup)

        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"\n[ERGEBNIS]")
            print(f"   Gescannt:  {report['files_scanned']} Dateien")
            print(f"   Geheilt:   {report['files_healed']} Dateien")
            print(f"   Fehler:    {report['errors']}")
            print(f"   Dauer:     {report['duration_seconds']:.2f}s")

            if 'safety_backup' in report:
                print(f"   Backup:    {Path(report['safety_backup']).name}")

            if report['healed_files']:
                print(f"\n[OK] GEHEILTE DATEIEN:")
                for f in report['healed_files'][:10]:
                    print(f"   - {Path(f['file']).name}")
                if len(report['healed_files']) > 10:
                    print(f"   ... und {len(report['healed_files']) - 10} weitere")

            # Cleanup Safety-Backup wenn gewuenscht und erfolgreich
            if args.cleanup and report['files_healed'] > 0 and report['errors'] == 0:
                print(f"\n[INFO] Heilung erfolgreich - loesche Safety-Backup...")
                healer.cleanup_safety_backup()

        if args.report:
            path = healer.save_report()
            print(f"\n[OK] Report gespeichert: {path}")

    print("\n" + "=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
