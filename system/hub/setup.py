# SPDX-License-Identifier: MIT
"""
Setup Handler - System-Konfiguration und Installationshilfe
============================================================

bach setup mcp              MCP-Server global installieren und Claude Code konfigurieren
bach setup n8n              n8n-manager-mcp optional installieren und konfigurieren
bach setup check             Pruefe ob alle Abhaengigkeiten konfiguriert sind
bach setup secrets           Secrets-Datei initialisieren / synchen
bach setup user              USER.md pruefen, personalisieren und mit DB synchronisieren

Teil von PEANUT Release: MCP-Server aus Repo entfernt, stattdessen via npm installieren.
B37: Optionale MCP-Server (n8n-manager-mcp) separat installierbar.
"""
import json
import re
import sqlite3
import subprocess
import shutil
from datetime import datetime
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

    # Optionale MCP-Server (nicht im Kern-Setup, separat installierbar)
    OPTIONAL_MCP_PACKAGES = {
        "n8n-manager-mcp": {
            "name": "n8n-manager",
            "config": {
                "command": "npx",
                "args": ["n8n-manager-mcp"]
            },
            "description": "n8n Workflow Manager MCP-Server",
        },
    }

    def get_operations(self) -> dict:
        return {
            "mcp": "MCP-Server global installieren und Claude Code konfigurieren",
            "n8n": "n8n-manager-mcp optional installieren und konfigurieren",
            "check": "Pruefe ob alle Abhaengigkeiten konfiguriert sind",
            "secrets": "Secrets-Datei initialisieren / synchen",
            "user": "USER.md pruefen, personalisieren und mit DB synchronisieren",
        }

    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if operation == "mcp":
            return self._setup_mcp(dry_run)
        elif operation == "n8n":
            return self._setup_n8n(dry_run)
        elif operation == "check":
            return self._check()
        elif operation == "secrets":
            return self._setup_secrets()
        elif operation == "user":
            return self._setup_user()
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

        # Hinweis auf optionale MCP-Server
        if self.OPTIONAL_MCP_PACKAGES:
            results.append("\n=== Optionale MCP-Server ===\n")
            for pkg, info in self.OPTIONAL_MCP_PACKAGES.items():
                installed = self._is_npm_package_installed(pkg)
                status_str = "[OK] installiert" if installed else "[--] nicht installiert"
                results.append(f"  {pkg}: {status_str}")
            results.append(f"\n  Installieren mit: bach setup n8n")

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

        # 5. Optionale MCP-Server (nur Info, kein Fehler wenn nicht installiert)
        for pkg, info in self.OPTIONAL_MCP_PACKAGES.items():
            installed = self._is_npm_package_installed(pkg)
            if installed:
                checks.append(f"[OK] {pkg} installiert (optional)")
            else:
                checks.append(f"[--] {pkg} nicht installiert (optional, bach setup n8n)")

        # 6. USER.md
        user_md = self.base_path.parent / "USER.md"
        if user_md.exists():
            content = user_md.read_text(encoding="utf-8")
            if "TEMPLATE" in content:
                checks.append("[!!] USER.md existiert, aber noch nicht personalisiert (TEMPLATE)")
                all_ok = False
            else:
                checks.append("[OK] USER.md vorhanden und personalisiert")
        else:
            checks.append("[!!] USER.md fehlt")
            all_ok = False

        status = "Alles OK" if all_ok else "Einige Checks fehlgeschlagen"
        output = f"=== BACH Setup Check ===\n\n" + "\n".join(checks) + f"\n\nStatus: {status}"

        return all_ok, output

    # =========================================================================
    # USER.md Setup (B34)
    # =========================================================================

    def _setup_user(self) -> tuple:
        """Prueft USER.md, personalisiert aus DB oder synct zurueck in DB.

        Logik:
          1. USER.md existiert nicht -> Fehler mit Hinweis
          2. USER.md ist noch TEMPLATE (enthaelt "TEMPLATE" Marker):
             -> Lese DB (assistant_user_profile), fuelle USER.md mit echten Daten
          3. USER.md ist bereits personalisiert (kein TEMPLATE Marker):
             -> Parse USER.md und sync relevante Felder in die DB
        """
        user_md = self.base_path.parent / "USER.md"
        db_path = self.base_path / "data" / "bach.db"
        results = ["=== USER.md Setup ===\n"]

        # 1. Existenz-Check
        if not user_md.exists():
            return False, (
                "USER.md nicht gefunden.\n"
                f"Erwartet: {user_md}\n"
                "Bitte USER.md aus dem Template wiederherstellen."
            )

        content = user_md.read_text(encoding="utf-8")
        is_template = "TEMPLATE" in content

        if is_template:
            # --- TEMPLATE -> Personalisieren aus DB ---
            results.append("  USER.md ist noch ein Template. Personalisiere aus DB...\n")

            if not db_path.exists():
                results.append("  [WARN] bach.db nicht gefunden - kann nicht aus DB personalisieren.")
                return False, "\n".join(results)

            # DB-Profil laden
            db_data = self._load_user_profile_from_db(db_path)

            if not db_data:
                results.append("  [WARN] Keine Profil-Daten in DB gefunden.")
                results.append("  USER.md bleibt als Template. Nutze 'bach profile edit' um Daten zu setzen.")
                return True, "\n".join(results)

            # USER.md mit DB-Daten fuellen
            new_content = self._personalize_user_md(content, db_data)
            user_md.write_text(new_content, encoding="utf-8")

            count = sum(len(v) if isinstance(v, (dict, list)) else 1 for v in db_data.values())
            results.append(f"  [OK] USER.md personalisiert ({count} Felder aus DB)")
            results.append("  TEMPLATE-Marker entfernt.")

        else:
            # --- Personalisiert -> Sync zurueck in DB ---
            results.append("  USER.md ist bereits personalisiert. Sync in DB...\n")

            if not db_path.exists():
                results.append("  [WARN] bach.db nicht gefunden - kann nicht in DB synchen.")
                return False, "\n".join(results)

            # USER.md parsen und in DB schreiben
            parsed = self._parse_user_md(content)
            synced = self._sync_user_md_to_db(parsed, db_path)

            results.append(f"  [OK] {synced} Eintraege in DB synchronisiert")

        # Sync-Timestamp in USER.md aktualisieren
        try:
            current_content = user_md.read_text(encoding="utf-8")
            today = datetime.now().strftime("%Y-%m-%d")
            direction = "DB -> USER.md" if is_template else "USER.md -> DB"
            updated = re.sub(
                r"\*\*Last Updated:\*\*.*",
                f"**Last Updated:** {today}",
                current_content,
            )
            updated = re.sub(
                r"\*\*Sync Source:\*\*.*",
                f"**Sync Source:** {direction} (setup user)",
                updated,
            )
            user_md.write_text(updated, encoding="utf-8")
            results.append(f"  Sync-Timestamp aktualisiert: {today}")
        except Exception as e:
            results.append(f"  [WARN] Timestamp-Update fehlgeschlagen: {e}")

        return True, "\n".join(results)

    def _load_user_profile_from_db(self, db_path: Path) -> dict:
        """Laedt Profildaten aus assistant_user_profile fuer USER.md-Personalisierung.

        Returns:
            Dict mit Kategorien: {
                'stats': {key: value, ...},
                'traits': {key: value, ...},
                'values': [value, ...],
                'preferences': {key: value, ...},
                'goals': {key: value, ...},
            }
        """
        try:
            conn = sqlite3.connect(str(db_path))
            rows = conn.execute(
                "SELECT category, key, value FROM assistant_user_profile ORDER BY category, key"
            ).fetchall()
            conn.close()
        except Exception:
            return {}

        data = {
            "stats": {},
            "traits": {},
            "values": [],
            "preferences": {},
            "goals": {},
        }

        for category, key, value in rows:
            if category == "stat":
                data["stats"][key] = value
            elif category == "trait":
                data["traits"][key] = value
            elif category == "value":
                data["values"].append(value)
            elif category == "preference":
                data["preferences"][key] = value
            elif category == "goal":
                data["goals"][key] = value

        return data

    def _personalize_user_md(self, template: str, db_data: dict) -> str:
        """Ersetzt Template-Platzhalter in USER.md mit echten DB-Daten.

        Strategie: Gezielte Ersetzungen in den bekannten Sektionen.
        Entfernt den TEMPLATE-Marker am Ende.
        """
        content = template
        stats = db_data.get("stats", {})
        traits = db_data.get("traits", {})
        values = db_data.get("values", [])
        goals = db_data.get("goals", {})

        # Basic Information
        if stats.get("name"):
            content = re.sub(
                r"\*\*Name:\*\*\s*.*",
                f"**Name:** {stats['name']}",
                content,
            )
        if stats.get("role"):
            content = re.sub(
                r"\*\*Role:\*\*\s*.*",
                f"**Role:** {stats['role']}",
                content,
            )
        if stats.get("language"):
            # Nur im Basic-Info-Block (erste Occurrence)
            content = re.sub(
                r"(\*\*Language:\*\*)\s*\w+",
                rf"\1 {stats['language']}",
                content,
                count=1,
            )
        if stats.get("timezone"):
            content = re.sub(
                r"\*\*Timezone:\*\*\s*.*",
                f"**Timezone:** {stats['timezone']}",
                content,
            )
        if stats.get("os"):
            content = re.sub(
                r"\*\*Operating System:\*\*\s*.*",
                f"**Operating System:** {stats['os']}",
                content,
            )

        # Communication Traits
        if traits.get("communication_style"):
            content = re.sub(
                r"\*\*Communication Style:\*\*\s*.*",
                f"**Communication Style:** {traits['communication_style']}",
                content,
            )
        if traits.get("detail_preference"):
            content = re.sub(
                r"\*\*Detail Preference:\*\*\s*.*",
                f"**Detail Preference:** {traits['detail_preference']}",
                content,
            )
        if traits.get("technical_depth"):
            content = re.sub(
                r"\*\*Technical Depth:\*\*\s*.*",
                f"**Technical Depth:** {traits['technical_depth']}",
                content,
            )

        # Core Values - ersetze die bestehende Liste
        if values:
            values_section = "\n".join(f"- {v}" for v in values)
            content = re.sub(
                r"(## .* Core Values\n\n)((?:- .*\n?)*)",
                rf"\g<1>{values_section}\n",
                content,
            )

        # Goals - short_term und long_term
        short_goals = [v for k, v in sorted(goals.items()) if k.startswith("short_term")]
        long_goals = [v for k, v in sorted(goals.items()) if k.startswith("long_term")]

        if short_goals:
            short_section = "\n".join(f"- {g}" for g in short_goals)
            content = re.sub(
                r"(### Short-term\n)((?:- .*\n?)*)",
                rf"\g<1>{short_section}\n",
                content,
            )
        if long_goals:
            long_section = "\n".join(f"- {g}" for g in long_goals)
            content = re.sub(
                r"(### Long-term\n)((?:- .*\n?)*)",
                rf"\g<1>{long_section}\n",
                content,
            )

        # TEMPLATE-Marker entfernen
        content = content.replace(
            "<!-- BACH-INTERNAL-MARKER: dist_type=1 TEMPLATE -->",
            "<!-- BACH-INTERNAL-MARKER: dist_type=1 PERSONALIZED -->",
        )
        content = re.sub(
            r"> \*\*Type:\*\* TEMPLATE.*",
            "> **Type:** PERSONALIZED (dist_type=1) -- customized from DB.",
            content,
        )

        return content

    def _parse_user_md(self, content: str) -> dict:
        """Parst eine personalisierte USER.md und extrahiert Profil-Daten.

        Returns:
            Dict mit Kategorien analog zu _load_user_profile_from_db()
        """
        data = {
            "stats": {},
            "traits": {},
            "values": [],
            "preferences": {},
            "goals_short": [],
            "goals_long": [],
        }

        # Basic Information
        m = re.search(r"\*\*Name:\*\*\s*(.+)", content)
        if m and m.group(1).strip() != "User":
            data["stats"]["name"] = m.group(1).strip()

        m = re.search(r"\*\*Role:\*\*\s*(.+)", content)
        if m:
            data["stats"]["role"] = m.group(1).strip()

        # Language im Basic-Info-Block (nicht im Coding-Block)
        m = re.search(r"Basic Information.*?\*\*Language:\*\*\s*(\w+)", content, re.DOTALL)
        if m:
            data["stats"]["language"] = m.group(1).strip()

        m = re.search(r"\*\*Timezone:\*\*\s*(.+)", content)
        if m:
            data["stats"]["timezone"] = m.group(1).strip()

        m = re.search(r"\*\*Operating System:\*\*\s*(.+)", content)
        if m:
            data["stats"]["os"] = m.group(1).strip()

        # Communication Traits
        m = re.search(r"\*\*Communication Style:\*\*\s*(.+)", content)
        if m:
            data["traits"]["communication_style"] = m.group(1).strip()

        m = re.search(r"\*\*Detail Preference:\*\*\s*(.+)", content)
        if m:
            data["traits"]["detail_preference"] = m.group(1).strip()

        m = re.search(r"\*\*Technical Depth:\*\*\s*(.+)", content)
        if m:
            data["traits"]["technical_depth"] = m.group(1).strip()

        # Core Values (Bullets nach "Core Values" Heading)
        values_match = re.search(
            r"## .* Core Values\n\n((?:- .+\n?)+)", content
        )
        if values_match:
            for line in values_match.group(1).strip().split("\n"):
                val = line.lstrip("- ").strip()
                if val:
                    data["values"].append(val)

        # Goals
        short_match = re.search(r"### Short-term\n((?:- .+\n?)+)", content)
        if short_match:
            for line in short_match.group(1).strip().split("\n"):
                g = line.lstrip("- ").strip()
                if g:
                    data["goals_short"].append(g)

        long_match = re.search(r"### Long-term\n((?:- .+\n?)+)", content)
        if long_match:
            for line in long_match.group(1).strip().split("\n"):
                g = line.lstrip("- ").strip()
                if g:
                    data["goals_long"].append(g)

        return data

    def _sync_user_md_to_db(self, parsed: dict, db_path: Path) -> int:
        """Schreibt geparste USER.md-Daten in assistant_user_profile.

        Nur sync-Eintraege werden ueberschrieben (manuell gelernte bleiben).

        Returns:
            Anzahl synchronisierter Eintraege
        """
        synced = 0
        try:
            conn = sqlite3.connect(str(db_path))
            now = datetime.now().isoformat()

            # Stats
            for key, value in parsed.get("stats", {}).items():
                if self._upsert_sync_row(conn, "stat", key, value, now):
                    synced += 1

            # Traits
            for key, value in parsed.get("traits", {}).items():
                if self._upsert_sync_row(conn, "trait", key, value, now):
                    synced += 1

            # Values
            for i, value in enumerate(parsed.get("values", [])):
                if self._upsert_sync_row(conn, "value", f"value_{i}", value, now):
                    synced += 1

            # Goals
            for i, goal in enumerate(parsed.get("goals_short", [])):
                if self._upsert_sync_row(conn, "goal", f"short_term_{i}", goal, now):
                    synced += 1

            for i, goal in enumerate(parsed.get("goals_long", [])):
                if self._upsert_sync_row(conn, "goal", f"long_term_{i}", goal, now):
                    synced += 1

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[WARN] USER.md -> DB sync fehlgeschlagen: {e}")

        return synced

    def _upsert_sync_row(self, conn: sqlite3.Connection, category: str,
                         key: str, value: str, now: str) -> bool:
        """Insert/Update einer Zeile, aber nur wenn nicht manuell gelernt.

        Returns:
            True wenn geschrieben, False wenn uebersprungen
        """
        existing = conn.execute(
            "SELECT learned_from FROM assistant_user_profile WHERE category=? AND key=?",
            (category, key),
        ).fetchone()

        if existing and existing[0] not in ("sync", "setup-user"):
            return False

        conn.execute("""
            INSERT INTO assistant_user_profile (category, key, value, confidence, learned_from, created_at, updated_at)
            VALUES (?, ?, ?, 'hoch', 'setup-user', ?, ?)
            ON CONFLICT(category, key) DO UPDATE SET
                value = excluded.value,
                confidence = excluded.confidence,
                learned_from = excluded.learned_from,
                updated_at = excluded.updated_at
        """, (category, key, value, now, now))
        return True

    # =========================================================================
    # Secrets Setup
    # =========================================================================

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

    # --- Hilfsmethoden ---

    def _is_npm_package_installed(self, package: str) -> bool:
        """Prueft ob ein npm-Paket global installiert ist."""
        try:
            proc = subprocess.run(
                ["npm", "list", "-g", package, "--depth=0"],
                capture_output=True, text=True, timeout=15
            )
            return proc.returncode == 0 and package in proc.stdout
        except Exception:
            return False

    def _find_claude_config(self) -> Path | None:
        """Findet die Claude Code MCP-Config-Datei."""
        claude_config = Path.home() / ".claude.json"
        if claude_config.exists():
            return claude_config
        alt_config = Path.home() / ".claude" / "mcp.json"
        if alt_config.exists():
            return alt_config
        return None

    def _setup_n8n(self, dry_run: bool = False) -> tuple:
        """Installiert n8n-manager-mcp und konfiguriert Claude Code. (B37)"""
        results = []
        errors = []
        pkg = "n8n-manager-mcp"
        info = self.OPTIONAL_MCP_PACKAGES[pkg]

        # 1. npm pruefen
        npm_path = shutil.which("npm")
        if not npm_path:
            return False, (
                "npm nicht gefunden. Bitte Node.js installieren:\n"
                "  https://nodejs.org/\n"
                "Nach der Installation Terminal neu starten und erneut ausfuehren."
            )

        # 2. Paket installieren
        results.append("=== n8n-manager-mcp Installation ===\n")

        if self._is_npm_package_installed(pkg):
            results.append(f"  [OK] {pkg} bereits installiert")
        elif dry_run:
            results.append(f"  [DRY-RUN] npm install -g {pkg}")
        else:
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
        claude_config = self._find_claude_config()

        if not claude_config:
            results.append(
                "  Claude Code Config nicht gefunden.\n"
                "  Manuell konfigurieren mit:\n"
                f"    claude mcp add --scope user {info['name']} -- npx {pkg}"
            )
        elif dry_run:
            results.append(f"  [DRY-RUN] Wuerde {claude_config} aktualisieren")
        else:
            try:
                config = json.loads(claude_config.read_text(encoding="utf-8"))
            except Exception:
                config = {}

            if "mcpServers" not in config:
                config["mcpServers"] = {}

            server_name = info["name"]
            if server_name not in config["mcpServers"]:
                config["mcpServers"][server_name] = info["config"]
                results.append(f"  [NEU] {server_name} hinzugefuegt")
            else:
                results.append(f"  [OK] {server_name} bereits konfiguriert")

            claude_config.write_text(
                json.dumps(config, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            results.append(f"  Config: {claude_config}")

        # Ergebnis
        output = "\n".join(results)
        if errors:
            output += "\n\nFehler:\n" + "\n".join(errors)
            return False, output

        return True, output
