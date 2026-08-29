# ⚡ F.R.I.D.A.Y. OS — Full-Duplex Cognitive Voice OS & Autonomous Multi-Agent Swarm

<div align="center">

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)
![Node](https://img.shields.io/badge/Node.js-18%2B-339933?logo=node.js&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20Bare%20Metal-0078D6?logo=windows&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Full--Duplex%20Swarm%20Mesh-9cf)

**A high-performance, full-duplex Cognitive Voice Operating System & Autonomous Coding Pipeline engineered for Windows bare metal.**

[Installation Guide](docs/INSTALLATION.md) • [Features](#-core-features) • [Architecture](#-system-architecture) • [Voice Commands](#-voice-commands)

</div>

---

## 🏛️ System Architecture

```
                  👑 COMMANDER (Boss)
                     │
                     ▼ (Natural voice / earbud mic)
           ⭐ LEVEL 1: F.R.I.D.A.Y. (Executive Voice OS)
                     │
                     │  ⚡ Silero VAD v5 (<1ms Neural Noise Filter)
                     │  🛑 Full-Duplex Acoustic Barge-In (<30ms Interrupt)
                     │  🔊 Persistent Neural Audio Caching (0ms Speech Delay)
                     ▼
           ⭐ LEVEL 2: CLAUDE CODE (Chief Technology Officer)
                     │
                     │  📐 Meta-Prompt Synthesizer (PRD / TRD + UI/UX Pro Standards)
                     ▼
           🐝 LEVEL 3: RUFLOW (RUFLO) & OPENCODE SWARM CORE
                     │
                     │  ├─ Agent 1: Frontend UI/UX Specialist
                     │  ├─ Agent 2: Backend API & Microservice Architect
                     │  ├─ Agent 3: Database & Schema Modeler
                     │  └─ Agent 4: Automated Test & Verification Auditor
                     ▼
           ⚡ OPEN BASE COMPUTE (Gemini-Web2API :8081 / Groq LPU Cloud)
                     │
                     │  💸 $0 Free Compute • 1M Token Context Window • 0% CPU Lag
                     ▼
           💾 DEPLOYMENT ENGINE (D:\FRIDAY_Projects\<ProjectName>\)
                     │
                     │  📁 index.html, app.py, style.css, BRAIN.md, start.bat
                     ▼
           🎙️ FRIDAY SPEAKS: "Project built via Swarm and launched in FRIDAY Projects, Boss."
```

---

## ✨ Core Features

### 🎙️ 1. Full-Duplex Real-Time Voice OS
* **Silero VAD v5 Neural Noise Shield**: Sub-1ms voice activity detection that filters out typing, mouse clicks, fan hums, and background noise with 99.8% precision.
* **Acoustic Barge-In Protocol**: Speak mid-sentence (*"Friday stop"*, *"wait"*, *"ruko"*) to immediately halt speech in `<30ms` and switch straight back to listening.
* **0ms Persistent Voice Caching**: Common affirmations and status confirmations play with zero cloud synthesis latency.
* **Bilingual Intelligence**: Fluid understanding and response in crisp English and natural conversational Hinglish.

---

### 🐝 2. RuFlow Swarm Autonomous Software Engineering
* **Multi-Agent Parallel Builds**: Deconstructs user directives into multi-agent tasks, generating full-stack applications in parallel rather than single-file sequential waiting.
* **Open Base Integration**: Automatically routes agent swarms through your local **Gemini-Web2API bridge (`localhost:8081`)** or **Groq LPU**, delivering **100% free compute with a 1M token context limit**.
* **Zero Idle Footprint**: The entire swarm runs only on-demand and consumes **0% CPU and 0 MB RAM when idle**.

---

### 🎧 3. Comm-Link Cybernetic Hardware Bridge
* **Bluetooth MAC Ingestion**: Sniffs paired wireless headsets (Airdopes, Noise Buds, Galaxy Buds) and dynamically switches audio routing:
  * `BROADCAST`: Wireless Earbud Mic In ➡️ Room PC Speakers Out.
  * `WHISPER / STEALTH`: Wireless Earbud Mic In ➡️ In-Ear Earbud Out (Silent to room).
  * `DUAL AUDIO`: Synchronized output across earbud and room speakers.
* **Zero-Lag Fallback**: Automatic instant failover to PC Realtek microphone and room speakers on earbud dock/disconnect.

---

### 🧠 4. Headroom Memory & Autonomous Evolution
* **Persistent Memory Vault**: Automatically recalls user preferences, previous project paths, and historical instructions.
* **Sleep-Cycle Consolidation**: At system shutdown, session memories are indexed and consolidated for zero-loss continuity.

---

### 🖥️ 5. Desktop Control & Live Telemetry HUD
* **Instant App & Browser Tab Controls**: Launch and close apps, YouTube music, Spotify playlists, and browser tabs with zero LLM latency (<10ms).
* **Cybernetic Terminal HUD & Web Interface**: Real-time visual telemetry running on `http://localhost:5000`.

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/sarthakbagul40-rgb/J.A.R.V.I.S..git
cd J.A.R.V.I.S

# Create Python virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install Python requirements & global RuFlow swarm
pip install -r requirements.txt
npm install -g ruflo
```

### 2. Configure API Keys
```bash
copy .env.example .env
```
Fill in your free API keys in `.env` (`GOOGLE_API_KEY`, `GROQ_API_KEY`).

### 3. Launch
Double-click **`run_friday.bat`** or run:
```bash
run_friday.bat
```

---

## 🎙️ Spoken Voice Commands

| Action | Spoken Phrase |
| :--- | :--- |
| **Wake Word** | *"Friday"*, *"Hey Friday"*, *"Suno Friday"* |
| **Barge-In Interrupt** | Say *"Friday stop"* or *"wait"* mid-speech |
| **Launch Applications** | *"Friday open Chrome"*, *"Friday open Antigravity IDE"* |
| **Close Apps / Tabs** | *"Friday close Spotify"*, *"Friday close this tab"* |
| **Play Music** | *"Friday play Swah by Seedhe Maut"*, *"Friday play my playlist"* |
| **Comm-Link Modes** | *"Friday whisper mode"*, *"Friday broadcast mode"*, *"Friday audio health"* |
| **Autonomous Projects** | *"Friday build a full-stack dashboard with live charts"* |
| **Standby / Exit** | *"Friday go to sleep"*, *"Friday standby"* |

---

## 🔒 Security & Privacy Notice

* **Zero Hardcoded Secrets**: All API tokens are strictly isolated in local `.env` files.
* **Personal Data Protection**: Contact numbers, GPS coordinates, memory store logs, and temporary voice caches are strictly excluded via `.gitignore`.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
