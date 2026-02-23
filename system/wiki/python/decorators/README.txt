# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: Python Documentation, PEP 318, PEP 3129, Real Python

================================================================================
                            PYTHON DECORATORS
================================================================================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
INHALTSVERZEICHNIS
================================================================================
  1. Einfuehrung und Konzept
  2. Grundlegende Decorator-Syntax
  3. functools.wraps - Metadaten bewahren
  4. Decorators mit Parametern
  5. Klassen als Decorators
  6. Klassen-Decorators (Klassen dekorieren)
  7. Verschachtelte Decorators
  8. Eingebaute Decorators
  9. Praktische Anwendungsbeispiele
  10. Best Practices und Fallstricke
  11. Fortgeschrittene Techniken

================================================================================
1. EINFUEHRUNG UND KONZEPT
================================================================================

  Decorators sind ein maechtigens Werkzeug in Python, das es ermoeglicht,
  das Verhalten von Funktionen oder Klassen zu modifizieren, ohne deren
  Quellcode zu aendern.

  KERNPRINZIP:
    Ein Decorator ist eine Funktion, die eine andere Funktion als Argument
    nimmt und eine neue Funktion zurueckgibt. Dies folgt dem "Higher-Order
    Functions"-Konzept aus der funktionalen Programmierung.

  ANWENDUNGSGEBIETE:
    - Logging und Debugging
    - Zugriffskontrolle und Authentifizierung
    - Caching und Memoization
    - Zeitmessung und Profiling
    - Eingabevalidierung
    - Retry-Logik bei Fehlern
    - Registrierung von Plugins/Routen

================================================================================
2. GRUNDLEGENDE DECORATOR-SYNTAX
================================================================================

  MANUELLER ANSATZ (ohne @-Syntax):
  ---------------------------------

    def my_decorator(func):
        def wrapper(*args, **kwargs):
            print("Vor dem Funktionsaufruf")
            result = func(*args, **kwargs)
            print("Nach dem Funktionsaufruf")
            return result
        return wrapper

    def say_hello(name):
        print(f"Hallo, {name}!")

    # Decorator manuell anwenden
    say_hello = my_decorator(say_hello)
    say_hello("Welt")

    # Ausgabe:
    # Vor dem Funktionsaufruf
    # Hallo, Welt!
    # Nach dem Funktionsaufruf


  MIT @-SYNTAX (Syntaktischer Zucker seit Python 2.4):
  ----------------------------------------------------

    def my_decorator(func):
        def wrapper(*args, **kwargs):
            print("Vor dem Funktionsaufruf")
            result = func(*args, **kwargs)
            print("Nach dem Funktionsaufruf")
            return result
        return wrapper

    @my_decorator
    def say_hello(name):
        print(f"Hallo, {name}!")

    # Identisch zu: say_hello = my_decorator(say_hello)


  WICHTIG: *args und **kwargs
  ---------------------------
    Die Verwendung von *args und **kwargs im Wrapper stellt sicher,
    dass der Decorator mit beliebigen Funktionssignaturen funktioniert:

    def universal_decorator(func):
        def wrapper(*args, **kwargs):
            # args = Tupel aller positionalen Argumente
            # kwargs = Dictionary aller Keyword-Argumente
            return func(*args, **kwargs)
        return wrapper

================================================================================
3. FUNCTOOLS.WRAPS - METADATEN BEWAHREN
================================================================================

  PROBLEM OHNE @wraps:
  --------------------
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @decorator
    def greet(name):
        """Begruesse eine Person."""
        print(f"Hallo, {name}")

    print(greet.__name__)  # Ausgabe: "wrapper" (FALSCH!)
    print(greet.__doc__)   # Ausgabe: None (FALSCH!)


  LOESUNG MIT @wraps:
  -------------------
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @decorator
    def greet(name):
        """Begruesse eine Person."""
        print(f"Hallo, {name}")

    print(greet.__name__)  # Ausgabe: "greet" (KORREKT!)
    print(greet.__doc__)   # Ausgabe: "Begruesse eine Person." (KORREKT!)


  @wraps BEWAHRT FOLGENDE ATTRIBUTE:
    - __name__      : Funktionsname
    - __doc__       : Docstring
    - __module__    : Modulname
    - __qualname__  : Qualifizierter Name
    - __annotations__: Type Hints
    - __dict__      : Funktionsattribute
    - __wrapped__   : Referenz zur Original-Funktion

