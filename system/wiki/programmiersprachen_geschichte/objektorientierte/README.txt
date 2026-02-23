# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: ACM Digital Library, Oracle Java Docs, Stroustrup.com, Smalltalk.org

PROGRAMMIERSPRACHEN: OBJEKTORIENTIERTE PROGRAMMIERUNG
=====================================================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
EINLEITUNG
================================================================================

Die objektorientierte Programmierung (OOP) ist ein Programmierparadigma, das
auf dem Konzept von "Objekten" basiert. Objekte sind Datenstrukturen, die
Zustand (Attribute/Felder) und Verhalten (Methoden) kapseln. OOP ermoeglicht
die Modellierung realer Probleme durch Abstraktion und wurde zum dominanten
Paradigma der Softwareentwicklung von den 1990ern bis heute.

Die Grundidee stammt aus der Simulation komplexer Systeme und wurde
massgeblich von Alan Kay gepraegt, der den Begriff "objektorientiert"
praegte und Smalltalk entwickelte.

================================================================================
HISTORISCHE ENTWICKLUNG
================================================================================

DIE URSPRUENGE (1960er)
-----------------------

  1962-1967: Simula (Simula 67)
        - Ole-Johan Dahl und Kristen Nygaard
        - Norwegian Computing Center, Oslo
        - Urspruenglich fuer Simulationen entwickelt
        - Erste Sprache mit OOP-Konzepten:
          * Klassen
          * Objekte
          * Vererbung
          * Virtuelle Methoden
        - Basis fuer alle nachfolgenden OOP-Sprachen
        - "Mutter aller objektorientierten Sprachen"

  1968: Alan Kays Vision
        - Inspiriert von Simula, LISP und Biologie
        - Konzept von "Messaging" zwischen Objekten
        - Zellen als Metapher fuer Objekte
        - Beginn der Arbeit an Smalltalk

DIE GEBURT VON SMALLTALK (1970er)
---------------------------------

  1972-1980: Smalltalk
        - Xerox PARC (Palo Alto Research Center)
        - Alan Kay, Dan Ingalls, Adele Goldberg
        - Smalltalk-72, Smalltalk-76, Smalltalk-80

        Revolutionaere Konzepte:
          * "Alles ist ein Objekt" (auch Zahlen, Klassen)
          * Message Passing als Grundprinzip
          * Dynamische Typisierung
          * Reflexion und Metaprogrammierung
          * Integrierte Entwicklungsumgebung (IDE)
          * Grafische Benutzeroberflaeche (GUI)
          * Model-View-Controller (MVC) Pattern

        Einfluss:
          * Apple Macintosh GUI
          * Objective-C
          * Ruby
          * Agile Entwicklung (XP, Scrum)

