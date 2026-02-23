#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
BACH OCR CLI Tool
=================

Command line interface for the OCR engine.
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.ocr.engine import get_engine

def main():
    parser = argparse.ArgumentParser(description="Extract text from images/PDFs.")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("--lang", default="deu+eng", help="OCR Language (default: deu+eng)")
    parser.add_argument("--output", "-o", help="Output file (optional, otherwise stdout)")
    
    args = parser.parse_args()
    
    engine = get_engine()
    if not engine.available:
        print("Error: Tesseract OCR not available.", file=sys.stderr)
        sys.exit(1)
        
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found.", file=sys.stderr)
        sys.exit(1)
        
    results = []
    
    if input_path.is_file():
        text = engine.extract_text(str(input_path), args.lang)
        results.append(f"--- File: {input_path.name} ---\n{text}")
        
    elif input_path.is_dir():
        for file in input_path.iterdir():
            if file.suffix.lower() in [".pdf", ".jpg", ".png"]:
                text = engine.extract_text(str(file), args.lang)
                results.append(f"--- File: {file.name} ---\n{text}")
    
    full_text = "\n\n".join(results)
    
    if args.output:
        Path(args.output).write_text(full_text, encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(full_text)

if __name__ == "__main__":
    main()
