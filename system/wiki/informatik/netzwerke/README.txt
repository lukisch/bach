# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: RFC-Standards, Cisco CCNA Curriculum, Tanenbaum "Computer Networks"

================================================================================
NETZWERKE - UMFASSENDER WIKI-ARTIKEL
================================================================================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
INHALTSVERZEICHNIS
================================================================================
  1. Einfuehrung in Netzwerke
  2. OSI-Referenzmodell
  3. TCP/IP-Modell
  4. Netzwerktopologien
  5. IP-Adressierung
  6. Wichtige Protokolle
  7. Routing und Switching
  8. DNS - Domain Name System
  9. DHCP - Dynamic Host Configuration Protocol
  10. Netzwerksicherheit
  11. Wireless Networks (WLAN)
  12. Diagnose und Troubleshooting
  13. Best Practices

================================================================================
1. EINFUEHRUNG IN NETZWERKE
================================================================================

  Ein Computernetzwerk verbindet mehrere Geraete zum Austausch von Daten
  und Ressourcen. Netzwerke bilden die Grundlage moderner Kommunikation
  und des Internets.

  NETZWERKTYPEN NACH REICHWEITE:
  ------------------------------
    PAN (Personal Area Network):
      - Reichweite: wenige Meter
      - Bluetooth, USB
      - Persoenliche Geraete

    LAN (Local Area Network):
      - Reichweite: Gebaeude/Campus
      - Ethernet, WLAN
      - Hohe Bandbreiten (1-100 Gbit/s)

    MAN (Metropolitan Area Network):
      - Reichweite: Stadt/Region
      - Verbindet mehrere LANs
      - Glasfaser-Backbone

    WAN (Wide Area Network):
      - Reichweite: global
      - Internet, MPLS
      - Verbindet geografisch verteilte Standorte

  UEBERTRAGUNGSMEDIEN:
  --------------------
    Kupferkabel:
      - Twisted Pair (Cat5e, Cat6, Cat6a, Cat7)
      - Koaxialkabel (veraltet fuer LANs)
      - Reichweite: max. 100m (Ethernet)

    Glasfaser:
      - Singlemode: lange Distanzen (km)
      - Multimode: kurze Distanzen (Rechenzentrum)
      - Immun gegen elektromagnetische Stoerungen

    Wireless:
      - WLAN (IEEE 802.11)
      - Mobilfunk (4G LTE, 5G)
      - Satellit

================================================================================
2. OSI-REFERENZMODELL
================================================================================

  Das OSI-Modell (Open Systems Interconnection) ist ein konzeptionelles
  Modell mit 7 Schichten zur Beschreibung von Netzwerkkommunikation.

  SCHICHT 7 - ANWENDUNG (Application):
  ------------------------------------
    - Schnittstelle fuer Endbenutzer-Anwendungen
    - Protokolle: HTTP, HTTPS, FTP, SMTP, POP3, IMAP, DNS, SNMP
    - Beispiel: Webbrowser, E-Mail-Client

  SCHICHT 6 - DARSTELLUNG (Presentation):
  ---------------------------------------
    - Datenformat-Konvertierung
    - Verschluesselung/Entschluesselung
    - Kompression
    - Beispiel: SSL/TLS, JPEG, ASCII, UTF-8

  SCHICHT 5 - SITZUNG (Session):
  ------------------------------
    - Verbindungsauf-/abbau
    - Session-Management
    - Synchronisation
    - Beispiel: NetBIOS, RPC, SQL-Sessions

  SCHICHT 4 - TRANSPORT:
  ----------------------
    - Ende-zu-Ende-Kommunikation
    - Segmentierung und Reassembly
    - Flusskontrolle, Fehlerkorrektur
    - Protokolle: TCP (verbindungsorientiert), UDP (verbindungslos)
    - Ports: 0-65535

  SCHICHT 3 - VERMITTLUNG (Network):
  ----------------------------------
    - Logische Adressierung (IP)
    - Routing zwischen Netzwerken
    - Paketweiterleitung
    - Protokolle: IP, ICMP, ARP, OSPF, BGP

  SCHICHT 2 - SICHERUNG (Data Link):
  ----------------------------------
    - Physische Adressierung (MAC)
    - Frame-Erstellung
    - Fehlererkennung (CRC)
    - Protokolle: Ethernet, PPP, HDLC, Wi-Fi (802.11)

  SCHICHT 1 - PHYSISCH (Physical):
  --------------------------------
    - Bitstrom-Uebertragung
    - Elektrische/optische Signale
    - Stecker, Kabel, Hubs
    - Spezifikationen: RS-232, RJ-45, Glasfaser-Standards

  MERKSATZ:
  ---------
    Von oben nach unten: "Alle Deutschen Schueler Trinken Verschiedene Sorten Bier"
    Von unten nach oben: "Please Do Not Throw Sausage Pizza Away"

