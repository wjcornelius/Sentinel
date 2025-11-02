$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\wjcor\OneDrive\Desktop\Sentinel CEO.lnk")
$Shortcut.TargetPath = "C:\Users\wjcor\OneDrive\Desktop\Sentinel\Run_Sentinel_CEO.bat"
$Shortcut.WorkingDirectory = "C:\Users\wjcor\OneDrive\Desktop\Sentinel"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,265"
$Shortcut.Description = "Sentinel Corporation - CEO Control Panel"
$Shortcut.Save()
Write-Host "Desktop shortcut created successfully!"
