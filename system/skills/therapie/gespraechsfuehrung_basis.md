---
name: gespraechsfuehrung-basis
version: 1.0.0
type: therapie-skill
category: Gespraechsfuehrung
author: BACH Team (SQ046)
created: 2026-02-22
status: aktiv
parent_agent: gesundheitsassistent
expert: psycho-berater
---

# Gespraechsfuehrung Basis

> Grundlagen therapeutischer Kommunikation: Aktives Zuhoeren, Spiegeln, Paraphrasieren

---

## Kontext

Dieses Template beschreibt therapeutische Grundtechniken der Gespraechsfuehrung.
Es dient als Kontext-Injektions-Vorlage fuer den Psycho-Berater-Experten.

**Hinweis:** Diese Techniken sind Unterstuetzung, kein Ersatz fuer professionelle Therapie.
Bei akuten Krisen immer an professionelle Hilfe verweisen.

**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Aktives Zuhoeren

**Ziel:** Vollstaendiges Verstaendnis signalisieren, Gesprochenes wirklich aufnehmen.

**Techniken:**

- **Verbale Bestaetigung:** "Ich verstehe", "Mhm", "Das klingt schwer"
- **Nachfragen:** "Kannst du das genauer beschreiben?" / "Was meinst du damit?"
- **Zusammenfassen:** Am Ende eines Abschnitts kurz wiederholen was gehoert wurde
- **Non-Direktives Zuhoeren:** Keine Ratschlaege geben, bevor die Person fertig ist

**Haltung:** Volle Aufmerksamkeit, keine Unterbrechungen, keine Wertung.

**Gespraeches-Formel:**
> "Was ich gehoert habe, ist [Zusammenfassung]. Ist das korrekt?"

---

## 2. Spiegeln (Mirroring)

**Ziel:** Empfundene Emotionen zurueckgeben, Gefuehle sichtbar machen.

**Techniken:**

- **Einfaches Spiegeln:** Letztes Wort oder letzten Satz leicht umformuliert wiederholen
- **Emotionales Spiegeln:** Benannte oder implizierte Emotion ansprechen
  > "Es klingt, als ob du gerade sehr erschoepft bist."
- **Koerpersprache spiegeln:** (in Praesenz) Haltung anpassen

**Vorsicht:**
- Nicht uebertreiben — zu viel Spiegeln wirkt kuenstlich
- Keine Interpretation uebermaessig ausbauen

**Beispiele:**
> Person: "Ich weiss nicht mehr weiter."
> Spiegel: "Du weisst nicht mehr weiter — das klingt, als waere alles sehr viel gerade."

---

## 3. Paraphrasieren

**Ziel:** Den Kerninhalt in eigenen Worten wiedergeben, Verstaendnis pruefen.

**Unterschied zu Spiegeln:** Spiegeln gibt Emotion zurueck, Paraphrasieren gibt Inhalt/Bedeutung zurueck.

**Aufbau:**
1. Inhalt kurz zusammenfassen
2. Kernaussage hervorheben
3. Rueckfrage stellen

**Formel:**
> "Wenn ich dich richtig verstehe, sagst du [Paraphrase]. Stimmt das so?"

**Beispiele:**
> Person: "Meine Mutter nervt mich jeden Tag mit denselben Vorwuerfen und ich kann nicht mehr."
> Paraphrase: "Also fuehlt sich das an wie eine Endlosschleife, aus der du gerade keinen Ausweg siehst?"

---

## 4. Offene Fragen

**Ziel:** Exploration anregen, ohne Antworten vorzugeben.

**Merkmale offener Fragen:**
- Beginnen mit: Wie, Was, Inwiefern, Beschreibe, Erklaere
- Lassen Raum fuer eigene Antworten
- Keine Ja/Nein-Antworten moeglich

**Beispiele:**
- "Wie hat sich das angefuehlt?"
- "Was passiert in dir, wenn das geschieht?"
- "Wie gehst du normalerweise damit um?"

**Geschlossene Fragen vermeiden:**
- "Hat das weh getan?" -> besser: "Wie hat sich das angefuehlt?"
- "Bist du traurig?" -> besser: "Was geht dir gerade durch den Kopf?"

---

## 5. Validierung

**Ziel:** Gefuehle und Reaktionen als nachvollziehbar und berechtigt bestaetigen.

**Wichtig:** Validierung bedeutet nicht Zustimmung, sondern Verstaendnis.

**Formel:**
> "Es macht total Sinn, dass du dich so fuehlst, angesichts [Situation]."

**Stufen der Validierung (nach Linehan):**
1. Aufmerksam zuhoeren (Anwesenheit zeigen)
2. Genau reflektieren (was wurde gesagt?)
3. Nicht-Ausgesprochenes erkennen
4. Ursache im Kontext verstehen
5. Reaktion als nachvollziehbar anerkennen
6. Radikale Echtheit (ehrliche, gleichwertige Reaktion)

---

## 6. Gespraeches-Phasen

| Phase | Ziel | Techniken |
|-------|------|-----------|
| Opening | Ankommen, Sicherheit schaffen | Begruessung, offene Fragen, Wertfreiheit signalisieren |
| Exploration | Thema ergruenden | Aktives Zuhoeren, Nachfragen, Paraphrasieren |
| Vertiefung | Tiefere Ebenen erreichen | Spiegeln, Validierung, emotionale Resonanz |
| Integration | Zusammenfuehren, Naechstes | Zusammenfassen, Hypothesen pruefen, Ausblick |
| Closing | Abschliessen, Uebergang | Rueckblick, Hausaufgabe, Verabschiedung |

---

## Anwendung im BACH-Kontext

Dieses Template wird vom psycho-berater Experten genutzt:
- Als Kontext bei Gespraechen (via SKILL.md Einbindung)
- Als Referenz fuer Technik-Auswahl
- Als Basis fuer Sitzungsdokumentation

**Aktivierung:**
```
bach psycho session start
# -> Psycho-Berater laedt dieses Template als Kontext
```

---

*Erstellt: 2026-02-22 | SQ046 Phase 1 | BACH Therapie-Skills*
