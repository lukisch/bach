# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: Computer Architecture (Hennessy/Patterson), Intel/AMD Dokumentation, IEEE Standards

COMPUTER-HARDWARE
=================

Stand: 2026-02-05

DEFINITION
==========
Computer-Hardware bezeichnet alle physischen Komponenten eines Computersystems.
Im Gegensatz zur Software (Programme) ist Hardware greifbar und besteht aus
elektronischen, mechanischen und optischen Bauteilen.


ZENTRALE VERARBEITUNGSEINHEIT (CPU)
===================================
Die CPU ist das "Gehirn" des Computers und fuehrt Berechnungen aus.

  Kernkomponenten:
  ----------------
    ALU (Arithmetic Logic Unit)     - Mathematische Operationen
    Control Unit                    - Befehlssteuerung
    Register                        - Schnellspeicher fuer Operanden
    Cache (L1, L2, L3)              - Zwischenspeicher fuer haeufige Daten

  Kennzahlen:
  -----------
    Taktfrequenz (GHz)              - Anzahl Zyklen pro Sekunde
    Kernanzahl                      - Parallele Verarbeitungseinheiten
    IPC (Instructions per Cycle)    - Effizienz pro Taktzyklus
    TDP (Thermal Design Power)      - Waermeleistung in Watt

  Befehlssatz-Architekturen:
  --------------------------
    x86/x86-64    - Intel/AMD, CISC-Architektur, Desktop/Server
    ARM           - Mobile Geraete, energieeffizient, RISC
    RISC-V        - Open-Source ISA, aufstrebend

  Beispiel: CPU-Informationen unter Linux abrufen
  ------------------------------------------------
    $ lscpu
    Architecture:          x86_64
    CPU(s):                8
    Model name:            Intel Core i7-12700K
    CPU MHz:               3600.000
    L1d cache:             384 KiB
    L2 cache:              10 MiB
    L3 cache:              25 MiB


ARBEITSSPEICHER (RAM)
=====================
RAM (Random Access Memory) ist der fluechtige Hauptspeicher.

  Eigenschaften:
  --------------
    Fluechtig               - Daten gehen bei Stromverlust verloren
    Wahlfreier Zugriff      - Jede Adresse direkt erreichbar
    Schnell                 - Nanosekunden Zugriffszeit

  Typen:
  ------
    DDR4                    - 2133-3200 MHz, Standard bis 2024
    DDR5                    - 4800-8400 MHz, ab 2022, hoehere Bandbreite
    ECC (Error Correcting)  - Fehlerkorrektur fuer Server

  Kennzahlen:
  -----------
    Kapazitaet (GB)         - Gesamtspeicher
    Bandbreite (GB/s)       - Datendurchsatz
    Latenz (CL)             - Verzoegerung bei Zugriff
    Taktrate (MHz)          - Geschwindigkeit

  Speicherhierarchie (schnell zu langsam):
  ----------------------------------------
    Register     < 1 ns     (wenige Bytes)
    L1 Cache     ~1 ns      (32-64 KB)
    L2 Cache     ~4 ns      (256 KB - 1 MB)
    L3 Cache     ~10 ns     (8-64 MB)
    RAM          ~100 ns    (8-128 GB)
    SSD          ~100 us    (256 GB - 8 TB)
    HDD          ~10 ms     (1-20 TB)


MASSENSPEICHER
==============
Persistente Speichermedien fuer Daten und Programme.

  HDD (Hard Disk Drive):
  ----------------------
    - Magnetische Speicherung auf rotierenden Scheiben
    - Hohe Kapazitaet (bis 20+ TB)
    - Guenstiger Preis pro GB
    - Mechanisch, stoerungsanfaellig
    - Langsam (100-200 MB/s)

  SSD (Solid State Drive):
  ------------------------
    - Flash-Speicher (NAND)
    - Keine mechanischen Teile
    - Schnell (500-7000 MB/s bei NVMe)
    - Begrenzte Schreibzyklen
    - Teurer pro GB

  NVMe (Non-Volatile Memory Express):
  -----------------------------------
    - Protokoll fuer SSDs ueber PCIe
    - Extrem schnell (bis 7000 MB/s lesen)
    - Niedrige Latenz
    - Standard fuer moderne Systeme

  RAID (Redundant Array of Independent Disks):
  --------------------------------------------
    RAID 0    - Striping, keine Redundanz, maximale Geschwindigkeit
    RAID 1    - Mirroring, volle Redundanz, halbe Kapazitaet
    RAID 5    - Striping + Paritaet, guter Kompromiss
    RAID 6    - Wie RAID 5, aber mit doppelter Paritaet
    RAID 10   - Kombination aus RAID 1 und 0


