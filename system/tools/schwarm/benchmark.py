#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
llmauto Benchmark -- Vergleich sequentiell vs. parallel
========================================================
Misst Geschwindigkeit und Erfolgsrate von LLM-Schwarm-Ausfuehrungen.

Usage:
    python benchmark.py                   Alle Benchmarks (dry-run)
    python benchmark.py --run             Benchmarks ausfuehren
    python benchmark.py --parallel        Nur parallele Ausfuehrung
    python benchmark.py --sequential      Nur sequentielle Ausfuehrung
    python benchmark.py --compare         Vergleich parallel vs. sequentiell
    python benchmark.py --dry-run         Nur Prompts anzeigen (Standard)
    python benchmark.py --workers N       Anzahl paralleler Worker (default: 3)
    python benchmark.py --category CAT    Nur bestimmte Kategorie ausfuehren
    python benchmark.py --export FILE     Ergebnisse als JSON exportieren

Portiert: BACH v3.8.0-SUGAR (system/tools/schwarm/)
"""
import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Import aus schwarm-Paket
from .runner import ClaudeRunner, log_schwarm_run


# ============================================================
# Task-Katalog: Kategorien mit Benchmark-Aufgaben
# ============================================================

TASK_CATALOG = {
    "software_dev": {
        "label": "Software-Entwicklung",
        "tasks": [
            {
                "name": "code_review",
                "prompt": (
                    "Analysiere die folgende Python-Funktion auf Fehler, Style-Probleme und "
                    "Verbesserungsmoeglichkeiten. Gib eine strukturierte Bewertung:\n\n"
                    "```python\n"
                    "def process_data(items, filter=None, sort_key=None):\n"
                    "    result = []\n"
                    "    for i in range(len(items)):\n"
                    "        if filter and filter(items[i]):\n"
                    "            result.append(items[i])\n"
                    "        elif not filter:\n"
                    "            result.append(items[i])\n"
                    "    if sort_key:\n"
                    "        result.sort(key=sort_key)\n"
                    "    return result\n"
                    "```"
                ),
            },
            {
                "name": "refactoring",
                "prompt": (
                    "Refaktoriere diese Klasse nach SOLID-Prinzipien. "
                    "Erklaere jede Aenderung:\n\n"
                    "```python\n"
                    "class UserManager:\n"
                    "    def __init__(self):\n"
                    "        self.users = []\n"
                    "    def add_user(self, name, email, role):\n"
                    "        self.users.append({'name': name, 'email': email, 'role': role})\n"
                    "    def remove_user(self, email):\n"
                    "        self.users = [u for u in self.users if u['email'] != email]\n"
                    "    def send_email(self, email, subject, body):\n"
                    "        import smtplib\n"
                    "        server = smtplib.SMTP('localhost')\n"
                    "        server.sendmail('admin@example.com', email, f'{subject}\\n{body}')\n"
                    "    def generate_report(self):\n"
                    "        report = 'Users:\\n'\n"
                    "        for u in self.users:\n"
                    "            report += f\"{u['name']} ({u['role']})\\n\"\n"
                    "        return report\n"
                    "```"
                ),
            },
            {
                "name": "bug_fix",
                "prompt": (
                    "Finde und erklaere alle Bugs in diesem Code:\n\n"
                    "```python\n"
                    "import threading\n\n"
                    "counter = 0\n"
                    "lock = threading.Lock()\n\n"
                    "def increment():\n"
                    "    global counter\n"
                    "    for _ in range(1000):\n"
                    "        counter += 1\n\n"
                    "def safe_divide(a, b):\n"
                    "    try:\n"
                    "        return a / b\n"
                    "    except:\n"
                    "        return 0\n\n"
                    "def read_config(path):\n"
                    "    f = open(path)\n"
                    "    data = f.read()\n"
                    "    config = eval(data)\n"
                    "    return config\n"
                    "```"
                ),
            },
        ],
    },
    "research": {
        "label": "Forschung & Analyse",
        "tasks": [
            {
                "name": "literatur",
                "prompt": (
                    "Erstelle eine strukturierte Zusammenfassung der wichtigsten "
                    "Konzepte und Unterschiede zwischen REST, GraphQL und gRPC APIs. "
                    "Vergleiche: Architektur, Performance, Typsicherheit, Einsatzgebiete."
                ),
            },
            {
                "name": "konzeptanalyse",
                "prompt": (
                    "Analysiere das CAP-Theorem in verteilten Systemen. "
                    "Erklaere: (1) Die drei Eigenschaften, "
                    "(2) Warum nur 2 von 3 gleichzeitig moeglich sind, "
                    "(3) Praktische Beispiele fuer CP, AP und CA Systeme, "
                    "(4) Wie moderne Systeme den Trade-off handhaben."
                ),
            },
        ],
    },
    "wiki": {
        "label": "Wiki & Dokumentation",
        "tasks": [
            {
                "name": "artikel_schreiben",
                "prompt": (
                    "Schreibe einen technischen Wiki-Artikel ueber 'asyncio in Python'. "
                    "Struktur: Einfuehrung, Event Loop, Coroutines, Tasks, "
                    "Synchronisierung, Fehlerbehandlung, Best Practices. "
                    "Mit Code-Beispielen."
                ),
            },
            {
                "name": "kategorisierung",
                "prompt": (
                    "Kategorisiere die folgenden Python-Bibliotheken nach Einsatzgebiet "
                    "und empfehle je Kategorie die beste Option fuer 2025:\n"
                    "requests, httpx, aiohttp, flask, fastapi, django, "
                    "sqlalchemy, peewee, tortoise-orm, pydantic, attrs, dataclasses, "
                    "click, typer, argparse, rich, textual, pytest, unittest, hypothesis"
                ),
            },
        ],
    },
}


# ============================================================
# Benchmark-Runner
# ============================================================

def _get_all_tasks(categories=None):
    """Sammelt alle Tasks, optional gefiltert nach Kategorien."""
    tasks = []
    for cat_key, cat in TASK_CATALOG.items():
        if categories and cat_key not in categories:
            continue
        for task in cat["tasks"]:
            tasks.append({
                "category": cat_key,
                "category_label": cat["label"],
                **task,
            })
    return tasks


def _format_table(headers, rows, col_widths=None):
    """Formatiert eine ASCII-Tabelle."""
    if not col_widths:
        col_widths = []
        for i, h in enumerate(headers):
            max_w = len(h)
            for row in rows:
                val = str(row[i]) if i < len(row) else ""
                max_w = max(max_w, len(val))
            col_widths.append(min(max_w, 40))

    def _fmt_row(values):
        parts = []
        for i, v in enumerate(values):
            s = str(v)[:col_widths[i]]
            parts.append(s.ljust(col_widths[i]))
        return "| " + " | ".join(parts) + " |"

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    lines = [sep, _fmt_row(headers), sep]
    for row in rows:
        lines.append(_fmt_row(row))
    lines.append(sep)
    return "\n".join(lines)


def run_benchmark(tasks, runner, mode="sequential", max_workers=3):
    """Fuehrt Benchmark-Tasks aus.

    Args:
        tasks: Liste von Task-Dicts {name, prompt, category, ...}
        runner: ClaudeRunner-Instanz
        mode: "sequential" oder "parallel"
        max_workers: Anzahl paralleler Worker (nur bei mode="parallel")

    Returns:
        Tuple (results_list, total_wall_time_s)
    """
    results = []

    if mode == "parallel":
        prompts = [t["prompt"] for t in tasks]
        print(f"  Starte {len(tasks)} Tasks mit {max_workers} Workern...")

        start = time.time()
        raw_results = runner.run_parallel(prompts, max_workers=max_workers)
        total_duration = time.time() - start

        for task, result in zip(tasks, raw_results):
            results.append({
                "name": task["name"],
                "category": task.get("category", ""),
                "category_label": task.get("category_label", ""),
                "mode": "parallel",
                "success": result["success"],
                "duration_s": result["duration_s"],
                "output_length": len(result["output"]),
                "model": result["model"],
                "returncode": result["returncode"],
                "tokens_in": result.get("tokens_in", 0),
                "tokens_out": result.get("tokens_out", 0),
                "cost_usd": result.get("cost_usd", 0.0),
            })
            status = "OK" if result["success"] else "FEHLER"
            print(f"  [{task.get('category', '')}] {task['name']}: {status} ({result['duration_s']:.0f}s)")

    else:  # sequential
        total_start = time.time()
        for task in tasks:
            print(f"  [{task.get('category', '')}] {task['name']}...", end=" ", flush=True)
            result = runner.run(task["prompt"])
            duration = result["duration_s"]
            results.append({
                "name": task["name"],
                "category": task.get("category", ""),
                "category_label": task.get("category_label", ""),
                "mode": "sequential",
                "success": result["success"],
                "duration_s": duration,
                "output_length": len(result["output"]),
                "model": result["model"],
                "returncode": result["returncode"],
                "tokens_in": result.get("tokens_in", 0),
                "tokens_out": result.get("tokens_out", 0),
                "cost_usd": result.get("cost_usd", 0.0),
            })
            status = "OK" if result["success"] else "FEHLER"
            print(f"{status} ({duration:.0f}s, {len(result['output'])} chars)")

        total_duration = time.time() - total_start

    return results, total_duration


def print_results(results, total_duration, mode_label):
    """Gibt Ergebnistabelle aus."""
    print(f"\n{'='*70}")
    print(f"  Ergebnisse: {mode_label}")
    print(f"{'='*70}")

    headers = ["Kategorie", "Task", "Status", "Dauer (s)", "Output (chars)", "Modell"]
    rows = []
    for r in results:
        status = "OK" if r["success"] else "FEHLER"
        rows.append([
            r.get("category", ""),
            r["name"],
            status,
            f"{r['duration_s']:.1f}",
            str(r["output_length"]),
            r["model"],
        ])

    print(_format_table(headers, rows))

    # Zusammenfassung
    success_count = sum(1 for r in results if r["success"])
    total_output = sum(r["output_length"] for r in results)
    total_cost = sum(r.get("cost_usd", 0) for r in results)

    print(f"\n  Gesamt:     {len(results)} Tasks")
    print(f"  Erfolg:     {success_count} | Fehler: {len(results) - success_count}")
    print(f"  Gesamtzeit: {total_duration:.1f}s")
    print(f"  Kosten:     ${total_cost:.4f}")
    if results:
        avg_duration = total_duration / len(results)
        print(f"  Avg/Task:   {avg_duration:.1f}s (Wall-Time)")
    print(f"  Output:     {total_output:,} Zeichen gesamt")


def main():
    parser = argparse.ArgumentParser(
        prog="benchmark",
        description="llmauto Benchmark -- Vergleich sequentiell vs. parallel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--run", action="store_true", help="Benchmarks tatsaechlich ausfuehren")
    parser.add_argument("--parallel", action="store_true", help="Nur parallele Ausfuehrung")
    parser.add_argument("--sequential", action="store_true", help="Nur sequentielle Ausfuehrung")
    parser.add_argument("--compare", action="store_true", help="Beide Modi vergleichen")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Nur Tasks anzeigen (Standard)")
    parser.add_argument("--workers", type=int, default=0,
                        help="Anzahl paralleler Worker (default: auto, basierend auf Task-Anzahl)")
    parser.add_argument("--max-workers", type=int, default=0,
                        help="Obere Schranke fuer dynamische Worker-Anzahl (default: min(CPU, 8))")
    parser.add_argument("--category", "-c", choices=list(TASK_CATALOG.keys()),
                        help="Nur eine Kategorie benchmarken")
    parser.add_argument("--model", "-m", default="claude-haiku-4-5-20251001",
                        help="Modell (default: haiku fuer guenstige Benchmarks)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="Timeout pro Task in Sekunden (default: 300)")
    parser.add_argument("--export", help="Ergebnisse als JSON exportieren")

    args = parser.parse_args()

    # --run/--parallel/--sequential/--compare deaktiviert dry-run
    if args.run or args.parallel or args.sequential or args.compare:
        args.dry_run = False

    # Kategorien filtern
    categories = [args.category] if args.category else None
    tasks = _get_all_tasks(categories)

    if not tasks:
        print(f"Keine Tasks gefunden fuer Kategorie '{args.category}'.")
        print(f"Verfuegbar: {', '.join(TASK_CATALOG.keys())}")
        return 1

    # Dry-Run: Nur Tasks anzeigen
    if args.dry_run:
        print("BENCHMARK TASKS (dry-run)")
        print("=" * 50)
        cat_groups = {}
        for t in tasks:
            cat = t["category"]
            if cat not in cat_groups:
                cat_groups[cat] = []
            cat_groups[cat].append(t)

        for cat, cat_tasks in cat_groups.items():
            label = TASK_CATALOG[cat]["label"]
            print(f"\n{label} ({len(cat_tasks)} Tasks):")
            for t in cat_tasks:
                print(f"  - {t['name']}: {t['prompt'][:70]}...")

        print(f"\nGesamt: {len(tasks)} Tasks")
        print("Ausfuehren mit: bach schwarm benchmark --run [--parallel|--sequential|--compare]")
        return 0

    # Dynamische Worker-Berechnung
    if args.workers <= 0:
        try:
            from .runner import calculate_dynamic_workers
            args.workers = calculate_dynamic_workers(len(tasks), max_workers=args.max_workers)
        except ImportError:
            cap = args.max_workers if args.max_workers > 0 else 8
            args.workers = min(max(2, len(tasks) // 2), cap)
        print(f"[BENCHMARK] Worker-Anzahl automatisch berechnet: {args.workers} (basierend auf {len(tasks)} Tasks)")

    # Runner erstellen
    print(f"\nSchwarm Benchmark")
    print(f"  Modell:     {args.model}")
    print(f"  Tasks:      {len(tasks)}")
    print(f"  Worker:     {args.workers}")
    print(f"  Timeout:    {args.timeout}s")
    print()

    runner = ClaudeRunner(
        model=args.model,
        timeout=args.timeout,
    )

    all_results = []

    if args.run and not args.parallel and not args.sequential and not args.compare:
        args.compare = True

    if args.sequential or args.compare:
        print("--- Sequentieller Durchlauf ---")
        seq_results, seq_duration = run_benchmark(tasks, runner, mode="sequential")
        print_results(seq_results, seq_duration, "Sequentiell")
        all_results.extend(seq_results)

    if args.parallel or args.compare:
        print("\n--- Paralleler Durchlauf ---")
        par_results, par_duration = run_benchmark(
            tasks, runner, mode="parallel", max_workers=args.workers
        )
        print_results(par_results, par_duration, f"Parallel ({args.workers} Worker)")
        all_results.extend(par_results)

    # Kosten-Tracking
    if all_results:
        total_tokens_in = sum(r.get("tokens_in", 0) for r in all_results)
        total_tokens_out = sum(r.get("tokens_out", 0) for r in all_results)
        total_cost = sum(r.get("cost_usd", 0) for r in all_results)
        total_duration = sum(r.get("duration_s", 0) for r in all_results)
        try:
            log_schwarm_run(
                pattern="benchmark",
                task=f"benchmark {len(all_results)} tasks",
                tokens_in=total_tokens_in,
                tokens_out=total_tokens_out,
                cost_usd=total_cost,
                workers=args.workers,
                duration_ms=int(total_duration * 1000),
                status="completed",
                result_summary=f"{sum(1 for r in all_results if r['success'])}/{len(all_results)} OK",
            )
        except Exception:
            pass

    # JSON-Export
    if args.export and all_results:
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "model": args.model,
            "max_workers": args.workers,
            "results": all_results,
        }
        export_path = Path(args.export)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        export_path.write_text(json.dumps(export_data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nErgebnisse exportiert: {export_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