DIE PRAGMATISCHE REVOLUTION (1980er)
------------------------------------

  1979-1983: C++
        - Bjarne Stroustrup, Bell Labs
        - Urspruenglich "C with Classes"
        - Pragmatischer Ansatz: OOP + Effizienz von C

        Entwicklungsphasen:
          1979: Erste Version (C with Classes)
          1983: Umbenennung zu C++
          1985: Erstes Buch "The C++ Programming Language"
          1998: ISO-Standardisierung (C++98)
          2011: Modernes C++ (C++11)
          2014, 2017, 2020, 2023: Weitere Standards

        Eigenschaften:
          * Mehrfachvererbung
          * Templates (Generische Programmierung)
          * Operator Overloading
          * RAII (Resource Acquisition Is Initialization)
          * Deterministische Destruktoren
          * Kompatibilitaet mit C

  1983: Objective-C
        - Brad Cox und Tom Love
        - Smalltalk-inspiriertes Messaging auf C
        - NeXTSTEP (Steve Jobs)
        - Spaeter: Apple macOS, iOS (bis Swift)

  1986: Object Pascal / Turbo Pascal 5.5
        - Anders Hejlsberg (spaeter C#-Erfinder)
        - Borland Delphi
        - Wichtig fuer Desktop-Anwendungen

DIE MAINSTREAM-AERA (1990er)
----------------------------

  1991: Python
        - Guido van Rossum
        - "Batteries included"
        - Multi-Paradigma (OOP, funktional, prozedural)
        - Dynamisch typisiert
        - Lesbarkeit als Designziel
        - Heute: Data Science, KI, Web, Scripting

  1995: Java
        - Sun Microsystems
        - James Gosling, urspruenglich fuer Set-Top-Boxes
        - "Write Once, Run Anywhere" (WORA)

        Schluesselinnovationen:
          * Java Virtual Machine (JVM)
          * Automatische Garbage Collection
          * Keine Pointer (Referenzen stattdessen)
          * Einfachvererbung (keine Mehrfachvererbung)
          * Interfaces fuer Mehrfachschnittstellen
          * Applets (fruehe Web-Interaktivitaet)
          * Standardbibliothek (umfangreich)

        Einfluss:
          * Enterprise-Standard (Java EE)
          * Android-Entwicklung
          * Spring Framework
          * Grundlage fuer C#, Kotlin, Scala

  1995: JavaScript
        - Brendan Eich, Netscape
        - Prototypenbasierte OOP (nicht klassenbasiert)
        - Spaeter: ES6 mit class-Syntax (2015)
        - Heute dominante Web-Sprache

  1995: Ruby
        - Yukihiro "Matz" Matsumoto
        - Inspiriert von Smalltalk, Perl, Lisp
        - "Programmer Happiness"
        - Alles ist ein Objekt (wie Smalltalk)
        - Ruby on Rails (2004) revolutioniert Webentwicklung

  1995: PHP 3 (objektorientierte Erweiterungen)
        - Spaeter: PHP 5 (2004) mit vollem OOP-Support
        - WordPress, Drupal, Laravel

  1995: Delphi (Object Pascal)
        - Borland
        - RAD (Rapid Application Development)
        - Wichtig fuer Windows-Anwendungen

DIE MODERNE AERA (2000er-heute)
-------------------------------

  2000: C#
        - Microsoft, Anders Hejlsberg
        - Teil von .NET Framework
        - Stark von Java beeinflusst
        - Eigenschaften:
          * Properties (nicht nur Getter/Setter)
          * Events und Delegates
          * LINQ (Language Integrated Query)
          * Async/Await
          * Pattern Matching (neuere Versionen)

  2009: Go
        - Google (Rob Pike, Ken Thompson)
        - Minimalistisches OOP (keine Vererbung)
        - Interfaces implizit implementiert
        - Composition over Inheritance

  2010: Rust
        - Mozilla
        - Ownership-System statt GC
        - Traits statt Vererbung
        - Beeinflusst von ML und OOP

  2011: Kotlin
        - JetBrains
        - Moderne JVM-Sprache
        - Null Safety
        - Data Classes
        - Android-offiziell (2017)

  2014: Swift
        - Apple
        - Ersatz fuer Objective-C
        - Protokollorientierte Programmierung
        - Optionals fuer Null-Sicherheit

================================================================================
DIE VIER SAEULEN DER OOP
================================================================================

1. KAPSELUNG (ENCAPSULATION)
----------------------------
  Definition:
    Zusammenfassung von Daten und Methoden in einer Einheit (Klasse)
    mit kontrolliertem Zugriff von aussen.

  Zugriffsmodifikatoren:
    - private:   Nur innerhalb der Klasse
    - protected: Klasse und Unterklassen
    - public:    Ueberall zugreifbar
    - package/internal: Innerhalb des Pakets/Moduls

  Vorteile:
    - Implementierungsdetails versteckt
    - Invarianten schuetzen
    - API-Stabilitaet
    - Aenderungen ohne externe Auswirkungen

  Beispiel (Java):
    public class BankAccount {
        private double balance;  // Gekapselt

        public void deposit(double amount) {
            if (amount > 0) {
                balance += amount;
            }
        }

        public double getBalance() {
            return balance;
        }
    }

2. VERERBUNG (INHERITANCE)
--------------------------
  Definition:
    Mechanismus, bei dem eine Klasse (Unterklasse) Eigenschaften
    und Verhalten einer anderen Klasse (Oberklasse) uebernimmt.

  Arten:
    - Einfachvererbung: Eine Oberklasse (Java, C#)
    - Mehrfachvererbung: Mehrere Oberklassen (C++, Python)
    - Interface-Vererbung: Mehrere Schnittstellen

  Beispiel (Java):
    class Animal {
        void eat() { System.out.println("Eating"); }
    }

    class Dog extends Animal {
        void bark() { System.out.println("Woof!"); }
    }

    // Dog erbt eat() von Animal

  Probleme:
    - Fragile Base Class Problem
    - Diamond Problem (Mehrfachvererbung)
    - Tight Coupling

  Moderne Alternative:
    - Composition over Inheritance
    - Mixins/Traits

3. POLYMORPHISMUS
-----------------
  Definition:
    Die Faehigkeit, verschiedene Objekte ueber dieselbe Schnittstelle
    anzusprechen, wobei jedes Objekt anders reagieren kann.

  Arten:
    a) Subtyp-Polymorphismus (Laufzeit):
       - Ueberschreiben von Methoden
       - Dynamische Bindung
       - Virtuelle Methoden

    b) Ad-hoc-Polymorphismus (Kompilierzeit):
       - Method Overloading
       - Operator Overloading

    c) Parametrischer Polymorphismus:
       - Generics/Templates

  Beispiel (Java):
    interface Shape {
        double area();
    }

    class Circle implements Shape {
        double radius;
        public double area() { return Math.PI * radius * radius; }
    }

    class Rectangle implements Shape {
        double width, height;
        public double area() { return width * height; }
    }

    // Polymorphe Verwendung
    Shape[] shapes = {new Circle(), new Rectangle()};
    for (Shape s : shapes) {
        System.out.println(s.area());  // Dynamische Bindung
    }

