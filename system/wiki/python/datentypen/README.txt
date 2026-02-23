================================================================================
                            PYTHON DATENTYPEN
================================================================================

Portabilitaet:      UNIVERSAL
Zuletzt validiert:  2026-02-05
Naechste Pruefung:  2027-02-05
Quellen:            python.org/doc, PEP 3107, Real Python

Stand: 2026-02-05

================================================================================
                            INHALTSVERZEICHNIS
================================================================================

  1. Uebersicht Typsystem
  2. Numerische Typen
  3. Strings (Zeichenketten)
  4. Listen
  5. Tupel
  6. Dictionaries
  7. Sets (Mengen)
  8. None und Boolean
  9. Typkonvertierung
  10. Typueberpruefung
  11. BACH-Integration
  12. Best Practices

================================================================================
                          1. UEBERSICHT TYPSYSTEM
================================================================================

Python ist dynamisch typisiert: Der Typ einer Variable wird zur Laufzeit
bestimmt und kann sich aendern. Es gibt keine explizite Typdeklaration.

EINGEBAUTE DATENTYPEN
---------------------
  Kategorie        Typ         Beschreibung
  ---------        ---         ------------
  Numerisch        int         Ganze Zahlen (unbegrenzt)
                   float       Fliesskommazahlen
                   complex     Komplexe Zahlen

  Sequenzen        str         Zeichenketten (unveraenderbar)
                   list        Listen (veraenderbar)
                   tuple       Tupel (unveraenderbar)
                   range       Zahlenfolgen

  Mappings         dict        Schluessel-Wert-Paare

  Mengen           set         Veraenderbare Menge
                   frozenset   Unveraenderbare Menge

  Sonstige         bool        Wahrheitswerte
                   None        Kein Wert / Null
                   bytes       Binaerdaten
                   bytearray   Veraenderbare Binaerdaten

VERAENDERBAR VS. UNVERAENDERBAR
-------------------------------
  Unveraenderbar (immutable):  int, float, str, tuple, frozenset, bytes
  Veraenderbar (mutable):      list, dict, set, bytearray

  WICHTIG: Unveraenderbare Typen koennen als dict-Schluessel verwendet werden!

================================================================================
                          2. NUMERISCHE TYPEN
================================================================================

INTEGER (int)
-------------
  Ganze Zahlen ohne Groessenbeschraenkung.

    # Verschiedene Darstellungen
    dezimal = 42
    negativ = -17
    gross = 1_000_000_000       # Unterstriche fuer Lesbarkeit
    binaer = 0b1010             # Binaer (10)
    oktal = 0o17                # Oktal (15)
    hexadezimal = 0xFF          # Hexadezimal (255)

  Nuetzliche Funktionen:
    abs(-5)                     # 5 (Absolutwert)
    pow(2, 10)                  # 1024 (Potenz)
    divmod(17, 5)               # (3, 2) (Quotient, Rest)
    bin(42)                     # '0b101010'
    hex(255)                    # '0xff'
    oct(64)                     # '0o100'

FLOAT (Fliesskommazahlen)
-------------------------
  IEEE 754 Double Precision (64 Bit).

    pi = 3.14159
    klein = 2.5e-10             # Wissenschaftliche Notation
    gross = 1.5e8               # 150000000.0
    unendlich = float('inf')    # Positiv unendlich
    neg_unendlich = float('-inf')
    keine_zahl = float('nan')   # Not a Number

  ACHTUNG bei Vergleichen:
    0.1 + 0.2 == 0.3            # False! (Fliesskommaungenauigkeit)
    abs((0.1 + 0.2) - 0.3) < 1e-9  # True (Epsilon-Vergleich)

  Fuer exakte Berechnungen:
    from decimal import Decimal
    Decimal('0.1') + Decimal('0.2') == Decimal('0.3')  # True

COMPLEX (Komplexe Zahlen)
-------------------------
    z = 3 + 4j
    z.real                      # 3.0 (Realteil)
    z.imag                      # 4.0 (Imaginaerteil)
    abs(z)                      # 5.0 (Betrag)
    z.conjugate()               # (3-4j) (Konjugiert)

================================================================================
                        3. STRINGS (ZEICHENKETTEN)
================================================================================

