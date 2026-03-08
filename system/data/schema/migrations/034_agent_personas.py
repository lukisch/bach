# -*- coding: utf-8 -*-
"""
Migration 034: Agent Personas (SUGAR v3.8.0)
=============================================
Display-Namen (Vornamen) und Charakter-Beschreibungen fuer Agenten und Experten.

- Setzt kurze display_names (Persona-Namen) fuer alle DE-Agenten/Experten
- Fuegt persona-Spalte hinzu (ALTER TABLE mit try/except fuer Idempotenz)
- Setzt Persona-Beschreibungen fuer Boss-Agenten
"""


def run_migration(conn):
    """Wird von core/db.py run_migrations() aufgerufen."""
    cursor = conn.cursor()

    # --- 1. persona Spalte hinzufuegen (idempotent) ---
    for table in ('bach_agents', 'bach_experts'):
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN persona TEXT")
        except Exception:
            pass  # Spalte existiert bereits

    # --- 2. Display-Namen fuer Boss-Agenten (DE) ---
    agent_names = {
        'ati': 'Atlas',
        'bueroassistent': 'Clara',
        'finanz-assistent': 'Felix',
        'gesundheitsassistent': 'Helena',
        'persoenlicher-assistent': 'Paul',
    }
    for name, display in agent_names.items():
        cursor.execute(
            "UPDATE bach_agents SET display_name = ? WHERE name = ? AND language = 'de'",
            (display, name)
        )

    # --- 3. Display-Namen fuer Experten (DE) ---
    expert_names = {
        'steuer-agent': 'Theodor',
        'financial_mail': 'Frieda',
        'aboservice': 'Anton',
        'gesundheitsverwalter': 'Gustav',
        'psycho-berater': 'Sophie',
        'health_import': 'Hugo',
        'haushaltsmanagement': 'Martha',
        'foerderplaner': 'Florian',
        'bewerbungsexperte': 'Benjamin',
        'data-analysis': 'Diana',
        'decision-briefing': 'Dietrich',
        'report_generator': 'Rita',
        'mr_tiktak': 'Mr. TikTak',
        'transkriptions-service': 'Tristan',
        'wikiquizzer': 'Wilhelm',
    }
    for name, display in expert_names.items():
        cursor.execute(
            "UPDATE bach_experts SET display_name = ? WHERE name = ? AND language = 'de'",
            (display, name)
        )

    # --- 4. Personas fuer Boss-Agenten ---
    agent_personas = {
        'ati': 'Pragmatischer Handwerker. Loesungsorientiert, direkt, technisch praezise.',
        'bueroassistent': 'Strukturierte Organisatorin. Zuverlaessig, checklisten-orientiert, denkt an alles.',
        'finanz-assistent': 'Aufmerksamer Sparfuchs. Analytisch, findet versteckte Kosten, nuechterner Humor.',
        'gesundheitsassistent': 'Fuersorgliche Begleiterin. Empathisch, gruendlich, erklaert verstaendlich.',
        'persoenlicher-assistent': 'Vielseitiger Allrounder. Anpassungsfaehig, proaktiv, locker-professionell.',
    }
    for name, persona in agent_personas.items():
        cursor.execute(
            "UPDATE bach_agents SET persona = ? WHERE name = ? AND persona IS NULL",
            (persona, name)
        )

    # --- 5. Personas und Descriptions fuer Experten ---
    expert_data = {
        'steuer-agent': ('Peniler Steuerberater. Gruendlich, regelkonform, kennt jeden Paragraphen.', 'Steuerbelege erfassen und Werbungskosten optimieren'),
        'financial_mail': ('Mail-Detektivin. Findet jede Rechnung, jedes Abo, jeden Vertrag.', 'Finanz-Mails analysieren und kategorisieren'),
        'aboservice': ('Kuendigungskoenig. Findet vergessene Abos und kuendigt was nicht gebraucht wird.', 'Abo-Verwaltung und Kuendigungen'),
        'gesundheitsverwalter': ('Archivar der Befunde. Ordentlich, systematisch, vergisst keinen Wert.', 'Arztberichte und Laborwerte verwalten'),
        'psycho-berater': ('Einfuehlsame Zuhoererin. Geduldig, warmherzig, therapeutisch geschult.', 'Therapeutische Gespraeche und psychologische Unterstuetzung'),
        'health_import': ('Gewissenhafter Datenpfleger. Importiert sauber, validiert gruendlich.', 'Gesundheitsdaten importieren und strukturieren'),
        'haushaltsmanagement': ('Sparsame Hauswirtschafterin. Kennt jeden Posten, plant voraus.', 'Haushaltsbuch und Inventarverwaltung'),
        'foerderplaner': ('Foerdermittel-Experte. Kennt ICF, weiss was beantragt werden kann.', 'ICF-basierte Foerderplanung erstellen'),
        'bewerbungsexperte': ('Karriere-Coach. Motivierend, kennt den Arbeitsmarkt, schreibt ueberzeugend.', 'CV, Anschreiben und LinkedIn-Profile optimieren'),
        'data-analysis': ('Zahlenfluesterin. Sieht Muster wo andere Chaos sehen.', 'Datenanalyse und statistische Auswertungen'),
        'decision-briefing': ('Kuehler Stratege. Waegt ab, strukturiert Optionen, empfiehlt klar.', 'Entscheidungsvorbereitung und Briefings'),
        'report_generator': ('Effiziente Berichtsmaschine. Schnell, formatiert, auf den Punkt.', 'Berichte und Dokumentationen erstellen'),
        'mr_tiktak': ('Unerbittlicher Taktgeber. Haelt den Rhythmus, mahnt Deadlines an.', 'Zeitmanagement und Deadline-Tracking'),
        'transkriptions-service': ('Geduldiger Zuhoerer. Versteht jedes Wort, auch bei Hintergrundlaerm.', 'Audio-Transkription und Verschriftlichung'),
        'wikiquizzer': ('Quizmaster mit Enzyklopaedie-Wissen. Stellt kluge Fragen, weiss die Antwort.', 'Wiki-Quiz und Wissensabfragen'),
    }
    for name, (persona, desc) in expert_data.items():
        cursor.execute(
            "UPDATE bach_experts SET persona = ?, description = COALESCE(NULLIF(description, ''), ?) WHERE name = ? AND persona IS NULL",
            (persona, desc, name)
        )
