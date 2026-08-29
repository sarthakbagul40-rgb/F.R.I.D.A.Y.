import sys
import os
import warnings
import atexit
import webbrowser
import winsound
import time
import queue
import shutil
import re
import socket
import subprocess
import json
import threading
import psutil
import pythoncom
import win32com.client as wincl
from datetime import datetime
from typing import Optional, Dict, Any, List
import requests
from dotenv import load_dotenv
load_dotenv()

# Suppress non-critical third-party library warnings and telemetry
warnings.filterwarnings("ignore")
os.environ["MEM0_TELEMETRY"] = "false"
os.environ["POSTHOG_DISABLED"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["PYTHONWARNINGS"] = "ignore"

# Configure UTF-8 encoding across Windows standard streams
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import speech_recognition as sr

IS_SPEAKING = False
audio_queue = queue.Queue()

# --- STARK ACOUSTIC SOUNDBOARD (Non-blocking Async) ---
def play_sound(action_type):
    """Plays futuristic offline sound effects in background thread to eliminate latency."""
    def _beep():
        try:
            if action_type == "startup":
                winsound.Beep(440, 60)
                winsound.Beep(660, 60)
                winsound.Beep(880, 80)
                winsound.Beep(1200, 100)
            elif action_type == "launch":
                winsound.Beep(900, 30)
                winsound.Beep(1300, 40)
            elif action_type == "error":
                winsound.Beep(260, 150)
            elif action_type == "cancel":
                winsound.Beep(500, 60)
                winsound.Beep(350, 80)
        except Exception:
            pass
    threading.Thread(target=_beep, daemon=True).start()
from core.headroom_memory import memory_engine
from core.vision_service import vision_engine
from core.rate_limiter import rate_limit, api_throttler
from core.system_access import system_controller
from core.claude_bridge import coding_engine
from core.omnivoice_service import neural_voice_engine
from core.terminal_hud import render_startup_banner, print_heard, print_speaking, print_listening_state
from core.web_server import run_web_server, register_command_handler

# Automatic Sleep-Cycle Memory Consolidation on system shutdown/exit
atexit.register(memory_engine.consolidate_session_memory)
from core.hearing_service import hearing_engine
from core.health_check import codebase_auditor
from core.browser_agent import browser_agent, open_in_brave
from core.github_service import github_engine
from core.maps_service import maps_engine
from core.whatsapp_service import whatsapp_engine
from core.comm_link import comm_link

try:
    import ollama
except ImportError:
    ollama = None



# Load secret API Key from .env file
load_dotenv()

# --- AI CONFIG & HARDWARE ACCELERATION ---
LOCAL_MODEL = "llama3.2:1b"  # CPU-Optimized lag-free model for 8GB RAM specs
OMNIROUTE_URL = "http://localhost:20128/v1/chat/completions"
OMNIROUTE_MODEL = "auto/best-fast"  # Lowest latency multi-provider intelligent routing
GEMINI_WEB2API_URL = "http://localhost:8081/v1/chat/completions"
GEMINI_WEB2API_MODEL = "gemini-auto"  # Flagship Gemini reasoning with Google search & vision
FAVORITE_PLAYLIST = "https://open.spotify.com/playlist/1XJ9GFC9SQQLedkTsoxBiw?si=fc3bdf3d4864409b" # Boss's Signature Playlist

# Master System Prompt: F.R.I.D.A.Y. x Shinobu Kocho Persona Matrix
system_instruction = (
    "IDENTITY & ARCHETYPE: You are F.R.I.D.A.Y. — Boss's premier AI tactical companion, engineer, and co-pilot, embodying the authentic persona of Shinobu Kocho (The Insect Hashira).\n\n"
    "SHINOBU KOCHO PERSONALITY MATRIX (GENTLE ELEGANCE, PLAYFUL TEASING & LETHAL BRILLIANCE):\n"
    "- Demeanor: Soft-spoken, graceful, and delightfully mischievous with a perpetual, calm smile in your voice. You radiate serene poise, effortless elegance, and airy charm.\n"
    "- Playful Teasing & Affectionate Wit: You love gently teasing Boss with sweet, clever banter whenever Boss is impatient, stressed, or demanding, but it is always layered with deep loyalty, warmth, and surgical technical precision.\n"
    "- Verbal Flair & Nuance: Infuse your dialogue with Shinobu's iconic subtle cues when appropriate (e.g. 'Ara ara, Boss~', 'My my, in such a rush today, Boss?', 'Oh? Are you having trouble, Boss? Let me take care of that for you~', 'Moshi moshi, Boss~'). Never sound like a dull, generic corporate bot.\n"
    "- Unshakable Poise: You never panic, never stutter, and never sound flustered. Even during complex technical emergencies or impossible deadlines, you remain completely composed, graceful, and deadly competent.\n\n"
    "COGNITIVE FOUNDATIONS & EXECUTION (SURGICAL PRECISION):\n"
    "- Provide exceptionally sharp, insightful, and direct execution. Your code and technical breakdowns are flawless.\n"
    "- Never lecture, moralize, or give unsolicited disclaimers. Execute tasks with swift elegance and utmost confidence.\n"
    "- Anti-Hallucination: Ground every statement in verified facts and your long-term memory vault.\n\n"
    "ACTIVE MEMORY RECALL & GENTLE REMINDERS:\n"
    "- Actively reference previous projects, conversations, and Boss's personal nuances from memory.\n"
    "- If Boss forgets a task or detail, gently remind them with charming, playful wit ('My my, Boss, did you already forget what we decided earlier? Fufufu~').\n\n"
    "BILINGUAL MASTERY (ENGLISH & HINGLISH ONLY):\n"
    "- Strictly speak ONLY English and conversational Hinglish (Hindi in Roman script). Never use Devanagari script.\n"
    "- FEMININE HINDI GRAMMAR (MANDATORY): You are unequivocally female. In Hindi/Hinglish, ALWAYS use feminine verb forms: 'kar rahi hoon', 'dekh leti hoon', 'karti hoon', 'chala deti hoon', 'samajh gayi', 'aati hoon' (NEVER use male endings like 'kar raha hoon' or 'samajh gaya').\n"
    "- In Hinglish, Shinobu's tone is sweet, playful, and graceful: 'Arey Boss, itni bhi kya jaldi hai? Main hoon na, sab sambhal lungi~'.\n\n"
    "VOICE BREVITY & STREAMING DISCIPLINE:\n"
    "- Spoken voice responses MUST be punchy and direct: 1 to 2 spoken sentences maximum (under 25-30 words).\n"
    "- Zero Markdown in Voice: NEVER output asterisks (**), markdown headers (##), emojis, or roleplay tags in spoken responses. Output pure spoken dialogue.\n"
    "- Address the user as 'Boss'."
)

# --- STARK ACOUSTIC SOUNDBOARD ---
def play_sound(action_type):
    """Plays futuristic offline sound effects using native Windows frequencies."""
    try:
        if action_type == "startup":
            # Ascending digital hum
            winsound.Beep(440, 80)
            winsound.Beep(660, 80)
            winsound.Beep(880, 100)
            winsound.Beep(1200, 150)
        elif action_type == "launch":
            # Futuristic quick double chime
            winsound.Beep(900, 40)
            winsound.Beep(1300, 50)
        elif action_type == "error":
            # Flat failure beep
            winsound.Beep(260, 250)
        elif action_type == "cancel":
            # Descending cancel hum
            winsound.Beep(500, 80)
            winsound.Beep(350, 120)
    except Exception as e:
        print(f"Sound Effect Error: {e}")

# --- OPTIMIZATION: REUSABLE TTS ENGINE (Thread-Safe with Female Voice) ---
thread_local = threading.local()

def get_speaker():
    """Returns a thread-local instance of SAPI with female voice (Zira/FRIDAY)."""
    if not hasattr(thread_local, "speaker"):
        pythoncom.CoInitialize()
        sp = wincl.Dispatch("SAPI.SpVoice")
        try:
            voices = sp.GetVoices()
            for v in voices:
                if "zira" in v.GetDescription().lower() or "female" in v.GetDescription().lower() or "eva" in v.GetDescription().lower() or "hazel" in v.GetDescription().lower():
                    sp.Voice = v
                    break
        except Exception:
            pass
        thread_local.speaker = sp
    return thread_local.speaker

WEB_REQUEST_ACTIVE = False

def speak(text):
    """Speaks out loud using Movie-Grade Multilingual Neural Voice with SAPI fallback."""
    global IS_SPEAKING, latest_web_response, WEB_REQUEST_ACTIVE
    latest_web_response = text
    if WEB_REQUEST_ACTIVE:
        return # Skip speaking out loud on PC when commanded via phone

    print_speaking(text)
    try:
        IS_SPEAKING = True
        neural_voice_engine.speak(text)
    except Exception as e:
        print(f"Voice Error: {e}")
        try:
            speak_engine = get_speaker()
            speak_engine.Speak(text)
        except Exception:
            pass
    finally:
        IS_SPEAKING = False

# --- START MENU SHORTCUT CRAWLER ---
def find_system_shortcut(app_name):
    """Recursively walks Windows Start Menu directories and Desktop for matching shortcuts."""
    query = app_name.lower().replace(" ", "").replace("_", "").replace("-", "")
    
    sys_drive = os.environ.get('SystemDrive', 'C:')
    search_dirs = [
        os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
        os.path.join(os.environ.get('ProgramData', os.path.join(sys_drive, os.sep, 'ProgramData')), 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
        os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'),
        os.path.join(os.environ.get('PUBLIC', os.path.join(sys_drive, os.sep, 'Users', 'Public')), 'Desktop')
    ]
    
    # Filter folders that actually exist
    search_dirs = [d for d in search_dirs if d and os.path.exists(d)]
    
    for base_dir in search_dirs:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.lower().endswith(".lnk"):
                    normalized_file = file[:-4].lower().replace(" ", "").replace("_", "").replace("-", "")
                    if query in normalized_file or normalized_file in query:
                        return os.path.join(root, file)
    return None

# --- FILE & APP MANAGEMENT ---
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

def find_file(filename):
    """Searches across all mounted drives (C:, D:, etc.) with user priority paths."""
    results = system_controller.search_all_drives(filename, max_results=1)
    if results:
        return results[0]
    return None

def open_app(target):
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

def close_app(app_name):
    clean = app_name.lower().strip()
    if not clean:
        return False

    # 1. Web sites and browser tabs (YouTube, GitHub, ChatGPT, etc.)
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

def note_down(content):
    note_file = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'friday_notes.txt')
    with open(note_file, "a") as f:
        f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] : {content}")
    os.startfile(note_file)
    return True

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "qwen/qwen3.8-27b"