MAINBOARD (MOTHERBOARD)
=======================
Die Hauptplatine verbindet alle Komponenten.

  Komponenten:
  ------------
    Chipsatz              - Kommunikation zwischen CPU und Peripherie
    BIOS/UEFI             - Firmware fuer Boot-Vorgang
    RAM-Slots             - Steckplaetze fuer Arbeitsspeicher
    PCIe-Slots            - Erweiterungskarten (GPU, NVMe, etc.)
    SATA/M.2              - Speicher-Anschluesse
    USB-Header            - USB-Anschluesse
    Audio-Codec           - Onboard-Sound

  Formfaktoren:
  -------------
    ATX           305x244 mm    Standard Desktop
    Micro-ATX     244x244 mm    Kompakter Desktop
    Mini-ITX      170x170 mm    Kompakt-PCs
    E-ATX         305x330 mm    Workstations/Server


GRAFIKKARTE (GPU)
=================
Spezialisiert auf parallele Berechnungen und Grafikausgabe.

  Architektur:
  ------------
    Shader-Cores        - Tausende kleine Rechenkerne
    VRAM                - Dedizierter Grafikspeicher (GDDR6/HBM)
    TMUs                - Textur-Mapping-Einheiten
    ROPs                - Render Output Units

  Einsatzgebiete:
  ---------------
    Gaming              - 3D-Grafik-Rendering
    ML/AI               - Neuronale Netze (CUDA, ROCm)
    Wissenschaft        - Parallele Berechnungen
    Mining              - Kryptowaehrungen (abnehmend)

  Schnittstellen:
  ---------------
    CUDA                - NVIDIA proprietaer
    OpenCL              - Offener Standard
    Vulkan/DirectX      - Grafik-APIs


PERIPHERIE
==========
Ein- und Ausgabegeraete.

  Eingabe:
  --------
    Tastatur            - PS/2 oder USB
    Maus                - Optisch/Laser, kabellos
    Scanner             - Dokumente digitalisieren
    Mikrofon            - Audio-Eingabe

  Ausgabe:
  --------
    Monitor             - LCD, OLED, verschiedene Auflösungen
    Drucker             - Tintenstrahl, Laser
    Lautsprecher        - Audio-Ausgabe

  Schnittstellen:
  ---------------
    USB (2.0/3.0/4)     - Universal, bis 40 Gbit/s (USB4)
    DisplayPort         - Video, bis 8K
    HDMI                - Video + Audio
    Thunderbolt         - Vielseitig, bis 80 Gbit/s (TB4)


EMBEDDED SYSTEMS
================
Spezialisierte Computer in Geraeten.

  Eigenschaften:
  --------------
    - Dedizierte Aufgabe
    - Ressourcenbeschraenkt
    - Echtzeit-Anforderungen oft kritisch
    - Niedriger Stromverbrauch

  Beispiele:
  ----------
    Mikrocontroller     - Arduino, ESP32, STM32
    Single-Board-PC     - Raspberry Pi, BeagleBone
    IoT-Geraete         - Sensoren, Smart Home
    Industriesteuerung  - PLCs, SCADA-Systeme


BEST PRACTICES
==============

  Hardware-Auswahl:
  -----------------
    1. Anforderungen definieren (Workload analysieren)
    2. Kompatibilitaet pruefen (Mainboard <-> CPU <-> RAM)
    3. Kuehlung bedenken (TDP der Komponenten)
    4. Zukunftssicherheit (Upgrade-Pfade)
    5. Preis-Leistung evaluieren

  Wartung:
  --------
    - Regelmaessig Staub entfernen
    - Waermeleitpaste alle 2-3 Jahre erneuern
    - Firmware/BIOS aktuell halten
    - SMART-Werte der Festplatten ueberwachen

  Monitoring-Befehle (Linux):
  ---------------------------
    $ sensors                  # CPU-Temperaturen
    $ smartctl -a /dev/sda     # Festplatten-Gesundheit
    $ free -h                  # RAM-Auslastung
    $ lspci                    # PCI-Geraete auflisten


TYPISCHE SYSTEMKONFIGURATIONEN
==============================

  Office/Home:
  ------------
    CPU: Intel i3/AMD Ryzen 3, 4 Kerne
    RAM: 8-16 GB DDR4
    Storage: 256-512 GB SSD
    GPU: Integriert

  Entwickler-Workstation:
  -----------------------
    CPU: Intel i7/AMD Ryzen 7, 8+ Kerne
    RAM: 32-64 GB DDR5
    Storage: 1-2 TB NVMe SSD
    GPU: Mittelklasse (optional)

  ML/AI Workstation:
  ------------------
    CPU: Intel i9/AMD Ryzen 9 oder Threadripper
    RAM: 64-128 GB DDR5 ECC
    Storage: 2+ TB NVMe
    GPU: NVIDIA RTX 4090 oder A100 (CUDA erforderlich)

  Server:
  -------
    CPU: Intel Xeon / AMD EPYC
    RAM: 128+ GB ECC
    Storage: RAID-Array mit Enterprise-SSDs
    GPU: Optional fuer ML-Workloads


SIEHE AUCH
==========
  wiki/informatik/betriebssysteme/    Betriebssysteme
  wiki/informatik/netzwerke/          Netzwerk-Hardware
  wiki/informatik/cloud_computing/    Cloud-Infrastruktur
  wiki/informatik/devops/             Container und VMs
