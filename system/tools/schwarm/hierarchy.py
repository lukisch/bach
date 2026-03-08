# SPDX-License-Identifier: MIT
"""
hierarchy.py - Hierarchie-Muster fuer Schwarm-Operationen
==========================================================
Boss-Worker-Aggregator Struktur:
  1. Boss (Sonnet/Opus) zerlegt Aufgabe in Sub-Tasks
  2. N Worker (Haiku) bearbeiten Sub-Tasks parallel
  3. Aggregator (Sonnet/Opus) synthetisiert Ergebnisse

Usage (als Modul):
    from tools.schwarm.hierarchy import HierarchyPattern
    hp = HierarchyPattern(task="Erstelle eine REST-API Dokumentation")
    result = hp.run()

Usage (CLI):
    python -m tools.schwarm.hierarchy "Aufgabe" --workers 4 --boss-model sonnet

Ref: BACH v3.8.0-SUGAR
"""
import argparse
import json
import sys
import time
from datetime import datetime
from typing import List, Dict, Optional

from .runner import ClaudeRunner, log_schwarm_run


class HierarchyPattern:
    """Hierarchie-Muster: Boss zerlegt, Worker bearbeiten, Aggregator fasst zusammen."""

    MODEL_MAP = {
        "haiku": "claude-haiku-4-5-20251001",
        "sonnet": "claude-sonnet-4-6",
        "opus": "claude-opus-4-6",
    }

    def __init__(self, task: str, num_workers: int = 3,
                 boss_model: str = "sonnet", worker_model: str = "haiku",
                 timeout: int = 300):
        """
        Initialisiert das Hierarchie-Muster.

        Args:
            task: Die zu bearbeitende Aufgabe
            num_workers: Anzahl paralleler Worker (default: 3)
            boss_model: Modell fuer Boss und Aggregator (default: sonnet)
            worker_model: Modell fuer Worker (default: haiku)
            timeout: Timeout pro Aufruf in Sekunden
        """
        self.task = task
        self.num_workers = max(1, num_workers)
        self.boss_model = self.MODEL_MAP.get(boss_model, boss_model)
        self.worker_model = self.MODEL_MAP.get(worker_model, worker_model)
        self.timeout = timeout
        self.subtasks: List[str] = []
        self.worker_results: List[Dict] = []
        self.final_result: Optional[str] = None

    def _boss_decompose(self) -> List[str]:
        """Boss zerlegt die Aufgabe in Sub-Tasks.

        Gibt eine Liste von Sub-Task-Beschreibungen zurueck.
        """
        prompt = (
            f"Du bist ein Projektmanager. Zerlege die folgende Aufgabe in genau "
            f"{self.num_workers} unabhaengige Sub-Tasks, die parallel bearbeitet "
            f"werden koennen.\n\n"
            f"Aufgabe: {self.task}\n\n"
            f"Antworte NUR mit einem JSON-Array von Strings. Jeder String ist ein "
            f"Sub-Task. Keine weitere Erklaerung.\n\n"
            f"Beispiel-Format:\n"
            f'["Sub-Task 1 Beschreibung", "Sub-Task 2 Beschreibung", "Sub-Task 3 Beschreibung"]'
        )

        runner = ClaudeRunner(
            model=self.boss_model,
            timeout=self.timeout,
            allowed_tools=[],
        )

        print(f"[BOSS] Zerlege Aufgabe in {self.num_workers} Sub-Tasks ({self.boss_model})...")
        result = runner.run(prompt)

        if not result["success"]:
            raise RuntimeError(f"Boss-Zerlegung fehlgeschlagen: {result['stderr']}")

        # JSON aus Antwort extrahieren
        output = result["output"].strip()
        try:
            # Versuche direktes JSON-Parsing
            subtasks = json.loads(output)
            if isinstance(subtasks, list) and all(isinstance(s, str) for s in subtasks):
                return subtasks
        except json.JSONDecodeError:
            pass

        # Fallback: JSON-Array aus Text extrahieren
        import re
        match = re.search(r'\[.*?\]', output, re.DOTALL)
        if match:
            try:
                subtasks = json.loads(match.group())
                if isinstance(subtasks, list):
                    return [str(s) for s in subtasks]
            except json.JSONDecodeError:
                pass

        # Letzter Fallback: Zeilen als Sub-Tasks
        lines = [l.strip().lstrip("0123456789.-) ") for l in output.split("\n") if l.strip()]
        if lines:
            return lines[:self.num_workers]

        raise RuntimeError(f"Boss konnte Aufgabe nicht zerlegen. Ausgabe: {output[:200]}")

    def _workers_execute(self, subtasks: List[str]) -> List[Dict]:
        """Worker bearbeiten die Sub-Tasks parallel.

        Args:
            subtasks: Liste von Sub-Task-Beschreibungen

        Returns:
            Liste von Ergebnis-Dicts mit worker_id, subtask, output, success, etc.
        """
        runner = ClaudeRunner(
            model=self.worker_model,
            timeout=self.timeout,
            allowed_tools=[],
        )

        prompts = []
        for i, subtask in enumerate(subtasks):
            prompt = (
                f"Du bist ein spezialisierter Worker. Bearbeite den folgenden Sub-Task "
                f"gruendlich und praezise.\n\n"
                f"Kontext der Gesamtaufgabe: {self.task}\n\n"
                f"Dein Sub-Task ({i+1}/{len(subtasks)}): {subtask}\n\n"
                f"Liefere ein vollstaendiges Ergebnis fuer genau diesen Sub-Task."
            )
            prompts.append(prompt)

        print(f"[WORKER] Starte {len(subtasks)} Worker ({self.worker_model})...")
        start = time.time()

        raw_results = runner.run_parallel(prompts, max_workers=len(subtasks))

        elapsed = time.time() - start
        print(f"[WORKER] Alle Worker fertig in {elapsed:.1f}s")

        results = []
        for i, (result, subtask) in enumerate(zip(raw_results, subtasks)):
            results.append({
                "worker_id": i + 1,
                "subtask": subtask,
                "success": result["success"],
                "output": result["output"],
                "duration_s": result["duration_s"],
                "tokens_in": result.get("tokens_in", 0),
                "tokens_out": result.get("tokens_out", 0),
                "cost_usd": result.get("cost_usd", 0.0),
            })
            status = "OK" if result["success"] else "FEHLER"
            preview = result["output"][:60].replace("\n", " ") if result["output"] else "(leer)"
            print(f"  Worker {i+1}: {status} ({result['duration_s']:.1f}s) - {preview}...")

        return results

    def _aggregator_synthesize(self, subtasks: List[str],
                                worker_results: List[Dict]) -> str:
        """Aggregator synthetisiert die Worker-Ergebnisse.

        Args:
            subtasks: Die urspruenglichen Sub-Tasks
            worker_results: Ergebnisse aller Worker

        Returns:
            Synthetisiertes Gesamtergebnis als String
        """
        # Worker-Ergebnisse zusammenstellen
        parts = []
        for wr in worker_results:
            if wr["success"] and wr["output"]:
                parts.append(
                    f"--- Sub-Task {wr['worker_id']}: {wr['subtask']} ---\n"
                    f"{wr['output']}\n"
                )
            else:
                parts.append(
                    f"--- Sub-Task {wr['worker_id']}: {wr['subtask']} ---\n"
                    f"[FEHLGESCHLAGEN]\n"
                )

        worker_output = "\n".join(parts)

        prompt = (
            f"Du bist ein Aggregator. Synthetisiere die folgenden Teilergebnisse "
            f"zu einem kohaerenten Gesamtergebnis.\n\n"
            f"Urspruengliche Aufgabe: {self.task}\n\n"
            f"Teilergebnisse der Worker:\n\n"
            f"{worker_output}\n\n"
            f"Erstelle ein zusammenhaengendes, vollstaendiges Ergebnis. "
            f"Entferne Redundanzen, stelle Konsistenz sicher und ergaenze "
            f"fehlende Verbindungen zwischen den Teilen."
        )

        runner = ClaudeRunner(
            model=self.boss_model,
            timeout=self.timeout,
            allowed_tools=[],
        )

        print(f"[AGGREGATOR] Synthetisiere Ergebnisse ({self.boss_model})...")
        result = runner.run(prompt)

        if not result["success"]:
            # Fallback: Einfache Konkatenation
            print("[AGGREGATOR] Fehler - nutze Fallback (Konkatenation)")
            return "\n\n".join(
                wr["output"] for wr in worker_results
                if wr["success"] and wr["output"]
            )

        return result["output"]

    def run(self, dry_run: bool = False) -> Dict:
        """Fuehrt das Hierarchie-Muster aus.

        Args:
            dry_run: Nur Konfiguration anzeigen, keine API-Aufrufe

        Returns:
            Dict mit result, subtasks, worker_results, stats
        """
        print(f"\n{'=' * 60}")
        print(f"  SCHWARM HIERARCHIE")
        print(f"{'=' * 60}")
        print(f"  Aufgabe:       {self.task[:80]}...")
        print(f"  Worker:        {self.num_workers}")
        print(f"  Boss-Modell:   {self.boss_model}")
        print(f"  Worker-Modell: {self.worker_model}")
        print()

        if dry_run:
            print("[DRY-RUN] Wuerde folgende Phasen durchlaufen:")
            print(f"  1. Boss ({self.boss_model}) zerlegt in {self.num_workers} Sub-Tasks")
            print(f"  2. {self.num_workers} Worker ({self.worker_model}) bearbeiten parallel")
            print(f"  3. Aggregator ({self.boss_model}) synthetisiert Ergebnisse")
            return {"dry_run": True}

        start_time = time.time()
        total_tokens_in = 0
        total_tokens_out = 0
        total_cost = 0.0

        # Phase 1: Boss zerlegt Aufgabe
        try:
            self.subtasks = self._boss_decompose()
            print(f"\n[BOSS] {len(self.subtasks)} Sub-Tasks erstellt:")
            for i, st in enumerate(self.subtasks):
                print(f"  {i+1}. {st[:80]}")
        except RuntimeError as e:
            print(f"[FEHLER] Boss-Phase: {e}")
            log_schwarm_run(
                pattern="hierarchy", task=self.task[:500],
                tokens_in=0, tokens_out=0, cost_usd=0.0,
                workers=self.num_workers,
                duration_ms=int((time.time() - start_time) * 1000),
                status="failed",
                result_summary=f"Boss-Zerlegung fehlgeschlagen: {e}",
            )
            return {
                "success": False,
                "error": str(e),
                "stats": {"total_duration_s": time.time() - start_time},
            }

        # Phase 2: Worker bearbeiten Sub-Tasks
        print()
        self.worker_results = self._workers_execute(self.subtasks)

        successful_workers = sum(1 for wr in self.worker_results if wr["success"])
        print(f"\n[WORKER] {successful_workers}/{len(self.worker_results)} erfolgreich")

        if successful_workers == 0:
            elapsed = time.time() - start_time
            log_schwarm_run(
                pattern="hierarchy", task=self.task[:500],
                tokens_in=0, tokens_out=0, cost_usd=0.0,
                workers=self.num_workers,
                duration_ms=int(elapsed * 1000),
                status="failed",
                result_summary="Alle Worker fehlgeschlagen",
            )
            return {
                "success": False,
                "error": "Alle Worker fehlgeschlagen",
                "subtasks": self.subtasks,
                "worker_results": self.worker_results,
                "stats": {"total_duration_s": elapsed},
            }

        # Phase 3: Aggregator synthetisiert
        print()
        self.final_result = self._aggregator_synthesize(
            self.subtasks, self.worker_results
        )

        elapsed = time.time() - start_time

        # Kosten berechnen
        for wr in self.worker_results:
            total_tokens_in += wr.get("tokens_in", 0)
            total_tokens_out += wr.get("tokens_out", 0)
            total_cost += wr.get("cost_usd", 0.0)

        # Kosten-Tracking in DB
        try:
            log_schwarm_run(
                pattern="hierarchy",
                task=self.task[:500],
                tokens_in=total_tokens_in,
                tokens_out=total_tokens_out,
                cost_usd=total_cost,
                workers=self.num_workers,
                duration_ms=int(elapsed * 1000),
                status="completed",
                result_summary=(
                    f"subtasks={len(self.subtasks)}, "
                    f"workers_ok={successful_workers}/{len(self.worker_results)}"
                ),
            )
        except Exception:
            pass

        # Ergebnis ausgeben
        print(f"\n{'=' * 60}")
        print(f"  ERGEBNIS")
        print(f"{'=' * 60}")
        print(f"  Sub-Tasks:     {len(self.subtasks)}")
        print(f"  Worker OK:     {successful_workers}/{len(self.worker_results)}")
        print(f"  Dauer:         {elapsed:.1f}s")
        print(f"  Kosten:        ${total_cost:.4f}")
        print(f"\n  --- SYNTHESIERTES ERGEBNIS ---")
        for line in self.final_result.split("\n"):
            print(f"  {line}")
        print(f"{'=' * 60}")

        return {
            "success": True,
            "result": self.final_result,
            "subtasks": self.subtasks,
            "worker_results": self.worker_results,
            "stats": {
                "total_duration_s": elapsed,
                "tokens_in": total_tokens_in,
                "tokens_out": total_tokens_out,
                "cost_usd": total_cost,
                "num_workers": self.num_workers,
                "boss_model": self.boss_model,
                "worker_model": self.worker_model,
                "successful_workers": successful_workers,
            },
        }


