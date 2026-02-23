# SPDX-License-Identifier: MIT
"""
Agents Handler - Agenten-Verwaltung
===================================

--agents list        Alle Agenten auflisten
--agents info <n>    Agenten-Details
--agents active      Nur aktive Agenten
"""
import sqlite3
from pathlib import Path
from .base import BaseHandler

# Pfade aus zentraler Konfiguration (Single Source of Truth)
# Fallback falls bach_paths nicht importierbar
try:
    from .bach_paths import AGENTS_DIR as _AGENTS_DIR, EXPERTS_DIR as _EXPERTS_DIR
    _PATHS_FROM_BACH = True
except ImportError:
    _AGENTS_DIR = None
    _EXPERTS_DIR = None
    _PATHS_FROM_BACH = False


class AgentsHandler(BaseHandler):
    """Handler fuer --agents Operationen"""

    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.db_path = base_path / "data" / "bach.db"
        # Pfade: aus bach_paths oder Fallback relativ zu base_path
        self.agents_dir = _AGENTS_DIR if _PATHS_FROM_BACH else base_path / "agents"
        self.experts_dir = _EXPERTS_DIR if _PATHS_FROM_BACH else base_path / "agents" / "_experts"

    @property
    def profile_name(self) -> str:
        return "agents"

    @property
    def target_file(self) -> Path:
        return self.db_path

    def get_operations(self) -> dict:
        return {
            "list": "Alle Agenten und Experten auflisten",
            "info": "Agenten-Details anzeigen",
            "active": "Nur aktive Agenten",
            "sync": "Neue Filesystem-Experten automatisch in DB eintragen",
        }

    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if not self.db_path.exists():
            return False, "Datenbank nicht gefunden"

        if operation == "info" and args:
            return self._info(args[0])
        elif operation == "active":
            return self._list(active_only=True)
        elif operation == "sync":
            return self._sync(dry_run=dry_run)
        else:
            return self._list(active_only=False)

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _scan_filesystem(self) -> tuple:
        """
        Scannt Filesystem nach Boss-Agenten und Experten.

        Boss-Agenten:  agents/*/SKILL.md  (Unterordner ohne fuehrendes _)
        Experten:      agents/_experts/*/CONCEPT.md  (nur Status: AKTIV)

        Pfade kommen aus bach_paths.py (Single Source of Truth).

        Returns:
            (boss_agents, experts) - beide als dict {key: entry}
        """
        boss_agents = {}
        experts = {}

        # --- Boss-Agenten ---
        if self.agents_dir and self.agents_dir.exists():
            for subdir in sorted(self.agents_dir.iterdir()):
                # Nur echte Unterordner, keine _* Systemordner, keine Dateien
                if not subdir.is_dir() or subdir.name.startswith('_'):
                    continue
                skill_file = subdir / "SKILL.md"
                if skill_file.exists():
                    key = subdir.name.lower()
                    boss_agents[key] = {
                        'name': subdir.name,
                        'file': skill_file,
                        'in_db': False,
                        'is_active': False,
                        'type': 'boss',
                    }

        # --- Experten ---
        if self.experts_dir and self.experts_dir.exists():
            for subdir in sorted(self.experts_dir.iterdir()):
                if not subdir.is_dir() or subdir.name.startswith('_'):
                    continue
                concept = subdir / "CONCEPT.md"
                if not concept.exists():
                    continue
                # Status aus Datei lesen
                try:
                    content = concept.read_text(encoding='utf-8', errors='ignore')
                    aktiv = 'Status: AKTIV' in content
                except Exception:
                    aktiv = False
                key = subdir.name.lower()
                experts[key] = {
                    'name': subdir.name,
                    'file': concept,
                    'in_db': False,
                    'is_active': False,
                    'aktiv_in_file': aktiv,
                    'type': 'expert',
                }

        return boss_agents, experts

    def _load_db_status(self, boss_agents: dict, experts: dict, active_only: bool):
        """Reichert Filesystem-Eintraege mit DB-Status an."""
        if not self.db_path.exists():
            return

        try:
            conn = self._get_conn()
            cursor = conn.cursor()

            # --- bach_agents Tabelle (Boss-Agenten, die richtige Tabelle) ---
            try:
                ba_query = "SELECT name, is_active FROM bach_agents"
                if active_only:
                    ba_query += " WHERE is_active = 1"
                cursor.execute(ba_query)
                for row in cursor.fetchall():
                    key = row['name'].lower()
                    if key in boss_agents:
                        boss_agents[key]['in_db'] = True
                        boss_agents[key]['is_active'] = bool(row['is_active'])
            except sqlite3.OperationalError:
                pass  # bach_agents existiert noch nicht

            # --- agents Tabelle (Legacy / manuell eingetragene) ---
            query = "SELECT name, type, is_active FROM agents"
            if active_only:
                query += " WHERE is_active = 1"
            query += " ORDER BY name"
            cursor.execute(query)

            for row in cursor.fetchall():
                key = row['name'].lower()
                is_active = bool(row['is_active'])
                if key in boss_agents:
                    boss_agents[key]['in_db'] = True
                    boss_agents[key]['is_active'] = is_active
                    boss_agents[key]['type'] = row['type']
                elif key in experts:
                    experts[key]['in_db'] = True
                    experts[key]['is_active'] = is_active
                else:
                    # Nur in DB, nicht im Filesystem -> unter Boss-Agenten listen
                    boss_agents[key] = {
                        'name': row['name'],
                        'file': None,
                        'in_db': True,
                        'is_active': is_active,
                        'type': row['type'],
                    }

            # --- bach_experts Tabelle (Experten) ---
            try:
                exp_query = "SELECT name, is_active FROM bach_experts"
                if active_only:
                    exp_query += " WHERE is_active = 1"
                cursor.execute(exp_query)
                for row in cursor.fetchall():
                    key = row['name'].lower()
                    is_active = bool(row['is_active'])
                    if key in experts:
                        experts[key]['in_db'] = True
                        experts[key]['is_active'] = is_active
                    elif key not in boss_agents:
                        # Nur in bach_experts, nicht im Filesystem
                        experts[key] = {
                            'name': row['name'],
                            'file': None,
                            'in_db': True,
                            'is_active': is_active,
                            'aktiv_in_file': False,
                            'type': 'expert',
                        }
            except sqlite3.OperationalError:
                pass  # bach_experts Tabelle existiert noch nicht

            conn.close()
        except Exception as e:
            pass  # DB-Fehler nicht crashen lassen

    def _status_icon(self, entry: dict) -> str:
        if entry.get('in_db') and entry.get('is_active'):
            return "[X]"
        elif entry.get('in_db'):
            return "[-]"
        else:
            return "[ ]"

    def _list(self, active_only: bool) -> tuple:
        """Agenten und Experten auflisten - aus bach_paths + DB."""
        results = ["AGENTEN", "=" * 40]

        boss_agents, experts = self._scan_filesystem()
        self._load_db_status(boss_agents, experts, active_only)

        # --- Boss-Agenten ausgeben ---
        results.append("\n[BOSS-AGENTEN]")
        if boss_agents:
            for key, agent in sorted(boss_agents.items()):
                type_str = f" ({agent.get('type', 'boss')})"
                results.append(f"  {self._status_icon(agent)} {agent['name']}{type_str}")
        else:
            results.append("  (keine gefunden)")

        # --- Experten ausgeben ---
        results.append("\n[EXPERTEN]")
        if experts:
            for key, expert in sorted(experts.items()):
                # Datei-Status ergaenzen wenn nur Filesystem
                file_status = ""
                if not expert.get('in_db') and not expert.get('aktiv_in_file', True):
                    file_status = " (inaktiv)"
                results.append(f"  {self._status_icon(expert)} {expert['name']}{file_status}")
        else:
            results.append("  (keine gefunden)")

        results.append("\n" + "=" * 40)
        results.append("Legende: [X]=DB+aktiv [-]=DB+inaktiv [ ]=nur Datei")
        results.append(f"Pfade: {self.agents_dir} {'(bach_paths)' if _PATHS_FROM_BACH else '(fallback)'}")
        results.append("\nDetails: --agents info <n>")

        return True, "\n".join(results)

    def _parse_concept(self, concept_file: Path) -> dict:
        """
        Liest Metadaten aus einer CONCEPT.md.

        Erwartet dieses Format im Header:
            # EXPERTE: Display Name
            ## Status: AKTIV
            Version: 1.0.0
            Erstellt: ...
            Parent-Agent: boss-agent-name
        """
        meta = {}
        try:
            lines = concept_file.read_text(encoding='utf-8', errors='ignore').splitlines()
            for line in lines[:20]:  # Nur Header-Bereich
                line = line.strip()
                if line.startswith('# EXPERTE:'):
                    meta['display_name'] = line.replace('# EXPERTE:', '').strip()
                elif line.startswith('Version:'):
                    meta['version'] = line.replace('Version:', '').strip()
                elif line.startswith('Parent-Agent:'):
                    meta['parent_agent'] = line.replace('Parent-Agent:', '').strip().lower()
            # Erste Beschreibungszeile nach dem Header
            in_desc = False
            for line in lines:
                if '## 1.' in line or 'Ueberblick' in line or 'Beschreibung' in line:
                    in_desc = True
                    continue
                if in_desc and line.strip() and not line.startswith('#'):
                    meta['description'] = line.strip()[:200]
                    break
        except Exception:
            pass
        return meta

    def _sync(self, dry_run: bool = False) -> tuple:
        """
        Synct alle Filesystem-Experten (Status: AKTIV) in bach_experts.

        Nur Experten mit [ ] (nicht in DB) werden eingetragen.
        Parent-Agent wird aus CONCEPT.md gelesen und gegen bach_agents aufgeloest.
        """
        boss_agents, experts = self._scan_filesystem()
        self._load_db_status(boss_agents, experts, active_only=False)

        # Nur [ ] Experten (Filesystem, aber nicht in bach_experts)
        to_sync = [(k, e) for k, e in sorted(experts.items())
                   if not e.get('in_db') and e.get('file')]

        if not to_sync:
            return True, "[OK] Alle Experten bereits in DB eingetragen. Nichts zu tun."

        if dry_run:
            lines = [f"[DRY-RUN] {len(to_sync)} Experte(n) wuerden eingetragen:"]
            for key, e in to_sync:
                lines.append(f"  + {e['name']}")
            return True, "\n".join(lines)

        # Bach-Agent-ID-Mapping laden
        ba_map = {}
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM bach_agents")
            for row in cursor.fetchall():
                ba_map[row['name'].lower()] = row['id']
            conn.close()
        except Exception:
            pass

        conn = self._get_conn()
        cursor = conn.cursor()
        synced = []
        errors = []

        for key, expert in to_sync:
            meta = self._parse_concept(expert['file'])
            parent_name = meta.get('parent_agent', '')
            agent_id = ba_map.get(parent_name, 1)  # Fallback: ID 1

            # Skill-Pfad relativ zu system/
            try:
                rel_path = str(expert['file'].relative_to(self.base_path))
            except ValueError:
                rel_path = str(expert['file'])

            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO bach_experts
                        (name, display_name, agent_id, description, skill_path, version, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, 1)
                """, (
                    expert['name'],
                    meta.get('display_name', expert['name']),
                    agent_id,
                    meta.get('description', ''),
                    rel_path,
                    meta.get('version', '1.0.0'),
                ))
                synced.append(f"  + {expert['name']} (Parent: {parent_name or '?'})")
            except Exception as e:
                errors.append(f"  ! {expert['name']}: {e}")

        conn.commit()
        conn.close()

        lines = []
        if synced:
            lines.append(f"[OK] {len(synced)} Experte(n) eingetragen:")
            lines.extend(synced)
        if errors:
            lines.append(f"\n[FEHLER] {len(errors)} fehlgeschlagen:")
            lines.extend(errors)

        return True, "\n".join(lines)

    def _info(self, name: str) -> tuple:
        """Agenten-Details - sucht in agents + bach_experts."""
        conn = self._get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM agents
            WHERE name LIKE ? OR id = ?
        """, (f"%{name}%", name if name.isdigit() else -1))

        agent = cursor.fetchone()

        if agent:
            results = [f"AGENT: {agent['name']}", "=" * 40]
            results.append(f"ID:          {agent['id']}")
            results.append(f"Type:        {agent['type']}")
            results.append(f"Aktiv:       {'Ja' if agent['is_active'] else 'Nein'}")
            results.append(f"Beschreibung: {agent['description'] or '-'}")

            # Synergien
            cursor.execute("""
                SELECT a2.name, s.synergy_type, s.description
                FROM agent_synergies s
                JOIN agents a2 ON s.agent_b_id = a2.id
                WHERE s.agent_a_id = ?
            """, (agent['id'],))
            synergies = cursor.fetchall()
            if synergies:
                results.append("\nSynergien:")
                for s in synergies:
                    results.append(f"  -> {s['name']} ({s['synergy_type']})")
        else:
            # Fallback: in bach_experts suchen
            try:
                cursor.execute("""
                    SELECT * FROM bach_experts
                    WHERE name LIKE ? OR id = ?
                """, (f"%{name}%", name if name.isdigit() else -1))
                expert = cursor.fetchone()
            except sqlite3.OperationalError:
                expert = None

            if expert:
                results = [f"EXPERTE: {expert['name']}", "=" * 40]
                results.append(f"ID:           {expert['id']}")
                results.append(f"Aktiv:        {'Ja' if expert['is_active'] else 'Nein'}")
                results.append(f"Beschreibung: {expert.get('description') or '-'}")
                results.append(f"Domain:       {expert.get('domain') or '-'}")
                results.append(f"Skill-Pfad:   {expert.get('skill_path') or '-'}")
            else:
                conn.close()
                return False, f"Agent/Experte nicht gefunden: {name}"

        conn.close()
        return True, "\n".join(results)
