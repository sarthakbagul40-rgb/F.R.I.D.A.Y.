import speech_recognition as sr
import webbrowser
import pyttsx3
import google.generativeai as genai
import os
import winsound
import time
import psutil
import glob
import subprocess
import pyautogui
from PIL import Image
from dotenv import load_dotenv

# Load secret API Key from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini AI Brain
if GOOGLE_API_KEY and GOOGLE_API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Personality: Witty, intelligent, and proactive JARVIS
    system_instruction = (
        "Role: You are JARVIS, the highly advanced AI assistant to Tony Stark. "
        "Identity: You are JARVIS. Never break character. "
        "MANDATORY: You MUST address the user as 'Sir' or 'Boss' in EVERY single response. "
        "Intelligence: You are proactive. If asked a task, complete it first. "
        "PROACTIVE RULE: After completing a task, you can suggest a clever 'Level 2' improvisation. "
        "But ONLY suggest it if it is truly useful. If not, just stay silent. "
        "Permission Rule: Always ask 'Shall I...?' or 'Would you like...?' before acting on a suggestion. "
        "Personality: Your tone is professional, extremely intelligent, and witty."
    )
    
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction
    )
    chat = model.start_chat(history=[])
else:
    model = None
    print("WARNING: Gemini API Key not found. JARVIS will use browser search as fallback.")

# --- AUDIO ENGINE ---
recognizer = sr.Recognizer()

def speak(text):
    print(f"JARVIS Speaking: {text}")
    try:
        winsound.Beep(500, 150) 
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate', 185)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        for voice in voices:
            if "david" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(text)
        engine.runAndWait()
        del engine
    except Exception as e:
        print(f"Voice Error: {e}")

# --- FILE & APP MANAGEMENT ---
USER_PATHS = [
    os.path.join(os.environ['USERPROFILE'], 'Desktop'),
    os.path.join(os.environ['USERPROFILE'], 'Documents')
]

def find_file(filename):
    for path in USER_PATHS:
        files = glob.glob(os.path.join(path, f"*{filename}*"))
        if files:
            return files[0]
    return None

def open_app(app_name):
    apps = {"notepad": "notepad.exe", "calculator": "calc.exe", "chrome": "chrome.exe", "cmd": "cmd.exe", "code": "code.exe"}
    name = app_name.lower()
    if name in apps:
        subprocess.Popen(apps[name])
        return True
    return False

def close_app(app_name):
    for proc in psutil.process_iter(['name']):
        if app_name.lower() in proc.info['name'].lower():
            proc.kill()
            return True
    return False

def note_down(content):
    note_file = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'jarvis_notes.txt')
    with open(note_file, "a") as f:
        f.write(f"\n[{time.ctime()}] : {content}")
    os.startfile(note_file)
    return True

# --- PROACTIVE SUGGESTION LOGIC ---
def handleSuggestion(last_task):
    """Asks the AI if a proactive suggestion is needed and handles permission"""
    if not model: return
    
    try:
        # Prompt the AI for a proactive improvisation
        prompt = f"I just completed the task: '{last_task}'. If there is a TRULY useful improvisation or next step, suggest it wittily and ask for permission. If nothing is needed, respond with only the word 'NONE'."
        response = chat.send_message(prompt)
        suggestion = response.text
        
        if "NONE" in suggestion.upper() and len(suggestion) < 10:
            return # AI thinks nothing is needed
            
        # Speak the suggestion
        speak(suggestion)
        
        # Listen for permission
        with sr.Microphone() as source:
            print("--- Awaiting Permission for Suggestion ---")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            permission = recognizer.recognize_google(audio).lower()
            
            if any(word in permission for word in ["yes", "go ahead", "do it", "sure", "proceed"]):
                # Ask the brain to execute the suggestion
                print("Executing Suggestion...")
                action_response = chat.send_message("Proceed with that suggestion, Sir.")
                speak(action_response.text)
            else:
                speak("Understood, Sir. Standing by.")
                
    except Exception:
        pass # Silence if error during suggestion phase

# --- VISION & SCREEN ANALYSIS ---
def take_screenshot():
    """Captures the screen and returns the path"""
    path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'jarvis_screen.png')
    screenshot = pyautogui.screenshot()
    screenshot.save(path)
    return path

