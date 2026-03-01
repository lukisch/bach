#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Citation Formatter — Zitationsstile und BibTeX-Export (INT01)

Portiert aus LitZentrum (5 Zitationsstile + BibTeX-Generator).
Arbeitet mit sqlite3.Row-Objekten oder Dicts mit LitZentrum-kompatiblen Feldern.

Stile: APA (7th), MLA (9th), Chicago, DIN 1505-2, Harvard
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


# ================================================================
# HILFSFUNKTIONEN
# ================================================================

def _parse_authors(authors_field) -> List[str]:
    """Parst authors aus JSON-String oder Liste."""
    if not authors_field:
        return []
    if isinstance(authors_field, list):
        return authors_field
    try:
        parsed = json.loads(authors_field)
        return parsed if isinstance(parsed, list) else [str(parsed)]
    except (json.JSONDecodeError, TypeError):
        return [str(authors_field)]


def _first_author_surname(authors: List[str]) -> str:
    """Extrahiert Nachname des ersten Autors. 'Smith, John' -> 'Smith'."""
    if not authors:
        return "Unbekannt"
    first = authors[0]
    if "," in first:
        return first.split(",")[0].strip()
    parts = first.strip().split()
    return parts[-1] if parts else "Unbekannt"


def _get(source: dict, key: str, default="") -> str:
    """Sicherer Dict/Row-Zugriff."""
    try:
        val = source[key]
        return str(val) if val is not None else default
    except (KeyError, IndexError):
        return default


# ================================================================
# ZITATIONSSTILE
# ================================================================

def format_apa(source: dict, page: int = None) -> Dict[str, str]:
    """APA 7th Edition. Returns {"full": ..., "inline": ...}."""
    authors = _parse_authors(source.get("authors"))
    year = _get(source, "year")
    title = _get(source, "title")
    journal = _get(source, "journal")
    volume = _get(source, "volume")
    issue = _get(source, "issue")
    pages = _get(source, "pages")
    doi = _get(source, "doi")
    publisher = _get(source, "publisher")
    stype = _get(source, "source_type", "article")

    # Autoren formatieren
    if len(authors) == 1:
        author_str = authors[0]
    elif len(authors) == 2:
        author_str = f"{authors[0]} & {authors[1]}"
    elif len(authors) <= 20:
        author_str = ", ".join(authors[:-1]) + f", & {authors[-1]}"
    else:
        author_str = ", ".join(authors[:19]) + f", ... {authors[-1]}"

    # Vollzitat
    parts = [f"{author_str}."]
    if year:
        parts.append(f"({year}).")

    if stype == "book":
        parts.append(f"*{title}*.")
    else:
        parts.append(f"{title}.")

    if journal:
        j_parts = [f"*{journal}*"]
        if volume:
            j_parts[0] += f", *{volume}*"
        if issue:
            j_parts[0] += f"({issue})"
        if pages:
            j_parts.append(pages)
        parts.append(", ".join(j_parts) + ".")

    if publisher:
        parts.append(f"{publisher}.")

    if doi:
        parts.append(f"https://doi.org/{doi}")

    full = " ".join(parts)

    # Inline
    surname = _first_author_surname(authors)
    if page:
        inline = f"({surname}, {year}, S. {page})"
    else:
        inline = f"({surname}, {year})"

    return {"full": full, "inline": inline}


def format_mla(source: dict, page: int = None) -> Dict[str, str]:
    """MLA 9th Edition."""
    authors = _parse_authors(source.get("authors"))
    year = _get(source, "year")
    title = _get(source, "title")
    journal = _get(source, "journal")
    volume = _get(source, "volume")
    issue = _get(source, "issue")
    pages = _get(source, "pages")
    publisher = _get(source, "publisher")

    if len(authors) <= 1:
        author_str = authors[0] if authors else "Unbekannt"
    else:
        author_str = f"{authors[0]}, et al."

    parts = [f'{author_str}. "{title}."']

    if journal:
        j = f"*{journal}*"
        if volume:
            j += f", vol. {volume}"
        if issue:
            j += f", no. {issue}"
        if year:
            j += f", {year}"
        if pages:
            j += f", pp. {pages}"
        parts.append(j + ".")
    elif publisher:
        parts.append(f"{publisher}, {year}.")

    full = " ".join(parts)

    surname = _first_author_surname(authors)
    inline = f"({surname} {page})" if page else f"({surname})"

    return {"full": full, "inline": inline}


def format_chicago(source: dict, page: int = None) -> Dict[str, str]:
    """Chicago Notes-Bibliography."""
    authors = _parse_authors(source.get("authors"))
    year = _get(source, "year")
    title = _get(source, "title")
    journal = _get(source, "journal")
    volume = _get(source, "volume")
    issue = _get(source, "issue")
    pages = _get(source, "pages")

    author_str = ", ".join(authors) if authors else "Unbekannt"

    parts = [f'{author_str}. "{title}."']

    if journal:
        j = f"*{journal}* {volume}" if volume else f"*{journal}*"
        if issue:
            j += f", no. {issue}"
        if year:
            j += f" ({year})"
        if pages:
            j += f": {pages}"
        parts.append(j + ".")

    full = " ".join(parts)

    surname = _first_author_surname(authors)
    inline = f"({surname} {year}, {page})" if page else f"({surname} {year})"

    return {"full": full, "inline": inline}


