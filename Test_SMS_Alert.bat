@echo off
REM Sentinel Corporation - Test SMS Alert
REM Double-click this file to send a test SMS to your phone

echo ========================================
echo SENTINEL CORPORATION
echo Test SMS Alert
echo ========================================
echo.

cd /d "%~dp0"

echo Sending test SMS to your phone...
echo (This verifies your Twilio setup)
echo.

python Utils\sms_alerter.py --test

echo.
echo ========================================
echo.
echo If you received the SMS, your setup is working!
echo.
echo Next steps:
echo   - Use Check_Portfolio_Alerts.bat to check for real alerts
echo   - Use Send_Daily_SMS_Summary.bat for end-of-day summary
echo.
pause
