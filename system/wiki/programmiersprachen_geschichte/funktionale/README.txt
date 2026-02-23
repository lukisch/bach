# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: ACM Digital Library, Lambda Papers, Haskell.org, erlang.org

PROGRAMMIERSPRACHEN: FUNKTIONALE PROGRAMMIERUNG
================================================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
EINLEITUNG
================================================================================

Die funktionale Programmierung ist ein Programmierparadigma, das Berechnungen
als Auswertung mathematischer Funktionen betrachtet. Im Gegensatz zur
imperativen Programmierung, die Zustandsaenderungen und Anweisungsfolgen
verwendet, basiert die funktionale Programmierung auf dem Lambda-Kalkuel
von Alonzo Church (1936).

Dieses Paradigma hat seine Wurzeln in der mathematischen Logik und hat
ueber Jahrzehnte hinweg die Entwicklung moderner Programmiersprachen
massgeblich beeinflusst.

================================================================================
HISTORISCHE ENTWICKLUNG
================================================================================

DIE ANFAENGE (1930er-1950er)
----------------------------

  1936: Alonzo Church entwickelt den Lambda-Kalkuel
        - Formales System zur Berechnung
        - Grundlage aller funktionalen Sprachen
        - Aequivalent zur Turing-Maschine

  1956: Information Processing Language (IPL)
        - Entwickelt bei RAND Corporation
        - Erste Listenverarbeitung
        - Einfluss auf LISP

  1958: LISP (LISt Processing)
        - John McCarthy am MIT
        - Erste funktionale Programmiersprache
        - Revolutionaere Konzepte:
          * Garbage Collection
          * Homoikonizitaet (Code als Daten)
          * Rekursive Funktionen
          * Dynamische Typisierung

DIE FORMALISIERUNG (1960er-1970er)
----------------------------------

  1966: ISWIM (If you See What I Mean)
        - Peter Landin
        - Theoretisches Konzept
        - Einfuehrung von "let" und "where"
        - Beeinflusste alle nachfolgenden Sprachen

  1973: ML (Meta Language)
        - Robin Milner an der Universitaet Edinburgh
        - Urspruenglich fuer LCF Theorem Prover
        - Wichtige Innovationen:
          * Hindley-Milner Typsystem
          * Typinferenz
          * Polymorphismus
          * Pattern Matching
        - Nachfolger: Standard ML (1983), OCaml (1996), F# (2005)

  1975: Scheme
        - Guy Steele und Gerald Sussman (MIT)
        - Minimalistischer LISP-Dialekt
        - Lexikalische Bindung
        - Tail-Call-Optimierung
        - Einfluss auf JavaScript

DIE REIFUNG (1980er-1990er)
---------------------------

  1985: Miranda
        - David Turner
        - Rein funktional
        - Lazy Evaluation
        - Vorlaeufer von Haskell

  1986: Erlang
        - Ericsson (Joe Armstrong, Robert Virding, Mike Williams)
        - Entwickelt fuer Telekommunikation
        - Schwerpunkte:
          * Concurrency (leichtgewichtige Prozesse)
          * Fehlertoleranz ("Let it crash")
          * Hot Code Swapping
          * Actor Model
        - Elixir (2011) als moderne Alternative

  1990: Haskell
        - Komitee-Entwurf (Simon Peyton Jones u.a.)
        - Benannt nach Haskell Curry
        - Rein funktional (purely functional)
        - Lazy Evaluation als Standard
        - Starke statische Typisierung
        - Typklassen
        - Monaden fuer Seiteneffekte

MODERNE ENTWICKLUNG (2000er-heute)
----------------------------------

  2003: Scala
        - Martin Odersky (EPFL Lausanne)
        - JVM-basiert
        - Fusion von OOP und funktional
        - Akka Framework (Actors)
        - Apache Spark

  2007: Clojure
        - Rich Hickey
        - Moderner LISP-Dialekt auf JVM
        - Immutable Data Structures
        - Software Transactional Memory
        - ClojureScript fuer Browser

  2012: Elm
        - Evan Czaplicki
        - Frontend-Entwicklung
        - Keine Runtime Exceptions
        - Virtual DOM (Einfluss auf React)

  2015-heute: Funktionale Features in Mainstream-Sprachen
        - Java 8: Lambda-Ausdruecke, Streams
        - C++11/14/17: Lambdas, std::function
        - Python: map, filter, reduce, comprehensions
        - JavaScript ES6: Arrow Functions
        - Rust: Funktionale Elemente, Pattern Matching

