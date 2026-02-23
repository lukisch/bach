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
Tool: c_sync_registry
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version c_sync_registry

Description:
    [Beschreibung hinzufügen]

Usage:
    python c_sync_registry.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

import sqlite3
import json
from pathlib import Path
from datetime import datetime

class RegistrySync:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.db_path = self.root / "data" / "bach.db"
        self.tools_json = self.root / "data" / "registries" / "tool_registry.json"
        self.skills_json = self.root / "data" / "registries" / "skill_registry.json"

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def sync_tools(self):
        print("\n[SYNC] Starte Tool-Synchronisation...")
        if not self.tools_json.exists():
            print(f"WARN: {self.tools_json} nicht gefunden.")
            return

        with open(self.tools_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            json_tools = data.get("tools", {})

        conn = self._get_conn()
        cur = conn.cursor()
        
        # 1. Update/Insert aus JSON
        for name, info in json_tools.items():
            now = datetime.now().isoformat()
            cur.execute("""
                INSERT INTO tools (name, type, category, path, description, updated_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    type=excluded.type,
                    category=excluded.category,
                    path=excluded.path,
                    description=excluded.description,
                    updated_at=excluded.updated_at
            """, (name, info.get("type", "unknown"), info.get("category"), info.get("path"), info.get("description"), now, now))
        
        # 2. Löschen was nicht mehr im JSON ist (optional, konfigurierbar)
        # cur.execute("DELETE FROM tools WHERE name NOT IN (" + ",".join(["?"]*len(json_tools)) + ")", list(json_tools.keys()))
        
        conn.commit()
        conn.close()
        print(f"[OK] {len(json_tools)} Tools synchronisiert.")

    def sync_skills(self):
        print("\n[SYNC] Starte Skill-Synchronisation...")
        if not self.skills_json.exists():
            print(f"WARN: {self.skills_json} nicht gefunden.")
            return

        with open(self.skills_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            json_skills = data.get("skills", {})

        conn = self._get_conn()
        cur = conn.cursor()
        
        for name, info in json_skills.items():
            now = datetime.now().isoformat()
            cur.execute("""
                INSERT INTO skills (name, type, category, path, description, updated_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    type=excluded.type,
                    category=excluded.category,
                    path=excluded.path,
                    description=excluded.description,
                    updated_at=excluded.updated_at
            """, (name, info.get("type", "unknown"), info.get("category"), info.get("path"), info.get("description"), now, now))
            
        conn.commit()
        conn.close()
        print(f"[OK] {len(json_skills)} Skills synchronisiert.")

if __name__ == "__main__":
    sync = RegistrySync()
    sync.sync_tools()
    sync.sync_skills()
