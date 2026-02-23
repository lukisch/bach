# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: Tanenbaum (Modern Operating Systems), Silberschatz (Operating System Concepts),
#          Linux Kernel Documentation, Microsoft Docs, IEEE/ACM Computing Surveys

BETRIEBSSYSTEME
===============

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

EINFUEHRUNG
===========
Ein Betriebssystem (engl. Operating System, OS) ist die fundamentale Software,
die als Vermittler zwischen Hardware und Anwendungsprogrammen fungiert. Es
verwaltet Systemressourcen, stellt Dienste bereit und ermoeglicht die
Ausfuehrung von Programmen in einer kontrollierten Umgebung.

Hauptaufgaben eines Betriebssystems:
  - Abstraktion der Hardware fuer Anwendungen
  - Ressourcenverwaltung (CPU, Speicher, E/A-Geraete)
  - Bereitstellung einer Benutzerschnittstelle
  - Sicherheit und Zugriffskontrolle
  - Fehlererkennung und -behandlung


GRUNDFUNKTIONEN
===============

  PROZESSVERWALTUNG
  -----------------
  Ein Prozess ist ein Programm in Ausfuehrung mit eigenem Adressraum,
  Registerzustand und Systemressourcen.

  Prozesszustaende:
    - NEU:       Prozess wird erstellt
    - BEREIT:    Wartet auf CPU-Zuteilung
    - LAUFEND:   Wird aktuell ausgefuehrt
    - WARTEND:   Wartet auf E/A oder Ereignis
    - BEENDET:   Ausfuehrung abgeschlossen

  Prozess vs. Thread:
    Prozess:
      - Eigener Adressraum
      - Unabhaengige Ressourcen
      - Hoher Overhead beim Wechsel
      - Isoliert von anderen Prozessen

    Thread (Leichtgewichtsprozess):
      - Teilt Adressraum mit anderen Threads
      - Gemeinsame Ressourcen im Prozess
      - Geringer Overhead beim Wechsel
      - Kommunikation ueber gemeinsamen Speicher


  SCHEDULING-ALGORITHMEN
  ----------------------
  Der Scheduler entscheidet, welcher Prozess CPU-Zeit erhaelt.

  Non-preemptive (kooperativ):
    - First-Come-First-Served (FCFS)
      Prozesse werden in Ankunftsreihenfolge abgearbeitet.
      Problem: Convoy-Effekt (lange Prozesse blockieren kurze)

    - Shortest Job First (SJF)
      Kuerzester Prozess zuerst.
      Optimal fuer durchschnittliche Wartezeit.

  Preemptive (unterbrechbar):
    - Round Robin (RR)
      Jeder Prozess erhaelt feste Zeitscheibe (Quantum).
      Typisch: 10-100 Millisekunden.
      Fairness, aber hoher Context-Switch-Overhead.

    - Priority Scheduling
      Prozesse nach Prioritaet geordnet.
      Problem: Starvation (niedrige Prioritaet wird nie bedient)
      Loesung: Aging (Prioritaet steigt mit Wartezeit)

    - Multilevel Feedback Queue
      Mehrere Warteschlangen mit unterschiedlichen Prioritaeten.
      Prozesse koennen zwischen Queues wechseln.
      Standard in modernen Systemen.


  DEADLOCKS
  ---------
  Vier Bedingungen fuer Deadlock (alle muessen erfuellt sein):
    1. Mutual Exclusion: Ressourcen nicht teilbar
    2. Hold and Wait: Prozess haelt Ressourcen und wartet auf weitere
    3. No Preemption: Ressourcen nicht entziehbar
    4. Circular Wait: Zyklische Abhaengigkeit

  Strategien:
    - Prevention:  Eine Bedingung verhindern
    - Avoidance:   Banker's Algorithm (sichere Zustaende)
    - Detection:   Zyklen im Ressourcen-Graph erkennen
    - Recovery:    Prozess abbrechen oder Ressourcen entziehen


  INTER-PROCESS COMMUNICATION (IPC)
  ---------------------------------
    - Pipes:           Unidirektionaler Datenstrom
    - Named Pipes:     Persistente Pipes mit Namen
    - Message Queues:  Asynchrone Nachrichten
    - Shared Memory:   Gemeinsamer Speicherbereich (schnellste Methode)
    - Sockets:         Netzwerkkommunikation
    - Signals:         Asynchrone Benachrichtigungen
    - Semaphore:       Synchronisation (zaehlerbasiert)
    - Mutex:           Gegenseitiger Ausschluss (binaer)


