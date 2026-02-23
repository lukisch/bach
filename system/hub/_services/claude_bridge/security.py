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
Security Challenge Layer fuer Claude Bridge
=============================================
Verhindert unbefugten Zugriff auf die Bridge.

Features:
- Challenge-Generierung (Math + Codewort)
- Fuzzy-Matching bei Antworten
- Brute-Force-Schutz (Max 3 Versuche/5 Min)
- 24h Verifikations-Cache

Task: 990
"""
import os
import sys
import re
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')


# Zahlen-Woerter fuer Fuzzy-Matching
ZAHLWOERTER = {
    "null": 0, "eins": 1, "zwei": 2, "drei": 3, "vier": 4,
    "fuenf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9,
    "zehn": 10, "elf": 11, "zwoelf": 12, "dreizehn": 13, "vierzehn": 14,
    "fuenfzehn": 15, "sechzehn": 16, "siebzehn": 17, "achtzehn": 18,
    "neunzehn": 19, "zwanzig": 20,
}

# Umgekehrt: Zahl -> Wort
ZAHL_ZU_WORT = {v: k for k, v in ZAHLWOERTER.items()}


class SecurityChallenge:
    """Security Challenge Layer fuer die Claude Bridge."""

    MAX_ATTEMPTS = 3
    LOCKOUT_MINUTES = 5
    VERIFICATION_HOURS = 24

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._ensure_table()

    def _get_conn(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_table(self):
        conn = self._get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS security_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                challenge_type TEXT NOT NULL,
                challenge_text TEXT NOT NULL,
                expected_answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                verified INTEGER DEFAULT 0,
                verified_at TIMESTAMP,
                attempts INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()

    def generate_challenge(self, user_id: str) -> dict:
        """Generiert eine neue Challenge fuer den User."""
        # Brute-Force Check
        if self._is_locked_out(user_id):
            return {
                "ok": False,
                "error": f"Zu viele Versuche. Warte {self.LOCKOUT_MINUTES} Minuten."
            }

        # Challenge-Typ zufaellig waehlen
        challenge_type = random.choice(["math", "math", "codewort"])

        if challenge_type == "math":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(["+", "-", "*"])
            if op == "+":
                answer = a + b
            elif op == "-":
                answer = a - b
            else:
                a = random.randint(1, 10)
                b = random.randint(1, 10)
                answer = a * b
            challenge_text = f"Was ist {a} {op} {b}?"
            expected = str(answer)
        else:
            words = ["Sonnenblume", "Regenbogen", "Kaffeetasse", "Mondschein",
                     "Sternenhimmel", "Wasserfall", "Blumenwiese", "Donnerwetter"]
            word = random.choice(words)
            challenge_text = f"Antworte mit dem Wort: {word}"
            expected = word

        # In DB speichern
        conn = self._get_conn()
        expires = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("""
            INSERT INTO security_challenges (user_id, challenge_type, challenge_text, expected_answer, expires_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, challenge_type, challenge_text, expected, expires))
        conn.commit()
        conn.close()

        return {"ok": True, "challenge": challenge_text, "type": challenge_type}

    def verify_challenge(self, user_id: str, answer: str) -> dict:
        """Verifiziert eine Challenge-Antwort mit Fuzzy-Matching."""
        conn = self._get_conn()

        # Letzte offene Challenge holen
        row = conn.execute("""
            SELECT id, expected_answer, challenge_type, attempts, expires_at
            FROM security_challenges
            WHERE user_id = ? AND verified = 0
            ORDER BY created_at DESC LIMIT 1
        """, (user_id,)).fetchone()

        if not row:
            conn.close()
            return {"ok": False, "error": "Keine offene Challenge. Nutze /challenge"}

        # Abgelaufen?
        if row['expires_at'] and datetime.now() > datetime.strptime(row['expires_at'], "%Y-%m-%d %H:%M:%S"):
            conn.close()
            return {"ok": False, "error": "Challenge abgelaufen. Neue anfordern."}

        # Versuch zaehlen
        attempts = row['attempts'] + 1
        conn.execute("UPDATE security_challenges SET attempts = ? WHERE id = ?", (attempts, row['id']))

        # Brute-Force Check
        if attempts > self.MAX_ATTEMPTS:
            conn.commit()
            conn.close()
            return {"ok": False, "error": f"Zu viele Versuche ({attempts}/{self.MAX_ATTEMPTS})."}

        # Fuzzy-Matching
        expected = row['expected_answer']
        if self._fuzzy_match(answer, expected, row['challenge_type']):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                "UPDATE security_challenges SET verified = 1, verified_at = ? WHERE id = ?",
                (now, row['id'])
            )
            conn.commit()
            conn.close()
            return {"ok": True, "message": "Verifizierung erfolgreich!"}
        else:
            conn.commit()
            conn.close()
            remaining = self.MAX_ATTEMPTS - attempts
            return {"ok": False, "error": f"Falsche Antwort. Noch {remaining} Versuch(e)."}

    def require_verification(self, user_id: str) -> bool:
        """Prueft ob User in den letzten 24h verifiziert wurde."""
        conn = self._get_conn()
        cutoff = (datetime.now() - timedelta(hours=self.VERIFICATION_HOURS)).strftime("%Y-%m-%d %H:%M:%S")

        row = conn.execute("""
            SELECT COUNT(*) as cnt FROM security_challenges
            WHERE user_id = ? AND verified = 1 AND verified_at > ?
        """, (user_id, cutoff)).fetchone()

        conn.close()
        return row['cnt'] > 0

    def _is_locked_out(self, user_id: str) -> bool:
        """Prueft ob User wegen zu vieler Versuche gesperrt ist."""
        conn = self._get_conn()
        cutoff = (datetime.now() - timedelta(minutes=self.LOCKOUT_MINUTES)).strftime("%Y-%m-%d %H:%M:%S")

        row = conn.execute("""
            SELECT SUM(attempts) as total FROM security_challenges
            WHERE user_id = ? AND created_at > ? AND verified = 0
        """, (user_id, cutoff)).fetchone()

        conn.close()
        total = row['total'] or 0
        return total >= self.MAX_ATTEMPTS * 2

    def _fuzzy_match(self, given: str, expected: str, challenge_type: str) -> bool:
        """Fuzzy-Matching: Gross/Klein, Whitespace, Zahlwoerter."""
        given = given.strip().lower()
        expected = expected.strip().lower()

        # Direkter Match
        if given == expected:
            return True

        # Whitespace normalisieren
        given_clean = re.sub(r'\s+', '', given)
        expected_clean = re.sub(r'\s+', '', expected)
        if given_clean == expected_clean:
            return True

        # Fuer Math-Challenges: Zahlwoerter akzeptieren
        if challenge_type == "math":
            # "drei" -> "3"
            if given in ZAHLWOERTER:
                if str(ZAHLWOERTER[given]) == expected:
                    return True
            # "3" -> akzeptiere auch "drei"
            try:
                num = int(expected)
                if given == ZAHL_ZU_WORT.get(num, ""):
                    return True
            except ValueError:
                pass

        return False
