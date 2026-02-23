# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: ACM History of Programming Languages (HOPL), Computer History Museum,
#          "The C Programming Language" (Kernighan & Ritchie), "Structured Programming"
#          (Dijkstra), IEEE Annals of the History of Computing

IMPERATIVE PROGRAMMIERUNG
=========================

Stand: 2026-02-05

================================================================================
TEIL 1: GRUNDLAGEN DES IMPERATIVEN PARADIGMAS
================================================================================

1.1 DEFINITION UND KERNKONZEPT
------------------------------
Imperative Programmierung beschreibt WIE ein Programm etwas tun soll,
durch eine Sequenz von Anweisungen, die den Programmzustand veraendern.

  ETYMOLOGIE:
    Vom lateinischen "imperare" = befehlen
    Der Code gibt dem Computer Befehle: "Tu dies, dann das!"

  GRUNDPRINZIP:
    - Programm = Folge von Anweisungen
    - Anweisungen aendern Zustand (Variablen, Speicher)
    - Ausfuehrung in definierter Reihenfolge
    - Computer als "Befehlsempfaenger"

  METAPHER:
    Kochrezept: "Nimm 2 Eier, schlage sie auf, ruehre um..."
    vs. Deklarativ: "Das Ergebnis soll Ruehrei sein."

1.2 ABGRENZUNG ZU ANDEREN PARADIGMEN
------------------------------------

  IMPERATIV VS. DEKLARATIV:
  -------------------------
  Imperativ:   WIE wird etwas gemacht?
  Deklarativ:  WAS soll das Ergebnis sein?

    BEISPIEL - Liste filtern:

    Imperativ (C-Stil):
      int filtered[100];
      int count = 0;
      for (int i = 0; i < n; i++) {
          if (array[i] > 10) {
              filtered[count++] = array[i];
          }
      }

    Deklarativ (SQL-Stil):
      SELECT * FROM array WHERE value > 10

  IMPERATIV VS. FUNKTIONAL:
  -------------------------
  Imperativ:   Zustandsaenderung durch Zuweisung
  Funktional:  Keine Seiteneffekte, Funktionen transformieren Daten

    BEISPIEL - Summe berechnen:

    Imperativ:
      sum = 0
      for i in range(len(numbers)):
          sum = sum + numbers[i]

    Funktional:
      sum = reduce(add, numbers)

1.3 KERNELEMENTE IMPERATIVER SPRACHEN
-------------------------------------

  1. VARIABLEN UND ZUWEISUNG:
     - Speicherplaetze mit Namen
     - Werte koennen geaendert werden
     - x = 5; x = x + 1; (Zuweisung, nicht Gleichung!)

  2. KONTROLLSTRUKTUREN:
     - Sequenz: Anweisung1; Anweisung2;
     - Selektion: if-else, switch
     - Iteration: while, for, do-while

  3. PROZEDUREN/FUNKTIONEN:
     - Zusammenfassung von Anweisungen
     - Parameter und Rueckgabewerte
     - Modularisierung des Codes

  4. DATENSTRUKTUREN:
     - Arrays, Records/Structs
     - Pointer/Referenzen
     - Zusammengesetzte Typen

================================================================================
TEIL 2: HISTORISCHE ENTWICKLUNG
================================================================================

2.1 DIE ANFAENGE (1940er-1950er)
--------------------------------

  MASCHINENSPRACHE:
    - Direkte CPU-Instruktionen (0101001...)
    - Voellig hardwareabhaengig
    - Extrem fehleranfaellig
    - Aber: Imperative Grundstruktur bereits vorhanden

  ASSEMBLER:
    - Mnemonische Codes (MOV, ADD, JMP)
    - 1:1-Entsprechung zu Maschinencode
    - Erste Abstraktion, immer noch imperativ
    - Beispiel:
        MOV AX, 5    ; Lade 5 in Register AX
        ADD AX, 3    ; Addiere 3
        MOV result, AX ; Speichere Ergebnis

  FORTRAN (1957):
    - FORmula TRANslation
    - Erste weit verbreitete Hochsprache
    - Entwickelt bei IBM (John Backus)
    - Fuer wissenschaftliches Rechnen
    - Imperative Grundstruktur mit Schleifen
    - Revolutionaer: Formeln statt Maschinencode

