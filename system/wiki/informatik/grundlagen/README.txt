# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: [Computer Science Fundamentals, Shannon 1948, von Neumann 1945]

INFORMATIK GRUNDLAGEN
=====================

Stand: 2026-02-05

WAS SIND INFORMATIK-GRUNDLAGEN?
===============================

Die Grundlagen der Informatik bilden das theoretische Fundament aller
Computersysteme und Software. Sie umfassen mathematische Konzepte,
Modelle der Berechenbarkeit und fundamentale Prinzipien der
Informationsverarbeitung.

Diese Konzepte sind zeitlos und aendern sich nicht mit neuen
Technologien - sie erklaeren WARUM Computer funktionieren.

BINAERSYSTEM (0 und 1)
======================

Das Binaersystem ist die Grundlage aller digitalen Computer.
Es verwendet nur zwei Ziffern: 0 und 1 (Bits).

  Warum binaer?
  -------------
  - Elektronische Schaltungen kennen nur AN/AUS
  - Zuverlaessiger als analoge Signale
  - Mathematisch einfach zu verarbeiten

  Umrechnung Dezimal -> Binaer
  ----------------------------
    13 (dezimal) = 1101 (binaer)

    8  4  2  1
    1  1  0  1  = 8+4+0+1 = 13

  Wichtige Einheiten
  ------------------
    1 Bit      = 0 oder 1
    1 Byte     = 8 Bit (Werte 0-255)
    1 Kilobyte = 1024 Byte
    1 Megabyte = 1024 KB
    1 Gigabyte = 1024 MB

BOOLESCHE LOGIK (AND, OR, NOT)
==============================

George Boole (1854) entwickelte eine Algebra fuer logische Aussagen.
Diese bildet die Grundlage aller Computerschaltungen.

  Grundoperationen
  ----------------

  AND (Konjunktion): Beide Eingaenge muessen 1 sein
    0 AND 0 = 0
    0 AND 1 = 0
    1 AND 0 = 0
    1 AND 1 = 1

  OR (Disjunktion): Mindestens ein Eingang muss 1 sein
    0 OR 0 = 0
    0 OR 1 = 1
    1 OR 0 = 1
    1 OR 1 = 1

  NOT (Negation): Kehrt den Wert um
    NOT 0 = 1
    NOT 1 = 0

  Abgeleitete Operationen
  -----------------------
    XOR  - Exklusiv-Oder (genau einer)
    NAND - NOT AND (Universal-Gatter)
    NOR  - NOT OR

  Anwendung
  ---------
  Aus diesen einfachen Operationen werden alle Berechnungen aufgebaut:
  - Addition, Subtraktion, Multiplikation
  - Vergleiche (gleich, groesser, kleiner)
  - Speicherung (Flip-Flops)

VON-NEUMANN-ARCHITEKTUR
=======================

John von Neumann beschrieb 1945 die Grundarchitektur moderner Computer.
Fast alle heutigen Rechner folgen diesem Prinzip.

  Komponenten
  -----------
    +------------------+
    |     CPU          |
    | +------------+   |
    | | Steuerwerk |   |
    | +------------+   |
    | | Rechenwerk |   |
    | +------------+   |
    +--------+---------+
             |
    +--------v---------+
    |    Speicher      |  <- Programme UND Daten
    |  (RAM/Festplatte)|     im gleichen Speicher
    +--------+---------+
             |
    +--------v---------+
    |   Ein-/Ausgabe   |
    | (Tastatur, Bild.)|
    +------------------+

  Kernprinzip
  -----------
  Programme und Daten liegen im gleichen Speicher.
  Das unterscheidet von Neumann von frueheren Rechnern,
  die feste Verdrahtung fuer Programme hatten.

  Von-Neumann-Flaschenhals
  ------------------------
  CPU und Speicher teilen sich einen Bus.
  Die CPU wartet oft auf Daten -> Geschwindigkeitsproblem.
  Moderne Loesungen: Caches, Pipeline, Parallelisierung.

INFORMATIONSTHEORIE (Shannon)
=============================

