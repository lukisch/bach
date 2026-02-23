# SPDX-License-Identifier: MIT
"""
BACH Maintain Handler
=====================
CLI-Handler fuer Wartungs- und Analyse-Tools.

Befehle:
    bach --maintain docs          Dokumentations-Check
    bach --maintain duplicates    Duplikat-Erkennung
    bach --maintain generate      Skill/Agent Generator
    bach --maintain export        Export-Tools
    bach --maintain pattern       Dateinamen-Pattern kuerzen
    bach --maintain scan          System nach CLI-Tools scannen
"""

import sys
import subprocess
from pathlib import Path
from .base import BaseHandler


class MaintainHandler(BaseHandler):
    """Handler fuer --maintain Befehle"""
    
    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.tools_dir = base_path / "tools"
    
    @property
    def profile_name(self) -> str:
        return "maintain"
    
    @property
    def target_file(self) -> Path:
        return self.tools_dir
    
    def get_operations(self) -> dict:
        return {
            "docs": "Dokumentations-Update-Check",
            "duplicates": "Duplikat-Erkennung fuer Tools",
            "generate": "Skill/Agent Generator",
            "export": "Export-Tools (Skill/Agent/OS)",
            "pattern": "Dateinamen-Pattern kuerzen",
            "scan": "System nach CLI-Tools scannen",
            "clean": "Dateien nach Alter/Muster loeschen",
            "json": "JSON-Dateien reparieren",
            "heal": "Pfad-Korrektur und Selbstheilung",
            "registry": "Registry-Konsistenz pruefen",
            "skills": "Skill-Gesundheit pruefen",
            "sync": "Skills mit Datenbank synchronisieren",
            "list": "Verfuegbare Wartungs-Tools anzeigen"
        }
    
    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if not operation or operation == "list":
            return True, self._list_tools()
        
        op = operation.lower()
        
        if op == "docs":
            return self._run_docs_check(args, dry_run)
        elif op == "duplicates":
            return self._run_duplicate_check(args)
        elif op == "generate":
            return self._run_generator(args)
        elif op == "export":
            return self._run_export(args)
        elif op == "pattern":
            return self._run_pattern_tool(args, dry_run)
        elif op == "scan":
            return self._run_tool_scanner(args)
        elif op == "clean":
            return self._run_file_cleaner(args, dry_run)
        elif op == "json":
            return self._run_json_fixer(args, dry_run)
        elif op == "heal":
            return self._run_path_healer(args, dry_run)
        elif op == "registry":
            return self._run_registry_watcher(args)
        elif op == "skills":
            return self._run_skill_health_monitor(args)
        elif op == "sync":
            return self._run_sync_skills(args, dry_run)
        elif op in ["help", "-h"]:
            return True, self._show_help()
        else:
            return False, f"Unbekannter Befehl: {op}\n\n{self._show_help()}"
    
    def _run_docs_check(self, args: list, dry_run: bool) -> tuple:
        """Fuehrt Dokumentations-Check aus."""
        script = self.tools_dir / "doc_update_checker.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        cmd_args = ["check"]
        if dry_run:
            cmd_args.append("--dry-run")
        if args:
            cmd_args.extend(args)
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + cmd_args,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(self.base_path)
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _run_duplicate_check(self, args: list) -> tuple:
        """Fuehrt Duplikat-Check aus."""
        script = self.tools_dir / "duplicate_detector.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        return True, """Duplicate Detector
==================
Dieses Tool benoetigt eine Tool-Registry.

Verwendung:
  from tools.duplicate_detector import DuplicateDetector
  detector = DuplicateDetector(registry)
  result = detector.check_duplicate("neues-tool", "Beschreibung", ["keywords"])

Features:
- Name-Similarity Check
- Keyword-Matching
- Usage-Tracking
- Gap-Analysis

Siehe: tools/duplicate_detector.py"""
    
    def _run_generator(self, args: list) -> tuple:
        """Fuehrt Skill/Agent Generator aus."""
        script = self.tools_dir / "generators" / "skill_generator.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        if not args:
            return True, """Skill Generator
===============
Generiert Skill-Strukturen von MICRO bis EXTENDED.

Verwendung:
  bach --maintain generate <n> [profil] [zielordner]

Profile:
  MICRO    Nur Datei(en), kein Ordnersystem
  LIGHT    Minimale Struktur (SKILL.md + _config + _data)
  STANDARD Standard-Skill mit einfachem Memory
  EXTENDED Komplexer Skill mit Mikro-Skills

Beispiele:
  bach --maintain generate mein-skill STANDARD skills/
  bach --maintain generate analyse MICRO skills/_protocols/

