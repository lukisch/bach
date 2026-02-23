---
name: registry-watcher
metadata:
  version: 2.0.0
  last_updated: 2025-12-29
  parent: controll/manage
description: >
  Zentrales Verzeichnis ALLER Registries im RecludOS-System.
  Schafft Übersicht über verteilte Registry-Dateien.
---

# Registry-Watcher Skill

## 🎯 Zweck

Zentrales Verzeichnis ALLER Registries im RecludOS-System.

**Problem gelöst:** Registries sind über das gesamte System verteilt - dieser Skill schafft Übersicht.

---

## 📂 Dateien

**master_registry.json** - Verzeichnis aller Registries
- Pfad zu jeder Registry
- Typ, Zweck, Priorität
- Boot-Integration

**config.json** - Konfiguration
- Auto-Scan Einstellungen
- Health-Check Intervalle

---

## 🔄 Boot-Integration

**Schritt 11:** Registry-Watcher laden
```
→ read_file("registry-watcher/master_registry.json")
→ Alle Registries bekannt
→ Optional: Health-Check durchführen
```

---

## 📋 Registries

**Critical (2):**
- system-registry.json
- skill_registry.json

**High (3):**
- agents/registry.json
- services/registry.json
- task-manager.json

**Medium (5):**
- Tool-Registries
- External-Tools
- Document-Rules
- Papierkorb

**Low (2):**
- Directory-Watcher
- Self (Meta)

---

## ✅ Verwendung

**Registry finden:**
```javascript
master = read_file("master_registry.json")
path = master.registries.core_system[0].path
/ → "main/main/main/system/boot/system-registry.json"
```

**Alle Registries iterieren:**
```javascript
for category in master.registries:
    for registry in category:
        load(registry.path)
```

---

**Erstellt:** 2025-12-27  
**RecludOS:** v3.0.0