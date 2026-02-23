================================================================================
WEB-APPS AUTHENTIFIZIERUNG - VOLLSTAENDIGER LEITFADEN
================================================================================

# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: OWASP, RFC 6749 (OAuth), RFC 7519 (JWT), NIST SP 800-63B

Stand: 2026-02-05
Status: VOLLSTAENDIG

================================================================================
INHALTSVERZEICHNIS
================================================================================
  1. Einfuehrung
  2. Session-basierte Authentifizierung
  3. JWT (JSON Web Tokens)
  4. OAuth 2.0
  5. OpenID Connect
  6. Passwort-Sicherheit
  7. Multi-Faktor-Authentifizierung (MFA)
  8. WebAuthn / Passkeys
  9. Sicherheits-Best-Practices
  10. Implementierungsbeispiele
  11. Haeufige Schwachstellen
  12. Siehe auch

================================================================================
1. EINFUEHRUNG
================================================================================

Authentifizierung bestaetigt die Identitaet eines Benutzers ("Wer bist du?"),
waehrend Autorisierung die Berechtigungen prueft ("Was darfst du?").

AUTHENTIFIZIERUNGS-METHODEN
---------------------------
  Wissen:     Passwort, PIN, Sicherheitsfragen
  Besitz:     Smartphone, Hardware-Token, Smartcard
  Biometrie:  Fingerabdruck, Gesicht, Iris

AUTHENTICATION FACTORS
----------------------
  Single Factor:  Nur Passwort
  Two Factor:     Passwort + SMS/TOTP
  Multi Factor:   Passwort + TOTP + Biometrie

================================================================================
2. SESSION-BASIERTE AUTHENTIFIZIERUNG
================================================================================

Klassischer Ansatz fuer serverseitig gerenderte Webanwendungen.

FUNKTIONSWEISE
--------------
  1. Benutzer sendet Credentials (Login)
  2. Server validiert und erstellt Session
  3. Session-ID wird als Cookie gesetzt
  4. Browser sendet Cookie bei jedem Request
  5. Server validiert Session-ID
  6. Bei Logout: Session wird geloescht

VORTEILE
--------
  - Einfach zu implementieren
  - Session kann serverseitig invalidiert werden
  - Keine Token-Groesse im Request

NACHTEILE
---------
  - Stateful (Server muss Sessions speichern)
  - Skalierung erfordert Session-Store (Redis)
  - CSRF-Schutz notwendig

SESSION-SPEICHERUNG
-------------------
  In-Memory:
    - Schnell
    - Verlust bei Server-Neustart
    - Nicht skalierbar

  Redis:
    - Schnell und persistent
    - Skalierbar
    - Session-Sharing zwischen Servern

  Datenbank:
    - Persistent
    - Langsamer
    - Einfach zu implementieren

EXPRESS.JS BEISPIEL
-------------------
  import session from 'express-session';
  import RedisStore from 'connect-redis';
  import { createClient } from 'redis';

  const redisClient = createClient();
  await redisClient.connect();

  app.use(session({
    store: new RedisStore({ client: redisClient }),
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true,       // Nur HTTPS
      httpOnly: true,     // Kein JavaScript-Zugriff
      sameSite: 'strict', // CSRF-Schutz
      maxAge: 24 * 60 * 60 * 1000 // 24 Stunden
    }
  }));

  // Login
  app.post('/login', async (req, res) => {
    const { email, password } = req.body;
    const user = await validateCredentials(email, password);

    if (user) {
      req.session.userId = user.id;
      req.session.role = user.role;
      res.json({ success: true });
    } else {
      res.status(401).json({ error: 'Invalid credentials' });
    }
  });

  // Logout
  app.post('/logout', (req, res) => {
    req.session.destroy((err) => {
      res.clearCookie('connect.sid');
      res.json({ success: true });
    });
  });

  // Auth Middleware
  function requireAuth(req, res, next) {
    if (req.session.userId) {
      next();
    } else {
      res.status(401).json({ error: 'Not authenticated' });
    }
  }

================================================================================
3. JWT (JSON WEB TOKENS)
================================================================================

Stateless Tokens fuer APIs und SPAs.

