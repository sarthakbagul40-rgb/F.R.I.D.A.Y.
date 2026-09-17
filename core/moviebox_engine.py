"""
========================================================================================
F.R.I.D.A.Y. OS 10.0: MovieBox-Tui Streaming Subsystem
High-Definition Ad-Free Cinema, Series & Anime Engine
Wires directly to local MPV Player (Hardware-Accelerated PIP HUD)
========================================================================================
"""

import os
import shutil
import subprocess
import threading
from typing import Dict, Any, Optional


class MovieBoxEngine:
    """
    Manages MovieBox-Tui integration for ad-free, 1080p Hollywood, Anime, and TV Series playback.
    Replaces broken YouTube search fallbacks with direct streaming scrapers piped to MPV.
    """

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.bin_path = self._locate_moviebox()
        self.mpv_path = self._locate_mpv()

    def _locate_moviebox(self) -> Optional[str]:
        """Locates the compiled moviebox-tui executable."""
        candidates = [
            os.path.join(self.base_dir, "bin", "moviebox", "moviebox-tui.exe"),
            os.path.join(self.base_dir, "bin", "moviebox", "moviebox.exe"),
            shutil.which("moviebox-tui"),
            shutil.which("moviebox"),
        ]
        for c in candidates:
            if c and os.path.exists(c):
                return c
        return None

    def _locate_mpv(self) -> str:
        """Locates the MPV player executable."""
        local_app = os.environ.get("LOCALAPPDATA", "")
        prog_files = os.environ.get("ProgramFiles", "")
        prog_files_x86 = os.environ.get("ProgramFiles(x86)", "")

        candidates = [
            shutil.which("mpv"),
            os.path.join(prog_files, "MPV Player", "mpv.exe"),
            os.path.join(prog_files, "mpv", "mpv.exe"),
            os.path.join(prog_files_x86, "MPV Player", "mpv.exe"),
            os.path.join(local_app, "Programs", "mpv", "mpv.exe"),
        ]
        for c in candidates:
            if c and os.path.exists(c):
                return c
        return "mpv"

    def is_available(self) -> bool:
        """Returns True if moviebox binary exists."""
        return self.bin_path is not None and os.path.exists(self.bin_path)

    def get_status(self) -> Dict[str, Any]:
        """Returns diagnostic status of the MovieBox-Tui subsystem."""
        return {
            "available": self.is_available(),
            "moviebox_path": self.bin_path,
            "mpv_path": self.mpv_path,
            "theme": "catppuccin",
            "player": "mpv"
        }

    def _build_env(self) -> Dict[str, str]:
        """Prepares environment variables for MovieBox-Tui execution."""
        env = os.environ.copy()
        env["MOVIEBOX_PLAYER"] = "mpv"
        if self.mpv_path and os.path.exists(self.mpv_path):
            env["MOVIEBOX_MPV_PATH"] = self.mpv_path
        env["MOVIEBOX_THEME"] = "catppuccin"
        env["MOVIEBOX_LOG"] = "warn"
        return env

    def launch_cinema_tui(self, title: Optional[str] = None, speak_fn=None) -> bool:
        """
        Launches MovieBox-Tui in a dedicated interactive terminal window.
        Allows the user to browse, search, select subtitles, and choose 1080p streams.
        """
        if not self.is_available():
            if speak_fn:
                speak_fn("MovieBox binary is not found, Boss. Falling back to web streamer.")
            return False

        if speak_fn:
            msg = f"Opening Cinema Terminal for {title}, Boss." if title else "Opening Cinema Terminal, Boss."
            threading.Thread(target=speak_fn, args=(msg,), daemon=True).start()

        env = self._build_env()
        bin_file = self.bin_path

        try:
            # Check if Windows Terminal is available
            wt_path = shutil.which("wt")
            if wt_path:
                cmd = [wt_path, "-w", "0", "nt", "--title", "F.R.I.D.A.Y. Cinema (MovieBox)", bin_file]
                subprocess.Popen(cmd, env=env)
            else:
                # Fallback to standard Windows CMD console
                cmd = f'start "F.R.I.D.A.Y. Cinema" "{bin_file}"'
                subprocess.Popen(cmd, shell=True, env=env)
            return True
        except Exception as e:
            print(f"[MovieBoxEngine Error] Failed to launch interactive TUI: {e}")
            return False

    def stream_movie(self, query: str, speak_fn=None) -> bool:
        """
        Primary playback trigger for movies and shows.
        Launches MovieBox with configured MPV player and gives visual/voice feedback.
        """
        return self.launch_cinema_tui(title=query, speak_fn=speak_fn)


# Global singleton instance
moviebox_engine = MovieBoxEngine()
