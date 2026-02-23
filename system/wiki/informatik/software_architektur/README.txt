# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: Clean Architecture (R. Martin), Design Patterns (GoF), Martin Fowler's Blog

SOFTWARE-ARCHITEKTUR
====================

Stand: 2026-02-05

Software-Architektur beschreibt die fundamentale Organisation eines
Softwaresystems: die Strukturierung in Komponenten, deren Beziehungen
zueinander und die Prinzipien, die Design und Evolution leiten.

GRUNDPRINZIPIEN
===============

  SEPARATION OF CONCERNS
  ----------------------
  Trenne verschiedene Aspekte eines Systems voneinander.
    - Jede Komponente hat eine klare Verantwortlichkeit
    - Aenderungen in einem Bereich beeinflussen andere nicht
    - Erhoehte Wartbarkeit und Testbarkeit

  LOOSE COUPLING
  --------------
  Minimiere Abhaengigkeiten zwischen Komponenten.
    - Kommunikation ueber definierte Schnittstellen
    - Komponenten sind austauschbar
    - Aenderungen haben lokale Auswirkungen

  HIGH COHESION
  -------------
  Halte zusammengehoerige Funktionalitaet zusammen.
    - Komponenten sind fokussiert
    - Verwandte Operationen in einer Einheit
    - Klare, verstaendliche Struktur

  ABSTRACTION
  -----------
  Verstecke Implementierungsdetails hinter Schnittstellen.
    - Reduziert Komplexitaet
    - Ermoeglicht Austauschbarkeit
    - Foerdert Wiederverwendung

SOLID PRINZIPIEN
================

  S - SINGLE RESPONSIBILITY PRINCIPLE (SRP)
  -----------------------------------------
  Eine Klasse sollte nur einen Grund zur Aenderung haben.

  Schlecht:
    class UserService {
      void createUser() { ... }
      void sendEmail() { ... }
      void generateReport() { ... }
    }

  Besser:
    class UserService { void createUser() { ... } }
    class EmailService { void sendEmail() { ... } }
    class ReportService { void generateReport() { ... } }

  O - OPEN/CLOSED PRINCIPLE (OCP)
  -------------------------------
  Offen fuer Erweiterung, geschlossen fuer Modifikation.

  Schlecht:
    class DiscountCalculator {
      double calculate(String type, double price) {
        if (type.equals("seasonal")) return price * 0.9;
        if (type.equals("clearance")) return price * 0.5;
        return price;  // Muss fuer jeden neuen Typ geaendert werden
      }
    }

  Besser:
    interface DiscountStrategy {
      double apply(double price);
    }

    class SeasonalDiscount implements DiscountStrategy {
      double apply(double price) { return price * 0.9; }
    }

    class DiscountCalculator {
      double calculate(DiscountStrategy strategy, double price) {
        return strategy.apply(price);
      }
    }

  L - LISKOV SUBSTITUTION PRINCIPLE (LSP)
  ---------------------------------------
  Subtypen muessen ihre Basistypen ersetzen koennen.

  Schlecht:
    class Rectangle {
      void setWidth(int w) { width = w; }
      void setHeight(int h) { height = h; }
    }

    class Square extends Rectangle {
      void setWidth(int w) { width = w; height = w; }  // Bricht LSP
      void setHeight(int h) { width = h; height = h; }
    }

  Besser:
    interface Shape { int area(); }
    class Rectangle implements Shape { ... }
    class Square implements Shape { ... }

  I - INTERFACE SEGREGATION PRINCIPLE (ISP)
  -----------------------------------------
  Viele spezifische Interfaces sind besser als ein allgemeines.

  Schlecht:
    interface Worker {
      void work();
      void eat();
      void sleep();
    }

    class Robot implements Worker {
      void work() { ... }
      void eat() { /* Sinnlos fuer Robot */ }
      void sleep() { /* Sinnlos fuer Robot */ }
    }

  Besser:
    interface Workable { void work(); }
    interface Eatable { void eat(); }
    interface Sleepable { void sleep(); }

    class Robot implements Workable { void work() { ... } }
    class Human implements Workable, Eatable, Sleepable { ... }

  D - DEPENDENCY INVERSION PRINCIPLE (DIP)
  ----------------------------------------
  Abhaengigkeiten auf Abstraktionen, nicht auf Konkretionen.

  Schlecht:
    class OrderService {
      private MySQLDatabase db = new MySQLDatabase();
    }

  Besser:
    interface Database { void save(Order o); }

    class OrderService {
      private Database db;
      OrderService(Database db) { this.db = db; }
    }

    // Nutzung
    new OrderService(new MySQLDatabase());
    new OrderService(new PostgreSQLDatabase());
    new OrderService(new InMemoryDatabase());  // Fuer Tests

