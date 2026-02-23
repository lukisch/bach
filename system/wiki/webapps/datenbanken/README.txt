================================================================================
WEB-APPS DATENBANKEN - VOLLSTAENDIGER LEITFADEN
================================================================================

# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: PostgreSQL Docs, MongoDB Manual, Redis Docs, Prisma Docs

Stand: 2026-02-05
Status: VOLLSTAENDIG

================================================================================
INHALTSVERZEICHNIS
================================================================================
  1. Einfuehrung
  2. Relationale Datenbanken (SQL)
  3. NoSQL-Datenbanken
  4. ORM und Query Builder
  5. Migrationen
  6. Connection Pooling
  7. Indexierung und Performance
  8. Backups und Recovery
  9. Sicherheit
  10. Best Practices
  11. Code-Beispiele
  12. Siehe auch

================================================================================
1. EINFUEHRUNG
================================================================================

Die Wahl der richtigen Datenbank ist entscheidend fuer den Erfolg einer
Webanwendung. Faktoren wie Datenstruktur, Skalierbarkeit, Konsistenz-
anforderungen und Teamexpertise beeinflussen diese Entscheidung.

HAUPTKATEGORIEN
---------------
  Relational (SQL):
    - Strukturierte Daten mit Beziehungen
    - ACID-Garantien
    - SQL als Abfragesprache

  NoSQL:
    - Document Stores (MongoDB)
    - Key-Value Stores (Redis)
    - Column Stores (Cassandra)
    - Graph Databases (Neo4j)

CAP-THEOREM
-----------
  Verteilte Systeme koennen maximal zwei von drei Eigenschaften garantieren:
    - Consistency: Alle Knoten sehen gleiche Daten
    - Availability: System antwortet immer
    - Partition Tolerance: System funktioniert trotz Netzwerkpartition

  CP: PostgreSQL, MongoDB (mit Replica Set)
  AP: Cassandra, CouchDB
  CA: Traditionelle RDBMS (nicht verteilt)

================================================================================
2. RELATIONALE DATENBANKEN (SQL)
================================================================================

POSTGRESQL
----------
  Der fortschrittlichste Open-Source SQL-Server.

  Staerken:
    - JSONB-Unterstuetzung (NoSQL-Features)
    - Erweiterungen (PostGIS, pg_trgm, etc.)
    - Volltextsuche integriert
    - Window Functions
    - CTEs (Common Table Expressions)
    - Ausgereifte Replikation

  JSONB-Beispiel:
    CREATE TABLE products (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      attributes JSONB DEFAULT '{}'
    );

    -- JSONB abfragen
    SELECT * FROM products
    WHERE attributes->>'color' = 'red';

    -- JSONB-Index
    CREATE INDEX idx_attributes ON products
    USING GIN (attributes);

  Array-Typen:
    CREATE TABLE posts (
      id SERIAL PRIMARY KEY,
      title TEXT,
      tags TEXT[] DEFAULT '{}'
    );

    SELECT * FROM posts WHERE 'javascript' = ANY(tags);

MYSQL / MARIADB
---------------
  Weit verbreitet und gut dokumentiert.

  Staerken:
    - Einfache Administration
    - Grosse Community
    - Gute Performance fuer Lesezugriffe
    - JSON-Unterstuetzung (ab MySQL 5.7)

  Storage Engines:
    - InnoDB: Standard, ACID, Foreign Keys
    - MyISAM: Schnell fuer Lesen, keine Transaktionen

  Konfiguration fuer Web-Apps:
    [mysqld]
    innodb_buffer_pool_size = 1G
    max_connections = 200
    query_cache_type = 1
    query_cache_size = 64M

SQLITE
------
  Serverlose, eingebettete Datenbank.

  Einsatzgebiete:
    - Entwicklung und Testing
    - Mobile Apps
    - Desktop-Anwendungen
    - Kleine bis mittlere Websites
    - Edge Computing

  Einschraenkungen:
    - Ein Schreiber zur Zeit
    - Keine Benutzerrechte
    - Begrenzte Skalierbarkeit

  WAL-Modus fuer bessere Concurrency:
    PRAGMA journal_mode=WAL;
    PRAGMA synchronous=NORMAL;

================================================================================
3. NOSQL-DATENBANKEN
================================================================================

