#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
PolicyApplier - BACH Policy Management System
==============================================
Version: 1.0.0
Date: 2026-01-22

Task: BOOTSTRAP_010 - Phase 3.2: PolicyApplier Klasse und Validation-Checks

Funktion:
- Liest BACH-Policies aus _policies/ Ordnern
- Wendet Policies auf Projekte an
- Führt Validation-Checks durch
- Generiert Compliance-Reports
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class PolicyApplier:
    """Wendet BACH-Policies auf Projekte an und validiert Compliance."""
    
    def __init__(self, project_root: str, policies_dir: Optional[str] = None):
        """
        Initialisiert den PolicyApplier.
        
        Args:
            project_root: Wurzelverzeichnis des Projekts
            policies_dir: Pfad zu Policy-Dateien (default: project_root/_policies)
        """
        self.project_root = Path(project_root)
        self.policies_dir = Path(policies_dir) if policies_dir else self.project_root / "_policies"
        self.policies: Dict[str, dict] = {}
        self.validation_results: List[dict] = []
        
    def load_policies(self) -> Dict[str, dict]:
        """Lädt alle verfügbaren Policies."""
        if not self.policies_dir.exists():
            return {}
            
        for policy_file in self.policies_dir.glob("*.json"):
            try:
                with open(policy_file, 'r', encoding='utf-8') as f:
                    self.policies[policy_file.stem] = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"[WARN] Policy nicht lesbar: {policy_file} - {e}")
                
        return self.policies
    
    def check_encoding(self, target_dir: Optional[Path] = None) -> List[dict]:
        """
        Prüft Encoding-Compliance (UTF-8 ohne BOM).
        
        Returns:
            Liste von Violations mit Datei und Problem
        """
        violations = []
        scan_dir = target_dir or self.project_root
        
        # Dateitypen die geprüft werden
        check_extensions = {'.py', '.md', '.json', '.txt', '.yaml', '.yml'}
        
        for root, _, files in os.walk(scan_dir):
            # Skip versteckte und system Ordner
            if any(skip in root for skip in ['.git', '__pycache__', 'node_modules']):
                continue
                
            for filename in files:
                ext = Path(filename).suffix.lower()
                if ext not in check_extensions:
                    continue
                    
                filepath = Path(root) / filename
                try:
                    with open(filepath, 'rb') as f:
                        content = f.read(4)
                        
                    # BOM-Check
                    if content.startswith(b'\xef\xbb\xbf'):
                        violations.append({
                            'file': str(filepath.relative_to(self.project_root)),
                            'type': 'encoding',
                            'issue': 'UTF-8 BOM detected',
                            'severity': 'warning'
                        })
                except IOError:
                    pass
                    
        return violations
    
    def check_naming(self, target_dir: Optional[Path] = None) -> List[dict]:
        """
        Prüft Naming Convention Compliance.
        
        Rules:
        - Keine Leerzeichen in Dateinamen
        - Keine Umlaute (äöüß)
        - Lowercase (außer README, SKILL, CHANGELOG, LICENSE)
        """
        violations = []
        scan_dir = target_dir or self.project_root
        
        # Erlaubte Großschreibung
        allowed_uppercase = {'README', 'SKILL', 'CHANGELOG', 'LICENSE', 'TODO', 'BUGLOG'}
        
        # Verbotene Zeichen
        forbidden_pattern = re.compile(r'[äöüßÄÖÜ\s]')
        
        for root, dirs, files in os.walk(scan_dir):
            if any(skip in root for skip in ['.git', '__pycache__', 'node_modules']):
                continue
                
            for name in files + dirs:
                issues = []
                
                # Leerzeichen/Umlaute
                if forbidden_pattern.search(name):
                    issues.append('Forbidden characters (spaces/umlauts)')
                    
                # Großbuchstaben-Check (für Dateien)
                stem = Path(name).stem
                if stem.upper() not in allowed_uppercase and not stem.islower() and not stem.startswith('_'):
                    if any(c.isupper() for c in stem):
                        issues.append('Should be lowercase')
                        
                if issues:
                    rel_path = Path(root).relative_to(self.project_root) / name
                    violations.append({
                        'file': str(rel_path),
                        'type': 'naming',
                        'issue': '; '.join(issues),
                        'severity': 'warning'
                    })
                    
        return violations
    
    def check_structure(self, template: str = 'python-cli') -> List[dict]:
        """
        Prüft ob erforderliche Strukturelemente vorhanden sind.
        
        Args:
            template: Template-Typ (python-cli, llm-skill, llm-agent)
        """
        violations = []
        
        # Template-spezifische Anforderungen
        requirements = {
            'python-cli': {
                'files': ['README.md', 'setup.py'],
                'dirs': ['src', 'tests']
            },
            'llm-skill': {
                'files': ['SKILL.md', 'README.md'],
                'dirs': ['_config', '_data']
            },
            'llm-agent': {
                'files': ['SKILL.md', 'README.md'],
                'dirs': ['_config', '_data', '_memory', '_workflows']
            }
        }
        
        reqs = requirements.get(template, requirements['python-cli'])
        
        # Pflichtdateien prüfen
        for required_file in reqs['files']:
            if not (self.project_root / required_file).exists():
                # Check auch pyproject.toml als Alternative zu setup.py
                if required_file == 'setup.py' and (self.project_root / 'pyproject.toml').exists():
                    continue
                violations.append({
                    'file': required_file,
                    'type': 'structure',
                    'issue': f'Required file missing',
                    'severity': 'error'
                })
                
        # Pflichtordner prüfen
        for required_dir in reqs['dirs']:
            if not (self.project_root / required_dir).is_dir():
                violations.append({
                    'file': required_dir,
                    'type': 'structure',
                    'issue': f'Required directory missing',
                    'severity': 'error'
                })
                
        return violations
    
    def validate_all(self, template: str = 'python-cli') -> Dict:
        """
        Führt alle Validation-Checks durch.
        
        Returns:
            Dict mit allen Ergebnissen und Zusammenfassung
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'project': str(self.project_root),
            'template': template,
            'encoding': self.check_encoding(),
            'naming': self.check_naming(),
            'structure': self.check_structure(template)
        }
        
        # Zusammenfassung
        total_errors = sum(1 for v in results['encoding'] + results['naming'] + results['structure'] 
                          if v.get('severity') == 'error')
        total_warnings = sum(1 for v in results['encoding'] + results['naming'] + results['structure'] 
                            if v.get('severity') == 'warning')
        
        results['summary'] = {
            'errors': total_errors,
            'warnings': total_warnings,
            'compliant': total_errors == 0
        }
        
        self.validation_results = results
        return results
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generiert einen lesbaren Compliance-Report."""
        if not self.validation_results:
            self.validate_all()
            
        r = self.validation_results
        lines = [
            "=" * 60,
            "BACH POLICY COMPLIANCE REPORT",
            "=" * 60,
            f"Project: {r['project']}",
            f"Template: {r['template']}",
            f"Timestamp: {r['timestamp']}",
            "",
            f"Status: {'[OK] COMPLIANT' if r['summary']['compliant'] else '[FAIL] NON-COMPLIANT'}",
            f"Errors: {r['summary']['errors']}",
            f"Warnings: {r['summary']['warnings']}",
            ""
        ]
        
        # Details für jeden Check-Typ
        for check_type in ['encoding', 'naming', 'structure']:
            violations = r.get(check_type, [])
            if violations:
                lines.append(f"\n[{check_type.upper()}] {len(violations)} Issues:")
                for v in violations:
                    icon = '[ERR]' if v['severity'] == 'error' else '[WARN]'
                    lines.append(f"  {icon} {v['file']}: {v['issue']}")
            else:
                lines.append(f"\n[{check_type.upper()}] [OK] No issues")
                
        lines.append("\n" + "=" * 60)
        
        report = "\n".join(lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
        return report
    
    def apply_encoding_fix(self, dry_run: bool = True) -> List[str]:
        """
        Entfernt UTF-8 BOM von Dateien.
        
        Args:
            dry_run: Nur anzeigen, nicht ändern
            
        Returns:
            Liste der geänderten/zu ändernden Dateien
        """
        violations = self.check_encoding()
        fixed = []
        
        for v in violations:
            if v['issue'] == 'UTF-8 BOM detected':
                filepath = self.project_root / v['file']
                if dry_run:
                    fixed.append(f"[DRY-RUN] Would fix: {v['file']}")
                else:
                    try:
                        with open(filepath, 'rb') as f:
                            content = f.read()
                        if content.startswith(b'\xef\xbb\xbf'):
                            with open(filepath, 'wb') as f:
                                f.write(content[3:])  # BOM entfernen
                            fixed.append(f"[FIXED] {v['file']}")
                    except IOError as e:
                        fixed.append(f"[ERROR] {v['file']}: {e}")
                        
        return fixed


# CLI Interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python policy_applier.py <project_path> [--template TYPE] [--fix-encoding]")
        sys.exit(1)
        
    project_path = sys.argv[1]
    template = 'python-cli'
    fix_encoding = False
    
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--template' and i + 1 < len(sys.argv):
            template = sys.argv[i + 1]
        elif arg == '--fix-encoding':
            fix_encoding = True
            
    applier = PolicyApplier(project_path)
    applier.validate_all(template)
    print(applier.generate_report())
    
    if fix_encoding:
        print("\n[ENCODING FIX]")
        for result in applier.apply_encoding_fix(dry_run=False):
            print(result)
