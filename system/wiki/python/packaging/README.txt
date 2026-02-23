# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: packaging.python.org, PEP 517, PEP 518, PEP 621,
#          setuptools docs, PyPI docs, Real Python

PYTHON PACKAGING UND DISTRIBUTION
=================================

Stand: 2026-02-05

UEBERBLICK
==========
  Python Packaging beschreibt den Prozess, Code als installierbare
  Pakete zu verteilen. Seit 2023 ist pyproject.toml der Standard,
  setup.py gilt als veraltet.

GRUNDKONZEPTE
=============

PACKAGE VS MODULE
-----------------
  Module:   Eine einzelne .py Datei
  Package:  Ein Ordner mit __init__.py (mehrere Module)

  mein_package/
  |-- __init__.py      <- Macht es zum Package
  |-- module_a.py
  |-- module_b.py
  |-- sub_package/
      |-- __init__.py
      |-- modul_c.py

DISTRIBUTION TYPES
------------------
  Source Distribution (sdist):
    - Quellcode als .tar.gz
    - Muss beim User kompiliert werden
    - Plattformunabhaengig

  Built Distribution (wheel):
    - Vorkompiliert als .whl
    - Schnellere Installation
    - Plattformspezifisch (oft)

MODERNE PROJEKT-STRUKTUR
========================

EMPFOHLENES LAYOUT
------------------
  mein_projekt/
  |-- src/
  |   |-- mein_paket/
  |       |-- __init__.py
  |       |-- core.py
  |       |-- utils.py
  |-- tests/
  |   |-- __init__.py
  |   |-- test_core.py
  |-- docs/
  |-- pyproject.toml      <- HAUPTKONFIGURATION
  |-- README.md
  |-- LICENSE
  |-- .gitignore

WARUM SRC-LAYOUT?
-----------------
  - Verhindert versehentlichen Import des lokalen Ordners
  - Testet das installierte Paket, nicht den Quellcode
  - Standard in der Python-Community seit 2020+

PYPROJECT.TOML (STANDARD)
=========================

MINIMALE KONFIGURATION
----------------------
  [build-system]
  requires = ["setuptools>=61.0", "wheel"]
  build-backend = "setuptools.build_meta"

  [project]
  name = "mein-paket"
  version = "1.0.0"
  description = "Kurze Beschreibung des Pakets"
  readme = "README.md"
  license = {text = "MIT"}
  requires-python = ">=3.9"
  authors = [
      {name = "Dein Name", email = "email@example.com"}
  ]

  dependencies = [
      "requests>=2.28",
      "pandas>=1.5",
  ]

  [project.urls]
  Homepage = "https://github.com/user/projekt"
  Documentation = "https://projekt.readthedocs.io"

VOLLSTAENDIGE KONFIGURATION
---------------------------
  [build-system]
  requires = ["setuptools>=61.0", "wheel"]
  build-backend = "setuptools.build_meta"

  [project]
  name = "mein-paket"
  version = "1.0.0"
  description = "Umfangreiche Python-Bibliothek"
  readme = "README.md"
  license = {text = "MIT"}
  requires-python = ">=3.9"
  authors = [
      {name = "Max Mustermann", email = "max@example.com"}
  ]
  maintainers = [
      {name = "Team", email = "team@example.com"}
  ]
  keywords = ["automation", "tools", "utilities"]
  classifiers = [
      "Development Status :: 4 - Beta",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3.11",
      "Programming Language :: Python :: 3.12",
  ]

  dependencies = [
      "requests>=2.28",
      "click>=8.0",
  ]

  [project.optional-dependencies]
  dev = [
      "pytest>=7.0",
      "black>=23.0",
      "mypy>=1.0",
  ]
  docs = [
      "sphinx>=6.0",
      "sphinx-rtd-theme",
  ]

  [project.scripts]
  mein-cli = "mein_paket.cli:main"

  [project.gui-scripts]
  mein-gui = "mein_paket.gui:main"

  [project.entry-points."mein_paket.plugins"]
  plugin1 = "mein_paket.plugins:Plugin1"

  [project.urls]
  Homepage = "https://github.com/user/mein-paket"
  Documentation = "https://mein-paket.readthedocs.io"
  Repository = "https://github.com/user/mein-paket.git"
  Changelog = "https://github.com/user/mein-paket/blob/main/CHANGELOG.md"

  [tool.setuptools.packages.find]
  where = ["src"]

