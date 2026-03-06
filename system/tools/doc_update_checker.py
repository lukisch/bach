#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: doc_update_checker
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version doc_update_checker

Description:
    [Beschreibung hinzufügen]

Usage:
    python doc_update_checker.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

# -*- coding: utf-8 -*-
"""
BACH Documentation Update Checker v1.0.1

Automatische Erkennung und Aktualisierung veralteter Dokumentationen.
Portiert von RecludOS, integriert mit BACH Memory-System.

Features:
- Erkennt veraltete Dokumente (>60 Tage, ungültige Pfade)
- Generiert Update-Vorschläge
- Erstellt Aktualisierungs-Reports
- Kann automatisch einfache Updates durchführen

Usage:
  python doc_update_checker.py check              # Prüfen
  python doc_update_checker.py report             # Report erstellen
  python doc_update_checker.py auto-update        # Auto-Update (sicher)
  python doc_update_checker.py schedule           # Für Micro-Routines
"""

import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse
import io

# Windows Console UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Pfade - BACH v1.1 (angepasst von RecludOS)
SCRIPT_DIR = Path(__file__).parent
BACH_ROOT = SCRIPT_DIR.parent  # tools/ ist direkt unter BACH/
DATA_DIR = BACH_ROOT / "data"
DB_FILE = DATA_DIR / "bach.db"
REPORTS_DIR = BACH_ROOT / "logs"
MESSAGEBOX_DIR = BACH_ROOT / "messages"

# Schwellwerte
OUTDATED_DAYS = 60
WARNING_DAYS = 30
CRITICAL_DAYS = 90

# Bekannte veraltete Pfad-Patterns (BACH-spezifisch)
PATH_MIGRATIONS = {
    # Alte Strukturen → neue BACH v1.1 Struktur
    "scripts/": "tools/",
    "handlers/": "hub/handlers/",
    "_services/": "skills/_services/",
    "_agents/": "agents/",
}

# Version-Pattern
VERSION_PATTERN = re.compile(r'[vV]?(\d+\.\d+\.\d+)')
DATE_PATTERN = re.compile(r'(\d{4}-\d{2}-\d{2})')


