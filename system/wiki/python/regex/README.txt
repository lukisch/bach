# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: docs.python.org/3/library/re.html, regex101.com, regular-expressions.info

REGULAERE AUSDRUECKE IN PYTHON
==============================

Stand: 2026-02-05

UEBERBLICK
==========
  Regulaere Ausdruecke (Regex) sind maechtige Muster zur Textsuche,
  -validierung und -manipulation. Python bietet das re-Modul als
  Standardbibliothek fuer Regex-Operationen.

  Einsatzgebiete:
    - Textsuche und -extraktion
    - Eingabevalidierung (E-Mail, Telefon, etc.)
    - String-Manipulation und -Ersetzung
    - Log-Analyse und Parsing
    - Datenbereinigung

DAS RE-MODUL
============

IMPORT UND GRUNDLAGEN
---------------------
  import re

  # Einfache Suche
  text = "Python ist eine tolle Sprache"
  result = re.search(r"tolle", text)
  if result:
      print(f"Gefunden: {result.group()}")  # Gefunden: tolle

HAUPTFUNKTIONEN
---------------

  re.search(pattern, string)
    - Sucht erstes Vorkommen im String
    - Gibt Match-Objekt oder None zurueck

    text = "Die Antwort ist 42"
    match = re.search(r"\d+", text)
    if match:
        print(match.group())  # 42

  re.match(pattern, string)
    - Sucht NUR am Anfang des Strings
    - Gibt Match-Objekt oder None zurueck

    text = "Python ist super"
    match = re.match(r"Python", text)
    print(bool(match))  # True

    match = re.match(r"super", text)
    print(bool(match))  # False (nicht am Anfang)

  re.findall(pattern, string)
    - Findet ALLE Vorkommen
    - Gibt Liste mit Strings zurueck

    text = "1 Apfel, 2 Birnen, 3 Orangen"
    zahlen = re.findall(r"\d+", text)
    print(zahlen)  # ['1', '2', '3']

  re.finditer(pattern, string)
    - Wie findall, aber gibt Iterator mit Match-Objekten
    - Speichereffizient fuer grosse Texte

    text = "a1 b2 c3"
    for match in re.finditer(r"[a-z]\d", text):
        print(f"{match.group()} bei Position {match.start()}")

  re.sub(pattern, replacement, string)
    - Ersetzt Muster durch neuen Text
    - Gibt modifizierten String zurueck

    text = "Hello World"
    result = re.sub(r"World", "Python", text)
    print(result)  # Hello Python

  re.split(pattern, string)
    - Teilt String an Muster-Stellen

    text = "Eins,Zwei;Drei.Vier"
    teile = re.split(r"[,;.]", text)
    print(teile)  # ['Eins', 'Zwei', 'Drei', 'Vier']

REGEX-SYNTAX
============

ZEICHENKLASSEN
--------------
  .       Beliebiges Zeichen (ausser Newline)
  \d      Ziffer [0-9]
  \D      Keine Ziffer [^0-9]
  \w      Wortzeichen [a-zA-Z0-9_]
  \W      Kein Wortzeichen
  \s      Whitespace (Leerzeichen, Tab, Newline)
  \S      Kein Whitespace

  Beispiel:
    text = "User123 hat 5 Punkte"
    print(re.findall(r"\d+", text))  # ['123', '5']
    print(re.findall(r"\w+", text))  # ['User123', 'hat', '5', 'Punkte']

ZEICHENBEREICHE
---------------
  [abc]     a, b oder c
  [a-z]     Kleinbuchstaben a-z
  [A-Z]     Grossbuchstaben A-Z
  [0-9]     Ziffern 0-9
  [a-zA-Z]  Alle Buchstaben
  [^abc]    NICHT a, b oder c (Negation)

  Beispiel:
    text = "Test123ABC"
    print(re.findall(r"[A-Z]+", text))  # ['T', 'ABC']
    print(re.findall(r"[^0-9]+", text)) # ['Test', 'ABC']

QUANTIFIZIERER
--------------
  *       0 oder mehr (gierig)
  +       1 oder mehr (gierig)
  ?       0 oder 1 (optional)
  {n}     Genau n mal
  {n,}    n oder mehr mal
  {n,m}   n bis m mal

  Beispiel:
    text = "aaa ab a aaaa"
    print(re.findall(r"a+", text))    # ['aaa', 'a', 'a', 'aaaa']
    print(re.findall(r"a{2,3}", text)) # ['aaa', 'aaa']

  Nicht-gierige Varianten (minimal):
    *?      0 oder mehr (nicht gierig)
    +?      1 oder mehr (nicht gierig)
    ??      0 oder 1 (nicht gierig)

    text = "<tag>Inhalt</tag>"
    print(re.findall(r"<.*>", text))   # ['<tag>Inhalt</tag>'] gierig
    print(re.findall(r"<.*?>", text))  # ['<tag>', '</tag>'] nicht gierig

