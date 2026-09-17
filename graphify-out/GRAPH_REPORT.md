# Graph Report - J.A.R.V.I.S  (2026-09-17)

## Corpus Check
- 77 files · ~69,440 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1164 nodes · 1789 edges · 66 communities (56 shown, 8 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 68 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ce58f803`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- gemini_web2api.py
- NeuralVoiceEngine
- SystemAccessController
- HeadroomMemoryEngine
- rate_limiter.py
- RalphFlowEngine
- processCommand
- AgentShieldAuditor
- ValkyriePersonalityEngine
- server.py
- CommLinkEngine
- web_hub.py
- main.py
- tools.py
- speak
- gemini.py
- NeuralHearingEngine
- MCPDesignBridge
- BackgroundCoProcessor
- code_reviewer.py
- GeminiHandler
- BooksAdapter
- log
- CodebaseAuditor
- GeospatialMapsEngine
- VisionService
- WhatsAppEngine
- play_sound
- GraphifyEngine
- DesignBlueprintEngine
- AutonomousCodingEngine
- RuntimeSelfHealer
- 🚀 Step-by-Step Installation
- claude_bridge.py
- gemini-web2api
- PromptEngineeringSynthesizer
- GitHubDiscoveryEngine
- ClaudeCodeExecutor
- MovieBoxEngine
- opencode.json
- vision_hub.py
- coding_hub.py
- Any
- format_search_results
- ._finalize_deployment
- MovieBox-TUI
- chat_hub.py
- graphify.js
- install_autostart.py
- gemini-web2api
- 3. Core Subsystem Deep-Dive
- F.R.I.D.A.Y. OS — CLAUDE CODE (CTO & LEAD ENGINEER SPECIFICATION)
- 2. Style Presets Catalog
- Cybersecurity Sentinel (Anthropic Cyber Skills Protocol)
- Diagram Design (Editorial HTML + SVG)
- Gemini-Web2API Bridge
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md
- VikingVaultEngine
- AegisMediaEngine
- test_aegis_interactive.py
- AutonomousBrowserAgent
- diagnose_all_systems.py

## God Nodes (most connected - your core abstractions)
1. `speak()` - 66 edges
2. `play_sound()` - 57 edges
3. `AegisMediaEngine` - 26 edges
4. `HeadroomMemoryEngine` - 23 edges
5. `AutonomousCodingEngine` - 19 edges
6. `VikingVaultEngine` - 19 edges
7. `SystemAccessController` - 18 edges
8. `gemini-web2api` - 17 edges
9. `GeminiHandler` - 16 edges
10. `GeminiHandler` - 16 edges

## Surprising Connections (you probably didn't know these)
- `processCommand()` --calls--> `play_sound()`  [EXTRACTED]
  main.py → core/hubs/base.py
- `processCommand()` --calls--> `speak()`  [EXTRACTED]
  main.py → core/hubs/base.py
- `processCommand()` --calls--> `get_ai_response()`  [EXTRACTED]
  main.py → core/hubs/chat_hub.py
- `processCommand()` --calls--> `dispatch_media_intent()`  [EXTRACTED]
  main.py → core/hubs/media_hub.py
- `processCommand()` --calls--> `dispatch_vision_intent()`  [EXTRACTED]
  main.py → core/hubs/vision_hub.py

## Import Cycles
- None detected.

## Communities (66 total, 8 thin omitted)

### Community 0 - "gemini_web2api.py"
Cohesion: 0.08
Nodes (40): account_prefix(), apply_chat_persistence_flags(), clean_gemini_text(), decode_data_url(), extract_response_text(), fetch_latest_bl(), gemini_stream_generate(), gemini_stream_generate_iter() (+32 more)

### Community 1 - "NeuralVoiceEngine"
Cohesion: 0.06
Nodes (22): EmotionProsodyEngine, _get_pygame(), LanguageProfileDetector, NeuralVoiceEngine, Analyzes text content to automatically route to the matching native neural…, Determines optimal voice profile ensuring continuous voice identity., Real-time zero-latency (<0.01ms) Affective Emotion & Prosody Analyzer.…, Calculates dynamic prosody modulation (rate, pitch, volume) matching Friday's… (+14 more)

### Community 2 - "SystemAccessController"
Cohesion: 0.06
Nodes (21): Any, Omni-System Controller for J.A.R.V.I.S. Provides total computer control: multi-…, Fast parallel-safe file search across user folders and drives with depth & time…, Reads the textual content of a file., Safely replaces text in a file after obtaining explicit confirmation., Safely writes or appends content to a file after obtaining confirmation., Safely deletes a file after obtaining explicit confirmation., Captures the entire desktop display, saves to Desktop/Screenshots/ with… (+13 more)

### Community 3 - "HeadroomMemoryEngine"
Cohesion: 0.07
Nodes (23): HeadroomMemoryEngine, Any, Completely purges and resets all persistent memories, vaults, profiles, and…, Retrieves the structured Living User Dossier: Identity, Tech DNA, Media Taste,…, Automatic Deduplication Engine: Normalizes facts, trims duplicate phrases, and…, Manages persistent long-term memory, rolling conversation buffer, and context…, Detects implicit or explicit remember commands and commits them with high…, Retrieves top relevant long-term memories using BM25 relevance scoring. (+15 more)

### Community 4 - "rate_limiter.py"
Cohesion: 0.10
Nodes (14): DebounceCooldown, exponential_backoff(), OutgoingThrottler, rate_limit(), Rate Limiting and Throttling Subsystem for J.A.R.V.I.S. Provides: 1. In-memory…, Decorator for retrying unstable network calls with exponential backoff., Debounces rapid duplicate events (e.g. repeated audio triggers)., Returns True if cooldown has elapsed since the last accepted trigger. (+6 more)

### Community 5 - "RalphFlowEngine"
Cohesion: 0.17
Nodes (9): Any, RalphFlowEngine, Autonomous Critic Gatekeeper (Ralph Review Loop): Audits generated codebase…, Autonomous goal-completion loop that runs until all milestone tasks pass., Initializes a new Ralph task queue from a feature specification., Loads active Ralph tasks., Finds the next incomplete task., Marks a task complete and advances the loop. (+1 more)

### Community 6 - "processCommand"
Cohesion: 0.13
Nodes (15): handleSuggestion(), get_system_stats(), handle_note(), handle_status(), note_down(), Appends dictation to Desktop friday_notes.txt and displays it., Calculates CPU load, memory usage, and battery percentages., Speaks real-time hardware status. (+7 more)

### Community 7 - "AgentShieldAuditor"
Cohesion: 0.20
Nodes (9): AgentShieldAuditor, Any, Audits non-python source files (.html, .js, .json, .env, .md) for credential…, Polymorphic file audit dispatcher., Audits all modified files in the working directory before commit., Enterprise-grade code security, secret detection, and architectural compliance…, Determines if a matched pattern is an intentional documentation placeholder., Scans code or text content for hardcoded secrets, tokens, and credentials. (+1 more)

### Community 8 - "ValkyriePersonalityEngine"
Cohesion: 0.09
Nodes (14): Any, F.R.I.D.A.Y. OS 10.0: Project Valkyrie Persona & Behavioral Engine Implements:…, Evaluates a proposed idea or architecture. If it detects obvious over-…, Monitors active coding past 02:30 AM and enforces safe protective disciplinary…, The living soul, debate partner, and protective guardian of F.R.I.D.A.Y. OS…, Triggers safe Windows workstation lock (Win + L) without data loss., Safely dims monitor brightness via PowerShell WMI., Refreshes state from disk. (+6 more)

### Community 9 - "server.py"
Cohesion: 0.14
Nodes (15): find_config(), load_config(), Configuration management., Load config from JSON file., Search for config file in standard locations., gemini-web2api: Gemini Web to OpenAI API proxy., main(), Entry point: python -m gemini_web2api (+7 more)

### Community 10 - "CommLinkEngine"
Cohesion: 0.12
Nodes (12): CommLinkEngine, Any, Scans speech_recognition microphone endpoints to bind directly to Bluetooth…, Returns specialized acoustic parameters for Earbud vs PC Mic hearing., Monitors Bluetooth connection transitions in the background with zero CPU…, Switches Comm-Link routing mode between Broadcast, Whisper, and Dual Audio., Cycles between Broadcast and Whisper modes (ideal for Double-Tap triggers)., Manages Bluetooth Comm-Link audio routing, connection detection, and mode… (+4 more)

### Community 11 - "web_hub.py"
Cohesion: 0.08
Nodes (29): open_in_brave(), F.R.I.D.A.Y. OS 9.0: Autonomous Headless Web-Browsing Agent (Pillar 3) Performs…, Opens a target URL in Brave browser if available, or system default browser as…, get_ai_response(), Tier 1 (Groq Cloud): Ultra-fast Qwen/Llama LPU reasoning (<0.6s latency). Tier…, battery_monitor_sentinel(), Background daemon thread monitoring battery health., get_person_location() (+21 more)

### Community 12 - "main.py"
Cohesion: 0.08
Nodes (27): F.R.I.D.A.Y. Cybernetic Comm-Link Subsystem Autonomous Hardware Bridge for…, collect_continuous_speech(), drain_audio_queues(), get_speaker(), F.R.I.D.A.Y. Honeycomb Base Infrastructure Shared acoustic soundboard, neural…, Flushes stale audio frames and acoustic echo from input queues., Continuous Speech Stream Accumulator: Allows Boss to speak naturally at their…, Returns a thread-local instance of SAPI with female voice (Zira/FRIDAY). (+19 more)

### Community 13 - "tools.py"
Cohesion: 0.15
Nodes (18): _build_tool_choice_instruction(), build_tool_prompt(), _compress_b64_if_needed(), _decode_data_url(), google_contents_to_prompt(), _google_tool_choice_instruction(), _image_from_part(), _image_from_url() (+10 more)

### Community 14 - "speak"
Cohesion: 0.06
Nodes (41): Speaks out loud using Movie-Grade Multilingual Neural Voice with SAPI fallback., speak(), close_app(), find_file(), find_system_shortcut(), handle_audio_health(), handle_broadcast_mode(), handle_close() (+33 more)

### Community 15 - "gemini.py"
Cohesion: 0.20
Nodes (18): _account_prefix(), _apply_chat_persistence_flags(), _build_headers(), _build_payload(), clean_text(), extract_response_text(), _extract_texts_from_line(), generate() (+10 more)

### Community 16 - "NeuralHearingEngine"
Cohesion: 0.11
Nodes (14): AudioData, NeuralHearingEngine, F.R.I.D.A.Y. Neural Ear Sensors & Multilingual Hearing Engine Powered by…, Loads INT8 CPU-quantized Whisper model for instant zero-cloud transcription., Context-aware phonetic normalizer repairing common English STT substitutions…, Sub-millisecond Neural Voice Activity Detector (Silero VAD v5 ONNX)., Enhances dynamic range and gain for low-energy audio frames (e.g. from in-ear…, Ultra-fast multilingual audio transcription with Silero VAD noise filtering:… (+6 more)

### Community 17 - "MCPDesignBridge"
Cohesion: 0.25
Nodes (6): MCPDesignBridge, Any, Direct bridge to Google Stitch Design Systems & UI/UX Pro Max Tokens. Ensures…, Dynamically matches project query to optimal Google Stitch + UI/UX Pro design…, Synthesizes a direct, comprehensive design directive enforcing Google Stitch +…, Directly wires project workspace to UI/UX Pro Max MCP and Google Stitch.…

### Community 18 - "BackgroundCoProcessor"
Cohesion: 0.13
Nodes (11): BackgroundCoProcessor, Any, Thread, F.R.I.D.A.Y. Background Co-Processor & Intelligence Distillation Engine Powered…, Distills raw conversation turns into structured Dual-Partition memory vaults:…, Dispatches memory distillation in a background thread to keep FRIDAY 100%…, Synthesizes raw web search dumps and news feeds into 1-2 punchy, spoken…, Synthesizes visual scan observations and live web pricing/specifications into a… (+3 more)

### Community 20 - "GeminiHandler"
Cohesion: 0.23
Nodes (8): Resolve model name to (name, mode_id, think_mode, error, extra_fields). Unknown…, resolve_model(), GeminiHandler, BaseHTTPRequestHandler, Upload images and return list of file references. Returns None if no images., _upload_images(), parse_tool_calls(), Extract tool_call blocks. Returns (clean_text, tool_calls_list).

### Community 21 - "BooksAdapter"
Cohesion: 0.10
Nodes (16): BooksAdapter, Any, F.R.I.D.A.Y. OS 10.0: PROJECT A.E.G.I.S. 6th Media Adapter - Books & Neural…, Extracts text from PDF and segments by chapter markers or page chunks., Parses EPUB archive using native zipfile and xml parsing (zero dependencies)., Segments plain text or Markdown files by markdown headers or chapter keywords., The 6th Aegis Media Adapter: Literary Ingestion and Continuous Neural Narration…, Starts or resumes neural audio narration in an asynchronous background thread. (+8 more)

### Community 22 - "log"
Cohesion: 0.26
Nodes (13): _get_ssl_ctx(), load_cookie(), log(), make_sapisidhash(), Load cookie from file with mtime-based caching., _cached_page_tokens(), fetch_image_bytes(), _get_page_tokens() (+5 more)

### Community 23 - "CodebaseAuditor"
Cohesion: 0.20
Nodes (8): CodebaseAuditor, Any, F.R.I.D.A.Y. Deep Codebase Health & Vulnerability Auditor Performs deep AST…, Displays rich cybernetic health diagnostic in terminal and speaks precise issue…, Executes autonomous self-healing protocol: 1. Auto-spawns offline background…, Deep line-by-line source code and subsystem vulnerability auditor., Checks if a daemon port is listening., Scans every line of code across the workspace.

### Community 24 - "GeospatialMapsEngine"
Cohesion: 0.18
Nodes (9): GeospatialMapsEngine, Any, Displays location card, launches in Brave, and speaks summary., F.R.I.D.A.Y. OS 10.0: God's Eye Tactical Orbital Reconnaissance. Resolves…, Manages map routing, distance computation, and live navigation links., Resolves place name into (lat, lon, display_name)., Calculates distance, duration, and builds Google Maps navigation link., Searches for a location, place of interest, or nearby spots on Google Maps. (+1 more)

### Community 26 - "VisionService"
Cohesion: 0.15
Nodes (10): _get_cv2(), _get_pyautogui(), Any, Omni-Vision System for J.A.R.V.I.S. Provides Dual-Channel Vision: Desktop…, Streams multimodal vision reasoning from Google Gemini 2.5 Flash Vision., Analyzes a product in the webcam frame, detecting branding or predicting…, Manages screen grabbing, webcam frame acquisition, and multimodal vision…, Captures the active screen display and returns a Base64-encoded JPEG Data URI. (+2 more)

### Community 27 - "WhatsAppEngine"
Cohesion: 0.16
Nodes (8): F.R.I.D.A.Y. Cybernetic WhatsApp Messaging & Contact Automation Engine Supports…, Parses and dispatches a WhatsApp message using Native WhatsApp Desktop with…, Manages natural language WhatsApp message parsing, native desktop dispatch, and…, Loads persistent contact book from disk., Saves or updates a contact's phone number., Extracts (contact_name, message_text) from spoken natural language commands.…, Waits for WhatsApp Desktop window to open and focuses input, then presses Enter…, WhatsAppEngine

### Community 28 - "play_sound"
Cohesion: 0.08
Nodes (35): play_sound(), Plays futuristic offline sound effects in background thread to eliminate…, control_media(), dispatch_media_intent(), handle_anime_lore(), handle_book_next_chapter(), handle_book_prev_chapter(), handle_book_status() (+27 more)

### Community 29 - "GraphifyEngine"
Cohesion: 0.16
Nodes (10): GraphifyEngine, Any, F.R.I.D.A.Y. OS 10.0: Graphify Deterministic AST Knowledge Graph Service Turns…, Instant Zero-Latency AST Reflex: Inspects questions regarding F.R.I.D.A.Y.'s…, Manages AST codebase knowledge graphs and zero-hallucination symbol resolution., Returns high-level graph topology stats., Runs graphify to generate or refresh graph.json and graph.html., Builds sub-millisecond in-memory inverted indices for symbol lookup and edge… (+2 more)

### Community 30 - "DesignBlueprintEngine"
Cohesion: 0.14
Nodes (10): DesignBlueprintEngine, Any, Unified Design Intelligence & Intent-Adaptive Blueprint Compiler for…, Detects application archetype to separate utilities from e-commerce stores.…, F.R.I.D.A.Y. autonomously evaluates requirements and chooses the technology…, Detects domain preset from user instruction., Synthesizes an archetype-aware master prompt. Enforces focused minimalist tool…, Synthesizes backend Python SQLite / FastAPI architecture prompt. (+2 more)

### Community 31 - "AutonomousCodingEngine"
Cohesion: 0.13
Nodes (10): AutonomousCodingEngine, Synthesizes the 7-Stage Cumulative Pre-Flight Cascade before code generation:…, Determines whether to route to Mode 1 (Lightning Core, <5s) or Mode 2 (Iron…, Audits, formats, and writes extracted code blocks to target directory., Dual-Mode Autonomous Multi-Agent Coding Orchestrator: - Mode 1: Lightning Core…, r"""Master controller orchestrating multi-language code generation, prompt…, Extracts (language, code) tuples from markdown code fences, HTML blocks, or raw…, Derives a clean, readable, concise project slug from user instruction. (+2 more)

### Community 32 - "RuntimeSelfHealer"
Cohesion: 0.17
Nodes (8): Any, F.R.I.D.A.Y. OS 9.0: Autonomous Runtime Debugger & Self-Healing Watcher (Pillar…, Monitors a launched subprocess. If it terminates with non-zero exit code or…, r""" Autonomous Crash Interceptor and Code Patching Engine. Continuously…, Parses standard Python traceback to extract failing file, line number, and…, Synthesizes a clean code patch using local repair engines (OpenCode / Groq /…, RuntimeSelfHealer, Popen

### Community 33 - "🚀 Step-by-Step Installation"
Cohesion: 0.07
Nodes (27): 1. Clone the Repository, 2. Create and Activate a Python Virtual Environment, 3. Install Python Dependencies, 4. Install RuFlow Multi-Agent Swarm CLI (Global), 5. Configure Environment Variables (`.env`), 6. Verify System Calibration, 🎙️ Core Voice Commands, 🛠️ F.R.I.D.A.Y. OS — Installation & Setup Guide (+19 more)

### Community 35 - "claude_bridge.py"
Cohesion: 0.20
Nodes (7): Universal Multi-Language Autonomous Coding Engine & Claude Code Bridge for…, ===============================================================================…, ===============================================================================…, print_code(), Renders sleek, clean progress card for autonomous project creation stages with…, Renders formatted syntax-highlighted code box., render_project_stage()

### Community 36 - "gemini-web2api"
Cohesion: 0.07
Nodes (27): Acknowledgments, Authenticated account path and XSRF token, Available Models, bash / macOS / Linux, Cherry Studio / ChatBox / any OpenAI client, Client Configuration, Configuration, curl (+19 more)

### Community 38 - "PromptEngineeringSynthesizer"
Cohesion: 0.25
Nodes (5): PromptEngineeringSynthesizer, Delegates domain design token synthesis to design_blueprint & mcp_design_bridge., Compiles raw user command into Stitch-UX Neural Blueprint Master Prompt in <1ms…, Chief Architect & Meta-Prompt Compiler for F.R.I.D.A.Y. Compiles raw voice…, Identifies target programming language with explicit priority for fullstack and…

### Community 39 - "GitHubDiscoveryEngine"
Cohesion: 0.22
Nodes (6): GitHubDiscoveryEngine, Any, F.R.I.D.A.Y. GitHub Intelligence & Repository Discovery Subsystem Enables real-…, Searches, ranks, and analyzes repositories directly from GitHub., Searches GitHub for top repositories matching the query., Displays rich terminal table and speaks executive summary.

### Community 40 - "ClaudeCodeExecutor"
Cohesion: 0.31
Nodes (5): ClaudeCodeExecutor, Executes synthesized master prompts with OpenCode Multi-Model Engine (DeepSeek…, Locates the global claude CLI binary on the system., Locates the global RuFlow/Ruflo CLI binary on the system with npx fallback., Locates the global OpenCode CLI binary on the system.

### Community 41 - "MovieBoxEngine"
Cohesion: 0.13
Nodes (11): MovieBoxEngine, Any, ===============================================================================…, Primary playback trigger for movies and shows. Launches MovieBox with…, Manages MovieBox-Tui integration for ad-free, 1080p Hollywood, Anime, and TV…, Locates the compiled moviebox-tui executable., Locates the MPV player executable., Returns True if moviebox binary exists. (+3 more)

### Community 43 - "vision_hub.py"
Cohesion: 0.23
Nodes (11): Extracts complete natural sentences from streaming AI token buffer without…, stream_audio_chunks(), dispatch_vision_intent(), handle_camera_vision(), handle_screen_vision(), handle_take_screenshot(), F.R.I.D.A.Y. Honeycomb Vision Hub Optical sensors: screen display perception,…, Captures and archives full screen to Desktop/Screenshots/. (+3 more)

### Community 44 - "coding_hub.py"
Cohesion: 0.13
Nodes (18): dispatch_coding_intent(), handle_code_review_cmd(), handle_coding_command(), handle_gods_eye_recon_cmd(), handle_graphify_cmd(), handle_graphify_reflex(), handle_project_status(), is_coding_intent() (+10 more)

### Community 45 - "Any"
Cohesion: 0.25
Nodes (5): Any, Thread, Dispatches heavy coding and multi-file projects to Claude Code CTO in an…, Executes across Level 2 Claude Code (CTO with UI/UX Pro MCP), RuFlow Multi-…, Direct ultra-fast fallback to Groq LPU Cloud (Qwen 3.8 / GPT-OSS) for instant…

### Community 46 - "format_search_results"
Cohesion: 0.40
Nodes (4): format_search_results(), Any, F.R.I.D.A.Y. Web Intelligence Utilities Formats search engine results into…, Formats DuckDuckGo / Bing results into a prompt-friendly string.

### Community 47 - "._finalize_deployment"
Cohesion: 0.40
Nodes (3): Generates start.bat launcher, requirements.txt, BRAIN.md manifest, logs memory,…, Renders sleek success card upon project deployment., render_project_complete()

### Community 48 - "MovieBox-TUI"
Cohesion: 0.14
Nodes (13): Android (Termux), Contributing, Disclaimer, Documentation, Features, Installation, License, macOS and Linux (+5 more)

### Community 49 - "chat_hub.py"
Cohesion: 0.13
Nodes (13): Headroom Memory & Context Optimization Engine for J.A.R.V.I.S. Provides…, ensure_gemini_web2api_running(), F.R.I.D.A.Y. Honeycomb Chat Hub Cognitive reasoning core: Groq LPU Cloud (Tier…, Streams ultra-low latency response chunks from Groq LPU Cloud (sub-second TTFT)., Streams response chunks from local OmniRoute multi-provider gateway., Auto-heals the Gemini-Web2API daemon on port 8081 if stopped., Streams response chunks from local Gemini-Web2API daemon on port 8081., stream_gemini_web2api_tokens() (+5 more)

### Community 60 - "3. Core Subsystem Deep-Dive"
Cohesion: 0.14
Nodes (13): 1. Executive System Architecture, 2. Subsystem Directory Hierarchy, 3.1. Acoustic Hearing Engine (`core/hearing_service.py`), 3.2. 3-Tier Cognitive Reasoning Stack (`main.py`), 3.3. Multimodal Optical Vision (`core/vision_service.py`), 3.4. Two-Stage Pipelined Audio Prefetching (`core/omnivoice_service.py`), 3.5. Mem0 Dynamic Relational Memory (`core/mem0_service.py` & `core/headroom_memory.py`), 3.6. Command Router & Direct Automation Matrix (`main.py`) (+5 more)

### Community 62 - "F.R.I.D.A.Y. OS — CLAUDE CODE (CTO & LEAD ENGINEER SPECIFICATION)"
Cohesion: 0.17
Nodes (11): 🎨 1. UI/UX PRO MCP INTEGRATION, 🌐 2. GEMINI-WEB2API REPOSITORY & REVERSE-ENGINEERED API, 🧠 3. HEADROOM MEMORY & PERSISTENT MEMORY VAULT, ⚙️ 4. RUFLOW (RUFLO) & OPENCODE SWARM INTEGRATION, 🎧 6. COMM-LINK CYBERNETIC EARBUD PROTOCOL, 🦹 7. PONYTAIL & SUPERPOWERS ENGINEERING DISCIPLINE, 🕸️ 8. GRAPHIFY & OPENVIKING ZERO-HALLUCINATION CONTEXT, 🔄 9. RALPH FLOW & CODERABBIT SAFETY GATEWAY (+3 more)

### Community 63 - "2. Style Presets Catalog"
Cohesion: 0.25
Nodes (7): 1. Core Aesthetic Principles (Zero-Boring UI), 2. Style Presets Catalog, 3. UI/UX Pro Design Checklist, A. Glassmorphism & Cybernetic HUD, B. Bento Grid Layout, C. Micro-Interactions & Transitions, UI/UX Pro Design Intelligence & Engineering Guide

### Community 67 - "Cybersecurity Sentinel (Anthropic Cyber Skills Protocol)"
Cohesion: 0.50
Nodes (3): Core Inspection Domains, Cybersecurity Sentinel (Anthropic Cyber Skills Protocol), When to Activate

### Community 68 - "Diagram Design (Editorial HTML + SVG)"
Cohesion: 0.50
Nodes (3): Core Principles, Diagram Design (Editorial HTML + SVG), Supported Layout Types

### Community 69 - "Gemini-Web2API Bridge"
Cohesion: 0.50
Nodes (3): Capabilities, Gemini-Web2API Bridge, Usage Example (Python)

### Community 76 - "VikingVaultEngine"
Cohesion: 0.09
Nodes (17): Any, Returns micro-abstracts (~100 tokens each) for instant relevance scanning., Loads an L1 overview for planning without reading full L2 data., Loads full L2 raw data on demand., Loads F.R.I.D.A.Y.'s live emotional and grievance state., Persists updated personality state., Loads Boss's persistent media taste matrix, affinities, and playback…, Persists updated taste matrix to disk. (+9 more)

### Community 77 - "AegisMediaEngine"
Cohesion: 0.07
Nodes (26): AegisMediaEngine, Any, Sends a JSON-IPC command to MPV over the Windows named pipe in <5ms., Queries a property from MPV via named pipe JSON-IPC., Acoustic Focus: Dips media volume in <5ms when Boss or F.R.I.D.A.Y. speaks., Restores media volume after speech completes in <5ms., Stops playback and ensures zero lingering processes., Toggles play / pause state. (+18 more)

### Community 78 - "test_aegis_interactive.py"
Cohesion: 0.06
Nodes (28): LoreTelemetryEngine, Any, F.R.I.D.A.Y. OS 10.0: PROJECT A.E.G.I.S. Lore & Cine-Companion Engine…, Queries TVMaze for show synopsis, genres, and premiere date., Provides encyclopedic lore, episode recaps, and live media companion…, Retrieves the exact plot synopsis for a specific episode for 'Previously on...'…, Fetches live song lyrics without API keys., Synthesizes a punchy 1-2 sentence spoken answer about what the user is watching. (+20 more)

### Community 79 - "AutonomousBrowserAgent"
Cohesion: 0.16
Nodes (8): AutonomousBrowserAgent, Any, Executes parallel multi-page deep research: searches DDG, fetches top 3 result…, F.R.I.D.A.Y. OS 10.0: Interactive Browser Automation via Playwright / Browser-…, High-level entry point to execute an autonomous web research or browser…, High-Speed Headless Web Intelligence & Extraction Agent. Navigates live web…, Fetches web page, removes boilerplate (navs, footers, ads, scripts), and…, Queries DuckDuckGo HTML endpoint without API keys, returning list of {title,…

### Community 81 - "diagnose_all_systems.py"
Cohesion: 0.28
Nodes (12): check_camera(), check_graphify(), check_health(), check_media_engine(), check_public_apis(), check_valkyrie_persona(), check_viking_vault(), main() (+4 more)

## Knowledge Gaps
- **91 isolated node(s):** `$schema`, `plugin`, `gemini-web2api`, `1. Core Aesthetic Principles (Zero-Boring UI)`, `A. Glassmorphism & Cybernetic HUD` (+86 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 592 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `speak()` connect `speak` to `processCommand`, `web_hub.py`, `main.py`, `coding_hub.py`, `vision_hub.py`, `chat_hub.py`, `play_sound`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `play_sound()` connect `play_sound` to `processCommand`, `web_hub.py`, `main.py`, `coding_hub.py`, `speak`, `vision_hub.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `AegisMediaEngine` connect `AegisMediaEngine` to `main.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `speak()` (e.g. with `handle_self_heal()` and `handle_route_navigation()`) actually correct?**
  _`speak()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `plugin`, `gemini-web2api` to the rest of the system?**
  _91 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `gemini_web2api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07811447811447811 - nodes in this community are weakly interconnected._
- **Should `NeuralVoiceEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.06342780026990553 - nodes in this community are weakly interconnected._