@echo off
REM ============================================================
REM Sentinel Corporation - Master Control Panel
REM ============================================================
REM
REM Simple menu to launch all Sentinel functions
REM ============================================================

:MENU
cls
echo.
echo ============================================================
echo   SENTINEL CORPORATION - CONTROL PANEL
echo ============================================================
echo.
echo   Current Portfolio: $65,802 (+65.80%%)
echo   Status: OPERATIONAL
echo.
echo ============================================================
echo.
echo   MAIN OPTIONS:
echo.
echo   [1] Launch Terminal Dashboard (Live Monitoring)
echo   [2] Preview Email Report (HTML)
echo   [3] Send Email Report (to your-email@gmail.com)
echo.
echo ============================================================
echo.
echo   SMS ALERTS (Twilio):
echo.
echo   [4] Send Test SMS
echo   [5] Check Portfolio Alerts
echo   [6] Send Daily SMS Summary
echo.
echo ============================================================
echo.
echo   [Q] Quit
echo.
echo ============================================================
echo.

set /p choice="Enter your choice: "

if /i "%choice%"=="1" goto DASHBOARD
if /i "%choice%"=="2" goto EMAIL_PREVIEW
if /i "%choice%"=="3" goto EMAIL_SEND
if /i "%choice%"=="4" goto SMS_TEST
if /i "%choice%"=="5" goto SMS_CHECK
if /i "%choice%"=="6" goto SMS_SUMMARY
if /i "%choice%"=="Q" goto QUIT
if /i "%choice%"=="q" goto QUIT

echo.
echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MENU

:DASHBOARD
cls
echo.
echo ============================================================
echo   LAUNCHING TERMINAL DASHBOARD
echo ============================================================
echo.
call Launch_Dashboard.bat
goto MENU

:EMAIL_PREVIEW
cls
echo.
echo ============================================================
echo   GENERATING EMAIL PREVIEW
echo ============================================================
echo.
call Preview_Email_Report.bat
goto MENU

:EMAIL_SEND
cls
echo.
echo ============================================================
echo   SENDING EMAIL REPORT
echo ============================================================
echo.
call Send_Email_Report.bat
goto MENU

:SMS_TEST
cls
echo.
echo ============================================================
echo   SENDING TEST SMS
echo ============================================================
echo.
call Test_SMS_Alert.bat
goto MENU

:SMS_CHECK
cls
echo.
echo ============================================================
echo   CHECKING PORTFOLIO ALERTS
echo ============================================================
echo.
call Check_Portfolio_Alerts.bat
goto MENU

:SMS_SUMMARY
cls
echo.
echo ============================================================
echo   SENDING DAILY SMS SUMMARY
echo ============================================================
echo.
call Send_Daily_SMS_Summary.bat
goto MENU

:QUIT
cls
echo.
echo ============================================================
echo   SENTINEL CORPORATION - SHUTTING DOWN
echo ============================================================
echo.
echo Thank you for using Sentinel Corporation!
echo.
timeout /t 2 >nul
exit
