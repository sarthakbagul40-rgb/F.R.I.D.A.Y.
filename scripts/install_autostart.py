"""
F.R.I.D.A.Y. Windows Auto-Startup Installer
Registers F.R.I.D.A.Y. in the Windows Startup directory so she automatically launches
and speaks her startup briefing whenever you log into or unlock your PC.
"""

import os
import sys
import win32com.client

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def install_autostart():
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    target_bat = os.path.join(project_dir, "run_friday.bat")
    startup_dir = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup")

    if not os.path.exists(startup_dir):
        print(f"[Error]: Startup directory not found: {startup_dir}")
        return False

    print(f"[*] Registering F.R.I.D.A.Y. in Windows Startup: {startup_dir}")

    # 1. Clean up old/redundant duplicate startup items in Startup folder & Windows Registry
    stale_files = ["FRIDAY.lnk", "JARVIS.lnk", "FRIDAY_AutoStart.bat", "FRIDAY_OS.lnk"]
    for stale in stale_files:
        stale_path = os.path.join(startup_dir, stale)
        if os.path.exists(stale_path):
            try:
                os.remove(stale_path)
                print(f"[✓] Removed legacy startup entry: {stale}")
            except Exception as e:
                print(f"[!] Could not remove {stale}: {e}")

    # Clean duplicate Registry Run entries to guarantee only ONE terminal window opens
    try:
        import winreg
        for reg_name in ["FRIDAY_OS", "FRIDAY", "JARVIS", "J.A.R.V.I.S"]:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteValue(key, reg_name)
                winreg.CloseKey(key)
                print(f"[✓] Removed duplicate Registry Run entry: {reg_name}")
            except FileNotFoundError:
                pass
            except Exception as re_err:
                print(f"[!] Registry check notice: {re_err}")
    except Exception:
        pass

    # 2. Create single unified Windows Shell Shortcut (.lnk)
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut_path = os.path.join(startup_dir, "FRIDAY.lnk")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = target_bat
        shortcut.WorkingDirectory = project_dir
        shortcut.Description = "F.R.I.D.A.Y. Cybernetic AI Assistant"
        shortcut.Save()
        print(f"[✓] Created clean Windows Startup Shortcut: {shortcut_path}")
    except Exception as e:
        print(f"[!] Warning creating .lnk shortcut: {e}")

    print("\n[SUCCESS] F.R.I.D.A.Y. is now cleanly registered for Windows Auto-Boot!")
    print("Startup overhead eliminated. Only a single optimized instance will boot with Windows.")
    return True

if __name__ == "__main__":
    install_autostart()
