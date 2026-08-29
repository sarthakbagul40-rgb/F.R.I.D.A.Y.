"""
Movie-Grade Neural Voice & OmniVoice Multilingual TTS Subsystem for F.R.I.D.A.Y.
Features:
1. Cinematic Irish Female Voice (Kerry Condon / Marvel FRIDAY tone: en-IE-EmilyNeural).
2. Universal Multilingual Neural Voices (Hindi, Hinglish, Marathi, Global languages).
3. Native Windows MCI / Pygame low-latency streaming playback.
4. Instant local SAPI (Microsoft Zira) fallback.
"""

import os
import re
import sys
import time
import uuid
import asyncio
import tempfile
import threading
import ctypes
from typing import Optional, Dict

# Windows SAPI COM fallback
import win32com.client as wincl
import pythoncom

try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    from kokoro_onnx import Kokoro
except ImportError:
    Kokoro = None

_PYGAME_AVAILABLE = None

def _get_pygame():
    global _PYGAME_AVAILABLE
    if _PYGAME_AVAILABLE is None:
        try:
            os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
            import pygame
            pygame.mixer.init()
            _PYGAME_AVAILABLE = pygame
        except Exception:
            _PYGAME_AVAILABLE = False
    return _PYGAME_AVAILABLE if _PYGAME_AVAILABLE else None


# Catalog of Movie-Grade Multilingual Neural Voices
VOICE_PROFILES: Dict[str, Dict[str, str]] = {
    "english_irish": {
        "voice": "en-GB-SoniaNeural",  # High-projection, loud, sophisticated British/Irish FRIDAY
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "British/Irish High-Clarity FRIDAY (Sonia)"
    },
    "english_british": {
        "voice": "en-GB-SoniaNeural",  # Sophisticated British tone
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "British Neural FRIDAY (Sonia)"
    },
    "english_libby": {
        "voice": "en-GB-LibbyNeural",  # Punchy, loud British tone
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "British Loud & Punchy (Libby)"
    },
    "multilingual_ava": {
        "voice": "en-US-AvaMultilingualNeural",  # Conversational multilingual voice
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "Multilingual FRIDAY (Ava)"
    },
    "multilingual_emma": {
        "voice": "en-US-EmmaMultilingualNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "Conversational Multilingual (Emma)"
    },
    "english_movie": {
        "voice": "en-GB-SoniaNeural",  # British / Irish FRIDAY
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "Cinematic British FRIDAY"
    },
    "hindi": {
        "voice": "en-IN-NeerjaNeural",  # Natural, effortless conversational Hinglish & Indian English
        "rate": "+3%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "Natural Conversational Hinglish (Neerja)"
    },
    "marathi": {
        "voice": "mr-IN-AarohiNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "Native Marathi"
    },
    "hindi_native": {
        "voice": "en-IN-NeerjaNeural",  # Dedicated smooth Indian Hinglish voice
        "rate": "+3%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "Indian Hinglish (Neerja Standard)"
    },
    "hindi_devanagari": {
        "voice": "hi-IN-SwaraNeural",  # Pure Devanagari Hindi voice
        "rate": "+2%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "Devanagari Hindi (Swara)"
    },
    "marathi_native": {
        "voice": "mr-IN-AarohiNeural",  # Dedicated Indian Marathi female voice
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "Indian Marathi"
    },
    "japanese": {
        "voice": "ja-JP-NanamiNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "Japanese Neural"
    },
    "spanish": {
        "voice": "es-ES-ElviraNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "Spanish Neural"
    },
    "french": {
        "voice": "fr-FR-VivienneMultilingualNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+800%",
        "desc": "French Multilingual Neural"
    }
}