SPEICHERVERWALTUNG
==================

  KONZEPTE
  --------
  Virtueller Speicher:
    Jeder Prozess sieht eigenen, zusammenhaengenden Adressraum.
    Unabhaengig vom physischen Speicher.
    Ermoeglicht Auslagerung auf Festplatte (Swapping).

  Paging:
    - Speicher in feste Bloecke unterteilt (Pages, typisch 4 KB)
    - Page Table uebersetzt virtuelle zu physischen Adressen
    - Translation Lookaside Buffer (TLB) als Cache
    - Page Fault: Seite nicht im RAM -> nachladen

  Page Replacement Algorithmen:
    - FIFO:    Aelteste Seite ersetzen (einfach, suboptimal)
    - LRU:     Least Recently Used (gut, aufwaendig)
    - Clock:   Approximation von LRU (praktikabel)
    - Optimal: Ersetze Seite mit spaetester Nutzung (theoretisch)

  Segmentierung:
    - Logische Unterteilung (Code, Daten, Stack)
    - Variable Groessen
    - Externe Fragmentierung moeglich

  Memory Management Unit (MMU):
    Hardware-Komponente fuer Adressueberetzung.
    Prueft Zugriffsrechte (Read, Write, Execute).
    Loest Page Faults aus.


DATEISYSTEME
============

  GRUNDLAGEN
  ----------
  Ein Dateisystem organisiert Daten auf Speichermedien und stellt
  eine hierarchische Struktur (Verzeichnisse, Dateien) bereit.

  Komponenten:
    - Superblock:     Metadaten des Dateisystems
    - Inode:          Metadaten einer Datei (Groesse, Rechte, Zeiger)
    - Datenblock:     Eigentlicher Dateiinhalt
    - Verzeichnis:    Zuordnung Name -> Inode

  Journaling:
    Protokolliert Aenderungen vor Ausfuehrung.
    Bei Absturz: Konsistente Wiederherstellung.
    Typen: Metadata-only, Full Journaling, Ordered


  DATEISYSTEME IM VERGLEICH
  -------------------------
  Windows:
    FAT32:
      - Einfach, hoechste Kompatibilitaet
      - Max. Dateigroesse: 4 GB
      - Max. Partitionsgroesse: 2 TB
      - Kein Journaling, keine Rechte

    NTFS:
      - Standard fuer Windows
      - Journaling, Kompression, Verschluesselung
      - ACL-basierte Berechtigungen
      - Max. Dateigroesse: 16 EB (theoretisch)

  Linux:
    ext4:
      - Standard fuer viele Linux-Distributionen
      - Journaling, Extents, Delayed Allocation
      - Max. Dateigroesse: 16 TB
      - Max. Partitionsgroesse: 1 EB

    Btrfs:
      - Copy-on-Write (CoW)
      - Snapshots, Kompression, RAID
      - Checksummen fuer Datenintegritaet

    XFS:
      - Hochperformant fuer grosse Dateien
      - Skaliert gut mit vielen Prozessoren

  macOS:
    APFS (Apple File System):
      - Copy-on-Write
      - Snapshots, Klonen, Verschluesselung
      - Optimiert fuer SSD
      - Ersetzt HFS+ seit 2017


