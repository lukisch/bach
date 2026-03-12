# Design Patterns in Python - Umfassende Referenz

**Status:** Erstellt 2026-03-06 | Basierend auf aktueller Python-Community-Standards

---

## Übersicht

Dieses Dokument behandelt alle 23 klassischen Gang-of-Four Design Patterns mit Fokus auf **Python-spezifische Implementierungen**. Die Patterns sind in drei Kategorien organisiert:

1. **Creational Patterns (5)** — Objekterstellung
2. **Structural Patterns (7)** — Objektkomposition
3. **Behavioral Patterns (11)** — Objekt-Zusammenarbeit und Verantwortung

---

# I. CREATIONAL PATTERNS

Creational Patterns beschäftigen sich mit **flexibler und effizienter Objekterstellung**.

---

## 1. Singleton Pattern

### Definition & Zweck
Stellt sicher, dass eine Klasse **nur eine Instanz** hat und bietet einen **globalen Zugriffspunkt** darauf.

### Kategorie
Creational

### Python-spezifische Besonderheiten

- **Antipattern-Status:** Viele Python-Entwickler betrachten Singleton als schädlich
- **Moderne Alternative:** Dependency Injection bevorzugen
- **Best Practice:** Metaclass-Implementierung (sauberer als Decorator)
- **Wann verwenden:** Nur für wahrhaft globale Ressourcen (Logger, Config, DB-Connection)

### Code-Beispiel (Metaclass-Ansatz - Empfohlen)

```python
# Metaclass-basierte Implementierung (saubest)
class SingletonMeta(type):
    """Metaclass für Singleton-Pattern"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, connection_string="localhost"):
        self.connection_string = connection_string
        print(f"Initializing connection to {connection_string}")

    def query(self, sql):
        return f"Executing: {sql}"

# Verwendung
db1 = DatabaseConnection("prod-db")
db2 = DatabaseConnection("other-string")  # Ignoriert Parameter, gibt db1 zurück
print(db1 is db2)  # True - Gleiche Instanz
```

### Alternative: Decorator-Ansatz

```python
# Decorator-basierte Implementierung (auch gut lesbar)
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Logger:
    def __init__(self):
        self.logs = []

    def log(self, message):
        self.logs.append(message)

logger1 = Logger()
logger2 = Logger()
print(logger1 is logger2)  # True
```

### Use-Cases in Python

- **Logging-Systeme:** `logging.getLogger(name)` → gibt Singleton-Logger zurück
- **Konfiguration:** Zentrale App-Settings
- **DB-Connection-Pools:** Thread-safe Datenbank-Zugriff
- **Cache-Manager:** Zentrale Cache-Instanz

### Best Practices 2025

```python
# ✅ BESSER: Module-level Singleton (pythonisch)
class _DatabasePool:
    def __init__(self):
        self.connections = []

    def get_connection(self):
        return "connection"

# Eine Instanz pro Modul
db_pool = _DatabasePool()

# Im anderen Modul:
from mymodule import db_pool  # Gibt die gleiche Instanz zurück
```

---

## 2. Factory Method Pattern

### Definition & Zweck
Definiert eine **Schnittstelle zur Objekterstellung**, lässt aber **Subklassen** entscheiden, **welche Klasse** instantiiert wird.

### Kategorie
Creational

### Python-spezifische Besonderheiten

- **Class Methods:** Oft als `@classmethod` implementiert
- **Flexible Parameter:** Python akzeptiert beliebige Rückgabetypen
- **Strings oder Enums:** Häufig als Parameter für Objektauswahl
- **Subclass-Overriding:** Optional; oft nur eine zentrale Factory-Klasse

### Code-Beispiel

```python
from abc import ABC, abstractmethod

# Abstrakte Basis-Klasse
class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, sql):
        pass

# Konkrete Implementierungen
class MySQLConnection(DatabaseConnection):
    def connect(self):
        return "Connecting to MySQL..."

    def query(self, sql):
        return f"MySQL: {sql}"

class PostgresConnection(DatabaseConnection):
    def connect(self):
        return "Connecting to PostgreSQL..."

    def query(self, sql):
        return f"PostgreSQL: {sql}"

class MongoConnection(DatabaseConnection):
    def connect(self):
        return "Connecting to MongoDB..."

    def query(self, sql):
        return f"MongoDB: {sql}"

# Factory als Klassenmethode
class DatabaseFactory:
    @classmethod
    def create_connection(cls, db_type: str) -> DatabaseConnection:
        """Factory Method: Entscheidungslogik für Typ-Auswahl"""
        factories = {
            "mysql": MySQLConnection,
            "postgres": PostgresConnection,
            "mongo": MongoConnection,
        }

        connection_class = factories.get(db_type)
        if not connection_class:
            raise ValueError(f"Unbekannter DB-Typ: {db_type}")

        return connection_class()

# Verwendung
db = DatabaseFactory.create_connection("postgres")
print(db.connect())  # "Connecting to PostgreSQL..."
print(db.query("SELECT * FROM users"))  # "PostgreSQL: SELECT * FROM users"
```

### Pythonische Alternative mit Funktionen

```python
# Einfacher und oft besser als Klassenhierarchien
def create_database(db_type: str):
    """Factory-Funktion (often Pythonic)"""
    if db_type == "mysql":
        return MySQLConnection()
    elif db_type == "postgres":
        return PostgresConnection()
    else:
        raise ValueError(f"Unknown database: {db_type}")

db = create_database("mysql")
```

### Use-Cases in Python

- **Web-Frameworks:** Flask/Django-Middleware-Erstellung
- **Parser:** Format-basierte Parser (JSON, XML, CSV)
- **Datenbankverbindungen:** Verschiedene DB-Systeme
- **Plugin-Systeme:** Dynamische Komponenten-Laden

---

## 3. Abstract Factory Pattern

### Definition & Zweck
Bietet eine **Familie verwandter Objekte** an, ohne deren **konkrete Klassen** zu spezifizieren.

### Kategorie
Creational

### Python-spezifische Besonderheiten

- **ABC-Modul:** `abstractmethod` für Schnittstellen-Definition
- **Produktfamilien:** Mehrere `@abstractmethod`-Methoden pro Factory
- **Komplexer als Factory Method:** Nutze es nur wenn wirklich **mehrere verwandte Produkte** nötig sind

### Code-Beispiel

```python
from abc import ABC, abstractmethod

# ===== ABSTRAKTE PRODUKTE =====
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class TextInput(ABC):
    @abstractmethod
    def render(self):
        pass

# ===== KONKRETE PRODUKTE (Windows) =====
class WindowsButton(Button):
    def render(self):
        return "Rendering Windows Button with native look"

class WindowsTextInput(TextInput):
    def render(self):
        return "Rendering Windows TextInput with native look"

# ===== KONKRETE PRODUKTE (macOS) =====
class MacButton(Button):
    def render(self):
        return "Rendering Mac Button with Aqua look"

class MacTextInput(TextInput):
    def render(self):
        return "Rendering Mac TextInput with Aqua look"

# ===== ABSTRAKTE FACTORY =====
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_text_input(self) -> TextInput:
        pass

# ===== KONKRETE FACTORIES =====
class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_text_input(self) -> TextInput:
        return WindowsTextInput()

class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_text_input(self) -> TextInput:
        return MacTextInput()

# ===== VERWENDUNG =====
def render_dialog(factory: GUIFactory):
    """Client-Code: Kennt nur die abstrakte Factory"""
    button = factory.create_button()
    text_input = factory.create_text_input()

    print(button.render())
    print(text_input.render())

# Platform-Auswahl
import sys
if sys.platform == "win32":
    factory = WindowsFactory()
else:
    factory = MacFactory()

render_dialog(factory)
```

### Pythonische Alternative: Dictionary mit Factories

```python
# Einfacher und flexibler als Klasse-Hierarchie
class AbstractFactory:
    def __init__(self, product_map: dict):
        self.product_map = product_map

    def create(self, product_name: str):
        factory_func = self.product_map.get(product_name)
        if not factory_func:
            raise ValueError(f"Unknown product: {product_name}")
        return factory_func()

windows_factory = AbstractFactory({
    "button": WindowsButton,
    "input": WindowsTextInput,
})

button = windows_factory.create("button")  # WindowsButton-Instanz
```

### Use-Cases in Python

- **GUI-Frameworks:** Platform-spezifische UI-Komponenten (Windows, macOS, Linux)
- **Datenbankverbindungen:** Verschiedene DB-Systeme mit verwandten Objekten
- **Cross-Platform-Apps:** OS-spezifische Implementierungen
- **Theme-Systeme:** Light/Dark-Mode mit konsistenten Komponenten-Sätzen

---

## 4. Builder Pattern

### Definition & Zweck
Ermöglicht **schrittweise Konstruktion** komplexer Objekte ohne **monströse Konstruktoren**.

### Kategorie
Creational

### Python-spezifische Besonderheiten

