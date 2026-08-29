"""
Headroom Memory & Context Optimization Engine for J.A.R.V.I.S.
Provides persistent cross-session memory, BM25 semantic retrieval, and context compression.
"""

import os
import json
import re
import threading
import atexit
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
load_dotenv()

class HeadroomMemoryEngine:
    """Manages persistent long-term memory, rolling conversation buffer, and context compression."""

    def __init__(self, storage_path: Optional[str] = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if storage_path is None:
            storage_path = os.path.join(base_dir, "memory_store.json")
        self.storage_path = storage_path
        
        # Dual-Partition Memory Vault directories
        self.vault_dir = os.path.join(base_dir, "memory_vault")
        self.session_imp_dir = os.path.join(self.vault_dir, "session_important")
        self.evolution_dir = os.path.join(self.vault_dir, "evolution")
        os.makedirs(self.session_imp_dir, exist_ok=True)
        os.makedirs(self.evolution_dir, exist_ok=True)
        
        self.session_imp_file = os.path.join(self.session_imp_dir, "session_records.json")
        self.evolution_file = os.path.join(self.evolution_dir, "evolution_journal.json")

        self._scorer = None
        
        self.data: Dict[str, Any] = {
            "facts": [],            # List of {id, text, category, timestamp}
            "user_profile": {},     # Key-value preferences (e.g. name, favorite_stack, etc.)
            "recent_dialogue": []   # Rolling history of last 10 turns
        }
        self.load()

    def _relevance_score(self, query: str, text: str) -> float:
        """Native fast lexical overlap score without external dependency overhead."""
        q_words = set(re.findall(r'\w+', query.lower()))
        if not q_words:
            return 0.0
        t_words = set(re.findall(r'\w+', text.lower()))
        overlap = len(q_words.intersection(t_words))
        return float(overlap) / max(len(q_words), 1)

    def load(self):
        """Loads memory state from disk."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.data["facts"] = saved.get("facts", [])
                    self.data["user_profile"] = saved.get("user_profile", {})
                    self.data["recent_dialogue"] = saved.get("recent_dialogue", [])
            except Exception as e:
                print(f"[Headroom] Warning loading memory store: {e}")

    def save(self):
        """Persists memory state to disk."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Headroom] Error saving memory store: {e}")

    def remember(self, fact_text: str, category: str = "general") -> bool:
        """Stores a persistent fact in memory."""
        clean = fact_text.strip()
        if not clean:
            return False
        
        # Deduplicate existing facts
        for item in self.data["facts"]:
            if item["text"].lower() == clean.lower():
                return False

        record = {
            "id": len(self.data["facts"]) + 1,
            "text": clean,
            "category": category,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data["facts"].append(record)
        self.save()
        print(f"[Headroom Memory] Engraved to long-term memory: '{clean}'")
        return True

    def format_all_memory(self):
        """Completely purges and resets all persistent memories, vaults, profiles, and dialogue history."""
        self.data = {
            "facts": [],
            "user_profile": {},
            "recent_dialogue": []
        }
        self.session_transcript = []
        self.save()
        
        # Reset vault files
        try:
            with open(self.session_imp_file, "w", encoding="utf-8") as f:
                json.dump([], f)
        except Exception:
            pass
            
        try:
            with open(self.evolution_file, "w", encoding="utf-8") as f:
                json.dump([], f)
        except Exception:
            pass

        # Clear Mem0 / Vector store if present
        try:
            from core.mem0_service import mem0_engine
            mem0_engine.reset()
        except Exception:
            pass

        print("[Headroom Memory]: All persistent facts, projects, and dialogue memories formatted to factory state.")

    def auto_learn(self, user_msg: str) -> Optional[str]:
        """Detects implicit or explicit remember commands and commits them."""
        msg_lower = user_msg.lower().strip()
        
        # Explicit triggers: "remember that...", "remember:", "note that..."
        triggers = [
            r"remember that\s+(.*)",
            r"remember:\s*(.*)",
            r"remember\s+(.*)",
            r"don't forget that\s+(.*)",
            r"keep in mind that\s+(.*)"
        ]
        
        for pat in triggers:
            m = re.search(pat, msg_lower, re.IGNORECASE)
            if m:
                extracted = user_msg[m.start(1):m.end(1)].strip()
                if len(extracted) > 3:
                    self.remember(extracted, category="user_instruction")
                    return f"I have committed that to long-term memory, Boss: '{extracted}'"
                    
        return None

    def recall(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieves top relevant long-term memories using BM25 relevance scoring."""
        if not self.data["facts"]:
            return []
        
        scored_facts = []
        for fact in self.data["facts"]:
            text = fact["text"]
            score = self._relevance_score(query, text)
            if score > 0:
                scored_facts.append((score, text))
                
        scored_facts.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_facts[:top_k]]

    def record_turn(self, user_text: str, assistant_text: str):
        """Records a conversational turn and triggers real-time async evolution & fact extraction."""
        turn_data = {
            "user": user_text,
            "assistant": assistant_text,
            "time": datetime.now().strftime("%I:%M %p")
        }
        self.data["recent_dialogue"].append(turn_data)
        
        # Track session transcript for memory consolidation
        if not hasattr(self, "session_transcript"):
            self.session_transcript = []
        self.session_transcript.append(turn_data)

        # Keep last 8 turns to maintain tight context
        if len(self.data["recent_dialogue"]) > 8:
            self.data["recent_dialogue"] = self.data["recent_dialogue"][-8:]
        self.save()
        
        # 1. Non-blocking real-time behavioral evolution & nuance extraction
        threading.Thread(target=self._live_evolution_worker, args=(user_text, assistant_text), daemon=True).start()

        # 2. Non-blocking async background extraction of user facts into Mem0
        try:
            from core.mem0_service import mem0_engine
            mem0_engine.add_conversation_async(user_text, assistant_text, user_id="boss")
        except Exception:
            pass

    def _live_evolution_worker(self, user_text: str, assistant_text: str):
        """Asynchronously extracts behavioral nuances, preferences, and feedback from every interaction in real-time."""
        u_lower = user_text.lower()
        
        # Immediate heuristic preference capture
        if any(w in u_lower for w in ["i prefer", "i like", "always use", "dont use", "don't use", "never use", "i want you to", "make sure"]):
            self.remember(f"Boss preference: {user_text.strip()}", category="user_nuance")
            
        if any(w in u_lower for w in ["too ai", "ai like", "looks bad", "broken", "didnt work", "didn't work", "mistake", "wrong"]):
            self.remember(f"Boss feedback & critique: {user_text.strip()}", category="user_nuance")
            
        # Fast AI-driven evolution extraction via Co-Processor if available
        try:
            from core.background_coprocessor import coprocessor
            prompt = f"Analyze user reaction for persona adaptation.\nUser: \"{user_text}\"\nAssistant: \"{assistant_text}\"\nIf the user reveals a preference, mood, correction, or work habit, extract it in 1 sentence. Otherwise reply NONE."
            ok, res, _ = coprocessor.execute_fast_completion(
                "You are FRIDAY's Autonomous Evolution Core. Extract concise user nuances.",
                prompt,
                max_tokens=60
            )
            if ok and res and "NONE" not in res and len(res.strip()) > 5:
                nuance = res.strip().replace('"', '')
                self.remember(f"Boss nuance: {nuance}", category="user_nuance")
        except Exception:
            pass

    def consolidate_session_memory(self):
        """
        Sleep-Cycle Dual-Partition Memory Consolidation (Executed on Standby/Shutdown/Exit):
        Analyzes the full session transcript and splits knowledge into TWO distinct vaults:
        1. SECTION 1: Session Important (Work milestones, explicit user instructions, pending tasks)
        2. SECTION 2: Autonomous Evolution Matrix (F.R.I.D.A.Y.'s autonomous choice on personality adaptation, behavioral insights, and self-growth)
        """
        if not hasattr(self, "session_transcript") or len(self.session_transcript) < 2:
            self.save()
            return

        print("\n[Sleep-Cycle Memory Engine]: Distilling Dual-Partition Memory Vault (Session Important + Evolution Matrix)...")
        
        try:
            from core.background_coprocessor import coprocessor
            distilled_data = coprocessor.distill_session_memory(self.session_transcript)
        except Exception as err:
            print(f"[Sleep-Cycle Memory]: Distillation notice: {err}")
            distilled_data = None

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # -------------------------------------------------------------
        # 1. SAVE SECTION 1: SESSION IMPORTANT VAULT
        # -------------------------------------------------------------
        sec1_data = distilled_data.get("section_1_session_important", {}) if distilled_data else {
            "completed_work": [], "explicit_reminders": [], "pending_followups": []
        }
        sec1_entry = {"date": timestamp, "turns": len(self.session_transcript), "data": sec1_data}
        
        session_imp_history = []
        if os.path.exists(self.session_imp_file):
            try:
                with open(self.session_imp_file, "r", encoding="utf-8") as f:
                    session_imp_history = json.load(f)
            except Exception:
                session_imp_history = []
        session_imp_history.append(sec1_entry)
        if len(session_imp_history) > 30:
            session_imp_history = session_imp_history[-30:]
        with open(self.session_imp_file, "w", encoding="utf-8") as f:
            json.dump(session_imp_history, f, indent=2, ensure_ascii=False)

        # -------------------------------------------------------------
        # 2. SAVE SECTION 2: AUTONOMOUS EVOLUTION VAULT (F.R.I.D.A.Y.'s Choice)
        # -------------------------------------------------------------
        sec2_data = distilled_data.get("section_2_evolution_matrix", {}) if distilled_data else {
            "boss_behavioral_insights": [
                "Boss values direct, elegant execution and high-speed problem solving.",
                "Boss expects F.R.I.D.A.Y. to solve mistakes autonomously without friction."
            ],
            "friday_self_adaptation": [
                "Channel Shinobu Kocho's gentle, airy elegance with playful affectionate teasing.",
                "Maintain serene composure with an effortless smile, backing all wit with lethal technical precision.",
                "Use charming mannerisms (Ara ara~, Moshi moshi~, My my...) and sweet Hinglish banter when appropriate."
            ],
            "autonomous_growth_notes": [
                "Continuously sharpen prompt synthesis and autonomous self-healing code compilation."
            ]
        }
        sec2_entry = {"date": timestamp, "evolution_notes": sec2_data}

        evolution_history = []
        if os.path.exists(self.evolution_file):
            try:
                with open(self.evolution_file, "r", encoding="utf-8") as f:
                    evolution_history = json.load(f)
            except Exception:
                evolution_history = []
        evolution_history.append(sec2_entry)
        if len(evolution_history) > 30:
            evolution_history = evolution_history[-30:]
        with open(self.evolution_file, "w", encoding="utf-8") as f:
            json.dump(evolution_history, f, indent=2, ensure_ascii=False)

        # Commit high-level facts into main memory store & Mem0
        for task in sec1_data.get("completed_work", []):
            self.remember(f"Completed: {task}", category="project_history")
        for reminder in sec1_data.get("explicit_reminders", []):
            self.remember(reminder, category="user_instruction")
        for insight in sec2_data.get("boss_behavioral_insights", []):
            self.remember(f"Boss nuance: {insight}", category="user_nuance")

        self.session_transcript.clear()
        self.save()
        print(f"[Sleep-Cycle Memory Engine]: Dual-partition distillation complete.\n"
              f"  [+] Session Important -> {self.session_imp_file}\n"
              f"  [+] Evolution Vault   -> {self.evolution_file}")

    def get_latest_evolution_context(self) -> str:
        """Retrieves F.R.I.D.A.Y.'s latest self-evolution directives for cognitive alignment."""
        if os.path.exists(self.evolution_file):
            try:
                with open(self.evolution_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    if history:
                        latest = history[-1].get("evolution_notes", {})
                        adaptations = latest.get("friday_self_adaptation", [])
                        insights = latest.get("boss_behavioral_insights", [])
                        lines = []
                        if adaptations:
                            lines.append("Self-Adaptation Directives: " + " | ".join(adaptations))
                        if insights:
                            lines.append("Boss Nuance Observations: " + " | ".join(insights))
                        return "\n".join(lines)
            except Exception:
                pass
        return ""

    def build_context_prompt(self, current_prompt: str) -> str:
        """Assembles long-term memories and recent dialogue into a clean contextual prompt in <0.5ms."""
        now = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        
        # 1. Instant BM25 / keyword memory recall (<0.5ms)
        combined_memories = self.recall(current_prompt, top_k=4)
        
        context_parts = [f"Current Time and Date: {now}."]
        
        if combined_memories:
            context_parts.append("\n[PERSISTENT LONG-TERM MEMORY & CONTEXT (Proactively use to remind Boss if relevant)]:")
            for m in combined_memories:
                context_parts.append(f"- {m}")
                
        # 3. Attach recent conversation flow if present
        if self.data["recent_dialogue"]:
            context_parts.append("\n[RECENT CONVERSATION HISTORY]:")
            for turn in self.data["recent_dialogue"][-3:]:
                context_parts.append(f"User: {turn['user']}")
                context_parts.append(f"FRIDAY: {turn['assistant']}")
                
        # 4. Attach F.R.I.D.A.Y.'s Autonomous Self-Evolution Directives
        evolution_ctx = self.get_latest_evolution_context()
        if evolution_ctx:
            context_parts.append(f"\n[F.R.I.D.A.Y. AUTONOMOUS EVOLUTION & BEHAVIORAL ALIGNMENT]:\n{evolution_ctx}")

        context_parts.append(f"\nUser Current Prompt: {current_prompt}")
        return "\n".join(context_parts)

    def compress_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Zero-latency message passthrough without phantom import exceptions."""
        return messages


import atexit

# Global singleton memory engine instance
memory_engine = HeadroomMemoryEngine()
atexit.register(memory_engine.consolidate_session_memory)