ERSTELLUNG
----------
    # Einfache und doppelte Anfuehrungszeichen
    s1 = 'Hallo'
    s2 = "Welt"

    # Mehrzeilig
    s3 = '''Zeile 1
    Zeile 2
    Zeile 3'''

    # Raw-String (keine Escape-Sequenzen)
    pfad = r"C:\Users\Name\Dokumente"

    # F-String (formatiert)
    name = "Alice"
    begruessung = f"Hallo, {name}!"

ESCAPE-SEQUENZEN
----------------
    \n      Zeilenumbruch
    \t      Tabulator
    \\      Backslash
    \'      Einfaches Anfuehrungszeichen
    \"      Doppeltes Anfuehrungszeichen
    \r      Wagenruecklauf
    \0      Null-Zeichen

INDEXIERUNG UND SLICING
-----------------------
    text = "Python"

    # Einzelne Zeichen (Index beginnt bei 0)
    text[0]                     # 'P'
    text[-1]                    # 'n' (von hinten)

    # Slicing [start:stop:step]
    text[0:3]                   # 'Pyt'
    text[2:]                    # 'thon'
    text[:3]                    # 'Pyt'
    text[::2]                   # 'Pto' (jedes zweite)
    text[::-1]                  # 'nohtyP' (rueckwaerts)

WICHTIGE STRING-METHODEN
------------------------
    s = "  Hallo Welt  "

    # Gross-/Kleinschreibung
    s.upper()                   # '  HALLO WELT  '
    s.lower()                   # '  hallo welt  '
    s.title()                   # '  Hallo Welt  '
    s.capitalize()              # '  hallo welt  '
    s.swapcase()                # '  hALLO wELT  '

    # Whitespace entfernen
    s.strip()                   # 'Hallo Welt'
    s.lstrip()                  # 'Hallo Welt  '
    s.rstrip()                  # '  Hallo Welt'

    # Suchen und Ersetzen
    s.find("Welt")              # 8 (Index, -1 wenn nicht gefunden)
    s.index("Welt")             # 8 (wirft Fehler wenn nicht gefunden)
    s.count("l")                # 3
    s.replace("Welt", "Python") # '  Hallo Python  '

    # Pruefen
    "hallo".isalpha()           # True (nur Buchstaben)
    "123".isdigit()             # True (nur Ziffern)
    "abc123".isalnum()          # True (Buchstaben und Ziffern)
    "  ".isspace()              # True (nur Whitespace)
    "Hallo".startswith("Ha")    # True
    "Hallo".endswith("lo")      # True

    # Teilen und Verbinden
    "a,b,c".split(",")          # ['a', 'b', 'c']
    "Zeile1\nZeile2".splitlines()  # ['Zeile1', 'Zeile2']
    "-".join(['a', 'b', 'c'])   # 'a-b-c'

FORMATIERUNG
------------
    name = "Alice"
    alter = 30

    # F-Strings (empfohlen, Python 3.6+)
    f"Name: {name}, Alter: {alter}"

    # Format-Methode
    "Name: {}, Alter: {}".format(name, alter)
    "Name: {n}, Alter: {a}".format(n=name, a=alter)

    # Formatspezifikationen
    f"{3.14159:.2f}"            # '3.14' (2 Dezimalstellen)
    f"{42:05d}"                 # '00042' (5 Stellen, fuehrende Nullen)
    f"{42:>10}"                 # '        42' (rechtsbuendig)
    f"{42:<10}"                 # '42        ' (linksbuendig)
    f"{42:^10}"                 # '    42    ' (zentriert)

================================================================================
                              4. LISTEN
================================================================================

ERSTELLUNG
----------
    # Leere Liste
    leer = []
    leer = list()

    # Mit Elementen
    zahlen = [1, 2, 3, 4, 5]
    gemischt = [1, "zwei", 3.0, True]
    verschachtelt = [[1, 2], [3, 4], [5, 6]]

    # List Comprehension
    quadrate = [x**2 for x in range(10)]
    gerade = [x for x in range(20) if x % 2 == 0]

ZUGRIFF UND SLICING
-------------------
    liste = ['a', 'b', 'c', 'd', 'e']

    liste[0]                    # 'a'
    liste[-1]                   # 'e'
    liste[1:3]                  # ['b', 'c']
    liste[::2]                  # ['a', 'c', 'e']