MONGODB (Document Store)
------------------------
  Speichert Daten als JSON-aehnliche Dokumente (BSON).

  Staerken:
    - Flexible Schemas
    - Horizontale Skalierung (Sharding)
    - Aggregation Pipeline
    - Change Streams fuer Echtzeit

  Datenmodell:
    {
      "_id": ObjectId("507f1f77bcf86cd799439011"),
      "name": "Max Mustermann",
      "email": "max@example.com",
      "address": {
        "street": "Musterstr. 1",
        "city": "Berlin"
      },
      "orders": [
        { "product": "Laptop", "price": 999 },
        { "product": "Mouse", "price": 29 }
      ]
    }

  Queries:
    // Finden
    db.users.find({ "address.city": "Berlin" });

    // Aggregation
    db.orders.aggregate([
      { $match: { status: "completed" } },
      { $group: {
          _id: "$customerId",
          total: { $sum: "$amount" }
      }},
      { $sort: { total: -1 } }
    ]);

  Indexierung:
    db.users.createIndex({ email: 1 }, { unique: true });
    db.users.createIndex({ "address.city": 1, createdAt: -1 });
    db.products.createIndex({ name: "text", description: "text" });

REDIS (Key-Value Store)
-----------------------
  In-Memory Datenbank fuer Hochgeschwindigkeitszugriffe.

  Anwendungsfaelle:
    - Caching
    - Session-Speicherung
    - Rate Limiting
    - Queues (mit Lists)
    - Pub/Sub
    - Leaderboards (mit Sorted Sets)

  Datenstrukturen:
    # Strings
    SET user:123:name "Max"
    GET user:123:name
    SETEX session:abc 3600 "user_data"  # Mit TTL

    # Hashes
    HSET user:123 name "Max" email "max@example.com"
    HGETALL user:123

    # Lists (Queue)
    LPUSH jobs:queue "job1"
    RPOP jobs:queue

    # Sets
    SADD user:123:tags "premium" "verified"
    SISMEMBER user:123:tags "premium"

    # Sorted Sets (Leaderboard)
    ZADD leaderboard 100 "user:1" 85 "user:2"
    ZREVRANGE leaderboard 0 9 WITHSCORES

  Persistenz:
    - RDB: Snapshots in Intervallen
    - AOF: Append-Only File (jede Operation)
    - Hybrid: RDB + AOF fuer beste Haltbarkeit

CASSANDRA (Column Store)
------------------------
  Fuer massive Schreiblast und globale Verteilung.

  Staerken:
    - Lineare Skalierbarkeit
    - Keine Single Point of Failure
    - Multi-Datacenter Replikation
    - Tunable Consistency

  Datenmodell:
    CREATE KEYSPACE myapp
    WITH replication = {
      'class': 'NetworkTopologyStrategy',
      'dc1': 3, 'dc2': 3
    };

    CREATE TABLE users (
      user_id UUID PRIMARY KEY,
      name TEXT,
      email TEXT,
      created_at TIMESTAMP
    );

================================================================================
4. ORM UND QUERY BUILDER
================================================================================

PRISMA (JavaScript/TypeScript)
------------------------------
  Moderner ORM mit Type-Safety.

  Schema (schema.prisma):
    generator client {
      provider = "prisma-client-js"
    }

    datasource db {
      provider = "postgresql"
      url      = env("DATABASE_URL")
    }

    model User {
      id        Int      @id @default(autoincrement())
      email     String   @unique
      name      String?
      posts     Post[]
      createdAt DateTime @default(now())
    }

    model Post {
      id        Int      @id @default(autoincrement())
      title     String
      content   String?
      published Boolean  @default(false)
      author    User     @relation(fields: [authorId], references: [id])
      authorId  Int
    }

  Queries:
    // Erstellen
    const user = await prisma.user.create({
      data: {
        email: 'max@example.com',
        name: 'Max',
        posts: {
          create: { title: 'Erster Post' }
        }
      },
      include: { posts: true }
    });

    // Abfragen mit Relationen
    const users = await prisma.user.findMany({
      where: { email: { contains: '@example.com' } },
      include: {
        posts: {
          where: { published: true }
        }
      }
    });

