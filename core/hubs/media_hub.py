"""
F.R.I.D.A.Y. Honeycomb Media Hub
Unified Aegis Media Suite: native audio/video MPV streaming, lyrics, anime, TV series, and books narration.
"""

import re
from core.media_engine import media_engine
from core.books_adapter import books_adapter
from core.lore_engine import lore_engine
from core.viking_vault import viking_vault
from core.hubs.base import play_sound, speak

FAVORITE_PLAYLIST = "https://open.spotify.com/playlist/1XJ9GFC9SQQLedkTsoxBiw?si=fc3bdf3d4864409b"
LAST_PLAYED_TRACK = ""

def control_media(action: str) -> bool:
    """Simulates media keyboard hotkeys via pyautogui."""
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

def handle_media(cmd: str):
    """General media playback and volume control."""
    cmd_lower = cmd.lower()
    if "pause" in cmd_lower or "resume" in cmd_lower:
        play_sound("launch")
        speak(media_engine.pause_or_resume())
        return
    elif "stop" in cmd_lower:
        handle_media_stop(cmd)
        return
    elif "volume up" in cmd_lower:
        speak(media_engine.set_volume_level(media_engine.current_volume + 10))
        return
    elif "volume down" in cmd_lower:
        speak(media_engine.set_volume_level(media_engine.current_volume - 10))
        return
    elif "mute" in cmd_lower:
        media_engine.send_ipc_command(["cycle", "mute"])
        speak("Media audio muted, Boss.")
        return
    elif "next" in cmd_lower or "forward" in cmd_lower or "skip" in cmd_lower:
        speak(media_engine.seek_relative(10))
        return
    elif "previous" in cmd_lower or "rewind" in cmd_lower or "back" in cmd_lower:
        speak(media_engine.seek_relative(-10))
        return

def handle_media_stop(cmd: str):
    """Terminates all active media playback."""
    play_sound("cancel")
    media_engine.stop()
    speak("Playback terminated, Boss. All background media pipelines freed.")

def handle_media_toggle_hud(cmd: str):
    """Toggles floating MPV video window visibility."""
    play_sound("launch")
    speak(media_engine.toggle_video_visibility())

def handle_media_focus_mode(cmd: str):
    """Engages deep focus synthwave ambient beat loop."""
    play_sound("launch")
    speak("Engaging Deep Focus Mode, Boss. Suppressing non-critical notifications and queuing flow-state frequencies.")
    media_engine.play_audio("deep focus synthwave ambient study beats")

def handle_media_recommendations(cmd: str):
    """Provides personalized media recommendations from Viking Vault."""
    play_sound("launch")
    recs = viking_vault.get_smart_recommendations()
    if recs:
        rec_text = ", ".join(recs[:3])
        speak(f"Based on your recent playback telemetry, Boss, you've shown high affinity for {rec_text}. Shall I queue up a mix?")
    else:
        speak("I am still mapping your taste profile, Boss. Tell me your favorite artists or anime to accelerate calibration.")

def handle_media_lyrics(cmd: str):
    """Fetches and displays live song lyrics."""
    play_sound("launch")
    title = media_engine.current_track.get("title", "")
    uploader = media_engine.current_track.get("uploader", "")
    if not title:
        speak("No active song playing to extract lyrics for, Boss.")
        return
    lyrics = lore_engine.get_lyrics(uploader, title)
    if lyrics:
        speak(f"Lyrics for {title}:\n" + lyrics[:200] + "...")
    else:
        speak(f"Unable to resolve verified live lyrics for {title}, Boss.")

def handle_media_companion_lore(cmd: str):
    """Synthesizes live anime/movie companion lore recap."""
    play_sound("launch")
    title = media_engine.current_track.get("title", "")
    if not title:
        speak("No active media playing on the HUD, Boss.")
        return
    ans = lore_engine.synthesize_live_companion_answer(title, cmd)
    speak(ans)

