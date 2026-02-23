# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: docs.python.org/3/tutorial/errors.html, PEP 3134, PEP 409

PYTHON FEHLERBEHANDLUNG
=======================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

EINFUEHRUNG
===========

Fehlerbehandlung ist ein essentieller Bestandteil robuster Software.
Python verwendet ein Exception-System, das Fehler als Objekte behandelt
und deren Weitergabe durch den Call-Stack ermoeglicht.

Vorteile des Exception-Systems:
  - Trennung von normalem Code und Fehlerbehandlung
  - Praezise Fehlerinformation (Typ, Nachricht, Traceback)
  - Fehler koennen auf passender Ebene behandelt werden
  - Vermeidung von Fehlercode-Rueckgaben

Grundprinzip:
  Fehler werden "geworfen" (raise) und "gefangen" (except).
  Nicht gefangene Fehler beenden das Programm mit Traceback.


TRY / EXCEPT / ELSE / FINALLY
=============================

GRUNDSTRUKTUR
-------------

  try:
      # Riskanter Code der Fehler werfen koennte
      ergebnis = operation()
  except FehlerTyp as e:
      # Fehlerbehandlung
      print(f"Fehler aufgetreten: {e}")
  else:
      # Wird nur ausgefuehrt wenn KEIN Fehler auftrat
      print(f"Erfolgreich: {ergebnis}")
  finally:
      # Wird IMMER ausgefuehrt (Aufraeumen)
      ressource.schliessen()

Ausfuehrungsreihenfolge:
  1. try-Block wird ausgefuehrt
  2. Bei Fehler: passender except-Block
  3. Ohne Fehler: else-Block (falls vorhanden)
  4. Immer: finally-Block (falls vorhanden)


MEHRERE EXCEPTIONS BEHANDELN
----------------------------

Spezifische Exceptions zuerst, allgemeine zuletzt:

  def lade_konfiguration(pfad):
      try:
          with open(pfad, 'r') as f:
              daten = json.load(f)
              return daten['einstellungen']
      except FileNotFoundError:
          print(f"Datei nicht gefunden: {pfad}")
          return {}
      except json.JSONDecodeError as e:
          print(f"Ungueltige JSON-Syntax: {e}")
          return {}
      except KeyError:
          print("Schluessel 'einstellungen' fehlt")
          return {}
      except Exception as e:
          # Letzter Fallback - loggen und weiterwerfen
          print(f"Unerwarteter Fehler: {type(e).__name__}: {e}")
          raise

Mehrere Exceptions in einem Block:

  try:
      wert = int(eingabe)
      ergebnis = 100 / wert
  except (ValueError, ZeroDivisionError) as e:
      print(f"Ungueltige Eingabe: {e}")


HAEUFIGE EINGEBAUTE EXCEPTIONS
==============================

ALLGEMEINE EXCEPTIONS
---------------------
  Exception         Basisklasse fuer alle Fehler
  BaseException     Absolute Basisklasse (inkl. SystemExit, KeyboardInterrupt)

WERT- UND TYPFEHLER
-------------------
  ValueError        Wert hat falsches Format
                    int("abc")  # ValueError

  TypeError         Falscher Datentyp
                    "text" + 5  # TypeError
                    len(42)     # TypeError

ZUGRIFFSFEHLER
--------------
  KeyError          Schluessel nicht in Dictionary
                    d = {"a": 1}
                    d["b"]      # KeyError: 'b'

  IndexError        Index ausserhalb des Bereichs
                    liste = [1, 2, 3]
                    liste[10]   # IndexError

  AttributeError    Attribut oder Methode nicht vorhanden
                    "text".foo()  # AttributeError

DATEIFEHLER
-----------
  FileNotFoundError     Datei existiert nicht
  PermissionError       Keine Berechtigung
  IsADirectoryError     Erwartet Datei, ist Verzeichnis
  FileExistsError       Datei existiert bereits

IMPORTFEHLER
------------
  ImportError       Modul nicht gefunden
  ModuleNotFoundError  (Python 3.6+) Spezialisierung von ImportError

WEITERE WICHTIGE
----------------
  ZeroDivisionError     Division durch Null
  StopIteration         Iterator erschoepft
  RuntimeError          Allgemeiner Laufzeitfehler
  RecursionError        Maximale Rekursionstiefe ueberschritten
  MemoryError           Nicht genug Speicher
  OverflowError         Numerisches Ergebnis zu gross
  NotImplementedError   Methode nicht implementiert
  AssertionError        assert-Anweisung fehlgeschlagen