2.2 DIE STRUKTURIERTE REVOLUTION (1960er-1970er)
-------------------------------------------------
Der Wendepunkt: Von Spaghetti-Code zu strukturierter Programmierung.

  DAS PROBLEM - "SPAGHETTI CODE":
    - GOTO-Anweisungen ueberall
    - Unuebersichtlicher Kontrollfuss
    - Schwer zu verstehen und zu warten
    - Bugs kaum auffindbar

    BEISPIEL (BASIC mit GOTO):
      10 LET X = 1
      20 IF X > 10 THEN GOTO 60
      30 PRINT X
      40 LET X = X + 1
      50 GOTO 20
      60 END

  DIJKSTRAS REVOLUTION (1968):
    "Go To Statement Considered Harmful" - beruehmt-beruechtigter Brief

    KERNARGUMENTE:
      - GOTO verhindert Nachvollziehbarkeit
      - Code sollte linear lesbar sein
      - Strukturierte Konstrukte genuegen fuer alles

  DIE STRUKTURIERTE THESE:
    Jedes Programm kann mit nur drei Konstrukten geschrieben werden:
      1. SEQUENZ: Anweisungen hintereinander
      2. SELEKTION: if-then-else
      3. ITERATION: while-Schleife

    Bewiesen von Boehm und Jacopini (1966)

================================================================================
TEIL 3: DIE GROSSEN SPRACHEN DER AERA
================================================================================

3.1 BASIC (1964)
----------------
Beginners All-purpose Symbolic Instruction Code

  ENTSTEHUNG:
    - Dartmouth College
    - John Kemeny und Thomas Kurtz
    - Ziel: Programmieren fuer alle zugaenglich machen

  DESIGN-PHILOSOPHIE:
    - Einfach zu lernen
    - Interaktiv (sofortige Rueckmeldung)
    - Fehlertolerant
    - Zeilennummern fuer Struktur

  BEISPIEL-PROGRAMM:
    10 PRINT "Wie heisst du?"
    20 INPUT N$
    30 PRINT "Hallo, "; N$
    40 FOR I = 1 TO 5
    50   PRINT I; " ";
    60 NEXT I
    70 END

  BEDEUTUNG:
    - Demokratisierung der Programmierung
    - Heimcomputer-Aera (C64, Apple II, etc.)
    - Generationen lernten damit Programmieren

  EVOLUTION:
    - QuickBASIC (1985)
    - Visual Basic (1991) - Event-driven, GUI
    - VB.NET (2002) - Objektorientiert
    - VBA (Excel, Access) - noch heute relevant

3.2 PASCAL (1970)
-----------------
Niklaus Wirths Lehrsprache fuer strukturiertes Programmieren.

  ENTSTEHUNG:
    - ETH Zuerich
    - Niklaus Wirth
    - Benannt nach Blaise Pascal

  DESIGN-ZIELE:
    - Strukturierte Programmierung erzwingen
    - Klare, lesbare Syntax
    - Strenge Typpruefung
    - Ideal fuer die Lehre

  SPRACHMERKMALE:
    - Klare Trennung: Deklaration vor Ausfuehrung
    - Strikte Typisierung
    - Prozeduren und Funktionen
    - Records (Vorlaeufer von Structs)
    - Sets (Mengen als Datentyp)
    - Pointer (kontrolliert)

  BEISPIEL-PROGRAMM:
    program HelloWorld;
    var
      name: string;
      i: integer;
    begin
      writeln('Wie heisst du?');
      readln(name);
      writeln('Hallo, ', name, '!');

      for i := 1 to 5 do
        write(i, ' ');
      writeln;
    end.

  BEDEUTUNG:
    - Standard-Lehrsprache der 1970er-1990er
    - Beeinflusste viele Sprachen (Ada, Modula, Oberon)
    - Turbo Pascal machte es auf PCs populaer

  NACHFOLGER:
    - Modula-2 (1978) - Module, Concurrency
    - Oberon (1987) - Minimalistisch
    - Delphi (1995) - Objektorientiert, Windows-GUI
    - Free Pascal / Lazarus (Open Source, heute noch aktiv)

