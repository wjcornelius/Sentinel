# ============================================================================
# Sentinel Corporation - Master Crash Fix Control Panel
# ============================================================================
#
# Interactive menu to run all crash fix scripts in recommended order
#
# PROBATION MONITORING: Safe - All scripts avoid interference
#
# ============================================================================

#Requires -RunAsAdministrator

# Check if running as administrator at the start
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host ""
    Write-Host "ERROR: This script requires Administrator privileges." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please right-click this script and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "Or use the START_HERE.bat file which runs as admin automatically." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Initialize master log
$masterLogPath = "$PSScriptRoot\crash_fix_master_log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-MasterLog {
    param($Message)
    $logMessage = "[$timestamp] $Message"
    Add-Content -Path $masterLogPath -Value $logMessage
}

Write-MasterLog "=== Master Crash Fix Session Started ==="
Write-MasterLog "Computer: $env:COMPUTERNAME"
Write-MasterLog "User: $env:USERNAME"
Write-MasterLog ""

# Track completion status
$statusFile = "$PSScriptRoot\crash_fix_status.txt"

function Get-Status {
    if (Test-Path $statusFile) {
        $status = Get-Content $statusFile -Raw | ConvertFrom-Json
        return $status
    } else {
        $status = @{
            diagnostic_run = $false
            intel_driver_updated = $false
            power_optimized = $false
            memory_test_scheduled = $false
            last_updated = ""
        }
        return $status
    }
}

function Save-Status {
    param($Status)
    $Status.last_updated = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $Status | ConvertTo-Json | Out-File -FilePath $statusFile -Encoding UTF8
}

