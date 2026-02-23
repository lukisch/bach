# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: Oracle Documentation, PostgreSQL Manual, MongoDB Docs, ACID-Theorie nach Haerder/Reuter

================================================================================
DATENBANKEN - UMFASSENDER WIKI-ARTIKEL
================================================================================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
INHALTSVERZEICHNIS
================================================================================
  1. Einfuehrung
  2. Relationale Datenbanken (RDBMS)
  3. SQL - Structured Query Language
  4. Datenmodellierung
  5. Normalisierung
  6. Transaktionen und ACID
  7. NoSQL-Datenbanken
  8. Indexierung und Performance
  9. Backup und Recovery
  10. Best Practices
  11. Werkzeuge und Administration

================================================================================
1. EINFUEHRUNG
================================================================================

  Datenbanken sind organisierte Sammlungen von strukturierten Daten, die
  elektronisch gespeichert und verwaltet werden. Ein Datenbankmanagementsystem
  (DBMS) ermoeglicht das Erstellen, Abfragen, Aktualisieren und Verwalten
  dieser Daten.

  HAUPTKATEGORIEN:
  ----------------
    - Relationale Datenbanken (RDBMS): Tabellenbasiert, SQL
    - NoSQL-Datenbanken: Document, Key-Value, Graph, Column-Family
    - NewSQL: Kombination aus relationalen und NoSQL-Eigenschaften
    - In-Memory-Datenbanken: Primaer im Arbeitsspeicher

  EINSATZGEBIETE:
  ---------------
    - Webanwendungen und E-Commerce
    - Enterprise Resource Planning (ERP)
    - Customer Relationship Management (CRM)
    - Data Warehousing und Business Intelligence
    - Echtzeit-Analyse und IoT

================================================================================
2. RELATIONALE DATENBANKEN (RDBMS)
================================================================================

  Relationale Datenbanken speichern Daten in Tabellen (Relationen), die aus
  Zeilen (Tupel/Datensaetze) und Spalten (Attribute) bestehen.

  GRUNDKONZEPTE:
  --------------
    TABELLE (Relation):
      - Sammlung von Datensaetzen gleicher Struktur
      - Jede Zeile ist eindeutig identifizierbar

    PRIMAERSCHLUESSEL (Primary Key):
      - Eindeutige Identifikation jeder Zeile
      - Darf nicht NULL sein
      - Beispiel: Kunden-ID, Bestellnummer

    FREMDSCHLUESSEL (Foreign Key):
      - Verweis auf Primaerschluessel einer anderen Tabelle
      - Stellt Beziehungen zwischen Tabellen her
      - Ermoeglicht referenzielle Integritaet

  BELIEBTE RDBMS:
  ---------------
    MySQL/MariaDB:
      - Open Source, weit verbreitet
      - Gut fuer Webanwendungen
      - Storage Engines: InnoDB, MyISAM

    PostgreSQL:
      - Erweiterte Funktionen (JSON, Arrays)
      - Strenge Standards-Konformitaet
      - Exzellent fuer komplexe Abfragen

    Oracle Database:
      - Enterprise-Loesung
      - Hochverfuegbarkeit und Skalierbarkeit
      - Umfangreiche Verwaltungstools

    Microsoft SQL Server:
      - Integration mit Microsoft-Oekosystem
      - Business Intelligence Features
      - Azure-Integration

    SQLite:
      - Serverlos, dateibasiert
      - Ideal fuer eingebettete Systeme
      - Null-Konfiguration

