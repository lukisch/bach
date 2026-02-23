# Connector Template System

## Uebersicht

Das Connector Template System ermoeglicht es, schnell und einfach neue Connectors
und Notification-Channels fuer BACH zu erstellen. Es gibt zwei Arten:

1. **Volle Connectors** - Bidirektional (Senden + Empfangen + Polling)
2. **Notification-Channels** - Nur Senden (Push-Benachrichtigungen)

Bestandteile:
1. **Template-Dateien** - Code-Templates mit Platzhaltern
2. **Template-Konfigurationen** - YAML-Dateien die Platzhalter definieren
3. **Setup-Wizard** - Interaktiver CLI-Wizard fuer die Connector-Erstellung

## WICHTIG: Secrets-Management

**API-Keys und Tokens gehoeren NIEMALS in die bach.db!**

Die bach.db wird beim Release-Build kopiert -- alle darin gespeicherten
Keys wuerden mit-veroeffentlicht werden.

Stattdessen: `user/secrets/secrets.json` (dist_type=0, wird nie gebuildet)

```python
# So liest ein Handler die Secrets:
secrets_file = BACH_ROOT / "user" / "secrets" / "secrets.json"
with open(secrets_file, 'r') as f:
    secrets = json.load(f)
token = secrets["telegram"]["bot_token"]
```

In der DB steht nur `auth_type='secrets_file'` als Verweis.

## Verzeichnisstruktur

```
connectors/
├── base.py                           # BaseConnector Interface
├── telegram_connector.py             # Telegram Implementierung (bidirektional)
├── discord_connector.py              # Discord Implementierung (bidirektional)
├── whatsapp_connector.py             # WhatsApp Implementierung (Beispiel)
├── homeassistant_connector.py        # Home Assistant Implementierung
├── signal_connector.py               # Signal Implementierung (geplant)
└── templates/
    ├── README.md                     # Diese Datei
    ├── connector_template.py         # Code-Template fuer volle Connectors
    ├── notification_template.yaml    # Anleitung fuer Notification-Channels
    ├── setup_wizard.py               # Interaktiver Setup-Wizard
    ├── telegram_template.yaml        # Telegram Connector-Konfiguration
    └── whatsapp_template.yaml        # WhatsApp Connector-Konfiguration

hub/notify.py                         # Notification-Handler (nur Senden)
user/secrets/secrets.json             # API-Keys (dist_type=0, PRIVAT!)
```

## Notification-Channels (Direktnachrichten)

Notification-Channels sind einfacher als volle Connectors -- sie senden nur,
empfangen nicht. Partner (Server, CI/CD, Agenten) koennen darueber
Push-Nachrichten an den User schicken.

### Vorhandene Notification-Channels

| Channel   | Status  | Handler                    |
|-----------|---------|----------------------------|
| telegram  | AKTIV   | hub/notify.py              |
| discord   | AKTIV   | hub/notify.py (Webhook)    |
| slack     | AKTIV   | hub/notify.py (Webhook)    |
| webhook   | AKTIV   | hub/notify.py (generisch)  |
| email     | AKTIV   | hub/notify.py (SMTP)       |

### Neuen Notification-Channel hinzufuegen

**Schritt 1: Key in secrets.json eintragen**

```json
// user/secrets/secrets.json
{
  "mein_channel": {
    "api_token": "...",
    "endpoint": "https://api.example.com/notify"
  }
}
```

**Schritt 2: hub/notify.py erweitern**

a) Channel-Name in `CHANNELS`-Tuple eintragen (~Zeile 39):
```python
CHANNELS = ("discord", "signal", "email", "telegram", "webhook", "slack", "mein_channel")
```

b) Dispatch-Methode erweitern (~Zeile 290):
```python
elif channel == "mein_channel":
    return self._send_mein_channel(text, auth_config)
```

c) Send-Methode implementieren:
```python
def _send_mein_channel(self, text, auth_config=""):
    secrets = self._load_secrets()
    token = secrets.get("mein_channel", {}).get("api_token", "")
    endpoint = secrets.get("mein_channel", {}).get("endpoint", "")
    if not token or not endpoint:
        return False
    # HTTP POST an endpoint...
    return True
```

**Schritt 3: In DB registrieren**

```bash
bach notify setup mein_channel
```

