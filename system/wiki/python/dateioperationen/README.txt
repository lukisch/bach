# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: docs.python.org/3/library/pathlib.html, docs.python.org/3/library/os.html, realpython.com

DATEIOPERATIONEN IN PYTHON
==========================

Stand: 2026-02-05

UEBERBLICK
==========
  Python bietet vielfaeltige Moeglichkeiten zur Arbeit mit Dateien
  und Verzeichnissen. Moderne Python-Versionen (3.4+) empfehlen
  pathlib als primaere Bibliothek fuer Pfadoperationen.

  Kernbibliotheken:
    - pathlib     Objektorientierte Pfade (empfohlen)
    - os          Betriebssystem-Interaktion
    - os.path     Pfadmanipulation (legacy)
    - shutil      Hoeherlevel Dateioperationen
    - glob        Dateisuche mit Mustern

PATHLIB - MODERNE PFADE
=======================

GRUNDLAGEN
----------
  from pathlib import Path

  # Pfad erstellen
  pfad = Path("C:/Users/User/Dokumente")
  pfad = Path.home() / "Dokumente"     # Plattformunabhaengig
  pfad = Path.cwd()                     # Aktuelles Verzeichnis

  # Pfade kombinieren (/ Operator)
  projekt = Path("C:/Projekte")
  datei = projekt / "src" / "main.py"
  print(datei)  # C:\Projekte\src\main.py

PFAD-EIGENSCHAFTEN
------------------
  pfad = Path("C:/Projekte/app/main.py")

  pfad.name           # 'main.py'
  pfad.stem           # 'main' (ohne Endung)
  pfad.suffix         # '.py'
  pfad.parent         # Path('C:/Projekte/app')
  pfad.parents        # Alle Elternordner
  pfad.parts          # ('C:\\', 'Projekte', 'app', 'main.py')
  pfad.anchor         # 'C:\\'

  # Absolute/Relative Pfade
  pfad.is_absolute()  # True/False
  pfad.resolve()      # Absoluter Pfad
  pfad.relative_to(Path("C:/Projekte"))  # Path('app/main.py')

EXISTENZ-PRUEFUNGEN
-------------------
  pfad = Path("meine_datei.txt")

  pfad.exists()       # Existiert?
  pfad.is_file()      # Ist Datei?
  pfad.is_dir()       # Ist Verzeichnis?
  pfad.is_symlink()   # Ist Symlink?

  # Beispiel
  if pfad.exists():
      if pfad.is_file():
          print("Datei gefunden")
      elif pfad.is_dir():
          print("Verzeichnis gefunden")
  else:
      print("Existiert nicht")

DATEIEN LESEN UND SCHREIBEN
===========================

MIT OPEN() UND WITH-STATEMENT
-----------------------------
  # IMMER with-Statement verwenden (schliesst Datei automatisch)

  # Datei lesen
  with open("datei.txt", "r", encoding="utf-8") as f:
      inhalt = f.read()           # Gesamter Inhalt als String
      # oder
      zeilen = f.readlines()      # Liste aller Zeilen
      # oder
      for zeile in f:             # Zeile fuer Zeile (speichereffizient)
          print(zeile.strip())

  # Datei schreiben
  with open("datei.txt", "w", encoding="utf-8") as f:
      f.write("Hallo Welt\n")
      f.write("Zweite Zeile\n")

  # An Datei anhaengen
  with open("datei.txt", "a", encoding="utf-8") as f:
      f.write("Neue Zeile am Ende\n")

DATEIMODI
---------
  'r'     Lesen (Standard)
  'w'     Schreiben (ueberschreibt!)
  'a'     Anhaengen
  'x'     Exklusiv erstellen (Fehler wenn existiert)
  'b'     Binaermodus (z.B. 'rb', 'wb')
  '+'     Lesen und Schreiben (z.B. 'r+')

  # Binaerdatei lesen
  with open("bild.png", "rb") as f:
      daten = f.read()

  # Binaerdatei schreiben
  with open("kopie.png", "wb") as f:
      f.write(daten)

