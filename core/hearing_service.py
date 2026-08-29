"""
F.R.I.D.A.Y. Neural Ear Sensors & Multilingual Hearing Engine
Powered by Faster-Whisper (CTranslate2 INT8 CPU acceleration) with seamless Google STT fallback.
"""

import os
import io
import re
import wave
import time
import threading
import speech_recognition as sr
from typing import Optional, Tuple

HAS_FASTER_WHISPER = True


class SileroVADFilter:
    """Sub-millisecond Neural Voice Activity Detector (Silero VAD v5 ONNX)."""

    def __init__(self):
        self.model = None
        self.is_ready = False
        threading.Thread(target=self._init_vad, daemon=True).start()

    def _init_vad(self):
        try:
            import silero_vad
            self.model = silero_vad.load_silero_vad(onnx=True)
            self.is_ready = True
            print("[Silero VAD v5]: Neural Speech Detector Online (ONNX Sub-1ms).")
        except Exception:
            try:
                import torch
                model, _ = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', onnx=True)
                self.model = model
                self.is_ready = True
                print("[Silero VAD v5]: Neural Speech Detector Online (Torch Hub).")
            except Exception:
                pass

    def contains_speech(self, audio_data: sr.AudioData, threshold: float = 0.10) -> bool:
        """Evaluates whether audio frame contains real human speech vs ambient room noise / keystrokes."""
        if not self.is_ready or self.model is None:
            return True
        try:
            import numpy as np
            raw_bytes = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
            if len(raw_bytes) < 1600:
                return False
            audio_np = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            
            chunk_size = 512
            num_chunks = len(audio_np) // chunk_size
            if num_chunks == 0:
                return True
            
            speech_probs = []
            for i in range(0, min(num_chunks, 50)):
                chunk = audio_np[i * chunk_size : (i + 1) * chunk_size]
                try:
                    import torch
                    chunk_t = torch.from_numpy(chunk)
                    prob = self.model(chunk_t, 16000).item()
                    speech_probs.append(prob)
                except Exception:
                    try:
                        prob = float(self.model(chunk, 16000))
                        speech_probs.append(prob)
                    except Exception:
                        return True
            
            if speech_probs:
                return max(speech_probs) >= threshold
        except Exception:
            pass
        return True