Siehe: tools/generators/skill_generator.py"""
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + args,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _run_export(self, args: list) -> tuple:
        """Fuehrt Export-Tool aus."""
        script = self.tools_dir / "generators" / "exporter.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        if not args:
            return True, """Exporter
========
Export-Tool fuer Skills, Agents und OS.

Befehle:
  skill     Exportiert einen Skill als Standalone
  agent     Exportiert einen Agent mit seinen Skills
  os-fresh  Erstellt ein frisches OS-Paket
  os-reset  Setzt ein OS zurueck

Verwendung:
  bach --maintain export skill <n> --from-os <path>
  bach --maintain export os-fresh <path> --output <zip>

Siehe: tools/generators/exporter.py"""
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + args,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _run_pattern_tool(self, args: list, dry_run: bool) -> tuple:
        """Fuehrt Pattern-Tool aus."""
        script = self.tools_dir / "pattern_tool.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        if not args:
            return True, """Pattern Tool
============
Kuerzt Dateinamen durch Pattern-Erkennung.

Verwendung:
  bach --maintain pattern <ordner> [optionen]

Optionen:
  --dry-run       Nur anzeigen (default)
  --execute       Umbenennungen durchfuehren
  --prefix-only   Nur Prefix-Patterns
  --suffix-only   Nur Suffix-Patterns
  -m <n>          Minimale Pattern-Laenge (default: 3)
  -r              Rekursiv scannen

Beispiele:
  bach --maintain pattern ./docs --dry-run
  bach --maintain pattern ./docs --execute -m 5

Siehe: tools/pattern_tool.py"""
        
        cmd_args = list(args)
        if dry_run and "--execute" not in args:
            cmd_args.append("--dry-run")
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + cmd_args,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _run_tool_scanner(self, args: list) -> tuple:
        """Fuehrt Tool-Scanner aus."""
        script = self.tools_dir / "tool_scanner.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        cmd_args = args if args else ["scan"]
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + cmd_args,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _run_file_cleaner(self, args: list, dry_run: bool) -> tuple:
        """Fuehrt File-Cleaner aus."""
        script = self.tools_dir / "file_cleaner.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        if not args:
            return True, """File Cleaner
============
Dateien nach Alter/Muster bereinigen.

Verwendung:
  bach --maintain clean <ordner> [optionen]

Optionen:
  --age <tage>    Dateien aelter als X Tage
  --keep <n>      Nur N neueste behalten
  --pattern <p>   Datei-Pattern (z.B. "*.log")
  -r              Rekursiv suchen
  --execute       Tatsaechlich loeschen

Beispiele:
  bach --maintain clean ./logs --age 30
  bach --maintain clean ./backups --keep 5 --execute

Siehe: tools/file_cleaner.py"""
        
        cmd_args = list(args)
        if dry_run and "--execute" not in args:
            pass  # Default ist dry-run
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + cmd_args,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _run_json_fixer(self, args: list, dry_run: bool) -> tuple:
        """Fuehrt JSON-Fixer aus."""
        script = self.tools_dir / "json_fixer.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        if not args:
            return True, """JSON Fixer
==========
Repariert kaputte JSON-Dateien.

Verwendung:
  bach --maintain json <datei/ordner> [optionen]

Optionen:
  --dry-run    Nur pruefen (default)
  --execute    Tatsaechlich reparieren
  --backup     Backup vor Aenderung

Repariert:
  - UTF-8 BOM
  - Trailing Commas
  - Single-Quotes
  - PowerShell Newlines

Beispiele:
  bach --maintain json ./config.json
  bach --maintain json ./data --execute --backup

Siehe: tools/json_fixer.py"""
        
        cmd_args = list(args)
        if dry_run and "--execute" not in args:
            cmd_args.append("--dry-run")
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + cmd_args,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _run_path_healer(self, args: list, dry_run: bool) -> tuple:
        """Fuehrt Path-Healer aus."""
        script = self.tools_dir / "path_healer.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        if not args:
            return True, """Path Healer
===========
Korrigiert veraltete Pfade in BACH-Dateien.

Verwendung:
  bach --maintain heal [optionen]

Optionen:
  --dry-run       Nur pruefen, nichts aendern (default)
  --execute       Tatsaechlich korrigieren
  --target <p>    Nur bestimmte Datei pruefen
  --report        Detaillierten Report generieren

Korrigiert:
  - Alte recludOS-Pfade -> BACH_v2_vanilla
  - Alte Skill-Pfade
  - Hub/Handler-Pfade
  - Tools-Verweise

Beispiele:
  bach --maintain heal                   # Dry-run fuer alle
  bach --maintain heal --execute         # Alle korrigieren
  bach --maintain heal --target config.py
  bach --maintain heal --report