def handle_anime_lore(cmd: str):
    """Fetches and speaks live anime lore, score, and synopsis from Jikan/Kitsu APIs."""
    clean_title = re.sub(r'(?i)\b(?:tell\s+me\s+)?(?:the\s+)?(?:anime\s+lore|enemy\s+law|enemy\s+lover|animal\s+lover|lore|synopsis)\s+(?:of|for|about)?\s*', '', cmd).strip()
    if not clean_title:
        title = media_engine.current_track.get("title", "")
        clean_title = title or "Naruto"
    
    play_sound("launch")
    speak(f"Querying global anime telemetry for {clean_title}, Boss.")
    info = lore_engine.get_anime_lore(clean_title)
    if info.get("found"):
        title_disp = info.get("title", clean_title)
        score = info.get("score", "N/A")
        episodes = info.get("episodes", "ongoing")
        synopsis = info.get("synopsis", "")
        synopsis = re.sub(r'\[Written by MAL Rewrite\]', '', synopsis).strip()
        short_synopsis = synopsis[:250] + "..." if len(synopsis) > 250 else synopsis
        speech = f"{title_disp} holds a rating of {score} with {episodes} episodes. Synopsis: {short_synopsis}"
        speak(speech)
    else:
        speak(f"Unable to locate verified anime lore records for {clean_title}, Boss.")

def handle_tv_lore(cmd: str):
    """Fetches TV show summary and premiere date from TVMaze API."""
    clean_title = re.sub(r'(?i)\b(?:tell\s+me\s+)?(?:the\s+)?(?:tv\s+show\s+lore|show\s+lore|tv\s+lore|who\s+is|lore\s+of)\s+(?:about|for)?\s*', '', cmd).strip()
    if not clean_title:
        clean_title = "Breaking Bad"
    play_sound("launch")
    info = lore_engine.get_tv_show_summary(clean_title)
    if info.get("found"):
        name = info.get("name", clean_title)
        rating = info.get("rating", "N/A")
        premiered = info.get("premiered", "")
        summary = info.get("summary", "")[:250]
        speech = f"{name}, premiered in {premiered}, rated {rating}. Summary: {summary}"
        speak(speech)
    else:
        speak(f"Unable to locate TV series records for {clean_title}, Boss.")

def handle_read_book(cmd: str):
    """Books Adapter: Loads book and begins streaming neural narration."""
    clean_target = re.sub(r"^(?:read\s+(?:book|aloud|me)?|narrate\s+(?:book)?|open\s+book)\s*", "", cmd, flags=re.I).strip()
    play_sound("launch")
    if not clean_target:
        status = books_adapter.get_status()
        if status.get("has_book"):
            speak(f"Resuming narration of {status['title']} from Chapter {status['current_chapter'] + 1}, Boss.")
            books_adapter.read_aloud(speak_fn=speak)
        else:
            speak("Which book or document should I open and narrate for you, Boss?")
        return
    res = books_adapter.load_book(clean_target)
    speak(res)
    if books_adapter.current_book:
        books_adapter.read_aloud(speak_fn=speak)

def handle_book_next_chapter(cmd: str):
    """Books Adapter: Skips to the next chapter."""
    play_sound("launch")
    speak(books_adapter.next_chapter())

def handle_book_prev_chapter(cmd: str):
    """Books Adapter: Rewinds to the previous chapter."""
    play_sound("launch")
    speak(books_adapter.prev_chapter())

def handle_book_status(cmd: str):
    """Books Adapter: Reports reading telemetry and bookmark progress."""
    play_sound("launch")
    st = books_adapter.get_status()
    if not st.get("has_book"):
        speak("No active book is loaded in the Books Adapter, Boss.")
    else:
        speak(f"Currently reading '{st['title']}', Chapter {st['current_chapter'] + 1} of {st['total_chapters']}. Progress stands at {st['progress_pct']}%, Boss.")

