# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: OWASP, NIST Cybersecurity Framework, BSI IT-Grundschutz, RFC-Standards

================================================================================
IT-SICHERHEIT - UMFASSENDER WIKI-ARTIKEL
================================================================================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
INHALTSVERZEICHNIS
================================================================================
  1. Einfuehrung in IT-Sicherheit
  2. Schutzziele (CIA-Triade)
  3. Kryptographie
  4. Authentifizierung und Autorisierung
  5. Angriffsvektoren und Bedrohungen
  6. Web-Security (OWASP Top 10)
  7. Netzwerksicherheit
  8. Endpunkt-Sicherheit
  9. Security Operations
  10. Compliance und Standards
  11. Incident Response
  12. Best Practices

================================================================================
1. EINFUEHRUNG IN IT-SICHERHEIT
================================================================================

  IT-Sicherheit (Informationssicherheit) umfasst alle Massnahmen zum Schutz
  von Informationen und IT-Systemen vor unbefugtem Zugriff, Manipulation,
  Stoerung und Zerstoerung.

  WICHTIGKEIT:
  ------------
    - Schutz sensibler Daten (personenbezogen, geschaeftskritisch)
    - Aufrechterhaltung von Geschaeftsprozessen
    - Einhaltung gesetzlicher Anforderungen
    - Vertrauenswuerdigkeit gegenueber Kunden/Partnern
    - Vermeidung finanzieller Schaeden

  SICHERHEITSBEREICHE:
  --------------------
    - Anwendungssicherheit
    - Netzwerksicherheit
    - Cloud-Sicherheit
    - Endpunkt-Sicherheit
    - Identitaets- und Zugriffsmanagement
    - Datensicherheit
    - Physische Sicherheit
    - Awareness und Schulung

================================================================================
2. SCHUTZZIELE (CIA-TRIADE)
================================================================================

  Die drei Grundpfeiler der Informationssicherheit:

  VERTRAULICHKEIT (Confidentiality):
  ----------------------------------
    - Nur autorisierte Personen haben Zugang
    - Schutz vor unbefugter Offenlegung
    - Massnahmen: Verschluesselung, Zugriffskontrollen
    - Beispiel: Kundendaten nur fuer befugte Mitarbeiter

  INTEGRITAET (Integrity):
  ------------------------
    - Daten sind korrekt und unveraendert
    - Schutz vor unbefugter Manipulation
    - Massnahmen: Hashes, digitale Signaturen, Audit-Logs
    - Beispiel: Bankueberweisungen duerfen nicht veraendert werden

  VERFUEGBARKEIT (Availability):
  ------------------------------
    - Systeme und Daten sind bei Bedarf erreichbar
    - Schutz vor Ausfaellen und Stoerungen
    - Massnahmen: Redundanz, Backups, DDoS-Schutz
    - Beispiel: Online-Shop muss erreichbar sein

  ERWEITERTE SCHUTZZIELE:
  -----------------------
    Authentizitaet: Echtheit der Identitaet
    Verbindlichkeit: Aktionen sind nachweisbar (Non-Repudiation)
    Zurechenbarkeit: Aktionen sind zuordenbar

