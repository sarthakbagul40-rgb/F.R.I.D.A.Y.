"""
F.R.I.D.A.Y. Honeycomb Vision Hub
Optical sensors: screen display perception, webcam frame analysis, multimodal product intelligence, and desktop screenshot archiving.
"""

import re
from core.vision_service import vision_engine
from core.system_access import system_controller
from core.hubs.base import play_sound, speak
from core.hubs.chat_hub import stream_audio_chunks, get_ai_response

def handle_screen_vision(cmd: str):
    """Captures the active screen display and speaks real-time visual analysis."""
    speak("Analyzing active display, Boss.")
    play_sound("launch")
    img_b64 = vision_engine.capture_screen()
    if not img_b64:
        speak("I could not capture the active display session, Boss.")
        return

    prompt = cmd if len(cmd.split()) > 3 else "Describe what you see on my screen. Highlight any errors, code, or open applications."
    full_resp = []
    current_sentence = ""
    for token in vision_engine.stream_vision_reasoning(img_b64, prompt):
        print(token, end="", flush=True)
        full_resp.append(token)
        current_sentence += token
        ready_sentences, current_sentence = stream_audio_chunks(current_sentence)
        for s in ready_sentences:
            if s:
                speak(s)

    if current_sentence.strip():
        tail = current_sentence.replace('<DOT>', '.').strip()
        if tail:
            speak(tail)
    print()

def handle_camera_vision(cmd: str):
    """Captures a webcam frame and performs visual analysis with autonomous product/web intelligence."""
    speak("Accessing optical sensors, Boss.")
    play_sound("launch")
    img_b64 = vision_engine.capture_webcam()
    if not img_b64:
        speak("I was unable to establish an optical link with the camera, Boss.")
        return

    # Check for product research / information lookup intent
    is_product_research = any(w in cmd.lower() for w in [
        "product", "information", "info", "search", "details", "detail", "price", 
        "specs", "specification", "about this", "brand", "model", "find me", 
        "tell me about", "buy", "review", "kya hai", "features"
    ])

    if is_product_research:
        # Multimodal Product Identification & Autonomous Web Search
        prod_data = vision_engine.extract_product_identity(img_b64, cmd)
        prod_name = prod_data.get("product_name", "Product")
        search_q = prod_data.get("search_query", cmd)
        visual_notes = prod_data.get("visual_notes", "")
        has_brand = prod_data.get("has_brand", False)

        search_context = ""
        if search_q:
            try:
                from core.hubs.web_hub import web_search_intelligence
                search_context = web_search_intelligence(search_q)
            except Exception:
                search_context = ""

        try:
            from core.background_coprocessor import coprocessor
            distilled_analysis = coprocessor.distill_product_intelligence(
                user_query=cmd,
                product_name=prod_name,
                visual_notes=visual_notes,
                has_brand=has_brand,
                search_context=search_context
            )
            speak(distilled_analysis)
        except Exception:
            prompt = (
                f"You are F.R.I.D.A.Y., Boss's tactical AI companion. The Boss asked: '{cmd}'.\n"
                f"Optical Sensor Scan: {visual_notes}.\n"
                f"Identified / Predicted Item: {prod_name} (Brand Verified: {has_brand}).\n"
                f"Live Web Data:\n{search_context}\n\n"
                f"Provide a crisp, highly knowledgeable response in 2 spoken sentences. "
                f"If branding/model is identified, state it with its key features or pricing. "
                f"In Hindi/Hinglish, always use female grammatical agreements (e.g. 'dekh rahi hoon'). Address the user as 'Boss'."
            )
            get_ai_response(prompt, speak_stream=True)
        return

    prompt = cmd if len(cmd.split()) > 3 else "Describe what you see through the camera in front of you. Identify any people or objects."
    full_resp = []
    current_sentence = ""
    for token in vision_engine.stream_vision_reasoning(img_b64, prompt):
        print(token, end="", flush=True)
        full_resp.append(token)
        current_sentence += token
        ready_sentences, current_sentence = stream_audio_chunks(current_sentence)
        for s in ready_sentences:
            if s:
                speak(s)

    if current_sentence.strip():
        tail = current_sentence.replace('<DOT>', '.').strip()
        if tail:
            speak(tail)
    print()

def handle_take_screenshot(cmd: str):
    """Captures and archives full screen to Desktop/Screenshots/."""
    speak("Capturing screen, Boss.")
    play_sound("launch")
    path = system_controller.take_and_save_screenshot(open_after=True)
    if path:
        speak("Screenshot archived to your Desktop, Boss.")
    else:
        speak("I encountered an issue capturing the screen archive, Boss.")

