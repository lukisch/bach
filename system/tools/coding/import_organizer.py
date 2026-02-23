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
Tool: c_import_organizer
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version c_import_organizer

Description:
    [Beschreibung hinzufügen]

Usage:
    python c_import_organizer.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

# coding: utf-8
"""
c_import_organizer.py - Organisiert Python-Imports nach PEP8

Funktionen:
  - Sammelt alle import/from-Statements
  - Entfernt Duplikate
  - Sortiert alphabetisch (erst import, dann from)
  - Platziert alle Imports am Dateianfang
  - Bereinigt mehrfache Leerzeilen

Extrahiert aus: A1 ProFiler/PythonBox.py (ImportOptimizer)

Usage:
    python c_import_organizer.py <datei.py>
    python c_import_organizer.py <datei.py> --dry-run
    python c_import_organizer.py <datei.py> --json
    python c_import_organizer.py --stdin < code.py

Autor: Claude (adaptiert)
Abhaengigkeiten: keine (nur stdlib)
"""

import ast
import re
import sys
import json
from pathlib import Path


def organize_imports(code: str) -> tuple:
    """
    Scannt Code nach Imports, entfernt sie aus dem Body,
    entfernt Duplikate, sortiert sie und packt sie nach oben.
    
    Args:
        code: Python-Quellcode als String
        
    Returns:
        tuple: (optimierter_code, nachricht) oder (None, fehlermeldung)
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return None, f"Syntax Fehler: {e}"

    imports = []
    from_imports = []
    other_lines = code.splitlines()
    
    # Zeilennummern der Imports sammeln, um sie zu loeschen
    import_linenos = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                asname = f" as {alias.asname}" if alias.asname else ""
                imports.append(f"import {name}{asname}")
            if hasattr(node, 'end_lineno'):
                import_linenos.update(range(node.lineno - 1, node.end_lineno))
            else:
                import_linenos.add(node.lineno - 1)
        
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            names = []
            for alias in node.names:
                name = alias.name
                asname = f" as {alias.asname}" if alias.asname else ""
                names.append(f"{name}{asname}")
            from_imports.append(f"from {module} import {', '.join(names)}")
            if hasattr(node, 'end_lineno'):
                import_linenos.update(range(node.lineno - 1, node.end_lineno))
            else:
                import_linenos.add(node.lineno - 1)

    # Duplikate entfernen und sortieren
    imports = sorted(list(set(imports)))
    from_imports = sorted(list(set(from_imports)))

    # Code ohne Imports rekonstruieren
    new_body = []
    for i, line in enumerate(other_lines):
        if i not in import_linenos:
            new_body.append(line)

    # Zusammenbauen
    header = imports + from_imports
    if header and new_body:
        final_code = "\n".join(header) + "\n\n" + "\n".join(new_body)
    elif header:
        final_code = "\n".join(header)
    else:
        final_code = "\n".join(new_body)

    # Mehrfache Leerzeilen bereinigen
    final_code = re.sub(r'\n{3,}', '\n\n', final_code)
    
    stats = {
        'imports_found': len(imports) + len(from_imports),
        'import_statements': len(imports),
        'from_statements': len(from_imports),
        'duplicates_removed': (len(imports) + len(from_imports)) - len(set(imports) | set(from_imports))
    }
    
    return final_code, stats


def analyze_imports(code: str) -> dict:
    """
    Analysiert Imports ohne Aenderungen vorzunehmen.
    
    Returns:
        dict mit Import-Statistiken
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {'error': str(e)}
    
    imports = []
    from_imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    'module': alias.name,
                    'alias': alias.asname,
                    'line': node.lineno
                })
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            for alias in node.names:
                from_imports.append({
                    'module': module,
                    'name': alias.name,
                    'alias': alias.asname,
                    'line': node.lineno
                })
    
    # Duplikate finden
    all_imports = [f"import {i['module']}" for i in imports]
    all_from = [f"from {i['module']} import {i['name']}" for i in from_imports]
    
    duplicates = []
    seen = set()
    for imp in all_imports + all_from:
        if imp in seen:
            duplicates.append(imp)
        seen.add(imp)
    
    return {
        'total_imports': len(imports) + len(from_imports),
        'import_statements': len(imports),
        'from_statements': len(from_imports),
        'duplicates': duplicates,
        'imports': imports,
        'from_imports': from_imports
    }


def main():
    if len(sys.argv) < 2 and sys.stdin.isatty():
        print(__doc__)
        sys.exit(1)
    
    # Optionen parsen
    dry_run = '--dry-run' in sys.argv
    json_output = '--json' in sys.argv
    analyze_only = '--analyze' in sys.argv
    from_stdin = '--stdin' in sys.argv or not sys.stdin.isatty()
    
    # Code laden
    if from_stdin:
        code = sys.stdin.read()
        filepath = None
    else:
        filepath = sys.argv[1]
        path = Path(filepath)
        if not path.exists():
            print(f"[FEHLER] Datei nicht gefunden: {filepath}")
            sys.exit(1)
        code = path.read_text(encoding='utf-8')
    
    # Nur Analyse?
    if analyze_only:
        result = analyze_imports(code)
        if json_output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Imports gesamt: {result['total_imports']}")
            print(f"  import-Statements: {result['import_statements']}")
            print(f"  from-Statements: {result['from_statements']}")
            if result['duplicates']:
                print(f"\nDuplikate gefunden:")
                for dup in result['duplicates']:
                    print(f"  - {dup}")
        sys.exit(0)
    
    # Imports organisieren
    optimized, stats = organize_imports(code)
    
    if optimized is None:
        if json_output:
            print(json.dumps({'error': stats}, ensure_ascii=False))
        else:
            print(f"[FEHLER] {stats}")
        sys.exit(1)
    
    if json_output:
        output = {
            'success': True,
            'stats': stats,
            'file': filepath
        }
        if dry_run or from_stdin:
            output['optimized_code'] = optimized
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        if dry_run:
            print(f"[DRY-RUN] Wuerde {stats['imports_found']} Imports organisieren")
            print("-" * 40)
            print(optimized)
        elif from_stdin:
            print(optimized)
        else:
            # Backup erstellen
            backup_path = filepath + '.bak'
            Path(backup_path).write_text(code, encoding='utf-8')
            
            # Optimierte Version speichern
            Path(filepath).write_text(optimized, encoding='utf-8')
            
            print(f"[OK] {stats['imports_found']} Imports organisiert")
            print(f"     Backup: {backup_path}")


if __name__ == "__main__":
    main()
