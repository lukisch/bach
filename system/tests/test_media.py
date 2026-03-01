#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests fuer MediaBrain Integration (INT03)

Testet: media.py Handler-Operationen
"""

import sys
import json
import sqlite3
import pytest
from pathlib import Path

BACH_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(BACH_ROOT))

from hub.media import MediaHandler, MEDIA_TYPES, SOURCES

MIGRATION_SQL = BACH_ROOT / "data" / "schema" / "migrations" / "027_media_integration.sql"


@pytest.fixture
def tmp_db(tmp_path):
    db_path = tmp_path / "test_bach.db"
    conn = sqlite3.connect(str(db_path))
    conn.executescript(MIGRATION_SQL.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def handler(tmp_db):
    import shutil
    base = tmp_db.parent / "system"
    data_dir = base / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(tmp_db), str(data_dir / "bach.db"))
    return MediaHandler(base)


@pytest.fixture
def seeded(handler):
    """Handler mit 3 Medien."""
    handler.handle("add", ["Inception", "--type", "movie", "--source", "netflix", "--rating", "5"])
    handler.handle("add", ["Dark", "--type", "series", "--source", "netflix", "--season", "1"])
    handler.handle("add", ["Bohemian Rhapsody", "--type", "music", "--source", "spotify", "--artist", "Queen"])
    return handler


# ================================================================
# ADD
# ================================================================

class TestAdd:
    def test_add_basic(self, handler):
        ok, txt = handler.handle("add", ["Test Movie", "--type", "movie"])
        assert ok
        assert "Test Movie" in txt

    def test_add_no_args(self, handler):
        ok, txt = handler.handle("add", [])
        assert not ok
        assert "Usage" in txt

    def test_add_with_all_fields(self, handler):
        ok, txt = handler.handle("add", [
            "Full Item", "--type", "music", "--source", "spotify",
            "--artist", "Artist", "--album", "Album", "--rating", "4",
            "--tags", "rock,classic"
        ])
        assert ok

    def test_add_invalid_type(self, handler):
        ok, txt = handler.handle("add", ["X", "--type", "invalid"])
        assert not ok
        assert "Unbekannter Typ" in txt

    def test_add_invalid_source(self, handler):
        ok, txt = handler.handle("add", ["X", "--source", "invalid"])
        assert not ok
        assert "Unbekannte Quelle" in txt


# ================================================================
# LIST
# ================================================================

class TestList:
    def test_list_empty(self, handler):
        ok, txt = handler.handle("list", [])
        assert ok
        assert "Keine Medien" in txt

    def test_list_with_data(self, seeded):
        ok, txt = seeded.handle("list", [])
        assert ok
        assert "3" in txt
        assert "Inception" in txt

    def test_list_filter_type(self, seeded):
        ok, txt = seeded.handle("list", ["--type", "movie"])
        assert ok
        assert "Inception" in txt
        assert "Dark" not in txt

    def test_list_filter_source(self, seeded):
        ok, txt = seeded.handle("list", ["--source", "spotify"])
        assert ok
        assert "Bohemian" in txt
        assert "Inception" not in txt

    def test_list_fav(self, seeded):
        seeded.handle("fav", ["1"])
        ok, txt = seeded.handle("list", ["--fav"])
        assert ok
        assert "Inception" in txt
        assert "Dark" not in txt

    def test_list_excludes_blacklisted(self, seeded):
        seeded.handle("blacklist", ["2"])
        ok, txt = seeded.handle("list", [])
        assert ok
        assert "Dark" not in txt


# ================================================================
# SEARCH
# ================================================================

class TestSearch:
    def test_search_found(self, seeded):
        ok, txt = seeded.handle("search", ["Inception"])
        assert ok
        assert "Inception" in txt

    def test_search_by_artist(self, seeded):
        ok, txt = seeded.handle("search", ["Queen"])
        assert ok
        assert "Bohemian" in txt

    def test_search_not_found(self, seeded):
        ok, txt = seeded.handle("search", ["nonexistent"])
        assert ok
        assert "Keine Treffer" in txt


# ================================================================
# SHOW
# ================================================================

class TestShow:
    def test_show(self, seeded):
        ok, txt = seeded.handle("show", ["1"])
        assert ok
        assert "Inception" in txt
        assert "movie" in txt
        assert "netflix" in txt

    def test_show_not_found(self, handler):
        ok, txt = handler.handle("show", ["999"])
        assert not ok


# ================================================================
# EDIT
# ================================================================

class TestEdit:
    def test_edit(self, seeded):
        ok, txt = seeded.handle("edit", ["1", "--title", "Inception (2010)", "--rating", "4"])
        assert ok
        assert "aktualisiert" in txt

    def test_edit_not_found(self, handler):
        ok, txt = handler.handle("edit", ["999", "--title", "X"])
        assert not ok


# ================================================================
# FAV
# ================================================================

class TestFav:
    def test_set_fav(self, seeded):
        ok, txt = seeded.handle("fav", ["1"])
        assert ok
        assert "gesetzt" in txt

    def test_remove_fav(self, seeded):
        seeded.handle("fav", ["1"])
        ok, txt = seeded.handle("fav", ["1", "--remove"])
        assert ok
        assert "entfernt" in txt


# ================================================================
# BLACKLIST
# ================================================================

class TestBlacklist:
    def test_blacklist(self, seeded):
        ok, txt = seeded.handle("blacklist", ["2"])
        assert ok
        assert "Gesperrt" in txt

    def test_unblacklist(self, seeded):
        seeded.handle("blacklist", ["2"])
        ok, txt = seeded.handle("blacklist", ["2", "--remove"])
        assert ok
        assert "entfernt" in txt


# ================================================================
# HISTORY
# ================================================================

class TestHistory:
    def test_history_empty(self, handler):
        ok, txt = handler.handle("history", [])
        assert ok
        assert "Keine Wiedergabe" in txt

    def test_history_after_open(self, seeded):
        # open ohne URL/Pfad markiert trotzdem Wiedergabe
        seeded.handle("open", ["1"])
        ok, txt = seeded.handle("history", [])
        assert ok
        assert "Inception" in txt


# ================================================================
# STATS
# ================================================================

class TestStats:
    def test_stats_empty(self, handler):
        ok, txt = handler.handle("stats", [])
        assert ok
        assert "leer" in txt

    def test_stats_with_data(self, seeded):
        ok, txt = seeded.handle("stats", [])
        assert ok
        assert "3" in txt
        assert "movie" in txt
        assert "netflix" in txt


# ================================================================
# HANDLER META
# ================================================================

class TestMeta:
    def test_operations_count(self, handler):
        ops = handler.get_operations()
        assert len(ops) == 11

    def test_help(self, handler):
        ok, txt = handler.handle("help", [])
        assert ok
        assert "MEDIENVERWALTUNG" in txt
