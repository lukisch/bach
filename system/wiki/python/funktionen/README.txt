================================================================================
                           PYTHON FUNKTIONEN
================================================================================

Portabilitaet: UNIVERSAL
Zuletzt validiert: 2026-02-05
Naechste Pruefung: 2027-02-05
Quellen: Python 3.12 Dokumentation, PEP 3107 (Annotations), PEP 484 (Type Hints)

Stand: 2026-02-05

================================================================================
                              EINFUEHRUNG
================================================================================

Funktionen sind fundamentale Bausteine in Python und ermoeglichen die
Strukturierung von Code in wiederverwendbare, logische Einheiten. Sie folgen
dem DRY-Prinzip (Don't Repeat Yourself) und verbessern die Lesbarkeit sowie
Wartbarkeit von Programmen erheblich.

Python unterstuetzt verschiedene Funktionsparadigmen:
  - Regulaere Funktionen (def)
  - Anonyme Funktionen (lambda)
  - Generatorfunktionen (yield)
  - Asynchrone Funktionen (async def)
  - Rekursive Funktionen

================================================================================
                           FUNKTIONSDEFINITION
================================================================================

GRUNDSTRUKTUR
-------------
  def funktionsname(parameter):
      '''Docstring: Beschreibt die Funktion.

      Args:
          parameter: Beschreibung des Parameters

      Returns:
          Beschreibung des Rueckgabewerts
      '''
      # Funktionskoerper
      ergebnis = verarbeitung(parameter)
      return ergebnis

BEISPIEL: Einfache Funktion
---------------------------
  def berechne_kreisflaeche(radius):
      '''Berechnet die Flaeche eines Kreises.

      Args:
          radius: Der Radius des Kreises (positiver Wert)

      Returns:
          Die Flaeche als float

      Raises:
          ValueError: Wenn radius negativ ist
      '''
      import math
      if radius < 0:
          raise ValueError("Radius darf nicht negativ sein")
      return math.pi * radius ** 2

  # Aufruf
  flaeche = berechne_kreisflaeche(5)
  print(f"Flaeche: {flaeche:.2f}")  # Ausgabe: Flaeche: 78.54

================================================================================
                              PARAMETER
================================================================================

POSITIONAL PARAMETERS
---------------------
  Parameter werden in der Reihenfolge ihrer Definition uebergeben.

  def erstelle_benutzer(vorname, nachname, alter):
      return {
          'vorname': vorname,
          'nachname': nachname,
          'alter': alter
      }

  # Aufruf mit positionalen Argumenten
  user = erstelle_benutzer("Max", "Mustermann", 30)

DEFAULT-PARAMETER
-----------------
  Parameter mit Standardwerten, falls beim Aufruf nicht angegeben.
  WICHTIG: Default-Parameter muessen NACH positionalen Parametern stehen.

  def erstelle_benutzer(vorname, nachname, alter=18, aktiv=True):
      return {
          'vorname': vorname,
          'nachname': nachname,
          'alter': alter,
          'aktiv': aktiv
      }

  # Aufrufe
  user1 = erstelle_benutzer("Max", "Mustermann")           # alter=18, aktiv=True
  user2 = erstelle_benutzer("Anna", "Schmidt", 25)         # aktiv=True
  user3 = erstelle_benutzer("Tom", "Weber", 40, False)     # alle explizit

  ACHTUNG - Mutable Default Arguments:
  ------------------------------------
  FALSCH:
    def append_to(element, liste=[]):  # GEFAEHRLICH!
        liste.append(element)
        return liste
    # Die Liste wird zwischen Aufrufen geteilt!

  RICHTIG:
    def append_to(element, liste=None):
        if liste is None:
            liste = []
        liste.append(element)
        return liste

KEYWORD-ARGUMENTE
-----------------
  Argumente werden mit Namen uebergeben (Reihenfolge egal).

  user = erstelle_benutzer(
      nachname="Mueller",
      vorname="Lisa",
      aktiv=False,
      alter=28
  )

*ARGS - Beliebig viele positionale Argumente
--------------------------------------------
  def summe(*zahlen):
      '''Summiert beliebig viele Zahlen.'''
      total = 0
      for zahl in zahlen:
          total += zahl
      return total

  # Aufrufe
  print(summe(1, 2, 3))           # 6
  print(summe(10, 20, 30, 40))    # 100
  print(summe())                   # 0

  # Liste entpacken mit *
  werte = [1, 2, 3, 4, 5]
  print(summe(*werte))             # 15

**KWARGS - Beliebige Keyword-Argumente
--------------------------------------
  def konfiguriere(**optionen):
      '''Verarbeitet beliebige Konfigurationsoptionen.'''
      for schluessel, wert in optionen.items():
          print(f"{schluessel} = {wert}")

  # Aufruf
  konfiguriere(
      debug=True,
      sprache="de",
      max_verbindungen=100
  )

  # Dictionary entpacken mit **
  config = {'timeout': 30, 'retry': 3}
  konfiguriere(**config)

KOMBINIERTE PARAMETER
---------------------
  Die Reihenfolge muss eingehalten werden:
  1. Positionale Parameter
  2. *args
  3. Keyword-only Parameter
  4. **kwargs

  def komplexe_funktion(a, b, *args, option=None, **kwargs):
      print(f"a={a}, b={b}")
      print(f"args={args}")
      print(f"option={option}")
      print(f"kwargs={kwargs}")

  komplexe_funktion(1, 2, 3, 4, option="test", extra="wert")
  # a=1, b=2
  # args=(3, 4)
  # option=test
  # kwargs={'extra': 'wert'}

POSITIONAL-ONLY UND KEYWORD-ONLY (Python 3.8+)
----------------------------------------------
  def spezielle_funktion(pos_only, /, standard, *, kw_only):
      '''
      pos_only:  Muss positional uebergeben werden (vor /)
      standard:  Kann positional oder keyword sein
      kw_only:   Muss als keyword uebergeben werden (nach *)
      '''
      return pos_only + standard + kw_only

  # Korrekte Aufrufe
  spezielle_funktion(1, 2, kw_only=3)
  spezielle_funktion(1, standard=2, kw_only=3)

  # Fehlerhafte Aufrufe
  # spezielle_funktion(pos_only=1, standard=2, kw_only=3)  # TypeError
  # spezielle_funktion(1, 2, 3)                            # TypeError

================================================================================
                             RETURN-WERTE
================================================================================

EINZELNER RUECKGABEWERT
-----------------------
  def quadrat(x):
      return x ** 2

MEHRERE RUECKGABEWERTE (Tuple)
------------------------------
  def teile_mit_rest(dividend, divisor):
      quotient = dividend // divisor
      rest = dividend % divisor
      return quotient, rest  # Gibt Tuple zurueck

  # Entpacken
  q, r = teile_mit_rest(17, 5)
  print(f"17 / 5 = {q} Rest {r}")  # 17 / 5 = 3 Rest 2

KEIN RETURN (implizit None)
---------------------------
  def drucke_nachricht(msg):
      print(msg)
      # Kein explizites return -> gibt None zurueck

  ergebnis = drucke_nachricht("Hallo")
  print(ergebnis)  # None

EARLY RETURN
------------
  def finde_index(liste, element):
      for i, item in enumerate(liste):
          if item == element:
              return i  # Beendet Funktion sofort
      return -1  # Element nicht gefunden

================================================================================
                          LAMBDA-FUNKTIONEN
================================================================================

Anonyme Funktionen fuer einfache, einzeilige Operationen.

SYNTAX
------
  lambda parameter: ausdruck

BEISPIELE
---------
  # Einfache Lambda
  quadrat = lambda x: x ** 2
  print(quadrat(5))  # 25

  # Mehrere Parameter
  addiere = lambda a, b: a + b
  print(addiere(3, 4))  # 7

  # Mit Default-Werten
  greet = lambda name, greeting="Hallo": f"{greeting}, {name}!"

TYPISCHE ANWENDUNGEN
--------------------
  # Sortieren mit Key-Funktion
  personen = [
      {'name': 'Anna', 'alter': 30},
      {'name': 'Max', 'alter': 25},
      {'name': 'Lisa', 'alter': 35}
  ]
  nach_alter = sorted(personen, key=lambda p: p['alter'])

  # Filter
  zahlen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  gerade = list(filter(lambda x: x % 2 == 0, zahlen))
  # [2, 4, 6, 8, 10]

  # Map
  quadrate = list(map(lambda x: x ** 2, zahlen))
  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

  # Reduce
  from functools import reduce
  produkt = reduce(lambda a, b: a * b, zahlen)
  # 3628800

================================================================================
                              SCOPE (GELTUNGSBEREICH)
================================================================================

LEGB-REGEL
----------
  Python sucht Variablen in dieser Reihenfolge:
  L - Local:     Innerhalb der aktuellen Funktion
  E - Enclosing: In umschliessenden Funktionen (Closures)
  G - Global:    Auf Modulebene
  B - Built-in:  Python-interne Namen

BEISPIEL
--------
  x = "global"  # Global

  def aeussere():
      x = "enclosing"  # Enclosing

      def innere():
          x = "local"  # Local
          print(x)     # local

      innere()
      print(x)         # enclosing

  aeussere()
  print(x)             # global

GLOBAL KEYWORD
--------------
  zaehler = 0

  def erhoehe():
      global zaehler  # Zugriff auf globale Variable
      zaehler += 1

  erhoehe()
  erhoehe()
  print(zaehler)  # 2

NONLOCAL KEYWORD
----------------
  def aeussere():
      zaehler = 0

      def erhoehe():
          nonlocal zaehler  # Zugriff auf Enclosing-Variable
          zaehler += 1

      erhoehe()
      erhoehe()
      return zaehler

  print(aeussere())  # 2

================================================================================
                              TYPE HINTS
================================================================================

Type Hints verbessern die Dokumentation und ermoeglichen statische Analyse.

GRUNDLEGENDE TYPEN
------------------
  def addiere(a: int, b: int) -> int:
      return a + b

  def greet(name: str) -> str:
      return f"Hallo, {name}!"

  def ist_gerade(zahl: int) -> bool:
      return zahl % 2 == 0

KOMPLEXE TYPEN
--------------
  from typing import List, Dict, Tuple, Optional, Union, Callable

  def verarbeite_liste(zahlen: List[int]) -> List[int]:
      return [x * 2 for x in zahlen]

  def erstelle_mapping(daten: List[str]) -> Dict[str, int]:
      return {item: len(item) for item in daten}

  def hole_koordinaten() -> Tuple[float, float]:
      return (52.52, 13.405)

  def finde_benutzer(id: int) -> Optional[Dict]:
      # Gibt Dict oder None zurueck
      pass

  def verarbeite(wert: Union[int, str]) -> str:
      return str(wert)

  def fuehre_aus(callback: Callable[[int, int], int], a: int, b: int) -> int:
      return callback(a, b)

PYTHON 3.10+ SYNTAX
-------------------
  # Neue Union-Syntax mit |
  def verarbeite(wert: int | str) -> str:
      return str(wert)

  # list, dict etc. direkt verwendbar
  def summe(zahlen: list[int]) -> int:
      return sum(zahlen)

================================================================================
                         BACH-INTEGRATION
================================================================================

BACH-SKRIPTE MIT FUNKTIONEN
---------------------------
  In BACH-Automatisierungen koennen Python-Funktionen als Module organisiert
  werden fuer bessere Wiederverwendbarkeit.

  Beispiel: system/utils/helper_functions.py
  ------------------------------------------
  '''BACH Hilfsfunktionen'''

  def parse_bach_config(config_path: str) -> dict:
      '''Liest BACH-Konfigurationsdatei.'''
      import json
      with open(config_path, 'r', encoding='utf-8') as f:
          return json.load(f)

  def log_bach_event(event: str, level: str = "INFO") -> None:
      '''Protokolliert BACH-Events.'''
      from datetime import datetime
      timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      print(f"[{timestamp}] [{level}] {event}")

  def validate_input(*args, **kwargs) -> bool:
      '''Validiert Benutzereingaben fuer BACH-Workflows.'''
      for arg in args:
          if arg is None or (isinstance(arg, str) and not arg.strip()):
              return False
      return True

BEST PRACTICES FUER BACH
------------------------
  1. Funktionen dokumentieren mit Docstrings
  2. Type Hints fuer bessere IDE-Unterstuetzung
  3. Fehlerbehandlung mit try/except
  4. Logging statt print() in Produktionscode
  5. Konfiguration als Parameter, nicht hardcoded

================================================================================
                           BEST PRACTICES
================================================================================

  1. KISS-Prinzip: Funktionen sollten eine Aufgabe erledigen
  2. Aussagekraeftige Namen: berechne_steuer() statt calc()
  3. Docstrings schreiben: Mindestens Args, Returns, Raises
  4. Type Hints nutzen: Verbessert Lesbarkeit und ermoeglicht Checks
  5. Seiteneffekte vermeiden: Pure Functions bevorzugen
  6. Mutable Defaults vermeiden: None statt [] oder {}
  7. Maximale Parameteranzahl: 5-7 Parameter, darueber hinaus Refactoring

================================================================================
                              SIEHE AUCH
================================================================================

  wiki/python/decorators/     - Funktionen erweitern
  wiki/python/generators/     - Generator-Funktionen mit yield
  wiki/python/oop/            - Methoden in Klassen
  wiki/python/closures/       - Funktionen mit Zustand
  wiki/python/async/          - Asynchrone Funktionen

================================================================================
                           VERSIONSVERLAUF
================================================================================

  2026-02-05  Vollstaendiger Artikel erstellt
  2026-01-24  Initialer Stub angelegt

================================================================================
