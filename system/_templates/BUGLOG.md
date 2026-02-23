# Buglog - Bekannte Probleme

Dokumentation bekannter Probleme, Workarounds und deren Status.

> Für aktiv bearbeitete Bugs: Issue-Tracker oder Task-System verwenden.
> BUGLOG ist für dokumentierte, bekannte Einschränkungen.

---

## Aktive Probleme

### [BUG-001] Kurze Beschreibung

**Status:** offen | workaround | won't fix | in Bearbeitung

**Betrifft:** Komponente, Version

**Beschreibung:**
Was passiert und wann tritt es auf?

**Workaround:**
Falls vorhanden - wie kann man das Problem umgehen?

**Ursache:**
Falls bekannt - warum passiert das?

**Verwandte Issues:** #123, #456

---

### [BUG-002] Beispiel: Encoding-Problem Windows Console

**Status:** workaround

**Betrifft:** Windows, cp1252 Konsole

**Beschreibung:**
Emojis und Unicode-Zeichen crashen die Windows-Konsole.

**Workaround:**
Keine Emojis in print() verwenden. Stattdessen [OK], [ERROR], [INFO].

**Ursache:**
Windows Console verwendet cp1252 statt UTF-8.

---

## Geschlossene Probleme

### [BUG-000] Beispiel geschlossen

**Status:** behoben in v1.2.3

**Lösung:**
Beschreibung der Lösung.

---

## Status-Legende

| Status | Bedeutung |
|--------|-----------|
| offen | Bekannt, noch nicht bearbeitet |
| workaround | Umgehung dokumentiert |
| in Bearbeitung | Wird aktiv gefixt |
| behoben | In Version X gefixt |
| won't fix | Wird nicht behoben (mit Begründung) |

---

*Erstellt mit BACH Template*
