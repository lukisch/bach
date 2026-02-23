# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: Microsoft Office Dokumentation, Google Workspace Help, Atlassian
#          Documentation, Notion Help Center, Obsidian Help, Stack Overflow,
#          Product Hunt, G2 Reviews

IT-TOOLS - UEBERSICHT UND PRAXISWISSEN
======================================

Stand: 2026-02-05

================================================================================
TEIL 1: BUERO-ANWENDUNGEN
================================================================================

1.1 TABELLENKALKULATION
-----------------------
Das universelle Werkzeug fuer Daten, Berechnungen und Analysen.

  MICROSOFT EXCEL:
  ----------------
  Der Standard in Unternehmen.

    STAERKEN:
      - Maechtige Formeln und Funktionen
      - Pivot-Tabellen fuer Datenanalyse
      - VBA-Makros fuer Automatisierung
      - Power Query fuer Datentransformation
      - Breite Akzeptanz und Kompatibilitaet

    VERSIONEN:
      - Excel Desktop (Windows/Mac) - Vollversion
      - Excel Online - Browser, eingeschraenkt
      - Excel Mobile - Smartphone/Tablet

    WANN NUTZEN:
      - Finanzmodelle und Budgets
      - Datenanalyse und Reporting
      - Listen und Tracker
      - Automatisierte Berechnungen

    GRENZEN:
      - Nicht fuer grosse Datenmengen (>1 Mio. Zeilen)
      - Versionierung schwierig
      - Kollaboration limitiert (vs. Google Sheets)

  GOOGLE SHEETS:
  --------------
  Die kollaborative Alternative.

    STAERKEN:
      - Echtzeit-Zusammenarbeit
      - Automatische Speicherung
      - Versionsverlauf
      - Kostenlos (mit Google-Konto)
      - Apps Script fuer Automatisierung

    WANN NUTZEN:
      - Team-Arbeit an Dokumenten
      - Einfache Formulare und Umfragen
      - Schneller Datenaustausch
      - Web-basierte Loesungen

    NACHTEILE:
      - Weniger Funktionen als Excel
      - Langsamere Performance bei grossen Dateien
      - Internetverbindung noetig

  LIBREOFFICE CALC:
  -----------------
  Open-Source-Alternative.

    VORTEILE:
      - Kostenlos und Open Source
      - Gute Excel-Kompatibilitaet
      - Laeuft offline
      - Keine Cloud-Abhaengigkeit

    NACHTEILE:
      - Weniger Funktionen
      - Kein nativer Cloud-Support
      - Makro-Kompatibilitaet eingeschraenkt

1.2 TEXTVERARBEITUNG
--------------------

  MICROSOFT WORD:
    STAERKEN:
      - Formatierung und Layout
      - Serienbrief-Funktion
      - Aenderungsnachverfolgung
      - Inhaltsverzeichnis, Fussnoten
      - Standard-Austauschformat (.docx)

    PRAXIS-TIPPS:
      - Formatvorlagen nutzen (nicht manuell formatieren!)
      - Abschnittswechsel fuer unterschiedliche Layouts
      - Felder fuer dynamische Inhalte
      - Dokumentvorlagen anlegen

  GOOGLE DOCS:
    STAERKEN:
      - Echtzeit-Kollaboration
      - Kommentare und Vorschlaege
      - Versionsverlauf
      - Einfache Freigabe

    PRAXIS-TIPPS:
      - "Vorschlaege" statt direkter Bearbeitung
      - Add-ons fuer erweiterte Funktionen
      - Voice Typing fuer Diktat

  MARKDOWN:
    KONZEPT:
      - Einfache Textauszeichnung
      - Plattformunabhaengig
      - Versionierbar mit Git
      - Konvertierbar in viele Formate

    SYNTAX-GRUNDLAGEN:
      # Ueberschrift 1
      ## Ueberschrift 2
      **fett** und *kursiv*
      - Aufzaehlung
      1. Nummerierung
      [Link](url)
      `Code`

    TOOLS:
      - Obsidian, Notion (Markdown-basiert)
      - Visual Studio Code
      - Typora, Mark Text

