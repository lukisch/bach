---
name: archiv
metadata:
  version: 1.0.0
  last_updated: 2025-12-29
  parent: controll/manage
description: >
  Zentrales Archivsystem für RecludOS mit automatischer Erfassung.
  Verzeichnisführung und Export-Funktionalität.
---

# Archiv-System Skill

## 🎯 Zweck

Zentrales Archivsystem für RecludOS mit automatischer Erfassung, 
Verzeichnisführung und Export-Funktionalität.

**Löst:** Dezentrale Archive, kein Überblick, manueller Export

---

## 📂 Komponenten

**archiv_registry.json** - Verzeichnis aller Archiv-Ordner
**config.json** - Systemkonfiguration
**archiv_manager.py** - Management-Script

---

## 🔄 Workflow

**1. Boot (Schritt 10.5):**
```
→ Alle "Archiv"-Ordner scannen
→ In registry.json registrieren
→ Gelöschte Archive entfernen
→ Statistik anzeigen
```

**2. Verzeichnisführung:**
```
→ Alle archivierten Dateien tracken
→ Metadaten speichern (Datum, Größe, Quelle)
→ Kategorie-Tags unterstützen
```

**3. Export auf Befehl:**
```
→ Alle Archive in ZIP packen
→ Datum-basierter Dateiname
→ Nach main/system/system/system/system/exports/ verschieben
→ Archive leeren (optional)
```

---

## 📋 Typische Archiv-Ordner

**1. Workspace/Archiviert/**
- Zweck: Abgeschlossene Workspace-Dokumente
- Export: Monatlich

**2. reports/Archiviert/**
- Zweck: Alte Reports und Dokumentationen
- Export: Quartalsweise

**3. User/Archiv/**
- Zweck: Persönliche archivierte Dateien
- Export: Manuell

---

## ⚙️ Befehle

| Befehl | Aktion |
|--------|--------|
| "Archiv scannen" | Neue Archiv-Ordner finden |
| "Archiv Übersicht" | Alle Dateien anzeigen |
| "Archiv exportieren" | ZIP erstellen + leeren |
| "Archiv-Status" | Statistiken anzeigen |

---

## 📦 Export-Format

```
main/system/system/system/system/exports/
└── Archiv_Export_2025-12-28.zip
    ├── Workspace_Archiviert/
    │   ├── datei1.pdf
    │   └── datei2.md
    ├── reports_Archiviert/
    │   └── report.pdf
    └── MANIFEST.json
```

---

**Erstellt:** 2025-12-28  
**RecludOS:** v3.0.1  
**Status:** ✅ Implementiert