STRUKTUR
--------
  Header.Payload.Signature

  Header (Base64URL):
    {
      "alg": "HS256",
      "typ": "JWT"
    }

  Payload (Base64URL):
    {
      "sub": "1234567890",
      "name": "Max Mustermann",
      "email": "max@example.com",
      "role": "admin",
      "iat": 1516239022,
      "exp": 1516242622
    }

  Signature:
    HMACSHA256(
      base64UrlEncode(header) + "." + base64UrlEncode(payload),
      secret
    )

STANDARD CLAIMS
---------------
  iss - Issuer (Aussteller)
  sub - Subject (Benutzer-ID)
  aud - Audience (Empfaenger)
  exp - Expiration Time
  nbf - Not Before
  iat - Issued At
  jti - JWT ID (eindeutige ID)

ALGORITHMEN
-----------
  Symmetrisch (Shared Secret):
    HS256, HS384, HS512

  Asymmetrisch (Public/Private Key):
    RS256, RS384, RS512 (RSA)
    ES256, ES384, ES512 (ECDSA)
    PS256, PS384, PS512 (RSA-PSS)

  Empfehlung: RS256 oder ES256 fuer Produktion

TOKEN-SPEICHERUNG
-----------------
  HttpOnly Cookie (empfohlen):
    + Kein XSS-Zugriff
    + Automatisch gesendet
    - CSRF-Schutz noetig

  LocalStorage:
    + Einfach zu implementieren
    - XSS-verwundbar
    - Manuell senden

  Memory (In-App Variable):
    + Sicher gegen XSS/CSRF
    - Verlust bei Refresh
    - Komplexer

ACCESS + REFRESH TOKEN PATTERN
------------------------------
  Access Token:
    - Kurze Lebensdauer (15 Min)
    - Enthaelt Berechtigungen
    - Bei jedem Request gesendet

  Refresh Token:
    - Lange Lebensdauer (7 Tage)
    - Nur zum Erneuern des Access Tokens
    - In HttpOnly Cookie speichern
    - Rotation bei jeder Verwendung

NODE.JS IMPLEMENTIERUNG
-----------------------
  import jwt from 'jsonwebtoken';

  const ACCESS_SECRET = process.env.ACCESS_TOKEN_SECRET;
  const REFRESH_SECRET = process.env.REFRESH_TOKEN_SECRET;

  function generateTokens(user) {
    const accessToken = jwt.sign(
      { sub: user.id, role: user.role },
      ACCESS_SECRET,
      { expiresIn: '15m' }
    );

    const refreshToken = jwt.sign(
      { sub: user.id, tokenVersion: user.tokenVersion },
      REFRESH_SECRET,
      { expiresIn: '7d' }
    );

    return { accessToken, refreshToken };
  }

  function verifyAccessToken(token) {
    try {
      return jwt.verify(token, ACCESS_SECRET);
    } catch (error) {
      return null;
    }
  }

  // Auth Middleware
  function authMiddleware(req, res, next) {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'No token provided' });
    }

    const token = authHeader.split(' ')[1];
    const payload = verifyAccessToken(token);

    if (!payload) {
      return res.status(401).json({ error: 'Invalid token' });
    }

    req.user = payload;
    next();
  }

  // Refresh Endpoint
  app.post('/refresh', async (req, res) => {
    const refreshToken = req.cookies.refreshToken;

    if (!refreshToken) {
      return res.status(401).json({ error: 'No refresh token' });
    }

    try {
      const payload = jwt.verify(refreshToken, REFRESH_SECRET);
      const user = await getUserById(payload.sub);

      // Token-Version pruefen (fuer Invalidierung)
      if (user.tokenVersion !== payload.tokenVersion) {
        return res.status(401).json({ error: 'Token revoked' });
      }

      const tokens = generateTokens(user);

      res.cookie('refreshToken', tokens.refreshToken, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000
      });

      res.json({ accessToken: tokens.accessToken });
    } catch (error) {
      res.status(401).json({ error: 'Invalid refresh token' });
    }
  });

================================================================================
4. OAUTH 2.0
================================================================================

Delegierte Autorisierung - Zugriff auf Ressourcen ohne Passwort-Weitergabe.

ROLLEN
------
  Resource Owner:      Benutzer, der Zugriff gewaehrt
  Client:              Anwendung, die Zugriff benoetigt
  Authorization Server: Stellt Tokens aus (z.B. Google, GitHub)
  Resource Server:     API mit geschuetzten Ressourcen