1.3 PRAESENTATIONEN
-------------------

  MICROSOFT POWERPOINT:
    STAERKEN:
      - Reichhaltige Gestaltung
      - Animationen und Uebergaenge
      - Referentenansicht
      - Breite Kompatibilitaet

    BEST PRACTICES:
      - Weniger Text, mehr Visualisierung
      - Konsistente Formatvorlagen
      - Masterfolien fuer Einheitlichkeit
      - 6x6-Regel: Max. 6 Punkte, max. 6 Woerter

  GOOGLE SLIDES:
    VORTEILE:
      - Kollaboration in Echtzeit
      - Keine Installation noetig
      - Einfache Freigabe

  ALTERNATIVEN:
    - Keynote (Apple) - Elegantes Design
    - Canva - Einfache, schoene Vorlagen
    - Prezi - Nicht-lineare Praesentation
    - reveal.js - HTML-Praesentationen (fuer Entwickler)

================================================================================
TEIL 2: WISSENSMANAGEMENT UND NOTIZEN
================================================================================

2.1 NOTION
----------
Das All-in-One-Workspace fuer Teams und Einzelne.

  KONZEPT:
    - Flexibel: Notizen, Datenbanken, Wikis, Projekte
    - Block-basiert: Alles ist ein Block
    - Verknuepfbar: Datenbanken verlinken sich
    - Templatable: Vorlagen fuer alles

  ANWENDUNGSFAELLE:
    - Persoenliches Wiki
    - Team-Dokumentation
    - Projektmanagement
    - CRM-Alternative
    - Habit Tracker

  PRAXIS-TIPPS:
    - Mit einer Hauptdatenbank starten
    - Templates fuer wiederkehrende Eintraege
    - Verlinkungen nutzen statt Duplizierung
    - Nicht zu komplex aufbauen (YAGNI)

  KOSTEN:
    - Free: 1 Nutzer, begrenzt
    - Plus: 10$/Monat, mehr Features
    - Business: 18$/Monat, Team-Features

2.2 OBSIDIAN
------------
Lokale Markdown-Notizen mit Vernetzung.

  PHILOSOPHIE:
    - Daten gehoeren dir (lokale Dateien)
    - Plain Text (Markdown)
    - Bidirektionale Links ([[Link]])
    - Graph-Ansicht zeigt Verbindungen

  STAERKEN:
    - Keine Cloud-Abhaengigkeit
    - Schnell und responsiv
    - Erweiterbar durch Plugins
    - Versionierung mit Git moeglich
    - Datenschutz (alles lokal)

  ANWENDUNGSFAELLE:
    - Zettelkasten-Methode
    - Second Brain aufbauen
    - Tagebuch und Journaling
    - Forschungsnotizen

  PLUGINS (Empfehlungen):
    - Dataview: Datenbank-Abfragen
    - Calendar: Tagesnotizen
    - Excalidraw: Skizzen
    - Templater: Erweiterte Templates

  KOSTEN:
    - Obsidian Core: Kostenlos
    - Obsidian Sync: 10$/Monat (optional)
    - Obsidian Publish: 10$/Monat (optional)

2.3 ONENOTE
-----------
Microsofts digitales Notizbuch.

  STAERKEN:
    - Freiform-Notizen (ueberall klicken)
    - Handschrift-Unterstuetzung
    - Integration mit Microsoft 365
    - Offline verfuegbar

  STRUKTUR:
    - Notizbuecher > Abschnitte > Seiten

  WANN NUTZEN:
    - Meeting-Notizen
    - Handschriftliche Notizen (Tablet)
    - Integration in Office-Umgebung

2.4 EVERNOTE
------------
Der Klassiker unter den Notiz-Apps.

  HISTORIE:
    - Pionier der Cloud-Notizen
    - Verliert Marktanteil an Notion/Obsidian

  STAERKEN:
    - Web Clipper (Webseiten speichern)
    - OCR in Bildern
    - Tagging-System

  NACHTEILE:
    - Preiserhoehungen
    - Weniger Innovation
    - Proprietaeres Format

================================================================================
TEIL 3: PROJEKTMANAGEMENT
================================================================================