class LanguageProfileDetector:
    """Analyzes text content to automatically route to the matching native neural voice."""

    def __init__(self):
        # Common Marathi keywords (Latin script)
        self.marathi_latin = {
            "ahe", "aahe", "ahet", "aahet", "zala", "jhala", "kasa", "kashi", "kashe",
            "namaskar", "dhanyawad", "kay", "karto", "kartes", "kartoy", "ho", "nahi",
            "sang", "sanga", "bagh", "aiko", "kuthe", "tula", "mala", "amhi", "chhan"
        }
        # Comprehensive Hindi / Hinglish keywords (Latin script)
        self.hindi_latin = {
            "haan", "nahi", "karo", "karna", "karein", "karta", "karti", "kaise", "kripya",
            "acha", "achha", "theek", "bhai", "shukriya", "aap", "tum", "mera", "meri",
            "kya", "hai", "hain", "hoon", "hoga", "hogi", "main", "hum", "yeh", "woh",
            "abhi", "batao", "samajh", "gaya", "gayi", "kardo", "dijiye", "bataiye",
            "gaana", "gana", "bajao", "chalao", "sunao", "kholo", "dekho", "kuch", "aur",
            "zara", "yaar", "suno", "bol", "bolo", "sab", "raha", "rahi", "rahe", "kar",
            "chal", "chalu", "bhi", "liye", "saare", "apne", "apna", "apni", "pe", "par",
            "se", "ko", "ka", "ki", "ke", "ne", "bilkul", "zarur", "kyun", "kab", "kahan"
        }

    def detect_profile(self, text: str) -> str:
        """Determines optimal voice profile ensuring continuous voice identity."""
        if not text:
            return "english_irish"
        
        # Devanagari script detection
        if re.search(r'[\u0900-\u097F]', text):
            words = set(re.findall(r'\b\w+\b', text.lower()))
            if len(words.intersection(self.marathi_latin)) >= 1:
                return "marathi_native"
            return "hindi_devanagari"

        words = set(re.findall(r'\b\w+\b', text.lower()))
        if len(words.intersection(self.marathi_latin)) >= 1:
            return "marathi_native"
        if len(words.intersection(self.hindi_latin)) >= 1:
            return "hindi_native"

        # Default is Cinematic Irish Kerry Condon FRIDAY
        return "english_irish"


import queue


import hashlib