3.3 C (1972)
------------
Die einflussreichste Programmiersprache der Geschichte.

  ENTSTEHUNG:
    - Bell Labs
    - Dennis Ritchie
    - Entwickelt fuer Unix

  KONTEXT:
    - Unix sollte portabel werden
    - Assembler zu hardwarespezifisch
    - Vorlaeufer B (Ken Thompson) zu eingeschraenkt

  DESIGN-PHILOSOPHIE:
    - Systemnah, aber abstrakt genug
    - Effizienter Code
    - Programmierer weiss, was er tut
    - Portabilitaet durch Abstraktion

  KERNMERKMALE:

    DATENTYPEN:
      - char, int, float, double
      - Arrays
      - Structs
      - Pointers (maechtig und gefaehrlich)
      - Typedefs

    KONTROLLSTRUKTUREN:
      - if-else, switch
      - for, while, do-while
      - break, continue
      - goto (existiert, aber verphoent)

    FUNKTIONEN:
      - Modulare Programmierung
      - Header-Files fuer Deklarationen
      - Variadic Functions (printf)

    PRAEPROZESSOR:
      - #include - Dateien einbinden
      - #define - Makros definieren
      - #ifdef - Bedingte Kompilierung

  BEISPIEL-PROGRAMM:
    #include <stdio.h>

    int main() {
        char name[50];
        int i;

        printf("Wie heisst du? ");
        scanf("%s", name);
        printf("Hallo, %s!\n", name);

        for (i = 1; i <= 5; i++) {
            printf("%d ", i);
        }
        printf("\n");

        return 0;
    }

  REVOLUTIONAERE ASPEKTE:
    - Portabilitaet: Unix auf verschiedenen Maschinen
    - Effizienz: Nahe an Assembler
    - Bibliotheken: Wiederverwendbarer Code
    - Einfachheit: Kleiner Sprachkern

  DER ENORME EINFLUSS:
    Direkt beeinflusst:
      - C++ (C mit Klassen)
      - Objective-C (C mit Smalltalk-OOP)
      - C# (Microsoft's modernes C)

    Syntax uebernommen:
      - Java
      - JavaScript
      - PHP
      - Perl
      - Go
      - Rust (teilweise)

  C HEUTE:
    - Immer noch Top 2 in TIOBE-Index
    - Betriebssysteme (Linux, Windows-Kernel)
    - Embedded Systems
    - Compiler und Interpreter
    - Performance-kritische Anwendungen

================================================================================
TEIL 4: KONZEPTE IM DETAIL
================================================================================

4.1 VARIABLEN UND SPEICHERMODELL
--------------------------------

  VARIABLEN VERSTEHEN:
    - Variable = benannter Speicherplatz
    - Hat einen Typ (bestimmt Speichergroesse)
    - Hat einen Wert (aktueller Inhalt)
    - Hat einen Scope (Gueltigkeitsbereich)

  ZUWEISUNG IST KEINE GLEICHUNG:
    x = x + 1
    Mathematisch: Widerspruch (kein x erfuellt das)
    Imperativ: "Nimm den Wert von x, addiere 1, speichere zurueck"

  SPEICHERMODELL IN C:
    - Stack: Lokale Variablen, automatisch verwaltet
    - Heap: Dynamischer Speicher (malloc/free)
    - Globaler Bereich: Globale Variablen
    - Code-Bereich: Programminstruktionen

  POINTER - MACHT UND GEFAHR:
    int x = 42;
    int *p = &x;    // p zeigt auf x
    *p = 100;       // x ist jetzt 100

    Vorteile:
      - Direkter Speicherzugriff
      - Effiziente Datenstrukturen
      - Call-by-Reference

    Gefahren:
      - Null Pointer Dereference
      - Dangling Pointers
      - Buffer Overflows
      - Memory Leaks

4.2 KONTROLLSTRUKTUREN VERTIEFT
-------------------------------

  SEQUENZ:
    Die einfachste Struktur - Anweisungen hintereinander.

    statement1;
    statement2;
    statement3;

    Ausfuehrung: 1, dann 2, dann 3.

  SELEKTION (if-else):
    Verzweigung basierend auf Bedingung.

    if (bedingung) {
        // wahrer Zweig
    } else {
        // falscher Zweig
    }

    Varianten:
      - Einfaches if
      - if-else
      - if-else if-else (Ketten)
      - switch-case (Mehrfachauswahl)

  ITERATION (Schleifen):

    WHILE - Kopfgesteuert:
      while (bedingung) {
          // wird wiederholt, solange bedingung wahr
      }
      Kann 0-mal ausgefuehrt werden.

    DO-WHILE - Fussgesteuert:
      do {
          // mindestens einmal ausgefuehrt
      } while (bedingung);
      Wird mindestens 1-mal ausgefuehrt.

    FOR - Zaehlschleife:
      for (init; bedingung; inkrement) {
          // Schleifenkoerper
      }
      Kompakte Zaehler-Logik.

  VERSCHACHTELUNG:
    Kontrollstrukturen koennen beliebig verschachtelt werden:

    for (i = 0; i < 10; i++) {
        if (i % 2 == 0) {
            for (j = 0; j < i; j++) {
                printf("*");
            }
        }
    }

