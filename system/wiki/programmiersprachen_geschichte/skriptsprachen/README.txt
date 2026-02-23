# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: MDN Web Docs, php.net, ruby-lang.org, perl.org, nodejs.org

PROGRAMMIERSPRACHEN: SKRIPTSPRACHEN
===================================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
EINLEITUNG
================================================================================

Skriptsprachen sind Programmiersprachen, die typischerweise interpretiert
statt kompiliert werden und fuer schnelle Entwicklung, Automatisierung
und dynamische Anwendungen konzipiert sind. Sie zeichnen sich durch
dynamische Typisierung, hohe Abstraktionsebene und geringe Einstiegshuerde
aus.

Der Begriff "Skriptsprache" stammt aus der fruehen Verwendung fuer kleine
Programme ("Scripts"), die Betriebssystemaufgaben automatisierten. Heute
treiben Skriptsprachen komplexe Web-Anwendungen, wissenschaftliche
Berechnungen und Enterprise-Systeme an.

================================================================================
HISTORISCHE ENTWICKLUNG
================================================================================

DIE SHELL-AERA (1970er)
-----------------------

  1971: Unix Shell (sh)
        - Ken Thompson, Bell Labs
        - Interaktive Befehlsausfuehrung
        - Pipes und Redirections
        - Grundlage aller Shell-Scripte

  1977: Bourne Shell (sh)
        - Stephen Bourne, Bell Labs
        - Programmierbare Shell
        - Control Flow (if, while, for)
        - Bis heute relevant (/bin/sh)

  1978: AWK
        - Aho, Weinberger, Kernighan
        - Textverarbeitung
        - Pattern-Action-Modell
        - Einfluss auf Perl

DIE AUTOMATIONS-AERA (1980er)
-----------------------------

  1987: Perl
        - Larry Wall
        - "Practical Extraction and Report Language"
        - Vereinigt sh, AWK, sed

        Eigenschaften:
          * Maechtige regulaere Ausdruecke
          * "There's more than one way to do it" (TMTOWTDI)
          * CPAN (Comprehensive Perl Archive Network)
          * CGI-Scripting fuer fruehes Web
          * Textverarbeitung und Systemadministration

        Versionen:
          Perl 4 (1991): Stabilitaet
          Perl 5 (1994): OOP, References, Modules
          Perl 6/Raku (2015): Komplette Neugestaltung

  1988: Tcl (Tool Command Language)
        - John Ousterhout
        - Einbettbare Sprache
        - Tk GUI-Toolkit
        - Erwartungshaltung-Konzept

  1989: Bash (Bourne Again Shell)
        - Brian Fox, GNU Project
        - POSIX-kompatibel
        - Erweitert Bourne Shell
        - Standard auf Linux
        - Arrays, Funktionen, Job Control

