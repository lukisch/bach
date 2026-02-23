================================================================================
                    PYTHON OBJEKTORIENTIERTE PROGRAMMIERUNG (OOP)
================================================================================

Portabilitaet: UNIVERSAL
Zuletzt validiert: 2026-02-05
Naechste Pruefung: 2027-02-05
Quellen: Python 3.12 Dokumentation, PEP 557 (Data Classes), PEP 3119 (ABC)

Stand: 2026-02-05

================================================================================
                              EINFUEHRUNG
================================================================================

Objektorientierte Programmierung (OOP) ist ein Programmierparadigma, das auf
dem Konzept von "Objekten" basiert. Objekte enthalten Daten (Attribute) und
Code (Methoden). Python unterstuetzt OOP vollstaendig und kombiniert es mit
anderen Paradigmen wie funktionaler Programmierung.

GRUNDPRINZIPIEN DER OOP
-----------------------
  1. Kapselung     - Daten und Methoden in Objekten buendeln
  2. Abstraktion   - Komplexitaet verbergen, Schnittstellen anbieten
  3. Vererbung     - Eigenschaften von Elternklassen uebernehmen
  4. Polymorphismus - Gleichnamige Methoden verhalten sich unterschiedlich

================================================================================
                          KLASSEN UND OBJEKTE
================================================================================

KLASSENDEFINITION
-----------------
  Eine Klasse ist ein Bauplan fuer Objekte.

  class Person:
      '''Repraesentiert eine Person.

      Attributes:
          vorname: Der Vorname der Person
          nachname: Der Nachname der Person
          alter: Das Alter in Jahren
      '''

      def __init__(self, vorname, nachname, alter):
          '''Initialisiert eine neue Person.

          Args:
              vorname: Der Vorname
              nachname: Der Nachname
              alter: Das Alter (muss >= 0 sein)
          '''
          self.vorname = vorname
          self.nachname = nachname
          self.alter = alter

      def vollstaendiger_name(self):
          '''Gibt den vollstaendigen Namen zurueck.'''
          return f"{self.vorname} {self.nachname}"

      def vorstellen(self):
          '''Gibt eine Vorstellung zurueck.'''
          return f"Hallo, ich bin {self.vollstaendiger_name()}, {self.alter} Jahre alt."

OBJEKTERSTELLUNG (Instanziierung)
---------------------------------
  # Objekt erstellen
  person1 = Person("Max", "Mustermann", 30)
  person2 = Person("Anna", "Schmidt", 25)

  # Methoden aufrufen
  print(person1.vorstellen())
  # Ausgabe: Hallo, ich bin Max Mustermann, 30 Jahre alt.

  # Attribute zugreifen
  print(person2.vorname)    # Anna
  print(person2.alter)      # 25

  # Attribute aendern
  person1.alter = 31

================================================================================
                              ATTRIBUTE
================================================================================

INSTANZ-ATTRIBUTE
-----------------
  Gehoeren zu einem spezifischen Objekt.

  class Hund:
      def __init__(self, name, rasse):
          self.name = name      # Instanz-Attribut
          self.rasse = rasse    # Instanz-Attribut

  hund1 = Hund("Bello", "Labrador")
  hund2 = Hund("Rex", "Schaeferhund")

  print(hund1.name)  # Bello
  print(hund2.name)  # Rex

KLASSEN-ATTRIBUTE
-----------------
  Werden von allen Instanzen geteilt.

  class Hund:
      art = "Canis familiaris"  # Klassen-Attribut
      anzahl_hunde = 0          # Zaehler fuer alle Instanzen

      def __init__(self, name):
          self.name = name
          Hund.anzahl_hunde += 1  # Klassen-Attribut erhoehen

  hund1 = Hund("Bello")
  hund2 = Hund("Rex")

  print(Hund.art)            # Canis familiaris
  print(Hund.anzahl_hunde)   # 2
  print(hund1.art)           # Canis familiaris (ueber Instanz zugreifbar)

PRIVATE UND PROTECTED ATTRIBUTE
-------------------------------
  Python hat keine echte Zugriffskontrolle, aber Konventionen:

  class Konto:
      def __init__(self, kontonummer, kontostand):
          self.kontonummer = kontonummer    # Oeffentlich
          self._kontostand = kontostand     # Protected (Konvention)
          self.__pin = "1234"               # Private (Name Mangling)

      def zeige_kontostand(self):
          return self._kontostand

      def _interne_methode(self):
          '''Protected Methode - nur intern verwenden.'''
          pass

  konto = Konto("DE123456", 1000)
  print(konto.kontonummer)       # DE123456
  print(konto._kontostand)       # 1000 (funktioniert, aber Konvention!)
  # print(konto.__pin)           # AttributeError!
  print(konto._Konto__pin)       # 1234 (Name Mangling umgehen)

