# SPDX-License-Identifier: MIT
"""
Wiki Handler - Wiki-Artikel aus wiki/ anzeigen
====================================================

bach wiki list              Alle Artikel auflisten
bach wiki <thema>           Artikel anzeigen
bach wiki <ordner>/<thema>  Artikel aus Unterordner anzeigen
bach wiki search "keyword"  Artikel durchsuchen
bach wiki folders           Alle Themenordner auflisten

Unterordner-Unterstuetzung (NEU v1.1.50):
  wiki/foerderung/icf.txt  ->  bach wiki foerderung/icf
  wiki/steuer/elster.txt   ->  bach wiki steuer/elster
"""
from pathlib import Path
from .base import BaseHandler


class WikiHandler(BaseHandler):
    """Handler fuer wiki Operationen"""

    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.wiki_path = base_path / "help" / "wiki"

    @property
    def profile_name(self) -> str:
        return "wiki"

    @property
    def target_file(self) -> Path:
        return self.wiki_path

    def get_operations(self) -> dict:
        return {
            "list": "Alle Wiki-Artikel auflisten",
            "folders": "Alle Themenordner auflisten",
            "<thema>": "Artikel zu einem Thema anzeigen",
            "<ordner>/<thema>": "Artikel aus Unterordner (z.B. foerderung/icf)",
            "search": "Artikel durchsuchen"
        }

    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if not self.wiki_path.exists():
            return False, f"Wiki-Ordner nicht gefunden: {self.wiki_path}"

        if operation == "list" or operation is None:
            return self._list()
        elif operation == "folders":
            return self._list_folders()
        elif operation == "search":
            if not args:
                return False, "Usage: bach wiki search \"keyword\""
            return self._search(" ".join(args))
        else:
            # operation ist das Thema (mit oder ohne Unterordner)
            return self._show(operation)

    def _list(self) -> tuple:
        """Alle Wiki-Artikel auflisten (inkl. Unterordner)"""
        # Index-Datei pruefen
        index_file = self.wiki_path / "_index.txt"
        if index_file.exists():
            index_content = index_file.read_text(encoding="utf-8")

            # Unterordner ergaenzen falls vorhanden
            folders = self._get_folders()
            if folders:
                folder_info = "\n\nTHEMENORDNER\n------------\n"
                for folder, count in folders:
                    folder_info += f"  {folder}/              ({count} Artikel)\n"
                folder_info += "\n  Abruf: bach wiki <ordner>/<thema>\n"
                folder_info += "  z.B.:  bach wiki foerderung/icf"
                return True, f"WIKI-ARTIKEL\n{'='*50}\n\n{index_content}{folder_info}"

            return True, f"WIKI-ARTIKEL\n{'='*50}\n\n{index_content}"

        # Sonst einfache Liste
        articles = list(self.wiki_path.glob("*.txt"))
        results = ["WIKI-ARTIKEL", "=" * 50, ""]

        for article in sorted(articles):
            if article.name.startswith("_"):
                continue
            name = article.stem
            try:
                first_line = article.read_text(encoding="utf-8").split("\n")[0]
                desc = first_line[:50] if first_line else ""
            except:
                desc = ""
            results.append(f"  {name:<20} {desc}")

        # Unterordner
        folders = self._get_folders()
        if folders:
            results.append("")
            results.append("THEMENORDNER")
            results.append("-" * 40)
            for folder, count in folders:
                results.append(f"  {folder}/              ({count} Artikel)")
            results.append("")
            results.append("  Abruf: bach wiki <ordner>/<thema>")

        results.append("")
        results.append(f"Gesamt: {len(articles)} Artikel")
        results.append("Anzeigen: bach wiki <thema>")

        return True, "\n".join(results)

    def _list_folders(self) -> tuple:
        """Alle Themenordner mit ihren Artikeln auflisten"""
        folders = self._get_folders()

        if not folders:
            return True, "Keine Themenordner vorhanden.\n\nThemenordner werden fuer grosse Wissensgebiete angelegt."

        results = ["WIKI-THEMENORDNER", "=" * 50, ""]

        for folder_name, count in folders:
            folder_path = self.wiki_path / folder_name
            results.append(f"{folder_name.upper()}/")
            results.append("-" * 40)

            # Index lesen falls vorhanden
            index_file = folder_path / "_index.txt"
            if index_file.exists():
                try:
                    content = index_file.read_text(encoding="utf-8")
                    # Nur erste Zeilen als Beschreibung
                    lines = content.split("\n")[:5]
                    for line in lines:
                        if line.strip():
                            results.append(f"  {line}")
                except:
                    pass

            # Artikel auflisten
            articles = [f for f in folder_path.glob("*.txt") if not f.name.startswith("_")]
            for article in sorted(articles):
                results.append(f"  - {folder_name}/{article.stem}")

            results.append("")

        results.append(f"Gesamt: {len(folders)} Ordner")
        results.append("Abruf: bach wiki <ordner>/<thema>")

        return True, "\n".join(results)

    def _get_folders(self) -> list:
        """Alle Unterordner mit Artikelanzahl zurueckgeben"""
        folders = []
        for item in self.wiki_path.iterdir():
            if item.is_dir() and not item.name.startswith("_"):
                txt_count = len([f for f in item.glob("*.txt") if not f.name.startswith("_")])
                if txt_count > 0:
                    folders.append((item.name, txt_count))
        return sorted(folders)

    def _show(self, thema: str) -> tuple:
        """Wiki-Artikel anzeigen (unterstuetzt Unterordner)"""
        # Normalisieren: Backslash zu Slash
        thema = thema.replace("\\", "/").lower()

        # Unterordner-Pfad?
        if "/" in thema:
            parts = thema.split("/", 1)
            folder = parts[0]
            subtopic = parts[1] if len(parts) > 1 else "_index"

            # Versuche Unterordner-Artikel
            article_path = self.wiki_path / folder / f"{subtopic}.txt"

            if not article_path.exists():
                # Vielleicht ohne .txt?
                article_path = self.wiki_path / folder / subtopic
                if article_path.is_dir():
                    # Es ist ein weiterer Unterordner - zeige dessen Index
                    article_path = article_path / "_index.txt"

            if not article_path.exists():
                # Fallback: Ordner-Index
                folder_index = self.wiki_path / folder / "_index.txt"
                if folder_index.exists():
                    try:
                        content = folder_index.read_text(encoding="utf-8")
                        return True, f"WIKI: {folder.upper()}/ (Index)\n{'='*50}\n\n{content}\n\nArtikel '{subtopic}' nicht gefunden im Ordner."
                    except:
                        pass

                # Fuzzy-Suche im Unterordner
                folder_path = self.wiki_path / folder
                if folder_path.is_dir():
                    matches = list(folder_path.glob(f"*{subtopic}*.txt"))
                    if matches:
                        suggestions = ", ".join(f"{folder}/{m.stem}" for m in matches[:5])
                        return False, f"Artikel '{thema}' nicht gefunden.\nMeintest du: {suggestions}?"

                return False, f"Artikel '{thema}' nicht gefunden.\nVerfuegbar: bach wiki list"
        else:
            # Einfacher Artikel im Hauptordner
            article_path = self.wiki_path / f"{thema}.txt"

            if not article_path.exists():
                # Vielleicht ist es ein Ordner?
                folder_path = self.wiki_path / thema
                if folder_path.is_dir():
                    # Zeige Ordner-Index
                    index_file = folder_path / "_index.txt"
                    if index_file.exists():
                        try:
                            content = index_file.read_text(encoding="utf-8")
                            # Liste auch Artikel
                            articles = [f for f in folder_path.glob("*.txt") if not f.name.startswith("_")]
                            article_list = "\n\nARTIKEL IN DIESEM ORDNER\n------------------------\n"
                            for a in sorted(articles):
                                article_list += f"  bach wiki {thema}/{a.stem}\n"
                            return True, f"WIKI: {thema.upper()}/ (Themenordner)\n{'='*50}\n\n{content}{article_list}"
                        except:
                            pass
                    # Ordner ohne Index - liste nur Artikel
                    articles = [f for f in folder_path.glob("*.txt") if not f.name.startswith("_")]
                    if articles:
                        results = [f"WIKI: {thema.upper()}/ (Themenordner)", "=" * 50, "", "Artikel:"]
                        for a in sorted(articles):
                            results.append(f"  bach wiki {thema}/{a.stem}")
                        return True, "\n".join(results)

            if not article_path.exists():
                # Fuzzy-Suche
                matches = list(self.wiki_path.glob(f"*{thema}*.txt"))
                if matches:
                    suggestions = ", ".join(m.stem for m in matches[:5])
                    return False, f"Artikel '{thema}' nicht gefunden.\nMeintest du: {suggestions}?"
                return False, f"Artikel '{thema}' nicht gefunden.\nVerfuegbar: bach wiki list"

        try:
            content = article_path.read_text(encoding="utf-8")
            display_name = thema.upper().replace("/", " / ")
            return True, f"WIKI: {display_name}\n{'='*50}\n\n{content}"
        except Exception as e:
            return False, f"Fehler beim Lesen: {e}"

    def _search(self, keyword: str) -> tuple:
        """Wiki-Artikel durchsuchen (inkl. Unterordner)"""
        matches = []
        keyword_lower = keyword.lower()

        # Hauptordner durchsuchen
        for article in self.wiki_path.glob("*.txt"):
            if article.name.startswith("_"):
                continue
            match = self._search_file(article, keyword_lower)
            if match:
                matches.append((article.stem, match))

        # Unterordner durchsuchen
        for folder in self.wiki_path.iterdir():
            if folder.is_dir() and not folder.name.startswith("_"):
                for article in folder.glob("*.txt"):
                    if article.name.startswith("_"):
                        continue
                    match = self._search_file(article, keyword_lower)
                    if match:
                        matches.append((f"{folder.name}/{article.stem}", match))

        if not matches:
            return True, f"Keine Treffer fuer: {keyword}"

        results = [f"WIKI-SUCHE: {keyword}", "=" * 50, ""]
        for name, context in matches:
            results.append(f"  {name}")
            if context:
                results.append(f"    ...{context}...")
            results.append("")

        results.append(f"{len(matches)} Treffer")
        return True, "\n".join(results)

    def _search_file(self, path: Path, keyword_lower: str) -> str:
        """Einzelne Datei durchsuchen, Kontext zurueckgeben"""
        try:
            content = path.read_text(encoding="utf-8").lower()
            if keyword_lower in content or keyword_lower in path.stem.lower():
                idx = content.find(keyword_lower)
                if idx >= 0:
                    return content[max(0, idx-20):idx+len(keyword_lower)+30].replace("\n", " ")
                return ""
        except:
            pass
        return None