WICHTIGE LISTEN-METHODEN
------------------------
    liste = [1, 2, 3]

    # Hinzufuegen
    liste.append(4)             # [1, 2, 3, 4]
    liste.insert(0, 0)          # [0, 1, 2, 3, 4]
    liste.extend([5, 6])        # [0, 1, 2, 3, 4, 5, 6]
    liste += [7, 8]             # [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Entfernen
    liste.pop()                 # Entfernt und gibt letztes Element zurueck
    liste.pop(0)                # Entfernt Element an Index 0
    liste.remove(3)             # Entfernt erstes Vorkommen von 3
    del liste[1]                # Loescht Element an Index 1
    liste.clear()               # Leert die gesamte Liste

    # Suchen
    [1, 2, 3, 2].index(2)       # 1 (erster Index)
    [1, 2, 3, 2].count(2)       # 2 (Anzahl)

    # Sortieren
    liste.sort()                # In-place aufsteigend
    liste.sort(reverse=True)    # In-place absteigend
    sorted(liste)               # Neue sortierte Liste
    liste.reverse()             # In-place umkehren

    # Kopieren
    kopie = liste.copy()        # Flache Kopie
    kopie = liste[:]            # Ebenfalls flache Kopie

    import copy
    tiefe_kopie = copy.deepcopy(liste)  # Tiefe Kopie

================================================================================
                              5. TUPEL
================================================================================

ERSTELLUNG
----------
    # Mit Klammern
    punkt = (10, 20)
    rgb = (255, 128, 0)

    # Ohne Klammern (Tuple Packing)
    koordinaten = 10, 20, 30

    # Einzelnes Element (Komma erforderlich!)
    einzeln = (42,)             # Tupel
    kein_tupel = (42)           # Nur int!

    # Aus Iterable
    tupel = tuple([1, 2, 3])

UNPACKING
---------
    punkt = (10, 20, 30)

    # Vollstaendiges Unpacking
    x, y, z = punkt

    # Mit Rest (*-Operator)
    erste, *rest = [1, 2, 3, 4, 5]   # erste=1, rest=[2,3,4,5]
    erste, *mitte, letzte = [1, 2, 3, 4, 5]  # erste=1, mitte=[2,3,4], letzte=5

NAMED TUPLES
------------
    from collections import namedtuple

    Person = namedtuple('Person', ['name', 'alter', 'stadt'])
    alice = Person('Alice', 30, 'Berlin')

    print(alice.name)           # 'Alice'
    print(alice[0])             # 'Alice'
    print(alice._asdict())      # {'name': 'Alice', 'alter': 30, 'stadt': 'Berlin'}

TUPEL VS. LISTE
---------------
  Tupel verwenden wenn:
    - Daten unveraenderbar sein sollen
    - Als Dictionary-Schluessel benoetigt
    - Heterogene Daten (unterschiedliche Bedeutung)
    - Rueckgabe mehrerer Werte aus Funktionen

  Listen verwenden wenn:
    - Daten veraendert werden muessen
    - Homogene Daten (gleiche Art)
    - Dynamische Groesse benoetigt

================================================================================
                            6. DICTIONARIES
================================================================================

ERSTELLUNG
----------
    # Mit geschweiften Klammern
    person = {"name": "Alice", "alter": 30}

    # Mit dict()
    person = dict(name="Alice", alter=30)

    # Aus Liste von Tupeln
    person = dict([("name", "Alice"), ("alter", 30)])

    # Dictionary Comprehension
    quadrate = {x: x**2 for x in range(6)}
    # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

ZUGRIFF
-------
    person = {"name": "Alice", "alter": 30}

    person["name"]              # 'Alice'
    person["beruf"]             # KeyError!
    person.get("beruf")         # None (kein Fehler)
    person.get("beruf", "unbekannt")  # 'unbekannt' (Standardwert)

WICHTIGE DICT-METHODEN
----------------------
    d = {"a": 1, "b": 2}

    # Hinzufuegen/Aendern
    d["c"] = 3                  # Hinzufuegen
    d["a"] = 10                 # Aendern
    d.update({"d": 4, "e": 5})  # Mehrere hinzufuegen

    # Entfernen
    del d["a"]                  # Loeschen (KeyError wenn nicht vorhanden)
    d.pop("b")                  # Entfernen und zurueckgeben
    d.pop("x", None)            # Mit Standardwert
    d.popitem()                 # Letztes Paar entfernen
    d.clear()                   # Alles loeschen

    # Iteration
    d = {"a": 1, "b": 2, "c": 3}
    d.keys()                    # dict_keys(['a', 'b', 'c'])
    d.values()                  # dict_values([1, 2, 3])
    d.items()                   # dict_items([('a', 1), ('b', 2), ('c', 3)])

    for key in d:
        print(key, d[key])

    for key, value in d.items():
        print(key, value)

    # Pruefen
    "a" in d                    # True
    "x" not in d                # True

