# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: MDN Web Docs, W3C Standards, Web.dev (Google), Can I Use,
#          State of JS/CSS Surveys, Framework-Dokumentationen

WEB-ENTWICKLUNG
===============

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

EINFUEHRUNG
===========
Web-Entwicklung umfasst die Erstellung von Websites und Webanwendungen,
die ueber Browser zugaenglich sind. Sie unterteilt sich in Frontend
(Nutzeroberflaeche), Backend (Serverlogik) und Full-Stack (beides).

Das moderne Web basiert auf offenen Standards:
  - HTTP/HTTPS als Uebertragungsprotokoll
  - HTML fuer Struktur
  - CSS fuer Gestaltung
  - JavaScript fuer Interaktivitaet
  - WebAssembly fuer performante Anwendungen


FRONTEND-ENTWICKLUNG
====================

  HTML (HYPERTEXT MARKUP LANGUAGE)
  --------------------------------
  HTML5 ist der aktuelle Standard fuer die Strukturierung von Webinhalten.

  Grundstruktur:
    <!DOCTYPE html>
    <html lang="de">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Seitentitel</title>
    </head>
    <body>
      <header>Kopfbereich</header>
      <main>Hauptinhalt</main>
      <footer>Fusszeile</footer>
    </body>
    </html>

  Semantische Elemente:
    <header>    Kopfbereich
    <nav>       Navigation
    <main>      Hauptinhalt
    <article>   Eigenstaendiger Inhalt
    <section>   Thematischer Abschnitt
    <aside>     Nebeninformation
    <footer>    Fussbereich

  Barrierefreiheit (Accessibility):
    - Alt-Texte fuer Bilder
    - ARIA-Attribute fuer Screenreader
    - Semantisches HTML bevorzugen
    - Tastaturnavigation ermoeglichen
    - Farbkontraste beachten (WCAG 2.1)


  CSS (CASCADING STYLE SHEETS)
  ----------------------------
  CSS3 ermoeglicht komplexe visuelle Gestaltung.

  Selektoren:
    Element:    p { }           Alle Paragraphen
    Klasse:     .card { }       Elemente mit class="card"
    ID:         #header { }     Element mit id="header"
    Attribut:   [type="text"]   Inputfelder vom Typ text
    Pseudo:     a:hover { }     Link beim Hovern

  Box Model:
    - Content:  Eigentlicher Inhalt
    - Padding:  Innenabstand
    - Border:   Rahmen
    - Margin:   Aussenabstand

  Layout-Systeme:
    Flexbox:
      - Eindimensionales Layout (Zeile ODER Spalte)
      - display: flex
      - justify-content, align-items fuer Ausrichtung
      - flex-grow, flex-shrink fuer Groessenanpassung

    CSS Grid:
      - Zweidimensionales Layout (Zeilen UND Spalten)
      - display: grid
      - grid-template-columns, grid-template-rows
      - Ideal fuer komplexe Seitenlayouts

  CSS-Variablen (Custom Properties):
    :root {
      --primary-color: #3498db;
      --spacing: 1rem;
    }
    .button {
      background: var(--primary-color);
      padding: var(--spacing);
    }

  Praeprozessoren und Tools:
    - Sass/SCSS:  Variablen, Nesting, Mixins
    - PostCSS:    Plugins fuer Autoprefixer etc.
    - Tailwind:   Utility-First Framework
    - CSS Modules: Lokaler Scope in Komponenten


  JAVASCRIPT
  ----------
  JavaScript ist die Programmiersprache des Webs.

  Moderne Syntax (ES6+):
    - let/const statt var
    - Arrow Functions: (a, b) => a + b
    - Template Literals: `Hallo ${name}`
    - Destructuring: const {a, b} = obj
    - Spread Operator: [...array, newItem]
    - Modules: import/export
    - async/await fuer asynchronen Code

  DOM-Manipulation:
    // Element selektieren
    const element = document.querySelector('.class');

    // Event Listener
    element.addEventListener('click', (e) => {
      console.log('Geklickt!');
    });

    // Inhalt aendern
    element.textContent = 'Neuer Text';
    element.innerHTML = '<strong>HTML</strong>';

  Fetch API (HTTP-Anfragen):
    async function getData() {
      const response = await fetch('/api/data');
      const data = await response.json();
      return data;
    }

  TypeScript:
    - Superset von JavaScript mit statischer Typisierung
    - Bessere IDE-Unterstuetzung (Autovervollstaendigung)
    - Fehler zur Kompilierzeit erkennen
    - Standard in professionellen Projekten


  FRONTEND-FRAMEWORKS
  -------------------
  React:
    - Deklarative UI-Bibliothek (Meta)
    - Komponentenbasiert
    - Virtual DOM fuer Performance
    - Hooks fuer State und Lifecycle
    - Groesstes Oekosystem

  Vue.js:
    - Progressive Framework
    - Einfacher Einstieg
    - Single File Components
    - Reactive Data Binding
    - Gute Dokumentation

  Angular:
    - Vollstaendiges Framework (Google)
    - TypeScript nativ
    - Dependency Injection
    - RxJS fuer reaktive Programmierung
    - Gut fuer Enterprise-Anwendungen

  Svelte:
    - Compiler statt Runtime
    - Weniger Boilerplate
    - Sehr performant
    - Einfache Syntax
    - Wachsende Community

  Solid.js:
    - Fine-grained Reactivity
    - Kein Virtual DOM
    - React-aehnliche Syntax
    - Hoechste Performance


  BUILD-TOOLS
  -----------
  Vite:
    - Moderner Build-Tool (schnell)
    - Native ES Modules in Entwicklung
    - Optimierter Production Build
    - Framework-agnostisch
    - Hot Module Replacement (HMR)

  Webpack:
    - Etablierter Bundler
    - Umfangreiches Plugin-System
    - Code Splitting
    - Tree Shaking (toten Code entfernen)

  esbuild:
    - Extrem schnell (Go-basiert)
    - Oft als Backend fuer andere Tools


