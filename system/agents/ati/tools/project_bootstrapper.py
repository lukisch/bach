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
ATI Project Bootstrapper v1.0.0
===============================

Automatisches Onboarding neuer Softwareprojekte mit BACH-Policies,
Git-Strukturvorlagen und wiederverwendbaren Modulen.

Erstellt: 2026-01-22
Konzept: agents/ati/ATI_PROJECT_BOOTSTRAPPING.md

Klassen:
- ProjectBootstrapper: Hauptorchestrator
- TemplateEngine: Generiert Projektstrukturen
- PolicyApplier: Wendet BACH-Policies an
- ModuleInjector: Injiziert wiederverwendbare Module
- StructureMigrator: Migriert bestehende Projekte
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

# BACH Root ermitteln
BACH_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(BACH_ROOT))

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ATI.Bootstrapper")


# ==============================================================================
# KONFIGURATION
# ==============================================================================

@dataclass
class BootstrapConfig:
    """Konfiguration für Bootstrap-Operationen."""
    
    default_template: str = "python-cli"
    default_modules: List[str] = field(default_factory=lambda: ["path_healer", "encoding"])
    default_policies: List[str] = field(default_factory=lambda: ["naming", "encoding"])
    
    templates_path: Path = field(default_factory=lambda: BACH_ROOT / "agents/ati/templates")
    modules_path: Path = field(default_factory=lambda: BACH_ROOT / "agents/ati/_modules")
    policies_path: Path = field(default_factory=lambda: BACH_ROOT / "agents/ati/_policies")
    
    create_onboarding_tasks: bool = True
    onboarding_tasks: List[str] = field(default_factory=lambda: [
        "SKILL.md anpassen",
        "config.json konfigurieren",
        "Erste Funktion implementieren",
        "README mit Projektbeschreibung ergaenzen"
    ])
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> 'BootstrapConfig':
        """Lädt Konfiguration aus JSON oder verwendet Defaults."""
        if config_path and config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls()


# ==============================================================================
# TEMPLATE ENGINE
# ==============================================================================

