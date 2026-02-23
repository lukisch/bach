================================================================================
                         WEB-APPS FRONTEND
================================================================================

Portabilitaet:      UNIVERSAL
Zuletzt validiert:  2026-02-05
Naechste Pruefung:  2027-02-05
Quellen:            MDN Web Docs, W3C Standards, Framework-Dokumentationen,
                    web.dev (Google), State of JS Survey 2025

Stand: 2026-02-05

================================================================================
                         EINFUEHRUNG
================================================================================

Frontend-Entwicklung umfasst alle Technologien und Praktiken, die zur
Erstellung der Benutzeroberflaeche von Webanwendungen eingesetzt werden.
Das Frontend ist die Schnittstelle zwischen Mensch und Maschine im Web.

Die drei Saeulen der Frontend-Entwicklung sind:
  - HTML (Struktur und Semantik)
  - CSS (Praesentation und Layout)
  - JavaScript (Interaktivitaet und Logik)

Moderne Frontend-Entwicklung geht weit ueber diese Grundlagen hinaus und
umfasst Frameworks, Build-Tools, Testing, Performance-Optimierung und
barrierefreie Gestaltung (Accessibility).

================================================================================
                         HTML5 - HYPERTEXT MARKUP LANGUAGE
================================================================================

SEMANTISCHE STRUKTUR
--------------------
HTML5 fuehrt semantische Elemente ein, die die Bedeutung des Inhalts
vermitteln:

  Dokument-Struktur:
    <header>      Kopfbereich einer Seite oder Sektion
    <nav>         Navigationsbereich
    <main>        Hauptinhalt (nur einmal pro Seite)
    <article>     Eigenstaendiger Inhalt
    <section>     Thematische Gruppierung
    <aside>       Ergaenzender Inhalt (Sidebar)
    <footer>      Fussbereich

  Inline-Semantik:
    <mark>        Hervorgehobener Text
    <time>        Datum/Uhrzeit (maschinenlesbar)
    <figure>      Abbildung mit Beschriftung
    <figcaption>  Beschriftung fuer <figure>

FORMULARE
---------
HTML5 erweitert Formulare um neue Input-Typen und Validierung:

  Neue Input-Typen:
    email, url, tel, number, range, date, time, datetime-local,
    month, week, color, search

  Attribute:
    required      Pflichtfeld
    pattern       Regex-Validierung
    placeholder   Platzhaltertext
    autofocus     Automatischer Fokus
    autocomplete  Browser-Autovervollstaendigung

  Beispiel:
    <form>
      <input type="email" required placeholder="E-Mail">
      <input type="password" minlength="8" required>
      <button type="submit">Anmelden</button>
    </form>

MULTIMEDIA
----------
Einbettung ohne Plugins:

  Audio:
    <audio src="sound.mp3" controls>
      Fallback-Text
    </audio>

  Video:
    <video src="video.mp4" controls width="640" height="360">
      <track kind="subtitles" src="untertitel.vtt" srclang="de">
    </video>

CANVAS UND SVG
--------------
  Canvas:   Pixel-basierte 2D-Grafik via JavaScript
  SVG:      Vektorbasierte Grafik, skalierbar, animierbar

================================================================================
                         CSS3 - CASCADING STYLE SHEETS
================================================================================

MODERNE LAYOUT-SYSTEME
----------------------

Flexbox (Eindimensional):
  .container {
    display: flex;
    justify-content: space-between;  /* Hauptachse */
    align-items: center;             /* Querachse */
    gap: 1rem;
  }

  .item {
    flex: 1;           /* Wachsen */
    flex-shrink: 0;    /* Nicht schrumpfen */
  }

CSS Grid (Zweidimensional):
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    grid-gap: 20px;
  }

  .grid-item {
    grid-column: span 2;  /* 2 Spalten breit */
  }

RESPONSIVE DESIGN
-----------------
Anpassung an verschiedene Bildschirmgroessen:

  Mobile First:
    /* Basis: Mobile */
    .element { font-size: 1rem; }

    /* Tablet */
    @media (min-width: 768px) {
      .element { font-size: 1.2rem; }
    }

    /* Desktop */
    @media (min-width: 1024px) {
      .element { font-size: 1.4rem; }
    }

  Container Queries (CSS3 neu):
    @container (min-width: 400px) {
      .card { flex-direction: row; }
    }

CSS VARIABLEN (CUSTOM PROPERTIES)
---------------------------------
  :root {
    --primary-color: #007bff;
    --spacing-unit: 8px;
    --border-radius: 4px;
  }

  .button {
    background: var(--primary-color);
    padding: calc(var(--spacing-unit) * 2);
    border-radius: var(--border-radius);
  }

ANIMATIONEN UND TRANSITIONS
---------------------------
  Transitions:
    .button {
      transition: background-color 0.3s ease, transform 0.2s;
    }
    .button:hover {
      background-color: #0056b3;
      transform: scale(1.05);
    }

  Keyframe-Animationen:
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .element {
      animation: fadeIn 0.5s ease-out forwards;
    }

PRAEPROZESSOREN
---------------
  Sass/SCSS:
    - Variablen, Nesting, Mixins, Funktionen
    - Partials und Import
    - Mathematische Operationen

  PostCSS:
    - Plugin-basiert
    - Autoprefixer (Vendor-Prefixes)
    - CSS Modules

================================================================================
                         JAVASCRIPT (ES6+)
================================================================================