================================================================================
KERNKONZEPTE
================================================================================

FUNKTIONEN ALS FIRST-CLASS CITIZENS
-----------------------------------
  Funktionen koennen wie normale Werte behandelt werden:
  - Als Argument uebergeben
  - Als Rueckgabewert zurueckgeben
  - In Variablen speichern
  - In Datenstrukturen ablegen

  Beispiel (Haskell):
    map :: (a -> b) -> [a] -> [b]
    map f []     = []
    map f (x:xs) = f x : map f xs

PURE FUNCTIONS (REINE FUNKTIONEN)
---------------------------------
  - Gleiches Input liefert immer gleiches Output
  - Keine Seiteneffekte
  - Referenzielle Transparenz
  - Vorteile:
    * Einfacheres Testen
    * Parallelisierbar
    * Memoization moeglich
    * Mathematisch beweisbar

IMMUTABILITY (UNVERAENDERLICHKEIT)
----------------------------------
  - Daten werden nicht veraendert, sondern kopiert
  - Neue Versionen statt Mutation
  - Vorteile:
    * Thread-Sicherheit
    * Einfacheres Debugging
    * Zeitreisen (Undo/Redo)
    * Persistente Datenstrukturen

HIGHER-ORDER FUNCTIONS
----------------------
  Funktionen, die andere Funktionen als Parameter nehmen oder zurueckgeben:

  - map:    Transformation jedes Elements
  - filter: Auswahl nach Praedikat
  - reduce/fold: Aggregation zu einem Wert
  - compose: Verkettung von Funktionen

  Beispiel (Haskell):
    -- Quadratzahlen der geraden Zahlen summieren
    sumEvenSquares = sum . map (^2) . filter even

LAZY EVALUATION
---------------
  - Ausdruecke werden erst bei Bedarf ausgewertet
  - Unendliche Datenstrukturen moeglich
  - Effiziente Verarbeitung grosser Datenmengen

  Beispiel (Haskell):
    -- Unendliche Liste aller natuerlichen Zahlen
    naturals = [1..]

    -- Nur die ersten 10 werden berechnet
    take 10 naturals  -- [1,2,3,4,5,6,7,8,9,10]

PATTERN MATCHING
----------------
  - Strukturelle Zerlegung von Daten
  - Elegante Fallunterscheidung
  - Exhaustiveness Checking

  Beispiel (Haskell):
    fibonacci :: Integer -> Integer
    fibonacci 0 = 0
    fibonacci 1 = 1
    fibonacci n = fibonacci (n-1) + fibonacci (n-2)

MONADEN
-------
  - Abstraktion fuer Berechnungen mit Kontext
  - Sequenzierung von Operationen
  - Behandlung von Seiteneffekten in reinen Sprachen

  Wichtige Monaden:
    - Maybe/Option: Optionale Werte
    - Either/Result: Fehlerbehandlung
    - IO: Ein-/Ausgabe
    - State: Zustandsverwaltung
    - List: Nichtdeterminismus

================================================================================
WICHTIGE SPRACHEN IM DETAIL
================================================================================

HASKELL
-------
  Eigenschaften:
    - Rein funktional (kein imperatives Entkommen)
    - Starke statische Typisierung mit Typinferenz
    - Lazy Evaluation (standardmaessig)
    - Typklassen fuer Ad-hoc-Polymorphismus
    - GHC als hochoptimierender Compiler

  Anwendungsgebiete:
    - Compiler-Entwicklung (GHC selbst)
    - Finanzsektor (Standard Chartered, Barclays)
    - Kryptographie (Cardano Blockchain)
    - Forschung und Lehre

  Codebeispiel:
    -- Quicksort in Haskell
    quicksort :: Ord a => [a] -> [a]
    quicksort []     = []
    quicksort (x:xs) = quicksort smaller ++ [x] ++ quicksort larger
      where
        smaller = [a | a <- xs, a <= x]
        larger  = [a | a <- xs, a > x]

