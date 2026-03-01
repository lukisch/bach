#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration 024: Memory-Migration Stufe D (SQ043)

Kopiert Daten aus den alten memory_* Tabellen in die neuen shared_memory_* Tabellen.
Laeuft idempotent — bereits migrierte Daten werden uebersprungen.

Quell-Tabellen:
  memory_sessions -> shared_memory_sessions
  context_triggers -> shared_context_triggers
  memory_facts -> shared_memory_facts
  memory_lessons -> shared_memory_lessons

Alte Tabellen werden NICHT geloescht (deprecated, aber kompatibel).
"""


def run(conn):
    """Hauptmigration (wird von setup.py aufgerufen)."""
    cursor = conn.cursor()

    # 1. memory_sessions -> shared_memory_sessions
    count = _migrate_sessions(cursor)
    print(f"     Sessions migriert: {count}")

    # 2. context_triggers -> shared_context_triggers
    count = _migrate_triggers(cursor)
    print(f"     Triggers migriert: {count}")

    # 3. memory_facts -> shared_memory_facts
    count = _migrate_facts(cursor)
    print(f"     Facts migriert: {count}")

    # 4. memory_lessons -> shared_memory_lessons
    count = _migrate_lessons(cursor)
    print(f"     Lessons migriert: {count}")

    conn.commit()


def _migrate_sessions(cursor):
    """memory_sessions -> shared_memory_sessions"""
    # Pruefen ob Quelltabelle existiert und Daten hat
    try:
        cursor.execute("SELECT COUNT(*) FROM memory_sessions")
        source_count = cursor.fetchone()[0]
        if source_count == 0:
            return 0
    except Exception:
        return 0

    # Bereits migrierte zaehlen
    cursor.execute("SELECT COUNT(*) FROM shared_memory_sessions")
    existing = cursor.fetchone()[0]
    if existing >= source_count:
        return 0  # Bereits migriert

    # Spaltennamen der Quelltabelle ermitteln
    cursor.execute("PRAGMA table_info(memory_sessions)")
    src_cols = {row[1] for row in cursor.fetchall()}

    # Nur Spalten uebernehmen die in beiden Tabellen existieren
    cursor.execute("PRAGMA table_info(shared_memory_sessions)")
    dst_cols = {row[1] for row in cursor.fetchall()}

    # Mapping: Alte Spalten -> Neue Spalten
    common_cols = src_cols & dst_cols - {'id'}

    if not common_cols:
        # Fallback: Minimale Migration
        cursor.execute("""
            INSERT OR IGNORE INTO shared_memory_sessions
                (session_id, agent_id, started_at, summary, created_at)
            SELECT
                COALESCE(session_id, 'legacy-' || id),
                COALESCE(agent_id, 'system'),
                COALESCE(started_at, created_at, datetime('now')),
                summary,
                COALESCE(created_at, datetime('now'))
            FROM memory_sessions
            WHERE id NOT IN (SELECT CAST(REPLACE(session_id, 'legacy-', '') AS INTEGER) FROM shared_memory_sessions WHERE session_id LIKE 'legacy-%')
        """)
    else:
        cols_str = ", ".join(sorted(common_cols))
        cursor.execute(f"""
            INSERT OR IGNORE INTO shared_memory_sessions ({cols_str})
            SELECT {cols_str} FROM memory_sessions
        """)

    return cursor.rowcount


def _migrate_triggers(cursor):
    """context_triggers -> shared_context_triggers"""
    try:
        cursor.execute("SELECT COUNT(*) FROM context_triggers")
        source_count = cursor.fetchone()[0]
        if source_count == 0:
            return 0
    except Exception:
        return 0

    cursor.execute("SELECT COUNT(*) FROM shared_context_triggers")
    if cursor.fetchone()[0] >= source_count:
        return 0

    # Spalten ermitteln
    cursor.execute("PRAGMA table_info(context_triggers)")
    src_cols = {row[1] for row in cursor.fetchall()}
    cursor.execute("PRAGMA table_info(shared_context_triggers)")
    dst_cols = {row[1] for row in cursor.fetchall()}

    common_cols = src_cols & dst_cols - {'id'}

    if 'agent_id' not in src_cols:
        # Alte Tabelle hat kein agent_id -> Default setzen
        cursor.execute("""
            INSERT OR IGNORE INTO shared_context_triggers
                (agent_id, trigger_phrase, hint_text, source, is_active, created_at)
            SELECT
                'system',
                trigger_phrase,
                hint_text,
                COALESCE(source, 'migrated'),
                COALESCE(is_active, 1),
                COALESCE(created_at, datetime('now'))
            FROM context_triggers
        """)
    elif common_cols:
        cols_str = ", ".join(sorted(common_cols))
        cursor.execute(f"""
            INSERT OR IGNORE INTO shared_context_triggers ({cols_str})
            SELECT {cols_str} FROM context_triggers
        """)

    return cursor.rowcount


def _migrate_facts(cursor):
    """memory_facts -> shared_memory_facts"""
    try:
        cursor.execute("SELECT COUNT(*) FROM memory_facts")
        source_count = cursor.fetchone()[0]
        if source_count == 0:
            return 0
    except Exception:
        return 0

    cursor.execute("SELECT COUNT(*) FROM shared_memory_facts")
    if cursor.fetchone()[0] >= source_count:
        return 0

    cursor.execute("""
        INSERT OR IGNORE INTO shared_memory_facts
            (agent_id, namespace, category, key, value, source, created_by, created_at)
        SELECT
            'system', 'global',
            COALESCE(category, 'general'),
            COALESCE(key, 'fact_' || id),
            value,
            'migrated',
            'migration_024',
            COALESCE(created_at, datetime('now'))
        FROM memory_facts
    """)
    return cursor.rowcount


def _migrate_lessons(cursor):
    """memory_lessons -> shared_memory_lessons"""
    try:
        cursor.execute("SELECT COUNT(*) FROM memory_lessons")
        source_count = cursor.fetchone()[0]
        if source_count == 0:
            return 0
    except Exception:
        return 0

    cursor.execute("SELECT COUNT(*) FROM shared_memory_lessons")
    if cursor.fetchone()[0] >= source_count:
        return 0

    cursor.execute("""
        INSERT OR IGNORE INTO shared_memory_lessons
            (agent_id, namespace, category, title, solution, source, created_by, created_at)
        SELECT
            'system', 'global',
            COALESCE(category, 'general'),
            COALESCE(title, 'Lesson ' || id),
            COALESCE(solution, content, ''),
            'migrated',
            'migration_024',
            COALESCE(created_at, datetime('now'))
        FROM memory_lessons
    """)
    return cursor.rowcount


# Standalone-Aufruf
if __name__ == "__main__":
    import sqlite3
    import sys
    from pathlib import Path

    db_path = Path(__file__).parent.parent / "bach.db"
    if not db_path.exists():
        print(f"bach.db nicht gefunden: {db_path}")
        sys.exit(1)

    conn = sqlite3.connect(str(db_path))
    run(conn)
    conn.close()
    print("Migration abgeschlossen.")