================================================================================
                              METHODEN
================================================================================

INSTANZ-METHODEN
----------------
  Erhalten self als ersten Parameter.

  class Rechteck:
      def __init__(self, breite, hoehe):
          self.breite = breite
          self.hoehe = hoehe

      def flaeche(self):
          '''Instanz-Methode: Berechnet die Flaeche.'''
          return self.breite * self.hoehe

      def umfang(self):
          '''Instanz-Methode: Berechnet den Umfang.'''
          return 2 * (self.breite + self.hoehe)

KLASSEN-METHODEN
----------------
  Erhalten cls als ersten Parameter, arbeiten mit der Klasse.

  class Datum:
      def __init__(self, jahr, monat, tag):
          self.jahr = jahr
          self.monat = monat
          self.tag = tag

      @classmethod
      def von_string(cls, datum_string):
          '''Erstellt Datum aus String "YYYY-MM-DD".'''
          jahr, monat, tag = map(int, datum_string.split('-'))
          return cls(jahr, monat, tag)

      @classmethod
      def heute(cls):
          '''Erstellt Datum mit heutigem Datum.'''
          from datetime import date
          heute = date.today()
          return cls(heute.year, heute.month, heute.day)

  # Verwendung
  datum1 = Datum(2026, 2, 5)
  datum2 = Datum.von_string("2026-12-24")
  datum3 = Datum.heute()

STATISCHE METHODEN
------------------
  Gehoeren zur Klasse, aber brauchen weder self noch cls.

  class Mathematik:
      @staticmethod
      def addiere(a, b):
          '''Statische Methode: Addiert zwei Zahlen.'''
          return a + b

      @staticmethod
      def ist_gerade(zahl):
          '''Prueft ob eine Zahl gerade ist.'''
          return zahl % 2 == 0

  # Aufruf ohne Instanz
  print(Mathematik.addiere(5, 3))      # 8
  print(Mathematik.ist_gerade(4))      # True

================================================================================
                          PROPERTIES
================================================================================

  Properties ermoeglichen kontrollierten Zugriff auf Attribute.

  class Temperatur:
      def __init__(self, celsius=0):
          self._celsius = celsius

      @property
      def celsius(self):
          '''Getter fuer Celsius.'''
          return self._celsius

      @celsius.setter
      def celsius(self, wert):
          '''Setter fuer Celsius mit Validierung.'''
          if wert < -273.15:
              raise ValueError("Temperatur unter absolutem Nullpunkt!")
          self._celsius = wert

      @property
      def fahrenheit(self):
          '''Berechnete Property (nur Getter).'''
          return self._celsius * 9/5 + 32

      @fahrenheit.setter
      def fahrenheit(self, wert):
          '''Setter fuer Fahrenheit.'''
          self.celsius = (wert - 32) * 5/9

  # Verwendung
  temp = Temperatur(25)
  print(temp.celsius)      # 25
  print(temp.fahrenheit)   # 77.0

  temp.fahrenheit = 100
  print(temp.celsius)      # 37.77...

================================================================================
                              VERERBUNG
================================================================================

EINFACHE VERERBUNG
------------------
  class Tier:
      def __init__(self, name):
          self.name = name

      def sprechen(self):
          raise NotImplementedError("Unterklasse muss implementieren")

  class Hund(Tier):
      def __init__(self, name, rasse):
          super().__init__(name)  # Elternkonstruktor aufrufen
          self.rasse = rasse

      def sprechen(self):
          return f"{self.name} sagt: Wuff!"

  class Katze(Tier):
      def sprechen(self):
          return f"{self.name} sagt: Miau!"

  # Verwendung
  hund = Hund("Bello", "Labrador")
  katze = Katze("Minka")

  print(hund.sprechen())   # Bello sagt: Wuff!
  print(katze.sprechen())  # Minka sagt: Miau!

MEHRFACHVERERBUNG
-----------------
  class Fliegend:
      def fliegen(self):
          return f"{self.name} fliegt."

  class Schwimmend:
      def schwimmen(self):
          return f"{self.name} schwimmt."

  class Ente(Tier, Fliegend, Schwimmend):
      def sprechen(self):
          return f"{self.name} sagt: Quak!"

  ente = Ente("Donald")
  print(ente.sprechen())   # Donald sagt: Quak!
  print(ente.fliegen())    # Donald fliegt.
  print(ente.schwimmen())  # Donald schwimmt.

