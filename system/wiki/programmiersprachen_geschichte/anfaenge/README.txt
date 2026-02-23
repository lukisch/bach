================================================================================
PROGRAMMIERSPRACHEN: DIE ANFAENGE (1940er - 1960er)
================================================================================

+------------------------------------------------------------------------------+
| METADATEN                                                                    |
+------------------------------------------------------------------------------+
| Portabilitaet:     UNIVERSAL                                                 |
| Zuletzt validiert: 2026-02-05                                                |
| Naechste Pruefung: 2027-02-05                                                |
| Quellen:           IEEE Annals of Computing, ACM History Committee,          |
|                    Computer History Museum, Original-Dokumentationen         |
+------------------------------------------------------------------------------+

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
EINFUEHRUNG
================================================================================

Die Geschichte der Programmiersprachen beginnt in den 1940er Jahren, als die
ersten elektronischen Computer entwickelt wurden. Diese Aera markiert einen
fundamentalen Wandel in der Mensch-Maschine-Interaktion: Vom direkten
Verdrahten von Schaltkreisen hin zur abstrakten Formulierung von Anweisungen.

Die Entwicklung der fruehen Programmiersprachen war getrieben von einem
zentralen Problem: Die direkte Programmierung in Maschinencode war extrem
fehleranfaellig, zeitaufwendig und erforderte tiefes Wissen ueber die
spezifische Hardware. Jede Verbesserung der Abstraktion bedeutete eine
enorme Steigerung der Produktivitaet.

================================================================================
TEIL I: DIE VORGESCHICHTE - MASCHINENNAHE PROGRAMMIERUNG
================================================================================

MASCHINENCODE (1940er)
----------------------

Der Maschinencode ist die unterste Ebene der Programmierung. Er besteht
ausschliesslich aus binaeren Zahlen (0 und 1), die direkt von der CPU
interpretiert werden.

Charakteristika:
  - Direkte CPU-Befehle in Binaerdarstellung
  - Vollstaendig hardwarespezifisch
  - Keine Abstraktion, keine Symbole
  - Extrem fehleranfaellig
  - Programme nicht portierbar

Historischer Kontext:
  Die ersten Programmierer wie Konrad Zuse, Grace Hopper und die ENIAC-
  Programmiererinnen (Kay McNulty, Betty Jennings, Betty Snyder, Marlyn
  Meltzer, Frances Bilas, Ruth Lichterman) mussten ihre Programme direkt
  in Maschinencode eingeben - oft durch das Setzen von Schaltern oder
  das Stecken von Kabeln.

Beispiel (vereinfacht, hypothetisch):
  10110000 00000101    ; Lade 5 in Register
  00000011 00000011    ; Addiere 3
  10001001 11000011    ; Speichere Ergebnis

--------------------------------------------------------------------------------

ASSEMBLERSPRACHEN (1947-1950er)
-------------------------------

Assembler war die erste echte Abstraktion ueber dem Maschinencode. Statt
binaerer Zahlen verwendet Assembler mnemonische Abkuerzungen (Mnemonics).

Entstehung:
  - 1947: Kathleen Booth entwickelt das Konzept der Assemblersprache
  - 1949: EDSAC Initial Orders (Cambridge) - erster praktischer Assembler
  - 1950er: Verbreitung auf verschiedenen Computersystemen

Charakteristika:
  - 1:1 Abbildung auf Maschinencode (eine Zeile = ein CPU-Befehl)
  - Verwendung von symbolischen Namen statt Adressen
  - Hardwarenah, aber lesbar
  - Assembler-Programm uebersetzt in Maschinencode

Beispiel (x86 Assembler):
  +------------------------------------------+
  |  MOV  AX, 5       ; Lade 5 in Register AX|
  |  ADD  AX, 3       ; Addiere 3            |
  |  MOV  BX, AX      ; Kopiere nach BX      |
  |  INT  21h         ; Systemaufruf         |
  +------------------------------------------+