DESIGN PATTERNS
===============

  CREATIONAL PATTERNS (ERZEUGUNGSMUSTER)
  --------------------------------------

  Singleton:
    Genau eine Instanz einer Klasse.
    class Database {
      private static Database instance;
      private Database() {}
      public static synchronized Database getInstance() {
        if (instance == null) instance = new Database();
        return instance;
      }
    }
    Warnung: Erschwert Testing, vorsichtig einsetzen!

  Factory Method:
    Delegiert Objekterzeugung an Subklassen.
    interface Product { void use(); }
    abstract class Creator {
      abstract Product createProduct();
      void doSomething() {
        Product p = createProduct();
        p.use();
      }
    }

  Abstract Factory:
    Familie verwandter Objekte erzeugen.
    interface UIFactory {
      Button createButton();
      Checkbox createCheckbox();
    }
    class WindowsFactory implements UIFactory { ... }
    class MacFactory implements UIFactory { ... }

  Builder:
    Komplexe Objekte schrittweise aufbauen.
    class User {
      private User(Builder b) { ... }
      static class Builder {
        Builder name(String n) { this.name = n; return this; }
        Builder email(String e) { this.email = e; return this; }
        User build() { return new User(this); }
      }
    }
    User user = new User.Builder().name("Max").email("m@x.de").build();

  STRUCTURAL PATTERNS (STRUKTURMUSTER)
  ------------------------------------

  Adapter:
    Inkompatible Schnittstellen kompatibel machen.
    interface ModernPayment { void pay(double amount); }
    class LegacyPaymentSystem { void makePayment(int cents) { ... } }
    class PaymentAdapter implements ModernPayment {
      private LegacyPaymentSystem legacy;
      void pay(double amount) {
        legacy.makePayment((int)(amount * 100));
      }
    }

  Decorator:
    Dynamisch Funktionalitaet hinzufuegen.
    interface Coffee { double cost(); }
    class SimpleCoffee implements Coffee {
      double cost() { return 1.0; }
    }
    class MilkDecorator implements Coffee {
      private Coffee coffee;
      double cost() { return coffee.cost() + 0.5; }
    }

  Facade:
    Vereinfachte Schnittstelle zu komplexem Subsystem.
    class VideoConversionFacade {
      String convert(String filename, String format) {
        // Versteckt komplexe Logik
        VideoFile file = new VideoFile(filename);
        Codec codec = CodecFactory.getCodec(format);
        return new Converter().convert(file, codec);
      }
    }

  Proxy:
    Stellvertreter fuer ein anderes Objekt.
    interface Image { void display(); }
    class ProxyImage implements Image {
      private RealImage realImage;
      void display() {
        if (realImage == null) realImage = new RealImage(); // Lazy Load
        realImage.display();
      }
    }

  BEHAVIORAL PATTERNS (VERHALTENSMUSTER)
  --------------------------------------

  Observer:
    Automatische Benachrichtigung bei Zustandsaenderungen.
    interface Observer { void update(String event); }
    class EventManager {
      private List<Observer> observers = new ArrayList<>();
      void subscribe(Observer o) { observers.add(o); }
      void notify(String event) {
        observers.forEach(o -> o.update(event));
      }
    }

  Strategy:
    Algorithmus zur Laufzeit austauschen.
    interface SortStrategy { void sort(int[] array); }
    class QuickSort implements SortStrategy { ... }
    class MergeSort implements SortStrategy { ... }
    class Sorter {
      private SortStrategy strategy;
      void setStrategy(SortStrategy s) { strategy = s; }
      void sort(int[] arr) { strategy.sort(arr); }
    }

  Command:
    Operationen als Objekte kapseln.
    interface Command { void execute(); void undo(); }
    class TypeCommand implements Command {
      private Editor editor;
      private String text;
      void execute() { editor.insert(text); }
      void undo() { editor.delete(text.length()); }
    }

  State:
    Verhalten abhaengig vom Zustand aendern.
    interface State { void handle(Context ctx); }
    class Context {
      private State state;
      void setState(State s) { state = s; }
      void request() { state.handle(this); }
    }

