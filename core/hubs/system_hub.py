"""
F.R.I.D.A.Y. Honeycomb System Hub
Operating system controls: application launching, process termination, shortcut crawling, sleep/shutdown, tab controls, Comm-Link audio routing, and battery monitoring.
"""

import os
import time
import shutil
import subprocess
import webbrowser
import psutil
from datetime import datetime

try:
    import pygetwindow as gw
except ImportError:
    gw = None

from core.system_access import system_controller
from core.health_check import codebase_auditor
from core.headroom_memory import memory_engine
from core.comm_link import comm_link
from core.hubs.base import play_sound, speak
from core.hubs.chat_hub import get_ai_response, handleSuggestion

USER_PATHS = [
    os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'),
    os.path.join(os.environ.get('USERPROFILE', ''), 'Documents')
]

SITES = {
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "instagram": "https://www.instagram.com",
    "chatgpt": "https://chatgpt.com",
    "google": "https://www.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "gmail": "https://mail.google.com",
    "spotify": "https://open.spotify.com"
}

def find_system_shortcut(app_name: str) -> Optional[str]:
    """Recursively walks Windows Start Menu directories and Desktop for matching shortcuts."""
    query = app_name.lower().replace(" ", "").replace("_", "").replace("-", "")
    sys_drive = os.environ.get('SystemDrive', 'C:')
    search_dirs = [
        os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
        os.path.join(os.environ.get('ProgramData', os.path.join(sys_drive, os.sep, 'ProgramData')), 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
        os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'),
        os.path.join(os.environ.get('PUBLIC', os.path.join(sys_drive, os.sep, 'Users', 'Public')), 'Desktop')
    ]
    search_dirs = [d for d in search_dirs if d and os.path.exists(d)]
    for base_dir in search_dirs:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.lower().endswith(".lnk"):
                    normalized_file = file[:-4].lower().replace(" ", "").replace("_", "").replace("-", "")
                    if query in normalized_file or normalized_file in query:
                        return os.path.join(root, file)
    return None

def find_file(filename: str) -> Optional[str]:
    """Searches across all mounted drives (C:, D:, etc.) with user priority paths."""
    results = system_controller.search_all_drives(filename, max_results=1)
    if results:
        return results[0]
    return None

def open_app(target: str) -> bool:
    """Intelligently resolves and launches applications or system tools."""
    name = target.lower().strip()
    
    # 1. Mapped Sites
    if name in SITES:
        webbrowser.open(SITES[name])
        return True

    # 2. Antigravity IDE & AI Editors (Priority 1)
    antigravity_aliases = ["antigravity", "antigravity ide", "integrity ide", "integrity", "anti gravity", "anti-gravity", "agy", "antigraviti"]
    if any(alias == name or alias in name for alias in antigravity_aliases):
        ag_paths = []
        for drive in ["C", "D", "E", "F"]:
            drive_root = os.path.join(f"{drive}:" + os.sep)
            ag_paths.append(os.path.join(drive_root, "Antigravity IDE", "Antigravity IDE.exe"))
            ag_paths.append(os.path.join(drive_root, "Antigravity IDE", "bin", "antigravity-ide.cmd"))
        ag_paths.extend([
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Antigravity IDE", "Antigravity IDE.exe"),
            os.path.join(os.environ.get("ProgramFiles", ""), "Antigravity IDE", "Antigravity IDE.exe"),
        ])
        for ag_path in ag_paths:
            if os.path.exists(ag_path):
                try:
                    if ag_path.endswith(".exe"):
                        subprocess.Popen([ag_path])
                    else:
                        subprocess.Popen(["cmd.exe", "/c", ag_path])
                    return True
                except Exception:
                    pass
        which_ag = shutil.which("antigravity") or shutil.which("agy") or shutil.which("antigravity-ide")
        if which_ag:
            try:
                subprocess.Popen(["cmd.exe", "/c", which_ag])
                return True
            except Exception:
                pass

    # 2.5. OpenCode Multi-Model Web IDE
    if "opencode" in name or "open code" in name:
        try:
            subprocess.Popen(["cmd.exe", "/c", "opencode", "web"])
            return True
        except Exception:
            pass

    # 3. Hardcoded common applications & tools
    apps = {
        "notepad": "notepad.exe", "calculator": "calc.exe", "calc": "calc.exe",
        "chrome": "chrome.exe", "brave": "brave.exe",
        "code": "code.cmd", "vscode": "code.cmd", "vs code": "code.cmd", "visual studio code": "code.cmd",
        "cmd": "cmd.exe", "command prompt": "cmd.exe", "powershell": "powershell.exe", "terminal": "wt.exe",
        "discord": "discord.exe", "spotify": "spotify.exe"
    }
    if name in apps:
        app_target = apps[name]
        try:
            if app_target.endswith(".cmd"):
                subprocess.Popen(["cmd.exe", "/c", app_target])
            else:
                subprocess.Popen(app_target)
            return True
        except Exception:
            pass

    # 4. PATH search with shutil.which
    which_path = shutil.which(name) or shutil.which(f"{name}.exe") or shutil.which(f"{name}.cmd") or shutil.which(f"{name}.bat")
    if which_path:
        try:
            if which_path.endswith(".cmd") or which_path.endswith(".bat"):
                subprocess.Popen(["cmd.exe", "/c", which_path])
            else:
                subprocess.Popen([which_path])
            return True
        except Exception:
            pass

    # 5. Dynamic Windows Start Menu & Desktop Shortcut Crawler
    shortcut_path = find_system_shortcut(name)
    if shortcut_path:
        try:
            os.startfile(shortcut_path)
            return True
        except Exception:
            pass

    # 6. Direct startfile attempt
    try:
        os.startfile(name)
        return True
    except Exception:
        pass
    
    return False

def close_app(app_name: str) -> bool:
    """Closes applications, browser tabs, or processes gracefully."""
    clean = app_name.lower().strip()
    if not clean:
        return False

    # 1. Web sites and browser tabs
    if clean in SITES or any(s in clean for s in SITES) or "tab" in clean or "page" in clean:
        target_title = clean.replace("tab", "").replace("page", "").strip()
        if target_title:
            system_controller.focus_window_by_title(target_title)
        else:
            for b in ["chrome", "brave", "edge", "firefox"]:
                if system_controller.focus_window_by_title(b):
                    break
        time.sleep(0.15)
        system_controller.control_browser_tabs("close_tab")
        return True

    # 2. Known desktop process aliases
    alias_map = {
        "calculator": ["calculatorapp.exe", "calc.exe"],
        "calc": ["calculatorapp.exe", "calc.exe"],
        "notepad": ["notepad.exe"],
        "antigravity": ["antigravity ide.exe", "antigravity.exe"],
        "integrity": ["antigravity ide.exe", "antigravity.exe"],
        "vscode": ["code.exe"],
        "code": ["code.exe"],
        "vs code": ["code.exe"],
        "terminal": ["windowsterminal.exe", "cmd.exe", "powershell.exe"],
        "cmd": ["cmd.exe"],
        "command prompt": ["cmd.exe"],
        "powershell": ["powershell.exe"],
        "spotify": ["spotify.exe"],
        "discord": ["discord.exe"],
        "chrome": ["chrome.exe"],
        "brave": ["brave.exe"],
        "edge": ["msedge.exe"]
    }
    targets = alias_map.get(clean, [clean, f"{clean}.exe"])

    for proc in psutil.process_iter(['name']):
        try:
            pname = proc.info['name'].lower()
            if any(t in pname for t in targets):
                proc.kill()
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # 3. Window title matching via pygetwindow
    if gw:
        try:
            for win in gw.getAllWindows():
                if win.title and clean in win.title.lower():
                    win.close()
                    return True
        except Exception:
            pass

    return False

def note_down(content: str) -> bool:
    """Appends dictation to Desktop friday_notes.txt and displays it."""
    desktop = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
    note_file = os.path.join(desktop, 'friday_notes.txt')
    with open(note_file, "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] : {content}")
    try:
        os.startfile(note_file)
    except Exception:
        pass
    return True

def get_system_stats() -> str:
    """Calculates CPU load, memory usage, and battery percentages."""
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    status = f"CPU load is at {cpu} percent, and system memory usage is at {ram} percent."
    if battery:
        status += f" System battery level stands at {battery.percent} percent."
    return status

def battery_monitor_sentinel():
    """Background daemon thread monitoring battery health."""
    while True:
        try:
            battery = psutil.sensors_battery()
            if battery and not battery.power_plugged and battery.percent <= 20:
                play_sound("error")
                alert_prompt = f"System alert: Laptop battery is critically low at {battery.percent} percent. Speak a calm, protective, emotionally mature warning to the Boss advising them to connect the charger soon, keeping it under two sentences."
                get_ai_response(alert_prompt, speak_stream=True)
            time.sleep(300)
        except Exception:
            time.sleep(60)

def handle_status(cmd: str):
    """Speaks real-time hardware status."""
    stats = get_system_stats()
    speak(f"Systems are completely stable, Boss. {stats}")
    handleSuggestion("Check system status")

def handle_sleep(cmd: str):
    """Puts computer to sleep after confirmation."""
    speak("Are you sure you want me to put the system to sleep, Boss?")
    conf = input("[y/n] >>> ").strip().lower()
    if "y" in conf or "yes" in conf or "do it" in conf:
        play_sound("cancel")
        speak("Powering down display systems. Sweet dreams, Sir.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else:
        speak("Standby aborted, Boss.")

def handle_shutdown(cmd: str):
    """Shuts down system after confirmation."""
    speak("Core shutdown target identified. Confirm system power down, Boss?")
    conf = input("[y/n] >>> ").strip().lower()
    if "y" in conf or "yes" in conf:
        play_sound("cancel")
        speak("Terminating all active processes. Until next time, Sir.")
        os.system("shutdown /s /t 1")
    else:
        speak("Shutdown protocol aborted, Boss.")

def handle_note(cmd: str):
    """Prompts for note content and archives it."""
    speak("What should I note down, Sir?")
    content = input("\n[Dictate Note] >>> ").strip()
    if content and note_down(content):
        play_sound("launch")
        speak("Note saved successfully, Boss.")
        handleSuggestion(f"Note down: {content}")

def handle_open(cmd: str):
    """Opens sites, local applications, or searched files."""
    target = cmd.lower().strip()
    for prefix in ["open up", "open", "launch", "start"]:
        if target.startswith(prefix):
            target = target[len(prefix):].strip()
            break
    target = target.replace("in browser", "").replace("in chrome", "").replace("in brave", "").replace("on browser", "").replace("website", "").replace("site", "").strip()

    if any(k in target for k in ["integrity", "anti gravity", "anti-gravity", "integirty", "antigravity", "agy"]):
        target = "antigravity ide"

    if "youtube" in target:
        webbrowser.open("https://www.youtube.com")
        play_sound("launch")
        speak("Opening YouTube, Boss.")
        return
    if "github" in target:
        webbrowser.open("https://www.github.com")
        play_sound("launch")
        speak("Opening GitHub, Boss.")
        return
    if "instagram" in target:
        webbrowser.open("https://www.instagram.com")
        play_sound("launch")
        speak("Opening Instagram, Boss.")
        return
    if "chatgpt" in target:
        webbrowser.open("https://chatgpt.com")
        play_sound("launch")
        speak("Opening ChatGPT, Boss.")
        return
    if "spotify" in target:
        webbrowser.open("https://open.spotify.com")
        play_sound("launch")
        speak("Opening Spotify, Boss.")
        return
    if "whatsapp" in target:
        webbrowser.open("https://web.whatsapp.com")
        play_sound("launch")
        speak("Opening WhatsApp, Boss.")
        return
    if "google" in target:
        webbrowser.open("https://www.google.com")
        play_sound("launch")
        speak("Opening Google, Boss.")
        return

    if open_app(target):
        play_sound("launch")
        display_name = "Antigravity IDE" if "antigravity" in target else target
        speak(f"Opening {display_name}, Boss.")
        handleSuggestion(f"Open app/site: {target}")
    else:
        file_path = find_file(target)
        if file_path:
            play_sound("launch")
            speak(f"Opening {os.path.basename(file_path)}, Boss.")
            os.startfile(file_path)
            handleSuggestion(f"Open file: {target}")
        else:
            play_sound("launch")
            speak(f"Opening {target} in browser, Boss.")
            webbrowser.open(f"https://www.google.com/search?q={target}")

def handle_close(cmd: str):
    """Closes applications, tabs, or focused windows."""
    raw = cmd.lower().replace("close", "").replace("band karo", "").replace("hata do", "").strip()
    app_name = re.sub(r'\b(the|tab|is|still|active|it|please|browser|window)\b', '', raw).strip()
    if not app_name:
        system_controller.control_browser_tabs("close_tab")
        play_sound("cancel")
        speak("Closed active tab, Boss.")
        return

    matched_site = None
    for s in SITES:
        if s in app_name:
            matched_site = s
            break

    target = matched_site or app_name.split()[0]
    if close_app(target):
        play_sound("cancel")
        speak(f"Closed {target}, Boss.")
    else:
        system_controller.control_browser_tabs("close_tab")
        play_sound("cancel")
        speak(f"Closed {target} tab, Boss.")

def handle_health_check(cmd: str):
    """Performs deep codebase and vulnerability audit."""
    speak("Initiating deep codebase and vulnerability audit, Boss. Stand by...")
    play_sound("launch")
    results = codebase_auditor.perform_deep_audit()
    codebase_auditor.render_audit_report(results, speak_fn=speak)

def handle_self_heal(cmd: str):
    """Triggers autonomous self-healing and restoration."""
    play_sound("launch")
    codebase_auditor.perform_self_healing(speak_fn=speak)

def handle_format_memory(cmd: str):
    """Purges and resets all long-term memory."""
    play_sound("launch")
    speak("Formatting complete long-term memory and project history, Boss. Resetting to factory state.")
    memory_engine.format_all_memory()
    speak("All memory files, project records, and session vaults have been wiped clean. We are starting completely fresh, Boss.")

def handle_copy_to_notepad(cmd: str):
    """Copies active selected text from screen and writes to Desktop."""
    speak("Copying selection to Notepad, Boss.")
    play_sound("launch")
    text = system_controller.copy_selection_to_notepad(open_notepad=True)
    if text:
        preview = text[:50] + ("..." if len(text) > 50 else "")
        speak(f"Appended note: '{preview}'. Notepad is open on your screen, Boss.")
    else:
        speak("I couldn't detect any highlighted text to copy, Boss. Make sure text is selected.")

def handle_tab_new(cmd: str):
    system_controller.control_browser_tabs("new_tab")
    speak("New tab opened, Boss.")

def handle_tab_close(cmd: str):
    system_controller.control_browser_tabs("close_tab")
    speak("Tab closed, Sir.")

def handle_tab_next(cmd: str):
    system_controller.control_browser_tabs("next_tab")

def handle_tab_prev(cmd: str):
    system_controller.control_browser_tabs("prev_tab")

def handle_tab_reopen(cmd: str):
    system_controller.control_browser_tabs("reopen_tab")
    speak("Reopening previous tab, Boss.")

def handle_minimize_all(cmd: str):
    system_controller.minimize_all_windows()
    speak("Minimizing all windows to desktop, Boss.")

def handle_scroll_down(cmd: str):
    system_controller.scroll_screen("down", amount=500)

def handle_scroll_up(cmd: str):
    system_controller.scroll_screen("up", amount=500)

def handle_guarded_edit(cmd: str):
    """Guarded file edit requiring explicit confirmation."""
    speak("What file would you like me to edit, Boss?")
    target_file = input("\n[File Path or Name to Edit] >>> ").strip()
    full_path = find_file(target_file) if not os.path.exists(target_file) else target_file

    if not full_path or not os.path.exists(full_path):
        speak(f"I could not locate '{target_file}' on any drive, Boss.")
        return

    content = system_controller.read_file(full_path, max_chars=1000)
    print(f"\n--- [Current File Preview for {os.path.basename(full_path)}] ---\n{content}\n")

    speak(f"What text inside {os.path.basename(full_path)} should I replace, Boss?")
    old_text = input("\n[Exact Text to Replace] >>> ").strip()
    speak("And what should I replace it with, Boss?")
    new_text = input("\n[New Replacement Content] >>> ").strip()

    system_controller.edit_file_guarded(full_path, old_text, new_text, speak_fn=speak)

def handle_broadcast_mode(cmd: str):
    """Comm-Link: Broadcast mode (Earbud mic -> PC room speakers)."""
    success, msg = comm_link.set_mode("broadcast")
    play_sound("launch")
    speak(msg)

def handle_whisper_mode(cmd: str):
    """Comm-Link: Stealth / whisper mode (Earbud mic -> In-Ear output)."""
    success, msg = comm_link.set_mode("whisper")
    play_sound("launch")
    speak(msg)

def handle_dual_audio_mode(cmd: str):
    """Comm-Link: Dual audio mode (Synchronized Earbud + PC speakers)."""
    success, msg = comm_link.set_mode("dual")
    play_sound("launch")
    speak(msg)

def handle_audio_health(cmd: str):
    """Comm-Link: Audio telemetry status."""
    play_sound("launch")
    speech = comm_link.get_health_speech()
    speak(speech)

COMMANDS = {
    "friday broadcast mode": handle_broadcast_mode,
    "broadcast mode": handle_broadcast_mode,
    "speaker mode": handle_broadcast_mode,
    "speaker pe aao": handle_broadcast_mode,
    "sabko sunao": handle_broadcast_mode,
    "friday whisper mode": handle_whisper_mode,
    "whisper mode": handle_whisper_mode,
    "stealth mode": handle_whisper_mode,
    "private mode": handle_whisper_mode,
    "kaan mein bolo": handle_whisper_mode,
    "sirf kaan mein": handle_whisper_mode,
    "friday dual audio mode": handle_dual_audio_mode,
    "dual audio mode": handle_dual_audio_mode,
    "dual audio": handle_dual_audio_mode,
    "mirror audio": handle_dual_audio_mode,
    "dono pe aao": handle_dual_audio_mode,
    "friday audio health": handle_audio_health,
    "audio health": handle_audio_health,
    "comm link status": handle_audio_health,
    "comm link": handle_audio_health,
    "audio status": handle_audio_health,
    "friday health check": handle_health_check,
    "codebase health check": handle_health_check,
    "system health check": handle_health_check,
    "codebase health": handle_health_check,
    "health check": handle_health_check,
    "audit codebase": handle_health_check,
    "scan codebase": handle_health_check,
    "health": handle_health_check,
    "friday heal yourself": handle_self_heal,
    "heal yourself": handle_self_heal,
    "auto heal": handle_self_heal,
    "self heal": handle_self_heal,
    "heal system": handle_self_heal,
    "heal codebase": handle_self_heal,
    "fix the issues": handle_self_heal,
    "fix the errors": handle_self_heal,
    "solve the error by yourself": handle_self_heal,
    "solve the errors by yourself": handle_self_heal,
    "can you solve the error by yourself": handle_self_heal,
    "can you solve the errors by yourself": handle_self_heal,
    "solve the errors that are you listed": handle_self_heal,
    "solve the errors that you listed": handle_self_heal,
    "solve the errors you listed": handle_self_heal,
    "solve the errors": handle_self_heal,
    "solve the error": handle_self_heal,
    "fix the errors you listed": handle_self_heal,
    "fix audit errors": handle_self_heal,
    "fix the error": handle_self_heal,
    "format memory": handle_format_memory,
    "format all memory": handle_format_memory,
    "format whole memory": handle_format_memory,
    "format fridays whole memory": handle_format_memory,
    "clear memory": handle_format_memory,
    "clear all memory": handle_format_memory,
    "reset memory": handle_format_memory,
    "reset all memory": handle_format_memory,
    "wipe memory": handle_format_memory,
    "forget everything": handle_format_memory,
    "start new": handle_format_memory,
    "start fresh": handle_format_memory,
    "copy this": handle_copy_to_notepad,
    "copy to notepad": handle_copy_to_notepad,
    "paste this in notepad": handle_copy_to_notepad,
    "save to notepad": handle_copy_to_notepad,
    "open new tab": handle_tab_new,
    "new tab": handle_tab_new,
    "close this tab": handle_tab_close,
    "close tab": handle_tab_close,
    "close the tab": handle_tab_close,
    "tab band karo": handle_tab_close,
    "next tab": handle_tab_next,
    "switch tab": handle_tab_next,
    "previous tab": handle_tab_prev,
    "reopen tab": handle_tab_reopen,
    "minimize all": handle_minimize_all,
    "show desktop": handle_minimize_all,
    "scroll down": handle_scroll_down,
    "scroll up": handle_scroll_up,
    "edit file": handle_guarded_edit,
    "edit a file": handle_guarded_edit,
    "modify file": handle_guarded_edit,
    "status": handle_status,
    "system": handle_status,
    "sleep": handle_sleep,
    "shutdown": handle_shutdown,
    "close youtube tab": handle_close,
    "close the youtube": handle_close,
    "close youtube": handle_close,
    "close google": handle_close,
    "close github": handle_close,
    "close chatgpt": handle_close,
    "close whatsapp": handle_close,
    "close instagram": handle_close,
    "band karo": handle_close,
    "close": handle_close,
    "note": handle_note,
    "open": handle_open
}
