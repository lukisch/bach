#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
memory_working_cleanup.py - Working Memory Cleanup Tool
========================================================

Bereinigt memory_working nach Expires-Regeln.

CLI:
    python memory_working_cleanup.py analyze     Analysiere Einträge
    python memory_working_cleanup.py cleanup     Soft Delete expired
    python memory_working_cleanup.py --dry-run   Zeige was gelöscht würde

Teil von SQ043: Memory-DB & Partner-Vernetzung
Referenz: BACH_Dev/docs/MEMORY_WORKING_CLEANUP_KONZEPT.md
"""

from pathlib import Path
from datetime import datetime, timedelta
import sqlite3


class WorkingMemoryCleanup:
    """Working Memory Cleanup & Analyse."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)

    def analyze(self, dry_run: bool = True) -> tuple[bool, str]:
        """Analysiert memory_working Einträge.

        Args:
            dry_run: Wird ignoriert (analyze ändert keine Daten)

        Returns:
            (success, message): Erfolgs-Status und formatierte Statistik
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Alle Einträge mit Alter
        cursor.execute("""
            SELECT
                id,
                type,
                content,
                priority,
                created_at,
                julianday('now') - julianday(created_at) as age_days,
                expires_at,
                is_active
            FROM memory_working
            ORDER BY created_at DESC
        """)
        entries = cursor.fetchall()
        conn.close()

        # Kategorisierung
        stats = {
            'total': len(entries),
            'keep': 0,
            'review': 0,
            'archive': 0,
            'by_age': {'< 7d': 0, '7-14d': 0, '> 14d': 0},
            'entries': []
        }

        for id, typ, content, priority, created_at, age_days, expires_at, is_active in entries:
            # Aktion bestimmen
            if age_days < 7:
                action = 'KEEP'
                stats['keep'] += 1
                stats['by_age']['< 7d'] += 1
            elif age_days < 14:
                action = 'REVIEW'
                stats['review'] += 1
                stats['by_age']['7-14d'] += 1
            else:
                action = 'ARCHIVE'
                stats['archive'] += 1
                stats['by_age']['> 14d'] += 1

            stats['entries'].append({
                'id': id,
                'type': typ,
                'content': content[:80] if content else "",
                'priority': priority,
                'age_days': round(age_days, 1),
                'action': action,
                'expires_at': expires_at,
                'is_active': is_active
            })

        # Formatiere Ausgabe
        msg = f"""
Working Memory Analyse
═══════════════════════════════════════════════════════════

GESAMT: {stats['total']} Einträge

EMPFEHLUNGEN:
  ✓ KEEP    (< 7 Tage):   {stats['keep']:3d}
  ⚠ REVIEW  (7-14 Tage):  {stats['review']:3d}
  📦 ARCHIVE (> 14 Tage): {stats['archive']:3d}

ALTER-VERTEILUNG:
  < 7 Tage:   {stats['by_age']['< 7d']:3d}
  7-14 Tage:  {stats['by_age']['7-14d']:3d}
  > 14 Tage:  {stats['by_age']['> 14d']:3d}

