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

# BACH ATI Policies
# Policy-Loader für das Bootstrapping-System

import json
from pathlib import Path

POLICIES_DIR = Path(__file__).parent

def load_policy(name: str) -> dict:
    """Lädt eine Policy-JSON-Datei."""
    policy_file = POLICIES_DIR / f"{name}_policy.json"
    if not policy_file.exists():
        raise FileNotFoundError(f"Policy nicht gefunden: {name}")
    with open(policy_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_all_policies() -> dict:
    """Lädt alle verfügbaren Policies."""
    policies = {}
    for policy_file in POLICIES_DIR.glob("*_policy.json"):
        name = policy_file.stem.replace("_policy", "")
        policies[name] = load_policy(name)
    return policies

# Convenience-Exporte
__all__ = ['load_policy', 'get_all_policies', 'POLICIES_DIR']