================================================================================
3. TCP/IP-MODELL
================================================================================

  Das TCP/IP-Modell ist das praktische Modell des Internets mit 4 Schichten.

  VERGLEICH OSI vs. TCP/IP:
  -------------------------
    OSI Schicht 7,6,5  -->  TCP/IP Anwendung
    OSI Schicht 4      -->  TCP/IP Transport
    OSI Schicht 3      -->  TCP/IP Internet
    OSI Schicht 2,1    -->  TCP/IP Netzzugang

  ANWENDUNGSSCHICHT:
  ------------------
    - Alle Anwendungsprotokolle
    - HTTP, FTP, SMTP, DNS, SSH, Telnet
    - Daten werden als "Messages" bezeichnet

  TRANSPORTSCHICHT:
  -----------------
    TCP (Transmission Control Protocol):
      - Verbindungsorientiert
      - Zuverlaessig (Acknowledgements, Retransmission)
      - Reihenfolge garantiert
      - Flusskontrolle (Sliding Window)
      - Anwendung: Web, E-Mail, Dateitransfer

    UDP (User Datagram Protocol):
      - Verbindungslos
      - Unzuverlaessig (keine Garantie)
      - Schneller, weniger Overhead
      - Anwendung: Streaming, VoIP, Gaming, DNS

  INTERNETSCHICHT:
  ----------------
    - IP-Adressierung und Routing
    - Fragmentierung von Paketen
    - Best-Effort-Delivery
    - ICMP fuer Fehlermeldungen (ping, traceroute)

  NETZZUGANGSSCHICHT:
  -------------------
    - Hardware-Schnittstelle
    - Ethernet-Frames
    - ARP (Address Resolution Protocol)
    - MAC-Adressen

================================================================================
4. NETZWERKTOPOLOGIEN
================================================================================

  PHYSISCHE TOPOLOGIEN:
  ---------------------
    STERN (Star):
      - Alle Geraete mit zentralem Switch/Hub verbunden
      - Einfach zu verwalten und erweitern
      - Single Point of Failure am Switch
      - Standard in modernen LANs

                    [PC]
                      |
           [PC]---[Switch]---[PC]
                      |
                    [PC]

    BUS:
      - Alle Geraete an einem Kabel
      - Veraltet (fruehes Ethernet)
      - Kollisionsprobleme

           [PC]--[PC]--[PC]--[PC]
           ======================== (Koax)

    RING:
      - Jedes Geraet mit zwei Nachbarn verbunden
      - Token-Passing (Token Ring)
      - Redundanz bei Dual-Ring

           [PC]---[PC]
            |       |
           [PC]---[PC]

    MESH:
      - Jedes Geraet mit mehreren anderen verbunden
      - Hohe Redundanz
      - Teuer, komplex
      - Full Mesh: Jeder mit jedem

    BAUM (Hierarchisch):
      - Kombination aus Stern-Topologien
      - Core, Distribution, Access Layer
      - Typisch in Enterprise-Netzwerken