GRANT TYPES (FLOWS)
-------------------
  Authorization Code (Web Apps):
    1. Client leitet zu Auth Server
    2. User authentifiziert sich
    3. Auth Server sendet Code an Redirect URI
    4. Client tauscht Code gegen Token (Server-to-Server)

  Authorization Code + PKCE (Mobile/SPA):
    - Wie oben, aber mit Code Verifier/Challenge
    - Schuetzt vor Code-Interception

  Client Credentials (Server-to-Server):
    - Kein User involviert
    - Client authentifiziert sich direkt

  Device Code (TV, IoT):
    - Fuer Geraete ohne Browser
    - Code auf Geraet anzeigen, auf anderem Geraet bestaetigen

AUTHORIZATION CODE FLOW BEISPIEL
--------------------------------
  // 1. Redirect zu Authorization Server
  const authUrl = new URL('https://auth.example.com/authorize');
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('client_id', CLIENT_ID);
  authUrl.searchParams.set('redirect_uri', 'https://myapp.com/callback');
  authUrl.searchParams.set('scope', 'openid profile email');
  authUrl.searchParams.set('state', generateRandomState());

  // Mit PKCE
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = generateCodeChallenge(codeVerifier);
  authUrl.searchParams.set('code_challenge', codeChallenge);
  authUrl.searchParams.set('code_challenge_method', 'S256');

  res.redirect(authUrl.toString());

  // 2. Callback Handler
  app.get('/callback', async (req, res) => {
    const { code, state } = req.query;

    // State validieren (CSRF-Schutz)
    if (state !== req.session.oauthState) {
      return res.status(400).send('Invalid state');
    }

    // 3. Code gegen Token tauschen
    const tokenResponse = await fetch('https://auth.example.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        redirect_uri: 'https://myapp.com/callback',
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET,
        code_verifier: req.session.codeVerifier // PKCE
      })
    });

    const tokens = await tokenResponse.json();
    // tokens.access_token, tokens.refresh_token, tokens.id_token
  });

================================================================================
5. OPENID CONNECT
================================================================================

Identitaetsschicht auf OAuth 2.0.

UNTERSCHIED ZU OAUTH 2.0
------------------------
  OAuth 2.0:  Autorisierung ("Darf App auf meine Fotos zugreifen?")
  OIDC:       Authentifizierung ("Wer ist der Benutzer?")

KOMPONENTEN
-----------
  ID Token:
    - JWT mit Benutzerinformationen
    - Claims: sub, name, email, picture, etc.

  UserInfo Endpoint:
    - /userinfo
    - Zusaetzliche Benutzerinformationen

  Discovery:
    - /.well-known/openid-configuration
    - Automatische Konfiguration

SCOPES
------
  openid   - Erforderlich fuer OIDC
  profile  - name, family_name, given_name, picture, etc.
  email    - email, email_verified
  address  - Adressinformationen
  phone    - phone_number, phone_number_verified

ID TOKEN CLAIMS
---------------
  {
    "iss": "https://auth.example.com",
    "sub": "user123",
    "aud": "client_id",
    "exp": 1516242622,
    "iat": 1516239022,
    "nonce": "abc123",
    "name": "Max Mustermann",
    "email": "max@example.com",
    "email_verified": true,
    "picture": "https://example.com/avatar.jpg"
  }

================================================================================
6. PASSWORT-SICHERHEIT
================================================================================

NIEMALS
-------
  - Passwoerter im Klartext speichern
  - Eigene Hashing-Algorithmen verwenden
  - MD5 oder SHA1 fuer Passwoerter
  - Passwoerter per E-Mail senden

HASHING-ALGORITHMEN
-------------------
  bcrypt (empfohlen):
    - Eingebautes Salting
    - Konfigurierbarer Cost Factor
    - Weit verbreitet und bewaehrt

  Argon2 (modern):
    - Gewinner Password Hashing Competition
    - Speicher-hart (gegen GPU-Angriffe)
    - Varianten: Argon2i, Argon2d, Argon2id

  scrypt:
    - Speicher- und CPU-hart
    - Gute Alternative zu bcrypt

BCRYPT BEISPIEL (Node.js)
-------------------------
  import bcrypt from 'bcrypt';

  const SALT_ROUNDS = 12; // Cost Factor

  // Passwort hashen
  async function hashPassword(password) {
    return bcrypt.hash(password, SALT_ROUNDS);
  }

  // Passwort verifizieren
  async function verifyPassword(password, hash) {
    return bcrypt.compare(password, hash);
  }

  // Registrierung
  app.post('/register', async (req, res) => {
    const { email, password } = req.body;

    // Passwort-Richtlinien pruefen
    if (!isStrongPassword(password)) {
      return res.status(400).json({ error: 'Weak password' });
    }

    const hashedPassword = await hashPassword(password);
    await createUser({ email, password: hashedPassword });

    res.status(201).json({ success: true });
  });

