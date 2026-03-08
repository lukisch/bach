---
name: exposition-begleitung
version: 1.0.0
type: therapie-skill
category: Verhaltenstherapie (Exposition)
author: BACH Team (SQ046)
created: 2026-03-08
status: aktiv
parent_agent: gesundheitsassistent
expert: psycho-berater
---

# Expositionsbegleitung

> Angst-Hierarchie, SUDs-Skala, graduierte Exposition und Habituation verstehen: BACH plant und begleitet — echte Exposition nur mit Therapeut

---

## Kontext

Exposition (Konfrontationstherapie) ist eine der wirksamsten Methoden der
Verhaltenstherapie bei Angststoerungen, Phobien, Zwangsstoerungen und PTBS.
Sie basiert auf den Prinzipien der Habituation und Extinktion: Wenn man sich
einer angstausloesenden Situation wiederholt aussetzt, nimmt die Angstreaktion
ueber die Zeit ab.

Evidenz: Expositionstherapie ist die Gold-Standard-Behandlung fuer spezifische
Phobien, soziale Angst, Panikstoerung und Agoraphobie (NICE Guidelines, Bandelow
et al. 2014, S3-Leitlinie Angststoerungen). Effektstaerken gehoeren zu den
hoechsten in der Psychotherapieforschung.

**WICHTIG:** BACH unterstuetzt bei der PLANUNG von Expositionsuebungen und
vermittelt das Verstaendnis der Wirkprinzipien. Die DURCHFUEHRUNG von Exposition
muss unter Anleitung eines qualifizierten Therapeuten erfolgen.
Siehe: [ETHICS.md](ETHICS.md)
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Wirkprinzipien verstehen

### Habituation

```
HABITUATION: Gewoehnung durch wiederholte Konfrontation

Angstlevel
100 |  *
    | * *
 80 |*   *
    |     *
 60 |      *
    |       *
 40 |        *
    |         *  *
 20 |          **  * *
    |                  * * * * * *
  0 |________________________________
    Zeit (waehrend der Exposition)

Die Angst steigt zunaechst an, erreicht einen Hoehepunkt
und sinkt dann OHNE Flucht oder Vermeidung von selbst ab.

Entscheidende Erfahrung: "Die Angst geht vorbei, auch wenn
ich in der Situation bleibe."
```

### Extinktion (Neues Lernen)

```
EXTINKTION: Neue Erfahrungen ueberschreiben alte Angst-Assoziationen

Alte Erfahrung: Hund -> Gefahr -> Angst -> Flucht
Neue Erfahrung: Hund -> Keine Gefahr -> Angst sinkt -> Ich bin sicher

Die alte Assoziation wird nicht geloescht, sondern durch neue
Erfahrungen ueberlagert. Deshalb kann die Angst in bestimmten
Kontexten zurueckkehren (Renewal, Reinstatement) — was NORMAL ist.
```

### Warum Vermeidung das Problem aufrechterhaelt

```
DER VERMEIDUNGSTEUFELSKREIS:

Angstausloesende Situation
        |
        v
Angst steigt (unangenehm)
        |
        v
Vermeidung/Flucht
        |
        v
Kurzfristige Erleichterung (Angst sinkt sofort)
        |
        v
Langfristige Verstaerkung der Angst
("Die Situation IST gefaehrlich, gut dass ich geflohen bin")
        |
        v
Naechstes Mal: Noch mehr Angst, noch mehr Vermeidung
```

---

## 2. Die SUDs-Skala

### Subjective Units of Distress (0-100)

```
SUDS-SKALA (Subjektive Belastungsskala)

  0  Voellig entspannt, keine Angst
 10  Minimale Anspannung, kaum spuerbar
 20  Leichte Unruhe, gut auszuhalten
 30  Deutlich unangenehm, aber kontrollierbar
 40  Merkliche Angst, noch handlungsfaehig
 50  Mittlere Angst, anstrengend aber machbar
 60  Starke Angst, Vermeidungsimpuls deutlich
 70  Sehr starke Angst, schwer auszuhalten
 80  Intensive Angst, am Rand der Belastbarkeit
 90  Extreme Angst, Panikgefuehl
100  Maximale Angst, schlimmste vorstellbare Belastung
```

