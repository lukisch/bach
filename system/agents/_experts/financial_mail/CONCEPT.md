# KONZEPT: Financial Mail Expert

## Status: IN ENTWICKLUNG
Erstellt: 2026-01-20

---

## 1. Ueberblick

Der Financial Mail Expert sammelt und verarbeitet Finanzdaten aus E-Mails:
- **Rechnungen** von Anbietern (O2, Blau, Amazon, etc.)
- **Versicherungsscheine** und Beitragsrechnungen
- **Kontoauszuege** (N26, etc.)
- **Abonnements** erkennen und tracken

### Integration mit BACH

```
E-Mail -> mail_service.py -> financial_emails (DB) -> steuer_posten (optional)
                          -> financial_data.json (n8n Export)
```

---

## 2. Komponenten

### 2.1 Mail Service (`skills/_services/mail/`)

| Datei | Beschreibung |
|-------|--------------|
| `config.json` | Service-Konfiguration |
| `providers.json` | 40+ Anbieter mit Pattern-Matching |
| `schema_financial.sql` | Datenbank-Schema |
| `mail_service.py` | Hauptlogik (IMAP, Extraktion, Export) |

### 2.2 Daemon-Integration (`skills/_services/daemon/profiles/`)

- `financial_mail.json`: Stuendlicher automatischer Abruf

### 2.3 Datenbankschema (user.db)

```sql
-- Konten
mail_accounts (id, email, imap_host, ...)

-- Erkannte E-Mails
financial_emails (id, provider_id, betrag, steuer_relevant, ...)

-- Erkannte Abonnements
financial_subscriptions (id, provider_name, betrag_monatlich, ...)

-- Sync-Historie
mail_sync_runs (id, emails_processed, status, ...)
```

---

## 3. Unterstuetzte Anbieter

### Telekommunikation
- O2 Internet/Mobilfunk
- Blau Mobilfunk
- Telekom, Vodafone, 1&1

### Versicherungen
- Check24 Versicherungen
- Allianz, AXA, HUK, ERGO, DEVK
- Krankenversicherungen (TK, AOK, Barmer, etc.)
- KFZ, Haftpflicht, Hausrat, Rechtsschutz, BU

### Banking
- N26
- PayPal Transaktionen

### Shopping (Steuer-relevant bei beruflicher Nutzung)
- Amazon, Temu, eBay, AliExpress
- MediaMarkt/Saturn, Otto

### Software & Tools
- Microsoft 365, Adobe Creative Cloud
- JetBrains, GitHub, Google Workspace
- Hosting: Strato, Hetzner, Netcup

### Weitere
- Streaming (Netflix, Spotify, etc.)
- Energie (Strom/Gas)
- Weiterbildung (Udemy, Coursera)
- Spenden, Gewerkschaft, Berufsverband

---

## 4. Steuer-Integration

### Automatische Kategorisierung

| steuer_typ | Beschreibung |
|------------|--------------|
| Werbungskosten | Direkt absetzbar |
| Versicherung | Teilweise absetzbar |
| Sonderausgaben | Riester, Spenden, etc. |
| Nachweis | Dokumentation |

### Export nach steuer_posten

```python
# In mail_service.py
def export_to_steuer(email_id: int):
    """Uebernimmt E-Mail-Daten in steuer_posten"""
    # ... automatische Zuordnung
```

---

## 5. CLI-Befehle

```bash
# Synchronisierung
python mail_service.py sync
python mail_service.py sync --account 1

# Export
python mail_service.py export
python mail_service.py export --output /pfad/zu/export.json

# Konto hinzufuegen
python mail_service.py add-account --email user@gmail.com --password xxx

# Status
python mail_service.py status
python mail_service.py list
```

---

## 6. N8N Integration

### Export-Format (financial_data.json)

```json
{
  "_info": "BACH Financial Mail Export",
  "_version": "1.0",
  "_exported": "2026-01-20T12:00:00",
  "summary": {
    "total": 150,
    "steuer_count": 85,
    "total_betrag": 4567.89,
    "steuer_betrag": 2345.67
  },
  "emails": [...],
  "subscriptions": [...]
}
```

### Webhook-Trigger

Der Export kann per Webhook an n8n gesendet werden:
```python
# Optionale n8n Webhook-Integration
def notify_n8n(data):
    requests.post(N8N_WEBHOOK_URL, json=data)
```

---

## 7. GUI-Dashboard (geplant)

### Route: `/financial` oder `/mail`

```
+------------------------------------------------------------------+
| FINANCIAL MAIL - Finanzdaten aus E-Mails                          |
+------------------------------------------------------------------+
| Konten: 2 aktiv | Letzte Sync: vor 45 Min | Neue: 5              |
+------------------------------------------------------------------+

+------------------+----------+----------+--------+----------------+
| Anbieter         | Kategorie| Betrag   | Datum  | Status         |
+------------------+----------+----------+--------+----------------+
| O2 Rechnung      | Telekom  | 29,99 EUR| Jan 18 | [Neu]          |
| Check24 Police   | Versich. | 120,00   | Jan 15 | [Verarbeitet]  |
| Amazon Bestellung| Shopping | 45,67    | Jan 14 | [Exportiert]   |
+------------------+----------+----------+--------+----------------+

+------------------------------------------------------------------+
| AKTIVE ABONNEMENTS                                                 |
+------------------------------------------------------------------+
| Netflix          | 12,99/Mo  | Streaming    | [Kuendigen]        |
| O2 Internet      | 29,99/Mo  | Telekom      | Steuer-relevant    |
| Microsoft 365    | 7,00/Mo   | Software     | Steuer-relevant    |
+------------------------------------------------------------------+
```

---

## 8. Sicherheit

### Passwort-Speicherung
- Keyring-Integration (Windows Credential Store)
- Keine Klartext-Passwoerter in Config

### OAuth (geplant)
- Gmail API fuer Google-Konten
- Outlook OAuth fuer Microsoft-Konten

---

## 9. Dateien

```
skills/_services/mail/
  __init__.py
  config.json
  providers.json          # 40+ Anbieter
  schema_financial.sql    # DB-Schema
  mail_service.py         # Hauptlogik (IMAP + Gmail API)
  account_manager.py      # Kontenverwaltung

skills/_services/mail/credentials/
  gmail_credentials.json  # Google OAuth Client
  gmail_token.json        # OAuth Token (automatisch erstellt)

skills/_services/daemon/profiles/
  financial_mail.json     # Daemon-Profil

agents/_experts/financial_mail/
  CONCEPT.md              # Diese Datei

gui/
  templates/financial.html # Dashboard mit Kontenverwaltung

data/
  financial_data.json     # N8N Export
  mail_attachments/       # Gespeicherte PDFs
```

---

## 10. Abhaengigkeiten

```
# Minimal (bereits in BACH)
sqlite3 (stdlib)
imaplib (stdlib)
email (stdlib)

# Optional
keyring>=24.0.0           # Sichere Passwort-Speicherung
```

---

## 11. Roadmap

### Phase 1: Basis (DONE)
- [x] Schema definieren
- [x] Provider-Liste erstellen
- [x] IMAP-Abruf implementieren
- [x] Pattern-Matching
- [x] N8N Export

### Phase 2: Integration
- [ ] GUI-Dashboard
- [ ] API-Endpunkte
- [ ] Steuer-Export
- [ ] Abo-Erkennung verbessern

### Phase 3: Erweiterungen
- [ ] OAuth-Support
- [ ] PDF-Text-Extraktion (OCR)
- [ ] LLM-basierte Datenextraktion
- [ ] Benachrichtigungen
