#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
POLICY: emoji_safe
VERSION: 1.0
SIZE: small (inline injection)
DESCRIPTION: Sichere Emoji-Handhabung fuer Speicherung/Transfer

Funktionen:
  - emoji_to_safe(text): Emoji -> ASCII-safe Text fuer Speicherung
  - emoji_to_display(text): ASCII-safe Text -> Emoji fuer Anzeige
"""

# === POLICY:emoji_safe:1.0 ===
try:
    import emoji as _emoji_pkg
    _EMOJI_AVAILABLE = True
except ImportError:
    _emoji_pkg = None
    _EMOJI_AVAILABLE = False

def emoji_to_safe(text: str) -> str:
    """Emoji -> ASCII-safe Text fuer Speicherung/Transfer"""
    if _EMOJI_AVAILABLE and text:
        return _emoji_pkg.demojize(text)
    return text

def emoji_to_display(text: str) -> str:
    """ASCII-safe Text -> Emoji fuer Anzeige"""
    if _EMOJI_AVAILABLE and text:
        return _emoji_pkg.emojize(text)
    return text
# === END:emoji_safe ===
