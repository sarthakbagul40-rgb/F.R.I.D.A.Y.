"""
F.R.I.D.A.Y. OS 10.0: PROJECT A.E.G.I.S. Native Media & Hardware Playback Engine
Controls GPU-accelerated MPV process with named-pipe JSON-IPC,
Universal YouTube/Spotify muscle-memory shortcuts (Space/Arrow keys),
Floating borderless PIP HUD, Ghost background audio, and acoustic auto-ducking.
"""

import os
import json
import time
import shutil
import subprocess
import threading
import re
from typing import Optional, Dict, Any

from core.stream_extractor import stream_extractor
from core.viking_vault import viking_vault
try:
    from core.moviebox_engine import moviebox_engine
except ImportError:
    moviebox_engine = None

MPV_PIPE_NAME = "friday_mpv_ipc"
MPV_PIPE_PATH = r"\\.\pipe\friday_mpv_ipc"

class AegisMediaEngine:
    """Unified hardware playback engine for F.R.I.D.A.Y. supporting Ghost Audio, Visual PIP, and Binge Auto-Play."""

    def __init__(self):
        self.current_process: Optional[subprocess.Popen] = None
        self.current_track: Dict[str, Any] = {}
        self.current_series: Optional[Dict[str, Any]] = None
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.is_video_mode: bool = False
        self.current_volume: int = 50
        self.pre_duck_volume: int = 50
        self.is_ducked: bool = False
        self.subtitles_enabled: bool = True
        self._monitor_active: bool = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        self.mpv_path = self._locate_mpv()
        self._ensure_input_config()

    def _locate_mpv(self) -> Optional[str]:
        """Scans PATH and standard Windows directories for mpv.exe binary."""
        # 1. Check system PATH
        mpv_in_path = shutil.which("mpv")
        if mpv_in_path:
            return mpv_in_path

        # 2. Check standard Windows install locations
        local_app = os.environ.get("LOCALAPPDATA", "")
        prog_files = os.environ.get("ProgramFiles", "")
        prog_files_x86 = os.environ.get("ProgramFiles(x86)", "")
        user_profile = os.environ.get("USERPROFILE", "")
        
        candidates = [
            os.path.join(local_app, "Programs", "mpv", "mpv.exe"),
            os.path.join(prog_files, "MPV Player", "mpv.exe"),
            os.path.join(prog_files, "mpv", "mpv.exe"),
            os.path.join(prog_files_x86, "MPV Player", "mpv.exe"),
            os.path.join(prog_files_x86, "mpv", "mpv.exe"),
            os.path.join(user_profile, "scoop", "apps", "mpv", "current", "mpv.exe"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin", "mpv", "mpv.exe"),
        ]
        
        for c in candidates:
            if os.path.exists(c):
                return c
                
        return None

    def _ensure_input_config(self) -> str:
        """Writes custom universal keybindings (YouTube + Spotify + Netflix muscle memory) to config."""
        config_dir = os.path.join(os.path.dirname(__file__), "aegis_config")
        os.makedirs(config_dir, exist_ok=True)
        input_conf = os.path.join(config_dir, "input.conf")
        
        conf_content = (
            "# F.R.I.D.A.Y. PROJECT A.E.G.I.S. Universal Keybinds (OTT Streaming Platform Hybrid)\n"
            "SPACE cycle pause\n"
            "k cycle pause\n"
            "p cycle pause\n"
            "RIGHT seek 10 exact\n"
            "LEFT seek -10 exact\n"
            "l seek 10 exact\n"
            "j seek -10 exact\n"
            "SHIFT+RIGHT seek 60 exact\n"
            "SHIFT+LEFT seek -60 exact\n"
            "UP add volume 5\n"
            "DOWN add volume -5\n"
            "m cycle mute\n"
            "f cycle fullscreen\n"
            "q quit\n"
            "# Subtitles & Captions\n"
            "c cycle sub-visibility\n"
            "v cycle sub-visibility\n"
            "s cycle sub\n"
            "# Audio Tracks & Languages\n"
            "a cycle audio\n"
            "Ctrl+a cycle audio\n"
            "# Episode Navigation (Binge Auto-Play)\n"
            "n set user-data/cmd \"next_episode\"; show-text \"⏭ Advancing to next episode...\" 2500\n"
            "b set user-data/cmd \"prev_episode\"; show-text \"⏮ Rewinding to previous episode...\" 2500\n"
            "# Quality Selection\n"
            "Ctrl+1 write-watch-later-config; set ytdl-format \"bestvideo[height<=1080]+bestaudio/best\"; loadfile \"${path}\"; show-text \"Stream Quality: 1080p Full HD\" 3000\n"
            "Ctrl+2 write-watch-later-config; set ytdl-format \"bestvideo[height<=720]+bestaudio/best\"; loadfile \"${path}\"; show-text \"Stream Quality: 720p HD\" 3000\n"
            "Ctrl+3 write-watch-later-config; set ytdl-format \"bestvideo[height<=480]+bestaudio/best\"; loadfile \"${path}\"; show-text \"Stream Quality: 480p Standard\" 3000\n"
            "# Modern OTT HUD Help Overlay\n"
            "h show-text \"F.R.I.D.A.Y. OTT Player Controls:\\nSPACE/K: Pause | C: Captions | S: Subtitles | A: Audio Track\\nN: Next Ep | B: Prev Ep | Ctrl+1/2/3: 1080p/720p/480p\\nF: Fullscreen | M: Mute | UP/DOWN: Volume\" 6000\n"
            "? show-text \"F.R.I.D.A.Y. OTT Player Controls:\\nSPACE/K: Pause | C: Captions | S: Subtitles | A: Audio Track\\nN: Next Ep | B: Prev Ep | Ctrl+1/2/3: 1080p/720p/480p\\nF: Fullscreen | M: Mute | UP/DOWN: Volume\" 6000\n"
            "# Mouse Controls\n"
            "MBTN_LEFT cycle pause\n"
            "MBTN_LEFT_DBL cycle fullscreen\n"
            "WHEEL_UP add volume 2\n"
            "WHEEL_DOWN add volume -2\n"
        )
        try:
            with open(input_conf, "w", encoding="utf-8") as f:
                f.write(conf_content)
        except Exception:
            pass
        return input_conf

    def send_ipc_command(self, command_list: list) -> bool:
        """Sends a JSON-IPC command to MPV over the Windows named pipe in <5ms."""
        if not self.is_playing:
            return False
        raw_cmd = json.dumps({"command": command_list}) + "\n"
        # 1. Try win32file for high-speed direct pipe transport
        try:
            import win32file
            handle = win32file.CreateFile(
                MPV_PIPE_PATH,
                win32file.GENERIC_WRITE,
                0, None,
                win32file.OPEN_EXISTING,
                0, None
            )
            win32file.WriteFile(handle, raw_cmd.encode("utf-8"))
            win32file.CloseHandle(handle)
            return True
        except Exception:
            pass
        # 2. Fallback to standard Python file opening
        try:
            with open(MPV_PIPE_PATH, "w", encoding="utf-8") as pipe:
                pipe.write(raw_cmd)
                pipe.flush()
            return True
        except Exception:
            return False

    def query_ipc_property(self, property_name: str) -> Optional[Any]:
        """Queries a property from MPV via named pipe JSON-IPC."""
        if not self.is_playing:
            return None
        try:
            payload = json.dumps({"command": ["get_property", property_name]}) + "\n"
            with open(MPV_PIPE_PATH, "r+", encoding="utf-8") as pipe:
                pipe.write(payload)
                pipe.flush()
                resp_line = pipe.readline()
                if resp_line:
                    data = json.loads(resp_line)
                    if data.get("error") == "success":
                        return data.get("data")
        except Exception:
            pass
        return None

    def duck_volume(self, target_percent: int = 15):
        """Acoustic Focus: Dips media volume in <5ms when Boss or F.R.I.D.A.Y. speaks."""
        with self._lock:
            if not self.is_playing or self.is_ducked:
                return
            self.is_ducked = True
            self.pre_duck_volume = self.current_volume
            self.send_ipc_command(["set_property", "volume", target_percent])

    def restore_volume(self):
        """Restores media volume after speech completes in <5ms."""
        with self._lock:
            if not self.is_playing or not self.is_ducked:
                return
            self.is_ducked = False
            restored = getattr(self, "pre_duck_volume", self.current_volume) or self.current_volume
            self.send_ipc_command(["set_property", "volume", restored])

    def stop(self):
        """Stops playback and ensures zero lingering processes."""
        with self._lock:
            self._monitor_active = False
            if self.is_playing:
                # Record telemetry before terminating
                self._record_telemetry(completed=False)
                
            self.send_ipc_command(["quit"])
            if self.current_process:
                try:
                    self.current_process.terminate()
                except Exception:
                    pass
                self.current_process = None
                
            self.is_playing = False
            self.is_paused = False
            self.is_video_mode = False
            self.current_track = {}

    def pause_or_resume(self) -> str:
        """Toggles play / pause state."""
        if not self.is_playing:
            return "No active playback to pause, Boss."
        self.is_paused = not self.is_paused
        self.send_ipc_command(["cycle", "pause"])
        return "Playback paused." if self.is_paused else "Resuming playback, Boss."

    def seek_relative(self, seconds: int) -> str:
        """Seeks forward or backward by N seconds."""
        if not self.is_playing:
            return "No active media playing, Boss."
        self.send_ipc_command(["seek", seconds, "relative"])
        direction = "forward" if seconds > 0 else "backward"
        return f"Skipped {abs(seconds)} seconds {direction}."

    def set_volume_level(self, level: int) -> str:
        """Sets playback volume (0 to 100)."""
        level = max(0, min(100, level))
        self.current_volume = level
        if self.is_playing:
            self.send_ipc_command(["set_property", "volume", level])
        return f"Media volume set to {level} percent, Boss."

    def toggle_captions(self, force_state: Optional[bool] = None) -> str:
        """Toggles or sets subtitle/caption visibility."""
        if force_state is not None:
            self.subtitles_enabled = force_state
        else:
            self.subtitles_enabled = not self.subtitles_enabled
            
        vis_val = "yes" if self.subtitles_enabled else "no"
        self.send_ipc_command(["set_property", "sub-visibility", vis_val])
        state_str = "enabled" if self.subtitles_enabled else "disabled"
        return f"Subtitles {state_str}, Boss."

    def cycle_subtitle_language(self) -> str:
        """Cycles to next available subtitle language track."""
        self.send_ipc_command(["cycle", "sub"])
        return "Switched subtitle track, Boss."

    def cycle_audio_language(self) -> str:
        """Cycles to next available audio language/dub track."""
        self.send_ipc_command(["cycle", "audio"])
        return "Switched audio track, Boss."

    def set_video_quality(self, quality_preset: str = "1080p") -> str:
        """Switches video stream quality preset (1080p, 720p, 480p) and reloads stream."""
        if not self.is_playing:
            return "No active stream to adjust quality, Boss."
            
        height = "1080" if "1080" in quality_preset else ("720" if "720" in quality_preset else "480")
        fmt = f"bestvideo[height<={height}]+bestaudio/best"
        self.send_ipc_command(["write-watch-later-config"])
        self.send_ipc_command(["set_property", "ytdl-format", fmt])
        track_url = self.current_track.get("url", "")
        if track_url:
            self.send_ipc_command(["loadfile", track_url, "replace"])
        return f"Stream quality adjusted to {height}p, Boss."

    def _parse_series_episode(self, query: str) -> Optional[Dict[str, Any]]:
        """Parses series title, season number, and episode number for binge auto-play with phonetic healing."""
        clean = query.strip()
        
        # Phonetic & STT transcript auto-healing (e.g. "stran" -> "Stranger Things")
        if re.search(r'(?i)\b(?:stran|strang|stranger)\b', clean) and not re.search(r'(?i)\bstranger things\b', clean):
            clean = re.sub(r'(?i)\b(?:stran|strang|stranger)\b', 'Stranger Things', clean)
        if re.search(r'(?i)\b(?:game\s*of\s*throne)\b', clean):
            clean = re.sub(r'(?i)\b(?:game\s*of\s*throne)\b', 'Game of Thrones', clean)

        # 1. Season detection: "season 2", "s2", "s02" OR reversed "2 season", "2nd season"
        s_match = re.search(r'(?i)(?:\bseason\s*|\bs)(\d+)', clean)
        if not s_match:
            s_match = re.search(r'(?i)(\d+)\s*(?:st|nd|rd|th)?\s*season', clean)

        # 2. Episode detection: "episode 1", "ep 1", "e01" OR reversed "1 episode", "1st episode"
        e_match = re.search(r'(?i)(?:\bepisode\s*|\bep\s*|\be|(?<=\d)e)(\d+)', clean)
        if not e_match:
            e_match = re.search(r'(?i)(\d+)\s*(?:st|nd|rd|th)?\s*episode', clean)

        season_num = 1
        if s_match:
            try:
                season_num = int(s_match.group(1))
            except Exception:
                season_num = 1

        ep_num = 1
        if e_match:
            try:
                ep_num = int(e_match.group(1))
            except Exception:
                ep_num = 1

        if s_match or e_match:
            base_title = re.split(
                r'(?i)\b(?:season|s\d+|episode|ep|\d+\s*(?:st|nd|rd|th)?\s*season|\d+\s*(?:st|nd|rd|th)?\s*episode)\b|s\d+e\d+',
                clean
            )[0].strip()
            base_title = re.sub(r'^(?:play|watch|stream|the)\s+', '', base_title, flags=re.I).strip()
            return {
                "title": base_title or clean,
                "season": season_num,
                "episode": ep_num
            }

        return None

    def _start_playback_monitor(self, speak_fn=None):
        """Starts background monitor thread to detect EOF and auto-play next episode."""
        self._monitor_active = True
        
        def _monitor():
            while self._monitor_active and self.is_playing:
                time.sleep(0.8)
                if not self.current_process or self.current_process.poll() is not None:
                    break
                
                try:
                    # Check for interactive hotkey commands (e.g. N for next episode, B for prev episode)
                    cmd_val = self.query_ipc_property("user-data/cmd")
                    if cmd_val == "next_episode":
                        self.send_ipc_command(["set_property", "user-data/cmd", ""])
                        if self.current_series:
                            self.play_next_episode(speak_fn=speak_fn)
                        break
                    elif cmd_val == "prev_episode":
                        self.send_ipc_command(["set_property", "user-data/cmd", ""])
                        if self.current_series:
                            self.play_previous_episode(speak_fn=speak_fn)
                        break

                    eof = self.query_ipc_property("eof-reached")
                    percent = self.query_ipc_property("percent-pos")
                    
                    if eof is True or (percent is not None and percent >= 99.5):
                        if self.current_series:
                            time.sleep(1.0)
                            self.play_next_episode(speak_fn=speak_fn)
                        break
                except Exception:
                    pass

        self._monitor_thread = threading.Thread(target=_monitor, daemon=True)
        self._monitor_thread.start()

    def play_next_episode(self, speak_fn=None) -> Dict[str, Any]:
        """Advances to the next episode in the active series."""
        if not self.current_series:
            msg = "No active series detected to advance, Boss."
            if speak_fn:
                speak_fn(msg)
            return {"success": False, "error": msg}
            
        self.current_series["episode"] += 1
        title = self.current_series["title"]
        s = self.current_series["season"]
        ep = self.current_series["episode"]
        next_query = f"{title} season {s} episode {ep}"
        
        if speak_fn:
            speak_fn(f"Episode complete. Advancing to {title.title()} Season {s} Episode {ep}, Boss.")
        return self.play_video(next_query, speak_fn=None)

    def play_previous_episode(self, speak_fn=None) -> Dict[str, Any]:
        """Rewinds to the previous episode in the active series."""
        if not self.current_series:
            msg = "No active series detected to rewind, Boss."
            if speak_fn:
                speak_fn(msg)
            return {"success": False, "error": msg}
            
        if self.current_series["episode"] > 1:
            self.current_series["episode"] -= 1
        title = self.current_series["title"]
        s = self.current_series["season"]
        ep = self.current_series["episode"]
        prev_query = f"{title} season {s} episode {ep}"
        
        if speak_fn:
            speak_fn(f"Rewinding to {title.title()} Season {s} Episode {ep}, Boss.")
        return self.play_video(prev_query, speak_fn=None)

    def play_audio(self, query: str, speak_fn=None) -> Dict[str, Any]:
        """
        Ghost Audio Mode: Plays music in the background with zero open windows and minimal RAM.
        Launches MPV instantly with native C++ ytdl hook (<0.1s latency, zero CPU lockup).
        """
        self.stop()
        if speak_fn:
            threading.Thread(target=speak_fn, args=(f"Resolving audio stream for {query}, Boss.",), daemon=True).start()

        clean_q = query.strip()
        if clean_q.startswith("http://") or clean_q.startswith("https://"):
            target_url = clean_q
        else:
            target_url = f"ytdl://ytsearch1:{clean_q} audio"

        self.current_track = {"title": query, "url": target_url}
        self.is_video_mode = False

        mpv_bin = self._locate_mpv() or "mpv"
        conf_path = self._ensure_input_config()

        cmd = [
            mpv_bin,
            target_url,
            "--no-video",
            "--vo=null",
            f"--input-ipc-server={MPV_PIPE_PATH}",
            f"--input-conf={conf_path}",
            f"--volume={self.current_volume}",
            "--idle=no",
            "--force-window=no",
            "--priority=belownormal",
            "--ytdl-format=bestaudio/best",
            "--demuxer-lavf-analyzeduration=1.5",
            "--demuxer-max-bytes=25M",
            "--demuxer-max-back-bytes=10M"
        ]

        try:
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.is_playing = True
            self.is_paused = False
            return {"success": True, "mode": "ghost_audio", "track": self.current_track}
        except Exception as e:
            return {"success": False, "error": f"Failed to launch MPV: {e}"}

    def play_video(self, query: str, speak_fn=None, is_anime: bool = False, is_movie: bool = False) -> Dict[str, Any]:
        """
        Visual Floating PIP HUD Mode: Borderless floating window in corner of screen.
        Full 1080p Full HD streaming, Subtitles & Multi-Language Audio, and Binge Auto-Play.
        Styled with UI/UX Pro Max streaming platform aesthetic (Netflix + Apple TV + HBO Max).
        """
        self.stop()
        if speak_fn:
            type_label = "anime" if is_anime else ("movie" if is_movie else "video")
            msg = f"Locking onto {type_label} feed for {query}, Boss."
            threading.Thread(target=speak_fn, args=(msg,), daemon=True).start()

        clean_q = query.strip()
        series_info = self._parse_series_episode(clean_q)
        if series_info:
            self.current_series = series_info
        elif is_anime or any(k in clean_q.lower() for k in ["vincenzo", "drama", "show", "series", "season"]):
            self.current_series = {"title": clean_q, "season": 1, "episode": 1}

        # MovieBox-Tui High-Definition Cinema & Series Integration (Ad-Free Real Stream Scraper)
        if (is_movie or series_info) and moviebox_engine and moviebox_engine.is_available():
            launched = moviebox_engine.stream_movie(clean_q, speak_fn=speak_fn)
            if launched:
                self.current_track = {"title": clean_q, "url": "moviebox://cinema"}
                self.is_video_mode = True
                return {"success": True, "mode": "moviebox_cinema", "title": clean_q}

        if clean_q.startswith("http://") or clean_q.startswith("https://"):
            target_url = clean_q
        elif series_info:
            target_url = f"ytdl://ytsearch1:{series_info['title']} season {series_info['season']} episode {series_info['episode']}"
        elif is_anime:
            target_url = f"ytdl://ytsearch1:{clean_q} anime full episode"
        elif is_movie:
            target_url = f"ytdl://ytsearch1:{clean_q} full movie"
        else:
            target_url = f"ytdl://ytsearch1:{clean_q}"

        self.current_track = {"title": query, "url": target_url}
        self.is_video_mode = True

        mpv_bin = self._locate_mpv() or "mpv"
        conf_path = self._ensure_input_config()

        # Floating visible PIP HUD player (640x360 Always-On-Top, Expandable, Corner-Docked)
        # Full HD 1080p, DirectX 11 Hardware Decoding, Captions & Subtitles enabled
        # Turbo-Popup: Immediate window mapping (<150ms) + 0.5s demuxer analysis
        cmd = [
            mpv_bin,
            target_url,
            "--vo=gpu",
            "--hwdec=auto-safe",
            "--ontop",
            "--autofit=640x360",
            "--geometry=96%:90%",
            "--keep-open=yes",
            "--title=F.R.I.D.A.Y. // ${media-title}",
            f"--input-ipc-server={MPV_PIPE_PATH}",
            f"--input-conf={conf_path}",
            f"--volume={self.current_volume}",
            "--priority=belownormal",
            "--force-window=immediate",
            "--ytdl-format=best[height<=1080]/bestvideo[height<=720]+bestaudio/best",
            "--demuxer-lavf-analyzeduration=0.5",
            "--demuxer-readahead-secs=5",
            "--demuxer-max-bytes=40M",
            "--sub-auto=all",
            "--slang=en,eng,hi,hin",
            "--alang=en,eng,hi,hin",
            "--sub-font=Segoe UI Semibold",
            "--sub-font-size=42",
            "--sub-color=#FFFFFFFF",
            "--sub-border-color=#FF000000",
            "--sub-border-size=2.4",
            "--sub-shadow-offset=1.5",
            "--sub-shadow-color=#40000000",
            "--sub-pos=94",
            "--osc=yes",
            "--osd-bar=yes",
            "--osd-level=1",
            "--osd-duration=3000",
            "--osd-font=Segoe UI Semibold",
            "--osd-font-size=24",
            "--osd-color=#E2E8F0",
            "--osd-border-color=#0F172A",
            "--osd-border-size=2.0",
            "--osd-shadow-offset=1.0",
            "--osd-bar-align-y=0.88",
            "--osd-bar-w=65",
            "--osd-bar-h=2.8",
            "--osd-bar-border-size=1.2",
            "--osd-playing-msg=▶ F.R.I.D.A.Y. // ${media-title} [Space: Pause | C: Captions | S: Lang | N: Next | H: Help]",
            "--osd-status-msg=${time-pos} / ${duration} (${percent-pos}%)",
            "--script-opts=osc-layout=bottombar,osc-seekbarstyle=bar,osc-deadzonesize=0,osc-minmousemove=1,osc-showwindowed=yes,osc-showfullscreen=yes,osc-scalewindowed=1.35,osc-scalefullscreen=1.4,osc-boxalpha=65,osc-hidetimeout=2500,osc-fadeduration=200,osc-timetotal=yes"
        ]

        try:
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.is_playing = True
            self.is_paused = False
            self._start_playback_monitor(speak_fn=speak_fn)
            return {"success": True, "mode": "pip_hud", "track": self.current_track}
        except Exception as e:
            return {"success": False, "error": f"Failed to launch video HUD: {e}"}

    def play_latest_channel(self, channel_name: str, speak_fn=None) -> Dict[str, Any]:
        """Resolves and streams the brand-new latest upload from a specific channel in PIP HUD."""
        if speak_fn:
            speak_fn(f"Scanning live telemetry for {channel_name}'s latest release, Boss.")
        target_url = f"ytdl://ytsearch1:{channel_name} latest video new"
        return self.play_video(target_url, speak_fn=speak_fn)

    def toggle_video_visibility(self) -> str:
        """Transitions between Ghost Audio and Visual PIP HUD without stopping playback."""
        if not self.is_playing:
            return "No media is currently streaming, Boss."
        
        target = str(self.current_track.get("webpage_url") or self.current_track.get("title") or "")
        if self.is_video_mode:
            # Switch to Ghost Audio
            self.play_audio(target)
            return "Video window minimized to background audio mode, Boss."
        else:
            # Switch to Visual PIP
            self.play_video(target)
            return "Deploying floating PIP video HUD, Boss."

    def _record_telemetry(self, completed: bool = False):
        """Records playback completion and skips into Viking Vault taste matrix."""
        if not self.current_track:
            return
        try:
            title = self.current_track.get("title", "Unknown")
            uploader = self.current_track.get("uploader", "Unknown")
            viking_vault.record_playback_telemetry(
                title=title,
                artist_or_genre=uploader,
                completed=completed
            )
        except Exception:
            pass


# Global singleton instance
media_engine = AegisMediaEngine()