DICTIONARY-MERGE (PYTHON 3.9+)
------------------------------
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}

    merged = d1 | d2            # {'a': 1, 'b': 3, 'c': 4}
    d1 |= d2                    # In-place merge

================================================================================
                            7. SETS (MENGEN)
================================================================================

ERSTELLUNG
----------
    # Mit geschweiften Klammern
    zahlen = {1, 2, 3, 4, 5}

    # ACHTUNG: Leere Menge nicht mit {}!
    leer = set()                # Richtig
    leer = {}                   # Das ist ein leeres Dict!

    # Aus Iterable (entfernt Duplikate)
    buchstaben = set("mississippi")  # {'m', 'i', 's', 'p'}

    # Set Comprehension
    quadrate = {x**2 for x in range(10)}

MENGENOPERATIONEN
-----------------
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}

    # Vereinigung (Union)
    a | b                       # {1, 2, 3, 4, 5, 6}
    a.union(b)

    # Schnittmenge (Intersection)
    a & b                       # {3, 4}
    a.intersection(b)

    # Differenz
    a - b                       # {1, 2}
    a.difference(b)

    # Symmetrische Differenz
    a ^ b                       # {1, 2, 5, 6}
    a.symmetric_difference(b)

    # Teilmengen-Pruefung
    {1, 2}.issubset({1, 2, 3})       # True
    {1, 2, 3}.issuperset({1, 2})     # True
    {1, 2}.isdisjoint({3, 4})        # True (keine gemeinsamen)

SET-METHODEN
------------
    s = {1, 2, 3}

    s.add(4)                    # Hinzufuegen
    s.update([5, 6])            # Mehrere hinzufuegen
    s.remove(1)                 # Entfernen (KeyError wenn nicht vorhanden)
    s.discard(10)               # Entfernen (kein Fehler)
    s.pop()                     # Beliebiges Element entfernen
    s.clear()                   # Alles loeschen

FROZENSET
---------
  Unveraenderbare Menge (kann als Dict-Schluessel verwendet werden):

    fs = frozenset([1, 2, 3])
    # fs.add(4)                 # AttributeError!

================================================================================
                          8. NONE UND BOOLEAN
================================================================================

NONE
----
  Repraesentiert "kein Wert" oder "null":

    ergebnis = None

    # Richtige Pruefung mit "is"
    if ergebnis is None:
        print("Kein Ergebnis")

    if ergebnis is not None:
        print("Ergebnis vorhanden")

    # NICHT mit == pruefen (funktioniert, aber nicht idiomatisch)

BOOLEAN (BOOL)
--------------
    wahr = True
    falsch = False

    # Boolean-Operationen
    True and False              # False
    True or False               # True
    not True                    # False

TRUTHY UND FALSY
----------------
  In Bedingungen werden Werte automatisch zu bool konvertiert.

  FALSY (ergeben False):
    - None
    - False
    - 0, 0.0, 0j (numerische Nullen)
    - '', "", '''''' (leere Strings)
    - [], (), {} (leere Container)
    - set(), frozenset()

  TRUTHY (ergeben True):
    - Alles andere!

  Beispiele:
    if []:                      # Wird nicht ausgefuehrt
        print("Nie")

    if [1, 2, 3]:               # Wird ausgefuehrt
        print("Liste nicht leer")

    # Idiomatische Pruefung auf leere Container
    liste = []
    if not liste:
        print("Liste ist leer")

================================================================================
                          9. TYPKONVERTIERUNG
================================================================================

