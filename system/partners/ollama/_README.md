# Ollama Partner Workspace

## Rolle
Ollama ist die lokale AI fuer Bulk-Verarbeitung und Offline-Tasks.

## Ordnerstruktur
- `inbox/` - Auftraege an Ollama
- `outbox/` - Ergebnisse von Ollama
- `workspace/` - Arbeitsdateien

## Staerken
- Token-freie Verarbeitung
- Bulk-Text-Operationen
- Embeddings-Generierung
- Offline-Verfuegbarkeit

## API
```
Endpoint: http://127.0.0.1:11434
Modelle: Mistral, nomic-embed-text
```

## Zugriffs-Typ
**API-basiert** - Ollama ist ein LLM-Server ohne eigenen Dateisystem-Zugriff.
Claude ruft Ollama via API auf und uebergibt Aufgaben.

## Task-Workflow
1. Claude legt Auftrag in `inbox/` ab
2. Claude ruft Ollama-API mit Inhalt auf
3. Ergebnis wird in `outbox/` gespeichert
4. Claude markiert Task als done

## Status
Derzeit: Standby (keine aktiven Tasks)