================================================================================
5. IP-ADRESSIERUNG
================================================================================

  IPv4-ADRESSEN:
  --------------
    - 32 Bit, 4 Oktette (0-255)
    - Beispiel: 192.168.1.100
    - Ca. 4,3 Milliarden Adressen (erschoepft)

    ADRESSKLASSEN (historisch):
      Klasse A: 1.0.0.0   - 126.255.255.255  (grosse Netze)
      Klasse B: 128.0.0.0 - 191.255.255.255  (mittlere Netze)
      Klasse C: 192.0.0.0 - 223.255.255.255  (kleine Netze)

    PRIVATE ADRESSEN (RFC 1918):
      10.0.0.0/8        (10.0.0.0 - 10.255.255.255)
      172.16.0.0/12     (172.16.0.0 - 172.31.255.255)
      192.168.0.0/16    (192.168.0.0 - 192.168.255.255)

    SPEZIELLE ADRESSEN:
      127.0.0.1         Localhost (Loopback)
      0.0.0.0           Alle Interfaces / Unbekannt
      255.255.255.255   Broadcast
      169.254.x.x       Link-Local (APIPA)

  SUBNETTING:
  -----------
    CIDR-Notation: IP-Adresse/Praefix-Laenge
    Beispiel: 192.168.1.0/24

    /24 = 255.255.255.0   = 256 Adressen (254 nutzbar)
    /25 = 255.255.255.128 = 128 Adressen (126 nutzbar)
    /26 = 255.255.255.192 = 64 Adressen (62 nutzbar)
    /27 = 255.255.255.224 = 32 Adressen (30 nutzbar)

    Formel: 2^(32-Praefix) = Anzahl Adressen

  IPv6-ADRESSEN:
  --------------
    - 128 Bit, hexadezimal
    - Beispiel: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
    - Kurzform: 2001:db8:85a3::8a2e:370:7334
    - Praktisch unbegrenzte Adressen (3.4 x 10^38)

    TYPEN:
      Unicast:    Einzeladresse
      Multicast:  Gruppenadresse (ff00::/8)
      Anycast:    Naechster aus Gruppe

================================================================================
6. WICHTIGE PROTOKOLLE
================================================================================

  HTTP/HTTPS (Port 80/443):
  -------------------------
    - Hypertext Transfer Protocol
    - Basis des World Wide Web
    - Request-Response-Modell
    - HTTPS: HTTP mit TLS-Verschluesselung

    Methoden: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS

  FTP/SFTP (Port 21/22):
  ----------------------
    - File Transfer Protocol
    - Dateiuebertragung
    - SFTP: Sicher ueber SSH

  SSH (Port 22):
  --------------
    - Secure Shell
    - Verschluesselte Remote-Verbindung
    - Ersetzt Telnet

  SMTP/POP3/IMAP (Port 25/110/143):
  ---------------------------------
    - E-Mail-Protokolle
    - SMTP: Versand
    - POP3/IMAP: Empfang

  DNS (Port 53):
  --------------
    - Domain Name System
    - Namensaufloesung
    - UDP fuer Abfragen, TCP fuer Zonentransfers

  DHCP (Port 67/68):
  ------------------
    - Dynamic Host Configuration Protocol
    - Automatische IP-Konfiguration

  SNMP (Port 161/162):
  --------------------
    - Simple Network Management Protocol
    - Netzwerkueberwachung

