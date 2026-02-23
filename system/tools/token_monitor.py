#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: token_monitor
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version token_monitor

Description:
    [Beschreibung hinzufügen]

Usage:
    python token_monitor.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional, Dict

# BACH-Pfade
BACH_ROOT = Path(__file__).parent.parent
DB_PATH = BACH_ROOT / "data" / "bach.db"

# Zonen-Grenzen (Prozent)
ZONE_THRESHOLDS = {
    1: (0, 70),      # 0-70%: Alle Partner
    2: (70, 85),     # 70-85%: Mittlere Sparsamkeit
    3: (85, 95),     # 85-95%: Nur lokale Partner
    4: (95, 100)     # 95-100%: Notfall
}

# Zonen-Beschreibungen
ZONE_DESCRIPTIONS = {
    1: "Alle Partner verfuegbar",
    2: "Mittlere Sparsamkeit - bevorzuge guenstige Partner",
    3: "Nur lokale Partner (Ollama)",
    4: "Notfall-Modus - nur kritische Delegationen"
}


def get_db_connection() -> sqlite3.Connection:
    """Erstellt DB-Verbindung."""
    return sqlite3.connect(str(DB_PATH))


def get_current_budget_percent() -> Optional[float]:
    """
    Holt aktuellen Token-Verbrauch in Prozent aus der DB.
    
    Returns:
        float: Budget-Prozent (0-100) oder None wenn keine Daten
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Neuesten Eintrag holen
        cur.execute("""
            SELECT budget_percent 
            FROM monitor_tokens 
            ORDER BY timestamp DESC 
            LIMIT 1
        """)
        
        row = cur.fetchone()
        conn.close()
        
        if row and row[0] is not None:
            return float(row[0])
        return None
        
    except Exception as e:
        print(f"[WARN] Token-Monitor DB-Fehler: {e}")
        return None


def get_token_zone(budget_percent: Optional[float] = None) -> Tuple[int, str, Dict]:
    """
    Ermittelt die aktuelle Token-Zone fuer Delegation-Entscheidungen.
    
    Args:
        budget_percent: Optional - Token-Verbrauch in %. 
                       Wenn None, wird aus DB gelesen.
    
    Returns:
        Tuple mit:
        - zone (int): Zone 1-4
        - description (str): Zonen-Beschreibung
        - details (dict): Zusaetzliche Infos
            - budget_percent: Aktueller Verbrauch
            - threshold_min: Untere Grenze der Zone
            - threshold_max: Obere Grenze der Zone
            - partners_allowed: Liste erlaubter Partner-Typen
    
    Beispiel:
        zone, desc, details = get_token_zone()
        print(f"Zone {zone}: {desc}")
        print(f"Budget: {details['budget_percent']:.1f}%")
    """
    # Budget ermitteln
    if budget_percent is None:
        budget_percent = get_current_budget_percent()
    
    # Default wenn keine Daten: Zone 1 (konservativ)
    if budget_percent is None:
        budget_percent = 0.0
    
    # Zone bestimmen
    zone = 1
    for z, (min_val, max_val) in ZONE_THRESHOLDS.items():
        if min_val <= budget_percent < max_val:
            zone = z
            break
    else:
        # >= 100%
        zone = 4
    
    # Partner-Typen pro Zone
    partners_by_zone = {
        1: ["all", "api", "local", "human"],
        2: ["local", "cheap_api", "human"],
        3: ["local", "human"],
        4: ["human"]  # Nur Notfall-Eskalation
    }
    
    threshold_min, threshold_max = ZONE_THRESHOLDS.get(zone, (95, 100))
    
    details = {
        "budget_percent": budget_percent,
        "threshold_min": threshold_min,
        "threshold_max": threshold_max,
        "partners_allowed": partners_by_zone.get(zone, ["human"]),
        "timestamp": datetime.now().isoformat()
    }
    
    return zone, ZONE_DESCRIPTIONS.get(zone, "Unbekannt"), details


def log_token_check(zone: int, budget_percent: float, session_id: str = None) -> bool:
    """
    Loggt Token-Check in die DB.
    
    Args:
        zone: Ermittelte Zone
        budget_percent: Aktueller Verbrauch
        session_id: Optional Session-ID
    
    Returns:
        bool: True wenn erfolgreich
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO monitor_tokens 
            (session_id, budget_percent, timestamp)
            VALUES (?, ?, ?)
        """, (session_id, budget_percent, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"[WARN] Token-Log Fehler: {e}")
        return False


def log_ollama_usage(prompt_tokens: int, completion_tokens: int, session_id: str = "ollama_session") -> bool:
    """
    Spezialisierte Funktion fuer Ollama (Gratis-Tokens).
    
    Args:
        prompt_tokens: Eingabe-Tokens
        completion_tokens: Ausgabe-Tokens
        session_id: Session-ID
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Hole letztes Budget-Level
        cur.execute("SELECT budget_percent FROM monitor_tokens ORDER BY timestamp DESC LIMIT 1")
        last_budget = cur.fetchone()
        budget = last_budget[0] if last_budget else 0.0
        
        cur.execute("""
            INSERT INTO monitor_tokens 
            (session_id, tokens_input, tokens_output, tokens_total, budget_percent, cost_eur, timestamp)
            VALUES (?, ?, ?, ?, ?, 0.0, ?)
        """, (session_id, prompt_tokens, completion_tokens, prompt_tokens + completion_tokens, budget, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[WARN] Ollama-Token-Log Fehler: {e}")
        return False


def check_emergency_shutdown(budget_percent: Optional[float] = None) -> Tuple[bool, str]:
    """
    Prueft ob Notfall-Shutdown bei 95%+ Token-Verbrauch noetig ist.
    
    Args:
        budget_percent: Optional - Token-Verbrauch in %. 
                       Wenn None, wird aus DB gelesen.
    
    Returns:
        Tuple mit:
        - should_shutdown (bool): True wenn Shutdown empfohlen
        - message (str): Warnmeldung oder OK-Status
    
    Beispiel:
        should_stop, msg = check_emergency_shutdown()
        if should_stop:
            print(msg)
            # Shutdown einleiten...
    
    Task: TOKEN_001
    """
    if budget_percent is None:
        budget_percent = get_current_budget_percent()
    
    if budget_percent is None:
        return False, "[OK] Keine Token-Daten - kein Shutdown noetig"
    
    if budget_percent >= 95:
        return True, f"""
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  NOTFALL: TOKEN-BUDGET KRITISCH ({budget_percent:.1f}%)              ║
╠══════════════════════════════════════════════════════════════╣
║  AKTION ERFORDERLICH:                                        ║
║  → Session SOFORT beenden (bach --shutdown)                  ║
║  → Nur kritische Aufgaben abschliessen                       ║
║  → Keine neuen Tasks starten                                 ║
╚══════════════════════════════════════════════════════════════╝
"""
    
    if budget_percent >= 85:
        return False, f"[WARN] Token-Budget bei {budget_percent:.1f}% - Session bald beenden"
    
    return False, f"[OK] Token-Budget bei {budget_percent:.1f}%"


def format_zone_status(zone: int, description: str, details: Dict) -> str:
    """
    Formatiert Zone-Status fuer CLI-Ausgabe.
    
    Returns:
        str: Formatierter Status-String
    """
    budget = details.get('budget_percent', 0)
    partners = ", ".join(details.get('partners_allowed', []))
    
    # Zone-Marker (ASCII-kompatibel fuer Windows)
    zone_marker = {1: "[OK]", 2: "[WARN]", 3: "[CRIT]", 4: "[STOP]"}
    marker = zone_marker.get(zone, "[?]")
    
    lines = [
        f"{marker} Token-Zone {zone}: {description}",
        f"   Budget: {budget:.1f}%",
        f"   Partner: {partners}"
    ]
    
    return "\n".join(lines)


# === CLI Interface ===

def main():
    """CLI-Einstiegspunkt fuer direkten Aufruf."""
    import sys
    
    zone, desc, details = get_token_zone()
    print(format_zone_status(zone, desc, details))
    
    # Exit-Code = Zone (fuer Scripting)
    sys.exit(zone)


if __name__ == "__main__":
    main()
