#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: data_importer
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version data_importer

Description:
    [Beschreibung hinzufügen]

Usage:
    python data_importer.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

# -*- coding: utf-8 -*-
"""
Data Import Framework - Generischer Daten-Import fuer BACH
==========================================================

Importiert strukturierte Daten (JSON, CSV, Dict-Listen) in
beliebige bach.db Tabellen. Schema-Erkennung, Duplikaterkennung,
dist_type-Automatik, Import-Logging.

Nutzbar als:
  - Library (from tools.data_importer import DataImporter)
  - CLI (python tools/data_importer.py --table health_diagnoses --file data.csv)

Ref: docs/WICHTIG_SYSTEMISCH_FIRST.md
"""

import sqlite3
import csv
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any


class DataImporter:
    """Generischer Daten-Importer fuer beliebige DB-Tabellen."""

    # Spalten die automatisch gesetzt werden (nicht vom User)
    AUTO_COLUMNS = {
        "id", "created_at", "updated_at", "dist_type",
    }

    # Spalten die bei Duplikat-Check ignoriert werden
    SKIP_DUPLICATE_COLS = {
        "id", "created_at", "updated_at", "dist_type",
        "first_seen", "last_scan", "last_modified",
    }

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._schema_cache = {}
        self._ensure_import_tables()

    def _get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_import_tables(self):
        """Erstellt Tabellen fuer Import-Tracking."""
        conn = self._get_db()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS import_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_table TEXT NOT NULL,
                source_type TEXT,
                source_path TEXT,
                rows_total INTEGER DEFAULT 0,
                rows_inserted INTEGER DEFAULT 0,
                rows_skipped INTEGER DEFAULT 0,
                rows_failed INTEGER DEFAULT 0,
                errors TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                triggered_by TEXT DEFAULT 'manual',
                dist_type INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()

    # ------------------------------------------------------------------
    # Schema-Introspection
    # ------------------------------------------------------------------

    def get_table_schema(self, table_name: str) -> Dict:
        """
        Liest Tabellen-Schema per PRAGMA table_info.

        Returns:
            Dict mit column_name -> {cid, type, notnull, default, pk}
        """
        if table_name in self._schema_cache:
            return self._schema_cache[table_name]

        conn = self._get_db()
        try:
            rows = conn.execute(
                f"PRAGMA table_info({table_name})"
            ).fetchall()

            if not rows:
                return {}

            schema = {}
            for r in rows:
                schema[r["name"]] = {
                    "cid": r["cid"],
                    "type": r["type"].upper() if r["type"] else "TEXT",
                    "notnull": bool(r["notnull"]),
                    "default": r["dflt_value"],
                    "pk": bool(r["pk"]),
                }

            self._schema_cache[table_name] = schema
            return schema
        finally:
            conn.close()

    def list_importable_tables(self) -> List[str]:
        """Gibt alle Tabellen zurueck die importierbar sind."""
        conn = self._get_db()
        try:
            rows = conn.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                AND name NOT IN ('import_runs', 'folder_scans', 'folder_scan_files')
                ORDER BY name
            """).fetchall()
            return [r["name"] for r in rows]
        finally:
            conn.close()

    def describe_table(self, table_name: str) -> str:
        """Gibt lesbares Schema fuer eine Tabelle zurueck."""
        schema = self.get_table_schema(table_name)
        if not schema:
            return f"Tabelle '{table_name}' nicht gefunden."

        lines = [f"Schema: {table_name}"]
        lines.append("-" * 60)

        for col, info in schema.items():
            flags = []
            if info["pk"]:
                flags.append("PK")
            if info["notnull"]:
                flags.append("NOT NULL")
            if info["default"] is not None:
                flags.append(f"DEFAULT {info['default']}")
            if col in self.AUTO_COLUMNS:
                flags.append("AUTO")

            flag_str = f"  [{', '.join(flags)}]" if flags else ""
            lines.append(f"  {col:<30} {info['type']:<10}{flag_str}")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Daten-Parsing (CSV, JSON, Dicts)
    # ------------------------------------------------------------------

    def parse_csv(self, file_path: str, delimiter: str = ";",
                  encoding: str = "utf-8-sig") -> List[Dict]:
        """
        Liest CSV-Datei und gibt Liste von Dicts zurueck.

        Args:
            file_path: Pfad zur CSV
            delimiter: Trennzeichen (Default: ; fuer DE-Format)
            encoding: Datei-Encoding
        """
        rows = []
        with open(file_path, "r", encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                # Leere Werte zu None
                cleaned = {}
                for k, v in row.items():
                    if k is None:
                        continue
                    k = k.strip()
                    if v is None or v.strip() == "":
                        cleaned[k] = None
                    else:
                        cleaned[k] = v.strip()
                if any(v is not None for v in cleaned.values()):
                    rows.append(cleaned)
        return rows

    def parse_json(self, file_path: str) -> List[Dict]:
        """Liest JSON-Datei (Array oder einzelnes Objekt)."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Einzelnes Objekt -> Liste mit einem Element
            return [data]
        else:
            raise ValueError(f"JSON muss Array oder Object sein, nicht {type(data)}")

    # ------------------------------------------------------------------
    # Wert-Konvertierung
    # ------------------------------------------------------------------

    def _convert_value(self, value: Any, col_type: str) -> Any:
        """Konvertiert Wert zum Ziel-Typ."""
        if value is None:
            return None

        col_type = col_type.upper()

        if col_type in ("INTEGER", "INT", "BIGINT"):
            if isinstance(value, str):
                # DE-Format: "1.234" -> 1234, "1,5" -> error
                value = value.replace(".", "").replace(" ", "")
                if value == "" or value == "-":
                    return None
            try:
                return int(value)
            except (ValueError, TypeError):
                return None

        elif col_type in ("REAL", "FLOAT", "DOUBLE", "NUMERIC"):
            if isinstance(value, str):
                # DE-Format: "1.234,56" -> 1234.56
                if "," in value and "." in value:
                    value = value.replace(".", "").replace(",", ".")
                elif "," in value:
                    value = value.replace(",", ".")
                value = value.strip()
                if value == "" or value == "-":
                    return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None

        elif col_type in ("BOOLEAN", "BOOL"):
            if isinstance(value, str):
                return value.lower() in ("1", "true", "ja", "yes", "x")
            return bool(value)

        elif col_type in ("DATE", "TIMESTAMP", "DATETIME"):
            if isinstance(value, str):
                return self._parse_date(value)
            return value

        else:
            # TEXT und alles andere
            return str(value) if value is not None else None

    def _parse_date(self, date_str: str) -> Optional[str]:
        """Parst gaengige Datumsformate nach YYYY-MM-DD."""
        if not date_str or date_str.strip() == "":
            return None

        date_str = date_str.strip()

        # Schon im richtigen Format?
        if len(date_str) >= 10 and date_str[4] == "-":
            return date_str[:10]

        # DD.MM.YYYY (DE-Format)
        for fmt in ["%d.%m.%Y", "%d.%m.%y", "%d/%m/%Y", "%m/%d/%Y",
                     "%Y%m%d", "%d-%m-%Y"]:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

        # ISO mit Zeit
        for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]:
            try:
                dt = datetime.strptime(date_str[:19], fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

        return date_str  # Unveraendert zurueckgeben

    # ------------------------------------------------------------------
    # Column Mapping
    # ------------------------------------------------------------------

    def auto_map_columns(self, source_keys: List[str],
                         table_name: str) -> Dict[str, str]:
        """
        Versucht Source-Spalten automatisch auf Ziel-Tabelle zu mappen.

        Returns:
            Dict {source_key: target_column}
        """
        schema = self.get_table_schema(table_name)
        if not schema:
            return {}

        target_cols = set(schema.keys()) - self.AUTO_COLUMNS
        mapping = {}

        for src_key in source_keys:
            src_lower = src_key.lower().strip()

            # 1. Exakter Match
            if src_lower in schema and src_lower not in self.AUTO_COLUMNS:
                mapping[src_key] = src_lower
                continue

            # 2. Ohne Prefix/Suffix Match
            # z.B. "Diagnosis_Name" -> "diagnosis_name"
            src_normalized = src_lower.replace(" ", "_").replace("-", "_")
            if src_normalized in schema and src_normalized not in self.AUTO_COLUMNS:
                mapping[src_key] = src_normalized
                continue

            # 3. Teilmatch - Source enthaelt Target oder umgekehrt
            for tcol in target_cols:
                if tcol in src_lower or src_lower in tcol:
                    if tcol not in mapping.values():
                        mapping[src_key] = tcol
                        break

        return mapping

    # ------------------------------------------------------------------
    # Duplikat-Erkennung
    # ------------------------------------------------------------------

    def _check_duplicate(self, conn, table_name: str,
                         row_data: Dict, unique_keys: Optional[List[str]] = None) -> bool:
        """
        Prueft ob ein aehnlicher Eintrag bereits existiert.

        Args:
            table_name: Zieltabelle
            row_data: Zu pruefende Daten
            unique_keys: Spalten fuer Duplikat-Check (None = alle nicht-auto Spalten)
        """
        if unique_keys:
            check_cols = [k for k in unique_keys if k in row_data and row_data[k] is not None]
        else:
            # Alle nicht-auto Spalten mit Wert nutzen
            check_cols = [
                k for k in row_data
                if k not in self.SKIP_DUPLICATE_COLS
                and row_data[k] is not None
            ]

        if not check_cols:
            return False

        conditions = " AND ".join(f"{col} = ?" for col in check_cols)
        values = [row_data[col] for col in check_cols]

        count = conn.execute(
            f"SELECT COUNT(*) FROM {table_name} WHERE {conditions}",
            values
        ).fetchone()[0]

        return count > 0

    # ------------------------------------------------------------------
    # Import-Methoden
    # ------------------------------------------------------------------

    def import_rows(self, table_name: str, rows: List[Dict],
                    column_map: Optional[Dict[str, str]] = None,
                    unique_keys: Optional[List[str]] = None,
                    skip_duplicates: bool = True,
                    dist_type: int = 0,
                    source_info: str = "manual",
                    triggered_by: str = "manual",
                    dry_run: bool = False) -> Dict:
        """
        Importiert eine Liste von Dicts in eine DB-Tabelle.

        Args:
            table_name: Zieltabelle
            rows: Liste von Dicts mit Daten
            column_map: Optionales Mapping {source_key: target_col}
            unique_keys: Spalten fuer Duplikat-Check
            skip_duplicates: Duplikate ueberspringen statt Fehler
            dist_type: Verteilungstyp (0=User, 1=Template, 2=Core)
            source_info: Beschreibung der Quelle
            triggered_by: Wer hat den Import ausgeloest
            dry_run: Nur validieren, nicht importieren

        Returns:
            Dict mit inserted, skipped, failed, errors, run_id
        """
        schema = self.get_table_schema(table_name)
        if not schema:
            return {"error": f"Tabelle '{table_name}' nicht gefunden."}

        if not rows:
            return {"error": "Keine Daten zum Importieren."}

        # Auto-Mapping wenn nicht angegeben
        if column_map is None:
            first_keys = list(rows[0].keys())
            column_map = self.auto_map_columns(first_keys, table_name)

        conn = self._get_db()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        inserted = 0
        skipped = 0
        failed = 0
        errors = []

        try:
            for i, row in enumerate(rows):
                try:
                    # Mapped Row erstellen
                    mapped = {}
                    for src_key, tgt_col in column_map.items():
                        if src_key in row:
                            col_type = schema.get(tgt_col, {}).get("type", "TEXT")
                            mapped[tgt_col] = self._convert_value(row[src_key], col_type)

                    # Auto-Spalten setzen
                    if "dist_type" in schema:
                        mapped["dist_type"] = dist_type
                    if "created_at" in schema:
                        mapped["created_at"] = now
                    if "updated_at" in schema:
                        mapped["updated_at"] = now

                    # Pflichtfeld-Check
                    for col, info in schema.items():
                        if info["notnull"] and not info["pk"] and info["default"] is None:
                            if col not in mapped or mapped[col] is None:
                                if col not in self.AUTO_COLUMNS:
                                    raise ValueError(
                                        f"Pflichtfeld '{col}' fehlt"
                                    )

                    # Duplikat-Check
                    if skip_duplicates and not dry_run:
                        if self._check_duplicate(conn, table_name, mapped, unique_keys):
                            skipped += 1
                            continue

                    if dry_run:
                        inserted += 1
                        continue

                    # INSERT
                    cols = list(mapped.keys())
                    placeholders = ", ".join("?" for _ in cols)
                    col_names = ", ".join(cols)
                    values = [mapped[c] for c in cols]

                    conn.execute(
                        f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})",
                        values
                    )
                    inserted += 1

                except Exception as e:
                    failed += 1
                    errors.append(f"Zeile {i+1}: {str(e)}")

            if not dry_run:
                conn.commit()

                # Import-Run protokollieren
                error_json = json.dumps(errors, ensure_ascii=False) if errors else None
                conn.execute("""
                    INSERT INTO import_runs
                    (target_table, source_type, source_path, rows_total,
                     rows_inserted, rows_skipped, rows_failed, errors,
                     completed_at, triggered_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (table_name, "rows", source_info, len(rows),
                      inserted, skipped, failed, error_json, now, triggered_by))
                conn.commit()

                run_id = conn.execute(
                    "SELECT last_insert_rowid()"
                ).fetchone()[0]
            else:
                run_id = None

            return {
                "table": table_name,
                "total": len(rows),
                "inserted": inserted,
                "skipped": skipped,
                "failed": failed,
                "errors": errors,
                "run_id": run_id,
                "dry_run": dry_run,
                "column_map": column_map,
            }

        finally:
            conn.close()

    def import_csv(self, table_name: str, file_path: str,
                   delimiter: str = ";",
                   column_map: Optional[Dict[str, str]] = None,
                   unique_keys: Optional[List[str]] = None,
                   skip_duplicates: bool = True,
                   dist_type: int = 0,
                   dry_run: bool = False) -> Dict:
        """Importiert CSV-Datei in eine Tabelle."""
        rows = self.parse_csv(file_path, delimiter=delimiter)
        return self.import_rows(
            table_name, rows,
            column_map=column_map,
            unique_keys=unique_keys,
            skip_duplicates=skip_duplicates,
            dist_type=dist_type,
            source_info=file_path,
            triggered_by="csv_import",
            dry_run=dry_run,
        )

    def import_json(self, table_name: str, file_path: str,
                    column_map: Optional[Dict[str, str]] = None,
                    unique_keys: Optional[List[str]] = None,
                    skip_duplicates: bool = True,
                    dist_type: int = 0,
                    dry_run: bool = False) -> Dict:
        """Importiert JSON-Datei in eine Tabelle."""
        rows = self.parse_json(file_path)
        return self.import_rows(
            table_name, rows,
            column_map=column_map,
            unique_keys=unique_keys,
            skip_duplicates=skip_duplicates,
            dist_type=dist_type,
            source_info=file_path,
            triggered_by="json_import",
            dry_run=dry_run,
        )

    # ------------------------------------------------------------------
    # Import-Historie
    # ------------------------------------------------------------------

    def get_import_history(self, table_name: Optional[str] = None,
                           limit: int = 20) -> List[Dict]:
        """Gibt Import-Historie zurueck."""
        conn = self._get_db()
        try:
            if table_name:
                rows = conn.execute("""
                    SELECT * FROM import_runs
                    WHERE target_table = ?
                    ORDER BY started_at DESC LIMIT ?
                """, (table_name, limit)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT * FROM import_runs
                    ORDER BY started_at DESC LIMIT ?
                """, (limit,)).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Rollback
    # ------------------------------------------------------------------

    def rollback_import(self, run_id: int) -> Dict:
        """
        Loescht Daten eines Import-Runs (nach created_at Zeitstempel).
        VORSICHT: Loescht alle Zeilen die im gleichen Zeitfenster erstellt wurden.
        """
        conn = self._get_db()
        try:
            run = conn.execute(
                "SELECT * FROM import_runs WHERE id = ?", (run_id,)
            ).fetchone()

            if not run:
                return {"error": f"Import-Run #{run_id} nicht gefunden."}

            table = run["target_table"]
            started = run["started_at"]
            completed = run["completed_at"]

            if not completed:
                return {"error": "Import-Run hat kein completed_at."}

            # Loesche Zeilen die im Zeitfenster erstellt wurden
            schema = self.get_table_schema(table)
            if "created_at" not in schema:
                return {"error": f"Tabelle '{table}' hat kein created_at Feld."}

            result = conn.execute(
                f"DELETE FROM {table} WHERE created_at BETWEEN ? AND ?",
                (started, completed)
            )
            deleted = result.rowcount

            # Import-Run als rollbacked markieren
            conn.execute(
                "UPDATE import_runs SET source_type = 'ROLLED_BACK' WHERE id = ?",
                (run_id,)
            )
            conn.commit()

            return {
                "run_id": run_id,
                "table": table,
                "deleted": deleted,
            }
        finally:
            conn.close()


