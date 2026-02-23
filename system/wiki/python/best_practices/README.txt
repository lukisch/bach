# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: PEP 8, PEP 484, PEP 257, Clean Code (Robert C. Martin),
#          docs.python.org, Real Python, Python Cookbook

PYTHON BEST PRACTICES
=====================

Stand: 2026-02-05

UEBERBLICK
==========
  Best Practices sind bewaehrte Methoden fuer sauberen, wartbaren
  und effizienten Python-Code. Sie erleichtern Zusammenarbeit,
  Debugging und langfristige Wartung von Projekten.

PEP 8 - STYLE GUIDE
===================

EINRUECKUNG UND FORMATIERUNG
----------------------------
  - 4 Leerzeichen pro Einrueckungsebene (keine Tabs)
  - Maximale Zeilenlaenge: 79 Zeichen (Code), 72 (Docstrings)
  - Zwei Leerzeilen vor Top-Level Definitionen
  - Eine Leerzeile zwischen Methoden in Klassen

  # Gut:
  def funktion_mit_vielen_parametern(
          param_eins, param_zwei,
          param_drei, param_vier):
      return param_eins + param_zwei

  # Schlecht:
  def funktion(param_eins,param_zwei,param_drei):return param_eins

NAMENSKONVENTIONEN
------------------
  Variablen/Funktionen:  snake_case         benutzer_name
  Klassen:               PascalCase         BenutzerProfil
  Konstanten:            SCREAMING_SNAKE    MAX_VERBINDUNGEN
  Private:               _fuehrend          _interne_methode
  Name Mangling:         __doppelt          __sehr_privat

  # Gut:
  class BenutzerManager:
      MAX_BENUTZER = 100

      def __init__(self):
          self._cache = {}
          self.aktive_benutzer = []

      def hole_benutzer_daten(self, benutzer_id):
          pass

IMPORTS
-------
  Reihenfolge:
    1. Standard Library
    2. Third-Party Packages
    3. Lokale Module

  # Gut:
  import os
  import sys
  from pathlib import Path

  import requests
  import pandas as pd

  from mein_projekt.utils import helper
  from mein_projekt.models import User

  # Schlecht:
  from os import *
  import pandas, numpy, requests

TYPE HINTS (PEP 484)
====================

GRUNDLAGEN
----------
  Type Hints verbessern Code-Lesbarkeit und ermoeglichen
  statische Analyse mit Tools wie mypy.

  def begruessung(name: str) -> str:
      return f"Hallo, {name}!"

  def addiere(a: int, b: int) -> int:
      return a + b

KOMPLEXE TYPEN
--------------
  from typing import List, Dict, Optional, Union, Callable, Tuple

  def verarbeite_liste(elemente: List[str]) -> Dict[str, int]:
      return {e: len(e) for e in elemente}

  def finde_benutzer(user_id: int) -> Optional[User]:
      """Gibt User oder None zurueck."""
      return db.get(user_id)

  def flexible_eingabe(wert: Union[str, int]) -> str:
      return str(wert)

TYPE ALIASES
------------
  from typing import Dict, List, Tuple

  # Komplexe Typen lesbar machen
  Koordinate = Tuple[float, float]
  BenutzerListe = List[Dict[str, str]]

  def entfernung(start: Koordinate, ende: Koordinate) -> float:
      x1, y1 = start
      x2, y2 = ende
      return ((x2-x1)**2 + (y2-y1)**2)**0.5

DOCSTRINGS (PEP 257)
====================

GOOGLE STYLE (EMPFOHLEN)
------------------------
  def berechne_rabatt(preis: float, prozent: float) -> float:
      """Berechnet den Rabattpreis.

      Args:
          preis: Urspruenglicher Preis in Euro.
          prozent: Rabatt in Prozent (0-100).

      Returns:
          Der reduzierte Preis.

      Raises:
          ValueError: Wenn prozent negativ oder > 100.

      Example:
          >>> berechne_rabatt(100.0, 20)
          80.0
      """
      if not 0 <= prozent <= 100:
          raise ValueError("Prozent muss zwischen 0 und 100 liegen")
      return preis * (1 - prozent / 100)