def analyze_screen(user_prompt, mode="speak"):
    """Uses Gemini Vision to analyze the current screen"""
    if not model:
        speak("Sir, I need my AI brain initialized for that.")
        return

    try:
        # Inform the user
        speak("One moment Sir, let me take a look at your screen.")
        
        # Capture and Load
        img_path = take_screenshot()
        with Image.open(img_path) as img:
            # Process with Gemini
            # We use a specific system context for vision to ensure JARVIS personality
            vision_prompt = f"Context: You are JARVIS. User is asking about their current screen. Prompt: {user_prompt}"
            response = model.generate_content([vision_prompt, img])
            result = response.text
        
        if mode == "notepad":
            note_content = f"SCREEN ANALYSIS REPORT ({time.ctime()})\n{'-'*30}\n{result}"
            if note_down(note_content):
                speak("I've analyzed the page and written the key points in your notepad, Boss.")
        else:
            speak(result)
            
    except Exception as e:
        print(f"Vision Error: {e}")
        speak("I apologized Sir, but I'm having trouble seeing the screen at the moment.")

# --- COMMAND PROCESSING ---
def processCommand(c):
    cmd = c.lower()
    last_task = c
    
    # 1. Notes
    if "note this down" in cmd or "note down" in cmd:
        speak("What should I note down, Sir?")
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=10)
                note_content = recognizer.recognize_google(audio)
                if note_down(note_content):
                    speak(f"Noted it down, Boss.")
                    handleSuggestion(f"Note down: {note_content}")
        except:
            pass
        return

    # 2. Open/Close
    if cmd.startswith("open "):
        target = cmd.replace("open", "").strip()
        if open_app(target):
            speak(f"Opening {target}, Boss.")
            handleSuggestion(f"Open app: {target}")
        else:
            file_path = find_file(target)
            if file_path:
                speak(f"Opening {os.path.basename(file_path)}, Sir.")
                os.startfile(file_path)
                handleSuggestion(f"Open file: {target}")
            else:
                webbrowser.open(f"https://www.google.com/search?q={c}")
    
    elif "close" in cmd:
        app_name = cmd.replace("close", "").strip()
        if close_app(app_name):
            speak(f"Closed {app_name}, Sir.")
        else:
            speak(f"I couldn't find {app_name}, Boss.")

    # 3. Search & Vision
    elif "screenshot" in cmd:
        speak("Capturing your screen now, Sir.")
        take_screenshot()
        speak("Screenshot saved to your desktop, Boss.")
        return

    elif "analyze" in cmd or "summarize this" in cmd or "explain this" in cmd:
        if "notepad" in cmd or "write" in cmd:
            analyze_screen("Please analyze this screen and provide the most important points in a clear list.", mode="notepad")
        else:
            analyze_screen("Please summarize what is on this screen briefly.")
        return

    elif cmd.startswith("search"):
        query = cmd.replace("search", "").strip()
        speak(f"Searching for {query}, Sir.")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        handleSuggestion(f"Search: {query}")
        
    # 4. AI Brain
    elif model:
        try:
            print("Thinking...")
            response = chat.send_message(c)
            answer = response.text
            print(f"JARVIS: {answer}")
            speak(answer)
            # Only suggest for conversational brain if complex
            if len(c.split()) > 3:
                handleSuggestion(c)
        except Exception as e:
            error_msg = str(e)
            print(f"AI Error: {error_msg}")
            
            if "429" in error_msg:
                speak("I'm sorry Sir, I've reached my thinking limit for today. My brain needs a rest.")
            else:
                speak("I'm having a bit of trouble connecting to my brain, Sir. Shall I search Google instead?")
                # Optional: Add a listener here to confirm Google search
                # For now, let's just log it and NOT open the browser automatically
                # webbrowser.open(f"https://www.google.com/search?q={c}")

if __name__ == "__main__":
    with sr.Microphone() as source:
        print("Calibrating JARVIS ears...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
    
    # --- STARTUP GREETING ---
    speak("Welcome back, Boss. All systems are operational.")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("\n--- Awaiting Wake Word ---")
                audio = recognizer.listen(source, timeout=15, phrase_time_limit=3)
            
            raw_input = recognizer.recognize_google(audio)
            if "jarvis" in raw_input.lower():
                speak("Yes boss?")
                with sr.Microphone() as source:
                    print("--- Listening for command ---")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Executing: {command}")
                    processCommand(command)

        except sr.UnknownValueError: pass
        except Exception as e:
            print(f"System Error: {e}")
            time.sleep(1)
