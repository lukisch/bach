# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: docs.oracle.com/javase/tutorial/essential/io, Baeldung Java IO

JAVA I/O UND NIO
================

Stand: 2026-02-05

UEBERBLICK
----------
Java bietet zwei APIs fuer Ein-/Ausgabe-Operationen:

  java.io    Klassische I/O (Stream-basiert, blockierend)
  java.nio   New I/O (Buffer/Channel-basiert, non-blocking)

Seit Java 7 gibt es java.nio.file (NIO.2) mit verbessertem
File-Handling ueber die Files und Path Klassen.

KLASSISCHE I/O (java.io)
========================

STREAM-HIERARCHIE
-----------------
  Byte-Streams (binaer):
    InputStream  <- FileInputStream, BufferedInputStream
    OutputStream <- FileOutputStream, BufferedOutputStream

  Character-Streams (Text):
    Reader <- FileReader, BufferedReader, InputStreamReader
    Writer <- FileWriter, BufferedWriter, OutputStreamWriter

DATEI LESEN (TEXT)
------------------
  // Modern mit try-with-resources (EMPFOHLEN)
  try (BufferedReader reader = new BufferedReader(
          new FileReader("input.txt", StandardCharsets.UTF_8))) {

      String line;
      while ((line = reader.readLine()) != null) {
          System.out.println(line);
      }

  } catch (IOException e) {
      e.printStackTrace();
  }

  // Alle Zeilen auf einmal (Java 8+)
  try (Stream<String> lines = Files.lines(
          Path.of("input.txt"), StandardCharsets.UTF_8)) {

      lines.filter(line -> !line.isEmpty())
           .map(String::trim)
           .forEach(System.out::println);
  }

  // Gesamten Inhalt als String
  String content = Files.readString(
      Path.of("input.txt"), StandardCharsets.UTF_8);

DATEI SCHREIBEN (TEXT)
----------------------
  // Mit BufferedWriter
  try (BufferedWriter writer = new BufferedWriter(
          new FileWriter("output.txt", StandardCharsets.UTF_8))) {

      writer.write("Zeile 1");
      writer.newLine();
      writer.write("Zeile 2");

  } catch (IOException e) {
      e.printStackTrace();
  }

  // Mit PrintWriter (bequemer)
  try (PrintWriter writer = new PrintWriter(
          new FileWriter("output.txt", StandardCharsets.UTF_8))) {

      writer.println("Zeile 1");
      writer.printf("Zahl: %d, Text: %s%n", 42, "Hallo");
  }

  // Einzeiler mit Files
  Files.writeString(Path.of("output.txt"), "Inhalt");

  // Mehrere Zeilen
  List<String> lines = List.of("Zeile 1", "Zeile 2", "Zeile 3");
  Files.write(Path.of("output.txt"), lines);

BINAERE DATEIEN
---------------
  // Lesen
  try (BufferedInputStream bis = new BufferedInputStream(
          new FileInputStream("image.png"))) {

      byte[] buffer = new byte[8192];
      int bytesRead;
      while ((bytesRead = bis.read(buffer)) != -1) {
          // buffer verarbeiten (0 bis bytesRead-1)
      }
  }

  // Schreiben
  try (BufferedOutputStream bos = new BufferedOutputStream(
          new FileOutputStream("output.bin"))) {

      byte[] data = getByteData();
      bos.write(data);
  }

  // Komplett einlesen
  byte[] bytes = Files.readAllBytes(Path.of("image.png"));

  // Komplett schreiben
  Files.write(Path.of("output.bin"), bytes);

NIO.2 - FILES UND PATH
======================

PATH (DATEIPFADE)
-----------------
  // Path erstellen
  Path path = Path.of("C:/Users/User/Documents/file.txt");
  Path path = Path.of("C:", "Users", "User", "Documents", "file.txt");
  Path path = Paths.get("relative/path/file.txt");

  // Path-Informationen
  path.getFileName()     // file.txt
  path.getParent()       // C:/Users/User/Documents
  path.getRoot()         // C:/
  path.isAbsolute()      // true
  path.getNameCount()    // 4
  path.getName(0)        // Users

  // Pfade kombinieren
  Path base = Path.of("C:/Users/User");
  Path full = base.resolve("Documents/file.txt");
  // -> C:/Users/User/Documents/file.txt

  // Relativen Pfad berechnen
  Path p1 = Path.of("C:/Users/User/Documents");
  Path p2 = Path.of("C:/Users/User/Downloads/file.txt");
  Path relative = p1.relativize(p2);
  // -> ../Downloads/file.txt

  // Normalisieren (. und .. aufloesen)
  Path messy = Path.of("C:/Users/./User/../User/Documents");
  Path clean = messy.normalize();
  // -> C:/Users/User/Documents

