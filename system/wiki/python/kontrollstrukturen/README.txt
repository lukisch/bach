# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: docs.python.org/3/tutorial/controlflow.html, PEP 634, PEP 636

PYTHON KONTROLLSTRUKTUREN
=========================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

EINFUEHRUNG
===========

Kontrollstrukturen sind fundamentale Bausteine jeder Programmiersprache.
Sie steuern den Programmfluss und bestimmen, welche Codeabschnitte wann
und wie oft ausgefuehrt werden. Python bietet elegante und gut lesbare
Kontrollstrukturen, die dem Prinzip "Readability counts" folgen.

Python unterscheidet drei Hauptkategorien:
  1. Bedingte Anweisungen (if/elif/else, match)
  2. Schleifen (for, while)
  3. Comprehensions (Listen-, Dict-, Set-, Generator-Comprehensions)


BEDINGTE ANWEISUNGEN
====================

IF / ELIF / ELSE
----------------

Die if-Anweisung ist die grundlegendste Kontrollstruktur. Sie fuehrt
Code nur aus, wenn eine Bedingung wahr (True) ist.

Syntax:
  if bedingung:
      # Code wenn bedingung True
  elif andere_bedingung:
      # Code wenn andere_bedingung True
  else:
      # Code wenn keine Bedingung True

Beispiel - Notenberechnung:
  def bewerte_note(punkte):
      """Bewertet Punkte nach deutschem Notensystem."""
      if punkte >= 90:
          return "sehr gut (1)"
      elif punkte >= 80:
          return "gut (2)"
      elif punkte >= 70:
          return "befriedigend (3)"
      elif punkte >= 60:
          return "ausreichend (4)"
      elif punkte >= 50:
          return "mangelhaft (5)"
      else:
          return "ungenuegend (6)"

  # Anwendung
  print(bewerte_note(85))  # Ausgabe: gut (2)

Wichtige Hinweise:
  - Einrueckung ist in Python syntaktisch relevant (4 Leerzeichen Standard)
  - elif und else sind optional
  - Beliebig viele elif-Bloecke moeglich
  - Nur ein else-Block am Ende erlaubt


WAHRHEITSWERTE IN PYTHON
------------------------

Python wertet folgende Werte als False (Falsy):
  - False, None
  - Numerische Nullwerte: 0, 0.0, 0j
  - Leere Sequenzen: '', [], (), {}
  - Leere Sets: set()
  - Objekte mit __bool__() -> False oder __len__() -> 0

Alles andere ist True (Truthy).

Beispiel:
  daten = []

  # Pythonic
  if daten:
      print("Daten vorhanden")
  else:
      print("Keine Daten")

  # Nicht pythonic (vermeiden)
  if len(daten) > 0:  # unnoetig explizit
      print("Daten vorhanden")


TERNARY OPERATOR (CONDITIONAL EXPRESSION)
-----------------------------------------

Kurzform fuer einfache if-else-Zuweisungen in einer Zeile.

Syntax:
  ergebnis = wert_wenn_true if bedingung else wert_wenn_false

Beispiele:
  # Einfache Zuweisung
  status = "aktiv" if benutzer.ist_eingeloggt else "inaktiv"

  # Mit Funktionsaufrufen
  text = gross_schreiben(s) if formatierung else s

  # Verschachtelt (vermeiden - schlechte Lesbarkeit)
  note = "A" if punkte >= 90 else "B" if punkte >= 80 else "C"

  # Besser lesbar mit Dictionary
  noten = {90: "A", 80: "B", 70: "C"}
  note = next((v for k, v in noten.items() if punkte >= k), "F")


MATCH STATEMENT (PYTHON 3.10+)
------------------------------

Structural Pattern Matching - aehnlich zu switch/case in anderen Sprachen,
aber wesentlich maechiger durch Pattern Matching.

Grundsyntax:
  match variable:
      case muster1:
          # Code
      case muster2:
          # Code
      case _:
          # Default (Wildcard)