class TemplateEngine:
    """
    Generiert Projektstrukturen aus Templates.
    
    Nutzt intern structure_generator.py für Basis-Funktionalität.
    
    Templates:
    - python-cli: Python CLI-Projekt
    - python-api: Python API-Projekt
    - llm-skill: LLM Skill (BACH-konform)
    - llm-agent: LLM Agent (BACH-konform)
    - generic: Universelles Projekt
    """
    
    SUPPORTED_TEMPLATES = [
        "python-cli",
        "python-api", 
        "llm-skill",
        "llm-agent",
        "llm-os",
        "generic"
    ]
    
    def __init__(self, templates_path: Path):
        self.templates_path = templates_path
        self._templates_cache: Dict[str, Dict] = {}
        
    def list_templates(self) -> List[str]:
        """Listet alle verfügbaren Templates."""
        available = []
        for template in self.SUPPORTED_TEMPLATES:
            template_dir = self.templates_path / template
            if template_dir.exists():
                available.append(template)
        return available
    
    def load_template(self, template_name: str) -> Dict[str, Any]:
        """Lädt ein Template aus dem Cache oder Dateisystem."""
        if template_name in self._templates_cache:
            return self._templates_cache[template_name]
        
        template_dir = self.templates_path / template_name
        if not template_dir.exists():
            raise ValueError(f"Template '{template_name}' nicht gefunden: {template_dir}")
        
        # Template-Struktur laden (structure.json oder scannen)
        structure_file = template_dir / "structure.json"
        if structure_file.exists():
            with open(structure_file, 'r', encoding='utf-8') as f:
                template = json.load(f)
        else:
            template = self._scan_template_structure(template_dir)
        
        self._templates_cache[template_name] = template
        return template
    
    def _scan_template_structure(self, template_dir: Path) -> Dict[str, Any]:
        """Scannt Template-Verzeichnis und erstellt Struktur."""
        structure = {
            "name": template_dir.name,
            "directories": [],
            "files": []
        }
        
        for item in template_dir.rglob("*"):
            rel_path = item.relative_to(template_dir)
            # Ignoriere __pycache__ und .git
            if "__pycache__" in str(rel_path) or ".git" in str(rel_path):
                continue
            if item.is_dir():
                structure["directories"].append(str(rel_path))
            elif item.is_file() and item.name != "structure.json":
                structure["files"].append({
                    "path": str(rel_path),
                    "template": item.name
                })
        
        return structure
    
    def generate_structure(
        self, 
        project_name: str, 
        target_path: Path, 
        template_name: str = "python-cli",
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Generiert Projektstruktur aus Template.
        
        Args:
            project_name: Name des neuen Projekts
            target_path: Zielverzeichnis
            template_name: Name des Templates
            description: Projektbeschreibung für Variablen
            
        Returns:
            Dict mit erstellten Dateien und Verzeichnissen
        """
        logger.info(f"Generiere Struktur: {project_name} (Template: {template_name})")
        
        result = {
            "project_name": project_name,
            "target_path": str(target_path),
            "template": template_name,
            "created_dirs": [],
            "created_files": [],
            "errors": [],
            "status": "pending"
        }
        
        try:
            # Template laden
            template = self.load_template(template_name)
            
            # Variablen für Ersetzung
            variables = {
                "project_name": project_name,
                "PROJECT_NAME": project_name.upper().replace("-", "_"),
                "description": description or f"{project_name} - A BACH-powered project"
            }
            
            # Projekt-Root erstellen
            if not target_path.exists():
                target_path.mkdir(parents=True, exist_ok=True)
                result["created_dirs"].append(str(target_path))
            
            # Verzeichnisse erstellen
            for dir_template in template.get("directories", []):
                # Variablen ersetzen
                dir_path = dir_template.format(**{k: v for k, v in variables.items()})
                full_path = target_path / dir_path
                
                if not full_path.exists():
                    full_path.mkdir(parents=True, exist_ok=True)
                    result["created_dirs"].append(str(full_path))
                    logger.debug(f"  Erstellt: {full_path}")
            
            # Dateien erstellen
            for file_spec in template.get("files", []):
                file_path_template = file_spec.get("path", "")
                file_path = file_path_template.format(**{k: v for k, v in variables.items()})
                full_path = target_path / file_path
                
                # Übergeordnetes Verzeichnis sicherstellen
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    content = self._resolve_file_content(file_spec, template_name, variables)
                    
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    result["created_files"].append(str(full_path))
                    logger.debug(f"  Erstellt: {full_path}")
                    
                except Exception as e:
                    result["errors"].append({
                        "file": str(full_path),
                        "error": str(e)
                    })
            
            result["status"] = "completed" if not result["errors"] else "partial"
            
        except Exception as e:
            logger.error(f"Struktur-Generierung fehlgeschlagen: {e}")
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _resolve_file_content(
        self, 
        file_spec: Dict[str, Any], 
        template_name: str,
        variables: Dict[str, str]
    ) -> str:
        """
        Löst Datei-Inhalt auf (content direkt oder aus Template).
        
        Args:
            file_spec: Datei-Spezifikation (content oder template)
            template_name: Name des aktiven Templates
            variables: Variablen für Ersetzung
            
        Returns:
            Aufgelöster Dateiinhalt
        """
        # Direkter Content
        if "content" in file_spec:
            content = file_spec["content"]
            # Variablen-Ersetzung mit ${var} Syntax
            for key, value in variables.items():
                content = content.replace(f"${{{key}}}", value)
            return content
        
        # Template-Datei laden
        if "template" in file_spec:
            template_file = self.templates_path / template_name / file_spec["template"]
            
            if template_file.exists():
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Variablen-Ersetzung
                for key, value in variables.items():
                    content = content.replace(f"${{{key}}}", value)
                    content = content.replace(f"{{{key}}}", value)
                return content
            else:
                # Template-Datei fehlt -> Platzhalter
                return f"# TODO: Template '{file_spec['template']}' nicht gefunden\n"
        
        return ""


# ==============================================================================
# POLICY APPLIER
# ==============================================================================

class PolicyApplier:
    """
    Wendet BACH-Policies auf Projekte an.
    
    Policies:
    - naming: Naming Convention (kebab-case, snake_case)
    - encoding: UTF-8 ohne BOM
    - path_rules: Pfad-Regeln
    - tier_classification: Tier-System
    """
    
    SUPPORTED_POLICIES = [
        "naming",
        "encoding",
        "path_rules",
        "tier_classification"
    ]
    
    def __init__(self, policies_path: Path):
        self.policies_path = policies_path
        self._policies_cache: Dict[str, Dict] = {}
        
    def list_policies(self) -> List[str]:
        """Listet alle verfügbaren Policies."""
        return [p for p in self.SUPPORTED_POLICIES 
                if (self.policies_path / f"{p}.md").exists() or
                   (self.policies_path / f"{p}.json").exists()]
    
    def load_policy(self, policy_name: str) -> Dict[str, Any]:
        """Lädt eine Policy-Definition."""
        if policy_name in self._policies_cache:
            return self._policies_cache[policy_name]
        
        # Versuche JSON, dann MD
        json_path = self.policies_path / f"{policy_name}.json"
        md_path = self.policies_path / f"{policy_name}.md"
        
        policy = {"name": policy_name, "rules": {}}
        
        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                policy = json.load(f)
        elif md_path.exists():
            # MD-Datei als Text laden
            with open(md_path, 'r', encoding='utf-8') as f:
                policy["content"] = f.read()
        
        self._policies_cache[policy_name] = policy
        return policy
    
    def check_compliance(self, project_path: Path, policies: List[str]) -> Dict[str, Any]:
        """
        Prüft Policy-Compliance eines Projekts.
        
        Returns:
            Dict mit Compliance-Status pro Policy
        """
        logger.info(f"Prüfe Compliance: {project_path}")
        
        # TODO: Implementierung in Phase 3
        return {
            "project": str(project_path),
            "policies": policies,
            "compliant": True,
            "violations": []
        }
    
    def apply_policies(
        self, 
        project_path: Path, 
        policies: List[str],
        dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        Wendet Policies auf ein Projekt an.
        
        Args:
            project_path: Pfad zum Projekt
            policies: Liste der anzuwendenden Policies
            dry_run: Nur prüfen, nicht ändern
            
        Returns:
            Dict mit angewendeten Änderungen
        """
        logger.info(f"Wende Policies an: {policies} (dry_run={dry_run})")
        
        # TODO: Implementierung in Phase 3
        return {
            "project": str(project_path),
            "policies": policies,
            "dry_run": dry_run,
            "changes": [],
            "status": "pending"
        }


# ==============================================================================
# MODULE INJECTOR
# ==============================================================================

class ModuleInjector:
    """
    Injiziert wiederverwendbare Module in Projekte.
    
    Module:
    - path_healer: Pfad-Selbstheilung (von RecludOS)
    - distribution: Tier-System, Siegel
    - encoding: UTF-8, BOM-Handling
    - backup: Snapshot, Restore
    - validation: Schema-Validierung
    """
    
    SUPPORTED_MODULES = [
        "path_healer",
        "distribution",
        "encoding",
        "backup",
        "validation"
    ]
    
    def __init__(self, modules_path: Path):
        self.modules_path = modules_path
        
    def list_modules(self) -> List[Dict[str, str]]:
        """Listet alle verfügbaren Module mit Beschreibung."""
        modules = []
        for module_name in self.SUPPORTED_MODULES:
            module_path = self.modules_path / f"{module_name}.py"
            modules.append({
                "name": module_name,
                "path": str(module_path),
                "available": module_path.exists()
            })
        return modules
    
    def inject_module(
        self,
        module_name: str,
        project_path: Path,
        target_dir: str = "_modules"
    ) -> Dict[str, Any]:
        """
        Injiziert ein Modul in ein Projekt.
        
        Args:
            module_name: Name des Moduls
            project_path: Pfad zum Projekt
            target_dir: Ziel-Unterordner (default: _modules)
            
        Returns:
            Dict mit Injektions-Details
        """
        logger.info(f"Injiziere Modul: {module_name} -> {project_path}")
        
        source = self.modules_path / f"{module_name}.py"
        target = project_path / target_dir / f"{module_name}.py"
        
        result = {
            "module": module_name,
            "source": str(source),
            "target": str(target),
            "status": "pending"
        }
        
        if not source.exists():
            result["status"] = "error"
            result["error"] = f"Modul nicht gefunden: {source}"
            return result
        
        try:
            # Ziel-Verzeichnis erstellen falls nötig
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # Modul kopieren
            shutil.copy2(source, target)
            
            # Optional: __init__.py erstellen falls nicht vorhanden
            init_file = target.parent / "__init__.py"
            if not init_file.exists():
                init_file.write_text(
                    f'# Auto-generated by ATI Project Bootstrapper\n'
                    f'# Modules: {module_name}\n',
                    encoding='utf-8'
                )
                result["init_created"] = str(init_file)
            
            result["status"] = "completed"
            result["copied_at"] = datetime.now().isoformat()
            logger.info(f"  [OK] Modul kopiert: {target}")
            
        except PermissionError as e:
            result["status"] = "error"
            result["error"] = f"Zugriff verweigert: {e}"
            logger.error(f"  [FAIL] Zugriff verweigert: {e}")
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.error(f"  [FAIL] Fehler: {e}")
        
        return result
    
    def inject_all(
        self,
        modules: List[str],
        project_path: Path,
        target_dir: str = "_modules"
    ) -> List[Dict[str, Any]]:
        """Injiziert mehrere Module."""
        results = []
        for module_name in modules:
            result = self.inject_module(module_name, project_path, target_dir)
            results.append(result)
        return results


# ==============================================================================
# STRUCTURE MIGRATOR
# ==============================================================================

class StructureMigrator:
    """
    Migriert bestehende Projekte auf BACH-Strukturvorgaben.
    
    Workflow:
    1. Analyse: Vergleich mit Ziel-Template
    2. Backup: Snapshot vor Migration
    3. Migration: Struktur anpassen
    4. Validierung: Ergebnis prüfen
    """
    
    def __init__(self, template_engine: TemplateEngine):
        self.template_engine = template_engine
        
    def analyze(self, project_path: Path, target_template: str = "llm-skill") -> Dict[str, Any]:
        """
        Analysiert ein bestehendes Projekt und vergleicht mit Template.
        
        Prüft:
        - Fehlende Verzeichnisse aus Template
        - Fehlende Pflicht-Dateien (SKILL.md, README.md, etc.)
        - Naming-Convention-Verstöße
        
        Returns:
            Dict mit Analyse-Ergebnis inkl. missing_dirs, missing_files, rename_suggestions
        """
        logger.info(f"Analysiere Projekt: {project_path}")
        
        result = {
            "project": str(project_path),
            "target_template": target_template,
            "missing_dirs": [],
            "missing_files": [],
            "rename_suggestions": [],
            "existing_structure": {"dirs": [], "files": []},
            "compliance_score": 0,
            "status": "pending"
        }
        
        if not project_path.exists():
            result["status"] = "error"
            result["error"] = f"Projekt nicht gefunden: {project_path}"
            return result
        
        try:
            # 1. Template laden
            template = self.template_engine.load_template(target_template)
            template_dirs = set(template.get("directories", []))
            template_files = set(f.get("path", "") for f in template.get("files", []))
            
            # 2. Existierende Struktur scannen
            existing_dirs = set()
            existing_files = set()
            
            for item in project_path.rglob("*"):
                rel_path = str(item.relative_to(project_path))
                # Ignoriere __pycache__, .git, node_modules
                if any(ignore in rel_path for ignore in ["__pycache__", ".git", "node_modules", ".pyc"]):
                    continue
                if item.is_dir():
                    existing_dirs.add(rel_path)
                elif item.is_file():
                    existing_files.add(rel_path)
            
            result["existing_structure"]["dirs"] = sorted(existing_dirs)
            result["existing_structure"]["files"] = sorted(existing_files)[:50]  # Limitiert
            
            # 3. Fehlende Verzeichnisse ermitteln
            for template_dir in template_dirs:
                # Variablen wie {project_name} erstmal ignorieren
                check_dir = template_dir
                if "{" in template_dir:
                    continue  # Variable Pfade überspringen
                if check_dir not in existing_dirs:
                    result["missing_dirs"].append(check_dir)
            
            # 4. Fehlende Pflicht-Dateien prüfen
            required_files = ["SKILL.md", "README.md", "CHANGELOG.md"]
            for req_file in required_files:
                if req_file not in existing_files and not any(req_file in f for f in existing_files):
                    result["missing_files"].append(req_file)
            
            # 5. Naming-Convention prüfen (kebab-case für Dateien)
            import re
            kebab_pattern = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z]+)?$')
            underscore_dirs = ["_config", "_data", "_memory", "_modules", "_policies"]
            
            for file_path in existing_files:
                filename = Path(file_path).name
                # Ignoriere spezielle Dateien
                if filename.startswith(".") or filename.startswith("__"):
                    continue
                # Großbuchstaben in Dateinamen (außer SKILL.md, README.md, etc.)
                if filename.isupper() or filename in ["SKILL.md", "README.md", "CHANGELOG.md", "LICENSE"]:
                    continue
                # Leerzeichen oder Sonderzeichen
                if " " in filename or any(c in filename for c in ["ä", "ö", "ü", "ß"]):
                    suggested = filename.lower().replace(" ", "-")
                    suggested = suggested.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
                    result["rename_suggestions"].append({
                        "current": file_path,
                        "suggested": str(Path(file_path).parent / suggested),
                        "reason": "Naming Convention (kebab-case, keine Umlaute)"
                    })
            
            # 6. Compliance Score berechnen
            total_checks = len(template_dirs) + len(required_files) + 1
            passed_checks = (
                len(template_dirs) - len(result["missing_dirs"]) +
                len(required_files) - len(result["missing_files"])
            )
            # Bonus für _modules und _policies
            if "_modules" in existing_dirs:
                passed_checks += 0.5
            if "_policies" in existing_dirs:
                passed_checks += 0.5
            
            result["compliance_score"] = round(passed_checks / max(total_checks, 1) * 100, 1)
            result["status"] = "analyzed"
            
            logger.info(f"  Compliance: {result['compliance_score']}%")
            logger.info(f"  Fehlend: {len(result['missing_dirs'])} Dirs, {len(result['missing_files'])} Files")
            
        except Exception as e:
            logger.error(f"Analyse fehlgeschlagen: {e}")
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def migrate(
        self,
        project_path: Path,
        target_template: str = "llm-skill",
        dry_run: bool = True,
        create_backup: bool = True
    ) -> Dict[str, Any]:
        """
        Migriert ein bestehendes Projekt auf BACH-Strukturvorgaben.
        
        Workflow:
        1. Analyse durchführen (missing_dirs, missing_files, rename_suggestions)
        2. Backup erstellen (optional, empfohlen)
        3. Fehlende Verzeichnisse anlegen
        4. Fehlende Pflicht-Dateien erstellen
        5. Renames durchführen (optional)
        
        Args:
            project_path: Pfad zum Projekt
            target_template: Ziel-Template
            dry_run: Nur prüfen, nicht ändern
            create_backup: Backup vor Migration erstellen
            
        Returns:
            Dict mit Migration-Details inkl. created_dirs, created_files, renamed, backup_path
        """
        logger.info(f"Migriere: {project_path} -> {target_template} (dry_run={dry_run})")
        
        result = {
            "project": str(project_path),
            "target_template": target_template,
            "dry_run": dry_run,
            "analysis": None,
            "backup_path": None,
            "created_dirs": [],
            "created_files": [],
            "renamed": [],
            "skipped": [],
            "errors": [],
            "status": "pending"
        }
        
        # Schritt 1: Analyse durchführen
        analysis = self.analyze(project_path, target_template)
        result["analysis"] = analysis
        
        if analysis.get("status") == "error":
            result["status"] = "error"
            result["error"] = analysis.get("error", "Analyse fehlgeschlagen")
            return result
        
        # Nichts zu tun?
        if (not analysis.get("missing_dirs") and 
            not analysis.get("missing_files") and 
            not analysis.get("rename_suggestions")):
            result["status"] = "no_changes_needed"
            result["message"] = f"Projekt bereits konform ({analysis.get('compliance_score', 0)}% Compliance)"
            return result
        
        # Dry-Run: Nur zeigen was passieren würde
        if dry_run:
            result["would_create_dirs"] = analysis.get("missing_dirs", [])
            result["would_create_files"] = analysis.get("missing_files", [])
            result["would_rename"] = analysis.get("rename_suggestions", [])
            result["status"] = "dry_run_complete"
            return result
        
        try:
            # Schritt 2: Backup erstellen
            if create_backup:
                backup_dir = project_path.parent / f"{project_path.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copytree(project_path, backup_dir, dirs_exist_ok=True)
                result["backup_path"] = str(backup_dir)
                logger.info(f"  Backup erstellt: {backup_dir}")
            
            # Schritt 3: Fehlende Verzeichnisse anlegen
            for dir_path in analysis.get("missing_dirs", []):
                full_path = project_path / dir_path
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    result["created_dirs"].append(str(dir_path))
                    logger.info(f"  [DIR] Erstellt: {dir_path}")
                except Exception as e:
                    result["errors"].append({"path": dir_path, "error": str(e)})
            
            # Schritt 4: Fehlende Pflicht-Dateien erstellen
            file_templates = {
                "SKILL.md": self._generate_skill_md(project_path.name),
                "README.md": self._generate_readme_md(project_path.name),
                "CHANGELOG.md": self._generate_changelog_md(project_path.name)
            }
            
            for file_name in analysis.get("missing_files", []):
                full_path = project_path / file_name
                try:
                    if file_name in file_templates:
                        content = file_templates[file_name]
                    else:
                        content = f"# {file_name}\n\n<!-- TODO: Inhalt ergänzen -->\n"
                    
                    full_path.write_text(content, encoding='utf-8')
                    result["created_files"].append(file_name)
                    logger.info(f"  [FILE] Erstellt: {file_name}")
                except Exception as e:
                    result["errors"].append({"path": file_name, "error": str(e)})
            
            # Schritt 5: Renames (nur bei expliziter Anforderung - hier übersprungen)
            # Renames sind riskant und sollten manuell geprüft werden
            for rename in analysis.get("rename_suggestions", []):
                result["skipped"].append({
                    "action": "rename",
                    "from": rename.get("current"),
                    "to": rename.get("suggested"),
                    "reason": "Automatische Renames deaktiviert - manuell prüfen"
                })
            
            # Status bestimmen
            if result["errors"]:
                result["status"] = "partial"
            else:
                result["status"] = "completed"
            
            # Neue Compliance berechnen
            new_analysis = self.analyze(project_path, target_template)
            result["new_compliance_score"] = new_analysis.get("compliance_score", 0)
            
            logger.info(f"  Migration abgeschlossen: {result['status']}")
            logger.info(f"  Neue Compliance: {result['new_compliance_score']}%")
            
        except Exception as e:
            logger.error(f"Migration fehlgeschlagen: {e}")
            result["status"] = "error"
            result["error"] = str(e)
            
            # Rollback bei Fehler (wenn Backup existiert)
            if result.get("backup_path") and Path(result["backup_path"]).exists():
                result["rollback_available"] = True
                result["rollback_hint"] = f"Backup verfügbar: {result['backup_path']}"
        
        return result
    
    def _generate_skill_md(self, project_name: str) -> str:
        """Generiert Template für SKILL.md."""
        return f'''---
name: {project_name}
version: 0.1.0
description: TODO - Beschreibung ergänzen
last_updated: {datetime.now().strftime('%Y-%m-%d')}
---

# {project_name}

## Übersicht

<!-- TODO: Kurzbeschreibung -->

## Quick Start

```bash
# TODO: Nutzungsbeispiele
```

## Funktionen

<!-- TODO: Features dokumentieren -->

## Changelog

Siehe [CHANGELOG.md](CHANGELOG.md)
'''

    def _generate_readme_md(self, project_name: str) -> str:
        """Generiert Template für README.md."""
        return f'''# {project_name}

> TODO: Kurze Beschreibung

## Installation

```bash
# TODO: Installationsanleitung
```

## Verwendung

```bash
# TODO: Nutzungsbeispiele
```

## Lizenz

<!-- TODO: Lizenz ergänzen -->
'''

    def _generate_changelog_md(self, project_name: str) -> str:
        """Generiert Template für CHANGELOG.md."""
        return f'''# Changelog - {project_name}

Alle wichtigen Änderungen werden hier dokumentiert.

## [0.1.0] - {datetime.now().strftime('%Y-%m-%d')}

### Hinzugefügt
- Initiale Version
- BACH-Struktur angewendet via ATI Project Bootstrapper
'''


