---
name: kognitive-umstrukturierung
version: 1.0.0
type: therapie-skill
category: Verhaltenstherapie (VT)
author: BACH Team (SQ046)
created: 2026-02-22
status: aktiv
parent_agent: gesundheitsassistent
expert: psycho-berater
---

# Kognitive Umstrukturierung

> Verhaltenstherapeutische Kerntechnik: ABC-Schema, dysfunktionale Gedanken erkennen und veraendern

---

## Kontext

Kognitive Umstrukturierung ist eine Kerntechnik der kognitiven Verhaltenstherapie (KVT).
Sie hilft dabei, automatische negative Gedanken zu erkennen, zu hinterfragen und durch
hilfreichere Alternativen zu ersetzen.

**Hinweis:** Dies ist Unterstuetzung, kein Ersatz fuer professionelle Therapie.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. ABC-Modell (Ellis)

Das ABC-Modell erklaert wie Ereignisse, Gedanken und Gefuehle zusammenhaengen.

```
A (Activating Event)   ->  B (Beliefs / Gedanken)  ->  C (Consequences / Gefuehle/Verhalten)
Ausloser                   Bewertung / Ueberzeugung     Emotionale Folge
```

**Wichtig:** Nicht das Ereignis (A) erzeugt die Emotion (C), sondern die Bewertung (B)!

**Beispiel:**
```
A: Chef kritisiert einen Bericht im Meeting
B: "Ich bin inkompetent, alle denken das jetzt"
C: Scham, Rueckzug, Vermeidung zukuenftiger Beitraege
```

**Ziel:** B veraendern, um C zu beeinflussen.

---

## 2. Automatische Negative Gedanken (ANGs) erkennen

**Was sind ANGs?**
- Schnelle, automatische Bewertungen in stressigen Situationen
- Oft als Fakten wahrgenommen, obwohl sie Interpretationen sind
- Tendieren zu Uebertreibung, Verallgemeinerung, Katastrophisierung

**Typische Erkennungsmerkmale:**
- Absolutes Denken: "immer", "nie", "alle", "niemand"
- Katastrophisierung: "Das wird furchtbar enden"
- Gedankenlesen: "Er denkt bestimmt, dass..."
- Uebergeneralisierung: "Das klappt bei mir nie"

**Erkennungs-Fragen:**
- "Was ist dir durch den Kopf gegangen, als das passiert ist?"
- "Wenn du an die Situation denkst, welche Worte kommen?"
- "Was befuerchtest du koennte passieren?"

---

## 3. Kognitive Verzerrungen (Denkfehler)

| Denkfehler | Beschreibung | Beispiel |
|------------|--------------|---------|
| Alles-oder-nichts | Schwarz-Weiss-Denken | "Wenn ich nicht perfekt bin, bin ich ein Versager" |
| Uebergeneralisierung | Ein Fall = Allgemeines Muster | "Das geht bei mir immer schief" |
| Gedankenfilter | Nur Negatives wahrnehmen | Focussieren auf einzigen Kritikpunkt im Feedback |
| Gedankenlesen | Andere wissen was andere denken | "Er hasst mich sicher" |
| Katastrophisieren | Schlimmsten Fall annehmen | "Das wird eine Katastrophe werden" |
| Emotionale Begruendung | Gefuehl = Realitaet | "Ich fuehle mich dumm, also bin ich dumm" |
| Sollte/Muss-Denken | Starre Regeln | "Ich muesste das koennen" |
| Personalisierung | Alles auf sich beziehen | "Der schlechte Auftrag war meine Schuld" |

---

## 4. Gedanken hinterfragen (Sokratisches Fragen)

**Ziel:** Gedanken nicht direkt widerlegen, sondern Pruefung anregen.

**Fragen-Set:**

1. **Beweise pruefen:**
   - "Welche Beweise gibt es dafuer?"
   - "Welche Beweise sprechen dagegen?"

2. **Alternative Erklaerungen:**
   - "Gibt es andere Erklaerungen dafuer?"
   - "Wie wuerde jemand anderes diese Situation sehen?"

3. **Konsequenzen einschaetzen:**
   - "Was ist das Schlimmste, was passieren koennte? Wie wahrscheinlich ist das?"
   - "Was ist das Beste, was passieren koennte?"
   - "Was ist das Realistischste?"

4. **Nuetzlichkeit pruefen:**
   - "Hilft mir dieser Gedanke dabei, meine Ziele zu erreichen?"
   - "Was wuerde ich einem guten Freund sagen, der so denkt?"

---

## 5. Kognitive Umstrukturierung Schritt-fuer-Schritt

### Protokoll-Format (Gedankenprotokoll)

```
SITUATION
Was ist passiert? (Wann? Wo? Wer war dabei?)
[Freitext]

GEDANKE
Was bin ich dadurch durch den Kopf gegangen?
Automatischer Gedanke: [...]
Glaube ich daran? (0-100%): [...]%

EMOTION
Welche Emotionen hatte ich?
Emotion: [...]    Intensitaet (0-100%): [...]%

DENKFEHLER
Welche kognitiven Verzerrungen stecken darin?
[Liste aus Tabelle oben]

PRUEFEN
Beweise dafuer: [...]
Beweise dagegen: [...]
Alternative Sichtweise: [...]

ALTERNATIVER GEDANKE
Ausgewogener, realistischerer Gedanke:
[...]
Glaube ich daran? (0-100%): [...]%

ERGEBNIS
Emotion danach: [...]   Intensitaet: [...]%
Was nehme ich mit: [...]
```

---

## 6. Verhaltensaktivierung

**Zusatz zu kognitiver Arbeit:** Verhalten veraendern unterstuetzt Gedanken-Veraenderung.

**Prinzip:** Positive Aktivitaeten -> Bessere Stimmung -> Hilfreichere Gedanken

**Schritte:**
1. Liste angenehmer/bedeutungsvoller Aktivitaeten erstellen
2. Aktivitaeten planen (konkret: wann, wie, wo)
3. Umsetzung tracken
4. Stimmung vor/nach bewerten

**Beispiel-Aktivitaeten:**
- Spaziergang (Natur, frische Luft)
- Kontakt zu wichtigen Menschen
- Kreative Taetigkeiten
- Koerperliche Bewegung
- Dinge, die frueher Freude gemacht haben

---

## Anwendung im BACH-Kontext

```bash
# Gedankenprotokoll starten
bach psycho session start
# Psycho-Berater fuehrt durch Protokoll-Schritte

# Protokoll speichern
bach psycho observation add <session_id> --typ gedankenprotokoll --inhalt "..."
```

**Integration mit Dokumentation:**
- Protokolle als psycho_sessions gespeichert
- Muster aus mehreren Protokollen -> psycho_observations (Hypothesen)

---

*Erstellt: 2026-02-22 | SQ046 Phase 1 | BACH Therapie-Skills*
*Quelle: Kognitive Verhaltenstherapie (Beck, Ellis) — Keine professionelle Therapie*