3.1 METHODEN-UEBERBLICK
-----------------------

  WASSERFALL:
    - Sequentielle Phasen
    - Planung vorab
    - Wenig Aenderungen
    - Tools: MS Project, Gantt-Charts

  AGILE/SCRUM:
    - Iterativ, Sprints (2-4 Wochen)
    - Regelmaessige Anpassung
    - Daily Standups
    - Tools: Jira, Azure DevOps

  KANBAN:
    - Visualisierung des Workflows
    - WIP-Limits (Work in Progress)
    - Kontinuierlicher Fluss
    - Tools: Trello, Kanban-Boards

3.2 TOOL-UEBERSICHT
-------------------

  JIRA:
  -----
  Der Standard fuer Software-Teams.

    FEATURES:
      - Scrum und Kanban Boards
      - Epics, Stories, Tasks
      - Sprints und Backlog
      - Workflows konfigurierbar
      - Integration mit Entwicklertools

    WANN NUTZEN:
      - Software-Entwicklung
      - Grosse Teams
      - Komplexe Projekte

    NACHTEILE:
      - Steep Learning Curve
      - Kann ueberladen werden
      - Kosten steigen mit Team-Groesse

  TRELLO:
  -------
  Einfaches Kanban fuer alle.

    KONZEPT:
      - Boards > Listen > Karten
      - Drag-and-Drop
      - Power-Ups fuer Erweiterungen

    STAERKEN:
      - Intuitiv und schnell
      - Visuell ansprechend
      - Gut fuer kleine Teams

    WANN NUTZEN:
      - Einfache Projekte
      - Persoenliche Organisation
      - Kleine Teams

  ASANA:
  ------
  Projekt- und Aufgabenmanagement.

    FEATURES:
      - Listen-, Board- und Zeitleistenansicht
      - Workflows und Automatisierungen
      - Portfolios fuer Projektueberblick
      - Gute Team-Funktionen

  MICROSOFT PLANNER:
  ------------------
  Kanban in Microsoft 365.

    VORTEILE:
      - In M365 enthalten
      - Teams-Integration
      - Einfache Bedienung

    NACHTEILE:
      - Begrenzte Features
      - Keine erweiterten Reports

  NOTION (als PM-Tool):
  ---------------------
    - Flexible Datenbanken als Boards
    - Timeline-Ansicht
    - Verknuepfung mit Dokumentation
    - Gut fuer kleinere Teams

3.3 BEST PRACTICES PROJEKTMANAGEMENT
------------------------------------

  GRUNDSAETZE:
    1. Ein Tool pro Team (nicht vermischen)
    2. Einfachheit vor Features
    3. Konsistente Nutzung wichtiger als Tool-Wahl
    4. Regelmaeessige Pflege der Daten

  TYPISCHE FEHLER:
    - Zu viele Tools parallel
    - Ueberkonfiguration
    - Daten nicht aktuell halten
    - Tool-Wechsel ohne Migration

================================================================================
TEIL 4: KOMMUNIKATION UND KOLLABORATION
================================================================================

4.1 INSTANT MESSAGING
---------------------

  MICROSOFT TEAMS:
    FEATURES:
      - Chat (1:1 und Gruppen)
      - Kanaele fuer Themen
      - Videocalls
      - Dateien teilen
      - App-Integrationen

    BEST PRACTICES:
      - Kanaele nach Themen, nicht Personen
      - @-Mentions gezielt einsetzen
      - Nicht alles in Chat klaeren (async vs. sync)
      - Status nutzen (Beschaeftigt, Nicht stoeren)

  SLACK:
    KONZEPT:
      - Channels fuer Themen
      - Threads fuer Diskussionen
      - Apps und Workflows

    STAERKEN:
      - Intuitive UX
      - Viele Integrationen
      - Gute Suche

    KOSTEN:
      - Free: 90 Tage Historie
      - Pro: 7.25$/Monat

  DISCORD:
    URSPRUNG:
      - Gaming-Community
      - Jetzt auch Business-Nutzung

    BESONDERHEITEN:
      - Voice Channels (persistent)
      - Server-Struktur
      - Kostenlos fuer viele Features

