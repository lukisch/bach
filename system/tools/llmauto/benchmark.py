#!/usr/bin/env python3
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
"""
import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Sicherstellen dass das Paket importierbar ist
PACKAGE_DIR = Path(__file__).resolve().parent
_parent = str(PACKAGE_DIR.parent)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from llmauto.core.runner import ClaudeRunner


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
            {
                "name": "feature_design",
                "prompt": (
                    "Entwirf ein Plugin-System fuer eine CLI-Anwendung in Python. "
                    "Anforderungen: (1) Plugins als separate .py Dateien, "
                    "(2) Automatische Erkennung im plugins/ Ordner, "
                    "(3) Definiertes Interface (name, version, execute), "
                    "(4) Fehlertoleranz bei defekten Plugins. "
                    "Zeige die Implementierung mit Beispiel-Plugin."
                ),
            },
            {
                "name": "test_generation",
                "prompt": (
                    "Schreibe umfassende Unit-Tests (pytest) fuer diese Funktion:\n\n"
                    "```python\n"
                    "def parse_duration(s: str) -> int:\n"
                    "    \"\"\"Parst Dauer-Strings wie '2h30m', '45s', '1d12h' in Sekunden.\"\"\"\n"
                    "    import re\n"
                    "    units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}\n"
                    "    total = 0\n"
                    "    for match in re.finditer(r'(\\\\d+)([dhms])', s.lower()):\n"
                    "        value, unit = int(match.group(1)), match.group(2)\n"
                    "        total += value * units[unit]\n"
                    "    if total == 0:\n"
                    "        raise ValueError(f'Ungueltiges Format: {s}')\n"
                    "    return total\n"
                    "```\n"
                    "Teste Normalfaelle, Edge-Cases und Fehlerfaelle."
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
            {
                "name": "vergleich",
                "prompt": (
                    "Vergleiche SQLite, PostgreSQL und MongoDB fuer den Einsatz "
                    "in einer Desktop-Anwendung mit 10.000-100.000 Datensaetzen. "
                    "Bewerte: Setup-Komplexitaet, Performance, Skalierbarkeit, "
                    "Backup, Portabilitaet."
                ),
            },
            {
                "name": "trendanalyse",
                "prompt": (
                    "Analysiere die Entwicklung von Python Type Hints seit PEP 484. "
                    "Welche PEPs sind relevant? Wie hat sich das Tooling entwickelt "
                    "(mypy, pyright, beartype)? Was sind Best Practices fuer 2025+?"
                ),
            },
            {
                "name": "bewertung",
                "prompt": (
                    "Bewerte die Vor- und Nachteile von Monorepo vs. Multi-Repo "
                    "Ansaetzen fuer ein Team von 5-10 Entwicklern mit 3-5 Services. "
                    "Beruecksichtige: CI/CD, Dependency Management, Code Sharing, "
                    "Onboarding, Tooling."
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
                "name": "artikel_update",
                "prompt": (
                    "Aktualisiere diesen veralteten Abschnitt ueber Python Packaging:\n\n"
                    "'Verwende setup.py mit distutils fuer die Paketierung. "
                    "Erstelle eine MANIFEST.in und fuehre python setup.py sdist aus.'\n\n"
                    "Bringe ihn auf den Stand 2025 (pyproject.toml, build, twine)."
                ),
            },
            {
                "name": "suche_kompilation",
                "prompt": (
                    "Recherchiere und kompiliere eine Uebersicht der wichtigsten "
                    "Design Patterns in Python. Fuer jedes Pattern: "
                    "Name, Kategorie (Creational/Structural/Behavioral), "
                    "Kurzbeschreibung, Python-spezifische Implementierung."
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
            {
                "name": "qualitaet_review",
                "prompt": (
                    "Pruefe diesen Wiki-Artikel auf Qualitaet und Vollstaendigkeit:\n\n"
                    "# Git Branching\n\n"
                    "Git hat Branches. Man erstellt sie mit git branch name.\n"
                    "Dann wechselt man mit git checkout name.\n"
                    "Merge geht mit git merge.\n"
                    "Bei Konflikten muss man die Dateien editieren.\n\n"
                    "Gib konkretes Feedback und eine verbesserte Version."
                ),
            },
        ],
    },
    "code_review": {
        "label": "Code-Review (Spezialisiert)",
        "tasks": [
            {
                "name": "security",
                "prompt": (
                    "Fuehre ein Security-Review dieses Flask-Endpoints durch:\n\n"
                    "```python\n"
                    "@app.route('/search')\n"
                    "def search():\n"
                    "    query = request.args.get('q')\n"
                    "    sql = f\"SELECT * FROM products WHERE name LIKE '%{query}%'\"\n"
                    "    results = db.execute(sql).fetchall()\n"
                    "    return render_template_string(\n"
                    "        '<h1>Ergebnisse fuer: ' + query + '</h1>'\n"
                    "        + ''.join(f'<p>{r[1]}</p>' for r in results)\n"
                    "    )\n"
                    "```\n"
                    "Identifiziere alle Sicherheitsluecken und zeige Fixes."
                ),
            },
            {
                "name": "performance",
                "prompt": (
                    "Analysiere die Performance dieses Codes und optimiere ihn:\n\n"
                    "```python\n"
                    "def find_duplicates(items):\n"
                    "    duplicates = []\n"
                    "    for i in range(len(items)):\n"
                    "        for j in range(i + 1, len(items)):\n"
                    "            if items[i] == items[j] and items[i] not in duplicates:\n"
                    "                duplicates.append(items[i])\n"
                    "    return duplicates\n\n"
                    "def count_words(text):\n"
                    "    words = text.split()\n"
                    "    counts = {}\n"
                    "    for word in words:\n"
                    "        found = False\n"
                    "        for key in counts:\n"
                    "            if key.lower() == word.lower():\n"
                    "                counts[key] += 1\n"
                    "                found = True\n"
                    "        if not found:\n"
                    "            counts[word] = 1\n"
                    "    return counts\n"
                    "```"
                ),
            },
            {
                "name": "style",
                "prompt": (
                    "Pruefe diesen Code gegen PEP 8, PEP 257 und Python Best Practices:\n\n"
                    "```python\n"
                    "class myClass:\n"
                    "  def __init__(self,x,y,z):\n"
                    "    self.x=x;self.y=y;self.z=z\n"
                    "  def Calculate(self):\n"
                    "    if self.x>0:\n"
                    "      if self.y>0:\n"
                    "        if self.z>0:\n"
                    "          return self.x*self.y*self.z\n"
                    "        else:\n"
                    "          return -1\n"
                    "      else:\n"
                    "        return -1\n"
                    "    else:\n"
                    "      return -1\n"
                    "  def toString(self): return f'{self.x},{self.y},{self.z}'\n"
                    "```"
                ),
            },
            {
                "name": "architektur",
                "prompt": (
                    "Bewerte die Architektur dieser Anwendung:\n\n"
                    "```\n"
                    "app/\n"
                    "  main.py          # Flask app + alle Routes + DB + Auth + Email\n"
                    "  templates/       # Jinja2 Templates\n"
                    "  static/          # CSS/JS\n"
                    "  requirements.txt # flask, sqlalchemy, jwt, smtplib\n"
                    "```\n\n"
                    "main.py hat 2000 Zeilen. Schlage eine bessere Struktur vor "
                    "mit konkreten Schritten zur Migration."
                ),
            },
            {
                "name": "test_coverage",
                "prompt": (
                    "Analysiere diese Test-Suite und identifiziere fehlende Tests:\n\n"
                    "```python\n"
                    "# calculator.py\n"
                    "class Calculator:\n"
                    "    def add(self, a, b): return a + b\n"
                    "    def divide(self, a, b): return a / b\n"
                    "    def power(self, base, exp): return base ** exp\n"
                    "    def sqrt(self, n): return n ** 0.5\n"
                    "    def history(self): return self._log\n\n"
                    "# test_calculator.py\n"
                    "def test_add():\n"
                    "    c = Calculator()\n"
                    "    assert c.add(2, 3) == 5\n\n"
                    "def test_divide():\n"
                    "    c = Calculator()\n"
                    "    assert c.divide(10, 2) == 5\n"
                    "```\n"
                    "Welche Tests fehlen? Schreibe sie."
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
    fail_count = len(results) - success_count
    total_output = sum(r["output_length"] for r in results)

    print(f"\n  Gesamt:     {len(results)} Tasks")
    print(f"  Erfolg:     {success_count} | Fehler: {fail_count}")
    print(f"  Gesamtzeit: {total_duration:.1f}s")
    if results:
        avg_duration = total_duration / len(results)
        print(f"  Avg/Task:   {avg_duration:.1f}s (Wall-Time)")
    print(f"  Output:     {total_output:,} Zeichen gesamt")

    # Per-Category Breakdown
    categories = {}
    for r in results:
        cat = r.get("category", "unknown")
        if cat not in categories:
            categories[cat] = {"count": 0, "success": 0, "duration": 0, "output": 0}
        categories[cat]["count"] += 1
        if r["success"]:
            categories[cat]["success"] += 1
        categories[cat]["duration"] += r["duration_s"]
        categories[cat]["output"] += r["output_length"]

    if len(categories) > 1:
        print(f"\n  Per Kategorie:")
        for cat, stats in sorted(categories.items()):
            label = TASK_CATALOG.get(cat, {}).get("label", cat)
            avg = stats["duration"] / stats["count"] if stats["count"] else 0
            print(f"    {label}: {stats['success']}/{stats['count']} OK, "
                  f"avg {avg:.1f}s, {stats['output']:,} chars")


def print_comparison(seq_results, seq_duration, par_results, par_duration, max_workers):
    """Vergleich sequential vs. parallel."""
    print(f"\n{'='*70}")
    print("  VERGLEICH: Sequentiell vs. Parallel")
    print(f"{'='*70}")

    headers = ["Metrik", "Sequentiell", f"Parallel ({max_workers}W)", "Speedup"]
    rows = []

    seq_success = sum(1 for r in seq_results if r["success"])
    par_success = sum(1 for r in par_results if r["success"])
    seq_output = sum(r["output_length"] for r in seq_results)
    par_output = sum(r["output_length"] for r in par_results)

    speedup = seq_duration / par_duration if par_duration > 0 else 0

    rows.append(["Gesamtzeit", f"{seq_duration:.1f}s", f"{par_duration:.1f}s", f"{speedup:.2f}x"])
    rows.append(["Erfolgsrate", f"{seq_success}/{len(seq_results)}",
                  f"{par_success}/{len(par_results)}", "-"])
    rows.append(["Output gesamt", f"{seq_output:,}", f"{par_output:,}", "-"])

    if seq_results and par_results:
        seq_avg = seq_duration / len(seq_results)
        par_avg = par_duration / len(par_results)
        rows.append(["Avg Wall-Time/Task", f"{seq_avg:.1f}s", f"{par_avg:.1f}s",
                      f"{seq_avg / par_avg:.2f}x" if par_avg > 0 else "-"])

        # Summe der Einzelzeiten (CPU-Zeit)
        seq_sum = sum(r["duration_s"] for r in seq_results)
        par_sum = sum(r["duration_s"] for r in par_results)
        rows.append(["Summe Einzelzeiten", f"{seq_sum:.1f}s", f"{par_sum:.1f}s", "-"])

    print(_format_table(headers, rows))

    # Effizienz-Bewertung
    if max_workers > 0 and seq_duration > 0:
        efficiency = speedup / max_workers * 100
        saving = (1 - par_duration / seq_duration) * 100 if seq_duration > 0 else 0
        print(f"\n  Parallel-Effizienz: {efficiency:.0f}% (ideal: 100%)")
        print(f"  Zeitersparnis:     {seq_duration - par_duration:.0f}s ({saving:.0f}%)")


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
    parser.add_argument("--workers", type=int, default=3, help="Anzahl paralleler Worker (default: 3)")
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
        print("Ausfuehren mit: python benchmark.py --run [--parallel|--sequential|--compare]")
        return 0

    # Runner erstellen
    print(f"\nllmauto Benchmark")
    print(f"  Modell:     {args.model}")
    print(f"  Tasks:      {len(tasks)}")
    print(f"  Worker:     {args.workers}")
    print(f"  Timeout:    {args.timeout}s")
    print(f"  Kategorien: {', '.join(set(t['category'] for t in tasks))}")
    print()

    runner = ClaudeRunner(
        model=args.model,
        timeout=args.timeout,
        cwd=str(PACKAGE_DIR.parent.parent),  # system/
    )

    all_results = []
    seq_results = seq_duration = par_results = par_duration = None

    # Default: --compare wenn --run ohne spezifischen Modus
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

    if args.compare and seq_results and par_results:
        print_comparison(seq_results, seq_duration, par_results, par_duration, args.workers)

    # JSON-Export
    if args.export and all_results:
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "model": args.model,
            "max_workers": args.workers,
            "results": [{k: v for k, v in r.items() if k != "prompt"} for r in all_results],
        }
        if seq_duration is not None:
            export_data["sequential_total_s"] = seq_duration
        if par_duration is not None:
            export_data["parallel_total_s"] = par_duration

        export_path = Path(args.export)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        export_path.write_text(json.dumps(export_data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nErgebnisse exportiert: {export_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
