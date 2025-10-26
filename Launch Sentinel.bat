@echo off
REM ============================================================
REM Sentinel Trading Dashboard Launcher
REM ============================================================
REM
REM This script launches the Sentinel dashboard and opens
REM your default browser to the dashboard interface.
REM
REM Press Ctrl+C in this window to stop the dashboard server.
REM ============================================================

echo.
echo ============================================================
echo   SENTINEL TRADING DASHBOARD LAUNCHER
echo ============================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please create a virtual environment first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Check if sentinel_dashboard.py exists
if not exist "sentinel_dashboard.py" (
    echo [ERROR] sentinel_dashboard.py not found in current directory
    echo Please run this script from the Sentinel project folder
    echo.
    pause
    exit /b 1
)

REM Check if config.py exists
if not exist "config.py" (
    echo [WARNING] config.py not found!
    echo.
    echo You need to configure Sentinel before first use.
    echo Please run: python setup_config.py
    echo.
    pause
    exit /b 1
)

REM Check Flask is installed in venv
echo [INFO] Checking dependencies...
venv\Scripts\python.exe -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Flask not installed in venv!
    echo Installing Flask...
    venv\Scripts\python.exe -m pip install flask --quiet
)

echo [OK] Dependencies verified
echo.
echo ============================================================
echo   STARTING DASHBOARD SERVER
echo ============================================================
echo.
echo Dashboard will be available at: http://localhost:5000
echo.
echo Opening browser in 3 seconds...
echo.

REM Start dashboard server using venv Python
start /B venv\Scripts\python.exe sentinel_dashboard.py

REM Wait 3 seconds for server to start
timeout /t 3 /nobreak >nul

REM Open browser to dashboard
start http://localhost:5000

echo.
echo ============================================================
echo   DASHBOARD IS RUNNING
echo ============================================================
echo.
echo Control panel: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server when finished
echo.
echo ============================================================
echo.

REM Keep window open and wait for user to press Ctrl+C
pause

REM Server will terminate when window closes or Ctrl+C is pressed
