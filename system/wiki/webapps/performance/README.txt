# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: Google Web Vitals, MDN Web Docs, web.dev, Lighthouse Dokumentation

WEB-PERFORMANCE-OPTIMIERUNG
===========================

Stand: 2026-02-05

UEBERBLICK
==========
  Performance ist entscheidend fuer User Experience und SEO.
  Langsame Seiten = hohe Absprungraten, schlechtes Ranking.

  Kernmetriken (Core Web Vitals):
    - LCP: Largest Contentful Paint
    - INP: Interaction to Next Paint
    - CLS: Cumulative Layout Shift

CORE WEB VITALS
===============

  LARGEST CONTENTFUL PAINT (LCP)
  ------------------------------
    Was: Ladezeit des groessten sichtbaren Elements
    Ziel: < 2.5 Sekunden

    Optimierung:
      - Server Response Time verbessern
      - Render-blocking Resources eliminieren
      - Hero-Images optimieren
      - CDN nutzen

  INTERACTION TO NEXT PAINT (INP)
  -------------------------------
    Was: Reaktionszeit auf User-Interaktionen
    Ziel: < 200 Millisekunden

    Optimierung:
      - JavaScript aufteilen (Code Splitting)
      - Long Tasks vermeiden
      - Event Handler optimieren
      - Web Workers fuer schwere Berechnungen

  CUMULATIVE LAYOUT SHIFT (CLS)
  -----------------------------
    Was: Visuelle Stabilitaet (unerwartete Verschiebungen)
    Ziel: < 0.1

    Optimierung:
      - Bild-Dimensionen immer angeben
      - Platzhalter fuer Ads/Embeds
      - Web Fonts richtig laden
      - Keine dynamischen Content-Injections

FRONTEND-OPTIMIERUNG
====================

  JAVASCRIPT
  ----------
    Code Splitting:
      // Dynamischer Import
      const module = await import('./schweres-modul.js');

      // React Lazy Loading
      const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

    Tree Shaking:
      - Nur genutzte Exports importieren
      - ES Modules nutzen (nicht CommonJS)

    Minification:
      - Terser/ESBuild fuer Production
      - Source Maps separat

    Bundle-Analyse:
      npm install webpack-bundle-analyzer
      # Visualisiert Bundle-Groesse

  CSS
  ---
    Critical CSS:
      - Above-the-fold CSS inline
      - Rest async laden

      <style>/* Critical CSS hier */</style>
      <link rel="preload" href="styles.css" as="style"
            onload="this.onload=null;this.rel='stylesheet'">

    CSS Minification:
      - cssnano, clean-css
      - Unused CSS entfernen (PurgeCSS)

    CSS-in-JS beachten:
      - Runtime-Overhead moeglich
      - Styled-components vs. CSS Modules

  BILDER
  ------
    Formate:
      - WebP: 25-35% kleiner als JPEG
      - AVIF: noch besser, aber weniger Support
      - SVG: fuer Vektorgrafiken

    Responsive Images:
      <picture>
        <source srcset="bild.avif" type="image/avif">
        <source srcset="bild.webp" type="image/webp">
        <img src="bild.jpg" alt="Beschreibung"
             width="800" height="600"
             loading="lazy">
      </picture>

    Lazy Loading:
      <img src="bild.jpg" loading="lazy" alt="...">

    Bildoptimierung:
      - Squoosh, ImageOptim
      - Sharp (Node.js)
      - Cloudinary, imgix (CDN)

  FONTS
  -----
    Font Loading Strategy:
      @font-face {
        font-family: 'MeineSchrift';
        src: url('font.woff2') format('woff2');
        font-display: swap;  /* Fallback waehrend Laden */
      }

    Optimierungen:
      - Nur benoetigte Glyphs (Subsetting)
      - WOFF2 Format (beste Kompression)
      - font-display: swap oder optional
      - Preload fuer wichtige Fonts

      <link rel="preload" href="font.woff2"
            as="font" type="font/woff2" crossorigin>

CACHING
=======

  BROWSER CACHING
  ---------------
    HTTP Cache Headers:
      Cache-Control: max-age=31536000, immutable
      # Fuer versionierte Assets (app.abc123.js)

      Cache-Control: no-cache
      # Immer revalidieren (HTML)

      ETag: "abc123"
      # Fuer bedingte Requests

  SERVICE WORKER
  --------------
    // sw.js
    self.addEventListener('install', event => {
      event.waitUntil(
        caches.open('v1').then(cache => {
          return cache.addAll([
            '/',
            '/styles.css',
            '/app.js'
          ]);
        })
      );
    });

    self.addEventListener('fetch', event => {
      event.respondWith(
        caches.match(event.request)
          .then(response => response || fetch(event.request))
      );
    });

  CDN
  ---
    Content Delivery Network:
      - Cloudflare, AWS CloudFront, Fastly
      - Assets naeher am User
      - DDoS-Schutz inklusive

    Konfiguration:
      - Lange Cache-Zeiten fuer Assets
      - Cache Invalidation bei Deploy