================================================================================
3. KRYPTOGRAPHIE
================================================================================

  Kryptographie ist die Wissenschaft der Verschluesselung und bildet
  die Grundlage vieler Sicherheitsmechanismen.

  SYMMETRISCHE VERSCHLUESSELUNG:
  ------------------------------
    - Gleicher Schluessel fuer Ver- und Entschluesselung
    - Schnell und effizient
    - Problem: Schluesselaustausch

    Algorithmen:
      AES (Advanced Encryption Standard):
        - Blockverschluesselung (128 Bit Bloecke)
        - Schluessellaengen: 128, 192, 256 Bit
        - Standard fuer moderne Anwendungen

      ChaCha20:
        - Stromverschluesselung
        - Schnell auf Systemen ohne AES-Hardware
        - Verwendet mit Poly1305 (ChaCha20-Poly1305)

      DES/3DES:
        - Veraltet, nicht mehr verwenden
        - Zu kurze Schluessel (56 Bit)

  ASYMMETRISCHE VERSCHLUESSELUNG:
  -------------------------------
    - Schluesselpaar: Oeffentlich und Privat
    - Oeffentlicher Schluessel zum Verschluesseln
    - Privater Schluessel zum Entschluesseln
    - Langsamer, loest Schluesselaustausch-Problem

    Algorithmen:
      RSA:
        - Beruht auf Faktorisierungsproblem
        - Typische Schluessellaengen: 2048, 4096 Bit
        - Weit verbreitet (TLS, S/MIME, PGP)

      ECC (Elliptic Curve Cryptography):
        - Kuerzere Schluessel bei gleicher Sicherheit
        - 256-Bit ECC ~ 3072-Bit RSA
        - Schneller, geringerer Ressourcenverbrauch

  HASH-FUNKTIONEN:
  ----------------
    - Einweg-Funktion (nicht umkehrbar)
    - Feste Ausgabelaenge unabhaengig von Eingabe
    - Kollisionsresistenz erforderlich

    Sichere Algorithmen:
      SHA-256/SHA-3:  256 Bit, aktueller Standard
      BLAKE2/BLAKE3:  Schnell und sicher

    Unsichere Algorithmen (NICHT verwenden):
      MD5:    Kollisionen bekannt, nur noch fuer Pruefsummen
      SHA-1:  Kollisionen nachgewiesen

  DIGITALE SIGNATUREN:
  --------------------
    - Kombination aus Hash und asymmetrischer Verschluesselung
    - Authentizitaet und Integritaet
    - Nicht-Abstreitbarkeit

    Prozess:
      1. Dokument hashen
      2. Hash mit privatem Schluessel signieren
      3. Empfaenger verifiziert mit oeffentlichem Schluessel

  TLS/SSL (Transport Layer Security):
  -----------------------------------
    - Verschluesselte Kommunikation
    - Verwendet symmetrische und asymmetrische Kryptographie
    - Zertifikatsbasierte Authentifizierung

    Aktuelle Versionen:
      TLS 1.3: Aktueller Standard, sicher
      TLS 1.2: Noch akzeptabel mit richtiger Konfiguration
      TLS 1.0/1.1, SSL: Veraltet, unsicher

================================================================================
4. AUTHENTIFIZIERUNG UND AUTORISIERUNG
================================================================================

  AUTHENTIFIZIERUNG (Wer bist du?):
  ---------------------------------
    Faktoren:
      Wissen:     Passwort, PIN, Sicherheitsfrage
      Besitz:     Token, Smartphone, Smartcard
      Biometrie:  Fingerabdruck, Gesicht, Iris

    Multi-Faktor-Authentifizierung (MFA):
      - Kombination mehrerer Faktoren
      - 2FA: Zwei Faktoren (z.B. Passwort + TOTP)
      - Deutlich sicherer als Ein-Faktor

  PASSWORT-SICHERHEIT:
  --------------------
    Speicherung:
      [+] Passwoerter niemals im Klartext speichern
      [+] Sichere Hash-Funktionen verwenden (bcrypt, Argon2, scrypt)
      [+] Salting: Zufallswert vor dem Hashen hinzufuegen
      [+] Peppering: Zusaetzlicher geheimer Wert

    Beispiel mit bcrypt (Python):
      import bcrypt
      password = b"geheim123"
      salt = bcrypt.gensalt(rounds=12)
      hashed = bcrypt.hashpw(password, salt)
      # Verifizierung
      bcrypt.checkpw(password, hashed)

    Passwort-Richtlinien:
      [+] Mindestlaenge: 12+ Zeichen
      [+] Keine bekannten Passwoerter (Breach-Listen)
      [+] Passphrasen empfehlen
      [-] Keine regelmaessigen Aenderungen erzwingen (NIST)
      [-] Keine Komplexitaetsregeln (schwer zu merken)

  AUTORISIERUNG (Was darfst du?):
  -------------------------------
    RBAC (Role-Based Access Control):
      - Berechtigungen an Rollen gebunden
      - Benutzer erhalten Rollen
      - Beispiel: Admin, Editor, Viewer

    ABAC (Attribute-Based Access Control):
      - Berechtigungen basierend auf Attributen
      - Flexibler als RBAC
      - Beispiel: Zugriff nur waehrend Arbeitszeit

    Principle of Least Privilege:
      - Minimale notwendige Berechtigungen
      - Reduziert Angriffsflaeche

  OAUTH 2.0 UND OPENID CONNECT:
  -----------------------------
    OAuth 2.0:
      - Autorisierungs-Framework
      - Delegierter Zugriff auf Ressourcen
      - Access Tokens

    OpenID Connect (OIDC):
      - Authentifizierungsschicht auf OAuth 2.0
      - ID Tokens (JWT)
      - Single Sign-On (SSO)