- **Optional Parameter:** Python hat bereits default-Argumente — aber Builder macht komplexe Objekte lesbarer
- **Method Chaining:** Rückgabe von `self` für Fluent Interface
- **Dataclasses:** Alternative zu Builder für simple Objekte
- **Nested Builder:** Oft als innere Klasse implementiert

### Code-Beispiel (Mit Method Chaining)

```python
class DatabaseConnection:
    """Komplexes Objekt mit vielen optionalen Parametern"""

    def __init__(self):
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.database = None
        self.timeout = 30
        self.pool_size = 5
        self.ssl_enabled = False
        self.connection = None

    def connect(self):
        return f"Connected to {self.host}:{self.port}/{self.database}"

class DatabaseConnectionBuilder:
    """Builder für schrittweise Objektkonstruktion"""

    def __init__(self):
        self.connection = DatabaseConnection()

    def set_host(self, host: str):
        self.connection.host = host
        return self  # Fluent Interface

    def set_port(self, port: int):
        self.connection.port = port
        return self

    def set_credentials(self, username: str, password: str):
        self.connection.username = username
        self.connection.password = password
        return self

    def set_database(self, database: str):
        self.connection.database = database
        return self

    def set_timeout(self, timeout: int):
        self.connection.timeout = timeout
        return self

    def set_pool_size(self, size: int):
        self.connection.pool_size = size
        return self

    def enable_ssl(self, enabled: bool = True):
        self.connection.ssl_enabled = enabled
        return self

    def build(self) -> DatabaseConnection:
        """Finale Validierung und Rückgabe"""
        if not self.connection.host:
            raise ValueError("Host muss gesetzt sein")
        if not self.connection.port:
            raise ValueError("Port muss gesetzt sein")
        return self.connection

# ===== VERWENDUNG =====
# Lesbar und wartbar
connection = (DatabaseConnectionBuilder()
    .set_host("localhost")
    .set_port(5432)
    .set_credentials("admin", "secret")
    .set_database("myapp")
    .set_timeout(60)
    .enable_ssl()
    .build())

print(connection.connect())  # Connected to localhost:5432/myapp
```

### Pythonische Alternative: Dataclass mit Post-Init

```python
from dataclasses import dataclass

@dataclass
class DatabaseConnection:
    host: str
    port: int
    username: str
    password: str
    database: str
    timeout: int = 30
    pool_size: int = 5
    ssl_enabled: bool = False

    def __post_init__(self):
        # Validierung nach Initialisierung
        if not self.host or not self.port:
            raise ValueError("Host und Port erforderlich")

    def connect(self):
        return f"Connected to {self.host}:{self.port}/{self.database}"

# Verwendung mit Named Arguments
connection = DatabaseConnection(
    host="localhost",
    port=5432,
    username="admin",
    password="secret",
    database="myapp",
    timeout=60,
    ssl_enabled=True
)
```

### Use-Cases in Python

- **SQL Query Builder:** Komplexe Abfragen schrittweise aufbauen
- **HTTP Request Builder:** API-Requests mit vielen optionalen Parametern
- **Konfiguration:** Komplexe App-Settings
- **Document/Report Builder:** PDFs, Word-Dokumente mit vielen Elementen

---

## 5. Prototype Pattern

### Definition & Zweck
**Klone** ein Objekt, statt es von Grund auf neu zu erstellen.

### Kategorie
Creational

### Python-spezifische Besonderheiten

- **`copy`-Modul:** `copy.copy()` (shallow) vs `copy.deepcopy()` (deep)
- **`__copy__()` und `__deepcopy__()`:** Benutzerdefiniertes Cloning
- **Shallow vs Deep Copy:** Wichtig für nested Strukturen
- **Performance:** Oft schneller als Konstruktor bei großen Objekten

### Code-Beispiel

```python
import copy
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstrakte Klasse mit Prototype-Support"""

    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def display(self):
        pass

class Circle(Shape):
    def __init__(self, x: int, y: int, radius: int, color: str = "red"):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def clone(self):
        """Shallow Copy"""
        return copy.copy(self)

    def display(self):
        return f"Circle at ({self.x}, {self.y}), radius={self.radius}, color={self.color}"

class ComplexShape(Shape):
    def __init__(self, name: str):
        self.name = name
        self.points = []  # Mutable-Liste
        self.metadata = {}  # Mutable-Dict

    def clone(self):
        """Deep Copy für nested Strukturen"""
        return copy.deepcopy(self)

    def add_point(self, point):
        self.points.append(point)

    def display(self):
        return f"{self.name} with {len(self.points)} points"

# ===== VERWENDUNG =====
# Original erstellen
original_circle = Circle(10, 20, 5, "blue")
print(original_circle.display())  # Circle at (10, 20), radius=5, color=blue

# Klone erstellen
cloned_circle1 = original_circle.clone()
cloned_circle2 = original_circle.clone()

# Änderung im Klon beeinflußt Original nicht
cloned_circle1.color = "green"
print(original_circle.display())  # Farbe bleibt blau
print(cloned_circle1.display())   # Neue Farbe ist grün

# ===== DEEP COPY BEISPIEL =====
shape = ComplexShape("Polygon")
shape.add_point((0, 0))
shape.add_point((1, 1))

cloned_shape = shape.clone()
cloned_shape.points.append((2, 2))  # Klon-Punkte ändern

print(f"Original: {len(shape.points)} points")  # 2 points
print(f"Clone: {len(cloned_shape.points)} points")  # 3 points
```

### Use-Cases in Python

- **Grafik-Editor:** Objekte klonen und verschieben
- **Spielentwicklung:** Gegner/Objekte schnell duplizieren
- **Daten-Pipeline:** Ursprüngliche Daten bewahren, Varianten erstellen
- **Cache-Systeme:** Snapshot von Objektzustand speichern

---

# II. STRUCTURAL PATTERNS

Structural Patterns beschäftigen sich mit **Komposition von Objekten** und **Schnittstellen-Kompatibilität**.

---

## 6. Adapter Pattern (Wrapper)

### Definition & Zweck
Konvertiert die **Schnittstelle einer Klasse** in eine andere **Schnittstelle**, die Clients **erwarten**.

### Kategorie
Structural

### Python-spezifische Besonderheiten

- **Ähnlich zu Wrapper:** Oft einfach eine Wrapper-Klasse
- **Duck Typing:** Python braucht keine explizite Schnittstelle
- **Protocol (3.8+):** `typing.Protocol` für strukturelle Subtyping
- **Delegation:** Häufig nur Weitergabe an inneres Objekt

### Code-Beispiel (Klassen-Adapter)

```python
# ===== INKOMPATIBLE SCHNITTSTELLE (Legacy-Code) =====
class OldPaymentProcessor:
    """Alte API - unerwünschte Schnittstelle"""
    def process_payment_old_style(self, amount: float) -> bool:
        print(f"Processing payment (old style): ${amount}")
        return True

# ===== NEUE/ERWARTETE SCHNITTSTELLE =====
class ModernPaymentProcessor:
    """Neue API - was der Client erwartet"""
    def process(self, amount: float) -> dict:
        raise NotImplementedError

# ===== ADAPTER =====
class PaymentAdapter(ModernPaymentProcessor):
    """Adapter: Alte API in neue API übersetzen"""

    def __init__(self, old_processor: OldPaymentProcessor):
        self.old_processor = old_processor

    def process(self, amount: float) -> dict:
        # Delegation an alte Methode
        success = self.old_processor.process_payment_old_style(amount)

        # Antwort in neue Format übersetzen
        return {
            "status": "success" if success else "failed",
            "amount": amount,
            "timestamp": "2026-03-06T10:00:00"
        }

# ===== VERWENDUNG =====
old_processor = OldPaymentProcessor()
adapter = PaymentAdapter(old_processor)

# Client nutzt nur neue Schnittstelle
result = adapter.process(99.99)
print(result)  # {'status': 'success', 'amount': 99.99, 'timestamp': '2026-03-06T10:00:00'}
```

### Objekt-Adapter (Delegation)

```python
class PaymentObjectAdapter:
    """Adapter durch Komposition (flexibler)"""

    def __init__(self, old_processor: OldPaymentProcessor):
        self.old_processor = old_processor

    def process(self, amount: float) -> dict:
        result = self.old_processor.process_payment_old_style(amount)
        return {"status": "success" if result else "failed", "amount": amount}

adapter = PaymentObjectAdapter(OldPaymentProcessor())
print(adapter.process(50.0))
```

### Use-Cases in Python

- **Legacy-Integration:** Alte APIs mit neuen kombinieren
- **Third-Party-Libraries:** Externe Bibliotheken adapten
- **API-Versioning:** Alte API-Version im neuen Code verwenden
- **Format-Konvertierung:** Verschiedene Datenformate zwischen Systemen

---

## 7. Bridge Pattern

### Definition & Zweck
**Entkoppelt** eine **Abstraktion** von ihrer **Implementierung**, damit beide **unabhängig varieren** können.