FILES (DATEIOPERATIONEN)
------------------------
  Path path = Path.of("file.txt");

  // Existenz pruefen
  boolean exists = Files.exists(path);
  boolean notExists = Files.notExists(path);

  // Datei-Attribute
  boolean isRegular = Files.isRegularFile(path);
  boolean isDir = Files.isDirectory(path);
  boolean isReadable = Files.isReadable(path);
  boolean isWritable = Files.isWritable(path);
  boolean isHidden = Files.isHidden(path);
  long size = Files.size(path);
  FileTime modified = Files.getLastModifiedTime(path);

  // Datei erstellen
  Files.createFile(path);

  // Verzeichnis erstellen
  Files.createDirectory(Path.of("newdir"));
  Files.createDirectories(Path.of("a/b/c/d"));  // inkl. Eltern

  // Kopieren
  Files.copy(source, target);
  Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
  Files.copy(inputStream, target);
  Files.copy(source, outputStream);

  // Verschieben / Umbenennen
  Files.move(source, target);
  Files.move(source, target, StandardCopyOption.ATOMIC_MOVE);

  // Loeschen
  Files.delete(path);        // wirft Exception wenn nicht existiert
  Files.deleteIfExists(path); // gibt false zurueck

  // Temporaere Dateien
  Path tempFile = Files.createTempFile("prefix_", ".tmp");
  Path tempDir = Files.createTempDirectory("myapp_");

VERZEICHNIS DURCHLAUFEN
-----------------------
  // Direkte Kinder (nicht rekursiv)
  try (DirectoryStream<Path> stream =
          Files.newDirectoryStream(dir, "*.txt")) {
      for (Path entry : stream) {
          System.out.println(entry.getFileName());
      }
  }

  // Rekursiv mit walk()
  try (Stream<Path> paths = Files.walk(startDir)) {
      paths.filter(Files::isRegularFile)
           .filter(p -> p.toString().endsWith(".java"))
           .forEach(System.out::println);
  }

  // Rekursiv mit Tiefenbegrenzung
  try (Stream<Path> paths = Files.walk(startDir, 2)) {
      // maxDepth = 2
  }

  // Mit FileVisitor (volle Kontrolle)
  Files.walkFileTree(startDir, new SimpleFileVisitor<Path>() {

      @Override
      public FileVisitResult visitFile(Path file,
              BasicFileAttributes attrs) {
          System.out.println("Datei: " + file);
          return FileVisitResult.CONTINUE;
      }

      @Override
      public FileVisitResult preVisitDirectory(Path dir,
              BasicFileAttributes attrs) {
          System.out.println("Betrete: " + dir);
          return FileVisitResult.CONTINUE;
      }

      @Override
      public FileVisitResult visitFileFailed(Path file,
              IOException exc) {
          System.err.println("Fehler: " + file);
          return FileVisitResult.CONTINUE;
      }
  });

WATCHSERVICE (DATEIAENDERUNGEN UEBERWACHEN)
-------------------------------------------
  WatchService watchService = FileSystems.getDefault().newWatchService();

  Path dir = Path.of("C:/watched");
  dir.register(watchService,
      StandardWatchEventKinds.ENTRY_CREATE,
      StandardWatchEventKinds.ENTRY_MODIFY,
      StandardWatchEventKinds.ENTRY_DELETE);

  while (true) {
      WatchKey key = watchService.take();  // blockiert

      for (WatchEvent<?> event : key.pollEvents()) {
          WatchEvent.Kind<?> kind = event.kind();
          Path filename = (Path) event.context();

          System.out.printf("%s: %s%n", kind, filename);
      }

      boolean valid = key.reset();
      if (!valid) {
          break;  // Verzeichnis nicht mehr zugreifbar
      }
  }

NIO CHANNELS UND BUFFERS
========================

KONZEPT
-------
  Channel    Verbindung zu I/O-Ressource (bidirektional)
  Buffer     Container fuer Daten (feste Groesse)

Channels:
  FileChannel        Dateizugriff
  SocketChannel      TCP Client
  ServerSocketChannel  TCP Server
  DatagramChannel    UDP

FILECHANNEL
-----------
  // Lesen
  try (FileChannel channel = FileChannel.open(
          Path.of("input.txt"), StandardOpenOption.READ)) {

      ByteBuffer buffer = ByteBuffer.allocate(1024);

      while (channel.read(buffer) > 0) {
          buffer.flip();  // Wechsel zu Lese-Modus

          while (buffer.hasRemaining()) {
              System.out.print((char) buffer.get());
          }

          buffer.clear();  // Zurueck zu Schreib-Modus
      }
  }

  // Schreiben
  try (FileChannel channel = FileChannel.open(
          Path.of("output.txt"),
          StandardOpenOption.CREATE,
          StandardOpenOption.WRITE)) {

      ByteBuffer buffer = ByteBuffer.wrap("Hello NIO!".getBytes());
      channel.write(buffer);
  }

