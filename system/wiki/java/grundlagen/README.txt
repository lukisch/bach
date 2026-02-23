================================================================================
JAVA GRUNDLAGEN - VOLLSTAENDIGE REFERENZ
================================================================================

Portabilitaet: UNIVERSAL
Zuletzt validiert: 2026-02-05
Naechste Pruefung: 2027-02-05
Quellen: Oracle Java Documentation, OpenJDK, JLS (Java Language Specification)

Stand: 2026-02-05
Status: VOLLSTAENDIG

================================================================================
INHALTSVERZEICHNIS
================================================================================
  1. Einfuehrung in Java
  2. JDK, JRE und JVM
  3. Installation und Einrichtung
  4. Erstes Programm (Hello World)
  5. Datentypen
  6. Variablen und Konstanten
  7. Operatoren
  8. Kontrollstrukturen
  9. Arrays
  10. Methoden
  11. BACH-Integration
  12. Haeufige Fehler
  13. Best Practices

================================================================================
1. EINFUEHRUNG IN JAVA
================================================================================

Java ist eine objektorientierte, plattformunabhaengige Programmiersprache,
die 1995 von Sun Microsystems (jetzt Oracle) entwickelt wurde.

HAUPTMERKMALE
-------------
  - Write Once, Run Anywhere (WORA)
  - Objektorientiert
  - Stark typisiert
  - Automatische Speicherverwaltung (Garbage Collection)
  - Multithreading-Unterstuetzung
  - Umfangreiche Standardbibliothek

EINSATZGEBIETE
--------------
  - Enterprise-Anwendungen (Java EE/Jakarta EE)
  - Android-Entwicklung
  - Web-Anwendungen
  - Desktop-Anwendungen (JavaFX, Swing)
  - Microservices (Spring Boot)
  - Big Data (Hadoop, Spark)

JAVA-VERSIONEN (WICHTIGE MEILENSTEINE)
--------------------------------------
  Java 8  (2014)  - Lambda-Ausdruecke, Streams, Optional
  Java 11 (2018)  - LTS, var in Lambdas, HTTP Client
  Java 17 (2021)  - LTS, Sealed Classes, Pattern Matching
  Java 21 (2023)  - LTS, Virtual Threads, Record Patterns
  Java 23 (2024)  - Structured Concurrency, Scoped Values

================================================================================
2. JDK, JRE UND JVM
================================================================================

JVM (JAVA VIRTUAL MACHINE)
--------------------------
Die JVM ist der Kern der Java-Plattform. Sie fuehrt den kompilierten
Bytecode aus und abstrahiert die zugrundeliegende Hardware.

  Aufgaben der JVM:
    - Laden von Klassen (Class Loader)
    - Bytecode-Verifikation
    - Bytecode-Ausfuehrung (Interpreter/JIT-Compiler)
    - Speicherverwaltung und Garbage Collection
    - Sicherheitsmanagement

  Speicherbereiche der JVM:
    +------------------+
    |   Method Area    |  <- Klassendefinitionen, statische Variablen
    +------------------+
    |      Heap        |  <- Objekte und Arrays
    +------------------+
    |     Stack        |  <- Methodenaufrufe, lokale Variablen
    +------------------+
    |   PC Register    |  <- Aktueller Befehlszeiger
    +------------------+
    | Native Method    |  <- Nativer Code (C/C++)
    +------------------+

JRE (JAVA RUNTIME ENVIRONMENT)
------------------------------
Das JRE enthaelt alles, was zur Ausfuehrung von Java-Programmen noetig ist:
  - JVM
  - Java-Klassenbibliotheken (rt.jar, etc.)
  - Konfigurationsdateien

  HINWEIS: Seit Java 11 gibt es kein separates JRE-Download mehr.
           Stattdessen wird jlink fuer modulare Runtime-Images verwendet.

JDK (JAVA DEVELOPMENT KIT)
--------------------------
Das JDK enthaelt das JRE plus Entwicklungswerkzeuge:

  Wichtige Werkzeuge:
    javac      - Java-Compiler
    java       - Java-Launcher
    jar        - Archiv-Tool
    javadoc    - Dokumentationsgenerator
    jdb        - Debugger
    jshell     - Interaktive Shell (REPL, ab Java 9)
    jlink      - Runtime-Image-Ersteller
    jpackage   - Installer-Ersteller (ab Java 14)

================================================================================
3. INSTALLATION UND EINRICHTUNG
================================================================================

