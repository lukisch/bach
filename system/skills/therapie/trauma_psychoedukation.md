---
name: trauma-psychoedukation
version: 1.0.0
type: therapie-skill
category: Psychoedukation (Trauma)
author: BACH Team (SQ046)
created: 2026-03-08
status: aktiv
parent_agent: gesundheitsassistent
expert: psycho-berater
---

# Trauma-Psychoedukation

> Wissen ueber Trauma, Traumafolgen und das Fenster der Belastbarkeit: Normale Reaktionen auf unnormale Ereignisse verstehen — reine Psychoedukation, KEINE Traumabearbeitung

---

## Kontext

Psychoedukation ueber Trauma hilft Betroffenen, ihre Reaktionen zu verstehen und
einzuordnen. Das Wissen, dass Symptome wie Flashbacks, Ueberregung oder Vermeidung
NORMALE Reaktionen auf UNNORMALE Ereignisse sind, wirkt bereits entlastend und
reduziert Scham und Selbstvorwuerfe.

Evidenz: Psychoedukation ist ein anerkannter Bestandteil der Traumatherapie
(Flatten et al. 2011, S3-Leitlinie PTBS). Als alleinige Intervention reicht sie
nicht aus, kann aber die Therapiemotivation erhoehen und Symptome mildern.

**WICHTIG:** Dieser Skill vermittelt ausschliesslich WISSEN ueber Trauma.
Er fuehrt KEINE Traumabearbeitung durch, exploriert KEINE belastenden Erinnerungen
und fragt NICHT nach Trauma-Details. Siehe: [ETHICS.md](ETHICS.md)
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Was ist ein Trauma?

### Definition

Ein Trauma ist ein Ereignis, das die Bewältigungsfaehigkeiten einer Person uebersteigt
und mit dem Erleben von Hilflosigkeit, Kontrollverlust und/oder Todesangst einhergeht.
Nicht das Ereignis allein definiert das Trauma, sondern das subjektive Erleben.

### Trauma-Typen

| Typ | Beschreibung | Beispiele |
|-----|-------------|----------|
| Typ I (Einzeltrauma) | Einmaliges, unerwartetes Ereignis | Unfall, Ueberfall, Naturkatastrophe |
| Typ II (Komplextrauma) | Wiederholte, langandauernde Traumatisierung | Misshandlung, Vernachlaessigung, Krieg |
| Akzidentelles Trauma | Zufaellige Ereignisse | Verkehrsunfall, Hausbrand, Arbeitsunfall |
| Interpersonelles Trauma | Durch Menschen verursacht | Gewalt, Missbrauch, Folter |
| Sekundaeres Trauma | Durch Miterfahren/Bezeugen | Helfende Berufe, Angehoerige |

### Was KEIN Trauma ist (Abgrenzung)

Nicht jedes belastende Ereignis ist ein Trauma im klinischen Sinne:
- Trennung, Kuendigung, Streit — belastend, aber in der Regel kein Trauma
- Mobbing — kann traumatisierend wirken (besonders bei Kindern), ist aber nicht automatisch Trauma
- Die individuelle Bewertung entscheidet, nicht die Art des Ereignisses

---

## 2. Normale Reaktionen auf unnormale Ereignisse

### Die drei Reaktionsmuster

```
UEBERREGUNG (Hyperarousal)
- Staendige Wachsamkeit und Anspannung
- Schreckhaftigkeit
- Schlafprobleme
- Reizbarkeit, Wutausbrueche
- Konzentrationsschwierigkeiten

WIEDERERLEBEN (Intrusion)
- Flashbacks (Erinnerungen, die sich real anfuehlen)
- Alptraeume
- Belastende Erinnerungen, die ploetzlich auftauchen
- Koerperliche Reaktionen bei Erinnerung (Herzrasen, Schwitzen)

VERMEIDUNG UND BETAEUBUNG (Constriction)
- Vermeidung von Orten, Personen, Situationen
- Emotionale Taubheit
- Rueckzug von anderen Menschen
- Gefuehl der Entfremdung
- Verlust von Interesse und Freude
```

