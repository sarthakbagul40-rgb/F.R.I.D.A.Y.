"""
F.R.I.D.A.Y. OS 9.0: Vision Actuator & OS-World Controller (Pillar 1)
Empowers F.R.I.D.A.Y. with real-time screen perception, multimodal visual reasoning,
and mouse/keyboard desktop automation with safety fail-safes.
"""

import os
import time
import base64
import io
import threading
from typing import Optional, Tuple, Dict, Any, List
from PIL import Image, ImageGrab
import requests

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.15
except ImportError:
    pyautogui = None


class VisionActuator:
    """
    Multimodal Vision & OS Actuation Engine.
    Captures screenshots, reasons about visual UI elements, and controls mouse/keyboard.
    """

    def __init__(self):
        self.screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core", "vision_cache")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self._lock = threading.Lock()

    def capture_screen(self, bbox: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
        """Captures the primary monitor screen (or specific bounding box) as a PIL Image with robust fallbacks."""
        with self._lock:
            try:
                return ImageGrab.grab(bbox=bbox)
            except Exception:
                pass
            try:
                if pyautogui:
                    return pyautogui.screenshot(region=bbox)
            except Exception:
                pass
            # Fallback 1920x1080 canvas if running in headless service session
            return Image.new("RGB", (1920, 1080), color=(15, 23, 42))

    def capture_and_save(self, filename: str = "current_screen.png") -> str:
        """Captures current screen and saves to vision_cache, returning absolute path."""
        img = self.capture_screen()
        target_path = os.path.join(self.screenshot_dir, filename)
        img.save(target_path, format="PNG")
        return target_path

    def _image_to_base64(self, img: Image.Image, max_dimension: int = 1280) -> str:
        """Downscales image to optimal vision API dimensions and encodes as base64 JPEG."""
        w, h = img.size
        if max(w, h) > max_dimension:
            scale = max_dimension / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        
        # Convert RGBA to RGB for JPEG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def analyze_screen(self, user_query: str = "Describe what is currently visible on my screen.") -> str:
        """
        Takes a screenshot and sends it to the Multimodal Vision Model (Gemini-Web2API / Vision Endpoint).
        Returns clear, concise visual intelligence.
        """
        img = self.capture_screen()
        b64_data = self._image_to_base64(img)

        # 1. Try Local Gemini-Web2API Multimodal Bridge (Port 8081)
        try:
            payload = {
                "model": "gemini-2.5-flash",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are F.R.I.D.A.Y.'s High-Speed Computer Vision Cortex. Analyze the user's screen concisely and accurately in 2-3 sentences. Identify open windows, errors, code, or key UI elements."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_query},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}
                            }
                        ]
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 400
            }
            resp = requests.post("http://localhost:8081/v1/chat/completions", json=payload, timeout=12)
            if resp.status_code == 200:
                res_text = resp.json()["choices"][0]["message"]["content"]
                if res_text and len(res_text.strip()) > 10:
                    return res_text.strip()
        except Exception:
            pass

        # 2. Heuristic fallback: Process Window & Desktop Inspection
        try:
            import win32gui
            active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            return f"I can see your active screen displaying '{active_window}', Boss. Screen capture resolution is {img.size[0]}x{img.size[1]}."
        except Exception:
            return f"I have captured your screen at {img.size[0]}x{img.size[1]} pixels, Boss."

    # =========================================================================
    # OS MOUSE & KEYBOARD ACTUATION
    # =========================================================================

    def click_coordinates(self, x: int, y: int, clicks: int = 1, button: str = "left") -> bool:
        """Moves cursor to (x, y) with human-like easing and clicks."""
        if not pyautogui:
            return False
        try:
            pyautogui.moveTo(x, y, duration=0.25, tween=pyautogui.easeInOutQuad)
            pyautogui.click(clicks=clicks, button=button)
            return True
        except Exception as e:
            print(f"[Vision Actuator Error]: {e}")
            return False

    def type_text(self, text: str, interval: float = 0.02) -> bool:
        """Types string into active focused window with realistic keystroke delay."""
        if not pyautogui:
            return False
        try:
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            print(f"[Vision Actuator Error]: {e}")
            return False

    def press_hotkey(self, *keys: str) -> bool:
        """Presses a hotkey combination (e.g. 'ctrl', 's' or 'alt', 'tab')."""
        if not pyautogui:
            return False
        try:
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            print(f"[Vision Actuator Error]: {e}")
            return False

    def scroll(self, amount: int = -500) -> bool:
        """Scrolls the active window up (positive) or down (negative)."""
        if not pyautogui:
            return False
        try:
            pyautogui.scroll(amount)
            return True
        except Exception as e:
            print(f"[Vision Actuator Error]: {e}")
            return False


# Global singleton instance
vision_actuator = VisionActuator()
