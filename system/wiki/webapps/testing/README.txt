# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: Jest, Cypress, Playwright Dokumentation, Testing Library, Martin Fowler

WEB-APP TESTING
===============

Stand: 2026-02-05

UEBERBLICK
==========
  Testing sichert Qualitaet und verhindert Regressionen.
  Verschiedene Test-Typen fuer verschiedene Ziele.

  Test-Pyramide (von unten nach oben):
    - Unit Tests (viele, schnell, isoliert)
    - Integration Tests (weniger, Komponenten-Interaktion)
    - E2E Tests (wenige, langsam, realistisch)

TEST-TYPEN
==========

  UNIT TESTS
  ----------
    Was: Einzelne Funktionen/Komponenten isoliert testen
    Wann: Logik, Utilities, reine Funktionen
    Tools: Jest, Vitest, Mocha

  INTEGRATION TESTS
  -----------------
    Was: Zusammenspiel mehrerer Komponenten
    Wann: API-Integration, Datenbank-Queries
    Tools: Jest, Testing Library, Supertest

  END-TO-END (E2E) TESTS
  ----------------------
    Was: Komplette User-Flows im echten Browser
    Wann: Kritische Pfade, Checkout, Login
    Tools: Cypress, Playwright, Selenium

  VISUAL REGRESSION TESTS
  -----------------------
    Was: Screenshot-Vergleiche
    Wann: UI-Aenderungen erkennen
    Tools: Percy, Chromatic, BackstopJS

UNIT TESTING MIT JEST
=====================

  INSTALLATION
  ------------
    npm install --save-dev jest

  KONFIGURATION
  -------------
    // jest.config.js
    module.exports = {
      testEnvironment: 'node',
      coverageThreshold: {
        global: { branches: 80, functions: 80, lines: 80 }
      }
    };

  GRUNDLAGEN
  ----------
    // sum.js
    function sum(a, b) {
      return a + b;
    }
    module.exports = sum;

    // sum.test.js
    const sum = require('./sum');

    describe('sum', () => {
      test('addiert 1 + 2 zu 3', () => {
        expect(sum(1, 2)).toBe(3);
      });

      test('addiert negative Zahlen', () => {
        expect(sum(-1, -2)).toBe(-3);
      });
    });

  MATCHER
  -------
    expect(value).toBe(3);              // Strikte Gleichheit
    expect(value).toEqual({a: 1});      // Deep Equality
    expect(value).toBeTruthy();         // Truthy
    expect(value).toBeFalsy();          // Falsy
    expect(value).toBeNull();           // null
    expect(value).toBeDefined();        // nicht undefined
    expect(value).toContain('text');    // String/Array enthaelt
    expect(value).toMatch(/regex/);     // Regex Match
    expect(fn).toThrow();               // Wirft Error
    expect(fn).toThrow('message');      // Spezifischer Error

  ASYNC TESTS
  -----------
    // Promise
    test('async mit Promise', () => {
      return fetchData().then(data => {
        expect(data).toBe('result');
      });
    });

    // Async/Await
    test('async mit await', async () => {
      const data = await fetchData();
      expect(data).toBe('result');
    });

  MOCKING
  -------
    // Funktion mocken
    const mockFn = jest.fn();
    mockFn.mockReturnValue(42);
    mockFn.mockResolvedValue('async result');

    expect(mockFn).toHaveBeenCalled();
    expect(mockFn).toHaveBeenCalledWith(arg1, arg2);
    expect(mockFn).toHaveBeenCalledTimes(3);

    // Modul mocken
    jest.mock('./api');
    const api = require('./api');
    api.fetchUser.mockResolvedValue({ name: 'Test' });

  SETUP/TEARDOWN
  --------------
    beforeAll(() => {
      // Vor allen Tests
    });

    afterAll(() => {
      // Nach allen Tests
    });

    beforeEach(() => {
      // Vor jedem Test
    });

    afterEach(() => {
      // Nach jedem Test
    });