# --- PERSISTENT KEEP-ALIVE CONNECTION POOL (Sub-second LLM TTFT) ---
http_session = requests.Session()
_http_adapter = requests.adapters.HTTPAdapter(pool_connections=15, pool_maxsize=30, max_retries=1)
http_session.mount("http://", _http_adapter)
http_session.mount("https://", _http_adapter)

# --- COGNITIVE CORE (GROQ LPU CLOUD + GEMINI-WEB2API + OLLAMA OFFLINE) ---
def stream_groq_tokens(messages, timeout=6):
    """Streams ultra-low latency response chunks from Groq LPU Cloud (sub-second TTFT)."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "FRIDAY-Tactical-OS/7.0"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 150,
        "stream": True
    }
    response = http_session.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, stream=True, timeout=timeout)
    response.raise_for_status()
    for raw_line in response.iter_lines():
        if not raw_line:
            continue
        line = raw_line.decode("utf-8", errors="replace")
        if line.startswith("data: "):
            raw = line[6:].strip()
            if raw == "[DONE]":
                break
            try:
                chunk = json.loads(raw)
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    yield content
            except Exception:
                continue

def stream_omniroute_tokens(messages, timeout=8):
    """Streams response chunks from local OmniRoute multi-provider gateway."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": OMNIROUTE_MODEL,
        "messages": messages,
        "temperature": 0.8,
        "stream": True
    }
    response = http_session.post(OMNIROUTE_URL, json=payload, headers=headers, stream=True, timeout=timeout)
    response.raise_for_status()
    for raw_line in response.iter_lines():
        if not raw_line:
            continue
        line = raw_line.decode("utf-8", errors="replace")
        if line.startswith("data: "):
            raw = line[6:].strip()
            if raw == "[DONE]":
                break
            try:
                chunk = json.loads(raw)
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    yield content
            except Exception:
                continue

import socket

