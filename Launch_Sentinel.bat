@echo off
REM ============================================================
REM Sentinel Corporation - Main Launcher
REM ============================================================
REM
REM This script activates the virtual environment and launches
REM the Sentinel terminal dashboard with real-time portfolio data
REM
REM Press Ctrl+C to exit the dashboard
REM ============================================================

echo.
echo ============================================================
echo   SENTINEL CORPORATION - MAIN LAUNCHER
echo ============================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Creating virtual environment...
    python -m venv venv

    echo.
    echo Installing dependencies...
    venv\Scripts\python.exe -m pip install --upgrade pip

    if exist "requirements.txt" (
        venv\Scripts\python.exe -m pip install -r requirements.txt
    ) else (
        echo [WARNING] requirements.txt not found
        echo Installing essential packages...
        venv\Scripts\python.exe -m pip install yfinance rich pandas numpy
    )
)

REM Check if database exists
if not exist "sentinel.db" (
    echo.
    echo [WARNING] sentinel.db not found!
    echo.
    echo If this is your first run, you may see errors.
    echo The database should be in the Sentinel folder.
    echo.
    pause
)

REM Check if terminal dashboard exists
if not exist "Utils\terminal_dashboard.py" (
    echo [ERROR] Utils\terminal_dashboard.py not found!
    echo.
    echo Please ensure you're running this from the Sentinel project folder.
    echo.
    pause
    exit /b 1
)

echo [OK] Environment ready
echo.
echo ============================================================
echo   STARTING SENTINEL TERMINAL DASHBOARD
echo ============================================================
echo.
echo Dashboard features:
echo   - Real-time portfolio performance
echo   - Live market prices (via yfinance)
echo   - Open positions tracking
echo   - System health monitoring
echo   - Auto-refresh every 5 seconds
echo.
echo Press Ctrl+C to exit
echo.
echo ============================================================
echo.

REM Launch terminal dashboard using venv Python
venv\Scripts\python.exe Utils\terminal_dashboard.py --refresh 5

echo.
echo ============================================================
echo   DASHBOARD CLOSED
echo ============================================================
echo.
pause