Beispiel - Befehlsverarbeitung:
  def verarbeite_befehl(befehl):
      match befehl.split():
          case ["quit"]:
              return "Programm beenden"
          case ["load", dateiname]:
              return f"Lade Datei: {dateiname}"
          case ["save", dateiname]:
              return f"Speichere in: {dateiname}"
          case ["move", x, y]:
              return f"Bewege zu ({x}, {y})"
          case ["help", *themen]:
              return f"Hilfe zu: {', '.join(themen) or 'alle Themen'}"
          case _:
              return "Unbekannter Befehl"

Beispiel - Datenstruktur-Matching:
  def analysiere_punkt(punkt):
      match punkt:
          case (0, 0):
              return "Ursprung"
          case (0, y):
              return f"Y-Achse bei y={y}"
          case (x, 0):
              return f"X-Achse bei x={x}"
          case (x, y) if x == y:
              return f"Diagonale bei {x}"
          case (x, y):
              return f"Punkt ({x}, {y})"

Guards (Bedingungen im Pattern):
  match wert:
      case n if n < 0:
          print("Negativ")
      case n if n == 0:
          print("Null")
      case n if n > 0:
          print("Positiv")


SCHLEIFEN
=========

FOR-SCHLEIFE
------------

Iteriert ueber jedes Element eines Iterables (Liste, Tuple, String, etc.).

Grundsyntax:
  for element in iterable:
      # Code mit element

Beispiele:
  # Ueber Liste iterieren
  fruechte = ["Apfel", "Birne", "Kirsche"]
  for frucht in fruechte:
      print(f"Frucht: {frucht}")

  # Mit Index (enumerate)
  for index, frucht in enumerate(fruechte):
      print(f"{index}: {frucht}")

  # Mit Start-Index
  for index, frucht in enumerate(fruechte, start=1):
      print(f"{index}. {frucht}")

  # Ueber range()
  for i in range(5):           # 0, 1, 2, 3, 4
      print(i)

  for i in range(2, 8):        # 2, 3, 4, 5, 6, 7
      print(i)

  for i in range(0, 10, 2):    # 0, 2, 4, 6, 8
      print(i)

  for i in range(10, 0, -1):   # 10, 9, 8, ..., 1
      print(i)

Ueber mehrere Listen gleichzeitig (zip):
  namen = ["Anna", "Bob", "Carl"]
  alter = [25, 30, 35]
  staedte = ["Berlin", "Hamburg", "Muenchen"]

  for name, a, stadt in zip(namen, alter, staedte):
      print(f"{name} ({a}) wohnt in {stadt}")

Dictionary-Iteration:
  person = {"name": "Max", "alter": 30, "stadt": "Berlin"}

  # Nur Keys (Standard)
  for key in person:
      print(key)

  # Nur Values
  for value in person.values():
      print(value)

  # Keys und Values
  for key, value in person.items():
      print(f"{key}: {value}")


WHILE-SCHLEIFE
--------------

Fuehrt Code aus, solange eine Bedingung wahr ist.

Syntax:
  while bedingung:
      # Code

Beispiel - Countdown:
  zaehler = 5
  while zaehler > 0:
      print(f"Noch {zaehler} Sekunden...")
      zaehler -= 1
  print("Start!")

Beispiel - Benutzereingabe:
  while True:
      eingabe = input("Gib 'quit' ein zum Beenden: ")
      if eingabe.lower() == 'quit':
          break
      print(f"Du hast eingegeben: {eingabe}")

Achtung: Endlosschleifen vermeiden!
  # FALSCH - Endlosschleife
  # i = 0
  # while i < 10:
  #     print(i)
  #     # i += 1 vergessen!

  # RICHTIG
  i = 0
  while i < 10:
      print(i)
      i += 1


SCHLEIFENKONTROLLE
==================

BREAK
-----
Beendet die Schleife sofort.

  for n in range(100):
      if n == 5:
          break
      print(n)  # Gibt 0, 1, 2, 3, 4 aus

CONTINUE
--------
Springt zur naechsten Iteration.

  for n in range(10):
      if n % 2 == 0:
          continue  # Gerade Zahlen ueberspringen
      print(n)  # Gibt 1, 3, 5, 7, 9 aus

PASS
----
Platzhalter - tut nichts, erfuellt aber syntaktische Anforderung.

  for item in liste:
      if bedingung:
          pass  # TODO: spaeter implementieren
      else:
          verarbeite(item)