### Anwendung der SUDs-Skala

**Vor der Exposition:**
- Geschaetzte Angst in der geplanten Situation (Erwartungswert)

**Waehrend der Exposition:**
- Alle 5 Minuten den aktuellen SUDs-Wert einschaetzen
- Dokumentieren, wie der Verlauf ist (steigt, sinkt, schwankt)

**Nach der Exposition:**
- Hoechster SUDs-Wert? Endwert? Wie schnell ging die Angst zurueck?
- War es so schlimm wie erwartet?

---

## 3. Angst-Hierarchie erstellen

### Prinzip

Eine Angst-Hierarchie ordnet angstausloesende Situationen vom niedrigsten
zum hoechsten Angstlevel. Die Exposition beginnt mit leichten Situationen
und steigert sich schrittweise.

### Vorgehen

```
ANGST-HIERARCHIE ERSTELLEN

Schritt 1: Alle angstausloesenden Situationen sammeln
Schritt 2: Jede Situation mit SUDs-Wert (0-100) bewerten
Schritt 3: Von niedrig nach hoch ordnen
Schritt 4: Luecken fuellen (moeglichst 10er-Schritte)
```

### Beispiel: Angst vor Hunden

```
ANGST-HIERARCHIE: Hundephobie

SUDs | Situation
-----|--------------------------------------------------
 10  | Bild von einem Hund anschauen
 15  | Video von spielenden Hunden anschauen
 25  | Ueber eigene Erfahrungen mit Hunden sprechen
 30  | Einen kleinen Hund aus 10 Metern Entfernung beobachten
 40  | Einen kleinen Hund aus 5 Metern Entfernung beobachten
 50  | Neben einem angeleinten kleinen Hund stehen (2 Meter)
 55  | Einen kleinen angeleigten Hund beruehren (Besitzer haelt)
 60  | Einen mittelgrossen Hund aus 5 Metern beobachten
 65  | Neben einem angeleinten mittelgrossen Hund sitzen
 70  | Einen mittelgrossen Hund streicheln
 75  | An einem freilaufenden Hund vorbeigehen (Park)
 80  | Allein in einem Raum mit einem ruhigen Hund sein
 85  | Einen grossen Hund streicheln
 90  | In einem Park mit mehreren freilaufenden Hunden sein
 95  | Einen Hund fuettern
100  | Einen fremden Hund auf sich zulaufen lassen
```

### Beispiel: Soziale Angst

```
ANGST-HIERARCHIE: Soziale Angst

SUDs | Situation
-----|--------------------------------------------------
 15  | Einen Fremden nach der Uhrzeit fragen
 20  | Im Supermarkt an der Kasse ein kurzes Gespraech fuehren
 30  | In einer kleinen Gruppe eine Frage stellen
 40  | Einen Bekannten anrufen
 45  | Blickkontakt halten waehrend eines Gespraechs
 55  | Allein in ein Cafe gehen und dort essen
 60  | Einer Gruppe von 5 Personen etwas erzaehlen
 70  | Bei einer Feier auf einen Fremden zugehen
 75  | Im Restaurant Essen zurueckschicken
 80  | Vor 10 Personen eine kurze Praesentation halten
 85  | In einer Diskussion eine abweichende Meinung vertreten
 90  | Vor 30 Personen einen Vortrag halten
 95  | Spontan eine Rede halten (Toast, Tischrede)
```

### Vorlage zum Ausfuellen

```
MEINE ANGST-HIERARCHIE

Angstthema: [...]

SUDs | Situation
-----|--------------------------------------------------
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
```

---

## 4. Arten der Exposition

### Graduierte Exposition (In Vivo)

**Prinzip:** Schrittweise Konfrontation mit realen Situationen,
beginnend bei niedrigen SUDs-Werten.

```
ABLAUF GRADUIERTER EXPOSITION:

1. Angst-Hierarchie erstellen (siehe oben)
2. Mit der leichtesten Situation beginnen (SUDs 20-30)
3. In der Situation BLEIBEN, bis die Angst nachlaeßt
   (mindestens 50% Reduktion oder SUDs < 25)
4. Uebung mehrfach wiederholen, bis die Situation
   routinemaessig bewaeltigbar ist
5. Naechste Stufe der Hierarchie angehen
6. Weiter bis zur Spitze
```