4. ABSTRAKTION
--------------
  Definition:
    Reduktion auf wesentliche Eigenschaften, Verbergen von
    Komplexitaet durch Schnittstellen und abstrakte Klassen.

  Mechanismen:
    - Abstrakte Klassen (nicht instanziierbar)
    - Interfaces (reine Vertraege)
    - Abstract Methods

  Beispiel (Java):
    abstract class Vehicle {
        abstract void move();  // Muss implementiert werden

        void start() {         // Konkrete Methode
            System.out.println("Starting...");
        }
    }

    class Car extends Vehicle {
        void move() { System.out.println("Driving"); }
    }

================================================================================
WICHTIGE KONZEPTE
================================================================================

KLASSEN UND OBJEKTE
-------------------
  Klasse:
    - Bauplan/Schablone fuer Objekte
    - Definiert Attribute und Methoden
    - Statische Elemente gehoeren zur Klasse

  Objekt:
    - Instanz einer Klasse
    - Hat eigenen Zustand (Attributwerte)
    - Lebt zur Laufzeit im Speicher

KONSTRUKTOREN UND DESTRUKTOREN
------------------------------
  Konstruktor:
    - Initialisiert neues Objekt
    - Gleicher Name wie Klasse
    - Ueberladung moeglich

  Destruktor/Finalizer:
    - Aufraeumen vor Objektzerstoerung
    - C++: Deterministisch (RAII)
    - Java/C#: Garbage Collector (nicht deterministisch)

INTERFACES VS. ABSTRAKTE KLASSEN
--------------------------------
  Interface:
    - Nur Methodensignaturen (bis Java 8)
    - Mehrfachimplementierung moeglich
    - Vertrag ohne Implementierung

  Abstrakte Klasse:
    - Kann Implementierung enthalten
    - Nur Einfachvererbung
    - Gemeinsamer Code fuer Unterklassen

STATISCH VS. INSTANZ
--------------------
  Statisch (static):
    - Gehoert zur Klasse, nicht zum Objekt
    - Gemeinsam fuer alle Instanzen
    - Factory Methods, Utilities

  Instanz:
    - Gehoert zum einzelnen Objekt
    - Jedes Objekt hat eigene Kopie

================================================================================
DESIGN PATTERNS
================================================================================

Die "Gang of Four" (GoF) dokumentierte 23 Entwurfsmuster (1994):

ERZEUGUNGSMUSTER
----------------
  - Singleton: Eine Instanz garantieren
  - Factory Method: Objekterzeugung delegieren
  - Abstract Factory: Familien von Objekten
  - Builder: Komplexe Objekte schrittweise
  - Prototype: Klonen statt Erzeugen

STRUKTURMUSTER
--------------
  - Adapter: Schnittstellen anpassen
  - Decorator: Dynamisch Funktionalitaet hinzufuegen
  - Facade: Vereinfachte Schnittstelle
  - Composite: Baumstrukturen behandeln
  - Proxy: Stellvertreter

VERHALTENSMUSTER
----------------
  - Observer: Publish/Subscribe
  - Strategy: Algorithmen austauschbar
  - Command: Aktionen als Objekte
  - State: Zustandsabhaengiges Verhalten
  - Template Method: Algorithmus-Skelett

================================================================================
KRITIK UND MODERNE ALTERNATIVEN
================================================================================

KRITIK AN OOP
-------------
  - "Banana Gorilla Problem" (Joe Armstrong)
  - Vererbungshierarchien werden komplex
  - Shared Mutable State problematisch
  - Overhead fuer kleine Programme
  - Nicht ideal fuer Concurrency

MODERNE ANSAETZE
----------------
  Composition over Inheritance:
    - Flexiblere Kombination von Verhalten
    - Go, Rust verwenden diesen Ansatz

  Entity Component System (ECS):
    - Besonders in Spieleentwicklung
    - Daten und Logik getrennt

  Protokollorientierte Programmierung:
    - Swift
    - Erweiterbare Protokolle

  Funktionale Elemente in OOP:
    - Lambdas, Streams (Java 8+)
    - LINQ (C#)
    - Immutable Objects

================================================================================
BEDEUTUNG UND EINFLUSS
================================================================================

  - Dominantes Paradigma seit den 1990ern
  - Basis fuer Enterprise-Softwareentwicklung
  - Grundlage vieler Frameworks und Bibliotheken
  - UML (Unified Modeling Language) basiert auf OOP
  - Agile Methoden entstanden im OOP-Kontext
  - Design Patterns als Wissenskanon

================================================================================
SIEHE AUCH
================================================================================

  wiki/java/oop/
  wiki/python/oop/
  wiki/designpatterns/
  wiki/uml/
  wiki/java/generics/
  wiki/cpp/templates/
  wiki/programmiersprachen_geschichte/paradigmen/

================================================================================
WEITERFUEHRENDE RESSOURCEN
================================================================================

  Buecher:
    - "Design Patterns" (Gang of Four, 1994)
    - "Object-Oriented Software Construction" (Bertrand Meyer)
    - "The C++ Programming Language" (Bjarne Stroustrup)
    - "Effective Java" (Joshua Bloch)
    - "Smalltalk-80: The Language" (Adele Goldberg)

  Online:
    - refactoring.guru/design-patterns
    - oracle.com/java/technologies
    - isocpp.org (C++ Standard)

================================================================================
