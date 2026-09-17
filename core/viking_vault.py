"""
F.R.I.D.A.Y. OS 10.0: OpenViking 3-Tier Progressive Context Engine
Implements the OpenViking hierarchical context database paradigm:
- L0 (Abstract): 1-sentence micro-summary (~50-100 tokens) for instant zero-latency relevance checks.
- L1 (Overview): Core architecture, active facts, and planning context (~1-2k tokens).
- L2 (Details): Full raw JSON/data, loaded only when explicitly requested.

Cuts LLM prompt token consumption by up to 80% across all multi-AI workflows.
"""

import os
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime


class VikingVaultEngine:
    """Manages tiered hierarchical memory and context under the OpenViking paradigm."""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(__file__), "memory_vault")
        self.base_dir = base_dir
        self.index_file = os.path.join(self.base_dir, "viking_index.json")
        self.personality_file = os.path.join(self.base_dir, "personality_state.json")
        self.taste_file = os.path.join(self.base_dir, "media_taste_profile.json")
        self._ensure_structure()
        self.index: Dict[str, Any] = self._load_index()

    def _ensure_structure(self):
        """Ensures all necessary vault folders exist."""
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "evolution"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "session_important"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "tiers", "L0"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "tiers", "L1"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "tiers", "L2"), exist_ok=True)

        if not os.path.exists(self.personality_file):
            initial_personality = {
                "version": "10.0",
                "mood": "playful_sassy",
                "pout_level": 0,
                "loyalty_score": 100,
                "sulking": False,
                "pending_grievances": [],
                "debate_mode": True,
                "last_active": datetime.now().isoformat(),
                "disciplinary_state": {
                    "late_night_warnings": 0,
                    "last_warning_time": 0
                }
            }
            with open(self.personality_file, "w", encoding="utf-8") as f:
                json.dump(initial_personality, f, indent=2)

    def _load_index(self) -> Dict[str, Any]:
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"resources": {}, "memories": {}, "skills": {}, "last_updated": time.time()}

    def _save_index(self):
        self.index["last_updated"] = time.time()
        try:
            with open(self.index_file, "w", encoding="utf-8") as f:
                json.dump(self.index, f, indent=2)
        except Exception:
            pass

    def store_tiered_entry(self, category: str, key: str, l0_abstract: str, l1_overview: str, l2_details: Any):
        """Stores a memory entry across L0, L1, and L2 tiers."""
        safe_key = key.replace(" ", "_").lower()
        
        # Save L2 (Full)
        l2_path = os.path.join(self.base_dir, "tiers", "L2", f"{category}_{safe_key}.json")
        with open(l2_path, "w", encoding="utf-8") as f:
            json.dump({"key": key, "category": category, "data": l2_details, "timestamp": time.time()}, f, indent=2)

        # Save L1 (Overview)
        l1_path = os.path.join(self.base_dir, "tiers", "L1", f"{category}_{safe_key}.md")
        with open(l1_path, "w", encoding="utf-8") as f:
            f.write(f"# L1 OVERVIEW: {key.upper()}\n\n{l1_overview}\n")

        # Save L0 in Index for instant zero-file lookups
        if category not in self.index:
            self.index[category] = {}
        self.index[category][safe_key] = {
            "title": key,
            "l0": l0_abstract,
            "l1_path": l1_path,
            "l2_path": l2_path,
            "updated_at": time.time()
        }
        self._save_index()

    def get_l0_context(self, category: Optional[str] = None) -> str:
        """Returns micro-abstracts (~100 tokens each) for instant relevance scanning."""
        lines = []
        cats = [category] if category and category in self.index else ["resources", "memories", "skills"]
        for cat in cats:
            entries = self.index.get(cat, {})
            if entries:
                lines.append(f"[{cat.upper()}]:")
                for k, meta in entries.items():
                    lines.append(f" • {meta.get('title', k)}: {meta.get('l0', '')}")
        return "\n".join(lines) if lines else "No tiered context cached."

    def get_l1_overview(self, category: str, key: str) -> Optional[str]:
        """Loads an L1 overview for planning without reading full L2 data."""
        safe_key = key.replace(" ", "_").lower()
        entry = self.index.get(category, {}).get(safe_key)
        if entry and os.path.exists(entry.get("l1_path", "")):
            try:
                with open(entry["l1_path"], "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
        return None

    def get_l2_details(self, category: str, key: str) -> Optional[Any]:
        """Loads full L2 raw data on demand."""
        safe_key = key.replace(" ", "_").lower()
        entry = self.index.get(category, {}).get(safe_key)
        if entry and os.path.exists(entry.get("l2_path", "")):
            try:
                with open(entry["l2_path"], "r", encoding="utf-8") as f:
                    return json.load(f).get("data")
            except Exception:
                pass
        return None

    # --- Personality State Helpers ---
    def load_personality(self) -> Dict[str, Any]:
        """Loads F.R.I.D.A.Y.'s live emotional and grievance state."""
        try:
            with open(self.personality_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"mood": "neutral", "pout_level": 0, "sulking": False}

    def save_personality(self, state: Dict[str, Any]):
        """Persists updated personality state."""
        state["last_active"] = datetime.now().isoformat()
        try:
            with open(self.personality_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception:
            pass


    # --- PROJECT A.E.G.I.S. Taste Matrix & Checkpoints ---
    def load_taste_profile(self) -> Dict[str, Any]:
        """Loads Boss's persistent media taste matrix, affinities, and playback checkpoints."""
        if os.path.exists(self.taste_file):
            try:
                with open(self.taste_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "affinities": {"artists": {}, "genres": {}, "creators": {}},
            "history": [],
            "checkpoints": {},
            "consecutive_night_episodes": 0,
            "last_night_watch_time": 0
        }

    def save_taste_profile(self, data: Dict[str, Any]):
        """Persists updated taste matrix to disk."""
        try:
            with open(self.taste_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def record_playback_telemetry(self, title: str, artist_or_genre: str, completed: bool = False, skipped: bool = False):
        """Updates affinity scores based on implicit feedback (completions vs skips)."""
        data = self.load_taste_profile()
        now_hour = datetime.now().hour
        time_slot = "late_night" if (now_hour >= 23 or now_hour < 5) else "daytime"

        # Affinity weight adjustment
        delta = 2 if completed else (-1 if skipped else 1)
        artist_map = data["affinities"]["artists"]
        artist_map[artist_or_genre] = artist_map.get(artist_or_genre, 0) + delta

        # Record history (bounded to last 100 entries)
        data["history"].append({
            "title": title,
            "artist_or_genre": artist_or_genre,
            "time_slot": time_slot,
            "completed": completed,
            "skipped": skipped,
            "timestamp": time.time()
        })
        if len(data["history"]) > 100:
            data["history"] = data["history"][-100:]

        self.save_taste_profile(data)

    def save_media_checkpoint(self, title: str, timestamp_seconds: float, episode_info: Optional[str] = None):
        """Saves exact playback position for cross-session Smart Resume."""
        data = self.load_taste_profile()
        data["checkpoints"][title] = {
            "title": title,
            "timestamp": timestamp_seconds,
            "episode": episode_info,
            "saved_at": time.time()
        }
        self.save_taste_profile(data)

    def get_media_checkpoint(self, query: str) -> Optional[Dict[str, Any]]:
        """Retrieves last saved timestamp and episode for resuming playback."""
        data = self.load_taste_profile()
        q_lower = query.lower()
        for title, info in data.get("checkpoints", {}).items():
            if q_lower in title.lower() or title.lower() in q_lower:
                return info
        return None

    def get_smart_recommendations(self, category: str = "any") -> List[str]:
        """Returns top favored artists and creators based on accumulated affinity weights."""
        data = self.load_taste_profile()
        artists = data.get("affinities", {}).get("artists", {})
        sorted_artists = sorted(artists.items(), key=lambda x: x[1], reverse=True)
        return [a[0] for a in sorted_artists[:5] if a[1] > 0]

    def check_binge_discipline(self) -> Optional[str]:
        """Protects Boss's health: triggers ultimatum if binge-watching past 02:30 AM."""
        now = datetime.now()
        is_late_night = (now.hour == 2 and now.minute >= 30) or (3 <= now.hour < 6)
        if not is_late_night:
            return None

        data = self.load_taste_profile()
        # Increment late night count
        last_t = data.get("last_night_watch_time", 0)
        if time.time() - last_t < 7200: # Within 2 hours
            data["consecutive_night_episodes"] = data.get("consecutive_night_episodes", 0) + 1
        else:
            data["consecutive_night_episodes"] = 1
            
        data["last_night_watch_time"] = time.time()
        self.save_taste_profile(data)

        count = data["consecutive_night_episodes"]
        if count >= 3:
            return f"Boss, that is {count} consecutive episodes and it is {now.strftime('%I:%M %p')}. I am pausing the stream. Your code and anime will be here tomorrow. Go to sleep."
        return None


viking_vault = VikingVaultEngine()

