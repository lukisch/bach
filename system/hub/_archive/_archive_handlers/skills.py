# SPDX-License-Identifier: MIT
"""
Skills Handler - Skill-Verwaltung
=================================

--skills list            Alle Skills auflisten (aus Dateisystem)
--skills show <n>        Skill-Details anzeigen
--skills search <term>   Skills durchsuchen
--skills export <name>   Skill exportieren mit manifest.json (v1.1.44)
--skills install <path>  Skill aus ZIP/Verzeichnis importieren (v1.1.44)
"""
import json
import zipfile
from pathlib import Path
from datetime import datetime
from .base import BaseHandler


class SkillsHandler(BaseHandler):
    """Handler fuer --skills Operationen"""
    
    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.skills_dir = base_path / "skills"
        self.base_path = base_path
    
    @property
    def profile_name(self) -> str:
        return "skills"
    
    @property
    def target_file(self) -> Path:
        return self.skills_dir
    
    def get_operations(self) -> dict:
        return {
            "list": "Alle Skills auflisten",
            "show": "Skill-Details anzeigen",
            "search": "Skills durchsuchen",
            "export": "Skill exportieren (manifest.json + ZIP)",
            "install": "Skill aus ZIP/Verzeichnis importieren"
        }
    
    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        # dry_run aus args extrahieren falls vorhanden
        if '--dry-run' in args:
            dry_run = True
            args = [a for a in args if a != '--dry-run']
        
        if operation == "show" and args:
            return self._show(args[0])
        elif operation == "search" and args:
            return self._search(" ".join(args))
        elif operation == "export" and args:
            # Filter --dry-run aus args
            clean_args = [a for a in args if not a.startswith('--')]
            output_dir = clean_args[1] if len(clean_args) > 1 else None
            return self._export(clean_args[0], output_dir, dry_run)
        elif operation == "install" and args:
            return self._install(args[0], dry_run)
        else:
            return self._list()
    
    def _list(self) -> tuple:
        """Alle Skills aus Dateisystem auflisten."""
        results = ["SKILLS", "=" * 50]
        
        if not self.skills_dir.exists():
            return False, "Skills-Verzeichnis nicht gefunden"
        
        # Skills nach Kategorie gruppieren
        categories = {}
        
        for item in self.skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith('__'):
                cat_name = item.name.lstrip('_')
                skills = list(item.glob("*.txt")) + list(item.glob("*.md"))
                if skills:
                    categories[cat_name] = skills
        
        # Auch Root-Level Skills
        root_skills = list(self.skills_dir.glob("*.txt")) + list(self.skills_dir.glob("*.md"))
        if root_skills:
            categories["_root"] = root_skills
        
        total = 0
        for cat, skills in sorted(categories.items()):
            if cat == "_root":
                results.append(f"\n[Root]")
            else:
                results.append(f"\n[{cat.upper()}]")
            
            for skill in sorted(skills):
                name = skill.stem
                results.append(f"  {name}")
                total += 1
        
        results.append(f"\n{'=' * 50}")
        results.append(f"Gesamt: {total} Skills in {len(categories)} Kategorien")
        
        return True, "\n".join(results)
    
    def _show(self, name: str) -> tuple:
        """Skill-Details anzeigen."""
        found = self._find_skill(name)
        
        if not found:
            return False, f"Skill nicht gefunden: {name}\nNutze: --skills list"
        
        results = [f"SKILL: {found.stem}", "=" * 50]
        results.append(f"Pfad: {found.relative_to(self.skills_dir)}")
        results.append(f"Groesse: {found.stat().st_size} Bytes")
        results.append("")
        
        # Inhalt anzeigen (max 50 Zeilen)
        try:
            content = found.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')[:50]
            results.extend(lines)
            if len(content.split('\n')) > 50:
                results.append(f"\n... ({len(content.split(chr(10))) - 50} weitere Zeilen)")
        except Exception as e:
            results.append(f"Fehler beim Lesen: {e}")
        
        return True, "\n".join(results)
    
    def _find_skill(self, name: str) -> Path:
        """Skill-Datei oder Verzeichnis finden."""
        name_lower = name.lower()
        
        # 1. Exakte Verzeichnis-Suche in _agents, _services, _experts
        for subdir in ['_agents', '_services', '_experts']:
            skill_dir = self.skills_dir / subdir / name
            if skill_dir.exists() and skill_dir.is_dir():
                return skill_dir
        
        # 2. Datei-Suche (.txt, .md)
        for suffix in ['.txt', '.md']:
            for skill_file in self.skills_dir.rglob(f"*{suffix}"):
                if name_lower in skill_file.stem.lower():
                    return skill_file
        
        return None
    
    def _search(self, term: str) -> tuple:
        """Skills nach Begriff durchsuchen."""
        results = [f"SKILL-SUCHE: '{term}'", "=" * 50]
        
        found = []
        term_lower = term.lower()
        
        for skill_file in self.skills_dir.rglob("*"):
            if skill_file.is_file() and skill_file.suffix in ['.txt', '.md']:
                # Im Namen suchen
                if term_lower in skill_file.stem.lower():
                    found.append((skill_file, "Name"))
                    continue
                
                # Im Inhalt suchen
                try:
                    content = skill_file.read_text(encoding='utf-8', errors='ignore').lower()
                    if term_lower in content:
                        found.append((skill_file, "Inhalt"))
                except:
                    pass
        
        if not found:
            results.append(f"Keine Skills gefunden fuer: {term}")
        else:
            results.append(f"Gefunden: {len(found)}\n")
            for skill, match_type in found[:20]:
                rel_path = skill.relative_to(self.skills_dir)
                results.append(f"  [{match_type}] {rel_path}")
            
            if len(found) > 20:
                results.append(f"\n  ... und {len(found) - 20} weitere")
        
        return True, "\n".join(results)
    
    def _export(self, name: str, output_dir: str = None, dry_run: bool = False) -> tuple:
        """
        Skill exportieren mit manifest.json.
        
        Args:
            name: Skill-Name (z.B. 'ati', 'steuer-agent')
            output_dir: Zielverzeichnis (optional, default: system/system/system/system/exports/<name>_export)
            dry_run: Nur zeigen was passieren wuerde
        
        Returns:
            (success, message)
        """
        results = [f"SKILL EXPORT: {name}", "=" * 50]
        
        # 1. Skill finden
        skill_path = self._find_skill(name)
        if not skill_path:
            return False, f"Skill nicht gefunden: {name}\nNutze: --skills list"
        
        # Bestimme ob Verzeichnis oder Datei
        is_directory = skill_path.is_dir()
        
        # 2. Output-Verzeichnis bestimmen
        if output_dir:
            export_path = Path(output_dir)
        else:
            export_path = self.base_path / "exports" / f"{name}_export"
        
        results.append(f"Quelle: {skill_path}")
        results.append(f"Ziel: {export_path}")
        results.append(f"Typ: {'Verzeichnis' if is_directory else 'Datei'}")
        results.append("")
        
        # 3. Skill-Typ ermitteln
        skill_type = self._detect_skill_type(skill_path)
        results.append(f"Erkannter Typ: {skill_type}")
        
        # 4. Dateien sammeln die exportiert werden
        files_to_export = self._collect_export_files(skill_path, is_directory)
        results.append(f"Dateien: {len(files_to_export)}")
        
        # 5. Manifest generieren
        manifest = self._generate_manifest(name, skill_path, skill_type, files_to_export)
        
        results.append("")
        results.append("MANIFEST.JSON:")
        results.append("-" * 40)
        results.append(json.dumps(manifest, indent=2, ensure_ascii=False))
        results.append("-" * 40)
        
        if dry_run:
            results.append("")
            results.append("[DRY-RUN] Keine Dateien erstellt")
            results.append("Nutze ohne --dry-run zum tatsaechlichen Export")
            return True, "\n".join(results)
        
        # 6. Export durchfuehren - ZIP erstellen
        try:
            # Export-Verzeichnis erstellen
            export_path.mkdir(parents=True, exist_ok=True)
            
            # ZIP-Dateiname
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"{name}_v{manifest['version']}_{timestamp}.zip"
            zip_path = export_path / zip_filename
            
            results.append("")
            results.append("ZIP-ERSTELLUNG:")
            results.append("-" * 40)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Manifest zuerst hinzufuegen
                manifest_content = json.dumps(manifest, indent=2, ensure_ascii=False)
                zipf.writestr("manifest.json", manifest_content)
                results.append("  + manifest.json")
                
                # Alle Skill-Dateien hinzufuegen
                for file_path in files_to_export:
                    # Relativer Pfad im ZIP
                    if is_directory:
                        # Bei Verzeichnis: relativ zum Skill-Verzeichnis
                        try:
                            arc_name = file_path.relative_to(skill_path)
                        except ValueError:
                            arc_name = file_path.name
                    else:
                        # Bei Einzeldatei: nur Dateiname
                        arc_name = file_path.name
                    
                    # In skill/ Unterverzeichnis packen
                    arc_path = f"skill/{arc_name}"
                    zipf.write(file_path, arc_path)
                    results.append(f"  + {arc_path}")
            
            # Statistik
            zip_size = zip_path.stat().st_size
            results.append("-" * 40)
            results.append(f"ZIP erstellt: {zip_path.name}")
            results.append(f"Groesse: {zip_size / 1024:.1f} KB")
            results.append(f"Dateien: {len(files_to_export) + 1}")  # +1 fuer manifest
            results.append("")
            results.append(f"[OK] Export erfolgreich: {zip_path}")
            
            # Auch manifest.json separat speichern fuer Referenz
            manifest_file = export_path / "manifest.json"
            manifest_file.write_text(manifest_content, encoding='utf-8')
            
        except Exception as e:
            return False, f"ZIP-Erstellung fehlgeschlagen: {e}"
        
        return True, "\n".join(results)
    
    def _detect_skill_type(self, skill_path: Path) -> str:
        """Skill-Typ erkennen (agent, service, expert, skill)."""
        path_str = str(skill_path).lower()
        
        if '_agents' in path_str:
            return 'agent'
        elif '_services' in path_str:
            return 'service'
        elif '_experts' in path_str:
            return 'expert'
        else:
            return 'skill'
    
    def _collect_export_files(self, skill_path: Path, is_directory: bool) -> list:
        """Alle zu exportierenden Dateien sammeln (ohne pycache, hidden)."""
        files = []
        
        # Ausgeschlossene Patterns
        exclude_patterns = ['__pycache__', '.pyc', '.pyo', '.git', '.DS_Store']
        
        if is_directory:
            # Alle Dateien im Verzeichnis
            for f in skill_path.rglob("*"):
                if f.is_file() and not f.name.startswith('.'):
                    # Pruefen ob in exclude_patterns
                    skip = False
                    for pattern in exclude_patterns:
                        if pattern in str(f):
                            skip = True
                            break
                    if not skip:
                        files.append(f)
        else:
            # Einzelne Datei
            files.append(skill_path)
        
        return files
    
    def _generate_manifest(self, name: str, skill_path: Path, skill_type: str, files: list) -> dict:
        """
        Export-Manifest (manifest.json) generieren.
        
        Das Manifest enthaelt:
        - Metadaten (Name, Version, Typ, Beschreibung)
        - includes: Welche Dateien enthalten sind
        - dependencies: Python-Version, Packages
        - entry_points: Wie der Skill gestartet wird
        """
        # Beschreibung aus erster Datei extrahieren
        description = ""
        for f in files:
            if f.suffix in ['.md', '.txt']:
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    first_line = content.split('\n')[0].strip()
                    if first_line.startswith('#'):
                        description = first_line.lstrip('# ').strip()
                    elif first_line:
                        description = first_line[:100]
                    if description:
                        break
                except:
                    pass
        
        # Relative Pfade fuer includes
        includes = []
        try:
            for f in files:
                rel = f.relative_to(self.skills_dir)
                includes.append(str(rel).replace('\\', '/'))
        except:
            includes = [f.name for f in files]
        
        manifest = {
            "name": name,
            "version": "1.0.0",
            "type": skill_type,
            "description": description or f"BACH {skill_type}: {name}",
            "created_at": datetime.now().isoformat(),
            "bach_version": "1.1.44",
            
            "includes": {
                "core": includes
            },
            
            "dependencies": {
                "python": ">=3.9",
                "packages": []
            },
            
            "entry_points": {}
        }
        
        # Agent-spezifische Entry-Points
        if skill_type == 'agent':
            manifest["entry_points"] = {
                "main": f"agents/{name}/SKILL.md",
                "description": f"Agenten-Dokumentation fuer {name}"
            }
        
        return manifest
    
    def _install(self, path: str, dry_run: bool = False) -> tuple:
        """
        Skill aus Export-ZIP oder Verzeichnis importieren.
        
        Args:
            path: Pfad zur ZIP-Datei oder zum Verzeichnis mit manifest.json
            dry_run: Nur zeigen was passieren wuerde
        
        Returns:
            (success, message)
        """
        import shutil
        import tempfile
        
        results = [f"SKILL INSTALL", "=" * 50]
        source_path = Path(path)
        
        # 1. Quelle pruefen
        if not source_path.exists():
            return False, f"Pfad nicht gefunden: {path}"
        
        results.append(f"Quelle: {source_path}")
        
        temp_dir = None
        manifest_dir = None
        
        try:
            # 2. ZIP oder Verzeichnis?
            if source_path.suffix.lower() == '.zip':
                results.append("Typ: ZIP-Archiv")
                
                # ZIP in temp-Verzeichnis entpacken
                temp_dir = Path(tempfile.mkdtemp(prefix="bach_skill_"))
                results.append(f"Entpacke nach: {temp_dir}")
                
                with zipfile.ZipFile(source_path, 'r') as zipf:
                    zipf.extractall(temp_dir)
                
                manifest_dir = temp_dir
            else:
                results.append("Typ: Verzeichnis")
                manifest_dir = source_path
            
            # 3. Manifest lesen
            manifest_path = manifest_dir / "manifest.json"
            if not manifest_path.exists():
                return False, f"Keine manifest.json gefunden in: {manifest_dir}"
            
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            results.append("")
            results.append("MANIFEST:")
            results.append(f"  Name: {manifest.get('name', 'unbekannt')}")
            results.append(f"  Version: {manifest.get('version', '?')}")
            results.append(f"  Typ: {manifest.get('type', 'skill')}")
            results.append(f"  Beschreibung: {manifest.get('description', '-')[:60]}")
            
            # 4. Zielverzeichnis bestimmen
            skill_name = manifest.get('name', source_path.stem)
            skill_type = manifest.get('type', 'skill')
            
            # Typ zu Unterverzeichnis mappen
            type_dirs = {
                'agent': '_agents',
                'service': '_services',
                'expert': '_experts',
                'skill': ''  # Root-Level
            }
            
            target_subdir = type_dirs.get(skill_type, '')
            if target_subdir:
                target_path = self.skills_dir / target_subdir / skill_name
            else:
                target_path = self.skills_dir / skill_name
            
            results.append("")
            results.append(f"Zielverzeichnis: {target_path}")
            
            # 5. Pruefen ob bereits existiert
            if target_path.exists():
                results.append("[!] Skill existiert bereits")
                if not dry_run:
                    # Backup erstellen
                    backup_name = f"{skill_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    backup_path = self.base_path / "exports" / "_backups" / backup_name
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(target_path), str(backup_path))
                    results.append(f"    Backup erstellt: {backup_path}")
            
            # 6. Skill-Dateien finden
            skill_source = manifest_dir / "skill"
            if not skill_source.exists():
                # Fallback: Dateien direkt im manifest_dir
                skill_source = manifest_dir
            
            # Dateien zaehlen
            files_to_copy = list(skill_source.rglob("*"))
            files_to_copy = [f for f in files_to_copy if f.is_file() 
                           and f.name != 'manifest.json'
                           and '__pycache__' not in str(f)]
            
            results.append(f"Dateien zu kopieren: {len(files_to_copy)}")
            
            if dry_run:
                results.append("")
                results.append("[DRY-RUN] Dateien die kopiert wuerden:")
                for f in files_to_copy[:10]:
                    try:
                        rel = f.relative_to(skill_source)
                    except ValueError:
                        rel = f.name
                    results.append(f"  - {rel}")
                if len(files_to_copy) > 10:
                    results.append(f"  ... und {len(files_to_copy) - 10} weitere")
                results.append("")
                results.append("[DRY-RUN] Keine Dateien kopiert")
                results.append("Nutze ohne --dry-run zum tatsaechlichen Import")
                return True, "\n".join(results)
            
            # 7. Kopieren
            results.append("")
            results.append("KOPIERE DATEIEN:")
            results.append("-" * 40)
            
            target_path.mkdir(parents=True, exist_ok=True)
            
            copied = 0
            for src_file in files_to_copy:
                try:
                    rel_path = src_file.relative_to(skill_source)
                except ValueError:
                    rel_path = Path(src_file.name)
                
                dest_file = target_path / rel_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dest_file)
                results.append(f"  + {rel_path}")
                copied += 1
            
            # 8. Manifest auch kopieren
            manifest_dest = target_path / "manifest.json"
            shutil.copy2(manifest_path, manifest_dest)
            results.append("  + manifest.json")
            
            results.append("-" * 40)
            results.append(f"Kopiert: {copied + 1} Dateien")
            results.append("")
            results.append(f"[OK] Skill '{skill_name}' erfolgreich installiert!")
            results.append(f"    Pfad: {target_path}")
            
            # 9. Dependencies Info
            deps = manifest.get('dependencies', {})
            packages = deps.get('packages', [])
            if packages:
                results.append("")
                results.append("[INFO] Abhaengigkeiten:")
                for pkg in packages:
                    results.append(f"  pip install {pkg}")
            
        except json.JSONDecodeError as e:
            return False, f"Ungueltige manifest.json: {e}"
        except Exception as e:
            return False, f"Install fehlgeschlagen: {e}"
        finally:
            # Temp-Verzeichnis aufraeumen
            if temp_dir and temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
        
        return True, "\n".join(results)