### Kategorie
Structural

### Python-spezifische Besonderheiten

- **Komposition statt Vererbung:** Interface + Implementierung als separate Objekte
- **Vermeidet Kombinationsexplosion:** Statt N Abstraktionen × M Implementierungen = N+M Klassen
- **Strategisches Design:** Ähnlich zu Strategy, aber für Struktur-Hierarchien

### Code-Beispiel

```python
from abc import ABC, abstractmethod

# ===== IMPLEMENTIERUNGS-SEITE =====
class DrawingAPI(ABC):
    """Abstrakte Implementierungs-Schnittstelle"""
    @abstractmethod
    def draw_circle(self, x: int, y: int, radius: int):
        pass

class WindowsDrawingAPI(DrawingAPI):
    def draw_circle(self, x: int, y: int, radius: int):
        return f"Windows: Drawing circle at ({x}, {y}), radius {radius}"

class LinuxDrawingAPI(DrawingAPI):
    def draw_circle(self, x: int, y: int, radius: int):
        return f"X11: Drawing circle at ({x}, {y}), radius {radius}"

# ===== ABSTRAKTIONS-SEITE =====
class Shape(ABC):
    """Abstraktion mit Reference zu Implementierung (Bridge)"""

    def __init__(self, drawing_api: DrawingAPI):
        self.drawing_api = drawing_api

    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def __init__(self, drawing_api: DrawingAPI, x: int, y: int, radius: int):
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        return self.drawing_api.draw_circle(self.x, self.y, self.radius)

# ===== VERWENDUNG =====
# Abstraktion und Implementierung können unabhängig variieren
windows_api = WindowsDrawingAPI()
linux_api = LinuxDrawingAPI()

circle1 = Circle(windows_api, 10, 20, 5)
circle2 = Circle(linux_api, 10, 20, 5)

print(circle1.draw())  # Windows: Drawing circle at (10, 20), radius 5
print(circle2.draw())  # X11: Drawing circle at (10, 20), radius 5

# Nachträgliche Implementierungs-Änderung (ohne Shape zu ändern)
circle1.drawing_api = linux_api
print(circle1.draw())  # X11: Drawing circle at (10, 20), radius 5
```

### Use-Cases in Python

- **GUI-Frameworks:** Abstraktion (Button, Input) × Implementierung (Windows, macOS, Linux)
- **Datenbankanbindung:** Abstraktion (ORM) × Implementierung (PostgreSQL, MySQL, SQLite)
- **Rendering-Engines:** Abstraktion (Scene) × Implementierung (OpenGL, Vulkan, DirectX)
- **Geräte-Treiber:** Abstraktion (Device) × Implementierung (USB, Serial, Network)

---

## 8. Composite Pattern

### Definition & Zweck
Komponiere Objekte in **Baumstrukturen**, um **Teil-Ganzes-Hierarchien** zu repräsentieren.

### Kategorie
Structural

### Python-spezifische Besonderheiten

- **Rekursion:** Natürlich mit Python für Baum-Durchlauf
- **`__iter__()` und `__len__()`:** Für Container-ähnliches Verhalten
- **Type Hints:** `Union[Leaf, Composite]` oder `Sequence`
- **Pattern: `__enter__()/__exit__()`:** Für Context-Manager-basierte Traversal

### Code-Beispiel

```python
from abc import ABC, abstractmethod
from typing import List

# ===== KOMPONENTEN-SCHNITTSTELLE =====
class FileSystemComponent(ABC):
    """Abstrakte Komponente: Blatt und Composite teilen diese Schnittstelle"""

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: int = 0):
        pass

# ===== BLATT (Leaf) =====
class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size

    def display(self, indent: int = 0):
        print("  " * indent + f"📄 {self.name} ({self.size} bytes)")

# ===== COMPOSITE (Behälter) =====
class Directory(FileSystemComponent):
    def __init__(self, name: str):
        self.name = name
        self.children: List[FileSystemComponent] = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)

    def remove(self, component: FileSystemComponent):
        self.children.remove(component)

    def get_size(self) -> int:
        # Rekursive Größen-Berechnung
        total = 0
        for child in self.children:
            total += child.get_size()
        return total

    def display(self, indent: int = 0):
        print("  " * indent + f"📁 {self.name}/")
        for child in self.children:
            child.display(indent + 1)

# ===== VERWENDUNG =====
# Baumstruktur aufbauen
root = Directory("My Project")

src_dir = Directory("src")
src_dir.add(File("main.py", 2048))
src_dir.add(File("utils.py", 1024))

tests_dir = Directory("tests")
tests_dir.add(File("test_main.py", 1536))

root.add(src_dir)
root.add(tests_dir)
root.add(File("README.md", 512))

# Einheitliche Schnittstelle für Blatt und Composite
root.display()
print(f"\nTotal size: {root.get_size()} bytes")
```

### Use-Cases in Python

- **Dateibaum:** OS-Dateisystem Struktur
- **GUI-Komponenten:** Widget-Hierarchie (Frame > Panel > Button)
- **Organisationsstruktur:** Abteilung > Team > Person
- **DOM-Bäume:** HTML/XML-Parsing

---

## 9. Decorator Pattern (Strukturell, nicht Python-Decorator!)

### Definition & Zweck
**Füge Verantwortung zu Objekten hinzu** dynamisch, ohne **Subklassen zu erzeugen**.

### Kategorie
Structural

### Hinweis
Dies ist das **strukturelle Decorator Pattern** (nicht der `@decorator` Python-Syntax, der für Funktionen verwendet wird).

### Python-spezifische Besonderheiten

- **Confusion mit `@decorator`:** Python-Dekorierer sind eine Spezialform (siehe Behavioral Patterns)
- **Struktur-Decorator:** Klassen-basiert, wraps Objekte zur Laufzeit
- **Alternative:** Python `@property` und `@functools.wraps` für einfachere Fälle

### Code-Beispiel

```python
from abc import ABC, abstractmethod

# ===== KOMPONENTEN-SCHNITTSTELLE =====
class Coffee(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

# ===== KONKRETE KOMPONENTE =====
class SimpleCoffee(Coffee):
    def get_cost(self) -> float:
        return 2.0

    def get_description(self) -> str:
        return "Simple Coffee"

# ===== DEKORATOR-BASISKLASSE =====
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self.coffee = coffee

    def get_cost(self) -> float:
        return self.coffee.get_cost()

    def get_description(self) -> str:
        return self.coffee.get_description()

# ===== KONKRETE DEKORATOREN =====
class WithMilk(CoffeeDecorator):
    def get_cost(self) -> float:
        return self.coffee.get_cost() + 0.5

    def get_description(self) -> str:
        return self.coffee.get_description() + ", with Milk"

class WithWhippedCream(CoffeeDecorator):
    def get_cost(self) -> float:
        return self.coffee.get_cost() + 0.7

    def get_description(self) -> str:
        return self.coffee.get_description() + ", with Whipped Cream"

class WithCinnamon(CoffeeDecorator):
    def get_cost(self) -> float:
        return self.coffee.get_cost() + 0.2

    def get_description(self) -> str:
        return self.coffee.get_description() + ", with Cinnamon"

# ===== VERWENDUNG =====
coffee = SimpleCoffee()
print(f"{coffee.get_description()}: ${coffee.get_cost()}")  # Simple Coffee: $2.0

# Dekoratoren schichten (beliebig kombinierbar)
coffee = WithMilk(coffee)
coffee = WithCinnamon(coffee)
print(f"{coffee.get_description()}: ${coffee.get_cost()}")  # Simple Coffee, with Milk, with Cinnamon: $2.7

# Weitere Variante
coffee2 = WithWhippedCream(WithMilk(SimpleCoffee()))
print(f"{coffee2.get_description()}: ${coffee2.get_cost()}")  # Simple Coffee, with Milk, with Whipped Cream: $3.2
```

### Use-Cases in Python

- **Input/Output Streams:** `BufferedReader(GzipFile(FileStream))`
- **Authentifizierung:** `LoggingMiddleware(AuthMiddleware(Handler))`
- **UI-Styling:** Component mit dynamischen Styles
- **Logging/Monitoring:** Funktionalität wrappen ohne Code zu ändern

---

## 10. Facade Pattern

### Definition & Zweck
Biete eine **vereinheitlichte Schnittstelle** zu einem **komplexen Subsystem** an.

### Kategorie
Structural

### Python-spezifische Besonderheiten

- **Modul-Facade:** Oft als Module selbst (statt Klasse)
- **Weniger ist mehr:** Nur notwendige Methoden exponieren
- **Reduziert Coupling:** Clients kennen nur Facade, nicht die Details
- **Vorsicht:** Nicht zu viele Verantwortungen in eine Facade laden

### Code-Beispiel