BACKEND-ENTWICKLUNG
===================

  SPRACHEN UND FRAMEWORKS
  -----------------------
  Node.js (JavaScript):
    - Express.js: Minimalistisch, flexibel
    - Fastify: Performant, Schema-basiert
    - NestJS: Enterprise-Framework (TypeScript)

  Python:
    - Django: Batteries-included, ORM, Admin
    - Flask: Microframework, flexibel
    - FastAPI: Modern, async, automatische Docs

  Java/Kotlin:
    - Spring Boot: Enterprise-Standard
    - Quarkus: Cloud-nativ, GraalVM

  Go:
    - Gin: Performant, minimalistisch
    - Echo: Feature-reich
    - Fiber: Express-inspiriert

  PHP:
    - Laravel: Elegant, umfangreich
    - Symfony: Komponenten-basiert

  Ruby:
    - Ruby on Rails: Convention over Configuration


  REST APIS
  ---------
  REST (Representational State Transfer) definiert Prinzipien fuer Web-APIs.

  HTTP-Methoden:
    GET:    Ressource abrufen
    POST:   Ressource erstellen
    PUT:    Ressource vollstaendig ersetzen
    PATCH:  Ressource teilweise aktualisieren
    DELETE: Ressource loeschen

  Statuscode-Kategorien:
    2xx: Erfolg (200 OK, 201 Created, 204 No Content)
    3xx: Umleitung (301 Moved, 304 Not Modified)
    4xx: Clientfehler (400 Bad Request, 401 Unauthorized, 404 Not Found)
    5xx: Serverfehler (500 Internal Server Error, 503 Service Unavailable)

  Best Practices:
    - Ressourcen-orientierte URLs (/users, /users/123)
    - JSON als Standard-Format
    - Versionierung (/api/v1/...)
    - Pagination fuer Listen
    - Konsistente Fehlerformate


  GRAPHQL
  -------
  Alternative zu REST mit flexiblen Abfragen.

  Vorteile:
    - Client bestimmt Datenstruktur
    - Eine Anfrage fuer mehrere Ressourcen
    - Starke Typisierung
    - Introspection (Schema abfragen)

  Nachteile:
    - Komplexeres Caching
    - Lernkurve
    - Potentiell teure Queries (N+1 Problem)

  Tools:
    - Apollo (Client & Server)
    - GraphQL Yoga
    - Hasura (automatische GraphQL-API)


  DATENBANKEN
  -----------
  Relational (SQL):
    - PostgreSQL: Feature-reich, ACID-konform
    - MySQL/MariaDB: Weit verbreitet
    - SQLite: Eingebettet, keine Server

  NoSQL:
    - MongoDB: Dokumentenbasiert
    - Redis: Key-Value, In-Memory
    - Elasticsearch: Suche und Analytics

  ORMs und Query Builder:
    - Prisma (TypeScript)
    - TypeORM (TypeScript)
    - SQLAlchemy (Python)
    - Sequelize (Node.js)