DOWNLOAD-QUELLEN
----------------
  - Oracle JDK:      https://www.oracle.com/java/technologies/downloads/
  - OpenJDK:         https://openjdk.org/
  - Adoptium:        https://adoptium.net/ (empfohlen fuer Open Source)
  - Amazon Corretto: https://aws.amazon.com/corretto/

UMGEBUNGSVARIABLEN (Windows)
----------------------------
  JAVA_HOME=C:\Program Files\Java\jdk-21
  PATH=%JAVA_HOME%\bin;%PATH%

UMGEBUNGSVARIABLEN (Linux/macOS)
--------------------------------
  export JAVA_HOME=/usr/lib/jvm/java-21-openjdk
  export PATH=$JAVA_HOME/bin:$PATH

INSTALLATION UEBERPRUEFEN
-------------------------
  java -version
  javac -version

  Erwartete Ausgabe (Beispiel):
    openjdk version "21.0.2" 2024-01-16
    OpenJDK Runtime Environment (build 21.0.2+13)
    OpenJDK 64-Bit Server VM (build 21.0.2+13, mixed mode, sharing)

================================================================================
4. ERSTES PROGRAMM (HELLO WORLD)
================================================================================

KLASSISCHE VARIANTE
-------------------
  // Datei: HelloWorld.java
  public class HelloWorld {
      public static void main(String[] args) {
          System.out.println("Hello World!");
      }
  }

  Kompilieren: javac HelloWorld.java
  Ausfuehren: java HelloWorld

  WICHTIG: Der Dateiname MUSS mit dem Klassennamen uebereinstimmen!

VEREINFACHTE VARIANTE (ab Java 21)
----------------------------------
  // Datei: Hello.java
  void main() {
      System.out.println("Hello World!");
  }

  Ausfuehren: java Hello.java

INTERAKTIV MIT JSHELL (ab Java 9)
---------------------------------
  > jshell
  jshell> System.out.println("Hello World!")
  Hello World!
  jshell> /exit

PROGRAMMSTRUKTUR ERKLAERT
-------------------------
  public class HelloWorld {          // Klassendefinition
      public static void main(       // Eintrittspunkt
          String[] args              // Kommandozeilenargumente
      ) {
          System.out.println(        // Ausgabe auf Konsole
              "Hello World!"         // String-Literal
          );
      }
  }

================================================================================
5. DATENTYPEN
================================================================================

PRIMITIVE DATENTYPEN
--------------------
  Typ       Groesse   Wertebereich                      Default
  -------   -------   ------------------------------    -------
  byte      8 bit     -128 bis 127                      0
  short     16 bit    -32.768 bis 32.767                0
  int       32 bit    -2.147.483.648 bis 2.147.483.647  0
  long      64 bit    -9.223.372.036.854.775.808 bis    0L
                       9.223.372.036.854.775.807
  float     32 bit    ca. +-3.4 * 10^38                 0.0f
  double    64 bit    ca. +-1.8 * 10^308                0.0d
  char      16 bit    0 bis 65.535 (Unicode)            '\u0000'
  boolean   1 bit     true oder false                   false

LITERALE
--------
  int dezimal = 42;
  int hex = 0x2A;
  int binaer = 0b101010;
  int oktal = 052;
  long gross = 1_000_000_000L;    // Underscores fuer Lesbarkeit

  float f = 3.14f;
  double d = 3.14159265359;
  double wissenschaft = 1.5e10;   // 1.5 * 10^10

  char zeichen = 'A';
  char unicode = '\u0041';        // auch 'A'

  boolean wahr = true;
  boolean falsch = false;

REFERENZTYPEN
-------------
  String text = "Hello";          // String (Sonderfall)
  int[] zahlen = {1, 2, 3};       // Array
  Object obj = new Object();      // Objekt
  Integer num = 42;               // Wrapper-Klasse (Autoboxing)

WRAPPER-KLASSEN
---------------
  Primitiv   Wrapper      Beispiel
  --------   ---------    ------------------------
  byte       Byte         Byte b = Byte.valueOf((byte)1);
  short      Short        Short s = Short.valueOf((short)1);
  int        Integer      Integer i = Integer.valueOf(1);
  long       Long         Long l = Long.valueOf(1L);
  float      Float        Float f = Float.valueOf(1.0f);
  double     Double       Double d = Double.valueOf(1.0);
  char       Character    Character c = Character.valueOf('A');
  boolean    Boolean      Boolean bool = Boolean.valueOf(true);