MEMORY-MAPPED FILES
-------------------
Fuer grosse Dateien - direkter Zugriff auf Speicher:

  try (FileChannel channel = FileChannel.open(
          Path.of("large.bin"), StandardOpenOption.READ)) {

      MappedByteBuffer buffer = channel.map(
          FileChannel.MapMode.READ_ONLY, 0, channel.size());

      // Direkter Zugriff
      byte b = buffer.get(1000000);  // 1 millionste Byte
  }

BUFFER OPERATIONEN
------------------
  ByteBuffer buffer = ByteBuffer.allocate(1024);

  // Wichtige Positionen
  buffer.capacity()   // Maximale Groesse (unveraenderlich)
  buffer.position()   // Aktuelle Lese-/Schreibposition
  buffer.limit()      // Aktuelles Limit
  buffer.remaining()  // limit - position

  // Schreiben in Buffer
  buffer.put((byte) 65);
  buffer.putInt(42);
  buffer.putDouble(3.14);

  // Wechsel zu Lese-Modus
  buffer.flip();  // limit = position, position = 0

  // Lesen aus Buffer
  byte b = buffer.get();
  int i = buffer.getInt();
  double d = buffer.getDouble();

  // Zuruecksetzen
  buffer.clear();   // position = 0, limit = capacity
  buffer.rewind();  // position = 0, limit unveraendert
  buffer.compact(); // Ungelesene Daten nach vorne, zum Weiterschreiben

SERIALISIERUNG
==============

JAVA SERIALIZATION
------------------
WARNUNG: Sicherheitsrisiko bei unbekannten Daten!

  public class User implements Serializable {
      private static final long serialVersionUID = 1L;

      private String name;
      private transient String password;  // Nicht serialisieren

      // Getter, Setter
  }

  // Schreiben
  try (ObjectOutputStream oos = new ObjectOutputStream(
          new FileOutputStream("user.ser"))) {
      oos.writeObject(user);
  }

  // Lesen
  try (ObjectInputStream ois = new ObjectInputStream(
          new FileInputStream("user.ser"))) {
      User user = (User) ois.readObject();
  }

BESSER: JSON SERIALISIERUNG
---------------------------
Mit Jackson:

  ObjectMapper mapper = new ObjectMapper();

  // Schreiben
  mapper.writeValue(new File("user.json"), user);
  String json = mapper.writeValueAsString(user);

  // Lesen
  User user = mapper.readValue(new File("user.json"), User.class);
  User user = mapper.readValue(jsonString, User.class);

BEST PRACTICES
--------------
  1. Immer try-with-resources verwenden
     - Automatisches Schliessen
     - Keine Resource Leaks

  2. BufferedReader/Writer fuer Text
     - Deutlich bessere Performance
     - Zeilenweises Lesen moeglich

  3. NIO.2 Files Klasse bevorzugen
     - Moderne API
     - Weniger Boilerplate
     - Bessere Fehlerbehandlung

  4. Encoding explizit angeben
     - StandardCharsets.UTF_8
     - Nie System-Default verlassen

  5. Grosse Dateien streamen
     - Nicht komplett in Speicher laden
     - Files.lines() fuer zeilenweise Verarbeitung

  6. Paths plattformunabhaengig
     - Path.of() statt String-Konkatenation
     - File.separator vermeiden

VERGLEICH: java.io vs java.nio
------------------------------
  Aspekt         java.io           java.nio
  ---------------------------------------------------
  Modell         Stream-basiert    Buffer/Channel
  Blocking       Ja                Optional (NIO)
  Direktzugriff  Nein              Ja (Memory-Mapped)
  API-Alter      Java 1.0          Java 1.4 / 7
  Einfachheit    Hoch              Mittel
  Performance    Gut               Sehr gut (gross)
  Use Case       Einfache I/O      High-Performance

HAEUFIGE AUFGABEN
-----------------
  // Datei in String
  String content = Files.readString(path);

  // String in Datei
  Files.writeString(path, content);

  // Datei kopieren
  Files.copy(source, target, REPLACE_EXISTING);

  // Verzeichnis mit Inhalt loeschen
  Files.walk(dir)
       .sorted(Comparator.reverseOrder())
       .forEach(p -> { try { Files.delete(p); } catch (Exception e) {} });

  // Alle Java-Dateien finden
  Files.walk(dir)
       .filter(p -> p.toString().endsWith(".java"))
       .collect(Collectors.toList());

SIEHE AUCH
==========
  wiki/java/README.txt           Java Uebersicht
  wiki/java/jdbc/README.txt      Datenbankzugriff
  wiki/informatik/programmierung/README.txt
