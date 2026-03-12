# -*- coding: utf-8 -*-
"""
Migration 035: Fix Mr TikTak Persona
=====================================
Korrigiert die falsche Persona-Beschreibung fuer mr_tiktak.
War: "Unerbittlicher Taktgeber" (Zeitmanagement) -- falsch.
Ist: "Strategischer Taktiker" (Strategeme, Verhandlung) -- korrekt laut CONCEPT.md.
"""


def run_migration(conn):
    """Wird von core/db.py run_migrations() aufgerufen."""
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE bach_experts SET persona = ?, description = ? WHERE name = 'mr_tiktak'",
        (
            'Strategischer Taktiker. Kennt die 36 Strategeme, beraet bei Verhandlungen und Machtspielen.',
            'Strategie- und Taktikberatung, Strategeme, Verhandlungstaktik',
        )
    )