### Flooding (Reizueberflutung)

**Prinzip:** Direkte Konfrontation mit stark angstausloesenden Situationen
(hohe SUDs-Werte) fuer laengere Zeit.

```
FLOODING:

- Sehr wirksam, aber belastender als graduierte Exposition
- Nur unter therapeutischer Anleitung
- Voraussetzung: Gute therapeutische Beziehung und Vorbereitung
- Nicht bei unkontrollierbaren Panikattacken oder Dissoziation
- NICHT durch BACH anleiten — nur erklaeren
```

### Exposition in sensu (in der Vorstellung)

**Prinzip:** Angstausloesende Situationen in der Vorstellung durchleben.

```
EXPOSITION IN SENSU:

- Hilfreich als Vorbereitung auf reale Exposition
- Bei Situationen, die nicht leicht reproduzierbar sind
- Bei starker Vermeidung als Einstieg
- BACH kann bei der Planung helfen, aber die Durchfuehrung
  sollte therapeutisch begleitet sein
```

### Interozeptive Exposition

**Prinzip:** Gezieltes Hervorrufen von koerperlichen Angstsymptomen
(z.B. Herzrasen durch Bewegung, Schwindel durch Drehen).

```
INTEROZEPTIVE EXPOSITION (bei Panikattacken):

- Durch Koerperuebungen: Hyperventilation, Strohhalm-Atmen,
  Kopfdrehen, Treppensteigen
- Ziel: Lernen, dass koerperliche Symptome ungefaehrlich sind
- NUR unter therapeutischer Anleitung
```

---

## 5. Begleitete Expositionsplanung

### Vorbereitungsprotokoll

```
EXPOSITIONS-PLANUNGSPROTOKOLL

Datum: [...]
Therapeut informiert: [ ] Ja  [ ] Nein (PFLICHT!)

Angstthema: [...]
Gewaehrte Situation: [...]
Erwarteter SUDs-Wert: [...]
Stufe in der Hierarchie: [...]

Was genau werde ich tun: [...]
Wo: [...]
Wann: [...]
Wie lange: [...]
Allein oder begleitet: [...]

Meine groesste Befuerchtung: [...]
Was realistisch passieren wird: [...]

Notfallplan (falls SUDs > 90 oder Dissoziation):
1. Grounding (5-4-3-2-1)
2. Atemuebung (Box-Breathing)
3. [Vertrauensperson anrufen]: Tel. [...]
4. Situation ordentlich verlassen (kein panisches Fluechten)
```

### Nachbereitungsprotokoll

```
EXPOSITIONS-NACHBEREITUNG

Datum: [...]
Situation: [...]

SUDs vorher (Erwartung): [...]
SUDs hoechster Wert waehrend: [...]
SUDs am Ende: [...]

Wie lange in der Situation geblieben: [...]
Habituation eingetreten: [ ] Ja  [ ] Teilweise  [ ] Nein

Was habe ich gelernt: [...]
War es so schlimm wie befuerchtet: [ ] Schlimmer  [ ] Wie erwartet  [ ] Weniger schlimm

Was moechte ich beim naechsten Mal anders machen: [...]
Naechste Stufe: [...]
```

---

## 6. Sicherheitshinweise und Abbruchkriterien

### Voraussetzungen fuer Exposition

```
CHECKLISTE VOR EXPOSITIONSBEGINN:

[ ] Qualifizierter Therapeut ist einbezogen
[ ] Ausreichende Stabilisierung vorhanden
[ ] Angst-Hierarchie ist erstellt und besprochen
[ ] Notfallplan ist vorbereitet
[ ] Person versteht das Wirkprinzip (Habituation)
[ ] Keine akute Suizidalitaet
[ ] Keine unkontrollierte psychotische Symptomatik
[ ] Keine schwere dissoziative Stoerung (ohne therapeutische Begleitung)
[ ] Keine akute Substanzintoxikation
[ ] Person hat freiwillig zugestimmt (keine Zwangsexposition!)
```

### Abbruchkriterien

