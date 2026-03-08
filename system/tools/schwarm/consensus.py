# SPDX-License-Identifier: MIT
"""
consensus.py - Konsensus-Muster fuer Schwarm-Entscheidungen
============================================================
Mehrere LLM-Instanzen beantworten dieselbe Frage.
Antworten werden verglichen und Konsens wird ermittelt.

Zwei Modi:
  1. Majority-Vote: Antworten werden auf Kernaussage reduziert, haeufigste gewinnt
  2. Similarity-basiert: Paarweise Aehnlichkeit, Antwort mit hoechstem Avg-Score gewinnt

Usage (als Modul):
    from tools.schwarm.consensus import ConsensusPattern
    cp = ConsensusPattern(question="Was ist Python?", num_voters=3)
    result = cp.run()

Usage (CLI):
    python -m tools.schwarm.consensus "Was ist Python?" --voters 5 --model haiku

Ref: BACH v3.8.0-SUGAR
"""
import argparse
import sys
import time
from collections import Counter
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import List, Dict, Optional

from .runner import ClaudeRunner, log_schwarm_run


class ConsensusPattern:
    """Konsensus-Muster: Mehrere LLM-Runs, dann Abstimmung."""

    # Modell-Shortnames
    MODEL_MAP = {
        "haiku": "claude-haiku-4-5-20251001",
        "sonnet": "claude-sonnet-4-6",
        "opus": "claude-opus-4-6",
    }

    def __init__(self, question: str, num_voters: int = 3,
                 model: str = "haiku", method: str = "similarity",
                 timeout: int = 300):
        """
        Initialisiert das Konsensus-Muster.

        Args:
            question: Die zu beantwortende Frage
            num_voters: Anzahl paralleler LLM-Instanzen (default: 3)
            model: Modell-Shortname oder volle ID (default: haiku)
            method: "majority" oder "similarity" (default: similarity)
            timeout: Timeout pro Aufruf in Sekunden
        """
        self.question = question
        self.num_voters = max(2, num_voters)  # Mindestens 2 Voter
        self.model = self.MODEL_MAP.get(model, model)
        self.method = method
        self.timeout = timeout
        self.responses: List[Dict] = []
        self.consensus_result: Optional[Dict] = None

    def _create_voter_prompt(self, voter_index: int) -> str:
        """Erstellt den Prompt fuer einen Voter.

        Jeder Voter bekommt leicht unterschiedliche Anweisungen,
        um Diversitaet in den Antworten zu foerdern.
        """
        perspectives = [
            "Beantworte die folgende Frage praezise und faktenbasiert.",
            "Beantworte die folgende Frage ausfuehrlich mit Beispielen.",
            "Beantworte die folgende Frage kompakt und auf den Punkt.",
            "Beantworte die folgende Frage aus einer praktischen Perspektive.",
            "Beantworte die folgende Frage aus einer theoretischen Perspektive.",
            "Beantworte die folgende Frage und beruecksichtige verschiedene Standpunkte.",
            "Beantworte die folgende Frage mit Fokus auf die wichtigsten Aspekte.",
        ]
        perspective = perspectives[voter_index % len(perspectives)]

        return (
            f"{perspective}\n\n"
            f"Frage: {self.question}\n\n"
            f"Antwort:"
        )

    def _collect_votes(self) -> List[Dict]:
        """Sammelt Antworten von allen Votern parallel."""
        runner = ClaudeRunner(
            model=self.model,
            timeout=self.timeout,
            allowed_tools=[],  # Keine Tools noetig fuer reine Q&A
        )

        prompts = [
            self._create_voter_prompt(i) for i in range(self.num_voters)
        ]

        print(f"[KONSENSUS] Starte {self.num_voters} Voter ({self.model})...")
        start = time.time()

        raw_results = runner.run_parallel(prompts, max_workers=self.num_voters)

        elapsed = time.time() - start
        print(f"[KONSENSUS] Alle Voter fertig in {elapsed:.1f}s")

        responses = []
        for i, result in enumerate(raw_results):
            responses.append({
                "voter_id": i + 1,
                "success": result["success"],
                "output": result["output"],
                "duration_s": result["duration_s"],
                "tokens_in": result.get("tokens_in", 0),
                "tokens_out": result.get("tokens_out", 0),
                "cost_usd": result.get("cost_usd", 0.0),
            })
            status = "OK" if result["success"] else "FEHLER"
            output_preview = result["output"][:80].replace("\n", " ") if result["output"] else "(leer)"
            print(f"  Voter {i+1}: {status} ({result['duration_s']:.1f}s) - {output_preview}...")

        return responses

    def _similarity_score(self, text_a: str, text_b: str) -> float:
        """Berechnet Aehnlichkeit zwischen zwei Texten (0.0 - 1.0)."""
        if not text_a or not text_b:
            return 0.0
        # SequenceMatcher fuer Textaehnlichkeit
        return SequenceMatcher(None, text_a.lower(), text_b.lower()).ratio()

    def _find_consensus_similarity(self, responses: List[Dict]) -> Dict:
        """Findet Konsens via Similarity-Scoring.

        Jede Antwort wird mit allen anderen verglichen.
        Die Antwort mit dem hoechsten durchschnittlichen Aehnlichkeits-Score gewinnt.
        """
        valid = [r for r in responses if r["success"] and r["output"]]
        if not valid:
            return {"method": "similarity", "consensus": None, "reason": "Keine gueltige Antwort"}

        if len(valid) == 1:
            return {
                "method": "similarity",
                "consensus": valid[0]["output"],
                "winner_voter": valid[0]["voter_id"],
                "confidence": 1.0,
                "reason": "Nur ein gueltiger Voter",
            }

        # Paarweise Aehnlichkeit berechnen
        scores = {}
        for i, resp_a in enumerate(valid):
            total_sim = 0.0
            for j, resp_b in enumerate(valid):
                if i != j:
                    sim = self._similarity_score(resp_a["output"], resp_b["output"])
                    total_sim += sim
            avg_sim = total_sim / (len(valid) - 1)
            scores[i] = avg_sim

        # Bester Score
        best_idx = max(scores, key=scores.get)
        best_score = scores[best_idx]

        return {
            "method": "similarity",
            "consensus": valid[best_idx]["output"],
            "winner_voter": valid[best_idx]["voter_id"],
            "confidence": best_score,
            "all_scores": {valid[i]["voter_id"]: round(s, 3) for i, s in scores.items()},
            "reason": f"Hoechste Durchschnitts-Aehnlichkeit: {best_score:.3f}",
        }

    def _find_consensus_majority(self, responses: List[Dict]) -> Dict:
        """Findet Konsens via Majority-Vote.

        Antworten werden auf erste 200 Zeichen reduziert und verglichen.
        """
        valid = [r for r in responses if r["success"] and r["output"]]
        if not valid:
            return {"method": "majority", "consensus": None, "reason": "Keine gueltige Antwort"}

        # Gruppiere aehnliche Antworten
        groups = []
        for resp in valid:
            placed = False
            for group in groups:
                # Vergleich mit erstem Element der Gruppe
                sim = self._similarity_score(
                    resp["output"][:300], group[0]["output"][:300]
                )
                if sim > 0.5:  # Schwelle fuer "gleiche Antwort"
                    group.append(resp)
                    placed = True
                    break
            if not placed:
                groups.append([resp])

        # Groesste Gruppe = Konsens
        groups.sort(key=len, reverse=True)
        winning_group = groups[0]
        confidence = len(winning_group) / len(valid)

        # Waehle die laengste Antwort aus der Gewinnergruppe
        best = max(winning_group, key=lambda r: len(r["output"]))

        return {
            "method": "majority",
            "consensus": best["output"],
            "winner_voter": best["voter_id"],
            "confidence": confidence,
            "group_sizes": [len(g) for g in groups],
            "reason": f"Groesste Gruppe: {len(winning_group)}/{len(valid)} Voter",
        }

    def run(self, dry_run: bool = False) -> Dict:
        """Fuehrt das Konsensus-Muster aus.

        Args:
            dry_run: Nur Konfiguration anzeigen, keine API-Aufrufe

        Returns:
            Dict mit consensus, confidence, responses, stats
        """
        print(f"\n{'=' * 60}")
        print(f"  SCHWARM KONSENSUS")
        print(f"{'=' * 60}")
        print(f"  Frage:    {self.question[:80]}...")
        print(f"  Voter:    {self.num_voters}")
        print(f"  Modell:   {self.model}")
        print(f"  Methode:  {self.method}")
        print()

        if dry_run:
            print("[DRY-RUN] Wuerde folgende Voter-Prompts senden:")
            for i in range(self.num_voters):
                prompt = self._create_voter_prompt(i)
                print(f"  Voter {i+1}: {prompt[:80]}...")
            return {"dry_run": True}

        start_time = time.time()

        # 1. Votes sammeln
        self.responses = self._collect_votes()

        # 2. Konsens finden
        print(f"\n[KONSENSUS] Ermittle Konsens ({self.method})...")
        if self.method == "majority":
            self.consensus_result = self._find_consensus_majority(self.responses)
        else:
            self.consensus_result = self._find_consensus_similarity(self.responses)

        elapsed = time.time() - start_time

        # 3. Kosten-Tracking
        total_tokens_in = sum(r.get("tokens_in", 0) for r in self.responses)
        total_tokens_out = sum(r.get("tokens_out", 0) for r in self.responses)
        total_cost = sum(r.get("cost_usd", 0.0) for r in self.responses)

        try:
            log_schwarm_run(
                pattern="consensus",
                task=self.question[:500],
                tokens_in=total_tokens_in,
                tokens_out=total_tokens_out,
                cost_usd=total_cost,
                workers=self.num_voters,
                duration_ms=int(elapsed * 1000),
                status="completed" if self.consensus_result.get("consensus") else "failed",
                result_summary=(
                    f"method={self.method}, confidence={self.consensus_result.get('confidence', 0):.2f}, "
                    f"winner=voter_{self.consensus_result.get('winner_voter', '?')}"
                ),
            )
        except Exception:
            pass

        # 4. Ergebnis ausgeben
        print(f"\n{'=' * 60}")
        print(f"  ERGEBNIS")
        print(f"{'=' * 60}")

        if self.consensus_result.get("consensus"):
            confidence = self.consensus_result.get("confidence", 0)
            confidence_label = (
                "HOCH" if confidence > 0.7
                else "MITTEL" if confidence > 0.4
                else "NIEDRIG"
            )
            print(f"  Konfidenz:     {confidence:.2f} ({confidence_label})")
            print(f"  Gewinner:      Voter {self.consensus_result.get('winner_voter', '?')}")
            print(f"  Methode:       {self.consensus_result.get('method')}")
            print(f"  Grund:         {self.consensus_result.get('reason')}")
            print(f"  Dauer:         {elapsed:.1f}s")
            print(f"  Kosten:        ${total_cost:.4f}")
            print(f"\n  --- KONSENS-ANTWORT ---")
            # Antwort umbrechen auf 76 Zeichen
            answer = self.consensus_result["consensus"]
            for line in answer.split("\n"):
                print(f"  {line}")
        else:
            print(f"  KEIN KONSENS GEFUNDEN")
            print(f"  Grund: {self.consensus_result.get('reason', 'Unbekannt')}")

        print(f"{'=' * 60}")

        return {
            "question": self.question,
            "consensus": self.consensus_result,
            "responses": self.responses,
            "stats": {
                "total_duration_s": elapsed,
                "tokens_in": total_tokens_in,
                "tokens_out": total_tokens_out,
                "cost_usd": total_cost,
                "num_voters": self.num_voters,
                "model": self.model,
            },
        }


