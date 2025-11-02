@echo off
REM ============================================================================
REM Sentinel Corporation - Crash Fix Launcher
REM ============================================================================
REM
REM This batch file launches the Master Crash Fix control panel with
REM Administrator privileges (required for driver updates and power settings).
REM
REM PROBATION MONITORING: Safe - All scripts avoid interference
REM
REM ============================================================================

echo.
echo ============================================================================
echo   SENTINEL CORPORATION - CRASH FIX LAUNCHER
echo ============================================================================
echo.
echo   This tool will fix your computer crashes by:
echo     1. Updating Intel Graphics driver (fixes 70-80%% of crashes)
echo     2. Optimizing power settings (prevents sleep/wake crashes)
echo     3. Testing RAM for faults (if needed)
echo.
echo   Probation Monitoring Safety:
echo     All scripts use standard Windows update mechanisms and avoid
echo     any interference with monitoring software.
echo.
echo ============================================================================
echo.
echo   Launching Master Control Panel with Administrator privileges...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if already running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo   Already running as Administrator - launching directly...
    echo.
    powershell.exe -ExecutionPolicy Bypass -File "Master_Crash_Fix.ps1"
) else (
    echo   Requesting Administrator privileges...
    echo   (You may see a UAC prompt - click Yes to continue)
    echo.
    powershell.exe -Command "Start-Process powershell.exe -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0Master_Crash_Fix.ps1\"' -Verb RunAs"
)

exit