================================================================================
7. ROUTING UND SWITCHING
================================================================================

  SWITCHING (Layer 2):
  --------------------
    - MAC-Adress-basierte Weiterleitung
    - MAC-Address-Table (CAM-Table)
    - VLANs fuer Netzwerksegmentierung

    SWITCH-FUNKTIONEN:
      - Learning: MAC-Adressen lernen
      - Forwarding: Frames weiterleiten
      - Filtering: Nur an Zielport senden
      - Flooding: Bei unbekanntem Ziel

    VLAN (Virtual LAN):
      - Logische Netzwerktrennung
      - Tagged (802.1Q) und Untagged Ports
      - Trunk-Ports fuer VLAN-Uebertragung

  ROUTING (Layer 3):
  ------------------
    - IP-basierte Weiterleitung
    - Routing-Tabelle
    - Statisch oder dynamisch

    STATISCHES ROUTING:
      - Manuell konfiguriert
      - Kleine Netzwerke
      - Kein Overhead

    DYNAMISCHES ROUTING:
      Interior Gateway Protocols (IGP):
        - RIP (Routing Information Protocol): Hop Count
        - OSPF (Open Shortest Path First): Link State
        - EIGRP (Enhanced IGRP): Cisco proprietaer

      Exterior Gateway Protocol (EGP):
        - BGP (Border Gateway Protocol): Internet-Routing

    ROUTING-ENTSCHEIDUNG:
      1. Laengster Praefix-Match
      2. Administrative Distanz
      3. Metrik

================================================================================
8. DNS - DOMAIN NAME SYSTEM
================================================================================

  DNS uebersetzt Domainnamen in IP-Adressen.

  HIERARCHIE:
  -----------
    Root-Server (.)
        |
    TLD-Server (.de, .com, .org)
        |
    Authoritative Server (example.de)
        |
    www.example.de --> 93.184.216.34

  RECORD-TYPEN:
  -------------
    A:      IPv4-Adresse
    AAAA:   IPv6-Adresse
    CNAME:  Alias/Canonical Name
    MX:     Mail Exchange
    NS:     Nameserver
    TXT:    Text (SPF, DKIM, etc.)
    PTR:    Reverse-Lookup
    SOA:    Start of Authority

  DNS-ABFRAGE (Beispiel):
  -----------------------
    nslookup www.example.de
    dig www.example.de A
    dig -x 93.184.216.34  (Reverse)

  CACHING:
  --------
    - TTL (Time To Live) bestimmt Cache-Dauer
    - Recursive Resolver cachen Antworten
    - Browser und OS haben lokalen Cache

================================================================================
9. DHCP - DYNAMIC HOST CONFIGURATION PROTOCOL
================================================================================

  DHCP-PROZESS (DORA):
  --------------------
    1. DISCOVER: Client sucht DHCP-Server (Broadcast)
    2. OFFER:    Server bietet IP-Adresse an
    3. REQUEST:  Client fordert angebotene IP an
    4. ACK:      Server bestaetigt Zuweisung

  DHCP-OPTIONEN:
  --------------
    - IP-Adresse
    - Subnetzmaske
    - Default Gateway
    - DNS-Server
    - Lease Time (Gueltigkeitsdauer)
    - Domain Name

  DHCP-RELAY:
  -----------
    - Weiterleitung von DHCP ueber Router
    - ip helper-address (Cisco)
    - Noetig wenn DHCP-Server in anderem Subnetz

================================================================================
10. NETZWERKSICHERHEIT
================================================================================

  FIREWALL:
  ---------
    Paketfilter:
      - Prueft Header (IP, Port, Protokoll)
      - Stateless oder Stateful
      - Access Control Lists (ACLs)

    Application Firewall:
      - Prueft Anwendungsdaten
      - Deep Packet Inspection
      - Web Application Firewall (WAF)

  NAT (Network Address Translation):
  ----------------------------------
    - Uebersetzt private in oeffentliche IPs
    - Source NAT (SNAT): Ausgehender Verkehr
    - Destination NAT (DNAT): Port-Forwarding
    - PAT (Port Address Translation): Viele zu einer IP

  VPN (Virtual Private Network):
  ------------------------------
    - Verschluesselte Tunnel
    - Site-to-Site: Standorte verbinden
    - Remote Access: Mitarbeiter-Zugang
    - Protokolle: IPSec, OpenVPN, WireGuard

  SICHERHEITSMASSNAHMEN:
  ----------------------
    [+] Segmentierung (VLANs)
    [+] ACLs und Firewall-Regeln
    [+] Port Security
    [+] 802.1X Authentifizierung
    [+] IDS/IPS-Systeme

