# SPDX-License-Identifier: MIT
"""
DB Handler - Datenbank-Operationen
==================================

--db status      Tabellen-Uebersicht
--db query "SQL" SQL-Query ausfuehren
--db tables      Tabellen mit Counts
"""
import sqlite3
from pathlib import Path
from .base import BaseHandler


class DbHandler(BaseHandler):
    """Handler fuer --db Operationen"""
    
    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.db_path = base_path / "data" / "bach.db"
    
    @property
    def profile_name(self) -> str:
        return "db"
    
    @property
    def target_file(self) -> Path:
        return self.db_path
    
    def get_operations(self) -> dict:
        return {
            "status": "Datenbank-Status anzeigen",
            "tables": "Alle Tabellen mit Counts",
            "query": "SQL-Query ausfuehren"
        }
    
    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if not self.db_path.exists():
            return False, f"Datenbank nicht gefunden: {self.db_path}"
        
        if operation == "status" or not operation:
            return self._status()
        elif operation == "tables":
            return self._tables()
        elif operation == "query" and args:
            if dry_run:
                return True, f"[DRY-RUN] Query: {' '.join(args)}"
            return self._query(" ".join(args))
        else:
            return self._status()
    
    def _get_conn(self):
        """DB-Verbindung holen."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _status(self) -> tuple:
        """Datenbank-Status."""
        results = ["BACH DATABASE", "=" * 40]
        
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Tabellen zaehlen
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        tables = cursor.fetchall()
        results.append(f"Tabellen: {len(tables)}")
        
        # DB-Groesse
        size_kb = self.db_path.stat().st_size / 1024
        results.append(f"Groesse:  {size_kb:.1f} KB")
        
        # Identity
        try:
            cursor.execute("SELECT instance_name, version FROM system_identity WHERE id = 1")
            row = cursor.fetchone()
            if row:
                results.append(f"Instance: {row['instance_name']} v{row['version']}")
        except:
            pass
        
        conn.close()
        return True, "\n".join(results)
    
    def _tables(self) -> tuple:
        """Tabellen mit Counts."""
        results = ["TABELLEN", "=" * 40]
        
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = cursor.fetchall()
        
        for t in tables:
            name = t['name']
            cursor.execute(f"SELECT COUNT(*) as cnt FROM {name}")
            count = cursor.fetchone()['cnt']
            results.append(f"  {name:<30} {count:>6}")
        
        conn.close()
        return True, "\n".join(results)
    
    def _query(self, sql: str) -> tuple:
        """SQL-Query ausfuehren."""
        results = []
        
        conn = self._get_conn()
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            
            if sql.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                if rows:
                    # Header
                    keys = rows[0].keys()
                    results.append(" | ".join(keys))
                    results.append("-" * 50)
                    # Rows
                    for row in rows[:50]:
                        results.append(" | ".join(str(row[k]) for k in keys))
                    if len(rows) > 50:
                        results.append(f"... und {len(rows) - 50} weitere")
                else:
                    results.append("Keine Ergebnisse.")
            else:
                conn.commit()
                results.append(f"[OK] {cursor.rowcount} Zeilen betroffen.")
            
        except Exception as e:
            results.append(f"[FEHLER] {e}")
        
        conn.close()
        return True, "\n".join(results)
