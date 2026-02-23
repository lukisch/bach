# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: Python Documentation, pytest Documentation, unittest Documentation

================================================================================
                            PYTHON TESTING
================================================================================

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
INHALTSVERZEICHNIS
================================================================================
  1. Einfuehrung und Grundkonzepte
  2. unittest - Das Standard-Framework
  3. pytest - Das moderne Test-Framework
  4. Assertions und Vergleiche
  5. Fixtures und Setup/Teardown
  6. Mocking und Patching
  7. Parametrisierte Tests
  8. Test Coverage
  9. Testorganisation und Best Practices
  10. Fortgeschrittene Testtechniken
  11. Continuous Integration

================================================================================
1. EINFUEHRUNG UND GRUNDKONZEPTE
================================================================================

  Software-Testing ist essentiell fuer zuverlaessigen Code. Python bietet
  mehrere Frameworks und Werkzeuge fuer verschiedene Testarten.

  TESTARTEN:
  ----------
    Unit Tests:        Einzelne Funktionen/Methoden isoliert testen
    Integration Tests: Zusammenspiel mehrerer Komponenten testen
    End-to-End Tests:  Gesamtes System aus Benutzersicht testen
    Regression Tests:  Sicherstellen, dass Aenderungen nichts kaputtmachen

  TESTPRINZIPIEN:
  ---------------
    AAA-Pattern (Arrange-Act-Assert):
      1. Arrange: Testdaten und Objekte vorbereiten
      2. Act:     Zu testende Aktion ausfuehren
      3. Assert:  Ergebnis ueberpruefen

    FIRST-Prinzip:
      - Fast:       Tests sollen schnell sein
      - Isolated:   Tests sollen unabhaengig sein
      - Repeatable: Tests sollen reproduzierbar sein
      - Self-validating: Tests sollen eindeutig bestehen/fehlschlagen
      - Timely:     Tests zeitnah zum Code schreiben

  VERZEICHNISSTRUKTUR:
  --------------------
    projekt/
    |-- src/
    |   |-- __init__.py
    |   |-- module.py
    |
    |-- tests/
    |   |-- __init__.py
    |   |-- test_module.py
    |   |-- conftest.py       # pytest Fixtures
    |
    |-- pyproject.toml

================================================================================
2. UNITTEST - DAS STANDARD-FRAMEWORK
================================================================================

  unittest ist Teil der Python-Standardbibliothek und folgt dem xUnit-Muster.

  GRUNDSTRUKTUR:
  --------------
    import unittest

    class TestCalculator(unittest.TestCase):
        """Tests fuer Calculator-Klasse."""

        @classmethod
        def setUpClass(cls):
            """Einmal vor allen Tests der Klasse."""
            print("Klasse wird vorbereitet")

        @classmethod
        def tearDownClass(cls):
            """Einmal nach allen Tests der Klasse."""
            print("Klasse wird aufgeraeumt")

        def setUp(self):
            """Vor jedem einzelnen Test."""
            self.calc = Calculator()

        def tearDown(self):
            """Nach jedem einzelnen Test."""
            self.calc = None

        def test_addition(self):
            """Test der Addition."""
            result = self.calc.add(2, 3)
            self.assertEqual(result, 5)

        def test_division_by_zero(self):
            """Test Division durch Null."""
            with self.assertRaises(ZeroDivisionError):
                self.calc.divide(10, 0)


  TESTS AUSFUEHREN:
  -----------------
    # Einzelne Datei
    python -m unittest test_module.py

    # Alle Tests im Verzeichnis
    python -m unittest discover

    # Mit Verzeichnisangabe
    python -m unittest discover -s tests -p "test_*.py"

    # Verbose-Modus
    python -m unittest -v test_module.py


  WICHTIGE ASSERT-METHODEN:
  -------------------------
    self.assertEqual(a, b)           # a == b
    self.assertNotEqual(a, b)        # a != b
    self.assertTrue(x)               # bool(x) is True
    self.assertFalse(x)              # bool(x) is False
    self.assertIs(a, b)              # a is b
    self.assertIsNot(a, b)           # a is not b
    self.assertIsNone(x)             # x is None
    self.assertIsNotNone(x)          # x is not None
    self.assertIn(a, b)              # a in b
    self.assertNotIn(a, b)           # a not in b
    self.assertIsInstance(a, b)      # isinstance(a, b)
    self.assertRaises(exc, fn, ...)  # fn(...) raises exc
    self.assertAlmostEqual(a, b)     # round(a-b, 7) == 0
    self.assertGreater(a, b)         # a > b
    self.assertLess(a, b)            # a < b
    self.assertRegex(s, r)           # r.search(s)

