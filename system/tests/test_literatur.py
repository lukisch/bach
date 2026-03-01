#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests fuer LitZentrum Integration (INT01)

Testet: citation_formatter.py + literatur.py Handler-Operationen
"""

import os
import sys
import json
import sqlite3
import pytest
from pathlib import Path

# BACH system path
BACH_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(BACH_ROOT))

from hub._services.literatur.citation_formatter import (
    format_citation, format_apa, format_mla, format_chicago,
    format_din, format_harvard, source_to_bibtex, export_bibtex,
    _parse_authors, _first_author_surname, STYLES,
)
from hub.literatur import LiteraturHandler

MIGRATION_SQL = BACH_ROOT / "data" / "schema" / "migrations" / "026_literatur_integration.sql"


@pytest.fixture
def tmp_db(tmp_path):
    """Erstellt temporaere DB mit Literatur-Schema."""
    db_path = tmp_path / "test_bach.db"
    conn = sqlite3.connect(str(db_path))
    conn.executescript(MIGRATION_SQL.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def handler(tmp_db):
    """LiteraturHandler mit temp-DB."""
    import shutil
    base = tmp_db.parent / "system"
    data_dir = base / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    target = data_dir / "bach.db"
    shutil.copy2(str(tmp_db), str(target))
    return LiteraturHandler(base)


@pytest.fixture
def sample_source():
    """Standard-Testquelle."""
    return {
        "title": "Understanding Deep Learning",
        "authors": '["Smith, John", "Doe, Jane"]',
        "year": "2024",
        "source_type": "article",
        "journal": "Nature Machine Intelligence",
        "volume": "5",
        "issue": "3",
        "pages": "234-250",
        "doi": "10.1234/example",
        "publisher": "",
    }


@pytest.fixture
def sample_book():
    """Testquelle: Buch."""
    return {
        "title": "Reinforcement Learning",
        "authors": '["Sutton, Richard", "Barto, Andrew"]',
        "year": "2018",
        "source_type": "book",
        "journal": "",
        "volume": "",
        "issue": "",
        "pages": "",
        "doi": "",
        "publisher": "MIT Press",
        "isbn": "978-0262039246",
    }


# ================================================================
# AUTHOR PARSING
# ================================================================

class TestAuthorParsing:
    def test_json_string(self):
        result = _parse_authors('["Smith, John", "Doe, Jane"]')
        assert result == ["Smith, John", "Doe, Jane"]

    def test_list_input(self):
        result = _parse_authors(["Smith, John"])
        assert result == ["Smith, John"]

    def test_empty(self):
        assert _parse_authors(None) == []
        assert _parse_authors("") == []

    def test_plain_string(self):
        result = _parse_authors("Smith, John")
        assert result == ["Smith, John"]

    def test_surname_comma(self):
        assert _first_author_surname(["Smith, John"]) == "Smith"

    def test_surname_space(self):
        assert _first_author_surname(["John Smith"]) == "Smith"

    def test_surname_empty(self):
        assert _first_author_surname([]) == "Unbekannt"


# ================================================================
# CITATION STYLES
# ================================================================

class TestAPA:
    def test_full_article(self, sample_source):
        result = format_apa(sample_source)
        assert "Smith, John & Doe, Jane" in result["full"]
        assert "(2024)" in result["full"]
        assert "*Nature Machine Intelligence*" in result["full"]
        assert "https://doi.org/10.1234/example" in result["full"]

    def test_inline(self, sample_source):
        result = format_apa(sample_source, page=42)
        assert result["inline"] == "(Smith, 2024, S. 42)"

    def test_inline_no_page(self, sample_source):
        result = format_apa(sample_source)
        assert result["inline"] == "(Smith, 2024)"

    def test_book(self, sample_book):
        result = format_apa(sample_book)
        assert "*Reinforcement Learning*" in result["full"]
        assert "MIT Press" in result["full"]


class TestMLA:
    def test_full(self, sample_source):
        result = format_mla(sample_source)
        assert '"Understanding Deep Learning."' in result["full"]
        assert "*Nature Machine Intelligence*" in result["full"]

    def test_inline_with_page(self, sample_source):
        result = format_mla(sample_source, page=42)
        assert result["inline"] == "(Smith 42)"


class TestChicago:
    def test_full(self, sample_source):
        result = format_chicago(sample_source)
        assert "(2024)" in result["full"]

    def test_inline(self, sample_source):
        result = format_chicago(sample_source, page=42)
        assert result["inline"] == "(Smith 2024, 42)"


class TestDIN:
    def test_full(self, sample_source):
        result = format_din(sample_source)
        assert "In: Nature Machine Intelligence" in result["full"]
        assert "Bd. 5" in result["full"]

    def test_inline(self, sample_source):
        result = format_din(sample_source, page=42)
        assert result["inline"] == "[Smith 2024, S. 42]"


class TestHarvard:
    def test_full(self, sample_source):
        result = format_harvard(sample_source)
        assert "Smith, John & Doe, Jane (2024)" in result["full"]

    def test_inline(self, sample_source):
        result = format_harvard(sample_source, page=42)
        assert result["inline"] == "(Smith, 2024, p. 42)"


class TestStyleDispatcher:
    def test_all_styles(self, sample_source):
        for style in STYLES:
            result = format_citation(sample_source, style)
            assert "full" in result
            assert "inline" in result

    def test_unknown_style(self, sample_source):
        with pytest.raises(ValueError):
            format_citation(sample_source, "unknown")

    def test_case_insensitive(self, sample_source):
        result = format_citation(sample_source, "APA")
        assert "full" in result


# ================================================================
# BIBTEX
# ================================================================

class TestBibTeX:
    def test_article(self, sample_source):
        bib = source_to_bibtex(sample_source)
        assert bib.startswith("@article{Smith2024,")
        assert "title = {Understanding Deep Learning}" in bib
        assert "author = {Smith, John and Doe, Jane}" in bib
        assert "doi = {10.1234/example}" in bib

    def test_book(self, sample_book):
        bib = source_to_bibtex(sample_book)
        assert bib.startswith("@book{Sutton2018,")
        assert "publisher = {MIT Press}" in bib
        assert "isbn = {978-0262039246}" in bib

    def test_export_multiple(self, sample_source, sample_book):
        result = export_bibtex([sample_source, sample_book])
        assert "% BACH BibTeX Export" in result
        assert "Entries: 2" in result
        assert "@article{Smith2024," in result
        assert "@book{Sutton2018," in result

    def test_conference_uses_booktitle(self):
        src = {"title": "Test", "authors": '["A"]', "year": "2024",
               "source_type": "conference", "journal": "ICML 2024"}
        bib = source_to_bibtex(src)
        assert "booktitle = {ICML 2024}" in bib

    def test_tags_as_keywords(self):
        src = {"title": "Test", "authors": '["A"]', "year": "2024",
               "source_type": "article", "tags": '["AI", "ML"]'}
        bib = source_to_bibtex(src)
        assert "keywords = {AI, ML}" in bib


# ================================================================
# HANDLER OPERATIONS
# ================================================================

class TestHandlerAdd:
    def test_add_basic(self, handler):
        ok, txt = handler.handle("add", ["Test Titel", "--author", "Mueller, Hans", "--year", "2023"])
        assert ok
        assert "Test Titel" in txt

    def test_add_no_args(self, handler):
        ok, txt = handler.handle("add", [])
        assert not ok
        assert "Usage" in txt

    def test_add_with_tags(self, handler):
        ok, txt = handler.handle("add", ["Tagged Source", "--author", "A", "--tags", "AI,ML"])
        assert ok

    def test_add_multiple_authors(self, handler):
        ok, txt = handler.handle("add", ["Multi Author", "--author", "Smith, J;Doe, J;Lee, K"])
        assert ok


class TestHandlerList:
    def test_list_empty(self, handler):
        ok, txt = handler.handle("list", [])
        assert ok
        assert "Keine Quellen" in txt

    def test_list_with_data(self, handler):
        handler.handle("add", ["Source A", "--year", "2020"])
        handler.handle("add", ["Source B", "--year", "2021"])
        ok, txt = handler.handle("list", [])
        assert ok
        assert "Source A" in txt
        assert "Source B" in txt
        assert "2 Quellen" in txt

    def test_list_filter_type(self, handler):
        handler.handle("add", ["Article", "--type", "article"])
        handler.handle("add", ["Book", "--type", "book"])
        ok, txt = handler.handle("list", ["--type", "book"])
        assert ok
        assert "Book" in txt
        assert "Article" not in txt


class TestHandlerSearch:
    def test_search_found(self, handler):
        handler.handle("add", ["Deep Learning Basics", "--author", "Smith"])
        ok, txt = handler.handle("search", ["Deep"])
        assert ok
        assert "Deep Learning Basics" in txt

    def test_search_not_found(self, handler):
        ok, txt = handler.handle("search", ["nonexistent"])
        assert ok
        assert "Keine Treffer" in txt


class TestHandlerShow:
    def test_show(self, handler):
        handler.handle("add", ["Show Test", "--author", "Test Author", "--year", "2024"])
        ok, txt = handler.handle("show", ["1"])
        assert ok
        assert "Show Test" in txt
        assert "Test Author" in txt

    def test_show_not_found(self, handler):
        ok, txt = handler.handle("show", ["999"])
        assert not ok
        assert "nicht gefunden" in txt


class TestHandlerEdit:
    def test_edit(self, handler):
        handler.handle("add", ["Edit Test"])
        ok, txt = handler.handle("edit", ["1", "--title", "Edited Title", "--year", "2025"])
        assert ok
        assert "aktualisiert" in txt

    def test_edit_not_found(self, handler):
        ok, txt = handler.handle("edit", ["999", "--title", "X"])
        assert not ok


class TestHandlerDelete:
    def test_delete(self, handler):
        handler.handle("add", ["Delete Me"])
        ok, txt = handler.handle("delete", ["1"])
        assert ok
        assert "geloescht" in txt
        # Verify gone
        ok2, txt2 = handler.handle("show", ["1"])
        assert not ok2

    def test_delete_cascades(self, handler):
        handler.handle("add", ["Cascade Test"])
        handler.handle("quote", ["1", "Some quote", "--page", "1"])
        handler.handle("summary", ["1", "Some summary"])
        ok, txt = handler.handle("delete", ["1"])
        assert ok


class TestHandlerQuotes:
    def test_add_quote(self, handler):
        handler.handle("add", ["Quote Source"])
        ok, txt = handler.handle("quote", ["1", "This is a test quote", "--page", "42"])
        assert ok
        assert "hinzugefuegt" in txt

    def test_list_quotes(self, handler):
        handler.handle("add", ["Quote Source"])
        handler.handle("quote", ["1", "Quote A", "--page", "10"])
        handler.handle("quote", ["1", "Quote B", "--page", "20", "--type", "indirect"])
        ok, txt = handler.handle("quotes", ["1"])
        assert ok
        assert "Quote A" in txt
        assert "Quote B" in txt
        assert "2 Zitat(e)" in txt

    def test_quote_invalid_source(self, handler):
        ok, txt = handler.handle("quote", ["999", "Some text"])
        assert not ok


class TestHandlerCite:
    def test_cite_all_styles(self, handler):
        handler.handle("add", ["Cite Test", "--author", "Smith, John", "--year", "2024"])
        for style in ["apa", "mla", "chicago", "din", "harvard"]:
            ok, txt = handler.handle("cite", ["1", "--style", style])
            assert ok, f"Stil {style} fehlgeschlagen"
            assert "Vollzitat:" in txt

    def test_cite_with_page(self, handler):
        handler.handle("add", ["Cite Page", "--author", "Doe, Jane", "--year", "2023"])
        ok, txt = handler.handle("cite", ["1", "--page", "55"])
        assert ok
        assert "S. 55" in txt


class TestHandlerExport:
    def test_export(self, handler):
        handler.handle("add", ["Export A", "--author", "Smith", "--year", "2024"])
        handler.handle("add", ["Export B", "--author", "Doe", "--year", "2023"])
        ok, txt = handler.handle("export", ["--all"])
        assert ok
        assert "@article{" in txt
        assert "Entries: 2" in txt


class TestHandlerSummary:
    def test_add_summary(self, handler):
        handler.handle("add", ["Summary Source"])
        ok, txt = handler.handle("summary", ["1", "This is a summary of the paper.", "--type", "abstract"])
        assert ok
        assert "hinzugefuegt" in txt

    def test_show_summaries(self, handler):
        handler.handle("add", ["Summary Source"])
        handler.handle("summary", ["1", "Summary text here."])
        ok, txt = handler.handle("summary", ["1"])
        assert ok
        assert "Summary text here." in txt


class TestHandlerStats:
    def test_stats_empty(self, handler):
        ok, txt = handler.handle("stats", [])
        assert ok
        assert "leer" in txt

    def test_stats_with_data(self, handler):
        handler.handle("add", ["Stats A", "--type", "article", "--year", "2020"])
        handler.handle("add", ["Stats B", "--type", "book", "--year", "2023"])
        ok, txt = handler.handle("stats", [])
        assert ok
        assert "2" in txt
        assert "article" in txt
        assert "book" in txt


class TestHandlerOps:
    def test_operations_count(self, handler):
        ops = handler.get_operations()
        assert len(ops) == 13

    def test_help(self, handler):
        ok, txt = handler.handle("help", [])
        assert ok
        assert "LITERATURVERWALTUNG" in txt
        assert "cite" in txt
        assert "export" in txt