def handle_spotify(cmd: str):
    """PROJECT A.E.G.I.S.: Unified native audio/video streaming dispatcher."""
    global FAVORITE_PLAYLIST, LAST_PLAYED_TRACK
    cmd_lower = cmd.lower().strip()

    # 0. Check late-night binge discipline
    binge_warning = viking_vault.check_binge_discipline()
    if binge_warning:
        media_engine.stop()
        play_sound("error")
        speak(binge_warning)
        return

    # Check playlist / favorites update
    if "set" in cmd_lower and "favorite" in cmd_lower:
        new_fav = cmd.split("to")[-1].strip()
        FAVORITE_PLAYLIST = new_fav
        speak(f"Signature playlist updated, Boss. I've stored {FAVORITE_PLAYLIST} in active memory.")
        return

    # 0. Check for Next Episode / Previous Episode intent
    if any(w in cmd_lower for w in ["next episode", "play next episode", "agla episode", "agle episode", "skip episode"]):
        play_sound("launch")
        media_engine.play_next_episode(speak_fn=speak)
        return
    if any(w in cmd_lower for w in ["previous episode", "play previous episode", "pichla episode", "pichle episode", "last episode"]):
        play_sound("launch")
        media_engine.play_previous_episode(speak_fn=speak)
        return

    # 0.1 Check for Caption / Subtitle voice controls
    if any(w in cmd_lower for w in ["captions on", "subtitles on", "turn on captions", "turn on subtitles", "show subtitles"]):
        res = media_engine.toggle_captions(force_state=True)
        speak(res)
        return
    if any(w in cmd_lower for w in ["captions off", "subtitles off", "turn off captions", "turn off subtitles", "hide subtitles"]):
        res = media_engine.toggle_captions(force_state=False)
        speak(res)
        return
    if any(w in cmd_lower for w in ["change language", "switch language", "change audio", "switch audio", "hindi audio", "english audio"]):
        res = media_engine.cycle_audio_language()
        speak(res)
        return
    if any(w in cmd_lower for w in ["change subtitle", "switch subtitle", "change caption", "switch caption"]):
        res = media_engine.cycle_subtitle_language()
        speak(res)
        return

    # 0.2 Check for Stream Quality voice controls
    if any(w in cmd_lower for w in ["1080p", "full hd", "high quality", "highest quality", "best quality"]):
        res = media_engine.set_video_quality("1080p")
        speak(res)
        return
    if any(w in cmd_lower for w in ["720p", "medium quality"]):
        res = media_engine.set_video_quality("720p")
        speak(res)
        return

    # 1. Check for K-Drama / TV Series / Web Shows / Season / Episode intent
    drama_triggers = [
        "kdrama", "k-drama", "drama", "series", "tv show", "web series", "show", "season", "episode",
        "vincenzo", "squid game", "all of us are dead", "breaking bad", "game of thrones",
        "stranger things", "stran", "peaky blinders", "dark", "money heist", "narcos", "the boys"
    ]
    if any(w in cmd_lower for w in drama_triggers):
        clean_show = re.sub(r'^(?:play|watch|stream|please|the)\s+', '', cmd, flags=re.I).strip()
        clean_show = re.sub(r'\b(?:on youtube|on netflix|on spotify)\b', '', clean_show, flags=re.I).strip()
        play_sound("launch")
        media_engine.play_video(clean_show, speak_fn=speak)
        return

    # 2. Check for anime intent
    if "anime" in cmd_lower:
        clean_anime = re.sub(r'\b(?:play|watch|stream|the|anime|series|episode|ep|show)\b', '', cmd, flags=re.I).strip()
        play_sound("launch")
        media_engine.play_video(clean_anime, speak_fn=speak, is_anime=True)
        return

    # 3. Check for MovieBox Cinema TUI launch
    if any(k in cmd_lower for k in ["open cinema", "open moviebox", "launch cinema", "launch moviebox", "start cinema", "moviebox"]):
        from core.moviebox_engine import moviebox_engine
        play_sound("launch")
        moviebox_engine.launch_cinema_tui(speak_fn=speak)
        return

    # 4. Check for movie intent
    if any(w in cmd_lower for w in ["movie", "film", "cinema"]):
        clean_movie = re.sub(r'\b(?:play|watch|stream|the|movie|film|cinema)\b', '', cmd, flags=re.I).strip()
        play_sound("launch")
        if not clean_movie:
            from core.moviebox_engine import moviebox_engine
            moviebox_engine.launch_cinema_tui(speak_fn=speak)
        else:
            media_engine.play_video(clean_movie, speak_fn=speak, is_movie=True)
        return

    # 4. Check for latest channel upload intent
    if any(w in cmd_lower for w in ["latest video", "new video", "new upload"]):
        chan = re.sub(r'\b(?:play|watch|show|the|a|latest|new|video|upload|by|from|pe)\b', '', cmd, flags=re.I).strip()
        chan = re.sub(r'[\'"]+', '', chan).strip()
        if chan:
            play_sound("launch")
            media_engine.play_latest_channel(chan, speak_fn=speak)
            return

    # 5. Check for video / visual intent
    if any(cmd_lower.startswith(p) for p in ["watch ", "video of ", "play video "]) or "video" in cmd_lower:
        clean_vid = re.sub(r'\b(?:play|watch|video|of|the|on youtube)\b', '', cmd, flags=re.I).strip()
        play_sound("launch")
        media_engine.play_video(clean_vid, speak_fn=speak)
        return

    # 6. Clean query for media playback
    query = cmd
    for p in [
        "play", "on spotify", "spotify pe", "spotify par", "spotify", "on youtube", "youtube pe", 
        "my", "playlist", "gaana", "gana", "music", "song", "track", "bajao", "chalao", "sunao", 
        "please", "zara", "ek", "chala do", "baja do", "chalu karo", "khol do"
    ]:
        query = re.sub(rf"\b{re.escape(p)}\b", "", query, flags=re.IGNORECASE)

    query = re.sub(r"^[,\.\s\"']+|[,\.\s\"']+$", "", query).strip()
    query = re.sub(r'\bkrishna\b', 'KR$NA', query, flags=re.IGNORECASE)

    play_sound("launch")

    # Explicit music/audio intent check
    music_keywords = [
        "song", "gaana", "gana", "music", "track", "playlist", "lofi", "beat",
        "beats", "spotify", "audio", "bajao", "sunao", "bgm", "ost", "remix", "album"
    ]
    is_explicit_music = any(m in cmd_lower for m in music_keywords)

    # Playlist or empty query fallback
    is_playlist_intent = any(p in cmd_lower for p in ["my playlist", "playlist", "meri playlist", "mera playlist", "signature playlist", "favorites"])
    if is_playlist_intent or not query:
        query = "lofi hip hop radio beats to relax study to"
        is_explicit_music = True

    LAST_PLAYED_TRACK = query

    if is_explicit_music:
        media_engine.play_audio(query, speak_fn=speak)
    else:
        media_engine.play_video(query, speak_fn=speak)