MIT PATHLIB (EINFACHER)
-----------------------
  from pathlib import Path

  pfad = Path("datei.txt")

  # Lesen
  inhalt = pfad.read_text(encoding="utf-8")
  zeilen = pfad.read_text().splitlines()
  binaer = pfad.read_bytes()

  # Schreiben
  pfad.write_text("Neuer Inhalt", encoding="utf-8")
  pfad.write_bytes(b"Binaerdaten")

  # Beispiel: Konfigurationsdatei
  config = Path("config.txt")
  if config.exists():
      einstellungen = config.read_text().splitlines()
  else:
      config.write_text("standard=wert\n")

VERZEICHNIS-OPERATIONEN
=======================

VERZEICHNISSE ERSTELLEN
-----------------------
  from pathlib import Path

  # Einzelnes Verzeichnis
  Path("neuer_ordner").mkdir()

  # Mit Elternverzeichnissen
  Path("a/b/c/d").mkdir(parents=True)

  # Nur wenn nicht existiert
  Path("ordner").mkdir(exist_ok=True)

  # Kombiniert (empfohlen)
  Path("projekte/python/src").mkdir(parents=True, exist_ok=True)

VERZEICHNISSE AUFLISTEN
-----------------------
  from pathlib import Path

  ordner = Path("C:/Projekte")

  # Alle Eintraege
  for eintrag in ordner.iterdir():
      print(eintrag.name, "DIR" if eintrag.is_dir() else "FILE")

  # Nur Dateien
  dateien = [f for f in ordner.iterdir() if f.is_file()]

  # Nur Verzeichnisse
  unterordner = [d for d in ordner.iterdir() if d.is_dir()]

  # Mit glob-Pattern
  python_dateien = list(ordner.glob("*.py"))
  alle_python = list(ordner.glob("**/*.py"))  # Rekursiv

  # rglob fuer rekursive Suche
  alle_txt = list(ordner.rglob("*.txt"))

DATEIEN SUCHEN
--------------
  from pathlib import Path

  projekt = Path("C:/Projekt")

  # Glob-Patterns
  projekt.glob("*.py")           # Alle .py im Ordner
  projekt.glob("**/*.py")        # Alle .py rekursiv
  projekt.glob("test_*.py")      # Beginnt mit test_
  projekt.glob("**/test/*.py")   # In test-Unterordnern

  # Beispiel: Alle Bilder finden
  bilder = []
  for endung in ["*.jpg", "*.png", "*.gif"]:
      bilder.extend(projekt.rglob(endung))

  # Mit os.walk (fuer komplexe Faelle)
  import os
  for wurzel, ordner, dateien in os.walk("C:/Projekt"):
      for datei in dateien:
          if datei.endswith(".py"):
              print(os.path.join(wurzel, datei))

DATEIEN UND ORDNER MANIPULIEREN
===============================

UMBENENNEN UND VERSCHIEBEN
--------------------------
  from pathlib import Path

  datei = Path("alt.txt")

  # Umbenennen
  datei.rename("neu.txt")

  # In anderen Ordner verschieben
  datei.rename(Path("archiv") / datei.name)

  # Mit replace (ueberschreibt Ziel)
  datei.replace("ziel.txt")

  # Suffix aendern
  neue_datei = datei.with_suffix(".md")
  datei.rename(neue_datei)

  # Name aendern
  neue_datei = datei.with_name("anderer_name.txt")

KOPIEREN
--------
  import shutil
  from pathlib import Path

  # Datei kopieren
  shutil.copy("quelle.txt", "ziel.txt")
  shutil.copy2("quelle.txt", "ziel.txt")  # Mit Metadaten

  # Verzeichnis kopieren
  shutil.copytree("quell_ordner", "ziel_ordner")

  # Mit pathlib
  quelle = Path("original.txt")
  ziel = Path("kopie.txt")
  ziel.write_bytes(quelle.read_bytes())

LOESCHEN
--------
  from pathlib import Path
  import shutil

  # Datei loeschen
  Path("datei.txt").unlink()

  # Nur wenn existiert
  Path("datei.txt").unlink(missing_ok=True)

  # Leeres Verzeichnis loeschen
  Path("leerer_ordner").rmdir()

  # Verzeichnis mit Inhalt loeschen
  shutil.rmtree("ordner_mit_inhalt")

  # Sicher loeschen (erst pruefen)
  pfad = Path("zu_loeschen")
  if pfad.exists():
      if pfad.is_file():
          pfad.unlink()
      elif pfad.is_dir():
          shutil.rmtree(pfad)

