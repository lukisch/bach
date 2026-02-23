# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: Python Documentation, PEP 255, PEP 289, PEP 380, Real Python

================================================================================
                            PYTHON GENERATORS
================================================================================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
INHALTSVERZEICHNIS
================================================================================
  1. Einfuehrung und Konzept
  2. Generator-Funktionen mit yield
  3. Das Iterator-Protokoll
  4. Generator Expressions
  5. yield from - Delegation
  6. Generator-Methoden: send, throw, close
  7. Speichereffizienz und Performance
  8. Praktische Anwendungsbeispiele
  9. Generatoren vs. Listen
  10. Best Practices und Fallstricke
  11. Fortgeschrittene Techniken

================================================================================
1. EINFUEHRUNG UND KONZEPT
================================================================================

  Generatoren sind eine elegante Methode zur Erstellung von Iteratoren in
  Python. Sie erzeugen Werte "on demand" (lazy evaluation), anstatt alle
  Werte auf einmal im Speicher zu halten.

  KERNPRINZIP:
    Ein Generator ist eine Funktion, die das Schluesselwort 'yield'
    verwendet. Bei jedem Aufruf von next() wird die Ausfuehrung bis zum
    naechsten yield fortgesetzt, der Wert zurueckgegeben und der Zustand
    "eingefroren".

  VORTEILE:
    - Speichereffizient: Nur ein Wert zur Zeit im Speicher
    - Lazy Evaluation: Werte werden erst bei Bedarf berechnet
    - Kann unendliche Sequenzen darstellen
    - Einfachere Syntax als manuelle Iterator-Klassen
    - Ideal fuer Streaming und Pipelining

  ANWENDUNGSGEBIETE:
    - Verarbeitung grosser Dateien
    - Datenbankabfragen mit vielen Ergebnissen
    - Netzwerk-Streams
    - Mathematische Sequenzen
    - Datentransformations-Pipelines

================================================================================
2. GENERATOR-FUNKTIONEN MIT YIELD
================================================================================

  EINFACHER GENERATOR:
  --------------------
    def count_up_to(max_value):
        """Zaehlt von 1 bis max_value."""
        current = 1
        while current <= max_value:
            yield current
            current += 1

    # Verwendung
    for num in count_up_to(5):
        print(num)  # Ausgabe: 1, 2, 3, 4, 5


  WIE ES FUNKTIONIERT:
  --------------------
    1. Aufruf von count_up_to(5) erzeugt Generator-Objekt (noch keine Ausfuehrung)
    2. Erster next()-Aufruf: Code laeuft bis zum ersten yield
    3. Wert wird zurueckgegeben, Zustand wird "eingefroren"
    4. Naechster next()-Aufruf: Fortsetzung nach yield
    5. Bei Funktionsende: StopIteration wird ausgeloest


  MEHRFACHES YIELD:
  -----------------
    def multi_yield():
        print("Erster Block")
        yield 1
        print("Zweiter Block")
        yield 2
        print("Dritter Block")
        yield 3
        print("Ende")

    gen = multi_yield()
    print(next(gen))  # "Erster Block", dann 1
    print(next(gen))  # "Zweiter Block", dann 2
    print(next(gen))  # "Dritter Block", dann 3
    # next(gen)       # "Ende", dann StopIteration


  YIELD MIT RUECKGABEWERT:
  ------------------------
    def generator_with_return():
        yield 1
        yield 2
        return "Fertig"  # Wird Teil von StopIteration.value

    gen = generator_with_return()
    print(next(gen))  # 1
    print(next(gen))  # 2
    try:
        next(gen)
    except StopIteration as e:
        print(e.value)  # "Fertig"

================================================================================
3. DAS ITERATOR-PROTOKOLL
================================================================================

  Generatoren implementieren automatisch das Iterator-Protokoll:

  __iter__():
    Gibt den Iterator selbst zurueck (Generator ist sein eigener Iterator)

  __next__():
    Gibt den naechsten Wert zurueck oder loest StopIteration aus


  MANUELLER ITERATOR (zum Vergleich):
  -----------------------------------
    class CountUpTo:
        """Manueller Iterator - mehr Code noetig."""

        def __init__(self, max_value):
            self.max_value = max_value
            self.current = 0

        def __iter__(self):
            return self

        def __next__(self):
            self.current += 1
            if self.current <= self.max_value:
                return self.current
            raise StopIteration


  GENERATOR-AEQUIVALENT:
  ----------------------
    def count_up_to(max_value):
        """Generator - viel einfacher!"""
        current = 1
        while current <= max_value:
            yield current
            current += 1


  ITERATOR-FUNKTIONEN:
  --------------------
    gen = (x**2 for x in range(5))

    next(gen)        # Naechster Wert: 0
    next(gen)        # Naechster Wert: 1

    # ACHTUNG: Generator ist erschoepft nach einmaligem Durchlauf
    list(gen)        # [4, 9, 16] - nur noch die verbliebenen Werte