================================================================================
5. ANGRIFFSVEKTOREN UND BEDROHUNGEN
================================================================================

  SOCIAL ENGINEERING:
  -------------------
    Phishing:
      - Gefaelschte E-Mails/Websites
      - Ziel: Zugangsdaten stehlen
      - Varianten: Spear Phishing, Whaling

    Pretexting:
      - Vorgetaeuschte Identitaet
      - Vertrauensaufbau

    Baiting:
      - Koeder (z.B. USB-Stick)
      - Neugier ausnutzen

  MALWARE:
  --------
    Viren:       Selbstreplizierende Programme, benoetigen Host
    Wuermer:     Selbstreplizierende Programme, autonom
    Trojaner:    Getarnte Schadsoftware
    Ransomware:  Verschluesselt Daten, fordert Loesegeld
    Spyware:     Spioniert Benutzer aus
    Rootkits:    Verstecken Praesenz im System

  NETZWERKANGRIFFE:
  -----------------
    DDoS (Distributed Denial of Service):
      - Ueberlastung durch Massenanfragen
      - Botnets als Angriffsinfrastruktur

    Man-in-the-Middle (MITM):
      - Abfangen/Manipulieren der Kommunikation
      - ARP Spoofing, DNS Spoofing

    Replay-Angriffe:
      - Wiederholtes Senden abgefangener Daten

  INSIDER-BEDROHUNGEN:
  --------------------
    - Mitarbeiter mit boesen Absichten
    - Versehentliche Datenlecks
    - Kompromittierte Accounts

================================================================================
6. WEB-SECURITY (OWASP TOP 10)
================================================================================

  Die OWASP Top 10 sind die kritischsten Webanwendungs-Sicherheitsrisiken.

  A01: BROKEN ACCESS CONTROL:
  ---------------------------
    - Unzureichende Zugriffskontrollen
    - Horizontale/Vertikale Rechteausweitung
    - Schutz: Serverseitige Validierung, Default Deny

  A02: CRYPTOGRAPHIC FAILURES:
  ----------------------------
    - Schwache oder fehlende Verschluesselung
    - Klartext-Uebertragung sensibler Daten
    - Schutz: TLS, sichere Algorithmen, keine Hardcoded Keys

  A03: INJECTION:
  ---------------
    SQL Injection:
      ANGREIFBAR:
        query = "SELECT * FROM users WHERE id=" + user_input

      SICHER (Prepared Statement):
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_input,))

    Command Injection:
      - Ausfuehrung von Systembefehlen
      - Schutz: Keine Shell-Befehle mit User-Input

    LDAP, XPath, NoSQL Injection analog

  A04: INSECURE DESIGN:
  ---------------------
    - Sicherheit nicht im Design beruecksichtigt
    - Schutz: Threat Modeling, Security Requirements

  A05: SECURITY MISCONFIGURATION:
  -------------------------------
    - Default-Passwoerter
    - Unnoetige Features aktiviert
    - Verbose Fehlermeldungen
    - Schutz: Hardening, Security Baselines

  A06: VULNERABLE COMPONENTS:
  ---------------------------
    - Veraltete Bibliotheken mit bekannten Schwachstellen
    - Schutz: Dependency Scanning, regelmaessige Updates

  A07: AUTHENTICATION FAILURES:
  -----------------------------
    - Schwache Passwoerter erlaubt
    - Brute-Force moeglich
    - Session-Management-Fehler
    - Schutz: MFA, Rate Limiting, sichere Session-Handling

  A08: SOFTWARE AND DATA INTEGRITY FAILURES:
  ------------------------------------------
    - Unsichere Deserialisierung
    - Fehlende Code-Signierung
    - Schutz: Integritaetspruefungen, sichere CI/CD

  A09: SECURITY LOGGING AND MONITORING FAILURES:
  ----------------------------------------------
    - Fehlende Logs
    - Keine Alarmierung
    - Schutz: Umfassendes Logging, SIEM

  A10: SERVER-SIDE REQUEST FORGERY (SSRF):
  ----------------------------------------
    - Server fuehrt Anfragen zu beliebigen URLs aus
    - Zugriff auf interne Ressourcen
    - Schutz: URL-Validierung, Allowlists

  CROSS-SITE SCRIPTING (XSS):
  ---------------------------
    Reflected XSS:  Angriffs-Code in URL-Parameter
    Stored XSS:     Angriffs-Code in Datenbank gespeichert
    DOM-based XSS:  Manipulation im Browser

    Schutz:
      - Output Encoding
      - Content Security Policy (CSP)
      - HttpOnly Cookies

  CROSS-SITE REQUEST FORGERY (CSRF):
  ----------------------------------
    - Ungewollte Aktionen im Namen des Benutzers
    - Schutz: CSRF-Tokens, SameSite Cookies

