#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Dedup Scanner — SHA256-basierte Duplikaterkennung (INT06)

Portiert aus ProFiler V4/V15. Scannt Verzeichnisse und erkennt
identische Dateien anhand ihres SHA256-Hashes.

Features:
- Chunk-basierte Hash-Berechnung (speichereffizient)
- OneDrive Cloud-Placeholder-Erkennung (kein Download)
- Duplikat-Report mit Groesse und Pfaden
"""

import hashlib
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Berechnet SHA256-Hash einer Datei mit Chunk-Verarbeitung."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def is_cloud_placeholder(path: Path) -> bool:
    """Prueft ob eine Datei ein OneDrive Cloud-Placeholder ist (nicht lokal)."""
    if os.name != "nt":
        return False
    try:
        attrs = os.stat(path).st_file_attributes
        FILE_ATTR_CLOUD_PLACEHOLDER = 0x1000
        FILE_ATTR_RECALL_ON_ACCESS = 0x400
        return bool(attrs & FILE_ATTR_CLOUD_PLACEHOLDER) or bool(attrs & FILE_ATTR_RECALL_ON_ACCESS)
    except (AttributeError, OSError):
        return False


class DedupScanner:
    """Scannt Verzeichnisse und findet Duplikate per SHA256."""

    def __init__(self, min_size: int = 0, skip_cloud: bool = True):
        """
        Args:
            min_size: Minimale Dateigroesse in Bytes (0 = alle)
            skip_cloud: Cloud-Placeholder ueberspringen
        """
        self.min_size = min_size
        self.skip_cloud = skip_cloud

    def scan(self, path: Path, recursive: bool = True) -> Dict:
        """Scannt Verzeichnis und liefert Duplikat-Report.

        Returns:
            {
                "total_files": int,
                "total_size": int,
                "skipped_cloud": int,
                "unique_hashes": int,
                "duplicate_groups": [{
                    "hash": str,
                    "size": int,
                    "count": int,
                    "files": [str, ...]
                }, ...],
                "wasted_bytes": int,
            }
        """
        path = Path(path)
        if not path.exists():
            raise ValueError(f"Pfad existiert nicht: {path}")

        hash_map = defaultdict(list)  # hash -> [(path, size), ...]
        total_files = 0
        total_size = 0
        skipped_cloud = 0

        # Dateien sammeln
        if path.is_file():
            files = [path]
        elif recursive:
            files = [f for f in path.rglob("*") if f.is_file()]
        else:
            files = [f for f in path.iterdir() if f.is_file()]

        for fpath in files:
            try:
                stat = fpath.stat()
                size = stat.st_size

                if size < self.min_size:
                    continue

                if self.skip_cloud and is_cloud_placeholder(fpath):
                    skipped_cloud += 1
                    continue

                total_files += 1
                total_size += size

                file_hash = sha256_file(fpath)
                hash_map[file_hash].append((str(fpath), size))

            except (PermissionError, OSError):
                continue

        # Duplikate filtern (mehr als 1 Datei pro Hash)
        duplicate_groups = []
        wasted = 0
        for h, entries in hash_map.items():
            if len(entries) > 1:
                size = entries[0][1]
                wasted += size * (len(entries) - 1)
                duplicate_groups.append({
                    "hash": h[:12],  # Gekuerzter Hash fuer Anzeige
                    "size": size,
                    "count": len(entries),
                    "files": [e[0] for e in entries],
                })

        # Sortieren: groesste Verschwendung zuerst
        duplicate_groups.sort(key=lambda x: x["size"] * (x["count"] - 1), reverse=True)

        return {
            "total_files": total_files,
            "total_size": total_size,
            "skipped_cloud": skipped_cloud,
            "unique_hashes": len(hash_map),
            "duplicate_groups": duplicate_groups,
            "wasted_bytes": wasted,
        }

    @staticmethod
    def format_report(result: Dict) -> str:
        """Formatiert Scan-Ergebnis als Text-Report."""
        lines = [
            "DUPLIKAT-SCAN ERGEBNIS",
            "=" * 50,
            "",
            f"  Dateien gescannt:  {result['total_files']}",
            f"  Gesamtgroesse:     {_fmt_size(result['total_size'])}",
            f"  Eindeutige Hashes: {result['unique_hashes']}",
        ]

        if result["skipped_cloud"]:
            lines.append(f"  Cloud-Placeholder: {result['skipped_cloud']} uebersprungen")

        groups = result["duplicate_groups"]
        if not groups:
            lines.append("")
            lines.append("  Keine Duplikate gefunden.")
            return "\n".join(lines)

        total_dupes = sum(g["count"] - 1 for g in groups)
        lines.extend([
            "",
            f"  DUPLIKATE: {total_dupes} Dateien in {len(groups)} Gruppen",
            f"  Verschwendet: {_fmt_size(result['wasted_bytes'])}",
            "",
        ])

        for i, g in enumerate(groups[:20], 1):  # Max 20 Gruppen anzeigen
            lines.append(f"  [{i}] {_fmt_size(g['size'])} x{g['count']} ({g['hash']})")
            for f in g["files"]:
                lines.append(f"      {f}")
            lines.append("")

        if len(groups) > 20:
            lines.append(f"  ... und {len(groups) - 20} weitere Gruppen")

        return "\n".join(lines)


def _fmt_size(n: int) -> str:
    """Formatiert Bytes als lesbaren String."""
    if n < 1024:
        return f"{n} B"
    elif n < 1024 ** 2:
        return f"{n / 1024:.1f} KB"
    elif n < 1024 ** 3:
        return f"{n / 1024 ** 2:.1f} MB"
    else:
        return f"{n / 1024 ** 3:.2f} GB"
