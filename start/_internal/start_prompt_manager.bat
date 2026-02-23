@echo off
REM =====================================================
REM  BACH Prompt Manager starten
REM =====================================================

REM Ins System-Verzeichnis wechseln
cd /d "%~dp0..\system"

pythonw gui\prompt_manager.py