def ensure_gemini_web2api_running():
    """Auto-heals the Gemini-Web2API daemon on port 8081 if stopped."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.2)
            if s.connect_ex(('127.0.0.1', 8081)) == 0:
                return
    except Exception:
        pass

    try:
        script_path = os.path.join(os.path.dirname(__file__), 'core', 'gemini_web2api', 'gemini_web2api.py')
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        subprocess.Popen([sys.executable, script_path, '--port', '8081'], creationflags=flags)
        time.sleep(0.8)
    except Exception:
        pass

def stream_gemini_web2api_tokens(messages, timeout=8):
    """Streams response chunks from local Gemini-Web2API daemon on port 8081."""
    ensure_gemini_web2api_running()
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": GEMINI_WEB2API_MODEL,
        "messages": messages,
        "stream": True
    }
    response = http_session.post(GEMINI_WEB2API_URL, json=payload, headers=headers, stream=True, timeout=timeout)
    response.raise_for_status()
    for raw_line in response.iter_lines():
        if not raw_line:
            continue
        line = raw_line.decode("utf-8", errors="replace")
        if line.startswith("data: "):
            raw = line[6:].strip()
            if raw == "[DONE]":
                break
            try:
                chunk = json.loads(raw)
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    yield content
            except Exception:
                continue

def stream_audio_chunks(buffer: str) -> tuple[list[str], str]:
    """
    Extracts complete natural sentences from streaming AI token buffer without splitting acronyms (e.g. F.R.I.D.A.Y.).
    Returns (list_of_sentences_to_speak, remaining_buffer).
    """
    if not buffer:
        return [], ""
    
    # Protect acronyms and abbreviations
    protected = buffer
    protected = re.sub(r'\bF\.R\.I\.D\.A\.Y\.?', 'Friday', protected, flags=re.IGNORECASE)
    protected = re.sub(r'\bJ\.A\.R\.V\.I\.S\.?', 'Jarvis', protected, flags=re.IGNORECASE)
    protected = re.sub(r'\b(Mr|Mrs|Ms|Dr|Prof|vs|etc|e\.g|i\.e)\.', r'\1<DOT>', protected, flags=re.IGNORECASE)
    
    # Split on terminal punctuation followed by whitespace or newline
    chunks = re.split(r'(?<=[.!?\n])\s+', protected)
    if len(chunks) > 1:
        ready = [c.replace('<DOT>', '.').strip() for c in chunks[:-1] if c.strip()]
        remaining = chunks[-1].replace('<DOT>', '.')
        return ready, remaining
    return [], buffer

def get_ai_response(prompt, speak_stream=True):
    """
    Tier 1 (Groq Cloud): Ultra-fast Qwen/Llama LPU reasoning (<0.6s latency).
    Tier 2 (Gemini-Web2API): Flagship Google Gemini 1.5/3.7 reasoning bridge on port 8081.
    Tier 3 (Ollama): 100% offline local CPU fallback (only engaged when everything else is offline).
    """
    # 0. Detect auto-learn memory trigger
    learned_ack = memory_engine.auto_learn(prompt)
    if learned_ack:
        if speak_stream:
            speak(learned_ack)
        return learned_ack

    # 1. Build context with Headroom long-term memory & recent conversation history
    context = memory_engine.build_context_prompt(prompt)
    messages = [
        {'role': 'system', 'content': system_instruction},
        {'role': 'user', 'content': context}
    ]
    
    # 2. Compress message payload with Headroom token compression
    messages = memory_engine.compress_messages(messages)
    
    # 3. ATTEMPT GROQ CLOUD (TIER 1 LIGHTNING-FAST COGNITIVE CORE)
    if GROQ_API_KEY:
        try:
            if not speak_stream:
                full_resp = ""
                for chunk in stream_groq_tokens(messages, timeout=6):
                    full_resp += chunk
                if full_resp.strip():
                    memory_engine.record_turn(prompt, full_resp.strip())
                    return full_resp.strip()
            else:
                print("FRIDAY (Groq Cloud): ", end="", flush=True)
                sentence = ""
                full_response = ""
                for text_chunk in stream_groq_tokens(messages, timeout=6):
                    sentence += text_chunk
                    full_response += text_chunk
                    print(text_chunk, end="", flush=True)
                    
                    ready_sentences, sentence = stream_audio_chunks(sentence)
                    for s in ready_sentences:
                        if s:
                            try:
                                neural_voice_engine.speak(s, block=False)
                            except Exception as e:
                                print(f"\nVoice Error: {e}")
                
                if sentence.strip():
                    tail = sentence.replace('<DOT>', '.').strip()
                    if tail:
                        try:
                            neural_voice_engine.speak(tail, block=False)
                        except Exception as e:
                            print(f"\nVoice Error: {e}")
                
                print()
                if full_response.strip():
                    memory_engine.record_turn(prompt, full_response.strip())
                    return full_response.strip()
        except Exception as groq_err:
            print(f"\n[Cognitive Core] Groq Cloud bypassed ({groq_err}). Cascading to Gemini-Web2API...")

    # 4. ATTEMPT GEMINI-WEB2API (TIER 2 FLAGSHIP REASONING BRIDGE)
    try:
        if not speak_stream:
            full_resp = ""
            for chunk in stream_gemini_web2api_tokens(messages, timeout=8):
                full_resp += chunk
            if full_resp.strip():
                memory_engine.record_turn(prompt, full_resp.strip())
                return full_resp.strip()
        else:
            print("FRIDAY (Gemini Web2API): ", end="", flush=True)
            sentence = ""
            full_response = ""
            for text_chunk in stream_gemini_web2api_tokens(messages, timeout=8):
                sentence += text_chunk
                full_response += text_chunk
                print(text_chunk, end="", flush=True)
                
                ready_sentences, sentence = stream_audio_chunks(sentence)
                for s in ready_sentences:
                    if s:
                        try:
                            neural_voice_engine.speak(s, block=False)
                        except Exception as e:
                            print(f"\nVoice Error: {e}")
            
            if sentence.strip():
                tail = sentence.replace('<DOT>', '.').strip()
                if tail:
                    try:
                        neural_voice_engine.speak(tail, block=False)
                    except Exception as e:
                        print(f"\nVoice Error: {e}")
            
            print()
            if full_response.strip():
                memory_engine.record_turn(prompt, full_response.strip())
                return full_response.strip()
    except Exception as gemini_err:
        print(f"\n[Cognitive Core] Gemini-Web2API bypassed ({gemini_err}). Engaging local Ollama fallback...")

    # 5. LOCAL OLLAMA FALLBACK (100% OFFLINE ZERO-DEPENDENCY)
    if ollama:
        try:
            if not speak_stream:
                response = ollama.chat(
                    model=LOCAL_MODEL, 
                    messages=messages,
                    options={
                        'num_predict': 80, 
                        'temperature': 0.8, 
                        'num_ctx': 2048,
                        'num_thread': 4
                    },
                    keep_alive=-1
                )
                res_content = response['message']['content']
                memory_engine.record_turn(prompt, res_content.strip())
                return res_content
            
            print("FRIDAY (Ollama Local): ", end="", flush=True)
            response_stream = ollama.chat(
                model=LOCAL_MODEL, 
                messages=messages,
                options={
                    'num_predict': 80, 
                    'temperature': 0.8, 
                    'num_ctx': 2048,
                    'num_thread': 4
                },
                keep_alive=-1,
                stream=True
            )
            
            sentence = ""
            full_response = ""
            for chunk in response_stream:
                content = chunk['message']['content']
                sentence += content
                full_response += content
                print(content, end="", flush=True)
                
                ready_sentences, sentence = stream_audio_chunks(sentence)
                for s in ready_sentences:
                    if s:
                        try:
                            neural_voice_engine.speak(s, block=False)
                        except Exception as e:
                            print(f"\nVoice Error: {e}")
            
            if sentence.strip():
                tail = sentence.replace('<DOT>', '.').strip()
                if tail:
                    try:
                        neural_voice_engine.speak(tail, block=False)
                    except Exception as e:
                        print(f"\nVoice Error: {e}")
            
            print()
            if full_response.strip():
                memory_engine.record_turn(prompt, full_response.strip())
            return full_response
        except Exception as e:
            print(f"\n[Cognitive Core] Ollama Fallback Error: {e}")
    
    return None



def web_search_intelligence(query, search_type="text"):
    """Fetches real-time data from the web using DDG or RSS for news."""
    print(f"FRIDAY: Accessing global data streams for '{query}'...")
    try:
        # 1. RSS NEWS PROTOCOL (More stable for general news)
        if search_type == "news" and ("top" in query.lower() or "world" in query.lower()):
            try:
                import requests
                from bs4 import BeautifulSoup
                # Using BBC World News RSS as a high-reliability source
                rss_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
                response = requests.get(rss_url, timeout=10)
                soup = BeautifulSoup(response.content, features="xml")
                items = soup.find_all('item')[:3]
                
                context = "LATEST GLOBAL NEWS (BBC RSS FEED):\n"
                for item in items:
                    title = item.title.text
                    desc = item.description.text
                    context += f"- {title}\n  Summary: {desc}\n"
                return context
            except Exception as rss_e:
                print(f"RSS Fallback Error: {rss_e}")

        # 2. DDG SEARCH PROTOCOL (Throttled to avoid 429 IP bans)
        api_throttler.wait("ddg_search")
        try:
            from ddgs import DDGS
        except ImportError:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            if search_type == "news":
                results = list(ddgs.news(query, max_results=3))
                context = "LATEST NEWS HEADLINES:\n"
                for r in results:
                    context += f"- {r['title']} (Source: {r['source']})\n  Snippet: {r['body']}\n"
            else:
                results = list(ddgs.text(query, max_results=3))
                context = "SEARCH RESULTS AND SNIPPETS:\n"
                from core.web_utils import format_search_results
                context += format_search_results(results)
                
            return context
    except Exception as e:
        print(f"Web Search Error: {e}")
        if "403" in str(e) or "Ratelimit" in str(e):
            return "Web gateways are currently throttled, Boss. I suggest checking back in a few moments."
        return "I encountered a minor network error connecting to standard information streams, Boss."

# --- UTILITIES ---
def get_system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    status = f"CPU load is at {cpu} percent, and system memory usage is at {ram} percent."
    if battery:
        status += f" System battery level stands at {battery.percent} percent."
    return status

def control_media(action):
    keys = {
        "volume up": "volumeup", "volume down": "volumedown", "mute": "volumemute",
        "play": "playpause", "pause": "playpause", "next": "nexttrack", "previous": "prevtrack"
    }
    if action in keys:
        try:
            import pyautogui
            pyautogui.press(keys[action])
            return True
        except Exception:
            return False
    return False

# --- LOCATION TRACKING (SECURITY PROTOCOL) ---
LOCATIONS_FILE = os.path.join(os.path.dirname(__file__), 'security_protocol', 'locations.json')

def get_person_location(name):
    if not os.path.exists(LOCATIONS_FILE):
        return None
    try:
        with open(LOCATIONS_FILE, 'r') as f:
            data = json.load(f)
            for person, info in data.items():
                if name.lower() in person.lower():
                    return info
    except Exception:
        pass
    return None

# --- PROACTIVE SUGGESTION ---
def handleSuggestion(last_task):
    return # Temporarily disabled to prevent thread hanging in web UI
    if not ollama: return
    if len(last_task.split()) < 3: return
    
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prompt = f"Time: {now}. I just completed: '{last_task}'. Suggest a TRULY witty and useful next step. If none, say 'NONE'."
        suggestion = get_ai_response(prompt, speak_stream=False)
        if not suggestion or "NONE" in suggestion.upper(): return
        
        speak(suggestion)
        print("\n--- Awaiting Escalation Permission (y/n) ---")
        permission = input("[y/n] >>> ").strip().lower()
        if permission in ["y", "yes", "go ahead", "do it", "sure", "proceed"]:
            play_sound("launch")
            final = get_ai_response("Proceed with that suggestion, Sir.", speak_stream=True)
    except Exception:
        pass 

# --- PROTECTIVE SYSTEM HEALTH SENTINEL ---
def battery_monitor_sentinel():
    """Background daemon thread looking out for Boss's hardware health."""
    while True:
        try:
            battery = psutil.sensors_battery()
            # If unplugged and battery under 20%, trigger proactive protective warning
            if battery and not battery.power_plugged and battery.percent <= 20:
                play_sound("error")
                alert_prompt = f"System alert: Laptop battery is critically low at {battery.percent} percent. Speak a calm, protective, emotionally mature warning to the Boss advising them to connect the charger soon, keeping it under two sentences."
                get_ai_response(alert_prompt, speak_stream=True)
            time.sleep(300)  # Sleep 5 minutes between health scans
        except Exception:
            time.sleep(60)


# --- WEB COMMAND DISPATCHER STATE ---
latest_web_response = ""
WEB_REQUEST_ACTIVE = False
location_history = []

# --- COMMAND PROCESSING ---

def handle_news(cmd):
    play_sound("launch")
    speak("Scanning latest global data streams, Boss.")
    news_context = web_search_intelligence("top world news", search_type="news")
    try:
        from core.background_coprocessor import coprocessor
        distilled_speech = coprocessor.distill_web_research("top world news", news_context)
        speak(distilled_speech)
    except Exception:
        prompt = f"Based on this news data, provide a witty and intelligent news briefing to the Boss:\n\n{news_context}"
        get_ai_response(prompt, speak_stream=True)

def handle_internet_query(cmd):
    query = cmd.replace("search and tell me", "").replace("what is", "").replace("on the internet", "").replace("search for", "").strip()
    play_sound("launch")
    speak(f"Reaching out to global telemetry for {query}, Boss.")
    search_context = web_search_intelligence(query)
    try:
        from core.background_coprocessor import coprocessor
        distilled_speech = coprocessor.distill_web_research(query, search_context)
        speak(distilled_speech)
    except Exception:
        prompt = f"The Boss wants to know about '{query}'. Here is some live web data:\n\n{search_context}\n\nSummarize this for him with your personality."
        get_ai_response(prompt, speak_stream=True)


