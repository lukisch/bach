#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
Encoding Module - Minimal Version v1.0.0

Wiederverwendbares Modul fuer:
- UTF-8 Encoding/Decoding
- BOM (Byte Order Mark) Handling
- Encoding-Detection
- Sichere Datei-I/O mit Encoding

Kann in beliebige Projekte injiziert werden.

Quelle: BACH Best-Practices und RecludOS
Datum: 2026-01-22
"""

import codecs
import os
import sys
from pathlib import Path
from typing import Optional, Tuple


# UTF-8 BOM
UTF8_BOM = codecs.BOM_UTF8


class EncodingDetector:
    """Erkennt und verwaltet Datei-Encodings."""
    
    # Bekannte BOMs
    BOMS = {
        codecs.BOM_UTF8: 'utf-8-sig',
        codecs.BOM_UTF16_LE: 'utf-16-le',
        codecs.BOM_UTF16_BE: 'utf-16-be',
        codecs.BOM_UTF32_LE: 'utf-32-le',
        codecs.BOM_UTF32_BE: 'utf-32-be',
    }
    
    @classmethod
    def detect_bom(cls, file_path: Path) -> Optional[str]:
        """Erkennt BOM am Dateianfang und gibt Encoding zurueck."""
        if not file_path.exists():
            return None
        
        with open(file_path, 'rb') as f:
            start = f.read(4)
        
        for bom, encoding in cls.BOMS.items():
            if start.startswith(bom):
                return encoding
        
        return None
    
    @classmethod
    def has_bom(cls, file_path: Path) -> bool:
        """Prueft ob Datei einen BOM hat."""
        return cls.detect_bom(file_path) is not None
    
    @classmethod
    def detect_encoding(cls, file_path: Path) -> str:
        """
        Versucht Encoding zu erkennen.
        Fallback: utf-8 (BACH Standard)
        """
        # BOM-Pruefung
        bom_encoding = cls.detect_bom(file_path)
        if bom_encoding:
            return bom_encoding
        
        # Versuche UTF-8
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read()
            return 'utf-8'
        except UnicodeDecodeError:
            pass
        
        # Fallback: Latin-1 (kann alles lesen)
        return 'latin-1'


class SafeFileIO:
    """Sichere Datei-I/O mit konsistentem Encoding."""
    
    DEFAULT_ENCODING = 'utf-8'
    
    @classmethod
    def read_text(cls, file_path: Path, encoding: str = None) -> Tuple[str, str]:
        """
        Liest Textdatei mit automatischer Encoding-Erkennung.
        
        Returns:
            Tuple[content, detected_encoding]
        """
        path = Path(file_path)
        
        if encoding is None:
            encoding = EncodingDetector.detect_encoding(path)
        
        with open(path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
        
        return content, encoding
    
    @classmethod
    def write_text(cls, file_path: Path, content: str, 
                   encoding: str = None, add_bom: bool = False) -> None:
        """
        Schreibt Textdatei mit konsistentem Encoding.
        
        Args:
            file_path: Zielpfad
            content: Zu schreibender Inhalt
            encoding: Encoding (default: utf-8)
            add_bom: BOM am Anfang hinzufuegen
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        enc = encoding or cls.DEFAULT_ENCODING
        
        if add_bom and enc == 'utf-8':
            enc = 'utf-8-sig'
        
        with open(path, 'w', encoding=enc, newline='\n') as f:
            f.write(content)
    
    @classmethod
    def convert_encoding(cls, file_path: Path, 
                        target_encoding: str = 'utf-8',
                        remove_bom: bool = True) -> bool:
        """
        Konvertiert Datei zu Ziel-Encoding.
        
        Returns:
            True wenn Aenderung, False wenn bereits korrekt
        """
        path = Path(file_path)
        content, source_encoding = cls.read_text(path)
        
        # BOM entfernen wenn gewuenscht
        if remove_bom and content.startswith('\ufeff'):
            content = content[1:]
        
        # Nichts zu tun?
        if source_encoding == target_encoding and not remove_bom:
            return False
        
        cls.write_text(path, content, target_encoding, add_bom=False)
        return True


class BOMHandler:
    """Spezialisiert auf BOM-Operationen."""
    
    @staticmethod
    def add_bom(file_path: Path) -> bool:
        """Fuegt UTF-8 BOM hinzu wenn nicht vorhanden."""
        path = Path(file_path)
        
        if EncodingDetector.has_bom(path):
            return False
        
        content, _ = SafeFileIO.read_text(path)
        SafeFileIO.write_text(path, content, 'utf-8-sig')
        return True
    
    @staticmethod
    def remove_bom(file_path: Path) -> bool:
        """Entfernt BOM wenn vorhanden."""
        path = Path(file_path)
        
        if not EncodingDetector.has_bom(path):
            return False
        
        content, _ = SafeFileIO.read_text(path)
        
        # BOM-Zeichen entfernen
        if content.startswith('\ufeff'):
            content = content[1:]
        
        SafeFileIO.write_text(path, content, 'utf-8')
        return True


def setup_console_utf8():
    """Konfiguriert Windows-Konsole fuer UTF-8."""
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding='utf-8', errors='replace'
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding='utf-8', errors='replace'
        )


# Convenience Functions
def read_file(path: Path, encoding: str = None) -> str:
    """Liest Datei mit Auto-Encoding."""
    content, _ = SafeFileIO.read_text(path, encoding)
    return content


def write_file(path: Path, content: str, encoding: str = 'utf-8') -> None:
    """Schreibt Datei mit UTF-8 Encoding."""
    SafeFileIO.write_text(path, content, encoding)


def fix_encoding(path: Path) -> bool:
    """Konvertiert Datei zu UTF-8 ohne BOM."""
    return SafeFileIO.convert_encoding(path, 'utf-8', remove_bom=True)


if __name__ == '__main__':
    print("Encoding Module - Minimal Version")
    print(f"Default Encoding: {SafeFileIO.DEFAULT_ENCODING}")
    print(f"Platform: {sys.platform}")
    
    # Test
    test_file = Path("_test_encoding.txt")
    write_file(test_file, "Test äöü ß 日本語")
    content = read_file(test_file)
    print(f"Test content: {content}")
    test_file.unlink()