================================================================================
4. GENERATOR EXPRESSIONS
================================================================================

  Generator Expressions sind die "lazy" Version von List Comprehensions:

  SYNTAX-VERGLEICH:
  -----------------
    # List Comprehension - alle Werte sofort im Speicher
    squares_list = [x**2 for x in range(1000000)]

    # Generator Expression - Werte on demand
    squares_gen = (x**2 for x in range(1000000))

    # Set Comprehension
    squares_set = {x**2 for x in range(10)}

    # Dict Comprehension
    squares_dict = {x: x**2 for x in range(10)}


  SPEICHERVERGLEICH:
  ------------------
    import sys

    # List: ca. 8 MB fuer 1 Million Integers
    list_mem = sys.getsizeof([x for x in range(1000000)])

    # Generator: ca. 200 Bytes (nur das Generator-Objekt)
    gen_mem = sys.getsizeof(x for x in range(1000000))

    print(f"Liste: {list_mem:,} Bytes")      # ~8,697,464 Bytes
    print(f"Generator: {gen_mem:,} Bytes")   # ~200 Bytes


  VERSCHACHTELTE EXPRESSIONS:
  ---------------------------
    # Matrix-Elemente
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    # Alle Elemente flach (Generator)
    flat = (elem for row in matrix for elem in row)

    # Mit Bedingung
    even_flat = (elem for row in matrix for elem in row if elem % 2 == 0)


  ALS FUNKTIONSARGUMENT:
  ----------------------
    # Klammern koennen weggelassen werden bei einzelnem Argument
    total = sum(x**2 for x in range(100))
    joined = ", ".join(str(x) for x in range(10))
    exists = any(x > 5 for x in [1, 2, 3, 4, 5, 6])

================================================================================
5. YIELD FROM - DELEGATION
================================================================================

  'yield from' (Python 3.3+, PEP 380) delegiert an einen Sub-Generator:

  GRUNDLEGENDE VERWENDUNG:
  ------------------------
    def sub_generator():
        yield 1
        yield 2
        yield 3

    def main_generator():
        yield "Start"
        yield from sub_generator()  # Delegiert
        yield "Ende"

    list(main_generator())  # ['Start', 1, 2, 3, 'Ende']


  OHNE YIELD FROM (aequivalent):
  ------------------------------
    def main_generator():
        yield "Start"
        for item in sub_generator():
            yield item
        yield "Ende"


  YIELD FROM MIT ITERABLES:
  -------------------------
    def flatten(nested):
        """Verschachtelte Liste flach machen."""
        for item in nested:
            if isinstance(item, list):
                yield from flatten(item)  # Rekursiv
            else:
                yield item

    nested = [1, [2, 3, [4, 5]], 6, [7, 8]]
    print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6, 7, 8]


  MEHRERE QUELLEN KOMBINIEREN:
  ----------------------------
    def combined():
        yield from range(3)        # 0, 1, 2
        yield from "ABC"           # 'A', 'B', 'C'
        yield from [10, 20, 30]    # 10, 20, 30

    list(combined())  # [0, 1, 2, 'A', 'B', 'C', 10, 20, 30]