DIE WEB-REVOLUTION (1990er)
---------------------------

  1991: Python
        - Guido van Rossum
        - Lesbarkeit als Designprinzip
        - "Batteries included"
        - Siehe separater Artikel

  1993: Lua
        - Roberto Ierusalimschy (PUC-Rio, Brasilien)
        - Leichtgewichtig und einbettbar
        - Tabellen als universelle Datenstruktur

        Eigenschaften:
          * Minimaler Kern (~20.000 Zeilen C)
          * Coroutines
          * Metatables fuer OOP
          * Garbage Collection

        Anwendung:
          * Spieleentwicklung (World of Warcraft, Roblox)
          * Embedded Systems
          * Nginx Konfiguration (OpenResty)
          * Redis Scripting

  1994: PHP
        - Rasmus Lerdorf
        - "Personal Home Page Tools"

        Evolution:
          PHP/FI (1995): Forms Interpreter
          PHP 3 (1998): Zend Engine, Zeev Suraski & Andi Gutmans
          PHP 4 (2000): Zend Engine 1.0
          PHP 5 (2004): Vollwertige OOP, PDO
          PHP 7 (2015): Performance-Revolution (2x schneller)
          PHP 8 (2020): JIT, Attributes, Union Types

        Eigenschaften:
          * In HTML eingebettet
          * Server-side Rendering
          * Riesiges Oekosystem
          * WordPress (43% aller Websites)
          * Laravel, Symfony Frameworks

  1995: JavaScript
        - Brendan Eich, Netscape
        - In 10 Tagen entwickelt
        - Urspruenglich "Mocha", dann "LiveScript"

        Meilensteine:
          1995: Netscape Navigator 2.0
          1996: JScript (Microsoft IE)
          1997: ECMAScript 1 (Standardisierung)
          2005: AJAX (Web 2.0)
          2008: V8 Engine (Google Chrome)
          2009: Node.js (Server-side JavaScript)
          2015: ES6/ES2015 (Moderne Syntax)
          2016+: Jaehrliche Updates (ES2016, ES2017, ...)

        Bedeutung:
          * Einzige native Browser-Sprache
          * Full-Stack moeglich (Node.js)
          * Groesstes Paket-Oekosystem (npm)
          * TypeScript als typisierte Variante

  1995: Ruby
        - Yukihiro "Matz" Matsumoto
        - Japan
        - "Programmer Happiness"

        Philosophie:
          * "Principle of Least Surprise"
          * Lesbarkeit und Eleganz
          * "Alles ist ein Objekt"
          * Smalltalk + Perl + Lisp

        Eigenschaften:
          * Blocks, Procs, Lambdas
          * Dynamische Typisierung
          * Metaprogrammierung
          * Offene Klassen
          * Gems (Paketsystem)

        Ruby on Rails (2004):
          * David Heinemeier Hansson
          * "Convention over Configuration"
          * "Don't Repeat Yourself" (DRY)
          * MVC-Framework
          * Praegte moderne Webentwicklung
          * Einfluss auf Django, Laravel, etc.

  1996: Active Server Pages (ASP)
        - Microsoft
        - VBScript/JScript
        - Spaeter: ASP.NET (2002)

DIE MODERNE AERA (2000er-heute)
-------------------------------

  2007: PowerShell
        - Microsoft
        - Objektorientierte Shell
        - .NET-Integration
        - Cross-Platform (seit v6)
        - Cmdlets statt Text-Pipelines

  2009: Node.js
        - Ryan Dahl
        - JavaScript auf dem Server
        - V8 Engine
        - Event-driven, non-blocking I/O
        - npm als Paketmanager

        Einfluss:
          * Full-Stack JavaScript
          * Microservices
          * Real-Time-Anwendungen
          * Serverless Computing

  2009: CoffeeScript
        - Jeremy Ashkenas
        - Kompiliert zu JavaScript
        - Beeinflusste ES6-Syntax
        - Heute: Durch ES6 abgeloest

  2012: TypeScript
        - Microsoft, Anders Hejlsberg
        - JavaScript mit statischer Typisierung
        - Kompiliert zu JavaScript
        - Heute: De-facto-Standard fuer grosse JS-Projekte

  2014: Swift Playgrounds / REPL-Trend
        - Interaktive Entwicklung
        - Jupyter Notebooks
        - Observable (JavaScript)

================================================================================
CHARAKTERISTIKA VON SKRIPTSPRACHEN
================================================================================

INTERPRETATION VS. KOMPILIERUNG
-------------------------------
  Interpretation:
    - Code wird zur Laufzeit ausgefuehrt
    - Kein separater Kompilierungsschritt
    - Schnellere Entwicklungszyklen
    - Plattformunabhaengigkeit

  Moderne Realitaet:
    - JIT-Kompilierung (V8, PyPy, LuaJIT)
    - Bytecode-Zwischenstufe
    - Grenzen verschwimmen

DYNAMISCHE TYPISIERUNG
----------------------
  Eigenschaften:
    - Typen zur Laufzeit bestimmt
    - Variablen nicht deklariert
    - Flexible Datenstrukturen
    - Duck Typing ("If it walks like a duck...")

  Beispiel (Python):
    x = 5         # int
    x = "hello"   # str - gleiche Variable
    x = [1, 2, 3] # list

  Vor- und Nachteile:
    + Schnellere Entwicklung
    + Flexiblerer Code
    - Laufzeitfehler statt Kompilierfehler
    - Weniger IDE-Unterstuetzung

REPL (Read-Eval-Print Loop)
---------------------------
  - Interaktive Ausfuehrung
  - Experimentieren und Testen
  - Schnelles Prototyping

  Beispiel:
    $ python
    >>> 2 + 2
    4
    >>> "hello".upper()
    'HELLO'

