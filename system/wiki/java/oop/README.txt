================================================================================
JAVA OOP - OBJEKTORIENTIERTE PROGRAMMIERUNG
================================================================================

Portabilitaet: UNIVERSAL
Zuletzt validiert: 2026-02-05
Naechste Pruefung: 2027-02-05
Quellen: Oracle Java Documentation, "Effective Java" (J. Bloch), JLS

Stand: 2026-02-05
Status: VOLLSTAENDIG

================================================================================
INHALTSVERZEICHNIS
================================================================================
  1. Grundprinzipien der OOP
  2. Klassen und Objekte
  3. Konstruktoren
  4. Encapsulation (Kapselung)
  5. Vererbung (Inheritance)
  6. Polymorphismus
  7. Abstrakte Klassen
  8. Interfaces
  9. Records (ab Java 14)
  10. Sealed Classes (ab Java 17)
  11. Innere Klassen
  12. Packages und Imports
  13. BACH-Integration
  14. Design Patterns
  15. Best Practices

================================================================================
1. GRUNDPRINZIPIEN DER OOP
================================================================================

Die objektorientierte Programmierung basiert auf vier Saeulen:

ABSTRAKTION
-----------
  Komplexitaet verbergen, nur relevante Details zeigen.

  Beispiel: Ein Auto-Objekt zeigt "fahren()", aber nicht die
  interne Motorsteuerung.

KAPSELUNG (ENCAPSULATION)
-------------------------
  Daten und Methoden buendeln, Zugriff kontrollieren.

  Beispiel: private Attribute mit public Getter/Setter.

VERERBUNG (INHERITANCE)
-----------------------
  Eigenschaften und Verhalten von Elternklassen uebernehmen.

  Beispiel: Student extends Person

POLYMORPHISMUS
--------------
  Gleiche Schnittstelle, unterschiedliches Verhalten.

  Beispiel: Verschiedene Tiere implementieren "machGeraeusch()"
  unterschiedlich.

================================================================================
2. KLASSEN UND OBJEKTE
================================================================================

KLASSENSTRUKTUR
---------------
  public class Person {
      // Attribute (Instanzvariablen)
      private String name;
      private int alter;

      // Statische Variable (Klassenvariable)
      private static int anzahlPersonen = 0;

      // Konstante
      public static final int MAX_ALTER = 150;

      // Konstruktor
      public Person(String name, int alter) {
          this.name = name;
          this.alter = alter;
          anzahlPersonen++;
      }

      // Instanzmethode
      public void vorstellen() {
          System.out.println("Ich bin " + name + ", " + alter + " Jahre alt.");
      }

      // Statische Methode
      public static int getAnzahlPersonen() {
          return anzahlPersonen;
      }

      // Getter
      public String getName() {
          return name;
      }

      // Setter mit Validierung
      public void setAlter(int alter) {
          if (alter >= 0 && alter <= MAX_ALTER) {
              this.alter = alter;
          } else {
              throw new IllegalArgumentException("Ungueltiges Alter: " + alter);
          }
      }
  }

OBJEKTE ERSTELLEN UND VERWENDEN
-------------------------------
  // Objekt erstellen
  Person max = new Person("Max Mustermann", 30);
  Person anna = new Person("Anna Schmidt", 25);

  // Methoden aufrufen
  max.vorstellen();                    // Instanzmethode
  System.out.println(Person.getAnzahlPersonen()); // Statische Methode

  // Attribute lesen/schreiben
  String name = max.getName();
  max.setAlter(31);

THIS-REFERENZ
-------------
  public class Beispiel {
      private int wert;

      public void setWert(int wert) {
          this.wert = wert;      // this unterscheidet Attribut von Parameter
      }

      public Beispiel getThis() {
          return this;           // Gibt aktuelle Instanz zurueck
      }

      public void methodenKette() {
          this.setWert(10);      // Expliziter Aufruf auf sich selbst
      }
  }

================================================================================
3. KONSTRUKTOREN
================================================================================

ARTEN VON KONSTRUKTOREN
-----------------------
  public class Auto {
      private String marke;
      private String modell;
      private int baujahr;

      // Standard-Konstruktor (Default)
      public Auto() {
          this.marke = "Unbekannt";
          this.modell = "Unbekannt";
          this.baujahr = 2000;
      }

      // Parametrisierter Konstruktor
      public Auto(String marke, String modell, int baujahr) {
          this.marke = marke;
          this.modell = modell;
          this.baujahr = baujahr;
      }

      // Konstruktor mit weniger Parametern (Ueberladung)
      public Auto(String marke, String modell) {
          this(marke, modell, 2024);  // Ruft anderen Konstruktor auf
      }

      // Copy-Konstruktor
      public Auto(Auto anderes) {
          this.marke = anderes.marke;
          this.modell = anderes.modell;
          this.baujahr = anderes.baujahr;
      }
  }