Bedeutung:
  - Erste Abstraktion ueber Hardware
  - Erhoehte Lesbarkeit und Wartbarkeit
  - Ermoeglichte symbolische Sprungmarken (Labels)
  - Grundlage fuer alle hoehere Sprachen
  - Bis heute relevant fuer systemnahe Programmierung

================================================================================
TEIL II: DIE ERSTEN HOCHSPRACHEN
================================================================================

FORTRAN (1957) - Die erste echte Hochsprache
--------------------------------------------

FORTRAN (FORmula TRANslation) gilt als die erste weit verbreitete Hochsprache
und revolutionierte die wissenschaftliche Programmierung.

Entstehung:
  - Entwickelt bei IBM unter Leitung von John Backus
  - Team: John Backus, Harlan Herrick, Peter Sheridan, Roy Nutt u.a.
  - Projekt begann 1954, erste Version 1957
  - Entwickelt fuer den IBM 704

Designziele:
  - Mathematische Formeln direkt ausdruecken
  - Automatische Optimierung des generierten Codes
  - Effizienz vergleichbar mit handgeschriebenem Assembler
  - Vereinfachung wissenschaftlicher Berechnungen

Sprachmerkmale (FORTRAN I-IV):
  - Mathematische Ausdrucke in gewohnter Notation
  - DO-Schleifen fuer Wiederholungen
  - IF-Anweisungen fuer Verzweigungen
  - SUBROUTINE und FUNCTION fuer Modularisierung
  - Implizite Typisierung (I-N = INTEGER, sonst REAL)
  - Formatierte Ein-/Ausgabe

Beispiel (FORTRAN 77):
  +----------------------------------------------------------+
  |        PROGRAM SUMME                                     |
  |        INTEGER I, N, S                                   |
  |        S = 0                                             |
  |        N = 100                                           |
  |        DO 10 I = 1, N                                    |
  |            S = S + I                                     |
  |   10   CONTINUE                                          |
  |        PRINT *, 'Summe 1 bis 100:', S                    |
  |        END                                               |
  +----------------------------------------------------------+

Historische Bedeutung:
  - Bewies, dass Hochsprachen praktikabel sind
  - Erzeugte Code mit nur 20% Overhead gegenueber Assembler
  - Etablierte das Konzept des Compilers
  - Standardisierung (FORTRAN 66, 77, 90, 95, 2003, 2008, 2018, 2023)

Heutiger Status:
  - Immer noch in aktivem Einsatz
  - Dominant im High Performance Computing (HPC)
  - Wissenschaftliche Simulationen, Wettervorhersage
  - Riesige Codebasis in Forschungseinrichtungen

--------------------------------------------------------------------------------

LISP (1958) - Geburt der funktionalen Programmierung
----------------------------------------------------

LISP (LISt Processing) ist eine der aeltesten noch verwendeten Sprachen und
begruendete das Paradigma der funktionalen Programmierung.

Entstehung:
  - Entwickelt von John McCarthy am MIT
  - Erste Implementierung 1958
  - Basiert auf Alonzo Churchs Lambda-Kalkuel
  - Urspruenglich fuer KI-Forschung konzipiert

Revolutionaere Konzepte:
  - Rekursion als fundamentales Konzept
  - Dynamische Typisierung
  - Automatische Speicherverwaltung (Garbage Collection)
  - Homoikonizitaet: Code = Daten (S-Expressions)
  - First-Class Functions
  - REPL (Read-Eval-Print Loop)
  - Symbolische Berechnung

Syntax (extrem minimalistisch):
  - Alles basiert auf Listen: (funktion arg1 arg2 ...)
  - Praefix-Notation
  - Klammern zur Strukturierung

