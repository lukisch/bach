# SPDX-License-Identifier: MIT
"""
Setup Handler - System-Konfiguration und Installationshilfe
============================================================

bach setup mcp              MCP-Server global installieren und Claude Code konfigurieren
bach setup check             Pruefe ob alle Abhaengigkeiten konfiguriert sind
bach setup secrets           Secrets-Datei initialisieren / synchen

Teil von PEANUT Release: MCP-Server aus Repo entfernt, stattdessen via npm installieren.
"""
import json
import subprocess
import shutil
from pathlib import Path
from .base import BaseHandler


class SetupHandler(BaseHandler):
    """Handler fuer System-Setup und Konfiguration."""

    def __init__(self, base_path: Path):
        super().__init__(base_path)

    @property
    def profile_name(self) -> str:
        return "setup"

    @property
    def target_file(self) -> Path:
        return self.base_path / "hub" / "setup.py"

    def get_operations(self) -> dict:
        return {
            "mcp": "MCP-Server global installieren und Claude Code konfigurieren",
            "check": "Pruefe ob alle Abhaengigkeiten konfiguriert sind",
            "secrets": "Secrets-Datei initialisieren / synchen",
        }

    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if operation == "mcp":
            return self._setup_mcp(dry_run)
        elif operation == "check":
            return self._check()
        elif operation == "secrets":
            return self._setup_secrets()
        elif operation is None or operation == "":
            return self._check()
        else:
            ops = ", ".join(self.get_operations().keys())
            return False, f"Unbekannte Operation: {operation}\n\nVerfuegbar: {ops}"

    def _setup_mcp(self, dry_run: bool = False) -> tuple:
        """Installiert MCP-Server via npm und konfiguriert Claude Code."""
        results = []
        errors = []

        # 1. Pruefen ob npm verfuegbar ist
        npm_path = shutil.which("npm")
        if not npm_path:
            return False, (
                "npm nicht gefunden. Bitte Node.js installieren:\n"
                "  https://nodejs.org/\n"
                "Nach der Installation Terminal neu starten und erneut ausfuehren."
            )

        # 2. MCP-Server installieren
        packages = [
            "bach-codecommander-mcp",
            "bach-filecommander-mcp",
        ]

        results.append("=== MCP-Server Installation ===\n")

        for pkg in packages:
            if dry_run:
                results.append(f"  [DRY-RUN] npm install -g {pkg}")
                continue

            results.append(f"  Installiere {pkg}...")
            try:
                proc = subprocess.run(
                    ["npm", "install", "-g", pkg],
                    capture_output=True, text=True, timeout=120
                )
                if proc.returncode == 0:
                    results.append(f"  [OK] {pkg} installiert")
                else:
                    errors.append(f"  [FEHLER] {pkg}: {proc.stderr.strip()}")
            except subprocess.TimeoutExpired:
                errors.append(f"  [TIMEOUT] {pkg}: Installation dauerte zu lange")
            except Exception as e:
                errors.append(f"  [FEHLER] {pkg}: {e}")

        # 3. Claude Code MCP-Config aktualisieren
        results.append("\n=== Claude Code Konfiguration ===\n")
        config_result = self._configure_claude_mcp(packages, dry_run)
        results.append(config_result)

        # Ergebnis
        output = "\n".join(results)
        if errors:
            output += "\n\nFehler:\n" + "\n".join(errors)
            return False, output

        return True, output

    def _configure_claude_mcp(self, packages: list, dry_run: bool) -> str:
        """Aktualisiert die Claude Code MCP-Konfiguration."""
        # Claude Code config: ~/.claude.json oder ~/.claude/mcp.json
        claude_config = Path.home() / ".claude.json"

        if not claude_config.exists():
            # Alternativ: ~/.claude/mcp.json
            alt_config = Path.home() / ".claude" / "mcp.json"
            if alt_config.exists():
                claude_config = alt_config
            else:
                return (
                    "  Claude Code Config nicht gefunden.\n"
                    "  Manuell konfigurieren mit:\n"
                    "    claude mcp add --scope user bach-codecommander -- npx bach-codecommander-mcp\n"
                    "    claude mcp add --scope user bach-filecommander -- npx bach-filecommander-mcp"
                )

        if dry_run:
            return f"  [DRY-RUN] Wuerde {claude_config} aktualisieren"

        try:
            config = json.loads(claude_config.read_text(encoding="utf-8"))
        except Exception:
            config = {}

        # mcpServers-Sektion sicherstellen
        if "mcpServers" not in config:
            config["mcpServers"] = {}

        # Server-Eintraege hinzufuegen/aktualisieren
        server_configs = {
            "bach-codecommander": {
                "command": "npx",
                "args": ["bach-codecommander-mcp"]
            },
            "bach-filecommander": {
                "command": "npx",
                "args": ["bach-filecommander-mcp"]
            },
        }

        updated = []
        for name, conf in server_configs.items():
            if name not in config["mcpServers"]:
                config["mcpServers"][name] = conf
                updated.append(f"  [NEU] {name} hinzugefuegt")
            else:
                updated.append(f"  [OK] {name} bereits konfiguriert")

        # Config speichern
        claude_config.write_text(
            json.dumps(config, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return "\n".join(updated) + f"\n  Config: {claude_config}"

    def _check(self) -> tuple:
        """Prueft ob alle Abhaengigkeiten konfiguriert sind."""
        checks = []
        all_ok = True

        # 1. npm
        npm_path = shutil.which("npm")
        if npm_path:
            checks.append("[OK] npm verfuegbar")
        else:
            checks.append("[!!] npm nicht gefunden")
            all_ok = False

        # 2. MCP-Server
        for pkg in ["bach-codecommander-mcp", "bach-filecommander-mcp"]:
            try:
                proc = subprocess.run(
                    ["npm", "list", "-g", pkg, "--depth=0"],
                    capture_output=True, text=True, timeout=15
                )
                if proc.returncode == 0 and pkg in proc.stdout:
                    checks.append(f"[OK] {pkg} installiert")
                else:
                    checks.append(f"[!!] {pkg} nicht installiert")
                    all_ok = False
            except Exception:
                checks.append(f"[??] {pkg} konnte nicht geprueft werden")
                all_ok = False

        # 3. Secrets-Datei
        secrets_file = Path.home() / ".bach" / "bach_secrets.json"
        if secrets_file.exists():
            try:
                data = json.loads(secrets_file.read_text(encoding="utf-8"))
                count = len(data.get("secrets", {}))
                checks.append(f"[OK] Secrets-Datei vorhanden ({count} Keys)")
            except Exception:
                checks.append("[!!] Secrets-Datei defekt")
                all_ok = False
        else:
            checks.append("[!!] Secrets-Datei fehlt (~/.bach/bach_secrets.json)")
            all_ok = False

        # 4. bach.db
        db_path = self.base_path / "data" / "bach.db"
        if db_path.exists():
            checks.append("[OK] bach.db vorhanden")
        else:
            checks.append("[!!] bach.db fehlt")
            all_ok = False

        status = "Alles OK" if all_ok else "Einige Checks fehlgeschlagen"
        output = f"=== BACH Setup Check ===\n\n" + "\n".join(checks) + f"\n\nStatus: {status}"

        return all_ok, output

    def _setup_secrets(self) -> tuple:
        """Initialisiert oder syncht die Secrets-Datei."""
        try:
            import sys
            sys.path.insert(0, str(self.base_path))
            from hub.secrets import SecretsHandler
            handler = SecretsHandler()
            handler.sync_from_file(enforce_authority=False)
            return True, "Secrets-Sync abgeschlossen."
        except Exception as e:
            return False, f"Fehler beim Secrets-Sync: {e}"