ELSE BEI SCHLEIFEN
------------------
Der else-Block wird ausgefuehrt, wenn die Schleife NICHT durch break
beendet wurde.

  def finde_primzahl(n):
      """Prueft ob n eine Primzahl ist."""
      if n < 2:
          return False
      for i in range(2, int(n**0.5) + 1):
          if n % i == 0:
              break
      else:
          # Kein Teiler gefunden -> Primzahl
          return True
      return False

  # Suche in Liste mit else
  gesucht = 42
  for item in liste:
      if item == gesucht:
          print(f"Gefunden: {item}")
          break
  else:
      print("Nicht gefunden")


COMPREHENSIONS
==============

Kompakte Syntax zum Erstellen von Listen, Dicts, Sets und Generatoren.

LIST COMPREHENSION
------------------
Syntax: [ausdruck for element in iterable if bedingung]

  # Quadratzahlen
  quadrate = [x**2 for x in range(10)]
  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

  # Mit Bedingung
  gerade_quadrate = [x**2 for x in range(10) if x % 2 == 0]
  # [0, 4, 16, 36, 64]

  # Verschachtelt (Matrix flach machen)
  matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
  flach = [n for zeile in matrix for n in zeile]
  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

  # Mit Funktionsaufruf
  woerter = ["hallo", "welt", "python"]
  gross = [w.upper() for w in woerter]
  # ["HALLO", "WELT", "PYTHON"]

DICT COMPREHENSION
------------------
Syntax: {key: value for element in iterable if bedingung}

  # Quadrat-Dictionary
  quadrat_dict = {x: x**2 for x in range(6)}
  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

  # Dict umkehren
  original = {"a": 1, "b": 2, "c": 3}
  umgekehrt = {v: k for k, v in original.items()}
  # {1: "a", 2: "b", 3: "c"}

  # Filtern
  preise = {"apfel": 1.5, "birne": 2.0, "kirsche": 3.5, "banane": 0.8}
  teuer = {k: v for k, v in preise.items() if v > 1.5}
  # {"birne": 2.0, "kirsche": 3.5}

SET COMPREHENSION
-----------------
Syntax: {ausdruck for element in iterable if bedingung}

  # Eindeutige Laengen
  woerter = ["hallo", "welt", "python", "code", "test"]
  laengen = {len(w) for w in woerter}
  # {4, 5, 6}

GENERATOR EXPRESSION
--------------------
Syntax: (ausdruck for element in iterable if bedingung)

Erzeugt einen Generator - speichereffizient fuer grosse Datenmengen.

  # Generator fuer Quadratzahlen
  gen = (x**2 for x in range(1000000))

  # Speicherverbrauch minimal - wird erst bei Bedarf berechnet
  for quad in gen:
      if quad > 100:
          break
      print(quad)

  # Mit sum(), max(), min() etc.
  summe = sum(x**2 for x in range(100))
  maximum = max(len(w) for w in woerter)


BEST PRACTICES
==============

1. Lesbarkeit vor Kurzheit
   # Schlecht
   result = [x.strip().lower() for x in data if x and x.strip() and len(x.strip()) > 3]

   # Besser
   def bereinige(text):
       return text.strip().lower()

   result = [bereinige(x) for x in data if x and len(x.strip()) > 3]

2. Richtige Schleife waehlen
   - for: Wenn Anzahl der Iterationen bekannt
   - while: Wenn Abbruchbedingung dynamisch

3. enumerate() statt range(len())
   # Schlecht
   for i in range(len(liste)):
       print(liste[i])

   # Besser
   for item in liste:
       print(item)

   # Mit Index
   for i, item in enumerate(liste):
       print(f"{i}: {item}")

4. Comprehensions sinnvoll einsetzen
   - Einfache Transformationen: Comprehension
   - Komplexe Logik: Normale Schleife mit append()

5. Walrus Operator := (Python 3.8+)
   # Vermeidet doppelten Funktionsaufruf
   if (n := len(daten)) > 10:
       print(f"Zu viele Elemente: {n}")


SIEHE AUCH
==========
  wiki/python/funktionen/
  wiki/python/datentypen/
  wiki/python/iteratoren/
  wiki/python/fehlerbehandlung/
