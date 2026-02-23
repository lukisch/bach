# RELEASES.md - Template

Dieses Template dokumentiert die Release-Struktur eines Projekts.
Kopieren und fuer jedes Projekt anpassen.

================================================================================
PROJEKTINFO
================================================================================

| Feld     | Wert            |
|----------|-----------------|
| Projekt  | {Projektname}   |
| Aktuell  | v{X.Y.Z}        |
| Stand    | {YYYY-MM-DD}    |

================================================================================
STRUKTUR
================================================================================

AKTIVE PLATTFORMEN:

| Plattform | Status    | Beschreibung     |
|-----------|-----------|------------------|
| desktop   | Aktiv     | Windows 10/11    |
| mobile    | Geplant   | Android (Zukunft)|
| web       | Nein      | Nicht geplant    |

AKTIVE STORES:

| Store        | Status    | Beschreibung                  |
|--------------|-----------|-------------------------------|
| GitHub       | Aktiv     | Primaerer Distributionskanal  |
| WindowsStore | Geplant   | Nach v1.0.0 Stabilisierung    |
| PyPI         | Nein      | Nicht geplant                 |

ORDNERSTRUKTUR:

releases/
+-- v1.0.0/
|   +-- {Projekt}-1.0.0-win64.exe
|   +-- {Projekt}-1.0.0-source.zip
+-- v1.1.0/
    +-- ...

================================================================================
VERSIONSUEBERSICHT
================================================================================

| Version | Datum       | Plattform | Store  | Aenderungen           |
|---------|-------------|-----------|--------|------------------------|
| v1.1.0  | YYYY-MM-DD  | desktop   | GitHub | Feature X, Bugfix Y   |
| v1.0.0  | YYYY-MM-DD  | desktop   | GitHub | Initiales Release     |

================================================================================
INHALT PRO RELEASE
================================================================================

Jeder Versions-Ordner enthaelt:

| Datei                              | Beschreibung                    |
|------------------------------------|---------------------------------|
| {Projekt}-{Version}-win64.exe      | Windows Executable (PyInstaller)|
| {Projekt}-{Version}-source.zip     | Quellcode-Archiv                |
| CHANGELOG.txt                      | Aenderungen dieser Version      |
| SHA256SUMS.txt                     | Checksummen zur Verifizierung   |

================================================================================
BUILD-PROZESS
================================================================================

WINDOWS EXECUTABLE:

  cd src/
  pyinstaller --onefile --windowed --icon=../resources/icons/app.ico main.py
  copy dist\main.exe ..\releases\v{X.Y.Z}\{Projekt}-{X.Y.Z}-win64.exe

SOURCE-ARCHIV:

  7z a -xr!__pycache__ -xr!.git -xr!*.pyc {Projekt}-{X.Y.Z}-source.zip src\ requirements.txt README.md

CHECKSUMMEN:

  certutil -hashfile {Projekt}-{X.Y.Z}-win64.exe SHA256 > SHA256SUMS.txt
  certutil -hashfile {Projekt}-{X.Y.Z}-source.zip SHA256 >> SHA256SUMS.txt

================================================================================
RELEASE-CHECKLISTE
================================================================================

VOR DEM RELEASE:
[ ] Alle Tests bestanden
[ ] Version in __version__ aktualisiert
[ ] CHANGELOG.txt geschrieben
[ ] README.md aktualisiert (falls noetig)
[ ] Usertests abgeschlossen

RELEASE ERSTELLEN:
[ ] Build durchgefuehrt (EXE)
[ ] Source-Archiv erstellt
[ ] Checksummen generiert
[ ] Versions-Ordner in releases/ erstellt
[ ] Dateien kopiert

NACH DEM RELEASE:
[ ] Diese RELEASES.md aktualisiert
[ ] Git-Tag erstellt (git tag v{X.Y.Z})
[ ] GitHub Release veroeffentlicht (falls aktiv)

================================================================================
HINWEISE
================================================================================

VERSIONIERUNG (Semantic Versioning):
- MAJOR (X.0.0): Breaking Changes
- MINOR (0.X.0): Neue Features, rueckwaertskompatibel
- PATCH (0.0.X): Bugfixes

WINDOWS STORE (MSIX):
Falls aktiviert:
- MSIX-Paket erfordert Signierung
- Separate Build-Pipeline noetig
- Struktur wird erweitert zu releases/GitHub/ und releases/WindowsStore/

================================================================================
AENDERUNGSHISTORIE DIESER DATEI
================================================================================

| Datum      | Aenderung            |
|------------|----------------------|
| YYYY-MM-DD | Initiale Erstellung  |
