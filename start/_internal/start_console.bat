@echo off
REM =====================================================
REM  BACH User-Konsole starten
REM =====================================================

REM Ins System-Verzeichnis wechseln
cd /d "%~dp0..\system"

title BACH User-Konsole

python tools\user_console.py

pause
