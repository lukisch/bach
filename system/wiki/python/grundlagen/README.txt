================================================================================
                            PYTHON GRUNDLAGEN
================================================================================

Portabilitaet:      UNIVERSAL
Zuletzt validiert:  2026-02-05
Naechste Pruefung:  2027-02-05
Quellen:            python.org/doc, PEP 8, Real Python

Stand: 2026-02-05

================================================================================
                            INHALTSVERZEICHNIS
================================================================================

  1. Einfuehrung
  2. Installation
  3. Erste Schritte
  4. Grundlegende Syntax
  5. Variablen und Zuweisungen
  6. Operatoren
  7. Eingabe und Ausgabe
  8. Kommentare und Dokumentation
  9. BACH-Integration
  10. Best Practices
  11. Haeufige Fehler

================================================================================
                              1. EINFUEHRUNG
================================================================================

Python ist eine interpretierte, hochrangige Programmiersprache, die 1991 von
Guido van Rossum entwickelt wurde. Sie zeichnet sich durch klare, lesbare
Syntax und eine umfangreiche Standardbibliothek aus.

HAUPTMERKMALE
-------------
  - Einfache, lesbare Syntax (Code liest sich fast wie Englisch)
  - Dynamische Typisierung (Typen werden zur Laufzeit bestimmt)
  - Automatische Speicherverwaltung (Garbage Collection)
  - Plattformunabhaengig (Windows, Linux, macOS)
  - Umfangreiche Standardbibliothek ("Batteries included")
  - Grosse Community und reichhaltiges Oekosystem

ANWENDUNGSBEREICHE
------------------
  - Webentwicklung (Django, Flask, FastAPI)
  - Datenanalyse und -visualisierung (Pandas, Matplotlib)
  - Machine Learning und KI (TensorFlow, PyTorch, scikit-learn)
  - Automatisierung und Scripting
  - Wissenschaftliches Rechnen (NumPy, SciPy)
  - Desktop-Anwendungen (Tkinter, PyQt)

================================================================================
                              2. INSTALLATION
================================================================================

WINDOWS
-------
  1. Download von https://www.python.org/downloads/
  2. Installer ausfuehren
  3. WICHTIG: "Add Python to PATH" aktivieren!
  4. Installation abschliessen

  Pruefung in der Kommandozeile:
    > python --version
    Python 3.12.x

LINUX (Debian/Ubuntu)
---------------------
  $ sudo apt update
  $ sudo apt install python3 python3-pip python3-venv

  Bei den meisten Linux-Distributionen ist Python vorinstalliert.

MACOS
-----
  Mit Homebrew:
    $ brew install python

  Oder Download von python.org

ANACONDA DISTRIBUTION
---------------------
  Fuer wissenschaftliches Arbeiten empfohlen:
    - Enthaelt viele vorinstallierte Pakete
    - Eigener Paketmanager (conda)
    - Download: https://www.anaconda.com/

PATH-KONFIGURATION
------------------
  Falls Python nicht gefunden wird:

  Windows (PowerShell):
    $env:PATH += ";C:\Python312;C:\Python312\Scripts"

  Linux/macOS (bash):
    export PATH="$PATH:/usr/local/bin/python3"

================================================================================
                            3. ERSTE SCHRITTE
================================================================================

INTERAKTIVER MODUS (REPL)
-------------------------
  Der REPL (Read-Eval-Print-Loop) ist ideal zum Experimentieren:

    $ python3
    Python 3.12.0 (main, Oct  2 2023, 00:00:00)
    >>> print("Hallo Welt!")
    Hallo Welt!
    >>> 2 + 2
    4
    >>> exit()

  Befehle:
    >>> help()          # Hilfesystem starten
    >>> help(print)     # Hilfe zu einer Funktion
    >>> dir()           # Verfuegbare Namen anzeigen
    >>> exit()          # REPL beenden (oder Ctrl+D)

PYTHON-DATEIEN ERSTELLEN
------------------------
  Python-Code wird in Dateien mit der Endung .py gespeichert.

  Beispiel: hallo.py
  ------------------
    # Mein erstes Python-Programm
    nachricht = "Hallo Welt!"
    print(nachricht)

  Ausfuehrung:
    $ python3 hallo.py
    Hallo Welt!

SHEBANG (UNIX/LINUX/MACOS)
--------------------------
  Um Scripts direkt ausfuehrbar zu machen:

    #!/usr/bin/env python3
    print("Direkt ausfuehrbar!")

  Dann:
    $ chmod +x script.py
    $ ./script.py

================================================================================
                          4. GRUNDLEGENDE SYNTAX
================================================================================

EINRUECKUNG
-----------
  Python verwendet Einrueckung statt geschweifter Klammern zur
  Strukturierung von Code-Bloecken.

  RICHTIG (4 Spaces empfohlen):
    if bedingung:
        print("Bedingung erfuellt")
        print("Noch eine Zeile")

  FALSCH:
    if bedingung:
    print("Fehler!")  # IndentationError

  ACHTUNG: Tabs und Spaces nicht mischen!

