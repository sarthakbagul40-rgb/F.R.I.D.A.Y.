"""
F.R.I.D.A.Y. Honeycomb Base Infrastructure
Shared acoustic soundboard, neural voice output, and audio queues.
"""

import queue
import threading
import winsound

try:
    import pythoncom
    import win32com.client as wincl
except ImportError:
    pythoncom = None
    wincl = None

from core.omnivoice_service import neural_voice_engine
from core.media_engine import media_engine
from core.terminal_hud import print_speaking

# Shared audio queues
audio_queue = queue.Queue()
raw_audio_queue = queue.Queue(maxsize=20)

# Global audio state flags
IS_SPEAKING = False
WEB_REQUEST_ACTIVE = False
latest_web_response = ""

thread_local = threading.local()

def play_sound(action_type: str):
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

def get_speaker():
    """Returns a thread-local instance of SAPI with female voice (Zira/FRIDAY)."""
    if not hasattr(thread_local, "speaker"):
        if pythoncom and wincl:
            try:
                pythoncom.CoInitialize()
                sp = wincl.Dispatch("SAPI.SpVoice")
                voices = sp.GetVoices()
                for v in voices:
                    desc = v.GetDescription().lower()
                    if "zira" in desc or "female" in desc or "eva" in desc or "hazel" in desc:
                        sp.Voice = v
                        break
                thread_local.speaker = sp
            except Exception:
                thread_local.speaker = None
        else:
            thread_local.speaker = None
    return thread_local.speaker

def speak(text: str):
    """Speaks out loud using Movie-Grade Multilingual Neural Voice with SAPI fallback."""
    global IS_SPEAKING, latest_web_response, WEB_REQUEST_ACTIVE
    latest_web_response = text
    if WEB_REQUEST_ACTIVE:
        return

    # Acoustic Auto-Ducking: smoothly dip media volume while speaking
    try:
        media_engine.duck_volume(15)
    except Exception:
        pass

    print_speaking(text)
    try:
        IS_SPEAKING = True
        neural_voice_engine.speak(text)
    except Exception as e:
        print(f"Voice Error: {e}")
        try:
            speak_engine = get_speaker()
            if speak_engine:
                speak_engine.Speak(text)
        except Exception:
            pass
    finally:
        if not neural_voice_engine.is_speaking():
            IS_SPEAKING = False
            try:
                media_engine.restore_volume()
            except Exception:
                pass

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

def collect_continuous_speech(initial_phrase: str = "", silence_timeout: float = 0.9) -> str:
    """
    Continuous Speech Stream Accumulator:
    Allows Boss to speak naturally at their own pace without arbitrary time limits.
    Accumulates speech fragments until silence (calibrated 0.9s timeout) is observed.
    """
    parts = []
    if initial_phrase and initial_phrase.strip():
        parts.append(initial_phrase.strip())
    
    while True:
        try:
            next_chunk = audio_queue.get(timeout=silence_timeout)
            if next_chunk and next_chunk.strip():
                clean_chunk = next_chunk.strip()
                if clean_chunk.lower() in ["cancel", "stop", "never mind", "nevermind", "chup", "ruko"]:
                    play_sound("cancel")
                    return ""
                parts.append(clean_chunk)
                print(f"   [Continued Speaking]: {clean_chunk}")
        except queue.Empty:
            break
    return " ".join(parts).strip()
