@echo off
REM Sentinel Corporation - Terminal Dashboard Launcher
REM Double-click this file to launch the real-time portfolio dashboard

echo ========================================
echo SENTINEL CORPORATION
echo Terminal Dashboard Launcher
echo ========================================
echo.

cd /d "%~dp0"

echo Starting terminal dashboard...
echo Press Ctrl+C to exit
echo.

python Utils\terminal_dashboard.py --refresh 5

pause