================================================================================
3. PYTEST - DAS MODERNE TEST-FRAMEWORK
================================================================================

  pytest ist das beliebteste Test-Framework fuer Python mit einfacher
  Syntax und maechtigen Features.

  INSTALLATION:
  -------------
    pip install pytest

  EINFACHER TEST:
  ---------------
    # test_calculator.py
    def test_addition():
        assert 1 + 1 == 2

    def test_subtraction():
        assert 5 - 3 == 2

    def test_string_contains():
        assert "hello" in "hello world"


  TESTS AUSFUEHREN:
  -----------------
    # Alle Tests
    pytest

    # Verbose
    pytest -v

    # Bestimmte Datei
    pytest test_calculator.py

    # Bestimmter Test
    pytest test_calculator.py::test_addition

    # Mit Keyword-Filter
    pytest -k "addition or subtraction"

    # Bei erstem Fehler stoppen
    pytest -x

    # Letzte fehlgeschlagene Tests
    pytest --lf

    # Output anzeigen
    pytest -s


  TESTKLASSEN IN PYTEST:
  ----------------------
    class TestCalculator:
        """Gruppierung von Tests."""

        def test_add(self):
            assert 2 + 2 == 4

        def test_multiply(self):
            assert 3 * 4 == 12


  EXPECTED FAILURES UND SKIP:
  ---------------------------
    import pytest

    @pytest.mark.skip(reason="Noch nicht implementiert")
    def test_future_feature():
        pass

    @pytest.mark.skipif(sys.version_info < (3, 10), reason="Python 3.10+ noetig")
    def test_new_feature():
        pass

    @pytest.mark.xfail(reason="Bekannter Bug #123")
    def test_known_bug():
        assert broken_function() == expected

================================================================================
4. ASSERTIONS UND VERGLEICHE
================================================================================

  PYTEST ASSERTIONS:
  ------------------
    # Einfache Assertions
    assert value == expected
    assert value != other
    assert value is None
    assert value is not None
    assert value in collection
    assert not condition

    # Mit Fehlermeldung
    assert value == expected, f"Erwartet {expected}, erhalten {value}"


  EXCEPTIONS TESTEN:
  ------------------
    import pytest

    def test_raises_value_error():
        with pytest.raises(ValueError):
            int("nicht_eine_zahl")

    def test_raises_with_message():
        with pytest.raises(ValueError, match="invalid literal"):
            int("abc")

    def test_raises_and_check():
        with pytest.raises(ValueError) as exc_info:
            raise ValueError("Testfehler")
        assert "Testfehler" in str(exc_info.value)


  APPROXIMATIVE VERGLEICHE:
  -------------------------
    import pytest
    from math import pi

    def test_float_comparison():
        # Relative Toleranz (Standard: 1e-6)
        assert 0.1 + 0.2 == pytest.approx(0.3)

        # Absolute Toleranz
        assert pi == pytest.approx(3.14159, abs=0.001)

        # Fuer Listen/Dicts
        assert [0.1 + 0.2, 0.2 + 0.4] == pytest.approx([0.3, 0.6])


  WARNINGS TESTEN:
  ----------------
    import warnings
    import pytest

    def test_warning_issued():
        with pytest.warns(DeprecationWarning):
            warnings.warn("veraltet", DeprecationWarning)

    def test_warning_message():
        with pytest.warns(UserWarning, match="wichtig"):
            warnings.warn("Wichtige Warnung", UserWarning)

