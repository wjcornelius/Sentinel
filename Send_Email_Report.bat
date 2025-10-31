@echo off
REM Sentinel Corporation - Email Report Sender
REM Double-click this file to send a daily summary email

echo ========================================
echo SENTINEL CORPORATION
echo Email Report Sender
echo ========================================
echo.

cd /d "%~dp0"

REM NOTE: You need to set up your Gmail app password first!
REM See: https://support.google.com/accounts/answer/185833
REM
REM Once you have your app password, edit this file and replace:
REM   YOUR_GMAIL_ADDRESS with your Gmail address
REM   YOUR_APP_PASSWORD with your 16-character app password

set SENDER_EMAIL=YOUR_GMAIL_ADDRESS
set SENDER_PASSWORD=YOUR_APP_PASSWORD
set RECIPIENT_EMAIL=YOUR_GMAIL_ADDRESS

if "%SENDER_EMAIL%"=="YOUR_GMAIL_ADDRESS" (
    echo.
    echo [ERROR] Email not configured yet!
    echo.
    echo Please edit this batch file and set:
    echo   1. SENDER_EMAIL to your Gmail address
    echo   2. SENDER_PASSWORD to your Gmail app password
    echo.
    echo To create a Gmail app password:
    echo   1. Go to: https://myaccount.google.com/apppasswords
    echo   2. Select "Mail" and "Windows Computer"
    echo   3. Click "Generate"
    echo   4. Copy the 16-character password
    echo.
    pause
    exit /b 1
)

echo Sending daily summary email to %RECIPIENT_EMAIL%...
echo.

python Utils\email_reporter.py ^
    --to %RECIPIENT_EMAIL% ^
    --from %SENDER_EMAIL% ^
    --password %SENDER_PASSWORD% ^
    --server smtp.gmail.com ^
    --port 587

echo.
echo ========================================
echo.
pause
