# BACH Claude Bridge -- Server Deployment

## Voraussetzungen

```bash
pip install fastapi uvicorn
```

## Konfiguration

In `config.json`:
```json
{
    "mode": "server",
    "server": {
        "host": "127.0.0.1",
        "port": 8080,
        "auth_token": "DEIN_SICHERES_TOKEN",
        "cors_origins": ["http://localhost:3000"]
    }
}
```

**Wichtig:** `auth_token` setzen! Ohne Token ist die API unauthentifiziert.

## Lokaler Start

```bash
PYTHONIOENCODING=utf-8 python bridge_daemon.py --server
```

Oder via config `"mode": "server"`:
```bash
PYTHONIOENCODING=utf-8 python bridge_daemon.py
```

## Hetzner-Deployment (CCX33)

### SSH-Tunnel (Entwicklung)

```bash
ssh -L 8080:localhost:8080 -i ~/.ssh/id_ed25519_mcmc root@YOUR_SERVER_IP
```

Dann lokal: `http://localhost:8080/docs`

### Systemd Service (Produktion)

Datei: `/etc/systemd/system/bach-bridge.service`

```ini
[Unit]
Description=BACH Claude Bridge Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/cfm-cosmology/BACH/system/hub/_services/claude_bridge
Environment=PYTHONIOENCODING=utf-8
ExecStart=/usr/bin/python3 bridge_daemon.py --server
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable bach-bridge
systemctl start bach-bridge
systemctl status bach-bridge
journalctl -u bach-bridge -f
```

### Hetzner-Hinweise

- Server: CCX33 (8 vCPU AMD, 32 GB RAM), IP: YOUR_SERVER_IP
- `nice -n 10` verwenden wenn andere Prozesse laufen
- Host auf `127.0.0.1` belassen (kein externer Zugriff ohne Tunnel)
- Fuer externen Zugriff: Reverse-Proxy (nginx) mit HTTPS + Firewall-Regel

## API-Endpunkte

| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| POST | `/api/message` | Nachricht an BACH senden |
| GET | `/api/status` | Bridge-Status abrufen |
| POST | `/api/control` | Steuerung (pause/resume/reload_config) |

### Authentifizierung

Bearer-Token im Header:
```
Authorization: Bearer DEIN_TOKEN
```

### Beispiele

```bash
# Status
curl -H "Authorization: Bearer TOKEN" http://localhost:8080/api/status

# Nachricht senden
curl -X POST http://localhost:8080/api/message \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hallo BACH!", "sender": "api-test"}'

# Pause
curl -X POST http://localhost:8080/api/control \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "pause"}'
```