================================================================================
11. WIRELESS NETWORKS (WLAN)
================================================================================

  IEEE 802.11 STANDARDS:
  ----------------------
    802.11b:  2.4 GHz, 11 Mbit/s (veraltet)
    802.11g:  2.4 GHz, 54 Mbit/s
    802.11n:  2.4/5 GHz, 600 Mbit/s (Wi-Fi 4)
    802.11ac: 5 GHz, 6.9 Gbit/s (Wi-Fi 5)
    802.11ax: 2.4/5/6 GHz, 9.6 Gbit/s (Wi-Fi 6/6E)

  SICHERHEIT:
  -----------
    WEP:  Veraltet, unsicher (nicht verwenden!)
    WPA:  Besser, aber Schwaechen
    WPA2: AES-Verschluesselung, Standard
    WPA3: Aktuellster Standard, SAE-Handshake

  KONFIGURATION:
  --------------
    - SSID (Netzwerkname)
    - Kanal (1, 6, 11 bei 2.4 GHz)
    - Bandbreite (20/40/80 MHz)
    - Authentifizierung (PSK, Enterprise/RADIUS)

================================================================================
12. DIAGNOSE UND TROUBLESHOOTING
================================================================================

  WICHTIGE BEFEHLE:
  -----------------
    ping <host>:
      - ICMP Echo Request/Reply
      - Erreichbarkeit pruefen

    traceroute / tracert <host>:
      - Route zum Ziel anzeigen
      - Hop-by-Hop-Analyse

    nslookup / dig <domain>:
      - DNS-Abfragen
      - Record-Typen pruefen

    netstat / ss:
      - Aktive Verbindungen
      - Listening Ports

    ifconfig / ip addr:
      - Netzwerkkonfiguration anzeigen

    arp -a:
      - ARP-Cache anzeigen

    tcpdump / Wireshark:
      - Paketanalyse
      - Protokoll-Debugging

  TROUBLESHOOTING-METHODIK:
  -------------------------
    1. Physische Schicht pruefen (Kabel, LEDs)
    2. IP-Konfiguration pruefen (ipconfig /all)
    3. Lokale Konnektivitaet (ping Gateway)
    4. DNS-Aufloesung (nslookup)
    5. Remote-Erreichbarkeit (ping Ziel)
    6. Anwendungsebene (telnet Port)

================================================================================
13. BEST PRACTICES
================================================================================

  DESIGN:
  -------
    [+] Hierarchisches Design (Core/Distribution/Access)
    [+] Redundanz einplanen (Spanning Tree, HSRP/VRRP)
    [+] Dokumentation fuehren
    [+] Standardisierte Adressierung
    [+] Skalierbarkeit beruecksichtigen

  SICHERHEIT:
  -----------
    [+] Starke Passwoerter fuer Netzwerkgeraete
    [+] Regelmaessige Firmware-Updates
    [+] Unnoetige Dienste deaktivieren
    [+] Logging und Monitoring
    [+] Change Management

  PERFORMANCE:
  ------------
    [+] QoS fuer kritische Anwendungen
    [+] Bandbreitenmanagement
    [+] Last-Verteilung (Load Balancing)
    [+] Caching-Strategien

================================================================================
SIEHE AUCH
================================================================================

  wiki/informatik/it_sicherheit/ (Netzwerksicherheit)
  wiki/webapps/api/ (HTTP/REST)
  wiki/linux/networking/ (Linux-Netzwerkbefehle)
  wiki/informatik/datenbanken/ (Datenbankverbindungen)

================================================================================
AENDERUNGSHISTORIE
================================================================================

  2026-02-05  Vollstaendiger Artikel erstellt (vorher Stub)
  2026-01-24  Initiale Stub-Version

================================================================================