### Wichtige Botschaft fuer Betroffene

```
"Diese Reaktionen sind NORMALE Reaktionen auf UNNORMALE Ereignisse.

Dein Koerper und dein Verstand versuchen, dich zu schuetzen.
Die Wachsamkeit schuetzt dich vor erneuter Gefahr.
Die Erinnerungen versuchen, das Erlebte zu verarbeiten.
Die Vermeidung schuetzt dich vor Ueberwaltigung.

Du bist nicht 'verrueckt'. Du bist nicht 'schwach'.
Dein Nervensystem reagiert so, wie es darauf programmiert ist,
auf extreme Bedrohung zu reagieren."
```

### Zeitlicher Verlauf

```
VERLAUF NACH TRAUMATISCHEM EREIGNIS

0-4 Wochen:  Akute Belastungsreaktion (NORMAL)
             - Schock, Betaeubung, Unruhe
             - Schlafprobleme, Schreckhaftigkeit
             - Flashbacks, Alptraeume
             - Bei den meisten Menschen: Spontane Erholung

4+ Wochen:   Wenn Symptome nicht nachlassen: Moegliche PTBS
             - Professionelle Diagnostik empfohlen
             - Fruehe Intervention verbessert Prognose

Monate-Jahre: Chronifizierung moeglich
             - Therapie ist auch nach langer Zeit wirksam
             - "Es ist nie zu spaet, sich Hilfe zu holen"
```

---

## 3. Das Fenster der Belastbarkeit (Window of Tolerance)

### Das Modell (nach Dan Siegel)

```
            ________________________________________________
           |                                                |
           |   UEBER DEM FENSTER: Hyperarousal              |
           |   Panik, Wut, Ueberregung, Flashbacks          |
           |   Herzrasen, Schwitzen, Zittern                 |
           |   "Kampf oder Flucht"                           |
           |________________________________________________|
           |                                                |
           |   FENSTER DER BELASTBARKEIT                     |
           |   (Window of Tolerance)                         |
           |                                                |
           |   Hier koennen wir:                             |
           |   - Denken und fuehlen gleichzeitig             |
           |   - Informationen verarbeiten                   |
           |   - Beziehungen gestalten                       |
           |   - Probleme loesen                             |
           |   - Lernen und wachsen                          |
           |________________________________________________|
           |                                                |
           |   UNTER DEM FENSTER: Hypoarousal                |
           |   Erstarrung, Taubheit, Dissoziation            |
           |   Energielosigkeit, Leere, Abschaltung          |
           |   "Totstell-Reflex"                             |
           |________________________________________________|
```

### Was bedeutet das?

- **Im Fenster:** Wir koennen Stress regulieren und funktionieren
- **Ueber dem Fenster:** Zu viel Erregung — Koerper im Alarmmodus
- **Unter dem Fenster:** Zu wenig Erregung — Koerper schaltet ab

### Trauma und das Fenster

```
VOR dem Trauma:           NACH dem Trauma (unbehandelt):

|_______________|         |_____|
|               |         |     |  <- Fenster ist ENGER geworden
|    FENSTER    |         | F.  |
|   (breit)     |         |     |
|_______________|         |_____|

Schon kleine Reize koennen nach einem Trauma dazu fuehren,
dass man aus dem Fenster faellt (Trigger).

ZIEL der Therapie: Das Fenster wieder WEITEN.
```

### Trigger verstehen