RAISE - EXCEPTIONS WERFEN
=========================

GRUNDLEGENDES RAISE
-------------------

  def teile(a, b):
      if b == 0:
          raise ValueError("Division durch Null nicht erlaubt")
      return a / b

  def setze_alter(alter):
      if not isinstance(alter, int):
          raise TypeError(f"Alter muss int sein, nicht {type(alter).__name__}")
      if alter < 0:
          raise ValueError("Alter kann nicht negativ sein")
      if alter > 150:
          raise ValueError("Unrealistisches Alter")
      self.alter = alter

RE-RAISE (WEITERWERFEN)
-----------------------

Exception nach Logging oder Teilbehandlung weiterwerfen:

  def verarbeite_datei(pfad):
      try:
          with open(pfad) as f:
              return verarbeite(f.read())
      except IOError as e:
          logger.error(f"Dateifehler bei {pfad}: {e}")
          raise  # Original-Exception mit vollem Traceback

RAISE FROM (EXCEPTION CHAINING)
-------------------------------

Neue Exception mit Ursache verknuepfen (Python 3):

  class KonfigurationsFehler(Exception):
      pass

  def lade_config(pfad):
      try:
          with open(pfad) as f:
              return json.load(f)
      except FileNotFoundError as e:
          raise KonfigurationsFehler(f"Config nicht gefunden: {pfad}") from e
      except json.JSONDecodeError as e:
          raise KonfigurationsFehler(f"Ungueltige Config-Syntax") from e

Ausgabe zeigt Verkettung:
  KonfigurationsFehler: Config nicht gefunden: config.json

  The above exception was the direct cause of the following exception:

  FileNotFoundError: [Errno 2] No such file or directory: 'config.json'

Kette unterdruecken (selten sinnvoll):
  raise NeuerFehler("Nachricht") from None


EIGENE EXCEPTIONS ERSTELLEN
===========================

EINFACHE CUSTOM EXCEPTION
-------------------------

  class AnwendungsFehler(Exception):
      """Basis fuer alle Anwendungsfehler."""
      pass

  class ValidierungsFehler(AnwendungsFehler):
      """Fehler bei Datenvalidierung."""
      pass

  class DatenbankFehler(AnwendungsFehler):
      """Fehler bei Datenbankoperationen."""
      pass

EXCEPTION MIT ZUSAETZLICHEN ATTRIBUTEN
--------------------------------------

  class APIFehler(Exception):
      """Fehler bei API-Aufrufen mit Statuscode."""

      def __init__(self, message, status_code, response=None):
          super().__init__(message)
          self.status_code = status_code
          self.response = response

      def __str__(self):
          return f"[{self.status_code}] {super().__str__()}"

  # Verwendung
  try:
      raise APIFehler("Nicht autorisiert", 401)
  except APIFehler as e:
      print(f"API-Fehler: {e}")
      print(f"Status: {e.status_code}")

EXCEPTION-HIERARCHIE FUER BIBLIOTHEKEN
--------------------------------------

  class BibliothekFehler(Exception):
      """Basisklasse fuer alle Bibliotheksfehler."""
      pass

  class VerbindungsFehler(BibliothekFehler):
      """Netzwerkverbindung fehlgeschlagen."""
      pass

  class ZeitablaufFehler(VerbindungsFehler):
      """Verbindung wegen Timeout abgebrochen."""
      pass

  class AuthentifizierungsFehler(BibliothekFehler):
      """Authentifizierung fehlgeschlagen."""
      pass

Benutzer koennen spezifisch oder allgemein fangen:
  try:
      bibliothek.verbinde()
  except ZeitablaufFehler:
      # Spezifisch: Timeout
      print("Timeout - erneut versuchen?")
  except VerbindungsFehler:
      # Alle Verbindungsfehler
      print("Verbindungsproblem")
  except BibliothekFehler:
      # Alle Bibliotheksfehler
      print("Bibliotheksfehler")


ASSERTIONS
==========

GRUNDLEGENDE VERWENDUNG
-----------------------

  assert bedingung, "Fehlermeldung"

  # Aequivalent zu:
  if not bedingung:
      raise AssertionError("Fehlermeldung")

WANN ASSERTIONS VERWENDEN
-------------------------

RICHTIG - Fuer Programmierfehler und interne Invarianten:

  def berechne_durchschnitt(werte):
      assert len(werte) > 0, "Liste darf nicht leer sein"
      return sum(werte) / len(werte)

  def sortiere(liste):
      # ... Sortierlogik ...
      assert ist_sortiert(liste), "Interner Fehler: Liste nicht sortiert"
      return liste