SQLALCHEMY (Python)
-------------------
  Das Standard-ORM fuer Python.

  Model Definition:
    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import relationship, declarative_base

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        email = Column(String(255), unique=True, nullable=False)
        name = Column(String(255))
        posts = relationship('Post', back_populates='author')

    class Post(Base):
        __tablename__ = 'posts'

        id = Column(Integer, primary_key=True)
        title = Column(String(255), nullable=False)
        author_id = Column(Integer, ForeignKey('users.id'))
        author = relationship('User', back_populates='posts')

  Queries:
    # Session erstellen
    from sqlalchemy.orm import Session

    with Session(engine) as session:
        # Erstellen
        user = User(email='max@example.com', name='Max')
        session.add(user)
        session.commit()

        # Abfragen
        users = session.query(User).filter(
            User.email.like('%@example.com')
        ).all()

================================================================================
5. MIGRATIONEN
================================================================================

Schema-Aenderungen versioniert und reproduzierbar verwalten.

PRISMA MIGRATE
--------------
  # Migration erstellen
  npx prisma migrate dev --name add_user_role

  # In Produktion anwenden
  npx prisma migrate deploy

ALEMBIC (Python/SQLAlchemy)
---------------------------
  # alembic/versions/001_add_users_table.py
  def upgrade():
      op.create_table(
          'users',
          sa.Column('id', sa.Integer(), primary_key=True),
          sa.Column('email', sa.String(255), unique=True),
          sa.Column('created_at', sa.DateTime(), default=sa.func.now())
      )

  def downgrade():
      op.drop_table('users')

  # Ausfuehren
  alembic upgrade head
  alembic downgrade -1

BEST PRACTICES FUER MIGRATIONEN
-------------------------------
  1. Immer Down-Migration schreiben
  2. Kleine, atomare Aenderungen
  3. Daten-Migrationen separat von Schema-Aenderungen
  4. In Produktion: Erst additive Aenderungen, dann Daten migrieren
  5. Nie Migration-Dateien aendern die bereits deployed wurden
  6. Migrationen in CI/CD testen

================================================================================
6. CONNECTION POOLING
================================================================================

Verbindungen wiederverwenden statt neu aufzubauen.

WARUM POOLING?
--------------
  - Verbindungsaufbau ist teuer (TCP, TLS, Auth)
  - Datenbanken haben Verbindungslimits
  - Bessere Ressourcennutzung

PGBOUNCER (PostgreSQL)
----------------------
  [databases]
  mydb = host=localhost port=5432 dbname=mydb

  [pgbouncer]
  listen_addr = 127.0.0.1
  listen_port = 6432
  auth_type = md5
  auth_file = /etc/pgbouncer/userlist.txt
  pool_mode = transaction
  max_client_conn = 1000
  default_pool_size = 20

  Pool-Modi:
    - session: Eine Verbindung pro Client-Session
    - transaction: Verbindung wird nach Transaktion freigegeben
    - statement: Verbindung wird nach Statement freigegeben

PRISMA CONNECTION POOL
----------------------
  datasource db {
    provider = "postgresql"
    url      = env("DATABASE_URL")
  }

  // URL mit Pool-Einstellungen
  DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=10"

================================================================================
7. INDEXIERUNG UND PERFORMANCE
================================================================================

INDEX-TYPEN
-----------
  B-Tree (Standard):
    - Gleichheit und Bereichsabfragen
    - Sortierung
    CREATE INDEX idx_users_email ON users(email);

  Hash:
    - Nur Gleichheitsabfragen
    - Schneller als B-Tree fuer =
    CREATE INDEX idx_users_id ON users USING hash(id);

  GIN (Generalized Inverted Index):
    - Arrays, JSONB, Volltext
    CREATE INDEX idx_posts_tags ON posts USING GIN(tags);

  GiST:
    - Geometrische Daten, Ranges
    CREATE INDEX idx_events_range ON events USING GIST(date_range);

QUERY-OPTIMIERUNG
-----------------
  EXPLAIN ANALYZE:
    EXPLAIN ANALYZE
    SELECT * FROM users
    WHERE email LIKE 'max%'
    ORDER BY created_at DESC
    LIMIT 10;

  Haeufige Probleme:
    - Seq Scan statt Index Scan
    - Fehlende Indizes
    - N+1 Queries
    - Zu viele Spalten selektiert
    - Fehlende LIMIT

