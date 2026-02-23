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
ATI Module: Path Healer v1.0.0
Wiederverwendbares Pfad-Heilungs-Modul für ATI-Projekte

Basiert auf: BACH Path Healer v1.0.0
Vereinfacht für projektübergreifende Nutzung

Usage (als Modul):
    from _modules.path_healer import ProjectPathHealer
    healer = ProjectPathHealer(project_root="/path/to/project")
    healer.add_correction("old/path", "new/path")
    issues = healer.scan()
    healer.fix_all()
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass


@dataclass
class PathIssue:
    """Gefundenes Pfad-Problem."""
    file_path: str
    line_number: int
    old_text: str
    new_text: str
    context: str


class ProjectPathHealer:
    """Projektunabhängiger Pfad-Heiler für ATI-Projekte."""
    
    DEFAULT_EXTENSIONS = {'.json', '.md', '.py', '.txt', '.yaml', '.yml', '.toml'}
    DEFAULT_IGNORE = {'__pycache__', '.git', 'node_modules', 'venv', '.venv', 'dist', 'build'}
    
    def __init__(self, project_root: str):
        """
        Args:
            project_root: Basis-Pfad des Projekts
        """
        self.project_root = Path(project_root)
        self.corrections: List[Tuple[str, str]] = []
        self.issues: List[PathIssue] = []
        self.extensions = self.DEFAULT_EXTENSIONS.copy()
        self.ignore_dirs = self.DEFAULT_IGNORE.copy()
    
    def add_correction(self, old_path: str, new_path: str) -> 'ProjectPathHealer':
        """Füge Pfad-Korrektur hinzu."""
        self.corrections.append((old_path, new_path))
        return self
    
    def add_corrections(self, corrections: List[Tuple[str, str]]) -> 'ProjectPathHealer':
        """Füge mehrere Korrekturen hinzu."""
        self.corrections.extend(corrections)
        return self
    
    def set_extensions(self, extensions: Set[str]) -> 'ProjectPathHealer':
        """Setze zu scannende Dateiendungen."""
        self.extensions = extensions
        return self
    
    def add_ignore_dir(self, dirname: str) -> 'ProjectPathHealer':
        """Füge zu ignorierendes Verzeichnis hinzu."""
        self.ignore_dirs.add(dirname)
        return self
    
    def scan(self) -> List[PathIssue]:
        """
        Scanne Projekt nach Pfad-Problemen.
        
        Returns:
            Liste gefundener Probleme
        """
        self.issues = []
        
        for file_path in self._walk_files():
            try:
                content = file_path.read_text(encoding='utf-8')
                self._check_file(file_path, content)
            except (UnicodeDecodeError, PermissionError):
                continue
        
        return self.issues
    
    def fix_all(self, dry_run: bool = False) -> int:
        """
        Behebe alle gefundenen Probleme.
        
        Args:
            dry_run: Wenn True, nur simulieren
            
        Returns:
            Anzahl behobener Dateien
        """
        if not self.issues:
            self.scan()
        
        files_fixed = set()
        
        for issue in self.issues:
            if issue.file_path in files_fixed and dry_run:
                continue
                
            file_path = Path(issue.file_path)
            try:
                content = file_path.read_text(encoding='utf-8')
                new_content = content.replace(issue.old_text, issue.new_text)
                
                if not dry_run and new_content != content:
                    file_path.write_text(new_content, encoding='utf-8')
                    files_fixed.add(issue.file_path)
            except Exception:
                continue
        
        return len(files_fixed)
    
    def _walk_files(self):
        """Iteriere über alle relevanten Dateien."""
        for root, dirs, files in os.walk(self.project_root):
            # Ignoriere bestimmte Verzeichnisse
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for filename in files:
                file_path = Path(root) / filename
                if file_path.suffix.lower() in self.extensions:
                    yield file_path
    
    def _check_file(self, file_path: Path, content: str):
        """Prüfe einzelne Datei auf Probleme."""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for old_str, new_str in self.corrections:
                if old_str in line:
                    self.issues.append(PathIssue(
                        file_path=str(file_path),
                        line_number=line_num,
                        old_text=old_str,
                        new_text=new_str,
                        context=line.strip()[:80]
                    ))
    
    def get_report(self) -> str:
        """Generiere Textbericht."""
        if not self.issues:
            return "Keine Pfad-Probleme gefunden."
        
        lines = [f"Path Healer Report: {len(self.issues)} Probleme gefunden\n"]
        
        by_file: Dict[str, List[PathIssue]] = {}
        for issue in self.issues:
            by_file.setdefault(issue.file_path, []).append(issue)
        
        for file_path, file_issues in by_file.items():
            lines.append(f"\n{file_path}:")
            for issue in file_issues:
                lines.append(f"  L{issue.line_number}: {issue.old_text} -> {issue.new_text}")
        
        return '\n'.join(lines)


# Standalone-Nutzung
if __name__ == "__main__":
    import sys
    
    project = sys.argv[1] if len(sys.argv) > 1 else "."
    healer = ProjectPathHealer(project)
    
    # Beispiel-Korrekturen
    healer.add_correction("old/path", "new/path")
    
    issues = healer.scan()
    print(healer.get_report())
