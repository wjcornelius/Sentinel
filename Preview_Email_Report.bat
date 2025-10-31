@echo off
REM Sentinel Corporation - Email Report Preview
REM Double-click this file to generate an HTML preview of the email report

echo ========================================
echo SENTINEL CORPORATION
echo Email Report Preview Generator
echo ========================================
echo.

cd /d "%~dp0"

echo Generating HTML preview...
echo.

python Utils\email_reporter.py ^
    --to your-email@gmail.com ^
    --from preview@sentinel.com ^
    --password dummy ^
    --test-html

if exist test_email_report.html (
    echo.
    echo ========================================
    echo Preview generated successfully!
    echo ========================================
    echo.
    echo Opening in your default browser...
    start test_email_report.html
) else (
    echo.
    echo [ERROR] Failed to generate preview!
    echo Check the console output above for errors.
    echo.
)

pause
