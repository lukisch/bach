================================================================================
                         WEB-APPS BACKEND
================================================================================

Portabilitaet:      UNIVERSAL
Zuletzt validiert:  2026-02-05
Naechste Pruefung:  2027-02-05
Quellen:            Offizielle Framework-Dokumentationen, OWASP Guidelines,
                    Twelve-Factor App Methodology, Cloud-Native Patterns

Stand: 2026-02-05

================================================================================
                         EINFUEHRUNG
================================================================================

Backend-Entwicklung umfasst die serverseitige Logik von Webanwendungen.
Das Backend verarbeitet Anfragen, kommuniziert mit Datenbanken, fuehrt
Geschaeftslogik aus und liefert Daten an das Frontend.

Kernaufgaben des Backends:
  - Request/Response-Handling
  - Authentifizierung und Autorisierung
  - Datenpersistenz und -abruf
  - Business-Logik
  - API-Bereitstellung
  - Sicherheit und Validierung

================================================================================
                         PROGRAMMIERSPRACHEN
================================================================================

NODE.JS (JAVASCRIPT)
--------------------
JavaScript auf dem Server mit V8 Engine.

  Eigenschaften:
    - Event-driven, non-blocking I/O
    - Single-threaded mit Event Loop
    - Riesiges npm-Oekosystem
    - Ideal fuer I/O-intensive Anwendungen

  Express.js (minimalistisch):
    const express = require('express');
    const app = express();

    app.use(express.json());

    app.get('/api/users', async (req, res) => {
      try {
        const users = await User.findAll();
        res.json(users);
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    app.listen(3000, () => console.log('Server auf Port 3000'));

  Fastify (performant):
    - Schema-basierte Validierung
    - Logging integriert
    - Plugin-Architektur
    - Schneller als Express

  NestJS (strukturiert):
    - TypeScript-first
    - Angular-inspirierte Architektur
    - Dependency Injection
    - Modularer Aufbau

PYTHON
------
Vielseitig mit exzellenter Lesbarkeit.

  Django (Full-Stack):
    # models.py
    class Article(models.Model):
        title = models.CharField(max_length=200)
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

    # views.py
    from django.shortcuts import render
    from .models import Article

    def article_list(request):
        articles = Article.objects.all()
        return render(request, 'articles/list.html', {'articles': articles})

    Eigenschaften:
      - ORM integriert
      - Admin-Interface automatisch
      - Batteries included
      - MTV-Architektur (Model-Template-View)

  FastAPI (modern, async):
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel

    app = FastAPI()

    class User(BaseModel):
        name: str
        email: str
        age: int | None = None

    @app.post("/users/", response_model=User)
    async def create_user(user: User):
        # Logik
        return user

    Eigenschaften:
      - Automatische OpenAPI-Dokumentation
      - Pydantic-Validierung
      - Async/await nativ
      - Sehr performant

  Flask (minimalistisch):
    - Microframework
    - Flexibel erweiterbar
    - Blueprints fuer Modularitaet

JAVA
----
Enterprise-Standard mit robustem Oekosystem.

  Spring Boot:
    @RestController
    @RequestMapping("/api/users")
    public class UserController {

        @Autowired
        private UserService userService;

        @GetMapping("/{id}")
        public ResponseEntity<User> getUser(@PathVariable Long id) {
            return userService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
        }

        @PostMapping
        public ResponseEntity<User> createUser(@Valid @RequestBody User user) {
            User saved = userService.save(user);
            return ResponseEntity.status(HttpStatus.CREATED).body(saved);
        }
    }

    Eigenschaften:
      - Dependency Injection
      - Auto-Configuration
      - Production-ready
      - Umfangreiches Security-Framework

GO (GOLANG)
-----------
Kompiliert, schnell, einfach.

  Standard Library:
    package main

    import (
        "encoding/json"
        "net/http"
    )

    func main() {
        http.HandleFunc("/api/health", healthHandler)
        http.ListenAndServe(":8080", nil)
    }

    func healthHandler(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
    }

  Frameworks:
    - Gin (performant, Express-aehnlich)
    - Echo (minimalistisch)
    - Fiber (Express-inspiriert)

  Eigenschaften:
    - Kompiliert zu Single Binary
    - Goroutines fuer Concurrency
    - Schnelle Kompilierung
    - Ideal fuer Microservices

RUST
----
Sicher und extrem performant.

  Actix-web:
    use actix_web::{web, App, HttpServer, HttpResponse};

    async fn hello() -> HttpResponse {
        HttpResponse::Ok().body("Hallo Welt!")
    }

    #[actix_web::main]
    async fn main() -> std::io::Result<()> {
        HttpServer::new(|| {
            App::new().route("/", web::get().to(hello))
        })
        .bind("127.0.0.1:8080")?
        .run()
        .await
    }

  Eigenschaften:
    - Memory Safety ohne Garbage Collector
    - Zero-Cost Abstractions
    - Exzellente Performance
    - Steile Lernkurve

PHP
---
Weit verbreitet, besonders im Web-Hosting.

  Laravel:
    - Eloquent ORM
    - Blade Templates
    - Artisan CLI
    - Queue-System

================================================================================
                         API-ARCHITEKTUREN
================================================================================

REST (REPRESENTATIONAL STATE TRANSFER)
--------------------------------------
Ressourcen-orientierter Architekturstil.

  Prinzipien:
    - Stateless (kein Server-State zwischen Requests)
    - Einheitliche Schnittstelle
    - Ressourcen durch URIs identifiziert
    - HTTP-Methoden (GET, POST, PUT, PATCH, DELETE)

  HTTP-Methoden:
    GET     /users          Alle Benutzer abrufen
    GET     /users/123      Benutzer 123 abrufen
    POST    /users          Neuen Benutzer erstellen
    PUT     /users/123      Benutzer 123 vollstaendig ersetzen
    PATCH   /users/123      Benutzer 123 teilweise aktualisieren
    DELETE  /users/123      Benutzer 123 loeschen

  HTTP-Statuscodes:
    2xx Erfolg:
      200 OK
      201 Created
      204 No Content

    4xx Client-Fehler:
      400 Bad Request
      401 Unauthorized
      403 Forbidden
      404 Not Found
      422 Unprocessable Entity

    5xx Server-Fehler:
      500 Internal Server Error
      502 Bad Gateway
      503 Service Unavailable

  Best Practices:
    - Versionierung: /api/v1/users
    - Pagination: ?page=2&limit=20
    - Filterung: ?status=active&role=admin
    - HATEOAS fuer Discoverability

GRAPHQL
-------
Flexible Query-Sprache von Meta.

  Schema-Definition:
    type User {
      id: ID!
      name: String!
      email: String!
      posts: [Post!]!
    }

    type Query {
      user(id: ID!): User
      users: [User!]!
    }

    type Mutation {
      createUser(name: String!, email: String!): User!
    }

  Query-Beispiel:
    query {
      user(id: "123") {
        name
        email
        posts {
          title
        }
      }
    }

  Vorteile:
    - Client bestimmt Datenstruktur
    - Kein Over-/Underfetching
    - Starke Typisierung
    - Introspection

  Nachteile:
    - Komplexeres Caching
    - N+1-Problem bei Relations
    - Hoehere Einstiegshuerde

GRPC
----
High-performance RPC Framework von Google.

  Eigenschaften:
    - Protocol Buffers (binäres Format)
    - HTTP/2 mit Streaming
    - Code-Generierung
    - Ideal fuer Microservices

================================================================================
                         AUTHENTIFIZIERUNG UND AUTORISIERUNG
================================================================================

SESSION-BASIERT
---------------
Klassischer Ansatz mit Server-State.

  Ablauf:
    1. Login: Server erstellt Session
    2. Cookie mit Session-ID an Client
    3. Jeder Request: Cookie wird mitgesendet
    4. Server validiert Session-ID

  Vorteile:
    - Einfach zu implementieren
    - Session kann serverseitig invalidiert werden

  Nachteile:
    - Server-State erforderlich
    - Skalierung komplexer (Sticky Sessions oder Redis)

JWT (JSON WEB TOKEN)
--------------------
Stateless Token-basierte Authentifizierung.

  Struktur:
    Header.Payload.Signature

    Header:   {"alg": "HS256", "typ": "JWT"}
    Payload:  {"sub": "123", "name": "Max", "exp": 1735689600}
    Signature: HMACSHA256(base64(header) + "." + base64(payload), secret)

  Ablauf:
    1. Login: Server generiert JWT
    2. Client speichert Token (localStorage, Cookie)
    3. Jeder Request: Token im Authorization Header
    4. Server validiert Signatur

  Best Practices:
    - Kurze Ablaufzeit (15 Min - 1 Stunde)
    - Refresh Tokens fuer Erneuerung
    - Keine sensiblen Daten im Payload
    - httpOnly Cookie bevorzugen

OAUTH 2.0
---------
Autorisierungs-Framework fuer Drittanbieter.

  Flows:
    Authorization Code  Serverseitige Apps (sicherster Flow)
    PKCE               Single Page Apps, Mobile
    Client Credentials Server-zu-Server

  Tokens:
    Access Token   Kurzlebig, fuer API-Zugriff
    Refresh Token  Langlebig, fuer Token-Erneuerung

================================================================================
                         SERVER-INFRASTRUKTUR
================================================================================

WEB SERVER
----------
  Nginx:
    - Reverse Proxy
    - Load Balancing
    - Static File Serving
    - SSL Termination

    Beispiel-Konfiguration:
      server {
          listen 80;
          server_name example.com;

          location / {
              proxy_pass http://localhost:3000;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
          }

          location /static/ {
              root /var/www/;
              expires 30d;
          }
      }

  Apache:
    - mod_rewrite
    - .htaccess
    - Virtual Hosts

APPLICATION SERVER
------------------
  Node.js:    PM2 (Process Manager, Clustering)
  Python:     Gunicorn, uWSGI
  Java:       Tomcat, Jetty
  Ruby:       Puma, Unicorn

================================================================================
                         MIDDLEWARE-PATTERN
================================================================================

Request/Response-Pipeline fuer querschnittliche Belange.

  Typische Middleware:
    - Logging (Request-Logging, Metriken)
    - Authentifizierung (Token-Validierung)
    - Autorisierung (Rechte-Pruefung)
    - CORS (Cross-Origin Resource Sharing)
    - Rate Limiting (Anfragen-Begrenzung)
    - Compression (gzip, brotli)
    - Error Handling (Zentrale Fehlerbehandlung)

  Express.js Beispiel:
    // Logging Middleware
    app.use((req, res, next) => {
      console.log(`${req.method} ${req.path}`);
      next();
    });

    // Auth Middleware
    const authMiddleware = (req, res, next) => {
      const token = req.headers.authorization?.split(' ')[1];
      if (!token) return res.status(401).json({ error: 'Unauthorized' });

      try {
        req.user = jwt.verify(token, SECRET);
        next();
      } catch {
        res.status(401).json({ error: 'Invalid token' });
      }
    };

    app.use('/api/protected', authMiddleware);

================================================================================
                         BEST PRACTICES
================================================================================

SICHERHEIT
----------
  - Input-Validierung (Server-Side, niemals nur Client)
  - SQL Injection verhindern (Prepared Statements, ORM)
  - XSS-Praevention (Output Encoding)
  - CSRF-Tokens fuer State-aendernde Requests
  - Rate Limiting gegen Brute Force
  - HTTPS erzwingen
  - Security Headers (CSP, HSTS, X-Frame-Options)
  - Secrets nicht im Code (Environment Variables)
  - Dependencies regelmaessig aktualisieren

ERROR HANDLING
--------------
  - Zentrale Fehlerbehandlung
  - Keine Stack Traces in Produktion
  - Strukturierte Fehler-Responses
  - Logging mit Kontext (Request-ID, User-ID)

LOGGING UND MONITORING
----------------------
  - Strukturierte Logs (JSON)
  - Log Levels (DEBUG, INFO, WARN, ERROR)
  - Correlation IDs fuer Request-Tracing
  - Metriken (Response Time, Error Rate)
  - Alerting bei Anomalien

TWELVE-FACTOR APP
-----------------
Methodik fuer Cloud-native Anwendungen:
  1. Codebase: Eine Codebase, viele Deployments
  2. Dependencies: Explizit deklarieren
  3. Config: In Environment Variables
  4. Backing Services: Als angehängte Ressourcen
  5. Build, Release, Run: Strikte Trennung
  6. Processes: Stateless, Share-Nothing
  7. Port Binding: Self-contained
  8. Concurrency: Horizontal skalieren
  9. Disposability: Schneller Start, graceful Shutdown
  10. Dev/Prod Parity: Umgebungen aehnlich halten
  11. Logs: Als Event Streams
  12. Admin Processes: Als einmalige Prozesse

================================================================================
                         BACH-INTEGRATION
================================================================================

BACH kann Backend-Entwicklung unterstuetzen durch:
  - API-Scaffolding und Boilerplate-Generierung
  - Code-Reviews fuer Sicherheit
  - Datenbankschema-Design
  - Automatische API-Dokumentation
  - Test-Generierung

Workflow-Integration:
  bach> generate fastapi-crud User name:str email:str
  bach> security-audit src/
  bach> generate openapi-spec src/routes/
  bach> analyze-sql-injection src/database/

Deployment-Unterstuetzung:
  bach> generate dockerfile python-fastapi
  bach> generate k8s-manifest api-service

================================================================================
                         SIEHE AUCH
================================================================================

  Intern:
    wiki/webapps/frontend/README.txt
    wiki/python/webframeworks/
    wiki/java/spring/
    wiki/datenbanken/
    wiki/devops/docker/
    wiki/security/web_security/

  Extern:
    https://12factor.net/
    https://owasp.org/
    https://restfulapi.net/

================================================================================
                         AENDERUNGSHISTORIE
================================================================================

  2026-02-05  Vollstaendiger Artikel erstellt (vorher Stub)
  2026-01-24  Stub angelegt

================================================================================