KLASSEN-DOCSTRINGS
------------------
  class Warenkorb:
      """Verwaltet Produkte im Einkaufswagen.

      Attributes:
          produkte: Liste der Produkte im Warenkorb.
          max_items: Maximale Anzahl Produkte (default: 100).

      Example:
          >>> korb = Warenkorb()
          >>> korb.hinzufuegen("Apfel", 2.50)
          >>> korb.gesamt()
          2.50
      """

CLEAN CODE PRINZIPIEN
=====================

FUNKTIONEN
----------
  - Eine Funktion = eine Aufgabe
  - Maximal 3 Parameter (sonst Objekt verwenden)
  - Aussagekraeftige Namen
  - Keine Seiteneffekte

  # Schlecht:
  def x(d, f):
      return [i for i in d if f(i)]

  # Gut:
  def filtere_aktive_benutzer(benutzer_liste, ist_aktiv):
      """Filtert Liste nach aktiven Benutzern."""
      return [b for b in benutzer_liste if ist_aktiv(b)]

VERMEIDUNG VON CODE-WIEDERHOLUNG (DRY)
--------------------------------------
  # Schlecht:
  def sende_email_an_admin(nachricht):
      smtp = smtplib.SMTP('server')
      smtp.send('admin@firma.de', nachricht)
      smtp.quit()

  def sende_email_an_support(nachricht):
      smtp = smtplib.SMTP('server')
      smtp.send('support@firma.de', nachricht)
      smtp.quit()

  # Gut:
  def sende_email(empfaenger: str, nachricht: str) -> None:
      """Sendet Email an angegebenen Empfaenger."""
      smtp = smtplib.SMTP('server')
      smtp.send(empfaenger, nachricht)
      smtp.quit()

EARLY RETURNS
-------------
  # Schlecht (verschachtelt):
  def verarbeite(daten):
      if daten:
          if daten.ist_valid():
              if daten.hat_inhalt():
                  return daten.verarbeiten()
      return None

  # Gut (early returns):
  def verarbeite(daten):
      if not daten:
          return None
      if not daten.ist_valid():
          return None
      if not daten.hat_inhalt():
          return None
      return daten.verarbeiten()

FEHLERBEHANDLUNG
================

SPEZIFISCHE EXCEPTIONS
----------------------
  # Schlecht:
  try:
      ergebnis = risiko_operation()
  except:
      print("Fehler")

  # Gut:
  try:
      ergebnis = risiko_operation()
  except FileNotFoundError:
      logger.error("Datei nicht gefunden")
      raise
  except PermissionError:
      logger.error("Keine Berechtigung")
      raise
  except Exception as e:
      logger.error(f"Unerwarteter Fehler: {e}")
      raise

CUSTOM EXCEPTIONS
-----------------
  class ValidationError(Exception):
      """Fehler bei Datenvalidierung."""
      pass

  class DatabaseConnectionError(Exception):
      """Verbindung zur Datenbank fehlgeschlagen."""
      def __init__(self, host: str, message: str):
          self.host = host
          super().__init__(f"DB-Fehler bei {host}: {message}")

CONTEXT MANAGER (WITH)
----------------------
  # Immer with fuer Ressourcen nutzen:
  with open('datei.txt', 'r') as f:
      inhalt = f.read()

  # Eigener Context Manager:
  from contextlib import contextmanager

  @contextmanager
  def db_verbindung(config):
      conn = create_connection(config)
      try:
          yield conn
      finally:
          conn.close()

PERFORMANCE BEST PRACTICES
==========================

LIST COMPREHENSIONS
-------------------
  # Schlecht (langsam):
  ergebnis = []
  for i in range(1000):
      if i % 2 == 0:
          ergebnis.append(i ** 2)

  # Gut (schneller):
  ergebnis = [i ** 2 for i in range(1000) if i % 2 == 0]