def format_din(source: dict, page: int = None) -> Dict[str, str]:
    """DIN 1505-2 (Deutsche Norm)."""
    authors = _parse_authors(source.get("authors"))
    year = _get(source, "year")
    title = _get(source, "title")
    journal = _get(source, "journal")
    volume = _get(source, "volume")
    issue = _get(source, "issue")
    pages = _get(source, "pages")
    publisher = _get(source, "publisher")
    isbn = _get(source, "isbn")

    author_str = "; ".join(authors) if authors else "Unbekannt"

    parts = [f"{author_str}: {title}."]

    if journal:
        j = f"In: {journal}"
        if volume:
            j += f" Bd. {volume}"
        if year:
            j += f" ({year})"
        if issue:
            j += f", H. {issue}"
        if pages:
            j += f", S. {pages}"
        parts.append(j + ".")

    if publisher:
        parts.append(f"{publisher}.")
    if isbn:
        parts.append(f"ISBN {isbn}.")

    full = " ".join(parts)

    surname = _first_author_surname(authors)
    inline = f"[{surname} {year}, S. {page}]" if page else f"[{surname} {year}]"

    return {"full": full, "inline": inline}


def format_harvard(source: dict, page: int = None) -> Dict[str, str]:
    """Harvard Style."""
    authors = _parse_authors(source.get("authors"))
    year = _get(source, "year")
    title = _get(source, "title")
    journal = _get(source, "journal")
    volume = _get(source, "volume")
    issue = _get(source, "issue")
    pages = _get(source, "pages")

    if len(authors) <= 1:
        author_str = authors[0] if authors else "Unbekannt"
    elif len(authors) == 2:
        author_str = f"{authors[0]} & {authors[1]}"
    else:
        author_str = f"{authors[0]} et al."

    parts = [f"{author_str} ({year})."]
    parts.append(f"'{title}',")

    if journal:
        j = f"*{journal}*"
        if volume:
            j += f", {volume}"
        if issue:
            j += f"({issue})"
        if pages:
            j += f", pp. {pages}"
        parts.append(j + ".")

    full = " ".join(parts)

    surname = _first_author_surname(authors)
    inline = f"({surname}, {year}, p. {page})" if page else f"({surname}, {year})"

    return {"full": full, "inline": inline}


# ================================================================
# STIL-REGISTRY
# ================================================================

STYLES = {
    "apa": format_apa,
    "mla": format_mla,
    "chicago": format_chicago,
    "din": format_din,
    "harvard": format_harvard,
}


def format_citation(source: dict, style: str = "apa", page: int = None) -> Dict[str, str]:
    """
    Formatiert eine Quelle im gewaehlten Zitationsstil.

    Args:
        source: Dict mit Feldern (title, authors, year, journal, etc.)
        style: apa|mla|chicago|din|harvard
        page: Optionale Seitenzahl fuer Inline-Zitat

    Returns:
        {"full": "Vollzitat", "inline": "(Inline-Zitat)"}
    """
    formatter = STYLES.get(style.lower())
    if not formatter:
        raise ValueError(f"Unbekannter Stil: {style}. Verfuegbar: {', '.join(STYLES.keys())}")
    return formatter(source, page)


# ================================================================
# BIBTEX-EXPORT
# ================================================================

BIBTEX_TYPE_MAP = {
    "article": "article",
    "book": "book",
    "chapter": "inbook",
    "thesis": "phdthesis",
    "conference": "inproceedings",
    "website": "online",
    "other": "misc",
}


def _bibtex_key(source: dict) -> str:
    """Generiert BibTeX-Key: AuthorYear."""
    authors = _parse_authors(source.get("authors"))
    surname = _first_author_surname(authors)
    year = _get(source, "year", "0000")
    # Umlaute und Sonderzeichen entfernen
    clean = surname.replace(" ", "").replace("-", "")
    return f"{clean}{year}"


def source_to_bibtex(source: dict) -> str:
    """Konvertiert eine Quelle in BibTeX-Eintrag."""
    stype = _get(source, "source_type", "article")
    bib_type = BIBTEX_TYPE_MAP.get(stype, "misc")
    key = _bibtex_key(source)

    fields = []

    title = _get(source, "title")
    if title:
        fields.append(f"  title = {{{title}}}")

    authors = _parse_authors(source.get("authors"))
    if authors:
        fields.append(f"  author = {{{' and '.join(authors)}}}")

    year = _get(source, "year")
    if year:
        fields.append(f"  year = {{{year}}}")

    journal = _get(source, "journal")
    if journal:
        if stype == "conference":
            fields.append(f"  booktitle = {{{journal}}}")
        else:
            fields.append(f"  journal = {{{journal}}}")

    for field, db_key in [("volume", "volume"), ("number", "issue"),
                           ("pages", "pages"), ("publisher", "publisher"),
                           ("doi", "doi"), ("isbn", "isbn"), ("url", "url")]:
        val = _get(source, db_key)
        if val:
            fields.append(f"  {field} = {{{val}}}")

    abstract = _get(source, "abstract")
    if abstract:
        clean = abstract.replace("\n", " ").strip()
        fields.append(f"  abstract = {{{clean}}}")

    tags = source.get("tags")
    if tags:
        if isinstance(tags, str):
            try:
                tags = json.loads(tags)
            except json.JSONDecodeError:
                tags = [tags]
        if isinstance(tags, list):
            fields.append(f"  keywords = {{{', '.join(tags)}}}")

    return f"@{bib_type}{{{key},\n" + ",\n".join(fields) + "\n}"


def export_bibtex(sources: List[dict]) -> str:
    """Exportiert mehrere Quellen als BibTeX-String."""
    header = (
        f"% BACH BibTeX Export\n"
        f"% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"% Entries: {len(sources)}\n\n"
    )
    entries = [source_to_bibtex(s) for s in sources]
    return header + "\n\n".join(entries) + "\n"