TYPE INFERENCE MIT VAR (ab Java 10)
-----------------------------------
  var name = "Max";               // String
  var zahl = 42;                  // int
  var liste = new ArrayList<String>();

  EINSCHRAENKUNGEN:
    - Nur fuer lokale Variablen
    - Initialisierung erforderlich
    - Nicht fuer null-Zuweisung

================================================================================
6. VARIABLEN UND KONSTANTEN
================================================================================

VARIABLENDEKLARATION
--------------------
  int alter;                      // Deklaration
  alter = 25;                     // Initialisierung
  int gewicht = 70;               // Deklaration + Initialisierung

  // Mehrere Variablen
  int x, y, z;
  int a = 1, b = 2, c = 3;

KONSTANTEN
----------
  final double PI = 3.14159265359;
  final int MAX_SIZE = 100;

  // Konstanten sollten GROSS_MIT_UNTERSTRICHEN benannt werden

NAMENSKONVENTIONEN
------------------
  - Variablen:  camelCase (alter, maxWert, istGueltig)
  - Konstanten: UPPER_SNAKE_CASE (MAX_VALUE, PI)
  - Klassen:    PascalCase (HelloWorld, StringBuffer)
  - Methoden:   camelCase (getName, setAge)
  - Packages:   lowercase (com.example.app)

GUELTIGKEITSBEREICHE (SCOPE)
----------------------------
  public class ScopeExample {
      static int klassenVariable = 1;    // Klassenvariable
      int instanzVariable = 2;           // Instanzvariable

      void methode() {
          int lokaleVariable = 3;        // Lokale Variable

          for (int i = 0; i < 10; i++) { // Block-Variable
              int blockVariable = 4;
          }
          // i und blockVariable hier nicht mehr sichtbar
      }
  }

================================================================================
7. OPERATOREN
================================================================================

ARITHMETISCHE OPERATOREN
------------------------
  +    Addition          5 + 3 = 8
  -    Subtraktion       5 - 3 = 2
  *    Multiplikation    5 * 3 = 15
  /    Division          5 / 3 = 1 (Ganzzahl!)
  %    Modulo            5 % 3 = 2

  ++   Inkrement         i++ oder ++i
  --   Dekrement         i-- oder --i

  WICHTIG: Bei int/int ist das Ergebnis int (abgerundet)
           5 / 3 = 1, aber 5.0 / 3 = 1.666...

ZUWEISUNGSOPERATOREN
--------------------
  =    Zuweisung         x = 5
  +=   Addition          x += 3  (x = x + 3)
  -=   Subtraktion       x -= 3
  *=   Multiplikation    x *= 3
  /=   Division          x /= 3
  %=   Modulo            x %= 3

VERGLEICHSOPERATOREN
--------------------
  ==   Gleich            5 == 5 -> true
  !=   Ungleich          5 != 3 -> true
  <    Kleiner           3 < 5 -> true
  >    Groesser          5 > 3 -> true
  <=   Kleiner/gleich    5 <= 5 -> true
  >=   Groesser/gleich   5 >= 3 -> true

  ACHTUNG: Bei Objekten vergleicht == die Referenz, nicht den Inhalt!
           Verwende .equals() fuer inhaltlichen Vergleich.

LOGISCHE OPERATOREN
-------------------
  &&   Logisches UND     true && false -> false
  ||   Logisches ODER    true || false -> true
  !    Logisches NICHT   !true -> false

  Short-Circuit Evaluation:
    Bei && wird rechts nicht ausgewertet, wenn links false
    Bei || wird rechts nicht ausgewertet, wenn links true

BITWEISE OPERATOREN
-------------------
  &    UND               5 & 3 = 1
  |    ODER              5 | 3 = 7
  ^    XOR               5 ^ 3 = 6
  ~    NOT               ~5 = -6
  <<   Links-Shift       5 << 1 = 10
  >>   Rechts-Shift      5 >> 1 = 2
  >>>  Unsigned Shift    -5 >>> 1 = 2147483645

TERNAERER OPERATOR
------------------
  int max = (a > b) ? a : b;

  // Entspricht:
  int max;
  if (a > b) {
      max = a;
  } else {
      max = b;
  }

INSTANCEOF OPERATOR
-------------------
  if (obj instanceof String) {
      String s = (String) obj;
  }

  // Pattern Matching (ab Java 16):
  if (obj instanceof String s) {
      System.out.println(s.length());
  }

================================================================================
8. KONTROLLSTRUKTUREN
================================================================================