def dispatch_media_intent(cmd: str) -> bool:
    """Checks for complex media patterns, anime/tv lore, and dispatches to Aegis streaming."""
    cmd_lower = cmd.lower()

    # 1. Anime / TV Lore Companion Queries
    if re.search(r'\b(?:anime\s+lore|enemy\s+law|enemy\s+lover|animal\s+lover|lore\s+of\s+anime)\b', cmd, re.I):
        handle_anime_lore(cmd)
        return True
    if re.search(r'\b(?:tv\s+show\s+lore|tv\s+lore|show\s+lore)\b', cmd, re.I):
        handle_tv_lore(cmd)
        return True

    # 2. Artist / Music intent even if 'play' was heard as 'please' or omitted
    if re.search(r'\b(?:starboy|weeknd|weekend|seedhe\s+maut|talha\s+anjum|krsna|lofi\s+beats)\b', cmd, re.I):
        handle_spotify(cmd)
        return True

    media_intent_triggers = [
        r'\b(?:season\s+\d+|episode\s+\d+|ep\s+\d+)\b',
        r'\b(?:next\s+episode|previous\s+episode|agla\s+episode|pichla\s+episode|skip\s+episode)\b',
        r'\b(?:captions\s+on|captions\s+off|subtitles\s+on|subtitles\s+off|show\s+subtitles|hide\s+subtitles)\b',
        r'\b(?:change\s+language|switch\s+language|change\s+audio|switch\s+audio|hindi\s+audio|english\s+audio)\b',
        r'\b(?:change\s+subtitle|switch\s+subtitle|change\s+caption|switch\s+caption)\b',
        r'\b(?:1080p|full\s+hd|high\s+quality|highest\s+quality|best\s+quality|720p)\b',
        r'\b(?:stranger\s+things|vincenzo|squid\s+game|breaking\s+bad|game\s+of\s+thrones|peaky\s+blinders|money\s+heist|dark|narcos|the\s+boys)\b',
        r'\b(?:kdrama|k-drama|anime|movie|trailer|full\s+movie)\b'
    ]
    if any(re.search(pat, cmd, re.I) for pat in media_intent_triggers):
        handle_spotify(cmd)
        return True
    return False