4.3 PROZEDUREN UND FUNKTIONEN
-----------------------------

  KONZEPT:
    - Zusammenfassung von Anweisungen unter einem Namen
    - Wiederverwendbar
    - Parameter fuer Eingabe
    - Rueckgabewert fuer Ausgabe

  FUNKTION IN C:
    int add(int a, int b) {
        return a + b;
    }

    // Aufruf:
    int result = add(3, 4);  // result = 7

  PARAMETER-UEBERGABE:

    CALL BY VALUE (Standard in C):
      - Kopie des Wertes wird uebergeben
      - Original bleibt unveraendert

      void increment(int x) {
          x = x + 1;  // Aendert nur lokale Kopie
      }

    CALL BY REFERENCE (ueber Pointer):
      - Adresse wird uebergeben
      - Original kann geaendert werden

      void increment(int *x) {
          *x = *x + 1;  // Aendert Original
      }

  REKURSION:
    Funktion ruft sich selbst auf.

    int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

    Achtung: Braucht Abbruchbedingung!

================================================================================
TEIL 5: BEST PRACTICES UND ANTI-PATTERNS
================================================================================

5.1 BEST PRACTICES
------------------

  LESBARKEIT:
    - Aussagekraeftige Variablennamen
    - Konsistente Einrueckung
    - Kurze Funktionen (eine Aufgabe pro Funktion)
    - Kommentare fuer das WARUM, nicht das WAS

    SCHLECHT:
      int f(int a, int b) { int c=a+b; return c; }

    BESSER:
      int calculateSum(int firstNumber, int secondNumber) {
          int sum = firstNumber + secondNumber;
          return sum;
      }

  STRUKTURIERUNG:
    - Zusammengehoerendes gruppieren
    - Trennung von Belangen (Separation of Concerns)
    - Keine globalen Variablen (wenn vermeidbar)
    - Modulare Aufteilung in Dateien

  DEFENSIVE PROGRAMMIERUNG:
    - Eingaben validieren
    - Fehler behandeln
    - Assertions fuer Annahmen
    - Keine Annahmen ueber fremden Code

    BEISPIEL:
      int divide(int a, int b) {
          if (b == 0) {
              fprintf(stderr, "Division by zero!\n");
              return 0;  // oder Fehlercode
          }
          return a / b;
      }

5.2 ANTI-PATTERNS VERMEIDEN
---------------------------

  GOTO-SPAGHETTI:
    Problem: Unkontrollierte Spruenge
    Loesung: Strukturierte Kontrollstrukturen

    Ausnahme: In C manchmal fuer Cleanup-Code akzeptiert:
      if (error) goto cleanup;
      ...
      cleanup:
          free(memory);
          return -1;

  MAGIC NUMBERS:
    SCHLECHT:
      if (age > 18) { ... }

    BESSER:
      #define LEGAL_AGE 18
      if (age > LEGAL_AGE) { ... }

  TIEFE VERSCHACHTELUNG:
    SCHLECHT:
      if (a) {
          if (b) {
              if (c) {
                  if (d) {
                      // schwer lesbar
                  }
              }
          }
      }

    BESSER:
      if (!a) return;
      if (!b) return;
      if (!c) return;
      if (!d) return;
      // Hauptlogik hier

  RIESENFUNKTIONEN:
    Problem: Funktionen mit 500+ Zeilen
    Loesung: Aufteilen in kleinere, benannte Einheiten

================================================================================
TEIL 6: ERBE UND VERMAECHTNIS
================================================================================