DYNAMISCHE VERSION
------------------
  # In pyproject.toml:
  [project]
  dynamic = ["version"]

  [tool.setuptools.dynamic]
  version = {attr = "mein_paket.__version__"}

  # In src/mein_paket/__init__.py:
  __version__ = "1.0.0"

VIRTUAL ENVIRONMENTS
====================

ERSTELLEN UND AKTIVIEREN
------------------------
  # Mit venv (eingebaut):
  python -m venv .venv

  # Windows aktivieren:
  .venv\Scripts\activate

  # Linux/Mac aktivieren:
  source .venv/bin/activate

  # Deaktivieren:
  deactivate

UV (MODERNER PAKETMANAGER)
--------------------------
  # UV ist 10-100x schneller als pip

  # Installation:
  pip install uv

  # Projekt erstellen:
  uv init mein_projekt

  # Virtuelle Umgebung:
  uv venv

  # Pakete installieren:
  uv pip install requests
  uv pip install -r requirements.txt

  # Sync mit pyproject.toml:
  uv pip sync

REQUIREMENTS MANAGEMENT
-----------------------
  # requirements.txt generieren:
  pip freeze > requirements.txt

  # Mit UV (besser):
  uv pip compile pyproject.toml -o requirements.txt

  # Separate Dateien:
  requirements/
  |-- base.txt         # Produktionsabhaengigkeiten
  |-- dev.txt          # Entwicklung (pytest, black...)
  |-- docs.txt         # Dokumentation (sphinx...)

BUILD UND INSTALLATION
======================

LOKALE ENTWICKLUNG
------------------
  # Editierbare Installation (fuer Entwicklung):
  pip install -e .

  # Mit optionalen Abhaengigkeiten:
  pip install -e ".[dev]"
  pip install -e ".[dev,docs]"

PAKET BAUEN
-----------
  # Build-Tools installieren:
  pip install build

  # Paket bauen:
  python -m build

  # Erzeugt:
  dist/
  |-- mein_paket-1.0.0.tar.gz    # sdist
  |-- mein_paket-1.0.0-py3-none-any.whl  # wheel

