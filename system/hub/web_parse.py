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
WebParseHandler - Webseiten-Parsing (ersetzt Jina Reader MCP)
==============================================================
bach web-parse url <url>        URL laden, als Markdown ausgeben
bach web-parse clean <url>      Nur Hauptinhalt (kein Nav/Footer)
bach web-parse cache list       Gecachte Seiten anzeigen
bach web-parse cache clear      Cache leeren

Task: 994
"""
import os
import re
import sys
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
from .base import BaseHandler

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


class WebParseHandler(BaseHandler):

    def __init__(self, base_path_or_app):
        super().__init__(base_path_or_app)
        self.cache_dir = self.base_path / "data" / "cache" / "web"

    @property
    def profile_name(self) -> str:
        return "web-parse"

    @property
    def target_file(self) -> Path:
        return self.cache_dir

    def get_operations(self) -> dict:
        return {
            "url": "URL laden und als Markdown: url <url>",
            "clean": "Nur Hauptinhalt: clean <url>",
            "cache": "Cache verwalten: cache list|clear",
        }

    def handle(self, operation: str, args: List[str], dry_run: bool = False) -> Tuple[bool, str]:
        if operation == "url" and args:
            if dry_run:
                return True, f"[DRY-RUN] Wuerde {args[0]} laden"
            return self._parse_url(args[0], clean=False)
        elif operation == "clean" and args:
            if dry_run:
                return True, f"[DRY-RUN] Wuerde {args[0]} clean parsen"
            return self._parse_url(args[0], clean=True)
        elif operation == "cache":
            sub = args[0] if args else "list"
            if sub == "list":
                return self._cache_list()
            elif sub == "clear":
                if dry_run:
                    return True, "[DRY-RUN] Cache wuerde geleert"
                return self._cache_clear()
            return False, f"Unbekannt: cache {sub}. Nutze: list, clear"
        else:
            ops = "\n".join(f"  {k}: {v}" for k, v in self.get_operations().items())
            return False, f"Nutzung:\n{ops}"

    def _fetch(self, url: str) -> Tuple[bool, str, str]:
        """Laedt URL herunter. Returns (success, content, error)."""
        try:
            import requests
        except ImportError:
            return False, "", "requests nicht installiert: pip install requests"

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (BACH WebParse/1.0)',
                'Accept': 'text/html,application/xhtml+xml,*/*',
            }
            resp = requests.get(url, timeout=20, headers=headers, allow_redirects=True)
            resp.raise_for_status()
            return True, resp.text, ""
        except Exception as e:
            return False, "", str(e)

    def _html_to_markdown(self, html: str, clean: bool = False) -> str:
        """Konvertiert HTML zu Markdown."""
        # Versuche html2text
        try:
            import html2text
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = True
            h.body_width = 0
            if clean:
                h.ignore_links = True
            return h.handle(html)
        except ImportError:
            pass

        # Fallback: Regex-basiert
        text = html
        # Script/Style entfernen
        text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', text, flags=re.DOTALL | re.IGNORECASE)

        if clean:
            # Nav, header, footer entfernen
            for tag in ['nav', 'header', 'footer', 'aside']:
                text = re.sub(rf'<{tag}[^>]*>.*?</{tag}>', '', text, flags=re.DOTALL | re.IGNORECASE)

        # Ueberschriften
        for i in range(1, 7):
            text = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>', lambda m: f"\n{'#' * i} {m.group(1).strip()}\n", text, flags=re.IGNORECASE)

        # Absaetze und Zeilenumbrueche
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<p[^>]*>', '\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</p>', '', text, flags=re.IGNORECASE)

        # Listen
        text = re.sub(r'<li[^>]*>', '\n- ', text, flags=re.IGNORECASE)

        # Links
        text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.IGNORECASE)

        # Bold/Italic
        text = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', text, flags=re.IGNORECASE)
        text = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', text, flags=re.IGNORECASE)

        # Code
        text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text, flags=re.IGNORECASE)
        text = re.sub(r'<pre[^>]*>(.*?)</pre>', lambda m: f"\n```\n{m.group(1)}\n```\n", text, flags=re.DOTALL | re.IGNORECASE)

        # Restliche Tags entfernen
        text = re.sub(r'<[^>]+>', '', text)

        # HTML-Entities
        text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace('&quot;', '"').replace('&nbsp;', ' ')

        # Mehrere Leerzeilen reduzieren
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def _parse_url(self, url: str, clean: bool = False) -> Tuple[bool, str]:
        """Parst URL und gibt Markdown zurueck."""
        # Cache pruefen
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
        suffix = "_clean" if clean else ""
        cache_file = self.cache_dir / f"{url_hash}{suffix}.md"

        if cache_file.exists():
            content = cache_file.read_text(encoding='utf-8', errors='replace')
            return True, f"[CACHE] {url}\n\n{content}"

        # Herunterladen
        ok, html, err = self._fetch(url)
        if not ok:
            return False, f"Fehler: {err}"

        # Konvertieren
        markdown = self._html_to_markdown(html, clean=clean)

        # Cachen
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        meta = f"<!-- URL: {url} | Parsed: {datetime.now().isoformat()} | Mode: {'clean' if clean else 'full'} -->\n\n"
        cache_file.write_text(meta + markdown, encoding='utf-8')

        return True, f"URL: {url}\nModus: {'clean' if clean else 'full'}\nGroesse: {len(markdown)} Zeichen\n{'=' * 40}\n\n{markdown[:3000]}{'...' if len(markdown) > 3000 else ''}"

    def _cache_list(self) -> Tuple[bool, str]:
        """Zeigt gecachte Seiten."""
        if not self.cache_dir.exists():
            return True, "Cache leer."

        files = list(self.cache_dir.glob("*.md"))
        if not files:
            return True, "Cache leer."

        lines = [f"WEB-PARSE CACHE ({len(files)} Dateien)", "=" * 35]
        total_size = 0
        for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
            size = f.stat().st_size
            total_size += size
            # URL aus Datei extrahieren
            first_line = f.read_text(encoding='utf-8', errors='replace').split('\n')[0]
            url_match = re.search(r'URL: ([^\s|]+)', first_line)
            url = url_match.group(1) if url_match else f.name
            lines.append(f"  {f.name} ({size // 1024}KB) - {url}")

        lines.append(f"\nGesamt: {total_size // 1024}KB")
        return True, "\n".join(lines)

    def _cache_clear(self) -> Tuple[bool, str]:
        """Leert den Cache."""
        if not self.cache_dir.exists():
            return True, "Cache bereits leer."

        count = 0
        for f in self.cache_dir.glob("*.md"):
            f.unlink()
            count += 1

        return True, f"Cache geleert: {count} Dateien entfernt."
