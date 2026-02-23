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
MistralClassifier - Event-Klassifikation via lokales Mistral-Modell
====================================================================
Nutzt OllamaClient (Chat-API) um eingehende Events in 4 Aktions-Kategorien
zu klassifizieren.

Version: 1.0.1
Erstellt: 2026-02-10
"""

import json
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from pathlib import Path


class EventAction(Enum):
    """Moegliche Aktionen nach Klassifikation."""
    RESPOND_DIRECT = "respond_direct"
    ESCALATE_CLAUDE = "escalate_claude"
    LOG_ONLY = "log_only"
    IGNORE = "ignore"


@dataclass
class WatcherEvent:
    """Ein eingehendes Event aus einer beliebigen Quelle."""
    source: str              # "connector", "filesystem", "task_queue", "scheduled"
    event_type: str          # "message", "file_created", "new_task", "cron"
    content: str             # Der eigentliche Inhalt/Text
    sender: str              # Wer/Was hat es generiert
    connector_name: str = "" # Welcher Connector (fuer Antworten)
    recipient: str = ""      # Reply-To Ziel
    metadata: dict = field(default_factory=dict)
    timestamp: str = ""
    source_id: int = 0       # DB-ID der Quell-Nachricht


@dataclass
class ClassificationResult:
    """Ergebnis einer Klassifikation."""
    action: EventAction
    confidence: float = 0.0
    reasoning: str = ""
    direct_response: str = ""
    escalation_profile: str = ""
    processing_time_ms: int = 0
    raw_response: str = ""


class MistralClassifier:
    """
    Klassifiziert Events via Mistral (OllamaClient Chat-API).

    Nutzt chat() statt generate() - schneller und zuverlaessiger
    mit System-Prompt. Temperatur 0.1 fuer konsistente Ergebnisse.
    """

    MODEL = "Mistral:latest"
    TEMPERATURE = 0.1
    TIMEOUT = 120

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self._client = None
        self._system_prompt = None
        self._prompts_dir = Path(__file__).parent / "prompts"

    @property
    def client(self):
        """Lazy-Load OllamaClient."""
        if self._client is None:
            import sys
            tools_path = str(self.base_path / "tools" / "ollama")
            if tools_path not in sys.path:
                sys.path.insert(0, tools_path)
            from ollama_client import OllamaClient
            self._client = OllamaClient(timeout=self.TIMEOUT)
        return self._client

    def _load_system_prompt(self) -> str:
        """Laedt Klassifikations-Systemprompt."""
        if self._system_prompt is None:
            prompt_file = self._prompts_dir / "classify_event.txt"
            if prompt_file.exists():
                self._system_prompt = prompt_file.read_text(encoding="utf-8")
            else:
                self._system_prompt = (
                    'Classify as: RESPOND_DIRECT, ESCALATE_CLAUDE, LOG_ONLY, IGNORE. '
                    'Reply JSON: {"action":"...","confidence":0.9,"reasoning":"...","response":"","profile":""}'
                )
        return self._system_prompt

    def is_available(self) -> bool:
        """Prueft ob Mistral einsatzbereit ist."""
        try:
            return self.client.is_available() and self.client.has_model(self.MODEL)
        except Exception:
            return False

    def warmup(self) -> float:
        """Warmup-Call um Modell in GPU zu laden. Gibt Dauer in Sekunden zurueck."""
        start = time.time()
        try:
            self.client.chat(
                [{"role": "user", "content": "Say OK"}],
                model=self.MODEL
            )
        except Exception:
            pass
        return time.time() - start

    def classify(self, event: WatcherEvent) -> ClassificationResult:
        """
        Klassifiziert ein einzelnes Event via Chat-API.

        Returns:
            ClassificationResult mit Aktion und Metadaten.
            Bei Fehlern: ESCALATE_CLAUDE als sicherer Fallback.
        """
        start = time.time()

        user_prompt = self._build_classify_prompt(event)

        try:
            response = self.client.chat(
                messages=[
                    {"role": "system", "content": self._load_system_prompt()},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.MODEL
            )

            if not response.success:
                return self._fallback_result(start, f"Ollama-Fehler: {response.error}")

            result = self._parse_response(response.text)
            result.processing_time_ms = int((time.time() - start) * 1000)
            result.raw_response = response.text
            return result

        except Exception as e:
            return self._fallback_result(start, str(e))

    def generate_response(self, event: WatcherEvent) -> str:
        """
        Generiert eine direkte Antwort fuer RESPOND_DIRECT Events.
        Wird nur aufgerufen wenn die Klassifikation keine Antwort enthielt.
        """
        try:
            response = self.client.chat(
                messages=[
                    {"role": "system", "content": "Du bist BACH, ein persoenlicher KI-Assistent. Antworte kurz (1-2 Saetze), freundlich, auf Deutsch."},
                    {"role": "user", "content": f"Nachricht von {event.sender} via {event.connector_name or event.source}: {event.content}"}
                ],
                model=self.MODEL
            )
            return response.text.strip() if response.success else ""
        except Exception:
            return ""

    def _build_classify_prompt(self, event: WatcherEvent) -> str:
        """Baut den Klassifikations-Prompt aus dem Event."""
        parts = [f"Message from {event.sender}"]
        if event.connector_name:
            parts[0] += f" via {event.connector_name}"
        parts.append(f": {event.content[:500]}")
        return "".join(parts)

    def _parse_response(self, text: str) -> ClassificationResult:
        """Parst Mistral-Antwort in ClassificationResult."""
        json_data = self._extract_json(text)

        if json_data:
            action_str = json_data.get("action", "ESCALATE_CLAUDE").upper()
            action_map = {
                "RESPOND_DIRECT": EventAction.RESPOND_DIRECT,
                "ESCALATE_CLAUDE": EventAction.ESCALATE_CLAUDE,
                "LOG_ONLY": EventAction.LOG_ONLY,
                "IGNORE": EventAction.IGNORE,
            }
            action = action_map.get(action_str, EventAction.ESCALATE_CLAUDE)

            return ClassificationResult(
                action=action,
                confidence=float(json_data.get("confidence", 0.5)),
                reasoning=json_data.get("reasoning", ""),
                direct_response=json_data.get("response", ""),
                escalation_profile=json_data.get("profile", ""),
            )

        # Fallback: Keywords in Rohtext suchen
        text_upper = text.upper()
        if "RESPOND_DIRECT" in text_upper:
            return ClassificationResult(action=EventAction.RESPOND_DIRECT, confidence=0.3, reasoning="Keyword-Match")
        if "LOG_ONLY" in text_upper:
            return ClassificationResult(action=EventAction.LOG_ONLY, confidence=0.3, reasoning="Keyword-Match")
        if "IGNORE" in text_upper:
            return ClassificationResult(action=EventAction.IGNORE, confidence=0.3, reasoning="Keyword-Match")

        return ClassificationResult(
            action=EventAction.ESCALATE_CLAUDE,
            confidence=0.1,
            reasoning="Konnte Antwort nicht parsen - sicher eskalieren"
        )

    def _extract_json(self, text: str) -> Optional[dict]:
        """Extrahiert JSON aus Text (robust)."""
        text = text.strip()
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            pass

        match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except (json.JSONDecodeError, ValueError):
                pass

        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except (json.JSONDecodeError, ValueError):
                pass

        return None

    def _fallback_result(self, start_time: float, error: str) -> ClassificationResult:
        """Erzeugt sicheren Fallback bei Fehlern."""
        return ClassificationResult(
            action=EventAction.ESCALATE_CLAUDE,
            confidence=0.0,
            reasoning=f"Fallback: {error}",
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
