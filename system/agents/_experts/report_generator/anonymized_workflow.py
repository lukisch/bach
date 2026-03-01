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
Anonymized Workflow - LLM-Schutz durch automatische Anonymisierung
===================================================================

Orchestriert den Workflow so, dass das LLM (und der Chatbot) niemals
echte Namen sehen. Quelldokumente werden automatisch anonymisiert,
Berichte beim Speichern de-anonymisiert.

Workflow:
    1. create_or_update_bundle() - Quelldokumente → anonymisiertes Bundle
    2. get_bundle_content() - LLM bekommt NUR Bundle-Inhalt
    3. save_deanonymized() - Bericht mit echten Namen speichern

Version: 1.0.0
Erstellt: 2026-02-05
"""

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Anonymizer Service importieren
import sys
_current = Path(__file__).resolve()
for _parent in [_current] + list(_current.parents):
    _hub = _parent / "system" / "hub"
    if _hub.exists():
        if str(_hub) not in sys.path:
            sys.path.insert(0, str(_hub))
        # Auch den document-Ordner hinzufügen
        _doc_svc = _hub / "_services" / "document"
        if _doc_svc.exists() and str(_doc_svc) not in sys.path:
            sys.path.insert(0, str(_doc_svc))
        break

try:
    from anonymizer_service import (
        DocumentAnonymizer, DocumentDeanonymizer,
        AnonymProfile, AnonymResult,
        encrypt_key_file, decrypt_key_file, get_key_path
    )
    ANONYMIZER_AVAILABLE = True
except ImportError:
    try:
        from _services.document.anonymizer_service import (
            DocumentAnonymizer, DocumentDeanonymizer,
            AnonymProfile, AnonymResult,
            encrypt_key_file, decrypt_key_file, get_key_path
        )
        ANONYMIZER_AVAILABLE = True
    except ImportError:
        ANONYMIZER_AVAILABLE = False
        # Fallback-Klassen für Type Hints
        AnonymProfile = None
        AnonymResult = None
        DocumentAnonymizer = None
        DocumentDeanonymizer = None


@dataclass
class BundleInfo:
    """Informationen über ein erstelltes Bundle."""
    client_id: str
    tarnname: str
    bundle_path: Path
    files_count: int
    created: str
    profile_path: Path


@dataclass
class WorkflowResult:
    """Ergebnis eines Workflow-Schritts."""
    success: bool = False
    message: str = ""
    output_path: str = ""
    errors: List[str] = field(default_factory=list)


class AnonymizedWorkflow:
    """
    Orchestriert den anonymisierten Berichts-Workflow.

    Das LLM und der Chatbot sehen NUR anonymisierte Daten (Tarnnamen).
    Echte Namen werden erst beim Export/Speichern wiederhergestellt.

    Verwendung:
        workflow = AnonymizedWorkflow(data_dir, bundles_dir)

        # Bundle erstellen (einmalig pro Klient)
        bundle_info = workflow.create_or_update_bundle(
            klient_ordner="Forman, Jaden Hannington",
            password="geheim"
        )

        # Für LLM: Nur Bundle-Inhalt verwenden
        content = workflow.get_bundle_content(bundle_info.client_id)

        # Nach Generierung: De-anonymisieren
        workflow.save_deanonymized(
            source_path=anonymized_report,
            client_id=bundle_info.client_id,
            password="geheim"
        )
    """

    def __init__(self, data_dir: Path = None, bundles_dir: Path = None):
        """
        Initialisiert den Workflow.

        Args:
            data_dir: Ordner mit echten Klientendaten
            bundles_dir: Ordner für anonymisierte Bundles
        """
        if not ANONYMIZER_AVAILABLE:
            raise RuntimeError("Anonymizer Service nicht verfügbar")

        # Pfade ermitteln
        if data_dir is None or bundles_dir is None:
            base = Path(__file__).parent.parent.parent.parent.parent
            foerderplaner = base / "user" / "documents" / "foerderplaner" / "Berichte"
            data_dir = data_dir or foerderplaner / "data"
            bundles_dir = bundles_dir or foerderplaner / "bundles"

        self.data_dir = Path(data_dir)
        self.bundles_dir = Path(bundles_dir)
        self.anonymizer = DocumentAnonymizer()
        self.deanonymizer = DocumentDeanonymizer()

        # Ordner erstellen falls nötig
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.bundles_dir.mkdir(parents=True, exist_ok=True)

    def _find_klient_folder(self, name_or_id: str) -> Optional[Path]:
        """
        Findet den Klienten-Ordner anhand von Name oder Client-ID.
        """
        # Direkt als Pfad?
        direct = self.data_dir / name_or_id
        if direct.exists():
            return direct

        # Suche nach .profil.json mit passender Client-ID
        for folder in self.data_dir.iterdir():
            if not folder.is_dir():
                continue
            profil_path = folder / ".profil.json"
            if profil_path.exists():
                try:
                    profil = json.loads(profil_path.read_text(encoding="utf-8"))
                    if profil.get("client_id") == name_or_id:
                        return folder
                except Exception:
                    pass

        # Teilname-Suche
        name_lower = name_or_id.lower()
        for folder in self.data_dir.iterdir():
            if folder.is_dir() and name_lower in folder.name.lower():
                return folder

        return None

    def _load_existing_profile(self, klient_folder: Path) -> Optional[Tuple[AnonymProfile, str]]:
        """
        Lädt ein existierendes Profil falls vorhanden.

        Returns:
            (profile, client_id) oder None
        """
        profil_path = klient_folder / ".profil.json"
        if not profil_path.exists():
            return None

        try:
            profil_data = json.loads(profil_path.read_text(encoding="utf-8"))
            client_id = profil_data.get("client_id")

            if not client_id:
                return None

            # Schlüssel laden (ohne Passwort - nur Metadaten)
            # Das vollständige Profil wird nur bei Bedarf mit Passwort geladen
            return None, client_id  # Wir haben die ID, aber nicht das volle Profil

        except Exception:
            return None

    def _extract_names_from_folder(self, folder: Path) -> Tuple[str, str, List[str]]:
        """
        Extrahiert Namen aus dem Ordnernamen und den Dokumenten.

        Returns:
            (hauptname, geburtsdatum, weitere_namen)
        """
        # Hauptname aus Ordnername
        # Format: "Nachname, Vorname" oder "Nachname, Vorname Zweitname"
        folder_name = folder.name
        parts = folder_name.split(", ")
        if len(parts) >= 2:
            nachname = parts[0].strip()
            vorname_teil = parts[1].strip()
            # Vorname kann mehrere Teile haben
            hauptname = f"{vorname_teil} {nachname}"
        else:
            hauptname = folder_name

        # Geburtsdatum aus Dokumenten extrahieren (vereinfacht)
        geburtsdatum = "01.01.2010"  # Default, wird idealerweise aus Dokumenten gelesen

        # TODO: Weitere Namen aus Dokumenten scannen
        weitere_namen = []

        return hauptname, geburtsdatum, weitere_namen

    def create_or_update_bundle(
        self,
        klient_ordner: str,
        password: str,
        force_recreate: bool = False
    ) -> BundleInfo:
        """
        Erstellt oder aktualisiert ein anonymisiertes Bundle.

        Args:
            klient_ordner: Name des Klienten-Ordners in data/
            password: Passwort für die Schlüssel-Verschlüsselung
            force_recreate: Bundle komplett neu erstellen

        Returns:
            BundleInfo mit Client-ID, Tarnname und Pfaden
        """
        # Klienten-Ordner finden
        klient_path = self._find_klient_folder(klient_ordner)
        if not klient_path:
            raise FileNotFoundError(f"Klienten-Ordner nicht gefunden: {klient_ordner}")

        # Existierendes Profil prüfen
        profil_path = klient_path / ".profil.json"
        existing_profile = None
        client_id = None

        if profil_path.exists() and not force_recreate:
            try:
                profil_data = json.loads(profil_path.read_text(encoding="utf-8"))
                client_id = profil_data.get("client_id")

                # Prüfen ob Bundle existiert
                bundle_path = self.bundles_dir / client_id
                if bundle_path.exists():
                    # Bundle existiert - nur aktualisieren wenn nötig
                    return BundleInfo(
                        client_id=client_id,
                        tarnname=profil_data.get("tarnname", ""),
                        bundle_path=bundle_path,
                        files_count=profil_data.get("files_anonymized", 0),
                        created=profil_data.get("created", ""),
                        profile_path=profil_path
                    )
            except Exception:
                pass

        # Neues Profil erstellen
        hauptname, geburtsdatum, weitere_namen = self._extract_names_from_folder(klient_path)

        # Dokumente nach sensiblen Daten scannen
        scanned_data = self.anonymizer.scan_folder_for_sensitive_data(str(klient_path))

        # Profil erstellen
        profile = self.anonymizer.create_profile(
            real_name=hauptname,
            geburtsdatum=geburtsdatum,
            weitere_namen=weitere_namen,
            scanned_data=scanned_data
        )

        # Bundle-Ordner erstellen
        bundle_path = self.bundles_dir / profile.client_id
        if bundle_path.exists():
            shutil.rmtree(bundle_path)

        (bundle_path / "core").mkdir(parents=True, exist_ok=True)
        (bundle_path / "extended").mkdir(parents=True, exist_ok=True)
        (bundle_path / "output").mkdir(parents=True, exist_ok=True)

        # Dokumente anonymisiert kopieren
        result = self.anonymizer.anonymize_folder(
            folder=str(klient_path),
            profile=profile,
            password=password,
            output_folder=str(bundle_path / "core")
        )

        # Profil-Info in data-Ordner speichern (nur Metadaten, keine Mappings)
        profil_info = {
            "client_id": profile.client_id,
            "tarnname": profile.tarnname,
            "fake_geburtsdatum": profile.fake_geburtsdatum,
            "created": profile.created,
            "files_anonymized": result.anonymized_files,
            "key_location": str(get_key_path(profile.client_id)),
            "key_info": "Schluessel liegt LOKAL (nicht in OneDrive)"
        }
        profil_path.write_text(
            json.dumps(profil_info, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return BundleInfo(
            client_id=profile.client_id,
            tarnname=profile.tarnname,
            bundle_path=bundle_path,
            files_count=result.anonymized_files,
            created=profile.created,
            profile_path=profil_path
        )

    def get_bundle_content(self, client_id: str, include_extended: bool = False) -> str:
        """
        Extrahiert den Text-Inhalt eines Bundles für den LLM-Prompt.

        WICHTIG: Diese Methode gibt NUR anonymisierte Daten zurück.
        Das LLM sieht hier nur Tarnnamen.

        Args:
            client_id: Die Client-ID (z.B. "K_A7B3C9")
            include_extended: Auch extended/ Ordner einbeziehen

        Returns:
            Anonymisierter Text für den LLM-Prompt
        """
        bundle_path = self.bundles_dir / client_id
        if not bundle_path.exists():
            raise FileNotFoundError(f"Bundle nicht gefunden: {client_id}")

        # Ordner zum Scannen
        folders = [bundle_path / "core"]
        if include_extended:
            folders.append(bundle_path / "extended")

        # Text extrahieren
        all_text = []
        supported = {".docx", ".txt", ".md", ".pdf", ".xlsx", ".xls"}

        for folder in folders:
            if not folder.exists():
                continue

            for filepath in sorted(folder.rglob("*")):
                if not filepath.is_file():
                    continue
                if filepath.suffix.lower() not in supported:
                    continue
                if filepath.name.startswith(".") or filepath.name.startswith("_"):
                    continue
                if "output" in filepath.parts:
                    continue

                rel_path = filepath.relative_to(bundle_path)
                text = self.anonymizer.extract_text_from_file(str(filepath))

                if text.strip():
                    all_text.append(f"--- Quelle: {rel_path} ---\n{text}")

        if not all_text:
            return "[FEHLER: Keine Dokumente im Bundle gefunden]"

        return "\n\n".join(all_text)

    def get_client_id_for_klient(self, klient_name: str) -> Optional[str]:
        """
        Ermittelt die Client-ID für einen Klienten-Namen.
        """
        klient_path = self._find_klient_folder(klient_name)
        if not klient_path:
            return None

        profil_path = klient_path / ".profil.json"
        if profil_path.exists():
            try:
                profil = json.loads(profil_path.read_text(encoding="utf-8"))
                return profil.get("client_id")
            except Exception:
                pass

        return None

    def save_deanonymized(
        self,
        source_path: str,
        client_id: str,
        password: str,
        output_folder: str = None
    ) -> WorkflowResult:
        """
        De-anonymisiert einen Bericht und speichert ihn.

        Args:
            source_path: Pfad zum anonymisierten Bericht
            client_id: Client-ID für den Schlüssel
            password: Passwort für die Entschlüsselung
            output_folder: Zielordner (default: data/<klient>/output/)

        Returns:
            WorkflowResult mit Pfad zum de-anonymisierten Bericht
        """
        result = WorkflowResult()

        try:
            # Schlüssel laden
            key_path = get_key_path(client_id)
            if not key_path.exists():
                result.errors.append(f"Schlüssel nicht gefunden: {key_path}")
                return result

            profile = decrypt_key_file(str(key_path), password)

            # Zielordner ermitteln
            if output_folder is None:
                # Klienten-Ordner aus Profil suchen
                for folder in self.data_dir.iterdir():
                    if not folder.is_dir():
                        continue
                    profil_path = folder / ".profil.json"
                    if profil_path.exists():
                        try:
                            profil = json.loads(profil_path.read_text(encoding="utf-8"))
                            if profil.get("client_id") == client_id:
                                output_folder = str(folder / "output")
                                break
                        except Exception:
                            pass

            if output_folder is None:
                output_folder = str(self.data_dir / client_id / "output")

            Path(output_folder).mkdir(parents=True, exist_ok=True)

            # Datei kopieren
            source = Path(source_path)
            dest = Path(output_folder) / source.name
            shutil.copy2(source, dest)

            # De-anonymisieren
            success, count = self.deanonymizer.deanonymize_file(str(dest), profile)

            if success:
                # Dateinamen auch de-anonymisieren
                new_name = dest.name
                for original, fake in profile.mappings.get("names", {}).items():
                    if fake in new_name:
                        new_name = new_name.replace(fake, original)

                if new_name != dest.name:
                    new_dest = dest.parent / new_name
                    dest.rename(new_dest)
                    dest = new_dest

                result.success = True
                result.output_path = str(dest)
                result.message = f"De-anonymisiert: {count} Ersetzungen"
            else:
                result.errors.append("De-Anonymisierung fehlgeschlagen")

        except Exception as e:
            result.errors.append(str(e))

        return result

    def list_bundles(self) -> List[Dict]:
        """
        Listet alle vorhandenen Bundles auf.
        """
        bundles = []

        for folder in self.bundles_dir.iterdir():
            if not folder.is_dir():
                continue
            if folder.name.startswith(".") or folder.name.startswith("_"):
                continue

            # Profil-Info aus data/ suchen
            tarnname = ""
            for data_folder in self.data_dir.iterdir():
                profil_path = data_folder / ".profil.json"
                if profil_path.exists():
                    try:
                        profil = json.loads(profil_path.read_text(encoding="utf-8"))
                        if profil.get("client_id") == folder.name:
                            tarnname = profil.get("tarnname", "")
                            break
                    except Exception:
                        pass

            bundles.append({
                "client_id": folder.name,
                "tarnname": tarnname,
                "path": str(folder),
                "has_core": (folder / "core").exists(),
                "has_output": (folder / "output").exists()
            })

        return bundles


# ═══════════════════════════════════════════════════════════════
# CLI Interface
# ═══════════════════════════════════════════════════════════════

def main():
    """CLI für den Anonymized Workflow."""
    import argparse

    parser = argparse.ArgumentParser(description="Anonymized Workflow CLI")
    subparsers = parser.add_subparsers(dest="command")

    # create-bundle
    create_p = subparsers.add_parser("create-bundle", help="Bundle erstellen")
    create_p.add_argument("klient", help="Klienten-Ordner Name")
    create_p.add_argument("--password", "-p", required=True, help="Schlüssel-Passwort")
    create_p.add_argument("--force", "-f", action="store_true", help="Neu erstellen")

    # list-bundles
    list_p = subparsers.add_parser("list-bundles", help="Bundles auflisten")

    # get-content
    content_p = subparsers.add_parser("get-content", help="Bundle-Inhalt abrufen")
    content_p.add_argument("client_id", help="Client-ID")
    content_p.add_argument("--extended", "-e", action="store_true", help="Extended einbeziehen")

    # deanonymize
    deanon_p = subparsers.add_parser("deanonymize", help="Bericht de-anonymisieren")
    deanon_p.add_argument("source", help="Quell-Datei (anonymisiert)")
    deanon_p.add_argument("client_id", help="Client-ID")
    deanon_p.add_argument("--password", "-p", required=True, help="Schlüssel-Passwort")
    deanon_p.add_argument("--output", "-o", help="Zielordner")

    args = parser.parse_args()

    if not ANONYMIZER_AVAILABLE:
        print("[FEHLER] Anonymizer Service nicht verfügbar")
        return

    workflow = AnonymizedWorkflow()

    if args.command == "create-bundle":
        print(f"Erstelle Bundle für: {args.klient}")
        try:
            info = workflow.create_or_update_bundle(
                klient_ordner=args.klient,
                password=args.password,
                force_recreate=args.force
            )
            print(f"[OK] Bundle erstellt:")
            print(f"  Client-ID: {info.client_id}")
            print(f"  Tarnname: {info.tarnname}")
            print(f"  Pfad: {info.bundle_path}")
            print(f"  Dateien: {info.files_count}")
        except Exception as e:
            print(f"[FEHLER] {e}")

    elif args.command == "list-bundles":
        bundles = workflow.list_bundles()
        if not bundles:
            print("Keine Bundles vorhanden")
        else:
            print(f"Bundles ({len(bundles)}):")
            for b in bundles:
                print(f"  {b['client_id']}: {b['tarnname'] or '(kein Tarnname)'}")

    elif args.command == "get-content":
        try:
            content = workflow.get_bundle_content(
                client_id=args.client_id,
                include_extended=args.extended
            )
            print(content[:5000])
            if len(content) > 5000:
                print(f"\n... ({len(content)} Zeichen insgesamt)")
        except Exception as e:
            print(f"[FEHLER] {e}")

    elif args.command == "deanonymize":
        result = workflow.save_deanonymized(
            source_path=args.source,
            client_id=args.client_id,
            password=args.password,
            output_folder=args.output
        )
        if result.success:
            print(f"[OK] {result.message}")
            print(f"  Ausgabe: {result.output_path}")
        else:
            print(f"[FEHLER] {result.errors}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