REACT TESTING MIT TESTING LIBRARY
=================================

  INSTALLATION
  ------------
    npm install --save-dev @testing-library/react @testing-library/jest-dom

  GRUNDPRINZIP
  ------------
    Teste wie ein User interagiert, nicht Implementation.

  BEISPIEL
  --------
    // Button.jsx
    function Button({ onClick, children }) {
      return <button onClick={onClick}>{children}</button>;
    }

    // Button.test.jsx
    import { render, screen, fireEvent } from '@testing-library/react';
    import Button from './Button';

    test('ruft onClick bei Klick auf', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Klick mich</Button>);

      const button = screen.getByRole('button', { name: /klick mich/i });
      fireEvent.click(button);

      expect(handleClick).toHaveBeenCalledTimes(1);
    });

  QUERIES
  -------
    // Nach Rolle (bevorzugt)
    screen.getByRole('button');
    screen.getByRole('heading', { level: 1 });

    // Nach Text
    screen.getByText('Hallo Welt');
    screen.getByText(/hallo/i);  // Case-insensitive

    // Nach Label (Formulare)
    screen.getByLabelText('Email');

    // Nach Placeholder
    screen.getByPlaceholderText('Suchen...');

    // Nach Test-ID (letzter Ausweg)
    screen.getByTestId('custom-element');

  QUERY-VARIANTEN
  ---------------
    getBy*    - Wirft Error wenn nicht gefunden
    queryBy*  - Gibt null zurueck wenn nicht gefunden
    findBy*   - Async, wartet auf Element

  ASYNC TESTING
  -------------
    test('laedt Daten asynchron', async () => {
      render(<UserProfile userId="123" />);

      // Warten auf async Content
      const name = await screen.findByText('Max Mustermann');
      expect(name).toBeInTheDocument();
    });

  USER EVENTS
  -----------
    import userEvent from '@testing-library/user-event';

    test('tippt in Input', async () => {
      const user = userEvent.setup();
      render(<SearchForm />);

      const input = screen.getByRole('textbox');
      await user.type(input, 'Suchbegriff');

      expect(input).toHaveValue('Suchbegriff');
    });

E2E TESTING MIT CYPRESS
=======================

  INSTALLATION
  ------------
    npm install --save-dev cypress
    npx cypress open

  GRUNDSTRUKTUR
  -------------
    // cypress/e2e/login.cy.js
    describe('Login', () => {
      beforeEach(() => {
        cy.visit('/login');
      });

      it('loggt User erfolgreich ein', () => {
        cy.get('[data-cy="email"]').type('user@example.com');
        cy.get('[data-cy="password"]').type('password123');
        cy.get('[data-cy="submit"]').click();

        cy.url().should('include', '/dashboard');
        cy.contains('Willkommen').should('be.visible');
      });

      it('zeigt Fehler bei falschem Passwort', () => {
        cy.get('[data-cy="email"]').type('user@example.com');
        cy.get('[data-cy="password"]').type('wrong');
        cy.get('[data-cy="submit"]').click();

        cy.contains('Falsches Passwort').should('be.visible');
      });
    });

  COMMANDS
  --------
    cy.visit('/page');                  // Seite besuchen
    cy.get('selector');                 // Element finden
    cy.contains('text');                // Element mit Text
    cy.click();                         // Klicken
    cy.type('text');                    // Tippen
    cy.should('be.visible');            // Assertion
    cy.wait('@apiCall');                // Auf Request warten

  CUSTOM COMMANDS
  ---------------
    // cypress/support/commands.js
    Cypress.Commands.add('login', (email, password) => {
      cy.visit('/login');
      cy.get('[data-cy="email"]').type(email);
      cy.get('[data-cy="password"]').type(password);
      cy.get('[data-cy="submit"]').click();
    });

    // In Tests
    cy.login('user@example.com', 'password123');

  API MOCKING
  -----------
    cy.intercept('GET', '/api/users', { fixture: 'users.json' });
    cy.intercept('POST', '/api/login', { statusCode: 200, body: { token: 'abc' } });