KONSTRUKTOR-VERKETTUNG
----------------------
  public class Fahrzeug {
      protected String typ;

      public Fahrzeug(String typ) {
          this.typ = typ;
      }
  }

  public class PKW extends Fahrzeug {
      private int sitze;

      public PKW(String typ, int sitze) {
          super(typ);           // MUSS erste Anweisung sein!
          this.sitze = sitze;
      }
  }

INITIALISIERUNGSBLOECKE
-----------------------
  public class InitBeispiel {
      private static int zaehler;
      private int id;

      // Statischer Initialisierungsblock (einmal beim Laden der Klasse)
      static {
          System.out.println("Klasse wird geladen");
          zaehler = 0;
      }

      // Instanz-Initialisierungsblock (bei jeder Objekterstellung)
      {
          id = ++zaehler;
          System.out.println("Objekt " + id + " wird erstellt");
      }

      public InitBeispiel() {
          System.out.println("Konstruktor aufgerufen");
      }
  }

  // Reihenfolge: static Block -> Instance Block -> Konstruktor

================================================================================
4. ENCAPSULATION (KAPSELUNG)
================================================================================

ZUGRIFFSMODIFIKATOREN
---------------------
  Modifikator   Klasse   Package   Subklasse   Welt
  -----------   ------   -------   ---------   ----
  public        Ja       Ja        Ja          Ja
  protected     Ja       Ja        Ja          Nein
  (default)     Ja       Ja        Nein        Nein
  private       Ja       Nein      Nein        Nein

GETTER UND SETTER
-----------------
  public class Konto {
      private double kontostand;
      private String inhaber;

      // Einfacher Getter
      public double getKontostand() {
          return kontostand;
      }

      // Getter mit Berechnung
      public double getKontostandMitZinsen() {
          return kontostand * 1.02;
      }

      // Setter mit Validierung
      public void setKontostand(double betrag) {
          if (betrag < -1000) {
              throw new IllegalArgumentException("Dispo-Limit ueberschritten!");
          }
          this.kontostand = betrag;
      }

      // Immutable Getter (defensives Kopieren)
      public String getInhaber() {
          return inhaber;  // String ist bereits immutable
      }
  }

IMMUTABLE KLASSEN
-----------------
  public final class Punkt {          // final verhindert Vererbung
      private final int x;            // final verhindert Aenderung
      private final int y;

      public Punkt(int x, int y) {
          this.x = x;
          this.y = y;
      }

      public int getX() { return x; }
      public int getY() { return y; }

      // Statt Setter: neue Instanz zurueckgeben
      public Punkt mitX(int neuesX) {
          return new Punkt(neuesX, this.y);
      }

      public Punkt mitY(int neuesY) {
          return new Punkt(this.x, neuesY);
      }
  }

================================================================================
5. VERERBUNG (INHERITANCE)
================================================================================

GRUNDLAGEN
----------
  // Basisklasse (Superklasse)
  public class Tier {
      protected String name;
      protected int alter;

      public Tier(String name, int alter) {
          this.name = name;
          this.alter = alter;
      }

      public void essen() {
          System.out.println(name + " isst.");
      }

      public void schlafen() {
          System.out.println(name + " schlaeft.");
      }
  }

  // Abgeleitete Klasse (Subklasse)
  public class Hund extends Tier {
      private String rasse;

      public Hund(String name, int alter, String rasse) {
          super(name, alter);   // Konstruktor der Basisklasse
          this.rasse = rasse;
      }

      // Neue Methode
      public void bellen() {
          System.out.println(name + " bellt: Wau!");
      }

      // Methode ueberschreiben
      @Override
      public void essen() {
          System.out.println(name + " frisst Hundefutter.");
      }
  }

VERWENDUNG
----------
  Hund bello = new Hund("Bello", 5, "Labrador");
  bello.essen();       // "Bello frisst Hundefutter." (ueberschrieben)
  bello.schlafen();    // "Bello schlaeft." (geerbt)
  bello.bellen();      // "Bello bellt: Wau!" (neu)