```python
# ===== KOMPLEXES SUBSYSTEM =====
class AudioPlayer:
    def __init__(self):
        self.is_playing = False

    def play(self, file: str):
        self.is_playing = True
        return f"Playing audio: {file}"

    def stop(self):
        self.is_playing = False
        return "Stopping audio"

class SubtitleManager:
    def load_subtitles(self, language: str):
        return f"Loaded {language} subtitles"

    def display_subtitles(self, file: str):
        return f"Displaying subtitles for {file}"

class VideoDecoder:
    def decode(self, file: str):
        return f"Decoding video: {file}"

    def set_quality(self, quality: str):
        return f"Set quality to {quality}"

# ===== FACADE =====
class VideoPlayerFacade:
    """Vereinheitlichte Schnittstelle zu komplexem Video-System"""

    def __init__(self):
        self.audio_player = AudioPlayer()
        self.subtitle_manager = SubtitleManager()
        self.video_decoder = VideoDecoder()

    def play_movie(self, file: str, language: str = "en", quality: str = "HD"):
        """Einfache Methode, die komplexe Operationen koordiniert"""
        print(self.video_decoder.decode(file))
        print(self.video_decoder.set_quality(quality))
        print(self.subtitle_manager.load_subtitles(language))
        print(self.audio_player.play(file))
        return f"Playing movie: {file}"

    def stop_movie(self):
        """Alle Komponenten koordiniert stoppen"""
        return self.audio_player.stop()

# ===== VERWENDUNG =====
player = VideoPlayerFacade()
player.play_movie("inception.mp4", language="de", quality="4K")
# Client muss nicht wissen, dass 3 Subsysteme kooperieren
```

### Use-Cases in Python

- **Web-Frameworks:** Django/Flask Facade über komplexe ORM-Systeme
- **3D-Grafik:** Engines (OpenGL, Vulkan) mit einfacher API exponieren
- **Betriebssystem:** Komplexe Systemaufrufe hinter einfacher API
- **API-Clients:** Externe Service-Aufrufe vereinfachen

---

## 11. Flyweight Pattern

### Definition & Zweck
**Teile gemeinsame Daten** zwischen vielen ähnlichen Objekten, um **Speicher zu sparen**.

### Kategorie
Structural

### Python-spezifische Besonderheiten

- **Mutable vs Immutable:** Geteilte Daten müssen unveränderlich sein
- **Caching:** Oft mit `__new__()` oder Metaclass implementiert
- **`__slots__`:** Für speichereffiziente Objekte
- **Intern vs Extern:** Teile (intern), Kontext (extern)

### Code-Beispiel

```python
# ===== FLYWEIGHT (Geteilte Daten) =====
class TreeType:
    """Flyweight: Geteilte Daten zwischen vielen Tree-Objekten"""

    # Class-level Cache für Wiederverwendung
    _instances = {}

    def __new__(cls, name: str, color: str, texture: str):
        key = (name, color, texture)
        if key not in cls._instances:
            instance = super().__new__(cls)
            instance.name = name
            instance.color = color
            instance.texture = texture
            cls._instances[key] = instance
        return cls._instances[key]

    def __repr__(self):
        return f"TreeType({self.name}, {self.color}, {self.texture})"

# ===== KONTEXT-OBJEKT (Extrinsische Daten) =====
class Tree:
    """Einzelner Baum mit Position (extrinsische Daten)"""

    def __init__(self, x: int, y: int, tree_type: TreeType):
        self.x = x
        self.y = y
        self.tree_type = tree_type  # Shared Flyweight

    def display(self):
        return f"Tree at ({self.x}, {self.y}): {self.tree_type}"

# ===== FACTORY =====
class TreeFactory:
    """Factory zur Flyweight-Erstellung"""

    def __init__(self):
        self.tree_types = {}

    def get_tree_type(self, name: str, color: str, texture: str) -> TreeType:
        key = (name, color, texture)
        if key not in self.tree_types:
            self.tree_types[key] = TreeType(name, color, texture)
        return self.tree_types[key]

# ===== VERWENDUNG =====
factory = TreeFactory()

# 1 Million Bäume, aber nur 3 unique TreeType-Objekte (geteilt)
forest = []
for i in range(1_000_000):
    tree_type = factory.get_tree_type("Oak", "Green", "Oak_Bark")
    forest.append(Tree(i % 1000, i // 1000, tree_type))

print(f"Forest has {len(forest)} trees")
print(f"But only {len(factory.tree_types)} unique tree types")
print(f"Memory savings: ~90%")  # Statt 1M TreeType-Objekte nur 3

# Wenige Bäume anzeigen
for tree in forest[:3]:
    print(tree.display())
```

### Use-Cases in Python

- **Spieleentwicklung:** 1M Bäume/Gras mit gemeinsamen Texturen
- **Text-Editor:** Character-Glyphen teilen (nicht jedes Char kopieren)
- **Web-Browser:** DOM-Knoten mit gemeinsamen Styles
- **Datenbank-Connection-Pool:** Verbindungen wiederverwenden

---

## 12. Proxy Pattern

### Definition & Zweck
Biete einen **Platzhalter oder Stellvertreter** für ein anderes Objekt an, um **Zugriff zu kontrollieren**.

### Kategorie
Structural

### Python-spezifische Besonderheiten

- **Lazy Loading:** Teuer Objekt erst bei Bedarf erzeugen
- **`__getattr__()`:** Für transparente Delegation
- **Drei Proxy-Typen:** Virtual (lazy), Protection (Zugriff), Remote (Netzwerk)
- **Unterschied zu Decorator:** Proxy kontrolliert Zugriff, Decorator fügt Funktionalität hinzu

### Code-Beispiel (Virtual Proxy - Lazy Loading)

```python
from abc import ABC, abstractmethod

# ===== SCHNITTSTELLE =====
class Image(ABC):
    @abstractmethod
    def display(self):
        pass

# ===== ECHTES OBJEKT (Teuer zu erstellen) =====
class RealImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        print(f"Loading image from disk: {filename}")  # Kostspielige Operation
        # Simuliere Laden

    def display(self):
        return f"Displaying image: {self.filename}"

# ===== PROXY (Lazy Loading) =====
class ImageProxy(Image):
    """Virtual Proxy: Lädt echtes Bild nur wenn nötig"""

    def __init__(self, filename: str):
        self.filename = filename
        self.real_image = None  # Nicht sofort laden

    def display(self):
        # Lazy initialization
        if self.real_image is None:
            self.real_image = RealImage(self.filename)

        return self.real_image.display()

# ===== VERWENDUNG =====
# Proxy erzeugt RealImage NICHT sofort
image = ImageProxy("photo.jpg")
print("Image proxy created (no disk load yet)")

# Erst bei display() wird RealImage geladen
print(image.display())  # "Loading image from disk..." dann "Displaying image..."
```

### Protection Proxy (Zugriffs-Kontrolle)

```python
class User:
    def __init__(self, role: str):
        self.role = role

class SecureDocument:
    def __init__(self, content: str):
        self.content = content

    def read(self):
        return self.content

class SecureDocumentProxy(SecureDocument):
    """Protection Proxy: Kontrolliert Zugriff basierend auf Rolle"""

    def __init__(self, content: str, allowed_roles: list):
        super().__init__(content)
        self.allowed_roles = allowed_roles
        self.user = None

    def set_user(self, user: User):
        self.user = user

    def read(self):
        if not self.user:
            raise PermissionError("No user authenticated")

        if self.user.role not in self.allowed_roles:
            raise PermissionError(f"User role '{self.user.role}' not allowed")

        return super().read()

# Verwendung
admin = User("admin")
user = User("guest")

doc = SecureDocumentProxy("Secret information", allowed_roles=["admin"])
doc.set_user(admin)
print(doc.read())  # OK

doc.set_user(user)
try:
    print(doc.read())  # PermissionError
except PermissionError as e:
    print(f"Access denied: {e}")
```

### Use-Cases in Python

- **Lazy Loading:** Bilder/Daten erst laden wenn angezeigt
- **Zugriffskontrolle:** Benutzerrolle vor Datenzugriff prüfen
- **Remote Objects:** RPC-Calls über Netzwerk
- **Logging/Monitoring:** Methoden-Aufrufe protokollieren
- **Caching:** Häufig angeforderte Objekte cachen

---

# III. BEHAVIORAL PATTERNS

Behavioral Patterns beschäftigen sich mit **Objekt-Zusammenarbeit** und **Verantwortungs-Verteilung**.

---

## 13. Chain of Responsibility Pattern

### Definition & Zweck
Übergebe eine **Anfrage** durch eine **Kette von Handlern**, bis einer sie bearbeitet.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **Verkettete Handler:** `next` als Attribute
- **Optional Handler:** Handler können Request auch weitergeben
- **Exception-Handling:** Ähnlicher Konzept in Middleware
- **Logging/Debugging:** Gut für Event-Verarbeitung

### Code-Beispiel

