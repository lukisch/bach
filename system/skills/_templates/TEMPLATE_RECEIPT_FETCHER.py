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
Tool: {anbieter}_quittung_fetcher
Version: 1.0.0
Author: BACH Team
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Anthropic-Compatible: True

TEMPLATE: Quittungs-/Beleg-Fetcher fuer Online-Shops
=========================================================

Dieses Template automatisiert den Abruf von detaillierten Quittungen
(Einzelposten, MwSt, Haendler) aus Online-Shops ueber Browser-Automation.

ANPASSUNGS-ANLEITUNG (3 Schritte):
-----------------------------------

1. EXTRAKTION anpassen:
   - extract_orders_from_source() implementieren
   - Bestellnummern aus Mails/PDFs/Dateien lesen
   - Pro Bestellung: beleg, order_id, out_name, receipt_url erzeugen

2. RECEIPT-URL anpassen:
   - RECEIPT_URL_TEMPLATE auf den Anbieter aendern
   - Login-Check in verify_login() anpassen (welcher Text = Login-Seite?)
   - Ggf. Cookie-Banner wegklicken in fetch_receipt_as_pdf()

3. DATEIFORMAT anpassen:
   - Dateiname-Konvention in extract_orders_from_source() anpassen
   - Ggf. wait_seconds erhoehen fuer langsame Seiten

BEREITS EXISTIERENDE IMPLEMENTIERUNGEN:
   - Temu:   system/tools/steuer/temu_quittung_fetcher.py
     Pattern: Mail-PDF -> Hyperlink _cmsg_biz=1004 -> parent_order_sn
     URL:     temu.com/bgt_order_receipt.html?parent_order_sn={sn}

ARCHITEKTUR:
   Mail/Beleg-Datei
     -> Bestellnummer extrahieren (Regex, PDF-Links, Text-Parsing)
     -> Receipt-URL konstruieren (URL-Template + Bestellnummer)
     -> Edge headless + echtes Profil (Login-Session)
     -> Seite laden + CDP Page.printToPDF
     -> PDF speichern mit Belegnummer

Dependencies:
    - selenium (pip install selenium)
    - PyMuPDF  (pip install PyMuPDF)  -- optional, nur fuer PDF-Quellen
    - Edge Browser mit aktiver Shop-Anmeldung

Exit Codes:
    0 - Erfolg
    1 - Fehler
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

import os
import sys
import subprocess
import time
import json
import base64
import argparse
from datetime import datetime

# Fuer PDF-basierte Quellen:
# import fitz  # PyMuPDF
# from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

# ===========================================================================
# ANPASSEN: Konfiguration fuer deinen Anbieter
# ===========================================================================

ANBIETER = "MeinShop"                     # Name des Anbieters
SHOP_DOMAIN = "www.meinshop.de"           # Domain fuer Login-Check
EDGE_USER_DATA = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")
EDGE_PROFILE = "Default"

# URL-Template: {order_id} wird durch die Bestellnummer ersetzt
RECEIPT_URL_TEMPLATE = (
    "https://{domain}/receipt?order_id={{order_id}}"
    .format(domain=SHOP_DOMAIN)
)

# Texte die auf der Login-Seite erscheinen (lowercase)
LOGIN_INDICATORS = ["anmelden", "einloggen", "sign in", "log in"]

# Dateiendung der Quell-Dateien (Mail-PDFs, HTML-Exports, etc.)
SOURCE_FILE_PATTERN = "_mail.pdf"


# ===========================================================================
# ANPASSEN: Bestellnummern extrahieren
# ===========================================================================