ARCHITEKTURMUSTER
=================

  MONOLITHISCHE ARCHITEKTUR
  -------------------------
  Alles in einer Anwendung.

  Struktur:
    monolith/
    ├── src/
    │   ├── controllers/
    │   ├── services/
    │   ├── models/
    │   └── utils/
    ├── tests/
    └── database/

  Vorteile:
    + Einfach zu entwickeln und deployen
    + Einfaches Debugging
    + Keine Netzwerk-Latenz intern
    + Transaktionen einfach

  Nachteile:
    - Skaliert nur als Ganzes
    - Lange Build-Zeiten bei Wachstum
    - Eine Aenderung erfordert neues Deployment
    - Technologie-Lock-in

  MICROSERVICES
  -------------
  Kleine, unabhaengige Services.

  Struktur:
    system/
    ├── user-service/
    │   ├── src/
    │   ├── Dockerfile
    │   └── api.yaml
    ├── order-service/
    ├── payment-service/
    ├── notification-service/
    └── api-gateway/

  Eigenschaften:
    - Eigene Datenbank pro Service
    - Kommunikation via HTTP/gRPC/Events
    - Unabhaengiges Deployment
    - Polyglot (verschiedene Sprachen moeglich)

  Vorteile:
    + Unabhaengige Skalierung
    + Team-Autonomie
    + Technologie-Flexibilitaet
    + Fehler sind isoliert

  Nachteile:
    - Komplexe Infrastruktur
    - Netzwerk-Latenz und Ausfaelle
    - Distributed Transactions schwierig
    - Debugging komplexer

  Kommunikationsmuster:
    Synchron     REST, gRPC (Request/Response)
    Asynchron    Message Queues (Kafka, RabbitMQ)

  SERVERLESS
  ----------
  Funktionen ohne Serververwaltung.

  Beispiel (AWS Lambda):
    exports.handler = async (event) => {
      const userId = event.pathParameters.id;
      const user = await db.getUser(userId);
      return {
        statusCode: 200,
        body: JSON.stringify(user)
      };
    };

  Vorteile:
    + Zahle nur fuer Ausfuehrung
    + Automatische Skalierung
    + Keine Infrastruktur-Wartung

  Nachteile:
    - Cold Starts
    - Vendor Lock-in
    - Timeout-Limits
    - Debugging schwieriger

  EVENT-DRIVEN ARCHITECTURE
  -------------------------
  Kommunikation ueber Events.

  Komponenten:
    Producer       Erzeugt Events
    Broker         Verteilt Events (Kafka, RabbitMQ)
    Consumer       Verarbeitet Events

  Event Sourcing:
    - Speichere alle Ereignisse, nicht nur aktuellen Zustand
    - Zustand aus Events rekonstruierbar
    - Vollstaendige Audit-Historie

  CQRS (Command Query Responsibility Segregation):
    - Trenne Lese- und Schreiboperationen
    - Optimierte Modelle fuer jeden Zweck
    - Oft mit Event Sourcing kombiniert

CLEAN ARCHITECTURE
==================

  SCHICHTEN (VON INNEN NACH AUSSEN)
  ---------------------------------

        ┌─────────────────────────────────┐
        │         Frameworks & Drivers     │  Web, DB, UI
        │   ┌─────────────────────────┐   │
        │   │   Interface Adapters     │   │  Controllers, Gateways
        │   │   ┌─────────────────┐   │   │
        │   │   │  Application     │   │   │  Use Cases
        │   │   │   ┌─────────┐   │   │   │
        │   │   │   │Entities │   │   │   │  Domain
        │   │   │   └─────────┘   │   │   │
        │   │   └─────────────────┘   │   │
        │   └─────────────────────────┘   │
        └─────────────────────────────────┘

  Entities (Domain):
    - Geschaeftslogik und Regeln
    - Keine Abhaengigkeiten nach aussen
    - Kern der Anwendung

  Application (Use Cases):
    - Anwendungsspezifische Geschaeftsregeln
    - Orchestriert Entities
    - Definiert Ports (Interfaces)

  Interface Adapters:
    - Konvertiert zwischen Formaten
    - Controller, Presenter, Gateways
    - Implementiert Ports

  Frameworks & Drivers:
    - Externe Bibliotheken
    - Datenbank, Web-Framework
    - Austauschbar

  DEPENDENCY RULE
  ---------------
  Abhaengigkeiten zeigen nur nach INNEN.
    - Entities kennen nichts anderes
    - Use Cases kennen nur Entities
    - Adapters kennen Use Cases
    - Frameworks kennen alles

  BEISPIELSTRUKTUR
  ----------------
    src/
    ├── domain/                 # Entities
    │   ├── entities/
    │   │   ├── User.ts
    │   │   └── Order.ts
    │   └── value-objects/
    │       └── Money.ts
    │
    ├── application/            # Use Cases
    │   ├── use-cases/
    │   │   ├── CreateOrder.ts
    │   │   └── GetUser.ts
    │   └── ports/
    │       ├── UserRepository.ts      # Interface
    │       └── PaymentGateway.ts      # Interface
    │
    ├── infrastructure/         # Adapters & Drivers
    │   ├── persistence/
    │   │   ├── PostgresUserRepo.ts   # Implements UserRepository
    │   │   └── migrations/
    │   ├── http/
    │   │   └── controllers/
    │   └── external/
    │       └── StripePayment.ts      # Implements PaymentGateway
    │
    └── main/                   # Composition Root
        └── index.ts