def main():
    """CLI-Einstieg fuer Konsensus-Muster."""
    parser = argparse.ArgumentParser(
        description="Schwarm Konsensus-Muster: Mehrere LLMs, eine Antwort"
    )
    parser.add_argument("question", nargs="?", help="Die zu beantwortende Frage")
    parser.add_argument(
        "--voters", "-v", type=int, default=3,
        help="Anzahl Voter (default: 3)"
    )
    parser.add_argument(
        "--model", "-m", default="haiku",
        help="Modell: haiku, sonnet, opus (default: haiku)"
    )
    parser.add_argument(
        "--method", choices=["similarity", "majority"], default="similarity",
        help="Konsens-Methode (default: similarity)"
    )
    parser.add_argument(
        "--timeout", type=int, default=300,
        help="Timeout pro Voter in Sekunden (default: 300)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Nur Konfiguration anzeigen"
    )

    args = parser.parse_args()

    if not args.question:
        parser.print_help()
        print("\nBeispiel: bach schwarm consensus \"Was ist der beste Ansatz fuer Error-Handling in Python?\"")
        return 1

    pattern = ConsensusPattern(
        question=args.question,
        num_voters=args.voters,
        model=args.model,
        method=args.method,
        timeout=args.timeout,
    )

    result = pattern.run(dry_run=args.dry_run)
    return 0 if result.get("consensus") or result.get("dry_run") else 1


if __name__ == "__main__":
    sys.exit(main())