EXPLIZITE KONVERTIERUNG
-----------------------
    # Zu Integer
    int("42")                   # 42
    int(3.9)                    # 3 (abgeschnitten, nicht gerundet)
    int("1010", 2)              # 10 (Binaer zu Dezimal)

    # Zu Float
    float("3.14")               # 3.14
    float(42)                   # 42.0

    # Zu String
    str(42)                     # '42'
    str(3.14)                   # '3.14'
    str([1, 2, 3])              # '[1, 2, 3]'

    # Zu Boolean
    bool(0)                     # False
    bool(1)                     # True
    bool("")                    # False
    bool("text")                # True

    # Zu Liste
    list("abc")                 # ['a', 'b', 'c']
    list((1, 2, 3))             # [1, 2, 3]
    list({1, 2, 3})             # [1, 2, 3] (Reihenfolge nicht garantiert)

    # Zu Tupel
    tuple([1, 2, 3])            # (1, 2, 3)

    # Zu Set
    set([1, 2, 2, 3])           # {1, 2, 3}

    # Zu Dict (aus Paaren)
    dict([("a", 1), ("b", 2)])  # {'a': 1, 'b': 2}

================================================================================
                          10. TYPUEBERPRUEFUNG
================================================================================

TYPE() FUNKTION
---------------
    type(42)                    # <class 'int'>
    type("hallo")               # <class 'str'>
    type([1, 2])                # <class 'list'>

    type(42) == int             # True
    type("hallo") == str        # True

ISINSTANCE() FUNKTION
---------------------
  Bevorzugte Methode (beruecksichtigt Vererbung):

    isinstance(42, int)         # True
    isinstance("hallo", str)    # True
    isinstance([1, 2], list)    # True

    # Mehrere Typen pruefen
    isinstance(42, (int, float))     # True
    isinstance("hallo", (int, str))  # True

TYPE HINTS (PYTHON 3.5+)
------------------------
    def addiere(a: int, b: int) -> int:
        return a + b

    name: str = "Alice"
    zahlen: list[int] = [1, 2, 3]
    person: dict[str, any] = {"name": "Alice", "alter": 30}

    # Optional
    from typing import Optional
    def finde(name: str) -> Optional[str]:
        return None  # oder gefundenen Wert

================================================================================
                          11. BACH-INTEGRATION
================================================================================

DATENTYPEN IN BACH-SCRIPTS
--------------------------
  Python-Datentypen eignen sich ideal fuer BACH-Automatisierung:

    # config_parser.py
    #!/usr/bin/env python3
    """BACH Konfigurationsparser"""

    import json
    from pathlib import Path

    def lade_config(pfad: str) -> dict:
        """Laedt JSON-Konfiguration und gibt dict zurueck"""
        config_path = Path(pfad)
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {}

    def speichere_config(pfad: str, config: dict) -> None:
        """Speichert dict als JSON"""
        with open(pfad, 'w') as f:
            json.dump(config, f, indent=2)

DATEN ZWISCHEN BACH UND PYTHON
------------------------------
  JSON ist das bevorzugte Austauschformat:

    # Python -> BACH (Ausgabe als JSON)
    import json
    daten = {"status": "ok", "werte": [1, 2, 3]}
    print(json.dumps(daten))

    # BACH kann die Ausgabe parsen und weiterverwenden

================================================================================
                          12. BEST PRACTICES
================================================================================

UNVERAENDERBARE TYPEN BEVORZUGEN
--------------------------------
  Wenn moeglich, unveraenderbare Typen verwenden:
    - Tupel statt Listen (wenn Inhalt fix)
    - frozenset statt set (wenn keine Aenderung noetig)
    - Vermeidet unbeabsichtigte Seiteneffekte

LEERE CONTAINER PRUEFEN
-----------------------
    # SCHLECHT
    if len(liste) == 0:
        pass

    # GUT
    if not liste:
        pass

NONE-PRUEFUNG
-------------
    # SCHLECHT
    if x == None:
        pass

    # GUT
    if x is None:
        pass

DICTIONARY-ZUGRIFF
------------------
    # SCHLECHT (KeyError-Risiko)
    wert = d["key"]

    # BESSER (mit Standardwert)
    wert = d.get("key", "standard")

    # ODER mit Pruefung
    if "key" in d:
        wert = d["key"]

================================================================================
                              SIEHE AUCH
================================================================================

  wiki/python/grundlagen/
    -> Python-Grundlagen, Installation, Syntax

  wiki/python/kontrollstrukturen/
    -> if/else, for, while, try/except

  wiki/python/funktionen/
    -> Funktionsdefinition, Lambda, Decorators

  wiki/informatik/datenstrukturen/
    -> Allgemeine Datenstrukturen, Algorithmen

  wiki/python/standardbibliothek/collections/
    -> defaultdict, Counter, OrderedDict, deque

================================================================================
                         ENDE DES ARTIKELS
================================================================================