ANKER
-----
  ^       Anfang des Strings (oder Zeile mit re.MULTILINE)
  $       Ende des Strings (oder Zeile mit re.MULTILINE)
  \b      Wortgrenze
  \B      Keine Wortgrenze

  Beispiel:
    text = "Python ist pythonisch"
    print(re.findall(r"^Python", text))     # ['Python']
    print(re.findall(r"\bpython\b", text, re.I))  # ['Python', 'python']

GRUPPEN
-------

EINFACHE GRUPPEN
  ()      Gruppierung und Erfassung

  text = "Max Mustermann"
  match = re.search(r"(\w+) (\w+)", text)
  if match:
      print(match.group(0))  # Max Mustermann (gesamter Match)
      print(match.group(1))  # Max
      print(match.group(2))  # Mustermann
      print(match.groups())  # ('Max', 'Mustermann')

BENANNTE GRUPPEN
  (?P<name>...)   Benannte Gruppe

  text = "Geboren: 15.03.1990"
  pattern = r"(?P<tag>\d{2})\.(?P<monat>\d{2})\.(?P<jahr>\d{4})"
  match = re.search(pattern, text)
  if match:
      print(match.group("tag"))    # 15
      print(match.group("monat"))  # 03
      print(match.group("jahr"))   # 1990
      print(match.groupdict())     # {'tag': '15', 'monat': '03', 'jahr': '1990'}

NICHT-ERFASSENDE GRUPPEN
  (?:...)   Gruppierung ohne Erfassung

  text = "httpx://example.com"
  # Mit Erfassung
  print(re.findall(r"(https?)://", text))   # ['http']
  # Ohne Erfassung
  print(re.findall(r"(?:https?)://", text)) # ['http://']

LOOKAHEAD UND LOOKBEHIND
------------------------

POSITIVE LOOKAHEAD
  (?=...)   Gefolgt von (ohne Erfassung)

  text = "Python3 Java8 Ruby"
  # Woerter, denen eine Zahl folgt
  print(re.findall(r"\w+(?=\d)", text))  # ['Python', 'Java']

NEGATIVE LOOKAHEAD
  (?!...)   NICHT gefolgt von

  text = "Python3 Java8 Ruby"
  # Woerter, denen KEINE Zahl folgt
  print(re.findall(r"\b\w+\b(?!\d)", text))  # ['Ruby']

POSITIVE LOOKBEHIND
  (?<=...)  Vorausgegangen von

  text = "Preis: 99 Euro"
  # Zahl nach "Preis: "
  print(re.findall(r"(?<=Preis: )\d+", text))  # ['99']

NEGATIVE LOOKBEHIND
  (?<!...)  NICHT vorausgegangen von

  text = "$100 und 200"
  # Zahl ohne $ davor
  print(re.findall(r"(?<!\$)\d+", text))  # ['00', '200']

FLAGS (MODIFIKATOREN)
=====================

  re.IGNORECASE (re.I)   Gross-/Kleinschreibung ignorieren
  re.MULTILINE (re.M)    ^ und $ auch bei Zeilenwechseln
  re.DOTALL (re.S)       . matcht auch Newline
  re.VERBOSE (re.X)      Erlaubt Kommentare und Whitespace

  Beispiel IGNORECASE:
    text = "Python PYTHON python"
    print(re.findall(r"python", text, re.I))  # ['Python', 'PYTHON', 'python']

  Beispiel MULTILINE:
    text = """Zeile1
    Zeile2
    Zeile3"""
    print(re.findall(r"^Zeile\d", text, re.M))  # ['Zeile1', 'Zeile2', 'Zeile3']

  Beispiel VERBOSE (lesbare Regex):
    pattern = re.compile(r"""
        (?P<vorname>\w+)   # Vorname
        \s+                # Leerzeichen
        (?P<nachname>\w+)  # Nachname
    """, re.VERBOSE)

KOMPILIERTE MUSTER
==================
  Bei mehrfacher Verwendung eines Musters - vorkompilieren!

  # Einmal kompilieren
  email_pattern = re.compile(
      r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
      re.IGNORECASE
  )

  # Mehrfach verwenden
  emails = [
      "test@example.com",
      "ungueltig",
      "noch.eine@mail.de"
  ]

  for email in emails:
      if email_pattern.match(email):
          print(f"Gueltig: {email}")

PRAXISBEISPIELE
===============

E-MAIL-VALIDIERUNG
------------------
  import re

  def ist_gueltige_email(email):
      pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
      return bool(re.match(pattern, email))

  print(ist_gueltige_email("test@example.com"))  # True
  print(ist_gueltige_email("ungueltig"))         # False

TELEFONNUMMER EXTRAHIEREN
-------------------------
  text = "Rufen Sie an: +49 123 456789 oder 0800-123456"
  pattern = r"(?:\+\d{2}\s?)?\d{3,4}[\s-]?\d{5,6}"
  telefone = re.findall(pattern, text)
  print(telefone)  # ['+49 123 456789', '0800-123456']

