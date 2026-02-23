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
Tool: c_code_analyzer
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version c_code_analyzer

Description:
    [Beschreibung hinzufügen]

Usage:
    python c_code_analyzer.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

# -*- coding: utf-8 -*-
"""
Code-Analyzer Modul für Entwickler-Agent
Phase 2: Core Features

Nutzt coding-tools Skill für Code-Analyse
"""

import ast
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class AnalysisResult:
    """Ergebnis einer Code-Analyse"""
    file_path: str
    language: str
    lines_total: int
    lines_code: int
    lines_comment: int
    lines_blank: int
    imports: List[str]
    functions: List[Dict]
    classes: List[Dict]
    complexity_score: int
    issues: List[Dict]
    suggestions: List[str]
    analyzed_at: str


class CodeAnalyzer:
    """Code-Analyse-Engine für Python-Dateien"""
    
    COMPLEXITY_WEIGHTS = {
        'if': 1, 'elif': 1, 'else': 1,
        'for': 2, 'while': 2,
        'try': 1, 'except': 1,
        'with': 1,
        'lambda': 1,
        'and': 0.5, 'or': 0.5,
        'nested_depth': 2
    }
    
    def __init__(self):
        self.results_cache = {}
    
    def analyze_file(self, file_path: str) -> AnalysisResult:
        """Analysiert eine Python-Datei vollständig"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
        
        content = path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Basis-Metriken
        lines_total = len(lines)
        lines_blank = sum(1 for line in lines if not line.strip())
        lines_comment = sum(1 for line in lines if line.strip().startswith('#'))
        lines_code = lines_total - lines_blank - lines_comment
        
        # AST-Analyse
        try:
            tree = ast.parse(content)
            imports = self._extract_imports(tree)
            functions = self._extract_functions(tree, content)
            classes = self._extract_classes(tree, content)
            complexity = self._calculate_complexity(tree)
        except SyntaxError as e:
            imports, functions, classes = [], [], []
            complexity = -1  # Fehler-Indikator
        
        # Issues & Suggestions
        issues = self._find_issues(content, lines)
        suggestions = self._generate_suggestions(
            lines_code, functions, classes, complexity, issues
        )
        
        result = AnalysisResult(
            file_path=str(path.absolute()),
            language="python",
            lines_total=lines_total,
            lines_code=lines_code,
            lines_comment=lines_comment,
            lines_blank=lines_blank,
            imports=imports,
            functions=functions,
            classes=classes,
            complexity_score=complexity,
            issues=issues,
            suggestions=suggestions,
            analyzed_at=datetime.now().isoformat()
        )
        
        self.results_cache[file_path] = result
        return result
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extrahiert alle Imports"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        return imports
    
    def _extract_functions(self, tree: ast.AST, content: str) -> List[Dict]:
        """Extrahiert Funktions-Informationen"""
        functions = []
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Docstring extrahieren
                docstring = ast.get_docstring(node) or ""
                
                # Parameter
                args = []
                for arg in node.args.args:
                    arg_info = {"name": arg.arg}
                    if arg.annotation:
                        arg_info["type"] = ast.unparse(arg.annotation)
                    args.append(arg_info)
                
                # Return-Typ
                return_type = None
                if node.returns:
                    return_type = ast.unparse(node.returns)
                
                functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "end_line": node.end_lineno,
                    "args": args,
                    "return_type": return_type,
                    "docstring": docstring[:200] if docstring else None,
                    "is_private": node.name.startswith('_'),
                    "decorators": [ast.unparse(d) for d in node.decorator_list]
                })
        
        return functions
    
    def _extract_classes(self, tree: ast.AST, content: str) -> List[Dict]:
        """Extrahiert Klassen-Informationen"""
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node) or ""
                
                # Methoden zählen
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                
                # Basis-Klassen
                bases = [ast.unparse(b) for b in node.bases]
                
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "end_line": node.end_lineno,
                    "bases": bases,
                    "method_count": len(methods),
                    "docstring": docstring[:200] if docstring else None,
                    "decorators": [ast.unparse(d) for d in node.decorator_list]
                })
        
        return classes
    
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Berechnet zyklomatische Komplexität (vereinfacht)"""
        complexity = 1  # Basis
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.IfExp)):
                complexity += self.COMPLEXITY_WEIGHTS['if']
            elif isinstance(node, ast.For):
                complexity += self.COMPLEXITY_WEIGHTS['for']
            elif isinstance(node, ast.While):
                complexity += self.COMPLEXITY_WEIGHTS['while']
            elif isinstance(node, ast.Try):
                complexity += self.COMPLEXITY_WEIGHTS['try']
            elif isinstance(node, ast.ExceptHandler):
                complexity += self.COMPLEXITY_WEIGHTS['except']
            elif isinstance(node, ast.With):
                complexity += self.COMPLEXITY_WEIGHTS['with']
            elif isinstance(node, ast.Lambda):
                complexity += self.COMPLEXITY_WEIGHTS['lambda']
            elif isinstance(node, ast.BoolOp):
                if isinstance(node.op, ast.And):
                    complexity += self.COMPLEXITY_WEIGHTS['and']
                elif isinstance(node.op, ast.Or):
                    complexity += self.COMPLEXITY_WEIGHTS['or']
        
        return int(complexity)
    
    def _find_issues(self, content: str, lines: List[str]) -> List[Dict]:
        """Findet potenzielle Code-Probleme"""
        issues = []
        
        # TODO/FIXME Kommentare
        for i, line in enumerate(lines, 1):
            if 'TODO' in line:
                issues.append({
                    "type": "todo",
                    "line": i,
                    "message": line.strip(),
                    "severity": "info"
                })
            elif 'FIXME' in line:
                issues.append({
                    "type": "fixme",
                    "line": i,
                    "message": line.strip(),
                    "severity": "warning"
                })
            elif 'XXX' in line or 'HACK' in line:
                issues.append({
                    "type": "hack",
                    "line": i,
                    "message": line.strip(),
                    "severity": "warning"
                })
        
        # Lange Zeilen (>120 Zeichen)
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append({
                    "type": "long_line",
                    "line": i,
                    "message": f"Zeile hat {len(line)} Zeichen (max 120 empfohlen)",
                    "severity": "style"
                })
        
        # Print-Statements (potenzielle Debug-Reste)
        print_pattern = re.compile(r'^\s*print\s*\(')
        for i, line in enumerate(lines, 1):
            if print_pattern.match(line):
                issues.append({
                    "type": "debug_print",
                    "line": i,
                    "message": "Print-Statement gefunden (Debug-Rest?)",
                    "severity": "info"
                })
        
        return issues
    
    def _generate_suggestions(self, lines_code: int, functions: List[Dict],
                             classes: List[Dict], complexity: int,
                             issues: List[Dict]) -> List[str]:
        """Generiert Verbesserungsvorschläge"""
        suggestions = []
        
        # Komplexitäts-Warnung
        if complexity > 20:
            suggestions.append(
                f"⚠️ Hohe Komplexität ({complexity}): Code aufteilen empfohlen"
            )
        elif complexity > 10:
            suggestions.append(
                f"💡 Mittlere Komplexität ({complexity}): Refactoring prüfen"
            )
        
        # Große Dateien
        if lines_code > 500:
            suggestions.append(
                f"📦 Große Datei ({lines_code} Zeilen): Module aufteilen?"
            )
        
        # Fehlende Docstrings
        undocumented = [f for f in functions if not f.get('docstring')]
        if undocumented:
            suggestions.append(
                f"📝 {len(undocumented)} Funktionen ohne Docstring"
            )
        
        # Issues zusammenfassen
        todos = len([i for i in issues if i['type'] == 'todo'])
        fixmes = len([i for i in issues if i['type'] == 'fixme'])
        
        if todos > 0:
            suggestions.append(f"📌 {todos} TODO-Kommentare offen")
        if fixmes > 0:
            suggestions.append(f"🔧 {fixmes} FIXME-Kommentare offen")
        
        return suggestions
    
    def to_dict(self, result: AnalysisResult) -> Dict:
        """Konvertiert Ergebnis zu Dictionary"""
        return asdict(result)
    
    def to_json(self, result: AnalysisResult) -> str:
        """Konvertiert Ergebnis zu JSON"""
        return json.dumps(self.to_dict(result), indent=2, ensure_ascii=False)


# CLI für direkten Aufruf
if __name__ == "__main__":
    import sys
    import io
    
    # Windows UTF-8 Fix
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    if len(sys.argv) < 2:
        print("Usage: python code_analyzer.py <file.py>")
        sys.exit(1)
    
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_file(sys.argv[1])
    
    print(f"\n=== Code-Analyse: {result.file_path} ===\n")
    print(f"Zeilen: {result.lines_total} (Code: {result.lines_code}, "
          f"Kommentare: {result.lines_comment}, Leer: {result.lines_blank})")
    print(f"Komplexität: {result.complexity_score}")
    print(f"Funktionen: {len(result.functions)}")
    print(f"Klassen: {len(result.classes)}")
    print(f"Imports: {len(result.imports)}")
    
    if result.issues:
        print(f"\n⚠️ Issues ({len(result.issues)}):")
        for issue in result.issues[:5]:
            print(f"  L{issue['line']}: {issue['message'][:60]}")
    
    if result.suggestions:
        print(f"\n💡 Vorschläge:")
        for suggestion in result.suggestions:
            print(f"  {suggestion}")
