# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: docs.python.org/3/tutorial/modules.html, PEP 328, PEP 420, packaging.python.org

PYTHON MODULE
=============

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

EINFUEHRUNG
===========

Module sind die grundlegende Organisationseinheit in Python. Sie ermoeglichen
die Strukturierung von Code in wiederverwendbare Einheiten und bieten
Namensraeume zur Vermeidung von Namenskonflikten.

Begriffsklaerung:
  - Modul: Eine einzelne .py-Datei
  - Package: Ein Verzeichnis mit __init__.py (oder Namespace Package)
  - Bibliothek: Sammlung von Modulen/Packages
  - Framework: Bibliothek mit vorgegebener Struktur

Vorteile von Modulen:
  - Wiederverwendbarkeit von Code
  - Namensraum-Trennung
  - Bessere Wartbarkeit
  - Klare Abhaengigkeiten


IMPORT-ANWEISUNGEN
==================

GRUNDLEGENDE IMPORTS
--------------------

  # Ganzes Modul importieren
  import os
  print(os.getcwd())

  # Bestimmte Namen importieren
  from os import getcwd, listdir
  print(getcwd())

  # Mit Alias (Umbenennung)
  import numpy as np
  import pandas as pd
  from datetime import datetime as dt

  # Mehrere Namen
  from os.path import join, exists, dirname

RELATIVE VS ABSOLUTE IMPORTS
----------------------------

Absolute Imports (empfohlen):
  from projekt.modul import funktion
  from projekt.unterpaket.modul import Klasse

Relative Imports (innerhalb von Packages):
  # In projekt/unterpaket/modul2.py:
  from . import modul1           # Gleiches Verzeichnis
  from .modul1 import funktion   # Aus modul1 im gleichen Verzeichnis
  from .. import anderes_modul   # Eine Ebene hoeher
  from ..utils import helper     # utils-Package eine Ebene hoeher

IMPORT-ANTIPATTERNS
-------------------

  # VERMEIDEN: Wildcard-Import
  from os import *  # Verschmutzt Namensraum, versteckt Abhaengigkeiten

  # VERMEIDEN: Zyklische Imports
  # modul_a.py: from modul_b import x
  # modul_b.py: from modul_a import y  # ImportError!

  # LOESUNG: Import in Funktion verschieben oder Struktur ueberdenken
  def funktion():
      from modul_b import x  # Verzoegerter Import
      return x


MODUL- UND PACKAGE-STRUKTUR
===========================

EINFACHES MODUL
---------------

Eine einzelne .py-Datei ist bereits ein Modul:

  # mathutils.py
  """Mathematische Hilfsfunktionen."""

  PI = 3.14159

  def quadrat(x):
      return x ** 2

  def kreisflaeche(radius):
      return PI * radius ** 2

  # Verwendung
  import mathutils
  print(mathutils.kreisflaeche(5))

REGULAERES PACKAGE
------------------

Verzeichnis mit __init__.py:

  meinprojekt/
      __init__.py
      core/
          __init__.py
          engine.py
          utils.py
      plugins/
          __init__.py
          plugin_a.py
          plugin_b.py
      config.py

__init__.py Aufgaben:
  - Markiert Verzeichnis als Package
  - Initialisierungscode beim Import
  - Definiert __all__ fuer from package import *
  - Stellt oeffentliche API bereit

Beispiel __init__.py:
  # meinprojekt/__init__.py
  """Hauptpaket des Projekts."""

  __version__ = "1.0.0"
  __all__ = ["Engine", "laden", "speichern"]

  from .core.engine import Engine
  from .core.utils import laden, speichern

NAMESPACE PACKAGES (PYTHON 3.3+)
--------------------------------

Packages ohne __init__.py - verteilt ueber mehrere Verzeichnisse:

  # Installation A
  site-packages/
      meinpaket/
          modul_a.py

  # Installation B
  site-packages/
      meinpaket/
          modul_b.py

  # Beide sind importierbar
  from meinpaket import modul_a
  from meinpaket import modul_b


PYTHON STANDARDBIBLIOTHEK
=========================

Die Standardbibliothek bietet umfangreiche Funktionalitaet ohne Installation.

