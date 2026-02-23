# -*- coding: utf-8 -*-
"""
Copyright (c) 2026 Lukas Geiger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
BACH Library API - Programmatischer Zugriff ohne CLI
=====================================================

Drei Zugriffsmodi:
  1. Bibliothek-Modus:  from bach_api import task; task.list()
  2. Gemischter Modus:  session.startup() + API + session.shutdown()
  3. Session-Modus:     python bach.py --startup (klassische CLI)

Nutzung:
    from bach_api import session, task, memory, partner, tools, injector

    # Session-Lifecycle (optional -- Modus 2)
    session.startup(partner="claude", mode="silent")
    # ... arbeiten ...
    session.shutdown("Zusammenfassung")

    # Kern-Handler
    task.add("Aufgabe", "--priority", "P3")
    task.list()
    task.done(42)
    memory.write("Notiz")
    memory.status()

    # Domain-Handler
    steuer.status()
    partner.list()
    partner.delegate("Recherche", "--to=gemini")
    tools.list()
    tools.search("ocr")

    # Kognitive Injektoren
    injector.process("ich bin blockiert")
    injector.check_between("task done 42")
    injector.set_mode("api")                 # CLI-Hinweise filtern

    # Raw-Zugriff (beliebiger der 64+ Handler)
    app().execute("gesundheit", "termine", ["--upcoming"])

Verfuegbare Module:
    session, task, memory, backup, steuer, lesson, status,
    partner, logs, msg, tools, help, update, injector, app
"""

import re
import sys
from pathlib import Path

# system/ Verzeichnis ermitteln
_SYSTEM_DIR = Path(__file__).parent

# sys.path sicherstellen
if str(_SYSTEM_DIR) not in sys.path:
    sys.path.insert(0, str(_SYSTEM_DIR))

# Lazy App-Singleton
_app = None


def get_app():
    """Gibt die App-Singleton-Instanz zurueck."""
    global _app
    if _app is None:
        from core.app import App
        _app = App(_SYSTEM_DIR)
    return _app


class _HandlerProxy:
    """Proxy fuer bequemen Zugriff auf Handler-Operationen.

    Ermoeglicht: task.add("...") statt app.execute("task", "add", ["..."])
    """

    def __init__(self, handler_name: str):
        self._name = handler_name

    def __getattr__(self, operation: str):
        """Jeder Attributzugriff wird zu einem Handler-Aufruf."""
        def caller(*args):
            app = get_app()
            str_args = [str(a) for a in args]
            success, message = app.execute(self._name, operation, str_args)
            if not success:
                print(f"[FEHLER] {message}")
            return message
        return caller

    def __call__(self, operation: str = "", *args):
        """Direkter Aufruf: task("list")"""
        app = get_app()
        str_args = [str(a) for a in args]
        success, message = app.execute(self._name, operation, str_args)
        return (success, message)


# --- Session-Management ---