SUPER-SCHLUESSELWORT
--------------------
  public class Katze extends Tier {
      public Katze(String name, int alter) {
          super(name, alter);
      }

      @Override
      public void essen() {
          super.essen();        // Ruft Tier.essen() auf
          System.out.println("...und schnurrt dabei.");
      }
  }

FINAL BEI VERERBUNG
-------------------
  // Klasse kann nicht vererbt werden
  public final class String { ... }

  // Methode kann nicht ueberschrieben werden
  public final void wichtigeMethode() { ... }

  // Variable kann nicht geaendert werden
  private final int konstante = 42;

================================================================================
6. POLYMORPHISMUS
================================================================================

METHODENUEBERSCHREIBUNG (OVERRIDING)
------------------------------------
  public class Form {
      public double berechneFlaeche() {
          return 0;
      }
  }

  public class Kreis extends Form {
      private double radius;

      public Kreis(double radius) {
          this.radius = radius;
      }

      @Override
      public double berechneFlaeche() {
          return Math.PI * radius * radius;
      }
  }

  public class Rechteck extends Form {
      private double breite, hoehe;

      public Rechteck(double breite, double hoehe) {
          this.breite = breite;
          this.hoehe = hoehe;
      }

      @Override
      public double berechneFlaeche() {
          return breite * hoehe;
      }
  }

DYNAMISCHE BINDUNG
------------------
  Form[] formen = {
      new Kreis(5),
      new Rechteck(4, 6),
      new Kreis(3)
  };

  for (Form f : formen) {
      // Zur Laufzeit wird die richtige Methode aufgerufen
      System.out.println("Flaeche: " + f.berechneFlaeche());
  }

METHODENUEBERLADUNG (OVERLOADING)
---------------------------------
  public class Rechner {
      public int addiere(int a, int b) {
          return a + b;
      }

      public double addiere(double a, double b) {
          return a + b;
      }

      public int addiere(int a, int b, int c) {
          return a + b + c;
      }

      public String addiere(String a, String b) {
          return a + b;
      }
  }

KOVARIANTE RUECKGABETYPEN
-------------------------
  public class Tier {
      public Tier kopieren() {
          return new Tier();
      }
  }

  public class Hund extends Tier {
      @Override
      public Hund kopieren() {    // Spezifischerer Rueckgabetyp erlaubt
          return new Hund();
      }
  }

================================================================================
7. ABSTRAKTE KLASSEN
================================================================================

DEFINITION
----------
  public abstract class Fahrzeug {
      protected String marke;

      // Konstruktor (kann nicht direkt aufgerufen werden)
      public Fahrzeug(String marke) {
          this.marke = marke;
      }

      // Konkrete Methode
      public void starten() {
          System.out.println(marke + " startet.");
      }

      // Abstrakte Methode (muss implementiert werden)
      public abstract void fahren();

      // Abstrakte Methode mit Rueckgabewert
      public abstract double getMaxGeschwindigkeit();
  }

IMPLEMENTIERUNG
---------------
  public class Auto extends Fahrzeug {
      private int ps;

      public Auto(String marke, int ps) {
          super(marke);
          this.ps = ps;
      }

      @Override
      public void fahren() {
          System.out.println(marke + " faehrt auf der Strasse.");
      }

      @Override
      public double getMaxGeschwindigkeit() {
          return ps * 0.8;
      }
  }

  public class Boot extends Fahrzeug {
      public Boot(String marke) {
          super(marke);
      }

      @Override
      public void fahren() {
          System.out.println(marke + " faehrt auf dem Wasser.");
      }

      @Override
      public double getMaxGeschwindigkeit() {
          return 50.0;
      }
  }

VERWENDUNG
----------
  // Fahrzeug f = new Fahrzeug("Test");  // FEHLER! Abstrakt!

  Fahrzeug auto = new Auto("BMW", 200);
  Fahrzeug boot = new Boot("Yamaha");

  auto.starten();  // "BMW startet." (geerbte Methode)
  auto.fahren();   // "BMW faehrt auf der Strasse." (implementiert)

================================================================================
8. INTERFACES
================================================================================

