# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: docs.oracle.com/javase/tutorial/jdbc, Baeldung JDBC Tutorials

JDBC - JAVA DATABASE CONNECTIVITY
=================================

Stand: 2026-02-05

WAS IST JDBC?
-------------
JDBC (Java Database Connectivity) ist die Standard-API fuer den
Zugriff auf relationale Datenbanken in Java. Es bietet eine
einheitliche Schnittstelle fuer verschiedene Datenbanksysteme.

Unterstuetzte Datenbanken (mit entsprechenden Treibern):
  - PostgreSQL
  - MySQL / MariaDB
  - Oracle Database
  - Microsoft SQL Server
  - SQLite
  - H2 (In-Memory)

ARCHITEKTUR
-----------
  Java Application
        |
    JDBC API (java.sql.*)
        |
   JDBC Driver Manager
        |
  +-----------+-----------+
  |           |           |
PostgreSQL  MySQL      Oracle
 Driver     Driver     Driver
  |           |           |
PostgreSQL  MySQL      Oracle
   DB         DB         DB

GRUNDLEGENDE SCHRITTE
---------------------
  1. Treiber laden (automatisch seit JDBC 4.0)
  2. Verbindung herstellen (Connection)
  3. Statement erstellen
  4. Query ausfuehren
  5. ResultSet verarbeiten
  6. Ressourcen schliessen

VERBINDUNG HERSTELLEN
---------------------
  // JDBC URL Format
  // jdbc:subprotocol:subname

  // PostgreSQL
  String url = "jdbc:postgresql://localhost:5432/mydb";

  // MySQL
  String url = "jdbc:mysql://localhost:3306/mydb";

  // SQLite
  String url = "jdbc:sqlite:C:/data/mydb.db";

  // H2 In-Memory
  String url = "jdbc:h2:mem:testdb";

  // Verbindung mit try-with-resources (EMPFOHLEN)
  try (Connection conn = DriverManager.getConnection(
          url, "username", "password")) {

      // Datenbankoperationen hier

  } catch (SQLException e) {
      e.printStackTrace();
  }
  // Connection wird automatisch geschlossen

STATEMENT ARTEN
---------------
  1. Statement        Einfache SQL-Befehle (NICHT fuer User-Input!)
  2. PreparedStatement  Parametrisierte Queries (SICHER)
  3. CallableStatement  Stored Procedures

STATEMENT (NUR FUER STATISCHES SQL)
-----------------------------------
WARNUNG: Niemals mit User-Input verwenden (SQL-Injection-Gefahr!)

  try (Connection conn = DriverManager.getConnection(url, user, pass);
       Statement stmt = conn.createStatement()) {

      // SELECT
      ResultSet rs = stmt.executeQuery("SELECT * FROM users");
      while (rs.next()) {
          System.out.println(rs.getString("name"));
      }

      // INSERT, UPDATE, DELETE
      int rowsAffected = stmt.executeUpdate(
          "INSERT INTO users (name) VALUES ('Max')");

  } catch (SQLException e) {
      e.printStackTrace();
  }

PREPAREDSTATEMENT (EMPFOHLEN)
-----------------------------
Sicher gegen SQL-Injection, bessere Performance bei Wiederholung:

  String sql = "SELECT * FROM users WHERE email = ? AND active = ?";

  try (Connection conn = DriverManager.getConnection(url, user, pass);
       PreparedStatement pstmt = conn.prepareStatement(sql)) {

      // Parameter setzen (Index beginnt bei 1!)
      pstmt.setString(1, "max@example.com");
      pstmt.setBoolean(2, true);

      try (ResultSet rs = pstmt.executeQuery()) {
          while (rs.next()) {
              long id = rs.getLong("id");
              String name = rs.getString("name");
              String email = rs.getString("email");
              LocalDate created = rs.getDate("created_at").toLocalDate();
          }
      }

  } catch (SQLException e) {
      e.printStackTrace();
  }