**Schritt 4: Testen**

```bash
bach notify test mein_channel
bach notify send mein_channel "Hallo Welt"
```

### Partner-Tagging (Konvention)

Nachrichten von Partnern sollten mit einem Tag-Prefix beginnen:

| Tag        | Quelle                              |
|------------|-------------------------------------|
| [MCMC]     | Server-Status, Fortschritt          |
| [ZENODO]   | DOI-Vergabe, Upload-Bestaetigung    |
| [LINKEDIN] | Post publiziert                     |
| [CI/CD]    | Build-Status, Test-Ergebnisse       |
| [BACH]     | Interne System-Meldungen            |
| [AGENT]    | Agent-Ergebnisse (Schwarm, etc.)    |

## Schnellstart

### 1. Neuen Connector mit Wizard erstellen

Der einfachste Weg ist der interaktive Setup-Wizard:

```bash
bach connector setup-wizard
```

Der Wizard führt Sie durch folgende Schritte:

1. Template auswählen (z.B. telegram, whatsapp)
2. Instanz-Namen vergeben
3. Authentifizierungs-Daten eingeben
4. Optionale Konfigurationen setzen
5. Connector-Datei generieren
6. In Datenbank registrieren

### 2. Manuell ein neues Template erstellen

Wenn Sie einen komplett neuen Connector-Typ erstellen möchten:

#### Schritt 1: Template-Konfiguration erstellen

Erstellen Sie eine neue YAML-Datei: `connectors/templates/signal_template.yaml`

```yaml
# Template-Konfiguration fuer Signal-Connector
connector_name: Signal
connector_type: signal
connector_display_name: Signal Messenger
connector_description: |
  Implementiert BaseConnector fuer Signal Messenger via signal-cli.

# Module und Klassen-Namen
connector_module: signal_connector
connector_instance_name: signal_main
recipient_example: "+49123456789"

# Auth-Konfiguration
auth_type: none
auth_config_example: |
  {}
options_example: |
  {"phone_number": "+49123456789", "signal_cli_path": "/usr/local/bin/signal-cli"}

# API-Konfiguration
api_base_comment: "# Signal verwendet signal-cli (kein HTTP API)"
api_base_url: ""

# Code-Snippets (siehe Beispiele unten)
init_variables: |
  self._phone_number = config.options.get("phone_number", "")
  self._signal_cli_path = config.options.get("signal_cli_path", "signal-cli")
  self._daemon_socket = config.options.get("daemon_socket", "")

# ... weitere Snippets ...

# Setup-Wizard Fragen
setup_questions:
  - name: phone_number
    prompt: "Registrierte Telefonnummer (z.B. +49123456789)"
    type: text
    required: true
    storage: options

  - name: signal_cli_path
    prompt: "Pfad zu signal-cli"
    type: text
    required: false
    storage: options
    default: "signal-cli"
```

#### Schritt 2: Code-Snippets definieren

Die wichtigsten Code-Snippets in der YAML-Datei:

**init_variables** - Initialisierung in `__init__`:
```yaml
init_variables: |
  self._api_token = config.auth_config.get("api_token", "")
  self._phone_number = config.options.get("phone_number", "")
```

**connect_validation** - Validierung vor Verbindungsaufbau:
```yaml
connect_validation: |
  if not self._api_token:
      self._status = ConnectorStatus.ERROR
      return False
```

**connect_implementation** - Verbindungsaufbau:
```yaml
connect_implementation: |
  result = self._api_call("GET", "/status")
  if result:
      self._session_data = result
```

**send_message_implementation** - Nachricht senden:
```yaml
send_message_implementation: |
  payload = {"to": recipient, "message": content}
  result = self._api_call("POST", "/send", payload)
  return result is not None
```

**get_messages_implementation** - Nachrichten abrufen:
```yaml
get_messages_implementation: |
  result = self._api_call("GET", "/messages")
  if not result:
      return []
```

**parse_messages_implementation** - Nachrichten parsen:
```yaml
parse_messages_implementation: |
  for msg in result:
      messages.append(Message(
          channel="signal",
          sender=msg.get("sender", ""),
          content=msg.get("message", ""),
          timestamp=msg.get("timestamp", ""),
          direction="in",
          message_id=msg.get("id", "")
      ))
```

