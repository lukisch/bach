#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
HaushaltHandler - Haushaltsmanagement CLI

Operationen:
  status            Haushalts-Dashboard (Zusammenfassung)
  routines          Alle Routinen (delegiert an RoutineHandler)
  due               Faellige Aufgaben (Routinen + Termine)
  today             Was steht heute an?
  week              Wochenplan
  shopping          Einkaufsliste anzeigen/verwalten
  inventory         Vorratsbestand
  costs             Monatliche Fixkosten-Uebersicht
  kosten-monat      Erwartete irregulare Kosten pro Monat
  add-kosten        Irregulare Kosten hinzufuegen
  help              Hilfe anzeigen

Nutzt: bach.db / household_routines, assistant_calendar, fin_contracts (Unified DB seit v1.1.84)
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from hub.base import BaseHandler
from hub.lang import t


class HaushaltHandler(BaseHandler):

    WEEKDAYS_DE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.user_db_path = base_path / "data" / "bach.db"  # Unified DB seit v1.1.84

    @property
    def profile_name(self) -> str:
        return "haushalt"

    @property
    def target_file(self) -> Path:
        return self.user_db_path

    def get_operations(self) -> dict:
        return {
            "status": "Haushalts-Dashboard",
            "due": "Faellige Aufgaben",
            "today": "Was steht heute an?",
            "week": "Wochenplan",
            "costs": "Fixkosten-Uebersicht",
            "kosten-monat": "Irregulare Kosten pro Monat",
            "add-kosten": "Irregulare Kosten hinzufuegen",
            "kosten-list": "Alle irregularen Kosten",
            "insurance-check": "Versicherungs-Portfolio analysieren",
            "shopping": "Einkaufsliste",
            "add-shopping": "Einkaufsartikel hinzufuegen",
            "done-shopping": "Einkaufsartikel als erledigt markieren",
            "help": "Hilfe",
        }

    def _get_db(self):
        conn = sqlite3.connect(str(self.user_db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def handle(self, operation: str, args: List[str], dry_run: bool = False) -> Tuple[bool, str]:
        op = operation.lower().replace("_", "-")
        if op == "status":
            return self._status(args)
        elif op == "due":
            return self._due(args)
        elif op == "today":
            return self._today(args)
        elif op == "week":
            return self._week(args)
        elif op == "costs":
            return self._costs(args)
        elif op == "kosten-monat":
            return self._kosten_monat(args)
        elif op == "add-kosten":
            return self._add_kosten(args)
        elif op == "kosten-list":
            return self._kosten_list(args)
        elif op == "insurance-check":
            return self._insurance_check(args)
        elif op == "shopping":
            return self._shopping(args)
        elif op == "add-shopping":
            return self._add_shopping(args)
        elif op == "done-shopping":
            return self._done_shopping(args)
        elif op in ("", "help"):
            return self._help()
        else:
            return False, f"Unbekannte Operation: {operation}\nNutze: bach haushalt help"

    # ------------------------------------------------------------------
    # STATUS - Dashboard
    # ------------------------------------------------------------------
    def _status(self, args: List[str]) -> Tuple[bool, str]:
        conn = self._get_db()
        try:
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d")
            week_str = (now + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

            # Routinen-Stats
            total_routines = conn.execute("SELECT COUNT(*) FROM household_routines WHERE is_active = 1").fetchone()[0]
            overdue = conn.execute("""
                SELECT COUNT(*) FROM household_routines
                WHERE is_active = 1 AND next_due <= ?
            """, (now_str + " 23:59:59",)).fetchone()[0]
            due_week = conn.execute("""
                SELECT COUNT(*) FROM household_routines
                WHERE is_active = 1 AND next_due <= ?
            """, (week_str,)).fetchone()[0]

            # Fixkosten
            try:
                monthly_costs = conn.execute("""
                    SELECT SUM(
                        CASE
                            WHEN intervall = 'monatlich' THEN betrag
                            WHEN intervall = 'jaehrlich' THEN betrag / 12.0
                            WHEN intervall = 'quartalsweise' THEN betrag / 3.0
                            ELSE betrag
                        END
                    ) as monthly
                    FROM fin_contracts WHERE kuendigungs_status = 'aktiv'
                """).fetchone()["monthly"] or 0
            except Exception:
                monthly_costs = 0

            try:
                insurance_monthly = conn.execute("""
                    SELECT SUM(
                        CASE
                            WHEN zahlweise = 'monatlich' THEN beitrag
                            WHEN zahlweise = 'jaehrlich' THEN beitrag / 12.0
                            WHEN zahlweise = 'quartalsweise' THEN beitrag / 3.0
                            ELSE beitrag
                        END
                    ) as monthly
                    FROM fin_insurances WHERE status = 'aktiv'
                """).fetchone()["monthly"] or 0
            except Exception:
                insurance_monthly = 0

            # Shopping list
            try:
                shopping_count = conn.execute("SELECT COUNT(*) FROM household_shopping WHERE is_done = 0").fetchone()[0]
            except Exception:
                shopping_count = 0

            # Top 5 ueberfaellige Routinen
            overdue_items = conn.execute("""
                SELECT name, next_due, category FROM household_routines
                WHERE is_active = 1 AND next_due <= ?
                ORDER BY next_due ASC LIMIT 5
            """, (now_str + " 23:59:59",)).fetchall()

            lines = [
                "=== HAUSHALTS-DASHBOARD ===",
                "",
                f"  Routinen aktiv:    {total_routines}",
                f"  Heute faellig:     {overdue}",
                f"  Diese Woche:       {due_week}",
                f"  Einkaufsliste:     {shopping_count} Artikel",
                "",
                f"  FIXKOSTEN/MONAT:",
                f"    Vertraege:       {monthly_costs:,.2f} EUR",
                f"    Versicherungen:  {insurance_monthly:,.2f} EUR",
                f"    GESAMT:          {monthly_costs + insurance_monthly:,.2f} EUR",
                "",
            ]

            if overdue_items:
                lines.append("  UEBERFAELLIGE ROUTINEN:")
                for r in overdue_items:
                    due = (r["next_due"] or "---")[:10]
                    lines.append(f"    - {r['name']:<30} (faellig: {due}, {r['category']})")
                lines.append("")

            lines.append("  Befehle: bach haushalt due | today | week | costs | shopping")

            return True, "\n".join(lines)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # DUE - Faellige Aufgaben
    # ------------------------------------------------------------------
    def _due(self, args: List[str]) -> Tuple[bool, str]:
        days = 7
        for a in args:
            try:
                days = int(a)
                break
            except ValueError:
                pass

        conn = self._get_db()
        try:
            cutoff = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
            now_str = datetime.now().strftime("%Y-%m-%d")

            routines = conn.execute("""
                SELECT id, name, category, next_due FROM household_routines
                WHERE is_active = 1 AND next_due <= ?
                ORDER BY next_due ASC
            """, (cutoff,)).fetchall()

            if not routines:
                return True, f"[HAUSHALT] Keine faelligen Aufgaben in den naechsten {days} Tagen."

            overdue = [r for r in routines if (r["next_due"] or "")[:10] <= now_str]
            upcoming = [r for r in routines if (r["next_due"] or "")[:10] > now_str]

            lines = [f"[HAUSHALT] Faellige Aufgaben ({days} Tage): {len(routines)}\n"]

            if overdue:
                lines.append(f"  *** UEBERFAELLIG ({len(overdue)}) ***")
                for r in overdue:
                    due = (r["next_due"] or "---")[:10]
                    lines.append(f"    [{r['id']:>3}] {r['name']:<30} faellig: {due}  ({r['category']})")
                lines.append("")

            if upcoming:
                lines.append(f"  Demnächst ({len(upcoming)}):")
                for r in upcoming:
                    due = (r["next_due"] or "---")[:10]
                    lines.append(f"    [{r['id']:>3}] {r['name']:<30} faellig: {due}  ({r['category']})")

            lines.append(f"\n  Erledigen: bach routine done <id> [id2 id3...]")
            return True, "\n".join(lines)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # TODAY - Was steht heute an?
    # ------------------------------------------------------------------
    def _today(self, args: List[str]) -> Tuple[bool, str]:
        conn = self._get_db()
        try:
            now = datetime.now()
            today_str = now.strftime("%Y-%m-%d")
            weekday = self.WEEKDAYS_DE[now.weekday()]

            lines = [f"=== HEUTE: {weekday} {now.strftime('%d.%m.%Y')} ===\n"]

            # Faellige Routinen
            routines = conn.execute("""
                SELECT id, name, category, next_due FROM household_routines
                WHERE is_active = 1 AND next_due <= ?
                ORDER BY category ASC, name ASC
            """, (today_str + " 23:59:59",)).fetchall()

            if routines:
                lines.append(f"  ROUTINEN ({len(routines)}):")
                for r in routines:
                    lines.append(f"    [{r['id']:>3}] {r['name']:<30} ({r['category']})")
                lines.append("")
            else:
                lines.append("  Keine faelligen Routinen heute.\n")

            # Termine
            try:
                appointments = conn.execute("""
                    SELECT id, title, event_date, event_time, event_type
                    FROM assistant_calendar
                    WHERE date(event_date) = ? AND status != 'erledigt'
                    ORDER BY event_time ASC
                """, (today_str,)).fetchall()

                if appointments:
                    lines.append(f"  TERMINE ({len(appointments)}):")
                    for a in appointments:
                        time = a["event_time"] or "--:--"
                        lines.append(f"    {time}  {a['title']}")
                    lines.append("")
            except Exception:
                pass  # Calendar table might not exist

            # Einkaufsliste
            try:
                shopping = conn.execute("SELECT COUNT(*) FROM household_shopping WHERE is_done = 0").fetchone()[0]
                if shopping > 0:
                    lines.append(f"  EINKAUFSLISTE: {shopping} Artikel offen")
                    lines.append("    -> bach haushalt shopping")
                    lines.append("")
            except Exception:
                pass

            if routines:
                lines.append(f"  Erledigen: bach routine done <id>")

            return True, "\n".join(lines)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # WEEK - Wochenplan
    # ------------------------------------------------------------------
    def _week(self, args: List[str]) -> Tuple[bool, str]:
        conn = self._get_db()
        try:
            now = datetime.now()
            # Start ab Montag dieser Woche
            monday = now - timedelta(days=now.weekday())
            sunday = monday + timedelta(days=6)

            lines = [f"=== WOCHENPLAN {monday.strftime('%d.%m.')} - {sunday.strftime('%d.%m.%Y')} ===\n"]

            for i in range(7):
                day = monday + timedelta(days=i)
                day_str = day.strftime("%Y-%m-%d")
                weekday = self.WEEKDAYS_DE[day.weekday()]
                is_today = day.date() == now.date()
                marker = " <<< HEUTE" if is_today else ""

                # Routinen fuer diesen Tag
                routines = conn.execute("""
                    SELECT id, name, category FROM household_routines
                    WHERE is_active = 1 AND date(next_due) = ?
                    ORDER BY category ASC
                """, (day_str,)).fetchall()

                # Ueberfallige Routinen am heutigen Tag anzeigen
                if is_today:
                    overdue = conn.execute("""
                        SELECT id, name, category FROM household_routines
                        WHERE is_active = 1 AND date(next_due) < ?
                        ORDER BY next_due ASC
                    """, (day_str,)).fetchall()
                else:
                    overdue = []

                # Termine
                cal_events = []
                try:
                    cal_events = conn.execute("""
                        SELECT title, event_time FROM assistant_calendar
                        WHERE date(event_date) = ? AND status != 'erledigt'
                        ORDER BY event_time ASC
                    """, (day_str,)).fetchall()
                except Exception:
                    pass

                has_items = routines or overdue or cal_events

                if has_items or is_today:
                    lines.append(f"  [{weekday} {day.strftime('%d.%m.')}] {'=' * 40}{marker}")

                    if overdue:
                        for r in overdue:
                            lines.append(f"    !!! [{r['id']:>3}] {r['name']} ({r['category']}) [UEBERFAELLIG]")

                    for r in routines:
                        lines.append(f"    [{r['id']:>3}] {r['name']} ({r['category']})")

                    for e in cal_events:
                        time = e["event_time"] or "--:--"
                        lines.append(f"    {time}  {e['title']}")

                    if not has_items:
                        lines.append("    (nichts geplant)")
                    lines.append("")

            return True, "\n".join(lines)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # COSTS - Fixkosten-Uebersicht
    # ------------------------------------------------------------------
    def _costs(self, args: List[str]) -> Tuple[bool, str]:
        conn = self._get_db()
        try:
            lines = ["=== MONATLICHE FIXKOSTEN ===\n"]

            # Vertraege
            try:
                contracts = conn.execute("""
                    SELECT name, kategorie, betrag, intervall
                    FROM fin_contracts
                    WHERE kuendigungs_status = 'aktiv'
                    ORDER BY kategorie ASC, betrag DESC
                """).fetchall()

                if contracts:
                    lines.append("  VERTRAEGE / ABOS:")
                    total_contracts = 0
                    current_cat = None
                    for c in contracts:
                        cat = c["kategorie"] or "Sonstige"
                        if cat != current_cat:
                            current_cat = cat
                            lines.append(f"    [{cat}]")

                        intervall = c["intervall"] or "monatlich"
                        betrag = c["betrag"] or 0
                        if intervall == "jaehrlich":
                            monthly = betrag / 12.0
                        elif intervall == "quartalsweise":
                            monthly = betrag / 3.0
                        else:
                            monthly = betrag
                        total_contracts += monthly

                        lines.append(f"      {c['name']:<30} {monthly:>8.2f} EUR/Mo  ({betrag:.2f} {intervall})")

                    lines.append(f"    {'':->50}")
                    lines.append(f"    {'Summe Vertraege':<30} {total_contracts:>8.2f} EUR/Mo")
                    lines.append("")
            except Exception:
                total_contracts = 0

            # Versicherungen
            try:
                insurances = conn.execute("""
                    SELECT anbieter, sparte, beitrag, zahlweise
                    FROM fin_insurances
                    WHERE status = 'aktiv'
                    ORDER BY sparte ASC, beitrag DESC
                """).fetchall()

                if insurances:
                    lines.append("  VERSICHERUNGEN:")
                    total_insurance = 0
                    for ins in insurances:
                        zahlweise = ins["zahlweise"] or "jaehrlich"
                        beitrag = ins["beitrag"] or 0
                        if zahlweise == "jaehrlich":
                            monthly = beitrag / 12.0
                        elif zahlweise == "quartalsweise":
                            monthly = beitrag / 3.0
                        else:
                            monthly = beitrag
                        total_insurance += monthly

                        lines.append(f"      {ins['sparte']:<20} ({ins['anbieter']:<15}) {monthly:>8.2f} EUR/Mo  ({beitrag:.2f} {zahlweise})")

                    lines.append(f"    {'':->50}")
                    lines.append(f"    {'Summe Versicherungen':<30} {total_insurance:>8.2f} EUR/Mo")
                    lines.append("")
            except Exception:
                total_insurance = 0

            grand_total = total_contracts + total_insurance
            lines.append(f"  {'=' * 50}")
            lines.append(f"  GESAMTE FIXKOSTEN:  {grand_total:>8.2f} EUR/Mo  ({grand_total * 12:>10.2f} EUR/Jahr)")

            return True, "\n".join(lines)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # KOSTEN-MONAT - Erwartete irregulare Kosten pro Monat
    # ------------------------------------------------------------------
    def _kosten_monat(self, args: List[str]) -> Tuple[bool, str]:
        """Zeigt erwartete irregulare Kosten fuer einen bestimmten Monat."""
        # Parse Monat aus args
        monat = None
        for arg in args:
            try:
                m = int(arg)
                if 1 <= m <= 12:
                    monat = m
                    break
            except ValueError:
                continue

        if not monat:
            monat = datetime.now().month

        monat_namen = ["", "Januar", "Februar", "Maerz", "April", "Mai", "Juni",
                       "Juli", "August", "September", "Oktober", "November", "Dezember"]

        conn = self._get_db()
        try:
            rows = conn.execute("""
                SELECT * FROM irregular_costs
                WHERE expected_month = ? AND is_recurring = 1
                ORDER BY category ASC, expected_amount DESC
            """, (monat,)).fetchall()

            if not rows:
                return True, f"[KOSTEN] Keine erwarteten Kosten fuer {monat_namen[monat]}.\nNutze: bach haushalt add-kosten \"Name\" --monat {monat} --betrag 100"

            lines = [f"[KOSTEN] Erwartete Kosten fuer {monat_namen[monat]}:\n"]

            total = 0
            current_cat = None
            for r in rows:
                cat = r["category"] or "Sonstige"
                if cat != current_cat:
                    current_cat = cat
                    lines.append(f"  [{cat.upper()}]")

                betrag = r["expected_amount"] or 0
                total += betrag
                last_paid = f" (zuletzt: {r['last_paid_date'][:10]})" if r["last_paid_date"] else ""
                lines.append(f"    [{r['id']:>3}] {r['name']:<30} {betrag:>8.2f} EUR{last_paid}")

            lines.append("")
            lines.append(f"  {'=' * 50}")
            lines.append(f"  ERWARTETE SUMME: {total:>8.2f} EUR")

            return True, "\n".join(lines)
        finally:
            conn.close()

    def _add_kosten(self, args: List[str]) -> Tuple[bool, str]:
        """Fuegt eine irregulare Kostenposition hinzu."""
        if not args:
            return False, (
                "Usage: bach haushalt add-kosten \"Name\" [Optionen]\n\n"
                "Optionen:\n"
                "  --monat, -m     Erwarteter Monat (1-12)\n"
                "  --betrag, -b    Erwarteter Betrag in EUR\n"
                "  --kategorie,-k  Kategorie (Steuer, Versicherung, Mitgliedschaft, etc.)\n"
                "  --beschreibung  Beschreibung\n"
                "  --einmalig      Einmalige Kosten (nicht wiederkehrend)"
            )

        # Parse args
        name = None
        for a in args:
            if not a.startswith("-"):
                name = a
                break

        if not name:
            return False, "Kein Name angegeben."

        monat_str = self._get_arg(args, "--monat") or self._get_arg(args, "-m")
        betrag_str = self._get_arg(args, "--betrag") or self._get_arg(args, "-b")
        kategorie = self._get_arg(args, "--kategorie") or self._get_arg(args, "-k")
        beschreibung = self._get_arg(args, "--beschreibung")
        is_recurring = 0 if "--einmalig" in args else 1

        try:
            monat = int(monat_str) if monat_str else None
            if monat and not (1 <= monat <= 12):
                return False, f"Ungueltiger Monat: {monat}. Erwartet: 1-12"
        except ValueError:
            return False, f"Ungueltiger Monat: {monat_str}"

        try:
            betrag = float(betrag_str) if betrag_str else None
        except ValueError:
            return False, f"Ungueltiger Betrag: {betrag_str}"

        conn = self._get_db()
        try:
            cursor = conn.execute("""
                INSERT INTO irregular_costs
                (name, description, category, expected_month, expected_amount, is_recurring)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, beschreibung, kategorie, monat, betrag, is_recurring))
            conn.commit()

            monat_txt = f" im Monat {monat}" if monat else ""
            betrag_txt = f" ({betrag:.2f} EUR)" if betrag else ""
            return True, f"[OK] Kostenposition #{cursor.lastrowid}: {name}{betrag_txt}{monat_txt}"
        finally:
            conn.close()

    def _kosten_list(self, args: List[str]) -> Tuple[bool, str]:
        """Listet alle irregularen Kosten auf."""
        conn = self._get_db()
        try:
            rows = conn.execute("""
                SELECT * FROM irregular_costs
                ORDER BY expected_month ASC NULLS LAST, category ASC, expected_amount DESC
            """).fetchall()

            if not rows:
                return True, "[KOSTEN] Keine irregularen Kosten erfasst.\nNutze: bach haushalt add-kosten \"Name\" --monat 3 --betrag 100 --kategorie Steuer"

            monat_namen = ["---", "Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
                           "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

            lines = [f"[KOSTEN] {len(rows)} Kostenposition(en):\n"]
            lines.append(f"  {'ID':>4} {'Name':<30} {'Kategorie':<15} {'Monat':<6} {'Betrag':>10} {'Typ'}")
            lines.append("  " + "-" * 80)

            total_yearly = 0
            for r in rows:
                monat = monat_namen[r["expected_month"]] if r["expected_month"] else "---"
                betrag = r["expected_amount"] or 0
                kategorie = (r["category"] or "---")[:15]
                typ = "wdhd" if r["is_recurring"] else "einm"
                if r["is_recurring"]:
                    total_yearly += betrag
                lines.append(f"  {r['id']:>4} {r['name']:<30} {kategorie:<15} {monat:<6} {betrag:>10.2f} {typ}")

            lines.append("")
            lines.append(f"  Jaehrliche wiederkehrende Summe: {total_yearly:.2f} EUR")

            return True, "\n".join(lines)
        finally:
            conn.close()

    def _get_arg(self, args: List[str], flag: str) -> Optional[str]:
        for i, a in enumerate(args):
            if a == flag and i + 1 < len(args):
                return args[i + 1]
            if a.startswith(flag + "="):
                return a[len(flag) + 1:]
        return None

    # ------------------------------------------------------------------
    # INSURANCE-CHECK - Versicherungs-Portfolio Analyse
    # ------------------------------------------------------------------
    def _insurance_check(self, args: List[str]) -> Tuple[bool, str]:
        conn = self._get_db()
        try:
            insurances = conn.execute("""
                SELECT id, anbieter, tarif_name, sparte, beitrag, zahlweise,
                       status, steuer_relevant_typ
                FROM fin_insurances WHERE status = 'aktiv'
                ORDER BY sparte
            """).fetchall()

            if not insurances:
                return True, "[HAUSHALT] Keine aktiven Versicherungen gefunden."

            lines = [
                "=== VERSICHERUNGS-PORTFOLIO CHECK ===",
                "",
            ]

            # Kosten berechnen
            total_monthly = 0
            by_category = {}
            no_cost = []
            for ins in insurances:
                monthly = ins["beitrag"] or 0
                zw = ins["zahlweise"] or "monatlich"
                if zw == "jaehrlich":
                    monthly /= 12
                elif zw == "quartalsweise":
                    monthly /= 3
                total_monthly += monthly

                cat = ins["sparte"] or "Sonstige"
                by_category[cat] = by_category.get(cat, 0) + monthly

                if not ins["beitrag"] or ins["beitrag"] == 0:
                    no_cost.append(ins)

            lines.append(f"  Aktive Versicherungen: {len(insurances)}")
            lines.append(f"  Kosten monatlich:      {total_monthly:.2f} EUR")
            lines.append(f"  Kosten jaehrlich:      {total_monthly * 12:.2f} EUR")
            lines.append("")

            # Aufteilung
            lines.append("  AUFTEILUNG:")
            for cat, cost in sorted(by_category.items(), key=lambda x: -x[1]):
                pct = (cost / total_monthly * 100) if total_monthly > 0 else 0
                bar = "#" * int(pct / 5)
                lines.append(f"    {cat:<22} {cost:>8.2f} EUR/Mo  ({pct:>3.0f}%) {bar}")
            lines.append("")

            # Analyse
            warnings = []
            infos = []

            # 1. Fehlende Beitraege
            if no_cost:
                warnings.append(f"{len(no_cost)} Versicherungen ohne Beitragsdaten:")
                for i in no_cost:
                    warnings.append(f"  -> #{i['id']} {i['anbieter']} ({i['sparte']})")
                warnings.append("  Empfehlung: Beitraege nachtragen")

            # 2. Mehrfach-Versicherungen
            from collections import Counter
            sparten = [i["sparte"] for i in insurances]
            dups = {s: c for s, c in Counter(sparten).items() if c > 1}
            if dups:
                for s, c in dups.items():
                    items = [i for i in insurances if i["sparte"] == s]
                    total = sum((i["beitrag"] or 0) for i in items)
                    if s == "KFZ":
                        infos.append(f"{c}x {s}-Versicherungen ({total:.2f} EUR/Mo) - Mehrere Fahrzeuge?")
                    else:
                        warnings.append(f"{c}x {s}-Versicherungen - Duplikat pruefen!")

            # 3. Steuer-Check
            steuer_basis = 0
            steuer_sonst = 0
            for ins in insurances:
                yearly = (ins["beitrag"] or 0)
                zw = ins["zahlweise"] or "monatlich"
                if zw == "monatlich":
                    yearly *= 12
                elif zw == "quartalsweise":
                    yearly *= 4

                if ins["steuer_relevant_typ"] == "Basisvorsorge":
                    steuer_basis += yearly
                elif ins["steuer_relevant_typ"] == "Sonstige_Vorsorge":
                    steuer_sonst += yearly

            lines.append("  STEUERLICHE ABSETZBARKEIT:")
            lines.append(f"    Basisvorsorge:     {steuer_basis:>8.2f} EUR/Jahr (voll absetzbar)")
            lines.append(f"    Sonstige Vorsorge: {steuer_sonst:>8.2f} EUR/Jahr (max 1.900 EUR)")
            if steuer_sonst > 1900:
                diff = steuer_sonst - 1900
                warnings.append(f"Hoechstbetrag Sonstige Vorsorge um {diff:.2f} EUR ueberschritten")
                warnings.append(f"  -> {diff:.2f} EUR jaehrlich nicht absetzbar")
            lines.append("")

            # 4. Fehlende wichtige Versicherungen
            wichtige = {"Haftpflicht": "Privathaftpflicht schuetzt vor Schadenersatz",
                        "Hausrat": "Schuetzt Wohnungsinventar",
                        "PKV": "Krankenversicherung ist Pflicht"}
            vorhandene = {i["sparte"] for i in insurances}
            for v, desc in wichtige.items():
                if v not in vorhandene:
                    warnings.append(f"Fehlend: {v} - {desc}")

            # 5. Empfehlungen
            empfehlungen = []
            if total_monthly > 800:
                empfehlungen.append("Versicherungskosten hoch (>800 EUR/Mo) - Vergleich empfohlen")
            if "Rechtsschutz" in vorhandene and any(i["beitrag"] == 0 for i in insurances if i["sparte"] == "Rechtsschutz"):
                empfehlungen.append("Rechtsschutz: Beitrag unbekannt - ggf. nicht mehr aktiv?")
            if "Risiko-LV" not in vorhandene:
                empfehlungen.append("Risikolebensversicherung fehlt - sinnvoll bei Familie/Kredit")

            # Output
            if warnings:
                lines.append("  [!] WARNUNGEN:")
                for w in warnings:
                    lines.append(f"    ! {w}")
                lines.append("")

            if infos:
                lines.append("  [i] HINWEISE:")
                for i in infos:
                    lines.append(f"    i {i}")
                lines.append("")

            if empfehlungen:
                lines.append("  [*] EMPFEHLUNGEN:")
                for e in empfehlungen:
                    lines.append(f"    * {e}")
                lines.append("")

            # Score
            score = 10
            score -= len(warnings)
            score -= len(no_cost) * 0.5
            score = max(1, min(10, score))
            lines.append(f"  Portfolio-Score: {score:.0f}/10")

            return True, "\n".join(lines)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # SHOPPING - Einkaufsliste
    # ------------------------------------------------------------------
    def _shopping(self, args: List[str]) -> Tuple[bool, str]:
        conn = self._get_db()
        try:
            self._ensure_shopping_table(conn)

            show_done = "--all" in args
            query = "SELECT * FROM household_shopping"
            if not show_done:
                query += " WHERE is_done = 0"
            query += " ORDER BY category ASC, item_name ASC"

            rows = conn.execute(query).fetchall()

            if not rows:
                return True, "[HAUSHALT] Einkaufsliste ist leer.\nNutze: bach haushalt add-shopping \"Milch\" --cat Lebensmittel"

            lines = [f"[HAUSHALT] Einkaufsliste ({len(rows)} Artikel):\n"]
            current_cat = None

            for r in rows:
                cat = r["category"] or "Sonstige"
                if cat != current_cat:
                    current_cat = cat
                    lines.append(f"  [{cat}]")

                done = "[x]" if r["is_done"] else "[ ]"
                qty = f" ({r['quantity']})" if r["quantity"] else ""
                lines.append(f"    {done} [{r['id']:>3}] {r['item_name']}{qty}")

            lines.append(f"\n  Erledigt: bach haushalt done-shopping <id>")
            lines.append(f"  Hinzufuegen: bach haushalt add-shopping \"Artikel\" --cat Lebensmittel")
            return True, "\n".join(lines)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # ADD-SHOPPING
    # ------------------------------------------------------------------
    def _add_shopping(self, args: List[str]) -> Tuple[bool, str]:
        if not args:
            return False, (
                "Usage: bach haushalt add-shopping \"Artikel\" [Optionen]\n\n"
                "Optionen:\n"
                "  --cat, -c    Kategorie (Lebensmittel|Haushalt|Drogerie|Getraenke|Sonstige)\n"
                "  --qty, -q    Menge (z.B. 2, 500g, 1L)"
            )

        name = None
        for a in args:
            if not a.startswith("-"):
                name = a
                break

        if not name:
            return False, "Kein Artikelname angegeben."

        cat = self._get_arg(args, "--cat") or self._get_arg(args, "-c") or "Sonstige"
        qty = self._get_arg(args, "--qty") or self._get_arg(args, "-q")

        conn = self._get_db()
        try:
            self._ensure_shopping_table(conn)
            cursor = conn.execute("""
                INSERT INTO household_shopping (item_name, category, quantity)
                VALUES (?, ?, ?)
            """, (name, cat, qty))
            conn.commit()
            return True, f"[OK] Einkaufsartikel #{cursor.lastrowid}: {name} ({cat})"
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # DONE-SHOPPING
    # ------------------------------------------------------------------
    def _done_shopping(self, args: List[str]) -> Tuple[bool, str]:
        ids, _ = self._parse_ids(args)
        if not ids:
            return False, "Usage: bach haushalt done-shopping <id> [id2...]"

        conn = self._get_db()
        try:
            self._ensure_shopping_table(conn)
            results = []
            for sid in ids:
                row = conn.execute("SELECT * FROM household_shopping WHERE id = ?", (sid,)).fetchone()
                if not row:
                    results.append(f"[WARN] Artikel {sid} nicht gefunden")
                    continue
                conn.execute("UPDATE household_shopping SET is_done = 1 WHERE id = ?", (sid,))
                results.append(f"[OK] {row['item_name']} erledigt")
            conn.commit()
            return True, "\n".join(results)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # HELP
    # ------------------------------------------------------------------
    def _help(self) -> Tuple[bool, str]:
        return True, """HAUSHALT - Haushaltsmanagement
=============================

BEFEHLE:
  bach haushalt status             Dashboard (Zusammenfassung)
  bach haushalt today              Was steht heute an?
  bach haushalt week               Wochenplan (Routinen + Termine)
  bach haushalt due                Faellige Aufgaben (7 Tage)
  bach haushalt due 14             Faellige Aufgaben (14 Tage)
  bach haushalt costs              Monatliche Fixkosten-Uebersicht
  bach haushalt insurance-check    Versicherungs-Portfolio analysieren
  bach haushalt shopping           Einkaufsliste anzeigen
  bach haushalt add-shopping "Milch" --cat Lebensmittel --qty 2
  bach haushalt done-shopping <id> Einkaufsartikel als erledigt markieren

DASHBOARD ZEIGT:
  - Aktive Routinen und ueberfaellige
  - Monatliche Fixkosten (Vertraege + Versicherungen)
  - Einkaufsliste
  - Naechste faellige Aufgaben

ZUSAMMENSPIEL:
  - bach routine: Detaillierte Routinen-Verwaltung (add/done/show)
  - bach calendar: Termine und Kalender
  - bach abo: Abo-Verwaltung und -Erkennung
  - bach gesundheit: Gesundheitsmanagement

DATENBANK: user.db / household_routines, fin_contracts, fin_insurances,
           assistant_calendar, household_shopping"""

    # ------------------------------------------------------------------
    # Hilfsmethoden
    # ------------------------------------------------------------------
    def _ensure_shopping_table(self, conn):
        """Erstellt household_shopping Tabelle falls nicht vorhanden."""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS household_shopping (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                category TEXT DEFAULT 'Sonstige',
                quantity TEXT,
                is_done INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def _parse_ids(self, args: List[str]) -> Tuple[List[int], List[str]]:
        ids = []
        rest = []
        for arg in args:
            try:
                ids.append(int(arg))
            except ValueError:
                rest.append(arg)
        return ids, rest

    def _get_arg(self, args: List[str], flag: str) -> Optional[str]:
        for i, a in enumerate(args):
            if a == flag and i + 1 < len(args):
                return args[i + 1]
            if a.startswith(flag + "="):
                return a[len(flag) + 1:]
        return None