PASSWORT-RICHTLINIEN
--------------------
  Empfohlen (NIST SP 800-63B):
    - Mindestens 8 Zeichen (besser 12+)
    - Keine Komplexitaetsanforderungen erzwingen
    - Gegen bekannte Passwoerter pruefen (Leaked Passwords)
    - Keine regelmaessigen Aenderungen erzwingen

  Pruefen gegen Leaks:
    - Have I Been Pwned API
    - k-Anonymity fuer sichere Abfrage

================================================================================
7. MULTI-FAKTOR-AUTHENTIFIZIERUNG (MFA)
================================================================================

METHODEN
--------
  TOTP (Time-based One-Time Password):
    + Offline-faehig
    + Keine SIM-Abhaengigkeit
    - Seed muss sicher gespeichert werden

  SMS:
    + Einfach fuer Benutzer
    - SIM-Swapping-Angriffe
    - Nicht verschluesselt

  E-Mail:
    + Weit verbreitet
    - Abhaengig von E-Mail-Sicherheit

  Push-Benachrichtigung:
    + Benutzerfreundlich
    - App erforderlich

  Hardware-Token (FIDO2/WebAuthn):
    + Sehr sicher
    + Phishing-resistent
    - Kosten fuer Hardware

TOTP IMPLEMENTIERUNG
--------------------
  import { authenticator } from 'otplib';
  import qrcode from 'qrcode';

  // Secret generieren
  function generateTOTPSecret() {
    return authenticator.generateSecret();
  }

  // QR-Code fuer Authenticator App
  async function generateQRCode(email, secret) {
    const otpauth = authenticator.keyuri(
      email,
      'MyApp',
      secret
    );
    return qrcode.toDataURL(otpauth);
  }

  // Code verifizieren
  function verifyTOTP(token, secret) {
    return authenticator.verify({ token, secret });
  }

  // MFA Setup
  app.post('/mfa/setup', requireAuth, async (req, res) => {
    const secret = generateTOTPSecret();
    const qrCode = await generateQRCode(req.user.email, secret);

    // Secret temporaer speichern bis Verifizierung
    req.session.pendingMFASecret = secret;

    res.json({ qrCode });
  });

  // MFA Aktivieren
  app.post('/mfa/verify', requireAuth, async (req, res) => {
    const { token } = req.body;
    const secret = req.session.pendingMFASecret;

    if (verifyTOTP(token, secret)) {
      await enableMFA(req.user.id, secret);
      delete req.session.pendingMFASecret;
      res.json({ success: true });
    } else {
      res.status(400).json({ error: 'Invalid code' });
    }
  });

================================================================================
8. WEBAUTHN / PASSKEYS
================================================================================

Passwordless Authentication mit Public-Key-Kryptographie.

VORTEILE
--------
  - Phishing-resistent (Origin-gebunden)
  - Keine Shared Secrets
  - Benutzerfreundlich
  - Biometrie-Integration

ABLAUF REGISTRIERUNG
--------------------
  1. Server sendet Challenge
  2. Authenticator erstellt Keypair
  3. Private Key bleibt auf Geraet
  4. Public Key wird an Server gesendet
  5. Server speichert Public Key + Credential ID

ABLAUF AUTHENTIFIZIERUNG
------------------------
  1. Server sendet Challenge
  2. Authenticator signiert Challenge
  3. Server verifiziert Signatur mit Public Key

SERVER-IMPLEMENTIERUNG (SimpleWebAuthn)
---------------------------------------
  import {
    generateRegistrationOptions,
    verifyRegistrationResponse,
    generateAuthenticationOptions,
    verifyAuthenticationResponse
  } from '@simplewebauthn/server';

  // Registrierung starten
  app.post('/webauthn/register/start', requireAuth, async (req, res) => {
    const user = await getUser(req.user.id);

    const options = await generateRegistrationOptions({
      rpName: 'My App',
      rpID: 'myapp.com',
      userID: user.id,
      userName: user.email,
      attestationType: 'none',
      authenticatorSelection: {
        residentKey: 'preferred',
        userVerification: 'preferred'
      }
    });

    req.session.challenge = options.challenge;
    res.json(options);
  });

  // Registrierung abschliessen
  app.post('/webauthn/register/finish', requireAuth, async (req, res) => {
    const verification = await verifyRegistrationResponse({
      response: req.body,
      expectedChallenge: req.session.challenge,
      expectedOrigin: 'https://myapp.com',
      expectedRPID: 'myapp.com'
    });

    if (verification.verified) {
      await saveCredential(req.user.id, verification.registrationInfo);
      res.json({ success: true });
    }
  });

