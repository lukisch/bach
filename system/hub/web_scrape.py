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
WebScrapeHandler - Browser-Steuerung (ersetzt Playwright MCP)
==============================================================
bach web-scrape get <url>           HTTP GET, Body zurueckgeben
bach web-scrape links <url>         Alle Links einer Seite
bach web-scrape forms <url>         Formular-Felder erkennen
bach web-scrape screenshot <url>    Screenshot (braucht selenium)
bach web-scrape headers <url>       Response-Headers anzeigen

Task: 996
"""
import os
import re
import sys
import json
from pathlib import Path
from typing import List, Tuple
from .base import BaseHandler

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


class WebScrapeHandler(BaseHandler):

    def __init__(self, base_path_or_app):
        super().__init__(base_path_or_app)
        self.output_dir = self.base_path / "data" / "cache" / "scrape"

    @property
    def profile_name(self) -> str:
        return "web-scrape"

    @property
    def target_file(self) -> Path:
        return self.output_dir

    def get_operations(self) -> dict:
        return {
            "get": "HTTP GET: get <url>",
            "links": "Links extrahieren: links <url>",
            "forms": "Formulare erkennen: forms <url>",
            "screenshot": "Screenshot: screenshot <url> (braucht selenium)",
            "headers": "Response-Headers: headers <url>",
        }

    def handle(self, operation: str, args: List[str], dry_run: bool = False) -> Tuple[bool, str]:
        if not args and operation in ('get', 'links', 'forms', 'screenshot', 'headers'):
            return False, f"URL fehlt: bach web-scrape {operation} <url>"

        if dry_run:
            return True, f"[DRY-RUN] {operation} {' '.join(args)}"

        if operation == "get":
            return self._get(args[0])
        elif operation == "links":
            return self._links(args[0])
        elif operation == "forms":
            return self._forms(args[0])
        elif operation == "screenshot":
            return self._screenshot(args[0])
        elif operation == "headers":
            return self._headers(args[0])
        else:
            ops = "\n".join(f"  {k}: {v}" for k, v in self.get_operations().items())
            return False, f"Nutzung:\n{ops}"

    def _request(self, url: str):
        """HTTP GET mit requests."""
        try:
            import requests
        except ImportError:
            return None, "requests nicht installiert: pip install requests"

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (BACH WebScrape/1.0)'}
            resp = requests.get(url, timeout=20, headers=headers, allow_redirects=True)
            resp.raise_for_status()
            return resp, ""
        except Exception as e:
            return None, str(e)

    def _get(self, url: str) -> Tuple[bool, str]:
        """Simple HTTP GET."""
        resp, err = self._request(url)
        if not resp:
            return False, f"Fehler: {err}"

        body = resp.text
        info = f"URL: {resp.url}\nStatus: {resp.status_code}\nContent-Type: {resp.headers.get('content-type', '?')}\nGroesse: {len(body)} Zeichen\n{'=' * 40}\n\n"

        if len(body) > 5000:
            return True, info + body[:5000] + f"\n\n... ({len(body) - 5000} weitere Zeichen)"
        return True, info + body

    def _links(self, url: str) -> Tuple[bool, str]:
        """Alle Links einer Seite extrahieren."""
        resp, err = self._request(url)
        if not resp:
            return False, f"Fehler: {err}"

        # Links mit Regex extrahieren
        links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', resp.text, re.IGNORECASE | re.DOTALL)

        if not links:
            return True, f"Keine Links auf {url}"

        # Bereinigen
        from urllib.parse import urljoin
        results = []
        seen = set()
        for href, text in links:
            href = urljoin(url, href)
            text = re.sub(r'<[^>]+>', '', text).strip()[:60]
            if href not in seen and not href.startswith(('javascript:', 'mailto:', '#')):
                seen.add(href)
                results.append(f"  {text or '(kein Text)'}\n    {href}")

        header = f"Links auf {url} ({len(results)} gefunden)\n{'=' * 40}\n"
        return True, header + "\n".join(results[:50])

    def _forms(self, url: str) -> Tuple[bool, str]:
        """Formular-Felder erkennen."""
        resp, err = self._request(url)
        if not resp:
            return False, f"Fehler: {err}"

        forms = re.findall(r'<form[^>]*>(.*?)</form>', resp.text, re.DOTALL | re.IGNORECASE)
        if not forms:
            return True, f"Keine Formulare auf {url}"

        results = []
        for i, form_html in enumerate(forms):
            # Action und Method
            action = re.search(r'action=["\']([^"\']*)["\']', form_html, re.IGNORECASE)
            method = re.search(r'method=["\']([^"\']*)["\']', form_html, re.IGNORECASE)

            fields = []
            # Input-Felder
            for inp in re.finditer(r'<input[^>]+>', form_html, re.IGNORECASE):
                tag = inp.group()
                name = re.search(r'name=["\']([^"\']*)["\']', tag)
                itype = re.search(r'type=["\']([^"\']*)["\']', tag)
                fields.append(f"    input[{itype.group(1) if itype else 'text'}] name={name.group(1) if name else '?'}")

            # Textarea
            for ta in re.finditer(r'<textarea[^>]*name=["\']([^"\']*)["\']', form_html, re.IGNORECASE):
                fields.append(f"    textarea name={ta.group(1)}")

            # Select
            for sel in re.finditer(r'<select[^>]*name=["\']([^"\']*)["\']', form_html, re.IGNORECASE):
                fields.append(f"    select name={sel.group(1)}")

            results.append(
                f"  Form #{i + 1}: action={action.group(1) if action else '?'} method={method.group(1) if method else 'GET'}\n"
                + "\n".join(fields)
            )

        header = f"Formulare auf {url} ({len(forms)} gefunden)\n{'=' * 40}\n"
        return True, header + "\n\n".join(results)

    def _screenshot(self, url: str) -> Tuple[bool, str]:
        """Screenshot via selenium."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
        except ImportError:
            return False, "selenium nicht installiert: pip install selenium\nFuer Screenshots wird ein Browser-Driver benoetigt."

        self.output_dir.mkdir(parents=True, exist_ok=True)
        out_file = self.output_dir / f"screenshot_{hash(url) & 0xFFFFFF:06x}.png"

        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1280,1024')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            driver.save_screenshot(str(out_file))
            driver.quit()
            return True, f"Screenshot gespeichert: {out_file}"
        except Exception as e:
            return False, f"Screenshot fehlgeschlagen: {e}"

    def _headers(self, url: str) -> Tuple[bool, str]:
        """Response-Headers anzeigen."""
        resp, err = self._request(url)
        if not resp:
            return False, f"Fehler: {err}"

        lines = [
            f"Headers fuer {resp.url}",
            f"Status: {resp.status_code}",
            "=" * 40,
        ]
        for k, v in resp.headers.items():
            lines.append(f"  {k}: {v}")

        return True, "\n".join(lines)
