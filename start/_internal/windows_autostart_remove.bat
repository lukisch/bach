@echo off
REM ============================================
REM BACH Bridge - Autostart Entfernen
REM ============================================

echo [BACH] Entferne Windows Autostart-Eintrag...
schtasks /delete /tn "BACH Bridge Tray" /f

if %ERRORLEVEL% EQU 0 (
    echo [OK] Autostart-Eintrag entfernt
) else (
    echo [WARN] Kein Autostart-Eintrag gefunden
)

pause