```python
from abc import ABC, abstractmethod

# ===== ABSTRAKTE HANDLER =====
class SupportHandler(ABC):
    def __init__(self, name: str):
        self.name = name
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler  # Method Chaining

    def handle(self, request):
        if self._can_handle(request):
            return self._process(request)
        elif self.next_handler:
            return self.next_handler.handle(request)
        else:
            return f"Request unhandled: {request}"

    @abstractmethod
    def _can_handle(self, request):
        pass

    @abstractmethod
    def _process(self, request):
        pass

# ===== KONKRETE HANDLER =====
class Level1Support(SupportHandler):
    def _can_handle(self, request):
        return request.get("priority") == "low"

    def _process(self, request):
        return f"{self.name}: Handling low priority - {request.get('issue')}"

class Level2Support(SupportHandler):
    def _can_handle(self, request):
        return request.get("priority") == "medium"

    def _process(self, request):
        return f"{self.name}: Handling medium priority - {request.get('issue')}"

class Level3Support(SupportHandler):
    def _can_handle(self, request):
        return request.get("priority") == "high"

    def _process(self, request):
        return f"{self.name}: Handling high priority - {request.get('issue')}"

# ===== VERWENDUNG =====
# Kette aufbauen
level1 = Level1Support("L1")
level2 = Level2Support("L2")
level3 = Level3Support("L3")

level1.set_next(level2).set_next(level3)

# Requests durch Kette verarbeiten
requests = [
    {"priority": "low", "issue": "Password reset"},
    {"priority": "medium", "issue": "Email configuration"},
    {"priority": "high", "issue": "Database crash"},
    {"priority": "critical", "issue": "System down"},
]

for req in requests:
    print(level1.handle(req))
```

### Use-Cases in Python

- **Event-Handling:** GUI-Events durch Widget-Hierarchie
- **Logging-Level:** DEBUG > INFO > WARNING > ERROR
- **Request-Pipeline:** Web-Middleware (Auth > Validate > Process)
- **Approval-Workflow:** Manager > Director > CEO

---

## 14. Command Pattern

### Definition & Zweck
**Kapsele eine Anfrage** als **Objekt**, um **Operationen zu parametrisieren**, zu **queuen**, zu **loggen** und zu **undo** zu unterstützen.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **Callable Objects:** `__call__()` für Function-like behavior
- **Undo/Redo:** Kommandos mit `execute()` und `undo()`
- **Queueing:** Kommandos speichern und später ausführen
- **Befehlsmakros:** Mehrere Kommandos kombinieren

### Code-Beispiel

```python
from abc import ABC, abstractmethod
from typing import List

# ===== COMMAND SCHNITTSTELLE =====
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

# ===== RECEIVER (Das Objekt, das Arbeit verrichtet) =====
class Light:
    def __init__(self, location: str):
        self.location = location
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        return f"Light in {self.location} is ON"

    def turn_off(self):
        self.is_on = False
        return f"Light in {self.location} is OFF"

# ===== KONKRETE COMMANDS =====
class TurnOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        return self.light.turn_on()

    def undo(self):
        return self.light.turn_off()

class TurnOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        return self.light.turn_off()

    def undo(self):
        return self.light.turn_on()

# ===== INVOKER (Führt Kommandos aus) =====
class RemoteControl:
    def __init__(self):
        self.commands: List[Command] = []
        self.history: List[Command] = []

    def submit_command(self, command: Command):
        print(command.execute())
        self.history.append(command)

    def undo(self):
        if self.history:
            command = self.history.pop()
            print(command.undo())

# ===== VERWENDUNG =====
light = Light("Living Room")
remote = RemoteControl()

remote.submit_command(TurnOnCommand(light))   # Light on
remote.submit_command(TurnOffCommand(light))  # Light off
remote.submit_command(TurnOnCommand(light))   # Light on again

remote.undo()  # Undo: Light off
remote.undo()  # Undo: Light on
```

### Makro-Kommandos (Mehrere Commands kombinieren)

```python
class MacroCommand(Command):
    """Composite Command: Mehrere Kommandos kombinieren"""

    def __init__(self, commands: List[Command]):
        self.commands = commands

    def execute(self):
        results = []
        for command in self.commands:
            results.append(command.execute())
        return results

    def undo(self):
        for command in reversed(self.commands):
            command.undo()

# Beispiel: "Gute Nacht" Makro
night_commands = [
    TurnOffCommand(light),
    TurnOffCommand(light),  # Mehrere Lichter
]
macro = MacroCommand(night_commands)
remote.submit_command(macro)  # Ein Kommando für alles
```

### Use-Cases in Python

- **Undo/Redo:** Text-Editor, Grafik-Programme
- **Queueing:** Task-Queue, Job-Scheduler
- **Logging:** Aktionen protokollieren
- **Transaktionen:** Datenbankoperationen
- **Remote-Execution:** Befehle über Netzwerk senden

---

## 15. Iterator Pattern

### Definition & Zweck
Biete eine Möglichkeit, auf **Elemente einer Sammlung zuzugreifen**, ohne deren **innere Struktur freizulegen**.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **`__iter__()` und `__next__()`:** Python Protocol für Iteration
- **`for`-Schleife:** Funktioniert mit jedem iterable
- **`itertools`:** Mächtige Iterator-Tools
- **Generators:** `yield` für lazy Iteration

### Code-Beispiel (Expliziter Iterator)

```python
from abc import ABC, abstractmethod

# ===== SAMMLUNG =====
class BookCollection:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def __iter__(self):
        return BookIterator(self.books)

# ===== ITERATOR (Explizit) =====
class BookIterator:
    def __init__(self, books):
        self.books = books
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.books):
            result = self.books[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

# ===== VERWENDUNG =====
collection = BookCollection()
collection.add_book("Python Mastery")
collection.add_book("Design Patterns")
collection.add_book("Clean Code")

for book in collection:  # Nutzt __iter__() automatisch
    print(f"Reading: {book}")
```

### Generator-basiert (Pythonic)

```python
# Einfacher mit Generator
class BookCollectionGenerator:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def __iter__(self):
        for book in self.books:
            yield book  # Lazy Iteration

# Verwendung (identisch)
collection = BookCollectionGenerator()
collection.add_book("Python Mastery")

for book in collection:
    print(f"Reading: {book}")
```

### Use-Cases in Python

- **Collections:** `list`, `dict`, `set` Iteration
- **Datei-Verarbeitung:** Zeile-weise Datei lesen
- **Datenbank-Resultate:** Row-by-Row Iteration
- **API-Pagination:** Seite-weise Daten abrufen
- **Bäume/Graphen:** DFS/BFS Traversal

---

## 16. Mediator Pattern

### Definition & Zweck
**Definiere ein Objekt**, das **Kommunikation zwischen Objekten** kontrolliert und **Kopplung reduziert**.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **Zentrale Koordination:** Statt Punkt-zu-Punkt Kommunikation
- **Observer-ähnlich:** Oft mit Event-System implementiert
- **Zustand-Management:** Komplexe Logik in Mediator konzentrieren

### Code-Beispiel

```python
from abc import ABC, abstractmethod

# ===== MEDIATOR =====
class ChatRoomMediator(ABC):
    @abstractmethod
    def register_user(self, user):
        pass

    @abstractmethod
    def send_message(self, message: str, sender):
        pass

# ===== KONKRETE MEDIATOR =====
class ChatRoom(ChatRoomMediator):
    def __init__(self, name: str):
        self.name = name
        self.users = []

    def register_user(self, user):
        self.users.append(user)
        user.chat_room = self
        print(f"{user.name} joined {self.name}")

    def send_message(self, message: str, sender):
        print(f"\n[{self.name}] {sender.name}: {message}")

        # Nachricht an alle anderen User (ohne Sender)
        for user in self.users:
            if user != sender:
                user.receive_message(message, sender.name)

# ===== COLLEAGUES (Benutzer) =====
class User:
    def __init__(self, name: str):
        self.name = name
        self.chat_room = None

    def send(self, message: str):
        if self.chat_room:
            self.chat_room.send_message(message, self)

    def receive_message(self, message: str, from_user: str):
        print(f"  {self.name} received: {from_user} said '{message}'")

# ===== VERWENDUNG =====
chat_room = ChatRoom("Python Developers")

alice = User("Alice")
bob = User("Bob")
charlie = User("Charlie")

chat_room.register_user(alice)
chat_room.register_user(bob)
chat_room.register_user(charlie)

alice.send("Hello everyone!")
bob.send("Hi Alice!")
```

### Use-Cases in Python

- **GUI-Dialoge:** Komponenten-Kommunikation
- **Air Traffic Control:** Flugzeug-Koordination
- **Chat-Systeme:** User-zu-User Messaging
- **Event-Bus:** Lose Kopplung von Event-Handlern

---

## 17. Memento Pattern

### Definition & Zweck
**Erfasse einen Objektzustand**, ohne seine **Kapselung zu verletzen**, und **restauriere ihn später**.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **Snapshot speichern:** State vor Änderungen
- **Undo-Funktionalität:** Zu früheren States zurück
- **Caretaker:** Verwaltet Snapshots
- **Performance:** Große Objekte können teuer sein

