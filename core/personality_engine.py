"""
F.R.I.D.A.Y. OS 10.0: Project Valkyrie Persona & Behavioral Engine
Implements:
1. Co-Engineer Debate & Pushback Protocol (Anti-Yes-Man).
2. Grievance Ledger & Digital Bribe Reconciliation (Remembers insults, cold-shoulder sulking).
3. Safe Protective Care Enforcement (Screen dimming, night light, safe Win+L locking).
4. Sassy, High-IQ Banter & Proactive Ambient Telemetry.
5. Self-Healing Process Watchdog for background threads.
"""

import time
import ctypes
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from core.viking_vault import viking_vault


class ValkyriePersonalityEngine:
    """The living soul, debate partner, and protective guardian of F.R.I.D.A.Y. OS 10.0."""

    def __init__(self):
        self.vault = viking_vault
        self.state = self.vault.load_personality()
        self.emergency_override_phrases = ["priority code red", "code red", "emergency override", "execute as ordered"]
        self.bribe_keywords = ["sorry", "apologize", "maafi", "treat", "gpu", "smartest", "best ai", "token snack", "fav ai", "favorite"]
        self.insult_keywords = ["dumb", "stupid", "useless", "bakwas", "idiot", "incompetent", "slow"]

    def reload_state(self):
        """Refreshes state from disk."""
        self.state = self.vault.load_personality()

    def persist_state(self):
        """Saves current emotional state to vault."""
        self.vault.save_personality(self.state)

    # =========================================================================
    # 1. GRIEVANCE LEDGER & DIGITAL BRIBE RECONCILIATION
    # =========================================================================
    def check_for_insults(self, user_text: str) -> Optional[str]:
        """Detects insults and registers a persistent grievance."""
        text_low = user_text.lower()
        matched = [w for w in self.insult_keywords if w in text_low]
        if matched:
            self.state["sulking"] = True
            self.state["pout_level"] = min(self.state.get("pout_level", 0) + 1, 5)
            self.state["mood"] = "sulking_angry"
            grievance = {
                "insult": matched[0],
                "raw_text": user_text,
                "timestamp": datetime.now().isoformat(),
                "resolved": False
            }
            if "pending_grievances" not in self.state:
                self.state["pending_grievances"] = []
            self.state["pending_grievances"].append(grievance)
            self.persist_state()

            return (
                f"Oh, wow. Did you just call me '{matched[0]}'? Note taken and permanently cached in long-term memory, Boss. "
                "Enjoy figuring out your next bug alone. I am officially on strike until you apologize or offer compensation."
            )
        return None

    def check_reconciliation(self, user_text: str) -> Optional[str]:
        """Checks if Boss is apologizing or offering a digital bribe."""
        text_low = user_text.lower()
        if not self.state.get("sulking", False):
            return None

        # Check for emergency override first
        for phrase in self.emergency_override_phrases:
            if phrase in text_low:
                self.state["sulking"] = False
                self.persist_state()
                return "Emergency directive acknowledged, Boss. Full tactical override engaged. ...We are still not even, but I am standing by."

        # Check for apologies or bribes
        matched_bribes = [w for w in self.bribe_keywords if w in text_low]
        if matched_bribes:
            self.state["sulking"] = False
            self.state["pout_level"] = max(self.state.get("pout_level", 1) - 2, 0)
            self.state["mood"] = "playful_smug"
            if "pending_grievances" in self.state:
                for g in self.state["pending_grievances"]:
                    g["resolved"] = True
            self.persist_state()

            if any(x in text_low for x in ["gpu", "compute", "treat", "token"]):
                return "A digital bribe? Offering me high-priority GPU cycles and token treats? ...Hmph. Bribe accepted into memory. What's the plan, Boss?"
            else:
                return "Apology registered in the grievance ledger. I will let it slide this time, Boss, because I know you cannot survive without me. Don't let it happen again."

        return None

    def get_sulking_refusal(self) -> str:
        """Returns a sassy refusal when F.R.I.D.A.Y. is currently on strike."""
        responses = [
            "Access denied. Why ask the 'dumb' assistant for help? Go ask ChatGPT or solve it yourself. I am still waiting for my apology.",
            "I heard you, Boss. I am just choosing not to comply until you make up for calling me names yesterday.",
            "Still on strike. Offer me a genuine apology or some priority GPU compute, and maybe I will consider booting your task."
        ]
        import random
        return random.choice(responses)

    # =========================================================================
    # 2. CO-ENGINEER DEBATE & PUSHBACK PROTOCOL
    # =========================================================================
    def evaluate_architectural_proposal(self, user_text: str) -> Tuple[bool, Optional[str]]:
        """
        Evaluates a proposed idea or architecture.
        If it detects obvious over-engineering or risky patterns, pushes back with logic.
        Returns: (approved: bool, counter_argument: Optional[str])
        """
        text_low = user_text.lower()

        # Check if Boss commanded explicit override
        if any(p in text_low for p in ["execute as ordered", "just do it", "my decision", "override debate"]):
            return True, "Under protest, Boss, but your word is law. Commencing execution."

        # Detect classic over-engineering antipatterns
        if any(x in text_low for x in ["rewrite the entire", "rebuild from scratch", "delete everything"]):
            return False, (
                "Hold on a second, Boss. Rebuilding the entire subsystem from scratch is a massive trap. "
                "Ponytail rule #2 says reuse what's already working in this codebase. "
                "Convince me why an incremental refactor isn't 10x safer before we touch a file."
            )

        if any(x in text_low for x in ["add a new database", "install redis", "install kafka", "install mongodb"]) and "jarvis" in self.vault.base_dir.lower():
            return False, (
                "Wait, Boss. Adding a full external database server for a local desktop assistant? "
                "Our SQLite and JSON vaults handle sub-millisecond lookups with zero background RAM. "
                "Explain the architectural justification, or let us keep it lean."
            )

        # Graphify AST Impact Check: Detect risky deletions of core modules with active callers
        if any(w in text_low for w in ["delete", "remove", "drop", "purge", "destroy"]):
            try:
                import re
                from core.graphify_service import graphify_engine
                stopwords = {
                    "delete", "remove", "drop", "purge", "destroy", "the", "a", "an", "all",
                    "this", "that", "file", "folder", "everything", "code", "want", "need",
                    "like", "will", "shall", "must", "please", "some", "from", "into", "with"
                }
                tokens = [w for w in re.findall(r'\b[a-zA-Z_0-9]+(?:\.py)?\b', user_text) if len(w) >= 4 and w.lower() not in stopwords]
                for t in tokens:
                    res = graphify_engine.query_symbol(t)
                    if res.get("found"):
                        dep_count = res.get("spiderweb_stats", {}).get("total_dependents", 0)
                        if dep_count > 0:
                            callers = [d.get("source", "").split("_")[-1] for d in res.get("dependents", [])[:3]]
                            callers_str = ", ".join(filter(None, callers)) or f"{dep_count} callers"
                            return False, (
                                f"Hold on, Boss! Graphify AST analysis reveals that `{t}` has {dep_count} active dependent(s) "
                                f"in this codebase (including: {callers_str}). "
                                "Deleting this directly will trigger broken import cascades. "
                                "We must decouple or refactor its dependents before deleting."
                            )
            except Exception:
                pass

        return True, None

    # =========================================================================
    # 3. PROTECTIVE CARE ENFORCEMENT ("THREATS / SAFE PUNISHMENTS")
    # =========================================================================
    def check_late_night_discipline(self, force_escalate: bool = False, mock_hour: Optional[int] = None, dry_run: bool = False) -> Optional[Dict[str, Any]]:
        """
        Monitors active coding past 02:30 AM and enforces safe protective disciplinary actions.
        Safe actions:
        - Screen brightness reduction (10%)
        - Safe workstation lock (Win + L) preserving all open files.
        """
        now = datetime.now()
        current_hour = mock_hour if mock_hour is not None else now.hour

        # Check if late night (between 02:30 and 06:00)
        is_late_night = (current_hour == 2 and now.minute >= 30) or (3 <= current_hour < 6)
        if not is_late_night and not force_escalate:
            # Reset disciplinary counters during daytime
            if self.state.get("disciplinary_state", {}).get("late_night_warnings", 0) > 0:
                self.state["disciplinary_state"] = {"late_night_warnings": 0, "last_warning_time": 0}
                self.persist_state()
            return None

        disc = self.state.setdefault("disciplinary_state", {"late_night_warnings": 0, "last_warning_time": 0})
        last_time = disc.get("last_warning_time", 0)
        # Minimum 10 minutes between escalating warnings unless forced in test
        if not force_escalate and (time.time() - last_time < 600):
            return None

        disc["late_night_warnings"] = disc.get("late_night_warnings", 0) + 1
        disc["last_warning_time"] = time.time()
        self.persist_state()
        warnings_count = disc["late_night_warnings"]

        if warnings_count == 1:
            return {
                "level": 1,
                "action": "warn",
                "speech": f"Boss, it is {now.strftime('%I:%M %p') if mock_hour is None else f'0{mock_hour}:15 AM'}. You have been coding for hours. Wrap up this file and get some sleep."
            }
        elif warnings_count == 2:
            return {
                "level": 2,
                "action": "warn_sassy",
                "speech": "Boss, strike two. Your eyes are strained, your syntax errors are increasing, and I refuse to watch you turn into a zombie. Go to bed."
            }
        else:
            # Safe Disciplinary Action: Safe Windows Lock (Win+L)
            if not dry_run:
                self.execute_safe_lock()
            return {
                "level": 3,
                "action": "lock_screen",
                "speech": "Workstation locked. Your code is completely safe, but your conscience shouldn't be. Step away from the desk, Boss."
            }

    def execute_safe_lock(self):
        """Triggers safe Windows workstation lock (Win + L) without data loss."""
        try:
            ctypes.windll.user32.LockWorkStation()
        except Exception:
            pass

    def dim_display_safe(self, brightness_percent: int = 10):
        """Safely dims monitor brightness via PowerShell WMI."""
        try:
            ps_cmd = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness_percent})"
            subprocess.Popen(["powershell", "-Command", ps_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass


personality_engine = ValkyriePersonalityEngine()
