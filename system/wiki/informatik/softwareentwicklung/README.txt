# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: IEEE Software Engineering Body of Knowledge (SWEBOK), Agile Manifesto,
#          Martin Fowler (Refactoring), Clean Code (Robert C. Martin), Git Documentation

SOFTWAREENTWICKLUNG
===================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

EINFUEHRUNG
===========
Softwareentwicklung (Software Engineering) umfasst alle Aktivitaeten zur
systematischen Erstellung, Wartung und Evolution von Softwaresystemen.
Sie verbindet technische Faehigkeiten mit methodischen Vorgehensweisen,
um qualitativ hochwertige Software effizient zu produzieren.

Kernprinzipien:
  - Systematisches, diszipliniertes Vorgehen
  - Fokus auf Qualitaet und Wartbarkeit
  - Iterative Verbesserung
  - Zusammenarbeit im Team
  - Kontinuierliches Lernen


SOFTWARE DEVELOPMENT LIFE CYCLE (SDLC)
======================================

Der SDLC beschreibt die Phasen der Softwareentwicklung von der Idee
bis zur Ausserbetriebnahme.

  PHASE 1: ANFORDERUNGSANALYSE
  ----------------------------
  Ziel: Verstehen, was die Software leisten soll.

  Aktivitaeten:
    - Stakeholder identifizieren
    - Interviews, Workshops, Beobachtung
    - User Stories / Use Cases erstellen
    - Anforderungen dokumentieren

  Anforderungstypen:
    Funktional:     Was das System tun soll
    Nicht-funktional: Qualitaetsattribute (Performance, Sicherheit)
    Constraints:    Einschraenkungen (Budget, Technologie, Zeit)

  Dokumentation:
    - Software Requirements Specification (SRS)
    - User Stories mit Akzeptanzkriterien
    - Prototypen fuer Visualisierung


  PHASE 2: DESIGN
  ---------------
  Ziel: Architektur und Struktur der Software festlegen.

  Ebenen:
    High-Level Design (Architektur):
      - Systemkomponenten und deren Interaktion
      - Technologieauswahl
      - Deployment-Architektur

    Low-Level Design (Detaildesign):
      - Klassen, Module, Schnittstellen
      - Datenstrukturen
      - Algorithmen

  Architekturmuster:
    - Monolith:        Alles in einer Anwendung
    - Microservices:   Kleine, unabhaengige Dienste
    - Serverless:      Funktionen ohne Serververwaltung
    - Event-Driven:    Reaktion auf Ereignisse

  Design Patterns (Auswahl):
    Creational:   Singleton, Factory, Builder
    Structural:   Adapter, Decorator, Facade
    Behavioral:   Observer, Strategy, Command


  PHASE 3: IMPLEMENTIERUNG
  ------------------------
  Ziel: Code schreiben, der die Anforderungen erfuellt.

  Best Practices:
    - Clean Code Prinzipien befolgen
    - SOLID-Prinzipien anwenden
    - DRY (Don't Repeat Yourself)
    - KISS (Keep It Simple, Stupid)
    - YAGNI (You Ain't Gonna Need It)

  SOLID-Prinzipien:
    S - Single Responsibility:  Eine Klasse, eine Aufgabe
    O - Open/Closed:           Offen fuer Erweiterung, geschlossen fuer Modifikation
    L - Liskov Substitution:   Subtypen muessen ersetzbar sein
    I - Interface Segregation: Kleine, spezifische Interfaces
    D - Dependency Inversion:  Abhaengig von Abstraktionen, nicht Konkretionen

  Code Reviews:
    - Wissenstransfer im Team
    - Fehler frueh erkennen
    - Konsistenz sicherstellen
    - Konstruktives Feedback geben


  PHASE 4: TESTING
  ----------------
  Ziel: Qualitaet sicherstellen, Fehler finden.

  Test-Pyramide (von unten nach oben):
    Unit Tests:
      - Kleinste testbare Einheiten
      - Schnell, isoliert, automatisiert
      - Hohe Abdeckung anstreben (70-90%)

    Integration Tests:
      - Zusammenspiel von Komponenten
      - Datenbank, APIs, externe Dienste
      - Langsamer als Unit Tests

    End-to-End Tests:
      - Gesamtes System aus Nutzersicht
      - Browser-Automation (Selenium, Playwright)
      - Wenige, aber kritische Szenarien

  Weitere Testarten:
    - Performance Tests:  Lastverhalten
    - Security Tests:     Schwachstellen finden
    - Usability Tests:    Nutzerfreundlichkeit
    - Regression Tests:   Keine neuen Fehler durch Aenderungen


  PHASE 5: DEPLOYMENT
  -------------------
  Ziel: Software in Produktionsumgebung bringen.

  Strategien:
    Big Bang:       Alles auf einmal (riskant)
    Rolling Update: Schrittweise Aktualisierung
    Blue-Green:     Zwei Umgebungen, Umschaltung
    Canary:         Kleine Nutzergruppe zuerst

  Infrastructure as Code (IaC):
    - Terraform, Pulumi, CloudFormation
    - Reproduzierbare Umgebungen
    - Versionskontrolle fuer Infrastruktur


  PHASE 6: WARTUNG
  ----------------
  Ziel: Software am Laufen halten und verbessern.

  Typen:
    Corrective:  Fehler beheben
    Adaptive:    An neue Umgebungen anpassen
    Perfective:  Funktionen verbessern
    Preventive:  Zukuenftige Probleme vermeiden (Refactoring)


ENTWICKLUNGSMETHODEN
====================

  TRADITIONELLE METHODEN
  ----------------------
  Wasserfall:
    Sequentielle Phasen: Anforderung -> Design -> Implementierung -> Test
    Vorteile: Klare Struktur, gute Dokumentation
    Nachteile: Unflexibel, spaetes Feedback, hohe Risiken

  V-Modell:
    Wasserfallvariant mit expliziten Testphasen
    Jeder Entwicklungsphase ist eine Testphase zugeordnet
    Verbreitet in regulierten Branchen (Automobil, Medizin)


  AGILE METHODEN
  --------------
  Agiles Manifest (2001):
    - Individuen und Interaktionen > Prozesse und Werkzeuge
    - Funktionierende Software > Umfassende Dokumentation
    - Zusammenarbeit mit Kunden > Vertragsverhandlung
    - Reagieren auf Veraenderung > Befolgen eines Plans

  Scrum:
    Rollen:
      - Product Owner: Anforderungen priorisieren
      - Scrum Master:  Prozess unterstuetzen
      - Development Team: Software entwickeln

    Events:
      - Sprint Planning:  Arbeit fuer Sprint planen
      - Daily Scrum:      15-min taegliches Standup
      - Sprint Review:    Ergebnisse zeigen
      - Sprint Retro:     Prozess verbessern

    Artefakte:
      - Product Backlog:  Priorisierte Anforderungsliste
      - Sprint Backlog:   Arbeit fuer aktuellen Sprint
      - Increment:        Fertiges Produkt-Inkrement

    Sprint: Typisch 2-4 Wochen

  Kanban:
    - Visualisierung des Workflows (Board)
    - Work in Progress (WIP) Limits
    - Kontinuierlicher Fluss (kein fester Sprint)
    - Pull-Prinzip: Arbeit wird gezogen, nicht geschoben

  Extreme Programming (XP):
    - Pair Programming
    - Test-Driven Development (TDD)
    - Continuous Integration
    - Kurze Iterationen (1-2 Wochen)
    - Collective Code Ownership


VERSIONSKONTROLLE MIT GIT
=========================

  GRUNDLAGEN
  ----------
  Git ist das Standard-Versionskontrollsystem fuer Softwareentwicklung.
  Dezentral, schnell, branchfreundlich.

  Kernkonzepte:
    Repository:  Projektverzeichnis mit Historie
    Commit:      Snapshot des Projektzustands
    Branch:      Unabhaengiger Entwicklungszweig
    Merge:       Zweige zusammenfuehren
    Remote:      Entferntes Repository (GitHub, GitLab)

  Wichtige Befehle:
    git init          Repository erstellen
    git clone         Repository kopieren
    git add           Aenderungen stagen
    git commit        Commit erstellen
    git push          Zu Remote hochladen
    git pull          Von Remote aktualisieren
    git branch        Branches verwalten
    git checkout      Branch wechseln
    git merge         Branches zusammenfuehren


  BRANCHING-STRATEGIEN
  --------------------
  Git Flow:
    - main:    Produktionscode
    - develop: Entwicklungszweig
    - feature/*: Neue Features
    - release/*: Release-Vorbereitung
    - hotfix/*: Dringende Fixes

  GitHub Flow:
    - main: Immer deploybar
    - Feature Branches fuer alles
    - Pull Request -> Review -> Merge

  Trunk-Based Development:
    - Hauptsaechlich auf main/trunk entwickeln
    - Sehr kurze Feature Branches (max 1-2 Tage)
    - Feature Flags fuer unfertige Features


  CODE REVIEW
  -----------
  Pull Request / Merge Request:
    - Aenderungen zur Pruefung einreichen
    - Reviewer geben Feedback
    - Diskussion und Iteration
    - Approval vor Merge

  Best Practices:
    - Kleine, fokussierte PRs
    - Aussagekraeftige Commit Messages
    - Automatisierte Checks (Tests, Linting)
    - Konstruktives Feedback


CI/CD (CONTINUOUS INTEGRATION / CONTINUOUS DELIVERY)
====================================================

  CONTINUOUS INTEGRATION
  ----------------------
  Automatisches Bauen und Testen bei jedem Commit.

  Prinzipien:
    - Haeufige Commits (mindestens taeglich)
    - Automatisierter Build
    - Automatisierte Tests
    - Schnelles Feedback (< 10 Minuten ideal)
    - Kaputten Build sofort reparieren

  Tools:
    - GitHub Actions
    - GitLab CI/CD
    - Jenkins
    - CircleCI
    - Azure DevOps


  CONTINUOUS DELIVERY / DEPLOYMENT
  --------------------------------
  Continuous Delivery:
    Software ist jederzeit deploybar.
    Deployment ist manueller Schritt.

  Continuous Deployment:
    Jede Aenderung geht automatisch in Produktion.
    Erfordert hohes Vertrauen in Tests.

  Pipeline-Stufen (typisch):
    1. Build:     Code kompilieren, Artefakte erstellen
    2. Test:      Unit, Integration, E2E Tests
    3. Security:  SAST, Dependency Scanning
    4. Stage:     In Staging-Umgebung deployen
    5. Approve:   (Optional) Manuelle Freigabe
    6. Deploy:    In Produktion deployen
    7. Monitor:   Ueberwachung nach Deployment


QUALITAETSSICHERUNG
===================

  CODE-QUALITAET
  --------------
  Static Analysis:
    - Linter (ESLint, Pylint, Checkstyle)
    - Formatierer (Prettier, Black)
    - Code Smells erkennen (SonarQube)

  Metriken:
    - Cyclomatic Complexity: Verzweigungskomplexitaet
    - Code Coverage: Testabdeckung
    - Technical Debt: Aufwand fuer Aufraeuemarbeiten
    - Code Churn: Aenderungshaeufigkeit

  Dokumentation:
    - API-Dokumentation (OpenAPI, JSDoc)
    - Architektur-Dokumentation (arc42, C4)
    - README mit Quickstart
    - Inline-Kommentare sparsam aber sinnvoll


  TECHNISCHE SCHULDEN
  -------------------
  Definition: Kurzfristige Kompromisse, die langfristig Aufwand verursachen.

  Umgang:
    - Sichtbar machen (Backlog, Tools)
    - Regelmaessig abbauen (20% der Kapazitaet)
    - Bei Neuentwicklung vermeiden
    - Bewusste Entscheidungen dokumentieren


BEST PRACTICES
==============
  - Code Reviews fuer jeden Merge
  - Automatisierte Tests als Sicherheitsnetz
  - Kontinuierliche Integration praktizieren
  - Refactoring als Teil der taeglichen Arbeit
  - Dokumentation aktuell halten
  - Wissensaustausch im Team foerdern
  - Retrospektiven zur Prozessverbesserung
  - Feature Flags fuer sichere Releases


SIEHE AUCH
==========
  wiki/management/managementmethoden.txt
  wiki/devops/
  wiki/informatik/programmiersprachen/
  wiki/projektmanagement/

