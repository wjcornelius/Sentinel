@echo off
REM Sentinel Corporation - End-to-End System Test
REM Double-click to test all systems

echo ========================================
echo SENTINEL CORPORATION
echo End-to-End System Test
echo ========================================
echo.

cd /d "%~dp0"

echo Running comprehensive system test...
echo This will check:
echo   - Database tables
echo   - All departments
echo   - Market data provider
echo   - Email reporter
echo   - Terminal dashboard
echo   - SMS alerter
echo   - File structure
echo.
echo ========================================
echo.

python test_end_to_end.py

echo.
echo ========================================
echo.
pause