def format_import_result(result: Dict) -> str:
    """Formatiert Import-Ergebnis als lesbaren Report."""
    if "error" in result:
        return f"[ERROR] {result['error']}"

    prefix = "[DRY-RUN] " if result.get("dry_run") else ""

    lines = [
        f"{prefix}[IMPORT] {result['table']}",
        f"  Gesamt:       {result['total']} Zeilen",
        f"  Importiert:   {result['inserted']}",
        f"  Uebersprungen:{result['skipped']} (Duplikate)",
        f"  Fehlerhaft:   {result['failed']}",
    ]

    if result.get("run_id"):
        lines.append(f"  Run-ID:       #{result['run_id']}")

    if result.get("column_map"):
        lines.append(f"\n  Column-Mapping:")
        for src, tgt in result["column_map"].items():
            lines.append(f"    {src:<25} -> {tgt}")

    if result.get("errors"):
        lines.append(f"\n  Fehler:")
        for e in result["errors"][:10]:
            lines.append(f"    ! {e}")
        if len(result["errors"]) > 10:
            lines.append(f"    ... und {len(result['errors']) - 10} weitere")

    return "\n".join(lines)


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    import argparse
    parser = argparse.ArgumentParser(
        description="BACH Data Import Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Tabellen anzeigen
  python data_importer.py --list-tables

  # Schema einer Tabelle
  python data_importer.py --describe health_diagnoses

  # CSV importieren
  python data_importer.py --table health_contacts --csv contacts.csv

  # JSON importieren
  python data_importer.py --table fin_insurances --json versicherungen.json

  # Dry-Run (nur Validierung)
  python data_importer.py --table health_contacts --csv data.csv --dry-run

  # Mit Duplikat-Keys
  python data_importer.py --table health_contacts --csv data.csv --unique name,phone

  # Import-Historie
  python data_importer.py --history
  python data_importer.py --history health_contacts

  # Rollback
  python data_importer.py --rollback 5
        """
    )

    parser.add_argument("--table", "-t", help="Zieltabelle")
    parser.add_argument("--csv", help="CSV-Datei importieren")
    parser.add_argument("--json", help="JSON-Datei importieren")
    parser.add_argument("--delimiter", default=";", help="CSV-Delimiter (Default: ;)")
    parser.add_argument("--unique", help="Spalten fuer Duplikat-Check (kommagetrennt)")
    parser.add_argument("--dry-run", action="store_true", help="Nur validieren")
    parser.add_argument("--dist-type", type=int, default=0, help="dist_type (0=User, 1=Template, 2=Core)")

    parser.add_argument("--list-tables", action="store_true", help="Importierbare Tabellen anzeigen")
    parser.add_argument("--describe", help="Schema einer Tabelle anzeigen")
    parser.add_argument("--history", nargs="?", const="__all__", help="Import-Historie anzeigen")
    parser.add_argument("--rollback", type=int, help="Import-Run rueckgaengig machen")

    args = parser.parse_args()

    base_path = Path(__file__).parent.parent
    db_path = str(base_path / "data" / "bach.db")

    importer = DataImporter(db_path)

    if args.list_tables:
        tables = importer.list_importable_tables()
        print(f"[TABLES] {len(tables)} importierbare Tabellen:\n")
        for t in tables:
            schema = importer.get_table_schema(t)
            col_count = len(schema) - len(importer.AUTO_COLUMNS & set(schema.keys()))
            print(f"  {t:<35} ({col_count} Daten-Spalten)")

    elif args.describe:
        print(importer.describe_table(args.describe))

    elif args.history:
        table = None if args.history == "__all__" else args.history
        runs = importer.get_import_history(table)
        if not runs:
            print("[HISTORY] Keine Import-Runs gefunden.")
        else:
            print(f"[HISTORY] {len(runs)} Import-Runs:")
            for r in runs:
                status = "ROLLED_BACK" if r.get("source_type") == "ROLLED_BACK" else "OK"
                print(f"  #{r['id']:<4} {r['target_table']:<25} "
                      f"+{r['rows_inserted']} ~{r['rows_skipped']} !{r['rows_failed']}  "
                      f"{r['started_at'][:16]}  [{status}]")

    elif args.rollback:
        result = importer.rollback_import(args.rollback)
        if "error" in result:
            print(f"[ERROR] {result['error']}")
        else:
            print(f"[ROLLBACK] Run #{result['run_id']}: "
                  f"{result['deleted']} Zeilen aus '{result['table']}' geloescht.")

    elif args.table and (args.csv or args.json):
        unique_keys = args.unique.split(",") if args.unique else None

        if args.csv:
            result = importer.import_csv(
                args.table, args.csv,
                delimiter=args.delimiter,
                unique_keys=unique_keys,
                dry_run=args.dry_run,
                dist_type=args.dist_type,
            )
        else:
            result = importer.import_json(
                args.table, args.json,
                unique_keys=unique_keys,
                dry_run=args.dry_run,
                dist_type=args.dist_type,
            )

        print(format_import_result(result))

    else:
        parser.print_help()