class NeuralVoiceEngine:
    """Manages high-fidelity neural voice synthesis and low-latency audio playback."""

    COMMON_PHRASES = [
        "Yes, Boss?",
        "Understood, Boss.",
        "Opening YouTube, Boss.",
        "Opening Google, Boss.",
        "Opening GitHub, Boss.",
        "Opening Spotify, Boss.",
        "Closed active tab, Boss.",
        "Systems are fully online and calibrated, Boss. Audio receptors active.",
        "Understood, Boss. Entering standby.",
        "Standby aborted, Boss."
    ]

    def __init__(self):
        self.detector = LanguageProfileDetector()
        self.temp_dir = os.path.join(tempfile.gettempdir(), "friday_voice_cache")
        self.cache_dir = os.path.join(tempfile.gettempdir(), "friday_voice_permanent_cache")
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)
        self.lock = threading.Lock()
        self._sapi_speaker = None
        self._text_queue = queue.Queue()
        self._audio_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._is_speaking_event = threading.Event()
        self._interrupt_event = threading.Event()
        self._active_voice_lock: Optional[str] = None

        self._synth_thread = threading.Thread(target=self._synthesis_worker, daemon=True)
        self._synth_thread.start()
        
        self._play_thread = threading.Thread(target=self._playback_worker, daemon=True)
        self._play_thread.start()

        threading.Thread(target=self._prewarm_cache, daemon=True).start()

    def _prewarm_cache(self):
        """Pre-caches standard affirmations and greetings in the background for zero-latency instant playback."""
        if not edge_tts:
            return
        for phrase in self.COMMON_PHRASES:
            try:
                voice_key = self.detector.detect_profile(phrase)
                cache_key = hashlib.md5(f"{phrase.strip().lower()}_{voice_key}".encode()).hexdigest()
                cached_file = os.path.join(self.cache_dir, f"cached_{cache_key}.mp3")
                if not os.path.exists(cached_file) or os.path.getsize(cached_file) < 100:
                    asyncio.run(self._synthesize_edge_tts(phrase, voice_key, cached_file))
            except Exception:
                pass

    def stop_immediate(self):
        """Immediately halts active speech playback and flushes speech queues in <30ms (Barge-In)."""
        self._interrupt_event.set()
        while not self._text_queue.empty():
            try:
                task = self._text_queue.get_nowait()
                if task and len(task) > 2 and task[2]:
                    task[2].set()
            except Exception:
                pass
        while not self._audio_queue.empty():
            try:
                item = self._audio_queue.get_nowait()
                if item and len(item) > 2 and item[2]:
                    item[2].set()
            except Exception:
                pass

        pyg = _get_pygame()
        if pyg:
            try:
                pyg.mixer.music.stop()
                pyg.mixer.music.unload()
            except Exception:
                pass

        try:
            mci = ctypes.windll.winmm.mciSendStringW
            mci("stop all", None, 0, 0)
            mci("close all", None, 0, 0)
        except Exception:
            pass

        self._is_speaking_event.clear()
        self._active_voice_lock = None
        time.sleep(0.01)
        self._interrupt_event.clear()

    def _synthesis_worker(self):
        """Pre-downloads MP3 files in advance so audio is ready before previous sentence finishes playing."""
        while not self._stop_event.is_set():
            try:
                task = self._text_queue.get(timeout=0.2)
            except queue.Empty:
                continue

            if task is None:
                break

            cleaned_text, voice_key, completion_event = task
            self._is_speaking_event.set()
            
            temp_path = None
            is_cached = False
            
            # 1. Check persistent instant-playback cache first
            cache_key = hashlib.md5(f"{cleaned_text.strip().lower()}_{voice_key}".encode()).hexdigest()
            cached_file = os.path.join(self.cache_dir, f"cached_{cache_key}.mp3")
            if os.path.exists(cached_file) and os.path.getsize(cached_file) > 100:
                temp_path = cached_file
                is_cached = True
            elif edge_tts:
                fallback_voices = [voice_key, "en-IN-NeerjaNeural", "en-IE-EmilyNeural"]
                for voice_candidate in fallback_voices:
                    try:
                        # For short common phrases (<= 120 chars), write directly to permanent cache
                        if len(cleaned_text) <= 120:
                            cand_cache_key = hashlib.md5(f"{cleaned_text.strip().lower()}_{voice_candidate}".encode()).hexdigest()
                            cand_cached_file = os.path.join(self.cache_dir, f"cached_{cand_cache_key}.mp3")
                            asyncio.run(self._synthesize_edge_tts(cleaned_text, voice_candidate, cand_cached_file))
                            if os.path.exists(cand_cached_file) and os.path.getsize(cand_cached_file) > 100:
                                temp_path = cand_cached_file
                                is_cached = True
                                break
                        else:
                            temp_filename = f"speech_{int(time.time() * 1000)}_{uuid.uuid4().hex[:6]}.mp3"
                            temp_path = os.path.join(self.temp_dir, temp_filename)
                            asyncio.run(self._synthesize_edge_tts(cleaned_text, voice_candidate, temp_path))
                            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 100:
                                is_cached = False
                                break
                            temp_path = None
                    except Exception:
                        temp_path = None

            # Push ready audio to playback queue
            self._audio_queue.put((temp_path, cleaned_text, completion_event, is_cached))
            self._text_queue.task_done()

    def _playback_worker(self):
        """Plays ready audio files smoothly one right after another with 0ms gap."""
        while not self._stop_event.is_set():
            try:
                item = self._audio_queue.get(timeout=0.2)
            except queue.Empty:
                continue

            if item is None:
                break

            temp_path, cleaned_text, completion_event, is_cached = item
            try:
                if temp_path and os.path.exists(temp_path):
                    with self.lock:
                        self._play_audio_file(temp_path)
                    if not is_cached:
                        try:
                            os.remove(temp_path)
                        except Exception:
                            pass
                else:
                    # Instant Local SAPI Female Fallback (Microsoft Zira)
                    sp = self._get_sapi_fallback()
                    sp.Speak(cleaned_text)
            except Exception as e:
                print(f"[Playback Error]: {e}")
            finally:
                if completion_event:
                    completion_event.set()
                self._audio_queue.task_done()
                if self._text_queue.empty() and self._audio_queue.empty():
                    self._is_speaking_event.clear()
                    self._active_voice_lock = None

    def _get_sapi_fallback(self):
        """Thread-local Windows SAPI female voice fallback (Microsoft Zira)."""
        pythoncom.CoInitialize()
        sp = wincl.Dispatch("SAPI.SpVoice")
        try:
            voices = sp.GetVoices()
            for v in voices:
                desc = v.GetDescription().lower()
                if "zira" in desc or "female" in desc or "eva" in desc or "hazel" in desc or "heera" in desc:
                    sp.Voice = v
                    return sp
            if voices.Count > 1:
                sp.Voice = voices.Item(1)
        except Exception:
            pass
        return sp

    def _play_audio_mci(self, file_path: str):
        """Native Windows MCI player for instant, zero-dependency MP3 playback."""
        try:
            alias = f"friday_audio_{int(time.time() * 1000)}"
            mci = ctypes.windll.winmm.mciSendStringW
            mci(f"close {alias}", None, 0, 0)
            mci(f'open "{file_path}" type mpegvideo alias {alias}', None, 0, 0)
            mci(f"setaudio {alias} volume to 1000", None, 0, 0)
            mci(f"play {alias} wait", None, 0, 0)
            mci(f"close {alias}", None, 0, 0)
        except Exception as e:
            print(f"[MCI Player Error]: {e}")

    def _play_audio_file(self, file_path: str):
        """Plays audio using Pygame or Native Windows MCI with instant barge-in support."""
        if self._interrupt_event.is_set():
            return
        pyg = _get_pygame()
        if pyg:
            try:
                pyg.mixer.music.load(file_path)
                pyg.mixer.music.set_volume(1.0)
                pyg.mixer.music.play()
                while pyg.mixer.music.get_busy():
                    if self._interrupt_event.is_set():
                        pyg.mixer.music.stop()
                        pyg.mixer.music.unload()
                        return
                    pyg.time.Clock().tick(25)
                pyg.mixer.music.unload()
                return
            except Exception:
                pass

        self._play_audio_mci(file_path)

    async def _synthesize_edge_tts(self, text: str, voice_key: str, output_file: str):
        """Synthesizes text using Edge-TTS neural stream with volume boost."""
        profile = VOICE_PROFILES.get(voice_key, VOICE_PROFILES["english_irish"])
        communicate = edge_tts.Communicate(
            text=text,
            voice=profile["voice"],
            rate=profile.get("rate", "+0%"),
            pitch=profile.get("pitch", "+0Hz"),
            volume=profile.get("volume", "+800%")
        )
        await communicate.save(output_file)

    def _normalize_speech_text(self, text: str) -> str:
        """Sanitizes and normalizes text for seamless, human-sounding voice synthesis."""
        if not text:
            return ""
        
        # 0. Normalize Assistant Acronyms for natural pronunciation
        t = re.sub(r'\bF\.R\.I\.D\.A\.Y\.?\b', 'Friday', text, flags=re.IGNORECASE)
        t = re.sub(r'\bJ\.A\.R\.V\.I\.S\.?\b', 'Jarvis', t, flags=re.IGNORECASE)

        # 1. Remove URLs
        t = re.sub(r"https?://\S+|www\.\S+", "website link", t)
        
        # 2. Remove code blocks and inline code
        t = re.sub(r"```[\s\S]*?```", "code omitted", t)
        t = re.sub(r"`[^`]*`", "", t)
        
        # 3. Remove bracketed technical system notes e.g. [Mem0], (timeout=...)
        t = re.sub(r"\[.*?\]", "", t)
        t = re.sub(r"\(HTTPConnectionPool.*?\)", "", t)
        
        # 4. Remove emojis and unusual unicode symbols
        t = re.sub(r"[\U00010000-\U0010ffff]", "", t)
        t = re.sub(r"[\u2600-\u26FF\u2700-\u27BF]", "", t)
        
        # 5. Remove markdown symbols (*, _, #, ~, >, |, `)
        t = re.sub(r"[\*#_`~>|]", "", t)
        
        # 6. Replace symbols with spoken words
        t = t.replace("&", " and ")
        t = t.replace("%", " percent ")
        t = t.replace("@", " at ")
        
        # 7. Normalize multiple spaces / line breaks
        t = re.sub(r"\s+", " ", t).strip()
        return t

    def speak(self, text: str, voice_override: Optional[str] = None, block: bool = False):
        """
        Synthesizes and speaks text using Movie-Grade Neural Multilingual Voice.
        Non-blocking by default (returns in <0.1ms). Audio begins playing as soon as first chunk synthesizes.
        """
        if not text or not text.strip():
            return

        cleaned_text = self._normalize_speech_text(text)
        if not cleaned_text:
            return

        # Determine or maintain session/turn voice lock
        if voice_override:
            voice_profile_key = voice_override
            self._active_voice_lock = voice_profile_key
        elif self.is_speaking() and self._active_voice_lock:
            # If current utterance turn is already locked (e.g. Hinglish), keep it consistent!
            voice_profile_key = self._active_voice_lock
        else:
            voice_profile_key = self.detector.detect_profile(cleaned_text)
            self._active_voice_lock = voice_profile_key

        # Stream sentences individually for sub-300ms first-word response
        sentences = [s.strip() for s in re.split(r'(?<=[.!?\n])\s+', cleaned_text) if s.strip()]
        if not sentences:
            sentences = [cleaned_text]

        completion_event = threading.Event() if block else None
        self._is_speaking_event.set()

        for idx, sentence in enumerate(sentences):
            # Only trigger block/completion_event on the final sentence
            event = completion_event if (idx == len(sentences) - 1) else None
            self._text_queue.put((sentence, voice_profile_key, event))

        if block and completion_event:
            completion_event.wait()

    def wait_until_done(self):
        """Blocks until all queued speech audio finishes playing."""
        self._text_queue.join()
        self._audio_queue.join()

    def is_speaking(self) -> bool:
        """Returns True if voice audio is currently playing."""
        return self._is_speaking_event.is_set() or not self._text_queue.empty() or not self._audio_queue.empty()


# Global instance
neural_voice_engine = NeuralVoiceEngine()