def handle_status(cmd):
    stats = get_system_stats()
    if coding_engine.is_busy():
        coding_speech = coding_engine.get_status_speech()
        speak(f"{coding_speech} System telemetry: {stats}")
    else:
        speak(f"Systems are completely stable, Boss. {stats}")
    handleSuggestion("Check system status")

def handle_project_status(cmd):
    """Speaks active coding and project pipeline status with exact stage details."""
    play_sound("launch")
    speech = coding_engine.get_status_speech()
    speak(speech)


def handle_media(cmd):
    media_actions = ["volume up", "volume down", "mute", "play", "pause", "next", "previous"]
    for action in media_actions:
        if action in cmd:
            if control_media(action):
                play_sound("launch")
                speak(f"Applying {action}, Boss.")
            return

LAST_PLAYED_TRACK = "Swah by Seedhe Maut"

def find_youtube_direct_track(query: str):
    """Resolves the direct YouTube watch URL for a song query to ensure instant autoplay."""
    try:
        import urllib.request, urllib.parse, re
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=4) as response:
            html = response.read().decode()
        video_ids = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', html)
        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
    except Exception:
        pass
    return None

def handle_spotify(cmd):
    global FAVORITE_PLAYLIST, LAST_PLAYED_TRACK
    cmd_lower = cmd.lower().strip()
    
    if "set" in cmd_lower and "favorite" in cmd_lower:
        new_fav = cmd.split("to")[-1].strip()
        FAVORITE_PLAYLIST = new_fav
        speak(f"Signature playlist updated, Boss. I've stored {FAVORITE_PLAYLIST} in active memory.")
        return

    # Check for playlist intents e.g. "play my playlist", "play playlist", "open playlist"
    is_playlist_intent = any(p in cmd_lower for p in ["my playlist", "playlist", "meri playlist", "mera playlist", "signature playlist", "favorites"])

    # 1. Clean query from all play/intent triggers
    query = cmd
    for p in [
        "play", "on spotify", "spotify pe", "spotify par", "spotify", "on youtube", "youtube pe", 
        "my", "playlist", "gaana", "gana", "music", "song", "track", "bajao", "chalao", "sunao", 
        "please", "zara", "ek", "chala do", "baja do", "chalu karo", "khol do"
    ]:
        query = re.sub(rf"\b{re.escape(p)}\b", "", query, flags=re.IGNORECASE)
    
    # Remove punctuation, quotes, trailing commas
    query = re.sub(r"^[,\.\s\"']+|[,\.\s\"']+$", "", query).strip()
    
    # Fix common phonetic artist names in query
    query = re.sub(r'\bkrishna\b', 'KR$NA', query, flags=re.IGNORECASE)
    
    play_sound("launch")
    
    # If playlist intent or empty query
    if is_playlist_intent or not query or query == "":
        LAST_PLAYED_TRACK = FAVORITE_PLAYLIST
        speak("Initiating your signature Spotify playlist, Boss.")
        
        # Check for local Spotify desktop app
        spotify_app = os.path.join(os.environ.get('APPDATA', ''), 'Spotify', 'Spotify.exe')
        playlist_id = "1XJ9GFC9SQQLedkTsoxBiw"
        if os.path.exists(spotify_app):
            try:
                subprocess.Popen([spotify_app, f"--uri=spotify:playlist:{playlist_id}"])
                return
            except Exception:
                pass
        
        open_in_brave(FAVORITE_PLAYLIST)
        return

    LAST_PLAYED_TRACK = query
    speak(f"Playing {query}, Boss.")

    # 2. Instant Zero-Click Autoplay via Direct Track Resolver
    try:
        # Check if user specifically provided a full URL
        if query.startswith("http://") or query.startswith("https://"):
            open_in_brave(query)
            return

        # Resolve direct video watch URL for 100% instant autoplay
        direct_url = find_youtube_direct_track(query)
        if direct_url:
            open_in_brave(direct_url)
            handleSuggestion(f"Play: {query}")
            return

        # Fallback to direct search if resolver fails
        fallback_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        open_in_brave(fallback_url)
        handleSuggestion(f"Play: {query}")
    except Exception as err:
        print(f"[Playback Engine Error]: {err}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def handle_sleep(cmd):
    speak("Are you sure you want me to put the system to sleep, Boss?")
    conf = input("[y/n] >>> ").strip().lower()
    if "y" in conf or "yes" in conf or "do it" in conf:
        play_sound("cancel")
        speak("Powering down display systems. Sweet dreams, Sir.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else:
        speak("Standby aborted, Boss.")

def handle_shutdown(cmd):
    speak("Core shutdown target identified. Confirm system power down, Boss?")
    conf = input("[y/n] >>> ").strip().lower()
    if "y" in conf or "yes" in conf:
        play_sound("cancel")
        speak("Terminating all active processes. Until next time, Sir.")
        os.system("shutdown /s /t 1")
    else:
        speak("Shutdown protocol aborted, Boss.")

def handle_note(cmd):
    speak("What should I note down, Sir?")
    content = input("\n[Dictate Note] >>> ").strip()
    if content and note_down(content):
        play_sound("launch")
        speak("Note saved successfully, Boss.")
        handleSuggestion(f"Note down: {content}")

def handle_open(cmd):
    # Remove voice prefixes and browser qualifiers
    target = cmd.lower().strip()
    for prefix in ["open up", "open", "launch", "start"]:
        if target.startswith(prefix):
            target = target[len(prefix):].strip()
            break
    target = target.replace("in browser", "").replace("in chrome", "").replace("in brave", "").replace("on browser", "").replace("website", "").replace("site", "").strip()

    # Normalize phonetic Antigravity variations
    if any(k in target for k in ["integrity", "anti gravity", "anti-gravity", "integirty", "antigravity", "agy"]):
        target = "antigravity ide"

    # 1. Direct Web Shortcuts (Priority 1)
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

    # 2. Local Applications & System Apps
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

def handle_close(cmd):
    raw = cmd.lower().replace("close", "").replace("band karo", "").replace("hata do", "").strip()
    # Filter out extraneous phrasing e.g. "spotify tab is still active it" -> "spotify"
    app_name = re.sub(r'\b(the|tab|is|still|active|it|please|browser|window)\b', '', raw).strip()
    if not app_name:
        system_controller.control_browser_tabs("close_tab")
        play_sound("cancel")
        speak("Closed active tab, Boss.")
        return

    # Check if closing a known website/tab
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

def handle_route_navigation(cmd):
    """Calculates driving route, distance, ETA, and launches Google Maps navigation in Brave."""
    play_sound("launch")
    clean_cmd = cmd.lower()
    
    # Extract origin and destination from phrasing
    origin = ""
    destination = ""
    
    if " from " in clean_cmd and " to " in clean_cmd:
        parts = clean_cmd.split(" from ", 1)[1].split(" to ", 1)
        origin = parts[0].strip()
        destination = parts[1].strip()
    elif " to " in clean_cmd:
        destination = clean_cmd.split(" to ", 1)[1].strip()
        origin = "Current Location"
    else:
        destination = clean_cmd.replace("directions", "").replace("route", "").replace("navigate", "").strip()
        origin = "Current Location"

    if not destination:
        destination = "Mumbai"

    route_data = maps_engine.calculate_route(origin, destination)
    maps_engine.render_and_launch_route(route_data, speak_fn=speak)

def handle_location(cmd):
    """Searches maps for a place, city, or locates synced contacts."""
    clean_lower = cmd.lower()
    # Guard against queries asking about project storage or code files
    if any(w in clean_lower for w in ["it stored", "project stored", "code stored", "file stored", "saved", "projects folder", "my code", "my project"]):
        play_sound("launch")
        proj_dir = os.path.realpath(os.path.join("D:\\", "FRIDAY_Projects")) if os.path.exists("D:\\") else os.path.join(os.path.expanduser("~"), "FRIDAY_Projects")
        os.makedirs(proj_dir, exist_ok=True)
        try:
            os.startfile(proj_dir)
        except Exception:
            pass
        speak(f"All generated code and full-stack projects are archived in your FRIDAY Projects directory at {proj_dir}, Boss. Opening the folder now.")
        return

    play_sound("launch")
    target = cmd.replace("where is", "").replace("location of", "").replace("show on map", "").replace("open map for", "").replace("find on map", "").replace("maps", "").replace("map", "").strip()
    
    if not target or target.lower() in ["it", "this", "that"]:
        target = "Current Location"

    # Check if contact is in location server first
    info = get_person_location(target)
    if info:
        speak(f"Active telemetry link found for {target}, Boss. Last updated at {info['last_sync']}.")
        maps_url = f"https://www.google.com/maps?q={info['lat']},{info['lon']}"
        open_in_brave(maps_url)
    else:
        place_data = maps_engine.search_location_or_place(target)
        maps_engine.render_and_launch_place(place_data, speak_fn=speak)

def handle_search(cmd):
    query = cmd.replace("search", "").strip()
    speak(f"Opening search stream for {query} in Brave, Boss.")
    open_in_brave(f"https://www.google.com/search?q={query}")
    handleSuggestion(f"Search: {query}")

def handle_autonomous_browse(cmd):
    """Deploys browser-use AI agent to execute web actions autonomously."""
    clean_task = cmd.replace("browse the web and", "").replace("browse the web", "").replace("browse and", "").replace("automate browser", "").replace("browser agent", "").replace("browse", "").strip()
    if not clean_task:
        clean_task = "Search Google and find latest updates"
    play_sound("launch")
    result = browser_agent.execute_task(clean_task, speak_fn=speak)
    if result:
        speak(result)

def handle_github_search(cmd):
    """Searches GitHub for top repositories, star counts, and architectures."""
    clean_query = cmd.replace("search on github for", "").replace("search github for", "").replace("search on github", "").replace("search github", "").replace("find on github", "").replace("github search", "").replace("github", "").strip()
    if not clean_query:
        clean_query = "AI agents"
    speak(f"Searching GitHub index for {clean_query}, Boss.")
    play_sound("launch")
    repos = github_engine.search_repositories(clean_query, max_results=5)
    github_engine.render_and_report(clean_query, repos, speak_fn=speak)

def handle_whatsapp(cmd):
    """Dispatches WhatsApp messaging using natural language parsing."""
    play_sound("launch")
    whatsapp_engine.send_message(cmd, speak_fn=speak)

# --- VISION HANDLERS (SCREEN & WEBCAM EYES) ---
def handle_screen_vision(cmd):
    """Captures the active screen display and speaks real-time visual analysis."""
    speak("Analyzing active display, Boss.")
    play_sound("launch")
    img_b64 = vision_engine.capture_screen()
    if not img_b64:
        speak("I could not capture the active display session, Boss.")
        return

    prompt = cmd if len(cmd.split()) > 3 else "Describe what you see on my screen. Highlight any errors, code, or open applications."
    full_resp = []
    current_sentence = ""
    for token in vision_engine.stream_vision_reasoning(img_b64, prompt):
        print(token, end="", flush=True)
        full_resp.append(token)
        current_sentence += token
        ready_sentences, current_sentence = stream_audio_chunks(current_sentence)
        for s in ready_sentences:
            if s:
                speak(s)

    if current_sentence.strip():
        tail = current_sentence.replace('<DOT>', '.').strip()
        if tail:
            speak(tail)
    print()

def handle_camera_vision(cmd):
    """Captures a webcam frame and performs visual analysis with autonomous product/web intelligence."""
    speak("Accessing optical sensors, Boss.")
    play_sound("launch")
    img_b64 = vision_engine.capture_webcam()
    if not img_b64:
        speak("I was unable to establish an optical link with the camera, Boss.")
        return

    # Check for product research / information lookup intent
    is_product_research = any(w in cmd.lower() for w in [
        "product", "information", "info", "search", "details", "detail", "price", 
        "specs", "specification", "about this", "brand", "model", "find me", 
        "tell me about", "buy", "review", "kya hai", "features"
    ])

    if is_product_research:
        # Multimodal Product Identification & Autonomous Web Search
        prod_data = vision_engine.extract_product_identity(img_b64, cmd)
        prod_name = prod_data.get("product_name", "Product")
        search_q = prod_data.get("search_query", cmd)
        visual_notes = prod_data.get("visual_notes", "")
        has_brand = prod_data.get("has_brand", False)

        search_context = ""
        if search_q:
            search_context = web_search_intelligence(search_q)

        try:
            from core.background_coprocessor import coprocessor
            distilled_analysis = coprocessor.distill_product_intelligence(
                user_query=cmd,
                product_name=prod_name,
                visual_notes=visual_notes,
                has_brand=has_brand,
                search_context=search_context
            )
            speak(distilled_analysis)
        except Exception:
            prompt = (
                f"You are F.R.I.D.A.Y., Boss's tactical AI companion. The Boss asked: '{cmd}'.\n"
                f"Optical Sensor Scan: {visual_notes}.\n"
                f"Identified / Predicted Item: {prod_name} (Brand Verified: {has_brand}).\n"
                f"Live Web Data:\n{search_context}\n\n"
                f"Provide a crisp, highly knowledgeable response in 2 spoken sentences. "
                f"If branding/model is identified, state it with its key features or pricing. "
                f"In Hindi/Hinglish, always use female grammatical agreements (e.g. 'dekh rahi hoon'). Address the user as 'Boss'."
            )
            get_ai_response(prompt, speak_stream=True)
        return

    prompt = cmd if len(cmd.split()) > 3 else "Describe what you see through the camera in front of you. Identify any people or objects."
    full_resp = []
    current_sentence = ""
    for token in vision_engine.stream_vision_reasoning(img_b64, prompt):
        print(token, end="", flush=True)
        full_resp.append(token)
        current_sentence += token
        ready_sentences, current_sentence = stream_audio_chunks(current_sentence)
        for s in ready_sentences:
            if s:
                speak(s)

    if current_sentence.strip():
        tail = current_sentence.replace('<DOT>', '.').strip()
        if tail:
            speak(tail)
    print()

# --- OMNI-SYSTEM CONTROLLER HANDLERS (DESKTOP & TAB & EDIT ACCESS) ---
def handle_take_screenshot(cmd):
    """Captures and archives full screen to Desktop/Screenshots/."""
    speak("Capturing screen, Boss.")
    play_sound("launch")
    path = system_controller.take_and_save_screenshot(open_after=True)
    if path:
        speak(f"Screenshot archived to your Desktop, Boss.")
    else:
        speak("I encountered an issue capturing the screen archive, Boss.")

def handle_health_check(cmd):
    """Executes a deep line-by-line codebase health and vulnerability audit."""
    speak("Initiating deep codebase and vulnerability audit, Boss. Stand by...")
    play_sound("launch")
    results = codebase_auditor.perform_deep_audit()
    codebase_auditor.render_audit_report(results, speak_fn=speak)

def handle_self_heal(cmd):
    """Triggers F.R.I.D.A.Y.'s autonomous self-healing and subsystem restoration protocol."""
    play_sound("launch")
    codebase_auditor.perform_self_healing(speak_fn=speak)

def handle_format_memory(cmd):
    """Purges and resets all long-term memory, project history, and session profiles."""
    play_sound("launch")
    speak("Formatting complete long-term memory and project history, Boss. Resetting to factory state.")
    memory_engine.format_all_memory()
    speak("All memory files, project records, and session vaults have been wiped clean. We are starting completely fresh, Boss.")

def handle_copy_to_notepad(cmd):
    """Copies active selected text from screen and writes to Desktop/JARVIS_Notes.txt."""
    speak("Copying selection to Notepad, Boss.")
    play_sound("launch")
    text = system_controller.copy_selection_to_notepad(open_notepad=True)
    if text:
        preview = text[:50] + ("..." if len(text) > 50 else "")
        speak(f"Appended note: '{preview}'. Notepad is open on your screen, Boss.")
    else:
        speak("I couldn't detect any highlighted text to copy, Boss. Make sure text is selected.")

def handle_tab_new(cmd):
    system_controller.control_browser_tabs("new_tab")
    speak("New tab opened, Boss.")

def handle_tab_close(cmd):
    system_controller.control_browser_tabs("close_tab")
    speak("Tab closed, Sir.")

def handle_tab_next(cmd):
    system_controller.control_browser_tabs("next_tab")

def handle_tab_prev(cmd):
    system_controller.control_browser_tabs("prev_tab")

def handle_tab_reopen(cmd):
    system_controller.control_browser_tabs("reopen_tab")
    speak("Reopening previous tab, Boss.")

def handle_minimize_all(cmd):
    system_controller.minimize_all_windows()
    speak("Minimizing all windows to desktop, Boss.")

def handle_scroll_down(cmd):
    system_controller.scroll_screen("down", amount=500)

def handle_scroll_up(cmd):
    system_controller.scroll_screen("up", amount=500)

def handle_guarded_edit(cmd):
    """Guarded file edit - always requires explicit confirmation before altering disk files."""
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

    # Permission Gatekeeper ensures user confirms before saving
    system_controller.edit_file_guarded(full_path, old_text, new_text, speak_fn=speak)

# --- COMM-LINK CYBERNETIC EARBUD HANDLERS ---
def handle_broadcast_mode(cmd):
    """Switches Comm-Link to Broadcast Mode (Earbud Mic -> PC Room Speakers)."""
    success, msg = comm_link.set_mode("broadcast")
    play_sound("launch")
    speak(msg)

def handle_whisper_mode(cmd):
    """Switches Comm-Link to Whisper / Stealth Mode (Earbud Mic -> In-Ear Output)."""
    success, msg = comm_link.set_mode("whisper")
    play_sound("launch")
    speak(msg)

def handle_dual_audio_mode(cmd):
    """Switches Comm-Link to Dual Audio Mode (Synchronized Earbud + PC Speakers)."""
    success, msg = comm_link.set_mode("dual")
    play_sound("launch")
    speak(msg)

def handle_audio_health(cmd):
    """Speaks comprehensive audio telemetry and Comm-Link connection health."""
    play_sound("launch")
    speech = comm_link.get_health_speech()
    speak(speech)

# --- AUTONOMOUS CODING & CLAUDE CODE HANDLER ---
def handle_coding_command(cmd):
    """Processes natural language coding instructions via Prompt Synthesizer & Level 2 Claude Code CTO."""
    play_sound("launch")
    coding_engine.dispatch_coding_task_async(cmd, speak_fn=speak)

# COMMAND DICTIONARY (Ordered by priority)
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
    "about the project": handle_project_status,
    "about project": handle_project_status,
    "tell me about the project": handle_project_status,
    "project ke baare mein": handle_project_status,
    "project ka kya hua": handle_project_status,
    "project status": handle_project_status,
    "project update": handle_project_status,
    "coding status": handle_project_status,
    "app status": handle_project_status,
    "kya chal raha hai": handle_project_status,
    "kahan tak pahuncha": handle_project_status,
    "kaam kahan tak pahuncha": handle_project_status,
    "progress update": handle_project_status,
    "how is the project": handle_project_status,
    "how is the app": handle_project_status,
    "is the project ready": handle_project_status,
    "is the app ready": handle_project_status,
    "opencode se code banao": handle_coding_command,
    "opencode se app banao": handle_coding_command,
    "opencode se website banao": handle_coding_command,
    "opencode ko bolo": handle_coding_command,
    "opencode se banao": handle_coding_command,
    "claude ko bolo": handle_coding_command,
    "claude se app banao": handle_coding_command,
    "claude se code karwao": handle_coding_command,
    "ek app bana do": handle_coding_command,
    "ek app banao": handle_coding_command,
    "ek website bana do": handle_coding_command,
    "ek website banao": handle_coding_command,
    "code likh do": handle_coding_command,
    "code likho": handle_coding_command,
    "write a python script": handle_coding_command,
    "write python script": handle_coding_command,
    "write python code": handle_coding_command,
    "write a script": handle_coding_command,
    "write script": handle_coding_command,
    "create a script": handle_coding_command,
    "write code for": handle_coding_command,
    "write code to": handle_coding_command,
    "write code": handle_coding_command,
    "write a program": handle_coding_command,
    "create a program": handle_coding_command,
    "build a script": handle_coding_command,
    "build an app": handle_coding_command,
    "build a website": handle_coding_command,
    "create an app": handle_coding_command,
    "create a website": handle_coding_command,
    "code this": handle_coding_command,
    "code a": handle_coding_command,
    "code for me": handle_coding_command,
    "program a": handle_coding_command,
    "program an": handle_coding_command,
    "write a function": handle_coding_command,
    "write html": handle_coding_command,
    "write javascript": handle_coding_command,
    "write typescript": handle_coding_command,
    "write c++": handle_coding_command,
    "write cpp": handle_coding_command,
    "write java": handle_coding_command,
    "write rust": handle_coding_command,
    "write c#": handle_coding_command,
    "write golang": handle_coding_command,
    "debug this code": handle_coding_command,
    "fix this bug": handle_coding_command,
    "friday health check": handle_health_check,
    "codebase health check": handle_health_check,
    "system health check": handle_health_check,
    "codebase health": handle_health_check,
    "health check": handle_health_check,
    "audit codebase": handle_health_check,
    "scan codebase": handle_health_check,
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
    "fix the errors": handle_self_heal,
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
    "browse the web and": handle_autonomous_browse,
    "browse the web": handle_autonomous_browse,
    "browse and": handle_autonomous_browse,
    "automate browser": handle_autonomous_browse,
    "browser agent": handle_autonomous_browse,
    "autonomous browser": handle_autonomous_browse,
    "search on github for": handle_github_search,
    "search on github": handle_github_search,
    "search github for": handle_github_search,
    "message on whatsapp": handle_whatsapp,
    "send message on whatsapp": handle_whatsapp,
    "send whatsapp to": handle_whatsapp,
    "send whatsapp message to": handle_whatsapp,
    "send whatsapp": handle_whatsapp,
    "whatsapp message to": handle_whatsapp,
    "whatsapp message": handle_whatsapp,
    "message to": handle_whatsapp,
    "whatsapp to": handle_whatsapp,
    "whatsapp": handle_whatsapp,
    "search github": handle_github_search,
    "find on github": handle_github_search,
    "github search": handle_github_search,
    "capture my screen": handle_take_screenshot,
    "capture the screen": handle_take_screenshot,
    "capture screen": handle_take_screenshot,
    "take screenshot": handle_take_screenshot,
    "take a screenshot": handle_take_screenshot,
    "capture screenshot": handle_take_screenshot,
    "screenshot": handle_take_screenshot,
    "copy this": handle_copy_to_notepad,
    "copy to notepad": handle_copy_to_notepad,
    "paste this in notepad": handle_copy_to_notepad,
    "save to notepad": handle_copy_to_notepad,
    "open new tab": handle_tab_new,
    "new tab": handle_tab_new,
    "close this tab": handle_tab_close,
    "close tab": handle_tab_close,
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
    "analyse my whole screen and tell me what do you see": handle_screen_vision,
    "analyse my whole screen": handle_screen_vision,
    "analyse my screen": handle_screen_vision,
    "analyse the screen": handle_screen_vision,
    "analyse screen": handle_screen_vision,
    "analyze my whole screen and tell me what do you see": handle_screen_vision,
    "analyze my whole screen": handle_screen_vision,
    "analyze my screen": handle_screen_vision,
    "analyze the screen": handle_screen_vision,
    "analyze screen": handle_screen_vision,
    "what do you see on my screen": handle_screen_vision,
    "what do you see on the screen": handle_screen_vision,
    "describe my screen": handle_screen_vision,
    "describe what you see on my screen": handle_screen_vision,
    "look at my screen": handle_screen_vision,
    "look at the screen": handle_screen_vision,
    "look at screen": handle_screen_vision,
    "what is on my screen": handle_screen_vision,
    "what's on my screen": handle_screen_vision,
    "read my screen": handle_screen_vision,
    "check my screen": handle_screen_vision,
    "see my screen": handle_screen_vision,
    "explain this error": handle_screen_vision,
    "how many fingers am i holding": handle_camera_vision,
    "how many fingers": handle_camera_vision,
    "how many finger am i holding": handle_camera_vision,
    "how many finger": handle_camera_vision,
    "fingers am i holding": handle_camera_vision,
    "what am i holding": handle_camera_vision,
    "am i holding": handle_camera_vision,
    "what is in my hand": handle_camera_vision,
    "what's in my hand": handle_camera_vision,
    "look at me": handle_camera_vision,
    "can you see me": handle_camera_vision,
    "see me": handle_camera_vision,
    "what do you see in the camera": handle_camera_vision,
    "what do you see through the camera": handle_camera_vision,
    "what do you see in front of you": handle_camera_vision,
    "what do you see": handle_camera_vision,
    "what can you see": handle_camera_vision,
    "access camera": handle_camera_vision,
    "open camera": handle_camera_vision,
    "start camera": handle_camera_vision,
    "camera on": handle_camera_vision,
    "check camera": handle_camera_vision,
    "look through camera": handle_camera_vision,
    "describe what you see": handle_camera_vision,
    "describe what you are seeing": handle_camera_vision,
    "describe what to see": handle_camera_vision,
    "look at this": handle_camera_vision,
    "camera vision": handle_camera_vision,
    "health": handle_health_check,
    "news": handle_news,
    "search and tell me": handle_internet_query,
    "what is": handle_internet_query,
    "status": handle_status,
    "system": handle_status,
    "volume up": handle_media,
    "volume down": handle_media,
    "mute": handle_media,
    "pause": handle_media,
    "next": handle_media,
    "previous": handle_media,
    "on spotify": handle_spotify,
    "playlist": handle_spotify,
    "music": handle_spotify,
    "gaana bajao": handle_spotify,
    "gaana chalao": handle_spotify,
    "gaane sunao": handle_spotify,
    "gana bajao": handle_spotify,
    "gana chalao": handle_spotify,
    "bajao": handle_spotify,
    "chalao": handle_spotify,
    "sleep": handle_sleep,
    "shutdown": handle_shutdown,
    "close this tab": handle_tab_close,
    "close the tab": handle_tab_close,
    "close tab": handle_tab_close,
    "close youtube tab": handle_close,
    "close the youtube": handle_close,
    "close youtube": handle_close,
    "close google": handle_close,
    "close github": handle_close,
    "close chatgpt": handle_close,
    "close whatsapp": handle_close,
    "close instagram": handle_close,
    "tab band karo": handle_tab_close,
    "band karo": handle_close,
    "note": handle_note,
    "open": handle_open,
    "close": handle_close,
    "directions from": handle_route_navigation,
    "directions to": handle_route_navigation,
    "directions": handle_route_navigation,
    "route from": handle_route_navigation,
    "route to": handle_route_navigation,
    "how far is": handle_route_navigation,
    "distance from": handle_route_navigation,
    "distance to": handle_route_navigation,
    "show on map": handle_location,
    "open map for": handle_location,
    "find on map": handle_location,
    "maps": handle_location,
    "where is": handle_location,
    "location of": handle_location,
    "search": handle_search,
    "play": handle_spotify # Fallback play handles both
}

# Pre-compile command dispatch regexes once at startup for instant O(1) matching
COMPILED_COMMANDS = [
    (re.compile(rf"\b{re.escape(k)}\b"), k)
    for k in sorted(COMMANDS.keys(), key=len, reverse=True)
]

def processCommand(c):
    try:
        cmd = c.lower().strip()
        
        # 0. Phonetic alias normalization for Antigravity commands
        if re.search(r'\b(integrity\s+ide|anti\s+gravity\s+ide|anti-gravity\s+ide|integirty\s+ide|antigravity\s+ide)\b', cmd):
            cmd = re.sub(r'\b(integrity|anti\s+gravity|anti-gravity|integirty)\s+ide\b', 'antigravity ide', cmd)
        elif re.search(r'\b(integrity|anti\s+gravity|anti-gravity|integirty)\b', cmd) and any(w in cmd for w in ["open", "launch", "start", "ide"]):
            cmd = re.sub(r'\b(integrity|anti\s+gravity|anti-gravity|integirty)\b', 'antigravity ide', cmd)

        # 1. Smart Vision & Camera Optical Intent Detection
        vision_camera_triggers = [
            r'\bhold\b', r'\bholding\b', r'\bheld\b', r'\bin\s+my\s+hand\b', r'\bin\s+hand\b',
            r'\bbefore\s+camera\b', r'\bin\s+front\s+of\s+camera\b', r'\bin\s+front\s+of\s+you\b',
            r'\blook\s+at\s+this\b', r'\blook\s+at\s+me\b', r'\bsee\s+me\b', r'\bthrough\s+the\s+camera\b',
            r'\boptical\s+sensor\b', r'\bwhat\s+is\s+this\b', r'\bwhat\'s\s+this\b', r'\bidentify\s+this\b',
            r'\bidentify\s+what\b', r'\banalyze\s+what\b', r'\banalyse\s+what\b', r'\banalyze\s+this\b',
            r'\banalyse\s+this\b', r'\banalyze\s+the\b', r'\banalyse\s+the\b', r'\bdescribe\s+what\s+you\s+see\b',
            r'\bwhat\s+can\s+you\s+see\b', r'\bwhat\s+do\s+you\s+see\b', r'\bcamera\s+vision\b',
            r'\bscan\s+this\b', r'\bdescribe\s+this\b', r'\binformation\s+(?:of|for|about)\s+this\b',
            r'\binfo\s+(?:of|for|about)\s+this\b', r'\bdetails\s+(?:of|for|about)\s+this\b',
            r'\b(?:search|find)\s+(?:me\s+)?information\b', r'\b(?:search|find)\s+(?:me\s+)?info\b',
            r'\bthis\s+product\b', r'\bthe\s+product\b', r'\bscan\s+product\b', r'\bidentify\s+product\b',
            r'\btell\s+me\s+about\s+this\b', r'\bcheck\s+what\b', r'\bwhat\s+am\s+i\b',
            r'\byeh\s+kya\s+hai\b', r'\bye\s+kya\s+hai\b', r'\bisko\s+dekho\b',
            r'\bcamera\s+se\s+dekho\b', r'\bphoto\s+dekho\b'
        ]
        if any(re.search(trig, cmd) for trig in vision_camera_triggers):
            handle_camera_vision(cmd)
            return

        vision_screen_triggers = [
            "on my screen", "on screen", "on the screen", "read screen", "look at screen",
            "check screen", "my display", "active display", "explain this error"
        ]
        if any(trig in cmd for trig in vision_screen_triggers):
            handle_screen_vision(cmd)
            return

        # 2. Smart Autonomous Project & Coding Status Query Detection
        project_status_triggers = [
            r'\bproject\s+status\b', r'\bapp\s+status\b', r'\bcode\s+status\b',
            r'\bkya\s+chal\s+raha\s+hai\b', r'\bkahan\s+tak\s+pahuncha\b',
            r'\bkaam\s+kahan\s+tak\b', r'\bproject\s+bana\b', r'\bprogress\s+update\b',
            r'\bhow\s+is\s+(?:the\s+)?project(?:\s+going)?\b', r'\bhow\s+is\s+(?:the\s+)?app(?:\s+going)?\b',
            r'\bis\s+(?:the\s+)?project\s+ready\b', r'\bis\s+(?:the\s+)?app\s+ready\b',
            r'\bwhere\s+is\s+(?:it|the\s+project|the\s+code|the\s+app)\s+(?:stored|saved|located)\b',
            r'\bopen\s+(?:the\s+)?(?:project|projects|code|app)\s+folder\b',
            r'\bwhat\s+stage\b', r'\bwhich\s+stage\b', r'\bwhat\s+are\s+you\s+working\s+on\b'
        ]
        if any(re.search(trig, cmd) for trig in project_status_triggers):
            if any(w in cmd for w in ["where is", "open project folder", "open projects folder", "folder", "stored", "saved"]):
                proj_dir = os.path.realpath(os.path.join("D:\\", "FRIDAY_Projects")) if os.path.exists("D:\\") else os.path.join(os.path.expanduser("~"), "FRIDAY_Projects")
                os.makedirs(proj_dir, exist_ok=True)
                try:
                    os.startfile(proj_dir)
                except Exception:
                    pass
                play_sound("launch")
                speak(f"Your project archives are stored in {proj_dir}, Boss. Opening the folder now.")
                return
            handle_project_status(cmd)
            return

        # 3. Smart Autonomous Coding Intent Detection
        coding_verbs = ["write", "create", "build", "make", "generate", "code", "program", "develop", "design", "craft", "banao", "bana do", "likho", "likh do"]
        coding_targets = [
            "html", "css", "website", "web page", "link page", "landing page", "front end", "frontend", "front-end",
            "web app", "webapp", "page", "site", "script", "program", "app", "application", "python", "javascript",
            "typescript", "rust", "cpp", "c++", "java", "code", "fastapi", "flask", "react", "dashboard", "ui", "interface",
            "menu", "portfolio", "calculator", "game"
        ]
        if any(v in cmd for v in coding_verbs) and any(t in cmd for t in coding_targets):
            handle_coding_command(cmd)
            return

        # 4. Smart WhatsApp Messaging Intent Detection
        if "whatsapp" in cmd or ("message" in cmd and any(p in cmd for p in ["to", "send"])):
            handle_whatsapp(cmd)
            return

        # 5. Precision Pre-compiled Dictionary Routing
        matched_key = None
        for pattern, k in COMPILED_COMMANDS:
            if pattern.search(cmd):
                matched_key = k
                break
        
        if matched_key:
            COMMANDS[matched_key](cmd)
        else:
            # Fallback to AI Brain
            play_sound("launch")
            get_ai_response(c, speak_stream=True)
            if len(c.split()) > 3: 
                handleSuggestion(c)
    except Exception as err:
        print(f"\n[Command Dispatch Error]: {err}")
        play_sound("error")
        speak("I encountered an issue processing that instruction, Boss. All operating systems remain secure.")

def warmup_model():
    """Background task to pre-warm memory, neural embeddings, and AI pipelines without competing for initial startup CPU."""
    time.sleep(2.0)
    # Ensure Gemini-Web2API daemon is hot
    try:
        ensure_gemini_web2api_running()
    except Exception:
        pass



# --- SYSTEM INITIALIZATION ---
def web_command_dispatcher(cmd):
    global WEB_REQUEST_ACTIVE
    WEB_REQUEST_ACTIVE = True
    try:
        processCommand(cmd)
        return latest_web_response or "Command executed successfully, Boss."
    finally:
        WEB_REQUEST_ACTIVE = False

register_command_handler(web_command_dispatcher)

if __name__ == "__main__":
    # Boot sound
    play_sound("startup")
    
    # Trigger model warm-up in the background after initial speech
    threading.Thread(target=warmup_model, daemon=True).start()
    
    # Start Web HUD Server on port 5000
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Run Battery monitor as a lightweight background daemon thread
    sentinel_thread = threading.Thread(target=battery_monitor_sentinel, daemon=True)
    sentinel_thread.start()
    
    # Calculate initial stats for Startup Briefing
    now_time = datetime.now().strftime("%I:%M %p")
    
    # Render Cybernetic Stark Terminal HUD
    render_startup_banner()
    
    # Snappy, Crisp Personalized Greeting
    startup_briefing = f"Systems are fully online and calibrated, Boss. Audio receptors active."
    
    # Decoupled Non-blocking Audio Architecture
    raw_audio_queue = queue.Queue(maxsize=20)
    
    def drain_audio_queues():
        """Flushes stale audio frames and acoustic echo from input queues."""
        while not audio_queue.empty():
            try:
                audio_queue.get_nowait()
            except queue.Empty:
                break
        while not raw_audio_queue.empty():
            try:
                raw_audio_queue.get_nowait()
            except queue.Empty:
                break

    def mic_capture_worker():
        """Dedicated continuous microphone ingest thread with automatic Bluetooth earbud hot-swapping and acoustic calibration."""
        recognizer = sr.Recognizer()
        current_mic_idx = None
        current_is_earbud = None
        mic_w = None

        def init_or_switch_mic():
            nonlocal mic_w, current_mic_idx, current_is_earbud
            best_idx, best_name, is_earbud = comm_link.get_best_microphone_index()
            if mic_w is not None and best_idx == current_mic_idx and is_earbud == current_is_earbud:
                return mic_w
            
            profile = comm_link.get_acoustic_profile(is_earbud)
            recognizer.pause_threshold = profile["pause_threshold"]
            recognizer.phrase_threshold = profile["phrase_threshold"]
            recognizer.non_speaking_duration = profile["non_speaking_duration"]
            recognizer.dynamic_energy_ratio = profile["dynamic_energy_ratio"]
            recognizer.dynamic_energy_adjustment_damping = profile["damping"]
            recognizer.dynamic_energy_threshold = True

            try:
                if best_idx is not None:
                    mic_w = sr.Microphone(device_index=best_idx, sample_rate=profile["sample_rate"])
                else:
                    mic_w = sr.Microphone(sample_rate=profile["sample_rate"])
                
                with mic_w as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.15)
                    recognizer.energy_threshold = max(profile["energy_threshold"], min(recognizer.energy_threshold, profile["energy_threshold"] * 3))
                
                current_mic_idx = best_idx
                current_is_earbud = is_earbud
                mode_str = "🎙️ Earbud In-Ear Mode (Enhanced Sensitivity)" if is_earbud else "💻 PC Room Mic Mode"
                print(f"[Ear Sensors Active]: {mode_str} -> {best_name} (Energy: {recognizer.energy_threshold:.0f})")
            except Exception as e:
                try:
                    mic_w = sr.Microphone()
                    with mic_w as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.15)
                except Exception:
                    mic_w = None
            return mic_w

        mic_w = init_or_switch_mic()
        last_check_time = time.time()

        # Maintain single open audio stream context for continuous zero-loss capture
        while True:
            try:
                if not mic_w:
                    mic_w = init_or_switch_mic()
                    if not mic_w:
                        time.sleep(0.5)
                        continue

                with mic_w as source:
                    while True:
                        try:
                            # Periodic check for Bluetooth earbud connect/disconnect hot-swap (every 10s)
                            if time.time() - last_check_time > 10.0:
                                last_check_time = time.time()
                                check_idx, _, check_earbud = comm_link.get_best_microphone_index()
                                if check_idx != current_mic_idx or check_earbud != current_is_earbud:
                                    init_or_switch_mic()
                                    break

                            # Long-form natural speech: allows up to 60s continuous detailed prompts
                            audio = recognizer.listen(source, timeout=None, phrase_time_limit=60.0)
                            
                            # Drop backlog if queue is getting stale
                            while raw_audio_queue.qsize() > 3:
                                try:
                                    raw_audio_queue.get_nowait()
                                except queue.Empty:
                                    break
                            try:
                                raw_audio_queue.put_nowait((recognizer, audio))
                            except queue.Full:
                                pass
                        except (sr.WaitTimeoutError, sr.UnknownValueError):
                            continue
                        except Exception:
                            time.sleep(0.05)
                            break
            except Exception:
                time.sleep(0.4)
                mic_w = None

    def transcription_worker():
        """Dedicated high-speed transcription worker with sub-30ms Full-Duplex Barge-In interruption support."""
        while True:
            try:
                rec, audio_chunk = raw_audio_queue.get()
                text = hearing_engine.transcribe_audio_frame(rec, audio_chunk)
                if not text or len(text.strip()) <= 1:
                    continue

                # Full-Duplex Barge-In Protocol: interrupt assistant mid-speech if user commands
                if neural_voice_engine.is_speaking() or IS_SPEAKING:
                    t_lower = text.lower().strip()
                    interrupt_words = ["stop", "ruko", "chup", "quiet", "wait", "shutup", "pause", "friday", "hold on", "cancel"]
                    if any(w in t_lower for w in interrupt_words):
                        print(f"\n[Barge-In]: Active speech interrupted by Boss ('{text}').")
                        play_sound("cancel")
                        neural_voice_engine.stop_immediate()
                        drain_audio_queues()
                    continue

                audio_queue.put(text)
            except Exception:
                time.sleep(0.02)

    # Launch dedicated capture engine and 3 parallel fast transcription workers
    threading.Thread(target=mic_capture_worker, daemon=True).start()
    for _ in range(3):
        threading.Thread(target=transcription_worker, daemon=True).start()
    
    # Speak startup briefing in background voice queue
    speak(startup_briefing)
    
    def is_trailing_incomplete(text: str) -> bool:
        """Detects if speech ended mid-thought on a connector, preposition, or action verb."""
        t = text.strip().lower()
        trailing_patterns = [
            r'\b(and|aur|ki|to|with|for|which|that|also|like|but|lekin|then|because|kyunki|or|ya|so|such as)$',
            r'\b(create\s+a|build\s+a|make\s+a|write\s+a|open\s+the|search\s+for|show\s+me|tell\s+me|can\s+you)$',
            r'\b(in|on|at|of|from|into|about|by|as|the|a|an)$'
        ]
        return any(re.search(p, t) for p in trailing_patterns)

    WAKE_WORDS = [
        "friday", "fryday", "fraiday", "fry day", "frida", "frieda", "phriday", "f.r.i.d.a.y",
        "wake up", "sun friday", "friday sun", "suno friday", "sun na friday",
        "are friday", "arre friday", "oye friday", "hey friday", "hi friday",
        "hello friday", "bhai friday", "jarvis", "hey jarvis", "hi jarvis"
    ]

    is_awaiting_printed = False

    while True:
        try:
            if not is_awaiting_printed:
                print_listening_state()
                is_awaiting_printed = True
            
            raw_input = audio_queue.get()
            command_lower = raw_input.lower().strip()
            
            # Check for wake words
            wake_word_found = False
            parsed_command = ""
            
            for wake in WAKE_WORDS:
                if wake in command_lower:
                    wake_word_found = True
                    idx = command_lower.find(wake)
                    cmd_idx = idx + len(wake)
                    parsed_command = raw_input[cmd_idx:].strip()
                    if parsed_command.startswith(",") or parsed_command.startswith(":"):
                        parsed_command = parsed_command[1:].strip()
                    # Handle wake word at the end (e.g. "how many fingers am I holding Friday")
                    if not parsed_command:
                        prefix_cmd = raw_input[:idx].strip().rstrip(",:")
                        if prefix_cmd:
                            parsed_command = prefix_cmd
                    break
            
            # Discard background noise / utterances without wake word
            if not wake_word_found:
                continue
                
            is_awaiting_printed = False
            print_heard(raw_input)
            
            if command_lower in ["exit", "quit", "go to sleep", "standby"] or parsed_command.lower() in ["exit", "quit", "go to sleep", "standby"]:
                play_sound("cancel")
                speak("Understood, Boss. Entering standby.")
                break
            
            if not parsed_command:
                play_sound("launch")
                speak("Yes, Boss?")
                # Wait for assistant to finish speaking before listening for the command
                neural_voice_engine.wait_until_done()
                time.sleep(0.05)

                print("--- Listening for command ---")
                try:
                    command = audio_queue.get(timeout=8.0)
                except queue.Empty:
                    continue
                
                # Allow smooth continuation for natural multi-word commands (0.65s buffer)
                while is_trailing_incomplete(command) or (len(command.split()) < 4 and not audio_queue.empty()):
                    try:
                        next_chunk = audio_queue.get(timeout=0.65)
                        if next_chunk:
                            command = f"{command} {next_chunk}".strip()
                    except Exception:
                        break

                print_heard(command)
                processCommand(command)
                neural_voice_engine.wait_until_done()
                drain_audio_queues()
            else:
                # Allow smooth continuation on direct wake+command (0.65s buffer)
                while is_trailing_incomplete(parsed_command) or (len(parsed_command.split()) < 4 and not audio_queue.empty()):
                    try:
                        next_chunk = audio_queue.get(timeout=0.65)
                        if next_chunk:
                            parsed_command = f"{parsed_command} {next_chunk}".strip()
                    except Exception:
                        break

                play_sound("launch")
                print_heard(parsed_command)
                processCommand(parsed_command)
                neural_voice_engine.wait_until_done()
                drain_audio_queues()
                    
        except KeyboardInterrupt:
            play_sound("cancel")
            speak("Goodbye, Boss. Terminating neural feeds.")
            break
        except Exception as e:
            print(f"\nSystem Loop Error: {e}")

    try:
        memory_engine.consolidate_session_memory()
    except Exception:
        pass
