#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Inventory Engine — Pull-basiertes Vorratsmanagement (INT02)

Portiert aus HausLagerist V4 (Standalone) fuer BACH-Integration.
Kernlogik: Pull-Quotient, Ampel, Bestandsbuchung, Exponentielles Glaetten.

Formeln:
  Pull-Quotient:  Q = stock / (daily_demand * days_ahead)
  Dringlichkeit:  D = (priority / min(Q, 10)) * max(0, 1 - Q)
  Exp. Glaetten:  V_new = alpha * V_measured + (1 - alpha) * V_old
  Abweichung:     |(actual - expected) / expected| > 0.2

Quellen: FAST_HausLagerist_V4/order_engine.py, intelligence.py
"""

import math
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Ampel-Konstanten
AMPEL_ROT = "ROT"
AMPEL_GELB = "GELB"
AMPEL_GRUEN = "GRUEN"
AMPEL_GRAU = "GRAU"

# Defaults
DEFAULT_WARN_DAYS = 7
DEFAULT_ALPHA = 0.3
DEFAULT_DEVIATION_THRESHOLD = 0.2


class InventoryEngine:
    """
    Pull-basierte Bestandsverwaltung fuer BACH.

    Berechnet Bedarf aus Orders, ermittelt Pull-Quotienten,
    generiert priorisierte Einkaufslisten und lernt Verbrauchsmuster.
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def _get_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    # ================================================================
    # BEDARF (Demand Calculation)
    # ================================================================

    def calculate_daily_demand(self, article_id: int,
                               target_date: Optional[date] = None,
                               conn: sqlite3.Connection = None) -> Tuple[float, List[Tuple[str, float]]]:
        """
        Summiert taeglichen Bedarf aus allen aktiven Orders fuer einen Artikel.

        Returns:
            (total_daily_demand, breakdown) wobei breakdown = [(reason, daily_amount), ...]
        """
        close = False
        if conn is None:
            conn = self._get_db()
            close = True

        try:
            target_date = target_date or date.today()
            target_str = target_date.isoformat()

            # Alle aktiven Orders fuer diesen Artikel
            rows = conn.execute("""
                SELECT id, order_type, start_date, end_date, target_date,
                       quantity_value, cycle_interval_days, reason, priority
                FROM household_orders
                WHERE article_id = ? AND status = 'active'
            """, (article_id,)).fetchall()

            total = 0.0
            breakdown = []

            for row in rows:
                daily = 0.0
                order_type = row["order_type"]

                if order_type == "routine":
                    cycle = row["cycle_interval_days"]
                    if cycle and cycle > 0:
                        daily = row["quantity_value"] / cycle

                elif order_type in ("period", "project"):
                    start = row["start_date"]
                    end = row["end_date"]
                    if start and end:
                        if target_str < start or target_str > end:
                            continue
                        duration = max(1, (date.fromisoformat(end) - date.fromisoformat(start)).days)
                        daily = row["quantity_value"] / duration

                elif order_type == "oneshot":
                    td = row["target_date"]
                    if td:
                        days_until = (date.fromisoformat(td) - target_date).days
                        if 0 < days_until <= 30:
                            daily = row["quantity_value"] / days_until

                if daily > 0:
                    reason = row["reason"] or self._order_type_label(order_type)
                    total += daily
                    breakdown.append((reason, daily))

            return total, breakdown
        finally:
            if close:
                conn.close()

    @staticmethod
    def _order_type_label(order_type: str) -> str:
        return {"routine": "Routine", "period": "Zeitraum",
                "oneshot": "Einmalig", "project": "Projekt"}.get(order_type, order_type)

    # ================================================================
    # PULL-QUOTIENT & DRINGLICHKEIT
    # ================================================================

    @staticmethod
    def calculate_pull_quotient(stock: float, demand: float) -> float:
        """Q = stock / demand. Returns inf wenn kein Bedarf."""
        if demand <= 0:
            return float("inf")
        return stock / demand

    @staticmethod
    def calculate_urgency(priority: int, quotient: float) -> float:
        """D = (priority / min(Q, 10)) * max(0, 1 - Q)"""
        if quotient == float("inf") or quotient <= 0:
            return 0.0
        q = min(quotient, 10.0)
        return max(0.0, (priority / q) * max(0.0, 1.0 - q))

    @staticmethod
    def needs_pull(quotient: float, threshold: float = 1.0) -> bool:
        if quotient == float("inf"):
            return False
        return quotient < threshold

    # ================================================================
    # AMPEL
    # ================================================================

    def get_ampel_status(self, article_id: int,
                         conn: sqlite3.Connection = None) -> str:
        """
        Ampelfarbe fuer einen Artikel.
        ROT:  Leer und Bedarf vorhanden
        GELB: Weniger als warn_days Vorrat
        GRUEN: Genug auf Lager
        GRAU: Kein Bedarf definiert
        """
        close = False
        if conn is None:
            conn = self._get_db()
            close = True

        try:
            row = conn.execute(
                "SELECT quantity, min_quantity FROM household_inventory WHERE id = ?",
                (article_id,)
            ).fetchone()
            if not row:
                return AMPEL_GRAU

            stock = row["quantity"] or 0
            daily_demand, _ = self.calculate_daily_demand(article_id, conn=conn)

            if daily_demand <= 0:
                return AMPEL_GRAU

            if stock <= 0:
                return AMPEL_ROT

            days_left = stock / daily_demand
            if days_left < DEFAULT_WARN_DAYS:
                return AMPEL_GELB

            return AMPEL_GRUEN
        finally:
            if close:
                conn.close()

    def get_ampel_overview(self) -> List[Dict]:
        """Alle nicht-archivierten Artikel mit Ampelstatus, sortiert nach Dringlichkeit."""
        conn = self._get_db()
        try:
            articles = conn.execute("""
                SELECT id, name, category, quantity, unit, min_quantity,
                       priority, pull_threshold, pack_size, location
                FROM household_inventory
                WHERE archived = 0
                ORDER BY category, name
            """).fetchall()

            result = []
            for art in articles:
                aid = art["id"]
                stock = art["quantity"] or 0
                daily_demand, breakdown = self.calculate_daily_demand(aid, conn=conn)

                total_demand = daily_demand * DEFAULT_WARN_DAYS
                q = self.calculate_pull_quotient(stock, total_demand)
                urgency = self.calculate_urgency(art["priority"] or 2, q)
                ampel = self.get_ampel_status(aid, conn=conn)
                days_left = (stock / daily_demand) if daily_demand > 0 else float("inf")

                result.append({
                    "id": aid,
                    "name": art["name"],
                    "category": art["category"] or "",
                    "stock": stock,
                    "unit": art["unit"] or "Stk",
                    "min_quantity": art["min_quantity"] or 0,
                    "daily_demand": daily_demand,
                    "days_left": days_left,
                    "pull_quotient": q,
                    "urgency": urgency,
                    "ampel": ampel,
                    "location": art["location"] or "",
                })

            # ROT zuerst, dann GELB, dann sortiert nach Dringlichkeit
            ampel_order = {AMPEL_ROT: 0, AMPEL_GELB: 1, AMPEL_GRUEN: 2, AMPEL_GRAU: 3}
            result.sort(key=lambda x: (ampel_order.get(x["ampel"], 9), -x["urgency"]))
            return result
        finally:
            conn.close()

    # ================================================================
    # PULL-LISTE (Einkaufsliste)
    # ================================================================

    def generate_pull_list(self, days_ahead: int = 30) -> List[Dict]:
        """
        Erzeugt priorisierte Einkaufsliste aller Pull-Kandidaten.

        Returns:
            [{name, category, stock, demand, missing, packs_needed,
              pull_quotient, urgency, unit, pack_size}, ...]
        """
        conn = self._get_db()
        try:
            articles = conn.execute("""
                SELECT id, name, category, quantity, unit, min_quantity,
                       priority, pull_threshold, pack_size
                FROM household_inventory
                WHERE archived = 0
            """).fetchall()

            pull_items = []

            for art in articles:
                aid = art["id"]
                stock = art["quantity"] or 0
                daily_demand, breakdown = self.calculate_daily_demand(aid, conn=conn)

                total_demand = daily_demand * days_ahead
                q = self.calculate_pull_quotient(stock, total_demand)
                threshold = art["pull_threshold"] or 1.0

                if not self.needs_pull(q, threshold):
                    continue

                priority = art["priority"] or 2
                urgency = self.calculate_urgency(priority, q)
                missing = max(0, total_demand - stock)
                pack_size = art["pack_size"] or 1.0
                packs = math.ceil(missing / pack_size) if missing > 0 else 0

                pull_items.append({
                    "id": aid,
                    "name": art["name"],
                    "category": art["category"] or "",
                    "stock": stock,
                    "unit": art["unit"] or "Stk",
                    "demand": total_demand,
                    "daily_demand": daily_demand,
                    "missing": missing,
                    "packs_needed": packs,
                    "pack_size": pack_size,
                    "pull_quotient": q,
                    "urgency": urgency,
                    "breakdown": breakdown,
                })

            # Hoechste Dringlichkeit zuerst
            pull_items.sort(key=lambda x: x["urgency"], reverse=True)
            return pull_items
        finally:
            conn.close()

    # ================================================================
    # BESTANDSAENDERUNGEN
    # ================================================================

    def stock_in(self, article_id: int, amount: float,
                 supplier_id: int = None, price: float = None,
                 note: str = None) -> Dict:
        """Eingang buchen: stock += amount, Transaction loggen."""
        conn = self._get_db()
        try:
            row = conn.execute(
                "SELECT quantity, name FROM household_inventory WHERE id = ?",
                (article_id,)
            ).fetchone()
            if not row:
                raise ValueError(f"Artikel {article_id} nicht gefunden")

            stock_before = row["quantity"] or 0
            stock_after = stock_before + amount

            conn.execute(
                "UPDATE household_inventory SET quantity = ?, last_restocked = date('now'), updated_at = datetime('now') WHERE id = ?",
                (stock_after, article_id)
            )
            conn.execute("""
                INSERT INTO household_stock_transactions
                (article_id, transaction_type, amount, stock_before, stock_after, supplier_id, price_per_unit, note)
                VALUES (?, 'purchase', ?, ?, ?, ?, ?, ?)
            """, (article_id, amount, stock_before, stock_after, supplier_id, price, note))
            conn.commit()

            return {"name": row["name"], "before": stock_before, "after": stock_after, "amount": amount}
        finally:
            conn.close()

    def stock_out(self, article_id: int, amount: float,
                  reason: str = "consumption", note: str = None) -> Dict:
        """Verbrauch buchen: stock -= amount, Transaction loggen."""
        conn = self._get_db()
        try:
            row = conn.execute(
                "SELECT quantity, name FROM household_inventory WHERE id = ?",
                (article_id,)
            ).fetchone()
            if not row:
                raise ValueError(f"Artikel {article_id} nicht gefunden")

            stock_before = row["quantity"] or 0
            stock_after = max(0, stock_before - amount)

            conn.execute(
                "UPDATE household_inventory SET quantity = ?, updated_at = datetime('now') WHERE id = ?",
                (stock_after, article_id)
            )
            conn.execute("""
                INSERT INTO household_stock_transactions
                (article_id, transaction_type, amount, stock_before, stock_after, note)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (article_id, reason, -amount, stock_before, stock_after, note))
            conn.commit()

            return {"name": row["name"], "before": stock_before, "after": stock_after, "amount": amount}
        finally:
            conn.close()

    # ================================================================
    # INTELLIGENCE: Exponentielles Glaetten
    # ================================================================

    def learn_consumption(self, article_id: int, measured_daily: float,
                          conn: sqlite3.Connection = None) -> Dict:
        """
        Exponentielles Glaetten: V_new = alpha * measured + (1-alpha) * V_old

        Speichert gelernten Wert in system_config (key: learned_consumption_<id>).
        """
        close = False
        if conn is None:
            conn = self._get_db()
            close = True

        try:
            art = conn.execute(
                "SELECT learning_alpha FROM household_inventory WHERE id = ?",
                (article_id,)
            ).fetchone()
            alpha = (art["learning_alpha"] if art else None) or DEFAULT_ALPHA

            # Bisheriger Wert
            key = f"inv_learned_{article_id}"
            dp_key = f"inv_dp_{article_id}"

            old_row = conn.execute(
                "SELECT value FROM system_config WHERE key = ?", (key,)
            ).fetchone()
            old_value = float(old_row["value"]) if old_row else None

            dp_row = conn.execute(
                "SELECT value FROM system_config WHERE key = ?", (dp_key,)
            ).fetchone()
            data_points = int(dp_row["value"]) if dp_row else 0

            if old_value is None or old_value == 0:
                new_value = measured_daily
                data_points = 1
            else:
                new_value = alpha * measured_daily + (1 - alpha) * old_value
                data_points += 1

            # Speichern (UPSERT)
            conn.execute(
                "INSERT INTO system_config (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?",
                (key, str(new_value), str(new_value))
            )
            conn.execute(
                "INSERT INTO system_config (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?",
                (dp_key, str(data_points), str(data_points))
            )
            conn.commit()

            return {
                "old_value": old_value or 0,
                "new_value": new_value,
                "alpha": alpha,
                "data_points": data_points,
            }
        finally:
            if close:
                conn.close()

    def detect_deviation(self, article_id: int) -> Optional[Dict]:
        """
        Prueft ob tatsaechlicher Verbrauch >20% vom erwarteten abweicht.

        Returns:
            {"type": "faster"|"slower", "expected": float, "actual": float,
             "deviation_pct": float, "suggestion": str} oder None
        """
        conn = self._get_db()
        try:
            # Erwarteter Verbrauch aus Routine-Orders
            rows = conn.execute("""
                SELECT quantity_value, cycle_interval_days
                FROM household_orders
                WHERE article_id = ? AND status = 'active' AND order_type = 'routine'
                  AND cycle_interval_days > 0
            """, (article_id,)).fetchall()

            if not rows:
                return None

            expected = sum(r["quantity_value"] / r["cycle_interval_days"] for r in rows)
            if expected <= 0:
                return None

            # Tatsaechlicher Verbrauch aus Transaktionen (letzte 14 Tage)
            cutoff = (date.today() - timedelta(days=14)).isoformat()
            txns = conn.execute("""
                SELECT amount, timestamp FROM household_stock_transactions
                WHERE article_id = ? AND timestamp >= ?
                  AND transaction_type IN ('consumption', 'remove')
                ORDER BY timestamp
            """, (article_id, cutoff)).fetchall()

            if len(txns) < 2:
                return None

            total_consumed = sum(abs(t["amount"]) for t in txns)
            first = datetime.fromisoformat(txns[0]["timestamp"]).date()
            last = datetime.fromisoformat(txns[-1]["timestamp"]).date()
            days = max(1, (last - first).days)
            actual = total_consumed / days

            deviation = (actual - expected) / expected
            if abs(deviation) < DEFAULT_DEVIATION_THRESHOLD:
                return None

            if deviation > 0:
                return {
                    "type": "faster",
                    "expected": expected,
                    "actual": actual,
                    "deviation_pct": deviation * 100,
                    "suggestion": f"Verbrauch {deviation*100:.0f}% hoeher. Intervall verkuerzen?",
                }
            else:
                return {
                    "type": "slower",
                    "expected": expected,
                    "actual": actual,
                    "deviation_pct": deviation * 100,
                    "suggestion": f"Verbrauch {abs(deviation)*100:.0f}% niedriger. Intervall verlaengern?",
                }
        finally:
            conn.close()

    def suggest_routine(self, article_id: int) -> Optional[Dict]:
        """
        Schlaegt Routine-Order basierend auf Verbrauchshistorie vor.

        Returns:
            {"quantity": float, "interval_days": int, "daily_consumption": float,
             "confidence": float} oder None
        """
        conn = self._get_db()
        try:
            art = conn.execute(
                "SELECT pack_size, learning_alpha FROM household_inventory WHERE id = ?",
                (article_id,)
            ).fetchone()
            if not art:
                return None

            pack_size = art["pack_size"] or 1.0

            # Gelernter Verbrauch
            key = f"inv_learned_{article_id}"
            dp_key = f"inv_dp_{article_id}"
            learned_row = conn.execute(
                "SELECT value FROM system_config WHERE key = ?", (key,)
            ).fetchone()
            dp_row = conn.execute(
                "SELECT value FROM system_config WHERE key = ?", (dp_key,)
            ).fetchone()

            learned = float(learned_row["value"]) if learned_row else None
            data_points = int(dp_row["value"]) if dp_row else 0

            if not learned or learned < 0.001:
                return None

            # Optimales Intervall: 1 Packung pro Zyklus
            optimal = pack_size / learned
            if optimal < 3:
                interval = 3
            elif optimal < 7:
                interval = 7
            elif optimal < 14:
                interval = 14
            elif optimal < 30:
                interval = int((optimal // 7) * 7) or 7
            else:
                interval = 30

            quantity = round(learned * interval, 1)
            confidence = min(0.95, 0.5 + (data_points * 0.1))

            return {
                "quantity": quantity,
                "interval_days": interval,
                "daily_consumption": round(learned, 3),
                "confidence": confidence,
                "data_points": data_points,
            }
        finally:
            conn.close()