**helper_methods** - Hilfsmethoden:
```yaml
helper_methods: |
  def _api_call(self, method: str, endpoint: str, data: dict = None) -> any:
      """API aufrufen."""
      # Implementierung hier
      pass
```

## Template-Platzhalter

Folgende Platzhalter werden im `connector_template.py` ersetzt:

| Platzhalter | Beschreibung | Beispiel |
|-------------|--------------|----------|
| `{{CONNECTOR_NAME}}` | Klassenname | `Telegram` |
| `{{CONNECTOR_TYPE}}` | Connector-Typ | `telegram` |
| `{{CONNECTOR_DISPLAY_NAME}}` | Anzeigename | `Telegram Bot API` |
| `{{CONNECTOR_DESCRIPTION}}` | Beschreibung | `Implementiert BaseConnector...` |
| `{{CONNECTOR_MODULE}}` | Modul-/Dateiname | `telegram_connector` |
| `{{CONNECTOR_INSTANCE_NAME}}` | Instanz-Name | `telegram_main` |
| `{{RECIPIENT_EXAMPLE}}` | Empfänger-Beispiel | `chat_id` |
| `{{AUTH_TYPE}}` | Auth-Typ | `api_key` |
| `{{AUTH_CONFIG_EXAMPLE}}` | Auth-Beispiel | `{"bot_token": "..."}` |
| `{{OPTIONS_EXAMPLE}}` | Options-Beispiel | `{"owner_chat_id": "..."}` |
| `{{API_BASE_COMMENT}}` | API-Kommentar | `# Telegram Bot API` |
| `{{API_BASE_URL}}` | API-Basis-URL | `https://api.telegram.org/...` |
| `{{INIT_VARIABLES}}` | Init-Code | `self._bot_token = ...` |
| `{{CONNECT_VALIDATION}}` | Connect-Validierung | `if not self._bot_token: ...` |
| `{{CONNECT_IMPLEMENTATION}}` | Connect-Implementierung | `result = self._api_call(...)` |
| `{{SEND_MESSAGE_IMPLEMENTATION}}` | Send-Implementierung | `params = {...}` |
| `{{GET_MESSAGES_IMPLEMENTATION}}` | Get-Messages-Implementierung | `result = self._api_call(...)` |
| `{{PARSE_MESSAGES_IMPLEMENTATION}}` | Parse-Messages-Code | `for msg in result: ...` |
| `{{HELPER_METHODS}}` | Hilfsmethoden | `def _api_call(...): ...` |

## Setup-Wizard Konfiguration

Die `setup_questions` in der Template-YAML definieren den interaktiven Wizard:

```yaml
setup_questions:
  - name: api_token            # Variablen-Name
    prompt: "API Token"        # Frage an den Benutzer
    type: secret               # Typ: text, secret, choice
    required: true             # Pflichtfeld?
    storage: auth_config       # Wo speichern: auth_config oder options
    default: ""                # Optional: Default-Wert

  - name: mode
    prompt: "Modus"
    type: choice
    choices: ["production", "development"]
    default: production
    required: true
    storage: options
```

**Fragetypen:**
- `text` - Normale Texteingabe
- `secret` - Geheime Eingabe (wird nicht angezeigt)
- `choice` - Auswahl aus vordefinierten Optionen

**Storage:**
- `auth_config` - Wird in `connections.auth_config` gespeichert
- `options` - Wird in `connections` als separate Felder gespeichert

## Beispiele

### Telegram-Connector erstellen

```bash
bach connector setup-wizard

# Wizard Dialog:
> Template waehlen: 1 (telegram)
> Instanz-Name: telegram_main
> Bot-Token: 123456:ABC-DEF...
> Owner Chat-ID: 123456789
> Default Channel: 123456789
> Connector in Datenbank registrieren? [J/n]: j
```

### WhatsApp-Connector erstellen

```bash
bach connector setup-wizard

# Wizard Dialog:
> Template waehlen: 2 (whatsapp)
> Instanz-Name: whatsapp_business
> API Token: YOUR_BUSINESS_API_TOKEN
> Phone Number ID: 123456789
> Modus: 1 (business_api)
> Webhook Verify Token: your_verify_token
> Connector in Datenbank registrieren? [J/n]: j
```

