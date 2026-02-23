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
Quarantine Scanner Service (DEPRECATED)
=======================================

HINWEIS: Dieser Service ist VERALTET seit v2.0.0 (2026-02-01).
Nutze stattdessen: report_workflow_service.py

Der QuarantineScanner wurde durch den ReportWorkflowService ersetzt,
der temporäre Anonymisierungsprofile verwendet anstatt permanenter Speicherung.

Migration:
- list_clients() → report_workflow_service.list_pending_reports()
- create_profile_for_folder() → ReportWorkflowService.create_temp_profile()

Dieser Service bleibt für Abwärtskompatibilität erhalten.
"""

import os
import json
import shutil
import warnings
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Import existing core component
try:
    from skills._services.document.anonymizer_service import AnonymProfile, DocumentAnonymizer
except ImportError:
    # Relativer Import als Fallback
    from .anonymizer_service import AnonymProfile, DocumentAnonymizer


def _show_deprecation_warning():
    warnings.warn(
        "QuarantineScanner ist veraltet. Nutze ReportWorkflowService stattdessen.",
        DeprecationWarning,
        stacklevel=3
    )


class QuarantineScanner:
    """
    DEPRECATED: Nutze ReportWorkflowService aus report_workflow_service.py

    Scans the _incoming_quarantine directory for new client folders.
    Manages the lifecycle of anonymization jobs.
    """

    def __init__(self, base_path: Path):
        _show_deprecation_warning()
        self.base_path = Path(base_path) if not isinstance(base_path, Path) else base_path

        # Alte Pfade (für Abwärtskompatibilität)
        self.quarantine_path = self.base_path / "_incoming_quarantine"
        self.jobs_path = self.base_path / "user" / "anonymization_jobs"

        # Neue Pfade (v2.0)
        self.foerderplaner_quarantine = self.base_path / "user" / "foerderplaner" / "_incoming_quarantine"
        self.berichte_path = self.base_path / "user" / "foerderplaner" / "Berichte"

        # Verzeichnisse erstellen falls nötig
        self.jobs_path.mkdir(parents=True, exist_ok=True)

        self.anonymizer = DocumentAnonymizer()

    def list_clients(self) -> List[Dict]:
        """
        DEPRECATED: Nutze report_workflow_service.list_pending_reports()

        Scans multiple locations for client folders:
        1. Legacy: _incoming_quarantine/
        2. New: user/foerderplaner/_incoming_quarantine/
        3. Archive check: user/_archive/legacy_quarantine_*/
        """
        _show_deprecation_warning()
        clients = []

        # 1. Legacy Root Quarantine (falls noch existent)
        if self.quarantine_path.exists():
            clients.extend(self._scan_folder(self.quarantine_path, "legacy_root"))

        # 2. Foerderplaner Quarantine
        if self.foerderplaner_quarantine.exists():
            clients.extend(self._scan_folder(self.foerderplaner_quarantine, "foerderplaner"))

        return clients

    def _scan_folder(self, folder: Path, source: str) -> List[Dict]:
        """Scannt einen Ordner nach Klienten."""
        clients = []

        for item in folder.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                # Check if we have a profile for this folder name
                profile = self._load_profile(item.name)

                file_count = len([f for f in item.rglob("*") if f.is_file()])
                last_mod = datetime.fromtimestamp(item.stat().st_mtime).isoformat()

                status = "new"  # Default
                if profile:
                    status = "profile_ready"

                clients.append({
                    "id": item.name,
                    "name": profile.tarnname if profile else item.name,
                    "real_name": item.name,
                    "path": str(item),
                    "file_count": file_count,
                    "last_modified": last_mod,
                    "status": status,
                    "source": source,
                    "progress": 0
                })

        return clients

    def create_profile_for_folder(self, folder_name: str, real_name: str,
                                  redaction_terms: List[str]) -> Dict:
        """
        DEPRECATED: Nutze ReportWorkflowService.create_temp_profile()

        Creates an anonymization profile for a specific quarantine folder.
        """
        _show_deprecation_warning()

        # Create profile using the core service logic
        profile = self.anonymizer.create_profile(
            real_name=real_name,
            geburtsdatum="01.01.2000",  # Placeholder
            weitere_daten={"redact": ",".join(redaction_terms)} if redaction_terms else None
        )

        # Save profile locally in the jobs folder
        self._save_profile(folder_name, profile)

        return {
            "success": True,
            "client_id": profile.client_id,
            "tarnname": profile.tarnname,
            "deprecated_warning": "Nutze ReportWorkflowService für temporäre Profile"
        }

    def _save_profile(self, folder_name: str, profile: AnonymProfile):
        """Saves profile metadata linked to the folder name."""
        profile_file = self.jobs_path / f"{folder_name}.json"

        data = {
            "folder_name": folder_name,
            "client_id": profile.client_id,
            "tarnname": profile.tarnname,
            "mappings": profile.mappings,
            "created": profile.created
        }

        profile_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _load_profile(self, folder_name: str) -> Optional[AnonymProfile]:
        """Loads profile if exists."""
        profile_file = self.jobs_path / f"{folder_name}.json"
        if not profile_file.exists():
            return None

        try:
            data = json.loads(profile_file.read_text(encoding="utf-8"))
            return AnonymProfile(
                client_id=data["client_id"],
                tarnname=data["tarnname"],
                fake_geburtsdatum="01.01.2000",  # Dummy
                mappings=data.get("mappings", {}),
                created=data.get("created")
            )
        except:
            return None

    def upload_file(self, filename: str, content: bytes, folder_name: Optional[str] = None):
        """
        DEPRECATED: Nutze ReportWorkflowService.import_files()

        Saves an uploaded file to the quarantine.
        """
        _show_deprecation_warning()

        # Nutze neue Berichte-Struktur
        target_dir = self.berichte_path / "data"
        target_dir.mkdir(parents=True, exist_ok=True)

        if folder_name:
            target_dir = target_dir / folder_name
            target_dir.mkdir(exist_ok=True)

        target_file = target_dir / filename
        target_file.write_bytes(content)
        return str(target_file)


# ═══════════════════════════════════════════════════════════════
# Migration Helper
# ═══════════════════════════════════════════════════════════════

def migrate_to_report_workflow():
    """
    Hilfs-Funktion zur Migration vom alten System zum neuen.

    Gibt Anweisungen aus, wie bestehende Profile migriert werden können.
    """
    print("""
╔══════════════════════════════════════════════════════════════╗
║            MIGRATION ZU REPORT WORKFLOW SERVICE              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Der QuarantineScanner ist VERALTET.                         ║
║  Nutze stattdessen: ReportWorkflowService                    ║
║                                                              ║
║  ÄNDERUNGEN:                                                 ║
║  - Keine permanenten Profile mehr                            ║
║  - Temporäre Anonymisierung pro Session                      ║
║  - Automatische De-Anonymisierung                            ║
║  - Neue Ordnerstruktur unter user/foerderplaner/Berichte/    ║
║                                                              ║
║  NEUE USAGE:                                                 ║
║  from report_workflow_service import ReportWorkflowService   ║
║  service = ReportWorkflowService()                           ║
║  session = service.start_session()                           ║
║  service.import_files(session, [files])                      ║
║  service.create_temp_profile(session, name, geburtsdatum)    ║
║  ...                                                         ║
║                                                              ║
║  ARCHIVIERTE DATEN:                                          ║
║  - user/_archive/legacy_quarantine_20260201/                 ║
║  - user/_archive/orphaned_anon_profiles/                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    migrate_to_report_workflow()
