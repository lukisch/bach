@echo off
REM ============================================
REM BACH Bridge - Windows Autostart Setup
REM ============================================

echo [BACH] Erstelle Windows Autostart-Eintrag...

REM Task Scheduler Eintrag erstellen
schtasks /create /tn "BACH Bridge Tray" ^
    /tr "pythonw \"%~dp0..\system\hub\_services\claude_bridge\bridge_tray.py\"" ^
    /sc onlogon ^
    /rl highest ^
    /f

if %ERRORLEVEL% EQU 0 (
    echo [OK] Autostart-Eintrag erstellt
    echo      Bridge startet jetzt automatisch bei Login
) else (
    echo [ERROR] Autostart-Eintrag fehlgeschlagen
    echo         Bitte als Administrator ausfuehren
)

pause