4.2 VIDEOKONFERENZEN
--------------------

  ZOOM:
    STAERKEN:
      - Stabile Verbindung
      - Breakout Rooms
      - Webinar-Funktion
      - Virtuelle Hintergruende

    PRAXIS-TIPPS:
      - Immer mit Video (wenn moeglich)
      - Mute als Standard
      - Bildschirmfreigabe planen
      - Recording ankuendigen

  MICROSOFT TEAMS:
    VORTEILE:
      - In M365 integriert
      - Kalender-Integration
      - Zusammen-Modus

  GOOGLE MEET:
    VORTEILE:
      - Keine Installation (Browser)
      - In Google Workspace integriert
      - Einfache Teilnahme

4.3 DOKUMENTEN-KOLLABORATION
----------------------------

  GRUNDPRINZIPIEN:
    - Single Source of Truth (eine Version)
    - Versionierung nutzen
    - Berechtigungen klar definieren
    - Kommentare statt E-Mail

  SHAREPOINT / ONEDRIVE:
    - Unternehmens-Dateiverwaltung
    - Integration mit Office
    - Berechtigungsmanagement

  GOOGLE DRIVE:
    - Einfache Freigabe
    - Echtzeit-Bearbeitung
    - 15 GB kostenlos

  DROPBOX:
    - Sync-Fokus
    - Dropbox Paper fuer Dokumente

================================================================================
TEIL 5: AUTOMATISIERUNG UND INTEGRATION
================================================================================

5.1 NO-CODE AUTOMATISIERUNG
---------------------------

  MICROSOFT POWER AUTOMATE:
  -------------------------
  Workflows in Microsoft 365.

    ANWENDUNGSFAELLE:
      - E-Mail-Anhaenge automatisch speichern
      - Genehmigungsworkflows
      - Daten zwischen Systemen synchronisieren
      - Benachrichtigungen

    BEISPIEL-FLOW:
      "Wenn neue E-Mail mit Anhang ->
       Speichere Anhang in OneDrive ->
       Sende Teams-Nachricht"

  ZAPIER:
  -------
  Web-App-Integration.

    KONZEPT:
      - Trigger: Loest Workflow aus
      - Action: Wird ausgefuehrt
      - Zaps: Verbinden Apps

    BEISPIELE:
      - Gmail -> Google Sheets
      - Typeform -> Slack
      - Stripe -> Mailchimp

    KOSTEN:
      - Free: 100 Tasks/Monat
      - Starter: 19.99$/Monat

  MAKE (ehem. INTEGROMAT):
  ------------------------
  Visueller Workflow-Builder.

    STAERKEN:
      - Komplexere Logik als Zapier
      - Guenstigere Preise
      - Visueller Editor

  N8N:
  ----
  Self-Hosted Automation.

    VORTEILE:
      - Open Source
      - Keine Beschraenkungen bei Self-Hosting
      - Datenschutz (eigene Infrastruktur)
      - Technisch flexibel

    NACHTEILE:
      - Technisches Setup noetig
      - Wartung selbst verantworten

5.2 ENTWICKLER-TOOLS
--------------------

  GIT / GITHUB / GITLAB:
    - Versionskontrolle fuer Code
    - Collaboration fuer Entwickler
    - CI/CD-Pipelines
    - Issue Tracking

  VISUAL STUDIO CODE:
    - Code-Editor
    - Erweiterbar durch Extensions
    - Integriertes Terminal
    - Git-Integration

  POSTMAN:
    - API-Testing
    - Dokumentation
    - Collections fuer Teams

================================================================================
TEIL 6: SPEZIALISIERTE TOOLS
================================================================================

6.1 DESIGN UND VISUALISIERUNG
-----------------------------

  FIGMA:
    - UI/UX Design
    - Kollaboration in Echtzeit
    - Prototyping
    - Design Systems

  MIRO / MURAL:
    - Digitale Whiteboards
    - Workshops remote
    - Brainstorming

  CANVA:
    - Einfaches Grafikdesign
    - Vorlagen fuer alles
    - Social Media Posts

  EXCALIDRAW:
    - Handgezeichnete Diagramme
    - Open Source
    - Schnell und einfach

