# Erfassungsschemas Gesundheitsassistent

## Schema: Patientenbezogenes Dokument

```yaml
dokument:
  dateiname: ""
  typ: "Arztbericht|Laborbefund|Bildgebung|Testbericht|Sonstiges"
  datum: "YYYY-MM-DD"
  
institution:
  name: ""
  adresse: ""
  telefon: ""
  email: ""
  arzt: ""

befunde:
  diagnosen: []
  verdachtsdiagnosen: []
  symptome: []
  laborwerte_auffaellig: []
  
empfehlungen:
  diagnostik: []
  behandlung: []
  medikation: []
```

## Schema: Wissensbezogenes Dokument

```yaml
dokument:
  dateiname: ""
  titel: ""
  typ: "Studie|Review|Leitlinie|Artikel"
  
quelle:
  autoren: []
  journal: ""
  jahr: ""
  doi: ""
  
inhalt:
  kernaussagen: []
  relevanz_fuer_fall: ""
  
validitaet:
  evidenzlevel: "I|II|III|IV|V"
  repliziert: true|false
```

## Schema: Diagnose-Eintrag

```yaml
diagnose:
  bezeichnung: ""
  icd10: ""
  status: "gesichert|verdacht|hypothese|widerlegt"
  
belege:
  dafuer: []
  dagegen: []
      
symptomabdeckung:
  erklaert_symptome: []
  
empfohlene_diagnostik:
  - untersuchung: ""
    fachgebiet: ""
    prioritaet: "hoch|mittel|niedrig"
    
bedeutung:
  lebensqualitaet: "hoch|mittel|niedrig"
  bedrohlichkeit: "hoch|mittel|niedrig"
```

## Schema: Medikament

```yaml
medikament:
  name: ""
  wirkstoff: ""
  
einnahme:
  start: "YYYY-MM-DD"
  ende: "YYYY-MM-DD|laufend"
  grund: ""
  
dosierung:
  menge: ""
  einheit: ""
  tageszeit: []
  
effekte:
  wirkung: ""
  nebenwirkungen: []
```

## Schema: Vorsorge

```yaml
vorsorge:
  bezeichnung: ""
  intervall: ""
  letzte: "YYYY-MM-DD"
  naechste: "YYYY-MM-DD"
  status: "aktuell|überfällig|geplant"
```