================================================================================
5. FIXTURES UND SETUP/TEARDOWN
================================================================================

  Fixtures sind pytest's maechtige Alternative zu setUp/tearDown.

  GRUNDLEGENDE FIXTURES:
  ----------------------
    import pytest

    @pytest.fixture
    def sample_data():
        """Stellt Testdaten bereit."""
        return [1, 2, 3, 4, 5]

    def test_sum(sample_data):
        assert sum(sample_data) == 15

    def test_length(sample_data):
        assert len(sample_data) == 5


  FIXTURE MIT SETUP UND TEARDOWN:
  -------------------------------
    @pytest.fixture
    def database_connection():
        # Setup
        conn = create_connection()
        conn.begin_transaction()

        yield conn  # Test laeuft hier

        # Teardown
        conn.rollback()
        conn.close()

    def test_database_query(database_connection):
        result = database_connection.execute("SELECT 1")
        assert result == 1


  FIXTURE SCOPES:
  ---------------
    @pytest.fixture(scope="function")  # Standard: Pro Test
    def per_test():
        return []

    @pytest.fixture(scope="class")     # Pro Testklasse
    def per_class():
        return []

    @pytest.fixture(scope="module")    # Pro Modul
    def per_module():
        return []

    @pytest.fixture(scope="session")   # Pro pytest-Lauf
    def per_session():
        return []


  FIXTURE FACTORY:
  ----------------
    @pytest.fixture
    def make_user():
        """Factory fuer User-Objekte."""
        created_users = []

        def _make_user(name, email):
            user = User(name=name, email=email)
            created_users.append(user)
            return user

        yield _make_user

        # Cleanup
        for user in created_users:
            user.delete()

    def test_user_creation(make_user):
        user1 = make_user("Alice", "alice@example.com")
        user2 = make_user("Bob", "bob@example.com")
        assert user1.name == "Alice"


  CONFTEST.PY - GEMEINSAME FIXTURES:
  ----------------------------------
    # tests/conftest.py
    import pytest

    @pytest.fixture
    def app():
        """Fixture verfuegbar fuer alle Tests im Verzeichnis."""
        from myapp import create_app
        app = create_app(testing=True)
        return app

    @pytest.fixture
    def client(app):
        """Test-Client fuer Flask/Django Apps."""
        return app.test_client()

================================================================================
6. MOCKING UND PATCHING
================================================================================

  Mocking ersetzt Abhaengigkeiten durch kontrollierte Ersatzobjekte.

  GRUNDLEGENDES MOCKING:
  ----------------------
    from unittest.mock import Mock, MagicMock

    # Einfacher Mock
    mock_service = Mock()
    mock_service.get_data.return_value = {"key": "value"}

    result = mock_service.get_data()
    assert result == {"key": "value"}

    # Aufruf verifizieren
    mock_service.get_data.assert_called_once()


  PATCH DECORATOR:
  ----------------
    from unittest.mock import patch

    # Als Decorator
    @patch("mymodule.external_api")
    def test_api_call(mock_api):
        mock_api.fetch.return_value = {"status": "ok"}

        result = my_function_using_api()

        mock_api.fetch.assert_called_with("endpoint")
        assert result["status"] == "ok"


  PATCH ALS CONTEXT MANAGER:
  --------------------------
    def test_file_operations():
        with patch("builtins.open", mock_open(read_data="test content")) as m:
            with open("file.txt") as f:
                content = f.read()

        assert content == "test content"
        m.assert_called_once_with("file.txt")


  PATCH.OBJECT:
  -------------
    from unittest.mock import patch

    class MyClass:
        def method(self):
            return "original"

    def test_method():
        obj = MyClass()
        with patch.object(obj, "method", return_value="mocked"):
            assert obj.method() == "mocked"


  MOCK MIT SIDE EFFECTS:
  ----------------------
    mock = Mock()

    # Verschiedene Rueckgabewerte bei mehreren Aufrufen
    mock.side_effect = [1, 2, 3]
    assert mock() == 1
    assert mock() == 2
    assert mock() == 3

    # Exception ausloesen
    mock.side_effect = ValueError("Fehler")
    with pytest.raises(ValueError):
        mock()

    # Funktion als side_effect
    mock.side_effect = lambda x: x * 2
    assert mock(5) == 10


  PYTEST-MOCK PLUGIN:
  -------------------
    # pip install pytest-mock

    def test_with_mocker(mocker):
        mock_api = mocker.patch("mymodule.api_client")
        mock_api.get.return_value = {"data": "test"}

        result = fetch_data()

        assert result == {"data": "test"}

