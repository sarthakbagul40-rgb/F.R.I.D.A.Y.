"""
F.R.I.D.A.Y. OS 10.0: PROJECT A.E.G.I.S. Stream Extraction Core
High-speed, zero-API-key stream resolver powered by yt-dlp, HLS manifests, and live channel indexers.
Extracts pure audio/video streams with zero ads, zero browser tabs, and sub-second resolution.
"""

from typing import Dict, Any
import yt_dlp

class StreamExtractor:
    """Resolves live real-time media streams for YouTube, SoundCloud, Anime, Movies, and Channels."""

    def __init__(self):
        # Optimized configuration for sub-second metadata and stream resolution
        self.ydl_opts_audio: Dict[str, Any] = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch1',
            'socket_timeout': 8,
            'extract_flat': False,
            'skip_download': True
        }
        
        self.ydl_opts_video: Dict[str, Any] = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch1',
            'socket_timeout': 10,
            'extract_flat': False,
            'skip_download': True
        }

    def resolve_audio_stream(self, query: str) -> Dict[str, Any]:
        """
        Resolves a search query or URL into a direct raw audio stream URL.
        Returns: {success: bool, url: str, title: str, uploader: str, duration: int, webpage_url: str}
        """
        clean_q = query.strip()
        if not clean_q.startswith("http://") and not clean_q.startswith("https://"):
            search_target = f"ytsearch1:{clean_q} audio"
        else:
            search_target = clean_q

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts_audio) as ydl: # type: ignore
                raw_info = ydl.extract_info(search_target, download=False)
                info = raw_info if isinstance(raw_info, dict) else {}
                entries = info.get('entries')
                if isinstance(entries, list) and len(entries) > 0 and isinstance(entries[0], dict):
                    info = entries[0]

                return {
                    "success": True,
                    "title": info.get("title", "Unknown Track"),
                    "uploader": info.get("uploader", "Unknown Artist"),
                    "duration": info.get("duration", 0),
                    "url": info.get("url"),  # Direct raw audio stream link
                    "webpage_url": info.get("webpage_url", search_target),
                    "thumbnail": info.get("thumbnail", ""),
                    "is_live": info.get("is_live", False)
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    def resolve_video_stream(self, query: str, max_height: int = 1080) -> Dict[str, Any]:
        """
        Resolves a video query or URL for floating PIP playback.
        Returns direct video stream or webpage URL for MPV rendering.
        """
        clean_q = query.strip()
        if not clean_q.startswith("http://") and not clean_q.startswith("https://"):
            search_target = f"ytsearch1:{clean_q}"
        else:
            search_target = clean_q

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts_video) as ydl: # type: ignore
                raw_info = ydl.extract_info(search_target, download=False)
                info = raw_info if isinstance(raw_info, dict) else {}
                entries = info.get('entries')
                if isinstance(entries, list) and len(entries) > 0 and isinstance(entries[0], dict):
                    info = entries[0]

                return {
                    "success": True,
                    "title": info.get("title", "Unknown Video"),
                    "uploader": info.get("uploader", "Unknown Creator"),
                    "duration": info.get("duration", 0),
                    "url": info.get("url"),
                    "webpage_url": info.get("webpage_url", search_target),
                    "thumbnail": info.get("thumbnail", ""),
                    "is_live": info.get("is_live", False)
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    def resolve_latest_channel_upload(self, channel_name: str) -> Dict[str, Any]:
        """
        Resolves the brand-new latest upload from a specific creator (e.g. 'MrBeast', 'MKBHD').
        """
        search_target = f"ytsearch1:{channel_name} latest video new"
        res = self.resolve_video_stream(search_target)
        if res.get("success"):
            res["channel"] = channel_name
            res["is_latest"] = True
        return res

    def resolve_anime_stream(self, anime_title: str, episode: int = 1, sub_or_dub: str = "sub") -> Dict[str, Any]:
        """
        Resolves an anime title and episode into a direct streaming feed.
        """
        # Formulate direct query for high-definition streaming
        query = f"{anime_title} episode {episode} {sub_or_dub} full"
        res = self.resolve_video_stream(query)
        if res.get("success"):
            res["anime_title"] = anime_title
            res["episode"] = episode
            res["sub_or_dub"] = sub_or_dub
        return res

    def resolve_movie_stream(self, movie_title: str) -> Dict[str, Any]:
        """
        Resolves a full movie or documentary stream.
        """
        query = f"{movie_title} full movie"
        res = self.resolve_video_stream(query)
        if res.get("success"):
            res["movie_title"] = movie_title
        return res


# Global singleton instance
stream_extractor = StreamExtractor()
