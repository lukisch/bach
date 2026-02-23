#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Research Agent v1.0.0

Wissenschaftliche Recherche und Literaturanalyse.
Integriert PubMed, Perplexity, Consensus und NotebookLM.

Usage:
  python research_agent.py search "query"
  python research_agent.py review --topic "topic" --years 5
  python research_agent.py status
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import Dict, List

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).parent
RECLUDOS_ROOT = SCRIPT_DIR.parents[2]
OUTPUT_DIR = RECLUDOS_ROOT / "User" / "services_output" / "research"
CACHE_DIR = SCRIPT_DIR / "cache"

# Externe Tools URLs
TOOLS = {
    "pubmed": "https:/pubmed.ncbi.nlm.nih.gov/",
    "perplexity": "https:/www.perplexity.ai/",
    "consensus": "https:/consensus.app/",
    "notebooklm": "https:/notebooklm.google.com/",
    "elicit": "https:/elicit.com/",
    "scite": "https:/scite.ai/"
}


class ResearchAgent:
    """Forschungs-Agent für wissenschaftliche Recherche"""
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self._ensure_dirs()
        self.history = self._load_history()
    
    def _ensure_dirs(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load_history(self) -> List[Dict]:
        history_file = CACHE_DIR / "search_history.json"
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_history(self):
        history_file = CACHE_DIR / "search_history.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history[-100:], f, indent=2, ensure_ascii=False)
    
    def search(self, query: str, sources: List[str] = None) -> Dict:
        """Führt Recherche durch"""
        sources = sources or ["pubmed", "perplexity"]
        
        result = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "sources": sources,
            "recommendations": []
        }
        
        # Empfehlungen basierend auf Query
        if any(term in query.lower() for term in ["gene", "protein", "disease", "clinical"]):
            result["recommendations"].append({
                "tool": "PubMed",
                "url": f"{TOOLS['pubmed']}?term={query.replace(' ', '+')}",
                "reason": "Biomedizinische Fachbegriffe erkannt"
            })
        
        if any(term in query.lower() for term in ["study", "evidence", "research"]):
            result["recommendations"].append({
                "tool": "Consensus",
                "url": TOOLS["consensus"],
                "reason": "Wissenschaftliche Evidenz-Suche"
            })
        
        result["recommendations"].append({
            "tool": "Perplexity",
            "url": TOOLS["perplexity"],
            "reason": "Allgemeine Recherche mit Quellen"
        })
        
        # History speichern
        self.history.append({
            "query": query,
            "timestamp": result["timestamp"],
            "sources": sources
        })
        self._save_history()
        
        return result
    
    def create_review_plan(self, topic: str, years: int = 5) -> Dict:
        """Erstellt Literatur-Review Plan"""
        plan = {
            "topic": topic,
            "timeframe": f"Letzte {years} Jahre",
            "created": datetime.now().isoformat(),
            "steps": [
                {
                    "phase": "1. Überblick",
                    "tool": "Perplexity",
                    "action": f"Suche: '{topic}' für Kontext",
                    "time": "5 min"
                },
                {
                    "phase": "2. Systematische Suche",
                    "tool": "PubMed + Consensus",
                    "action": "Strukturierte Datenbanksuche",
                    "time": "15 min"
                },
                {
                    "phase": "3. Screening",
                    "tool": "NotebookLM",
                    "action": "Abstracts filtern und clustern",
                    "time": "10 min"
                },
                {
                    "phase": "4. Volltext-Analyse",
                    "tool": "Claude/Gemini",
                    "action": "Schlüsselpapers analysieren",
                    "time": "20 min"
                },
                {
                    "phase": "5. Synthese",
                    "tool": "Claude",
                    "action": "Zusammenfassung und Gaps",
                    "time": "10 min"
                }
            ],
            "output_file": OUTPUT_DIR / f"review_{topic.replace(' ', '_')[:30]}.md"
        }
        
        return plan
    
    def get_status(self) -> Dict:
        """Agent-Status"""
        return {
            "agent": "Research Agent",
            "version": self.VERSION,
            "status": "active",
            "searches_total": len(self.history),
            "last_search": self.history[-1] if self.history else None,
            "tools_available": list(TOOLS.keys()),
            "output_dir": str(OUTPUT_DIR)
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Research Agent v1.0.0")
    parser.add_argument("command", choices=["search", "review", "status"])
    parser.add_argument("query", nargs="?")
    parser.add_argument("--topic", help="Review-Thema")
    parser.add_argument("--years", type=int, default=5)
    args = parser.parse_args()
    
    agent = ResearchAgent()
    
    if args.command == "search" and args.query:
        result = agent.search(args.query)
        print(f"\n🔬 RECHERCHE: {args.query}")
        print("=" * 60)
        for rec in result["recommendations"]:
            print(f"\n  📚 {rec['tool']}")
            print(f"     {rec['reason']}")
            print(f"     → {rec['url']}")
    
    elif args.command == "review":
        topic = args.topic or args.query or "Thema"
        plan = agent.create_review_plan(topic, args.years)
        print(f"\n📋 REVIEW-PLAN: {topic}")
        print("=" * 60)
        for step in plan["steps"]:
            print(f"\n  {step['phase']}")
            print(f"     Tool: {step['tool']}")
            print(f"     Zeit: {step['time']}")
    
    elif args.command == "status":
        status = agent.get_status()
        print(f"\n📊 RESEARCH AGENT STATUS")
        print("=" * 60)
        print(f"  Version: {status['version']}")
        print(f"  Suchen gesamt: {status['searches_total']}")
        print(f"  Tools: {', '.join(status['tools_available'])}")


if __name__ == "__main__":
    main()