INTERFACE-DEFINITION
--------------------
  public interface Druckbar {
      // Konstante (implizit public static final)
      int MAX_SEITEN = 100;

      // Abstrakte Methode (implizit public abstract)
      void drucken();

      // Default-Methode (ab Java 8)
      default void druckenMitRahmen() {
          System.out.println("========");
          drucken();
          System.out.println("========");
      }

      // Statische Methode (ab Java 8)
      static void info() {
          System.out.println("Druckbar Interface v1.0");
      }

      // Private Methode (ab Java 9)
      private void helferMethode() {
          // Interne Hilfsmethode
      }
  }

INTERFACE IMPLEMENTIEREN
------------------------
  public class Dokument implements Druckbar {
      private String inhalt;

      public Dokument(String inhalt) {
          this.inhalt = inhalt;
      }

      @Override
      public void drucken() {
          System.out.println(inhalt);
      }
  }

  public class Bild implements Druckbar {
      private String dateiname;

      public Bild(String dateiname) {
          this.dateiname = dateiname;
      }

      @Override
      public void drucken() {
          System.out.println("[Bild: " + dateiname + "]");
      }
  }

MEHRFACHE INTERFACES
--------------------
  public interface Speicherbar {
      void speichern(String pfad);
      void laden(String pfad);
  }

  public class TextDokument implements Druckbar, Speicherbar {
      private String text;

      @Override
      public void drucken() {
          System.out.println(text);
      }

      @Override
      public void speichern(String pfad) {
          // Speicherlogik
      }

      @Override
      public void laden(String pfad) {
          // Ladelogik
      }
  }

INTERFACE VERERBUNG
-------------------
  public interface Exportierbar extends Druckbar, Speicherbar {
      void exportieren(String format);
  }

FUNKTIONALE INTERFACES (ab Java 8)
----------------------------------
  @FunctionalInterface
  public interface Berechnung {
      double berechne(double x, double y);
  }

  // Verwendung mit Lambda
  Berechnung addition = (a, b) -> a + b;
  Berechnung multiplikation = (a, b) -> a * b;

  System.out.println(addition.berechne(5, 3));       // 8.0
  System.out.println(multiplikation.berechne(5, 3)); // 15.0

================================================================================
9. RECORDS (ab Java 14)
================================================================================

Records sind kompakte, unveraenderliche Datenklassen.

DEFINITION
----------
  // Klassische Klasse
  public class PersonKlassisch {
      private final String name;
      private final int alter;

      public PersonKlassisch(String name, int alter) {
          this.name = name;
          this.alter = alter;
      }

      public String getName() { return name; }
      public int getAlter() { return alter; }

      @Override
      public boolean equals(Object o) { ... }
      @Override
      public int hashCode() { ... }
      @Override
      public String toString() { ... }
  }

  // Aequivalent als Record (eine Zeile!)
  public record Person(String name, int alter) {}

RECORD-FEATURES
---------------
  public record Punkt(int x, int y) {
      // Kompakter Konstruktor (Validierung)
      public Punkt {
          if (x < 0 || y < 0) {
              throw new IllegalArgumentException("Koordinaten muessen >= 0 sein");
          }
      }

      // Zusaetzliche Methode
      public double distanzZumUrsprung() {
          return Math.sqrt(x * x + y * y);
      }

      // Statische Factory-Methode
      public static Punkt ursprung() {
          return new Punkt(0, 0);
      }
  }

VERWENDUNG
----------
  Person p = new Person("Max", 30);
  System.out.println(p.name());     // "Max" (Accessor, nicht getName!)
  System.out.println(p.alter());    // 30
  System.out.println(p);            // "Person[name=Max, alter=30]"

================================================================================
10. SEALED CLASSES (ab Java 17)
================================================================================

Sealed Classes beschraenken, welche Klassen erben duerfen.

DEFINITION
----------
  public sealed class Form
      permits Kreis, Rechteck, Dreieck {
      // ...
  }

  // Muss final, sealed oder non-sealed sein
  public final class Kreis extends Form {
      private double radius;
      // ...
  }

  public sealed class Rechteck extends Form
      permits Quadrat {
      // ...
  }

  public final class Quadrat extends Rechteck {
      // ...
  }

  public non-sealed class Dreieck extends Form {
      // Kann beliebig erweitert werden
  }

PATTERN MATCHING MIT SEALED CLASSES
-----------------------------------
  public double berechneFlaeche(Form form) {
      return switch (form) {
          case Kreis k -> Math.PI * k.getRadius() * k.getRadius();
          case Rechteck r -> r.getBreite() * r.getHoehe();
          case Dreieck d -> 0.5 * d.getGrundseite() * d.getHoehe();
          // Kein default noetig - Compiler weiss alle Faelle!
      };
  }

