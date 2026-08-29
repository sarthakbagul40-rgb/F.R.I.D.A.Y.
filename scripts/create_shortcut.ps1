$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ScriptDir) { $ScriptDir = $PSScriptRoot }
$WshShell = New-Object -ComObject WScript.Shell
$StartupDir = [System.IO.Path]::Combine($env:APPDATA, "Microsoft\Windows\Start Menu\Programs\Startup")
$Shortcut = $WshShell.CreateShortcut("$StartupDir\JARVIS.lnk")
$Shortcut.TargetPath = "$ScriptDir\run_jarvis.bat"
$Shortcut.WorkingDirectory = "$ScriptDir"
$Shortcut.Save()