================================================================================
7. PARAMETRISIERTE TESTS
================================================================================

  Parametrisierte Tests fuehren denselben Test mit verschiedenen Daten aus.

  PYTEST PARAMETRIZE:
  -------------------
    import pytest

    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
        (4, 8),
    ])
    def test_double(input, expected):
        assert input * 2 == expected


  MEHRERE PARAMETER:
  ------------------
    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (5, 5, 10),
        (-1, 1, 0),
        (0, 0, 0),
    ])
    def test_addition(a, b, expected):
        assert a + b == expected


  IDS FUER BESSERE AUSGABE:
  -------------------------
    @pytest.mark.parametrize("input,expected", [
        pytest.param("hello", 5, id="simple_word"),
        pytest.param("", 0, id="empty_string"),
        pytest.param("hello world", 11, id="with_space"),
    ])
    def test_string_length(input, expected):
        assert len(input) == expected


  KOMBINATIONEN MIT MEHREREN DECORATORS:
  --------------------------------------
    @pytest.mark.parametrize("x", [1, 2])
    @pytest.mark.parametrize("y", [10, 20])
    def test_combinations(x, y):
        # Testet: (1,10), (1,20), (2,10), (2,20)
        assert x + y > 0


  PARAMETRISIERUNG MIT FIXTURES:
  ------------------------------
    @pytest.fixture(params=["mysql", "postgresql", "sqlite"])
    def database(request):
        db = create_database(request.param)
        yield db
        db.close()

    def test_database_operations(database):
        # Laeuft fuer jeden Datenbanktyp
        database.execute("SELECT 1")

================================================================================
8. TEST COVERAGE
================================================================================

  Coverage misst, welcher Code durch Tests ausgefuehrt wird.

  INSTALLATION:
  -------------
    pip install pytest-cov

  VERWENDUNG:
  -----------
    # Einfacher Coverage-Bericht
    pytest --cov=mypackage

    # Mit HTML-Report
    pytest --cov=mypackage --cov-report=html

    # Mit Terminal-Report
    pytest --cov=mypackage --cov-report=term-missing

    # Minimum Coverage erzwingen
    pytest --cov=mypackage --cov-fail-under=80


  COVERAGE-KONFIGURATION (pyproject.toml):
  ----------------------------------------
    [tool.coverage.run]
    source = ["src"]
    branch = true
    omit = [
        "*/tests/*",
        "*/__init__.py",
    ]

    [tool.coverage.report]
    exclude_lines = [
        "pragma: no cover",
        "if __name__ == .__main__.:",
        "raise NotImplementedError",
    ]


  CODE VON COVERAGE AUSSCHLIESSEN:
  --------------------------------
    def debug_function():  # pragma: no cover
        """Wird von Coverage ignoriert."""
        pass

    if TYPE_CHECKING:  # pragma: no cover
        from typing import Protocol