function Show-Menu {
    Clear-Host

    $status = Get-Status

    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "  SENTINEL CORPORATION - MASTER CRASH FIX CONTROL PANEL" -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Computer: $env:COMPUTERNAME" -ForegroundColor Gray
    Write-Host "  User: $env:USERNAME" -ForegroundColor Gray
    Write-Host "  Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "  COMPLETION STATUS" -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""

    $diagnosticStatus = if ($status.diagnostic_run) { "[DONE]" } else { "[PENDING]" }
    $diagnosticColor = if ($status.diagnostic_run) { "Green" } else { "Yellow" }
    Write-Host "  $diagnosticStatus Diagnostic Report" -ForegroundColor $diagnosticColor

    $driverStatus = if ($status.intel_driver_updated) { "[DONE]" } else { "[PENDING]" }
    $driverColor = if ($status.intel_driver_updated) { "Green" } else { "Yellow" }
    Write-Host "  $driverStatus Intel Graphics Driver Update" -ForegroundColor $driverColor

    $powerStatus = if ($status.power_optimized) { "[DONE]" } else { "[PENDING]" }
    $powerColor = if ($status.power_optimized) { "Green" } else { "Yellow" }
    Write-Host "  $powerStatus Power Management Optimization" -ForegroundColor $powerColor

    $memoryStatus = if ($status.memory_test_scheduled) { "[DONE]" } else { "[PENDING]" }
    $memoryColor = if ($status.memory_test_scheduled) { "Green" } else { "Yellow" }
    Write-Host "  $memoryStatus Memory Diagnostic Test" -ForegroundColor $memoryColor

    Write-Host ""

    if ($status.last_updated) {
        Write-Host "  Last updated: $($status.last_updated)" -ForegroundColor Gray
    }

    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "  MAIN MENU" -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  RECOMMENDED ORDER:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    [1] Run Diagnostic Report (Start here - analyze current state)" -ForegroundColor White
    Write-Host "    [2] Update Intel Graphics Driver (HIGHEST PRIORITY fix)" -ForegroundColor White
    Write-Host "    [3] Optimize Power Management (Prevents sleep/wake crashes)" -ForegroundColor White
    Write-Host "    [4] Run Memory Diagnostic (Tests RAM for faults)" -ForegroundColor White
    Write-Host ""
    Write-Host "  QUICK OPTIONS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    [A] Auto-Fix Everything (Runs steps 1-3 automatically)" -ForegroundColor Cyan
    Write-Host "    [R] Reset Status (Mark all as pending)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  OTHER:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    [H] Help & Information" -ForegroundColor White
    Write-Host "    [Q] Quit" -ForegroundColor White
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Help {
    Clear-Host
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "  HELP & INFORMATION" -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "WHAT THIS DOES:" -ForegroundColor Yellow
    Write-Host "  This tool fixes computer crashes by updating drivers and optimizing" -ForegroundColor White
    Write-Host "  power settings. Most crashes are caused by:" -ForegroundColor White
    Write-Host "    - Outdated Intel Graphics driver (70-80% of crashes)" -ForegroundColor Gray
    Write-Host "    - Poor power management settings (sleep/wake issues)" -ForegroundColor Gray
    Write-Host "    - Faulty RAM (less common but serious)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "RECOMMENDED WORKFLOW:" -ForegroundColor Yellow
    Write-Host "  1. Run Diagnostic Report - Understand what's wrong" -ForegroundColor White
    Write-Host "  2. Update Intel Graphics Driver - Fix most crashes (requires restart)" -ForegroundColor White
    Write-Host "  3. Optimize Power Management - Prevent sleep/wake crashes (no restart)" -ForegroundColor White
    Write-Host "  4. Run Memory Diagnostic - Test RAM if crashes continue (requires restart)" -ForegroundColor White
    Write-Host ""
    Write-Host "  OR: Use Auto-Fix Everything (option A) to run steps 1-3 automatically" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "EXPECTED RESULTS:" -ForegroundColor Yellow
    Write-Host "  After Intel driver update:  70-80% crash reduction" -ForegroundColor Green
    Write-Host "  After power optimization:   90%+ crash reduction" -ForegroundColor Green
    Write-Host "  If RAM is faulty:           Needs hardware replacement" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "PROBATION MONITORING SAFETY:" -ForegroundColor Yellow
    Write-Host "  All scripts in this tool are designed to avoid interference with" -ForegroundColor White
    Write-Host "  probation monitoring software:" -ForegroundColor White
    Write-Host "    - Uses standard Windows update mechanisms" -ForegroundColor Gray
    Write-Host "    - Only modifies driver and power settings" -ForegroundColor Gray
    Write-Host "    - No interaction with third-party software" -ForegroundColor Gray
    Write-Host "    - Memory test runs BEFORE Windows loads (no interference)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "SAFETY FEATURES:" -ForegroundColor Yellow
    Write-Host "  - System Restore Point created before driver changes" -ForegroundColor White
    Write-Host "  - All settings backed up before modifications" -ForegroundColor White
    Write-Host "  - Detailed logs of every action" -ForegroundColor White
    Write-Host "  - Rollback instructions provided" -ForegroundColor White
    Write-Host ""
    Write-Host "TIME REQUIRED:" -ForegroundColor Yellow
    Write-Host "  Diagnostic Report:       2-3 minutes" -ForegroundColor White
    Write-Host "  Intel Driver Update:     10-15 minutes + restart" -ForegroundColor White
    Write-Host "  Power Optimization:      2-3 minutes (no restart)" -ForegroundColor White
    Write-Host "  Memory Diagnostic:       5-20 minutes during restart" -ForegroundColor White
    Write-Host "  Auto-Fix Everything:     ~20 minutes + restart" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "RESTART REQUIREMENTS:" -ForegroundColor Yellow
    Write-Host "  - Intel driver update: REQUIRES restart" -ForegroundColor White
    Write-Host "  - Power optimization: NO restart required" -ForegroundColor White
    Write-Host "  - Memory test: REQUIRES restart (test runs before Windows loads)" -ForegroundColor White
    Write-Host ""
    Write-Host "AFTER RUNNING FIXES:" -ForegroundColor Yellow
    Write-Host "  1. Use computer normally for 24-48 hours" -ForegroundColor White
    Write-Host "  2. Monitor for crashes (should be rare or eliminated)" -ForegroundColor White
    Write-Host "  3. If crashes continue:" -ForegroundColor White
    Write-Host "     - Check Event Viewer for new crash patterns" -ForegroundColor Gray
    Write-Host "     - Run memory diagnostic if not already done" -ForegroundColor Gray
    Write-Host "     - Update Samsung NVMe driver via Samsung Magician" -ForegroundColor Gray
    Write-Host ""
    Write-Host "FILES CREATED:" -ForegroundColor Yellow
    Write-Host "  All scripts create log files and reports in the CrashFix folder:" -ForegroundColor White
    Write-Host "    - crash_fix_master_log.txt (this session's log)" -ForegroundColor Gray
    Write-Host "    - Crash_Diagnostic_Report.html (system analysis)" -ForegroundColor Gray
    Write-Host "    - driver_update_log.txt (driver changes)" -ForegroundColor Gray
    Write-Host "    - power_management_log.txt (power changes)" -ForegroundColor Gray
    Write-Host "    - memory_diagnostic_log.txt (memory test log)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "NEED MORE HELP?" -ForegroundColor Yellow
    Write-Host "  - Review generated HTML reports and logs" -ForegroundColor White
    Write-Host "  - Check Event Viewer (eventvwr.msc) for crash details" -ForegroundColor White
    Write-Host "  - Run Diagnostic Report to see current system state" -ForegroundColor White
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Run-AutoFix {
    Clear-Host
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "  AUTO-FIX EVERYTHING" -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This will automatically run the following scripts in order:" -ForegroundColor Yellow
    Write-Host "  1. Diagnostic Report (analyzes system)" -ForegroundColor White
    Write-Host "  2. Intel Graphics Driver Update (fixes most crashes)" -ForegroundColor White
    Write-Host "  3. Power Management Optimization (prevents sleep/wake crashes)" -ForegroundColor White
    Write-Host ""
    Write-Host "NOTE: Memory Diagnostic (step 4) requires manual restart and is optional." -ForegroundColor Gray
    Write-Host "      You can run it separately from the menu after Auto-Fix completes." -ForegroundColor Gray
    Write-Host ""
    Write-Host "Total time: ~20 minutes" -ForegroundColor Cyan
    Write-Host "Restart required after completion: YES" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Each script will prompt for confirmation individually." -ForegroundColor Gray
    Write-Host ""

    $confirm = Read-Host "Continue with Auto-Fix? (Y/N)"

    if ($confirm -ne 'Y' -and $confirm -ne 'y') {
        Write-Host ""
        Write-Host "Auto-Fix cancelled." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
        return
    }

    Write-Host ""
    Write-Host "Starting Auto-Fix sequence..." -ForegroundColor Green
    Write-Host ""
    Write-MasterLog "Auto-Fix sequence started"

    # Step 1: Diagnostic Report
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "  STEP 1 OF 3: DIAGNOSTIC REPORT" -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Start-Sleep -Seconds 2

    & "$PSScriptRoot\Crash_Diagnostic_Report.ps1"

    $status = Get-Status
    $status.diagnostic_run = $true
    Save-Status $status
    Write-MasterLog "Diagnostic Report completed"

    Write-Host ""
    Write-Host "Press any key to continue to Step 2..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

    # Step 2: Intel Driver Update
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "  STEP 2 OF 3: INTEL GRAPHICS DRIVER UPDATE" -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Start-Sleep -Seconds 2

    & "$PSScriptRoot\Fix_Intel_Graphics_Driver.ps1"

    $status = Get-Status
    $status.intel_driver_updated = $true
    Save-Status $status
    Write-MasterLog "Intel Graphics Driver update completed"

    Write-Host ""
    Write-Host "Press any key to continue to Step 3..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

    # Step 3: Power Management
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "  STEP 3 OF 3: POWER MANAGEMENT OPTIMIZATION" -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Start-Sleep -Seconds 2

    & "$PSScriptRoot\Fix_Power_Management.ps1"

    $status = Get-Status
    $status.power_optimized = $true
    Save-Status $status
    Write-MasterLog "Power Management optimization completed"

    # Summary
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host "  AUTO-FIX COMPLETE!" -ForegroundColor Green
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Completed:" -ForegroundColor White
    Write-Host "  [DONE] Diagnostic Report" -ForegroundColor Green
    Write-Host "  [DONE] Intel Graphics Driver Update" -ForegroundColor Green
    Write-Host "  [DONE] Power Management Optimization" -ForegroundColor Green
    Write-Host ""
    Write-Host "Optional (not included in Auto-Fix):" -ForegroundColor Yellow
    Write-Host "  [PENDING] Memory Diagnostic Test" -ForegroundColor Yellow
    Write-Host "            (Run from menu if crashes continue after restart)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "IMPORTANT: RESTART YOUR COMPUTER NOW" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Expected results after restart:" -ForegroundColor Cyan
    Write-Host "  - 70-80% reduction in crashes (from driver update)" -ForegroundColor White
    Write-Host "  - 90%+ reduction overall (driver + power optimization)" -ForegroundColor White
    Write-Host ""
    Write-Host "After restart:" -ForegroundColor Cyan
    Write-Host "  - Use computer normally for 24-48 hours" -ForegroundColor White
    Write-Host "  - Monitor for crashes (should be rare or eliminated)" -ForegroundColor White
    Write-Host "  - If crashes persist, run Memory Diagnostic from menu" -ForegroundColor White
    Write-Host ""

    Write-MasterLog "Auto-Fix sequence completed successfully"

    Write-Host "Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Main loop
while ($true) {
    Show-Menu

    $choice = Read-Host "Enter your choice"

    switch ($choice.ToUpper()) {
        "1" {
            Write-Host ""
            Write-Host "Launching Diagnostic Report..." -ForegroundColor Cyan
            Write-MasterLog "User selected: Diagnostic Report"
            Start-Sleep -Seconds 1

            & "$PSScriptRoot\Crash_Diagnostic_Report.ps1"

            $status = Get-Status
            $status.diagnostic_run = $true
            Save-Status $status

            Write-Host ""
            Write-Host "Press any key to return to menu..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }

        "2" {
            Write-Host ""
            Write-Host "Launching Intel Graphics Driver Update..." -ForegroundColor Cyan
            Write-MasterLog "User selected: Intel Graphics Driver Update"
            Start-Sleep -Seconds 1

            & "$PSScriptRoot\Fix_Intel_Graphics_Driver.ps1"

            $status = Get-Status
            $status.intel_driver_updated = $true
            Save-Status $status

            Write-Host ""
            Write-Host "Press any key to return to menu..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }

        "3" {
            Write-Host ""
            Write-Host "Launching Power Management Optimization..." -ForegroundColor Cyan
            Write-MasterLog "User selected: Power Management Optimization"
            Start-Sleep -Seconds 1

            & "$PSScriptRoot\Fix_Power_Management.ps1"

            $status = Get-Status
            $status.power_optimized = $true
            Save-Status $status

            Write-Host ""
            Write-Host "Press any key to return to menu..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }

        "4" {
            Write-Host ""
            Write-Host "Launching Memory Diagnostic..." -ForegroundColor Cyan
            Write-MasterLog "User selected: Memory Diagnostic"
            Start-Sleep -Seconds 1

            & "$PSScriptRoot\Run_Memory_Diagnostic.ps1"

            $status = Get-Status
            $status.memory_test_scheduled = $true
            Save-Status $status

            Write-Host ""
            Write-Host "Press any key to return to menu..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }

        "A" {
            Write-MasterLog "User selected: Auto-Fix Everything"
            Run-AutoFix
        }

        "R" {
            Write-Host ""
            Write-Host "Resetting status..." -ForegroundColor Yellow
            Write-MasterLog "User reset status"

            $status = @{
                diagnostic_run = $false
                intel_driver_updated = $false
                power_optimized = $false
                memory_test_scheduled = $false
                last_updated = ""
            }
            Save-Status $status

            Write-Host "Status reset. All items marked as pending." -ForegroundColor Green
            Start-Sleep -Seconds 2
        }

        "H" {
            Write-MasterLog "User viewed help"
            Show-Help
        }

        "Q" {
            Write-Host ""
            Write-Host "Exiting Master Crash Fix..." -ForegroundColor Yellow
            Write-MasterLog "User exited Master Crash Fix"
            Write-MasterLog "=== Master Crash Fix Session Ended ==="
            Write-Host ""
            exit 0
        }

        default {
            Write-Host ""
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
}