# ==============================================================================
# MAIN ORCHESTRATOR
# ==============================================================================

class ProjectBootstrapper:
    """
    Hauptorchestrator für ATI Project Bootstrapping.
    
    Koordiniert:
    - TemplateEngine für Struktur-Generierung
    - PolicyApplier für BACH-Policies
    - ModuleInjector für wiederverwendbare Module
    - StructureMigrator für bestehende Projekte
    
    Usage:
        bootstrapper = ProjectBootstrapper()
        
        # Neues Projekt erstellen
        result = bootstrapper.bootstrap(
            name="my-tool",
            template="python-cli",
            target_path=Path("/projects")
        )
        
        # Bestehendes Projekt migrieren
        result = bootstrapper.migrate(
            project_path=Path("/projects/legacy-tool"),
            target_template="llm-skill"
        )
    """
    
    def __init__(self, config: Optional[BootstrapConfig] = None):
        self.config = config or BootstrapConfig.load()
        
        self.template_engine = TemplateEngine(self.config.templates_path)
        self.policy_applier = PolicyApplier(self.config.policies_path)
        self.module_injector = ModuleInjector(self.config.modules_path)
        self.structure_migrator = StructureMigrator(self.template_engine)
        
        logger.info("ProjectBootstrapper initialisiert")
        
    def bootstrap(
        self,
        name: str,
        template: str = "python-cli",
        target_path: Optional[Path] = None,
        modules: Optional[List[str]] = None,
        policies: Optional[List[str]] = None,
        init_git: bool = True,
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Erstellt ein neues Projekt mit BACH-Policies und Modulen.
        
        Args:
            name: Projektname
            template: Template-Name (python-cli, llm-skill, etc.)
            target_path: Zielverzeichnis (default: aktuelles Verzeichnis)
            modules: Module zum Injizieren (default: aus Config)
            policies: Anzuwendende Policies (default: aus Config)
            init_git: Git-Repository initialisieren
            description: Projektbeschreibung
            
        Returns:
            Dict mit Bootstrap-Ergebnis
        """
        logger.info(f"Bootstrap: {name} (template={template})")
        
        modules = modules or self.config.default_modules
        policies = policies or self.config.default_policies
        target_path = target_path or Path.cwd()
        project_path = target_path / name
        
        result = {
            "name": name,
            "template": template,
            "project_path": str(project_path),
            "modules": modules,
            "policies": policies,
            "steps": [],
            "status": "pending"
        }
        
        try:
            # Schritt 1: Struktur generieren
            structure_result = self.template_engine.generate_structure(
                name, project_path, template, description
            )
            result["steps"].append({"step": "structure", "result": structure_result})
            
            # Schritt 2: Module injizieren
            modules_result = self.module_injector.inject_all(
                modules, project_path
            )
            result["steps"].append({"step": "modules", "result": modules_result})
            
            # Schritt 3: Policies anwenden
            policies_result = self.policy_applier.apply_policies(
                project_path, policies, dry_run=False
            )
            result["steps"].append({"step": "policies", "result": policies_result})
            
            # Schritt 4: Git initialisieren (optional)
            if init_git:
                # TODO: Git-Initialisierung
                result["steps"].append({"step": "git", "result": {"status": "pending"}})
            
            result["status"] = "completed"
            
        except Exception as e:
            logger.error(f"Bootstrap fehlgeschlagen: {e}")
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def migrate(
        self,
        project_path: Path,
        target_template: str = "llm-skill",
        modules: Optional[List[str]] = None,
        policies: Optional[List[str]] = None,
        dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        Migriert ein bestehendes Projekt auf BACH-Strukturvorgaben.
        
        Args:
            project_path: Pfad zum bestehenden Projekt
            target_template: Ziel-Template
            modules: Module zum Hinzufügen
            policies: Anzuwendende Policies
            dry_run: Nur prüfen, nicht ändern
            
        Returns:
            Dict mit Migration-Ergebnis
        """
        logger.info(f"Migrate: {project_path} (dry_run={dry_run})")
        
        return self.structure_migrator.migrate(
            project_path, target_template, dry_run
        )
    
    def analyze(self, project_path: Path, target_template: str = "llm-skill") -> Dict[str, Any]:
        """Analysiert ein Projekt ohne Änderungen."""
        return self.structure_migrator.analyze(project_path, target_template)


# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def main():
    """CLI Entry-Point für direkten Aufruf."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ATI Project Bootstrapper - Neue Projekte mit BACH-Policies erstellen"
    )
    subparsers = parser.add_subparsers(dest="command", help="Befehle")
    
    # bootstrap
    bp = subparsers.add_parser("bootstrap", help="Neues Projekt erstellen")
    bp.add_argument("name", help="Projektname")
    bp.add_argument("--template", "-t", default="python-cli", 
                    choices=TemplateEngine.SUPPORTED_TEMPLATES,
                    help="Template (default: python-cli)")
    bp.add_argument("--path", "-p", type=Path, help="Zielverzeichnis")
    bp.add_argument("--modules", "-m", nargs="+", help="Module zum Injizieren")
    bp.add_argument("--policies", nargs="+", help="Policies anzuwenden")
    bp.add_argument("--no-git", action="store_true", help="Kein Git initialisieren")
    
    # migrate
    mg = subparsers.add_parser("migrate", help="Bestehendes Projekt migrieren")
    mg.add_argument("path", type=Path, help="Pfad zum Projekt")
    mg.add_argument("--template", "-t", default="llm-skill", help="Ziel-Template")
    mg.add_argument("--dry-run", "-n", action="store_true", help="Nur prüfen")
    mg.add_argument("--execute", action="store_true", help="Migration ausführen")
    
    # analyze
    an = subparsers.add_parser("analyze", help="Projekt analysieren")
    an.add_argument("path", type=Path, help="Pfad zum Projekt")
    an.add_argument("--template", "-t", default="llm-skill", help="Vergleichs-Template")
    
    # modules
    mo = subparsers.add_parser("modules", help="Module verwalten")
    mo.add_argument("action", choices=["list", "add", "update"])
    mo.add_argument("--module", "-m", help="Modul-Name")
    mo.add_argument("--project", "-p", type=Path, help="Projekt-Pfad")
    
    # policies
    po = subparsers.add_parser("policies", help="Policies verwalten")
    po.add_argument("action", choices=["list", "check", "apply"])
    po.add_argument("--project", "-p", type=Path, help="Projekt-Pfad")
    po.add_argument("--policy", nargs="+", help="Policy-Namen")
    
    args = parser.parse_args()
    
    bootstrapper = ProjectBootstrapper()
    
    if args.command == "bootstrap":
        result = bootstrapper.bootstrap(
            name=args.name,
            template=args.template,
            target_path=args.path,
            modules=args.modules,
            policies=args.policies,
            init_git=not args.no_git
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif args.command == "migrate":
        dry_run = not args.execute
        result = bootstrapper.migrate(
            project_path=args.path,
            target_template=args.template,
            dry_run=dry_run
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif args.command == "analyze":
        result = bootstrapper.analyze(args.path, args.template)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif args.command == "modules":
        if args.action == "list":
            modules = bootstrapper.module_injector.list_modules()
            for m in modules:
                status = "[OK]" if m["available"] else "[--]"
                print(f"  {status} {m['name']}")
        elif args.action == "add" and args.module and args.project:
            result = bootstrapper.module_injector.inject_module(
                args.module, args.project
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
    elif args.command == "policies":
        if args.action == "list":
            policies = bootstrapper.policy_applier.list_policies()
            for p in policies:
                print(f"  - {p}")
        elif args.action == "check" and args.project:
            policies = args.policy or bootstrapper.config.default_policies
            result = bootstrapper.policy_applier.check_compliance(
                args.project, policies
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
