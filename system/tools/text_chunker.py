#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: text_chunker
Version: 1.0.0
Author: Claude Opus 4.6
Created: 2026-03-01
Origin: Portiert aus KnowledgeDigest/chunker.py

Description:
    Text-Chunking-Utility fuer BACH. Teilt Texte in ~400-Token-Chunks auf,
    optimiert fuer gemischten DE/EN/YAML-Content (z.B. BACH Skills).

    Heuristik: 1 Token ~ 1 Wort (konservativ).

    Strategie:
        1. YAML-Frontmatter wird als eigener Chunk extrahiert
        2. Body wird an Satz-/Absatzgrenzen gesplittet
        3. Chunks von ~300-400 Woertern (Target: 350)
        4. Optional: Overlap von 50-100 Woertern

    Verwendung in BACH:
        - unified_search.py: Dokument-Indexierung mit Chunk-Granularitaet
        - Zukuenftige Embedding-Pipeline (sqlite-vec)
        - Zusammenfassungs-Pipeline (LLM-Summarization)

Usage:
    from text_chunker import chunk_text, split_frontmatter, estimate_tokens

    chunks = chunk_text(skill_content, chunk_size=350)
    for chunk in chunks:
        print(f"Chunk {chunk.index}: {chunk.token_count} Tokens")
        print(chunk.content[:100])
