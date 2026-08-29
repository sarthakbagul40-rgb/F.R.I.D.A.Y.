"""
F.R.I.D.A.Y. Cybernetic WhatsApp Messaging & Contact Automation Engine
Supports natural spoken phrase parsing, persistent contact book, native WhatsApp Desktop execution, and autonomous auto-send.
"""

import os
import re
import json
import time
import threading
import urllib.parse
import webbrowser
from typing import Optional, Tuple, Dict

try:
    import pyautogui
except ImportError:
    pyautogui = None

CONTACTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts.json")


class WhatsAppEngine:
    """Manages natural language WhatsApp message parsing, native desktop dispatch, and automated message transmission."""

    def __init__(self):
        self.contacts = self._load_contacts()

    def _load_contacts(self) -> Dict[str, str]:
        """Loads persistent contact book from disk."""
        if os.path.exists(CONTACTS_FILE):
            try:
                with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def save_contact(self, name: str, phone_number: str) -> bool:
        """Saves or updates a contact's phone number."""
        clean_name = name.lower().strip()
        clean_phone = re.sub(r"[^\d+]", "", phone_number.strip())
        self.contacts[clean_name] = clean_phone
        try:
            with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.contacts, f, indent=2)
            return True
        except Exception:
            return False

    def parse_command(self, cmd: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts (contact_name, message_text) from spoken natural language commands.
        Handles punctuation, casing, filler wake words, and multi-syntax requests.
        """
        c = cmd.strip()
        # 1. Clean filler wake words and trailing punctuation
        c = re.sub(r"^(friday|jarvis)\s*,?\s*", "", c, flags=re.IGNORECASE)
        c = re.sub(r"[.,!?;:]+$", "", c).strip()
        
        # 2. Strip trailing "on/in/via whatsapp" tokens
        c_clean = re.sub(r"\b(on|in|via)?\s*whatsapp\b", "", c, flags=re.IGNORECASE).strip()
        c_clean = re.sub(r"[.,!?;:]+$", "", c_clean).strip()
        
        # Pattern 1: send/message [msg] to [contact]
        m1 = re.search(r"^(?:send|message|text)\s+(?:a\s+)?(?:message\s+)?(.+?)\s+to\s+(.+)$", c_clean, re.IGNORECASE)
        if m1:
            msg, contact = m1.group(1).strip(), m1.group(2).strip()
            return contact.lower(), msg
            
        # Pattern 2: send/message [contact] [saying/that/with] [msg]
        m2 = re.search(r"^(?:send|message|text)\s+(?:to\s+)?(.+?)\s+(?:saying|that|with|message)\s+(.+)$", c_clean, re.IGNORECASE)
        if m2:
            contact, msg = m2.group(1).strip(), m2.group(2).strip()
            return contact.lower(), msg
            
        # Pattern 3: send/message [contact] [msg]
        m3 = re.search(r"^(?:send|message|text)\s+(?:to\s+)?([a-zA-Z]+)\s+(.+)$", c_clean, re.IGNORECASE)
        if m3:
            contact, msg = m3.group(1).strip(), m3.group(2).strip()
            return contact.lower(), msg

        # Pattern 4: whatsapp [contact] [msg]
        m4 = re.search(r"^(?:whatsapp)\s+([a-zA-Z]+)\s+(.+)$", c_clean, re.IGNORECASE)
        if m4:
            contact, msg = m4.group(1).strip(), m4.group(2).strip()
            return contact.lower(), msg

        return None, None

    def _auto_send_worker(self, delay: float = 2.8):
        """Waits for WhatsApp Desktop window to open and focuses input, then presses Enter to send automatically."""
        if not pyautogui:
            return
        time.sleep(delay)
        try:
            # Verify active window is WhatsApp to prevent blind typing into other apps
            is_whatsapp_focused = False
            try:
                import pygetwindow as gw
                active_win = gw.getActiveWindow()
                if active_win and "whatsapp" in (active_win.title or "").lower():
                    is_whatsapp_focused = True
                else:
                    # Try finding and activating WhatsApp window
                    for win in gw.getAllWindows():
                        if win.title and "whatsapp" in win.title.lower():
                            if win.isMinimized:
                                win.restore()
                            win.activate()
                            time.sleep(0.3)
                            is_whatsapp_focused = True
                            break
            except Exception:
                is_whatsapp_focused = False

            if is_whatsapp_focused:
                pyautogui.press("enter")
                print("\n[WhatsApp Engine]: WhatsApp window confirmed. Pressed Enter. Message dispatched!")
            else:
                print("\n[WhatsApp Engine Guard]: WhatsApp window not active. Aborted blind Enter press to protect system.")
        except Exception as e:
            print(f"\n[WhatsApp Auto-Send Error]: {e}")

    def send_message(self, cmd: str, speak_fn=None, auto_send: bool = True) -> bool:
        """Parses and dispatches a WhatsApp message using Native WhatsApp Desktop with autonomous auto-send."""
        self.contacts = self._load_contacts()
        contact, msg = self.parse_command(cmd)
        
        if not contact or not msg:
            if speak_fn:
                speak_fn("Please specify who to message and what to send, Boss.")
            return False

        encoded_msg = urllib.parse.quote(msg)
        phone = self.contacts.get(contact.lower())

        if phone:
            # 1. Native WhatsApp Desktop URI
            uri = f"whatsapp://send?phone={phone}&text={encoded_msg}"
            try:
                os.startfile(uri)
                if speak_fn:
                    speak_fn(f"Sending message to {contact.capitalize()} on WhatsApp Desktop, Boss.")
                print(f"[WhatsApp Engine]: Opening WhatsApp Desktop for {contact} ({phone}) -> '{msg}'")
            except Exception:
                # Web Fallback
                web_url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
                webbrowser.open(web_url)
                if speak_fn:
                    speak_fn(f"Dispatching message to {contact.capitalize()} on WhatsApp, Boss.")

            # Trigger automated send key in background
            if auto_send:
                threading.Thread(target=self._auto_send_worker, args=(2.8,), daemon=True).start()
            return True
        else:
            # No registered phone number -> draft in WhatsApp Desktop
            uri = f"whatsapp://send?text={encoded_msg}"
            try:
                os.startfile(uri)
                if speak_fn:
                    speak_fn(f"Opening WhatsApp Desktop with your message for {contact.capitalize()}, Boss.")
                print(f"[WhatsApp Engine]: Drafted message in WhatsApp Desktop for '{contact}' -> '{msg}'")
            except Exception:
                web_url = f"https://web.whatsapp.com/send?text={encoded_msg}"
                webbrowser.open(web_url)
                if speak_fn:
                    speak_fn(f"Opening WhatsApp with your message for {contact.capitalize()}, Boss.")

            if auto_send:
                threading.Thread(target=self._auto_send_worker, args=(2.8,), daemon=True).start()
            return True


# Global singleton instance
whatsapp_engine = WhatsAppEngine()