MODERNE SYNTAX
--------------
  Variablen:
    const CONSTANT = 'unveraenderlich';
    let variable = 'aenderbar';
    // var vermeiden (Function Scope, Hoisting-Probleme)

  Arrow Functions:
    const add = (a, b) => a + b;
    const greet = name => `Hallo, ${name}!`;

  Template Literals:
    const message = `Willkommen, ${user.name}!
    Sie haben ${count} neue Nachrichten.`;

  Destructuring:
    const { name, age } = user;
    const [first, second, ...rest] = array;

  Spread/Rest:
    const merged = { ...obj1, ...obj2 };
    const cloned = [...array];

ASYNCHRONE PROGRAMMIERUNG
-------------------------
  Promises:
    fetch('/api/data')
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));

  Async/Await:
    async function fetchData() {
      try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return data;
      } catch (error) {
        console.error('Fehler:', error);
      }
    }

  Promise.all (Parallele Ausfuehrung):
    const [users, posts] = await Promise.all([
      fetch('/api/users').then(r => r.json()),
      fetch('/api/posts').then(r => r.json())
    ]);

DOM MANIPULATION
----------------
  Selektion:
    const element = document.querySelector('.class');
    const elements = document.querySelectorAll('div.item');

  Event Handling:
    element.addEventListener('click', (event) => {
      event.preventDefault();
      // Logik
    });

  Klassen-Manipulation:
    element.classList.add('active');
    element.classList.remove('hidden');
    element.classList.toggle('expanded');

================================================================================
                         FRAMEWORKS UND BIBLIOTHEKEN
================================================================================

REACT
-----
Deklarative UI-Bibliothek von Meta (Facebook).

  Funktionale Komponenten:
    function Greeting({ name }) {
      const [count, setCount] = useState(0);

      useEffect(() => {
        document.title = `Zaehler: ${count}`;
      }, [count]);

      return (
        <div>
          <h1>Hallo, {name}!</h1>
          <button onClick={() => setCount(c => c + 1)}>
            Geklickt: {count}
          </button>
        </div>
      );
    }

  Wichtige Hooks:
    useState     Lokaler State
    useEffect    Side Effects (Lifecycle)
    useContext   Context-Zugriff
    useReducer   Komplexer State
    useMemo      Memoization
    useCallback  Callback-Memoization

VUE.JS
------
Progressives Framework mit sanfter Lernkurve.

  Composition API (Vue 3):
    <script setup>
    import { ref, computed, onMounted } from 'vue';

    const count = ref(0);
    const doubled = computed(() => count.value * 2);

    onMounted(() => {
      console.log('Komponente geladen');
    });
    </script>

    <template>
      <button @click="count++">{{ count }}</button>
      <p>Verdoppelt: {{ doubled }}</p>
    </template>

ANGULAR
-------
Vollstaendiges Framework von Google, TypeScript-basiert.

  Eigenschaften:
    - Dependency Injection
    - Reactive Forms
    - Router integriert
    - CLI fuer Scaffolding

SVELTE
------
Compiler-basierter Ansatz ohne Virtual DOM.

  Vorteile:
    - Kleinere Bundle-Groesse
    - Bessere Runtime-Performance
    - Einfachere Syntax

================================================================================
                         BUILD TOOLS UND TOOLCHAIN
================================================================================

VITE
----
Moderner Build-Tool (empfohlen fuer neue Projekte):
  - Extrem schneller Dev-Server (ES Modules)
  - Hot Module Replacement (HMR)
  - Optimierter Production Build

  Installation:
    npm create vite@latest my-app -- --template react

WEBPACK
-------
Etablierter Bundler fuer komplexe Projekte:
  - Code Splitting
  - Tree Shaking
  - Plugin-Oekosystem

PAKETMANAGER
------------
  npm       Standard Node.js Package Manager
  yarn      Alternative mit Workspaces
  pnpm      Platzsparend durch Hardlinks

================================================================================
                         BEST PRACTICES
================================================================================

PERFORMANCE
-----------
  - Lazy Loading fuer Bilder und Komponenten
  - Code Splitting
  - Caching-Strategien
  - Critical CSS inline
  - Bilder optimieren (WebP, AVIF)

ACCESSIBILITY (A11Y)
--------------------
  - Semantisches HTML verwenden
  - ARIA-Attribute wo noetig
  - Tastatur-Navigation sicherstellen
  - Farbkontrast pruefen (WCAG 2.1)
  - Alt-Texte fuer Bilder

SICHERHEIT
----------
  - Content Security Policy (CSP)
  - XSS-Praevention (Input sanitizen)
  - HTTPS erzwingen
  - Subresource Integrity (SRI)

================================================================================
                         BACH-INTEGRATION
================================================================================

BACH kann Frontend-Entwicklung unterstuetzen durch:
  - Generierung von Komponenten-Boilerplate
  - CSS-Optimierung und -Konvertierung
  - Code-Reviews fuer Accessibility
  - Performance-Analyse
  - Automatisierte Tests generieren

Workflow-Integration:
  bach> generate react-component UserProfile
  bach> analyze-a11y src/components/
  bach> optimize-css styles/main.css

================================================================================
                         SIEHE AUCH
================================================================================

  Intern:
    wiki/webapps/backend/README.txt
    wiki/informatik/web_entwicklung/
    wiki/javascript/
    wiki/typescript/

  Extern:
    https://developer.mozilla.org/de/docs/Web
    https://web.dev/
    https://caniuse.com/

================================================================================
                         AENDERUNGSHISTORIE
================================================================================

  2026-02-05  Vollstaendiger Artikel erstellt (vorher Stub)
  2026-01-24  Stub angelegt

================================================================================
