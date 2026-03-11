# ============================================================================
# Sentinel Corporation - Task Scheduler Setup
# Creates a scheduled task to run automated trading daily at 8:00 AM PT
#
# Run this script as Administrator:
#   PowerShell -ExecutionPolicy Bypass -File setup_automated_trading_task.ps1
# ============================================================================

$TaskName = "Sentinel Automated Trading"
$TaskDescription = "Runs Sentinel automated trading workflow daily at 8:00 AM PT"
$ScriptPath = "C:\Users\wjcor\OneDrive\Desktop\Sentinel\run_automated_trading_silent.vbs"

# Check if running as administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   SENTINEL CORPORATION - Task Scheduler Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$TaskName' already exists." -ForegroundColor Yellow
    $response = Read-Host "Do you want to replace it? (y/n)"
    if ($response -ne 'y') {
        Write-Host "Setup cancelled." -ForegroundColor Red
        exit 0
    }

    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create the trigger - 8:00 AM daily
Write-Host "Creating daily trigger at 8:00 AM..." -ForegroundColor Green
$Trigger = New-ScheduledTaskTrigger -Daily -At "8:00AM"

# Create the action - run the VBScript
Write-Host "Creating action to run: $ScriptPath" -ForegroundColor Green
$Action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$ScriptPath`""

# Create settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -WakeToRun

# Create principal (run whether user is logged on or not)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

# Register the task
Write-Host "Registering scheduled task..." -ForegroundColor Green
Register-ScheduledTask `
    -TaskName $TaskName `
    -Description $TaskDescription `
    -Trigger $Trigger `
    -Action $Action `
    -Settings $Settings `
    -Principal $Principal

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "   SUCCESS! Task created successfully." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Task Details:" -ForegroundColor Cyan
Write-Host "  Name: $TaskName"
Write-Host "  Schedule: Daily at 8:00 AM"
Write-Host "  Script: $ScriptPath"
Write-Host ""
Write-Host "The task will:" -ForegroundColor Cyan
Write-Host "  1. Wake the computer if sleeping"
Write-Host "  2. Run even if on battery power"
Write-Host "  3. Start if a scheduled run was missed"
Write-Host "  4. Require network connection"
Write-Host ""
Write-Host "To verify, open Task Scheduler and look for '$TaskName'" -ForegroundColor Yellow
Write-Host ""

# Show next run time
$task = Get-ScheduledTask -TaskName $TaskName
$taskInfo = Get-ScheduledTaskInfo -TaskName $TaskName
Write-Host "Next scheduled run: $($taskInfo.NextRunTime)" -ForegroundColor Green
Write-Host ""

# Offer to run a test
$testResponse = Read-Host "Would you like to run a test now? (y/n)"
if ($testResponse -eq 'y') {
    Write-Host ""
    Write-Host "Starting test run..." -ForegroundColor Cyan
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "Task started! Check the logs folder for results." -ForegroundColor Green
}

Write-Host ""
Read-Host "Press Enter to exit"