PYPI UPLOAD
-----------
  # Twine installieren:
  pip install twine

  # Auf Test-PyPI hochladen (zum Testen):
  twine upload --repository testpypi dist/*

  # Auf echtes PyPI hochladen:
  twine upload dist/*

  # API-Token verwenden (empfohlen):
  # In ~/.pypirc oder als Umgebungsvariable

ALTERNATIVE BUILD-BACKENDS
==========================

POETRY
------
  # Installation:
  pip install poetry

  # Neues Projekt:
  poetry new mein_projekt

  # In bestehendem Ordner:
  poetry init

  # Abhaengigkeit hinzufuegen:
  poetry add requests
  poetry add --group dev pytest

  # Paket bauen:
  poetry build

  # Veroeffentlichen:
  poetry publish

FLIT
----
  # Fuer reine Python-Pakete (kein C-Code)

  [build-system]
  requires = ["flit_core>=3.4"]
  build-backend = "flit_core.buildapi"

  [project]
  name = "mein-paket"
  dynamic = ["version", "description"]

  [tool.flit.module]
  name = "mein_paket"

HATCH
-----
  # Modernes Build-System mit Environment-Management

  [build-system]
  requires = ["hatchling"]
  build-backend = "hatchling.build"

  [tool.hatch.version]
  path = "src/mein_paket/__init__.py"

  [tool.hatch.build.targets.wheel]
  packages = ["src/mein_paket"]

CLI-ANWENDUNGEN
===============

MIT CLICK
---------
  # src/mein_paket/cli.py
  import click

  @click.group()
  @click.version_option()
  def main():
      """Mein CLI Tool - Beschreibung."""
      pass

  @main.command()
  @click.argument('name')
  @click.option('--count', '-c', default=1, help='Anzahl')
  def greet(name, count):
      """Begruesst NAME mehrfach."""
      for _ in range(count):
          click.echo(f'Hallo, {name}!')

  if __name__ == '__main__':
      main()

ENTRY POINT KONFIGURATION
-------------------------
  # In pyproject.toml:
  [project.scripts]
  mein-tool = "mein_paket.cli:main"

  # Nach Installation verfuegbar als:
  # $ mein-tool greet Max --count 3

VERSIONIERUNG
=============

SEMANTIC VERSIONING
-------------------
  MAJOR.MINOR.PATCH

  MAJOR: Inkompatible API-Aenderungen
  MINOR: Neue Features (rueckwaertskompatibel)
  PATCH: Bugfixes (rueckwaertskompatibel)

  Beispiele:
  1.0.0  -> Erste stabile Version
  1.1.0  -> Neues Feature
  1.1.1  -> Bugfix
  2.0.0  -> Breaking Change

PRE-RELEASE VERSIONEN
---------------------
  1.0.0a1   Alpha 1
  1.0.0b1   Beta 1
  1.0.0rc1  Release Candidate 1
  1.0.0     Finale Version

CHANGELOG FUEHREN
-----------------
  # CHANGELOG.md

  ## [1.1.0] - 2026-02-05
  ### Added
  - Neues Feature X
  - Neue Option --verbose

  ### Changed
  - Verbesserte Performance bei Y

  ### Fixed
  - Bug bei Z behoben (#123)

  ## [1.0.0] - 2026-01-01
  - Initial Release

PRIVATE PAKETE
==============

INSTALLATION VON GIT
--------------------
  # Direkt von GitHub:
  pip install git+https://github.com/user/repo.git

  # Bestimmter Branch:
  pip install git+https://github.com/user/repo.git@develop

  # Bestimmter Tag:
  pip install git+https://github.com/user/repo.git@v1.0.0

  # In requirements.txt:
  mein-paket @ git+https://github.com/user/repo.git@v1.0.0

PRIVATES PYPI
-------------
  # .pypirc fuer privates Repository:
  [distutils]
  index-servers =
      pypi
      private

  [private]
  repository = https://pypi.firma.de/
  username = __token__
  password = pypi-xxx

  # Installation von privatem Repository:
  pip install --index-url https://pypi.firma.de/ mein-paket

QUALITAETSSICHERUNG
===================

PRE-PUBLISH CHECKLISTE
----------------------
  [ ] Tests bestanden (pytest)
  [ ] Linting bestanden (ruff/flake8)
  [ ] Type Checking bestanden (mypy)
  [ ] README aktuell
  [ ] CHANGELOG aktuell
  [ ] Version erhoeht
  [ ] License vorhanden
  [ ] Classifiers korrekt

GITHUB ACTIONS WORKFLOW
-----------------------
  # .github/workflows/publish.yml
  name: Publish to PyPI

  on:
    release:
      types: [published]

  jobs:
    publish:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with:
            python-version: '3.11'
        - run: pip install build twine
        - run: python -m build
        - run: twine upload dist/*
          env:
            TWINE_USERNAME: __token__
            TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}

BACH-INTEGRATION
================
  Partner-Zuweisung:
    - Claude: pyproject.toml erstellen, Struktur planen
    - GitHub Actions: CI/CD fuer PyPI
    - UV: Schnelles Dependency Management

  Workflow:
    1. Claude erstellt Projektstruktur
    2. UV verwaltet Abhaengigkeiten
    3. GitHub Actions baut und veroeffentlicht

HAEUFIGE FEHLER
===============
  Problem: "ModuleNotFoundError" nach Installation
  Loesung: src-Layout pruefen, __init__.py vorhanden?

  Problem: Package nicht auf PyPI gefunden
  Loesung: Name bereits vergeben, anderen waehlen

  Problem: "Invalid version" beim Upload
  Loesung: Semantic Versioning einhalten

  Problem: Abhaengigkeiten fehlen
  Loesung: dependencies in pyproject.toml pruefen

SIEHE AUCH
==========
  wiki/python/best_practices/      Python Best Practices
  wiki/python/testing/             Testing mit pytest
  wiki/github_konventionen.txt     Git und GitHub
  wiki/informatik/devops/          CI/CD Pipelines
