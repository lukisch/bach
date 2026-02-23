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
DirectResponder - Sendet Mistral-Antworten via Connector zurueck
================================================================
Fuer RESPOND_DIRECT Events wird die Antwort in die connector_messages
Outbound-Queue eingefuegt. Der existierende dispatch-Job sendet sie.

Version: 1.0.0
Erstellt: 2026-02-10
"""

import sqlite3
from datetime import datetime
from pathlib import Path

try:
    from .classifier import WatcherEvent, ClassificationResult
except ImportError:
    from classifier import WatcherEvent, ClassificationResult


class DirectResponder:
    """
    Sendet direkte Antworten via bestehende Connector-Queue.

    Nutzt connector_messages Tabelle (direction='out') - der existierende
    dispatch Daemon-Job sendet die Nachricht via Telegram/Discord.
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def respond(self, event: WatcherEvent, response_text: str) -> bool:
        """
        Reiht Antwort-Nachricht in Outbound-Queue ein.

        Returns:
            True wenn erfolgreich eingefuegt.
        """
        if not response_text or not event.connector_name:
            return False

        # Encoding-Sanitierung
        try:
            from tools.encoding_fix import sanitize_outbound
            response_text = sanitize_outbound(response_text)
        except ImportError:
            pass

        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.execute(
                "INSERT INTO connector_messages "
                "(connector_name, direction, sender, recipient, content, processed, created_at) "
                "VALUES (?, 'out', 'bach-watcher', ?, ?, 0, ?)",
                (
                    event.connector_name,
                    event.sender,
                    response_text,
                    datetime.now().isoformat(),
                )
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    def log_event(self, event: WatcherEvent, result: ClassificationResult,
                  response_sent: str = "") -> bool:
        """
        Loggt ein klassifiziertes Event in watcher_event_log.
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.execute(
                "INSERT INTO watcher_event_log "
                "(source, event_type, sender, content_preview, action, "
                "confidence, reasoning, response_sent, escalation_profile, "
                "processing_time_ms, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event.source,
                    event.event_type,
                    event.sender,
                    event.content[:200],
                    result.action.value,
                    result.confidence,
                    result.reasoning,
                    response_sent,
                    result.escalation_profile,
                    result.processing_time_ms,
                    datetime.now().isoformat(),
                )
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False