class NeuralHearingEngine:
    """Manages high-speed neural acoustic ingestion, noise immunity, and multilingual transcription."""

    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.whisper_model = None
        self.vad = SileroVADFilter()
        self.is_loading = False
        self.lock = threading.Lock()
        self.initial_prompt = (
            "Hinglish, Hindi, English, Roman Urdu, Roman Hindi. F.R.I.D.A.Y., Friday, Jarvis, Boss. "
            "OpenCode, Claude Code, DeepSeek, Antigravity IDE, project status, about the project, "
            "kya chal raha hai, kahan tak pahuncha, kaam kahan tak pahuncha, progress update, "
            "kya haal hai, kaise ho, batao, samjhao, sunao, dikhao, play gaana, "
            "gaana bajao, gaana chalao, gaane sunao, kholo, band karo, roko, chalu karo, ruko, "
            "aaj ka mausam kaisa hai, taaza khabar batao, WhatsApp message bhejo, call karo, "
            "Seedhe Maut, Swah, Namastute, Nanchaku, 11K, Lunch Break, Bayaan, Nayaab, "
            "KR$NA, Divine, Raftaar, Talha Anjum, Talhah Yunus, Young Stunners, King, "
            "AP Dhillon, Shubh, Karan Aujla, Diljit Dosanjh, Sidhu Moosewala, Anuv Jain, "
            "Arijit Singh, Ritviz, Spotify, YouTube, Google Antigravity, "
            "VS Code, Python, code likho, program banao, screen dekho, photo dekho."
        )
        
        # Pre-warm Faster-Whisper model in background thread
        threading.Thread(target=self._init_whisper, daemon=True).start()

    def _init_whisper(self):
        """Loads INT8 CPU-quantized Whisper model for instant zero-cloud transcription."""
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            return

        with self.lock:
            try:
                # 1. Attempt instant offline load from local cache first
                self.whisper_model = WhisperModel(
                    self.model_size,
                    device="cpu",
                    compute_type="int8",
                    cpu_threads=4,
                    local_files_only=True
                )
                print(f"[Neural Hearing Engine]: Local Faster-Whisper ({self.model_size}) loaded (offline cache).")
            except Exception:
                try:
                    # 2. Download/verify from HuggingFace if not in local cache
                    self.whisper_model = WhisperModel(
                        self.model_size,
                        device="cpu",
                        compute_type="int8",
                        cpu_threads=4
                    )
                    print(f"[Neural Hearing Engine]: Local Faster-Whisper ({self.model_size}) loaded.")
                except Exception as e:
                    print(f"[Neural Hearing Engine Notice]: Faster-Whisper init: {e}. Fallback active.")

    def normalize_phonetics(self, raw_text: str) -> str:
        """
        Context-aware phonetic normalizer repairing common English STT substitutions
        for Hinglish slang, verbs, Desi Hip-Hop tracks, and software commands.
        """
        if not raw_text:
            return ""
        text = raw_text.strip()
        text_lower = text.lower()

        # 1. Seedhe Maut & DHH Track corrections
        text = re.sub(r'\b(cd\s+month|city\s+mouth|cd\s+mode|seedhe\s+mod|sidhe\s+maut|cd\s+maut|seedha\s+maut|sidha\s+maut)\b', 'Seedhe Maut', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(swaha|swat|swap|suah)\b(?=.*(?:seedhe|maut|song|track|play))', 'Swah', text, flags=re.IGNORECASE)
        text = re.sub(r'(?:play|song|track)\s+\b(swaha|swat|swap|suah)\b', 'play Swah', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(namaste\s+ute|namastutey|namas\s+tute)\b', 'Namastute', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(nanchaku|nan\s+chaku)\b', 'Nanchaku', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(krishna|krisna|krshna)\b(?=.*(?:rapper|artist|song|track|play|krsna))', 'KR$NA', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(talha\s+anjum|talha\s+yunus|young\s+stunners)\b', lambda m: m.group(0).title(), text, flags=re.IGNORECASE)
        text = re.sub(r'\b(ap\s+dhillon|karan\s+aujla|diljit\s+dosanjh|sidhu\s+moose\s*wala|anuv\s+jain|arijit\s+singh)\b', lambda m: m.group(0).title(), text, flags=re.IGNORECASE)

        # 2. Antigravity IDE & Tech corrections
        if re.search(r'\b(integrity\s+ide|anti\s+gravity\s+ide|anti-gravity\s+ide|integirty\s+ide|antigravity\s+ide)\b', text, flags=re.IGNORECASE):
            text = re.sub(r'\b(integrity|anti\s+gravity|anti-gravity|integirty|antigravity)\s+ide\b', 'Antigravity IDE', text, flags=re.IGNORECASE)
        elif re.search(r'\b(integrity|anti\s+gravity|anti-gravity|integirty)\b', text, flags=re.IGNORECASE) and any(w in text_lower for w in ["open", "launch", "start", "ide", "code", "editor", "google"]):
            text = re.sub(r'\b(integrity|anti\s+gravity|anti-gravity|integirty)\b', 'Antigravity IDE', text, flags=re.IGNORECASE)

        # 3. Common Hinglish verbs and intent phonetic repair
        text = re.sub(r'\b(gana|ganna|ghana)\b(?=.*(?:bajao|chalao|sunao|play|lagao))', 'gaana', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(bajo|bajha\s+do|baja\s+do|bajade|baja\s+de)\b', 'bajao', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(chala\s+do|chalado|chala\s+de|chalade)\b', 'chalao', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(bata\s+do|batado|bata\s+de|batade)\b', 'batao', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(khol\s+do|kholdo|khol\s+de|kholde)\b', 'kholo', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(samjha\s+do|samjhado|samjha\s+de|samjhade)\b', 'samjhao', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(dikha\s+do|dikhado|dikha\s+de|dikhade)\b', 'dikhao', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(bana\s+do|banado|bana\s+de|banade|banwa\s+do|banwado|banwa\s+de)\b', 'banao', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(likh\s+do|likhdo|likh\s+de|likhde)\b', 'likho', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(kar\s+do|kardo|kar\s+de|karde)\b', 'karo', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(rok\s+do|rokdo|rok\s+de|rokde)\b', 'roko', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(band\s+kardo|band\s+karde|bandh\s+karo)\b', 'band karo', text, flags=re.IGNORECASE)

        # 4. Hinglish Coding, OpenCode, Claude Code & AI delegation repairs
        text = re.sub(r'\b(coupon\s+code|coupon\s+se|coupon|open\s+code|open\s+cort|open\s+cad|opencode)\b', 'OpenCode', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(clod|claud|cloud\s+code|clawed|claud\s+code)\b', 'Claude', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(deep\s*seek|dip\s*seek|deep\s*sik)\b', 'DeepSeek', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(full\s*stake|fool\s*stack|ful\s*stack)\b', 'full stack', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(wether\s+app|wether|wheather)\b', 'weather app' if 'app' in text_lower else 'weather', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(ek\s+app\s+banao|ek\s+website\s+banao|code\s+likh\s+do)\b', lambda m: m.group(0), text, flags=re.IGNORECASE)

        # 5. Volume & OS control Hinglish repairs
        text = re.sub(r'\b(awaz|aawaz|aawaaz|sound)\s+(badha\s+do|badhao|up\s+karo|tez\s+karo)\b', 'volume badhao', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(awaz|aawaz|aawaaz|sound)\s+(kam\s+karo|ghatao|down\s+karo|dheeme\s+karo)\b', 'volume kam karo', text, flags=re.IGNORECASE)

        # 6. Accurate Friday wake-word phonetic repair (including Bluetooth earbud compressions)
        text = re.sub(r'\b(fry\s*day|fraiday|fryday|frida|frieda|phriday|flay\s*day|pride\s*day|freeday)\b', 'Friday', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(sun\s+friday|suno\s+friday|arre\s+friday|oye\s+friday|hey\s+friday|hi\s+friday|bhai\s+friday)\b', 'Friday', text, flags=re.IGNORECASE)

        # 7. Self-heal and vision intent phonetic repair
        text = re.sub(r'\b(heel\s+yourself|hill\s+yourself|heal\s+you\s*self)\b', 'heal yourself', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhow\s+many\s+finger\b', 'how many fingers', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdescribe\s+what\s+to\s+see\b', 'describe what you see', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdescribe\s+what\s+you\s+are\s+seeing\b', 'describe what you see', text, flags=re.IGNORECASE)

        return text

    def enhance_audio_for_stt(self, audio_data: sr.AudioData) -> sr.AudioData:
        """
        Enhances dynamic range and gain for low-energy audio frames (e.g. from in-ear Bluetooth mics).
        Prevents clipping and ensures crystal-clear speech recognition even when speaking softly.
        """
        try:
            import audioop
            raw = audio_data.get_raw_data()
            rms = audioop.rms(raw, audio_data.sample_width)
            # If audio is soft/whispery (< 1300 RMS), apply adaptive clean gain
            if 60 < rms < 1300:
                gain_factor = min(2.4, 1800.0 / max(rms, 100))
                boosted = audioop.mul(raw, audio_data.sample_width, gain_factor)
                return sr.AudioData(boosted, audio_data.sample_rate, audio_data.sample_width)
        except Exception:
            pass
        return audio_data

    def transcribe_audio_frame(self, recognizer: sr.Recognizer, audio_data: sr.AudioData) -> str:
        """
        Ultra-fast multilingual audio transcription with Silero VAD noise filtering:
        Stage 0: Neural VAD Filter - Instant (<1ms) rejection of keyboard clicks, noise, and silence.
        Tier 1: Cloud Google STT (en-IN / en-US) - Instant (<200ms), zero CPU overhead.
        Tier 2: Local Faster-Whisper (tiny) - Offline fallback with zero internet required.
        """
        # Stage 0: Neural VAD Screening
        if hasattr(self, 'vad') and not self.vad.contains_speech(audio_data):
            return ""

        # Preprocess low-volume earbud speech
        proc_audio = self.enhance_audio_for_stt(audio_data)

        import socket
        old_timeout = socket.getdefaulttimeout()
        try:
            socket.setdefaulttimeout(3.0) # Fast 3-second network limit prevents hanging queues
            # Tier 1: Lightning-fast Google STT (handles Hindi + English mixed natively)
            try:
                raw_text = recognizer.recognize_google(proc_audio, language="en-IN")
                if raw_text and len(raw_text.strip()) > 1:
                    return self.normalize_phonetics(raw_text)
            except Exception:
                pass

            try:
                raw_text = recognizer.recognize_google(proc_audio, language="en-US")
                if raw_text and len(raw_text.strip()) > 1:
                    return self.normalize_phonetics(raw_text)
            except Exception:
                pass
        finally:
            socket.setdefaulttimeout(old_timeout)

        # Tier 2: Local Offline Fallback via Faster-Whisper
        if self.whisper_model is not None:
            try:
                wav_bytes = proc_audio.get_wav_data(convert_rate=16000, convert_width=2)
                # Ignore tiny sound clicks (<0.20s)
                if len(wav_bytes) < 6400:
                    return ""

                wav_stream = io.BytesIO(wav_bytes)
                segments, info = self.whisper_model.transcribe(
                    wav_stream,
                    beam_size=1,
                    initial_prompt="English and Hinglish conversational voice commands.",
                    vad_filter=True,
                    vad_parameters=dict(min_silence_duration_ms=300, threshold=0.45),
                    condition_on_previous_text=False,
                    no_speech_threshold=0.6
                )
                
                valid_parts = []
                for seg in segments:
                    if getattr(seg, 'no_speech_prob', 0.0) < 0.6 and seg.text.strip():
                        valid_parts.append(seg.text.strip())
                
                text = " ".join(valid_parts).strip()
                text = self.normalize_phonetics(text)

                hallucinations = {
                    ".", "thank you.", "thank you", "thanks for watching.", 
                    "thanks for watching", "bye.", "no.", "you", "oh,", "oh.",
                    "subtitles by", "amara.org", "friday", "friday.", "boss", "boss."
                }
                if text and text.lower() not in hallucinations and len(text) > 1:
                    return text
            except Exception:
                pass

        return ""


# Global singleton instance (CPU-optimized tiny model for zero-lag offline fallback)
hearing_engine = NeuralHearingEngine(model_size="tiny")