GENERATOREN FUER GROSSE DATEN
-----------------------------
  # Schlecht (alles im Speicher):
  def alle_zeilen(datei):
      with open(datei) as f:
          return f.readlines()  # Alles laden!

  # Gut (lazy evaluation):
  def alle_zeilen(datei):
      with open(datei) as f:
          for zeile in f:
              yield zeile.strip()

STRING-OPERATIONEN
------------------
  # Schlecht:
  s = ""
  for wort in woerter:
      s += wort + " "

  # Gut:
  s = " ".join(woerter)

PROJEKT-STRUKTUR
================

EMPFOHLENE STRUKTUR
-------------------
  mein_projekt/
  |-- src/
  |   |-- mein_projekt/
  |   |   |-- __init__.py
  |   |   |-- core/
  |   |   |-- utils/
  |   |   |-- models/
  |-- tests/
  |   |-- test_core.py
  |   |-- test_utils.py
  |-- docs/
  |-- pyproject.toml
  |-- README.md
  |-- .gitignore

__INIT__.PY
-----------
  # mein_projekt/__init__.py
  """Mein Projekt - Kurze Beschreibung."""

  __version__ = "1.0.0"
  __author__ = "Name"

  from .core import HauptKlasse
  from .utils import hilfs_funktion

LOGGING STATT PRINT
===================

  import logging

  # Konfiguration
  logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  )

  logger = logging.getLogger(__name__)

  # Verwendung
  logger.debug("Debug-Info fuer Entwickler")
  logger.info("Normale Information")
  logger.warning("Warnung - potentielles Problem")
  logger.error("Fehler aufgetreten")
  logger.critical("Kritischer Fehler - System stoppt")

TESTING BEST PRACTICES
======================

  import pytest

  # Gute Tests sind:
  # - Unabhaengig voneinander
  # - Wiederholbar
  # - Schnell
  # - Selbst-dokumentierend

  def test_berechne_rabatt_standard():
      """Testet Standardfall mit gueltigem Rabatt."""
      assert berechne_rabatt(100, 20) == 80

  def test_berechne_rabatt_null():
      """Testet ohne Rabatt."""
      assert berechne_rabatt(50, 0) == 50

  def test_berechne_rabatt_ungueltig():
      """Testet mit ungueltigem Rabatt."""
      with pytest.raises(ValueError):
          berechne_rabatt(100, -10)

TOOLS UND AUTOMATISIERUNG
=========================

EMPFOHLENE TOOLS
----------------
  Formatter:      black, yapf
  Linter:         flake8, pylint, ruff
  Type Checker:   mypy, pyright
  Test:           pytest, coverage
  Pre-commit:     pre-commit hooks

BEISPIEL PRE-COMMIT CONFIG
--------------------------
  # .pre-commit-config.yaml
  repos:
    - repo: https://github.com/psf/black
      rev: 23.1.0
      hooks:
        - id: black
    - repo: https://github.com/pycqa/flake8
      rev: 6.0.0
      hooks:
        - id: flake8

BACH-INTEGRATION
================
  Partner-Zuweisung:
    - Claude: Code-Review, Best Practice Checks
    - Copilot: Inline-Vorschlaege nach PEP 8
    - Ruff: Automatische Formatierung

CHECKLISTE
==========
  [ ] PEP 8 eingehalten?
  [ ] Type Hints vorhanden?
  [ ] Docstrings geschrieben?
  [ ] Tests vorhanden?
  [ ] Logging statt print?
  [ ] Exceptions spezifisch?
  [ ] DRY-Prinzip befolgt?
  [ ] Code reviewt?

SIEHE AUCH
==========
  wiki/python/packaging/           Packaging und Distribution
  wiki/python/testing/             Testing mit pytest
  wiki/automatisierung/code_testing.txt  Automatisiertes Testen
  wiki/github_konventionen.txt     Git Best Practices
