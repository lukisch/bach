#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: trigger_maintainer
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version trigger_maintainer

Description:
    [Beschreibung hinzufügen]

Usage:
    python trigger_maintainer.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

# Pfade
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "bach.db"

def run_maintenance():
    if not DB_PATH.exists():
        print("[ERROR] Datenbank nicht gefunden.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    print("Starte Trigger-Wartung (Decay & Boost)...")
    
    # 1. BOOST: Confidence erhöhen basierend auf Nutzung
    # Wir nehmen an: 10 Nutzungen = +0.1 Confidence, Start bei 0.5
    cursor.execute("""
        UPDATE context_triggers 
        SET confidence = MIN(1.0, 0.5 + (usage_count * 0.01)),
            updated_at = CURRENT_TIMESTAMP
        WHERE is_active = 1 AND usage_count > 0
    """)
    boosted = cursor.rowcount
    
    # 2. DECAY: Deaktivieren wenn lange nicht genutzt
    # Aber nur wenn sie nicht 'manual' sind (User-Triggers schützen)
    # Und nur wenn sie eine gewisse Zeit existieren (created_at)
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
    
    cursor.execute("""
        UPDATE context_triggers
        SET is_active = 0, updated_at = CURRENT_TIMESTAMP
        WHERE is_active = 1 
        AND is_protected = 0
        AND source != 'manual'
        AND last_used IS NOT NULL 
        AND last_used < ?
    """, (thirty_days_ago,))
    decayed = cursor.rowcount
    
    # Spezialfall: Nie genutzte Trigger nach 60 Tagen deaktivieren
    sixty_days_ago = (datetime.now() - timedelta(days=60)).isoformat()
    cursor.execute("""
        UPDATE context_triggers
        SET is_active = 0, updated_at = CURRENT_TIMESTAMP
        WHERE is_active = 1
        AND is_protected = 0
        AND source != 'manual'
        AND last_used IS NULL
        AND created_at < ?
    """, (sixty_days_ago,))
    never_used_decayed = cursor.rowcount

    conn.commit()
    conn.close()
    
    print(f"[OK] Boost: {boosted} Trigger optimiert.")
    print(f"[OK] Decay: {decayed + never_used_decayed} inaktive Trigger abgeschaltet.")

if __name__ == "__main__":
    run_maintenance()
