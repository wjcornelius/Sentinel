@echo off
REM Sentinel Corporation - Send Daily SMS Summary
REM Double-click this file to send end-of-day SMS summary

echo ========================================
echo SENTINEL CORPORATION
echo Daily SMS Summary Sender
echo ========================================
echo.

cd /d "%~dp0"

echo Sending daily summary SMS to your phone...
echo (Brief P/L, Sharpe, and Win Rate)
echo.

python Utils\sms_alerter.py --summary

echo.
echo ========================================
echo.
echo You can schedule this to run daily at 4:30 PM ET
echo using Windows Task Scheduler (Week 7 Day 5)
echo.
pause