================================================================================
6. GENERATOR-METHODEN: SEND, THROW, CLOSE
================================================================================

  Generatoren sind bidirektional - man kann Werte hineinsenden:

  SEND - WERTE SENDEN:
  --------------------
    def accumulator():
        """Summiert gesendete Werte."""
        total = 0
        while True:
            value = yield total
            if value is not None:
                total += value

    acc = accumulator()
    next(acc)           # Initialisieren, gibt 0 zurueck
    print(acc.send(10)) # 10
    print(acc.send(5))  # 15
    print(acc.send(3))  # 18


  KOROUTINEN-MUSTER:
  ------------------
    def coroutine():
        print("Gestartet")
        while True:
            received = yield
            print(f"Empfangen: {received}")

    coro = coroutine()
    next(coro)           # "Gestartet" - bis zum ersten yield
    coro.send("Hallo")   # "Empfangen: Hallo"
    coro.send("Welt")    # "Empfangen: Welt"


  THROW - EXCEPTION EINWERFEN:
  ----------------------------
    def generator_with_error_handling():
        try:
            while True:
                value = yield
                print(f"Wert: {value}")
        except ValueError as e:
            print(f"ValueError abgefangen: {e}")
            yield "Fehler behandelt"

    gen = generator_with_error_handling()
    next(gen)
    gen.send(1)                              # "Wert: 1"
    result = gen.throw(ValueError, "Test")   # "ValueError abgefangen: Test"
    print(result)                            # "Fehler behandelt"


  CLOSE - GENERATOR BEENDEN:
  --------------------------
    def resource_generator():
        print("Resource oeffnen")
        try:
            while True:
                yield "Daten"
        finally:
            print("Resource schliessen (Cleanup)")

    gen = resource_generator()
    next(gen)      # "Resource oeffnen", gibt "Daten"
    gen.close()    # "Resource schliessen (Cleanup)"
    # GeneratorExit wird im Generator ausgeloest

================================================================================
7. SPEICHEREFFIZIENZ UND PERFORMANCE
================================================================================

  GROSSE DATEIEN LESEN:
  ---------------------
    # SCHLECHT: Ganze Datei im Speicher
    def read_all_lines(filename):
        with open(filename) as f:
            return f.readlines()  # Liste mit allen Zeilen

    # GUT: Generator - eine Zeile zur Zeit
    def read_lines(filename):
        with open(filename) as f:
            for line in f:
                yield line.strip()

    # Verwendung
    for line in read_lines("huge_file.txt"):
        process(line)  # Nur eine Zeile im Speicher


  DATENTRANSFORMATION PIPELINE:
  -----------------------------
    def read_csv_lines(filename):
        with open(filename) as f:
            next(f)  # Header ueberspringen
            for line in f:
                yield line.strip()

    def parse_row(lines):
        for line in lines:
            yield line.split(",")

    def filter_valid(rows):
        for row in rows:
            if len(row) >= 3:
                yield row

    def transform(rows):
        for row in rows:
            yield {
                "name": row[0],
                "value": int(row[1]),
                "category": row[2]
            }

    # Pipeline zusammensetzen - nichts passiert bis zur Iteration
    pipeline = transform(filter_valid(parse_row(read_csv_lines("data.csv"))))

    # Erst jetzt werden Daten verarbeitet
    for record in pipeline:
        print(record)


  ITERTOOLS FUER GENERATOREN:
  ---------------------------
    from itertools import islice, chain, takewhile, dropwhile

    gen = (x**2 for x in range(100))

    # Erste 5 Elemente
    first_five = list(islice(gen, 5))

    # Generatoren verketten
    combined = chain(range(3), range(10, 13))

    # Bedingt nehmen
    under_50 = takewhile(lambda x: x < 50, (x**2 for x in range(20)))

================================================================================
8. PRAKTISCHE ANWENDUNGSBEISPIELE
================================================================================

  FIBONACCI-SEQUENZ (unendlich):
  ------------------------------
    def fibonacci():
        """Unendliche Fibonacci-Sequenz."""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    # Erste 10 Fibonacci-Zahlen
    from itertools import islice
    print(list(islice(fibonacci(), 10)))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


  SLIDING WINDOW:
  ---------------
    from collections import deque

    def sliding_window(iterable, size):
        """Erzeugt gleitende Fenster ueber Daten."""
        it = iter(iterable)
        window = deque(maxlen=size)

        # Fenster fuellen
        for _ in range(size):
            window.append(next(it))
        yield tuple(window)

        # Weiterschieben
        for item in it:
            window.append(item)
            yield tuple(window)

    data = [1, 2, 3, 4, 5, 6]
    for window in sliding_window(data, 3):
        print(window)
    # (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6)


  BATCH-VERARBEITUNG:
  -------------------
    def batch(iterable, size):
        """Teilt Iterable in Batches auf."""
        from itertools import islice
        it = iter(iterable)
        while True:
            chunk = list(islice(it, size))
            if not chunk:
                return
            yield chunk

    for b in batch(range(10), 3):
        print(b)
    # [0, 1, 2], [3, 4, 5], [6, 7, 8], [9]


  LOG-FILE MONITORING (tail -f):
  ------------------------------
    import time

    def follow(filename):
        """Folgt einer Datei wie tail -f."""
        with open(filename) as f:
            f.seek(0, 2)  # Ende der Datei
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                yield line.strip()

    # for line in follow("/var/log/syslog"):
    #     print(line)