HOHE ABSTRAKTIONSEBENE
----------------------
  - Automatische Speicherverwaltung
  - Eingebaute Datenstrukturen (Listen, Dictionaries)
  - String-Manipulation
  - Regulaere Ausdruecke

================================================================================
WICHTIGE SKRIPTSPRACHEN IM DETAIL
================================================================================

PERL
----
  Staerken:
    - Textverarbeitung und Regex
    - "Swiss Army Chainsaw"
    - Bioinformatik
    - Legacy-System-Automation

  Codebeispiel:
    #!/usr/bin/perl
    use strict;
    use warnings;

    # E-Mail-Adressen extrahieren
    while (<STDIN>) {
        while (/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g) {
            print "$1\n";
        }
    }

  Status heute:
    - Wartung von Legacy-Code
    - Systemadministration
    - Raku als Nachfolger

PHP
---
  Staerken:
    - Web-Entwicklung
    - Einfacher Einstieg
    - Guenstige Hosting-Optionen
    - Riesiges Oekosystem

  Codebeispiel:
    <?php
    // Datenbankabfrage mit PDO
    $pdo = new PDO('mysql:host=localhost;dbname=test', 'user', 'pass');
    $stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?');
    $stmt->execute([$_GET['id']]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);
    ?>

    <h1>Willkommen, <?= htmlspecialchars($user['name']) ?>!</h1>

  Frameworks:
    - Laravel (elegant, modern)
    - Symfony (Enterprise)
    - WordPress (CMS)
    - Drupal, Magento

RUBY
----
  Staerken:
    - Elegante Syntax
    - Metaprogrammierung
    - Webentwicklung (Rails)
    - DevOps (Chef, Puppet, Vagrant)

  Codebeispiel:
    # Elegante Syntax
    5.times { puts "Hello!" }

    # Blocks
    [1, 2, 3, 4, 5].select { |n| n.even? }.map { |n| n * 2 }
    # => [4, 8]

    # Klassen
    class Person
      attr_accessor :name, :age

      def initialize(name, age)
        @name = name
        @age = age
      end

      def greeting
        "Hi, I'm #{name}!"
      end
    end

  Status heute:
    - Weiterhin stark bei Startups
    - Rails immer noch relevant
    - Konkurrenz durch Node.js, Go

JAVASCRIPT
----------
  Staerken:
    - Browser-Monopol
    - Full-Stack moeglich
    - Groesstes Oekosystem
    - Asynchrone Programmierung

  Codebeispiel (Modern ES6+):
    // Arrow Functions, Destructuring, Template Literals
    const greet = ({ name, age }) => `Hello ${name}, you are ${age}`;

    // Async/Await
    async function fetchUser(id) {
        const response = await fetch(`/api/users/${id}`);
        const user = await response.json();
        return user;
    }

    // Classes
    class Animal {
        constructor(name) {
            this.name = name;
        }

        speak() {
            console.log(`${this.name} makes a sound.`);
        }
    }

  Frontend-Frameworks:
    - React (Meta/Facebook)
    - Vue.js (Evan You)
    - Angular (Google)
    - Svelte

  Backend (Node.js):
    - Express.js
    - Fastify
    - NestJS
    - Deno, Bun (Alternativen)

LUA
---
  Staerken:
    - Extrem leichtgewichtig
    - Schnelle Einbettung
    - Einfach zu erlernen
    - Coroutines

  Codebeispiel:
    -- Tabellen als universelle Datenstruktur
    local person = {
        name = "Alice",
        age = 30,
        greet = function(self)
            print("Hi, I'm " .. self.name)
        end
    }

    person:greet()  -- Syntactic sugar fuer person.greet(person)

    -- Metatables fuer OOP
    local Animal = {}
    Animal.__index = Animal

    function Animal:new(name)
        local obj = setmetatable({}, self)
        obj.name = name
        return obj
    end

