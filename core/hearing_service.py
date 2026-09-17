"""
F.R.I.D.A.Y. Neural Ear Sensors & Multilingual Hearing Engine
Powered by Faster-Whisper (CTranslate2 INT8 CPU acceleration) with seamless Google STT fallback.
"""

import io
import re
import time
import threading
import speech_recognition as sr

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
                hub_res = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', onnx=True)
                self.model = hub_res[0] if isinstance(hub_res, (list, tuple)) else hub_res
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
            "Stranger Things, Vincenzo, Game of Thrones, Breaking Bad, Squid Game, Peaky Blinders, "
            "Dark, All of Us Are Dead, Money Heist, Narcos, The Boys, Season, Episode, Ep, "
            "anime, full movie, trailer, stream, watch, play, "
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

        # 8. Popular Cinema, K-Drama, and Show title phonetic repairs
        text = re.sub(r'\b(titani|tight\s*anic|titannic|titan)\b(?=.*(?:movie|film|scene|song|ship|play|watch))', 'Titanic', text, flags=re.IGNORECASE)
        text = re.sub(r'(?:play|watch|stream)\s+\b(titan|titani|tight\s*anic)\b', 'play Titanic', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(vin\s*cenzo|vincenso|vinsenzo|vinsanzo|winzenzo)\b', 'Vincenzo', text, flags=re.IGNORECASE)

        # 9. Media, Anime Lore & Coding phonetic repairs (Acoustic drift compensation)
        text = re.sub(r'\b(?:please|plz)\s+(?:play\s+)?(?=.*(?:starboy|the\s+weeknd|the\s+weekend|song|track|music|lofi|video|movie|episode|season))', 'play ', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(?:enemy\s+law|enemy\s+lover|animal\s+lover|enemy\s+lore|anime\s+law|any\s+lore|enemy\s+lord)\b', 'anime lore', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(?:built\s+and|built\s+an|build\s+and)\b', 'build an', text, flags=re.IGNORECASE)
        text = re.sub(r'\blofi\s+be\b', 'lofi beats', text, flags=re.IGNORECASE)

        # 10. System Status & Code question acoustic repairs
        text = re.sub(r'\b(?:warriors\s+are|warrior\s+is)\b', 'where is our', text, flags=re.IGNORECASE)
        text = re.sub(r'\bwhatsapp\s+system(?:\s+status)?\b', 'what is our system status', text, flags=re.IGNORECASE)
        text = re.sub(r'\bwhat\s+is\s+a\s+system\b', 'what is our system status', text, flags=re.IGNORECASE)

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
                rec_fn = getattr(recognizer, "recognize_google", None)
                if rec_fn:
                    raw_text = rec_fn(proc_audio, language="en-IN")
                    if raw_text and len(raw_text.strip()) > 1:
                        return self.normalize_phonetics(raw_text)
            except Exception:
                pass

            try:
                rec_fn = getattr(recognizer, "recognize_google", None)
                if rec_fn:
                    raw_text = rec_fn(proc_audio, language="en-US")
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


def start_speech_pipeline(audio_queue, raw_audio_queue, media_engine, neural_voice_engine, comm_link, play_sound_fn, is_speaking_fn=None, drain_fn=None):
    """
    Dedicated continuous audio ingestion pipeline:
    - Dedicated mic worker with automatic Bluetooth earbud hot-swapping and acoustic calibration.
    - 3 parallel transcription workers with sub-30ms Full-Duplex Barge-In and instant media pause.
    """
    def mic_capture_worker():
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
            except Exception:
                try:
                    mic_w = sr.Microphone()
                    with mic_w as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.15)
                except Exception:
                    mic_w = None
            return mic_w

        mic_w = init_or_switch_mic()
        last_check_time = time.time()

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
                            if time.time() - last_check_time > 10.0:
                                last_check_time = time.time()
                                check_idx, _, check_earbud = comm_link.get_best_microphone_index()
                                if check_idx != current_mic_idx or check_earbud != current_is_earbud:
                                    init_or_switch_mic()
                                    break

                            p_limit = 3.5 if getattr(media_engine, 'is_playing', False) else 12.0
                            audio = recognizer.listen(source, timeout=None, phrase_time_limit=p_limit)
                            while raw_audio_queue.qsize() > 3:
                                try:
                                    raw_audio_queue.get_nowait()
                                except Exception:
                                    break
                            try:
                                raw_audio_queue.put_nowait((recognizer, audio))
                            except Exception:
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
        while True:
            try:
                rec, audio_chunk = raw_audio_queue.get()
                text = hearing_engine.transcribe_audio_frame(rec, audio_chunk)
                if not text or len(text.strip()) <= 1:
                    continue

                if getattr(media_engine, 'is_playing', False):
                    t_lower = text.lower().strip()
                    media_interrupt_words = ["stop", "ruko", "pause", "band karo", "quiet", "mute", "chup", "shutup"]
                    if any(w in t_lower for w in media_interrupt_words):
                        print(f"\n[Instant Media Stop]: Intercepted '{text}' -> Halting playback immediately.")
                        if play_sound_fn:
                            play_sound_fn("cancel")
                        media_engine.stop()
                        if drain_fn:
                            drain_fn()
                        continue

                speaking = neural_voice_engine.is_speaking() if neural_voice_engine else False
                if is_speaking_fn:
                    speaking = speaking or is_speaking_fn()
                if speaking:
                    t_lower = text.lower().strip()
                    interrupt_words = ["stop", "ruko", "chup", "quiet", "wait", "shutup", "pause", "friday", "hold on", "cancel"]
                    if any(w in t_lower for w in interrupt_words):
                        print(f"\n[Barge-In]: Active speech interrupted by Boss ('{text}').")
                        if play_sound_fn:
                            play_sound_fn("cancel")
                        if neural_voice_engine:
                            neural_voice_engine.stop_immediate()
                        if drain_fn:
                            drain_fn()
                    continue

                audio_queue.put(text)
            except Exception:
                time.sleep(0.02)

    t_mic = threading.Thread(target=mic_capture_worker, daemon=True)
    t_mic.start()
    for _ in range(3):
        threading.Thread(target=transcription_worker, daemon=True).start()
