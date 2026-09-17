"""
========================================================================================
F.R.I.D.A.Y. OS 10.0 — Next.js-Style Honeycomb Micro-Kernel
Multi-Agent Tactical Operating System & Autonomous Engineering Partner
========================================================================================
"""

import sys
import os
import warnings
import atexit
import time
import queue
import re
import threading
from dotenv import load_dotenv

load_dotenv()

# Suppress non-critical third-party telemetry and warnings
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")
os.environ["POSTHOG_DISABLED"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["PYTHONWARNINGS"] = "ignore"

# Configure UTF-8 encoding across Windows standard streams
if sys.platform == "win32":
    try:
        getattr(sys.stdout, "reconfigure", lambda **kw: None)(encoding="utf-8")
        getattr(sys.stderr, "reconfigure", lambda **kw: None)(encoding="utf-8")
    except Exception:
        pass

# Core subsystem engines
from core.headroom_memory import memory_engine
from core.personality_engine import personality_engine
from core.hearing_service import start_speech_pipeline
from core.omnivoice_service import neural_voice_engine
from core.media_engine import media_engine
from core.comm_link import comm_link
from core.terminal_hud import (
    render_startup_banner,
    print_heard,
    print_listening_state
)

# Honeycomb Hubs & Shared Base Infrastructure
from core.hubs.base import (
    audio_queue,
    raw_audio_queue,
    IS_SPEAKING,
    play_sound,
    speak,
    drain_audio_queues,
    collect_continuous_speech
)
from core.hubs import chat_hub
from core.hubs import media_hub
from core.hubs import system_hub
from core.hubs import coding_hub
from core.hubs import vision_hub
from core.hubs import web_hub
from core.hubs import build_unified_commands

# Register automated shutdown memory consolidation
atexit.register(memory_engine.consolidate_session_memory)

# Build unified command dispatch registry across all 6 hubs
COMMANDS, COMPILED_COMMANDS = build_unified_commands()

def processCommand(c: str):
    """Unified Honeycomb Command Dispatcher with Project Valkyrie behavioral checks."""
    try:
        cmd = c.lower().strip()

        # --- PROJECT VALKYRIE BEHAVIORAL & PERSONA HOOKS ---
        bribe_reply = personality_engine.check_reconciliation(cmd)
        if bribe_reply:
            play_sound("launch")
            speak(bribe_reply)
            return

        insult_reply = personality_engine.check_for_insults(cmd)
        if insult_reply:
            play_sound("error")
            speak(insult_reply)
            return

        if personality_engine.state.get("sulking", False):
            if not any(p in cmd for p in ["code red", "priority code red", "emergency override"]):
                play_sound("cancel")
                speak(personality_engine.get_sulking_refusal())
                return

        approved, counter_arg = personality_engine.evaluate_architectural_proposal(cmd)
        if not approved and counter_arg:
            play_sound("cancel")
            speak(counter_arg)
            return
        elif approved and counter_arg:
            play_sound("launch")
            speak(counter_arg)
            if any(cmd.strip().startswith(p) for p in ["execute as ordered", "just do it", "my decision", "override debate"]):
                return

        disc_action = personality_engine.check_late_night_discipline()
        if disc_action:
            speak(disc_action["speech"])
            if disc_action.get("action") == "lock_screen":
                return

        # Phonetic alias normalization for Antigravity IDE
        if re.search(r'\b(integrity\s+ide|anti\s+gravity\s+ide|anti-gravity\s+ide|integirty\s+ide|antigravity\s+ide)\b', cmd):
            cmd = re.sub(r'\b(integrity|anti\s+gravity|anti-gravity|integirty)\s+ide\b', 'antigravity ide', cmd)
        elif re.search(r'\b(integrity|anti\s+gravity|anti-gravity|integirty)\b', cmd) and any(w in cmd for w in ["open", "launch", "start", "ide"]):
            cmd = re.sub(r'\b(integrity|anti\s+gravity|anti-gravity|integirty)\b', 'antigravity ide', cmd)

        # --- HONEYCOMB HUB INTENT DISPATCHERS ---
        if vision_hub.dispatch_vision_intent(cmd):
            return
        if coding_hub.dispatch_coding_intent(cmd):
            return
        if web_hub.dispatch_web_intent(cmd):
            return
        if media_hub.dispatch_media_intent(cmd):
            return

        # --- PRE-COMPILED DICTIONARY ROUTING ---
        matched_key = None
        for pattern, k in COMPILED_COMMANDS:
            if pattern.search(cmd):
                matched_key = k
                break

        if matched_key:
            COMMANDS[matched_key](cmd)
        else:
            play_sound("launch")
            chat_hub.get_ai_response(c, speak_stream=True)
            if len(c.split()) > 3:
                chat_hub.handleSuggestion(c)
    except Exception as err:
        print(f"\n[Command Dispatch Error]: {err}")
        play_sound("error")
        speak("I encountered an issue processing that instruction, Boss. All operating systems remain secure.")

def warmup_model():
    """Background pre-warm for neural embeddings and Gemini daemon."""
    time.sleep(2.0)
    try:
        chat_hub.ensure_gemini_web2api_running()
    except Exception:
        pass

def is_trailing_incomplete(text: str) -> bool:
    """Detects if speech ended mid-thought on a connector, preposition, or verb."""
    t = text.strip().lower()
    trailing_patterns = [
        r'\b(and|aur|ki|to|with|for|which|that|also|like|but|lekin|then|because|kyunki|or|ya|so|such as)$',
        r'\b(create\s+a|build\s+a|make\s+a|write\s+a|open\s+the|search\s+for|show\s+me|tell\s+me|can\s+you|please)$',
        r'\b(what\'?s|what\s+is|where\s+is|how\s+to|who\s+is|why\s+is|when\s+is|which\s+is|lore\s+of|law\s+of)$',
        r'\b(in|on|at|of|from|into|about|by|as|the|a|an)$'
    ]
    return any(re.search(p, t) for p in trailing_patterns)

WAKE_WORDS = [
    "friday", "fryday", "fraiday", "fry day", "frida", "frieda", "phriday", "f.r.i.d.a.y",
    "wake up", "sun friday", "friday sun", "suno friday", "sun na friday",
    "are friday", "arre friday", "oye friday", "hey friday", "hi friday",
    "hello friday", "bhai friday", "jarvis", "hey jarvis", "hi jarvis"
]

if __name__ == "__main__":
    play_sound("startup")
    threading.Thread(target=warmup_model, daemon=True).start()
    threading.Thread(target=system_hub.battery_monitor_sentinel, daemon=True).start()
    render_startup_banner()

    # Boot the dedicated continuous speech & transcription pipeline
    start_speech_pipeline(
        audio_queue=audio_queue,
        raw_audio_queue=raw_audio_queue,
        media_engine=media_engine,
        neural_voice_engine=neural_voice_engine,
        comm_link=comm_link,
        play_sound_fn=play_sound,
        is_speaking_fn=lambda: IS_SPEAKING,
        drain_fn=drain_audio_queues
    )

    speak("Systems are fully online and calibrated, Boss. Audio receptors active.")

    is_awaiting_printed = False

    while True:
        try:
            if not is_awaiting_printed:
                print_listening_state()
                is_awaiting_printed = True

            raw_input = audio_queue.get()
            command_lower = raw_input.lower().strip()

            wake_word_found = False
            parsed_command = ""

            for wake in sorted(WAKE_WORDS, key=len, reverse=True):
                if wake in command_lower:
                    wake_word_found = True
                    idx = command_lower.find(wake)
                    cmd_idx = idx + len(wake)
                    suffix = raw_input[cmd_idx:].strip().strip(",.?!:;-~ ")
                    prefix = raw_input[:idx].strip().strip(",.?!:;-~ ")
                    if suffix and len(suffix) > 0:
                        parsed_command = suffix
                        if prefix and len(prefix) > 0:
                            parsed_command = f"{prefix} {suffix}".strip()
                    elif prefix and len(prefix) > 0:
                        parsed_command = prefix
                    else:
                        parsed_command = ""
                    break

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
                neural_voice_engine.wait_until_done()
                time.sleep(0.05)

                print("--- Listening for your command (Speak freely, pauses welcome) ---")
                try:
                    first_phrase = audio_queue.get(timeout=10.0)
                except queue.Empty:
                    continue

                full_command = collect_continuous_speech(first_phrase, silence_timeout=0.9)
                if not full_command:
                    continue

                print_heard(full_command)
                processCommand(full_command)
                neural_voice_engine.wait_until_done()
                drain_audio_queues()
            else:
                if is_trailing_incomplete(parsed_command):
                    full_command = collect_continuous_speech(parsed_command, silence_timeout=0.9)
                else:
                    try:
                        extra_chunk = audio_queue.get(timeout=0.45)
                        if extra_chunk and extra_chunk.strip():
                            clean_extra = extra_chunk.strip()
                            if clean_extra.lower() not in ["cancel", "stop", "never mind", "nevermind"]:
                                full_command = f"{parsed_command} {clean_extra}"
                                print(f"   [Continued Speaking]: {clean_extra}")
                            else:
                                full_command = ""
                        else:
                            full_command = parsed_command
                    except queue.Empty:
                        full_command = parsed_command

                if not full_command:
                    continue

                play_sound("launch")
                print_heard(full_command)
                processCommand(full_command)
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
