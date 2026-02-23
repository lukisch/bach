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
BACH Inbox Rule Engine
======================

Regelbasiertes Matching fuer Dokumenten-Sortierung.

Task: INBOX_005
"""

import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class MatchResult:
    """Ergebnis eines Regel-Matches."""
    matched: bool
    rule_name: str = ""
    confidence: float = 0.0
    target_path: str = ""
    actions: List[str] = field(default_factory=list)


class Condition:
    """Einzelne Bedingung innerhalb einer Regel."""

    def __init__(self, condition_type: str, values: Any):
        self.condition_type = condition_type
        self.values = values if isinstance(values, list) else [values]

    def check(self, filename: str, content: str, metadata: Dict) -> bool:
        """Prueft ob Bedingung erfuellt ist."""
        if self.condition_type == "filename_contains":
            return any(v.lower() in filename.lower() for v in self.values)

        elif self.condition_type == "filename_regex":
            pattern = self.values[0] if self.values else ""
            return bool(re.search(pattern, filename, re.IGNORECASE))

        elif self.condition_type == "content_contains":
            if not content:
                return False
            return any(v.lower() in content.lower() for v in self.values)

        elif self.condition_type == "content_regex":
            if not content:
                return False
            pattern = self.values[0] if self.values else ""
            return bool(re.search(pattern, content, re.IGNORECASE))

        elif self.condition_type == "extension":
            ext = Path(filename).suffix.lower().lstrip(".")
            return ext in [v.lower().lstrip(".") for v in self.values]

        elif self.condition_type == "size_min_kb":
            size_kb = metadata.get("size_bytes", 0) / 1024
            return size_kb >= float(self.values[0])

        elif self.condition_type == "size_max_kb":
            size_kb = metadata.get("size_bytes", 0) / 1024
            return size_kb <= float(self.values[0])

        return True  # Unbekannte Bedingung = ignorieren


class Rule:
    """Eine Sortier-Regel."""

    def __init__(self, config: Dict[str, Any]):
        self.name = config.get("name", "Unnamed")
        self.priority = config.get("priority", 100)
        self.target = config.get("target", "")
        self.actions = config.get("actions", [])
        self.enabled = config.get("enabled", True)

        # Parse Bedingungen
        self.conditions: List[Condition] = []
        conditions_config = config.get("conditions", {})
        for cond_type, cond_values in conditions_config.items():
            self.conditions.append(Condition(cond_type, cond_values))

    def match(self, filename: str, content: str = "", metadata: Dict = None) -> MatchResult:
        """Prueft ob Regel matched."""
        if not self.enabled:
            return MatchResult(matched=False)

        if metadata is None:
            metadata = {}

        # Alle Bedingungen muessen erfuellt sein (AND-Logik)
        all_matched = all(c.check(filename, content, metadata) for c in self.conditions)

        if all_matched:
            target = self._expand_target()
            return MatchResult(
                matched=True,
                rule_name=self.name,
                confidence=1.0,
                target_path=target,
                actions=self.actions
            )

        return MatchResult(matched=False)

    def _expand_target(self) -> str:
        """Expandiert Variablen im Zielpfad."""
        target = self.target

        # {year} -> aktuelles Jahr
        target = target.replace("{year}", str(datetime.now().year))

        # {month} -> aktueller Monat
        target = target.replace("{month}", datetime.now().strftime("%m"))

        # {date} -> aktuelles Datum
        target = target.replace("{date}", datetime.now().strftime("%Y-%m-%d"))

        return target


class RuleSet:
    """Sammlung von Regeln mit Prioritaets-Sortierung."""

    def __init__(self, config_path: Optional[Path] = None):
        self.rules: List[Rule] = []
        self.fallback_target = ""
        self.create_task_on_fallback = True

        if config_path and config_path.exists():
            self.load(config_path)

    def load(self, config_path: Path):
        """Laedt Regeln aus JSON-Konfiguration."""
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))

            # Regeln laden
            for rule_config in config.get("rules", []):
                self.rules.append(Rule(rule_config))

            # Nach Prioritaet sortieren (niedrig = wichtiger)
            self.rules.sort(key=lambda r: r.priority)

            # Fallback-Einstellungen
            fallback = config.get("fallback", {})
            self.fallback_target = fallback.get("target", "")
            self.create_task_on_fallback = fallback.get("create_task", True)

        except Exception as e:
            print(f"[RuleEngine] Fehler beim Laden: {e}")

    def add_rule(self, rule: Rule):
        """Fuegt Regel hinzu und sortiert neu."""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority)

    def remove_rule(self, name: str):
        """Entfernt Regel nach Name."""
        self.rules = [r for r in self.rules if r.name != name]

    def find_match(self, filename: str, content: str = "", metadata: Dict = None) -> MatchResult:
        """Findet erste passende Regel (First-Match-Prinzip)."""
        for rule in self.rules:
            result = rule.match(filename, content, metadata)
            if result.matched:
                return result

        # Fallback
        return MatchResult(
            matched=False,
            rule_name="[Fallback]",
            target_path=self.fallback_target,
            actions=["create_task"] if self.create_task_on_fallback else []
        )

    def test_file(self, filename: str, content: str = "") -> List[Dict[str, Any]]:
        """Testet Datei gegen alle Regeln (fuer Debugging)."""
        results = []
        for rule in self.rules:
            result = rule.match(filename, content)
            results.append({
                "rule": rule.name,
                "priority": rule.priority,
                "matched": result.matched,
                "target": result.target_path if result.matched else ""
            })
        return results

    def to_dict(self) -> Dict[str, Any]:
        """Exportiert Regeln als Dictionary."""
        return {
            "rules": [
                {
                    "name": r.name,
                    "priority": r.priority,
                    "conditions": {c.condition_type: c.values for c in r.conditions},
                    "target": r.target,
                    "actions": r.actions,
                    "enabled": r.enabled
                }
                for r in self.rules
            ],
            "fallback": {
                "target": self.fallback_target,
                "create_task": self.create_task_on_fallback
            }
        }


# ═══════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════

def create_rule_from_example(
    name: str,
    filename_patterns: List[str] = None,
    content_patterns: List[str] = None,
    target: str = "",
    priority: int = 50
) -> Rule:
    """Erstellt Regel aus einfachen Parametern."""
    config = {
        "name": name,
        "priority": priority,
        "target": target,
        "conditions": {}
    }

    if filename_patterns:
        config["conditions"]["filename_contains"] = filename_patterns

    if content_patterns:
        config["conditions"]["content_contains"] = content_patterns

    return Rule(config)


if __name__ == "__main__":
    # Test
    ruleset = RuleSet()
    ruleset.add_rule(create_rule_from_example(
        name="Test-Rechnung",
        filename_patterns=["rechnung", "invoice"],
        target="/tmp/rechnungen/{year}/"
    ))

    result = ruleset.find_match("Rechnung_2026.pdf")
    print(f"Match: {result.matched}, Target: {result.target_path}")
