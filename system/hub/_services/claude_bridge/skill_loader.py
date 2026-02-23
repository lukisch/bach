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
SKILL.md Auto-Loader für Bridge
================================
Lädt automatisch beim Bridge-Start:
- SKILL.md (Root-Skill)
- persoenlicher-assistent.txt

Wird vom System-Prompt-Builder aufgerufen.
"""

from pathlib import Path
from typing import List

BACH_DIR = Path(__file__).parent.parent.parent.parent.parent  # claude_bridge → _services → hub → system → BACH_v2_vanilla

def log(msg: str, level: str = "INFO"):
    """Einfacher Logger."""
    print(f"[{level}] [SkillLoader] {msg}")

def load_startup_skills() -> str:
    """
    Lädt SKILL.md + persoenlicher-assistent beim Start.

    Returns:
        Formatierter String mit allen Skills
    """
    skills = []

    # 1. SKILL.md (root)
    root_skill = BACH_DIR / "SKILL.md"
    if root_skill.exists():
        try:
            content = root_skill.read_text(encoding='utf-8')
            skills.append(f"### SKILL.md (Root-Skill)\n{content}")
            log(f"SKILL.md geladen ({len(content)} Zeichen)", "INFO")
        except Exception as e:
            log(f"Fehler beim Laden von SKILL.md: {e}", "ERROR")
    else:
        log("SKILL.md nicht gefunden", "WARN")

    # 2. Persönlicher Assistent
    assistant_paths = [
        BACH_DIR / "skills" / "persoenlicher-assistent.txt",
        BACH_DIR / "agents" / "persoenlicher-assistent.txt",
    ]

    assistant_loaded = False
    for assistant_skill in assistant_paths:
        if assistant_skill.exists():
            try:
                content = assistant_skill.read_text(encoding='utf-8')
                skills.append(f"### Persönlicher Assistent\n{content}")
                log(f"persoenlicher-assistent.txt geladen von {assistant_skill.parent.name}/ ({len(content)} Zeichen)", "INFO")
                assistant_loaded = True
                break
            except Exception as e:
                log(f"Fehler beim Laden von {assistant_skill}: {e}", "ERROR")

    if not assistant_loaded:
        log("persoenlicher-assistent.txt nicht gefunden", "WARN")

    # Ergebnis zusammenbauen
    if not skills:
        return "# Keine Skills geladen (SKILL.md fehlt)"

    result = "\n\n".join(skills)
    log(f"Gesamt {len(skills)} Skills geladen", "INFO")
    return result

def get_skill_summary() -> List[str]:
    """
    Gibt Liste der geladenen Skill-Dateien zurück (für Logging/Debug).

    Returns:
        Liste von Dateinamen
    """
    loaded = []

    root_skill = BACH_DIR / "SKILL.md"
    if root_skill.exists():
        loaded.append("SKILL.md")

    assistant_paths = [
        BACH_DIR / "skills" / "persoenlicher-assistent.txt",
        BACH_DIR / "agents" / "persoenlicher-assistent.txt",
    ]

    for path in assistant_paths:
        if path.exists():
            loaded.append(f"{path.parent.name}/persoenlicher-assistent.txt")
            break

    return loaded

if __name__ == "__main__":
    # Test
    print("=== Skill-Loader Test ===")
    print(f"Skills gefunden: {get_skill_summary()}")
    print("\n=== Geladener Content ===")
    print(load_startup_skills())
