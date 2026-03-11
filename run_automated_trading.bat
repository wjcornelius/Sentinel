@echo off
REM ============================================================================
REM Sentinel Corporation - Automated Trading Launcher
REM Runs the automated trading script via Windows Task Scheduler
REM ============================================================================

REM Change to Sentinel directory
cd /d "C:\Users\wjcor\OneDrive\Desktop\Sentinel"

REM Activate virtual environment and run script
call venv\Scripts\activate.bat
python run_automated_trading.py

REM Deactivate (optional, script will exit anyway)
deactivate