class _SessionProxy:
    """Ergonomische API fuer Session-Lifecycle (Startup/Shutdown).

    Ersetzt: python bach.py --startup --partner=claude --mode=silent
    Durch:   session.startup(partner="claude", mode="silent")
    """

    def startup(self, partner: str = "claude", mode: str = "silent",
                quick: bool = False) -> str:
        """Startet eine BACH-Session.

        Fuehrt das komplette Startprotokoll aus:
        - Partner ein-stempeln (Presence)
        - Vorherige Session des Partners auto-schliessen
        - Memory-Check, Task-Uebersicht, Nachrichten
        - Injektoren aktivieren

        Args:
            partner: Partner-ID (claude, gemini, user, ...)
            mode: Startup-Modus (silent, gui, text, dual)
            quick: True = ohne Directory-Scan (schneller)

        Returns:
            Startup-Report als String
        """
        a = get_app()
        operation = "quick" if quick else "run"
        args = [f"--partner={partner}", f"--mode={mode}"]
        success, message = a.execute("startup", operation, args)
        return message

    def shutdown(self, summary: str = None, partner: str = "claude",
                 mode: str = "complete") -> str:
        """Beendet eine BACH-Session.

        Fuehrt das Shutdown-Protokoll aus:
        - Directory-Scan (Aenderungen erkennen)
        - Session in DB speichern
        - Auto-Snapshot bei vielen Aenderungen
        - Memory-Konsolidierung
        - Partner aus-stempeln

        Args:
            summary: Session-Zusammenfassung (optional, Autolog-Fallback)
            partner: Partner-ID
            mode: complete, quick, oder emergency

        Returns:
            Shutdown-Report als String
        """
        a = get_app()
        # Partner-Flag muss VOR dem Summary stehen, da der Handler
        # args durchsucht und den Rest als Summary joined
        args = [f"--partner={partner}"]
        if summary:
            # Summary als separates Argument (Handler joined mit " ")
            args.extend(summary.split())
        success, message = a.execute("shutdown", mode, args)
        return message

    def shutdown_quick(self, summary: str = None,
                       partner: str = "claude") -> str:
        """Schneller Shutdown ohne Directory-Scan."""
        return self.shutdown(summary=summary, partner=partner, mode="quick")

    def shutdown_emergency(self, note: str = None,
                           partner: str = "claude") -> str:
        """Notfall-Shutdown - nur Working Memory sichern."""
        return self.shutdown(summary=note, partner=partner, mode="emergency")


# --- Convenience-Module ---

# Session-Lifecycle
session = _SessionProxy()

# Handler-Proxies (haeufigste)
task = _HandlerProxy("task")
memory = _HandlerProxy("memory")
backup = _HandlerProxy("backup")
steuer = _HandlerProxy("steuer")
lesson = _HandlerProxy("lesson")
status = _HandlerProxy("status")
partner = _HandlerProxy("partner")
logs = _HandlerProxy("logs")
msg = _HandlerProxy("msg")
tools = _HandlerProxy("tools")
help = _HandlerProxy("help")
update = _HandlerProxy("update")
email = _HandlerProxy("email")

# App-Instanz fuer direkten Zugriff
app = get_app

# Hook-Framework (Lifecycle-Events)
try:
    from core.hooks import hooks
except ImportError:
    hooks = None

# Plugin-API (Dynamische Erweiterung)
try:
    from core.plugin_api import plugins
except ImportError:
    plugins = None


# --- Injector-Integration ---

# Pattern: "bach befehl" oder "--befehl" CLI-Hinweise erkennen
_CLI_PATTERN = re.compile(
    r'bach\s+\w+'           # "bach steuer status", "bach task list"
    r'|--\w+'               # "--help tasks", "--memory"
    r'|python\s+\w+\.py'    # "python injectors.py"
)


