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
FinancialProof - Datenbank-Modul
SQLite-Datenbank für Watchlist, Jobs und Analyse-Ergebnisse
"""
import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from enum import Enum
import sys
from pathlib import Path

# Füge das Hauptverzeichnis zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import config


class JobStatus(str, Enum):
    """Status eines Analyse-Auftrags"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class WatchlistItem:
    """Ein Asset in der Watchlist"""
    id: Optional[int] = None
    symbol: str = ""
    name: str = ""
    asset_type: str = "stock"  # stock, etf, fund, crypto
    sector: Optional[str] = None
    notes: Optional[str] = None
    added_at: Optional[datetime] = None


@dataclass
class Job:
    """Ein Analyse-Auftrag"""
    id: Optional[int] = None
    symbol: str = ""
    analysis_type: str = ""
    parameters: Optional[Dict] = None
    status: JobStatus = JobStatus.PENDING
    progress: int = 0
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


@dataclass
class AnalysisResult:
    """Ergebnis einer Analyse"""
    id: Optional[int] = None
    job_id: int = 0
    summary: str = ""
    details: Optional[str] = None
    data: Optional[Dict] = None
    signals: Optional[List[Dict]] = None
    confidence: Optional[float] = None
    created_at: Optional[datetime] = None


class DatabaseManager:
    """Verwaltet die SQLite-Datenbank"""

    def __init__(self):
        self.db_path = config.DB_PATH
        self._init_db()

    @contextmanager
    def get_connection(self):
        """Context Manager für Datenbankverbindungen"""
        conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _init_db(self):
        """Initialisiert die Datenbank mit dem Schema"""
        schema = """
        -- Beobachtete Assets (Watchlist)
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL,
            name TEXT,
            asset_type TEXT DEFAULT 'stock',
            sector TEXT,
            notes TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Portfolio-Positionen
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            quantity REAL,
            avg_buy_price REAL,
            buy_date DATE,
            FOREIGN KEY (symbol) REFERENCES watchlist(symbol) ON DELETE CASCADE
        );

        -- Analyse-Aufträge
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            analysis_type TEXT NOT NULL,
            parameters TEXT,
            status TEXT DEFAULT 'pending',
            progress INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT
        );

        -- Analyse-Ergebnisse
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            summary TEXT,
            details TEXT,
            data TEXT,
            signals TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
        );

        -- Indices für Performance
        CREATE INDEX IF NOT EXISTS idx_jobs_symbol ON jobs(symbol);
        CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
        CREATE INDEX IF NOT EXISTS idx_results_job ON results(job_id);
        """

        with self.get_connection() as conn:
            conn.executescript(schema)

    # ===== WATCHLIST OPERATIONEN =====

    def add_to_watchlist(self, item: WatchlistItem) -> int:
        """Fügt ein Asset zur Watchlist hinzu"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT OR REPLACE INTO watchlist
                   (symbol, name, asset_type, sector, notes)
                   VALUES (?, ?, ?, ?, ?)""",
                (item.symbol.upper(), item.name, item.asset_type,
                 item.sector, item.notes)
            )
            return cursor.lastrowid

    def remove_from_watchlist(self, symbol: str):
        """Entfernt ein Asset aus der Watchlist"""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM watchlist WHERE symbol = ?", (symbol.upper(),))

    def get_watchlist(self) -> List[WatchlistItem]:
        """Gibt alle Assets in der Watchlist zurück"""
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM watchlist ORDER BY added_at DESC"
            ).fetchall()
            return [WatchlistItem(
                id=row['id'],
                symbol=row['symbol'],
                name=row['name'],
                asset_type=row['asset_type'],
                sector=row['sector'],
                notes=row['notes'],
                added_at=row['added_at']
            ) for row in rows]

    def get_watchlist_item(self, symbol: str) -> Optional[WatchlistItem]:
        """Holt ein einzelnes Watchlist-Item"""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM watchlist WHERE symbol = ?", (symbol.upper(),)
            ).fetchone()
            if row:
                return WatchlistItem(
                    id=row['id'],
                    symbol=row['symbol'],
                    name=row['name'],
                    asset_type=row['asset_type'],
                    sector=row['sector'],
                    notes=row['notes'],
                    added_at=row['added_at']
                )
            return None

    def is_in_watchlist(self, symbol: str) -> bool:
        """Prüft ob ein Symbol in der Watchlist ist"""
        with self.get_connection() as conn:
            result = conn.execute(
                "SELECT 1 FROM watchlist WHERE symbol = ?", (symbol.upper(),)
            ).fetchone()
            return result is not None

    def update_watchlist_notes(self, symbol: str, notes: str):
        """Aktualisiert Notizen für ein Watchlist-Item"""
        with self.get_connection() as conn:
            conn.execute(
                "UPDATE watchlist SET notes = ? WHERE symbol = ?",
                (notes, symbol.upper())
            )

    # ===== JOB OPERATIONEN =====

    def create_job(self, job: Job) -> int:
        """Erstellt einen neuen Analyse-Auftrag"""
        params_json = json.dumps(job.parameters, ensure_ascii=False) if job.parameters else None
        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO jobs (symbol, analysis_type, parameters, status, progress)
                   VALUES (?, ?, ?, ?, ?)""",
                (job.symbol.upper(), job.analysis_type, params_json,
                 job.status.value, job.progress)
            )
            return cursor.lastrowid

    def get_job(self, job_id: int) -> Optional[Job]:
        """Holt einen Job anhand der ID"""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM jobs WHERE id = ?", (job_id,)
            ).fetchone()
            if row:
                return self._row_to_job(row)
            return None

    def get_jobs(self, symbol: Optional[str] = None,
                 status: Optional[JobStatus] = None,
                 limit: int = 50) -> List[Job]:
        """Holt Jobs mit optionalen Filtern"""
        query = "SELECT * FROM jobs WHERE 1=1"
        params = []

        if symbol:
            query += " AND symbol = ?"
            params.append(symbol.upper())
        if status:
            query += " AND status = ?"
            params.append(status.value)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_job(row) for row in rows]

    def update_job_status(self, job_id: int, status: JobStatus,
                          progress: int = None, error: str = None):
        """Aktualisiert den Status eines Jobs"""
        updates = ["status = ?"]
        params = [status.value]

        if progress is not None:
            updates.append("progress = ?")
            params.append(progress)

        if status == JobStatus.RUNNING:
            updates.append("started_at = ?")
            params.append(datetime.now().isoformat())
        elif status in (JobStatus.COMPLETED, JobStatus.FAILED):
            updates.append("completed_at = ?")
            params.append(datetime.now().isoformat())

        if error:
            updates.append("error_message = ?")
            params.append(error)

        params.append(job_id)

        with self.get_connection() as conn:
            conn.execute(
                f"UPDATE jobs SET {', '.join(updates)} WHERE id = ?",
                params
            )

    def delete_job(self, job_id: int):
        """Löscht einen Job und seine Ergebnisse"""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM results WHERE job_id = ?", (job_id,))
            conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))

    def _row_to_job(self, row) -> Job:
        """Konvertiert eine DB-Zeile zu einem Job-Objekt"""
        params = json.loads(row['parameters']) if row['parameters'] else None
        return Job(
            id=row['id'],
            symbol=row['symbol'],
            analysis_type=row['analysis_type'],
            parameters=params,
            status=JobStatus(row['status']),
            progress=row['progress'],
            created_at=row['created_at'],
            started_at=row['started_at'],
            completed_at=row['completed_at'],
            error_message=row['error_message']
        )

    # ===== RESULT OPERATIONEN =====

    def save_result(self, result: AnalysisResult) -> int:
        """Speichert ein Analyse-Ergebnis"""
        data_json = json.dumps(result.data, ensure_ascii=False) if result.data else None
        signals_json = json.dumps(result.signals, ensure_ascii=False) if result.signals else None

        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO results (job_id, summary, details, data, signals, confidence)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (result.job_id, result.summary, result.details,
                 data_json, signals_json, result.confidence)
            )
            return cursor.lastrowid

    def get_result(self, result_id: int) -> Optional[AnalysisResult]:
        """Holt ein Ergebnis anhand der ID"""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM results WHERE id = ?", (result_id,)
            ).fetchone()
            if row:
                return self._row_to_result(row)
            return None

    def get_results_for_job(self, job_id: int) -> List[AnalysisResult]:
        """Holt alle Ergebnisse für einen Job"""
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM results WHERE job_id = ? ORDER BY created_at DESC",
                (job_id,)
            ).fetchall()
            return [self._row_to_result(row) for row in rows]

    def get_results_for_symbol(self, symbol: str,
                                analysis_type: Optional[str] = None,
                                limit: int = 20) -> List[AnalysisResult]:
        """Holt alle Ergebnisse für ein Symbol"""
        query = """
            SELECT r.* FROM results r
            JOIN jobs j ON r.job_id = j.id
            WHERE j.symbol = ?
        """
        params = [symbol.upper()]

        if analysis_type:
            query += " AND j.analysis_type = ?"
            params.append(analysis_type)

        query += " ORDER BY r.created_at DESC LIMIT ?"
        params.append(limit)

        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_result(row) for row in rows]

    def _row_to_result(self, row) -> AnalysisResult:
        """Konvertiert eine DB-Zeile zu einem Result-Objekt"""
        data = json.loads(row['data']) if row['data'] else None
        signals = json.loads(row['signals']) if row['signals'] else None
        return AnalysisResult(
            id=row['id'],
            job_id=row['job_id'],
            summary=row['summary'],
            details=row['details'],
            data=data,
            signals=signals,
            confidence=row['confidence'],
            created_at=row['created_at']
        )

    # ===== STATISTIKEN =====

    def get_job_counts(self) -> Dict[str, int]:
        """Gibt Job-Zählungen nach Status zurück"""
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT status, COUNT(*) as count FROM jobs GROUP BY status"
            ).fetchall()
            return {row['status']: row['count'] for row in rows}

    def get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """Holt die neuesten Aktivitäten (Jobs + Ergebnisse)"""
        with self.get_connection() as conn:
            rows = conn.execute("""
                SELECT j.id, j.symbol, j.analysis_type, j.status,
                       j.created_at, r.summary
                FROM jobs j
                LEFT JOIN results r ON j.id = r.job_id
                ORDER BY j.created_at DESC
                LIMIT ?
            """, (limit,)).fetchall()
            return [dict(row) for row in rows]


# Singleton-Instanz
db = DatabaseManager()
