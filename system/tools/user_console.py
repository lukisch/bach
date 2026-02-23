#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: user_console
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version user_console

Description:
    [Beschreibung hinzufügen]

Usage:
    python user_console.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

# -*- coding: utf-8 -*-
"""
user_console.py - BACH Interaktive User-Konsole
================================================

Interaktiver Konsolenmodus fuer den Nutzer.
Ermoeglicht BACH-Befehle und Nachrichten direkt einzugeben.

Usage:
    python tools/user_console.py
    Oder: user/start_console.bat
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "bach.db"


def get_unread_messages():
    """Prueft auf ungelesene Nachrichten an den User."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        c.execute("""
            SELECT id, sender, content, created_at
            FROM comm_messages
            WHERE receiver = 'user' AND is_read = 0
            ORDER BY created_at DESC
            LIMIT 5
        """)
        msgs = c.fetchall()
        conn.close()
        return msgs
    except Exception:
        return []


def get_open_tasks_count():
    """Zaehlt offene Tasks."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
        count = c.fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 0


def run_bach_command(args_str):
    """Fuehrt einen BACH-Befehl aus."""
    cmd = f'python "{BASE_DIR / "bach.py"}" {args_str}'
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("[TIMEOUT] Befehl hat zu lange gedauert.")
    except Exception as e:
        print(f"[FEHLER] {e}")


def show_welcome():
    """Zeigt Willkommensnachricht."""
    now = datetime.now()
    if now.hour < 12:
        gruss = "Guten Morgen"
    elif now.hour < 18:
        gruss = "Guten Tag"
    else:
        gruss = "Guten Abend"

    tasks = get_open_tasks_count()
    msgs = get_unread_messages()

    print()
    print("=" * 60)
    print(f"  BACH v1.1 - User-Konsole")
    print(f"  {gruss}! | {now.strftime('%d.%m.%Y %H:%M')}")
    print("=" * 60)
    print()
    print(f"  Offene Tasks: {tasks}")
    print(f"  Ungelesene Nachrichten: {len(msgs)}")

    if msgs:
        print()
        print("  Neue Nachrichten:")
        for msg_id, sender, content, created in msgs:
            preview = content[:60] + "..." if len(content) > 60 else content
            print(f"    [{sender}] {preview}")

    print()
    print("  Befehle:")
    print("    bach <befehl>     BACH-Befehl ausfuehren")
    print("    msg <text>        Nachricht an alle Partner senden")
    print("    msg <partner> <t> Nachricht an Partner senden")
    print("    tasks             Offene Tasks anzeigen")
    print("    status            System-Status")
    print("    inbox             Neue Nachrichten lesen")
    print("    help              Hilfe anzeigen")
    print("    exit              Konsole beenden")
    print()


def show_help():
    """Zeigt erweiterte Hilfe."""
    print()
    print("  BACH User-Konsole - Befehle")
    print("  " + "=" * 40)
    print()
    print("  Direkte Befehle:")
    print("    tasks              Offene Tasks anzeigen")
    print("    status             System-Uebersicht")
    print("    inbox              Nachrichten lesen")
    print("    msg <text>         Nachricht an alle Partner")
    print("    msg claude <text>  Nachricht an Claude")
    print("    msg gemini <text>  Nachricht an Gemini")
    print()
    print("  BACH-Befehle (mit 'bach' Prefix):")
    print("    bach task add \"...\"    Task erstellen")
    print("    bach task done <id>    Task erledigen")
    print("    bach mem write \"...\"   Memory-Notiz")
    print("    bach --help <thema>    Hilfe zu Thema")
    print("    bach --status          Schnellstatus")
    print()
    print("  Beliebige BACH-Befehle:")
    print("    bach <alles>           Wird an bach.py weitergeleitet")
    print()
    print("  Konsole:")
    print("    help                   Diese Hilfe")
    print("    clear                  Bildschirm loeschen")
    print("    exit / quit            Konsole beenden")
    print()


def mark_messages_read():
    """Markiert Nachrichten an User als gelesen."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        c.execute("UPDATE comm_messages SET is_read = 1 WHERE receiver = 'user' AND is_read = 0")
        count = c.changes
        conn.commit()
        conn.close()
        return count
    except Exception:
        return 0


def main():
    """Hauptschleife der User-Konsole."""
    show_welcome()

    while True:
        try:
            user_input = input("  BACH> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  Auf Wiedersehen!")
            break

        if not user_input:
            continue

        lower = user_input.lower()

        # Exit
        if lower in ("exit", "quit", "q"):
            print("  Auf Wiedersehen!")
            break

        # Clear
        elif lower == "clear":
            os.system("cls" if os.name == "nt" else "clear")

        # Help
        elif lower == "help":
            show_help()

        # Tasks shortcut
        elif lower == "tasks":
            run_bach_command("task list")

        # Status shortcut
        elif lower == "status":
            run_bach_command("--status")

        # Inbox shortcut
        elif lower == "inbox":
            run_bach_command("msg list --to user")
            marked = mark_messages_read()
            if marked:
                print(f"  [{marked} Nachricht(en) als gelesen markiert]")

        # Nachricht senden
        elif lower.startswith("msg "):
            parts = user_input[4:].strip()
            if not parts:
                print("  Verwendung: msg <text> oder msg <partner> <text>")
                continue

            # Check ob erster Teil ein bekannter Partner ist
            known_partners = ["claude", "gemini", "ollama", "copilot", "deepseek"]
            first_word = parts.split()[0].lower() if parts.split() else ""

            if first_word in known_partners and len(parts.split()) > 1:
                partner = first_word
                text = parts[len(partner):].strip()
                run_bach_command(f'msg send {partner} "{text}"')
            else:
                # An alle Partner senden
                run_bach_command(f'msg send claude "{parts}"')
                run_bach_command(f'msg send gemini "{parts}"')

        # Bach-Befehl
        elif lower.startswith("bach "):
            cmd = user_input[5:].strip()
            run_bach_command(cmd)

        # Unbekannt - als Bach-Befehl versuchen
        else:
            print(f"  Unbekannter Befehl: {user_input}")
            print("  Tipp: 'help' fuer Befehle, 'bach <befehl>' fuer BACH-Befehle")


if __name__ == "__main__":
    main()