================================================================================
11. INNERE KLASSEN
================================================================================

MEMBER INNER CLASS
------------------
  public class Aussen {
      private int x = 10;

      public class Innen {
          public void zeige() {
              System.out.println("x = " + x);  // Zugriff auf aeussere Klasse
          }
      }
  }

  // Verwendung
  Aussen aussen = new Aussen();
  Aussen.Innen innen = aussen.new Innen();
  innen.zeige();

STATIC NESTED CLASS
-------------------
  public class Aussen {
      private static int y = 20;

      public static class Nested {
          public void zeige() {
              System.out.println("y = " + y);  // Nur statische Member
          }
      }
  }

  // Verwendung
  Aussen.Nested nested = new Aussen.Nested();

LOCAL INNER CLASS
-----------------
  public void methode() {
      final int z = 30;

      class Lokal {
          public void zeige() {
              System.out.println("z = " + z);
          }
      }

      new Lokal().zeige();
  }

ANONYMOUS INNER CLASS
---------------------
  Druckbar anonym = new Druckbar() {
      @Override
      public void drucken() {
          System.out.println("Anonyme Implementierung");
      }
  };

  // Moderne Alternative: Lambda (wenn funktionales Interface)
  Runnable r = () -> System.out.println("Lambda statt anonymer Klasse");

================================================================================
12. PACKAGES UND IMPORTS
================================================================================

PACKAGE-DEKLARATION
-------------------
  // Muss erste Anweisung sein (vor imports)
  package com.beispiel.meineapp;

  public class MeineKlasse {
      // ...
  }

IMPORT-ANWEISUNGEN
------------------
  // Einzelne Klasse importieren
  import java.util.ArrayList;
  import java.util.HashMap;

  // Alle Klassen eines Packages (nicht empfohlen)
  import java.util.*;

  // Statischer Import
  import static java.lang.Math.PI;
  import static java.lang.Math.sqrt;

  // Verwendung
  double umfang = 2 * PI * radius;  // statt Math.PI

PACKAGE-STRUKTUR (Konvention)
-----------------------------
  com.firma.projekt/
    ├── model/
    │   ├── User.java
    │   └── Product.java
    ├── service/
    │   ├── UserService.java
    │   └── ProductService.java
    ├── repository/
    │   └── UserRepository.java
    └── util/
        └── StringHelper.java

