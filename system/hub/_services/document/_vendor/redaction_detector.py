#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
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
DokuZentrum Pro - Redaction Detector
====================================
Erkennt sensible Daten für Schwärzung.
"""

import re
from typing import List, Set, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

from utils.logger import LoggerMixin

try:
    from rapidfuzz import fuzz, process
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False


class SensitiveType(Enum):
    """Typen sensibler Daten."""
    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    IBAN = "iban"
    DATE = "date"
    ADDRESS = "address"
    CUSTOM = "custom"


@dataclass
class Match:
    """Ein gefundener Treffer."""
    text: str
    start: int
    end: int
    type: SensitiveType
    confidence: float
    page: int = 0


class RedactionDetector(LoggerMixin):
    """
    Erkennt sensible Daten in Text.
    
    Features:
    - Regex-basierte Erkennung (Email, Telefon, IBAN, etc.)
    - Blacklist-Wörter (exakt und fuzzy)
    - Whitelist (Ausnahmen)
    - Konfigurierbare Schwellwerte
    """
    
    # Regex-Patterns für deutsche Formate
    PATTERNS = {
        SensitiveType.EMAIL: r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        SensitiveType.PHONE: r'\b(?:\+49|0049|0)[\s\-]?(?:\d[\s\-]?){9,14}\b',
        SensitiveType.IBAN: r'\b[A-Z]{2}\d{2}[\s]?(?:\d{4}[\s]?){4}\d{2}\b',
        SensitiveType.DATE: r'\b\d{1,2}[.\-/]\d{1,2}[.\-/](?:\d{2}|\d{4})\b',
    }
    
    def __init__(self, fuzzy_threshold: int = 80):
        """
        Initialisiert den Detector.
        
        Args:
            fuzzy_threshold: Schwellwert für Fuzzy-Matching (0-100)
        """
        self._blacklist: Set[str] = set()
        self._whitelist: Set[str] = set()
        self._fuzzy_threshold = fuzzy_threshold
        self._compiled_patterns: Dict[SensitiveType, re.Pattern] = {}
        
        # Patterns kompilieren
        for type_, pattern in self.PATTERNS.items():
            self._compiled_patterns[type_] = re.compile(pattern, re.IGNORECASE)
        
        if not RAPIDFUZZ_AVAILABLE:
            self.logger.warning("rapidfuzz nicht installiert - Fuzzy-Matching deaktiviert")
    
    def load_blacklist(self, path: str) -> int:
        """
        Lädt Blacklist aus Datei.
        
        Args:
            path: Pfad zur Textdatei (ein Wort pro Zeile)
            
        Returns:
            Anzahl geladener Wörter
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                words = {line.strip().lower() for line in f if line.strip()}
            self._blacklist.update(words)
            self.logger.info(f"Blacklist geladen: {len(words)} Wörter aus {path}")
            return len(words)
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der Blacklist: {e}")
            return 0
    
    def load_whitelist(self, path: str) -> int:
        """Lädt Whitelist aus Datei."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                words = {line.strip().lower() for line in f if line.strip()}
            self._whitelist.update(words)
            self.logger.info(f"Whitelist geladen: {len(words)} Wörter")
            return len(words)
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der Whitelist: {e}")
            return 0
    
    def add_to_blacklist(self, words: List[str]):
        """Fügt Wörter zur Blacklist hinzu."""
        self._blacklist.update(w.lower() for w in words)
    
    def add_to_whitelist(self, words: List[str]):
        """Fügt Wörter zur Whitelist hinzu."""
        self._whitelist.update(w.lower() for w in words)
    
    def clear_blacklist(self):
        """Leert die Blacklist."""
        self._blacklist.clear()
    
    def clear_whitelist(self):
        """Leert die Whitelist."""
        self._whitelist.clear()
    
    def detect(self, text: str, page: int = 0,
               use_patterns: bool = True,
               use_blacklist: bool = True,
               use_fuzzy: bool = True) -> List[Match]:
        """
        Erkennt sensible Daten im Text.
        
        Args:
            text: Zu analysierender Text
            page: Seitennummer (für Referenz)
            use_patterns: Regex-Patterns verwenden
            use_blacklist: Blacklist-Wörter suchen
            use_fuzzy: Fuzzy-Matching für Blacklist
            
        Returns:
            Liste von Match-Objekten
        """
        matches: List[Match] = []
        
        if use_patterns:
            matches.extend(self._detect_patterns(text, page))
        
        if use_blacklist and self._blacklist:
            if use_fuzzy and RAPIDFUZZ_AVAILABLE:
                matches.extend(self._detect_fuzzy(text, page))
            else:
                matches.extend(self._detect_exact(text, page))
        
        # Whitelist-Filterung
        matches = self._filter_whitelist(matches)
        
        # Duplikate entfernen (basierend auf Position)
        matches = self._deduplicate(matches)
        
        return sorted(matches, key=lambda m: (m.page, m.start))
    
    def _detect_patterns(self, text: str, page: int) -> List[Match]:
        """Erkennt Patterns via Regex."""
        matches = []
        
        for type_, pattern in self._compiled_patterns.items():
            for m in pattern.finditer(text):
                matches.append(Match(
                    text=m.group(),
                    start=m.start(),
                    end=m.end(),
                    type=type_,
                    confidence=100.0,
                    page=page
                ))
        
        return matches
    
    def _detect_exact(self, text: str, page: int) -> List[Match]:
        """Sucht exakte Blacklist-Treffer."""
        matches = []
        text_lower = text.lower()
        
        for word in self._blacklist:
            start = 0
            while True:
                pos = text_lower.find(word, start)
                if pos == -1:
                    break
                
                matches.append(Match(
                    text=text[pos:pos+len(word)],
                    start=pos,
                    end=pos + len(word),
                    type=SensitiveType.CUSTOM,
                    confidence=100.0,
                    page=page
                ))
                start = pos + 1
        
        return matches
    
    def _detect_fuzzy(self, text: str, page: int) -> List[Match]:
        """Fuzzy-Matching für Blacklist."""
        matches = []
        
        # Text in Wörter aufteilen
        words = re.findall(r'\b\w+\b', text)
        
        for word in words:
            if len(word) < 3:  # Zu kurze Wörter ignorieren
                continue
            
            # Bestes Match in Blacklist suchen
            result = process.extractOne(
                word.lower(),
                self._blacklist,
                scorer=fuzz.ratio,
                score_cutoff=self._fuzzy_threshold
            )
            
            if result:
                match_word, score, _ = result
                
                # Position im Original-Text finden
                pos = text.lower().find(word.lower())
                if pos != -1:
                    matches.append(Match(
                        text=text[pos:pos+len(word)],
                        start=pos,
                        end=pos + len(word),
                        type=SensitiveType.CUSTOM,
                        confidence=score,
                        page=page
                    ))
        
        return matches
    
    def _filter_whitelist(self, matches: List[Match]) -> List[Match]:
        """Filtert Whitelist-Einträge heraus."""
        if not self._whitelist:
            return matches
        
        return [
            m for m in matches
            if m.text.lower() not in self._whitelist
        ]
    
    def _deduplicate(self, matches: List[Match]) -> List[Match]:
        """Entfernt überlappende Treffer."""
        if not matches:
            return matches
        
        # Nach Position sortieren
        sorted_matches = sorted(matches, key=lambda m: (m.page, m.start, -m.end))
        
        result = [sorted_matches[0]]
        for match in sorted_matches[1:]:
            last = result[-1]
            
            # Überlappung prüfen
            if match.page != last.page or match.start >= last.end:
                result.append(match)
            elif match.confidence > last.confidence:
                result[-1] = match
        
        return result


class RedactionApplier(LoggerMixin):
    """Wendet Schwärzungen auf PDFs an."""
    
    def __init__(self):
        try:
            import fitz
            self._fitz = fitz
            self._available = True
        except ImportError:
            self._available = False
            self.logger.warning("PyMuPDF nicht verfügbar")
    
    def redact_pdf(self, input_path: str, output_path: str,
                   matches: List[Match],
                   redaction_color: Tuple[int, int, int] = (0, 0, 0)) -> bool:
        """
        Schwärzt Textstellen in einer PDF.
        
        Args:
            input_path: Eingabe-PDF
            output_path: Ausgabe-PDF
            matches: Zu schwärzende Stellen
            redaction_color: Farbe (R, G, B)
            
        Returns:
            True bei Erfolg
        """
        if not self._available:
            return False
        
        try:
            doc = self._fitz.open(input_path)
            
            # Matches nach Seite gruppieren
            by_page: Dict[int, List[Match]] = {}
            for m in matches:
                by_page.setdefault(m.page, []).append(m)
            
            # Pro Seite schwärzen
            for page_num, page_matches in by_page.items():
                if page_num < 1 or page_num > doc.page_count:
                    continue
                
                page = doc[page_num - 1]
                
                for match in page_matches:
                    # Text suchen
                    text_instances = page.search_for(match.text)
                    
                    for rect in text_instances:
                        # Redaction-Annotation hinzufügen
                        page.add_redact_annot(rect, fill=redaction_color)
                
                # Redactions anwenden
                page.apply_redactions()
            
            # Speichern
            doc.save(output_path)
            doc.close()
            
            self.logger.info(f"PDF geschwärzt: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Schwärzungsfehler: {e}")
            return False


# === Hilfsfunktionen ===

def detect_sensitive_data(text: str, blacklist_path: Optional[str] = None) -> List[Match]:
    """Schnelle Erkennung sensibler Daten."""
    detector = RedactionDetector()
    if blacklist_path:
        detector.load_blacklist(blacklist_path)
    return detector.detect(text)


def redact_pdf(input_path: str, output_path: str,
               blacklist_path: Optional[str] = None) -> bool:
    """Schwärzt sensible Daten in einer PDF."""
    # Text extrahieren
    try:
        import fitz
        doc = fitz.open(input_path)
        
        detector = RedactionDetector()
        if blacklist_path:
            detector.load_blacklist(blacklist_path)
        
        all_matches = []
        for i, page in enumerate(doc):
            text = page.get_text()
            matches = detector.detect(text, page=i+1)
            all_matches.extend(matches)
        
        doc.close()
        
        if all_matches:
            applier = RedactionApplier()
            return applier.redact_pdf(input_path, output_path, all_matches)
        
        return True
        
    except Exception as e:
        return False
