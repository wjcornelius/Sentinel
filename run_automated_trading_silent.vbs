' ============================================================================
' Sentinel Corporation - Silent Automated Trading Launcher
' Runs the trading script without showing a console window
' ============================================================================

Set WshShell = CreateObject("WScript.Shell")

' Change to Sentinel directory
WshShell.CurrentDirectory = "C:\Users\wjcor\OneDrive\Desktop\Sentinel"

' Run the batch file silently (0 = hidden window)
WshShell.Run "run_automated_trading.bat", 0, True

Set WshShell = Nothing
