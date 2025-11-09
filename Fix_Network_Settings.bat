@echo off
REM ==============================================================================
REM Network Connectivity Fix - Phase 1
REM ==============================================================================
REM Purpose: Increase TCP/UDP port range to prevent port exhaustion
REM Safe: YES - Increases available ports for ALL software including monitoring
REM Date: November 7, 2025
REM ==============================================================================

echo.
echo ================================================================================
echo NETWORK CONNECTIVITY FIX - PHASE 1
echo ================================================================================
echo.
echo This script will:
echo   1. Show current TCP/UDP port ranges
echo   2. Increase dynamic port range from 16,384 to 55,000 ports
echo   3. Verify changes were applied
echo.
echo This is SAFE and HELPFUL for monitoring software:
echo   - MORE ports = MORE available connections
echo   - Prevents port exhaustion that causes connectivity loss
echo   - Standard Windows network optimization
echo.
echo ================================================================================
echo.

pause

echo.
echo [STEP 1] Current TCP Port Range:
echo ----------------------------------------
netsh int ipv4 show dynamicport tcp
echo.

echo [STEP 1] Current UDP Port Range:
echo ----------------------------------------
netsh int ipv4 show dynamicport udp
echo.

pause

echo.
echo [STEP 2] Increasing TCP port range to 55,000 ports...
netsh int ipv4 set dynamicport tcp start=10000 num=55000
if %errorlevel% equ 0 (
    echo SUCCESS: TCP port range increased
) else (
    echo ERROR: Failed to increase TCP port range
    echo Make sure you are running as Administrator
    pause
    exit /b 1
)
echo.

echo [STEP 2] Increasing UDP port range to 55,000 ports...
netsh int ipv4 set dynamicport udp start=10000 num=55000
if %errorlevel% equ 0 (
    echo SUCCESS: UDP port range increased
) else (
    echo ERROR: Failed to increase UDP port range
    pause
    exit /b 1
)
echo.

echo [STEP 3] Verifying new settings...
echo ----------------------------------------
echo.
echo New TCP Port Range:
netsh int ipv4 show dynamicport tcp
echo.
echo New UDP Port Range:
netsh int ipv4 show dynamicport udp
echo.

echo ================================================================================
echo PHASE 1 COMPLETE
echo ================================================================================
echo.
echo Changes applied successfully!
echo.
echo BEFORE: 16,384 ports (default)
echo AFTER:  55,000 ports (3.4x more available connections)
echo.
echo Benefits:
echo   - Prevents port exhaustion
echo   - Reduces "TCP/IP failed to establish connection" errors
echo   - MORE reliable connectivity for ALL software (including monitoring)
echo.
echo IMPORTANT: A reboot is recommended for full effect, but not required.
echo.
echo ================================================================================
echo.

pause