FALSCH - Nicht fuer Benutzereingaben oder erwartete Fehler:

  # NIEMALS SO:
  assert benutzername, "Benutzername erforderlich"  # FALSCH!
  assert alter >= 18, "Mindestalter 18"              # FALSCH!

  # RICHTIG:
  if not benutzername:
      raise ValueError("Benutzername erforderlich")
  if alter < 18:
      raise ValueError("Mindestalter 18")

Grund: Assertions koennen mit -O Flag deaktiviert werden:
  python -O script.py  # Assertions werden ignoriert!


CONTEXT MANAGER UND FEHLERBEHANDLUNG
====================================

MIT WITH-STATEMENT
------------------

  # Ressource wird automatisch geschlossen, auch bei Fehler
  with open("datei.txt") as f:
      inhalt = f.read()
  # Datei ist hier garantiert geschlossen

MEHRERE RESSOURCEN
------------------

  with open("quelle.txt") as quelle, open("ziel.txt", "w") as ziel:
      ziel.write(quelle.read())

EIGENER CONTEXT MANAGER
-----------------------

  from contextlib import contextmanager

  @contextmanager
  def datenbankverbindung(host, port):
      verbindung = erstelle_verbindung(host, port)
      try:
          yield verbindung
      except Exception as e:
          verbindung.rollback()
          raise
      else:
          verbindung.commit()
      finally:
          verbindung.close()

  # Verwendung
  with datenbankverbindung("localhost", 5432) as db:
      db.execute("INSERT INTO users VALUES (%s)", (name,))


BEST PRACTICES
==============

1. SPEZIFISCHE EXCEPTIONS FANGEN
   # Schlecht
   try:
       operation()
   except Exception:
       pass  # Verschluckt ALLE Fehler!

   # Gut
   try:
       operation()
   except (ValueError, KeyError) as e:
       handle_error(e)

2. NICHT BARE EXCEPT VERWENDEN
   # Sehr schlecht - faengt auch SystemExit, KeyboardInterrupt
   try:
       operation()
   except:
       pass

   # Wenn unbedingt noetig, mindestens loggen
   except Exception as e:
       logger.exception("Unerwarteter Fehler")
       raise

3. FEHLER NICHT VERSCHLUCKEN
   # Schlecht
   try:
       wichtige_operation()
   except:
       pass  # Fehler verschwindet spurlos

   # Besser
   try:
       wichtige_operation()
   except SomeFehler as e:
       logger.warning(f"Operation fehlgeschlagen: {e}")
       # Fallback oder Re-raise

4. EAFP VS LBYL
   # LBYL (Look Before You Leap) - nicht pythonic
   if "key" in dictionary:
       wert = dictionary["key"]

   # EAFP (Easier to Ask Forgiveness) - pythonic
   try:
       wert = dictionary["key"]
   except KeyError:
       wert = default_wert

5. EXCEPTION-NACHRICHT INFORMATIV GESTALTEN
   # Schlecht
   raise ValueError("Fehler")

   # Gut
   raise ValueError(
       f"Alter muss zwischen 0 und 150 liegen, erhalten: {alter}"
   )

6. CLEANUP MIT FINALLY ODER CONTEXT MANAGER
   # Mit finally
   ressource = oeffne_ressource()
   try:
       verarbeite(ressource)
   finally:
       ressource.schliesse()

   # Besser: Context Manager
   with oeffne_ressource() as ressource:
       verarbeite(ressource)


DEBUGGING-TIPPS
===============

VOLLSTAENDIGEN TRACEBACK ANZEIGEN
---------------------------------

  import traceback

  try:
      fehlerhafte_funktion()
  except Exception:
      traceback.print_exc()

EXCEPTION-INFORMATIONEN EXTRAHIEREN
-----------------------------------

  import sys

  try:
      fehlerhafte_funktion()
  except Exception:
      exc_type, exc_value, exc_tb = sys.exc_info()
      print(f"Typ: {exc_type.__name__}")
      print(f"Nachricht: {exc_value}")
      print(f"Datei: {exc_tb.tb_frame.f_code.co_filename}")
      print(f"Zeile: {exc_tb.tb_lineno}")


SIEHE AUCH
==========
  wiki/python/testing/
  wiki/python/logging/
  wiki/python/debugging/
  wiki/python/kontrollstrukturen/
