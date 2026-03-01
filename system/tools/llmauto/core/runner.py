"""
llmauto.core.runner -- Claude CLI Wrapper
==========================================
Zentraler Baustein: Startet Claude-Prozesse mit konfigurierbaren Parametern.
Handhabt Environment, Fallback, Timeout, Output-Capture.
"""
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime


class ClaudeRunner:
    """Wrapper um die Claude CLI fuer automatisierte Aufrufe."""

    def __init__(self, model="claude-sonnet-4-6", fallback_model=None,
                 permission_mode="dontAsk", allowed_tools=None, timeout=1800,
                 cwd=None):
        self.model = model
        self.fallback_model = fallback_model
        self.permission_mode = permission_mode
        self.allowed_tools = allowed_tools or ["Read", "Edit", "Write", "Bash", "Glob", "Grep"]
        self.timeout = timeout
        self.cwd = cwd

    def _build_env(self):
        """Environment vorbereiten: CLAUDECODE entfernen, Encoding setzen."""
        env = os.environ.copy()
        env.pop("CLAUDECODE", None)
        env["PYTHONIOENCODING"] = "utf-8"
        return env

    def _build_cmd(self, prompt, **overrides):
        """Claude CLI Kommando zusammenbauen."""
        model = overrides.get("model", self.model)
        continue_conv = overrides.get("continue_conversation", False)

        cmd = ["claude"]
        if continue_conv:
            cmd.append("--continue")
        cmd.extend([
            "--model", model,
            "-p", prompt,
            "--permission-mode", self.permission_mode,
            "--allowedTools", ",".join(self.allowed_tools),
        ])
        fallback = overrides.get("fallback_model", self.fallback_model)
        if fallback:
            cmd.extend(["--fallback-model", fallback])
        return cmd

    def run(self, prompt, **overrides):
        """
        Fuehrt einen Claude-Aufruf aus.

        Returns:
            dict mit keys: success, output, stderr, returncode, duration_s
        """
        cmd = self._build_cmd(prompt, **overrides)
        env = self._build_env()
        cwd = overrides.get("cwd", self.cwd)
        timeout = overrides.get("timeout", self.timeout)

        start = datetime.now()
        try:
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                cwd=str(cwd) if cwd else None
            )
            duration = (datetime.now() - start).total_seconds()
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip(),
                "stderr": result.stderr.strip() if result.stderr else "",
                "returncode": result.returncode,
                "duration_s": duration,
                "model": overrides.get("model", self.model),
            }

        except subprocess.TimeoutExpired:
            duration = (datetime.now() - start).total_seconds()
            return {
                "success": False,
                "output": "",
                "stderr": f"TIMEOUT nach {timeout}s",
                "returncode": -1,
                "duration_s": duration,
                "model": overrides.get("model", self.model),
            }

        except FileNotFoundError:
            return {
                "success": False,
                "output": "",
                "stderr": "claude CLI nicht gefunden. Ist Claude Code installiert?",
                "returncode": -2,
                "duration_s": 0,
                "model": overrides.get("model", self.model),
            }

        except Exception as e:
            duration = (datetime.now() - start).total_seconds()
            return {
                "success": False,
                "output": "",
                "stderr": str(e),
                "returncode": -3,
                "duration_s": duration,
                "model": overrides.get("model", self.model),
            }

    def pipe(self, prompt, **overrides):
        """Kurzform: Prompt rein, Text raus. Wirft Exception bei Fehler."""
        result = self.run(prompt, **overrides)
        if not result["success"]:
            raise RuntimeError(f"Claude Fehler (rc={result['returncode']}): {result['stderr']}")
        return result["output"]