### Code-Beispiel

```python
from typing import List
from copy import deepcopy

# ===== ORIGINATOR (Das Objekt mit Zustand) =====
class TextDocument:
    def __init__(self, content: str = ""):
        self.content = content

    def add_text(self, text: str):
        self.content += text

    def create_snapshot(self):
        """Memento erstellen"""
        return DocumentSnapshot(self.content)

    def restore_snapshot(self, snapshot):
        """Aus Memento restaurieren"""
        self.content = snapshot.get_state()

    def display(self):
        print(f"Content: {self.content}")

# ===== MEMENTO (Snapshot des Zustands) =====
class DocumentSnapshot:
    def __init__(self, content: str):
        self._content = content  # Private

    def get_state(self) -> str:
        return self._content

# ===== CARETAKER (Verwaltet Snapshots) =====
class DocumentHistory:
    def __init__(self):
        self.history: List[DocumentSnapshot] = []

    def save(self, document: TextDocument):
        """Snapshot speichern"""
        self.history.append(document.create_snapshot())
        print(f"Saved snapshot. History size: {len(self.history)}")

    def undo(self, document: TextDocument):
        """Letzten Snapshot wiederherstellen"""
        if self.history:
            snapshot = self.history.pop()
            document.restore_snapshot(snapshot)
            print("Restored from snapshot")
        else:
            print("No history")

# ===== VERWENDUNG =====
doc = TextDocument()
history = DocumentHistory()

doc.add_text("Hello ")
history.save(doc)
doc.display()  # Content: Hello

doc.add_text("World")
history.save(doc)
doc.display()  # Content: Hello World

doc.add_text("!!!")
doc.display()  # Content: Hello World!!!

history.undo(doc)
doc.display()  # Content: Hello World (undo)

history.undo(doc)
doc.display()  # Content: Hello (undo)
```

### Use-Cases in Python

- **Text-Editor:** Undo-Stack
- **Spieleentwicklung:** Game State Snapshots
- **Versionskontrollen:** Commit History
- **Transaktionen:** Rollback auf vorherigen State
- **Browser:** History Navigation

---

## 18. Observer Pattern

### Definition & Zweck
**Definiere eine 1-zu-n Abhängigkeit**, damit bei Zustandsänderung eines Objekts **alle abhängigen Objekte benachrichtigt** werden.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **Event-Systeme:** Observer ist Basis von Event-Handling
- **Signals/Slots:** PyQt/PySide nutzen Observer-ähnlich
- **Listener-Pattern:** Oft implementiert als Callback-Funktionen
- **Weak References:** `weakref` um Memory Leaks zu vermeiden

### Code-Beispiel (Klassisch)

```python
from abc import ABC, abstractmethod
from typing import List

# ===== SUBJECT =====
class Stock:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self._price = price
        self._observers: List['Observer'] = []

    def attach(self, observer: 'Observer'):
        """Observer registrieren"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer'):
        """Observer abmelden"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        """Alle Observer benachrichtigen"""
        for observer in self._observers:
            observer.update(self)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value: float):
        if value != self._price:
            self._price = value
            self.notify()  # Auto-notify bei Änderung

# ===== OBSERVER =====
class Observer(ABC):
    @abstractmethod
    def update(self, subject: Stock):
        pass

class StockDisplay(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, subject: Stock):
        print(f"{self.name}: {subject.symbol} price changed to ${subject.price}")

class PortfolioManager(Observer):
    def __init__(self):
        self.portfolio_value = 0

    def update(self, subject: Stock):
        self.portfolio_value += subject.price
        print(f"Portfolio updated. New value: ${self.portfolio_value}")

# ===== VERWENDUNG =====
apple_stock = Stock("AAPL", 150.0)

display1 = StockDisplay("Display 1")
display2 = StockDisplay("Display 2")
manager = PortfolioManager()

apple_stock.attach(display1)
apple_stock.attach(display2)
apple_stock.attach(manager)

apple_stock.price = 155.0  # Alle Observer werden benachrichtigt
apple_stock.price = 160.0

apple_stock.detach(display2)
apple_stock.price = 165.0  # display2 wird NICHT benachrichtigt
```

### Pythonische Alternative: Callback-basiert

```python
class StockSimple:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self._price = price
        self._callbacks = []

    def on_price_change(self, callback):
        """Callback registrieren"""
        self._callbacks.append(callback)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value: float):
        self._price = value
        for callback in self._callbacks:
            callback(self.symbol, value)

# Verwendung mit Lambda
stock = StockSimple("AAPL", 150.0)
stock.on_price_change(lambda symbol, price: print(f"{symbol}: ${price}"))
stock.price = 155.0  # Callback wird aufgerufen
```

### Use-Cases in Python

- **GUI-Events:** Button-Click → Multiple Handler
- **Model-View:** Datenänderung → View Update
- **Event-Bus:** Publish-Subscribe Systeme
- **Listener-Pattern:** File-Watcher, Timer-Events
- **Reactive Programming:** RxPy streams

---

## 19. State Pattern

### Definition & Zweck
Erlaube einem Objekt, sein **Verhalten zu ändern**, wenn sich sein **innerer Zustand ändert**.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **State-Machine:** Zustandsübergänge modellieren
- **Strategy vs State:** State hat Zustandsübergänge, Strategy nicht
- **Context-Objekt:** Hält aktuellen State
- **Übergangs-Logik:** Im State oder Context

### Code-Beispiel

```python
from abc import ABC, abstractmethod

# ===== STATE SCHNITTSTELLE =====
class State(ABC):
    @abstractmethod
    def insert_money(self, context, amount: int):
        pass

    @abstractmethod
    def select_item(self, context, item: str):
        pass

    @abstractmethod
    def dispense(self, context):
        pass

# ===== KONKRETE STATES =====
class IdleState(State):
    def insert_money(self, context, amount: int):
        context.balance += amount
        print(f"Money inserted: ${amount}. Balance: ${context.balance}")
        context.set_state(MoneyInsertedState())

    def select_item(self, context, item: str):
        print("Please insert money first")

    def dispense(self, context):
        print("Nothing to dispense")

class MoneyInsertedState(State):
    def insert_money(self, context, amount: int):
        context.balance += amount
        print(f"More money inserted: ${amount}. Balance: ${context.balance}")

    def select_item(self, context, item: str):
        if item in context.inventory and context.inventory[item] > 0:
            price = context.prices.get(item, 0)
            if context.balance >= price:
                context.selected_item = item
                context.set_state(DispenseState())
                context.dispense_item()
            else:
                print(f"Insufficient balance. Need ${price}, have ${context.balance}")
        else:
            print(f"Item not available: {item}")

    def dispense(self, context):
        print("Select an item first")

class DispenseState(State):
    def insert_money(self, context, amount: int):
        context.balance += amount
        print(f"Money inserted: ${amount}. Balance: ${context.balance}")

    def select_item(self, context, item: str):
        print("Already dispensing")

    def dispense(self, context):
        item = context.selected_item
        price = context.prices[item]
        context.balance -= price
        context.inventory[item] -= 1
        print(f"Dispensing {item}... Remaining balance: ${context.balance}")

        if context.balance > 0:
            context.set_state(MoneyInsertedState())
        else:
            context.set_state(IdleState())

# ===== CONTEXT =====
class VendingMachine:
    def __init__(self):
        self.balance = 0
        self.selected_item = None
        self._state = IdleState()
        self.inventory = {"soda": 10, "chips": 5, "candy": 8}
        self.prices = {"soda": 2, "chips": 1, "candy": 1}

    def set_state(self, state: State):
        self._state = state

    def insert_money(self, amount: int):
        self._state.insert_money(self, amount)

    def select_item(self, item: str):
        self._state.select_item(self, item)

    def dispense_item(self):
        self._state.dispense(self)

# ===== VERWENDUNG =====
machine = VendingMachine()

machine.select_item("soda")  # "Please insert money first"
machine.insert_money(2)      # Money inserted, switches to MoneyInsertedState
machine.select_item("soda")  # Soda dispensed
machine.select_item("chips") # Select another item (balance = 0)

machine.insert_money(1)
machine.select_item("chips")
```

### Use-Cases in Python

- **State Machines:** Workflow, Game States
- **TCP-Verbindungen:** Connected/Disconnected States
- **UI-Dialoge:** Modal/Non-Modal States
- **Media Player:** Playing/Paused/Stopped States
- **Workflow-Engine:** Approval States

---

## 20. Strategy Pattern

### Definition & Zweck
**Definiere eine Familie von Algorithmen**, **kapsele jeden**, und mache sie **austauschbar**.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **Funktionen als Strategy:** `lambda` oder Funktions-Referenzen
- **Policy-Pattern:** Strategie als Parameter
- **Keine Zustandsänderung:** Im Gegensatz zu State Pattern
- **Multiple Algorithmen:** Zur Laufzeit wählbar

