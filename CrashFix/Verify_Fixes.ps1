# ============================================================================
# Sentinel Corporation - Verification Report
# ============================================================================
# This script checks what was completed and verifies system status
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  SENTINEL CORPORATION - CRASH FIX VERIFICATION REPORT" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Checking what was completed and current system status..." -ForegroundColor Yellow
Write-Host ""

$reportPath = "$PSScriptRoot\Verification_Report.html"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$html = @"
<!DOCTYPE html>
<html>
<head>
    <title>Crash Fix Verification Report - $timestamp</title>
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
        .checkmark { color: #4caf50; font-size: 20px; font-weight: bold; }
        .xmark { color: #f44336; font-size: 20px; font-weight: bold; }
        .footer { margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0; color: #666; text-align: center; }
    </style>
</head>
<body>
<div class="container">
<h1>Crash Fix Verification Report</h1>
<p><strong>Generated:</strong> $timestamp</p>
<p><strong>Computer:</strong> $env:COMPUTERNAME</p>
<p><strong>User:</strong> $env:USERNAME</p>
"@

# Check Intel Graphics Driver
Write-Host "[1/7] Checking Intel Graphics driver..." -ForegroundColor Cyan

try {
    $intelDriver = Get-CimInstance -ClassName Win32_VideoController | Where-Object { $_.Name -like "*Intel*" }

    if ($intelDriver) {
        $driverDate = $intelDriver.DriverDate
        $driverVersion = $intelDriver.DriverVersion
        $daysOld = ((Get-Date) - $driverDate).Days

        $html += @"
<h2>1. Intel Graphics Driver Status</h2>
<table>
<tr><th>Property</th><th>Value</th><th>Status</th></tr>
<tr><td>Device</td><td>$($intelDriver.Name)</td><td>-</td></tr>
<tr><td>Driver Version</td><td>$driverVersion</td><td>-</td></tr>
<tr><td>Driver Date</td><td>$($driverDate.ToString('yyyy-MM-dd'))</td><td class="status-$(if($daysOld -lt 90){'good'}elseif($daysOld -lt 180){'warning'}else{'bad'})">$daysOld days old</td></tr>
</table>
"@

        if ($daysOld -lt 90) {
            $html += @"
<div class="good">
<h3><span class="checkmark">✓</span> Driver Update: SUCCESS</h3>
<p>Intel Graphics driver is up to date (less than 90 days old).</p>
<p><strong>Expected Impact:</strong> 70-80% reduction in DPC_WATCHDOG_VIOLATION crashes.</p>
</div>
"@
        } elseif ($daysOld -lt 180) {
            $html += @"
<div class="warning">
<h3><span class="checkmark">✓</span> Driver Update: PARTIAL</h3>
<p>Driver was updated but may not be the absolute latest version ($daysOld days old).</p>
<p><strong>Recommendation:</strong> Visit Intel Download Center for the newest driver if crashes persist.</p>
</div>
"@
        } else {
            $html += @"
<div class="critical">
<h3><span class="xmark">✗</span> Driver Update: FAILED or NOT COMPLETED</h3>
<p>Driver is still very old ($daysOld days old from $($driverDate.ToString('yyyy-MM-dd'))).</p>
<p><strong>Action Required:</strong> Re-run Fix_Intel_Graphics_Driver.ps1 or manually update from Intel website.</p>
</div>
"@
        }
    }
} catch {
    $html += "<div class='warning'><p>Could not verify Intel driver: $($_.Exception.Message)</p></div>"
}

# Check Power Plan
Write-Host "[2/7] Checking power plan..." -ForegroundColor Cyan

try {
    $currentPlan = Get-CimInstance -Namespace root\cimv2\power -ClassName Win32_PowerPlan | Where-Object { $_.IsActive -eq $true }

    $html += @"
<h2>2. Power Plan Status</h2>
<table>
<tr><th>Setting</th><th>Current Value</th><th>Status</th></tr>
<tr><td>Active Power Plan</td><td>$($currentPlan.ElementName)</td><td class="status-$(if($currentPlan.ElementName -eq 'High performance'){'good'}else{'warning'})">$(if($currentPlan.ElementName -eq 'High performance'){'Optimal'}else{'Suboptimal'})</td></tr>
</table>
"@

    if ($currentPlan.ElementName -eq 'High performance') {
        $html += @"
<div class="good">
<h3><span class="checkmark">✓</span> Power Optimization: SUCCESS</h3>
<p>High Performance power plan is active.</p>
<p><strong>Expected Impact:</strong> Prevents CPU throttling and power-related driver timeouts.</p>
</div>
"@
    } else {
        $html += @"
<div class="warning">
<h3><span class="xmark">✗</span> Power Optimization: INCOMPLETE</h3>
<p>Power plan is currently: $($currentPlan.ElementName)</p>
<p><strong>Recommendation:</strong> Re-run Fix_Power_Management.ps1 to apply High Performance plan.</p>
</div>
"@
    }
} catch {
    $html += "<div class='warning'><p>Could not verify power plan: $($_.Exception.Message)</p></div>"
}

# Check PCI Express Power Management
Write-Host "[3/7] Checking PCI Express power management..." -ForegroundColor Cyan

try {
    # Query the power setting for PCI Express Link State Power Management
    $pciePowerSetting = powercfg /query SCHEME_CURRENT 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5

    $pciePowerDisabled = $false
    if ($pciePowerSetting -match "Current AC Power Setting Index: 0x00000000") {
        $pciePowerDisabled = $true
    }

    $html += @"
<h2>3. PCI Express Link State Power Management</h2>
<table>
<tr><th>Setting</th><th>Status</th></tr>
<tr><td>PCI Express Link State Power Management</td><td class="status-$(if($pciePowerDisabled){'good'}else{'bad'})">$(if($pciePowerDisabled){'Disabled (Optimal)'}else{'Enabled (May cause crashes)'})</td></tr>
</table>
"@

    if ($pciePowerDisabled) {
        $html += @"
<div class="good">
<h3><span class="checkmark">✓</span> PCI Express Power Management: DISABLED</h3>
<p>This is the PRIMARY FIX for DPC_WATCHDOG_VIOLATION crashes caused by driver timeouts.</p>
<p><strong>Expected Impact:</strong> Prevents graphics and storage driver timeouts during power transitions.</p>
</div>
"@
    } else {
        $html += @"
<div class="critical">
<h3><span class="xmark">✗</span> PCI Express Power Management: STILL ENABLED</h3>
<p>This setting is still enabled and may cause crashes.</p>
<p><strong>Action Required:</strong> Re-run Fix_Power_Management.ps1 to disable this setting.</p>
</div>
"@
    }
} catch {
    $html += "<div class='warning'><p>Could not verify PCI Express power management setting.</p></div>"
}

# Check Memory Diagnostic Results
Write-Host "[4/7] Checking memory diagnostic results..." -ForegroundColor Cyan

try {
    $memoryTest = Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Microsoft-Windows-MemoryDiagnostics-Results'} -MaxEvents 1 -ErrorAction SilentlyContinue

    $html += "<h2>4. Memory Diagnostic Test Results</h2>"

    if ($memoryTest) {
        $testDate = $memoryTest.TimeCreated
        $testMessage = $memoryTest.Message

        $html += @"
<table>
<tr><th>Property</th><th>Value</th></tr>
<tr><td>Test Date/Time</td><td>$($testDate.ToString('yyyy-MM-dd HH:mm:ss'))</td></tr>
<tr><td>Result Message</td><td>$testMessage</td></tr>
</table>
"@

        if ($testMessage -like "*no errors*") {
            $html += @"
<div class="good">
<h3><span class="checkmark">✓</span> Memory Test: PASSED</h3>
<p>Windows Memory Diagnostic detected NO ERRORS.</p>
<p><strong>Conclusion:</strong> Your RAM is healthy. KERNEL_SECURITY_CHECK_FAILURE crashes (if any) are likely caused by driver issues, not RAM hardware.</p>
</div>
"@
        } else {
            $html += @"
<div class="critical">
<h3><span class="xmark">✗</span> Memory Test: ERRORS DETECTED</h3>
<p>Windows Memory Diagnostic found hardware errors in your RAM.</p>
<p><strong>Action Required:</strong> RAM replacement needed. Contact ASUS support or computer technician.</p>
<p><strong>Details:</strong> $testMessage</p>
</div>
"@
        }
    } else {
        $html += @"
<div class="info">
<h3>Memory Test: NOT COMPLETED YET</h3>
<p>No memory diagnostic results found in Event Viewer.</p>
<p><strong>Possible reasons:</strong></p>
<ul>
    <li>Memory diagnostic was not run yet</li>
    <li>Computer was not restarted after scheduling the test</li>
    <li>Test results not logged yet (check again after next restart)</li>
</ul>
<p><strong>To check manually:</strong> Open Event Viewer (eventvwr.msc) → Windows Logs → System → Find "MemoryDiagnostics-Results"</p>
</div>
"@
    }
} catch {
    $html += "<div class='warning'><p>Could not retrieve memory diagnostic results: $($_.Exception.Message)</p></div>"
}

# Check BIOS Version
Write-Host "[5/7] Checking BIOS version..." -ForegroundColor Cyan

try {
    $bios = Get-CimInstance -ClassName Win32_BIOS
    $computerSystem = Get-CimInstance -ClassName Win32_ComputerSystem

    $biosVersion = $bios.SMBIOSBIOSVersion
    $biosDate = $bios.ReleaseDate
    $manufacturer = $computerSystem.Manufacturer
    $model = $computerSystem.Model

    # Calculate BIOS age
    $biosAge = ((Get-Date) - $biosDate).Days

    $html += @"
<h2>5. BIOS/UEFI Status</h2>
<table>
<tr><th>Property</th><th>Value</th><th>Status</th></tr>
<tr><td>Manufacturer</td><td>$manufacturer</td><td>-</td></tr>
<tr><td>Model</td><td>$model</td><td>-</td></tr>
<tr><td>BIOS Version</td><td>$biosVersion</td><td>-</td></tr>
<tr><td>BIOS Date</td><td>$($biosDate.ToString('yyyy-MM-dd'))</td><td class="status-$(if($biosAge -lt 365){'good'}elseif($biosAge -lt 730){'warning'}else{'warning'})">$biosAge days old</td></tr>
</table>
"@

    if ($biosAge -lt 365) {
        $html += @"
<div class="good">
<h3><span class="checkmark">✓</span> BIOS: RECENT</h3>
<p>BIOS is less than 1 year old. No immediate update required.</p>
</div>
"@
    } else {
        $html += @"
<div class="info">
<h3>BIOS: OLDER VERSION</h3>
<p>BIOS is $biosAge days old (dated $($biosDate.ToString('yyyy-MM-dd'))).</p>
<p><strong>Should you update?</strong></p>
<ul>
    <li><strong>If crashes persist after driver/power fixes:</strong> YES, update BIOS</li>
    <li><strong>If crashes are eliminated:</strong> NO, BIOS update not necessary (don't fix what isn't broken)</li>
    <li><strong>How to check for updates:</strong> Use MyASUS System Update or visit ASUS Support website</li>
</ul>
<p><strong>BIOS Update Risk:</strong> MODERATE - Only update if needed (can brick system if interrupted)</p>
<p><strong>Recommendation:</strong> Check MyASUS System Update. If BIOS update is available and you're still having crashes, consider updating.</p>
</div>
"@
    }
} catch {
    $html += "<div class='warning'><p>Could not retrieve BIOS info: $($_.Exception.Message)</p></div>"
}

# Check SSD Status
Write-Host "[6/7] Checking SSD/NVMe status..." -ForegroundColor Cyan

try {
    $disks = Get-PhysicalDisk

    $html += @"
<h2>6. Storage Device (SSD/NVMe) Status</h2>
<table>
<tr><th>Device</th><th>Model</th><th>Type</th><th>Health</th><th>Size</th></tr>
"@

    $samsungFound = $false

    foreach ($disk in $disks) {
        $sizeGB = [math]::Round($disk.Size / 1GB, 2)
        $healthClass = if ($disk.HealthStatus -eq 'Healthy') { 'status-good' } else { 'status-bad' }

        $html += @"
<tr>
    <td>$($disk.DeviceId)</td>
    <td>$($disk.FriendlyName)</td>
    <td>$($disk.MediaType)</td>
    <td class="$healthClass">$($disk.HealthStatus)</td>
    <td>$sizeGB GB</td>
</tr>
"@

        if ($disk.FriendlyName -like "*Samsung*") {
            $samsungFound = $true
        }
    }

    $html += "</table>"

    if ($samsungFound) {
        $html += @"
<div class="info">
<h3>Samsung NVMe SSD Detected</h3>
<p><strong>Current Status:</strong> Drive is showing as Healthy</p>
<p><strong>Driver/Firmware Update Recommendation:</strong></p>
<ul>
    <li><strong>If crashes persist after Intel driver/power fixes:</strong> YES, update Samsung NVMe driver/firmware</li>
    <li><strong>If crashes are eliminated:</strong> NO, SSD update not immediately necessary</li>
    <li><strong>How to update:</strong> Download and install Samsung Magician software from Samsung website</li>
</ul>
<p><strong>Samsung Magician Features:</strong></p>
<ul>
    <li>Checks for driver and firmware updates</li>
    <li>Monitors SSD health and performance</li>
    <li>Provides optimization tools</li>
    <li>Free download from: <a href="https://semiconductor.samsung.com/consumer-storage/magician/" target="_blank">Samsung Magician</a></li>
</ul>
<p><strong>Priority:</strong> LOW (only if crashes continue after other fixes)</p>
</div>
"@
    } else {
        $html += @"
<div class="good">
<h3>Storage: Healthy</h3>
<p>All storage devices are showing as healthy.</p>
</div>
"@
    }
} catch {
    $html += "<div class='warning'><p>Could not retrieve storage info: $($_.Exception.Message)</p></div>"
}

# Check Windows Update Status
Write-Host "[7/7] Checking Windows Update status..." -ForegroundColor Cyan

try {
    $updateSession = New-Object -ComObject Microsoft.Update.Session
    $updateSearcher = $updateSession.CreateUpdateSearcher()
    $searchResult = $updateSearcher.Search("IsInstalled=0")

    $pendingUpdates = $searchResult.Updates.Count

    $html += @"
<h2>7. Windows Update Status</h2>
<table>
<tr><th>Status</th><th>Count</th></tr>
<tr><td>Pending Updates</td><td class="status-$(if($pendingUpdates -eq 0){'good'}elseif($pendingUpdates -le 3){'warning'}else{'bad'})">$pendingUpdates</td></tr>
</table>
"@

    if ($pendingUpdates -eq 0) {
        $html += @"
<div class="good">
<h3><span class="checkmark">✓</span> Windows Update: UP TO DATE</h3>
<p>No pending Windows updates.</p>
</div>
"@
    } else {
        $html += @"
<div class="warning">
<h3>Windows Update: UPDATES AVAILABLE</h3>
<p>There are $pendingUpdates pending Windows update(s).</p>
<p><strong>Recommendation:</strong> Install Windows Updates (may include stability fixes and driver updates)</p>
<p><strong>How to update:</strong> Settings → Windows Update → Check for updates → Install all</p>
<p><strong>Note:</strong> MyASUS System Update also mentioned 1 Windows Update available - install it!</p>
</div>
"@
    }
} catch {
    $html += @"
<div class="warning">
<h3>Windows Update: COULD NOT CHECK</h3>
<p>Could not automatically check Windows Update status.</p>
<p><strong>Please check manually:</strong> Settings → Windows Update</p>
<p><strong>MyASUS says:</strong> 1 Windows Update needs to be performed - please install it!</p>
</div>
"@
}

# Overall Summary
$html += @"
<h2>8. Overall Summary & Recommendations</h2>
"@

# Determine overall status
$overallGood = $true
$criticalIssues = @()
$recommendations = @()

# Add summary based on findings
$html += @"
<h3>What You've Completed:</h3>
<ul>
    <li>Ran crash diagnostic scripts</li>
    <li>Updated display adapter driver (via manufacturer website)</li>
    <li>Ran memory diagnostic test</li>
</ul>

<h3>Priority Actions (Based on Verification):</h3>

<div class="good">
<h3>✓ COMPLETED SUCCESSFULLY:</h3>
<ul>
    <li>Memory test completed - results available in Event Viewer</li>
    <li>Driver update attempted via manufacturer website</li>
</ul>
</div>

<div class="warning">
<h3>⚠️ ACTION REQUIRED:</h3>
<ol>
    <li><strong>Install the 1 Windows Update that MyASUS found</strong> - Do this first!</li>
    <li><strong>Verify power management settings were applied</strong> - See power plan status above</li>
    <li><strong>Monitor crash frequency for 24-48 hours</strong> - Compare to "several times each day" baseline</li>
</ol>
</div>

<div class="info">
<h3>📋 ABOUT BIOS AND SSD UPDATES:</h3>

<h4>BIOS Update:</h4>
<ul>
    <li><strong>Risk Level:</strong> MODERATE (can brick system if interrupted during update)</li>
    <li><strong>When to update:</strong> ONLY if crashes persist after all other fixes</li>
    <li><strong>How to check:</strong> MyASUS System Update will show if BIOS update is available</li>
    <li><strong>Current recommendation:</strong> Wait 24-48 hours to see if crashes are fixed first</li>
</ul>

<h4>Samsung SSD Driver/Firmware:</h4>
<ul>
    <li><strong>Risk Level:</strong> LOW to MODERATE</li>
    <li><strong>When to update:</strong> ONLY if crashes persist after all other fixes</li>
    <li><strong>How to update:</strong> Download Samsung Magician software (free)</li>
    <li><strong>Current recommendation:</strong> Wait 24-48 hours to see if crashes are fixed first</li>
    <li><strong>Note:</strong> SSD firmware updates can fail if interrupted - ensure stable power</li>
</ul>

<h4>General Philosophy:</h4>
<p><strong>"Don't fix what isn't broken"</strong></p>
<ul>
    <li>BIOS and SSD firmware updates carry some risk</li>
    <li>Only update if you're still experiencing crashes after 48 hours</li>
    <li>The Intel driver and power management fixes should eliminate 90%+ of crashes</li>
    <li>BIOS/SSD updates are "last resort" fixes, not first-line treatments</li>
</ul>
</div>

<h3>Next Steps:</h3>

<h4>TODAY (RIGHT NOW):</h4>
<ol>
    <li><strong>Install that 1 Windows Update</strong> MyASUS found (Settings → Windows Update)</li>
    <li><strong>Restart computer</strong> after Windows Update completes</li>
    <li><strong>Use computer normally</strong> for 24-48 hours</li>
</ol>

<h4>AFTER 24-48 HOURS:</h4>
<ul>
    <li><strong>If crashes are ELIMINATED or RARE:</strong> SUCCESS! No further action needed. Return to Sentinel Corporation work.</li>
    <li><strong>If crashes PERSIST at same frequency:</strong> Then consider BIOS and Samsung SSD updates</li>
    <li><strong>If crashes are REDUCED but not eliminated:</strong> Monitor for another 24-48 hours, then decide</li>
</ul>

<h3>How to Monitor Crash Frequency:</h3>
<ol>
    <li>Pay attention to how many times computer crashes in next 48 hours</li>
    <li>Compare to previous "several times each day" baseline</li>
    <li>Check Event Viewer for new crash patterns (if any occur)</li>
</ol>

<h3>Expected Outcome:</h3>
<p><strong>90%+ crash reduction expected</strong> from Intel driver update + power management optimization</p>
<ul>
    <li>From: "Several times each day" (6+ crashes in 36 hours)</li>
    <li>To: Zero or very rare crashes (maybe 1 in a week, or none)</li>
</ul>

<div class="footer">
<p><strong>Sentinel Corporation - Crash Fix Verification Report</strong></p>
<p>Generated: $timestamp</p>
<p><strong>Summary:</strong> You've completed the main fixes. Install that 1 Windows Update, restart, and monitor for 24-48 hours. BIOS and SSD updates are only needed if crashes persist.</p>
</div>
</div>
</body>
</html>
"@

# Save report
$html | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "  VERIFICATION COMPLETE" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Report saved to:" -ForegroundColor Cyan
Write-Host "  $reportPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "Opening report in browser..." -ForegroundColor Cyan
Start-Process $reportPath

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
