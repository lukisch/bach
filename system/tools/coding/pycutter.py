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
Tool: c_pycutter
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version c_pycutter

Description:
    [Beschreibung hinzufügen]

Usage:
    python c_pycutter.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

"""
c_pycutter.py - Python-Klassen-Extractor

Zweck: Zerlegt Python-Dateien in separate Textdateien für jede Klasse,
       plus eine Hilfsfunktionen.txt für Imports, Funktionen und globalen Code.
       Ideal für Code-Review, Dokumentation oder LLM-Kontextmanagement.

Autor: Claude (adaptiert von pyCuttertxt.py)
Abhängigkeiten: ast, os, datetime (stdlib)

Usage:
    python c_pycutter.py <python_file> [--output-dir <dir>] [--json]
    
Beispiele:
    python c_pycutter.py main.py                    # Ausgabe im aktuellen Verzeichnis
    python c_pycutter.py main.py --output-dir ./out # Ausgabe in ./out
    python c_pycutter.py main.py --json             # JSON-Output für Weiterverarbeitung
"""

import os
import ast
import sys
import json
from datetime import datetime
from typing import Dict, Any, List, Optional


def extract_python_components(filepath: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Extrahiert Klassen, Funktionen und Imports aus einer Python-Datei.
    
    Args:
        filepath: Pfad zur Python-Datei
        output_dir: Optionaler Ausgabeordner (default: neben Quelldatei)
    
    Returns:
        Dict mit Statistiken und erstellten Dateien
    """
    if not os.path.isfile(filepath):
        return {"error": f"Datei nicht gefunden: {filepath}"}
    
    # Ausgabeordner bestimmen
    base_dir = os.path.dirname(filepath) or "."
    name = os.path.splitext(os.path.basename(filepath))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if output_dir:
        outdir = output_dir
    else:
        outdir = os.path.join(base_dir, f"{name}_{timestamp}")
    
    os.makedirs(outdir, exist_ok=True)
    
    # Datei lesen und parsen
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return {"error": f"Syntax-Fehler: {e}"}
    
    lines = source.splitlines()
    
    # Komponenten sammeln
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    
    result = {
        "source_file": filepath,
        "output_dir": outdir,
        "classes": [],
        "helper_file": None,
        "stats": {
            "total_classes": len(classes),
            "total_functions": len(functions),
            "total_imports": len(imports),
            "total_lines": len(lines)
        }
    }
    
    # Klassen in separate Dateien speichern
    for cls in classes:
        start_line = cls.lineno - 1
        end_line = getattr(cls, "end_lineno", start_line)
        code = "\n".join(lines[start_line:end_line])
        
        out_path = os.path.join(outdir, f"{cls.name}.txt")
        with open(out_path, "w", encoding="utf-8") as out:
            out.write(code)
        
        result["classes"].append({
            "name": cls.name,
            "file": f"{cls.name}.txt",
            "lines": end_line - start_line
        })
    
    # Hilfsfunktionen sammeln (Imports, Funktionen, globaler Code)
    helper_lines = []
    
    # Imports
    for imp in imports:
        start = imp.lineno - 1
        end = getattr(imp, "end_lineno", imp.lineno)
        helper_lines.extend(lines[start:end])
    
    # Funktionen
    for func in functions:
        start = func.lineno - 1
        end = getattr(func, "end_lineno", func.lineno)
        helper_lines.extend(lines[start:end])
    
    # Restlicher Top-Level-Code
    occupied = set()
    for node in classes + functions + imports:
        occupied.update(range(node.lineno - 1, getattr(node, "end_lineno", node.lineno)))
    
    for i, line in enumerate(lines):
        if i not in occupied and line.strip():
            helper_lines.append(line)
    
    # Hilfsfunktionen speichern
    if helper_lines:
        helper_path = os.path.join(outdir, "Hilfsfunktionen.txt")
        with open(helper_path, "w", encoding="utf-8") as out:
            out.write("\n".join(helper_lines))
        result["helper_file"] = {
            "file": "Hilfsfunktionen.txt",
            "lines": len(helper_lines)
        }
    
    return result


def print_report(result: Dict[str, Any]) -> None:
    """Gibt einen lesbaren Report aus."""
    if "error" in result:
        print(f"FEHLER: {result['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"pyCutter - Python-Klassen-Extractor")
    print(f"{'='*60}")
    print(f"Quelle: {result['source_file']}")
    print(f"Ausgabe: {result['output_dir']}")
    print(f"{'='*60}\n")
    
    print("Extrahierte Klassen:")
    for cls in result["classes"]:
        print(f"  • {cls['file']:30} ({cls['lines']} Zeilen)")
    
    if result["helper_file"]:
        print(f"\nHilfsfunktionen:")
        print(f"  • {result['helper_file']['file']:30} ({result['helper_file']['lines']} Zeilen)")
    
    stats = result["stats"]
    print(f"\n{'='*60}")
    print(f"Statistik: {stats['total_classes']} Klassen, {stats['total_functions']} Funktionen, {stats['total_imports']} Imports")
    print(f"Original: {stats['total_lines']} Zeilen")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Zerlegt Python-Dateien in separate Klassen-Dateien",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python c_pycutter.py main.py
  python c_pycutter.py main.py --output-dir ./extracted
  python c_pycutter.py main.py --json
        """
    )
    parser.add_argument("file", help="Python-Datei zum Zerlegen")
    parser.add_argument("--output-dir", "-o", help="Ausgabeverzeichnis")
    parser.add_argument("--json", action="store_true", help="JSON-Output")
    
    args = parser.parse_args()
    
    result = extract_python_components(args.file, args.output_dir)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_report(result)