ERLANG/OTP
----------
  Eigenschaften:
    - Leichtgewichtige Prozesse (Millionen moeglich)
    - Message Passing (kein Shared State)
    - Supervisors fuer Fehlerbehandlung
    - Hot Code Swapping
    - OTP Framework fuer robuste Systeme

  Anwendungsgebiete:
    - Telekommunikation (Ericsson AXD301)
    - Messaging (WhatsApp, Discord)
    - Datenbanken (CouchDB, Riak)
    - RabbitMQ Message Broker

  Codebeispiel:
    %% Einfacher Server in Erlang
    loop(State) ->
        receive
            {get, Pid} ->
                Pid ! {ok, State},
                loop(State);
            {set, NewState} ->
                loop(NewState);
            stop ->
                ok
        end.

LISP-DIALEKTE
-------------
  Common Lisp:
    - ANSI-standardisiert (1994)
    - Multi-Paradigma
    - Leistungsstarkes Makrosystem
    - CLOS (Common Lisp Object System)

  Scheme:
    - Minimalistisch
    - Lexikalische Bindung
    - Continuations
    - R7RS Standard

  Clojure:
    - Moderner Ansatz
    - JVM-Integration
    - Persistente Datenstrukturen
    - Concurrency-Primitiven

================================================================================
EINFLUSS AUF MODERNE PROGRAMMIERUNG
================================================================================

LAMBDA-AUSDRUECKE
-----------------
  Heute in fast allen Sprachen verfuegbar:

  Java:      list.stream().filter(x -> x > 5).map(x -> x * 2)
  C++:       auto square = [](int x) { return x * x; };
  Python:    square = lambda x: x * x
  JavaScript: const square = x => x * x;
  C#:        Func<int, int> square = x => x * x;

FUNKTIONALE DATENVERARBEITUNG
-----------------------------
  - Stream APIs (Java, C#)
  - LINQ (C#, F#)
  - Array-Methoden (JavaScript: map, filter, reduce)
  - Comprehensions (Python, Haskell)

REAKTIVE PROGRAMMIERUNG
-----------------------
  - RxJS, RxJava, Reactor
  - Funktionale Konzepte fuer Ereignisströme
  - Einfluss von Functional Reactive Programming (FRP)

UNVERAENDERLICHE DATENSTRUKTUREN
--------------------------------
  - Immutable.js (JavaScript)
  - Immer (JavaScript)
  - Vavr (Java)
  - Redux (React State Management)

================================================================================
VOR- UND NACHTEILE
================================================================================

VORTEILE
--------
  + Weniger Bugs durch Immutability
  + Einfachere Parallelisierung
  + Bessere Testbarkeit
  + Mathematische Beweisbarkeit
  + Modularer, wiederverwendbarer Code
  + Concise und expressiv

NACHTEILE
---------
  - Steilere Lernkurve
  - Performance-Overhead bei naiver Implementierung
  - Schwieriger fuer I/O-lastige Programme
  - Weniger intuitiv fuer imperative Denker
  - Kleineres Oekosystem als Mainstream-Sprachen

================================================================================
ZUKUNFTSPERSPEKTIVEN
================================================================================

  - Zunehmende Integration in Mainstream-Sprachen
  - Wachsende Bedeutung durch Multicore-Prozessoren
  - Einfluss auf UI-Frameworks (React, Elm Architecture)
  - Algebraische Effekte als Alternative zu Monaden
  - Dependently Typed Languages (Idris, Agda)

================================================================================
SIEHE AUCH
================================================================================

  wiki/python/generators/
  wiki/python/decorators/
  wiki/python/comprehensions/
  wiki/java/streams/
  wiki/javascript/funktional/
  wiki/programmiersprachen_geschichte/paradigmen/

================================================================================
WEITERFUEHRENDE RESSOURCEN
================================================================================

  Buecher:
    - "Structure and Interpretation of Computer Programs" (SICP)
    - "Learn You a Haskell for Great Good!"
    - "Programming Erlang" (Joe Armstrong)
    - "Functional Programming in Scala" (Red Book)

  Online:
    - haskell.org
    - erlang.org
    - clojure.org
    - elm-lang.org

================================================================================
