@echo off
REM ============================================================
REM Sentinel Corporation - CEO Control Panel Launcher
REM ============================================================
REM
REM Launches the proper corporate control panel
REM Single interface to CEO who manages all departments
REM
REM ============================================================

echo.
echo ============================================================
echo   SENTINEL CORPORATION - CEO CONTROL PANEL
echo ============================================================
echo.
echo   Initializing connection to CEO...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run setup first or check installation.
    echo.
    pause
    exit /b 1
)

REM Launch CEO Control Panel
venv\Scripts\python.exe sentinel_control_panel.py

echo.
echo ============================================================
echo   SESSION ENDED
echo ============================================================
echo.
pause
