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
ATI Export System - Packt ATI-Agent in exportierbares ZIP

Usage:
    python ati_exporter.py                    # Export mit Standardeinstellungen
    python ati_exporter.py --output dist/     # Export in bestimmten Ordner
    python ati_exporter.py --dry-run          # Nur anzeigen, was exportiert wuerde
    python ati_exporter.py --verbose          # Detaillierte Ausgabe

Liest manifest.json und erstellt ein ZIP mit allen gelisteten Dateien.
"""

import json
import zipfile
import glob
import os
import sys
from pathlib import Path
from datetime import datetime
import argparse

# BACH-Root ermitteln (4 Ebenen hoch von diesem Skript)
SCRIPT_DIR = Path(__file__).parent
ATI_DIR = SCRIPT_DIR.parent
AGENTS_DIR = ATI_DIR.parent
SKILLS_DIR = AGENTS_DIR.parent
BACH_ROOT = SKILLS_DIR.parent

MANIFEST_PATH = SCRIPT_DIR / "manifest.json"


def load_manifest() -> dict:
    """Laedt manifest.json"""
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest nicht gefunden: {MANIFEST_PATH}")
    
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def resolve_patterns(patterns: list, base_path: Path) -> list:
    """Loest Glob-Patterns auf und gibt absolute Pfade zurueck"""
    resolved = []
    for pattern in patterns:
        # Pattern relativ zu BACH_ROOT
        full_pattern = base_path / pattern
        
        # Glob ausfuehren
        matches = glob.glob(str(full_pattern), recursive=True)
        
        if matches:
            resolved.extend(matches)
        else:
            # Warnung bei nicht gefundenen Patterns
            print(f"  [WARN] Keine Treffer fuer: {pattern}")
    
    return resolved


def collect_files(manifest: dict, verbose: bool = False) -> dict:
    """Sammelt alle zu exportierenden Dateien basierend auf manifest"""
    includes = manifest.get("includes", {})
    all_files = {}
    
    categories = ["core", "services", "tools", "data", "docs"]
    
    for category in categories:
        patterns = includes.get(category, [])
        if not patterns:
            continue
            
        if verbose:
            print(f"\n[{category.upper()}]")
        
        files = resolve_patterns(patterns, BACH_ROOT)
        
        for filepath in files:
            # Relativen Pfad fuer ZIP berechnen
            rel_path = os.path.relpath(filepath, BACH_ROOT)
            
            # Nur Dateien, keine Verzeichnisse
            if os.path.isfile(filepath):
                all_files[rel_path] = filepath
                if verbose:
                    print(f"  + {rel_path}")
    
    return all_files


def create_export_zip(files: dict, manifest: dict, output_dir: Path) -> Path:
    """Erstellt das Export-ZIP"""
    name = manifest.get("name", "export")
    version = manifest.get("version", "0.0.0")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    zip_name = f"bach-{name}-v{version}-{timestamp}.zip"
    zip_path = output_dir / zip_name
    
    # Verzeichnis erstellen falls noetig
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Manifest zuerst
        zf.write(MANIFEST_PATH, "manifest.json")
        
        # Alle gesammelten Dateien
        for rel_path, abs_path in files.items():
            zf.write(abs_path, rel_path)
    
    return zip_path


def main():
    parser = argparse.ArgumentParser(
        description="ATI Agent Export Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=BACH_ROOT / "dist" / "exports",
        help="Ausgabeverzeichnis fuer ZIP"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Nur anzeigen, keine ZIP erstellen"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Detaillierte Ausgabe"
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("       ATI EXPORT SYSTEM")
    print("=" * 50)
    print(f" BACH Root: {BACH_ROOT}")
    print(f" Manifest:  {MANIFEST_PATH}")
    print("=" * 50)
    
    # Manifest laden
    try:
        manifest = load_manifest()
        print(f"\n[MANIFEST]")
        print(f"  Name:    {manifest.get('name')}")
        print(f"  Version: {manifest.get('version')}")
        print(f"  Type:    {manifest.get('type')}")
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
    
    # Dateien sammeln
    print(f"\n[COLLECTING FILES]")
    files = collect_files(manifest, verbose=args.verbose)
    
    print(f"\n[SUMMARY]")
    print(f"  Dateien gefunden: {len(files)}")
    
    if args.dry_run:
        print(f"\n[DRY-RUN] Keine ZIP erstellt")
        print(f"  Dateien die exportiert wuerden:")
        for rel_path in sorted(files.keys()):
            print(f"    - {rel_path}")
        return
    
    # ZIP erstellen
    print(f"\n[CREATING ZIP]")
    zip_path = create_export_zip(files, manifest, args.output)
    
    # Statistik
    zip_size = os.path.getsize(zip_path)
    print(f"\n[DONE]")
    print(f"  Export: {zip_path}")
    print(f"  Groesse: {zip_size / 1024:.1f} KB")
    print(f"  Dateien: {len(files) + 1}")  # +1 fuer manifest
    

if __name__ == "__main__":
    main()