================================================================================
3. SQL - STRUCTURED QUERY LANGUAGE
================================================================================

  SQL ist die Standardsprache fuer relationale Datenbanken.

  DDL - DATA DEFINITION LANGUAGE:
  -------------------------------
    CREATE TABLE kunden (
        id          INT PRIMARY KEY AUTO_INCREMENT,
        name        VARCHAR(100) NOT NULL,
        email       VARCHAR(255) UNIQUE,
        erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    ALTER TABLE kunden ADD COLUMN telefon VARCHAR(20);

    DROP TABLE alte_daten;

  DML - DATA MANIPULATION LANGUAGE:
  ---------------------------------
    -- Einfuegen
    INSERT INTO kunden (name, email) VALUES ('Max Mustermann', 'max@example.de');

    -- Aktualisieren
    UPDATE kunden SET email = 'neu@example.de' WHERE id = 1;

    -- Loeschen
    DELETE FROM kunden WHERE id = 1;

    -- Abfragen
    SELECT name, email FROM kunden WHERE erstellt_am > '2026-01-01';

  JOINS - TABELLEN VERKNUEPFEN:
  -----------------------------
    INNER JOIN:
      SELECT k.name, b.bestellnummer
      FROM kunden k
      INNER JOIN bestellungen b ON k.id = b.kunden_id;

    LEFT JOIN:
      SELECT k.name, b.bestellnummer
      FROM kunden k
      LEFT JOIN bestellungen b ON k.id = b.kunden_id;
      -- Zeigt auch Kunden ohne Bestellungen

    RIGHT JOIN, FULL OUTER JOIN, CROSS JOIN analog

  AGGREGATFUNKTIONEN:
  -------------------
    SELECT
        COUNT(*) AS anzahl,
        SUM(betrag) AS summe,
        AVG(betrag) AS durchschnitt,
        MIN(betrag) AS minimum,
        MAX(betrag) AS maximum
    FROM bestellungen
    GROUP BY kunden_id
    HAVING SUM(betrag) > 1000;

================================================================================
4. DATENMODELLIERUNG
================================================================================

  ER-DIAGRAMME (Entity-Relationship):
  -----------------------------------
    Entitaeten: Objekte der realen Welt (Kunde, Produkt, Bestellung)
    Attribute: Eigenschaften der Entitaeten (Name, Preis, Datum)
    Beziehungen: Verbindungen zwischen Entitaeten

  KARDINALITAETEN:
  ----------------
    1:1   - Ein Mitarbeiter hat einen Parkplatz
    1:N   - Ein Kunde hat viele Bestellungen
    N:M   - Studenten belegen viele Kurse, Kurse haben viele Studenten

  BEISPIEL-MODELL E-COMMERCE:
  ---------------------------
    [KUNDE] 1---N [BESTELLUNG] N---M [PRODUKT]
       |                              |
       +--- id (PK)                   +--- id (PK)
       +--- name                      +--- bezeichnung
       +--- email                     +--- preis
       +--- adresse                   +--- lagerbestand

================================================================================
5. NORMALISIERUNG
================================================================================

  Normalisierung reduziert Redundanz und verbessert Datenintegritaet.

  ERSTE NORMALFORM (1NF):
  -----------------------
    - Atomare Werte (keine Listen in Feldern)
    - Eindeutige Zeilenerkennung

    FALSCH: name = "Max, Moritz"
    RICHTIG: Separate Zeilen fuer Max und Moritz

  ZWEITE NORMALFORM (2NF):
  ------------------------
    - 1NF erfuellt
    - Alle Nicht-Schluessel-Attribute abhaengig vom gesamten Primaerschluessel

    Bei zusammengesetzten Schluesseln: Keine partielle Abhaengigkeit

  DRITTE NORMALFORM (3NF):
  ------------------------
    - 2NF erfuellt
    - Keine transitiven Abhaengigkeiten

    FALSCH: bestellung(id, kunde_id, kunde_name) -- kunde_name haengt von kunde_id ab
    RICHTIG: Separate Kundentabelle

  DENORMALISIERUNG:
  -----------------
    Bewusste Verletzung der Normalformen fuer Performance:
    - Vorberechnete Aggregate
    - Redundante Kopien fuer schnellere Lesezugriffe
    - Typisch in Data Warehouses

================================================================================
6. TRANSAKTIONEN UND ACID
================================================================================

  ACID-PRINZIPIEN:
  ----------------
    ATOMICITY (Atomaritaet):
      - Transaktion ist unteilbar
      - Alles oder nichts wird ausgefuehrt
      - Bei Fehler: Rollback

    CONSISTENCY (Konsistenz):
      - Datenbank bleibt in gueltigem Zustand
      - Constraints werden eingehalten
      - Integritaetsregeln gelten

    ISOLATION:
      - Parallele Transaktionen beeinflussen sich nicht
      - Verschiedene Isolationsebenen moeglich

    DURABILITY (Dauerhaftigkeit):
      - Abgeschlossene Transaktionen sind persistent
      - Auch bei Systemausfall

  ISOLATION LEVELS:
  -----------------
    READ UNCOMMITTED: Niedrigste Isolation, Dirty Reads moeglich
    READ COMMITTED:   Nur committete Daten sichtbar
    REPEATABLE READ:  Konsistente Lesungen innerhalb Transaktion
    SERIALIZABLE:     Hoechste Isolation, sequentielle Ausfuehrung

  TRANSAKTIONSBEISPIEL:
  ---------------------
    START TRANSACTION;

    UPDATE konten SET saldo = saldo - 100 WHERE id = 1;
    UPDATE konten SET saldo = saldo + 100 WHERE id = 2;

    -- Bei Erfolg
    COMMIT;

    -- Bei Fehler
    -- ROLLBACK;

================================================================================
7. NOSQL-DATENBANKEN
================================================================================

  NoSQL = "Not Only SQL" - Alternative zu relationalen Datenbanken

  DOCUMENT STORES:
  ----------------
    MongoDB, CouchDB
    - Speichern JSON/BSON-Dokumente
    - Schema-flexibel
    - Gut fuer hierarchische Daten

    Beispiel MongoDB:
    {
      "_id": ObjectId("..."),
      "name": "Max Mustermann",
      "adressen": [
        {"typ": "privat", "stadt": "Berlin"},
        {"typ": "arbeit", "stadt": "Hamburg"}
      ]
    }

  KEY-VALUE STORES:
  -----------------
    Redis, Memcached
    - Einfaches Schluessel-Wert-Modell
    - Extrem schnell (oft in-memory)
    - Caching, Session-Speicher

    Beispiel Redis:
    SET user:1001:name "Max"
    GET user:1001:name

  COLUMN-FAMILY STORES:
  ---------------------
    Apache Cassandra, HBase
    - Spaltenorientierte Speicherung
    - Skalierbar fuer Big Data
    - Hohe Schreibperformance

  GRAPH-DATENBANKEN:
  ------------------
    Neo4j, Amazon Neptune
    - Knoten und Kanten
    - Beziehungsanalyse
    - Social Networks, Empfehlungssysteme

    Beispiel Cypher (Neo4j):
    MATCH (p:Person)-[:KENNT]->(f:Person)
    WHERE p.name = "Max"
    RETURN f.name

================================================================================
8. INDEXIERUNG UND PERFORMANCE
================================================================================

  INDEXTYPEN:
  -----------
    B-Tree Index:     Standard, gut fuer Gleichheit und Bereiche
    Hash Index:       Schnell fuer exakte Treffer
    Volltext-Index:   Textsuche
    Raeumlicher Index: Geodaten (GIS)

  INDEX ERSTELLEN:
  ----------------
    CREATE INDEX idx_kunden_email ON kunden(email);
    CREATE UNIQUE INDEX idx_kunden_id ON kunden(id);
    CREATE INDEX idx_multi ON bestellungen(kunden_id, datum);

  QUERY-OPTIMIERUNG:
  ------------------
    - EXPLAIN ANALYZE verwenden
    - Selektive Indizes waehlen
    - Zusammengesetzte Indizes bei haeufigen Kombinationen
    - Vermeiden von SELECT *
    - Paginierung bei grossen Ergebnismengen

  PERFORMANCE-TIPPS:
  ------------------
    - Connection Pooling nutzen
    - Prepared Statements verwenden
    - N+1 Query Problem vermeiden
    - Batch-Operationen fuer Massendaten
    - Regelmaessige VACUUM/ANALYZE (PostgreSQL)

================================================================================
9. BACKUP UND RECOVERY
================================================================================

  BACKUP-STRATEGIEN:
  ------------------
    Vollbackup:       Komplette Datenbank
    Inkrementell:     Nur Aenderungen seit letztem Backup
    Differenziell:    Aenderungen seit letztem Vollbackup
    Point-in-Time:    Wiederherstellung zu beliebigem Zeitpunkt

  BACKUP-BEFEHLE:
  ---------------
    MySQL:      mysqldump -u user -p database > backup.sql
    PostgreSQL: pg_dump database > backup.sql
    MongoDB:    mongodump --db database --out /backup/

  REPLIKATION:
  ------------
    Master-Slave:  Ein Schreiber, mehrere Leser
    Master-Master: Mehrere Schreiber (Konfliktloesung noetig)
    Synchron:      Garantierte Konsistenz
    Asynchron:     Bessere Performance, moeglicher Datenverlust

================================================================================
10. BEST PRACTICES
================================================================================

  DESIGN:
  -------
    [+] Sinnvolle Namenskonventionen (snake_case oder CamelCase)
    [+] Konsistente Datentypen verwenden
    [+] Primaerschluessel immer definieren
    [+] Fremdschluessel-Constraints setzen
    [+] Sinnvolle Defaults und NOT NULL

  SICHERHEIT:
  -----------
    [+] Prepared Statements gegen SQL Injection
    [+] Minimale Berechtigungen (Principle of Least Privilege)
    [+] Passwoerter verschluesselt speichern
    [+] Regelmaessige Sicherheitsupdates
    [+] Netzwerkzugriff einschraenken

  WARTUNG:
  --------
    [+] Regelmaessige Backups mit Tests
    [+] Monitoring von Performance-Metriken
    [+] Logfiles ueberwachen
    [+] Kapazitaetsplanung
    [+] Dokumentation pflegen

================================================================================
11. WERKZEUGE UND ADMINISTRATION
================================================================================

  GUI-TOOLS:
  ----------
    - DBeaver (Universal, Open Source)
    - pgAdmin (PostgreSQL)
    - MySQL Workbench
    - MongoDB Compass
    - DataGrip (JetBrains, kommerziell)

  COMMAND-LINE:
  -------------
    - mysql/mariadb Client
    - psql (PostgreSQL)
    - mongosh (MongoDB)
    - redis-cli

  ORM-FRAMEWORKS:
  ---------------
    Java:       Hibernate, JPA
    Python:     SQLAlchemy, Django ORM
    JavaScript: Sequelize, Prisma, TypeORM
    PHP:        Doctrine, Eloquent

================================================================================
SIEHE AUCH
================================================================================

  wiki/webapps/datenbanken/
  wiki/java/jdbc/
  wiki/python/sqlalchemy/
  wiki/informatik/netzwerke/ (Datenbankverbindungen)
  wiki/informatik/it_sicherheit/ (SQL Injection)

================================================================================
AENDERUNGSHISTORIE
================================================================================

  2026-02-05  Vollstaendiger Artikel erstellt (vorher Stub)
  2026-01-24  Initiale Stub-Version

================================================================================
