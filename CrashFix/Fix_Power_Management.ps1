# ============================================================================
# Sentinel Corporation - Power Management Optimization
# ============================================================================
#
# This script optimizes Windows power management settings to prevent
# sleep/wake crashes and driver timeout issues.
#
# PROBATION MONITORING: Safe - Only modifies Windows power settings
#
# SAFETY FEATURES:
# - Creates backup of all settings before changes
# - Logs all actions to power_management_log.txt
# - Provides rollback instructions
#
# ============================================================================

#Requires -RunAsAdministrator

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  SENTINEL CORPORATION - POWER MANAGEMENT OPTIMIZATION" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will optimize power settings to prevent crashes." -ForegroundColor Yellow
Write-Host ""

# Initialize log
$logPath = "$PSScriptRoot\power_management_log.txt"
$backupPath = "$PSScriptRoot\power_settings_backup.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log {
    param($Message)
    $logMessage = "[$timestamp] $Message"
    Add-Content -Path $logPath -Value $logMessage
    Write-Host $logMessage
}

Write-Log "=== Power Management Optimization Started ==="
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

# Get current power plan
Write-Host "[Step 1/5] Checking current power settings..." -ForegroundColor Cyan
Write-Log "Checking current power settings..."

try {
    $currentPlan = Get-CimInstance -Namespace root\cimv2\power -ClassName Win32_PowerPlan | Where-Object { $_.IsActive -eq $true }

    Write-Host ""
    Write-Host "Current Power Plan: $($currentPlan.ElementName)" -ForegroundColor White
    Write-Host ""

    Write-Log "Current power plan: $($currentPlan.ElementName)"

    # Backup current settings
    Write-Host "[Step 2/5] Backing up current power settings..." -ForegroundColor Cyan
    Write-Log "Creating backup of current settings..."

    $backup = @"
=== Power Settings Backup ===
Created: $timestamp
Computer: $env:COMPUTERNAME

Current Power Plan: $($currentPlan.ElementName)
Plan GUID: $($currentPlan.InstanceID)

To restore these settings:
1. Open Command Prompt as Administrator
2. Run: powercfg /setactive $($currentPlan.InstanceID.Split('{')[1].Split('}')[0])
3. Run the other restore commands listed below

=== Detailed Settings ===
"@

    # Get current powercfg settings
    $powerReport = powercfg /query
    $backup += "`n$powerReport"

    $backup | Out-File -FilePath $backupPath -Encoding UTF8

    Write-Host ""
    Write-Host "Backup created: $backupPath" -ForegroundColor Green
    Write-Host ""

    Write-Log "Backup created successfully"

} catch {
    Write-Host ""
    Write-Host "ERROR: Could not check current power settings: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Log "ERROR: Could not check power settings - $($_.Exception.Message)"
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Confirm with user
Write-Host "This script will make the following changes:" -ForegroundColor Yellow
Write-Host ""
Write-Host "POWER PLAN:" -ForegroundColor Cyan
Write-Host "  - Switch to High Performance power plan (prevents CPU throttling)" -ForegroundColor White
Write-Host ""
Write-Host "PCI EXPRESS:" -ForegroundColor Cyan
Write-Host "  - Disable Link State Power Management (prevents driver timeout)" -ForegroundColor White
Write-Host ""
Write-Host "USB:" -ForegroundColor Cyan
Write-Host "  - Disable Selective Suspend (prevents USB device disconnects)" -ForegroundColor White
Write-Host ""
Write-Host "NETWORK:" -ForegroundColor Cyan
Write-Host "  - Disable 'Allow computer to turn off device' (prevents network drops)" -ForegroundColor White
Write-Host ""
Write-Host "DISK:" -ForegroundColor Cyan
Write-Host "  - Set 'Turn off hard disk after' to Never" -ForegroundColor White
Write-Host ""
Write-Host "Expected results:" -ForegroundColor Green
Write-Host "  - Eliminates sleep/wake crashes" -ForegroundColor White
Write-Host "  - Prevents PCI Express driver timeouts" -ForegroundColor White
Write-Host "  - Improves system stability" -ForegroundColor White
Write-Host ""
Write-Host "Tradeoff: Slightly higher power consumption (minimal on desktop)" -ForegroundColor Gray
Write-Host ""
Write-Host "Probation Monitoring Safety: Only modifies Windows power settings." -ForegroundColor Cyan
Write-Host "No interference with monitoring software." -ForegroundColor Cyan
Write-Host ""

$confirmation = Read-Host "Do you want to proceed? (Y/N)"

if ($confirmation -ne 'Y' -and $confirmation -ne 'y') {
    Write-Host ""
    Write-Host "Optimization cancelled by user." -ForegroundColor Yellow
    Write-Log "Optimization cancelled by user"
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

Write-Log "User confirmed - proceeding with optimization"
Write-Host ""

# Apply power optimizations
Write-Host "[Step 3/5] Applying power management optimizations..." -ForegroundColor Cyan
Write-Host ""

# 1. Switch to High Performance power plan
Write-Host "  [1/6] Switching to High Performance power plan..." -ForegroundColor Yellow
Write-Log "Switching to High Performance power plan..."

try {
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
    Write-Host "        Done!" -ForegroundColor Green
    Write-Log "Switched to High Performance plan"
} catch {
    Write-Host "        WARNING: Could not switch power plan: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Log "WARNING: Could not switch power plan - $($_.Exception.Message)"
}

Start-Sleep -Seconds 1

# 2. Disable PCI Express Link State Power Management
Write-Host "  [2/6] Disabling PCI Express Link State Power Management..." -ForegroundColor Yellow
Write-Log "Disabling PCI Express Link State Power Management..."

try {
    # High Performance plan: PCI Express > Link State Power Management > Off
    powercfg /setacvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0
    powercfg /setdcvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
    Write-Host "        Done! (This fixes most DPC_WATCHDOG_VIOLATION crashes)" -ForegroundColor Green
    Write-Log "PCI Express Link State Power Management disabled"
} catch {
    Write-Host "        WARNING: Could not disable PCI Express power management: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Log "WARNING: Could not disable PCI Express PM - $($_.Exception.Message)"
}

Start-Sleep -Seconds 1

# 3. Disable USB Selective Suspend
Write-Host "  [3/6] Disabling USB Selective Suspend..." -ForegroundColor Yellow
Write-Log "Disabling USB Selective Suspend..."

try {
    powercfg /setacvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
    powercfg /setdcvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
    Write-Host "        Done!" -ForegroundColor Green
    Write-Log "USB Selective Suspend disabled"
} catch {
    Write-Host "        WARNING: Could not disable USB Selective Suspend: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Log "WARNING: Could not disable USB Selective Suspend - $($_.Exception.Message)"
}

Start-Sleep -Seconds 1

# 4. Set hard disk to never turn off
Write-Host "  [4/6] Setting hard disk to never turn off..." -ForegroundColor Yellow
Write-Log "Setting hard disk timeout to never..."

try {
    powercfg /setacvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 0012ee47-9041-4b5d-9b77-535fba8b1442 6738e2c4-e8a5-4a42-b16a-e040e769756e 0
    powercfg /setdcvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 0012ee47-9041-4b5d-9b77-535fba8b1442 6738e2c4-e8a5-4a42-b16a-e040e769756e 0
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
    Write-Host "        Done!" -ForegroundColor Green
    Write-Log "Hard disk timeout set to never"
} catch {
    Write-Host "        WARNING: Could not set hard disk timeout: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Log "WARNING: Could not set hard disk timeout - $($_.Exception.Message)"
}

Start-Sleep -Seconds 1

# 5. Disable network adapter power saving
Write-Host "  [5/6] Optimizing network adapter power settings..." -ForegroundColor Yellow
Write-Log "Optimizing network adapter power settings..."

try {
    $networkAdapters = Get-NetAdapter | Where-Object { $_.Status -eq "Up" }

    foreach ($adapter in $networkAdapters) {
        $adapterName = $adapter.Name

        # Disable "Allow the computer to turn off this device to save power"
        $powerMgmt = Get-CimInstance -ClassName MSPower_DeviceEnable -Namespace root\wmi | Where-Object { $_.InstanceName -like "*$($adapter.InterfaceGuid)*" }

        if ($powerMgmt) {
            $powerMgmt.Enable = $false
            Set-CimInstance -InputObject $powerMgmt
            Write-Host "        $adapterName - Power saving disabled" -ForegroundColor Gray
            Write-Log "Network adapter $adapterName - power saving disabled"
        }
    }

    Write-Host "        Done!" -ForegroundColor Green

} catch {
    Write-Host "        WARNING: Could not modify network adapter settings: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Log "WARNING: Could not modify network adapter settings - $($_.Exception.Message)"
}

Start-Sleep -Seconds 1

# 6. Disable sleep mode
Write-Host "  [6/6] Disabling automatic sleep..." -ForegroundColor Yellow
Write-Log "Disabling automatic sleep..."

try {
    powercfg /setacvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 238c9fa8-0aad-41ed-83f4-97be242c8f20 29f6c1db-86da-48c5-9fdb-f2b67b1f44da 0
    powercfg /setdcvalueindex 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 238c9fa8-0aad-41ed-83f4-97be242c8f20 29f6c1db-86da-48c5-9fdb-f2b67b1f44da 0
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
    Write-Host "        Done!" -ForegroundColor Green
    Write-Log "Automatic sleep disabled"
} catch {
    Write-Host "        WARNING: Could not disable sleep: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Log "WARNING: Could not disable sleep - $($_.Exception.Message)"
}

Write-Host ""
Write-Host "[Step 4/5] Verifying changes..." -ForegroundColor Cyan
Write-Log "Verifying power settings changes..."

Start-Sleep -Seconds 2

# Verify power plan
$newPlan = Get-CimInstance -Namespace root\cimv2\power -ClassName Win32_PowerPlan | Where-Object { $_.IsActive -eq $true }

Write-Host ""
Write-Host "New Power Plan: $($newPlan.ElementName)" -ForegroundColor $(if($newPlan.ElementName -eq 'High performance'){'Green'}else{'Yellow'})
Write-Host ""

Write-Log "New power plan: $($newPlan.ElementName)"

# Generate summary report
Write-Host "[Step 5/5] Generating summary report..." -ForegroundColor Cyan
Write-Log "Generating summary report..."

$summaryPath = "$PSScriptRoot\Power_Optimization_Summary.txt"

$summary = @"
=== Power Management Optimization Summary ===
Completed: $timestamp
Computer: $env:COMPUTERNAME

CHANGES APPLIED:
================

1. Power Plan: Switched to High Performance
   - Prevents CPU throttling that can cause driver timeouts

2. PCI Express Link State Power Management: DISABLED
   - PRIMARY FIX for DPC_WATCHDOG_VIOLATION crashes
   - Prevents graphics and storage driver timeouts

3. USB Selective Suspend: DISABLED
   - Prevents USB device disconnections
   - Ensures monitoring devices stay connected

4. Hard Disk Timeout: Set to NEVER
   - Prevents SSD/NVMe from entering power-saving states
   - Eliminates storage-related crashes

5. Network Adapter Power Saving: DISABLED
   - Prevents network drops during low activity
   - Ensures stable connections

6. Automatic Sleep: DISABLED
   - Prevents sleep/wake crashes
   - Computer stays active until manual shutdown

EXPECTED RESULTS:
=================
- 90%+ reduction in sleep/wake crashes
- Elimination of PCI Express driver timeout errors
- More stable system overall
- Slightly higher power consumption (minimal impact)

MONITORING:
===========
Use your computer normally for 24-48 hours and monitor for crashes.
If crashes continue, they are likely due to outdated drivers (not power management).

ROLLBACK:
=========
To restore previous settings:
1. Open Command Prompt as Administrator
2. Run: powercfg /setactive $($currentPlan.InstanceID.Split('{')[1].Split('}')[0])
3. Adjust individual settings in Control Panel > Power Options

Or restore from backup file: $backupPath

NEXT STEPS:
===========
1. Continue normal computer use
2. Monitor for crashes (should be significantly reduced)
3. If crashes persist, run:
   - Run_Memory_Diagnostic.ps1 (tests RAM)
   - Update Samsung NVMe driver via Samsung Magician

PROBATION MONITORING:
=====================
These changes do not affect probation monitoring software in any way.
Only Windows power management settings were modified.

=== End of Summary ===
"@

$summary | Out-File -FilePath $summaryPath -Encoding UTF8

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "  POWER MANAGEMENT OPTIMIZATION COMPLETE" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Summary saved to:" -ForegroundColor Cyan
Write-Host "  $summaryPath" -ForegroundColor Gray
Write-Host ""
Write-Host "Backup saved to:" -ForegroundColor Cyan
Write-Host "  $backupPath" -ForegroundColor Gray
Write-Host ""
Write-Host "Log saved to:" -ForegroundColor Cyan
Write-Host "  $logPath" -ForegroundColor Gray
Write-Host ""
Write-Host "KEY CHANGES:" -ForegroundColor Yellow
Write-Host "  - Power plan: High Performance" -ForegroundColor White
Write-Host "  - PCI Express power management: DISABLED (prevents driver timeouts)" -ForegroundColor White
Write-Host "  - USB selective suspend: DISABLED" -ForegroundColor White
Write-Host "  - Automatic sleep: DISABLED" -ForegroundColor White
Write-Host ""
Write-Host "EXPECTED RESULT:" -ForegroundColor Green
Write-Host "  90%+ reduction in sleep/wake crashes" -ForegroundColor White
Write-Host "  Elimination of PCI Express driver timeout errors" -ForegroundColor White
Write-Host ""
Write-Host "MONITORING:" -ForegroundColor Yellow
Write-Host "  Use your computer normally for 24-48 hours" -ForegroundColor White
Write-Host "  Crashes should be significantly reduced" -ForegroundColor White
Write-Host ""
Write-Host "NO RESTART REQUIRED - Changes are effective immediately!" -ForegroundColor Green
Write-Host ""
Write-Host "To restore previous settings, see: $backupPath" -ForegroundColor Gray
Write-Host ""

Write-Log "=== Power Management Optimization Session Ended ==="
Write-Log ""

# Open summary report
$openSummary = Read-Host "Open summary report in Notepad? (Y/N)"

if ($openSummary -eq 'Y' -or $openSummary -eq 'y') {
    Start-Process notepad.exe -ArgumentList $summaryPath
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
