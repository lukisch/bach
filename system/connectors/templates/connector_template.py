#!/usr/bin/env python3
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
{{CONNECTOR_NAME}}Connector - {{CONNECTOR_DISPLAY_NAME}} Connector fuer BACH
==============================================================================

{{CONNECTOR_DESCRIPTION}}

Implementiert BaseConnector fuer {{CONNECTOR_DISPLAY_NAME}}.

Verwendung:
    from connectors.{{CONNECTOR_MODULE}} import {{CONNECTOR_NAME}}Connector
    from connectors.base import ConnectorConfig

    config = ConnectorConfig(
        name="{{CONNECTOR_INSTANCE_NAME}}",
        connector_type="{{CONNECTOR_TYPE}}",
        auth_type="{{AUTH_TYPE}}",
        auth_config={{AUTH_CONFIG_EXAMPLE}},
        options={{OPTIONS_EXAMPLE}}
    )
    connector = {{CONNECTOR_NAME}}Connector(config)
    connector.connect()
    messages = connector.get_messages()
    connector.send_message("{{RECIPIENT_EXAMPLE}}", "Hallo von BACH!")
"""

import os
import sys
import json
import time
import threading
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Optional, Callable, Tuple

# UTF-8 Encoding fix
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from connectors.base import BaseConnector, ConnectorConfig, ConnectorStatus, Message


class {{CONNECTOR_NAME}}Connector(BaseConnector):
    """{{CONNECTOR_DISPLAY_NAME}} Connector mit Polling-Runtime."""

    {{API_BASE_COMMENT}}
    API_BASE = "{{API_BASE_URL}}"

    def __init__(self, config: ConnectorConfig):
        super().__init__(config)
        {{INIT_VARIABLES}}
        self._polling = False

    def connect(self) -> bool:
        """Verbindung pruefen."""
        {{CONNECT_VALIDATION}}

        self._status = ConnectorStatus.CONNECTING
        try:
            {{CONNECT_IMPLEMENTATION}}
            self._status = ConnectorStatus.CONNECTED
            return True
        except Exception as e:
            print(f"[{{CONNECTOR_NAME}} connect Error] {type(e).__name__}: {e}", file=sys.stderr)

        self._status = ConnectorStatus.ERROR
        return False

    def disconnect(self) -> bool:
        """Verbindung trennen."""
        self._polling = False
        self._status = ConnectorStatus.DISCONNECTED
        return True

    def send_message(self, recipient: str, content: str,
                     attachments: Optional[List[str]] = None) -> bool:
        """Nachricht senden."""
        try:
            {{SEND_MESSAGE_IMPLEMENTATION}}
            return True
        except Exception as e:
            print(f"[{{CONNECTOR_NAME}} send_message Error] {type(e).__name__}: {e}", file=sys.stderr)
            return False

    def get_messages(self, since: Optional[str] = None,
                     limit: int = 50) -> List[Message]:
        """Neue Nachrichten abrufen."""
        try:
            {{GET_MESSAGES_IMPLEMENTATION}}

            messages = []
            {{PARSE_MESSAGES_IMPLEMENTATION}}

            return messages
        except Exception as e:
            print(f"[{{CONNECTOR_NAME}} get_messages Error] {type(e).__name__}: {e}", file=sys.stderr)
            return []

    # ------------------------------------------------------------------
    # Polling Runtime (optional - kann entfernt werden wenn nicht benoetigt)
    # ------------------------------------------------------------------

    def poll_loop(self, on_message: Callable[[Message], None],
                  interval: float = 5.0, stop_event: threading.Event = None):
        """Blockierender Polling-Loop. Ruft on_message() fuer jede neue Nachricht auf."""
        self._polling = True
        while self._polling and not (stop_event and stop_event.is_set()):
            try:
                messages = self.get_messages()
                for msg in messages:
                    try:
                        on_message(msg)
                    except Exception as e:
                        print(f"[{{CONNECTOR_NAME}} on_message callback Error] {type(e).__name__}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"[{{CONNECTOR_NAME}} poll_loop Error] {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(interval)

    def poll_threaded(self, on_message: Callable[[Message], None],
                      interval: float = 5.0) -> Tuple[threading.Thread, threading.Event]:
        """Startet Polling in eigenem Thread. Gibt (Thread, StopEvent) zurueck."""
        stop_event = threading.Event()
        thread = threading.Thread(
            target=self.poll_loop,
            args=(on_message, interval, stop_event),
            daemon=True, name="bach-{{CONNECTOR_TYPE}}-poll")
        thread.start()
        return thread, stop_event

    # ------------------------------------------------------------------
    # Internal Helper Methods
    # ------------------------------------------------------------------

    {{HELPER_METHODS}}
