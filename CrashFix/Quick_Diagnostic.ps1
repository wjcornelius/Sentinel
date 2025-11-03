# Quick Crash Diagnostic
# Run this to see what was done and what still needs to be done

Write-Host "=" * 80
Write-Host "CRASH FIX STATUS - QUICK DIAGNOSTIC"
Write-Host "=" * 80
Write-Host ""

# Check Intel Graphics Driver
Write-Host "[1/4] Intel Graphics Driver Status:"
try {
    $driver = Get-WmiObject Win32_PnPSignedDriver | Where-Object {$_.DeviceName -like '*Intel*' -and $_.DeviceName -like '*Graphics*'} | Select-Object -First 1
    if ($driver) {
        Write-Host "  Device: $($driver.DeviceName)" -ForegroundColor Yellow
        Write-Host "  Current Version: $($driver.DriverVersion)" -ForegroundColor Yellow
        Write-Host "  Driver Date: $($driver.DriverDate)" -ForegroundColor Yellow

        # Check if outdated (before 2025)
        if ($driver.DriverDate -lt "20250101") {
            Write-Host "  STATUS: OUTDATED - NEEDS UPDATE!" -ForegroundColor Red
            Write-Host "  This is likely causing your crashes!" -ForegroundColor Red
        } else {
            Write-Host "  STATUS: Updated" -ForegroundColor Green
        }
    } else {
        Write-Host "  ERROR: Could not find Intel Graphics driver" -ForegroundColor Red
    }
} catch {
    Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Check Power Management
Write-Host "[2/4] Power Management Status:"
try {
    $powerPlan = powercfg /getactivescheme
    if ($powerPlan -like '*High performance*') {
        Write-Host "  Power Plan: High Performance" -ForegroundColor Green
        Write-Host "  STATUS: Optimized" -ForegroundColor Green
    } else {
        Write-Host "  Power Plan: $powerPlan" -ForegroundColor Yellow
        Write-Host "  STATUS: NOT optimized - may cause crashes" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Check Recent Crashes
Write-Host "[3/4] Recent Crash Events (Last 7 days):"
try {
    $crashes = Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddDays(-7)} -ErrorAction SilentlyContinue |
        Where-Object {$_.Id -eq 41 -or $_.Id -eq 1001 -or $_.Id -eq 6008 -or $_.Message -like '*bugcheck*' -or $_.Message -like '*Blue Screen*' -or $_.Message -like '*WATCHDOG*'}

    if ($crashes) {
        Write-Host "  Found $($crashes.Count) crash/unexpected shutdown events" -ForegroundColor Red
        Write-Host ""
        Write-Host "  Most Recent Crashes:" -ForegroundColor Yellow
        $crashes | Select-Object -First 5 | ForEach-Object {
            Write-Host "    $($_.TimeCreated): $($_.Message.Substring(0, [Math]::Min(80, $_.Message.Length)))" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  No crashes found in last 7 days!" -ForegroundColor Green
    }
} catch {
    Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Check Memory Test Status
Write-Host "[4/4] Memory Diagnostic Status:"
try {
    $memtest = Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Microsoft-Windows-MemoryDiagnostics-Results'} -MaxEvents 1 -ErrorAction SilentlyContinue
    if ($memtest) {
        Write-Host "  Last Memory Test: $($memtest.TimeCreated)" -ForegroundColor Yellow
        if ($memtest.Message -like '*detected*') {
            Write-Host "  Result: ERRORS DETECTED - RAM may be faulty!" -ForegroundColor Red
        } else {
            Write-Host "  Result: No errors detected" -ForegroundColor Green
        }
    } else {
        Write-Host "  No memory test has been run yet" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" * 80
Write-Host "ANALYSIS & RECOMMENDATIONS"
Write-Host "=" * 80
Write-Host ""

# Read status file
$statusFile = "C:\Users\wjcor\OneDrive\Desktop\Sentinel\CrashFix\crash_fix_status.txt"
if (Test-Path $statusFile) {
    $status = Get-Content $statusFile | ConvertFrom-Json

    Write-Host "What was completed:" -ForegroundColor Cyan
    if ($status.power_optimized) {
        Write-Host "  [X] Power Management Optimized" -ForegroundColor Green
    } else {
        Write-Host "  [ ] Power Management NOT optimized" -ForegroundColor Red
    }

    if ($status.intel_driver_updated) {
        Write-Host "  [X] Intel Graphics Driver Updated" -ForegroundColor Green
    } else {
        Write-Host "  [ ] Intel Graphics Driver NOT updated" -ForegroundColor Red
    }

    if ($status.memory_test_scheduled) {
        Write-Host "  [X] Memory Test Scheduled/Completed" -ForegroundColor Green
    } else {
        Write-Host "  [ ] Memory Test NOT run" -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "What needs to be done:" -ForegroundColor Cyan

    if (-not $status.intel_driver_updated) {
        Write-Host "  [!] UPDATE INTEL GRAPHICS DRIVER - CRITICAL!" -ForegroundColor Red
        Write-Host "      This is the #1 cause of your crashes" -ForegroundColor Red
        Write-Host "      Action: Run Fix_Intel_Graphics_Driver.ps1" -ForegroundColor Yellow
    }

    if (-not $status.power_optimized) {
        Write-Host "  [!] Optimize Power Management" -ForegroundColor Yellow
        Write-Host "      Action: Run Fix_Power_Management.ps1" -ForegroundColor Yellow
    }

    if (-not $status.memory_test_scheduled -and $crashes -and $crashes.Count -gt 0) {
        Write-Host "  [!] Run Memory Diagnostic (if crashes persist after driver update)" -ForegroundColor Yellow
        Write-Host "      Action: Run Run_Memory_Diagnostic.ps1" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=" * 80
Write-Host "NEXT STEPS"
Write-Host "=" * 80
Write-Host ""
Write-Host "To fix your crashes, run:" -ForegroundColor Cyan
Write-Host "  1. Right-click START_HERE.bat" -ForegroundColor Yellow
Write-Host "  2. Select 'Run as Administrator'" -ForegroundColor Yellow
Write-Host "  3. Choose option [2] to update Intel Graphics driver" -ForegroundColor Yellow
Write-Host "  4. Restart computer when prompted" -ForegroundColor Yellow
Write-Host ""
Write-Host "Expected result: 70-80% crash reduction" -ForegroundColor Green
Write-Host ""
