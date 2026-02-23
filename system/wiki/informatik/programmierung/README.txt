# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: Structure and Interpretation of Computer Programs (Abelson/Sussman), Clean Code (Martin), Design Patterns (GoF)

PROGRAMMIERUNG GRUNDLAGEN
=========================

Stand: 2026-02-05

DEFINITION
==========
Programmierung ist die Erstellung von Anweisungen (Code), die ein Computer
ausfuehren kann. Sie umfasst Problemanalyse, Algorithmenentwurf und die
Umsetzung in einer Programmiersprache.


PROGRAMMIERPARADIGMEN
=====================
Verschiedene Denkweisen und Ansaetze zur Problemloesung.

  Imperativ:
  ----------
    - Beschreibt WIE etwas berechnet wird
    - Sequenz von Anweisungen
    - Zustandsaenderungen durch Variablen
    - Beispiele: C, Pascal, BASIC

    # Imperativ: Summe berechnen
    summe = 0
    for i in range(1, 11):
        summe = summe + i
    print(summe)  # 55

  Objektorientiert (OOP):
  -----------------------
    - Daten und Funktionen in Objekten gekapselt
    - Vier Saeulen: Kapselung, Abstraktion, Vererbung, Polymorphie
    - Beispiele: Java, C++, Python, C#

    # Objektorientiert
    class Rechteck:
        def __init__(self, breite, hoehe):
            self._breite = breite
            self._hoehe = hoehe

        def flaeche(self):
            return self._breite * self._hoehe

    r = Rechteck(5, 3)
    print(r.flaeche())  # 15

  Funktional:
  -----------
    - Funktionen als First-Class Citizens
    - Unveraenderliche Daten (Immutability)
    - Keine Seiteneffekte (Pure Functions)
    - Beispiele: Haskell, Erlang, Clojure, F#

    # Funktional: Summe berechnen
    from functools import reduce
    summe = reduce(lambda acc, x: acc + x, range(1, 11), 0)
    print(summe)  # 55

  Deklarativ:
  -----------
    - Beschreibt WAS berechnet werden soll
    - Nicht WIE es berechnet wird
    - Beispiele: SQL, HTML, CSS, Prolog

    -- Deklarativ (SQL)
    SELECT SUM(wert) FROM tabelle WHERE kategorie = 'A';


DATENTYPEN
==========
Klassifizierung von Daten nach Art und Speicherung.

  Primitive Datentypen:
  ---------------------
    Integer     - Ganze Zahlen         (-1, 0, 42)
    Float       - Fliesskommazahlen    (3.14, -0.001)
    Boolean     - Wahrheitswerte       (True, False)
    Character   - Einzelne Zeichen     ('a', '5', '#')
    String      - Zeichenketten        ("Hello World")

  Zusammengesetzte Datentypen:
  ----------------------------
    Array/List       - Geordnete Sammlung      [1, 2, 3]
    Dictionary/Map   - Key-Value Paare         {"name": "Max", "age": 30}
    Set              - Eindeutige Elemente     {1, 2, 3}
    Tuple            - Unveraenderliche Liste  (1, "a", True)

  Typsysteme:
  -----------
    Statisch typisiert   - Typ zur Compilezeit (Java, C++, Rust)
    Dynamisch typisiert  - Typ zur Laufzeit (Python, JavaScript)
    Stark typisiert      - Keine impliziten Konvertierungen (Python)
    Schwach typisiert    - Implizite Konvertierungen (JavaScript)


VARIABLEN UND KONSTANTEN
========================

  Variablen:
  ----------
    - Benannter Speicherplatz fuer Werte
    - Wert kann sich aendern
    - Scope (Gueltigkeitsbereich) beachten

    # Python
    zaehler = 0           # Global
    def erhoehen():
        global zaehler    # Zugriff auf globale Variable
        zaehler += 1

  Konstanten:
  -----------
    - Wert aendert sich nicht
    - Verbessert Lesbarkeit und Wartbarkeit

    # Python (Konvention: GROSSBUCHSTABEN)
    MAX_VERSUCHE = 3
    PI = 3.14159

    // Java
    public static final int MAX_VERSUCHE = 3;

    // JavaScript (ES6+)
    const MAX_VERSUCHE = 3;

  Namenskonventionen:
  -------------------
    snake_case      - Python, Ruby (mein_variablenname)
    camelCase       - JavaScript, Java (meinVariablenname)
    PascalCase      - Klassen in vielen Sprachen (MeineKlasse)
    SCREAMING_SNAKE - Konstanten (MAXIMALER_WERT)