Claude Shannon (1948) begruendete die mathematische
Theorie der Information.

  Kernkonzepte
  ------------

  Information = Reduzierung von Unsicherheit

  Entropie (H): Mass fuer Informationsgehalt
    H = -SUM(p(x) * log2(p(x)))

    Beispiel: Faire Muenze
    H = -(0.5 * log2(0.5) + 0.5 * log2(0.5)) = 1 Bit

  Redundanz: Ueberfluessige Information
    Natuerliche Sprache hat ~50% Redundanz
    Ermoeglicht Kompression und Fehlerkorrektur

  Kanalkapazitaet: Maximale Uebertragungsrate
    Begrenzt durch Bandbreite und Rauschen

  Anwendungen
  -----------
  - Datenkompression (ZIP, MP3, JPEG)
  - Fehlerkorrektur (QR-Codes, CDs)
  - Kryptographie
  - Maschinelles Lernen

KOMPLEXITAETSTHEORIE (O-Notation)
=================================

Beschreibt, wie der Ressourcenbedarf eines Algorithmus
mit der Eingabegroesse waechst.

  Big-O-Notation
  --------------
  Gibt die obere Schranke des Wachstums an.

  Haeufige Komplexitaetsklassen (sortiert):

    O(1)       - Konstant
                 Beispiel: Array-Zugriff per Index

    O(log n)   - Logarithmisch
                 Beispiel: Binaere Suche

    O(n)       - Linear
                 Beispiel: Liste durchsuchen

    O(n log n) - Quasi-linear
                 Beispiel: Effiziente Sortierung (Merge Sort)

    O(n^2)     - Quadratisch
                 Beispiel: Bubble Sort, verschachtelte Schleifen

    O(2^n)     - Exponentiell
                 Beispiel: Brute-Force bei Verschluesselung

  P vs. NP Problem
  ----------------
  P:  Probleme, die in polynomieller Zeit loesbar sind
  NP: Probleme, deren Loesung in polynomieller Zeit pruefbar ist

  Ungeloeste Frage: Ist P = NP?
  (Eines der groessten offenen Probleme der Informatik)

AUTOMATENTHEORIE
================

Beschreibt abstrakte Maschinen und ihre Berechnungsfaehigkeit.

  Hierarchie (Chomsky)
  --------------------

  1. Endliche Automaten (DFA/NFA)
     - Erkennen: Regulaere Sprachen
     - Anwendung: Lexer, Pattern Matching

  2. Kellerautomaten (PDA)
     - Erkennen: Kontextfreie Sprachen
     - Anwendung: Parser, Syntaxanalyse

  3. Turingmaschinen
     - Erkennen: Rekursiv aufzaehlbare Sprachen
     - Modell: Universelle Berechenbarkeit

  Turing-Vollstaendigkeit
  -----------------------
  Ein System ist Turing-vollstaendig, wenn es alles
  berechnen kann, was eine Turingmaschine kann.

  Beispiele: Python, C, JavaScript, Excel (!)

  Halteproblem
  ------------
  Es ist unmoeglich, einen Algorithmus zu schreiben,
  der fuer JEDES Programm entscheidet, ob es terminiert.
  (Beweis durch Diagonalisierung, Turing 1936)

PRAKTISCHE RELEVANZ FUER BACH
=============================

Diese Grundlagen sind relevant fuer:

  - Datenbanken: Relationale Algebra (Mengenlehre)
  - Suche: Komplexitaet von Such-Algorithmen
  - KI/ML: Informationstheorie bei Entscheidungsbaeumen
  - Parsing: Automaten fuer Texterkennung
  - Speicher: Binaere Darstellung von Daten

LITERATUR
=========

  [1] Shannon, C. (1948): A Mathematical Theory of Communication
  [2] von Neumann, J. (1945): First Draft of a Report on the EDVAC
  [3] Turing, A. (1936): On Computable Numbers
  [4] Sipser, M.: Introduction to the Theory of Computation

SIEHE AUCH
==========
  wiki/informatik/algorithmen/     Algorithmen und Datenstrukturen
  wiki/informatik/hardware/        Hardware-Grundlagen
  wiki/informatik/datenbanken/     Datenbanktheorie
  wiki/python/grundlagen/          Python als Beispielsprache
