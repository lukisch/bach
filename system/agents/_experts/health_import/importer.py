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
Health Import Expert
====================

Verarbeitet medizinische Dokumente (PDFs, Bilder) und extrahiert strukturierte Daten.
Nutzt die universelle OCR Engine und LLM.
"""

import os
import json
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# BACH imports
# Assuming generic structure for imports as typical in this project
from tools.ocr.engine import get_engine
from skills._services.document.anonymizer_service import AnonymizerProfile # Optional usage
# LLM Import - pending standard wrapper, using generic placeholder or direct
# We will use the 'gemini_llm.py' or similar if reachable, 
# but usually experts trigger LLMs via the Cortex/Agent interface.
# For now, we simulate the LLM call or assume a `call_llm` helper is passed/available.
# To fit "Systemisch First", we should likely use a generic LLM service.

logger = logging.getLogger("health_import")

class HealthImporter:
    def __init__(self, output_dir: str, archive_dir: str, llm_callback=None):
        self.output_dir = Path(output_dir)
        self.archive_dir = Path(archive_dir)
        self.ocr_engine = get_engine()
        self.llm_callback = llm_callback
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Load Schema
        self.schema_path = Path(__file__).parent / "schemas" / "health_doc.json"
        self.schema = json.loads(self.schema_path.read_text(encoding="utf-8"))

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Processes a single file: OCR -> LLM Extraction -> Save JSON -> Archive File.
        """
        path = Path(file_path)
        if not path.exists():
            return {"success": False, "error": "File not found"}

        logger.info(f"Processing {path.name}...")

        # 1. OCR / Text Extraction
        try:
            text = self.ocr_engine.extract_text(str(path), lang="deu+eng")
        except Exception as e:
            return {"success": False, "error": f"OCR Failed: {e}"}

        if not text or len(text) < 10:
             return {"success": False, "error": "No text extracted"}

        # 2. LLM Extraction
        if not self.llm_callback:
            # Fallback / Dry Run if no LLM
             return {"success": False, "error": "No LLM callback provided", "ocr_text": text}
        
        try:
            prompt = self._build_prompt(text)
            llm_response = self.llm_callback(prompt, output_json=True) # Expecting JSON response
            data = llm_response if isinstance(llm_response, dict) else json.loads(llm_response)
        except Exception as e:
             return {"success": False, "error": f"LLM Extraction Failed: {e}"}

        # 3. Post-Processing & Saving
        saved_path = self._save_result(data, path)
        
        # 4. Archive/Move Original
        # We move the original file to specific folder structure like YYYY/Doctor/
        archive_rel_path = self._archive_original(path, data)

        return {
            "success": True,
            "data": data,
            "saved_json": str(saved_path),
            "archived_file": str(archive_rel_path)
        }

    def _build_prompt(self, text: str) -> str:
        return f"""
Du bist ein medizinischer Assistent. Analysiere das folgende Dokument und extrahiere Informationen im JSON-Format.
Halte dich strikt an das Schema.

DOKUMENTEN-TEXT:
{text[:10000]}  # Truncate if too long

SCHEMA:
{json.dumps(self.schema)}
"""

    def _save_result(self, data: Dict, original_path: Path) -> Path:
        """Saves extracted data to JSON file."""
        # Naming convention: YYYY-MM-DD_Type_Doctor.json
        date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
        doc_type = data.get("document_type", "Doc")
        doctor = data.get("doctor", {}).get("name", "Unknown")
        
        # Sanitize
        safe_doc = doctor.replace(" ", "_").replace(".", "")
        filename = f"{date_str}_{doc_type}_{safe_doc}.json"
        
        target = self.output_dir / filename
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        return target

    def _archive_original(self, path: Path, data: Dict) -> Path:
        """Moves original file to structured archive."""
        year = data.get("date", datetime.now().strftime("%Y-%m-%d"))[:4]
        target_dir = self.archive_dir / year
        target_dir.mkdir(exist_ok=True)
        
        target_path = target_dir / path.name
        # Handle duplicates
        if target_path.exists():
            stem = path.stem
            ext = path.suffix
            timestamp = datetime.now().strftime("%H%M%S")
            target_path = target_dir / f"{stem}_{timestamp}{ext}"
            
        shutil.move(str(path), str(target_path))
        return target_path

# Helper for CLI usage
def run_cli_import(input_path: str, output_dir: str, llm_func=None):
    importer = HealthImporter(output_dir, output_dir + "/_archive", llm_callback=llm_func)
    return importer.process_file(input_path)
