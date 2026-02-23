JAVA EXCEPTIONS
===============

# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: Oracle Java Documentation, Effective Java (Joshua Bloch)

Stand: 2026-02-05
Status: VOLLSTAENDIG

EINFUEHRUNG
===========
Exceptions (Ausnahmen) sind Ereignisse, die den normalen Programmfluss
unterbrechen. Java verwendet ein robustes Exception-Handling-System,
das Fehler strukturiert behandelt und Programme widerstandsfaehiger macht.

Das Exception-Handling in Java basiert auf fuenf Schluesselbegriffen:
  - try: Markiert einen Block, der Exceptions werfen kann
  - catch: Faengt und behandelt spezifische Exceptions
  - finally: Wird immer ausgefuehrt (Aufraeumarbeiten)
  - throw: Wirft eine Exception
  - throws: Deklariert, dass eine Methode Exceptions werfen kann

EXCEPTION HIERARCHIE
====================
Alle Exceptions erben von java.lang.Throwable:

  Throwable
      |
      +-- Error (Schwerwiegende Systemfehler - NICHT fangen!)
      |     +-- OutOfMemoryError
      |     +-- StackOverflowError
      |     +-- VirtualMachineError
      |     +-- AssertionError
      |
      +-- Exception
            |
            +-- RuntimeException (Unchecked - Programmierfehler)
            |     +-- NullPointerException
            |     +-- ArrayIndexOutOfBoundsException
            |     +-- IndexOutOfBoundsException
            |     +-- IllegalArgumentException
            |     +-- IllegalStateException
            |     +-- NumberFormatException
            |     +-- ClassCastException
            |     +-- ArithmeticException
            |     +-- UnsupportedOperationException
            |
            +-- Checked Exceptions (Muessen behandelt werden)
                  +-- IOException
                  +-- FileNotFoundException
                  +-- SQLException
                  +-- ClassNotFoundException
                  +-- InterruptedException
                  +-- ParseException

CHECKED VS UNCHECKED EXCEPTIONS
===============================
  CHECKED EXCEPTIONS
  ------------------
  - Erben von Exception (aber nicht von RuntimeException)
  - Muessen explizit behandelt werden (try-catch oder throws)
  - Repraesentieren vorhersehbare Fehler (Datei nicht gefunden, etc.)
  - Compiler erzwingt Behandlung

  UNCHECKED EXCEPTIONS (Runtime Exceptions)
  -----------------------------------------
  - Erben von RuntimeException
  - Muessen nicht explizit behandelt werden
  - Repraesentieren Programmierfehler (null-Zugriff, falscher Index)
  - Sollten durch besseren Code vermieden werden

  ERRORS
  ------
  - Schwerwiegende Systemprobleme
  - Sollten NIEMALS gefangen werden
  - Programm kann sich nicht sinnvoll erholen

TRY-CATCH-FINALLY
=================
Die grundlegende Struktur zur Exception-Behandlung:

  Codebeispiel:
    public class TryCatchDemo {
        public static void main(String[] args) {
            FileReader reader = null;

            try {
                // Code, der Exceptions werfen kann
                reader = new FileReader("datei.txt");
                int zeichen = reader.read();
                System.out.println((char) zeichen);

            } catch (FileNotFoundException e) {
                // Spezifische Exception zuerst
                System.err.println("Datei nicht gefunden: " + e.getMessage());

            } catch (IOException e) {
                // Allgemeinere Exception danach
                System.err.println("Lesefehler: " + e.getMessage());

            } finally {
                // Wird IMMER ausgefuehrt (auch nach return!)
                // Ideal fuer Ressourcen-Aufraeumung
                if (reader != null) {
                    try {
                        reader.close();
                    } catch (IOException e) {
                        System.err.println("Fehler beim Schliessen");
                    }
                }
            }
        }
    }

  WICHTIGE REGELN:
  - Spezifische Exceptions VOR allgemeinen fangen
  - finally wird auch bei return ausgefuehrt
  - finally wird NICHT ausgefuehrt bei System.exit() oder JVM-Absturz
  - try muss mindestens einen catch- ODER finally-Block haben

MULTI-CATCH (JAVA 7+)
=====================
Mehrere Exceptions mit einem Handler behandeln:

  Codebeispiel:
    try {
        // Verschiedene moegliche Exceptions
        Class<?> clazz = Class.forName("MeineKlasse");
        Method method = clazz.getMethod("meineMethode");
        method.invoke(null);

    } catch (ClassNotFoundException | NoSuchMethodException e) {
        // Beide werden gleich behandelt
        System.err.println("Reflection-Fehler: " + e.getMessage());

    } catch (IllegalAccessException | InvocationTargetException e) {
        System.err.println("Aufruf-Fehler: " + e.getMessage());
    }

  HINWEIS:
  - Die Exception-Variable ist implizit final
  - Exceptions duerfen nicht in Vererbungsbeziehung stehen

