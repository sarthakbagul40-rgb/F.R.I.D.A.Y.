$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\best it\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\JARVIS.lnk")
$Shortcut.TargetPath = "d:\python\J.A.R.V.I.S\run_jarvis.bat"
$Shortcut.WorkingDirectory = "d:\python\J.A.R.V.I.S"
$Shortcut.Save()