================================================================================
7. NETZWERKSICHERHEIT
================================================================================

  FIREWALLS:
  ----------
    Paketfilter:
      - Layer 3/4 Filterung
      - IP-Adressen, Ports, Protokolle
      - Stateless oder Stateful

    Next-Generation Firewall (NGFW):
      - Deep Packet Inspection
      - Application Awareness
      - Intrusion Prevention

    Web Application Firewall (WAF):
      - Layer 7 Schutz
      - OWASP-Regeln
      - Vor Webanwendungen platziert

  INTRUSION DETECTION/PREVENTION:
  -------------------------------
    IDS (Intrusion Detection System):
      - Erkennt verdaechtige Aktivitaeten
      - Alarmierung
      - Signatur- oder Anomalie-basiert

    IPS (Intrusion Prevention System):
      - Erkennung und aktive Blockierung
      - Inline-Platzierung

  NETWORK SEGMENTATION:
  ---------------------
    - Trennung in Sicherheitszonen
    - DMZ fuer oeffentliche Dienste
    - VLANs und Firewalls zwischen Segmenten
    - Zero Trust: Microsegmentation

  VPN:
  ----
    - Verschluesselte Tunnel
    - IPSec: Layer 3, Enterprise
    - OpenVPN: SSL-basiert, flexibel
    - WireGuard: Modern, performant

================================================================================
8. ENDPUNKT-SICHERHEIT
================================================================================

  ANTIVIRUS/ANTI-MALWARE:
  -----------------------
    - Signaturbasierte Erkennung
    - Heuristische Analyse
    - Verhaltensbasierte Erkennung
    - EDR (Endpoint Detection and Response)

  PATCH-MANAGEMENT:
  -----------------
    - Regelmaessige Updates
    - Automatisierte Verteilung
    - Testen vor Rollout
    - Notfall-Patches priorisieren

  GERAETEVERSCHLUESSELUNG:
  ------------------------
    - Full Disk Encryption (BitLocker, FileVault, LUKS)
    - Schutz bei Geraeteverlust
    - TPM-Integration

  APPLICATION WHITELISTING:
  -------------------------
    - Nur erlaubte Anwendungen ausfuehrbar
    - Effektiv gegen unbekannte Malware
    - Aufwendig zu verwalten

================================================================================
9. SECURITY OPERATIONS
================================================================================

  SIEM (Security Information and Event Management):
  -------------------------------------------------
    - Zentrales Log-Management
    - Korrelation von Events
    - Alarmierung und Dashboards
    - Beispiele: Splunk, Elastic SIEM, Microsoft Sentinel

  VULNERABILITY MANAGEMENT:
  -------------------------
    Prozess:
      1. Asset-Inventar erstellen
      2. Regelmaessige Scans (Nessus, Qualys, OpenVAS)
      3. Risikobewertung (CVSS)
      4. Priorisierung und Remediation
      5. Verifizierung

    CVSS (Common Vulnerability Scoring System):
      - 0.0-3.9:   Low
      - 4.0-6.9:   Medium
      - 7.0-8.9:   High
      - 9.0-10.0:  Critical

  PENETRATION TESTING:
  --------------------
    - Simulierte Angriffe
    - Manuelle und automatisierte Tests
    - Black/White/Grey Box
    - Regelmaessig durchfuehren

  SECURITY AWARENESS:
  -------------------
    - Schulungen fuer Mitarbeiter
    - Phishing-Simulationen
    - Security-Champions im Team
    - Regelmaessige Updates

