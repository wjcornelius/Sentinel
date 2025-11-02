# ============================================================================
# Sentinel Corporation - Windows Memory Diagnostic Launcher
# ============================================================================
#
# This script schedules Windows Memory Diagnostic to test your RAM for faults
# that could be causing KERNEL_SECURITY_CHECK_FAILURE crashes.
#
# PROBATION MONITORING: Safe - Uses built-in Windows diagnostic tool
#
# SAFETY FEATURES:
# - Uses Microsoft's built-in tool (mdsched.exe)
# - Tests run before Windows loads (no interference with software)
# - Non-destructive test (only reads memory, doesn't modify)
#
# ============================================================================

#Requires -RunAsAdministrator

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  SENTINEL CORPORATION - MEMORY DIAGNOSTIC" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will test your RAM for faults." -ForegroundColor Yellow
Write-Host ""

# Initialize log
$logPath = "$PSScriptRoot\memory_diagnostic_log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log {
    param($Message)
    $logMessage = "[$timestamp] $Message"
    Add-Content -Path $logPath -Value $logMessage
    Write-Host $logMessage
}

Write-Log "=== Memory Diagnostic Launcher Started ==="
Write-Log "Computer: $env:COMPUTERNAME"
Write-Log "User: $env:USERNAME"
Write-Log ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host ""
    Write-Host "ERROR: This script requires Administrator privileges." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please right-click this script and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    Write-Log "ERROR: Script not run as administrator - exiting"
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Log "Running with Administrator privileges - OK"
Write-Host ""

# Get system memory info
Write-Host "[Step 1/3] Checking system memory..." -ForegroundColor Cyan
Write-Log "Checking system memory configuration..."

try {
    $computerSystem = Get-CimInstance -ClassName Win32_ComputerSystem
    $memory = Get-CimInstance -ClassName Win32_PhysicalMemory

    $totalMemoryGB = [math]::Round($computerSystem.TotalPhysicalMemory / 1GB, 2)

    Write-Host ""
    Write-Host "System Memory Configuration:" -ForegroundColor White
    Write-Host "  Total RAM: $totalMemoryGB GB" -ForegroundColor Gray
    Write-Host ""

    Write-Log "Total RAM: $totalMemoryGB GB"

    Write-Host "Memory Modules:" -ForegroundColor White
    foreach ($mem in $memory) {
        $capacityGB = [math]::Round($mem.Capacity / 1GB, 2)
        Write-Host "  $($mem.DeviceLocator): $capacityGB GB @ $($mem.Speed) MHz ($($mem.Manufacturer))" -ForegroundColor Gray
        Write-Log "  Memory module: $($mem.DeviceLocator) - $capacityGB GB @ $($mem.Speed) MHz"
    }

    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "WARNING: Could not retrieve memory info: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "Continuing with diagnostic anyway..." -ForegroundColor Gray
    Write-Host ""
    Write-Log "WARNING: Could not retrieve memory info - $($_.Exception.Message)"
}

# Explain what this test does
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  ABOUT WINDOWS MEMORY DIAGNOSTIC" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "What it does:" -ForegroundColor Yellow
Write-Host "  - Tests all your RAM for hardware faults" -ForegroundColor White
Write-Host "  - Runs BEFORE Windows loads (no software interference)" -ForegroundColor White
Write-Host "  - Takes 5-20 minutes depending on RAM size" -ForegroundColor White
Write-Host "  - Two test passes: Basic and Standard" -ForegroundColor White
Write-Host ""
Write-Host "Why you need this:" -ForegroundColor Yellow
Write-Host "  - KERNEL_SECURITY_CHECK_FAILURE (0x139) often indicates RAM fault" -ForegroundColor White
Write-Host "  - Faulty RAM can cause random crashes and data corruption" -ForegroundColor White
Write-Host "  - This test will identify if RAM needs replacement" -ForegroundColor White
Write-Host ""
Write-Host "What happens:" -ForegroundColor Yellow
Write-Host "  1. This script schedules the test for next restart" -ForegroundColor White
Write-Host "  2. You restart your computer now (or later)" -ForegroundColor White
Write-Host "  3. Blue screen appears with test progress bar" -ForegroundColor White
Write-Host "  4. Computer boots to Windows when test completes" -ForegroundColor White
Write-Host "  5. You check results in Event Viewer" -ForegroundColor White
Write-Host ""
Write-Host "Probation Monitoring Safety:" -ForegroundColor Cyan
Write-Host "  - Test runs BEFORE Windows loads (monitoring software not active)" -ForegroundColor White
Write-Host "  - Built-in Microsoft tool (mdsched.exe)" -ForegroundColor White
Write-Host "  - No interference with any software" -ForegroundColor White
Write-Host "  - Monitoring software resumes normally after restart" -ForegroundColor White
Write-Host ""
Write-Host "Expected test duration: 5-20 minutes (with your 8 GB RAM)" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Confirm with user
$confirmation = Read-Host "Do you want to schedule the memory diagnostic? (Y/N)"

