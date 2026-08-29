import os
import win32com.client

def create_shortcut():
    desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    shortcut_path = os.path.join(desktop, "DeepSeek Harness.lnk")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(base_dir, "scripts", "launch_deepseek_harness.bat")
    
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.WorkingDirectory = base_dir
    shortcut.Description = "DeepSeek Harness AI Agent Web IDE"
    shortcut.Save()
    print(f"DeepSeek Harness shortcut created successfully at: {shortcut_path}")

if __name__ == "__main__":
    create_shortcut()
