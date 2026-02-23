# Connector Template System - Schnellstart

## Installation

Das Template-System ist bereits installiert. Benötigte Abhängigkeiten:
- Python 3.8+
- PyYAML (bereits installiert)

## Neuen Connector in 3 Minuten erstellen

### Option 1: Interaktiver Wizard (Empfohlen)

```bash
bach connector setup-wizard
```

Folgen Sie einfach den Anweisungen! Der Wizard:
1. Zeigt verfügbare Templates
2. Fragt nach Konfiguration
3. Generiert Connector-Code
4. Registriert in Datenbank

### Option 2: Manuell

```bash
# 1. Connector in DB registrieren
bach connector add whatsapp whatsapp_main

# 2. Auth-Config setzen (direkt in DB oder via Python)
# 3. Connector testen
bach connector poll whatsapp_main
```

## Verfügbare Templates

| Template | Beschreibung | Status |
|----------|--------------|--------|
| **telegram** | Telegram Bot API | ✅ Produktiv |
| **whatsapp** | WhatsApp Business API | ✅ Beispiel |
| signal | Signal Messenger | 🚧 Geplant |
| discord | Discord Bot | ✅ Vorhanden (kein Template) |

## Beispiel: WhatsApp-Connector erstellen

```bash
$ bach connector setup-wizard

=============================================================
BACH Connector Setup Wizard
=============================================================

Verfuegbare Templates:

  1. telegram
  2. whatsapp

Template waehlen (Nummer oder Name): 2

 Template: WhatsApp Business API
 Beschreibung: Implementiert BaseConnector fuer WhatsApp Business API.
  Unterstuetzt Baileys (WhatsApp Web) oder offizielle Business API.

Konfiguration:
------------------------------------------------------------

Instanz-Name (z.B. whatsapp_main): whatsapp_business

WhatsApp Business API Token (von Meta Business Manager) (wird nicht angezeigt):
  > [Eingabe...]

Phone Number ID (aus WhatsApp Business Manager): 123456789

Modus (business_api oder baileys)
  1. business_api (default)
  2. baileys
  Auswahl (Nummer oder Text): 1

Webhook Verify Token (fuer Webhook-Setup) (wird nicht angezeigt):
  > [Eingabe...]

------------------------------------------------------------
Konfiguration abgeschlossen.

[OK] Connector-Datei erstellt: connectors/whatsapp_connector.py

Connector in Datenbank registrieren? [J/n]: j

[OK] Connector 'whatsapp_business' registriert!

Naechste Schritte:
  1. Connector testen: bach connector poll whatsapp_business
  2. Daemon-Jobs einrichten: bach connector setup-daemon

=============================================================
Setup abgeschlossen!
=============================================================
```

## Nach dem Setup

### 1. Connector testen

```bash
# Status prüfen
bach connector list

# Verbindung testen
bach connector poll whatsapp_business

# Test-Nachricht senden
bach connector send whatsapp_business "49123456789@s.whatsapp.net" "Test"
```

### 2. Automatisches Polling einrichten

```bash
# Daemon-Jobs für alle Connectors einrichten
bach connector setup-daemon

# Queue-Status prüfen
bach connector queue-status
```

### 3. Monitoring

```bash
# Connector-Status
bach connector status

# Nachrichten anzeigen
bach connector messages whatsapp_business --limit 10

# Unverarbeitete Nachrichten
bach connector unprocessed
```

## Eigenes Template erstellen

### 1. Template-YAML erstellen

Erstellen Sie `connectors/templates/signal_template.yaml`:

```yaml
connector_name: Signal
connector_type: signal
connector_display_name: Signal Messenger
connector_description: |
  Implementiert BaseConnector fuer Signal Messenger.

connector_module: signal_connector
connector_instance_name: signal_main
recipient_example: "+49123456789"

auth_type: none
auth_config_example: |
  {}
options_example: |
  {"phone_number": "+49123456789"}

api_base_comment: "# Signal verwendet signal-cli"
api_base_url: ""

init_variables: |
  self._phone_number = config.options.get("phone_number", "")
  self._signal_cli = config.options.get("signal_cli_path", "signal-cli")

connect_validation: |
  if not self._phone_number:
      self._status = ConnectorStatus.ERROR
      return False

connect_implementation: |
  # Signal-CLI Verbindung testen
  pass

send_message_implementation: |
  # Nachricht via signal-cli senden
  pass

get_messages_implementation: |
  # Nachrichten via signal-cli abrufen
  pass

parse_messages_implementation: |
  # Nachrichten parsen
  pass

helper_methods: |
  def _signal_cli_call(self, args: list) -> str:
      """Signal-CLI aufrufen."""
      import subprocess
      cmd = [self._signal_cli] + args
      result = subprocess.run(cmd, capture_output=True, text=True)
      return result.stdout

setup_questions:
  - name: phone_number
    prompt: "Registrierte Telefonnummer"
    type: text
    required: true
    storage: options
```

### 2. Template nutzen

```bash
bach connector setup-wizard
# Wählen Sie Ihr neues Template!
```

## Troubleshooting

### "Template nicht gefunden"

```bash
# Prüfen, dass YAML-Datei existiert
ls -la connectors/templates/*_template.yaml
```

### "Import Error"

```bash
# PyYAML installieren
pip install pyyaml
```

### "Connector lädt nicht"

1. Prüfen Sie Dateinamen: `{type}_connector.py`
2. Prüfen Sie Klassennamen: `{Type}Connector`
3. Prüfen Sie SUPPORTED_TYPES in `hub/connector.py`

## Weitere Informationen

- Vollständige Dokumentation: `connectors/templates/README.md`
- Beispiel-Templates: `telegram_template.yaml`, `whatsapp_template.yaml`
- Beispiel-Implementierung: `telegram_connector.py`

## Support

Bei Fragen:
1. README.md lesen
2. Beispiele anschauen
3. Code kommentieren und Issues melden
