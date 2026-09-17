"""
F.R.I.D.A.Y. OS 10.0: PROJECT A.E.G.I.S. Lore & Cine-Companion Engine
Integrates battle-tested zero-key public APIs (Jikan/MAL, TVMaze, Lyrics.ovh)
to provide live context, episode recaps, character trivia, and synchronized lyrics.
"""

import requests
import urllib.parse
from typing import Dict, Any, Optional, List

class LoreTelemetryEngine:
    """Provides encyclopedic lore, episode recaps, and live media companion intelligence."""

    def __init__(self):
        self.headers = {"User-Agent": "FRIDAY-OS/10.0 (Stark-AEGIS-Companion)"}

    # =========================================================================
    # 1. ANIME LORE & CHARACTER INTEL (Jikan / MyAnimeList API)
    # =========================================================================
    def get_anime_lore(self, title: str) -> Dict[str, Any]:
        """
        Queries Jikan v4 (MyAnimeList) with automatic resilient fallback to Kitsu.io.
        Zero API keys required.
        """
        # 1. Primary: Jikan v4
        try:
            url = f"https://api.jikan.moe/v4/anime?q={urllib.parse.quote(title)}&limit=1"
            resp = requests.get(url, headers=self.headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                if data:
                    anime = data[0]
                    return {
                        "found": True,
                        "title": anime.get("title"),
                        "title_english": anime.get("title_english") or anime.get("title"),
                        "episodes": anime.get("episodes"),
                        "score": anime.get("score"),
                        "status": anime.get("status"),
                        "synopsis": anime.get("synopsis", "")[:600],
                        "genres": [g.get("name") for g in anime.get("genres", [])],
                        "year": anime.get("year"),
                        "source": "jikan"
                    }
        except Exception:
            pass

        # 2. Resilient Fallback: Kitsu API
        try:
            k_url = f"https://kitsu.io/api/edge/anime?filter[text]={urllib.parse.quote(title)}&page[limit]=1"
            k_headers = {"Accept": "application/vnd.api+json", "User-Agent": "FRIDAY-OS/10.0"}
            k_resp = requests.get(k_url, headers=k_headers, timeout=5)
            if k_resp.status_code == 200:
                k_data = k_resp.json().get("data", [])
                if k_data:
                    attr = k_data[0].get("attributes", {})
                    score = None
                    try:
                        raw_score = float(attr.get("averageRating", 0))
                        score = round(raw_score / 10.0, 2)
                    except Exception:
                        pass
                    return {
                        "found": True,
                        "title": attr.get("canonicalTitle"),
                        "title_english": attr.get("titles", {}).get("en") or attr.get("canonicalTitle"),
                        "episodes": attr.get("episodeCount"),
                        "score": score,
                        "status": attr.get("status"),
                        "synopsis": attr.get("synopsis", "")[:600],
                        "genres": [],
                        "year": attr.get("startDate", "")[:4] if attr.get("startDate") else None,
                        "source": "kitsu"
                    }
        except Exception as e:
            return {"found": False, "error": str(e)}

        return {"found": False}

    def get_anime_characters(self, anime_id: int) -> List[Dict[str, str]]:
        """Fetches top characters and Japanese/English voice actors."""
        try:
            url = f"https://api.jikan.moe/v4/anime/{anime_id}/characters"
            resp = requests.get(url, headers=self.headers, timeout=6)
            if resp.status_code == 200:
                chars = resp.json().get("data", [])[:5]
                results = []
                for c in chars:
                    char_name = c.get("character", {}).get("name", "")
                    va_name = ""
                    vas = c.get("voice_actors", [])
                    if vas:
                        va_name = vas[0].get("person", {}).get("name", "")
                    results.append({"character": char_name, "voice_actor": va_name})
                return results
        except Exception:
            pass
        return []

    # =========================================================================
    # 2. TV SERIES & MOVIE PLOT ENGINE (TVMaze API)
    # =========================================================================
    def get_tv_show_summary(self, show_name: str) -> Dict[str, Any]:
        """
        Queries TVMaze for show synopsis, genres, and premiere date.
        """
        try:
            url = f"https://api.tvmaze.com/singlesearch/shows?q={urllib.parse.quote(show_name)}"
            resp = requests.get(url, headers=self.headers, timeout=6)
            if resp.status_code == 200:
                show = resp.json()
                import re
                clean_summary = re.sub(r"<[^>]+>", "", show.get("summary", "")).strip()
                return {
                    "found": True,
                    "name": show.get("name"),
                    "rating": show.get("rating", {}).get("average"),
                    "genres": show.get("genres", []),
                    "premiered": show.get("premiered"),
                    "summary": clean_summary[:600],
                    "show_id": show.get("id")
                }
        except Exception as e:
            return {"found": False, "error": str(e)}
        return {"found": False}

    def get_episode_recap(self, show_name: str, season: int, episode: int) -> Optional[str]:
        """
        Retrieves the exact plot synopsis for a specific episode for 'Previously on...' recaps.
        """
        show_info = self.get_tv_show_summary(show_name)
        if not show_info.get("found"):
            return None
        show_id = show_info.get("show_id")
        try:
            url = f"https://api.tvmaze.com/shows/{show_id}/episodebynumber?season={season}&number={episode}"
            resp = requests.get(url, headers=self.headers, timeout=6)
            if resp.status_code == 200:
                ep_data = resp.json()
                import re
                recap = re.sub(r"<[^>]+>", "", ep_data.get("summary", "")).strip()
                return recap if recap else f"Episode {episode} of season {season}."
        except Exception:
            pass
        return None

    # =========================================================================
    # 3. LIVE SONG LYRICS (Lyrics.ovh API)
    # =========================================================================
    def get_lyrics(self, artist: str, title: str) -> Optional[str]:
        """Fetches live song lyrics without API keys."""
        try:
            url = f"https://api.lyrics.ovh/v1/{urllib.parse.quote(artist)}/{urllib.parse.quote(title)}"
            resp = requests.get(url, headers=self.headers, timeout=5)
            if resp.status_code == 200:
                lyrics = resp.json().get("lyrics", "")
                return lyrics.strip() if lyrics else None
        except Exception:
            pass
        return None

    # =========================================================================
    # 4. COMPANION LIVE TRIVIA SYNTHESIS
    # =========================================================================
    def synthesize_live_companion_answer(self, media_title: str, user_question: str) -> str:
        """
        Synthesizes a punchy 1-2 sentence spoken answer about what the user is watching.
        """
        # First query Jikan or TVMaze for facts
        anime_info = self.get_anime_lore(media_title)
        tv_info = self.get_tv_show_summary(media_title) if not anime_info.get("found") else {}

        context_data = ""
        if anime_info.get("found"):
            context_data = f"ANIME: {anime_info.get('title')} ({anime_info.get('year')}). Score: {anime_info.get('score')}. Synopsis: {anime_info.get('synopsis')}"
        elif tv_info.get("found"):
            context_data = f"SHOW: {tv_info.get('name')}. Summary: {tv_info.get('summary')}"

        prompt = (
            f"You are F.R.I.D.A.Y., Boss's witty, high-IQ co-engineer and movie companion.\n"
            f"Boss is watching: {media_title}\n"
            f"Reference Data: {context_data}\n"
            f"Boss asks: \"{user_question}\"\n"
            f"Give a punchy, crisp, 1-sentence answer (max 20 words) suitable to be whispered into Boss's ear without interrupting the movie."
        )

        try:
            from core.background_coprocessor import coprocessor
            ok, answer, _ = coprocessor.execute_fast_completion(
                "You are F.R.I.D.A.Y. Cine-Companion. Answer in 1 crisp sentence.",
                prompt,
                max_tokens=50
            )
            if ok and answer:
                return answer.strip()
        except Exception:
            pass

        if anime_info.get("found"):
            return f"That's from {anime_info['title']}, rated {anime_info.get('score')} on MyAnimeList, Boss."
        return f"Checking records on {media_title}, Boss. Standing by."


# Global singleton instance
lore_engine = LoreTelemetryEngine()