URL-PARSING
-----------
  url = "https://www.example.com:8080/path/to/page?query=value"
  pattern = r"(?P<protocol>https?)://(?P<domain>[^:/]+)(?::(?P<port>\d+))?(?P<path>/[^?]*)?(?:\?(?P<query>.*))?"

  match = re.match(pattern, url)
  if match:
      print(match.groupdict())
      # {'protocol': 'https', 'domain': 'www.example.com',
      #  'port': '8080', 'path': '/path/to/page', 'query': 'query=value'}

LOG-PARSING
-----------
  log_line = "2026-02-05 14:30:45 ERROR [main] NullPointerException"
  pattern = r"(?P<datum>\d{4}-\d{2}-\d{2}) (?P<zeit>\d{2}:\d{2}:\d{2}) (?P<level>\w+) \[(?P<modul>\w+)\] (?P<msg>.*)"

  match = re.match(pattern, log_line)
  if match:
      info = match.groupdict()
      print(f"Level: {info['level']}, Modul: {info['modul']}")

PASSWORT-VALIDIERUNG
--------------------
  def ist_sicheres_passwort(pw):
      """
      Prueft: min 8 Zeichen, Gross-/Kleinbuchstabe, Zahl, Sonderzeichen
      """
      if len(pw) < 8:
          return False
      if not re.search(r"[A-Z]", pw):
          return False
      if not re.search(r"[a-z]", pw):
          return False
      if not re.search(r"\d", pw):
          return False
      if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
          return False
      return True

TEXT BEREINIGEN
---------------
  def bereinige_text(text):
      # Mehrfache Leerzeichen zu einem
      text = re.sub(r"\s+", " ", text)
      # Sonderzeichen entfernen
      text = re.sub(r"[^\w\s]", "", text)
      # Trim
      return text.strip()

  dirty = "  Viel   zu   viele!!!   Leerzeichen...  "
  print(bereinige_text(dirty))  # "Viel zu viele Leerzeichen"

BEST PRACTICES
==============

RAW STRINGS VERWENDEN
---------------------
  # IMMER r"..." fuer Regex verwenden
  # RICHTIG:
  pattern = r"\d+\.\d+"

  # FALSCH (Escape-Probleme):
  pattern = "\d+\.\d+"

LESBARKEIT PRIORISIEREN
-----------------------
  # Komplexe Muster mit re.VERBOSE
  pattern = re.compile(r"""
      ^                    # Zeilenanfang
      (?P<jahr>\d{4})      # Jahr (4 Ziffern)
      -                    # Trennzeichen
      (?P<monat>\d{2})     # Monat (2 Ziffern)
      -                    # Trennzeichen
      (?P<tag>\d{2})       # Tag (2 Ziffern)
      $                    # Zeilenende
  """, re.VERBOSE)

FEHLERBEHANDLUNG
----------------
  def sichere_regex_suche(pattern, text):
      try:
          return re.findall(pattern, text)
      except re.error as e:
          print(f"Ungueltiges Muster: {e}")
          return []

PERFORMANCE
-----------
  # Muster vorkompilieren bei mehrfacher Verwendung
  pattern = re.compile(r"\d+")

  # NICHT in Schleifen kompilieren!
  for line in lines:
      # SCHLECHT: re.search(r"\d+", line)
      # GUT: pattern.search(line)
      match = pattern.search(line)

ESCAPE-FUNKTION
---------------
  # Benutzereingaben escapen
  user_input = "test.file[1]"
  safe_pattern = re.escape(user_input)
  print(safe_pattern)  # test\.file\[1\]

HAEUFIGE FEHLER
===============

  1. Vergessene Raw-Strings
     FALSCH: re.search("\d+", text)
     RICHTIG: re.search(r"\d+", text)

  2. Gieriges Matching bei HTML/XML
     FALSCH: re.findall(r"<.*>", "<a><b>")  # ['<a><b>']
     RICHTIG: re.findall(r"<.*?>", "<a><b>")  # ['<a>', '<b>']

  3. match() vs search()
     match() sucht NUR am Anfang!
     search() sucht ueberall.

  4. Zeichenklassen-Sonderzeichen
     In [...] haben nur wenige Zeichen Sonderbedeutung:
     ] - ^ \

     Das hier ist RICHTIG: [.+*?]  # matcht . + * ?

ALTERNATIVEN
============
  Fuer einfache Faelle oft besser:
    - str.startswith() / str.endswith()
    - str.find() / str.replace()
    - "substring" in string
    - str.split()

  Regex nur wenn wirklich noetig!

SIEHE AUCH
==========
  wiki/python/README.txt               Python Uebersicht
  wiki/python/dateioperationen/        Dateien mit Regex durchsuchen
  wiki/python/automatisierung/         Regex fuer Log-Parsing
  wiki/informatik/programmierung/      Allgemeine Programmierkonzepte