def extract_orders_from_source(folder, beleg_filter=None):
    """Extrahiert Bestellnummern aus Quelldateien.

    ANPASSEN: Implementiere die Logik fuer deinen Anbieter.

    Beispiele:
    - PDF-Hyperlinks scannen (wie Temu)
    - Text aus PDFs extrahieren und Regex anwenden
    - HTML/EML-Dateien parsen
    - CSV/JSON mit Bestelldaten lesen

    Returns:
        list[dict]: Liste mit:
            - beleg: str       Belegnummer (z.B. "B0607")
            - order_id: str    Bestellnummer des Shops
            - filename: str    Quelldatei
            - out_name: str    Ausgabedateiname
            - receipt_url: str URL zur Quittung
    """
    orders = []

    for fname in sorted(os.listdir(folder)):
        if not fname.endswith(SOURCE_FILE_PATTERN):
            continue

        beleg = fname.split("_")[0]  # Belegnummer aus Dateiname
        if beleg_filter and beleg != beleg_filter:
            continue

        # ---------------------------------------------------------------
        # HIER ANPASSEN: Bestellnummer(n) aus der Datei extrahieren
        # ---------------------------------------------------------------

        # Beispiel: Aus PDF-Hyperlinks (wie Temu)
        # import fitz
        # from urllib.parse import urlparse, parse_qs
        # path = os.path.join(folder, fname)
        # doc = fitz.open(path)
        # order_ids = set()
        # for page in doc:
        #     for link in page.get_links():
        #         uri = link.get("uri", "")
        #         if "receipt" in uri and "order_id=" in uri:
        #             parsed = parse_qs(urlparse(uri).query)
        #             oid = parsed.get("order_id", [None])[0]
        #             if oid:
        #                 order_ids.add(oid)
        # doc.close()

        # Beispiel: Aus Dateiname extrahieren
        # import re
        # match = re.search(r'ORDER-(\d+)', fname)
        # order_ids = {match.group(1)} if match else set()

        # Beispiel: Aus Text im PDF
        # import fitz
        # doc = fitz.open(os.path.join(folder, fname))
        # text = "".join(page.get_text() for page in doc)
        # order_ids = set(re.findall(r'Bestellnummer:\s*(\S+)', text))
        # doc.close()

        # PLATZHALTER - ersetzen mit echter Logik:
        order_ids = set()
        print(f"  [WARNUNG] extract_orders_from_source() nicht implementiert!")
        print(f"            Bitte fuer {ANBIETER} anpassen.")
        break

        # ---------------------------------------------------------------
        # Ab hier generisch: Orders aufbauen
        # ---------------------------------------------------------------
        sorted_ids = sorted(order_ids)
        multi = len(sorted_ids) > 1

        for idx, oid in enumerate(sorted_ids, 1):
            suffix = f"_{idx}" if multi else ""
            out_name = f"{beleg}{suffix}_quittung.pdf"

            orders.append({
                "beleg": beleg,
                "order_id": oid,
                "filename": fname,
                "out_name": out_name,
                "receipt_url": RECEIPT_URL_TEMPLATE.format(order_id=oid),
            })

    return orders


# ===========================================================================
# Edge-Management (generisch, normalerweise nicht aendern)
# ===========================================================================

def is_edge_running():
    """Prueft ob Edge-Prozesse laufen."""
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "(Get-Process msedge -ErrorAction SilentlyContinue).Count"],
            capture_output=True, text=True, timeout=10,
        )
        return int(result.stdout.strip() or "0") > 0
    except Exception:
        return False


def kill_edge():
    """Beendet alle Edge-Prozesse sauber."""
    try:
        subprocess.run(
            ["powershell", "-Command",
             "Get-Process msedge -ErrorAction SilentlyContinue | "
             "ForEach-Object { $_.CloseMainWindow() | Out-Null }"],
            capture_output=True, timeout=10,
        )
        time.sleep(2)
        if is_edge_running():
            subprocess.run(
                ["powershell", "-Command",
                 "Stop-Process -Name msedge -Force -ErrorAction SilentlyContinue"],
                capture_output=True, timeout=10,
            )
            time.sleep(1)
        return not is_edge_running()
    except Exception:
        return False


def create_driver(headless=True):
    """Erstellt Edge WebDriver mit dem echten User-Profil."""
    options = EdgeOptions()
    options.add_argument(f"--user-data-dir={EDGE_USER_DATA}")
    options.add_argument(f"--profile-directory={EDGE_PROFILE}")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--disable-features=msEdgeSidebarV2")
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1200,900")
    return webdriver.Edge(options=options)


# ===========================================================================
# ANPASSEN: Login-Pruefung
# ===========================================================================

def verify_login(driver):
    """Prueft ob der User beim Shop eingeloggt ist.

    ANPASSEN: URL und Login-Erkennung fuer deinen Anbieter.
    """
    driver.get(f"https://{SHOP_DOMAIN}/orders")  # Bestelluebersicht
    time.sleep(3)
    page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    return not any(ind in page_text[:300] for ind in LOGIN_INDICATORS)


# ===========================================================================
# Quittungs-Abruf (generisch, selten aendern)
# ===========================================================================

def fetch_receipt_as_pdf(driver, url, output_path, wait_seconds=4):
    """Ruft eine Quittungsseite ab und speichert als PDF.

    Optional ANPASSEN:
    - Cookie-Banner wegklicken
    - Auf bestimmte Elemente warten
    - Druckansicht aktivieren
    """
    driver.get(url)
    time.sleep(wait_seconds)

    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)
    except TimeoutException:
        pass

    # Optional: Cookie-Banner wegklicken
    # try:
    #     btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='cookie-accept']")
    #     btn.click()
    #     time.sleep(0.5)
    # except Exception:
    #     pass

    page_text = driver.find_element(By.TAG_NAME, "body").text[:500]
    lower_text = page_text.lower()

    if any(ind in lower_text[:200] for ind in LOGIN_INDICATORS):
        return {"status": "error", "reason": "not_logged_in"}

    pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {
        "printBackground": True,
        "preferCSSPageSize": True,
        "paperWidth": 8.27,
        "paperHeight": 11.69,
        "marginTop": 0.4,
        "marginBottom": 0.4,
        "marginLeft": 0.4,
        "marginRight": 0.4,
    })

    with open(output_path, "wb") as f:
        f.write(base64.b64decode(pdf_data["data"]))

    return {
        "status": "ok",
        "size": os.path.getsize(output_path),
        "page_text_preview": page_text[:200],
    }