================================================================================
9. TESTORGANISATION UND BEST PRACTICES
================================================================================

  NAMENKONVENTIONEN:
  ------------------
    - Testdateien: test_*.py oder *_test.py
    - Testfunktionen: test_*
    - Testklassen: Test* (ohne __init__)

  TESTSTRUKTUR:
  -------------
    def test_function_name_should_expected_behavior():
        # Arrange
        data = prepare_test_data()
        service = create_service()

        # Act
        result = service.process(data)

        # Assert
        assert result.status == "success"
        assert result.count == 5


  PYTEST.INI / PYPROJECT.TOML:
  ----------------------------
    # pyproject.toml
    [tool.pytest.ini_options]
    testpaths = ["tests"]
    python_files = ["test_*.py"]
    python_classes = ["Test*"]
    python_functions = ["test_*"]
    addopts = "-v --tb=short"
    markers = [
        "slow: markiert langsame Tests",
        "integration: markiert Integrationstests",
    ]


  CUSTOM MARKERS:
  ---------------
    import pytest

    @pytest.mark.slow
    def test_large_dataset():
        # Langsamer Test
        pass

    @pytest.mark.integration
    def test_database_integration():
        # Integrationstest
        pass

    # Ausfuehrung:
    # pytest -m "not slow"           # Ohne langsame Tests
    # pytest -m "integration"        # Nur Integrationstests


  BEST PRACTICES:
  ---------------
    1. Ein Assert pro Test (idealerweise)
    2. Tests isoliert halten - keine Abhaengigkeiten zwischen Tests
    3. Aussagekraeftige Testnamen
    4. Testdaten explizit definieren, nicht implizit erwarten
    5. Externe Abhaengigkeiten mocken
    6. Tests schnell halten (<100ms pro Unit-Test)
    7. Coverage als Metrik, nicht als Ziel (80-90% ist oft ausreichend)

================================================================================
10. FORTGESCHRITTENE TESTTECHNIKEN
================================================================================

  PROPERTY-BASED TESTING (Hypothesis):
  ------------------------------------
    # pip install hypothesis
    from hypothesis import given, strategies as st

    @given(st.integers(), st.integers())
    def test_addition_commutative(a, b):
        assert a + b == b + a

    @given(st.lists(st.integers()))
    def test_sorted_is_sorted(lst):
        result = sorted(lst)
        assert all(result[i] <= result[i+1] for i in range(len(result)-1))


  SNAPSHOT TESTING:
  -----------------
    # pip install pytest-snapshot
    def test_api_response(snapshot):
        response = api.get_user(123)
        snapshot.assert_match(response, "user_response.json")


  ASYNCHRONE TESTS:
  -----------------
    # pip install pytest-asyncio
    import pytest

    @pytest.mark.asyncio
    async def test_async_function():
        result = await async_fetch_data()
        assert result is not None

    @pytest.fixture
    async def async_client():
        async with AsyncClient() as client:
            yield client

    @pytest.mark.asyncio
    async def test_with_async_fixture(async_client):
        response = await async_client.get("/api/data")
        assert response.status == 200


  DOCTEST:
  --------
    def add(a, b):
        """
        Addiert zwei Zahlen.

        >>> add(2, 3)
        5
        >>> add(-1, 1)
        0
        """
        return a + b

    # Ausfuehrung:
    # python -m doctest module.py
    # pytest --doctest-modules

================================================================================
11. CONTINUOUS INTEGRATION
================================================================================

  GITHUB ACTIONS (.github/workflows/tests.yml):
  ---------------------------------------------
    name: Tests

    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            python-version: ["3.10", "3.11", "3.12"]

        steps:
          - uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: ${{ matrix.python-version }}

          - name: Install dependencies
            run: |
              pip install -e ".[test]"

          - name: Run tests
            run: |
              pytest --cov=mypackage --cov-report=xml

          - name: Upload coverage
            uses: codecov/codecov-action@v3


  TOX FUER MEHRERE PYTHON-VERSIONEN:
  ----------------------------------
    # tox.ini
    [tox]
    envlist = py310, py311, py312

    [testenv]
    deps = pytest
    commands = pytest tests/


  PRE-COMMIT HOOKS:
  -----------------
    # .pre-commit-config.yaml
    repos:
      - repo: local
        hooks:
          - id: pytest
            name: pytest
            entry: pytest
            language: system
            types: [python]
            pass_filenames: false

================================================================================
SIEHE AUCH
================================================================================

  wiki/python/fehlerbehandlung/    - Exception Handling
  wiki/python/decorators/          - Decorators (@pytest.fixture)
  wiki/informatik/softwareentwicklung/  - Allgemeine Entwicklungspraktiken
  wiki/python/debugging/           - Debugging-Techniken

================================================================================