"""

__version__ = "1.0.0"
__author__ = "Claude Opus 4.6"
__all__ = ["chunk_text", "split_frontmatter", "estimate_tokens", "Chunk"]

import re
from dataclasses import dataclass
from typing import List, Tuple, Optional

# -----------------------------------------------------------------
# Konfiguration
# -----------------------------------------------------------------

DEFAULT_CHUNK_SIZE = 350     # Ziel-Woerter pro Chunk (~400 Token)
MAX_CHUNK_SIZE = 500         # Harte Obergrenze
MIN_CHUNK_SIZE = 50          # Minimum (kleinere werden angehaengt)
DEFAULT_OVERLAP = 0          # Standard: kein Overlap


# -----------------------------------------------------------------
# Datenstrukturen
# -----------------------------------------------------------------

@dataclass
class Chunk:
    """Ein Textabschnitt mit Metadaten."""
    index: int
    content: str
    token_count: int
    is_frontmatter: bool = False

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "content": self.content,
            "token_count": self.token_count,
            "is_frontmatter": self.is_frontmatter,
        }


# -----------------------------------------------------------------
# Hilfsfunktionen
# -----------------------------------------------------------------

def estimate_tokens(text: str) -> int:
    """Schaetzt Token-Anzahl ueber Wortanzahl (konservativ).

    Fuer gemischten DE/EN/YAML-Content ist 1 Wort ~ 1.1 Token
    eine gute Naeherung. Wir nutzen Wortanzahl als konservative
    Untergrenze.

    Args:
        text: Eingabetext

    Returns:
        Geschaetzte Token-Anzahl
    """
    if not text:
        return 0
    return len(text.split())


def split_frontmatter(text: str) -> Tuple[Optional[str], str]:
    """Trennt YAML-Frontmatter vom Body.

    BACH Skills haben oft das Format:
        ---
        name: ...
        metadata: ...
        ---
        # Body content

    Args:
        text: Volltext (ggf. mit Frontmatter)

    Returns:
        (frontmatter, body) -- frontmatter ist None wenn nicht vorhanden
    """
    if not text:
        return None, ""

    text = text.strip()

    # Frontmatter: beginnt mit --- und endet mit ---
    if text.startswith("---"):
        # Suche das schliessende ---
        end_match = re.search(r'\n---\s*\n', text[3:])
        if end_match:
            end_pos = end_match.end() + 3  # +3 fuer das erste ---
            frontmatter = text[:end_pos].strip()
            body = text[end_pos:].strip()
            return frontmatter, body

    return None, text


def _split_sentences(text: str) -> List[str]:
    """Teilt Text in Saetze/Absaetze auf.

    Splittet an:
    - Leerzeilen (Absaetze)
    - Satzenden (. ! ?) gefolgt von Grossbuchstabe oder Zeilenumbruch
    - Markdown-Ueberschriften (#)
    - Listen-Items (- oder *)

    Args:
        text: Eingabetext

    Returns:
        Liste von Textsegmenten
    """
    if not text:
        return []

    # Erst an Leerzeilen splitten (Absaetze)
    paragraphs = re.split(r'\n\s*\n', text)

    segments = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Innerhalb eines Absatzes: an Satzgrenzen splitten
        # Aber nur wenn der Absatz lang genug ist
        if estimate_tokens(para) <= MAX_CHUNK_SIZE:
            segments.append(para)
        else:
            # Langen Absatz an Satzgrenzen splitten
            sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z\u00C4\u00D6\u00DC])', para)
            if len(sentences) <= 1:
                # Fallback: an Zeilenumbruechen splitten
                sentences = para.split('\n')
            segments.extend(s.strip() for s in sentences if s.strip())

    return segments


# -----------------------------------------------------------------
# Haupt-Funktion
# -----------------------------------------------------------------

def chunk_text(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE,
               overlap: int = DEFAULT_OVERLAP,
               separate_frontmatter: bool = True) -> List[Chunk]:
    """Teilt Text in Chunks auf.

    Args:
        text: Volltext des Dokuments/Skills
        chunk_size: Ziel-Woerter pro Chunk (Default: 350)
        overlap: Overlap in Woertern zwischen Chunks (Default: 0)
        separate_frontmatter: Frontmatter als eigenen Chunk extrahieren

    Returns:
        Liste von Chunk-Objekten

    Examples:
        >>> chunks = chunk_text("Kurzer Text.")
        >>> len(chunks)
        1
        >>> chunks[0].content
        'Kurzer Text.'

        >>> long_text = "Satz eins. " * 500
        >>> chunks = chunk_text(long_text, chunk_size=100)
        >>> all(c.token_count <= 500 for c in chunks)
        True
    """
    if not text or not text.strip():
        return []

    chunks = []
    chunk_idx = 0

    # Frontmatter separieren
    frontmatter = None
    body = text
    if separate_frontmatter:
        frontmatter, body = split_frontmatter(text)

    if frontmatter:
        chunks.append(Chunk(
            index=chunk_idx,
            content=frontmatter,
            token_count=estimate_tokens(frontmatter),
            is_frontmatter=True,
        ))
        chunk_idx += 1

    # Body in Segmente splitten
    segments = _split_sentences(body)
    if not segments:
        return chunks

    # Segmente zu Chunks zusammenfassen
    current_parts: List[str] = []
    current_tokens = 0

    for segment in segments:
        seg_tokens = estimate_tokens(segment)

        # Wenn einzelnes Segment schon zu gross: forciert eigenen Chunk
        if seg_tokens > MAX_CHUNK_SIZE:
            # Aktuelle Teile erst abschliessen
            if current_parts:
                content = "\n\n".join(current_parts)
                chunks.append(Chunk(
                    index=chunk_idx,
                    content=content,
                    token_count=estimate_tokens(content),
                ))
                chunk_idx += 1
                current_parts = []
                current_tokens = 0

            # Grosses Segment als eigenen Chunk
            chunks.append(Chunk(
                index=chunk_idx,
                content=segment,
                token_count=seg_tokens,
            ))
            chunk_idx += 1
            continue

        # Passt Segment noch in aktuellen Chunk?
        if current_tokens + seg_tokens <= chunk_size:
            current_parts.append(segment)
            current_tokens += seg_tokens
        else:
            # Aktuellen Chunk abschliessen
            if current_parts:
                content = "\n\n".join(current_parts)
                chunks.append(Chunk(
                    index=chunk_idx,
                    content=content,
                    token_count=estimate_tokens(content),
                ))
                chunk_idx += 1

                # Overlap: letzte Teile uebernehmen
                if overlap > 0:
                    overlap_parts = []
                    overlap_tokens = 0
                    for part in reversed(current_parts):
                        pt = estimate_tokens(part)
                        if overlap_tokens + pt > overlap:
                            break
                        overlap_parts.insert(0, part)
                        overlap_tokens += pt
                    current_parts = overlap_parts + [segment]
                    current_tokens = overlap_tokens + seg_tokens
                else:
                    current_parts = [segment]
                    current_tokens = seg_tokens
            else:
                current_parts = [segment]
                current_tokens = seg_tokens

    # Letzten Chunk abschliessen
    if current_parts:
        content = "\n\n".join(current_parts)
        tokens = estimate_tokens(content)

        # Zu kleiner letzter Chunk? An vorherigen anhaengen
        if tokens < MIN_CHUNK_SIZE and len(chunks) > 0 and not chunks[-1].is_frontmatter:
            prev = chunks[-1]
            merged = prev.content + "\n\n" + content
            chunks[-1] = Chunk(
                index=prev.index,
                content=merged,
                token_count=estimate_tokens(merged),
                is_frontmatter=prev.is_frontmatter,
            )
        else:
            chunks.append(Chunk(
                index=chunk_idx,
                content=content,
                token_count=tokens,
            ))

    return chunks


# -----------------------------------------------------------------
# CLI Entrypoint (fuer Debugging)
# -----------------------------------------------------------------

def main():
    """CLI: Datei chunken und Statistiken ausgeben."""
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python text_chunker.py <datei> [--chunk-size N] [--overlap N]")
        print("       python text_chunker.py --test")
        return 1

    if sys.argv[1] == "--test":
        # Schnelltest
        test_text = """---
name: test_skill
type: agent
---

# Test Skill

Dies ist ein Testtext fuer den Chunker. Er enthaelt mehrere Absaetze
und sollte korrekt aufgeteilt werden.

## Abschnitt 1

Erster Abschnitt mit etwas Inhalt. Dieser Absatz ist kurz genug
fuer einen einzelnen Chunk.

## Abschnitt 2

Zweiter Abschnitt. Auch dieser ist relativ kurz.
"""
        chunks = chunk_text(test_text)
        print(f"Input: {estimate_tokens(test_text)} Woerter")
        print(f"Chunks: {len(chunks)}")
        for c in chunks:
            label = "[FM]" if c.is_frontmatter else f"[{c.index}]"
            print(f"  {label} {c.token_count} Woerter: {c.content[:60]}...")
        return 0

    # Datei chunken
    filepath = sys.argv[1]
    chunk_size = DEFAULT_CHUNK_SIZE
    overlap = DEFAULT_OVERLAP

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--chunk-size" and i + 1 < len(sys.argv):
            chunk_size = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--overlap" and i + 1 < len(sys.argv):
            overlap = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    from pathlib import Path
    p = Path(filepath)
    if not p.exists():
        print(f"Datei nicht gefunden: {filepath}")
        return 1

    text = p.read_text(encoding='utf-8', errors='ignore')
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

    result = {
        "file": filepath,
        "input_words": estimate_tokens(text),
        "chunk_count": len(chunks),
        "chunks": [c.to_dict() for c in chunks],
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
