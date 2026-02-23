#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
B007 - Abhaengigkeiten
======================
Analysiert externe Dependencies und Imports.

Output: JSON mit Dependency-Liste und Risiko-Bewertung
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def analyze_dependencies(root_path: str) -> dict:
    """Analysiert Abhaengigkeiten eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "scan_date": datetime.now().isoformat(),
        "package_files": [],
        "python_imports": defaultdict(int),
        "js_imports": defaultdict(int),
        "external_refs": [],
        "summary": {},
        "score": 0.0
    }
    
    # Suche Package-Dateien
    package_patterns = [
        "requirements.txt",
        "setup.py",
        "pyproject.toml",
        "package.json",
        "package-lock.json",
        "Pipfile",
        "environment.yml"
    ]
    
    for pattern in package_patterns:
        for f in root.rglob(pattern):
            if "__pycache__" not in str(f):
                rel = str(f.relative_to(root))
                result["package_files"].append({
                    "file": pattern,
                    "path": rel,
                    "size": f.stat().st_size
                })
    
    # Python-Standard-Library (vereinfacht)
    stdlib = {
        "os", "sys", "re", "json", "datetime", "pathlib", "collections",
        "typing", "functools", "itertools", "math", "random", "time",
        "subprocess", "shutil", "glob", "logging", "argparse", "configparser",
        "sqlite3", "csv", "io", "copy", "hashlib", "base64", "urllib"
    }
    
    # Analysiere Python-Dateien
    for f in root.rglob("*.py"):
        if "__pycache__" in str(f):
            continue
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            
            # import xyz
            for match in re.finditer(r'^import\s+(\w+)', content, re.MULTILINE):
                module = match.group(1)
                result["python_imports"][module] += 1
            
            # from xyz import ...
            for match in re.finditer(r'^from\s+(\w+)', content, re.MULTILINE):
                module = match.group(1)
                result["python_imports"][module] += 1
                
        except:
            continue
    
    # Klassifiziere Python-Imports
    py_imports = dict(result["python_imports"])
    result["python_imports"] = {
        "stdlib": {k: v for k, v in py_imports.items() if k in stdlib},
        "external": {k: v for k, v in py_imports.items() if k not in stdlib and not k.startswith('_')},
        "local": {k: v for k, v in py_imports.items() if k.startswith('_') or k == "src"}
    }
    
    # Analysiere JS/TS-Dateien
    for f in list(root.rglob("*.js")) + list(root.rglob("*.ts")):
        if "node_modules" in str(f):
            continue
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            
            # require('xyz') oder import ... from 'xyz'
            for match in re.finditer(r"(?:require\(['\"]|from\s+['\"])([^'\"./][^'\"]*)", content):
                module = match.group(1).split('/')[0]
                result["js_imports"][module] += 1
                
        except:
            continue
    
    result["js_imports"] = dict(result["js_imports"])
    
    # Externe Referenzen (URLs, Pfade)
    url_pattern = re.compile(r'https?:/[^\s\'"<>]+')
    path_pattern = re.compile(r'[A-Z]:\[^\s\'"]+|/(?:home|mnt|usr)/[^\s\'"]+')
    
    for f in root.rglob("*"):
        if not f.is_file() or f.suffix not in ['.py', '.js', '.ts', '.json', '.md', '.txt']:
            continue
        if "__pycache__" in str(f) or "node_modules" in str(f):
            continue
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            
            for url in url_pattern.findall(content):
                if len(url) < 200:  # Keine kaputten Matches
                    result["external_refs"].append({
                        "type": "url",
                        "value": url[:100],
                        "file": str(f.relative_to(root))
                    })
            
            for path in path_pattern.findall(content):
                result["external_refs"].append({
                    "type": "path",
                    "value": path[:100],
                    "file": str(f.relative_to(root))
                })
        except:
            continue
    
    # Dedupliziere und limitiere
    seen = set()
    unique_refs = []
    for ref in result["external_refs"]:
        key = ref["value"]
        if key not in seen:
            seen.add(key)
            unique_refs.append(ref)
    result["external_refs"] = unique_refs[:30]
    
    # Summary
    py_external = len(result["python_imports"].get("external", {}))
    js_external = len(result["js_imports"])
    
    result["summary"] = {
        "has_package_manager": len(result["package_files"]) > 0,
        "python_external_deps": py_external,
        "js_external_deps": js_external,
        "total_external_deps": py_external + js_external,
        "external_urls": sum(1 for r in result["external_refs"] if r["type"] == "url"),
        "hardcoded_paths": sum(1 for r in result["external_refs"] if r["type"] == "path")
    }
    
    # Score: Weniger externe Deps = besser, keine hardcoded paths = besser
    score = 4.0
    
    if result["summary"]["total_external_deps"] > 20:
        score -= 1.0
    elif result["summary"]["total_external_deps"] > 10:
        score -= 0.5
    
    if result["summary"]["hardcoded_paths"] > 10:
        score -= 1.0
    elif result["summary"]["hardcoded_paths"] > 5:
        score -= 0.5
    
    if result["summary"]["has_package_manager"]:
        score += 0.5
    
    result["score"] = max(1.0, min(5.0, round(score, 2)))
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python B007_dependencies.py <system_path> [output_json]")
        sys.exit(1)
    
    result = analyze_dependencies(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
