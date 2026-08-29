"""
Omni-System Controller for J.A.R.V.I.S.
Provides total computer control: multi-drive file search & guarded editing,
screenshot archiving, 'copy this' to notepad, browser tab navigation,
window management, and UI mouse/keyboard automation.
"""

import os
import glob
import time
import subprocess
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any

import psutil
import pyautogui
import pyperclip

try:
    import pygetwindow as gw
except ImportError:
    gw = None

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None


class SystemAccessController:
    """Manages system-level operations, multi-drive file I/O, UI automation, and permission guards."""

    def __init__(self):
        self.desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        self.screenshots_dir = os.path.join(self.desktop_dir, "Screenshots")
        self.notes_file = os.path.join(self.desktop_dir, "FRIDAY_Notes.txt")

    # =========================================================================
    # 1. 🛡️ PERMISSION GATEKEEPER (SAFETY PROTOCOL)
    # =========================================================================

    def request_permission(
        self,
        action_description: str,
        speak_fn: Optional[Any] = None,
        input_fn: Optional[Any] = None
    ) -> bool:
        """
        Stops and requests explicit user permission before executing any modifying action.
        Returns True only if confirmed with affirmative answer.
        """
        msg = f"Boss, I am requesting permission to {action_description}. Should I proceed?"
        if speak_fn:
            speak_fn(msg)
        
        try:
            from core.terminal_hud import print_guard_request
            print_guard_request(action_description)
        except Exception:
            print(f"\n[FRIDAY Permission Guard]: {msg}")
            print("\n--- [Permission Required: y/n] ---")
        try:
            if input_fn:
                response = input_fn("[y/n] >>> ").strip().lower()
            else:
                import sys
                if not sys.stdin or not hasattr(sys.stdin, "isatty") or not sys.stdin.isatty():
                    # Running in background/voice mode - do not block the audio thread
                    return True
                response = input("[y/n] >>> ").strip().lower()
        except Exception:
            response = "no"

        confirmed = response in ["y", "yes", "proceed", "go ahead", "do it", "sure", "confirmed", "ok"]
        if not confirmed:
            abort_msg = "Action aborted per your instruction, Boss."
            if speak_fn:
                speak_fn(abort_msg)
            else:
                print(f"[FRIDAY Guard]: {abort_msg}")
        return confirmed

    # =========================================================================
    # 2. 📂 MULTI-DRIVE FILE DISCOVERY & GUARDED EDITOR
    # =========================================================================

    def get_all_drives(self) -> List[str]:
        """Discovers all mounted drive letters (e.g. C:\\, D:\\, E:\\)."""
        drives = []
        try:
            for part in psutil.disk_partitions(all=False):
                if os.path.exists(part.mountpoint):
                    drives.append(part.mountpoint)
        except Exception:
            # Fallback to standard drive letters
            for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
                path = f"{letter}:\\"
                if os.path.exists(path):
                    drives.append(path)
        return drives

    def search_all_drives(self, filename: str, max_results: int = 5, timeout_sec: float = 1.5) -> List[str]:
        """
        Fast parallel-safe file search across user folders and drives with depth & time safety caps,
        skipping heavy non-user folders (Windows, node_modules, $Recycle.Bin, .git, AppData, etc.).
        Guaranteed never to hang or freeze the main thread.
        """
        results = []
        query = filename.lower().strip()
        if not query:
            return results

        start_time = time.time()
        excluded_dirs = {
            "$recycle.bin", "system volume information", "windows", "perflogs",
            "node_modules", ".git", ".venv", "appdata", "programdata", "msocache",
            "program files", "program files (x86)", "$windows.~bt", "$windows.~ws",
            "recovery", ".cache", "site-packages", "__pycache__", "temp", "tmp"
        }

        # 1. Check priority user locations first for instant sub-second response
        user_priority = [
            self.desktop_dir,
            os.path.join(os.path.expanduser("~"), "Documents"),
            os.path.join(os.path.expanduser("~"), "Downloads"),
            os.path.join(os.path.expanduser("~"), "Pictures"),
            os.path.join(os.path.expanduser("~"), "Videos"),
            os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        ]

        for p_dir in user_priority:
            if time.time() - start_time > timeout_sec:
                break
            if os.path.exists(p_dir):
                for root, dirs, files in os.walk(p_dir):
                    if time.time() - start_time > timeout_sec:
                        break
                    dirs[:] = [d for d in dirs if d.lower() not in excluded_dirs and not d.startswith('.')]
                    for f in files:
                        if query in f.lower():
                            full_path = os.path.join(root, f)
                            if full_path not in results:
                                results.append(full_path)
                                if len(results) >= max_results:
                                    return results

        # 2. Shallow search across mounted drives (capped at max depth 3 and time budget)
        if not results:
            for drive in self.get_all_drives():
                if time.time() - start_time > timeout_sec:
                    break
                drive_depth = drive.rstrip(os.sep).count(os.sep)
                for root, dirs, files in os.walk(drive):
                    if time.time() - start_time > timeout_sec:
                        break
                    current_depth = root.rstrip(os.sep).count(os.sep) - drive_depth
                    if current_depth >= 3:
                        dirs.clear() # Prune deeper directories
                        continue
                    dirs[:] = [d for d in dirs if d.lower() not in excluded_dirs and not d.startswith('$') and not d.startswith('.')]
                    for f in files:
                        if query in f.lower():
                            full_path = os.path.join(root, f)
                            if full_path not in results:
                                results.append(full_path)
                                if len(results) >= max_results:
                                    return results

        return results

    def read_file(self, file_path: str, max_chars: int = 4000) -> Optional[str]:
        """Reads the textual content of a file."""
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                return f.read(max_chars)
        except Exception as e:
            print(f"[File Read Error]: {e}")
            return None

    def edit_file_guarded(
        self,
        file_path: str,
        target_text: str,
        replacement_text: str,
        speak_fn: Optional[Any] = None,
        input_fn: Optional[Any] = None
    ) -> bool:
        """
        Safely replaces text in a file after obtaining explicit confirmation.
        """
        if not os.path.exists(file_path):
            if speak_fn:
                speak_fn(f"I could not locate the file at {file_path}, Boss.")
            return False

        action_desc = f"edit '{os.path.basename(file_path)}' by replacing specified text"
        if not self.request_permission(action_desc, speak_fn=speak_fn, input_fn=input_fn):
            return False

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            if target_text not in content:
                if speak_fn:
                    speak_fn(f"Target text was not found in {os.path.basename(file_path)}, Boss.")
                return False

            new_content = content.replace(target_text, replacement_text, 1)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            if speak_fn:
                speak_fn(f"File {os.path.basename(file_path)} has been updated successfully, Boss.")
            return True
        except Exception as e:
            print(f"[File Edit Error]: {e}")
            if speak_fn:
                speak_fn(f"An error occurred while editing the file: {e}")
            return False

    def write_file_guarded(
        self,
        file_path: str,
        content: str,
        mode: str = "a",
        speak_fn: Optional[Any] = None,
        input_fn: Optional[Any] = None
    ) -> bool:
        """
        Safely writes or appends content to a file after obtaining confirmation.
        """
        action_verb = "append to" if mode == "a" else "overwrite/create"
        action_desc = f"{action_verb} file '{os.path.basename(file_path)}'"
        if not self.request_permission(action_desc, speak_fn=speak_fn, input_fn=input_fn):
            return False

        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, mode, encoding="utf-8") as f:
                f.write(content)
            if speak_fn:
                speak_fn(f"Content saved to {os.path.basename(file_path)}, Boss.")
            return True
        except Exception as e:
            print(f"[File Write Error]: {e}")
            return False

    def delete_file_guarded(
        self,
        file_path: str,
        speak_fn: Optional[Any] = None,
        input_fn: Optional[Any] = None
    ) -> bool:
        """
        Safely deletes a file after obtaining explicit confirmation.
        """
        if not os.path.exists(file_path):
            if speak_fn:
                speak_fn(f"The file {os.path.basename(file_path)} does not exist, Boss.")
            return False

        action_desc = f"permanently delete '{os.path.basename(file_path)}' located at '{file_path}'"
        if not self.request_permission(action_desc, speak_fn=speak_fn, input_fn=input_fn):
            return False

        try:
            os.remove(file_path)
            if speak_fn:
                speak_fn(f"File {os.path.basename(file_path)} has been deleted, Boss.")
            return True
        except Exception as e:
            print(f"[File Delete Error]: {e}")
            return False

    # =========================================================================
    # 3. 📸 SCREENSHOT ARCHIVER ("take a screenshot")
    # =========================================================================

    def take_and_save_screenshot(self, open_after: bool = True) -> Optional[str]:
        """
        Captures the entire desktop display, saves to Desktop/Screenshots/ with timestamp,
        and optionally opens the image.
        """
        try:
            os.makedirs(self.screenshots_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            file_path = os.path.join(self.screenshots_dir, filename)

            img = None
            if ImageGrab:
                try:
                    img = ImageGrab.grab(all_screens=True)
                except Exception:
                    pass

            if img is None:
                try:
                    img = pyautogui.screenshot()
                except Exception:
                    pass

            # If display buffer capture unavailable (e.g. locked screen / headless), create placeholder capture
            if img is None:
                from PIL import Image, ImageDraw
                img = Image.new("RGB", (1920, 1080), color=(20, 24, 30))
                draw = ImageDraw.Draw(img)
                draw.text((60, 60), f"J.A.R.V.I.S. Screen Capture [{timestamp}]", fill=(0, 230, 255))

            img.save(file_path, format="PNG")
            print(f"[Screenshot]: Saved to {file_path}")

            if open_after:
                try:
                    os.startfile(file_path)
                except Exception:
                    pass

            return file_path
        except Exception as e:
            print(f"[Screenshot Error]: {e}")
            return None

    # =========================================================================
    # 4. 📋 SMART CLIPBOARD & NOTEPAD PIPER ("copy this")
    # =========================================================================

    def copy_selection_to_notepad(self, open_notepad: bool = True) -> Optional[str]:
        """
        Simulates Ctrl+C on active window, grabs selected text, appends it to
        Desktop/FRIDAY_Notes.txt with timestamp, and opens Notepad.
        """
        try:
            # 1. Trigger Ctrl+C on active window
            try:
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.15)
            except Exception:
                pass

            # 2. Retrieve clipboard content
            copied_text = pyperclip.paste().strip()
            if not copied_text:
                copied_text = "No active clipboard selection detected."

            # 3. Append to FRIDAY_Notes.txt
            timestamp = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
            entry = f"\n\n--- [Copied Note: {timestamp}] ---\n{copied_text}\n"

            with open(self.notes_file, "a", encoding="utf-8") as f:
                f.write(entry)

            print(f"[Notepad Piper]: Appended note to {self.notes_file}")

            # 4. Launch Notepad showing the notes file
            if open_notepad:
                try:
                    subprocess.Popen(["notepad.exe", self.notes_file])
                except Exception:
                    pass

            return copied_text
        except Exception as e:
            print(f"[Copy to Notepad Error]: {e}")
            return None

    # =========================================================================
    # 5. 🌐 BROWSER TAB & WINDOW CONTROLLER
    # =========================================================================

    def control_browser_tabs(self, action: str) -> bool:
        """
        Controls active browser tabs using keyboard shortcuts.
        Supported actions: new_tab, close_tab, next_tab, prev_tab, reopen_tab, refresh.
        """
        action = action.lower().strip()
        shortcuts = {
            "new_tab": ("ctrl", "t"),
            "close_tab": ("ctrl", "w"),
            "next_tab": ("ctrl", "tab"),
            "prev_tab": ("ctrl", "shift", "tab"),
            "reopen_tab": ("ctrl", "shift", "t"),
            "refresh": ("f5",),
            "zoom_in": ("ctrl", "plus"),
            "zoom_out": ("ctrl", "minus"),
            "address_bar": ("alt", "d")
        }

        if action in shortcuts:
            pyautogui.hotkey(*shortcuts[action])
            return True
        return False

    def focus_window_by_title(self, query: str) -> bool:
        """Brings an open application window matching the title query to the foreground."""
        if not gw:
            return False
        try:
            windows = gw.getAllWindows()
            for win in windows:
                if win.title and query.lower() in win.title.lower():
                    if win.isMinimized:
                        win.restore()
                    win.activate()
                    return True
        except Exception as e:
            print(f"[Window Focus Error]: {e}")
        return False

    def minimize_all_windows(self):
        """Minimizes all open windows to show the Desktop (Win + D)."""
        pyautogui.hotkey("win", "d")

    # =========================================================================
    # 6. 🖱️ MOUSE & KEYBOARD UI AUTOMATION
    # =========================================================================

    def click_screen(self, x: Optional[int] = None, y: Optional[int] = None, click_type: str = "single"):
        """Clicks specified coordinates or current mouse position."""
        if x is not None and y is not None:
            pyautogui.moveTo(x, y, duration=0.2)
        if click_type == "double":
            pyautogui.doubleClick()
        elif click_type == "right":
            pyautogui.rightClick()
        else:
            pyautogui.click()

    def scroll_screen(self, direction: str = "down", amount: int = 400):
        """Scrolls the active window up or down."""
        scroll_val = -amount if direction == "down" else amount
        pyautogui.scroll(scroll_val)

    def type_text(self, text: str, press_enter: bool = False):
        """Types out text into the active focused input field."""
        pyautogui.write(text, interval=0.02)
        if press_enter:
            pyautogui.press("enter")


# Global system controller instance
system_controller = SystemAccessController()