HEXAGONAL ARCHITECTURE (PORTS & ADAPTERS)
=========================================

  Kern-Idee:
    - Anwendung ist unabhaengig von aeusserer Welt
    - Kommunikation nur ueber definierte Ports
    - Adapter verbinden Ports mit Aussenwelt

  Struktur:
          Driving Adapters              Driven Adapters
    (Primary/Input)              (Secondary/Output)
           │                              │
           ▼                              ▼
    ┌──────────┐                   ┌──────────┐
    │   REST   │                   │ Database │
    │   CLI    │  ──▶  PORTS  ──▶  │   API    │
    │   GUI    │                   │  Email   │
    └──────────┘                   └──────────┘
                    ▲     ▲
                    │     │
              ┌─────────────────┐
              │  APPLICATION    │
              │     CORE        │
              └─────────────────┘

API DESIGN
==========

  REST PRINZIPIEN
  ---------------
    - Ressourcenbasiert (Substantive, nicht Verben)
    - HTTP-Methoden fuer Aktionen
    - Statuslose Kommunikation
    - HATEOAS (Hypermedia)

  HTTP Methoden:
    GET     /users           Liste aller User
    GET     /users/123       Ein User
    POST    /users           User erstellen
    PUT     /users/123       User komplett ersetzen
    PATCH   /users/123       User teilweise aendern
    DELETE  /users/123       User loeschen

  Statuscodes:
    200 OK                    Erfolg
    201 Created               Ressource erstellt
    204 No Content            Erfolg ohne Body
    400 Bad Request           Clientfehler
    401 Unauthorized          Nicht authentifiziert
    403 Forbidden             Nicht autorisiert
    404 Not Found             Nicht gefunden
    422 Unprocessable Entity  Validierungsfehler
    500 Internal Server Error Serverfehler

  GRAPHQL
  -------
  Query-Sprache fuer APIs.

    query {
      user(id: "123") {
        name
        email
        orders {
          id
          total
        }
      }
    }

  Vorteile:
    + Nur angeforderte Daten
    + Ein Endpoint
    + Starke Typisierung
    + Selbstdokumentierend

  gRPC
  ----
  Hochperformantes RPC-Framework.

  Protocol Buffers:
    service UserService {
      rpc GetUser (UserRequest) returns (User);
      rpc ListUsers (Empty) returns (stream User);
    }

  Vorteile:
    + Sehr schnell (Binary)
    + Streaming-Support
    + Code-Generierung

TESTING-STRATEGIEN
==================

  TEST-PYRAMIDE
  -------------
           /\
          /  \      E2E Tests (wenige)
         /----\
        /      \    Integration Tests
       /--------\
      /          \  Unit Tests (viele)
     /------------\

  Unit Tests:
    - Testen einzelne Funktionen/Klassen
    - Isoliert (Mocking)
    - Schnell
    - Viele

  Integration Tests:
    - Testen Zusammenspiel von Komponenten
    - Mit echten Abhaengigkeiten
    - Langsamer

  E2E Tests:
    - Testen komplettes System
    - Aus Nutzerperspektive
    - Teuer, wenige

DOKUMENTATION
=============

  ARCHITEKTUR-DOKUMENTATION
  -------------------------
    - Architekturentscheidungen (ADRs)
    - Systemuebersicht (C4-Modell)
    - Sequenzdiagramme
    - Deployment-Diagramme

  ADR (Architecture Decision Record):
    # ADR-001: Verwendung von PostgreSQL

    ## Status: Accepted

    ## Context
    Wir brauchen eine Datenbank fuer strukturierte Daten.

    ## Decision
    Wir verwenden PostgreSQL.

    ## Consequences
    + Bewährte, stabile Technologie
    + Team hat Erfahrung
    - Skalierung komplexer als NoSQL

BEST PRACTICES
==============

  ALLGEMEIN
  ---------
    - Starte einfach, refaktoriere bei Bedarf
    - YAGNI (You Aren't Gonna Need It)
    - DRY (Don't Repeat Yourself)
    - KISS (Keep It Simple, Stupid)

  TEAMS
  -----
    - Conway's Law beachten
    - Architektur an Team-Struktur anpassen
    - Klare Schnittstellen zwischen Teams

  EVOLUTION
  ---------
    - Architektur ist nicht statisch
    - Regelmaessige Reviews
    - Technische Schulden tracken

SIEHE AUCH
==========
  wiki/informatik/softwareentwicklung/README.txt
  wiki/informatik/programmierung/README.txt
  wiki/webapps/README.txt
  wiki/java/README.txt
