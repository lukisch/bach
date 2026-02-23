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
PDF-Verarbeitungs-Service fuer BACH.

Nutzt pypdf fuer Basis-Operationen und Anthropic PDF Skills
aus _vendor/anthropic_pdf/ fuer erweiterte Funktionen.
"""

import sys
from pathlib import Path


class PDFProcessor:
    """Stellt Funktionen zur PDF-Verarbeitung bereit."""

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extrahiert Text aus einer PDF-Datei via pypdf."""
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    @staticmethod
    def get_metadata(file_path: str) -> dict:
        """Liest PDF-Metadaten."""
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        meta = reader.metadata
        return {k: str(v) for k, v in (meta or {}).items()}

    @staticmethod
    def get_page_count(file_path: str) -> int:
        """Gibt die Seitenzahl zurueck."""
        from pypdf import PdfReader
        return len(PdfReader(file_path).pages)

    @staticmethod
    def extract_form_fields(file_path: str) -> list:
        """Extrahiert Formularfelder mit Typ, Position und Optionen.

        Nutzt anthropic_pdf Vendor-Tool fuer detaillierte Feld-Analyse.
        """
        from pypdf import PdfReader
        # Vendor-Modul hat relative Imports; wir nutzen die Funktion direkt
        vendor_dir = Path(__file__).parent / "_vendor" / "anthropic_pdf"
        sys.path.insert(0, str(vendor_dir))
        try:
            from extract_form_field_info import get_field_info
            reader = PdfReader(file_path)
            return get_field_info(reader)
        finally:
            sys.path.pop(0)

    @staticmethod
    def extract_form_structure(file_path: str) -> dict:
        """Extrahiert Formular-Struktur (Labels, Linien, Checkboxen).

        Nutzt pdfplumber fuer Struktur-Analyse.
        """
        vendor_dir = Path(__file__).parent / "_vendor" / "anthropic_pdf"
        sys.path.insert(0, str(vendor_dir))
        try:
            from extract_form_structure import extract_form_structure
            return extract_form_structure(file_path)
        finally:
            sys.path.pop(0)

    @staticmethod
    def fill_form(file_path: str, field_values: dict, output_path: str) -> str:
        """Fuellt PDF-Formularfelder aus.

        Args:
            file_path: Pfad zur Quell-PDF
            field_values: Dict {field_id: value} oder Liste von Dicts
            output_path: Pfad fuer die ausgefuellte PDF

        Returns:
            Pfad zur ausgefuellten PDF
        """
        from pypdf import PdfReader, PdfWriter

        reader = PdfReader(file_path)
        writer = PdfWriter(clone_from=reader)

        # field_values nach Seiten gruppieren
        if isinstance(field_values, dict):
            # Einfaches Format: alle Felder auf einmal setzen
            for page in writer.pages:
                writer.update_page_form_field_values(
                    page, field_values, auto_regenerate=False
                )
        elif isinstance(field_values, list):
            # Listen-Format aus Vendor-Tool: [{field_id, page, value}, ...]
            by_page = {}
            for entry in field_values:
                pg = entry.get("page", 1)
                by_page.setdefault(pg, {})[entry["field_id"]] = entry["value"]
            for pg, vals in by_page.items():
                writer.update_page_form_field_values(
                    writer.pages[pg - 1], vals, auto_regenerate=False
                )

        writer.set_need_appearances_writer(True)
        with open(output_path, "wb") as f:
            writer.write(f)
        return output_path

    @staticmethod
    def to_images(file_path: str, output_dir: str, max_dim: int = 1000) -> list:
        """Konvertiert PDF-Seiten zu PNG-Bildern.

        Benoetigt pdf2image + poppler.

        Args:
            file_path: Pfad zur PDF
            output_dir: Ausgabe-Ordner fuer die Bilder
            max_dim: Maximale Dimension (Breite/Hoehe) in Pixeln

        Returns:
            Liste der erzeugten Bild-Pfade
        """
        from pdf2image import convert_from_path

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        images = convert_from_path(file_path, dpi=200)
        paths = []

        for i, image in enumerate(images):
            width, height = image.size
            if width > max_dim or height > max_dim:
                scale = min(max_dim / width, max_dim / height)
                image = image.resize((int(width * scale), int(height * scale)))
            img_path = str(Path(output_dir) / f"page_{i + 1}.png")
            image.save(img_path)
            paths.append(img_path)

        return paths

    @staticmethod
    def check_fillable(file_path: str) -> bool:
        """Prueft ob die PDF ausfuellbare Formularfelder hat."""
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        fields = reader.get_fields()
        return bool(fields)