6.1 EINFLUSS AUF MODERNE SPRACHEN
---------------------------------
Das imperative Paradigma ist Grundlage fast aller modernen Sprachen.

  SYNTAX-EINFLUSS (C-Stil):
    - Geschweifte Klammern {} fuer Bloecke
    - Semikolon als Statement-Trenner
    - for (init; cond; incr) Schleifensyntax
    - = fuer Zuweisung, == fuer Vergleich

  SPRACHEN MIT C-SYNTAX:
    - C++ (Erweiterung von C)
    - Java (C++ ohne Pointer)
    - JavaScript (C-Syntax fuer Web)
    - C# (Microsoft's modernes C)
    - PHP (C-Syntax fuer Web)
    - Go, Rust (teilweise)

  KONZEPTUELLE UEBERNAHMEN:
    - Variablen und Zuweisung ueberall
    - Kontrollstrukturen (if, while, for)
    - Funktionen/Methoden
    - Typsysteme (statisch oder dynamisch)

6.2 IMPERATIVE ELEMENTE IN ANDEREN PARADIGMEN
---------------------------------------------

  OBJEKTORIENTIERUNG:
    - Methoden sind imperativ (Sequenz von Anweisungen)
    - Zustandsaenderung durch Methodenaufrufe
    - OOP = Imperative + Kapselung + Vererbung

  FUNKTIONALE SPRACHEN:
    - Viele erlauben imperative Elemente
    - Haskell: do-Notation fuer Sequenzen
    - OCaml: Mutable Variablen moeglich
    - Scala: Hybride Sprache

  SKRIPTSPRACHEN:
    - Python, Ruby, Perl: Grundsaetzlich imperativ
    - Mit funktionalen Elementen angereichert

6.3 WANN IMPERATIV HEUTE NOCH?
------------------------------

  GEEIGNET FUER:
    - Systemprogrammierung
    - Performance-kritische Teile
    - Echtzeitsysteme
    - Embedded Systems
    - Low-Level-Operationen
    - Wenn explizite Kontrolle noetig

  WENIGER GEEIGNET FUER:
    - Parallelisierung (geteilter Zustand problematisch)
    - Komplexe Transformationen (funktional eleganter)
    - Deklarative Domaenen (Datenbanken, UI-Binding)

================================================================================
TEIL 7: BACH-INTEGRATION
================================================================================

7.1 IMPERATIVES PROGRAMMIEREN MIT BACH
--------------------------------------
BACH unterstuetzt imperative Programmierung in verschiedenen Kontexten:

  BATCH-DATEIEN (Windows):
    - Sequentielle Befehle
    - @echo, set, if, for
    - Automatisierung von Aufgaben

  PYTHON-SCRIPTS:
    - Imperatives Grundparadigma
    - Klare Sequenzen von Aktionen
    - Ideale BACH-Integrationssprache

  SHELL-SCRIPTS (Bash/PowerShell):
    - Imperatives Paradigma
    - Systemautomatisierung
    - Dateiverwaltung

7.2 PRAXIS-EMPFEHLUNGEN
-----------------------
  - Einfache Automatisierungen: Imperativ optimal
  - Datenverarbeitung: Mix aus imperativ und funktional
  - Komplexe Logik: Strukturiert aufteilen
  - Bei Parallelitaet: Funktionale Anteile erhoehen

================================================================================

ZUSAMMENFASSUNG
===============
Die imperative Programmierung ist das Urparadigma der Softwareentwicklung.

  KERNKONZEPTE:
    1. Sequenz: Anweisungen nacheinander
    2. Selektion: Bedingte Verzweigung
    3. Iteration: Wiederholung
    4. Zustandsaenderung: Variablen modifizieren

  HISTORISCHE MEILENSTEINE:
    - 1964: BASIC - Programmieren fuer alle
    - 1970: Pascal - Strukturierte Programmierung
    - 1972: C - Die einflussreichste Sprache

  BLEIBENDES ERBE:
    - C-Syntax in vielen Sprachen
    - Kontrollstrukturen ueberall
    - Grundlage auch fuer OOP und andere Paradigmen

  MERKSATZ:
    "Ein imperatives Programm sagt dem Computer Schritt fuer Schritt,
     was er tun soll - wie ein detailliertes Kochrezept."

================================================================================

SIEHE AUCH
==========
  wiki/programmiersprachen_geschichte/anfaenge/
  wiki/programmiersprachen_geschichte/objektorientierte/
  wiki/programmiersprachen_geschichte/funktionale/
  wiki/informatik/programmierung/
  wiki/batch.txt

================================================================================
[Ende des Artikels - IMPERATIVE PROGRAMMIERUNG]
================================================================================
