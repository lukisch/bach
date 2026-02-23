#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
POLICY: json_safe
VERSION: 1.0
SIZE: medium (externe Datei)
DESCRIPTION: Sichere JSON-Operationen mit Emoji/Encoding-Handling

Funktionen:
  - json_load_safe(filepath): Laedt JSON mit Encoding-Fallback
  - json_save_safe(data, filepath): Speichert JSON mit Emoji-Konvertierung
  - json_dumps_safe(data): Serialisiert mit ensure_ascii=False
"""

# === POLICY:json_safe:1.0 ===
import json
from pathlib import Path
from typing import Any, Union

try:
    import emoji as _emoji_pkg
    _EMOJI_AVAILABLE = True
except ImportError:
    _emoji_pkg = None
    _EMOJI_AVAILABLE = False


def _emoji_to_safe(text: str) -> str:
    """Intern: Emoji -> ASCII-safe"""
    if _EMOJI_AVAILABLE and isinstance(text, str):
        return _emoji_pkg.demojize(text)
    return text


def _process_for_save(obj: Any) -> Any:
    """Rekursiv alle Strings in dict/list konvertieren"""
    if isinstance(obj, str):
        return _emoji_to_safe(obj)
    elif isinstance(obj, dict):
        return {k: _process_for_save(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_process_for_save(item) for item in obj]
    return obj


def json_load_safe(filepath: Union[str, Path]) -> Any:
    """Laedt JSON mit Encoding-Fallback"""
    filepath = Path(filepath)
    
    for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    
    raise ValueError(f"Konnte {filepath} nicht laden")


def json_save_safe(data: Any, filepath: Union[str, Path], 
                   convert_emojis: bool = True) -> None:
    """Speichert JSON mit optionaler Emoji-Konvertierung"""
    filepath = Path(filepath)
    
    if convert_emojis:
        data = _process_for_save(data)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def json_dumps_safe(data: Any, convert_emojis: bool = True) -> str:
    """Serialisiert zu JSON-String"""
    if convert_emojis:
        data = _process_for_save(data)
    return json.dumps(data, indent=2, ensure_ascii=False)
# === END:json_safe ===