class DocUpdateChecker:
    """Automatische Dokumentations-Aktualisierung für BACH"""
    
    VERSION = "1.0.1"
    
    def __init__(self, db_path: Path = None):
        self.db_path = db_path or DB_FILE
        self.root = BACH_ROOT
        self.findings = []
        self.updates_made = []
    
    def check_all(self) -> Dict:
        """Führt vollständige Prüfung durch"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_docs": 0,
            "outdated": [],
            "invalid_paths": [],
            "version_mismatch": [],
            "missing_sections": [],
            "suggestions": []
        }
        
        # Lade alle Dokumentationen aus DB
        docs = self._get_all_docs()
        results["total_docs"] = len(docs)
        
        for doc in docs:
            # 1. Alter prüfen
            age_issue = self._check_age(doc)
            if age_issue:
                results["outdated"].append(age_issue)
            
            # 2. Pfade im Dokument prüfen
            path_issues = self._check_paths_in_doc(doc)
            results["invalid_paths"].extend(path_issues)
            
            # 3. Version prüfen (bei SKILL.md)
            if doc.get("doc_type") == "skill":
                version_issue = self._check_version(doc)
                if version_issue:
                    results["version_mismatch"].append(version_issue)
            
            # 4. Pflicht-Sektionen prüfen
            section_issues = self._check_required_sections(doc)
            results["missing_sections"].extend(section_issues)
        
        # Vorschläge generieren
        results["suggestions"] = self._generate_suggestions(results)
        
        return results
    
    def _get_all_docs(self) -> List[Dict]:
        """Lädt alle Dokumentationen per Dateisuche (glob-basiert)
        
        Durchsucht docs/, docs/docs/docs/help/, skills/ nach Markdown-Dateien.
        Keine DB-Tabelle erforderlich - rein dateibasiert.
        """
        docs = []
        
        # Dokumentations-Verzeichnisse durchsuchen
        doc_dirs = [
            ("docs", "readme"),
            ("help", "guide"),
            ("agents", "skill"),
            ("skills/_services", "skill"),
            ("skills/workflows", "guide"),
        ]
        
        for subdir, doc_type in doc_dirs:
            search_path = self.root / subdir
            if not search_path.exists():
                continue
            
            for md_file in search_path.rglob("*.md"):
                # Skip archivierte Dateien
                if "_archive" in str(md_file) or "__pycache__" in str(md_file):
                    continue
                
                rel_path = md_file.relative_to(self.root)
                
                # SKILL.md als "skill" markieren
                actual_doc_type = doc_type
                if md_file.name.upper() == "SKILL.MD":
                    actual_doc_type = "skill"
                elif md_file.name.upper() == "README.MD":
                    actual_doc_type = "readme"
                
                docs.append({
                    "path": str(rel_path),
                    "absolute_path": str(md_file),
                    "doc_type": actual_doc_type,
                    "name": md_file.stem
                })
        
        # Auch Root-Level Dokumentation
        for root_md in ["SKILL.md", "README.md", "ROADMAP.md", "CHANGELOG.md", "BUGLOG.md"]:
            root_file = self.root / root_md
            if root_file.exists():
                docs.append({
                    "path": root_md,
                    "absolute_path": str(root_file),
                    "doc_type": "readme" if "README" in root_md else "guide",
                    "name": root_file.stem
                })
        
        return docs
    
    def _check_age(self, doc: Dict) -> Optional[Dict]:
        """Prüft das Alter eines Dokuments"""
        if not doc.get("path"):
            return None
        
        full_path = self.root / doc["path"]
        if not full_path.exists():
            return None
        
        try:
            mtime = datetime.fromtimestamp(full_path.stat().st_mtime)
            age_days = (datetime.now() - mtime).days
            
            if age_days > CRITICAL_DAYS:
                severity = "critical"
            elif age_days > OUTDATED_DAYS:
                severity = "warning"
            else:
                return None
            
            return {
                "path": doc["path"],
                "doc_type": doc.get("doc_type"),
                "age_days": age_days,
                "last_modified": mtime.isoformat(),
                "severity": severity
            }
        except:
            return None
    
    def _check_paths_in_doc(self, doc: Dict) -> List[Dict]:
        """Prüft Pfade innerhalb eines Dokuments auf Gültigkeit"""
        issues = []
        
        if not doc.get("path"):
            return issues
        
        full_path = self.root / doc["path"]
        if not full_path.exists():
            return issues
        
        try:
            content = full_path.read_text(encoding='utf-8')
            
            # Suche nach Pfad-Referenzen
            for old_path, new_path in PATH_MIGRATIONS.items():
                if old_path in content:
                    issues.append({
                        "doc_path": doc["path"],
                        "invalid_path": old_path,
                        "correct_path": new_path,
                        "auto_fixable": True
                    })
            
            # Suche nach absoluten Windows-Pfaden die nicht existieren
            win_paths = re.findall(r'C:\[^"\s\n]+', content)
            for win_path in win_paths:
                clean_path = win_path.rstrip(r'\.,;:')
                if not Path(clean_path).exists():
                    # Prüfe ob es ein BACH-Pfad ist
                    if "BACH" in clean_path:
                        issues.append({
                            "doc_path": doc["path"],
                            "invalid_path": clean_path,
                            "correct_path": None,
                            "auto_fixable": False,
                            "note": "Pfad existiert nicht mehr"
                        })
        except:
            pass
        
        return issues
    
    def _check_version(self, doc: Dict) -> Optional[Dict]:
        """Prüft ob SKILL.md Version mit Registry übereinstimmt"""
        if not doc.get("path"):
            return None
        
        full_path = self.root / doc["path"]
        if not full_path.exists():
            return None
        
        try:
            content = full_path.read_text(encoding='utf-8')
            
            # Extrahiere Version aus SKILL.md
            match = VERSION_PATTERN.search(content[:500])  # Nur Header prüfen
            if match:
                doc_version = match.group(1)
                
                # TODO: Mit skill_registry.json vergleichen
                # Vorerst nur prüfen ob Version vorhanden
                return None
        except:
            pass
        
        return None
    
    def _check_required_sections(self, doc: Dict) -> List[Dict]:
        """Prüft ob Pflicht-Sektionen vorhanden sind"""
        issues = []
        
        if not doc.get("path"):
            return issues
        
        full_path = self.root / doc["path"]
        if not full_path.exists():
            return issues
        
        required_sections = {
            "skill": ["## Übersicht", "## CLI-Befehle", "## Dateien"],
            "readme": ["## Installation", "## Usage"],
            "guide": ["## Einleitung", "## Schritte"],
        }
        
        doc_type = doc.get("doc_type", "")
        if doc_type not in required_sections:
            return issues
        
        try:
            content = full_path.read_text(encoding='utf-8')
            
            for section in required_sections[doc_type]:
                # Flexible Suche (case-insensitive, mit/ohne ##)
                pattern = section.replace("## ", "").lower()
                if pattern not in content.lower():
                    issues.append({
                        "doc_path": doc["path"],
                        "doc_type": doc_type,
                        "missing_section": section,
                        "auto_fixable": False
                    })
        except:
            pass
        
        return issues
    
    def _generate_suggestions(self, results: Dict) -> List[Dict]:
        """Generiert Aktualisierungs-Vorschläge"""
        suggestions = []
        
        # Vorschläge für veraltete Dokumente
        for doc in results["outdated"]:
            if doc["severity"] == "critical":
                suggestions.append({
                    "priority": "high",
                    "action": "review_and_update",
                    "target": doc["path"],
                    "reason": f"Dokument seit {doc['age_days']} Tagen nicht aktualisiert",
                    "suggestion": "Inhalt prüfen und aktualisieren oder als veraltet markieren"
                })
            else:
                suggestions.append({
                    "priority": "medium",
                    "action": "check",
                    "target": doc["path"],
                    "reason": f"Dokument seit {doc['age_days']} Tagen nicht aktualisiert",
                    "suggestion": "Bei nächster Gelegenheit prüfen"
                })
        
        # Vorschläge für ungültige Pfade
        auto_fixable = [p for p in results["invalid_paths"] if p.get("auto_fixable")]
        if auto_fixable:
            suggestions.append({
                "priority": "high",
                "action": "auto_fix_paths",
                "targets": [p["doc_path"] for p in auto_fixable],
                "count": len(auto_fixable),
                "suggestion": f"{len(auto_fixable)} Pfade können automatisch korrigiert werden"
            })
        
        return suggestions
    
    def auto_fix_paths(self, dry_run: bool = True) -> List[Dict]:
        """Korrigiert automatisch veraltete Pfade in Dokumenten"""
        fixed = []
        
        docs = self._get_all_docs()
        
        for doc in docs:
            if not doc.get("path"):
                continue
            
            full_path = self.root / doc["path"]
            if not full_path.exists():
                continue
            
            try:
                content = full_path.read_text(encoding='utf-8')
                original = content
                
                # Ersetze alte Pfade
                for old_path, new_path in PATH_MIGRATIONS.items():
                    if old_path in content:
                        content = content.replace(old_path, new_path)
                
                if content != original:
                    if not dry_run:
                        full_path.write_text(content, encoding='utf-8')
                    
                    fixed.append({
                        "path": doc["path"],
                        "changes": sum(1 for o in PATH_MIGRATIONS if o in original),
                        "applied": not dry_run
                    })
            except Exception as e:
                print(f"[WARN] Fehler bei {doc['path']}: {e}")
        
        return fixed
    
    def update_timestamps(self) -> int:
        """Aktualisiert Zeitstempel-Info (dateibasiert, keine DB noetig)
        
        HINWEIS: Diese Methode ist jetzt ein No-Op da wir keine DB mehr verwenden.
        Die Alters-Pruefung erfolgt direkt bei check_all() per Datei-mtime.
        """
        # Dateibasierte Variante: Nichts zu aktualisieren in DB
        # Stattdessen wird das Alter direkt bei _check_age() ermittelt
        print("[INFO] update_timestamps() ist jetzt no-op (dateibasierte Pruefung)")
        return 0
    
    def generate_report(self, results: Dict = None) -> Path:
        """Erstellt einen Aktualisierungs-Report"""
        if results is None:
            results = self.check_all()
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        report_path = REPORTS_DIR / f"Doc_Update_Report_{timestamp}.md"
        
        # Erstelle Report
        lines = [
            "# Dokumentations-Update Report",
            f"\n**Erstellt:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**Geprüfte Dokumente:** {results['total_docs']}",
            "",
            "---",
            "",
            "## Zusammenfassung",
            "",
            f"| Kategorie | Anzahl |",
            f"|-----------|--------|",
            f"| Veraltet (>{OUTDATED_DAYS} Tage) | {len(results['outdated'])} |",
            f"| Ungültige Pfade | {len(results['invalid_paths'])} |",
            f"| Fehlende Sektionen | {len(results['missing_sections'])} |",
            f"| Vorschläge | {len(results['suggestions'])} |",
            "",
        ]
        
        # Veraltete Dokumente
        if results["outdated"]:
            lines.extend([
                "## Veraltete Dokumente",
                "",
            ])
            
            critical = [d for d in results["outdated"] if d["severity"] == "critical"]
            warning = [d for d in results["outdated"] if d["severity"] == "warning"]
            
            if critical:
                lines.append("### Kritisch (>90 Tage)")
                lines.append("")
                for doc in critical:
                    lines.append(f"- **{doc['path']}** ({doc['age_days']} Tage)")
                lines.append("")
            
            if warning:
                lines.append("### Warnung (>60 Tage)")
                lines.append("")
                for doc in warning:
                    lines.append(f"- {doc['path']} ({doc['age_days']} Tage)")
                lines.append("")
        
        # Ungültige Pfade
        if results["invalid_paths"]:
            lines.extend([
                "## Ungültige Pfade in Dokumenten",
                "",
            ])
            
            auto_fix = [p for p in results["invalid_paths"] if p.get("auto_fixable")]
            manual = [p for p in results["invalid_paths"] if not p.get("auto_fixable")]
            
            if auto_fix:
                lines.append("### Automatisch korrigierbar")
                lines.append("")
                for p in auto_fix:
                    lines.append(f"- `{p['doc_path']}`")
                    lines.append(f"  - `{p['invalid_path']}` → `{p['correct_path']}`")
                lines.append("")
            
            if manual:
                lines.append("### Manuelle Prüfung erforderlich")
                lines.append("")
                for p in manual:
                    lines.append(f"- `{p['doc_path']}`: `{p['invalid_path']}`")
                lines.append("")
        
        # Vorschläge
        if results["suggestions"]:
            lines.extend([
                "## Empfohlene Aktionen",
                "",
            ])
            
            for i, s in enumerate(results["suggestions"], 1):
                priority_emoji = "🔴" if s["priority"] == "high" else "🟡"
                lines.append(f"{i}. {priority_emoji} **{s['action']}**")
                lines.append(f"   - {s['suggestion']}")
                if s.get("target"):
                    lines.append(f"   - Ziel: `{s['target']}`")
                lines.append("")
        
        # Schreibe Report
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_path.write_text("\n".join(lines), encoding='utf-8')
        
        return report_path
    
    def schedule_output(self) -> Dict:
        """Ausgabe für Micro-Routines Integration"""
        results = self.check_all()
        
        output = {
            "has_issues": False,
            "summary": "",
            "actions": []
        }
        
        total_issues = (
            len(results["outdated"]) + 
            len(results["invalid_paths"]) + 
            len(results["missing_sections"])
        )
        
        if total_issues > 0:
            output["has_issues"] = True
            
            parts = []
            if results["outdated"]:
                critical = len([d for d in results["outdated"] if d["severity"] == "critical"])
                if critical:
                    parts.append(f"{critical} kritisch veraltet")
                else:
                    parts.append(f"{len(results['outdated'])} veraltet")
            
            if results["invalid_paths"]:
                parts.append(f"{len(results['invalid_paths'])} ungültige Pfade")
            
            output["summary"] = f"📄 Dokumentation: {', '.join(parts)}"
            
            # Auto-Fix vorschlagen
            auto_fixable = [p for p in results["invalid_paths"] if p.get("auto_fixable")]
            if auto_fixable:
                output["actions"].append({
                    "type": "auto_fix",
                    "command": "python doc_update_checker.py auto-update",
                    "description": f"{len(auto_fixable)} Pfade automatisch korrigieren"
                })
        
        return output


def main():
    parser = argparse.ArgumentParser(description="Documentation Update Checker")
    parser.add_argument('command', nargs='?', default='check',
                        help='Befehl: check, report, auto-update, schedule')
    parser.add_argument('--dry-run', action='store_true', help='Nur simulieren')
    parser.add_argument('--json', action='store_true', help='JSON-Ausgabe')
    
    args = parser.parse_args()
    cmd = args.command.lower()
    checker = DocUpdateChecker()
    
    # === CHECK ===
    if cmd == "check":
        results = checker.check_all()
        
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
            return
        
        print(f"\n{'='*60}")
        print(f"  DOKUMENTATIONS-PRÜFUNG")
        print(f"{'='*60}")
        print(f"  Dokumente geprüft: {results['total_docs']}")
        print(f"  Veraltet:          {len(results['outdated'])}")
        print(f"  Ungültige Pfade:   {len(results['invalid_paths'])}")
        print(f"  Fehlende Sektionen: {len(results['missing_sections'])}")
        print(f"  Vorschläge:        {len(results['suggestions'])}")
        
        if results["outdated"]:
            print(f"\n  ⚠️ VERALTETE DOKUMENTE:")
            for doc in results["outdated"][:5]:
                emoji = "🔴" if doc["severity"] == "critical" else "🟡"
                print(f"    {emoji} {doc['path']} ({doc['age_days']}d)")
            if len(results["outdated"]) > 5:
                print(f"    ... und {len(results['outdated']) - 5} weitere")
        
        if results["suggestions"]:
            print(f"\n  💡 EMPFEHLUNGEN:")
            for s in results["suggestions"][:3]:
                print(f"    - {s['suggestion']}")
    
    # === REPORT ===
    elif cmd == "report":
        report_path = checker.generate_report()
        print(f"\n✅ Report erstellt: {report_path}")
    
    # === AUTO-UPDATE ===
    elif cmd in ["auto-update", "auto-fix"]:
        dry_run = args.dry_run
        
        print(f"\n[AUTO-UPDATE] {'[DRY-RUN]' if dry_run else '[LIVE]'}")
        
        # 1. Pfade korrigieren
        fixed = checker.auto_fix_paths(dry_run=dry_run)
        print(f"  Pfad-Korrekturen: {len(fixed)}")
        
        for f in fixed[:5]:
            status = "würde" if dry_run else "wurde"
            print(f"    - {f['path']} ({f['changes']} Änderungen {status} angewendet)")
        
        # 2. Timestamps aktualisieren
        if not dry_run:
            updated = checker.update_timestamps()
            print(f"  DB-Einträge aktualisiert: {updated}")
        
        print(f"\n✅ Auto-Update {'simuliert' if dry_run else 'abgeschlossen'}")
    
    # === SCHEDULE ===
    elif cmd == "schedule":
        output = checker.schedule_output()
        
        if args.json:
            print(json.dumps(output, ensure_ascii=False))
        else:
            if output["has_issues"]:
                print(output["summary"])
                for action in output["actions"]:
                    print(f"  → {action['description']}")
            else:
                print("✅ Dokumentation aktuell")
    
    # === HELP ===
    elif cmd in ["help", "-h", "--help"]:
        print("""
Documentation Update Checker - Befehle:

  check                 Prüft alle Dokumentationen
  check --json          Prüfung mit JSON-Ausgabe
  
  report                Erstellt Markdown-Report
  
  auto-update           Korrigiert automatisch (Pfade)
  auto-update --dry-run Nur simulieren
  
  schedule              Ausgabe für Micro-Routines
  schedule --json       JSON für automatische Verarbeitung
        """)
    
    else:
        print(f"[ERR] Unbekannter Befehl: {cmd}")


if __name__ == "__main__":
    main()