Basiert auf: RecludOS Unified Path Healer v2.3.0
Siehe: tools/path_healer.py"""
        
        cmd_args = list(args)
        if dry_run and "--execute" not in args:
            cmd_args.append("--dry-run")
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + cmd_args,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(self.base_path)
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _run_registry_watcher(self, args: list) -> tuple:
        """Fuehrt Registry Watcher aus."""
        script = self.tools_dir / "maintenance" / "registry_watcher.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        if not args:
            args = ["check"]  # Default: Quick-Check
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + list(args),
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.base_path)
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _run_skill_health_monitor(self, args: list) -> tuple:
        """Fuehrt Skill Health Monitor aus."""
        script = self.tools_dir / "maintenance" / "skill_health_monitor.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        if not args:
            args = ["check"]  # Default: Quick-Check
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + list(args),
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.base_path)
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _run_sync_skills(self, args: list, dry_run: bool) -> tuple:
        """Synchronisiert skills/ Dateien mit DB."""
        script = self.tools_dir / "sync_skills.py"
        if not script.exists():
            return False, f"Script nicht gefunden: {script}"
        
        cmd_args = []
        if dry_run or "--dry-run" in args:
            cmd_args.append("--dry-run")
        if "--verbose" in args or "-v" in args:
            cmd_args.append("--verbose")
        
        try:
            result = subprocess.run(
                [sys.executable, str(script)] + cmd_args,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.base_path)
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _list_tools(self) -> str:
        """Listet verfuegbare Wartungs-Tools."""
        lines = []
        lines.append("=" * 50)
        lines.append("WARTUNGS-TOOLS")
        lines.append("=" * 50)
        lines.append("")
        lines.append("Verfuegbare Befehle:")
        lines.append("")
        lines.append("  docs        Dokumentations-Update-Check")
        lines.append("              Erkennt veraltete Dokumente (>60 Tage)")
        lines.append("")
        lines.append("  duplicates  Duplikat-Erkennung")
        lines.append("              Verhindert Tool-Duplikate")
        lines.append("")
        lines.append("  generate    Skill/Agent Generator")
        lines.append("              Erstellt neue Skill-Strukturen")
        lines.append("")
        lines.append("  export      Export-Tools")
        lines.append("              Exportiert Skills/Agents/OS")
        lines.append("")
        lines.append("  pattern     Pattern-Tool")
        lines.append("              Kuerzt Dateinamen durch Pattern-Erkennung")
        lines.append("")
        lines.append("  scan        Tool-Scanner")
        lines.append("              Findet installierte CLI-Tools")
        lines.append("")
        lines.append("  clean       File-Cleaner")
        lines.append("              Loescht Dateien nach Alter/Muster")
        lines.append("")
        lines.append("  json        JSON-Fixer")
        lines.append("              Repariert kaputte JSON-Dateien")
        lines.append("")
        lines.append("  heal        Path-Healer")
        lines.append("              Korrigiert veraltete Pfade")
        lines.append("")
        lines.append("  registry    Registry-Watcher")
        lines.append("              Prueft DB/JSON-Konsistenz")
        lines.append("")
        lines.append("  skills      Skill-Health-Monitor")
        lines.append("              Prueft Skills/Agenten-Zustand")
        lines.append("")
        lines.append("Verwendung: bach --maintain <befehl> [optionen]")
        
        return "\n".join(lines)
    
    def _show_help(self) -> str:
        """Zeigt Hilfe."""
        return """BACH Maintain - Wartungs-Tools
==============================

Befehle:
  bach --maintain docs [--dry-run]    Dokumentations-Check
  bach --maintain duplicates          Duplikat-Info
  bach --maintain generate <args>     Skill Generator
  bach --maintain export <args>       Export-Tool
  bach --maintain pattern <ordner>    Pattern-Tool
  bach --maintain scan                Tool-Scanner
  bach --maintain clean <ordner>      File-Cleaner
  bach --maintain json <pfad>         JSON-Fixer
  bach --maintain heal                Path-Healer
  bach --maintain registry            Registry-Konsistenz
  bach --maintain skills              Skill-Gesundheit
  bach --maintain list                Tools anzeigen

Beispiele:
  bach --maintain docs                # Doku pruefen
  bach --maintain heal                # Pfade korrigieren
  bach --maintain registry report     # Detaillierter Registry-Report
  bach --maintain skills check        # Skill-Health Check
  bach --maintain clean ./logs --age 30

Tools (11):
  tools/doc_update_checker.py
  tools/duplicate_detector.py
  tools/generators/skill_generator.py
  tools/generators/exporter.py
  tools/pattern_tool.py
  tools/tool_scanner.py
  tools/file_cleaner.py
  tools/json_fixer.py
  tools/path_healer.py"""