IF-ELSE
-------
  if (bedingung) {
      // Code wenn wahr
  } else if (andereBedingung) {
      // Code wenn andere Bedingung wahr
  } else {
      // Code wenn alle Bedingungen falsch
  }

  // Beispiel
  int note = 2;
  if (note == 1) {
      System.out.println("Sehr gut");
  } else if (note == 2) {
      System.out.println("Gut");
  } else if (note <= 4) {
      System.out.println("Bestanden");
  } else {
      System.out.println("Nicht bestanden");
  }

SWITCH (klassisch)
------------------
  switch (tag) {
      case 1:
          System.out.println("Montag");
          break;
      case 2:
          System.out.println("Dienstag");
          break;
      default:
          System.out.println("Anderer Tag");
  }

SWITCH EXPRESSION (ab Java 14)
------------------------------
  String tagName = switch (tag) {
      case 1 -> "Montag";
      case 2 -> "Dienstag";
      case 3 -> "Mittwoch";
      case 4 -> "Donnerstag";
      case 5 -> "Freitag";
      case 6, 7 -> "Wochenende";
      default -> "Unbekannt";
  };

FOR-SCHLEIFE
------------
  for (int i = 0; i < 10; i++) {
      System.out.println(i);
  }

  // Enhanced For-Loop (For-Each)
  int[] zahlen = {1, 2, 3, 4, 5};
  for (int zahl : zahlen) {
      System.out.println(zahl);
  }

WHILE-SCHLEIFE
--------------
  int i = 0;
  while (i < 10) {
      System.out.println(i);
      i++;
  }

DO-WHILE-SCHLEIFE
-----------------
  int i = 0;
  do {
      System.out.println(i);
      i++;
  } while (i < 10);

  // Wird mindestens einmal ausgefuehrt!

BREAK UND CONTINUE
------------------
  for (int i = 0; i < 10; i++) {
      if (i == 5) break;        // Beendet Schleife
      if (i % 2 == 0) continue; // Springt zur naechsten Iteration
      System.out.println(i);    // Gibt 1, 3 aus
  }

  // Labeled Break (fuer verschachtelte Schleifen)
  outer:
  for (int i = 0; i < 3; i++) {
      for (int j = 0; j < 3; j++) {
          if (i == 1 && j == 1) break outer;
          System.out.println(i + "," + j);
      }
  }

================================================================================
9. ARRAYS
================================================================================

DEKLARATION UND INITIALISIERUNG
-------------------------------
  int[] zahlen = new int[5];              // Array mit 5 Elementen
  int[] werte = {1, 2, 3, 4, 5};          // Direkte Initialisierung
  int[] kopie = new int[]{1, 2, 3};       // Alternative Syntax

  // Mehrdimensionale Arrays
  int[][] matrix = new int[3][3];
  int[][] tabelle = {
      {1, 2, 3},
      {4, 5, 6},
      {7, 8, 9}
  };

ZUGRIFF
-------
  zahlen[0] = 10;                         // Erstes Element setzen
  int wert = zahlen[0];                   // Erstes Element lesen
  int laenge = zahlen.length;             // Array-Laenge

  // Iteration
  for (int i = 0; i < zahlen.length; i++) {
      System.out.println(zahlen[i]);
  }

  // For-Each
  for (int zahl : zahlen) {
      System.out.println(zahl);
  }

ARRAYS UTILITY-KLASSE
---------------------
  import java.util.Arrays;

  int[] arr = {3, 1, 4, 1, 5, 9};

  Arrays.sort(arr);                       // Sortieren
  Arrays.fill(arr, 0);                    // Alle Elemente auf 0
  int index = Arrays.binarySearch(arr, 5);// Binaere Suche
  int[] kopie = Arrays.copyOf(arr, 10);   // Kopieren
  boolean gleich = Arrays.equals(arr, kopie);
  String text = Arrays.toString(arr);     // "[0, 0, 0, ...]"

================================================================================
10. METHODEN
================================================================================

METHODENDEFINITION
------------------
  public static int addiere(int a, int b) {
      return a + b;
  }

  Bestandteile:
    public    - Zugriffsmodifikator
    static    - Gehoert zur Klasse, nicht zum Objekt
    int       - Rueckgabetyp
    addiere   - Methodenname
    (int a, int b) - Parameter
    return    - Rueckgabewert

VOID-METHODEN
-------------
  public static void gruss(String name) {
      System.out.println("Hallo, " + name + "!");
      // Kein return noetig (oder: return;)
  }