if ($confirmation -ne 'Y' -and $confirmation -ne 'y') {
    Write-Host ""
    Write-Host "Memory diagnostic cancelled by user." -ForegroundColor Yellow
    Write-Log "Memory diagnostic cancelled by user"
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

Write-Log "User confirmed - proceeding with scheduling"
Write-Host ""

# Create instructions file for after restart
Write-Host "[Step 2/3] Creating instructions for checking results..." -ForegroundColor Cyan
Write-Log "Creating instructions file..."

$instructionsPath = "$PSScriptRoot\Memory_Test_Results_Instructions.txt"

$instructions = @"
=== Windows Memory Diagnostic - Results Instructions ===
Test Scheduled: $timestamp
Computer: $env:COMPUTERNAME

WHAT YOU JUST DID:
==================
You scheduled a Windows Memory Diagnostic test that will run when you restart.

WHAT HAPPENS DURING RESTART:
=============================
1. Computer restarts
2. Blue screen appears showing "Windows Memory Diagnostic"
3. Progress bar shows test status
4. Two passes: Basic (quick) and Standard (thorough)
5. Computer boots to Windows automatically when done
6. Results are logged in Event Viewer

TEST DURATION:
==============
Approximately 5-20 minutes (depends on RAM size and test thoroughness)

During the test, you'll see:
  - Current test pass (Pass 1 of 2, Pass 2 of 2)
  - Overall status
  - Cache tests, various pattern tests
  - DO NOT interrupt the test - let it complete

HOW TO CHECK RESULTS AFTER RESTART:
====================================

METHOD 1: Automatic Popup (Sometimes)
--------------------------------------
Windows may show a notification with results when you log in.

METHOD 2: Event Viewer (Most Reliable)
---------------------------------------
1. Press Windows Key + R
2. Type: eventvwr.msc
3. Press Enter
4. Navigate to: Windows Logs > System
5. Click "Find..." in right panel
6. Search for: MemoryDiagnostics-Results
7. Double-click the result to see details

METHOD 3: PowerShell (Quick)
-----------------------------
1. Open PowerShell as Administrator
2. Run this command:

   Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Microsoft-Windows-MemoryDiagnostics-Results'} -MaxEvents 1 | Format-List *

INTERPRETING RESULTS:
=====================

GOOD RESULT:
------------
"Windows Memory Diagnostic tested the computer's memory and detected no errors."
-> Your RAM is healthy!
-> Crashes are caused by something else (driver, software, etc.)

BAD RESULT:
-----------
"Windows Memory Diagnostic tested the computer's memory and detected hardware errors."
-> Your RAM is faulty and needs replacement
-> Contact ASUS support or computer technician
-> RAM is usually easy and inexpensive to replace

If Errors Found:
----------------
1. Note the specific error details
2. Run the test again to confirm (may be intermittent)
3. If errors persist, replace RAM
4. RAM errors cannot be fixed with software - hardware replacement required

WHAT TO DO NEXT:
================

If NO ERRORS (Good RAM):
------------------------
Continue troubleshooting:
  - Intel Graphics driver is most likely culprit (update first)
  - Power management settings (already optimized if you ran Fix_Power_Management.ps1)
  - Samsung NVMe driver (update via Samsung Magician)
  - Check Event Viewer for crash patterns

If ERRORS FOUND (Bad RAM):
---------------------------
1. Run test one more time to confirm
2. If errors persist, RAM needs replacement
3. Identify which module is faulty (if multiple modules)
4. Replace faulty RAM module
5. Computer should be stable after RAM replacement

PROBATION MONITORING NOTE:
==========================
The memory test runs BEFORE Windows loads, so your probation monitoring
software is not active during the test. It will resume normally when
Windows boots after the test completes. No interference will occur.

RUNNING THE TEST AGAIN:
========================
If you need to run the test again:
  1. Press Windows Key + R
  2. Type: mdsched.exe
  3. Click "Restart now and check for problems"

Or run this script (Run_Memory_Diagnostic.ps1) again.

NEED HELP?
==========
If you have trouble interpreting results or need assistance:
  - Check Event Viewer as described above
  - Screenshot the results
  - Contact computer technician if errors found

=== End of Instructions ===

This file will remain here: $instructionsPath
You can reference it after the test completes.
"@

$instructions | Out-File -FilePath $instructionsPath -Encoding UTF8

Write-Host ""
Write-Host "Instructions saved to:" -ForegroundColor Green
Write-Host "  $instructionsPath" -ForegroundColor Gray
Write-Host ""
Write-Host "You can refer to this file after the test to check your results." -ForegroundColor Cyan
Write-Host ""

Write-Log "Instructions file created"

# Schedule memory diagnostic
Write-Host "[Step 3/3] Scheduling Windows Memory Diagnostic..." -ForegroundColor Cyan
Write-Log "Launching Windows Memory Diagnostic scheduler..."

Write-Host ""
Write-Host "Launching Windows Memory Diagnostic..." -ForegroundColor Yellow
Write-Host ""
Write-Host "A Windows dialog will appear with two options:" -ForegroundColor White
Write-Host "  1. Restart now and check for problems (recommended)" -ForegroundColor Gray
Write-Host "  2. Check for problems the next time I start my computer" -ForegroundColor Gray
Write-Host ""
Write-Host "Choose option 1 if you're ready to restart now." -ForegroundColor Cyan
Write-Host "Choose option 2 if you want to restart later." -ForegroundColor Cyan
Write-Host ""

Write-Log "Launching mdsched.exe..."

try {
    # Launch Windows Memory Diagnostic
    Start-Process "mdsched.exe" -Wait

    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host "  MEMORY DIAGNOSTIC SCHEDULED" -ForegroundColor Green
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "The Windows Memory Diagnostic has been scheduled." -ForegroundColor White
    Write-Host ""
    Write-Host "NEXT STEPS:" -ForegroundColor Yellow
    Write-Host ""

    $restartChoice = Read-Host "Did you choose to restart now? (Y/N)"

    if ($restartChoice -eq 'Y' -or $restartChoice -eq 'y') {
        Write-Host ""
        Write-Host "Your computer will restart and the memory test will begin." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "WHAT TO EXPECT:" -ForegroundColor Yellow
        Write-Host "  1. Blue screen with 'Windows Memory Diagnostic'" -ForegroundColor White
        Write-Host "  2. Progress bar showing test status" -ForegroundColor White
        Write-Host "  3. Two test passes (5-20 minutes total)" -ForegroundColor White
        Write-Host "  4. Automatic boot to Windows when complete" -ForegroundColor White
        Write-Host ""
        Write-Host "AFTER THE TEST:" -ForegroundColor Yellow
        Write-Host "  - Log back into Windows normally" -ForegroundColor White
        Write-Host "  - Open this file for instructions on checking results:" -ForegroundColor White
        Write-Host "    $instructionsPath" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  - Or check Event Viewer: eventvwr.msc > Windows Logs > System" -ForegroundColor White
        Write-Host "    Search for: MemoryDiagnostics-Results" -ForegroundColor White
        Write-Host ""

        Write-Log "User chose to restart now - test will run immediately"

    } else {
        Write-Host ""
        Write-Host "The test will run the next time you restart your computer." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "WHEN YOU'RE READY:" -ForegroundColor Yellow
        Write-Host "  1. Save all your work" -ForegroundColor White
        Write-Host "  2. Restart your computer" -ForegroundColor White
        Write-Host "  3. Memory test will run automatically" -ForegroundColor White
        Write-Host ""
        Write-Host "AFTER THE TEST:" -ForegroundColor Yellow
        Write-Host "  - Check results using instructions in:" -ForegroundColor White
        Write-Host "    $instructionsPath" -ForegroundColor Gray
        Write-Host ""

        Write-Log "User chose to restart later - test will run at next restart"
    }

    Write-Host "PROBATION MONITORING:" -ForegroundColor Cyan
    Write-Host "  The test runs BEFORE Windows loads. Your monitoring software will" -ForegroundColor White
    Write-Host "  resume normally after Windows boots. No interference will occur." -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "ERROR: Could not launch Memory Diagnostic: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Log "ERROR: Could not launch mdsched.exe - $($_.Exception.Message)"

    Write-Host "MANUAL ALTERNATIVE:" -ForegroundColor Yellow
    Write-Host "  1. Press Windows Key + R" -ForegroundColor White
    Write-Host "  2. Type: mdsched.exe" -ForegroundColor White
    Write-Host "  3. Press Enter" -ForegroundColor White
    Write-Host "  4. Click 'Restart now and check for problems'" -ForegroundColor White
    Write-Host ""
}

Write-Host "Log saved to:" -ForegroundColor Cyan
Write-Host "  $logPath" -ForegroundColor Gray
Write-Host ""

Write-Log "=== Memory Diagnostic Launcher Session Ended ==="
Write-Log ""

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