METHOD RESOLUTION ORDER (MRO)
-----------------------------
  Bei Mehrfachvererbung bestimmt die MRO, welche Methode aufgerufen wird.

  print(Ente.__mro__)
  # (<class 'Ente'>, <class 'Tier'>, <class 'Fliegend'>,
  #  <class 'Schwimmend'>, <class 'object'>)

================================================================================
                       SPEZIELLE METHODEN (DUNDER)
================================================================================

  Spezielle Methoden beginnen und enden mit doppeltem Unterstrich.

KONSTRUKTION UND INITIALISIERUNG
--------------------------------
  __new__(cls)       - Erstellt neue Instanz (selten ueberschrieben)
  __init__(self)     - Initialisiert die Instanz
  __del__(self)      - Destruktor (bei Garbage Collection)

STRING-DARSTELLUNG
------------------
  class Punkt:
      def __init__(self, x, y):
          self.x = x
          self.y = y

      def __str__(self):
          '''Benutzerfreundliche Darstellung (str(), print())'''
          return f"Punkt({self.x}, {self.y})"

      def __repr__(self):
          '''Entwickler-Darstellung (repr(), Debugger)'''
          return f"Punkt(x={self.x}, y={self.y})"

  p = Punkt(3, 4)
  print(str(p))    # Punkt(3, 4)
  print(repr(p))   # Punkt(x=3, y=4)

VERGLEICHSOPERATOREN
--------------------
  class Punkt:
      def __init__(self, x, y):
          self.x = x
          self.y = y

      def __eq__(self, other):
          '''Gleichheit (==)'''
          if not isinstance(other, Punkt):
              return NotImplemented
          return self.x == other.x and self.y == other.y

      def __lt__(self, other):
          '''Kleiner als (<) - basierend auf Distanz zum Ursprung'''
          return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)

      def __hash__(self):
          '''Fuer Verwendung in Sets und als Dict-Keys'''
          return hash((self.x, self.y))

ARITHMETISCHE OPERATOREN
------------------------
  class Vektor:
      def __init__(self, x, y):
          self.x = x
          self.y = y

      def __add__(self, other):
          '''Addition (+)'''
          return Vektor(self.x + other.x, self.y + other.y)

      def __sub__(self, other):
          '''Subtraktion (-)'''
          return Vektor(self.x - other.x, self.y - other.y)

      def __mul__(self, skalar):
          '''Multiplikation mit Skalar (*)'''
          return Vektor(self.x * skalar, self.y * skalar)

      def __rmul__(self, skalar):
          '''Rechtsseitige Multiplikation (3 * vektor)'''
          return self.__mul__(skalar)

CONTAINER-METHODEN
------------------
  class MeineSequenz:
      def __init__(self, daten):
          self._daten = list(daten)

      def __len__(self):
          '''len() Unterstuetzung'''
          return len(self._daten)

      def __getitem__(self, index):
          '''Index-Zugriff (obj[i])'''
          return self._daten[index]

      def __setitem__(self, index, wert):
          '''Index-Zuweisung (obj[i] = x)'''
          self._daten[index] = wert

      def __contains__(self, item):
          '''in-Operator'''
          return item in self._daten

      def __iter__(self):
          '''Iteration (for x in obj)'''
          return iter(self._daten)

CONTEXT MANAGER
---------------
  class Datei:
      def __init__(self, pfad, modus):
          self.pfad = pfad
          self.modus = modus
          self.datei = None

      def __enter__(self):
          '''Wird bei with-Statement aufgerufen'''
          self.datei = open(self.pfad, self.modus)
          return self.datei

      def __exit__(self, exc_type, exc_val, exc_tb):
          '''Wird beim Verlassen des with-Blocks aufgerufen'''
          if self.datei:
              self.datei.close()
          return False  # Exceptions nicht unterdruecken

  # Verwendung
  with Datei("test.txt", "w") as f:
      f.write("Hallo Welt")

================================================================================
                       ABSTRAKTE BASISKLASSEN (ABC)
================================================================================

  from abc import ABC, abstractmethod

  class Form(ABC):
      '''Abstrakte Basisklasse fuer geometrische Formen.'''

      @abstractmethod
      def flaeche(self):
          '''Muss von Unterklassen implementiert werden.'''
          pass

      @abstractmethod
      def umfang(self):
          '''Muss von Unterklassen implementiert werden.'''
          pass

      def beschreibung(self):
          '''Konkrete Methode - kann vererbt werden.'''
          return f"Form mit Flaeche {self.flaeche()}"

  class Kreis(Form):
      def __init__(self, radius):
          self.radius = radius

      def flaeche(self):
          import math
          return math.pi * self.radius ** 2

      def umfang(self):
          import math
          return 2 * math.pi * self.radius

  # form = Form()  # TypeError: Can't instantiate abstract class
  kreis = Kreis(5)
  print(kreis.flaeche())       # 78.54...
  print(kreis.beschreibung())  # Form mit Flaeche 78.54...

