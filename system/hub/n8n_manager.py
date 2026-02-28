# SPDX-License-Identifier: MIT
"""
n8n_manager.py -- n8n Workflow Manager BACH-Integration (STUB)

Verweist auf MODULAR_AGENTS/n8nManager/ fuer vollstaendige Implementierung.
Bietet BACH-Handler-Interface fuer n8n-Workflow-Verwaltung.

n8n laeuft standardmaessig auf Port 5678.
Verbindung: http://localhost:5678

TODO: Integration wenn n8nManager stabil
Referenz: MODULAR_AGENTS/n8nManager/README.md
SQ081: n8n Workflow Manager
"""
from __future__ import annotations

import urllib.request
import urllib.error
from typing import Optional


# Pfad zum externen n8nManager-Modul
_N8N_MANAGER_PATH = r'C:\Users\lukas\OneDrive\KI&AI\MODULAR_AGENTS\n8nManager'


class N8nManagerHandler:
    """
    BACH-Handler fuer n8n Workflow Manager Integration.

    Stellt grundlegende n8n-Operationen bereit:
    - status: n8n-Instanz pruefen
    - list:   Workflows auflisten
    - sync:   Workflows synchronisieren

    Verbindung zum externen n8nManager-Modul in MODULAR_AGENTS/n8nManager/.
    """

    profile_name = "n8n-manager"
    N8N_DEFAULT_URL = 'http://localhost:5678'

    def __init__(self, n8n_base_url: str = None):
        self.n8n_base_url = n8n_base_url or self.N8N_DEFAULT_URL
        self._n8n_manager_path = _N8N_MANAGER_PATH

    def get_operations(self) -> dict:
        """Gibt verfuegbare Operationen zurueck."""
        return {
            "status": "n8n Status pruefen: n8n-manager status",
            "list":   "Workflows auflisten: n8n-manager list",
            "sync":   "Workflows synchronisieren: n8n-manager sync",
        }

    def _check_n8n_running(self) -> bool:
        """Prueft ob n8n erreichbar ist."""
        try:
            req = urllib.request.urlopen(
                f'{self.n8n_base_url}/healthz',
                timeout=3
            )
            return req.status == 200
        except (urllib.error.URLError, Exception):
            pass
        # Fallback: /api/v1/workflows pruefen
        try:
            req = urllib.request.urlopen(
                f'{self.n8n_base_url}/api/v1/workflows',
                timeout=3
            )
            return True
        except Exception:
            return False

    def handle(self, operation: str = 'status', **kwargs) -> dict:
        """
        Hauptentrypoint fuer BACH-Handler-Aufrufe.

        Args:
            operation: 'status' | 'list' | 'sync'
            **kwargs:  Operation-spezifische Parameter

        Returns:
            dict mit Ergebnis
        """
        if operation == 'status':
            running = self._check_n8n_running()
            return {
                'status': 'ok' if running else 'warning',
                'n8n_running': running,
                'n8n_url': self.n8n_base_url,
                'message': 'n8n erreichbar' if running else 'n8n nicht erreichbar (laeuft n8n?)',
            }

        elif operation == 'list':
            if not self._check_n8n_running():
                return {
                    'status': 'error',
                    'message': 'n8n nicht erreichbar -- bitte n8n starten',
                }
            # TODO: Vollstaendige Implementierung via n8nManager
            return {
                'status': 'stub',
                'message': 'list noch nicht implementiert (TODO: n8nManager einbinden)',
            }

        elif operation == 'sync':
            return {
                'status': 'stub',
                'message': 'sync noch nicht implementiert (TODO: n8nManager einbinden)',
            }

        else:
            ops = list(self.get_operations().keys())
            return {
                'status': 'error',
                'message': f"Unbekannte Operation: '{operation}'. Verfuegbar: {ops}",
            }

    def get_info(self) -> dict:
        """Gibt Handler-Info zurueck."""
        return {
            'handler': 'N8nManagerHandler',
            'profile': self.profile_name,
            'n8n_url': self.n8n_base_url,
            'external_module': self._n8n_manager_path,
            'status': 'stub',
            'operations': list(self.get_operations().keys()),
        }