```
TRIGGER sind Reize, die an das Trauma erinnern und das Nervensystem
in den Alarmmodus versetzen — oft unbewusst.

Trigger koennen sein:
- Geraeusche (Knall, Schreien, bestimmte Musik)
- Gerueche (Rauch, Parfuem, Alkohol)
- Bilder (Nachrichten, Filme, Orte)
- Koerperempfindungen (Enge, Beruehrung, Schmerz)
- Kalenderdaten (Jahrestage)
- Beziehungssituationen (Streit, Kontrollverlust)

Trigger sind KEINE Schwaeche. Sie sind gespeicherte Warnsignale
des Nervensystems. In der Therapie lernt man, Trigger zu erkennen
und das Nervensystem zu regulieren.
```

---

## 4. Selbstfuersorge-Strategien

### Grundbeduerfnisse sicherstellen

```
CHECKLISTE GRUNDBEDUERFNISSE

[ ] Schlaf: Regelmaessige Schlafenszeiten, mindestens 7 Stunden
[ ] Ernaehrung: Regelmaessige Mahlzeiten, ausreichend Wasser
[ ] Bewegung: Taeglich mindestens 20 Minuten (Spaziergang reicht)
[ ] Soziale Kontakte: Mindestens eine vertrauensvolle Person
[ ] Sicherheit: Sich im eigenen Umfeld sicher fuehlen
[ ] Struktur: Tagesablauf mit festen Ankerpunkten
```

### Selbstfuersorge-Strategien im Alltag

**Koerperlich:**
- Regelmaessige Bewegung (senkt Stresshormone)
- Atemuebungen (siehe: stabilisierungstechniken.md)
- Genuegend Schlaf (Schlafhygiene beachten)
- Koffein und Alkohol reduzieren (verstaerken Ueberregung/Betaeubung)

**Sozial:**
- Vertrauensperson haben (muss nicht ueber Trauma sprechen)
- Isolation vermeiden — auch kleine Kontakte helfen
- Grenzen setzen lernen ("Nein" sagen duerfen)
- Unterstuetzung annehmen

**Emotional:**
- Gefuehle benennen (nicht bewerten)
- Stabilisierungstechniken nutzen (5-4-3-2-1, Sicherer Ort)
- Tagebuch fuehren (optional, nicht erzwingen)
- Kreative Ausdruecke finden (Malen, Musik, Schreiben)

**Kognitiv:**
- Sich informieren (Psychoedukation — dieser Skill)
- Selbstvorwuerfe hinterfragen ("Es war nicht meine Schuld")
- Realitaetscheck bei Katastrophisieren
- Geduldmit sich selbst haben (Heilung braucht Zeit)

---

## 5. Professionelle Hilfe finden

### Wann professionelle Hilfe suchen?

```
PROFESSIONELLE HILFE IST ANGEZEIGT, WENN:

- Symptome laenger als 4 Wochen anhalten
- Symptome sich verschlimmern statt bessern
- Der Alltag nicht mehr bewaeltigbar ist (Arbeit, Beziehungen)
- Flashbacks oder Alptraeume sehr haeufig auftreten
- Vermeidungsverhalten das Leben stark einschraenkt
- Substanzmissbrauch als Bewaeltigungsstrategie
- Suizidgedanken oder Selbstverletzung
- Das Gefuehl: "Ich schaffe das nicht alleine"
```

### Anlaufstellen (Deutschland)

```
SOFORTHILFE:
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222 (24/7, kostenlos)
- Krisenchat: krisenchat.de (per Chat, fuer junge Menschen)
- Psychiatrischer Notdienst: 112

TRAUMASPEZIFISCH:
- Traumaambulanzen (an vielen Kliniken, keine Ueberweisung noetig)
- Opferhilfe: Weisser Ring (116 006)
- Gewaltschutzambulanz (bei koerperlicher Gewalt)
- Frauenhaus-Hotline: 08000 116 016
- Hilfetelefon sexueller Missbrauch: 0800 22 55 530

THERAPIEPLATZ:
- Terminservicestelle der Kassenärztlichen Vereinigung: 116 117
- Psychotherapie-Informationsdienst (PID): www.psychotherapiesuche.de
- Wichtig: Auf "Traumatherapie" spezialisierte Therapeuten suchen
```