KONTROLLSTRUKTUREN
==================
Steuerung des Programmablaufs.

  Verzweigungen (Conditionals):
  -----------------------------
    # if-elif-else
    if temperatur < 0:
        print("Frost")
    elif temperatur < 15:
        print("Kuehl")
    elif temperatur < 25:
        print("Angenehm")
    else:
        print("Heiss")

    # Ternary Operator (Kurzform)
    status = "Erwachsen" if alter >= 18 else "Minderjaehrig"

    # Match/Switch (Python 3.10+)
    match status_code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case _:
            return "Unknown"

  Schleifen (Loops):
  ------------------
    # for-Schleife (bekannte Anzahl)
    for i in range(5):
        print(i)  # 0, 1, 2, 3, 4

    # while-Schleife (Bedingung)
    count = 0
    while count < 5:
        print(count)
        count += 1

    # Iteration ueber Collections
    for name in ["Anna", "Bob", "Clara"]:
        print(f"Hallo {name}")

    # break und continue
    for i in range(10):
        if i == 3:
            continue  # Ueberspringt 3
        if i == 7:
            break     # Beendet bei 7
        print(i)      # 0, 1, 2, 4, 5, 6


FUNKTIONEN UND PROZEDUREN
=========================

  Grundlagen:
  -----------
    # Funktion mit Rueckgabewert
    def addiere(a, b):
        """Addiert zwei Zahlen."""
        return a + b

    ergebnis = addiere(3, 5)  # 8

    # Prozedur (ohne Rueckgabe)
    def begruessung(name):
        print(f"Hallo {name}!")

  Parameter:
  ----------
    # Positional und Keyword Arguments
    def person_info(name, alter, stadt="Unbekannt"):
        return f"{name}, {alter}, aus {stadt}"

    person_info("Max", 30)                    # Positional
    person_info(alter=30, name="Max")         # Keyword
    person_info("Max", 30, stadt="Berlin")    # Gemischt

    # Variable Argumente
    def summe(*zahlen):           # *args (Tuple)
        return sum(zahlen)

    def config(**optionen):       # **kwargs (Dict)
        for key, val in optionen.items():
            print(f"{key}: {val}")

  Rekursion:
  ----------
    def fakultaet(n):
        if n <= 1:              # Basisfall
            return 1
        return n * fakultaet(n - 1)  # Rekursiver Aufruf

    print(fakultaet(5))  # 120 (5 * 4 * 3 * 2 * 1)

  Lambda-Funktionen:
  ------------------
    # Anonyme Einzeiler-Funktionen
    quadrat = lambda x: x ** 2
    print(quadrat(4))  # 16

    # Haeufig mit map, filter, sorted
    zahlen = [1, 2, 3, 4, 5]
    gerade = list(filter(lambda x: x % 2 == 0, zahlen))  # [2, 4]


FEHLERBEHANDLUNG
================
Umgang mit Ausnahmen und Fehlern.

  Try-Except (Python):
  --------------------
    try:
        ergebnis = 10 / 0
    except ZeroDivisionError:
        print("Division durch Null!")
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
    else:
        print(f"Ergebnis: {ergebnis}")  # Nur bei Erfolg
    finally:
        print("Wird immer ausgefuehrt")  # Cleanup

  Eigene Exceptions:
  ------------------
    class ValidationError(Exception):
        """Eigene Exception fuer Validierungsfehler."""
        pass

    def validiere_alter(alter):
        if alter < 0:
            raise ValidationError("Alter kann nicht negativ sein")
        return True

  Best Practices:
  ---------------
    - Spezifische Exceptions fangen, nicht generische
    - Exceptions fuer Ausnahmen, nicht fuer Kontrollfluss
    - Aussagekraeftige Fehlermeldungen
    - Logging nicht vergessen


DATENSTRUKTUREN
===============
Organisationsformen fuer Daten.

  Listen/Arrays:
  --------------
    - Geordnete Sammlung, Index-Zugriff
    - O(1) Zugriff, O(n) Suche

    liste = [1, 2, 3, 4, 5]
    liste.append(6)        # Hinzufuegen
    liste.pop()            # Entfernen (Ende)
    liste[0]               # Zugriff (1)
    liste[-1]              # Letztes Element (5)
    liste[1:3]             # Slicing ([2, 3])

  Dictionaries/Hash Maps:
  -----------------------
    - Key-Value Paare
    - O(1) Zugriff und Einfuegen (durchschnittlich)

    person = {
        "name": "Max",
        "alter": 30,
        "stadt": "Berlin"
    }
    person["name"]              # "Max"
    person.get("job", "N/A")    # "N/A" (Default)
    person.keys()               # Keys
    person.values()             # Values

  Stacks und Queues:
  ------------------
    # Stack (LIFO - Last In First Out)
    stack = []
    stack.append(1)  # Push
    stack.append(2)
    stack.pop()      # 2 (Pop)

    # Queue (FIFO - First In First Out)
    from collections import deque
    queue = deque()
    queue.append(1)     # Enqueue
    queue.append(2)
    queue.popleft()     # 1 (Dequeue)