DATEI-INFORMATIONEN
===================

METADATEN AUSLESEN
------------------
  from pathlib import Path
  from datetime import datetime

  datei = Path("dokument.txt")
  stat = datei.stat()

  # Groesse
  groesse_bytes = stat.st_size
  groesse_kb = stat.st_size / 1024
  groesse_mb = stat.st_size / (1024 * 1024)

  # Zeiten
  erstellt = datetime.fromtimestamp(stat.st_ctime)
  geaendert = datetime.fromtimestamp(stat.st_mtime)
  zugegriffen = datetime.fromtimestamp(stat.st_atime)

  print(f"Groesse: {groesse_kb:.2f} KB")
  print(f"Geaendert: {geaendert.strftime('%d.%m.%Y %H:%M')}")

DATEIGROESSE FORMATIEREN
------------------------
  def formatiere_groesse(bytes_anzahl):
      """Formatiert Bytes in lesbare Groesse."""
      for einheit in ['B', 'KB', 'MB', 'GB', 'TB']:
          if bytes_anzahl < 1024:
              return f"{bytes_anzahl:.2f} {einheit}"
          bytes_anzahl /= 1024
      return f"{bytes_anzahl:.2f} PB"

  pfad = Path("grosses_archiv.zip")
  print(formatiere_groesse(pfad.stat().st_size))

ORDNERGROESSE BERECHNEN
-----------------------
  def ordner_groesse(pfad):
      """Berechnet Gesamtgroesse eines Ordners."""
      ordner = Path(pfad)
      gesamt = sum(f.stat().st_size for f in ordner.rglob("*") if f.is_file())
      return gesamt

  projekt = Path("C:/Projekte/MeinProjekt")
  print(f"Projektgroesse: {formatiere_groesse(ordner_groesse(projekt))}")

SPEZIELLE DATEITYPEN
====================

CSV-DATEIEN
-----------
  import csv

  # CSV lesen
  with open("daten.csv", "r", encoding="utf-8", newline='') as f:
      reader = csv.reader(f)
      header = next(reader)  # Erste Zeile als Header
      for zeile in reader:
          print(zeile)

  # CSV als Dictionary
  with open("daten.csv", "r", encoding="utf-8", newline='') as f:
      reader = csv.DictReader(f)
      for zeile in reader:
          print(zeile['Name'], zeile['Alter'])

  # CSV schreiben
  daten = [
      ["Name", "Alter", "Stadt"],
      ["Max", 30, "Berlin"],
      ["Anna", 25, "Hamburg"]
  ]

  with open("ausgabe.csv", "w", encoding="utf-8", newline='') as f:
      writer = csv.writer(f)
      writer.writerows(daten)

JSON-DATEIEN
------------
  import json
  from pathlib import Path

  # JSON lesen
  with open("config.json", "r", encoding="utf-8") as f:
      daten = json.load(f)

  # Oder mit pathlib
  daten = json.loads(Path("config.json").read_text())

  # JSON schreiben
  config = {
      "name": "MeinProjekt",
      "version": "1.0",
      "einstellungen": {
          "debug": True,
          "port": 8080
      }
  }

  with open("config.json", "w", encoding="utf-8") as f:
      json.dump(config, f, indent=2, ensure_ascii=False)

  # Oder mit pathlib
  Path("config.json").write_text(
      json.dumps(config, indent=2, ensure_ascii=False),
      encoding="utf-8"
  )

YAML-DATEIEN
------------
  import yaml  # pip install pyyaml
  from pathlib import Path

  # YAML lesen
  with open("config.yaml", "r", encoding="utf-8") as f:
      config = yaml.safe_load(f)

  # YAML schreiben
  with open("config.yaml", "w", encoding="utf-8") as f:
      yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

INI-DATEIEN
-----------
  import configparser

  # INI lesen
  config = configparser.ConfigParser()
  config.read("settings.ini", encoding="utf-8")

  wert = config['Section']['key']
  alle_keys = dict(config['Section'])

  # INI schreiben
  config['Database'] = {
      'host': 'localhost',
      'port': '5432',
      'name': 'mydb'
  }

  with open("settings.ini", "w") as f:
      config.write(f)