Beispiel:
  +----------------------------------------------------------+
  |  ; Definition einer Funktion                             |
  |  (defun fakultaet (n)                                    |
  |    (if (<= n 1)                                          |
  |        1                                                 |
  |        (* n (fakultaet (- n 1)))))                       |
  |                                                          |
  |  ; Aufruf                                                |
  |  (fakultaet 5)  ; Ergebnis: 120                          |
  |                                                          |
  |  ; Listen-Operationen                                    |
  |  (car '(a b c))   ; Erstes Element: a                    |
  |  (cdr '(a b c))   ; Rest: (b c)                          |
  |  (cons 'x '(a b)) ; Neues Element: (x a b)               |
  +----------------------------------------------------------+

Dialekte und Nachfolger:
  - Common Lisp (1984, standardisiert)
  - Scheme (1975, minimalistisch, akademisch)
  - Emacs Lisp (Erweiterungssprache fuer Emacs)
  - Clojure (2007, auf JVM, modern)

Einfluss auf spaetere Sprachen:
  - Garbage Collection -> Java, Python, Go, etc.
  - Funktionale Konzepte -> ML, Haskell, Scala, JavaScript
  - Makrosysteme -> Rust, Julia
  - REPL -> Python, Ruby, JavaScript

--------------------------------------------------------------------------------

COBOL (1959) - Sprache der Geschaeftswelt
-----------------------------------------

COBOL (COmmon Business-Oriented Language) wurde fuer kaufmaennische
Anwendungen entwickelt und ist bis heute in Banken und Versicherungen
im Einsatz.

Entstehung:
  - Entwickelt durch CODASYL-Komitee (Conference on Data Systems Languages)
  - Hauptakteurin: Grace Hopper (bereits bekannt durch A-0 Compiler)
  - Erste Spezifikation: 1959
  - Ziel: Eine gemeinsame Sprache fuer alle Hersteller

Designphilosophie:
  - Lesbarkeit durch englisch-aehnliche Syntax
  - Selbstdokumentierender Code
  - Trennung von Daten und Prozeduren
  - Portabilitaet ueber verschiedene Systeme
  - Praezise Dezimalarithmetik fuer Finanzen

Programmstruktur (vier Divisionen):
  1. IDENTIFICATION DIVISION - Programm-Metadaten
  2. ENVIRONMENT DIVISION    - Hardware-Umgebung
  3. DATA DIVISION           - Datenstrukturen
  4. PROCEDURE DIVISION      - Programmlogik

Beispiel:
  +----------------------------------------------------------+
  |  IDENTIFICATION DIVISION.                                |
  |  PROGRAM-ID. GEHALTSBERECHNUNG.                          |
  |                                                          |
  |  DATA DIVISION.                                          |
  |  WORKING-STORAGE SECTION.                                |
  |  01 GEHALT        PIC 9(6)V99.                           |
  |  01 STEUER        PIC 9(5)V99.                           |
  |  01 NETTO-GEHALT  PIC 9(6)V99.                           |
  |                                                          |
  |  PROCEDURE DIVISION.                                     |
  |      MOVE 5000.00 TO GEHALT.                             |
  |      COMPUTE STEUER = GEHALT * 0.19.                     |
  |      SUBTRACT STEUER FROM GEHALT                         |
  |          GIVING NETTO-GEHALT.                            |
  |      DISPLAY "Netto: " NETTO-GEHALT.                     |
  |      STOP RUN.                                           |
  +----------------------------------------------------------+

Heutiger Status (Stand 2026):
  - Geschaetzte 220+ Milliarden Zeilen COBOL-Code weltweit
  - 95% der ATM-Transaktionen laufen auf COBOL
  - Banken, Versicherungen, Behoerden abhaengig
  - Akuter Mangel an COBOL-Programmierern
  - Migration schwierig und teuer

--------------------------------------------------------------------------------

ALGOL (1958/1960) - Die akademische Referenz
--------------------------------------------

ALGOL (ALGOrithmic Language) war die erste Sprache mit formaler Grammatik
und beeinflusste fast alle nachfolgenden imperativen Sprachen.

Entstehung:
  - ALGOL 58: Erste Version, internationales Komitee
  - ALGOL 60: Standardisiert, Backus-Naur-Form (BNF)
  - ALGOL 68: Maechtiger, aber komplexer
  - Beteiligt: John Backus, Peter Naur, Edsger Dijkstra u.a.

Revolutionaere Beitraege:
  - Backus-Naur-Form (BNF) fuer formale Sprachspezifikation
  - Blockstruktur mit BEGIN...END
  - Lexikalischer Scope (lokale Variablen)
  - Rekursion als Standard
  - Call-by-value und Call-by-name
  - Strukturierte Kontrollstrukturen

Beispiel (ALGOL 60):
  +----------------------------------------------------------+
  |  begin                                                   |
  |      integer i, sum;                                     |
  |      sum := 0;                                           |
  |      for i := 1 step 1 until 100 do                      |
  |          sum := sum + i;                                 |
  |      print(sum)                                          |
  |  end                                                     |
  +----------------------------------------------------------+

Einfluss:
  - Direkter Vorfahre von Pascal, C, und damit C++, Java, C#
  - BNF wird bis heute fuer Sprachspezifikationen verwendet
  - Strukturierte Programmierung wurde Standard
  - Akademischer Referenzpunkt fuer Jahrzehnte

================================================================================
TEIL III: ZUSAMMENFASSUNG UND VERMAECHTNIS
================================================================================

ZEITLEISTE
----------
  1947 - Erste Assemblersprachen-Konzepte (Kathleen Booth)
  1949 - EDSAC Initial Orders (erster praktischer Assembler)
  1954 - Beginn der FORTRAN-Entwicklung
  1957 - FORTRAN I veroeffentlicht
  1958 - LISP konzipiert (McCarthy), ALGOL 58
  1959 - COBOL spezifiziert
  1960 - ALGOL 60 standardisiert

WICHTIGE PERSOENLICHKEITEN
--------------------------
  John Backus     - FORTRAN, Backus-Naur-Form
  John McCarthy   - LISP, Begriff "Kuenstliche Intelligenz"
  Grace Hopper    - COBOL, A-0 Compiler, Begriff "Bug"
  Peter Naur      - ALGOL, BNF
  Edsger Dijkstra - ALGOL, strukturierte Programmierung
  Kathleen Booth  - Assembler-Konzept, ARC

FUNDAMENTALE KONZEPTE DIESER AERA
---------------------------------
  Abstraktion        -> Trennung von Hardware und Logik
  Compiler           -> Automatische Uebersetzung in Maschinencode
  Hochsprache        -> Menschenlesbare Programmierung
  Formale Grammatik  -> Praezise Sprachspezifikation
  Modularisierung    -> Wiederverwendbare Unterprogramme
  Rekursion          -> Selbstaufrufende Funktionen

VERMAECHTNIS
------------
Die Sprachen dieser Aera legten das Fundament fuer alles, was folgte:
  - FORTRAN zeigte, dass Hochsprachen praktikabel sind
  - LISP begruendete funktionale Programmierung und Garbage Collection
  - COBOL etablierte lesbare, geschaeftsorientierte Programmierung
  - ALGOL definierte die Syntax-Standards fuer Generationen

Bemerkenswert: Alle vier Sprachen (FORTRAN, LISP, COBOL, ALGOL-Nachfolger)
sind in verschiedenen Formen bis heute im Einsatz - ein Zeugnis ihrer
fundamentalen Bedeutung.

================================================================================
SIEHE AUCH
================================================================================

  wiki/programmiersprachen_geschichte/imperative/
  wiki/programmiersprachen_geschichte/funktionale/
  wiki/programmiersprachen_geschichte/strukturierte_aera/
  wiki/informatik/grundlagen/
  wiki/informatik/compiler/
  wiki/persoenlichkeiten/grace_hopper.txt
  wiki/persoenlichkeiten/john_mccarthy.txt

================================================================================
GEPLANTE VERTIEFENDE ARTIKEL
================================================================================

  [ ] assembler_grundlagen.txt
  [ ] fortran_versionen.txt
  [ ] cobol_in_der_praxis.txt
  [ ] lisp_dialekte.txt
  [ ] algol_einfluss.txt

================================================================================
                              Ende des Artikels
================================================================================