DATEISYSTEM UND BETRIEBSSYSTEM
------------------------------

  import os
  os.getcwd()              # Aktuelles Verzeichnis
  os.chdir("/pfad")        # Verzeichnis wechseln
  os.listdir(".")          # Verzeichnisinhalt
  os.makedirs("a/b/c")     # Verzeichnisse erstellen
  os.environ["PATH"]       # Umgebungsvariable

  import os.path
  os.path.join("a", "b")   # Pfade verbinden
  os.path.exists(pfad)     # Existiert?
  os.path.isfile(pfad)     # Ist Datei?
  os.path.isdir(pfad)      # Ist Verzeichnis?

  from pathlib import Path  # Modern (empfohlen)
  p = Path("/home/user")
  p / "dokumente" / "datei.txt"   # Pfad-Operationen
  p.exists()
  p.is_file()
  p.glob("*.py")           # Dateien suchen
  p.read_text()            # Datei lesen
  p.write_text("inhalt")   # Datei schreiben

PYTHON-SYSTEM
-------------

  import sys
  sys.argv                 # Kommandozeilenargumente
  sys.path                 # Modul-Suchpfade
  sys.version              # Python-Version
  sys.exit(0)              # Programm beenden
  sys.stdin, sys.stdout    # Standard-Streams

DATUM UND ZEIT
--------------

  from datetime import datetime, date, timedelta

  jetzt = datetime.now()
  heute = date.today()
  morgen = heute + timedelta(days=1)

  # Formatierung
  jetzt.strftime("%Y-%m-%d %H:%M:%S")

  # Parsing
  datetime.strptime("2026-02-05", "%Y-%m-%d")

DATENFORMATE
------------

  import json
  json.dumps({"a": 1})     # Python -> JSON-String
  json.loads('{"a": 1}')   # JSON-String -> Python
  json.dump(daten, f)      # In Datei schreiben
  json.load(f)             # Aus Datei lesen

  import csv
  with open("daten.csv") as f:
      reader = csv.DictReader(f)
      for zeile in reader:
          print(zeile["spalte"])

  import configparser      # INI-Dateien
  import xml.etree.ElementTree as ET  # XML

REGULAERE AUSDRUECKE
--------------------

  import re

  # Suchen
  re.search(r"\d+", "abc123def")  # Match-Objekt oder None
  re.findall(r"\d+", "a1b2c3")    # ['1', '2', '3']

  # Ersetzen
  re.sub(r"\s+", " ", "a   b")    # "a b"

  # Kompilieren (Performance)
  muster = re.compile(r"[a-z]+")
  muster.findall("abc123def")

DATENSTRUKTUREN
---------------

  from collections import Counter, defaultdict, deque, namedtuple

  Counter("mississippi")   # {'i': 4, 's': 4, 'p': 2, 'm': 1}

  dd = defaultdict(list)
  dd["key"].append(1)      # Kein KeyError

  dq = deque([1, 2, 3])
  dq.appendleft(0)         # Effizient links anfuegen

  Punkt = namedtuple("Punkt", ["x", "y"])
  p = Punkt(3, 4)
  print(p.x, p.y)

FUNKTIONALE WERKZEUGE
---------------------

  from itertools import chain, cycle, islice, groupby, combinations

  list(chain([1, 2], [3, 4]))      # [1, 2, 3, 4]
  list(islice(cycle([1,2,3]), 7)) # [1, 2, 3, 1, 2, 3, 1]
  list(combinations("ABC", 2))     # [('A','B'), ('A','C'), ('B','C')]

  from functools import reduce, partial, lru_cache

  @lru_cache(maxsize=128)
  def fibonacci(n):
      if n < 2:
          return n
      return fibonacci(n-1) + fibonacci(n-2)

MATHEMATIK UND ZUFALL
---------------------

  import math
  math.sqrt(16)            # 4.0
  math.sin(math.pi/2)      # 1.0
  math.ceil(4.2)           # 5
  math.floor(4.8)          # 4

  import random
  random.random()          # Float 0.0-1.0
  random.randint(1, 10)    # Int 1-10
  random.choice(liste)     # Zufaelliges Element
  random.shuffle(liste)    # Liste mischen (in-place)
  random.sample(liste, 3)  # 3 zufaellige ohne Zuruecklegen


PIP UND PYPI
============

INSTALLATION VON PAKETEN
------------------------

  # Einzelnes Paket
  pip install requests
  pip install requests==2.28.0     # Bestimmte Version
  pip install "requests>=2.25"     # Mindestversion

  # Aus requirements.txt
  pip install -r requirements.txt

  # Entwicklungsmodus (editierbar)
  pip install -e .
  pip install -e ".[dev,test]"     # Mit Extras

  # Upgrade
  pip install --upgrade requests

PAKETVERWALTUNG
---------------

  # Installierte Pakete anzeigen
  pip list
  pip list --outdated

  # Paketinfo
  pip show requests

  # Deinstallieren
  pip uninstall requests

  # Requirements exportieren
  pip freeze > requirements.txt

