@echo off
REM Sentinel Corporation - Check Portfolio Alerts
REM Double-click this file to check if any alert thresholds are exceeded

echo ========================================
echo SENTINEL CORPORATION
echo Portfolio Alert Checker
echo ========================================
echo.

cd /d "%~dp0"

echo Checking portfolio for alert conditions...
echo.
echo Alert Thresholds:
echo   - Daily P/L moves ^>5%%
echo   - Portfolio milestones ($100K, $250K, $500K, $1M)
echo   - Unhealthy departments
echo   - Win rate ^<50%%
echo   - Sharpe ratio ^<1.0
echo.
echo ========================================
echo.

python Utils\sms_alerter.py --check

echo.
echo ========================================
echo.
pause