================================================================================
4. DECORATORS MIT PARAMETERN
================================================================================

  Um Parameter an einen Decorator zu uebergeben, benoetigt man eine
  zusaetzliche aeussere Funktion (Decorator-Factory):

  STRUKTUR:
  ---------
    def decorator_with_args(arg1, arg2):      # Aeussere Funktion (Factory)
        def decorator(func):                   # Eigentlicher Decorator
            @wraps(func)
            def wrapper(*args, **kwargs):      # Wrapper-Funktion
                # Zugriff auf arg1, arg2, func, args, kwargs
                return func(*args, **kwargs)
            return wrapper
        return decorator


  BEISPIEL - Repeat Decorator:
  ----------------------------
    from functools import wraps

    def repeat(times):
        """Fuehrt eine Funktion mehrfach aus."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = None
                for _ in range(times):
                    result = func(*args, **kwargs)
                return result
            return wrapper
        return decorator

    @repeat(times=3)
    def greet(name):
        print(f"Hallo, {name}!")

    greet("Welt")
    # Ausgabe:
    # Hallo, Welt!
    # Hallo, Welt!
    # Hallo, Welt!


  BEISPIEL - Retry Decorator:
  ---------------------------
    import time
    from functools import wraps

    def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
        """Wiederholt Funktionsaufruf bei Fehler."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt < max_attempts - 1:
                            time.sleep(delay)
                raise last_exception
            return wrapper
        return decorator

    @retry(max_attempts=5, delay=2.0, exceptions=(ConnectionError,))
    def fetch_data(url):
        # Netzwerk-Code
        pass

