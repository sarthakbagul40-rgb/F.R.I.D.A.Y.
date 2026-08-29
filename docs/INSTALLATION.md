# 🛠️ F.R.I.D.A.Y. OS — Installation & Setup Guide

This guide provides step-by-step instructions to install, configure, and launch **F.R.I.D.A.Y. OS** on Windows bare metal.

---

## 📋 System Prerequisites

| Requirement | Specification |
| :--- | :--- |
| **Operating System** | Windows 10 / Windows 11 (64-bit) |
| **Python** | Python 3.10 to 3.12+ (Installed and added to system `PATH`) |
| **Node.js** | Node.js v18+ & `npm` (Required for RuFlow swarm engine) |
| **Memory (RAM)** | 8 GB RAM or higher (Tuned for ultra-lightweight ~105MB idle footprint) |
| **Microphone & Audio** | Working PC microphone or Bluetooth Earbuds (e.g. Airdopes / Noise Buds) |

---

## 🚀 Step-by-Step Installation

### 1. Clone the Repository
Open PowerShell or Command Prompt and clone the repository:
```bash
git clone https://github.com/sarthakbagul40-rgb/J.A.R.V.I.S..git
cd J.A.R.V.I.S
```

---

### 2. Create and Activate a Python Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3. Install Python Dependencies
Install all core neural, audio, and systems libraries:
```bash
pip install -r requirements.txt
```

---

### 4. Install RuFlow Multi-Agent Swarm CLI (Global)
Install the **RuFlow (Ruflo)** swarm orchestration engine via npm:
```bash
npm install -g ruflo
```
*(Verify installation by running `ruflo --version`)*

---

### 5. Configure Environment Variables (`.env`)
Copy the provided `.env.example` template into a new `.env` file:
```bash
copy .env.example .env
```

Open `.env` in any text editor and insert your free API keys:
```env
# Google Gemini API Key (Google AI Studio: https://aistudio.google.com/app/apikey)
GOOGLE_API_KEY=your_gemini_api_key_here

# Groq Cloud API Key (Ultra-Fast LPU Inference: https://console.groq.com/keys)
GROQ_API_KEY=your_groq_api_key_here

# Optional: OpenAI API Key
OPENAI_API_KEY=your_openai_key_here
```

---

### 6. Verify System Calibration
Run the automated system diagnostic test:
```bash
test_systems.bat
```
This tests your audio interfaces, memory engines, and cognitive dispatchers.

---

## 🎯 Launching F.R.I.D.A.Y.

Double-click **`run_friday.bat`** or execute in your terminal:
```bash
run_friday.bat
```

### 🌐 Web Telemetry HUD
Once started, open your browser to access the live futuristic telemetry HUD:
* **HUD URL**: `http://localhost:5000`

---

## 🎙️ Core Voice Commands

* **Wake Words**: *"Friday"*, *"Hey Friday"*, *"Suno Friday"*
* **App Control**: *"Friday open Chrome"*, *"Friday launch Antigravity IDE"*, *"Friday close Spotify"*
* **Music Playback**: *"Friday play Swah by Seedhe Maut"*, *"Friday play my playlist"*
* **System Control**: *"Friday volume up"*, *"Friday check battery"*, *"Friday take a note"*
* **Autonomous Coding**: *"Friday build a full-stack restaurant landing page"*
* **Comm-Link Audio**: *"Friday broadcast mode"*, *"Friday whisper mode"*, *"Friday audio health"*
* **Barge-In Interruption**: Say *"Friday stop"* or *"wait"* mid-speech to halt playback in `<30ms`.