REQUIREMENTS.TXT FORMAT
-----------------------

  # Exakte Versionen (reproduzierbar)
  requests==2.28.1
  numpy==1.24.0

  # Versionsbereiche
  pandas>=1.5.0,<2.0.0

  # Aus Git
  git+https://github.com/user/repo.git@v1.0.0

  # Mit Extras
  uvicorn[standard]>=0.20.0


VIRTUELLE UMGEBUNGEN
====================

WARUM VIRTUELLE UMGEBUNGEN?
---------------------------

  - Projektspezifische Abhaengigkeiten
  - Verschiedene Paketversionen gleichzeitig
  - Saubere Trennung von Projekten
  - Reproduzierbare Umgebungen

VENV (EINGEBAUT)
----------------

  # Erstellen
  python -m venv venv
  python -m venv .venv     # Verstecktes Verzeichnis

  # Aktivieren
  # Windows:
  venv\Scripts\activate
  # Linux/Mac:
  source venv/bin/activate

  # Deaktivieren
  deactivate

  # Mit bestimmter Python-Version
  python3.11 -m venv venv

PIPENV (ALTERNATIVE)
--------------------

  # Installation
  pip install pipenv

  # Neue Umgebung mit Paket
  pipenv install requests

  # Entwicklungsabhaengigkeit
  pipenv install pytest --dev

  # Shell aktivieren
  pipenv shell

  # Ausfuehren ohne Shell
  pipenv run python script.py

POETRY (MODERNE ALTERNATIVE)
----------------------------

  # Installation
  pip install poetry

  # Neues Projekt
  poetry new meinprojekt

  # Paket hinzufuegen
  poetry add requests
  poetry add pytest --group dev

  # Umgebung aktivieren
  poetry shell

  # Installieren
  poetry install


EIGENE MODULE ERSTELLEN
=======================

GRUNDSTRUKTUR EINES MODULS
--------------------------

  # meinmodul.py
  """
  Kurze Beschreibung des Moduls.

  Ausfuehrliche Beschreibung mit Beispielen.
  """

  __version__ = "1.0.0"
  __author__ = "Max Mustermann"
  __all__ = ["oeffentliche_funktion", "OeffentlicheKlasse"]

  # Konstanten
  STANDARD_WERT = 42

  # Private Funktion (Konvention: Unterstrich)
  def _interne_hilfsfunktion():
      pass

  # Oeffentliche Funktion
  def oeffentliche_funktion(param):
      """Dokumentation der Funktion."""
      return _interne_hilfsfunktion()

  # Klasse
  class OeffentlicheKlasse:
      """Dokumentation der Klasse."""
      pass

  # Ausfuehrung nur wenn direkt gestartet
  if __name__ == "__main__":
      print("Modul direkt ausgefuehrt")
      # Tests oder Demo-Code

__name__ UND __main__
---------------------

  # Wenn Modul importiert wird: __name__ == "modulname"
  # Wenn Modul ausgefuehrt wird: __name__ == "__main__"

  # Typische Verwendung
  if __name__ == "__main__":
      # Nur bei direkter Ausfuehrung
      import sys
      sys.exit(main())

PACKAGE MIT SETUP.PY / PYPROJECT.TOML
-------------------------------------

Moderne Variante (pyproject.toml):

  [build-system]
  requires = ["setuptools>=61.0"]
  build-backend = "setuptools.build_meta"

  [project]
  name = "meinpaket"
  version = "1.0.0"
  description = "Beschreibung"
  readme = "README.md"
  requires-python = ">=3.9"
  dependencies = [
      "requests>=2.25",
      "click>=8.0",
  ]

  [project.optional-dependencies]
  dev = ["pytest", "black", "mypy"]

  [project.scripts]
  mein-cli = "meinpaket.cli:main"


BEST PRACTICES
==============

1. IMPORTS AM DATEIANFANG
   # Standard: Standardbibliothek, Drittanbieter, Lokal
   import os
   import sys

   import requests
   import numpy as np

   from .utils import helper

2. ZYKLISCHE IMPORTS VERMEIDEN
   # Struktur ueberdenken oder Import in Funktion

3. __all__ DEFINIEREN
   __all__ = ["funktion1", "Klasse1"]  # Fuer from x import *

4. VIRTUELLE UMGEBUNGEN NUTZEN
   # Immer projekt-spezifische venv verwenden

5. REQUIREMENTS PINNEN
   # Exakte Versionen fuer Reproduzierbarkeit
   pip freeze > requirements.txt

6. RELATIVE IMPORTS IN PACKAGES
   from . import modul      # Nicht: from meinpaket import modul


SIEHE AUCH
==========
  wiki/python/packaging/
  wiki/python/projektstruktur/
  wiki/python/pip/
  wiki/python/funktionen/