ALGORITHMEN GRUNDLAGEN
======================

  Komplexitaet (Big-O):
  ---------------------
    O(1)        - Konstant (Array-Zugriff)
    O(log n)    - Logarithmisch (Binary Search)
    O(n)        - Linear (Liste durchsuchen)
    O(n log n)  - Linearithmisch (Merge Sort)
    O(n^2)      - Quadratisch (Bubble Sort)
    O(2^n)      - Exponentiell (Fibonacci naiv)

  Sortieralgorithmen:
  -------------------
    # Python: Timsort (O(n log n))
    sortiert = sorted([3, 1, 4, 1, 5, 9, 2, 6])
    liste.sort()  # In-place

  Suchalgorithmen:
  ----------------
    # Lineare Suche - O(n)
    def lineare_suche(liste, ziel):
        for i, element in enumerate(liste):
            if element == ziel:
                return i
        return -1

    # Binaere Suche - O(log n), sortierte Liste
    def binaere_suche(liste, ziel):
        links, rechts = 0, len(liste) - 1
        while links <= rechts:
            mitte = (links + rechts) // 2
            if liste[mitte] == ziel:
                return mitte
            elif liste[mitte] < ziel:
                links = mitte + 1
            else:
                rechts = mitte - 1
        return -1


OBJEKTORIENTIERUNG IM DETAIL
============================

  Die vier Saeulen:
  -----------------
    1. Kapselung (Encapsulation)
       - Daten und Methoden zusammenfassen
       - Zugriffskontrolle (public, private, protected)

    2. Abstraktion
       - Komplexitaet verbergen
       - Einfache Schnittstellen anbieten

    3. Vererbung (Inheritance)
       - Code wiederverwenden
       - Hierarchien aufbauen

    4. Polymorphie
       - Gleiche Schnittstelle, verschiedene Implementierungen

  Beispiel:
  ---------
    from abc import ABC, abstractmethod

    # Abstrakte Basisklasse
    class Tier(ABC):
        def __init__(self, name):
            self._name = name  # Protected

        @abstractmethod
        def laut(self):
            pass

        def vorstellen(self):
            return f"Ich bin {self._name}"

    # Konkrete Klassen
    class Hund(Tier):
        def laut(self):
            return "Wuff!"

    class Katze(Tier):
        def laut(self):
            return "Miau!"

    # Polymorphie in Aktion
    tiere = [Hund("Bello"), Katze("Minka")]
    for tier in tiere:
        print(f"{tier.vorstellen()}: {tier.laut()}")


CLEAN CODE PRINZIPIEN
=====================

  Namen:
  ------
    - Aussagekraeftige Namen (nicht x, temp, data)
    - Verben fuer Funktionen (berechne_summe)
    - Substantive fuer Klassen (Rechnung, Benutzer)

  Funktionen:
  -----------
    - Klein halten (max 20-30 Zeilen)
    - Eine Aufgabe pro Funktion
    - Wenige Parameter (max 3-4)
    - Keine Seiteneffekte wenn moeglich

  Kommentare:
  -----------
    - Code sollte selbsterklaerend sein
    - Kommentare erklaeren WARUM, nicht WAS
    - Docstrings fuer oeffentliche APIs

  DRY (Don't Repeat Yourself):
  ----------------------------
    - Keine Code-Duplikation
    - Wiederverwendbare Funktionen extrahieren

  KISS (Keep It Simple, Stupid):
  ------------------------------
    - Einfachste Loesung bevorzugen
    - Keine vorzeitige Optimierung


DEBUGGING UND TESTING
=====================

  Debugging:
  ----------
    # Print-Debugging
    print(f"DEBUG: variable = {variable}")

    # Python Debugger (pdb)
    import pdb; pdb.set_trace()  # Breakpoint

    # Logging (besser als print)
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Variable: %s", variable)

  Unit Testing:
  -------------
    import unittest

    def addiere(a, b):
        return a + b

    class TestAddiere(unittest.TestCase):
        def test_positive(self):
            self.assertEqual(addiere(2, 3), 5)

        def test_negative(self):
            self.assertEqual(addiere(-1, 1), 0)

        def test_null(self):
            self.assertEqual(addiere(0, 0), 0)

    if __name__ == '__main__':
        unittest.main()


SIEHE AUCH
==========
  wiki/python/                        Python-spezifisch
  wiki/java/                          Java-spezifisch
  wiki/informatik/software_architektur/  Design Patterns
  wiki/programmiersprachen_geschichte/   Sprachgeschichte
  wiki/informatik/devops/             Testing und CI/CD
