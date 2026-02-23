# SPDX-License-Identifier: MIT
"""
Chain Handler - Ausfuehrung von verketteten Tool-Befehlen
=========================================================

Erlaubt das Definieren und Ausfuehren von "Toolchains" (Skripten),
die nacheinander BACH-Befehle ausfuehren ohne LLM-Interaktion.

Befehle:
  bach chain list                Alle Chains anzeigen
  bach chain run <id>            Chain ausfuehren
  bach chain add "JSON"          Neue Chain erstellen
  bach chain show <id>           Details ansehen
  bach chain log <id>            Logs einer Chain

Ref: SYS_002
"""
import sqlite3
import json
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from .base import BaseHandler

class ChainHandler(BaseHandler):
    """Handler fuer Toolchains"""

    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.db_path = base_path / "data" / "bach.db"

    @property
    def profile_name(self) -> str:
        return "chain"

    @property
    def target_file(self) -> Path:
        return self.db_path

    def get_operations(self) -> dict:
        return {
            "list": "Alle Chains auflisten",
            "run": "Chain ausfuehren",
            "add": "Neue Chain erstellen",
            "show": "Details einer Chain",
            "delete": "Chain loeschen",
            "log": "Logs anzeigen"
        }

    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if operation == "list":
            return self._list()
        elif operation == "run":
            if not args: return False, "ID benoetigt: bach chain run <id>"
            return self._run(args[0], dry_run)
        elif operation == "add":
            return self._add(args)
        elif operation == "show":
            if not args: return False, "ID benoetigt: bach chain show <id>"
            return self._show(args[0])
        elif operation == "delete":
            if not args: return False, "ID benoetigt: bach chain delete <id>"
            return self._delete(args[0])
        elif operation == "log":
             if not args: return False, "ID benoetigt: bach chain log <id>"
             return self._log(args[0])
        else:
            return False, f"Unbekannte Operation: {operation}"

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _list(self) -> tuple:
        conn = self._get_conn()
        try:
            rows = conn.execute("SELECT * FROM toolchains ORDER BY id").fetchall()
            if not rows:
                return True, "Keine Toolchains definiert."
            
            lines = ["TOOLCHAINS", "="*40]
            lines.append(f"{'ID':<4} {'Name':<30} {'Trigger':<10} {'Active':<6} {'Last Run'}")
            lines.append("-" * 70)
            
            for r in rows:
                active = "Yes" if r['is_active'] else "No"
                last = r['last_run'] if r['last_run'] else "Never"
                lines.append(f"{r['id']:<4} {r['name']:<30} {r['trigger_type']:<10} {active:<6} {last}")
                
            return True, "\n".join(lines)
        finally:
            conn.close()

    def _run(self, chain_id: str, dry_run: bool) -> tuple:
        conn = self._get_conn()
        try:
            # Chain laden
            chain = conn.execute("SELECT * FROM toolchains WHERE id = ?", (chain_id,)).fetchone()
            if not chain:
                return False, f"Chain {chain_id} nicht gefunden."

            try:
                steps = json.loads(chain['steps_json'])
            except json.JSONDecodeError:
                return False, "Fehlerhaftes JSON in steps_definition."

            triggered_by = "manual"  # Default

            if dry_run:
                msg = [f"[DRY-RUN] Chain '{chain['name']}' ({len(steps)} Steps):"]
                self._dry_run_recursive(steps, msg, indent=1)
                return True, "\n".join(msg)

            # Ausfuehrung
            start_time = time.time()
            started_at_iso = datetime.now().isoformat()
            logs = []
            success = True
            
            print(f"Starte Chain '{chain['name']}'...")
            
            # Recursive execution needed for blocks
            steps_completed, failure_occurred, final_output_log, final_error_log = self._execute_steps(steps, logs)
            
            if failure_occurred:
                success = False

            duration = time.time() - start_time
            finished_at_iso = datetime.now().isoformat()
            status = 'success' if success else 'failed'
            
            # Run loggen (Updated Schema)
            # Schema: chain_id, status, log, duration_seconds, finished_at, steps_completed, steps_total, output, error, triggered_by
            full_log = "\n".join(logs)
            conn.execute("""
                INSERT INTO toolchain_runs (
                    chain_id, status, log, duration_seconds, started_at, finished_at,
                    steps_completed, steps_total, output, error, triggered_by
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chain_id, status, full_log, duration, started_at_iso, finished_at_iso,
                steps_completed, len(steps), final_output_log, final_error_log, triggered_by
            ))
            
            # Last Run update
            conn.execute("UPDATE toolchains SET last_run = CURRENT_TIMESTAMP WHERE id = ?", (chain_id,))
            conn.commit()
            
            return True, f"Chain beendet ({status}, {duration:.2f}s).\nDetails: bach chain log {chain_id}"
            
        finally:
            conn.close()

    def _dry_run_recursive(self, steps, msg_list, indent):
        for i, step in enumerate(steps):
            prefix = "  " * indent
            if 'parallel' in step and step['parallel']:
                msg_list.append(f"{prefix}{i+1}. [PARALLEL BLOCK]")
                substeps = step.get('tools', [])
                for sub in substeps:
                     msg_list.append(f"{prefix}  - {sub.get('tool')} {sub.get('args')}")
            else:
                msg_list.append(f"{prefix}{i+1}. {step.get('tool')} {step.get('args')}")

    def _execute_steps(self, steps: list, logs: list) -> tuple:
        """
        Recursive execution engine.
        Returns: (steps_completed_count, failure_occurred, output_str, error_str)
        """
        import concurrent.futures
        
        steps_completed = 0
        failure_occurred = False
        outputs = []
        errors = []
        
        for i, step in enumerate(steps):
            # 1. PARALLEL EXECUTION
            if 'parallel' in step and step['parallel'] is True:
                subtools = step.get('tools', [])
                log_entry = f"Step {i+1}: Start Parallel Block ({len(subtools)} Tasks)"
                print(f"  > [PARALLEL] {len(subtools)} Tasks...")
                logs.append(log_entry)
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = []
                    for subt in subtools:
                        futures.append(executor.submit(self._run_single_tool, subt))
                    
                    for future in concurrent.futures.as_completed(futures):
                        res = future.result()
                        # Merge parallel logs
                        logs.append(f"    [THREAD] {res['tool']}: {'SUCCESS' if res['success'] else 'FAILED'}\n{res['log']}")
                        if res['output']: outputs.append(res['output'])
                        if res['error']: errors.append(res['error'])
                        if not res['success']:
                            failure_occurred = True
                
                steps_completed += 1 # Count block as 1 step
                
            # 2. SEQUENTIAL EXECUTION
            else:
                res = self._run_single_tool(step)
                
                step_log = f"Step {i+1}: {step.get('tool')} {step.get('args')}\n"
                logs.append(step_log + res['log'])
                if res['output']: outputs.append(res['output'])
                if res['error']: errors.append(res['error'])
                
                if res['success']:
                    steps_completed += 1
                else:
                    failure_occurred = True
                    # ON FAILURE HANDLING
                    action = "abort" # default
                    if 'on_failure' in step:
                        on_fail = step['on_failure']
                        action = on_fail.get('action', 'abort')
                        msg = on_fail.get('message', 'Fehler aufgetreten')
                        logs.append(f"  [ON_FAILURE] {msg} -> Action: {action}")
                        print(f"    [ON_FAILURE] {msg} -> {action}")
                    
                    if action == 'abort':
                        logs.append("  [ABORT] Chain abgebrochen.")
                        break
                    elif action == 'continue':
                        logs.append("  [CONTINUE] Fehler ignoriert.")
                        failure_occurred = False # Reset flag if we continue explicitly? Or keep it? Let's keep it to mark run as "warning" ideally.
                        # But for now, simple boolean logic: if we continue, we proceed.
                    # 'retry' not implemented yet simple
                    
        final_out = "\n".join(outputs)
        final_err = "\n".join(errors)
        return steps_completed, failure_occurred, final_out, final_err

    def _run_single_tool(self, step_def: dict) -> dict:
        """
        Runs a single tool command and returns dict with results.
        """
        tool = step_def.get('tool')
        args = step_def.get('args', [])
        
        # Command build
        cmd = [sys.executable, "bach.py", tool] + [str(a) for a in args]
        
        print(f"  > {tool} {' '.join(str(x) for x in args)}")
        
        start = time.time()
        res = {
            "tool": tool,
            "success": False,
            "log": "",
            "output": "",
            "error": ""
        }
        
        try:
            proc = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                cwd=str(self.base_path)
            )
            
            duration = time.time() - start
            res['output'] = proc.stdout
            res['error'] = proc.stderr
            
            if proc.returncode == 0:
                res['success'] = True
                res['log'] = f"[OK] ({duration:.2f}s) {proc.stdout[:200]}..."
            else:
                res['success'] = False
                res['log'] = f"[FAILED] ({duration:.2f}s) Code {proc.returncode}\nStderr: {proc.stderr}"
                
        except Exception as e:
            res['success'] = False
            res['error'] = str(e)
            res['log'] = f"[EXCEPTION] {e}"
            
        return res

    def _add(self, args: list) -> tuple:
        # Erwartet JSON-String als Argument oder interaktives Bauen (vereinfacht: Name + JSON)
        # Usage: bach chain add "Name" --steps '[{"tool":"scan","args":["--mode","quick"]}]'
        
        if len(args) < 1:
            return False, 'Usage: bach chain add "Name" --steps \'[...]\' [--trigger manual]'
            
        name = args[0]
        steps_json = "[]"
        trigger = "manual"
        
        # Argument parsing manually
        for i, arg in enumerate(args):
            if arg == "--steps" and i+1 < len(args):
                steps_json = args[i+1]
            elif arg == "--trigger" and i+1 < len(args):
                trigger = args[i+1]

        # Validierung
        try:
            json.loads(steps_json)
        except:
             return False, "Ungueltiges JSON fuer Steps."

        conn = self._get_conn()
        try:
            conn.execute("""
                INSERT INTO toolchains (name, steps_json, trigger_type)
                VALUES (?, ?, ?)
            """, (name, steps_json, trigger))
            conn.commit()
            return True, f"Chain '{name}' erstellt."
        finally:
            conn.close()

    def _show(self, chain_id: str) -> tuple:
        conn = self._get_conn()
        try:
            chain = conn.execute("SELECT * FROM toolchains WHERE id = ?", (chain_id,)).fetchone()
            if not chain: return False, "Nicht gefunden."
            
            lines = [
                f"CHAIN: {chain['name']} (ID: {chain['id']})",
                f"Trigger: {chain['trigger_type']} {chain['trigger_value'] or ''}",
                f"Active: {chain['is_active']}",
                f"Last Run: {chain['last_run']}",
                "",
                "STEPS:"
            ]
            steps = json.loads(chain['steps_json'])
            for i, s in enumerate(steps):
                if 'parallel' in s and s['parallel']:
                    subtools = s.get('tools', [])
                    lines.append(f"  {i+1}. [PARALLEL BLOCK] ({len(subtools)} tasks)")
                    for sub in subtools:
                        lines.append(f"     - {sub.get('tool')} {sub.get('args')}")
                else:
                    lines.append(f"  {i+1}. {s.get('tool')} {s.get('args')}")
                
            return True, "\n".join(lines)
        finally:
            conn.close()

    def _delete(self, chain_id: str) -> tuple:
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM toolchains WHERE id = ?", (chain_id,))
            conn.commit()
            return True, f"Chain {chain_id} geloescht."
        finally:
            conn.close()

    def _log(self, chain_id: str) -> tuple:
         # Zeige letzten Run
        conn = self._get_conn()
        try:
            run = conn.execute("SELECT * FROM toolchain_runs WHERE chain_id = ? ORDER BY id DESC LIMIT 1", (chain_id,)).fetchone()
            if not run: return False, "Keine Logs gefunden."
            
            return True, f"LAST RUN ({run['started_at']}) - {run['status']}\nDuration: {run['duration_seconds']:.2f}s\n\nLOG:\n{run['log']}"
        finally:
            conn.close()