```
EXPOSITION ABBRECHEN, WENN:

- Dissoziation auftritt (Person "ist weg", reagiert nicht)
- Panikattacke mit Kontrollverlust
- Person will ausdruecklich abbrechen (Autonomie respektieren!)
- Koerperliche Symptome: Brustschmerz, Atemnot, Ohnmacht
- Suizidgedanken waehrend der Exposition
- Die Situation objektiv unsicher wird

BEI ABBRUCH:
1. Grounding und Stabilisierung (5-4-3-2-1, Atemuebung)
2. Sicherstellen, dass die Person orientiert und stabil ist
3. Erfahrung besprechen (was ist passiert, was wurde gelernt)
4. Keinen Vorwurf machen ("Du haettest bleiben sollen")
5. Naechsten Schritt mit Therapeut planen
```

### Sicherheitsverhaltensweisen erkennen

```
SICHERHEITSVERHALTEN (Safety Behaviors):

Sicherheitsverhalten sind Strategien, die die Angst kurzfristig senken,
aber das Lernen verhindern:

| Sicherheitsverhalten | Problem |
|---------------------|---------|
| Ablenkung waehrend Exposition | Verhindert volle Konfrontation |
| Handy griffbereit halten | "Ich habe es nur geschafft, weil..." |
| Begleitperson dabei | Lernt nicht, es allein zu schaffen |
| Beruhigungstablette vorher | Erfolg wird Tablette zugeschrieben |
| Nur kurz in Situation bleiben | Habituation hat keine Zeit |
| Fluchtweg im Kopf planen | Aufmerksamkeit nicht bei Erfahrung |

Ziel: Sicherheitsverhalten schrittweise reduzieren,
damit die volle Lernerfahrung moeglich wird.
Aber: Nicht zu frueh wegnehmen — in Absprache mit Therapeut.
```

---

## Ethik und Grenzen

**BACH darf:**
- Expositionsprinzipien erklaeren (Psychoedukation)
- Angst-Hierarchie gemeinsam erstellen
- SUDs-Skala erklaeren und nutzen
- Expositionsplanung unterstuetzen (Protokolle ausfuellen)
- Nachbereitung dokumentieren
- Sicherheitshinweise geben
- Motivieren und normalisieren ("Angst bei Exposition ist erwuenscht und normal")

**BACH darf NICHT:**
- Exposition eigenstaendig durchfuehren oder anleiten
- Flooding anleiten (NUR Therapeut)
- Interozeptive Exposition anleiten (NUR Therapeut)
- Prolonged Exposure bei PTBS durchfuehren
- Exposition bei schwerer Dissoziation begleiten
- Zur Exposition draengen ("Du musst dich dem stellen")
- Ergebnisse garantieren
- Diagnosen stellen oder Therapieplan erstellen
- Medikamentenbezogene Empfehlungen geben

**BESONDERS STRENGE GRENZE:** BACH plant und erklaert. Die echte Exposition
findet unter Anleitung eines qualifizierten Therapeuten statt. Bei jeder
Anfrage zur Durchfuehrung: Verweis an Fachperson. Exposition ohne
professionelle Begleitung kann re-traumatisieren oder die Angst verstaerken.

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

## Anwendung im BACH-Kontext

```bash
# Expositionsplanung starten
bach psycho session start
# Psycho-Berater erstellt Angst-Hierarchie und Planungsprotokolle

# Hierarchie und Protokolle dokumentieren
bach psycho observation add <session_id> --typ exposition --inhalt "..."
```

**SIEHE AUCH:**
- Wiki: `psychotherapie/verhaltenstherapie.txt`
- Wiki: `psychotherapie/angststoerungen.txt`
- Wiki: `psychotherapie/exposition.txt`
- Skill: `stabilisierungstechniken.md` (Notfall-Skills bei Abbruch)
- Skill: `kognitive_umstrukturierung.md` (Kognitive Vorbereitung)
- Skill: `dbt_fertigkeiten.md` (Stresstoleranz waehrend Exposition)
- Skill: `verhaltensaktivierung.md` (Vermeidung ueberwinden)

---

*Erstellt: 2026-03-08 | SQ046 Phase 2 | BACH v3.8.0-SUGAR Therapie-Skills*
*Quellen: Foa & Kozak (1986), Craske et al. (2014), Bandelow et al. (2014), S3-Leitlinie Angststoerungen (2014) — Keine professionelle Therapie*
