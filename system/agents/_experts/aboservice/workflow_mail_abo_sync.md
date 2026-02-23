# Workflow: Mail-Abo-Abgleich (Task #814)

## Übersicht

Der **Mail-Abo-Abgleich** ermöglicht es, Abonnements, die der `mail_service` automatisch aus E-Mails extrahiert hat, in die zentrale Abonnement-Verwaltung von BACH zu übernehmen.

## Voraussetzungen

1. **Mail-Konto konfiguriert:** Ein E-Mail-Konto muss in `bach.db` (Tabelle `mail_accounts`) hinterlegt sein.
2. **Mail-Scan ausgeführt:** Der Befehl `bach mail fetch` (oder der entsprechende Service) muss bereits Finanz-E-Mails erkannt und in der Tabelle `financial_subscriptions` abgelegt haben.

## Durchführung

### 1. Synchronisation (Vorschau)

Um zu sehen, welche Abos aus E-Mails neu erkannt wurden, ohne sie direkt zu speichern:

```bash
bach abo sync-mail --dry-run
```

### 2. Synchronisation (Ausführung)

Um die Abos tatsächlich in die zentrale Liste zu übernehmen:

```bash
bach abo sync-mail
```

### 3. Kontrolle und Bestätigung

Nach dem Abgleich können die neuen Abos in der zentralen Liste eingesehen werden:

```bash
bach abo list
```

Neue Abos aus Mails werden zunächst im Status **"Erkannt"** (bestaetigt=0) angelegt. Nutze den `confirm` Befehl, um sie dauerhaft zu aktivieren:

```bash
bach abo confirm <ID>
```

## Technische Details

- **Deduplizierung:** Der Sync-Service prüft anhand des Anbieternamens, ob das Abo bereits in der Liste existiert, um Dubletten zu vermeiden.
- **Speicherort:** Daten fließen von `financial_subscriptions` nach `abo_subscriptions`.
- **Log:** Die Synchronisation wird im Standard-Log protokolliert.

## Fehlerbehebung

- Wenn keine Abos gefunden werden, prüfe mit `bach mail status`, ob der E-Mail-Abruf erfolgreich war.
- Bei Fehlermeldungen zur Datenbank-Struktur führe `bach abo init` aus.
