# SPDX-License-Identifier: MIT
"""
Docs Handler - Dokumentations-Zugriff
=====================================

--docs list          Alle Dokumentationen auflisten
--docs show <n>   Dokument anzeigen
--docs search <term> Dokumentation durchsuchen
"""
from pathlib import Path
from .base import BaseHandler


class DocsHandler(BaseHandler):
    """Handler fuer --docs Operationen"""
    
    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.docs_dir = base_path / "docs"
    
    @property
    def profile_name(self) -> str:
        return "docs"
    
    @property
    def target_file(self) -> Path:
        return self.docs_dir
    
    def get_operations(self) -> dict:
        return {
            "list": "Alle Dokumentationen auflisten",
            "show": "Dokument anzeigen",
            "search": "Dokumentation durchsuchen"
        }
    
    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if operation == "show" and args:
            return self._show(args[0])
        elif operation == "search" and args:
            return self._search(" ".join(args))
        else:
            return self._list()
    
    def _list(self) -> tuple:
        """Dokumentationen auflisten."""
        results = ["BACH DOKUMENTATION", "=" * 50]
        
        if not self.docs_dir.exists():
            return False, "Docs-Verzeichnis nicht gefunden."
        
        # Nach Typ gruppieren
        konzepte = []
        analysen = []
        schemata = []
        andere = []
        
        for doc in sorted(self.docs_dir.glob("*")):
            if doc.is_file() and doc.suffix in ['.md', '.txt', '.sql']:
                name = doc.stem
                if 'KONZEPT' in name.upper():
                    konzepte.append(doc)
                elif 'ANALYSE' in name.upper() or 'SOLL_IST' in name.upper() or 'SYNOPSE' in name.upper():
                    analysen.append(doc)
                elif 'SCHEMA' in name.upper() or doc.suffix == '.sql':
                    schemata.append(doc)
                else:
                    andere.append(doc)
        
        if konzepte:
            results.append("\n[KONZEPTE]")
            for doc in konzepte:
                results.append(f"  {doc.stem}")
        
        if analysen:
            results.append("\n[ANALYSEN]")
            for doc in analysen:
                results.append(f"  {doc.stem}")
        
        if schemata:
            results.append("\n[SCHEMATA]")
            for doc in schemata:
                results.append(f"  {doc.stem}")
        
        if andere:
            results.append("\n[SONSTIGE]")
            for doc in andere:
                results.append(f"  {doc.stem}")
        
        total = len(konzepte) + len(analysen) + len(schemata) + len(andere)
        results.append(f"\n{'=' * 50}")
        results.append(f"Gesamt: {total} Dokumente")
        results.append("\nAnzeigen: --docs show <n>")
        
        return True, "\n".join(results)
    
    def _show(self, name: str) -> tuple:
        """Dokument anzeigen."""
        # Dokument suchen
        found = None
        for doc in self.docs_dir.glob("*"):
            if doc.is_file() and name.lower() in doc.stem.lower():
                found = doc
                break
        
        if not found:
            return False, f"Dokument nicht gefunden: {name}\nNutze: --docs list"
        
        results = [f"DOC: {found.name}", "=" * 50]
        
        try:
            content = found.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            # Max 80 Zeilen anzeigen
            if len(lines) > 80:
                results.extend(lines[:80])
                results.append(f"\n... ({len(lines) - 80} weitere Zeilen)")
                results.append(f"\nVollständig: {found}")
            else:
                results.extend(lines)
        except Exception as e:
            return False, f"Fehler beim Lesen: {e}"
        
        return True, "\n".join(results)
    
    def _search(self, term: str) -> tuple:
        """Dokumentation durchsuchen."""
        results = [f"DOCS SUCHE: '{term}'", "=" * 50]
        
        found = []
        term_lower = term.lower()
        
        for doc in self.docs_dir.rglob("*"):
            if doc.is_file() and doc.suffix in ['.md', '.txt', '.sql']:
                # Im Namen suchen
                if term_lower in doc.stem.lower():
                    found.append((doc, "Name", ""))
                    continue
                
                # Im Inhalt suchen
                try:
                    content = doc.read_text(encoding='utf-8', errors='ignore')
                    if term_lower in content.lower():
                        # Kontext finden
                        idx = content.lower().find(term_lower)
                        context = content[max(0, idx-30):idx+len(term)+30].replace('\n', ' ')
                        found.append((doc, "Inhalt", context))
                except:
                    pass
        
        if not found:
            results.append(f"Keine Dokumente gefunden für: {term}")
        else:
            results.append(f"Gefunden: {len(found)}\n")
            for doc, match_type, context in found[:15]:
                results.append(f"  [{match_type}] {doc.stem}")
                if context:
                    results.append(f"         ...{context}...")
            
            if len(found) > 15:
                results.append(f"\n  ... und {len(found) - 15} weitere")
        
        return True, "\n".join(results)