CACHING-STRATEGIEN
------------------
  Cache-Aside:
    data = cache.get(key)
    if not data:
        data = db.query(...)
        cache.set(key, data, ttl=300)
    return data

  Write-Through:
    db.insert(data)
    cache.set(key, data)

  Cache Invalidation:
    - TTL-basiert
    - Event-basiert (bei DB-Aenderung)
    - Tag-basiert (verwandte Daten zusammen)

================================================================================
8. BACKUPS UND RECOVERY
================================================================================

POSTGRESQL
----------
  # Logisches Backup
  pg_dump -Fc mydb > backup.dump
  pg_restore -d mydb backup.dump

  # Physisches Backup (Point-in-Time Recovery)
  pg_basebackup -D /backup/base -Fp -Xs -P

  # WAL-Archivierung
  archive_mode = on
  archive_command = 'cp %p /archive/%f'

MONGODB
-------
  # Dump
  mongodump --db=mydb --out=/backup/

  # Restore
  mongorestore --db=mydb /backup/mydb/

  # Continuous Backup (Atlas oder Ops Manager)

BACKUP-STRATEGIEN
-----------------
  3-2-1 Regel:
    - 3 Kopien der Daten
    - 2 verschiedene Medien
    - 1 Offsite-Backup

  Automatisierung:
    - Cronjobs fuer regelmaessige Backups
    - Retention Policy definieren
    - Restore regelmaessig testen!

================================================================================
9. SICHERHEIT
================================================================================

GRUNDREGELN
-----------
  1. Prepared Statements / Parameterized Queries (SQL Injection)
  2. Principle of Least Privilege (minimale Rechte)
  3. Verschluesselung (TLS fuer Verbindung, Encryption at Rest)
  4. Keine Klartext-Passwoerter speichern
  5. Audit-Logging aktivieren
  6. Netzwerk-Segmentierung (DB nicht oeffentlich)

SQL INJECTION VERHINDERN
------------------------
  FALSCH:
    query = f"SELECT * FROM users WHERE email = '{email}'"

  RICHTIG:
    cursor.execute(
      "SELECT * FROM users WHERE email = %s",
      (email,)
    )

BENUTZERRECHTE (PostgreSQL)
---------------------------
  -- Read-Only User
  CREATE USER readonly WITH PASSWORD 'secret';
  GRANT CONNECT ON DATABASE mydb TO readonly;
  GRANT USAGE ON SCHEMA public TO readonly;
  GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;

  -- App User (CRUD)
  CREATE USER appuser WITH PASSWORD 'secret';
  GRANT CONNECT ON DATABASE mydb TO appuser;
  GRANT USAGE ON SCHEMA public TO appuser;
  GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO appuser;

================================================================================
10. BEST PRACTICES
================================================================================

  1. Eine Datenbank pro Anwendung (Isolation)
  2. Umgebungsvariablen fuer Credentials
  3. Connection Pooling immer verwenden
  4. Migrationen versionieren
  5. Indizes fuer haeufige Queries
  6. Monitoring einrichten (slow queries, connections)
  7. Backups testen (nicht nur erstellen!)
  8. Read Replicas fuer Skalierung
  9. Soft Deletes statt Hard Deletes (deleted_at)
  10. Timestamps automatisch setzen (created_at, updated_at)

================================================================================
11. CODE-BEISPIELE
================================================================================

PRISMA SETUP (TypeScript)
-------------------------
  // prisma/schema.prisma siehe oben

  // src/db.ts
  import { PrismaClient } from '@prisma/client';

  const prisma = new PrismaClient({
    log: ['query', 'error', 'warn'],
  });

  export default prisma;

  // src/users.ts
  import prisma from './db';

  export async function createUser(email: string, name: string) {
    return prisma.user.create({
      data: { email, name },
    });
  }

  export async function getUserWithPosts(id: number) {
    return prisma.user.findUnique({
      where: { id },
      include: {
        posts: {
          where: { published: true },
          orderBy: { createdAt: 'desc' },
        },
      },
    });
  }

================================================================================
SIEHE AUCH
================================================================================

  BACH Wiki:
    wiki/informatik/datenbanken/
    wiki/webapps/api/
    wiki/python/api/
    wiki/informatik/software_architektur/

  Externe Ressourcen:
    https://www.postgresql.org/docs/
    https://www.mongodb.com/docs/
    https://redis.io/documentation
    https://www.prisma.io/docs/

================================================================================
