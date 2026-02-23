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

"""Abhängigkeits- und Nutzungsanalyse der Tools"""
import os
import re
from pathlib import Path
from collections import defaultdict
import json

# Verzeichnisse die gescannt werden
scan_dirs = [".", "tools", "core", "connectors", "agents", "hub"]
tools_dir = Path("tools")

# Sammle alle Tool-Namen
all_tools = []
for pyfile in sorted(tools_dir.glob("**/*.py")):
    if "node_modules" in str(pyfile) or "__pycache__" in str(pyfile):
        continue
    tool_name = pyfile.stem
    all_tools.append((tool_name, pyfile))

# Abhängigkeiten finden
dependencies = defaultdict(list)  # Tool -> [was es importiert]
used_by = defaultdict(list)        # Tool -> [wer es benutzt]

print("=" * 80)
print("ABHÄNGIGKEITSANALYSE")
print("=" * 80)
print(f"\nAnalysiere {len(all_tools)} Tools...\n")

# 1. Interne Abhängigkeiten (Import-Beziehungen)
for tool_name, tool_path in all_tools:
    try:
        content = tool_path.read_text(encoding="utf-8")
    except:
        try:
            content = tool_path.read_text(encoding="latin-1")
        except:
            continue

    # Finde alle Imports
    # from tools.xyz import ... oder import tools.xyz
    imports = re.findall(r'from\s+tools\.(\S+)\s+import', content)
    imports += re.findall(r'import\s+tools\.(\S+)', content)

    for imp in imports:
        # Bereinige den Import-Namen
        imp_clean = imp.split(".")[0]
        dependencies[tool_name].append(imp_clean)

# 2. Externe Nutzung (wird das Tool irgendwo aufgerufen?)
usage_patterns = defaultdict(list)

print("Scanne System nach Tool-Aufrufen...")
for scan_dir in scan_dirs:
    scan_path = Path(scan_dir)
    if not scan_path.exists():
        continue

    for pyfile in scan_path.glob("**/*.py"):
        if "node_modules" in str(pyfile) or "__pycache__" in str(pyfile):
            continue

        try:
            content = pyfile.read_text(encoding="utf-8")
        except:
            try:
                content = pyfile.read_text(encoding="latin-1")
            except:
                continue

        # Prüfe ob Tools erwähnt werden
        for tool_name, tool_path in all_tools:
            # Suche nach verschiedenen Nutzungsmustern
            patterns = [
                f"python.*{tool_name}",  # python tool.py
                f"import.*{tool_name}",  # import tool
                f"from.*{tool_name}",    # from tool import
                f"{tool_name}\\.py",     # tool.py erwähnt
            ]

            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    rel_path = str(pyfile.relative_to("."))
                    if rel_path not in usage_patterns[tool_name]:
                        usage_patterns[tool_name].append(rel_path)
                    if tool_path.stem not in ["__init__"]:
                        used_by[pyfile.stem].append(tool_name)
                    break

# 3. CLI-Registrierung prüfen
cli_registered = []
try:
    # Prüfe bach.py
    bach_content = Path("bach.py").read_text(encoding="utf-8")
    for tool_name, _ in all_tools:
        if tool_name in bach_content:
            cli_registered.append(tool_name)
except:
    pass

# 4. Ausgabe
print("\n" + "=" * 80)
print("ABHÄNGIGKEITEN (Top 20)")
print("=" * 80)
for tool, deps in sorted(dependencies.items(), key=lambda x: -len(x[1]))[:20]:
    if deps:
        print(f"\n{tool}:")
        for dep in deps:
            print(f"  → {dep}")

print("\n" + "=" * 80)
print("NUTZUNGSANALYSE")
print("=" * 80)

# Ungenutzte Tools
unused_tools = []
for tool_name, tool_path in all_tools:
    if tool_name not in usage_patterns and tool_name not in cli_registered:
        if "_archive" not in str(tool_path) and tool_name != "__init__":
            unused_tools.append(str(tool_path.relative_to("tools")))

print(f"\n🔴 UNGENUTZTE TOOLS ({len(unused_tools)} Dateien):")
print("-" * 40)
for tool in sorted(unused_tools)[:30]:
    print(f"  • {tool}")
if len(unused_tools) > 30:
    print(f"  ... und {len(unused_tools) - 30} weitere")

# Meist-genutzte Tools
print(f"\n\n🟢 MEIST-GENUTZTE TOOLS (Top 20):")
print("-" * 40)
for tool, usages in sorted(usage_patterns.items(), key=lambda x: -len(x[1]))[:20]:
    print(f"  {tool:40s} - {len(usages):2d}x verwendet")

# CLI-registrierte Tools
print(f"\n\n📋 CLI-REGISTRIERTE TOOLS:")
print("-" * 40)
print(f"  {len(cli_registered)} Tools in bach.py gefunden")

# Tools die nirgends auftauchen (Kandidaten zum Löschen)
truly_unused = []
for tool_name, tool_path in all_tools:
    if (tool_name not in usage_patterns and
        tool_name not in cli_registered and
        "_archive" not in str(tool_path) and
        "test" not in str(tool_path).lower() and
        tool_name != "__init__"):
        truly_unused.append(str(tool_path.relative_to("tools")))

print(f"\n\n⚠️  KANDIDATEN ZUM LÖSCHEN ({len(truly_unused)} Dateien):")
print("-" * 40)
print("(nicht in Archive, nicht in Tests, keine Nutzung gefunden)")
for tool in sorted(truly_unused)[:20]:
    print(f"  • {tool}")
if len(truly_unused) > 20:
    print(f"  ... und {len(truly_unused) - 20} weitere")

# Statistik
print("\n" + "=" * 80)
print("STATISTIK")
print("=" * 80)
print(f"Gesamt Tools:           {len(all_tools)}")
print(f"Mit Dependencies:       {len([d for d in dependencies.values() if d])}")
print(f"Verwendet (gefunden):   {len(usage_patterns)}")
print(f"CLI-registriert:        {len(cli_registered)}")
print(f"Ungenutzt (potentiell): {len(unused_tools)}")
print(f"Lösch-Kandidaten:       {len(truly_unused)}")

print("\n" + "=" * 80)

# Export für weitere Analyse
result = {
    "dependencies": {k: v for k, v in dependencies.items() if v},
    "usage": {k: v for k, v in usage_patterns.items()},
    "unused": unused_tools,
    "delete_candidates": truly_unused
}

with open("tools/analysis_results.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("\n✓ Detaillierte Ergebnisse in tools/analysis_results.json")