[TIPP] bach mem working cleanup --dry-run
"""
        return True, msg.strip()

    def set_expires_retroactive(self, dry_run: bool = True) -> tuple[bool, str]:
        """Setzt Expires rückwirkend für alle Einträge ohne Expires."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Zähle Einträge ohne Expires
        cursor.execute("SELECT COUNT(*) FROM memory_working WHERE expires_at IS NULL")
        count_null = cursor.fetchone()[0]

        if count_null == 0:
            conn.close()
            return True, "✓ Alle Einträge haben bereits expires_at gesetzt"

        if dry_run:
            conn.close()
            return True, f"[DRY-RUN] Würde {count_null} Einträgen expires_at setzen"

        # Setze Expires basierend auf Alter
        # < 7 Tage: +7 Tage ab jetzt
        cursor.execute("""
            UPDATE memory_working
            SET expires_at = datetime('now', '+7 days')
            WHERE julianday('now') - julianday(created_at) < 7
            AND expires_at IS NULL
        """)
        recent_updated = cursor.rowcount

        # >= 7 Tage: SOFORT (zur Review)
        cursor.execute("""
            UPDATE memory_working
            SET expires_at = datetime('now')
            WHERE julianday('now') - julianday(created_at) >= 7
            AND expires_at IS NULL
        """)
        old_updated = cursor.rowcount

        conn.commit()
        conn.close()

        return True, f"✓ Expires gesetzt: {recent_updated} recent (+7d), {old_updated} old (now)"

    def cleanup_soft(self, dry_run: bool = True) -> tuple[bool, str]:
        """Soft Delete (is_active=0) für expired Einträge."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Zähle expired Einträge
        cursor.execute("""
            SELECT COUNT(*)
            FROM memory_working
            WHERE expires_at < datetime('now')
            AND is_active = 1
        """)
        count_expired = cursor.fetchone()[0]

        if count_expired == 0:
            conn.close()
            return True, "✓ Keine expired Einträge zum Bereinigen"

        if dry_run:
            conn.close()
            return True, f"[DRY-RUN] Würde {count_expired} expired Einträge soft-deleten"

        # Soft Delete
        cursor.execute("""
            UPDATE memory_working
            SET is_active = 0
            WHERE expires_at < datetime('now')
            AND is_active = 1
        """)

        conn.commit()
        conn.close()

        return True, f"✓ {count_expired} expired Einträge soft-deleted (is_active=0)"


def print_analysis(stats: dict):
    """Druckt Analyse-Ergebnisse."""
    print("=" * 70)
    print("WORKING MEMORY ANALYSE")
    print("=" * 70)
    print("")
    print(f"Total Einträge:  {stats['total']}")
    print("")
    print("AKTIONEN:")
    print(f"  KEEP (< 7 Tage):      {stats['keep']:<3} ({stats['by_age']['< 7d']})")
    print(f"  REVIEW (7-14 Tage):   {stats['review']:<3} ({stats['by_age']['7-14d']})")
    print(f"  ARCHIVE (> 14 Tage):  {stats['archive']:<3} ({stats['by_age']['> 14d']})")
    print("")

    # Top 10 älteste
    print("TOP 10 ÄLTESTE EINTRÄGE:")
    print("-" * 70)
    oldest = sorted(stats['entries'], key=lambda x: x['age_days'], reverse=True)[:10]
    for entry in oldest:
        age = entry['age_days']
        action = entry['action']
        content = entry['content'][:60]
        print(f"  [{action:7}] {age:5.1f}d | {content}")
    print("")


def main():
    """CLI Entry Point."""
    import sys

    # Bach-Root ermitteln
    bach_root = Path(__file__).parent.parent
    db_path = bach_root / "data" / "bach.db"

    if not db_path.exists():
        print(f"[ERROR] DB nicht gefunden: {db_path}")
        sys.exit(1)

    cleanup = WorkingMemoryCleanup(db_path)

    # Kommando
    cmd = sys.argv[1] if len(sys.argv) > 1 else "analyze"
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv

    if cmd == "analyze":
        stats = cleanup.analyze()
        print_analysis(stats)

    elif cmd == "set-expires":
        success, msg = cleanup.set_expires_retroactive(dry_run=dry_run)
        print(msg)

    elif cmd == "cleanup":
        success, msg = cleanup.cleanup_soft(dry_run=dry_run)
        print(msg)

    else:
        print("Usage: python memory_working_cleanup.py <command> [--dry-run]")
        print("")
        print("Commands:")
        print("  analyze          Analysiere memory_working Einträge")
        print("  set-expires      Setze Expires rückwirkend")
        print("  cleanup          Soft Delete expired Einträge")
        sys.exit(1)


if __name__ == "__main__":
    main()
