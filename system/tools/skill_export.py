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
Tool: skill_export
Version: 1.0.0
Author: BACH Team
Created: 2026-02-08
Updated: 2026-02-08
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version skill_export

skill_export.py - Skill-Export mit Dependency Resolution
=========================================================

Exportiert einen BACH-Skill als autarkes Paket mit allen Abhaengigkeiten.

Skills koennen sich auf BACH-Ressourcen stuetzen solange sie Teil des Systems sind.
Erst beim Export muessen alle Abhaengigkeiten gebuendelt werden, einschliesslich
Services aus hub/_services/.

Usage:
    python skill_export.py --skill <name> [--dry-run] [--output <dir>]

    Oder via BACH CLI:
    bach skill export <name> [--dry-run] [--output <dir>]

Features:
    - Liest SKILL.md YAML-Header fuer deklarierte Abhaengigkeiten
    - Scannt Python-Imports fuer implizite Abhaengigkeiten
    - Kopiert alle aufgeloesten Dependencies in _deps/
    - Generiert manifest.json und requirements.txt
"""

import sys
import re
import ast
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional

# Pfade
SCRIPT_DIR = Path(__file__).parent
SYSTEM_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = SYSTEM_ROOT / "skills"
TOOLS_DIR = SYSTEM_ROOT / "tools"
HUB_DIR = SYSTEM_ROOT / "hub"
SERVICES_DIR = HUB_DIR / "_services"
WORKFLOWS_DIR = SKILLS_DIR / "workflows"
EXPORTS_DIR = SYSTEM_ROOT.parent / "exports"

# Standard-Bibliotheken (nicht in requirements.txt aufnehmen)
STDLIB_MODULES = {
    'abc', 'argparse', 'ast', 'asyncio', 'base64', 'bisect', 'calendar',
    'collections', 'configparser', 'contextlib', 'copy', 'csv', 'ctypes',
    'dataclasses', 'datetime', 'decimal', 'difflib', 'email', 'enum',
    'fnmatch', 'functools', 'getpass', 'glob', 'gzip', 'hashlib', 'html',
    'http', 'importlib', 'inspect', 'io', 'itertools', 'json', 'logging',
    'math', 'mimetypes', 'multiprocessing', 'numbers', 'operator', 'os',
    'pathlib', 'pickle', 'platform', 'pprint', 'queue', 're', 'secrets',
    'shlex', 'shutil', 'signal', 'socket', 'sqlite3', 'string', 'struct',
    'subprocess', 'sys', 'tempfile', 'textwrap', 'threading', 'time',
    'timeit', 'traceback', 'typing', 'unittest', 'urllib', 'uuid', 'warnings',
    'weakref', 'xml', 'zipfile', 'zlib',
    # Windows-spezifisch
    'winreg', 'msvcrt', 'winsound',
    # Interne BACH-Module die nicht exportiert werden muessen
    'hub', 'hub.base',
}


class DependencyResolver:
    """Loest Abhaengigkeiten eines Skills rekursiv auf."""

    def __init__(self, system_root: Path):
        self.system_root = system_root
        self.skills_dir = system_root / "skills"
        self.tools_dir = system_root / "tools"
        self.services_dir = system_root / "hub" / "_services"
        self.workflows_dir = self.skills_dir / "workflows"

        # Gesammelte Abhaengigkeiten
        self.resolved_tools: Dict[str, Path] = {}
        self.resolved_services: Dict[str, Path] = {}
        self.resolved_workflows: Dict[str, Path] = {}
        self.pip_packages: Set[str] = set()
        self.warnings: List[str] = []

        # Bereits verarbeitete Pfade (Zykluserkennung)
        self._processed: Set[str] = set()

    def resolve(self, skill_path: Path) -> dict:
        """
        Hauptmethode: Loest alle Abhaengigkeiten eines Skills auf.

        Args:
            skill_path: Pfad zum Skill-Verzeichnis oder zur Skill-Datei

        Returns:
            dict mit allen aufgeloesten Abhaengigkeiten
        """
        # 1. Deklarierte Abhaengigkeiten aus SKILL.md lesen
        declared = self._read_declared_dependencies(skill_path)

        # 2. Deklarierte Abhaengigkeiten aufloesen
        for tool_name in declared.get('tools', []):
            self._resolve_tool(tool_name)

        for service_name in declared.get('services', []):
            self._resolve_service(service_name)

        for workflow_name in declared.get('workflows', []):
            self._resolve_workflow(workflow_name)

        # 3. Python-Imports scannen fuer implizite Abhaengigkeiten
        self._scan_python_imports(skill_path)

        return {
            'tools': dict(self.resolved_tools),
            'services': dict(self.resolved_services),
            'workflows': dict(self.resolved_workflows),
            'pip_packages': sorted(self.pip_packages),
            'warnings': list(self.warnings),
        }

    def _read_declared_dependencies(self, skill_path: Path) -> dict:
        """Liest deklarierte Abhaengigkeiten aus SKILL.md YAML-Header."""
        skill_md = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path

        if not skill_md.exists():
            self.warnings.append(f"Keine SKILL.md gefunden: {skill_md}")
            return {'tools': [], 'services': [], 'workflows': []}

        try:
            content = skill_md.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            self.warnings.append(f"Fehler beim Lesen von {skill_md}: {e}")
            return {'tools': [], 'services': [], 'workflows': []}

        # YAML-Frontmatter extrahieren
        yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not yaml_match:
            self.warnings.append("Kein YAML-Frontmatter in SKILL.md gefunden")
            return {'tools': [], 'services': [], 'workflows': []}

        yaml_text = yaml_match.group(1)

        # Dependencies-Block parsen (einfach, ohne yaml-Modul als harte Abhaengigkeit)
        deps = {'tools': [], 'services': [], 'workflows': []}

        try:
            import yaml
            header = yaml.safe_load(yaml_text)
            if header and isinstance(header, dict):
                dep_section = header.get('dependencies', {})
                if isinstance(dep_section, dict):
                    for key in ['tools', 'services', 'workflows']:
                        val = dep_section.get(key, [])
                        if isinstance(val, list):
                            deps[key] = [str(v) for v in val if v]
                        elif isinstance(val, str) and val.strip():
                            deps[key] = [v.strip() for v in val.split(',') if v.strip()]
        except ImportError:
            # Fallback: Regex-basiertes Parsen
            deps = self._parse_deps_regex(yaml_text)
        except Exception as e:
            self.warnings.append(f"YAML-Parse-Fehler: {e}")
            deps = self._parse_deps_regex(yaml_text)

        return deps

    def _parse_deps_regex(self, yaml_text: str) -> dict:
        """Fallback: Dependencies per Regex aus YAML extrahieren."""
        deps = {'tools': [], 'services': [], 'workflows': []}

        for key in ['tools', 'services', 'workflows']:
            # Pattern: tools: [item1, item2] oder tools:\n  - item1\n  - item2

            # Inline-Liste: tools: [a, b, c]
            inline = re.search(
                rf'{key}:\s*\[([^\]]*)\]', yaml_text, re.IGNORECASE
            )
            if inline:
                items = [i.strip().strip('"\'') for i in inline.group(1).split(',')]
                deps[key] = [i for i in items if i]
                continue

            # Block-Liste: tools:\n    - a\n    - b
            block = re.search(
                rf'{key}:\s*\n((?:\s+-\s+.+\n?)+)', yaml_text, re.IGNORECASE
            )
            if block:
                items = re.findall(r'-\s+(.+)', block.group(1))
                deps[key] = [i.strip().strip('"\'') for i in items if i.strip()]

        return deps

    def _resolve_tool(self, tool_name: str):
        """Loest ein Tool aus tools/ auf."""
        if tool_name in self.resolved_tools:
            return

        # Versuche verschiedene Namenskonventionen
        candidates = [
            self.tools_dir / f"{tool_name}.py",
            self.tools_dir / f"c_{tool_name}.py",
            self.tools_dir / tool_name,
        ]

        # Auch Unterordner durchsuchen
        for subdir in self.tools_dir.iterdir():
            if subdir.is_dir() and not subdir.name.startswith('_') and not subdir.name.startswith('.'):
                candidates.append(subdir / f"{tool_name}.py")

        # Fuzzy-Match: Tool-Name als Substring
        for py_file in self.tools_dir.glob("*.py"):
            clean_name = tool_name.lower().replace('-', '_').replace(' ', '_')
            if clean_name in py_file.stem.lower():
                candidates.append(py_file)

        for candidate in candidates:
            if candidate.exists():
                if candidate.is_file():
                    self.resolved_tools[tool_name] = candidate
                elif candidate.is_dir():
                    self.resolved_tools[tool_name] = candidate
                return

        self.warnings.append(f"Tool nicht gefunden: {tool_name}")

    def _resolve_service(self, service_name: str):
        """Loest einen Service aus hub/_services/ auf."""
        if service_name in self.resolved_services:
            return

        candidates = [
            self.services_dir / service_name,
            self.services_dir / f"{service_name}.md",
            self.services_dir / f"{service_name}.py",
        ]

        # Fuzzy-Match
        if self.services_dir.exists():
            for item in self.services_dir.iterdir():
                clean_name = service_name.lower().replace('-', '_').replace(' ', '_')
                if clean_name in item.name.lower():
                    candidates.append(item)

        for candidate in candidates:
            if candidate.exists():
                self.resolved_services[service_name] = candidate
                return

        self.warnings.append(f"Service nicht gefunden: {service_name}")

    def _resolve_workflow(self, workflow_name: str):
        """Loest einen Workflow aus skills/workflows/ auf."""
        if workflow_name in self.resolved_workflows:
            return

        candidates = [
            self.workflows_dir / f"{workflow_name}.md",
            self.workflows_dir / workflow_name,
        ]

        # Fuzzy-Match
        if self.workflows_dir.exists():
            for md_file in self.workflows_dir.glob("*.md"):
                clean_name = workflow_name.lower().replace('-', '_').replace(' ', '_')
                if clean_name in md_file.stem.lower():
                    candidates.append(md_file)

        for candidate in candidates:
            if candidate.exists():
                self.resolved_workflows[workflow_name] = candidate
                return

        self.warnings.append(f"Workflow nicht gefunden: {workflow_name}")

    def _scan_python_imports(self, skill_path: Path):
        """Scannt Python-Dateien im Skill nach Import-Statements."""
        if skill_path.is_file():
            if skill_path.suffix == '.py':
                self._scan_single_file(skill_path)
            return

        for py_file in skill_path.rglob("*.py"):
            if '__pycache__' not in str(py_file):
                self._scan_single_file(py_file)

    def _scan_single_file(self, py_file: Path):
        """Scannt eine einzelne Python-Datei nach Imports."""
        file_key = str(py_file)
        if file_key in self._processed:
            return
        self._processed.add(file_key)

        try:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            tree = ast.parse(content)
        except (SyntaxError, Exception):
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._classify_import(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self._classify_import(node.module)

    def _classify_import(self, module_name: str):
        """Klassifiziert einen Import als stdlib, pip-Paket oder BACH-intern."""
        if not module_name:
            return

        top_level = module_name.split('.')[0]

        # Stdlib?
        if top_level in STDLIB_MODULES:
            return

        # BACH-internes Modul?
        if top_level in ('hub', 'skills', 'tools', 'gui'):
            return

        # Bekannte pip-Pakete erkennen
        pip_mapping = {
            'yaml': 'PyYAML',
            'docx': 'python-docx',
            'PIL': 'Pillow',
            'cv2': 'opencv-python',
            'numpy': 'numpy',
            'pandas': 'pandas',
            'requests': 'requests',
            'flask': 'flask',
            'fastapi': 'fastapi',
            'pydantic': 'pydantic',
            'jinja2': 'Jinja2',
            'bs4': 'beautifulsoup4',
            'lxml': 'lxml',
            'openpyxl': 'openpyxl',
            'anthropic': 'anthropic',
            'openai': 'openai',
            'google': 'google-api-python-client',
            'aiohttp': 'aiohttp',
            'httpx': 'httpx',
            'rich': 'rich',
            'click': 'click',
            'toml': 'toml',
            'dotenv': 'python-dotenv',
            'cryptography': 'cryptography',
            'psutil': 'psutil',
            'watchdog': 'watchdog',
            'markdown': 'markdown',
            'pytest': 'pytest',
            'tqdm': 'tqdm',
        }

        if top_level in pip_mapping:
            self.pip_packages.add(pip_mapping[top_level])
        elif top_level.replace('_', '').isalpha() and top_level not in ('autolog',):
            # Unbekanntes Modul - koennte pip oder lokal sein
            # Pruefen ob es eine lokale Datei ist
            local_file = TOOLS_DIR / f"{top_level}.py"
            local_file_c = TOOLS_DIR / f"c_{top_level}.py"
            if local_file.exists() or local_file_c.exists():
                # Lokales Tool - als Tool-Abhaengigkeit aufnehmen
                if top_level not in self.resolved_tools:
                    found = local_file if local_file.exists() else local_file_c
                    self.resolved_tools[top_level] = found
            # Sonst ignorieren - koennte ein relativer Import sein


class SkillExporter:
    """Erstellt Export-Bundles fuer BACH-Skills."""

    def __init__(self, system_root: Path):
        self.system_root = system_root
        self.skills_dir = system_root / "skills"
        self.exports_dir = system_root.parent / "exports"
        self.resolver = DependencyResolver(system_root)

    def find_skill(self, name: str) -> Optional[Path]:
        """Findet einen Skill nach Name."""
        name_lower = name.lower()

        # In Standard-Verzeichnissen suchen
        for subdir in ['_agents', '_experts', '_services']:
            skill_dir = self.skills_dir / subdir / name
            if skill_dir.exists() and skill_dir.is_dir():
                return skill_dir

        # Fuzzy-Match
        for subdir in ['_agents', '_experts', '_services']:
            parent = self.skills_dir / subdir
            if parent.exists():
                for item in parent.iterdir():
                    if item.is_dir() and name_lower in item.name.lower():
                        return item

        # Einzeldatei-Suche
        for suffix in ['.md', '.txt']:
            for skill_file in self.skills_dir.rglob(f"*{suffix}"):
                if name_lower == skill_file.stem.lower():
                    return skill_file

        return None

    def export(self, name: str, output_dir: Optional[str] = None, dry_run: bool = False) -> Tuple[bool, str]:
        """
        Exportiert einen Skill mit allen Abhaengigkeiten.

        Args:
            name: Skill-Name
            output_dir: Optionales Zielverzeichnis
            dry_run: Nur zeigen, nichts kopieren

        Returns:
            (success, message)
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f"SKILL EXPORT: {name}")
        lines.append("=" * 60)

        # 1. Skill finden
        skill_path = self.find_skill(name)
        if not skill_path:
            return False, f"Skill nicht gefunden: {name}\nVerfuegbare Skills pruefen mit: bach --skills list"

        is_dir = skill_path.is_dir()
        skill_type = self._detect_type(skill_path)

        lines.append(f"Quelle:  {skill_path}")
        lines.append(f"Typ:     {skill_type}")
        lines.append(f"Format:  {'Verzeichnis' if is_dir else 'Datei'}")
        lines.append("")

        # 2. Abhaengigkeiten aufloesen
        lines.append("ABHAENGIGKEITS-ANALYSE")
        lines.append("-" * 40)

        deps = self.resolver.resolve(skill_path)

        if deps['tools']:
            lines.append(f"  Tools ({len(deps['tools'])}):")
            for tool_name, tool_path in deps['tools'].items():
                lines.append(f"    + {tool_name} -> {tool_path.relative_to(self.system_root)}")
        else:
            lines.append("  Tools: keine")

        if deps['services']:
            lines.append(f"  Services ({len(deps['services'])}):")
            for svc_name, svc_path in deps['services'].items():
                lines.append(f"    + {svc_name} -> {svc_path.relative_to(self.system_root)}")
        else:
            lines.append("  Services: keine")

        if deps['workflows']:
            lines.append(f"  Workflows ({len(deps['workflows'])}):")
            for wf_name, wf_path in deps['workflows'].items():
                lines.append(f"    + {wf_name} -> {wf_path.relative_to(self.system_root)}")
        else:
            lines.append("  Workflows: keine")

        if deps['pip_packages']:
            lines.append(f"  Pip-Pakete ({len(deps['pip_packages'])}):")
            for pkg in deps['pip_packages']:
                lines.append(f"    + {pkg}")

        if deps['warnings']:
            lines.append("")
            lines.append("  WARNUNGEN:")
            for warn in deps['warnings']:
                lines.append(f"    [!] {warn}")

        lines.append("")

        # 3. Export-Verzeichnis bestimmen
        if output_dir:
            export_path = Path(output_dir)
        else:
            export_path = self.exports_dir / f"{name}_export"

        lines.append(f"Zielverzeichnis: {export_path}")

        # 4. Skill-Dateien zaehlen
        if is_dir:
            skill_files = [
                f for f in skill_path.rglob("*")
                if f.is_file()
                and '__pycache__' not in str(f)
                and not f.name.startswith('.')
                and not f.suffix == '.pyc'
            ]
        else:
            skill_files = [skill_path]

        # Gesamtzahl berechnen
        dep_file_count = 0
        for tool_path in deps['tools'].values():
            if tool_path.is_dir():
                dep_file_count += sum(1 for f in tool_path.rglob("*") if f.is_file())
            else:
                dep_file_count += 1
        for svc_path in deps['services'].values():
            if svc_path.is_dir():
                dep_file_count += sum(1 for f in svc_path.rglob("*") if f.is_file())
            else:
                dep_file_count += 1
        dep_file_count += len(deps['workflows'])

        total_files = len(skill_files) + dep_file_count + 2  # +manifest +requirements
        lines.append(f"Dateien gesamt: {total_files} ({len(skill_files)} Skill + {dep_file_count} Deps + 2 Meta)")
        lines.append("")

        # 5. Manifest generieren
        manifest = self._generate_manifest(name, skill_path, skill_type, deps)

        lines.append("MANIFEST:")
        lines.append("-" * 40)
        manifest_json = json.dumps(manifest, indent=2, ensure_ascii=False)
        lines.append(manifest_json)
        lines.append("-" * 40)
        lines.append("")

        # 6. Dry-Run?
        if dry_run:
            lines.append("[DRY-RUN] Keine Dateien erstellt.")
            lines.append("Zum tatsaechlichen Export: ohne --dry-run ausfuehren")
            return True, "\n".join(lines)

        # 7. Export durchfuehren
        try:
            lines.append("EXPORT-VORGANG:")
            lines.append("-" * 40)

            # Zielverzeichnis erstellen (altes loeschen falls vorhanden)
            if export_path.exists():
                shutil.rmtree(export_path)
            export_path.mkdir(parents=True, exist_ok=True)

            # Skill-Dateien kopieren
            skill_dest = export_path / name
            if is_dir:
                shutil.copytree(
                    skill_path, skill_dest,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git')
                )
                lines.append(f"  [+] Skill-Verzeichnis kopiert: {name}/")
            else:
                skill_dest.mkdir(parents=True, exist_ok=True)
                shutil.copy2(skill_path, skill_dest / skill_path.name)
                lines.append(f"  [+] Skill-Datei kopiert: {skill_path.name}")

            # Dependencies kopieren
            deps_dir = export_path / "_deps"
            deps_dir.mkdir(exist_ok=True)

            # Tools
            if deps['tools']:
                tools_dest = deps_dir / "tools"
                tools_dest.mkdir(exist_ok=True)
                for tool_name, tool_path in deps['tools'].items():
                    if tool_path.is_dir():
                        shutil.copytree(
                            tool_path, tools_dest / tool_path.name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc')
                        )
                    else:
                        shutil.copy2(tool_path, tools_dest / tool_path.name)
                    lines.append(f"  [+] Tool: {tool_name}")

            # Services
            if deps['services']:
                services_dest = deps_dir / "services"
                services_dest.mkdir(exist_ok=True)
                for svc_name, svc_path in deps['services'].items():
                    if svc_path.is_dir():
                        shutil.copytree(
                            svc_path, services_dest / svc_path.name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc')
                        )
                    else:
                        shutil.copy2(svc_path, services_dest / svc_path.name)
                    lines.append(f"  [+] Service: {svc_name}")

            # Workflows
            if deps['workflows']:
                workflows_dest = deps_dir / "workflows"
                workflows_dest.mkdir(exist_ok=True)
                for wf_name, wf_path in deps['workflows'].items():
                    shutil.copy2(wf_path, workflows_dest / wf_path.name)
                    lines.append(f"  [+] Workflow: {wf_name}")

            # manifest.json schreiben
            manifest_path = export_path / "manifest.json"
            manifest_path.write_text(manifest_json, encoding='utf-8')
            lines.append("  [+] manifest.json")

            # requirements.txt generieren
            if deps['pip_packages']:
                req_content = "\n".join(deps['pip_packages']) + "\n"
            else:
                req_content = "# Keine externen Abhaengigkeiten\n"
            req_path = export_path / "requirements.txt"
            req_path.write_text(req_content, encoding='utf-8')
            lines.append("  [+] requirements.txt")

            lines.append("-" * 40)
            lines.append("")
            lines.append(f"[OK] Export erfolgreich: {export_path}")

            return True, "\n".join(lines)

        except Exception as e:
            return False, f"Export fehlgeschlagen: {e}\n\n" + "\n".join(lines)

    def _detect_type(self, skill_path: Path) -> str:
        """Erkennt den Skill-Typ anhand des Pfads."""
        path_str = str(skill_path).lower()
        if '_agents' in path_str:
            return 'agent'
        elif '_experts' in path_str:
            return 'expert'
        elif '_services' in path_str:
            return 'service'
        elif 'workflows' in path_str:
            return 'workflow'
        return 'skill'

    def _generate_manifest(self, name: str, skill_path: Path, skill_type: str, deps: dict) -> dict:
        """Generiert das manifest.json fuer den Export."""
        # Version und Beschreibung aus SKILL.md extrahieren
        version = "1.0.0"
        description = f"BACH {skill_type}: {name}"
        author = "BACH Team"

        skill_md = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path
        if skill_md.exists():
            try:
                content = skill_md.read_text(encoding='utf-8', errors='ignore')
                yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                if yaml_match:
                    yaml_text = yaml_match.group(1)

                    ver_match = re.search(r'version:\s*(.+)', yaml_text)
                    if ver_match:
                        version = ver_match.group(1).strip().strip('"\'')

                    desc_match = re.search(r'description:\s*>?\s*\n?\s*(.+)', yaml_text)
                    if desc_match:
                        description = desc_match.group(1).strip()

                    auth_match = re.search(r'author:\s*(.+)', yaml_text)
                    if auth_match:
                        author = auth_match.group(1).strip()
            except Exception:
                pass

        manifest = {
            "name": name,
            "version": version,
            "type": skill_type,
            "description": description,
            "author": author,
            "created_at": datetime.now().isoformat(),
            "bach_version": "2.0.0",
            "export_tool": "skill_export.py",

            "dependencies": {
                "tools": list(deps['tools'].keys()),
                "services": list(deps['services'].keys()),
                "workflows": list(deps['workflows'].keys()),
                "pip_packages": deps['pip_packages'],
            },

            "structure": {
                "skill": f"{name}/",
                "deps": "_deps/",
                "manifest": "manifest.json",
                "requirements": "requirements.txt",
            },
        }

        return manifest


def main():
    """CLI-Einstiegspunkt."""
    parser = argparse.ArgumentParser(
        description="BACH Skill Export mit Dependency Resolution"
    )
    parser.add_argument(
        '--skill', '-s',
        required=True,
        help='Name des zu exportierenden Skills'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Nur zeigen was exportiert wuerde'
    )
    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Zielverzeichnis (Standard: system/system/system/system/exports/<skill>_export)'
    )

    args = parser.parse_args()

    exporter = SkillExporter(SYSTEM_ROOT)
    success, message = exporter.export(
        name=args.skill,
        output_dir=args.output,
        dry_run=args.dry_run,
    )

    print(message)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