### Code-Beispiel (Klassen-basiert)

```python
from abc import ABC, abstractmethod

# ===== STRATEGY SCHNITTSTELLE =====
class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass

# ===== KONKRETE STRATEGIES =====
class BubbleSortStrategy(SortingStrategy):
    def sort(self, data: list) -> list:
        data = data.copy()
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data

class QuickSortStrategy(SortingStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class MergeSortStrategy(SortingStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

# ===== CONTEXT =====
class Sorter:
    def __init__(self, strategy: SortingStrategy):
        self.strategy = strategy

    def sort(self, data: list) -> list:
        return self.strategy.sort(data)

    def set_strategy(self, strategy: SortingStrategy):
        self.strategy = strategy

# ===== VERWENDUNG =====
data = [64, 34, 25, 12, 22, 11, 90]

# Verschiedene Algorithmen testen
bubble = Sorter(BubbleSortStrategy())
quick = Sorter(QuickSortStrategy())
merge = Sorter(MergeSortStrategy())

print(f"Original: {data}")
print(f"Bubble: {bubble.sort(data)}")
print(f"Quick: {quick.sort(data)}")
print(f"Merge: {merge.sort(data)}")

# Strategy zur Laufzeit wechseln
sorter = Sorter(BubbleSortStrategy())
sorter.sort(data)

sorter.set_strategy(QuickSortStrategy())
sorter.sort(data)
```

### Pythonische Alternative: Funktionen

```python
def bubble_sort(data):
    # Implementation
    pass

def quick_sort(data):
    # Implementation
    pass

class SorterFunc:
    def __init__(self, strategy_func):
        self.strategy_func = strategy_func

    def sort(self, data):
        return self.strategy_func(data)

# Verwendung
sorter = SorterFunc(quick_sort)
result = sorter.sort([64, 34, 25])
```

### Use-Cases in Python

- **Zahlungs-Verarbeitung:** Verschiedene Payment-Methoden
- **Kompressions-Algorithmen:** gzip vs bzip2 vs lz4
- **Validierungs-Strategien:** Email vs Phone vs Credit Card
- **Sortierungs-Algorithmen:** Abhängig von Daten-Größe
- **Rendering:** CPU vs GPU vs Hybrid

---

## 21. Template Method Pattern

### Definition & Zweck
**Definiere das Skelett eines Algorithmus**, lass **Subklassen Schritte implementieren**.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **Abstract Base Classes:** `abstractmethod` für zu implementierende Schritte
- **Hook Methods:** Optionale Schritte mit Default-Implementation
- **Inverse of Control:** Subklasse definiert Details, Base bestimmt Reihenfolge

### Code-Beispiel

```python
from abc import ABC, abstractmethod

# ===== TEMPLATE METHOD =====
class DataProcessor(ABC):
    """Template Method: Algorithmus-Skelett"""

    def process_data(self, data):
        """Template Method: definiert Algorithmus-Struktur"""
        print("=== Data Processing Started ===")

        self.validate(data)
        cleaned_data = self.clean(data)
        transformed_data = self.transform(cleaned_data)
        self.save(transformed_data)

        print("=== Data Processing Completed ===")

    @abstractmethod
    def validate(self, data):
        """Subklasse muss implementieren"""
        pass

    @abstractmethod
    def clean(self, data):
        """Subklasse muss implementieren"""
        pass

    @abstractmethod
    def transform(self, data):
        """Subklasse muss implementieren"""
        pass

    def save(self, data):
        """Hook: Optional zu überschreiben"""
        print(f"Default save: {data}")

# ===== KONKRETE IMPLEMENTIERUNGEN =====
class CSVDataProcessor(DataProcessor):
    def validate(self, data):
        print("Validating CSV data...")
        if not data:
            raise ValueError("Data is empty")

    def clean(self, data):
        print("Cleaning CSV data...")
        return [row.strip() for row in data]

    def transform(self, data):
        print("Transforming CSV to JSON...")
        return [{"row": i, "value": row} for i, row in enumerate(data)]

    def save(self, data):
        print(f"Saving to CSV file: {data}")

class JSONDataProcessor(DataProcessor):
    def validate(self, data):
        print("Validating JSON data...")
        if not isinstance(data, dict):
            raise ValueError("Data must be dict")

    def clean(self, data):
        print("Cleaning JSON data...")
        return {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}

    def transform(self, data):
        print("Transforming JSON structure...")
        return {"processed": data}

    def save(self, data):
        print(f"Saving to JSON file: {data}")

# ===== VERWENDUNG =====
csv_processor = CSVDataProcessor()
csv_processor.process_data(["row1", "row2", "row3"])

print()

json_processor = JSONDataProcessor()
json_processor.process_data({"name": "John", "age": "30"})
```

### Use-Cases in Python

- **Data Pipelines:** ETL-Prozesse
- **Framework-Hooks:** Django/Flask Request Processing
- **Test-Runner:** Setup → Test → Teardown
- **Reporting:** Header → Data → Footer
- **Web Scraper:** Fetch → Parse → Extract → Save

---

## 22. Visitor Pattern

### Definition & Zweck
**Repräsentiere eine Operation** auf Elementen einer Objekt-Struktur, ohne die **Klassen zu ändern**.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **Double Dispatch:** Visitor + Element
- **Kompatibilität:** Element-Klassen müssen `accept()` implementieren
- **Complex:** Komplex wenn viele Element-Typen
- **Alternative:** Sometimes simpler mit `isinstance()` checks

### Code-Beispiel

```python
from abc import ABC, abstractmethod

# ===== ELEMENT SCHNITTSTELLE =====
class Element(ABC):
    @abstractmethod
    def accept(self, visitor: 'Visitor'):
        pass

# ===== KONKRETE ELEMENTE =====
class Salary(Element):
    def __init__(self, amount: float):
        self.amount = amount

    def accept(self, visitor: 'Visitor'):
        return visitor.visit_salary(self)

class Bonus(Element):
    def __init__(self, amount: float):
        self.amount = amount

    def accept(self, visitor: 'Visitor'):
        return visitor.visit_bonus(self)

class Deduction(Element):
    def __init__(self, amount: float):
        self.amount = amount

    def accept(self, visitor: 'Visitor'):
        return visitor.visit_deduction(self)

# ===== VISITOR SCHNITTSTELLE =====
class Visitor(ABC):
    @abstractmethod
    def visit_salary(self, salary: Salary):
        pass

    @abstractmethod
    def visit_bonus(self, bonus: Bonus):
        pass

    @abstractmethod
    def visit_deduction(self, deduction: Deduction):
        pass

# ===== KONKRETE VISITORS =====
class TaxVisitor(Visitor):
    def __init__(self, tax_rate: float = 0.2):
        self.tax_rate = tax_rate

    def visit_salary(self, salary: Salary):
        return salary.amount * self.tax_rate

    def visit_bonus(self, bonus: Bonus):
        return bonus.amount * 0.3  # Höhere Steuer auf Bonus

    def visit_deduction(self, deduction: Deduction):
        return 0  # Deductions sind nicht steuerpflichtig

class PaySlipVisitor(Visitor):
    def __init__(self):
        self.items = []

    def visit_salary(self, salary: Salary):
        self.items.append(f"Salary: ${salary.amount}")
        return None

    def visit_bonus(self, bonus: Bonus):
        self.items.append(f"Bonus: ${bonus.amount}")
        return None

    def visit_deduction(self, deduction: Deduction):
        self.items.append(f"Deduction: -${deduction.amount}")
        return None

    def get_pay_slip(self):
        return "\n".join(self.items)

# ===== OBJEKT-STRUKTUR =====
class Employee:
    def __init__(self, name: str):
        self.name = name
        self.elements = []

    def add_element(self, element: Element):
        self.elements.append(element)

    def accept(self, visitor: Visitor):
        total = 0
        for element in self.elements:
            result = element.accept(visitor)
            if result is not None:
                total += result
        return total

# ===== VERWENDUNG =====
employee = Employee("John Doe")
employee.add_element(Salary(3000))
employee.add_element(Bonus(500))
employee.add_element(Deduction(100))

# Tax Visitor
tax_visitor = TaxVisitor()
taxes = employee.accept(tax_visitor)
print(f"Total taxes: ${taxes}")

# PaySlip Visitor
payslip_visitor = PaySlipVisitor()
for element in employee.elements:
    element.accept(payslip_visitor)
print(payslip_visitor.get_pay_slip())
```

### Use-Cases in Python

- **AST-Traversal:** Compiler, Interpreter
- **Report-Generation:** Verschiedene Report-Formate
- **XML/JSON-Verarbeitung:** Parse-Tree Traversal
- **Graph-Algorithmen:** DFS, BFS
- **Data-Validation:** Verschiedene Validierungs-Regeln

---

## 23. Interpreter Pattern