E2E TESTING MIT PLAYWRIGHT
==========================

  INSTALLATION
  ------------
    npm init playwright@latest

  GRUNDSTRUKTUR
  -------------
    // tests/login.spec.ts
    import { test, expect } from '@playwright/test';

    test.describe('Login', () => {
      test('loggt User erfolgreich ein', async ({ page }) => {
        await page.goto('/login');

        await page.getByLabel('Email').fill('user@example.com');
        await page.getByLabel('Passwort').fill('password123');
        await page.getByRole('button', { name: 'Einloggen' }).click();

        await expect(page).toHaveURL(/.*dashboard/);
        await expect(page.getByText('Willkommen')).toBeVisible();
      });
    });

  VORTEILE GEGENUEBER CYPRESS
  ---------------------------
    - Multi-Browser (Chromium, Firefox, WebKit)
    - Schneller (parallele Ausfuehrung)
    - Bessere TypeScript-Integration
    - Network-Interception maechtiger

  LOCATORS
  --------
    page.getByRole('button', { name: 'Submit' });
    page.getByLabel('Email');
    page.getByPlaceholder('Suchen');
    page.getByText('Hallo');
    page.locator('[data-testid="submit"]');

  FIXTURES
  --------
    // fixtures.ts
    import { test as base } from '@playwright/test';

    export const test = base.extend({
      loggedInPage: async ({ page }, use) => {
        await page.goto('/login');
        await page.getByLabel('Email').fill('user@example.com');
        await page.getByLabel('Passwort').fill('password');
        await page.getByRole('button', { name: 'Login' }).click();
        await use(page);
      },
    });

API TESTING
===========

  SUPERTEST (NODE.JS)
  -------------------
    const request = require('supertest');
    const app = require('./app');

    describe('GET /api/users', () => {
      it('gibt User-Liste zurueck', async () => {
        const response = await request(app)
          .get('/api/users')
          .expect('Content-Type', /json/)
          .expect(200);

        expect(response.body).toHaveLength(3);
      });
    });

  PYTEST (PYTHON/FASTAPI)
  -----------------------
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)

    def test_get_users():
        response = client.get("/api/users")
        assert response.status_code == 200
        assert len(response.json()) == 3

TEST-STRATEGIEN
===============

  WAS TESTEN?
  -----------
    Unit Tests:
      - Business-Logik
      - Utility-Funktionen
      - Validierungen
      - State-Management

    Integration Tests:
      - API-Endpoints
      - Datenbank-Operationen
      - Komponenten-Interaktion

    E2E Tests:
      - Kritische User-Journeys
      - Checkout-Prozess
      - Authentifizierung
      - Hauptnavigation

  TESTABDECKUNG
  -------------
    Empfehlung:
      - 70-80% Unit Test Coverage
      - Kritische Pfade: 100%
      - E2E: 3-5 wichtigste Flows

    Coverage messen:
      jest --coverage
      npx nyc mocha

CI/CD INTEGRATION
=================

  GITHUB ACTIONS
  --------------
    # .github/workflows/test.yml
    name: Tests
    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-node@v4
            with:
              node-version: '20'
          - run: npm ci
          - run: npm test
          - run: npm run test:e2e

BEST PRACTICES
==============
  1. Tests muessen isoliert sein
  2. Keine Abhaengigkeiten zwischen Tests
  3. Aussagekraeftige Test-Namen
  4. AAA-Pattern: Arrange, Act, Assert
  5. Keine Implementation testen, nur Verhalten
  6. Flaky Tests sofort fixen
  7. Test-Daten in Fixtures
  8. Mocking sparsam einsetzen

ANTI-PATTERNS
=============
  - Tests die nie fehlschlagen
  - Zu viele Mocks
  - Tests die Implementation kennen
  - Langsame Unit Tests
  - Keine Assertions
  - Copy-Paste Tests

BACH-INTEGRATION
================
  Partner-Zuweisung:
    - Claude: Test-Strategien, Code-Review
    - Gemini: Framework-Dokumentation
    - Antigravity: Automatische Test-Generierung

  Typische Aufgaben:
    - Tests generieren
    - Coverage verbessern
    - Flaky Tests debuggen
    - Test-Strategie planen

SIEHE AUCH
==========
  wiki/webapps/README.txt
  wiki/webapps/performance/README.txt
  wiki/automatisierung/code_testing.txt
  wiki/python/testing/README.txt