def main():
    """CLI-Einstieg fuer Hierarchie-Muster."""
    parser = argparse.ArgumentParser(
        description="Schwarm Hierarchie-Muster: Boss-Worker-Aggregator"
    )
    parser.add_argument("task", nargs="?", help="Die zu bearbeitende Aufgabe")
    parser.add_argument(
        "--workers", "-w", type=int, default=3,
        help="Anzahl Worker (default: 3)"
    )
    parser.add_argument(
        "--boss-model", default="sonnet",
        help="Boss/Aggregator Modell: haiku, sonnet, opus (default: sonnet)"
    )
    parser.add_argument(
        "--worker-model", default="haiku",
        help="Worker Modell: haiku, sonnet, opus (default: haiku)"
    )
    parser.add_argument(
        "--timeout", type=int, default=300,
        help="Timeout pro Aufruf in Sekunden (default: 300)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Nur Konfiguration anzeigen"
    )

    args = parser.parse_args()

    if not args.task:
        parser.print_help()
        print("\nBeispiel: python -m tools.schwarm.hierarchy \"Erstelle eine API-Dokumentation\" --workers 4")
        return 1

    pattern = HierarchyPattern(
        task=args.task,
        num_workers=args.workers,
        boss_model=args.boss_model,
        worker_model=args.worker_model,
        timeout=args.timeout,
    )

    result = pattern.run(dry_run=args.dry_run)
    return 0 if result.get("success") or result.get("dry_run") else 1


if __name__ == "__main__":
    sys.exit(main())
