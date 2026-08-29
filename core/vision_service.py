"""
Omni-Vision System for J.A.R.V.I.S.
Provides Dual-Channel Vision: Desktop Screen Understanding & Physical Webcam Sight.
"""

import base64
import io
import json
import os
import time
from typing import Generator, Optional, Tuple

import requests
from PIL import Image, ImageGrab
from dotenv import load_dotenv
load_dotenv()

_cv2 = None
def _get_cv2():
    global _cv2
    if _cv2 is None:
        try:
            import cv2
            _cv2 = cv2
        except ImportError:
            _cv2 = False
    return _cv2 if _cv2 is not False else None

_pyautogui = None
def _get_pyautogui():
    global _pyautogui
    if _pyautogui is None:
        try:
            import pyautogui
            _pyautogui = pyautogui
        except ImportError:
            _pyautogui = False
    return _pyautogui if _pyautogui is not False else None


OMNIROUTE_URL = os.environ.get("OMNIROUTE_URL", "http://localhost:20128/v1/chat/completions")
VISION_MODEL = os.environ.get("VISION_MODEL", "auto/best-vision")


class VisionService:
    """Manages screen grabbing, webcam frame acquisition, and multimodal vision analysis."""

    def __init__(self):
        self.last_screen_b64: Optional[str] = None
        self.last_cam_b64: Optional[str] = None

    def capture_screen(self, max_width: int = 1280, quality: int = 75) -> Optional[str]:
        """Captures the active screen display and returns a Base64-encoded JPEG Data URI."""
        img = None
        try:
            img = ImageGrab.grab(all_screens=True)
        except Exception:
            pyag = _get_pyautogui()
            if pyag:
                try:
                    img = pyag.screenshot()
                except Exception:
                    pass

        if img is None:
            print("[Vision] Screen capture failed: Display session unavailable.")
            return None

        # Convert RGBA to RGB if needed
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize if width exceeds max_width to keep latency low
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int(float(img.height) * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        self.last_screen_b64 = f"data:image/jpeg;base64,{b64}"
        return self.last_screen_b64

    def capture_webcam(self, camera_index: int = 0, quality: int = 85) -> Optional[str]:
        """Captures a high-definition 720p frame from the webcam with auto-exposure calibration."""
        cv = _get_cv2()
        if cv is None:
            print("[Vision] OpenCV (cv2) not installed.")
            return None

        cap = None
        try:
            # Try DirectShow backend on Windows with fast buffer size
            cap = cv.VideoCapture(camera_index, cv.CAP_DSHOW)
            if not cap.isOpened():
                cap = cv.VideoCapture(camera_index)

            if not cap.isOpened():
                print(f"[Vision] Camera index {camera_index} could not be opened.")
                return None

            cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
            cap.set(cv.CAP_PROP_BUFFERSIZE, 1)

            # Warm up camera sensor (gives auto-exposure and auto-focus time to settle)
            for _ in range(8):
                cap.read()

            ret, frame = cap.read()
            if not ret or frame is None:
                time.sleep(0.1)
                ret, frame = cap.read()

            if not ret or frame is None:
                print("[Vision] Failed to read frame from camera.")
                return None

            encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]
            ret, buffer = cv.imencode(".jpg", frame, encode_param)
            if not ret:
                return None

            b64 = base64.b64encode(buffer).decode("utf-8")
            self.last_cam_b64 = f"data:image/jpeg;base64,{b64}"
            return self.last_cam_b64
        except Exception as e:
            print(f"[Vision] Webcam capture error: {e}")
            return None
        finally:
            if cap is not None:
                cap.release()

    def stream_vision_reasoning(
        self,
        image_data_uri: str,
        user_prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None
    ) -> Generator[str, None, None]:
        """Streams multimodal vision reasoning from Google Gemini 2.5 Flash Vision."""
        if not system_prompt:
            system_prompt = (
                "You are F.R.I.D.A.Y., Boss's dedicated female tactical AI assistant. "
                "Analyze the visual camera/screen frame provided carefully. "
                "CRITICAL FACTUALITY RULES: "
                "1. If the user asks how many fingers they are holding, count ONLY fingers that are clearly and visibly extended. "
                "2. If no hands are visible, or if the user is not holding up any fingers, explicitly state that no fingers or hands are visible (e.g. 'Boss, aap koi ungli nahi dikha rahe hain' or 'Boss, frame mein koi haath nazar nahi aa raha'). Never guess or invent numbers. "
                "3. Answer directly, accurately, and concisely (1 to 2 spoken sentences, under 25 words). "
                "4. In Hindi/Hinglish, always use female grammatical agreements (e.g., 'dekh rahi hoon', 'bata rahi hoon'). "
                "5. Never use markdown formatting. Address the user as 'Boss'."
            )

        google_key = os.environ.get("GOOGLE_API_KEY", "")
        
        # Strip data URL prefix to get raw base64
        b64_data = image_data_uri
        if "," in image_data_uri:
            b64_data = image_data_uri.split(",", 1)[1]

        # 1. Primary: Google Gemini 2.5 Flash Vision REST Endpoint
        if google_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={google_key}"
                payload = {
                    "system_instruction": {
                        "parts": [{"text": system_prompt}]
                    },
                    "contents": [{
                        "parts": [
                            {"text": user_prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": b64_data
                                }
                            }
                        ]
                    }],
                    "generationConfig": {
                        "maxOutputTokens": 120,
                        "temperature": 0.0,
                        "thinkingConfig": {
                            "thinkingBudget": 0
                        }
                    }
                }
                resp = requests.post(url, json=payload, timeout=25)
                if resp.status_code == 200:
                    res_json = resp.json()
                    candidates = res_json.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts:
                            text_out = parts[0].get("text", "").strip()
                            if text_out:
                                yield text_out
                                return
            except Exception as e:
                print(f"[Vision Stream Gemini Error]: {e}")

        # 2. Secondary Fallback: Port 8081 Gemini-Web2API
        try:
            web2api_url = "http://localhost:8081/v1/chat/completions"
            payload = {
                "model": "gemini-auto",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {"type": "image_url", "image_url": {"url": image_data_uri}}
                        ]
                    }
                ]
            }
            r = requests.post(web2api_url, json=payload, timeout=25)
            if r.status_code == 200:
                out = r.json()["choices"][0]["message"].get("content", "")
                if out:
                    yield out
                    return
        except Exception:
            pass

        yield "I couldn't get a clear look through the optical sensors, Boss. Please try holding it closer to the camera."

    def extract_product_identity(self, image_data_uri: str, user_prompt: str = "") -> dict:
        """Analyzes a product in the webcam frame, detecting branding or predicting product type for web search."""
        google_key = os.environ.get("GOOGLE_API_KEY", "")
        b64_data = image_data_uri
        if "," in image_data_uri:
            b64_data = image_data_uri.split(",", 1)[1]

        sys_prompt = (
            "You are an expert computer vision product identifier. "
            "Examine the physical product, phone, device, or item shown in the camera frame carefully. "
            "1. Inspect visible brand logos, model text, camera module layouts, buttons, colors, and body design. "
            "2. If brand/model is identifiable (e.g. Samsung Galaxy, boAt, Apple, etc.), identify it accurately. "
            "3. If exact model isn't marked, visually predict the most likely brand and device class (e.g. 'Samsung Galaxy Smartphone' or 'Black Wireless Earbuds'). "
            "4. Formulate an effective search query to look up specifications, features, and retail price. "
            "Output ONLY valid JSON with keys: "
            "product_name (str), search_query (str - optimal web search query for specs/info/price), "
            "visual_notes (str - concise visual description of physical features, color, shape), "
            "has_brand (bool)."
        )

        def _clean_json_parse(raw_text: str) -> Optional[dict]:
            t = raw_text.strip()
            if "```json" in t:
                t = t.split("```json", 1)[1].split("```", 1)[0].strip()
            elif "```" in t:
                t = t.split("```", 1)[1].split("```", 1)[0].strip()
            s = t.find("{")
            e = t.rfind("}")
            if s != -1 and e != -1:
                t = t[s:e+1]
            return json.loads(t)

        if google_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={google_key}"
                payload = {
                    "system_instruction": {"parts": [{"text": sys_prompt}]},
                    "contents": [{
                        "parts": [
                            {"text": f"User query: {user_prompt}. Identify this product and formulate the best web search query."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": b64_data}}
                        ]
                    }],
                    "generationConfig": {
                        "response_mime_type": "application/json",
                        "maxOutputTokens": 300,
                        "temperature": 0.0,
                        "thinkingConfig": {
                            "thinkingBudget": 0
                        }
                    }
                }
                resp = requests.post(url, json=payload, timeout=15)
                if resp.status_code == 200:
                    res_json = resp.json()
                    candidates = res_json.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts:
                            raw_text = parts[0].get("text", "").strip()
                            data = _clean_json_parse(raw_text)
                            if data:
                                return data
            except Exception as e:
                print(f"[Product Vision Extraction Error]: {e}")

        # Fallback to web2api
        try:
            web2api_url = "http://localhost:8081/v1/chat/completions"
            payload = {
                "model": "gemini-auto",
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"User query: {user_prompt}. Output JSON only."},
                            {"type": "image_url", "image_url": {"url": image_data_uri}}
                        ]
                    }
                ]
            }
            r = requests.post(web2api_url, json=payload, timeout=15)
            if r.status_code == 200:
                out = r.json()["choices"][0]["message"].get("content", "")
                if out:
                    data = _clean_json_parse(out)
                    if data:
                        return data
        except Exception:
            pass

        return {
            "product_name": "Product in frame",
            "search_query": user_prompt if user_prompt else "electronic device specifications",
            "visual_notes": "Object held in front of camera",
            "has_brand": False
        }


# Global vision singleton
vision_engine = VisionService()

