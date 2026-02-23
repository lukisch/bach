---
name: connectors
version: 2.1.0
type: service
author: BACH Team
created: 2026-02-06
updated: 2026-02-08
anthropic_compatible: true
status: beta

dependencies:
  tools: []
  services: [queue_processor]
  workflows: []

metadata:
  inputs: "connector-config, outgoing-messages"
  outputs: "incoming-messages, delivery-status, queue-stats"

description: >
  Connector-System fuer externe Kommunikation (Telegram, Discord,
  HomeAssistant). Bidirektionales Messaging mit zuverlaessiger
  Zustellung via Queue, Retry/Backoff und Circuit Breaker.
---

# Connectors

## Status: BETA

Bidirektionale Kommunikation mit externen Services.
3 Runtime-Adapter verfuegbar, Queue-Processor fuer zuverlaessige Zustellung.

## Zwei Subsysteme

### 1. Volle Connectors (bidirektional)

| Typ | Status | Features |
|-----|--------|----------|
| Telegram | Beta | Polling, Owner-Filter, Send, Poll-Loop |
| Discord | Beta | Webhook-Send, Incremental Polling, Bot-Filter |
| HomeAssistant | Beta | States, Services, History, Events |
| Signal | Geplant | signal-cli Integration |
| WhatsApp | Geplant | Baileys Integration |

### 2. Notification-Channels (nur Senden)

| Channel | Status | Dispatch |
|---------|--------|----------|
| Telegram | Aktiv | Bot API via secrets.json |
| Discord | Aktiv | Webhook |
| Slack | Aktiv | Webhook |
| Webhook | Aktiv | Generischer HTTP POST |
| Email | Aktiv | SMTP_SSL |

Neue Channels: siehe `connectors/templates/README.md`

## Secrets-Management

**Keys gehoeren in `user/secrets/secrets.json` (dist_type=0), NICHT in bach.db!**
In der DB steht nur `auth_type='secrets_file'` als Verweis.

## Architektur

```
  CLI / REST-API / Daemon
         |
  ┌──────┴──────────────────────┐
  |                             |
  hub/connector.py (bidir.)     hub/notify.py (nur Senden)
  |                             |
  queue_processor.py            _load_secrets()
  |                             |
  connectors/ (Adapter)         user/secrets/secrets.json
    ├── base.py (ABC)
    ├── telegram_connector.py
    ├── discord_connector.py
    └── homeassistant_connector.py
```

## Queue-System (v2.0)

- **Retry**: Exponentieller Backoff (30s → 480s, 5 Versuche)
- **Circuit Breaker**: 5 Fehler → 5 Min Sperre, Auto-Reset
- **Dead Letter**: Nach max_retries, manuell wiederherstellbar
- **Kontext-Hints**: ContextInjector + context_triggers beim Routing
- **Daemon**: 2 automatische Jobs (poll_and_route 2min, dispatch 1min)

## Verwendung

```bash
# Connector registrieren
bach connector add telegram mein_bot

# Einmalig pollen
bach connector poll mein_bot

# Queue verwalten
bach connector queue-status
bach connector retry all

# Automatisch (Daemon)
bach connector setup-daemon
bach daemon start --bg
```

## REST-API (Port 8001)

```
POST /api/v1/messages/send      Queue Nachricht
GET  /api/v1/messages/queue     Queue-Status
GET  /api/v1/messages/inbox     Inbox (paginiert)
POST /api/v1/messages/route     Routing ausloesen
```

## Dateien

```
connectors/
├── SKILL.md                    # Diese Datei
├── base.py                     # BaseConnector ABC
├── telegram_connector.py       # Telegram Bot API (bidirektional)
├── discord_connector.py        # Discord REST + Webhook
├── homeassistant_connector.py  # Home Assistant API
├── signal_connector.py         # Signal (geplant)
├── whatsapp_connector.py       # WhatsApp (Beispiel)
└── templates/
    ├── README.md               # Anleitung: Neue Connectors + Channels
    ├── connector_template.py   # Code-Template (volle Connectors)
    ├── notification_template.yaml  # Anleitung: Notification-Channels
    ├── setup_wizard.py         # Interaktiver Setup-Wizard
    ├── telegram_template.yaml  # Telegram-Konfiguration
    └── whatsapp_template.yaml  # WhatsApp-Konfiguration

hub/connector.py                # CLI-Handler (bidirektionale Connectors)
hub/notify.py                   # CLI-Handler (Notification-Channels)
hub/_services/connector/
├── __init__.py
└── queue_processor.py          # Queue-Processor (Kern)

user/secrets/secrets.json       # API-Keys (dist_type=0, PRIVAT!)

gui/api/messages_api.py         # REST-API Router
db/migrations/001_*.sql         # Schema-Migration
```

## Changelog

### v2.1.0 (2026-02-17)
- Notification-Channel-System via hub/notify.py
- Telegram-Dispatch in notify.py (Push-Nachrichten)
- Secrets-Management: user/secrets/secrets.json (dist_type=0)
- Keys raus aus bach.db, rein in secrets.json
- notification_template.yaml: Anleitung fuer neue Channels
- README.md: Erweitert um Notification-Channels + Secrets-Hinweis
- Partner-Tagging-Konvention ([MCMC], [ZENODO], [BACH], etc.)

### v2.0.0 (2026-02-08)
- Queue-Processor mit Retry/Backoff und Circuit Breaker
- Daemon-Integration (automatisches Polling + Dispatch)
- REST-API (4 Endpoints: send, queue, inbox, route)
- ContextInjector + context_triggers beim Routing
- 3 neue CLI-Operationen: setup-daemon, queue-status, retry

### v1.1.0 (2026-02-08)
- Telegram: Owner-Filter, Poll-Loop, Threaded Polling
- Discord: Incremental Polling, Bot-Filter, Poll-Loop
- Connector Runtime: _instantiate, _poll, _dispatch in hub/connector.py

### v1.0.0 (2026-02-06)
- Initiale Connector-Verwaltung (add/remove/enable/disable)
- BaseConnector ABC mit Message-Dataclass
- Telegram, Discord, HomeAssistant Adapter

---
BACH Skill-Architektur v2.0