METHODENUEBERLADUNG (OVERLOADING)
---------------------------------
  public static int addiere(int a, int b) {
      return a + b;
  }

  public static double addiere(double a, double b) {
      return a + b;
  }

  public static int addiere(int a, int b, int c) {
      return a + b + c;
  }

VARARGS (VARIABLE ARGUMENTE)
----------------------------
  public static int summe(int... zahlen) {
      int sum = 0;
      for (int z : zahlen) {
          sum += z;
      }
      return sum;
  }

  // Aufruf
  summe(1, 2, 3);
  summe(1, 2, 3, 4, 5);

REKURSION
---------
  public static int fakultaet(int n) {
      if (n <= 1) return 1;
      return n * fakultaet(n - 1);
  }

  public static int fibonacci(int n) {
      if (n <= 1) return n;
      return fibonacci(n - 1) + fibonacci(n - 2);
  }

================================================================================
11. BACH-INTEGRATION
================================================================================

Java-Programme koennen in BACH auf verschiedene Arten integriert werden:

KOMPILIERUNG UND AUSFUEHRUNG
----------------------------
  BACH> javac MeinProgramm.java
  BACH> java MeinProgramm

BACH-SKRIPT FUER JAVA-PROJEKT
-----------------------------
  @echo off
  :: build.cmd - BACH-Skript fuer Java-Projekt

  set SRC_DIR=src
  set OUT_DIR=bin
  set MAIN_CLASS=com.example.Main

  :: Kompilieren
  javac -d %OUT_DIR% %SRC_DIR%\*.java

  :: Ausfuehren
  java -cp %OUT_DIR% %MAIN_CLASS%

JAR-DATEIEN ERSTELLEN
---------------------
  :: Manifest erstellen
  echo Main-Class: com.example.Main > manifest.txt

  :: JAR packen
  jar cfm app.jar manifest.txt -C bin .

  :: JAR ausfuehren
  java -jar app.jar

UMGEBUNG IN BACH PRUEFEN
------------------------
  BACH> java -version
  BACH> echo %JAVA_HOME%
  BACH> where java

================================================================================
12. HAEUFIGE FEHLER
================================================================================

KOMPILIERFEHLER
---------------
  "cannot find symbol"
    -> Tippfehler im Variablen-/Methodennamen
    -> Import fehlt
    -> Variable nicht deklariert

  "incompatible types"
    -> Falscher Datentyp bei Zuweisung
    -> Cast erforderlich

  "missing return statement"
    -> Nicht alle Codepfade haben return

LAUFZEITFEHLER
--------------
  NullPointerException
    -> Zugriff auf null-Referenz
    -> Loesung: null-Pruefung oder Optional verwenden

  ArrayIndexOutOfBoundsException
    -> Array-Index ausserhalb der Grenzen
    -> Loesung: Index pruefen (0 bis length-1)

  ArithmeticException
    -> Division durch 0 (bei Ganzzahlen)
    -> Loesung: Divisor pruefen

  ClassCastException
    -> Ungueltiger Cast
    -> Loesung: instanceof pruefen

================================================================================
13. BEST PRACTICES
================================================================================

  1. Aussagekraeftige Namen verwenden
     SCHLECHT: int x = 5;
     GUT:      int alterInJahren = 5;

  2. Konstanten statt Magic Numbers
     SCHLECHT: if (status == 3) { ... }
     GUT:      if (status == STATUS_COMPLETED) { ... }

  3. Immer Klammern bei if/for/while
     SCHLECHT: if (x > 0) doSomething();
     GUT:      if (x > 0) { doSomething(); }

  4. Ressourcen mit try-with-resources schliessen
     try (FileReader reader = new FileReader("file.txt")) {
         // ...
     }

  5. equals() statt == fuer Objekte
     SCHLECHT: if (str == "test") { ... }
     GUT:      if ("test".equals(str)) { ... }

  6. StringBuilder fuer String-Verkettung in Schleifen
     StringBuilder sb = new StringBuilder();
     for (String s : strings) {
         sb.append(s);
     }

================================================================================
SIEHE AUCH
================================================================================
  wiki/java/oop/                      - Objektorientierte Programmierung
  wiki/java/collections/              - Collections Framework
  wiki/java/exceptions/               - Exception Handling
  wiki/java/streams/                  - Stream API
  wiki/programmiersprachen_geschichte/ - Geschichte der Programmiersprachen
  wiki/entwicklungsumgebungen/        - IDEs und Editoren

================================================================================
ENDE DES ARTIKELS
================================================================================