BETRIEBSSYSTEME IM UEBERBLICK
=============================

  LINUX
  -----
  Open-Source, Unix-aehnlich, 1991 von Linus Torvalds.

  Kernel-Architektur:
    - Monolithisch mit ladbaren Modulen
    - Multitasking, Multiuser
    - POSIX-kompatibel

  Distributionen:
    Server:     Debian, Ubuntu Server, RHEL, Rocky Linux
    Desktop:    Ubuntu, Fedora, Linux Mint, Arch
    Embedded:   Yocto, Buildroot

  Wichtige Konzepte:
    - Alles ist eine Datei (/dev, /proc, /sys)
    - Shell als primaere Schnittstelle
    - Paketmanager (apt, dnf, pacman)


  WINDOWS
  -------
  Proprietaer, Microsoft, seit 1985.

  Architektur:
    - Hybrid-Kernel (NT-Kernel)
    - Hardware Abstraction Layer (HAL)
    - Win32 API, .NET Framework

  Versionen (aktuell):
    - Windows 11: Desktop
    - Windows Server 2022: Server

  Besonderheiten:
    - Registry als zentrale Konfiguration
    - Active Directory fuer Netzwerke
    - WSL: Linux-Subsystem integriert


  MACOS
  -----
  Unix-basiert (Darwin/XNU), Apple, seit 2001.

  Architektur:
    - XNU Hybrid-Kernel (Mach + BSD)
    - Cocoa/Cocoa Touch Frameworks
    - Metal fuer Grafik

  Besonderheiten:
    - Nur auf Apple-Hardware
    - Starke Integration mit iOS
    - UNIX-zertifiziert


  MOBILE BETRIEBSSYSTEME
  ----------------------
  Android:
    - Linux-Kernel
    - Java/Kotlin Anwendungen
    - Open Source (AOSP), Google-Dienste optional
    - Groesster Marktanteil weltweit

  iOS:
    - XNU-Kernel (wie macOS)
    - Swift/Objective-C Anwendungen
    - Geschlossenes System
    - Strenge App Store Kontrolle


VIRTUALISIERUNG
===============

  VIRTUELLE MASCHINEN
  -------------------
  Vollstaendige Emulation eines Computersystems.

  Hypervisor-Typen:
    Typ 1 (Bare-Metal):
      - Direkt auf Hardware
      - VMware ESXi, Microsoft Hyper-V, Xen
      - Bessere Performance

    Typ 2 (Hosted):
      - Auf Host-Betriebssystem
      - VirtualBox, VMware Workstation
      - Einfacher zu installieren


  CONTAINER
  ---------
  Leichtgewichtige Isolation auf Betriebssystemebene.

  Docker:
    - Container teilen Kernel mit Host
    - Images als unveraenderliche Vorlagen
    - Schneller Start, geringer Overhead
    - Dockerfile beschreibt Build-Prozess

  Container-Orchestrierung:
    - Kubernetes (K8s): Standard fuer Produktion
    - Docker Swarm: Einfacher, weniger Features
    - Podman: Docker-kompatibel, rootless


  WINDOWS SUBSYSTEM FOR LINUX (WSL)
  ---------------------------------
  WSL2:
    - Echter Linux-Kernel in leichtgewichtiger VM
    - Volle Systemaufruf-Kompatibilitaet
    - Integration mit Windows (Dateizugriff, GUI)
    - Ideal fuer Entwickler


BEST PRACTICES
==============
  - Regelmaessige Updates und Patches einspielen
  - Principle of Least Privilege anwenden
  - Backups automatisieren und testen
  - Monitoring fuer Ressourcenauslastung einrichten
  - Sicherheitshärtung (Firewall, SELinux/AppArmor)
  - Dokumentation der Systemkonfiguration pflegen


SIEHE AUCH
==========
  wiki/informatik/hardware/
  wiki/devops/
  wiki/informatik/netzwerke/
  wiki/sicherheit/

