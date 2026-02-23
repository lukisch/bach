#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Test-Skript für sqlite-vec Installation und Funktionalität (SQ064)
===================================================================

Prüft:
1. Ob sqlite-vec installiert ist
2. Ob sqlite-vec mit sqlite3 kompatibel ist
3. Basis-Vektorsuche Funktionalität

Installation:
    pip install sqlite-vec

Referenz: https://github.com/asg017/sqlite-vec
"""

import sqlite3
from pathlib import Path


def test_sqlite_vec_import():
    """Test 1: Prüft ob sqlite-vec importierbar ist."""
    print("=== Test 1: sqlite-vec Import ===")
    try:
        import sqlite_vec
        print(f"[OK] sqlite-vec ist installiert")
        if hasattr(sqlite_vec, "__version__"):
            print(f"[OK] Version: {sqlite_vec.__version__}")
        else:
            print("[INFO] Version unbekannt (kein __version__ Attribut)")
        return True
    except ImportError as e:
        print(f"[FAIL] sqlite-vec ist NICHT installiert: {e}")
        print("[INFO] Installation: pip install sqlite-vec")
        return False


def test_sqlite_vec_extension():
    """Test 2: Prüft ob sqlite-vec Extension geladen werden kann."""
    print("\n=== Test 2: sqlite-vec Extension laden ===")
    try:
        import sqlite_vec

        # In-Memory DB für Test
        conn = sqlite3.connect(":memory:")

        # Extension laden
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)

        print("[OK] sqlite-vec Extension erfolgreich geladen")

        # Prüfen ob vec0 Funktion verfügbar
        cursor = conn.cursor()
        cursor.execute("SELECT vec_version()")
        version = cursor.fetchone()[0]
        print(f"[OK] vec_version(): {version}")

        conn.close()
        return True

    except Exception as e:
        print(f"[FAIL] Extension konnte nicht geladen werden: {e}")
        return False


def test_basic_vector_search():
    """Test 3: Basis-Vektorsuche Test."""
    print("\n=== Test 3: Basis-Vektorsuche ===")
    try:
        import sqlite_vec

        conn = sqlite3.connect(":memory:")
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)

        cursor = conn.cursor()

        # Virtual Table erstellen
        cursor.execute("""
            CREATE VIRTUAL TABLE vec_items USING vec0(
                id INTEGER PRIMARY KEY,
                embedding FLOAT[3]
            )
        """)

        # Test-Daten einfügen
        cursor.execute("INSERT INTO vec_items(id, embedding) VALUES (1, '[1.0, 0.0, 0.0]')")
        cursor.execute("INSERT INTO vec_items(id, embedding) VALUES (2, '[0.0, 1.0, 0.0]')")
        cursor.execute("INSERT INTO vec_items(id, embedding) VALUES (3, '[0.0, 0.0, 1.0]')")

        conn.commit()

        # Ähnlichkeitssuche (Cosine Distance)
        query_vec = "[1.0, 0.0, 0.0]"
        cursor.execute("""
            SELECT id, distance
            FROM vec_items
            WHERE embedding MATCH ?
            ORDER BY distance
            LIMIT 3
        """, (query_vec,))

        results = cursor.fetchall()
        print(f"[OK] Vektorsuche erfolgreich: {len(results)} Ergebnisse")

        for id, distance in results:
            print(f"  ID: {id}, Distance: {distance:.4f}")

        conn.close()
        return True

    except Exception as e:
        print(f"[FAIL] Vektorsuche fehlgeschlagen: {e}")
        return False


def test_bach_db_integration():
    """Test 4: Integration mit bach.db (falls vorhanden)."""
    print("\n=== Test 4: bach.db Integration ===")

    db_path = Path(__file__).parent.parent / "data" / "bach.db"
    if not db_path.exists():
        print("[SKIP] bach.db nicht gefunden")
        return True

    try:
        import sqlite_vec

        conn = sqlite3.connect(str(db_path))
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)

        # Prüfen ob vec_version() funktioniert
        cursor = conn.cursor()
        cursor.execute("SELECT vec_version()")
        version = cursor.fetchone()[0]
        print(f"[OK] sqlite-vec in bach.db geladen: {version}")

        conn.close()
        return True

    except Exception as e:
        print(f"[FAIL] Integration mit bach.db fehlgeschlagen: {e}")
        return False


def run_all_tests():
    """Führt alle Tests aus."""
    print("=" * 60)
    print("sqlite-vec Installation & Funktionstest (SQ064)")
    print("=" * 60)
    print()

    results = []

    # Test 1: Import
    results.append(("Import", test_sqlite_vec_import()))

    # Nur weitermachen wenn Import erfolgreich
    if results[0][1]:
        results.append(("Extension laden", test_sqlite_vec_extension()))
        results.append(("Basis-Vektorsuche", test_basic_vector_search()))
        results.append(("bach.db Integration", test_bach_db_integration()))
    else:
        print("\n[SKIP] Weitere Tests übersprungen (sqlite-vec nicht installiert)")

    # Zusammenfassung
    print()
    print("=" * 60)
    print("Zusammenfassung:")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[OK]" if result else "[FAIL]"
        print(f"{status} {name}")

    print()
    print(f"Ergebnis: {passed}/{total} Tests bestanden")

    if passed == total:
        print("[SUCCESS] Alle Tests erfolgreich!")
        return 0
    else:
        print("[PARTIAL] Einige Tests fehlgeschlagen")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(run_all_tests())