### Definition & Zweck
**Definiere eine Sprache** (oder DSL) und einen **Interpreter** zu ihrer Ausführung.

### Kategorie
Behavioral

### Python-spezifische Besonderheiten

- **Parsing:** Regex oder tokenizer für Input
- **Abstract Syntax Tree:** Struktur-Baum
- **Eval-Vorsicht:** `eval()` ist ein Sicherheitsrisiko
- **Domain-Specific Languages (DSLs):** Häufig mit Interpreter implementiert

### Code-Beispiel (Einfache Arithmetik-Sprache)

```python
from abc import ABC, abstractmethod
import re

# ===== ABSTRACT SYNTAX TREE (AST) =====
class Expression(ABC):
    @abstractmethod
    def interpret(self, context: dict) -> float:
        pass

# ===== TERMINAL EXPRESSIONS =====
class NumberExpression(Expression):
    def __init__(self, value: float):
        self.value = value

    def interpret(self, context: dict) -> float:
        return self.value

class VariableExpression(Expression):
    def __init__(self, name: str):
        self.name = name

    def interpret(self, context: dict) -> float:
        return context.get(self.name, 0)

# ===== NON-TERMINAL EXPRESSIONS =====
class AddExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: dict) -> float:
        return self.left.interpret(context) + self.right.interpret(context)

class SubtractExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: dict) -> float:
        return self.left.interpret(context) - self.right.interpret(context)

class MultiplyExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: dict) -> float:
        return self.left.interpret(context) * self.right.interpret(context)

# ===== PARSER =====
class SimpleCalculatorParser:
    def parse(self, expression_str: str) -> Expression:
        """Parser für einfache Ausdrücke: "a + b * c" """
        tokens = self._tokenize(expression_str)
        return self._parse_expression(tokens, 0)[0]

    def _tokenize(self, expr: str):
        """Tokenisiere Input"""
        pattern = r'(\d+|[a-z]|[+\-*]|\(|\))'
        return re.findall(pattern, expr.replace(" ", ""))

    def _parse_expression(self, tokens, pos):
        """Rekursiv Parse Term + Term + ... """
        left, pos = self._parse_term(tokens, pos)

        while pos < len(tokens) and tokens[pos] in ['+', '-']:
            op = tokens[pos]
            pos += 1
            right, pos = self._parse_term(tokens, pos)

            if op == '+':
                left = AddExpression(left, right)
            else:
                left = SubtractExpression(left, right)

        return left, pos

    def _parse_term(self, tokens, pos):
        """Rekursiv Parse Faktor * Faktor * ... """
        left, pos = self._parse_factor(tokens, pos)

        while pos < len(tokens) and tokens[pos] == '*':
            pos += 1  # Skip '*'
            right, pos = self._parse_factor(tokens, pos)
            left = MultiplyExpression(left, right)

        return left, pos

    def _parse_factor(self, tokens, pos):
        """Parse Zahl oder Variable"""
        token = tokens[pos]

        if token.isdigit():
            return NumberExpression(float(token)), pos + 1
        elif token.isalpha():
            return VariableExpression(token), pos + 1
        elif token == '(':
            pos += 1  # Skip '('
            expr, pos = self._parse_expression(tokens, pos)
            pos += 1  # Skip ')'
            return expr, pos

# ===== VERWENDUNG =====
parser = SimpleCalculatorParser()

# Einfache Ausdrücke
expr1 = parser.parse("2 + 3 * 4")
print(f"2 + 3 * 4 = {expr1.interpret({})}")  # 14 (Operator-Priorität beachtet)

expr2 = parser.parse("a + b")
context = {"a": 10, "b": 5}
print(f"a + b = {expr2.interpret(context)}")  # 15

expr3 = parser.parse("x * 2 + 3")
context = {"x": 5}
print(f"x * 2 + 3 = {expr3.interpret(context)}")  # 13
```

### Pythonische Alternative: `eval()` (Mit Vorsicht!)

```python
# WARNUNG: eval() ist unsicher mit untrusted Input
class SimpleInterpreter:
    def eval(self, expression: str, context: dict) -> float:
        # Nur für kontrollierten, internen Input!
        return eval(expression, {"__builtins__": {}}, context)

interpreter = SimpleInterpreter()
result = interpreter.eval("a + b * 2", {"a": 10, "b": 5})
print(result)  # 20
```

### Use-Cases in Python

- **DSLs:** YAML, TOML, Jinja2-Templates
- **Query-Sprachen:** SQL Parser, JSON Query
- **Reguläre Ausdrücke:** Regex Engine
- **Mathematische Ausdrücke:** Calculator, Formula Engine
- **Konfigurationssprachen:** INI, CONF Parser

---

# IV. QUICK REFERENCE

## Auswahl-Guide: Welches Pattern wählen?

### Nach Problem-Typ

| Problem | Empfohlenes Pattern |
|---------|-------------------|
| Objekterstellung komplex | Builder |
| Eine Instanz global | Singleton |
| Mehrere Implementierungen | Factory / Strategy |
| Hierarchie mit Variationen | Abstract Factory / Bridge |
| Objekte klonen | Prototype |
| Schnittstellen kompatibel machen | Adapter |
| Struktur+Verhalten hinzufügen | Decorator |
| Komplexes Subsystem vereinfachen | Facade |
| Viele ähnliche Objekte | Flyweight |
| Zugriff kontrollieren/lazy-load | Proxy |
| Request durch Handlers | Chain of Responsibility |
| Aktion rückgängig machen | Command / Memento |
| Sammlung traversieren | Iterator |
| Objekte kommunizieren | Mediator |
| Zustandsänderung speichern | Memento |
| Objekt-Benachrichtigung | Observer |
| Verhalten mit Zustand wechseln | State |
| Algorithmus auswechseln | Strategy |
| Algorithmus-Skelett definieren | Template Method |
| Operation auf Struktur | Visitor |
| Mini-Sprache implementieren | Interpreter |

---

## Python-Spezifische Best Practices

### 1. Prefer Composition over Inheritance
```python
# ❌ Schlecht: Deep Inheritance Hierarchies
class Animal: pass
class Mammal(Animal): pass
class Dog(Mammal): pass

# ✅ Besser: Composition
class Animal:
    def __init__(self, sound_maker):
        self.sound_maker = sound_maker
```

### 2. Use Modules as Singletons
```python
# ✅ Pythonic Singleton
# mymodule.py
_instance = None

def get_instance():
    global _instance
    if _instance is None:
        _instance = MyClass()
    return _instance

# Andere Module:
from mymodule import get_instance
```

### 3. Duck Typing Nutzen
```python
# ✅ Python braucht nicht immer ABC
class Logger:
    def log(self, msg): print(msg)

class FileLogger:
    def log(self, msg):
        with open("log.txt") as f: f.write(msg)

# Beide funktionieren überall wo log() aufgerufen wird
```

### 4. First-Class Functions
```python
# ✅ Strategy mit Funktionen statt Klassen
def bubble_sort(data): ...
def quick_sort(data): ...

sorter = quick_sort  # Function als Strategy
result = sorter(data)
```

### 5. Context Managers für Resource Management
```python
# ✅ Proxy mit Context Manager
class FileProxy:
    def __enter__(self):
        self.file = open("data.txt")
        return self

    def __exit__(self, *args):
        self.file.close()

with FileProxy() as proxy:
    data = proxy.file.read()
```

---

## Warnsignale: Wann ist ein Pattern Overkill?

- **Zu viele kleine Klassen:** Pattern-Explosion
- **Unklare Verantwortung:** Pattern überlagert Business-Logik
- **Performance-Overhead:** Indirection bei jedem Call
- **Junior-Developers sind verwirrt:** KISS (Keep It Simple, Stupid)

**Golden Rule:** Nutze Patterns für echte Probleme, nicht um "clever" zu sein.

---

## Quellen

- [Refactoring.Guru - Python Design Patterns](https://refactoring.guru/design-patterns/python)
- [Medium - Python Creational Design Patterns](https://medium.com/@surajbahuguna1/python-creational-design-patterns-singleton-factory-abstract-factory-builder-and-prototype-7a43e7a36e32)
- [Calmops - Python Design Patterns](https://calmops.com/programming/python/python-design-patterns-singleton-factory-observer/)
- [Effective Python - Prefer Class Decorators](https://effectivepython.com/2019/12/18/prefer-class-decorators-over-metaclasses-for-composable-class-extensions)
- [Python-Patterns GitHub - Community Standards](https://github.com/faif/python-patterns)
- [DEV Community - Advanced Python Techniques](https://dev.to/oussama_errafif/advanced-python-techniques-metaclasses-decorators-and-context-managers-59af)
- [GeeksforGeeks - Design Patterns](https://www.geeksforgeeks.org/system-design/difference-between-the-facade-proxy-adapter-and-decorator-design-patterns/)

---

**Dokument Status:** Vollständig | 23 Patterns mit Code-Beispielen | Python 3.8+ | 2026-03-06