CLASSPATH
---------
  // Kompilieren mit Classpath
  javac -cp lib/* -d bin src/com/beispiel/*.java

  // Ausfuehren mit Classpath
  java -cp bin:lib/* com.beispiel.Main

================================================================================
13. BACH-INTEGRATION
================================================================================

OOP-PROJEKTE IN BACH VERWALTEN
------------------------------
  :: Projektstruktur erstellen
  mkdir src bin lib

  :: Kompilieren aller Java-Dateien
  javac -d bin src\com\beispiel\*.java

  :: Mit externen Bibliotheken
  javac -cp "lib\*" -d bin src\com\beispiel\*.java

  :: Ausfuehren
  java -cp bin com.beispiel.Main

BACH-SKRIPT FUER OOP-PROJEKT
----------------------------
  @echo off
  :: build_oop.cmd - BACH Build-Skript fuer OOP-Projekt

  set PROJECT_NAME=MeinProjekt
  set SRC_DIR=src
  set BIN_DIR=bin
  set LIB_DIR=lib
  set MAIN_CLASS=com.beispiel.Main

  echo [%PROJECT_NAME%] Kompiliere...

  :: Bin-Verzeichnis erstellen falls noetig
  if not exist %BIN_DIR% mkdir %BIN_DIR%

  :: Alle Java-Dateien finden und kompilieren
  dir /s /b %SRC_DIR%\*.java > sources.txt
  javac -cp "%LIB_DIR%\*" -d %BIN_DIR% @sources.txt
  del sources.txt

  if %ERRORLEVEL% EQU 0 (
      echo [%PROJECT_NAME%] Kompilierung erfolgreich!
      echo [%PROJECT_NAME%] Starte...
      java -cp "%BIN_DIR%;%LIB_DIR%\*" %MAIN_CLASS%
  ) else (
      echo [%PROJECT_NAME%] Kompilierung fehlgeschlagen!
  )

JAR MIT MANIFEST ERSTELLEN
--------------------------
  :: Manifest erstellen
  echo Manifest-Version: 1.0 > MANIFEST.MF
  echo Main-Class: com.beispiel.Main >> MANIFEST.MF
  echo Class-Path: lib/externe.jar >> MANIFEST.MF

  :: JAR packen
  jar cfm %PROJECT_NAME%.jar MANIFEST.MF -C bin .

  :: Ausfuehren
  java -jar %PROJECT_NAME%.jar

================================================================================
14. DESIGN PATTERNS
================================================================================

SINGLETON
---------
  public class Singleton {
      private static Singleton instance;

      private Singleton() {}

      public static synchronized Singleton getInstance() {
          if (instance == null) {
              instance = new Singleton();
          }
          return instance;
      }
  }

FACTORY METHOD
--------------
  public interface Tier {
      void sprich();
  }

  public class TierFactory {
      public static Tier erzeuge(String typ) {
          return switch (typ.toLowerCase()) {
              case "hund" -> new Hund();
              case "katze" -> new Katze();
              default -> throw new IllegalArgumentException("Unbekannter Typ");
          };
      }
  }

BUILDER
-------
  public class Person {
      private String name;
      private int alter;
      private String beruf;

      private Person(Builder builder) {
          this.name = builder.name;
          this.alter = builder.alter;
          this.beruf = builder.beruf;
      }

      public static class Builder {
          private String name;
          private int alter;
          private String beruf;

          public Builder name(String name) {
              this.name = name;
              return this;
          }

          public Builder alter(int alter) {
              this.alter = alter;
              return this;
          }

          public Builder beruf(String beruf) {
              this.beruf = beruf;
              return this;
          }

          public Person build() {
              return new Person(this);
          }
      }
  }

  // Verwendung
  Person p = new Person.Builder()
      .name("Max")
      .alter(30)
      .beruf("Entwickler")
      .build();

OBSERVER
--------
  public interface Observer {
      void update(String nachricht);
  }

  public class Subject {
      private List<Observer> observers = new ArrayList<>();

      public void addObserver(Observer o) {
          observers.add(o);
      }

      public void notifyObservers(String nachricht) {
          for (Observer o : observers) {
              o.update(nachricht);
          }
      }
  }

================================================================================
15. BEST PRACTICES
================================================================================

KLASSEN-DESIGN
--------------
  1. Single Responsibility Principle (SRP)
     - Eine Klasse sollte nur eine Aufgabe haben

  2. Open/Closed Principle (OCP)
     - Offen fuer Erweiterung, geschlossen fuer Modifikation

  3. Liskov Substitution Principle (LSP)
     - Subklassen muessen Basisklassen ersetzen koennen

  4. Interface Segregation Principle (ISP)
     - Viele spezifische Interfaces statt einem grossen

  5. Dependency Inversion Principle (DIP)
     - Abhaengig von Abstraktionen, nicht Implementierungen

VERERBUNG VS KOMPOSITION
------------------------
  // SCHLECHT: Tiefe Vererbungshierarchie
  class A { }
  class B extends A { }
  class C extends B { }
  class D extends C { }

  // BESSER: Komposition (Has-A statt Is-A)
  class Motor { }
  class Auto {
      private Motor motor;  // Auto HAT einen Motor
  }

IMMUTABILITY BEVORZUGEN
-----------------------
  // Immutable Objekte sind threadsicher und einfacher zu verstehen
  public record Adresse(String strasse, String ort, String plz) {}

DEFENSIVE KOPIEN
----------------
  public class Kurs {
      private final List<String> teilnehmer;

      public Kurs(List<String> teilnehmer) {
          // Defensive Kopie im Konstruktor
          this.teilnehmer = new ArrayList<>(teilnehmer);
      }

      public List<String> getTeilnehmer() {
          // Defensive Kopie beim Getter
          return new ArrayList<>(teilnehmer);
          // Oder: return Collections.unmodifiableList(teilnehmer);
      }
  }

================================================================================
SIEHE AUCH
================================================================================
  wiki/java/grundlagen/             - Java Grundlagen
  wiki/java/collections/            - Collections Framework
  wiki/java/generics/               - Generics
  wiki/java/streams/                - Stream API und Lambdas
  wiki/java/exceptions/             - Exception Handling
  wiki/design_patterns/             - Design Patterns ausfuehrlich
  wiki/python/oop/                  - OOP in Python (Vergleich)
  wiki/informatik/programmierung/   - Allgemeine Programmierkonzepte

================================================================================
ENDE DES ARTIKELS
================================================================================