================================================================================
10. COMPLIANCE UND STANDARDS
================================================================================

  DSGVO (GDPR):
  -------------
    - EU-Datenschutzverordnung
    - Personenbezogene Daten schuetzen
    - Rechte der Betroffenen
    - Meldepflicht bei Datenpannen (72h)
    - Hohe Strafen moeglich

  ISO 27001:
  ----------
    - Internationaler Standard fuer ISMS
    - Risikomanagement
    - Kontinuierliche Verbesserung
    - Zertifizierung moeglich

  BSI IT-GRUNDSCHUTZ:
  -------------------
    - Deutsches Framework
    - Bausteine und Massnahmen
    - Kompatibel mit ISO 27001

  PCI DSS:
  --------
    - Payment Card Industry Standard
    - Fuer Kreditkartendaten
    - 12 Anforderungsbereiche

  SOC 2:
  ------
    - Service Organization Control
    - Trust Principles: Security, Availability, etc.
    - Fuer Dienstleister

================================================================================
11. INCIDENT RESPONSE
================================================================================

  INCIDENT-RESPONSE-PHASEN:
  -------------------------
    1. VORBEREITUNG:
       - Team definieren
       - Plaene erstellen
       - Tools bereitstellen
       - Uebungen durchfuehren

    2. ERKENNUNG UND ANALYSE:
       - Alarm-Triage
       - Scope bestimmen
       - Beweissicherung

    3. EINDAEMMUNG (Containment):
       - Kurzfristig: Sofortige Isolation
       - Langfristig: Temporaere Massnahmen
       - Ausbreitung verhindern

    4. BESEITIGUNG (Eradication):
       - Malware entfernen
       - Schwachstellen schliessen
       - Kompromittierte Accounts zuruecksetzen

    5. WIEDERHERSTELLUNG (Recovery):
       - Systeme wiederherstellen
       - Monitoring verstaerken
       - Schrittweise Normalbetrieb

    6. LESSONS LEARNED:
       - Analyse des Vorfalls
       - Dokumentation
       - Prozessverbesserungen

  FORENSIK:
  ---------
    - Beweissicherung (Chain of Custody)
    - Imaging von Systemen
    - Timeline-Analyse
    - Malware-Analyse

================================================================================
12. BEST PRACTICES
================================================================================

  ENTWICKLUNG (Secure SDLC):
  --------------------------
    [+] Threat Modeling in Design-Phase
    [+] Code Reviews mit Sicherheitsfokus
    [+] Static Application Security Testing (SAST)
    [+] Dynamic Application Security Testing (DAST)
    [+] Dependency Scanning (SCA)
    [+] Security in CI/CD-Pipeline

  INFRASTRUKTUR:
  --------------
    [+] Haertung von Systemen (CIS Benchmarks)
    [+] Minimale Angriffsoberflaeche
    [+] Regelmaessige Backups (3-2-1 Regel)
    [+] Netzwerksegmentierung
    [+] Verschluesselung in Transit und at Rest

  BETRIEB:
  --------
    [+] Zentrales Logging
    [+] Monitoring und Alerting
    [+] Regelmaessige Vulnerability Scans
    [+] Patch-Management-Prozess
    [+] Change Management

  ORGANISATORISCH:
  ----------------
    [+] Security Policies dokumentieren
    [+] Regelmaessige Awareness-Schulungen
    [+] Incident-Response-Plan
    [+] Business Continuity Planning
    [+] Regelmaessige Audits

  CHECKLISTE SICHERE WEBANWENDUNG:
  --------------------------------
    [ ] Input Validierung (Whitelist)
    [ ] Output Encoding (Context-spezifisch)
    [ ] Prepared Statements fuer Datenbank
    [ ] HTTPS ueberall (HSTS)
    [ ] Sichere Session-Cookies (HttpOnly, Secure, SameSite)
    [ ] Content Security Policy
    [ ] CSRF-Schutz
    [ ] Rate Limiting
    [ ] Security Headers
    [ ] Keine sensiblen Daten in URLs/Logs

================================================================================
SIEHE AUCH
================================================================================

  wiki/webapps/authentifizierung/ (OAuth, JWT)
  wiki/jura/ (DSGVO, Datenschutz)
  wiki/informatik/netzwerke/ (Netzwerksicherheit)
  wiki/informatik/datenbanken/ (SQL Injection)
  wiki/linux/security/ (Linux-Haertung)

================================================================================
AENDERUNGSHISTORIE
================================================================================

  2026-02-05  Vollstaendiger Artikel erstellt (vorher Stub)
  2026-01-24  Initiale Stub-Version

================================================================================