================================================================================
                            DATACLASSES
================================================================================

  Dataclasses reduzieren Boilerplate-Code fuer Datenklassen (Python 3.7+).

  from dataclasses import dataclass, field
  from typing import List

  @dataclass
  class Produkt:
      name: str
      preis: float
      lagerbestand: int = 0

  @dataclass
  class Warenkorb:
      kunde: str
      produkte: List[Produkt] = field(default_factory=list)

      def gesamtpreis(self):
          return sum(p.preis for p in self.produkte)

  # Automatisch generiert: __init__, __repr__, __eq__
  produkt1 = Produkt("Laptop", 999.99, 10)
  produkt2 = Produkt("Maus", 29.99)

  print(produkt1)  # Produkt(name='Laptop', preis=999.99, lagerbestand=10)

ERWEITERTE DATACLASS-OPTIONEN
-----------------------------
  @dataclass(frozen=True)  # Immutable
  class Koordinate:
      x: float
      y: float

  @dataclass(order=True)  # Vergleichsoperatoren generieren
  class Prioritaet:
      wert: int
      name: str = field(compare=False)  # Nicht fuer Vergleich verwenden

================================================================================
                         BACH-INTEGRATION
================================================================================

BACH-PLUGIN-KLASSE
------------------
  '''Beispiel fuer eine BACH-Plugin-Basisklasse.'''

  from abc import ABC, abstractmethod
  from dataclasses import dataclass
  from typing import Dict, Any, Optional

  @dataclass
  class PluginConfig:
      name: str
      version: str
      aktiv: bool = True
      optionen: Dict[str, Any] = field(default_factory=dict)

  class BachPlugin(ABC):
      '''Abstrakte Basisklasse fuer BACH-Plugins.'''

      def __init__(self, config: PluginConfig):
          self.config = config
          self._initialisiert = False

      @abstractmethod
      def initialisiere(self) -> bool:
          '''Plugin initialisieren.'''
          pass

      @abstractmethod
      def ausfuehren(self, eingabe: Any) -> Any:
          '''Hauptfunktion des Plugins.'''
          pass

      def beende(self) -> None:
          '''Aufraeumarbeiten beim Beenden.'''
          self._initialisiert = False

  class TextVerarbeitungsPlugin(BachPlugin):
      '''Konkretes Plugin fuer Textverarbeitung.'''

      def initialisiere(self) -> bool:
          # Initialisierungslogik
          self._initialisiert = True
          return True

      def ausfuehren(self, eingabe: str) -> str:
          if not self._initialisiert:
              raise RuntimeError("Plugin nicht initialisiert")
          return eingabe.upper()

================================================================================
                           BEST PRACTICES
================================================================================

  1. Composition over Inheritance: Oft ist Komposition flexibler
  2. Single Responsibility: Eine Klasse = eine Verantwortung
  3. Liskov Substitution: Unterklassen muessen Elternklassen ersetzen koennen
  4. Interface Segregation: Kleine, spezifische Interfaces bevorzugen
  5. Dependency Inversion: Von Abstraktionen abhaengen, nicht Implementierungen
  6. Docstrings: Klassen und Methoden dokumentieren
  7. Type Hints: Verbessern Lesbarkeit und IDE-Unterstuetzung
  8. Properties: Fuer kontrollierten Attributzugriff
  9. __slots__: Fuer speichereffiziente Klassen mit festen Attributen
  10. Dataclasses: Fuer einfache Datencontainer verwenden

================================================================================
                              SIEHE AUCH
================================================================================

  wiki/python/funktionen/           - Funktionen und Methoden
  wiki/python/decorators/           - Decorators fuer Methoden
  wiki/python/exceptions/           - Eigene Exceptions definieren
  wiki/informatik/programmierung/   - Allgemeine Programmierkonzepte
  wiki/java/oop/                    - OOP in Java (Vergleich)
  wiki/design_patterns/             - Design Patterns in OOP

================================================================================
                           VERSIONSVERLAUF
================================================================================

  2026-02-05  Vollstaendiger Artikel erstellt
  2026-01-24  Initialer Stub angelegt

================================================================================