# ===========================================================================
# Hauptlogik (generisch)
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(
        description=f"{ANBIETER} Quittungs-Fetcher",
    )
    parser.add_argument("--beleg-dir", type=str, default=None,
                        help="Ordner mit Quelldateien (Default: Skript-Verzeichnis)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--beleg", type=str, default=None,
                        help="Nur bestimmten Beleg (z.B. B0650)")
    parser.add_argument("--visible", action="store_true",
                        help="Browser sichtbar")
    parser.add_argument("--wait", type=int, default=4,
                        help="Wartezeit pro Seite (Sek.)")
    parser.add_argument("--force", action="store_true",
                        help="Vorhandene erneut abrufen")
    parser.add_argument("--no-kill", action="store_true",
                        help="Edge nicht schliessen")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    beleg_dir = args.beleg_dir or os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(beleg_dir, "Quittungen")
    log_file = os.path.join(output_dir, "fetch_log.json")

    print("=" * 60)
    print(f"  {ANBIETER} Quittungs-Fetcher v{__version__}")
    print("=" * 60)

    # 1. Orders extrahieren
    print(f"\n[1/4] Extrahiere Bestellnummern...")
    orders = extract_orders_from_source(beleg_dir, beleg_filter=args.beleg)

    if not orders:
        print("  Keine Bestellungen gefunden!")
        return 0

    belege = set(o["beleg"] for o in orders)
    print(f"  -> {len(orders)} Bestellungen aus {len(belege)} Belegen")

    os.makedirs(output_dir, exist_ok=True)

    if not args.force:
        todo = [o for o in orders
                if not os.path.exists(os.path.join(output_dir, o["out_name"]))]
        skipped = len(orders) - len(todo)
        if skipped:
            print(f"  -> {skipped} bereits vorhanden (uebersprungen)")
        orders = todo

    if not orders:
        print("\n  Alle Quittungen bereits vorhanden! (--force zum Neuabruf)")
        return 0

    if args.dry_run:
        print(f"\n[DRY-RUN] Wuerde {len(orders)} Quittungen abrufen:")
        for o in orders:
            print(f"  {o['out_name']:30s} <- {o['order_id']}")
        return 0

    # 2. Edge schliessen
    print(f"\n[2/4] Edge-Profil vorbereiten...")
    if is_edge_running():
        if args.no_kill:
            print("  [FEHLER] Edge laeuft! Bitte schliessen oder --no-kill entfernen.")
            return 1
        print("  Edge laeuft -> wird kurz geschlossen...")
        if not kill_edge():
            print("  [FEHLER] Edge konnte nicht beendet werden!")
            return 1
        print("  -> Edge geschlossen")
    else:
        print("  -> Edge ist nicht aktiv")

    # 3. Browser starten
    mode = "(sichtbar)" if args.visible else "(headless)"
    print(f"\n[3/4] Starte Edge {mode}...")
    try:
        driver = create_driver(headless=not args.visible)
    except WebDriverException as e:
        print(f"\n[FEHLER] Edge nicht startbar:\n  {e}")
        return 1

    print("  -> Pruefe Login...")
    if not verify_login(driver):
        print(f"\n  [!] Nicht bei {ANBIETER} eingeloggt!")
        print(f"      Bitte in Edge bei {SHOP_DOMAIN} einloggen und erneut starten.")
        driver.quit()
        return 1
    print("  -> Login OK!")

    # 4. Quittungen abrufen
    print(f"\n[4/4] Rufe {len(orders)} Quittungen ab...\n")

    log = {
        "timestamp": datetime.now().isoformat(),
        "tool": f"{ANBIETER.lower()}_quittung_fetcher",
        "version": __version__,
        "total": len(orders),
        "success": 0,
        "errors": 0,
        "results": [],
    }

    try:
        for i, order in enumerate(orders, 1):
            out_name = order["out_name"]
            out_path = os.path.join(output_dir, out_name)

            print(f"  [{i:3d}/{len(orders)}] {out_name:30s} ...", end=" ", flush=True)

            try:
                result = fetch_receipt_as_pdf(
                    driver, order["receipt_url"], out_path, args.wait)

                if result["status"] == "ok":
                    print(f"OK ({result['size']/1024:.0f} KB)")
                    log["success"] += 1
                else:
                    reason = result.get("reason", "unbekannt")
                    print(f"FEHLER: {reason}")
                    log["errors"] += 1
                    if reason == "not_logged_in":
                        print("\n  [!] Session abgelaufen!")
                        break

                result["out_name"] = out_name
                result["order_id"] = order["order_id"]
                log["results"].append(result)

            except Exception as e:
                print(f"FEHLER: {e}")
                log["errors"] += 1
                log["results"].append({
                    "out_name": out_name,
                    "order_id": order["order_id"],
                    "status": "exception",
                    "error": str(e),
                })

            if i < len(orders):
                time.sleep(1)

    finally:
        driver.quit()

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"  Ergebnis: {log['success']} OK, {log['errors']} Fehler")
    print(f"  Gespeichert in: {output_dir}")
    print(f"{'=' * 60}")
    print(f"\n  Edge kann jetzt wieder normal gestartet werden.")

    return 0 if log["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