================================================================================
9. GENERATOREN VS. LISTEN
================================================================================

  WANN GENERATOREN VERWENDEN:
  ---------------------------
    + Grosse oder unbekannte Datenmenge
    + Daten werden nur einmal durchlaufen
    + Speicher ist begrenzt
    + Streaming/Pipeline-Verarbeitung
    + Unendliche Sequenzen

  WANN LISTEN VERWENDEN:
  ----------------------
    + Mehrfacher Zugriff auf Elemente noetig
    + Random Access erforderlich (index)
    + Laenge muss bekannt sein
    + Daten muessen sortiert werden
    + Kleine, bekannte Datenmenge

  VERGLEICHSTABELLE:
  ------------------
    Eigenschaft          | Generator        | Liste
    ---------------------|------------------|------------------
    Speicher             | O(1)             | O(n)
    Random Access        | Nein             | Ja
    Mehrfach iterierbar  | Nein             | Ja
    Laenge (len)         | Nicht direkt     | O(1)
    Slicing              | Mit islice       | Ja
    Sortieren            | Nicht moeglich   | Ja

================================================================================
10. BEST PRACTICES UND FALLSTRICKE
================================================================================

  BEST PRACTICES:
  ---------------
    1. Generatoren fuer grosse/unbekannte Datenmengen nutzen
    2. yield from fuer Sub-Generatoren verwenden
    3. Cleanup-Code in finally-Block bei close()
    4. Generator Expressions fuer einfache Transformationen
    5. itertools fuer komplexe Generator-Operationen

  HAEUFIGE FALLSTRICKE:
  ---------------------
    1. Generator kann nur einmal durchlaufen werden:

       gen = (x for x in range(5))
       list(gen)  # [0, 1, 2, 3, 4]
       list(gen)  # [] - leer!

    2. len() funktioniert nicht direkt:

       gen = (x for x in range(5))
       # len(gen)  # TypeError!

       # Loesung (verbraucht Generator):
       length = sum(1 for _ in gen)

    3. Debugging ist schwieriger (Zustand nicht sichtbar)

    4. StopIteration-Propagation (vor Python 3.7 problematisch)

    5. Generator-Ausdruecke mit spaeter Bindung:

       funcs = [lambda: x for x in range(3)]
       print([f() for f in funcs])  # [2, 2, 2] - nicht [0, 1, 2]!

================================================================================
11. FORTGESCHRITTENE TECHNIKEN
================================================================================

  GENERATOR ALS CONTEXT MANAGER:
  ------------------------------
    from contextlib import contextmanager

    @contextmanager
    def managed_resource(name):
        print(f"Resource '{name}' oeffnen")
        try:
            yield name
        finally:
            print(f"Resource '{name}' schliessen")

    with managed_resource("Datei") as res:
        print(f"Arbeite mit {res}")


  ASYNCHRONE GENERATOREN (Python 3.6+):
  -------------------------------------
    async def async_generator():
        for i in range(5):
            await asyncio.sleep(0.1)
            yield i

    async def main():
        async for value in async_generator():
            print(value)


  GENERATOR-BASIERTES COROUTINE-SCHEDULING:
  -----------------------------------------
    def task(name, count):
        for i in range(count):
            print(f"{name}: Schritt {i}")
            yield  # Kontrolle abgeben

    def scheduler(tasks):
        """Einfacher Round-Robin Scheduler."""
        from collections import deque
        queue = deque(tasks)
        while queue:
            task = queue.popleft()
            try:
                next(task)
                queue.append(task)
            except StopIteration:
                pass

    scheduler([task("A", 3), task("B", 2), task("C", 4)])

================================================================================
SIEHE AUCH
================================================================================

  wiki/python/funktionen/          - Grundlagen zu Funktionen
  wiki/python/decorators/          - Decorators
  wiki/python/itertools/           - itertools Modul
  wiki/python/asyncio/             - Asynchrone Programmierung

================================================================================
