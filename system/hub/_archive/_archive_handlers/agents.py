# SPDX-License-Identifier: MIT
"""
Agents Handler - Agenten-Verwaltung
===================================

--agents list        Alle Agenten auflisten
--agents info <n> Agenten-Details
--agents active      Nur aktive Agenten
"""
import sqlite3
from pathlib import Path
from .base import BaseHandler


class AgentsHandler(BaseHandler):
    """Handler fuer --agents Operationen"""
    
    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.db_path = base_path / "data" / "bach.db"
    
    @property
    def profile_name(self) -> str:
        return "agents"
    
    @property
    def target_file(self) -> Path:
        return self.db_path
    
    def get_operations(self) -> dict:
        return {
            "list": "Alle Agenten auflisten",
            "info": "Agenten-Details anzeigen",
            "active": "Nur aktive Agenten"
        }
    
    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if not self.db_path.exists():
            return False, "Datenbank nicht gefunden"
        
        if operation == "info" and args:
            return self._info(args[0])
        elif operation == "active":
            return self._list(active_only=True)
        else:
            return self._list(active_only=False)
    
    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _list(self, active_only: bool) -> tuple:
        """Agenten auflisten - aus DB UND Dateisystem."""
        results = ["AGENTEN", "=" * 40]
        
        # 1. Aus Dateisystem (agents/)
        skills_agents_dir = self.base_path / "skills" / "_agents"
        file_agents = {}
        
        if skills_agents_dir.exists():
            for skill_file in skills_agents_dir.glob("*.txt"):
                name = skill_file.stem
                file_agents[name.lower()] = {
                    'name': name,
                    'file': skill_file,
                    'in_db': False
                }
        
        # 2. Aus Datenbank
        db_agents = []
        if self.db_path.exists():
            try:
                conn = self._get_conn()
                cursor = conn.cursor()
                
                if active_only:
                    cursor.execute("""
                        SELECT name, type, description, is_active
                        FROM agents WHERE is_active = 1
                        ORDER BY name
                    """)
                else:
                    cursor.execute("""
                        SELECT name, type, description, is_active
                        FROM agents ORDER BY name
                    """)
                
                db_agents = cursor.fetchall()
                conn.close()
                
                # Markiere welche auch in DB sind
                for a in db_agents:
                    key = a['name'].lower()
                    if key in file_agents:
                        file_agents[key]['in_db'] = True
                        file_agents[key]['type'] = a['type']
                        file_agents[key]['is_active'] = a['is_active']
                    else:
                        # Nur in DB, nicht als Skill-Datei
                        file_agents[key] = {
                            'name': a['name'],
                            'file': None,
                            'in_db': True,
                            'type': a['type'],
                            'is_active': a['is_active']
                        }
            except Exception as e:
                results.append(f"[DB-Fehler: {e}]")
        
        # 3. Ausgabe
        if not file_agents:
            results.append("Keine Agenten gefunden.")
        else:
            results.append("\n[SKILL-DATEIEN + DB]")
            for key, agent in sorted(file_agents.items()):
                # Status-Icon
                if agent.get('in_db') and agent.get('is_active'):
                    status = "[X]"  # In DB und aktiv
                elif agent.get('in_db'):
                    status = "[-]"  # In DB aber inaktiv
                else:
                    status = "[ ]"  # Nur als Datei, nicht in DB
                
                # Typ wenn bekannt
                type_str = f" ({agent.get('type', 'skill')})" if agent.get('type') else ""
                
                # CLI-Hinweis wenn eigener Handler existiert
                cli_hint = ""
                if "steuer" in key:
                    cli_hint = " -> --steuer"
                
                results.append(f"  {status} {agent['name']}{type_str}{cli_hint}")
        
        results.append("\n" + "=" * 40)
        results.append("Legende: [X]=DB+aktiv [-]=DB+inaktiv [ ]=nur Skill-Datei")
        results.append("\nDetails: --agents info <n>")
        
        return True, "\n".join(results)
    
    def _info(self, name: str) -> tuple:
        """Agenten-Details."""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM agents 
            WHERE name LIKE ? OR id = ?
        """, (f"%{name}%", name if name.isdigit() else -1))
        
        agent = cursor.fetchone()
        
        if not agent:
            conn.close()
            return False, f"Agent nicht gefunden: {name}"
        
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
        
        conn.close()
        return True, "\n".join(results)