def dispatch_vision_intent(cmd: str) -> bool:
    """Evaluates smart camera and screen triggers."""
    vision_camera_triggers = [
        r'\bhold\b', r'\bholding\b', r'\bheld\b', r'\bin\s+my\s+hand\b', r'\bin\s+hand\b',
        r'\bbefore\s+camera\b', r'\bin\s+front\s+of\s+camera\b', r'\bin\s+front\s+of\s+you\b',
        r'\blook\s+at\s+this\b', r'\blook\s+at\s+me\b', r'\bsee\s+me\b', r'\bthrough\s+the\s+camera\b',
        r'\boptical\s+sensor\b', r'\bwhat\s+is\s+this\b', r'\bwhat\'s\s+this\b', r'\bidentify\s+this\b',
        r'\bidentify\s+what\b', r'\banalyze\s+what\b', r'\banalyse\s+what\b', r'\banalyze\s+this\b',
        r'\banalyse\s+this\b', r'\banalyze\s+the\b', r'\banalyse\s+the\b', r'\bdescribe\s+what\s+you\s+see\b',
        r'\bwhat\s+can\s+you\s+see\b', r'\bwhat\s+do\s+you\s+see\b', r'\bcamera\s+vision\b',
        r'\bscan\s+this\b', r'\bdescribe\s+this\b', r'\binformation\s+(?:of|for|about)\s+this\b',
        r'\binfo\s+(?:of|for|about)\s+this\b', r'\bdetails\s+(?:of|for|about)\s+this\b',
        r'\b(?:search|find)\s+(?:me\s+)?information\b', r'\b(?:search|find)\s+(?:me\s+)?info\b',
        r'\bthis\s+product\b', r'\bthe\s+product\b', r'\bscan\s+product\b', r'\bidentify\s+product\b',
        r'\btell\s+me\s+about\s+this\b', r'\bcheck\s+what\b', r'\bwhat\s+am\s+i\b',
        r'\byeh\s+kya\s+hai\b', r'\bye\s+kya\s+hai\b', r'\bisko\s+dekho\b',
        r'\bcamera\s+se\s+dekho\b', r'\bphoto\s+dekho\b'
    ]
    if any(re.search(trig, cmd, re.I) for trig in vision_camera_triggers):
        handle_camera_vision(cmd)
        return True

    vision_screen_triggers = [
        "on my screen", "on screen", "on the screen", "read screen", "look at screen",
        "check screen", "my display", "active display", "explain this error",
        "scan my screen", "scan the screen", "scan screen", "scan display", "screen scan",
        "analyse screen", "analyze screen"
    ]
    if any(trig in cmd.lower() for trig in vision_screen_triggers):
        handle_screen_vision(cmd)
        return True

    return False

COMMANDS = {
    "capture my screen": handle_take_screenshot,
    "capture the screen": handle_take_screenshot,
    "capture screen": handle_take_screenshot,
    "take screenshot": handle_take_screenshot,
    "take a screenshot": handle_take_screenshot,
    "capture screenshot": handle_take_screenshot,
    "screenshot": handle_take_screenshot,
    "analyse my whole screen and tell me what do you see": handle_screen_vision,
    "analyse my whole screen": handle_screen_vision,
    "analyse my screen": handle_screen_vision,
    "analyse the screen": handle_screen_vision,
    "analyse screen": handle_screen_vision,
    "analyze my whole screen and tell me what do you see": handle_screen_vision,
    "analyze my whole screen": handle_screen_vision,
    "analyze the screen": handle_screen_vision,
    "analyze screen": handle_screen_vision,
    "what do you see on my screen": handle_screen_vision,
    "what do you see on the screen": handle_screen_vision,
    "describe my screen": handle_screen_vision,
    "describe what you see on my screen": handle_screen_vision,
    "look at the screen": handle_screen_vision,
    "look at screen": handle_screen_vision,
    "what's on my screen": handle_screen_vision,
    "read my screen": handle_screen_vision,
    "check my screen": handle_screen_vision,
    "see my screen": handle_screen_vision,
    "explain this error": handle_screen_vision,
    "how many fingers am i holding": handle_camera_vision,
    "how many fingers": handle_camera_vision,
    "how many finger am i holding": handle_camera_vision,
    "how many finger": handle_camera_vision,
    "fingers am i holding": handle_camera_vision,
    "what am i holding": handle_camera_vision,
    "am i holding": handle_camera_vision,
    "what is in my hand": handle_camera_vision,
    "what's in my hand": handle_camera_vision,
    "look at me": handle_camera_vision,
    "can you see me": handle_camera_vision,
    "see me": handle_camera_vision,
    "what do you see in the camera": handle_camera_vision,
    "what do you see through the camera": handle_camera_vision,
    "what do you see in front of you": handle_camera_vision,
    "what do you see": handle_camera_vision,
    "what can you see": handle_camera_vision,
    "access camera": handle_camera_vision,
    "open camera": handle_camera_vision,
    "start camera": handle_camera_vision,
    "camera on": handle_camera_vision,
    "check camera": handle_camera_vision,
    "look through camera": handle_camera_vision,
    "describe what you see": handle_camera_vision,
    "describe what you are seeing": handle_camera_vision,
    "describe what to see": handle_camera_vision,
    "look at this": handle_camera_vision,
    "camera vision": handle_camera_vision,
    "analyze my screen": handle_screen_vision,
    "look at my screen": handle_screen_vision,
    "what is on my screen": handle_screen_vision,
    "screen analysis": handle_screen_vision
}