## Connector testen

Nach der Erstellung eines Connectors:

```bash
# Status prüfen
bach connector list

# Verbindung testen
bach connector poll <name>

# Nachricht senden
bach connector send <name> <recipient> "Test-Nachricht"

# Daemon-Jobs einrichten (automatisches Polling)
bach connector setup-daemon

# Queue-Status prüfen
bach connector queue-status
```

## BaseConnector Interface

Alle Connectors implementieren das `BaseConnector` Interface:

```python
from connectors.base import BaseConnector, ConnectorConfig, Message

class MyConnector(BaseConnector):
    def __init__(self, config: ConnectorConfig):
        super().__init__(config)
        # Initialisierung

    def connect(self) -> bool:
        """Verbindung herstellen"""
        # Implementierung
        return True

    def disconnect(self) -> bool:
        """Verbindung trennen"""
        return True

    def send_message(self, recipient: str, content: str,
                     attachments: Optional[List[str]] = None) -> bool:
        """Nachricht senden"""
        # Implementierung
        return True

    def get_messages(self, since: Optional[str] = None,
                     limit: int = 50) -> List[Message]:
        """Nachrichten abrufen"""
        # Implementierung
        return []
```

## Best Practices

### 1. Fehlerbehandlung

Immer Try-Except verwenden und Fehler loggen:

```python
try:
    result = self._api_call("method", params)
    return True
except Exception as e:
    print(f"[ConnectorName Error] {type(e).__name__}: {e}", file=sys.stderr)
    return False
```

### 2. UTF-8 Encoding

UTF-8 Encoding fix am Anfang jeder Datei:

```python
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
```

### 3. Polling Runtime

Wenn der Connector Polling unterstützt, `poll_loop` und `poll_threaded` implementieren:

```python
def poll_threaded(self, on_message: Callable[[Message], None],
                  interval: float = 5.0) -> Tuple[threading.Thread, threading.Event]:
    """Startet Polling in eigenem Thread."""
    stop_event = threading.Event()
    thread = threading.Thread(
        target=self.poll_loop,
        args=(on_message, interval, stop_event),
        daemon=True, name="bach-connector-poll")
    thread.start()
    return thread, stop_event
```

### 4. Webhook-basierte Connectors

Für Webhook-basierte APIs (z.B. WhatsApp Business API):

```python
def process_webhook(self, webhook_data: dict) -> List[Message]:
    """Webhook-Daten verarbeiten."""
    messages = []
    # Parse webhook_data
    return messages
```

## Troubleshooting

### Wizard startet nicht

```bash
# YAML-Modul installieren
pip install pyyaml
```

### Template nicht gefunden

Prüfen Sie, dass die Template-Datei existiert:
```bash
ls -la connectors/templates/*_template.yaml
```

### Connector lädt nicht

Prüfen Sie:
1. Ist der Connector in `hub/connector.py` SUPPORTED_TYPES?
2. Ist die Datei korrekt benannt (`{type}_connector.py`)?
3. Ist die Klasse korrekt benannt (`{Type}Connector`)?

### Import-Fehler

Stellen Sie sicher, dass `connectors/base.py` existiert und das BaseConnector Interface definiert.

## Erweiterung des Systems

### Neues Template-Feature hinzufügen

1. Platzhalter in `connector_template.py` hinzufügen
2. Platzhalter in Template-YAML definieren
3. Replacement-Logic in `setup_wizard.py` erweitern

### Neuen Fragetyp hinzufügen

1. In Template-YAML `setup_questions` definieren
2. In `setup_wizard.py` `gather_configuration()` erweitern

## Support

Bei Fragen oder Problemen:

1. Dokumentation prüfen: `connectors/templates/README.md`
2. Beispiele anschauen: `telegram_template.yaml`, `whatsapp_template.yaml`
3. Bestehende Implementierungen studieren: `telegram_connector.py`

## Roadmap

- [ ] Signal-Connector Template
- [ ] Matrix-Connector Template
- [ ] Slack-Connector Template
- [ ] Discord Webhook Template
- [ ] Email-Connector Template
- [ ] SMS-Connector Template
- [ ] Webhook-basiertes generisches Template
- [ ] Template-Validator
- [ ] Template-Tests
- [ ] Web-UI für Setup-Wizard