INSERT MIT GENERIERTEM KEY
--------------------------
  String sql = "INSERT INTO users (name, email) VALUES (?, ?)";

  try (PreparedStatement pstmt = conn.prepareStatement(
          sql, Statement.RETURN_GENERATED_KEYS)) {

      pstmt.setString(1, "Max Mustermann");
      pstmt.setString(2, "max@example.com");

      int affected = pstmt.executeUpdate();

      // Generierte ID abrufen
      try (ResultSet keys = pstmt.getGeneratedKeys()) {
          if (keys.next()) {
              long generatedId = keys.getLong(1);
              System.out.println("Neue ID: " + generatedId);
          }
      }
  }

RESULTSET VERARBEITUNG
----------------------
  // Spalten per Name (EMPFOHLEN)
  String name = rs.getString("name");
  int age = rs.getInt("age");
  double salary = rs.getDouble("salary");
  boolean active = rs.getBoolean("active");
  Date date = rs.getDate("created_at");
  Timestamp timestamp = rs.getTimestamp("updated_at");

  // Spalten per Index (weniger lesbar)
  String name = rs.getString(1);
  int age = rs.getInt(2);

  // NULL-Pruefung
  int age = rs.getInt("age");
  if (rs.wasNull()) {
      // Wert war NULL in der Datenbank
  }

  // ResultSet-Typen
  // TYPE_FORWARD_ONLY     Nur vorwaerts (Standard)
  // TYPE_SCROLL_INSENSITIVE  Vor- und zurueck, snapshot
  // TYPE_SCROLL_SENSITIVE    Vor- und zurueck, live

BATCH OPERATIONS
----------------
Mehrere Operationen gebuendelt ausfuehren:

  String sql = "INSERT INTO users (name, email) VALUES (?, ?)";

  try (PreparedStatement pstmt = conn.prepareStatement(sql)) {

      conn.setAutoCommit(false);  // Transaktion starten

      for (User user : users) {
          pstmt.setString(1, user.getName());
          pstmt.setString(2, user.getEmail());
          pstmt.addBatch();
      }

      int[] results = pstmt.executeBatch();
      conn.commit();

  } catch (SQLException e) {
      conn.rollback();
      throw e;
  }

TRANSAKTIONEN
-------------
ACID-Eigenschaften fuer Datenkonsistenz:

  Connection conn = null;
  try {
      conn = DriverManager.getConnection(url, user, pass);
      conn.setAutoCommit(false);  // Transaktion starten

      // Mehrere Operationen
      transferMoney(conn, fromAccount, toAccount, amount);
      logTransaction(conn, fromAccount, toAccount, amount);

      conn.commit();  // Alles erfolgreich

  } catch (SQLException e) {
      if (conn != null) {
          try {
              conn.rollback();  // Alles rueckgaengig
          } catch (SQLException ex) {
              ex.printStackTrace();
          }
      }
      throw e;
  } finally {
      if (conn != null) {
          conn.setAutoCommit(true);
          conn.close();
      }
  }

Isolation Levels:
  TRANSACTION_READ_UNCOMMITTED  Dirty Reads moeglich
  TRANSACTION_READ_COMMITTED    Standard PostgreSQL
  TRANSACTION_REPEATABLE_READ   Standard MySQL
  TRANSACTION_SERIALIZABLE      Hoechste Isolation

  conn.setTransactionIsolation(
      Connection.TRANSACTION_READ_COMMITTED);

CONNECTION POOLING
------------------
Verbindungen wiederverwenden fuer bessere Performance.

HikariCP (empfohlen):

  HikariConfig config = new HikariConfig();
  config.setJdbcUrl("jdbc:postgresql://localhost:5432/mydb");
  config.setUsername("user");
  config.setPassword("password");

  // Pool-Einstellungen
  config.setMaximumPoolSize(10);
  config.setMinimumIdle(5);
  config.setIdleTimeout(300000);      // 5 Minuten
  config.setConnectionTimeout(20000); // 20 Sekunden
  config.setMaxLifetime(1800000);     // 30 Minuten

  HikariDataSource dataSource = new HikariDataSource(config);

  // Verbindung aus Pool holen
  try (Connection conn = dataSource.getConnection()) {
      // Datenbankoperationen
  }

  // Bei Anwendungsende
  dataSource.close();