================================================================================
9. SICHERHEITS-BEST-PRACTICES
================================================================================

ALLGEMEIN
---------
  1. HTTPS immer und ueberall
  2. Secure, HttpOnly, SameSite Cookies
  3. CSRF-Token fuer State-aendernde Requests
  4. Rate Limiting bei Login (z.B. 5 Versuche/Min)
  5. Account Lockout nach Fehlversuchen
  6. Login-Versuche loggen

PASSWOERTER
-----------
  1. Starke Hashing-Algorithmen (bcrypt, Argon2)
  2. Gegen Leaked Passwords pruefen
  3. Passwort-Reset mit zeitlich begrenztem Token
  4. Alte Sessions bei Passwort-Aenderung invalidieren

TOKENS
------
  1. Kurze Lebensdauer fuer Access Tokens
  2. Refresh Token Rotation
  3. Token-Blacklist fuer kritische Invalidierung
  4. Keine sensitiven Daten in JWT Payload

SESSION-SICHERHEIT
------------------
  1. Session-ID nach Login regenerieren
  2. Inaktivitaets-Timeout
  3. Absolute Session-Lebensdauer
  4. Session bei Logout vollstaendig loeschen

================================================================================
10. IMPLEMENTIERUNGSBEISPIELE
================================================================================

VOLLSTAENDIGES LOGIN-SYSTEM (Express.js)
----------------------------------------
  import express from 'express';
  import bcrypt from 'bcrypt';
  import rateLimit from 'express-rate-limit';

  const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 Minuten
    max: 5, // 5 Versuche
    message: { error: 'Too many login attempts' }
  });

  app.post('/login', loginLimiter, async (req, res) => {
    const { email, password, totpCode } = req.body;

    // 1. Benutzer finden
    const user = await getUserByEmail(email);
    if (!user) {
      // Timing-Attack vermeiden
      await bcrypt.hash(password, 12);
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // 2. Passwort pruefen
    const validPassword = await bcrypt.compare(password, user.passwordHash);
    if (!validPassword) {
      await logFailedLogin(user.id, req.ip);
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // 3. MFA pruefen (falls aktiviert)
    if (user.mfaEnabled) {
      if (!totpCode) {
        return res.status(200).json({ requireMFA: true });
      }
      if (!verifyTOTP(totpCode, user.mfaSecret)) {
        return res.status(401).json({ error: 'Invalid MFA code' });
      }
    }

    // 4. Session erstellen
    req.session.regenerate((err) => {
      req.session.userId = user.id;
      req.session.role = user.role;
      res.json({ success: true });
    });
  });

================================================================================
11. HAEUFIGE SCHWACHSTELLEN
================================================================================

  Broken Authentication (OWASP Top 10):
    - Schwache Passwoerter erlaubt
    - Keine Rate Limiting
    - Session-IDs in URL
    - Fehlende Session-Invalidierung

  Credential Stuffing:
    - Gestohlene Credentials testen
    - Abhilfe: MFA, Leaked Password Check

  Session Hijacking:
    - Session-ID gestohlen (XSS, Network Sniffing)
    - Abhilfe: HttpOnly, Secure, HTTPS

  Session Fixation:
    - Angreifer setzt Session-ID vor Login
    - Abhilfe: Session-ID nach Login regenerieren

================================================================================
SIEHE AUCH
================================================================================

  BACH Wiki:
    wiki/informatik/it_sicherheit/
    wiki/webapps/api/
    wiki/webapps/datenbanken/

  Externe Ressourcen:
    https://owasp.org/www-project-web-security-testing-guide/
    https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
    https://datatracker.ietf.org/doc/html/rfc6749 (OAuth 2.0)
    https://datatracker.ietf.org/doc/html/rfc7519 (JWT)
    https://webauthn.guide/

================================================================================
