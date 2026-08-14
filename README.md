# 🤖 J.A.R.V.I.S — Just A Rather Very Intelligent System

A witty, voice-activated desktop AI assistant powered by **Google Gemini 2.5 Flash**, featuring screen vision analysis, app/file automation, desktop notes, and proactive task improvisations.

---

## 📌 Project Overview & System Description

**J.A.R.V.I.S** (*Just A Rather Very Intelligent System*) is a full-featured, voice-driven personal AI desktop companion inspired by Tony Stark's iconic assistant from Marvel's *Iron Man*.

Built natively for Windows using Python and Google's flagship **Gemini 2.5 Flash** multimodal model, JARVIS operates in the background as your interactive voice agent. It listens for the wake word **"JARVIS"**, addresses you as *"Sir"* or *"Boss"*, executes automation tasks, transcribes voice notes, analyzes your current computer screen via computer vision, and proactively suggests helpful follow-up actions.

### 🌟 Key Architectural Highlights
- **Multimodal Intelligence**: Uses the official `google-genai` SDK for low-latency conversational AI and computer vision screen reporting.
- **Proactive Task Improvisation**: Evaluates completed commands to offer clever "Level-2" improvisations (e.g., after opening an editor, asking to load your workspace).
- **High Resilience & Graceful Fallbacks**: Automatically falls back to local file searching or web queries if apps or API connections are unavailable, with zero process-crash risks.
- **Native Windows Integration**: Built-in SAPI5 speech output, Win32 process controls, desktop screen capture, and Windows Startup automation.

---

## ✨ Features

- 🧠 **Gemini 2.5 Flash AI Brain**: Integrated with Google's latest `google-genai` SDK for intelligent, character-driven voice responses (always addresses you as *Sir* or *Boss*).
- 🎙️ **Hands-Free Speech Engine**: Wake-word listening (`"JARVIS"`) with real-time speech recognition (`speech_recognition`) and offline voice synthesis (`pyttsx3`).
- 👁️ **Desktop Vision Analysis**: Captures desktop screenshots (`pyautogui` & `Pillow`) and provides brief or detailed summaries using Gemini Vision.
- ⚡ **Proactive Level-2 Suggestions**: Recommends clever next steps after executing commands and waits for your verbal permission to proceed.
- 📁 **App & File Control**: Dynamically launches applications (`notepad`, `chrome`, `code`, `calc`), finds files across Desktop/Documents, or opens search fallback.
- 📝 **Voice Note-Taking**: Dictate quick notes that automatically append to `jarvis_notes.txt` on your desktop.
- 🛡️ **Robust Error Handling**: Exception guards for process termination (`psutil`), screen grab failures, and API key fallbacks.

---

## 🛠️ Prerequisites

- **Python**: 3.10 or higher (Tested on Python 3.14)
- **OS**: Windows 10 / 11 (uses Windows SAPI5 audio and winsound)
- **Gemini API Key**: Obtain a free API key from [Google AI Studio](https://aistudio.google.com/)

---

## 🚀 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sarthakbagul40-rgb/J.A.R.V.I.S..git
   cd J.A.R.V.I.S
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the project root folder:
   ```env
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```

---

## 🎮 Usage

### Running JARVIS
Run directly from terminal:
```bash
python main.py
```
Or double-click **`run_jarvis.bat`** to launch in a batch terminal.

### Starting JARVIS on Windows Boot
To automatically launch JARVIS when Windows starts:
```powershell
powershell -ExecutionPolicy Bypass -File create_shortcut.ps1
```
This creates a startup shortcut in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`.

---

## 🗣️ Voice Commands Guide

| Category | Example Voice Command | Description |
| :--- | :--- | :--- |
| **Wake Word** | *"JARVIS"* | Activates listener (*"Yes boss?"*) |
| **Open App** | *"Open notepad"* / *"Open code"* | Launches applications or desktop files |
| **Close App** | *"Close chrome"* / *"Close notepad"* | Safely terminates target process |
| **Search** | *"Search latest AI news"* | Performs web search |
| **Take Notes** | *"Note down update meeting at 3 PM"* | Saves timestamped note to `jarvis_notes.txt` |
| **Screenshot** | *"Take a screenshot"* | Saves screenshot to your desktop |
| **Analyze Screen**| *"Analyze this screen"* / *"Summarize this in notepad"* | Analyzes desktop display via Gemini Vision |
| **General Q&A** | *"Explain quantum computing briefly"* | Answers using JARVIS personality |

---

## 📂 Project Structure

```text
J.A.R.V.I.S/
├── main.py              # Main assistant loop, audio engine, vision & Gemini logic
├── requirements.txt     # Python dependency manifest
├── run_jarvis.bat       # Portable Windows launcher batch script
├── create_shortcut.ps1  # Windows Startup shortcut generator script
├── .env                 # API Key environment configuration (git-ignored)
└── .gitignore           # Git ignore rules
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