DOPPELPUNKT BEI BLOECKEN
------------------------
  Nach Kontrollstrukturen folgt immer ein Doppelpunkt:

    if x > 0:           # Doppelpunkt
        print("positiv")

    for i in range(5):  # Doppelpunkt
        print(i)

    def funktion():     # Doppelpunkt
        pass

ZEILENFORTSETZUNG
-----------------
  Lange Zeilen koennen fortgesetzt werden:

  Mit Backslash:
    summe = 1 + 2 + 3 + \
            4 + 5 + 6

  In Klammern (bevorzugt):
    summe = (1 + 2 + 3 +
             4 + 5 + 6)

MEHRERE ANWEISUNGEN PRO ZEILE
-----------------------------
  Moeglich, aber nicht empfohlen:
    x = 1; y = 2; z = 3

================================================================================
                        5. VARIABLEN UND ZUWEISUNGEN
================================================================================

GRUNDLAGEN
----------
  In Python werden Variablen ohne Typdeklaration erstellt:

    name = "Alice"          # String
    alter = 30              # Integer
    groesse = 1.75          # Float
    ist_student = True      # Boolean

NAMENSKONVENTIONEN (PEP 8)
--------------------------
  Variablen und Funktionen:    snake_case
    benutzer_name = "Max"
    def berechne_summe():
        pass

  Konstanten:                  GROSSBUCHSTABEN
    MAX_VERSUCHE = 3
    PI = 3.14159
    DATENBANK_URL = "localhost:5432"

  Klassen:                     PascalCase
    class MeineKlasse:
        pass

GUELTIGE NAMEN
--------------
  - Beginnen mit Buchstabe oder Unterstrich
  - Enthalten Buchstaben, Zahlen, Unterstriche
  - Keine reservierten Woerter

  GUELTIG:        UNGUELTIG:
    name            2name (beginnt mit Zahl)
    _privat         mein-name (Bindestrich)
    name2           class (reserviert)
    mein_name       for (reserviert)

MEHRFACHZUWEISUNG
-----------------
    # Gleicher Wert
    a = b = c = 0

    # Verschiedene Werte
    x, y, z = 1, 2, 3

    # Werte tauschen
    a, b = b, a

================================================================================
                              6. OPERATOREN
================================================================================

ARITHMETISCHE OPERATOREN
------------------------
    +     Addition           5 + 3    = 8
    -     Subtraktion        5 - 3    = 2
    *     Multiplikation     5 * 3    = 15
    /     Division           5 / 3    = 1.666...
    //    Ganzzahldivision   5 // 3   = 1
    %     Modulo (Rest)      5 % 3    = 2
    **    Potenz             5 ** 3   = 125

VERGLEICHSOPERATOREN
--------------------
    ==    Gleich             5 == 5   -> True
    !=    Ungleich           5 != 3   -> True
    <     Kleiner            3 < 5    -> True
    >     Groesser           5 > 3    -> True
    <=    Kleiner gleich     3 <= 3   -> True
    >=    Groesser gleich    5 >= 3   -> True

LOGISCHE OPERATOREN
-------------------
    and   Und                True and False  -> False
    or    Oder               True or False   -> True
    not   Nicht              not True        -> False

  Beispiel:
    alter = 25
    if alter >= 18 and alter < 65:
        print("Erwachsener im Arbeitsalter")

ZUGEHOERIGKEITS- UND IDENTITAETSOPERATOREN
------------------------------------------
    in        Enthalten in    "a" in "hallo"    -> True
    not in    Nicht enthalten "x" not in "abc"  -> True
    is        Identisch       a is b
    is not    Nicht identisch a is not None

  WICHTIG: "is" prueft Identitaet, "==" prueft Gleichheit!
    a = [1, 2, 3]
    b = [1, 2, 3]
    a == b    # True (gleicher Inhalt)
    a is b    # False (verschiedene Objekte)

ERWEITERTE ZUWEISUNGSOPERATOREN
-------------------------------
    x += 5    # x = x + 5
    x -= 3    # x = x - 3
    x *= 2    # x = x * 2
    x /= 4    # x = x / 4
    x //= 2   # x = x // 2
    x %= 3    # x = x % 3
    x **= 2   # x = x ** 2

================================================================================
                          7. EINGABE UND AUSGABE
================================================================================

AUSGABE MIT PRINT()
-------------------
    print("Hallo Welt!")
    print("Wert:", 42)
    print("Eins", "Zwei", "Drei")       # Mit Leerzeichen
    print("Eins", "Zwei", sep="-")      # Mit Trennzeichen: Eins-Zwei
    print("Zeile 1", end=" ")           # Ohne Zeilenumbruch
    print("Zeile 2")                    # Ausgabe: Zeile 1 Zeile 2

