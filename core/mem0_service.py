"""
Mem0 Dynamic Relational Memory Engine for J.A.R.V.I.S.
Extracts user facts, resolves conflicts, and provides semantic profile recall via OmniRoute & Qdrant.
"""

import os
import sys
import threading
import warnings
from typing import List, Dict, Any, Optional

# Suppress library warnings and telemetry
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", module="qdrant_client")
warnings.filterwarnings("ignore", module="mem0")
os.environ["MEM0_TELEMETRY"] = "false"
os.environ["POSTHOG_DISABLED"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

try:
    from mem0 import Memory
except ImportError:
    Memory = None


class Mem0MemoryEngine:
    """Manages semantic entity memory extraction, conflict resolution, and vector search."""

    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), "mem0_storage")
        self.storage_dir = storage_dir
        self.memory: Optional[Any] = None
        self._init_memory()

    def _init_memory(self):
        """Initializes Mem0 connected to OmniRoute and local FastEmbed vectors."""
        if not Memory:
            return

        config = {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gemini-auto",
                    "openai_base_url": "http://localhost:8081/v1",
                    "api_key": "sk-dummy"
                }
            },
            "embedder": {
                "provider": "fastembed",
                "config": {
                    "model": "BAAI/bge-small-en-v1.5",
                    "embedding_dims": 384
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "jarvis_profile_memories",
                    "path": self.storage_dir,
                    "embedding_model_dims": 384
                }
            },
            "version": "v1.1"
        }
        try:
            self.memory = Memory.from_config(config)
        except Exception:
            self.memory = None

    def search_memories(self, query: str, user_id: str = "boss", top_k: int = 4) -> List[str]:
        """Searches relevant extracted profile memories for a given query."""
        if not self.memory:
            return []
        try:
            res = self.memory.search(query, filters={"user_id": user_id}, limit=top_k)
            memories = []
            for item in res.get("results", []):
                mem_text = item.get("memory", "")
                if mem_text and mem_text not in memories:
                    memories.append(mem_text)
            return memories
        except Exception as e:
            print(f"[Mem0 Search Error]: {e}")
            return []

    def add_conversation_async(self, user_msg: str, assistant_msg: str, user_id: str = "boss"):
        """Asynchronously extracts and updates facts in a background thread to prevent latency."""
        if not self.memory:
            return

        def _bg_worker():
            try:
                # Format conversation for Mem0 fact extraction
                dialogue = f"User: {user_msg}\nFRIDAY: {assistant_msg}"
                self.memory.add(dialogue, user_id=user_id)
            except Exception as e:
                # Silent background failure logging
                pass

        threading.Thread(target=_bg_worker, daemon=True).start()

    def get_all_memories(self, user_id: str = "boss") -> List[str]:
        """Returns all persistent memories for the user."""
        if not self.memory:
            return []
        try:
            res = self.memory.get_all(user_id=user_id)
            return [m.get("memory", "") for m in res.get("results", []) if m.get("memory")]
        except Exception:
            return []

    def reset(self, user_id: str = "boss"):
        """Purges all memories from Mem0 vector database."""
        if not self.memory:
            return
        try:
            if hasattr(self.memory, "reset"):
                self.memory.reset()
            elif hasattr(self.memory, "delete_all"):
                self.memory.delete_all(user_id=user_id)
        except Exception as e:
            print(f"[Mem0 Reset]: {e}")


# Global singleton instance
mem0_engine = Mem0MemoryEngine()

import atexit
def _cleanup_mem0():
    try:
        if mem0_engine and mem0_engine.memory:
            if hasattr(mem0_engine.memory, "vector_store") and hasattr(mem0_engine.memory.vector_store, "client"):
                mem0_engine.memory.vector_store.client.close()
    except Exception:
        pass

atexit.register(_cleanup_mem0)