class _InjectorProxy:
    """Proxy fuer Injector-Zugriff ueber die Library API.

    Alle 6 Injektoren verfuegbar. Optional CLI-Hinweise filterbar.

    Beispiel:
        from bach_api import injector
        hints = injector.process("ich bin blockiert bei diesem bug")
        # → ['[STRATEGIE] Fehler sind wertvolle Informationen...']
    """

    def __init__(self):
        self._system = None
        self._mode = "cli"  # "cli" = alles, "api" = CLI-Hinweise gefiltert

    def _get_system(self):
        """Lazy-Init des InjectorSystem."""
        if self._system is None:
            sys.path.insert(0, str(_SYSTEM_DIR / "tools"))
            try:
                from injectors import InjectorSystem
                self._system = InjectorSystem(_SYSTEM_DIR)
            finally:
                sys.path.pop(0)
        return self._system

    def set_mode(self, mode: str):
        """Setzt den Modus: 'cli' (alles) oder 'api' (CLI-Hinweise gefiltert).

        Im API-Modus werden Kontext-Hinweise die CLI-Befehle enthalten
        (z.B. 'bach steuer status') herausgefiltert. Pfad-Hinweise und
        kognitive Strategien bleiben erhalten.
        """
        if mode in ("cli", "api"):
            self._mode = mode

    def _filter_cli(self, injections: list) -> list:
        """Filtert CLI-spezifische Hinweise im API-Modus."""
        if self._mode != "api":
            return injections
        result = []
        for inj in injections:
            # Strategy, Between, Time → immer behalten (kein CLI)
            if inj.startswith(("[STRATEGIE]", "[BETWEEN]", "[ZEIT]", "[AUFGABE")):
                result.append(inj)
            # Kontext-Hinweise: nur behalten wenn kein CLI-Befehl drin
            elif inj.startswith("[KONTEXT]"):
                if not _CLI_PATTERN.search(inj):
                    result.append(inj)
            # Tool-Hinweise: Pfade sind OK, CLI-Befehle rausfiltern
            elif inj.startswith("[TOOL"):
                # Tool-Reminder hat Pfade (tools/xyz.py) → behalten
                result.append(inj)
            else:
                result.append(inj)
        return result

    def process(self, text: str, context: dict = None) -> list:
        """Verarbeitet Text durch alle aktiven Injektoren.

        Args:
            text: Zu analysierender Text (z.B. User-Input, Task-Beschreibung)
            context: Optional - Zusaetzlicher Kontext

        Returns:
            Liste von Hinweisen (kann leer sein)
        """
        system = self._get_system()
        injections = system.process(text, context)
        return self._filter_cli(injections)

    def check_between(self, last_action: str, session_ending: bool = False):
        """Prueft ob Between-Task Quality-Check faellig ist.

        Gibt Erinnerung zurueck nach Task-Abschluss:
        'Testergebnis? Doku? Commit? Naechste Aufgabe?'

        Args:
            last_action: Beschreibung der letzten Aktion (z.B. "task done 42")
            session_ending: True wenn Session endet

        Returns:
            Reminder-String oder None
        """
        system = self._get_system()
        return system.check_between(last_action, session_ending)

    def tool_reminder(self):
        """Gibt einmalige Tool-Erinnerung fuer Session-Start zurueck.

        Listet verfuegbare Tool-Kategorien (OCR, Import, Domain-Handler, etc.)
        Wird nur beim ersten Aufruf zurueckgegeben, danach None.

        Returns:
            Tool-Uebersicht String oder None
        """
        system = self._get_system()
        return system.get_tool_reminder()

    def assign_task(self, max_minutes: int = 5):
        """Weist automatisch eine passende Aufgabe zu.

        Args:
            max_minutes: Maximale geschaetzte Dauer

        Returns:
            Tuple (success: bool, message: str)
        """
        system = self._get_system()
        return system.assign_task(max_minutes)

    def decompose(self, task_id: str):
        """Zerlegt grosse Aufgabe in Teilschritte.

        Args:
            task_id: ID der Aufgabe

        Returns:
            Tuple (success: bool, message: str)
        """
        system = self._get_system()
        return system.decompose_task(task_id)

    def time_check(self):
        """Gibt aktuelle Zeit + ungelesene Nachrichten zurueck.

        Returns:
            Zeit-Info String oder None (wenn Intervall nicht erreicht)
        """
        system = self._get_system()
        if system.config.is_enabled("time_injector"):
            return system.time_injector.check()
        return None

    def status(self):
        """Zeigt Status aller Injektoren (an/aus, Cooldown-Info).

        Returns:
            Status-String
        """
        system = self._get_system()
        return system.status()

    def toggle(self, injector_name: str):
        """Schaltet einzelnen Injektor an/aus.

        Args:
            injector_name: strategy_injector, context_injector,
                          time_injector, between_injector

        Returns:
            Tuple (success: bool, message: str)
        """
        system = self._get_system()
        return system.toggle(injector_name)


injector = _InjectorProxy()