---

## 6. Haeufige Fragen (FAQ)

### "Bin ich jetzt traumatisiert?"

Nicht jeder, der ein belastendes Ereignis erlebt, entwickelt eine Traumafolgestoerung.
Die Mehrheit der Menschen erholt sich spontan innerhalb von Wochen. Ob eine PTBS
vorliegt, kann nur eine Fachperson diagnostizieren.

### "Muss ich darueber reden?"

Nein. Sich zum Reden zu zwingen kann schaedlich sein. Manche Menschen profitieren
vom Darueber-Sprechen, andere nicht. Es gibt kein "muss". In der Therapie wird
der richtige Zeitpunkt gemeinsam bestimmt.

### "Warum reagiere ich so, obwohl es lange her ist?"

Traumatische Erinnerungen werden anders gespeichert als normale Erinnerungen.
Sie koennen durch Trigger reaktiviert werden und fuehlen sich an, als wuerde
das Ereignis JETZT passieren. Das Gehirn unterscheidet nicht zwischen "damals" und "jetzt".
Therapie hilft, diese Erinnerungen "umzusortieren".

### "Bin ich schwach, weil ich das nicht alleine schaffe?"

Nein. Hilfe zu suchen ist ein Zeichen von Staerke. Traumatherapie ist wirksam —
die meisten Menschen koennen mit professioneller Hilfe deutlich besser werden.

---

## Ethik und Grenzen

**BACH darf:**
- Wissen ueber Trauma und Traumafolgen vermitteln (Psychoedukation)
- Normale Reaktionen normalisieren und entlasten
- Das Fenster der Belastbarkeit erklaeren
- Selbstfuersorge-Strategien vorschlagen
- An professionelle Hilfe verweisen
- Stabilisierungstechniken anbieten (siehe: stabilisierungstechniken.md)

**BACH darf NICHT:**
- Traumabearbeitung durchfuehren (EMDR, Exposition, NET, IRRT)
- Nach Trauma-Details fragen oder diese explorieren
- Flashbacks inhaltlich bearbeiten (nur stabilisieren)
- PTBS oder andere Traumafolgestoerungen diagnostizieren
- Suizidalitaet einschaetzen
- Medikamentenbezogene Empfehlungen geben
- Aussagen ueber Schuld oder Verantwortung machen
- Erinnerungen "aufarbeiten" oder "durcharbeiten"
- Suggestive Fragen stellen ("Koennte es sein, dass...")

**BESONDERS STRENGE GRENZE:** Traumabearbeitung gehoert in die Haende
ausgebildeter Traumatherapeuten. BACH bietet ausschliesslich Psychoedukation
und Stabilisierung. Bei jeder Form von Traumaexploration: STOPP und Verweis
an Fachperson.

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

## Anwendung im BACH-Kontext

```bash
# Psychoedukationssitzung starten
bach psycho session start
# Psycho-Berater vermittelt Traumawissen

# Erkenntnisse dokumentieren
bach psycho observation add <session_id> --typ psychoedukation --inhalt "..."
```

**SIEHE AUCH:**
- Wiki: `psychotherapie/traumatherapie.txt`
- Wiki: `psychotherapie/ptbs.txt`
- Wiki: `psychologie/stress.txt`
- Skill: `stabilisierungstechniken.md` (Grounding, Sicherer Ort, Containment)
- Skill: `dbt_fertigkeiten.md` (Stresstoleranz-Skills)
- Skill: `achtsamkeit_basis.md` (Achtsamkeit als Regulationshilfe)
- Skill: `psychoedukation.md` (Allgemeine Psychoedukation)

---

*Erstellt: 2026-03-08 | SQ046 Phase 2 | BACH v3.8.0-SUGAR Therapie-Skills*
*Quellen: Flatten et al. (2011), Siegel (2012), Reddemann (2001), S3-Leitlinie PTBS (2019) — Keine professionelle Therapie*