TRY-WITH-RESOURCES (JAVA 7+)
============================
Automatisches Ressourcen-Management fuer AutoCloseable-Objekte:

  Codebeispiel:
    import java.io.*;

    public class TryWithResourcesDemo {
        public static void main(String[] args) {
            // Eine Ressource
            try (BufferedReader reader = new BufferedReader(
                    new FileReader("input.txt"))) {

                String zeile;
                while ((zeile = reader.readLine()) != null) {
                    System.out.println(zeile);
                }

            } catch (IOException e) {
                System.err.println("Fehler: " + e.getMessage());
            }
            // reader.close() wird automatisch aufgerufen!

            // Mehrere Ressourcen
            try (FileInputStream fis = new FileInputStream("quelle.txt");
                 FileOutputStream fos = new FileOutputStream("ziel.txt")) {

                byte[] buffer = new byte[1024];
                int bytes;
                while ((bytes = fis.read(buffer)) != -1) {
                    fos.write(buffer, 0, bytes);
                }

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

  VORTEILE:
  - Keine finally-Bloecke fuer close() noetig
  - Ressourcen werden in umgekehrter Reihenfolge geschlossen
  - Suppressed Exceptions werden erhalten

  JAVA 9+ ERWEITERUNG:
    // Effektiv finale Variablen koennen referenziert werden
    BufferedReader reader = new BufferedReader(new FileReader("datei.txt"));
    try (reader) {
        // reader nutzen
    }

THROW UND THROWS
================
  THROW - Exception werfen:
    public void setAlter(int alter) {
        if (alter < 0) {
            throw new IllegalArgumentException("Alter kann nicht negativ sein: " + alter);
        }
        if (alter > 150) {
            throw new IllegalArgumentException("Unrealistisches Alter: " + alter);
        }
        this.alter = alter;
    }

  THROWS - Exception deklarieren:
    public void leseDatei(String pfad) throws IOException {
        // IOException muss nicht hier gefangen werden
        // Aufrufer muss sie behandeln
        FileReader reader = new FileReader(pfad);
        // ...
    }

    // Mehrere Exceptions deklarieren
    public void komplexeMethode() throws IOException, SQLException {
        // ...
    }

  Codebeispiel - Vollstaendig:
    public class ThrowDemo {
        public static void main(String[] args) {
            try {
                validateInput("", 25);
            } catch (IllegalArgumentException e) {
                System.err.println("Validierungsfehler: " + e.getMessage());
            }
        }

        public static void validateInput(String name, int alter)
                throws IllegalArgumentException {

            if (name == null || name.trim().isEmpty()) {
                throw new IllegalArgumentException("Name darf nicht leer sein");
            }

            if (alter < 0 || alter > 150) {
                throw new IllegalArgumentException(
                    "Alter muss zwischen 0 und 150 liegen, war: " + alter);
            }
        }
    }

CUSTOM EXCEPTIONS
=================
Eigene Exception-Klassen fuer spezifische Anwendungsfaelle:

  Codebeispiel:
    // Checked Exception
    public class BusinessException extends Exception {

        private final String errorCode;

        public BusinessException(String message) {
            super(message);
            this.errorCode = "GENERAL";
        }

        public BusinessException(String message, String errorCode) {
            super(message);
            this.errorCode = errorCode;
        }

        public BusinessException(String message, Throwable cause) {
            super(message, cause);
            this.errorCode = "GENERAL";
        }

        public String getErrorCode() {
            return errorCode;
        }
    }

    // Unchecked Exception
    public class ValidationException extends RuntimeException {

        private final String fieldName;

        public ValidationException(String fieldName, String message) {
            super(message);
            this.fieldName = fieldName;
        }

        public String getFieldName() {
            return fieldName;
        }
    }

    // Verwendung
    public class BenutzerService {

        public void registrieren(String email, String passwort)
                throws BusinessException {

            if (!email.contains("@")) {
                throw new ValidationException("email", "Ungueltige E-Mail");
            }

            if (passwort.length() < 8) {
                throw new ValidationException("passwort", "Passwort zu kurz");
            }

            if (emailExistiert(email)) {
                throw new BusinessException(
                    "E-Mail bereits registriert", "USER_EXISTS");
            }

            // Registrierung durchfuehren...
        }
    }

EXCEPTION CHAINING
==================
Exceptions verketten, um Ursachen zu erhalten:

  Codebeispiel:
    public class ChainingDemo {

        public void obersteMethode() {
            try {
                mittlereMethode();
            } catch (ServiceException e) {
                System.err.println("Service-Fehler: " + e.getMessage());
                System.err.println("Ursache: " + e.getCause().getMessage());

                // Stack Trace ausgeben
                e.printStackTrace();
            }
        }

        public void mittlereMethode() throws ServiceException {
            try {
                datenbankAufruf();
            } catch (SQLException e) {
                // Original-Exception als Ursache beibehalten
                throw new ServiceException("Datenbankfehler", e);
            }
        }

        public void datenbankAufruf() throws SQLException {
            throw new SQLException("Verbindung fehlgeschlagen");
        }
    }

EXCEPTION BEST PRACTICES
========================
  1. SPEZIFISCHE EXCEPTIONS FANGEN
     // SCHLECHT
     catch (Exception e) { }

     // GUT
     catch (FileNotFoundException e) { }

  2. EXCEPTIONS NICHT VERSCHLUCKEN
     // SCHLECHT
     catch (IOException e) {
         // Nichts tun
     }

     // GUT
     catch (IOException e) {
         logger.error("Fehler beim Lesen", e);
         throw new ServiceException("Lesefehler", e);
     }

  3. LOGGING BEI EXCEPTIONS
     catch (Exception e) {
         // Stack Trace im Log behalten
         logger.error("Fehler aufgetreten: {}", e.getMessage(), e);
     }

  4. NICHT FUER CONTROL FLOW VERWENDEN
     // SCHLECHT
     try {
         int i = 0;
         while (true) {
             array[i++].doSomething();
         }
     } catch (ArrayIndexOutOfBoundsException e) { }

     // GUT
     for (int i = 0; i < array.length; i++) {
         array[i].doSomething();
     }

  5. PRAEVENTIVE PRUEFUNGEN
     // SCHLECHT
     try {
         return map.get(key).toString();
     } catch (NullPointerException e) {
         return "default";
     }

     // GUT
     Object value = map.get(key);
     return value != null ? value.toString() : "default";

  6. FINALLY FUER AUFRAEUMUNG
     // Oder besser: try-with-resources verwenden

  7. EXCEPTIONS DOKUMENTIEREN
     /**
      * Liest Konfiguration aus Datei.
      *
      * @param pfad Pfad zur Konfigurationsdatei
      * @throws FileNotFoundException wenn Datei nicht existiert
      * @throws InvalidConfigException wenn Format ungueltig
      */
     public Config leseConfig(String pfad) throws FileNotFoundException,
             InvalidConfigException {
         // ...
     }

  8. CHECKED VS UNCHECKED WAHL
     - Checked: Wenn Aufrufer sinnvoll reagieren kann
     - Unchecked: Bei Programmierfehlern, die behoben werden sollten

HAEUFIGE EXCEPTIONS UND IHRE BEDEUTUNG
======================================
  NullPointerException
    Zugriff auf null-Referenz. Loesung: Null-Check oder Optional

  ArrayIndexOutOfBoundsException
    Ungueltiger Array-Index. Loesung: Index-Validierung

  ClassCastException
    Ungueltiger Type-Cast. Loesung: instanceof-Pruefung

  NumberFormatException
    String kann nicht in Zahl konvertiert werden.
    Loesung: Eingabe validieren oder try-catch

  IllegalArgumentException
    Ungueltiges Argument uebergeben.
    Verwenden fuer eigene Validierungen

  IllegalStateException
    Objekt in ungueltigem Zustand fuer Operation.
    Z.B. Iterator.remove() ohne vorheriges next()

  ConcurrentModificationException
    Collection waehrend Iteration geaendert.
    Loesung: Iterator.remove() oder ConcurrentHashMap

JAVA 14+ NUETZLICHE NULLPOINTEREXCEPTION MELDUNGEN
==================================================
Ab Java 14 enthalten NullPointerExceptions hilfreiche Details:

  Vorher: NullPointerException
  Nachher: Cannot invoke "String.length()" because "str" is null

SIEHE AUCH
==========
  wiki/java/logging/
  wiki/java/debugging/
  wiki/java/io/
  wiki/java/optional/
  wiki/patterns/fehlerbehandlung/
  wiki/python/fehlerbehandlung/