SERVER-OPTIMIERUNG
==================

  KOMPRESSION
  -----------
    Gzip/Brotli:
      # Nginx
      gzip on;
      gzip_types text/plain text/css application/json
                 application/javascript;

      brotli on;
      brotli_types text/plain text/css application/json
                   application/javascript;

  HTTP/2 UND HTTP/3
  -----------------
    Vorteile:
      - Multiplexing (mehrere Requests parallel)
      - Header-Kompression
      - Server Push (vorsichtig einsetzen)

    Konfiguration:
      # Nginx
      listen 443 ssl http2;

  DATABASE
  --------
    Query-Optimierung:
      - Indizes richtig setzen
      - N+1 Queries vermeiden
      - Pagination nutzen

    Connection Pooling:
      - PgBouncer (PostgreSQL)
      - Connections wiederverwenden

  CACHING-LAYER
  -------------
    Redis/Memcached:
      - Session Storage
      - Frequently accessed Data
      - Rate Limiting

    Beispiel (Python/Redis):
      import redis
      r = redis.Redis()

      cached = r.get('user:123')
      if not cached:
          data = db.get_user(123)
          r.setex('user:123', 3600, json.dumps(data))

LAZY LOADING STRATEGIEN
=======================

  KOMPONENTEN
  -----------
    // React
    const HeavyChart = React.lazy(() => import('./HeavyChart'));

    function Dashboard() {
      return (
        <Suspense fallback={<Loading />}>
          <HeavyChart />
        </Suspense>
      );
    }

  ROUTES
  ------
    // React Router
    const Home = lazy(() => import('./pages/Home'));
    const About = lazy(() => import('./pages/About'));

  INTERSECTION OBSERVER
  ---------------------
    // Laden wenn sichtbar
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          loadComponent(entry.target);
          observer.unobserve(entry.target);
        }
      });
    });

    observer.observe(document.querySelector('.lazy-section'));

MESSUNG UND MONITORING
======================

  TOOLS
  -----
    Lighthouse:
      - Chrome DevTools
      - CLI: lighthouse https://example.com

    WebPageTest:
      - webpagetest.org
      - Detaillierte Wasserfall-Analyse

    Core Web Vitals:
      - Google Search Console
      - Chrome User Experience Report

  REAL USER MONITORING (RUM)
  --------------------------
    Web Vitals Library:
      import {onLCP, onINP, onCLS} from 'web-vitals';

      onLCP(console.log);
      onINP(console.log);
      onCLS(console.log);

    Services:
      - Google Analytics
      - Sentry Performance
      - Datadog RUM

CHECKLISTE
==========
  [ ] Core Web Vitals messen
  [ ] Bilder optimieren (WebP, Lazy Loading)
  [ ] JavaScript aufteilen (Code Splitting)
  [ ] CSS Critical Path optimieren
  [ ] Caching-Strategie implementieren
  [ ] CDN einrichten
  [ ] Kompression aktivieren (Brotli/Gzip)
  [ ] HTTP/2 aktivieren
  [ ] Fonts optimieren
  [ ] Third-Party Scripts minimieren
  [ ] Monitoring einrichten

BEST PRACTICES
==============
  1. Performance Budget definieren
  2. Lighthouse in CI/CD integrieren
  3. Real User Monitoring nutzen
  4. Mobile-First optimieren
  5. Third-Party-Scripts kritisch pruefen
  6. Regelmaessig messen und verbessern

ANTI-PATTERNS
=============
  - Zu viele HTTP-Requests
  - Unoptimierte Bilder
  - Render-blocking Scripts
  - Inline-Styles statt CSS
  - Kein Caching
  - Synchrone Third-Party Scripts
  - Layout Shifts durch Ads

BACH-INTEGRATION
================
  Partner-Zuweisung:
    - Claude: Code-Review, Optimierungsvorschlaege
    - Gemini: Aktuelle Best Practices recherchieren
    - Ollama: Lokale Performance-Tests

  Typische Aufgaben:
    - Lighthouse-Reports analysieren
    - Optimierungsplan erstellen
    - Code refactoren
    - Monitoring einrichten

SIEHE AUCH
==========
  wiki/webapps/README.txt
  wiki/webapps/testing/README.txt
  wiki/informatik/devops/README.txt
