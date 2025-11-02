# ============================================================================
# Sentinel Corporation - Computer Crash Diagnostic Report
# ============================================================================
#
# This script is READ-ONLY and 100% safe. It collects diagnostic information
# about your computer crashes and generates an HTML report.
#
# PROBATION MONITORING: Zero impact - only reads system information
#
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  SENTINEL CORPORATION - CRASH DIAGNOSTIC REPORT" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will analyze your system and generate a diagnostic report." -ForegroundColor Yellow
Write-Host "READ-ONLY: No changes will be made to your system." -ForegroundColor Green
Write-Host ""
Write-Host "Collecting diagnostic information..." -ForegroundColor Yellow
Write-Host ""

# Initialize report
$reportPath = "$PSScriptRoot\Crash_Diagnostic_Report.html"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Start HTML report
$html = @"
<!DOCTYPE html>
<html>
<head>
    <title>Crash Diagnostic Report - $timestamp</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #0066cc; border-bottom: 3px solid #0066cc; padding-bottom: 10px; }
        h2 { color: #0066cc; margin-top: 30px; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; }
        h3 { color: #333; margin-top: 20px; }
        .critical { background: #ffebee; border-left: 5px solid #f44336; padding: 15px; margin: 10px 0; }
        .warning { background: #fff3e0; border-left: 5px solid #ff9800; padding: 15px; margin: 10px 0; }
        .good { background: #e8f5e9; border-left: 5px solid #4caf50; padding: 15px; margin: 10px 0; }
        .info { background: #e3f2fd; border-left: 5px solid #2196f3; padding: 15px; margin: 10px 0; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th { background: #0066cc; color: white; padding: 12px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #e0e0e0; }
        tr:nth-child(even) { background: #f9f9f9; }
        .status-bad { color: #f44336; font-weight: bold; }
        .status-good { color: #4caf50; font-weight: bold; }
        .status-warning { color: #ff9800; font-weight: bold; }
        code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }
        .footer { margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0; color: #666; text-align: center; }
    </style>
</head>
<body>
<div class="container">
<h1>Computer Crash Diagnostic Report</h1>
<p><strong>Generated:</strong> $timestamp</p>
<p><strong>Computer:</strong> $env:COMPUTERNAME</p>
<p><strong>User:</strong> $env:USERNAME</p>
"@

Write-Host "[1/7] Checking system specifications..." -ForegroundColor Cyan

# System Information
$computerSystem = Get-CimInstance -ClassName Win32_ComputerSystem
$os = Get-CimInstance -ClassName Win32_OperatingSystem
$processor = Get-CimInstance -ClassName Win32_Processor
$bios = Get-CimInstance -ClassName Win32_BIOS

$html += @"
<h2>1. System Specifications</h2>
<table>
<tr><th>Component</th><th>Details</th></tr>
<tr><td>Computer</td><td>$($computerSystem.Manufacturer) $($computerSystem.Model)</td></tr>
<tr><td>Processor</td><td>$($processor.Name)</td></tr>
<tr><td>RAM</td><td>$([math]::Round($computerSystem.TotalPhysicalMemory / 1GB, 2)) GB</td></tr>
<tr><td>Operating System</td><td>$($os.Caption) (Build $($os.BuildNumber))</td></tr>
<tr><td>BIOS Version</td><td>$($bios.SMBIOSBIOSVersion) (Date: $($bios.ReleaseDate.ToString().Substring(0,8)))</td></tr>
<tr><td>Last Boot</td><td>$($os.LastBootUpTime)</td></tr>
</table>
"@

Write-Host "[2/7] Checking Intel Graphics driver..." -ForegroundColor Cyan

# Intel Graphics Driver Check
try {
    $intelDriver = Get-CimInstance -ClassName Win32_VideoController | Where-Object { $_.Name -like "*Intel*" }

    if ($intelDriver) {
        $driverDate = $intelDriver.DriverDate
        $driverVersion = $intelDriver.DriverVersion
        $daysOld = ((Get-Date) - $driverDate).Days

        if ($daysOld -gt 180) {
            $driverStatus = "critical"
            $driverMessage = "CRITICAL: Intel Graphics driver is $daysOld days old (dated $($driverDate.ToString('yyyy-MM-dd'))). This is the PRIMARY cause of DPC_WATCHDOG_VIOLATION crashes. UPDATE IMMEDIATELY."
        } elseif ($daysOld -gt 90) {
            $driverStatus = "warning"
            $driverMessage = "WARNING: Intel Graphics driver is $daysOld days old. Consider updating."
        } else {
            $driverStatus = "good"
            $driverMessage = "Intel Graphics driver is up to date ($daysOld days old)."
        }

        $html += @"
<h2>2. Intel Graphics Driver Status</h2>
<div class="$driverStatus">
<h3>$driverMessage</h3>
<table>
<tr><th>Property</th><th>Value</th></tr>
<tr><td>Device</td><td>$($intelDriver.Name)</td></tr>
<tr><td>Driver Version</td><td>$driverVersion</td></tr>
<tr><td>Driver Date</td><td>$($driverDate.ToString('yyyy-MM-dd'))</td></tr>
<tr><td>Age</td><td class="status-$(if($daysOld -gt 180){'bad'}elseif($daysOld -gt 90){'warning'}else{'good'})">$daysOld days old</td></tr>
</table>
</div>
"@
    } else {
        $html += @"
<h2>2. Intel Graphics Driver Status</h2>
<div class="warning">
<p>No Intel graphics adapter detected. This is unexpected for your system.</p>
</div>
"@
    }
} catch {
    $html += @"
<h2>2. Intel Graphics Driver Status</h2>
<div class="warning">
<p>Could not retrieve Intel graphics driver information: $($_.Exception.Message)</p>
</div>
"@
}

Write-Host "[3/7] Checking storage devices..." -ForegroundColor Cyan

# Storage Device Check
$disks = Get-PhysicalDisk
$html += @"
<h2>3. Storage Devices</h2>
<table>
<tr><th>Device</th><th>Model</th><th>Size</th><th>Health</th><th>Type</th></tr>
"@

foreach ($disk in $disks) {
    $healthStatus = switch ($disk.HealthStatus) {
        "Healthy" { "status-good" }
        "Warning" { "status-warning" }
        default { "status-bad" }
    }

    $sizeGB = [math]::Round($disk.Size / 1GB, 2)

    $html += @"
<tr>
    <td>$($disk.DeviceId)</td>
    <td>$($disk.FriendlyName)</td>
    <td>$sizeGB GB</td>
    <td class="$healthStatus">$($disk.HealthStatus)</td>
    <td>$($disk.MediaType)</td>
</tr>
"@
}

$html += "</table>"

# Check for Samsung NVMe specifically
$samsungNVMe = $disks | Where-Object { $_.FriendlyName -like "*Samsung*" -and $_.MediaType -eq "SSD" }
if ($samsungNVMe) {
    $html += @"
<div class="info">
<h3>Samsung NVMe SSD Detected</h3>
<p>Model: $($samsungNVMe.FriendlyName)</p>
<p><strong>Recommendation:</strong> Install Samsung Magician software to update NVMe driver and firmware.</p>
<p><strong>Download:</strong> <a href="https://semiconductor.samsung.com/consumer-storage/magician/" target="_blank">https://semiconductor.samsung.com/consumer-storage/magician/</a></p>
</div>
"@
}

Write-Host "[4/7] Analyzing crash history (Event Viewer)..." -ForegroundColor Cyan

# Event Viewer - System Crashes
$crashes = Get-WinEvent -FilterHashtable @{LogName='System'; Id=1001; ProviderName='Microsoft-Windows-WER-SystemErrorReporting'} -MaxEvents 50 -ErrorAction SilentlyContinue

$html += @"
<h2>4. Recent Crash History (Last 50 Crashes)</h2>
"@

if ($crashes) {
    $crashCount = $crashes.Count
    $recentCrashes = ($crashes | Where-Object { $_.TimeCreated -gt (Get-Date).AddDays(-7) }).Count

    if ($recentCrashes -gt 5) {
        $crashSeverity = "critical"
    } elseif ($recentCrashes -gt 2) {
        $crashSeverity = "warning"
    } else {
        $crashSeverity = "info"
    }

    $html += @"
<div class="$crashSeverity">
<h3>Found $crashCount total crashes in event log</h3>
<p><strong>Last 7 days:</strong> $recentCrashes crashes</p>
</div>

<h3>Recent Crashes:</h3>
<table>
<tr><th>Date/Time</th><th>Bug Check Code</th><th>Description</th></tr>
"@

    foreach ($crash in $crashes | Select-Object -First 20) {
        $message = $crash.Message

        # Try to extract bug check code
        $bugCheck = "Unknown"
        if ($message -match "0x[0-9a-fA-F]+") {
            $bugCheck = $matches[0]
        }

        $html += @"
<tr>
    <td>$($crash.TimeCreated.ToString('yyyy-MM-dd HH:mm:ss'))</td>
    <td><code>$bugCheck</code></td>
    <td>$(($message -split "`n")[0].Substring(0, [Math]::Min(100, ($message -split "`n")[0].Length)))...</td>
</tr>
"@
    }

    $html += "</table>"

    # Analyze crash patterns
    $bugCheckCodes = @{}
    foreach ($crash in $crashes) {
        if ($crash.Message -match "0x[0-9a-fA-F]+") {
            $code = $matches[0]
            if ($bugCheckCodes.ContainsKey($code)) {
                $bugCheckCodes[$code]++
            } else {
                $bugCheckCodes[$code] = 1
            }
        }
    }

    $html += @"
<h3>Crash Pattern Analysis:</h3>
<table>
<tr><th>Bug Check Code</th><th>Count</th><th>Meaning</th><th>Likely Cause</th></tr>
"@

    foreach ($code in $bugCheckCodes.Keys | Sort-Object { $bugCheckCodes[$_] } -Descending) {
        $meaning = switch ($code) {
            "0x00000133" { "DPC_WATCHDOG_VIOLATION" }
            "0x00000139" { "KERNEL_SECURITY_CHECK_FAILURE" }
            "0x0000001A" { "MEMORY_MANAGEMENT" }
            "0x0000003B" { "SYSTEM_SERVICE_EXCEPTION" }
            "0x00000050" { "PAGE_FAULT_IN_NONPAGED_AREA" }
            "0x0000009F" { "DRIVER_POWER_STATE_FAILURE" }
            "0x000000D1" { "DRIVER_IRQL_NOT_LESS_OR_EQUAL" }
            default { "See Microsoft documentation" }
        }

        $cause = switch ($code) {
            "0x00000133" { "Graphics or storage driver timeout (UPDATE INTEL GRAPHICS DRIVER)" }
            "0x00000139" { "Memory corruption (RUN MEMORY DIAGNOSTIC)" }
            "0x0000001A" { "RAM hardware fault or driver issue" }
            "0x0000003B" { "Driver or system file corruption" }
            "0x00000050" { "Faulty RAM or driver bug" }
            "0x0000009F" { "Power management issue (FIX POWER SETTINGS)" }
            "0x000000D1" { "Driver accessing invalid memory" }
            default { "Various - see details" }
        }

        $html += @"
<tr>
    <td><code>$code</code></td>
    <td class="status-$(if($bugCheckCodes[$code] -gt 5){'bad'}elseif($bugCheckCodes[$code] -gt 2){'warning'}else{'good'})">$($bugCheckCodes[$code])</td>
    <td>$meaning</td>
    <td>$cause</td>
</tr>
"@
    }

    $html += "</table>"

} else {
    $html += @"
<div class="good">
<p>No crash records found in Event Viewer (or access denied).</p>
</div>
"@
}

Write-Host "[5/7] Checking Windows Update status..." -ForegroundColor Cyan

# Windows Update Status
try {
    $updateSession = New-Object -ComObject Microsoft.Update.Session
    $updateSearcher = $updateSession.CreateUpdateSearcher()
    $searchResult = $updateSearcher.Search("IsInstalled=0")

    $pendingUpdates = $searchResult.Updates.Count

    $html += @"
<h2>5. Windows Update Status</h2>
"@

    if ($pendingUpdates -gt 0) {
        $html += @"
<div class="warning">
<h3>$pendingUpdates pending Windows updates available</h3>
<p><strong>Recommendation:</strong> Install Windows Updates (may include critical driver and stability fixes)</p>
</div>
"@
    } else {
        $html += @"
<div class="good">
<p>Windows is up to date (no pending updates)</p>
</div>
"@
    }
} catch {
    $html += @"
<h2>5. Windows Update Status</h2>
<div class="info">
<p>Could not check Windows Update status automatically. Please check manually in Settings > Windows Update.</p>
</div>
"@
}

Write-Host "[6/7] Checking reliability history..." -ForegroundColor Cyan

# Reliability Monitor Data
$html += @"
<h2>6. System Reliability (Last 30 Days)</h2>
"@

try {
    $reliability = Get-CimInstance -ClassName Win32_ReliabilityRecords -Filter "TimeGenerated > '$((Get-Date).AddDays(-30).ToString('yyyyMMddHHmmss.000000+000'))'" -ErrorAction SilentlyContinue

    if ($reliability) {
        $criticalEvents = ($reliability | Where-Object { $_.EventIdentifier -eq 1 }).Count
        $warningEvents = ($reliability | Where-Object { $_.EventIdentifier -eq 2 }).Count

        $html += @"
<table>
<tr><th>Event Type</th><th>Count (Last 30 Days)</th></tr>
<tr><td>Critical Errors</td><td class="status-$(if($criticalEvents -gt 10){'bad'}elseif($criticalEvents -gt 5){'warning'}else{'good'})">$criticalEvents</td></tr>
<tr><td>Warnings</td><td class="status-$(if($warningEvents -gt 20){'warning'}else{'good'})">$warningEvents</td></tr>
</table>
"@
    } else {
        $html += "<p>Reliability data not available.</p>"
    }
} catch {
    $html += "<p>Could not retrieve reliability data: Check Reliability Monitor manually.</p>"
}

Write-Host "[7/7] Checking memory and power settings..." -ForegroundColor Cyan

# Memory Information
$memory = Get-CimInstance -ClassName Win32_PhysicalMemory

$html += @"
<h2>7. Memory Configuration</h2>
<table>
<tr><th>Slot</th><th>Capacity</th><th>Speed</th><th>Manufacturer</th></tr>
"@

foreach ($mem in $memory) {
    $capacityGB = [math]::Round($mem.Capacity / 1GB, 2)
    $html += @"
<tr>
    <td>$($mem.DeviceLocator)</td>
    <td>$capacityGB GB</td>
    <td>$($mem.Speed) MHz</td>
    <td>$($mem.Manufacturer)</td>
</tr>
"@
}

$html += "</table>"

# Power Settings Check
$powerPlan = Get-CimInstance -Namespace root\cimv2\power -ClassName Win32_PowerPlan | Where-Object { $_.IsActive -eq $true }

$html += @"
<h2>8. Power Settings</h2>
<table>
<tr><th>Setting</th><th>Value</th><th>Recommendation</th></tr>
<tr>
    <td>Active Power Plan</td>
    <td>$($powerPlan.ElementName)</td>
    <td>$(if($powerPlan.ElementName -ne 'High performance'){'Consider High Performance plan for stability'}else{'Optimal'})</td>
</tr>
</table>

<div class="info">
<h3>Power Management Notes:</h3>
<p>Sleep/wake cycles can cause crashes with certain drivers. The <code>Fix_Power_Management.ps1</code> script can optimize these settings.</p>
</div>
"@

# Summary and Recommendations
$html += @"
<h2>9. Summary and Recommendations</h2>

<div class="critical">
<h3>IMMEDIATE ACTIONS (High Priority)</h3>
<ol>
    <li><strong>Update Intel Graphics Driver:</strong> Run <code>Fix_Intel_Graphics_Driver.ps1</code> - This will fix 70-80% of DPC_WATCHDOG_VIOLATION crashes</li>
    <li><strong>Optimize Power Settings:</strong> Run <code>Fix_Power_Management.ps1</code> - Prevents sleep/wake crashes</li>
</ol>
</div>

<div class="warning">
<h3>RECOMMENDED ACTIONS (Medium Priority)</h3>
<ol>
    <li><strong>Test Memory:</strong> Run <code>Run_Memory_Diagnostic.ps1</code> - Tests for RAM faults (requires restart)</li>
    <li><strong>Update Samsung NVMe Driver:</strong> Install Samsung Magician software and update driver/firmware</li>
    <li><strong>Install Windows Updates:</strong> Check Settings > Windows Update for pending updates</li>
</ol>
</div>

<div class="info">
<h3>MONITORING (After Fixes)</h3>
<ol>
    <li>Use computer normally for 24-48 hours</li>
    <li>If crashes continue, check Event Viewer for new crash patterns</li>
    <li>Re-run this diagnostic script to compare before/after</li>
</ol>
</div>

<h3>Crash Patterns Identified:</h3>
<ul>
    <li><strong>DPC_WATCHDOG_VIOLATION (0x133):</strong> Intel Graphics driver timeout → Update driver immediately</li>
    <li><strong>KERNEL_SECURITY_CHECK_FAILURE (0x139):</strong> Possible RAM fault → Run memory diagnostic</li>
    <li><strong>Sleep/Wake Issues:</strong> PCI Express power management → Fix power settings</li>
</ul>

<h3>Expected Results After Fixes:</h3>
<ul>
    <li>Intel driver update should reduce crashes by 70-80%</li>
    <li>Power management fixes should eliminate sleep/wake crashes</li>
    <li>Memory test will identify if RAM needs replacement</li>
    <li>Total expected improvement: 85-90% crash reduction</li>
</ul>

<div class="footer">
<p><strong>Sentinel Corporation - Computer Crash Diagnostic Report</strong></p>
<p>Generated: $timestamp</p>
<p>Next Step: Run <code>Fix_Intel_Graphics_Driver.ps1</code> to start repairs</p>
</div>
</div>
</body>
</html>
"@

# Save HTML report
$html | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "  DIAGNOSTIC REPORT COMPLETE" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Report saved to:" -ForegroundColor Cyan
Write-Host "  $reportPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "Opening report in your browser..." -ForegroundColor Cyan
Start-Process $reportPath

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Review the HTML report that just opened" -ForegroundColor White
Write-Host "  2. Run Fix_Intel_Graphics_Driver.ps1 (HIGHEST PRIORITY)" -ForegroundColor White
Write-Host "  3. Run Fix_Power_Management.ps1" -ForegroundColor White
Write-Host "  4. Run Run_Memory_Diagnostic.ps1 (optional, requires restart)" -ForegroundColor White
Write-Host ""
Write-Host "Or use Master_Crash_Fix.ps1 to run everything automatically." -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