DAO PATTERN
-----------
Data Access Object - Trennung von Datenzugriff und Business-Logik:

  public interface UserDao {
      Optional<User> findById(long id);
      List<User> findAll();
      User save(User user);
      void update(User user);
      void delete(long id);
  }

  public class JdbcUserDao implements UserDao {

      private final DataSource dataSource;

      public JdbcUserDao(DataSource dataSource) {
          this.dataSource = dataSource;
      }

      @Override
      public Optional<User> findById(long id) {
          String sql = "SELECT * FROM users WHERE id = ?";

          try (Connection conn = dataSource.getConnection();
               PreparedStatement pstmt = conn.prepareStatement(sql)) {

              pstmt.setLong(1, id);

              try (ResultSet rs = pstmt.executeQuery()) {
                  if (rs.next()) {
                      return Optional.of(mapRow(rs));
                  }
              }
          } catch (SQLException e) {
              throw new DataAccessException("Fehler beim Laden", e);
          }
          return Optional.empty();
      }

      @Override
      public User save(User user) {
          String sql = "INSERT INTO users (name, email) VALUES (?, ?)";

          try (Connection conn = dataSource.getConnection();
               PreparedStatement pstmt = conn.prepareStatement(
                   sql, Statement.RETURN_GENERATED_KEYS)) {

              pstmt.setString(1, user.getName());
              pstmt.setString(2, user.getEmail());
              pstmt.executeUpdate();

              try (ResultSet keys = pstmt.getGeneratedKeys()) {
                  if (keys.next()) {
                      user.setId(keys.getLong(1));
                  }
              }
              return user;

          } catch (SQLException e) {
              throw new DataAccessException("Fehler beim Speichern", e);
          }
      }

      private User mapRow(ResultSet rs) throws SQLException {
          return new User(
              rs.getLong("id"),
              rs.getString("name"),
              rs.getString("email"),
              rs.getTimestamp("created_at").toLocalDateTime()
          );
      }
  }

FEHLERBEHANDLUNG
----------------
SQLException liefert detaillierte Informationen:

  try {
      // Datenbankoperation
  } catch (SQLException e) {
      System.err.println("SQL State: " + e.getSQLState());
      System.err.println("Error Code: " + e.getErrorCode());
      System.err.println("Message: " + e.getMessage());

      // Verkettete Exceptions
      SQLException next = e.getNextException();
      while (next != null) {
          System.err.println("Next: " + next.getMessage());
          next = next.getNextException();
      }
  }

Haeufige SQL States:
  23505  Unique Constraint Violation
  23503  Foreign Key Violation
  42P01  Tabelle nicht gefunden
  08001  Verbindung fehlgeschlagen

BEST PRACTICES
--------------
  1. Immer PreparedStatement verwenden
     - Schutz vor SQL-Injection
     - Bessere Performance durch Query-Caching

  2. Try-with-resources nutzen
     - Automatisches Schliessen von Ressourcen
     - Verhindert Connection Leaks

  3. Connection Pooling einsetzen
     - HikariCP ist Industriestandard
     - Nie fuer jeden Request neue Connection

  4. Transaktionen bewusst einsetzen
     - Nur wenn wirklich noetig
     - Kurz halten (Lock-Zeiten minimieren)

  5. Keine Passwoerter im Code
     - Umgebungsvariablen oder Config-Dateien
     - Secrets Manager in Produktion

  6. Logging aktivieren
     - SQL-Queries im Debug-Modus loggen
     - Slow Queries ueberwachen

JDBC VS. ORM (JPA/HIBERNATE)
----------------------------
  Aspekt          JDBC              JPA/Hibernate
  --------------------------------------------------------
  Kontrolle       Volle SQL-Kontrolle   Abstraktion
  Performance     Sehr gut (direkt)     Gut (mit Tuning)
  Boilerplate     Viel                  Wenig
  Lernkurve       Flach                 Steil
  Caching         Manuell               Automatisch
  Portabilitaet   SQL-Dialekt beachten  Abstrahiert

Wann JDBC direkt?
  - Komplexe, optimierte Queries
  - Bulk-Operationen
  - Volle Kontrolle erforderlich
  - Einfache Anwendungen

Wann JPA?
  - CRUD-lastige Anwendungen
  - Schnelle Entwicklung
  - Objekt-Relationale Abbildung wichtig

SIEHE AUCH
==========
  wiki/java/README.txt           Java Uebersicht
  wiki/java/spring/README.txt    Spring Data JPA
  wiki/informatik/datenbanken/README.txt