# Mapping of voice triggers to media handlers
COMMANDS = {
    "volume up": handle_media,
    "volume down": handle_media,
    "mute": handle_media,
    "pause": handle_media,
    "next": handle_media,
    "previous": handle_media,
    "stop music": handle_media_stop,
    "stop player": handle_media_stop,
    "stop playing": handle_media_stop,
    "stop stream": handle_media_stop,
    "stop video": handle_media_stop,
    "show video": handle_media_toggle_hud,
    "open player": handle_media_toggle_hud,
    "display video": handle_media_toggle_hud,
    "hide video": handle_media_toggle_hud,
    "close video player": handle_media_toggle_hud,
    "ghost audio": handle_media_toggle_hud,
    "focus mode": handle_media_focus_mode,
    "deep work mode": handle_media_focus_mode,
    "study mode": handle_media_focus_mode,
    "what should i watch": handle_media_recommendations,
    "recommend a movie": handle_media_recommendations,
    "recommend anime": handle_media_recommendations,
    "recommend music": handle_media_recommendations,
    "lyrics of": handle_media_lyrics,
    "what are the lyrics": handle_media_lyrics,
    "lyrics": handle_media_lyrics,
    "tell me the anime lore of": handle_anime_lore,
    "tell me the anime lore": handle_anime_lore,
    "anime lore of": handle_anime_lore,
    "anime lore": handle_anime_lore,
    "enemy law of": handle_anime_lore,
    "enemy lover of": handle_anime_lore,
    "animal lover of": handle_anime_lore,
    "tv show lore": handle_tv_lore,
    "show lore": handle_tv_lore,
    "tv lore": handle_tv_lore,
    "who plays this": handle_media_companion_lore,
    "what happened in last episode": handle_media_companion_lore,
    "recap episode": handle_media_companion_lore,
    "watch": handle_spotify,
    "stream": handle_spotify,
    "stranger things": handle_spotify,
    "vincenzo": handle_spotify,
    "season": handle_spotify,
    "episode": handle_spotify,
    "on spotify": handle_spotify,
    "playlist": handle_spotify,
    "music": handle_spotify,
    "starboy": handle_spotify,
    "the weeknd": handle_spotify,
    "the weekend": handle_spotify,
    "gaana bajao": handle_spotify,
    "gaana chalao": handle_spotify,
    "gaane sunao": handle_spotify,
    "gana bajao": handle_spotify,
    "gana chalao": handle_spotify,
    "bajao": handle_spotify,
    "chalao": handle_spotify,
    "play": handle_spotify,
    "read book": handle_read_book,
    "read aloud": handle_read_book,
    "narrate book": handle_read_book,
    "next chapter": handle_book_next_chapter,
    "previous chapter": handle_book_prev_chapter,
    "book status": handle_book_status,
    "reading progress": handle_book_status
}
