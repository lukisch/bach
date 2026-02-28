@echo off
REM ============================================================
REM BACH Automatisierung - MarbleRun Ketten
REM Scannt und startet MarbleRun Chains
REM ============================================================
title BACH MarbleRun
setlocal enabledelayedexpansion

set MARBLE_DIR=%~dp0..\..\..\..\BACH_Dev\marble_run

echo.
echo  ===================================================
echo   BACH MarbleRun - Ketten starten
echo  ===================================================
echo.

if not exist "%MARBLE_DIR%\marble.py" (
    echo  MarbleRun nicht gefunden: %MARBLE_DIR%
    pause
    exit /b 1
)

echo  Verfuegbare Aktionen:
echo.
echo   [1]  Kette starten (Name eingeben)
echo   [S]  Status anzeigen
echo   [X]  Kette stoppen
echo   [0]  Abbrechen
echo.

set /P CHOICE=  Auswahl:
if /I "%CHOICE%"=="0" exit /b 0
if /I "%CHOICE%"=="" exit /b 0

if /I "%CHOICE%"=="S" (
    cd /d "%MARBLE_DIR%"
    set PYTHONIOENCODING=utf-8
    python marble.py status
    echo.
    pause
    exit /b 0
)

if /I "%CHOICE%"=="X" (
    cd /d "%MARBLE_DIR%"
    set PYTHONIOENCODING=utf-8
    python marble.py stop
    echo.
    pause
    exit /b 0
)

if "%CHOICE%"=="1" (
    set /P CHAIN_ID=  Ketten-ID eingeben:
    if "!CHAIN_ID!"=="" exit /b 0

    echo.
    echo  Starte MarbleRun: !CHAIN_ID!
    echo.

    start cmd /k "title MarbleRun: !CHAIN_ID! && cd /d "%MARBLE_DIR%" && set PYTHONIOENCODING=utf-8 && python marble.py start --chain !CHAIN_ID!"

    echo  [OK] Kette !CHAIN_ID! gestartet (neues Fenster^).
    echo.
    pause
    exit /b 0
)

echo  Ungueltige Auswahl.
pause