================================================================================
5. KLASSEN ALS DECORATORS
================================================================================

  Klassen koennen als Decorators verwendet werden, indem __call__
  implementiert wird:

  EINFACHE KLASSE:
  ----------------
    class CountCalls:
        """Zaehlt Funktionsaufrufe."""

        def __init__(self, func):
            self.func = func
            self.count = 0
            # Metadaten kopieren
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__

        def __call__(self, *args, **kwargs):
            self.count += 1
            print(f"Aufruf #{self.count} von {self.func.__name__}")
            return self.func(*args, **kwargs)

    @CountCalls
    def say_hello():
        print("Hallo!")

    say_hello()  # Aufruf #1 von say_hello
    say_hello()  # Aufruf #2 von say_hello
    print(say_hello.count)  # 2


  KLASSE MIT PARAMETERN:
  ----------------------
    class RateLimit:
        """Begrenzt Aufrufe pro Zeiteinheit."""

        def __init__(self, max_calls, period):
            self.max_calls = max_calls
            self.period = period
            self.calls = []

        def __call__(self, func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                import time
                now = time.time()
                # Alte Aufrufe entfernen
                self.calls = [c for c in self.calls if now - c < self.period]
                if len(self.calls) >= self.max_calls:
                    raise RuntimeError("Rate limit exceeded")
                self.calls.append(now)
                return func(*args, **kwargs)
            return wrapper

    @RateLimit(max_calls=5, period=60)
    def api_call():
        pass

================================================================================
6. KLASSEN-DECORATORS (KLASSEN DEKORIEREN)
================================================================================

  Seit Python 3.0 (PEP 3129) koennen auch Klassen dekoriert werden:

    def add_method(cls):
        """Fuegt einer Klasse eine Methode hinzu."""
        def new_method(self):
            return f"Neue Methode in {cls.__name__}"
        cls.new_method = new_method
        return cls

    @add_method
    class MyClass:
        pass

    obj = MyClass()
    print(obj.new_method())  # "Neue Methode in MyClass"


  BEKANNTES BEISPIEL - @dataclass:
  --------------------------------
    from dataclasses import dataclass

    @dataclass
    class Person:
        name: str
        age: int

    # Generiert automatisch: __init__, __repr__, __eq__, etc.

================================================================================
7. VERSCHACHTELTE DECORATORS
================================================================================

  Mehrere Decorators werden von unten nach oben angewendet:

    @decorator_a
    @decorator_b
    @decorator_c
    def func():
        pass

    # Entspricht:
    func = decorator_a(decorator_b(decorator_c(func)))


  BEISPIEL:
  ---------
    def bold(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return f"<b>{func(*args, **kwargs)}</b>"
        return wrapper

    def italic(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return f"<i>{func(*args, **kwargs)}</i>"
        return wrapper

    @bold
    @italic
    def greet(name):
        return f"Hallo, {name}"

    print(greet("Welt"))  # <b><i>Hallo, Welt</i></b>

================================================================================
8. EINGEBAUTE DECORATORS
================================================================================

  PYTHON STANDARD LIBRARY:
  ------------------------
    @staticmethod      # Methode ohne self/cls
    @classmethod       # Methode mit cls statt self
    @property          # Getter fuer Attribut
    @name.setter       # Setter fuer Property
    @abstractmethod    # Abstrakte Methode (abc)

  FUNCTOOLS:
  ----------
    @functools.wraps           # Metadaten bewahren
    @functools.lru_cache       # Memoization/Caching
    @functools.cache           # Einfaches Caching (Python 3.9+)
    @functools.cached_property # Gecachte Property (Python 3.8+)
    @functools.singledispatch  # Funktionsueberladung

  DATACLASSES:
  ------------
    @dataclass         # Automatische __init__, __repr__, etc.

  TYPING:
  -------
    @typing.overload   # Typisierung fuer Ueberladungen

  CONTEXTLIB:
  -----------
    @contextmanager    # Context Manager aus Generator

================================================================================
9. PRAKTISCHE ANWENDUNGSBEISPIELE
================================================================================

  LOGGING DECORATOR:
  ------------------
    import logging
    from functools import wraps

    def log_calls(logger=None):
        if logger is None:
            logger = logging.getLogger(__name__)

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                logger.info(f"Aufruf: {func.__name__}(args={args}, kwargs={kwargs})")
                try:
                    result = func(*args, **kwargs)
                    logger.info(f"Rueckgabe: {func.__name__} -> {result}")
                    return result
                except Exception as e:
                    logger.exception(f"Fehler in {func.__name__}: {e}")
                    raise
            return wrapper
        return decorator


  ZEITMESSUNG:
  ------------
    import time
    from functools import wraps

    def timeit(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"{func.__name__} dauerte {end - start:.4f} Sekunden")
            return result
        return wrapper


  EINGABEVALIDIERUNG:
  -------------------
    from functools import wraps

    def validate_types(**expected_types):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for name, expected_type in expected_types.items():
                    if name in kwargs:
                        if not isinstance(kwargs[name], expected_type):
                            raise TypeError(
                                f"{name} muss {expected_type.__name__} sein"
                            )
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @validate_types(name=str, age=int)
    def create_user(name, age):
        return {"name": name, "age": age}

================================================================================
10. BEST PRACTICES UND FALLSTRICKE
================================================================================

  BEST PRACTICES:
  ---------------
    1. Immer @wraps verwenden
    2. *args und **kwargs im Wrapper nutzen
    3. Decorators sollten transparent sein (Funktion sollte normal funktionieren)
    4. Aussagekraeftige Docstrings fuer Decorators
    5. Decorator-Factories fuer parametrisierte Decorators

  HAEUFIGE FALLSTRICKE:
  ---------------------
    1. Vergessen von @wraps -> Metadaten gehen verloren
    2. Vergessen von return im Wrapper -> None wird zurueckgegeben
    3. Decorator mit Klammer verwechseln:
       - @decorator     : Decorator ohne Parameter
       - @decorator()   : Decorator-Factory ohne Parameter
    4. Reihenfolge bei mehreren Decorators falsch verstehen

  DEBUGGING VON DEKORIERTEN FUNKTIONEN:
  -------------------------------------
    # Original-Funktion erreichen (wenn @wraps verwendet wurde)
    original = decorated_func.__wrapped__

================================================================================
11. FORTGESCHRITTENE TECHNIKEN
================================================================================

  OPTIONALE PARAMETER:
  --------------------
    def decorator(func=None, *, debug=False):
        """Decorator mit optionalem Parameter."""
        def actual_decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                if debug:
                    print(f"Debug: Aufruf von {f.__name__}")
                return f(*args, **kwargs)
            return wrapper

        if func is not None:
            return actual_decorator(func)
        return actual_decorator

    # Beide Varianten funktionieren:
    @decorator
    def func1(): pass

    @decorator(debug=True)
    def func2(): pass


  METHODEN-DECORATOR MIT DESCRIPTOR:
  ----------------------------------
    class MethodDecorator:
        def __init__(self, func):
            self.func = func

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            return lambda *args, **kwargs: self.func(obj, *args, **kwargs)

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

================================================================================
SIEHE AUCH
================================================================================

  wiki/python/funktionen/          - Grundlagen zu Funktionen
  wiki/python/oop/                  - Objektorientierte Programmierung
  wiki/python/generators/          - Generatoren und yield
  wiki/python/context_manager/     - Context Manager (@contextmanager)

================================================================================