6.2 DIAGRAMME UND MODELLIERUNG
------------------------------

  LUCIDCHART:
    - Flowcharts
    - Netzwerkdiagramme
    - UML

  DRAW.IO (diagrams.net):
    - Kostenlos
    - Desktop oder Web
    - Viele Vorlagen

  PLANTUML:
    - Diagramme aus Text
    - Versionierbar
    - UML, Sequenz, Aktivitaet

6.3 PASSWORT-MANAGER
--------------------

  BITWARDEN:
    - Open Source
    - Self-Hosting moeglich
    - Kostenlose Basisversion

  1PASSWORD:
    - Team-Features
    - Gute UX
    - Business-Fokus

  KEEPASS:
    - Lokal, Open Source
    - Maximale Kontrolle

6.4 ZEITERFASSUNG
-----------------

  TOGGL:
    - Einfaches Time Tracking
    - Reports
    - Pomodoro-Timer

  CLOCKIFY:
    - Kostenlos
    - Team-Funktionen

  TIMELY:
    - Automatisches Tracking
    - KI-basiert

================================================================================
TEIL 7: BACH-INTEGRATION
================================================================================

7.1 EMPFOHLENE TOOL-KOMBINATIONEN
---------------------------------

  FUER EINZELPERSONEN:
    - Obsidian fuer Notizen und Wissen
    - Todoist oder TickTick fuer Aufgaben
    - n8n fuer Automatisierung (technik-affin)
    - Bitwarden fuer Passwoerter

  FUER KLEINE TEAMS:
    - Notion fuer Dokumentation und Projekte
    - Slack oder Discord fuer Kommunikation
    - Google Workspace oder M365 fuer Office

  FUER UNTERNEHMEN:
    - Microsoft 365 (Teams, SharePoint, etc.)
    - Jira fuer Entwicklung
    - Confluence fuer Dokumentation
    - Power Automate fuer Workflows

7.2 BACH-SPEZIFISCHE EMPFEHLUNGEN
---------------------------------

  DOCUMENTATION:
    - Wiki-Dateien in Markdown/Text
    - Versionierung via Git wo moeglich

  AUTOMATISIERUNG:
    - n8n fuer komplexe Workflows
    - Power Automate bei M365-Umgebung
    - Python-Scripts fuer spezifische Aufgaben

  NOTIZEN UND WISSEN:
    - Obsidian fuer lokale Wissensbasis
    - Verlinkung mit BACH-Wiki

================================================================================

ZUSAMMENFASSUNG
===============

  KERNPRINZIPIEN BEI TOOL-WAHL:
    1. Weniger ist mehr - nicht zu viele Tools
    2. Konsistenz vor Features
    3. Team-Akzeptanz wichtiger als Funktionsumfang
    4. Datenschutz und Datenhoheit beachten
    5. Integrationsfaehigkeit pruefen

  DIE WICHTIGSTEN TOOLS:
    - Tabellen: Excel oder Google Sheets
    - Notizen: Obsidian oder Notion
    - Projekte: Jira, Trello oder Asana
    - Kommunikation: Teams oder Slack
    - Automatisierung: Power Automate, Zapier, n8n

  MERKSATZ:
    "Das beste Tool ist das, das genutzt wird.
     Einfachheit schlaegt Features."

================================================================================

ARTIKEL IN DIESEM BEREICH
=========================
  wiki/it_tools/excel_formeln.txt
  wiki/it_tools/excel_tricks.txt

GEPLANTE ARTIKEL
================
  [ ] powerpoint_tipps.txt
  [ ] notion_einfuehrung.txt
  [ ] obsidian_workflows.txt
  [ ] n8n_grundlagen.txt
  [ ] projektmanagement_vergleich.txt

SIEHE AUCH
==========
  wiki/methoden/visualisierung/
  wiki/management/
  wiki/automatisierung/
  wiki/n8n.txt

================================================================================
[Ende des Artikels - IT-TOOLS UEBERSICHT]
================================================================================