FULL-STACK FRAMEWORKS
=====================

  NEXT.JS
  -------
  React-basiertes Framework fuer Produktion.

  Features:
    - Server-Side Rendering (SSR)
    - Static Site Generation (SSG)
    - API Routes (Backend integriert)
    - App Router (React Server Components)
    - Automatisches Code Splitting
    - Image Optimization

  NUXT
  ----
  Vue-Aequivalent zu Next.js.

  Features:
    - Universal Rendering
    - Auto-imports
    - File-based Routing
    - Nitro Server Engine

  REMIX
  -----
  Full-Stack React Framework.

  Philosophie:
    - Web-Fundamentals (Forms, HTTP)
    - Progressive Enhancement
    - Nested Routing mit Datenladen
    - Optimistische UI-Updates

  ASTRO
  -----
  Content-fokussiertes Framework.

  Besonderheiten:
    - Islands Architecture
    - Partial Hydration
    - Framework-agnostisch (React, Vue, Svelte)
    - Ideal fuer Content-Websites


RESPONSIVE DESIGN
=================

  PRINZIPIEN
  ----------
  Mobile First:
    Basis-Design fuer kleine Bildschirme,
    Erweiterungen fuer groessere mit Media Queries.

  Viewport Meta:
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

  Media Queries:
    /* Basis (Mobile) */
    .container { width: 100%; }

    /* Tablet */
    @media (min-width: 768px) {
      .container { width: 750px; }
    }

    /* Desktop */
    @media (min-width: 1024px) {
      .container { width: 960px; }
    }

  Flexible Einheiten:
    - rem/em statt px fuer Schriftgroessen
    - % oder vw/vh fuer Layouts
    - clamp() fuer responsive Werte

  Responsive Bilder:
    <picture>
      <source media="(min-width: 800px)" srcset="large.jpg">
      <source media="(min-width: 400px)" srcset="medium.jpg">
      <img src="small.jpg" alt="Beschreibung">
    </picture>


WEB PERFORMANCE
===============

  METRIKEN (CORE WEB VITALS)
  --------------------------
  LCP (Largest Contentful Paint):
    Zeit bis groesstes Element sichtbar.
    Ziel: < 2.5 Sekunden

  FID (First Input Delay):
    Zeit bis erste Interaktion moeglich.
    Ziel: < 100 Millisekunden

  CLS (Cumulative Layout Shift):
    Visuelle Stabilitaet (kein Springen).
    Ziel: < 0.1

  OPTIMIERUNGEN
  -------------
    - Bilder komprimieren (WebP, AVIF)
    - Lazy Loading fuer Bilder/Videos
    - Code Splitting (nur laden was noetig)
    - Caching-Strategien (Browser, CDN)
    - Critical CSS inline
    - JavaScript minimieren und deferrieren
    - HTTP/2 oder HTTP/3 nutzen


SICHERHEIT
==========
  - HTTPS verwenden (TLS)
  - Input validieren (Client UND Server)
  - SQL Injection verhindern (Prepared Statements)
  - XSS verhindern (Output escapen)
  - CSRF-Tokens verwenden
  - Content Security Policy (CSP)
  - CORS korrekt konfigurieren
  - Abhaengigkeiten aktuell halten


BEST PRACTICES
==============
  - Semantisches HTML fuer Barrierefreiheit
  - Mobile First Design
  - Performance von Anfang an beachten
  - Progressive Enhancement
  - Automatisierte Tests (Unit, E2E)
  - Versionskontrolle mit Git
  - CI/CD fuer Deployments
  - Monitoring und Error Tracking


SIEHE AUCH
==========
  wiki/webapps/
  wiki/python/webframeworks/
  wiki/javascript/
  wiki/informatik/softwareentwicklung/