BASH/SHELL
----------
  Staerken:
    - System-Administration
    - Automation
    - CI/CD-Pipelines
    - Universell auf Unix/Linux

  Codebeispiel:
    #!/bin/bash

    # Alle Log-Dateien aelter als 30 Tage loeschen
    find /var/log -name "*.log" -mtime +30 -delete

    # Backup mit Fehlerbehandlung
    backup_dir="/backup/$(date +%Y-%m-%d)"

    if mkdir -p "$backup_dir"; then
        tar -czf "$backup_dir/data.tar.gz" /data
        echo "Backup erfolgreich: $backup_dir"
    else
        echo "Fehler: Konnte Backup-Verzeichnis nicht erstellen" >&2
        exit 1
    fi

POWERSHELL
----------
  Staerken:
    - Windows-Administration
    - Objekt-Pipeline (nicht Text)
    - .NET-Integration
    - Cross-Platform (seit v6)

  Codebeispiel:
    # Alle Prozesse mit >100MB Memory
    Get-Process | Where-Object { $_.WorkingSet -gt 100MB } |
        Sort-Object WorkingSet -Descending |
        Select-Object Name, @{N='Memory(MB)';E={[math]::Round($_.WorkingSet/1MB,2)}}

    # Active Directory Benutzer erstellen
    New-ADUser -Name "Max Mustermann" `
               -GivenName "Max" `
               -Surname "Mustermann" `
               -UserPrincipalName "max.mustermann@firma.de" `
               -Path "OU=Users,DC=firma,DC=de"

================================================================================
ANWENDUNGSBEREICHE
================================================================================

WEB-ENTWICKLUNG
---------------
  Backend:
    - PHP (WordPress, Laravel)
    - JavaScript/Node.js (Express, Next.js)
    - Ruby (Rails)
    - Python (Django, Flask)

  Frontend:
    - JavaScript (React, Vue, Angular)
    - TypeScript

SYSTEM-ADMINISTRATION
---------------------
  - Bash/Shell (Linux/Unix)
  - PowerShell (Windows)
  - Python (Ansible, plattformuebergreifend)
  - Perl (Legacy)

DATENANALYSE / DATA SCIENCE
---------------------------
  - Python (Pandas, NumPy, Jupyter)
  - R (Statistik)
  - Julia (High-Performance)

SPIELEENTWICKLUNG
-----------------
  - Lua (Embedded Scripting)
  - Python (Pygame, Tools)
  - JavaScript (Browser Games)

DEVOPS / CI/CD
--------------
  - Bash (Skripte, Pipelines)
  - Python (Automation)
  - Ruby (Chef, Puppet, Vagrant)
  - Groovy (Jenkins)
  - YAML + Scripting

================================================================================
PERFORMANCE-BETRACHTUNGEN
================================================================================

  Reine Interpretation:
    - Am langsamsten
    - Einfachste Implementierung

  Bytecode-Kompilierung:
    - Python (.pyc), Ruby (YARV)
    - Zwischenschritt vor Interpretation

  JIT-Kompilierung:
    - V8 (JavaScript), PyPy, LuaJIT
    - Kann native Geschwindigkeit erreichen

  Typische Performance-Rangfolge:
    1. C/C++ (Referenz)
    2. LuaJIT, V8 JavaScript
    3. PyPy, PHP 8
    4. Standard Python, Ruby

================================================================================
ZUKUNFTSTRENDS
================================================================================

  - WebAssembly als Alternative zu JavaScript
  - TypeScript-aehnliche Typisierung fuer alle
  - Serverless Computing
  - Edge Computing
  - Bun, Deno als Node.js-Alternativen
  - AI-gestuetzte Code-Generierung

================================================================================
SIEHE AUCH
================================================================================

  wiki/webapps/frontend/
  wiki/webapps/backend/
  wiki/python/
  wiki/javascript/
  wiki/bash/
  wiki/powershell/
  wiki/programmiersprachen_geschichte/paradigmen/

================================================================================
WEITERFUEHRENDE RESSOURCEN
================================================================================

  Buecher:
    - "Learning Perl" (Randal Schwartz)
    - "Eloquent JavaScript" (Marijn Haverbeke)
    - "The Ruby Programming Language" (David Flanagan)
    - "Programming in Lua" (Roberto Ierusalimschy)
    - "PHP: The Right Way" (Online)

  Online:
    - developer.mozilla.org (MDN Web Docs)
    - php.net
    - ruby-lang.org
    - nodejs.org
    - lua.org

================================================================================