TEMPORAERE DATEIEN
==================

  import tempfile
  from pathlib import Path

  # Temporaere Datei
  with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
      f.write("Temporaerer Inhalt")
      temp_pfad = f.name

  print(f"Temp-Datei: {temp_pfad}")
  # Datei existiert noch, manuell loeschen wenn fertig

  # Automatisch geloescht nach Verlassen des Blocks
  with tempfile.TemporaryFile(mode='w+') as f:
      f.write("Wird automatisch geloescht")
      f.seek(0)
      print(f.read())

  # Temporaeres Verzeichnis
  with tempfile.TemporaryDirectory() as temp_dir:
      temp_pfad = Path(temp_dir)
      (temp_pfad / "test.txt").write_text("Test")
      # Wird automatisch geloescht

FEHLERBEHANDLUNG
================

TYPISCHE FEHLER
---------------
  from pathlib import Path

  def sichere_datei_operation(pfad):
      """Demonstriert Fehlerbehandlung."""

      pfad = Path(pfad)

      try:
          inhalt = pfad.read_text()
          return inhalt

      except FileNotFoundError:
          print(f"Datei nicht gefunden: {pfad}")

      except PermissionError:
          print(f"Keine Berechtigung: {pfad}")

      except IsADirectoryError:
          print(f"Ist ein Verzeichnis: {pfad}")

      except UnicodeDecodeError:
          print(f"Encoding-Fehler, versuche binaer...")
          return pfad.read_bytes()

      except OSError as e:
          print(f"Betriebssystem-Fehler: {e}")

      return None

ENCODING-PROBLEME
-----------------
  def lese_mit_encoding_erkennung(pfad):
      """Versucht verschiedene Encodings."""

      encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

      for encoding in encodings:
          try:
              with open(pfad, 'r', encoding=encoding) as f:
                  inhalt = f.read()
                  print(f"Erfolgreich mit {encoding}")
                  return inhalt
          except UnicodeDecodeError:
              continue

      print("Kein passendes Encoding gefunden")
      return None

  # Mit chardet-Bibliothek (pip install chardet)
  import chardet

  def erkenne_encoding(pfad):
      with open(pfad, 'rb') as f:
          result = chardet.detect(f.read())
      return result['encoding']

BEST PRACTICES
==============

  1. IMMER with-Statement fuer Dateien verwenden
     - Garantiert Schliessen der Datei
     - Auch bei Exceptions

  2. IMMER encoding="utf-8" angeben
     - Verhindert Plattform-Probleme
     - Explizit ist besser als implizit

  3. pathlib statt os.path verwenden
     - Moderner und lesbarer
     - Objektorientiert

  4. Existenz pruefen vor Operationen
     - pfad.exists() vor Lesen
     - exist_ok=True bei mkdir

  5. Relative Pfade vermeiden
     - Path.resolve() fuer absolute Pfade
     - Path.cwd() explizit verwenden

  6. Pfade niemals als Strings bauen
     FALSCH:  pfad = "ordner" + "/" + "datei.txt"
     RICHTIG: pfad = Path("ordner") / "datei.txt"

ZUSAMMENFASSUNG
===============

  Aufgabe                  Methode
  -------                  -------
  Pfad erstellen           Path("pfad/zur/datei")
  Pfade verbinden          pfad1 / pfad2
  Datei lesen              pfad.read_text()
  Datei schreiben          pfad.write_text(inhalt)
  Existenz pruefen         pfad.exists()
  Verzeichnis erstellen    pfad.mkdir(parents=True)
  Dateien auflisten        pfad.iterdir() / pfad.glob()
  Datei loeschen           pfad.unlink()
  Verzeichnis loeschen     shutil.rmtree(pfad)
  Kopieren                 shutil.copy(quelle, ziel)
  Verschieben              pfad.rename(ziel)

SIEHE AUCH
==========
  wiki/python/README.txt               Python Uebersicht
  wiki/python/automatisierung/         Datei-Automatisierung
  wiki/python/regex/                   Regex fuer Dateisuche
  wiki/python/fehlerbehandlung/        Exception-Handling