FORMATIERTE AUSGABE (F-STRINGS)
-------------------------------
  F-Strings (Python 3.6+) sind die modernste Methode:

    name = "Alice"
    alter = 30

    print(f"Name: {name}, Alter: {alter}")
    print(f"In 5 Jahren: {alter + 5}")
    print(f"Pi: {3.14159:.2f}")         # Zwei Dezimalstellen
    print(f"Zahl: {42:05d}")            # Mit fuehrenden Nullen: 00042

EINGABE MIT INPUT()
-------------------
    name = input("Wie heisst du? ")
    print(f"Hallo, {name}!")

  WICHTIG: input() gibt immer einen String zurueck!

    # Fuer Zahlen konvertieren:
    alter = int(input("Dein Alter: "))
    preis = float(input("Preis: "))

================================================================================
                      8. KOMMENTARE UND DOKUMENTATION
================================================================================

EINZEILIGE KOMMENTARE
---------------------
    # Dies ist ein Kommentar
    x = 5  # Kommentar am Zeilenende

MEHRZEILIGE KOMMENTARE
----------------------
    """
    Dies ist ein mehrzeiliger
    Kommentar oder Docstring.
    """

    '''
    Auch mit einfachen
    Anfuehrungszeichen moeglich.
    '''

DOCSTRINGS
----------
  Dokumentation fuer Module, Klassen und Funktionen:

    def berechne_flaeche(laenge, breite):
        """
        Berechnet die Flaeche eines Rechtecks.

        Args:
            laenge: Die Laenge des Rechtecks
            breite: Die Breite des Rechtecks

        Returns:
            Die Flaeche als float

        Beispiel:
            >>> berechne_flaeche(5, 3)
            15
        """
        return laenge * breite

================================================================================
                            9. BACH-INTEGRATION
================================================================================

PYTHON IN BACH VERWENDEN
------------------------
  BACH kann Python-Scripts ausfuehren und deren Ausgabe verarbeiten:

    [BACH]> python mein_script.py
    [BACH]> python -c "print('Schneller Einzeiler')"

BACH-HELPER SCRIPTS
-------------------
  Python eignet sich ideal fuer BACH-Erweiterungen:

    # bach_helper.py
    #!/usr/bin/env python3
    """BACH Helper Script fuer Dateiverwaltung"""

    import os
    import sys

    def liste_dateien(pfad="."):
        """Listet alle Dateien im Verzeichnis"""
        for eintrag in os.listdir(pfad):
            print(eintrag)

    if __name__ == "__main__":
        pfad = sys.argv[1] if len(sys.argv) > 1 else "."
        liste_dateien(pfad)

VIRTUELLE UMGEBUNGEN
--------------------
  Fuer isolierte Projektumgebungen:

    $ python -m venv mein_projekt_env
    $ source mein_projekt_env/bin/activate    # Linux/macOS
    $ mein_projekt_env\Scripts\activate       # Windows

    (mein_projekt_env) $ pip install requests
    (mein_projekt_env) $ deactivate

================================================================================
                            10. BEST PRACTICES
================================================================================

CODE-STIL (PEP 8)
-----------------
  - 4 Spaces fuer Einrueckung (keine Tabs)
  - Maximale Zeilenlaenge: 79-120 Zeichen
  - Leerzeilen zwischen Funktionen/Klassen
  - Imports am Dateianfang
  - Beschreibende Variablennamen

IMPORTS ORGANISIEREN
--------------------
    # 1. Standardbibliothek
    import os
    import sys
    from datetime import datetime

    # 2. Drittanbieter
    import requests
    import numpy as np

    # 3. Lokale Module
    from . import mein_modul

TYPE HINTS (PYTHON 3.5+)
------------------------
    def addiere(a: int, b: int) -> int:
        return a + b

    name: str = "Alice"
    zahlen: list[int] = [1, 2, 3]

================================================================================
                            11. HAEUFIGE FEHLER
================================================================================

SYNTAXFEHLER
------------
    # Fehlender Doppelpunkt
    if x > 0      # SyntaxError
        print(x)

    # Falsche Einrueckung
    if True:
    print("Fehler")  # IndentationError

TYPFEHLER
---------
    # String und Zahl addieren
    "Alter: " + 25    # TypeError
    # Loesung:
    "Alter: " + str(25)

NAMENFEHLER
-----------
    print(unbekannte_variable)  # NameError

INDEX AUSSERHALB
----------------
    liste = [1, 2, 3]
    print(liste[5])  # IndexError

================================================================================
                              SIEHE AUCH
================================================================================

  wiki/python/datentypen/
    -> Ausfuehrliche Beschreibung aller Python-Datentypen

  wiki/python/kontrollstrukturen/
    -> if/else, Schleifen, Ausnahmebehandlung

  wiki/python/funktionen/
    -> Funktionsdefinition, Parameter, Lambda

  wiki/python/module/
    -> Import-System, Pakete, pip

  wiki/programmierung/paradigmen/
    -> OOP, Funktionale Programmierung

================================================================================
                         ENDE DES ARTIKELS
================================================================================
