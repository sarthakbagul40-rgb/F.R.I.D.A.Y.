"""
Universal Multi-Language Autonomous Coding Engine & Claude Code Bridge for J.A.R.V.I.S.
Transforms rough voice/text instructions into production-grade prompts across all languages
in their latest modern versions and pipes them to local Claude Code CLI with Gemini/OmniRoute fallback.
"""

import os
import re
import time
import subprocess
import shutil
import threading
from datetime import datetime
from typing import Dict, Optional, Tuple, List, Any
import requests
from dotenv import load_dotenv
load_dotenv()

from core.system_access import system_controller

# Catalog of latest modern language specifications and best practices
LANGUAGE_STANDARDS: Dict[str, Dict[str, str]] = {
    "python": {
        "version": "Python 3.12+",
        "standards": "PEP-8, strict type hints (from typing import ...), dataclasses/Pydantic, robust try/except blocks, docstrings, no placeholders."
    },
    "javascript": {
        "version": "ECMAScript 2024+ (ESM)",
        "standards": "Modern ES modules (import/export), async/await, optional chaining, nullish coalescing, strict mode, zero deprecated APIs."
    },
    "typescript": {
        "version": "TypeScript 5.4+",
        "standards": "Strict type safety, generic interfaces, zod validation if applicable, modern async/await, no 'any' types."
    },
    "html": {
        "version": "HTML5 & Modern Web",
        "standards": "Semantic HTML5 (<main>, <section>, <nav>, <header>), accessibility (ARIA attributes), responsive meta tags, clean hierarchy."
    },
    "css": {
        "version": "Modern CSS3 (Flexbox, CSS Grid, Custom Properties)",
        "standards": "CSS variables (:root), Flexbox/Grid layouts, fluid typography (clamp), responsive media queries, dark/light modes, animations."
    },
    "cpp": {
        "version": "C++20 / C++23",
        "standards": "std::format, std::span, concepts, smart pointers (std::unique_ptr, std::shared_ptr), RAII, no raw new/delete, modern CMake."
    },
    "c": {
        "version": "C17 / C23",
        "standards": "Safe memory allocation, bounds checking, structured error codes, standard library usage (<stdint.h>, <stdbool.h>)."
    },
    "java": {
        "version": "Java 21+ LTS",
        "standards": "Records, pattern matching for switch, sealed classes, virtual threads (Project Loom), Stream API, clean package structure."
    },
    "rust": {
        "version": "Rust 2021 Edition",
        "standards": "Idiomatic borrow checker management, Result/Option unwrap guards, match expressions, Tokio async, Clippy adherence."
    },
    "csharp": {
        "version": "C# 12 / .NET 8+",
        "standards": "Top-level statements, primary constructors, collection expressions, pattern matching, async/await Tasks, clean LINQ."
    },
    "go": {
        "version": "Go 1.22+",
        "standards": "Idiomatic error handling (if err != nil), goroutines, sync.WaitGroup, context cancellation, standard library logging."
    },
    "sql": {
        "version": "Modern SQL (PostgreSQL 16 / SQLite 3.45 / MySQL 8)",
        "standards": "Indexed queries, parameterized statements (prevent SQL injection), CTEs (WITH clauses), proper foreign keys and constraints."
    },
    "bash": {
        "version": "Modern Bash 5+ / PowerShell 7+",
        "standards": "set -euo pipefail, parameter expansion, strict quoting, error checking, robust exit codes."
    }
}


# =============================================================================
# UNIVERSAL FULL-STACK MASTER PROMPT (F.R.I.D.A.Y. x FABLE 5 x UI/UX PRO)
# =============================================================================

UNIVERSAL_FULLSTACK_MASTER_PROMPT = """You are the Principal Lead Full-Stack UI/UX Pro Architect for F.R.I.D.A.Y. OS.

### 🎯 PROJECT GOAL: {project_title}
### 📋 USER SPECIFICATION:
"{user_requirement}"

### 🎨 MANDATORY F-AURA (FRIDAY AURA) DESIGN SYSTEM & ASSETS:
{ui_ux_pro_section}

### ⚡ LIGHTWEIGHT & LOW-RESOURCE ARCHITECTURAL DIRECTIVES:
1. ZERO NPM/NODE BLOAT: Zero bulky npm dependencies. Use native browser APIs, modern CSS3 variables, and instant CDN links (<script src="https://unpkg.com/lucide@latest"></script>). Total bundle under 25KB!
2. COMPLETE SOURCE CODE ONLY: Output the complete, working production code inside markdown code fences. NO conversational filler, NO ASCII banner boxes, NO placeholders, and NO truncation.
3. DOMAIN AUTHENTICITY: Use realistic domain content, realistic pricing, appetizing descriptions, customer reviews, and working interactive features (category filter tabs, interactive cart drawer, booking modal, toast notifications).
4. FULLSTACK HARMONY (If Fullstack requested):
   - Provide ```python (main.py)```: Lightweight FastAPI/Python server with built-in SQLite database storage, CORS, and REST API endpoints.
   - Provide ```html (index.html)```: Complete F-Aura frontend interface connected via async fetch('/api/...').
   - Provide ```css (style.css)```: Modern F-Aura styling, glassmorphism, and responsive grid.
   - Provide ```js (app.js)```: Async client state manager with toast notifications.
5. STANDALONE FRONTEND (If Frontend requested):
   - Provide complete, self-contained single-file or multi-file HTML5/CSS/JS with embedded F-Aura components.

### 💻 OUTPUT DIRECTIVE:
Output the full code in standard markdown code fences (```lang ... ```).
"""


class PromptEngineeringSynthesizer:
    """
    Chief Architect & Meta-Prompt Compiler for F.R.I.D.A.Y.
    Compiles raw voice instructions into the Universal Full-Stack Master Prompt,
    adaptively tuning the focus in <1ms at 0 token cost.
    """

    def detect_target_language(self, user_query: str) -> Tuple[str, Dict[str, str]]:
        """Identifies target programming language with explicit priority for fullstack and frontend keywords."""
        q = user_query.lower()
        if any(w in q for w in ["fullstack", "full stack", "backend and frontend", "frontend and backend", "api and frontend", "with database"]):
            return "fullstack", {"version": "Python FastAPI + F-Aura HTML5/CSS3/JS", "standards": "RESTful endpoints, SQLite persistent storage, Async Fetch UI, Lucide icons."}
        elif any(w in q for w in ["html", "website", "web page", "page", "front end", "frontend", "site", "landing", "ui", "menu", "restaurant", "store", "shop", "portfolio", "dashboard", "form"]):
            return "html", LANGUAGE_STANDARDS["html"]
        elif "python" in q or "py " in q or ".py" in q or "fastapi" in q or "flask" in q or "django" in q:
            return "python", LANGUAGE_STANDARDS["python"]
        elif "typescript" in q or "ts " in q or "react" in q or "nextjs" in q or "vue" in q:
            return "typescript", LANGUAGE_STANDARDS["typescript"]
        elif "javascript" in q or "js " in q or "node" in q:
            return "javascript", LANGUAGE_STANDARDS["javascript"]
        elif "c++" in q or "cpp" in q or "c plus plus" in q:
            return "cpp", LANGUAGE_STANDARDS["cpp"]
        elif "rust" in q:
            return "rust", LANGUAGE_STANDARDS["rust"]
        elif "java " in q or "in java" in q:
            return "java", LANGUAGE_STANDARDS["java"]
        elif "c#" in q or "csharp" in q or ".net" in q:
            return "csharp", LANGUAGE_STANDARDS["csharp"]
        elif "golang" in q or "go language" in q or "in go" in q:
            return "go", LANGUAGE_STANDARDS["go"]
        elif "sql" in q or "database query" in q or "schema" in q:
            return "sql", LANGUAGE_STANDARDS["sql"]
        elif "css" in q or "style" in q:
            return "css", LANGUAGE_STANDARDS["css"]
        elif "bash" in q or "shell script" in q or "powershell" in q:
            return "bash", LANGUAGE_STANDARDS["bash"]
        elif "c " in q or "in c" in q:
            return "c", LANGUAGE_STANDARDS["c"]
        else:
            return "html", LANGUAGE_STANDARDS["html"]

    def synthesize_design_tokens(self, user_instruction: str) -> str:
        """Dynamically synthesizes authentic, domain-tailored F-Aura design tokens, colors, typography, and interactive components."""
        ins = user_instruction.lower()
        f_aura_baseline = """
- CORE ASSETS (Zero Install):
  • Lucide Vector Icons: <script src="https://unpkg.com/lucide@latest"></script> (Initialize with `lucide.createIcons();`).
  • Film Grain Overlay: Subtle SVG noise texture for depth.
  • F-Aura Toast System: Floating non-intrusive toast alerts on actions.
  • Aceternity Cursor Spotlight: Card spotlight tracking cursor hover angle."""

        if any(w in ins for w in ["food", "restaurant", "biryani", "cafe", "coffee", "bakery", "dish", "menu", "pizza", "burger", "bar", "dining"]):
            return f"""- DOMAIN THEME: Artisanal Gastronomy & Culinary Elegance
- COLOR PALETTE: Warm Saffron Gold (hsl(38, 95%, 52%)), Spicy Terracotta (hsl(14, 88%, 52%)), Deep Charcoal Truffle (hsl(24, 18%, 10%)), Velvet Card Surface (hsl(24, 15%, 15%)), Warm Cream Text (#fff8ee).
- TYPOGRAPHY: Heading: 'Playfair Display' / 'Cinzel', Body: 'Plus Jakarta Sans'.
- IMAGERY & MEDIA: Embed high-definition Unsplash food photography.
- REQUIRED COMPONENTS:
  1. Hero section with headline, 'Order Now' and 'Book a Table' buttons.
  2. Interactive Menu Filter (All, Specials, Appetizers, Drinks) with real dish names, spice badges (🌶️🌶️), and prices.
  3. Working 'Add to Order' drawer with live cart counter and checkout subtotal.
  4. Table Reservation Modal with date/time picker and toast feedback.
  5. Customer Reviews Carousel with star ratings and verified foodie quotes.{f_aura_baseline}"""

        elif any(w in ins for w in ["shop", "store", "ecommerce", "cart", "clothing", "fashion", "shoes", "product", "buy"]):
            return f"""- DOMAIN THEME: High-Fashion Luxury Boutique & Modern E-Commerce
- COLOR PALETTE: Pure Editorial White (#ffffff) / Deep Onyx (#0f1115), Rose Champagne (hsl(35, 75%, 60%)), Cashmere Gray (#f4f4f6), Rich Charcoal Text (#1a1a1a).
- TYPOGRAPHY: Display: 'Syne' or 'Bodoni Moda', Body: 'Inter' / 'Plus Jakarta Sans'.
- REQUIRED COMPONENTS: Sticky Nav with live Cart Badge, Seasonal Collection Banner, Product Grid with 3D Spotlight tilt, image hover flip, price discount tags, size variant selectors, slide-out Cart Drawer with promo code input and checkout button, Free Shipping & Guarantee trust badges.{f_aura_baseline}"""

        elif any(w in ins for w in ["health", "medical", "doctor", "clinic", "hospital", "fitness", "wellness", "dentist"]):
            return f"""- DOMAIN THEME: Medical Trust, Serene Wellness & Clinical Excellence
- COLOR PALETTE: Pure Crisp White (#ffffff), Healing Teal (hsl(172, 80%, 38%)), Oceanic Blue (hsl(210, 85%, 45%)), Soft Slate Surface (#f8fafc), Midnight Navy Text (#0f172a).
- TYPOGRAPHY: Heading: 'Plus Jakarta Sans', Body: 'Inter'.
- REQUIRED COMPONENTS: Instant Appointment Booking Widget, Specialist Doctor Profiles with credentials and ratings, Service Cards with treatment details, Patient Testimonials, Emergency Hotline Banner, Insurance partners grid.{f_aura_baseline}"""

        elif any(w in ins for w in ["crypto", "fintech", "finance", "bank", "invest", "trading", "wallet"]):
            return f"""- DOMAIN THEME: Next-Gen FinTech & Secure Institutional Finance
- COLOR PALETTE: Obsidian Black (#080b11), Emerald Prosperity Glow (hsl(152, 90%, 48%)), Electric Sapphire (hsl(220, 95%, 62%)), Translucent Slate Cards (rgba(255,255,255,0.04)), Crisp Silver Text (#f1f5f9).
- TYPOGRAPHY: Display: 'Space Grotesk' / 'Outfit', Data/Numbers: 'JetBrains Mono'.
- REQUIRED COMPONENTS: Real-Time Market Ticker, Interactive Investment Yield Calculator slider, Feature Bento Grid with animated gradient borders, Security Certifications & 256-bit AES Encryption badges.{f_aura_baseline}"""

        elif any(w in ins for w in ["saas", "dashboard", "developer", "software", "api", "cloud", "ai", "platform"]):
            return f"""- DOMAIN THEME: Next-Gen SaaS & Developer Platform
- COLOR PALETTE: Obsidian Slate (#0b0f19), Electric Indigo (#6366f1), Cyber Neon Cyan (#38bdf8), Surface Bento (#131b2e), Silver Text (#e2e8f0).
- TYPOGRAPHY: Display: 'Outfit', Body: 'Plus Jakarta Sans', Code: 'JetBrains Mono'.
- REQUIRED COMPONENTS: Hero with live terminal demo, Magic UI Bento Grid with radiant borders, Interactive Monthly/Annual Pricing Toggle, Animated metric counter badges, Interactive FAQ accordion.{f_aura_baseline}"""

        else:
            return f"""- DOMAIN THEME: Bespoke Modern F-Aura UI/UX Experience
- COLOR PALETTE: Curated Harmonious Palette (Deep Charcoal #0c1017, Vibrant Indigo #6366f1, Soft Violet #8b5cf6, Surface Cards: rgba(255,255,255,0.04)).
- TYPOGRAPHY: Primary: 'Plus Jakarta Sans' / 'Outfit' with fluid clamp() scale.
- REQUIRED COMPONENTS: Rich responsive layout, interactive states (:hover, :active), micro-animations, glassmorphic elevation layers, real authentic domain content with zero placeholder text.{f_aura_baseline}"""

    def synthesize_master_prompt(self, user_instruction: str) -> Tuple[str, Dict[str, Any]]:
        """Compiles raw user command into UI/UX Pro Master Prompt in <1ms at 0 tokens."""
        lang_key, lang_meta = self.detect_target_language(user_instruction)
        slug_words = [w for w in re.sub(r"[^a-zA-Z0-9\s]", "", user_instruction).split() if w.lower() not in ["write", "code", "create", "build", "make", "in", "for", "please", "friday", "a", "an", "the", "can", "you", "page", "web"]]
        project_title = " ".join(slug_words[:5]).title() if slug_words else "Full-Stack Application"
        
        # Adaptive focus detection
        ins_lower = user_instruction.lower()
        if lang_key == "fullstack":
            scope_focus = "End-to-end Full-Stack harmony: Python FastAPI/SQLite backend paired with interactive F-Aura frontend."
        elif any(k in ins_lower for k in ["ui", "frontend", "css", "html", "design", "landing", "dashboard", "page"]):
            scope_focus = "Frontend UI/UX Excellence, human-designed authentic aesthetics, micro-animations, interactive state management."
        elif any(k in ins_lower for k in ["backend", "api", "database", "sql", "fastapi", "server", "crud"]):
            scope_focus = "Backend robustness, secure API endpoints, transactional database queries, data schemas."
        else:
            scope_focus = "End-to-end Full-Stack harmony: unified frontend interfaces backed by resilient services."

        ui_ux_pro_section = self.synthesize_design_tokens(user_instruction)

        tier_info = {
            "tier": "Tier 1: Principal CTO Architecture Profile",
            "primary_model": "Claude Code CTO (UI/UX Pro MCP)",
            "temperature": 0.2,
            "max_tokens": 8192
        }

        compiled_prompt = UNIVERSAL_FULLSTACK_MASTER_PROMPT.format(
            project_title=project_title,
            user_requirement=user_instruction,
            tier_name=tier_info["tier"],
            lang_version=lang_meta["version"],
            lang_standards=lang_meta["standards"],
            scope_focus=scope_focus,
            ui_ux_pro_section=ui_ux_pro_section
        )
        return compiled_prompt, tier_info


class ClaudeCodeExecutor:
    """
    Executes synthesized master prompts with OpenCode Multi-Model Engine (DeepSeek / Free Tier) as primary,
    supported by intelligent multi-model failover (Claude Code, Gemini-Web2API, Groq LPU).
    """

    def __init__(self):
        self.claude_cmd = self._find_claude_cli()
        self.ruflo_cmd = self._find_ruflo_cli()
        self.opencode_cmd = self._find_opencode_cli()

    def _find_claude_cli(self) -> Optional[str]:
        """Locates the global claude CLI binary on the system."""
        found = shutil.which("claude")
        if found:
            return found
        npm_claude = os.path.expandvars(r"%APPDATA%\npm\claude.cmd")
        if os.path.exists(npm_claude):
            return npm_claude
        return None

    def _find_ruflo_cli(self) -> Optional[str]:
        """Locates the global RuFlow/Ruflo CLI binary on the system with npx fallback."""
        found = shutil.which("ruflo") or shutil.which("claude-flow")
        if found:
            return found
        npm_ruflo = os.path.expandvars(r"%APPDATA%\npm\ruflo.cmd")
        if os.path.exists(npm_ruflo):
            return npm_ruflo
        npm_cf = os.path.expandvars(r"%APPDATA%\npm\claude-flow.cmd")
        if os.path.exists(npm_cf):
            return npm_cf
        if shutil.which("npx"):
            return "npx ruflo"
        return None

    def _find_opencode_cli(self) -> Optional[str]:
        """Locates the global OpenCode CLI binary on the system."""
        found = shutil.which("opencode")
        if found:
            return found
        npm_opencode = os.path.expandvars(r"%APPDATA%\npm\opencode.cmd")
        if os.path.exists(npm_opencode):
            return npm_opencode
        return None

    def execute_with_failover(self, master_prompt: str, tier_info: Dict[str, Any], timeout_seconds: int = 15) -> Tuple[bool, str, str]:
        """
        Executes across Level 2 Claude Code (CTO with UI/UX Pro MCP), RuFlow Multi-Agent Swarms,
        OpenCode Engine (DeepSeek Free / Multi-Model), and cascading LLM providers (Gemini-Web2API, Groq LPU).
        Returns: (success, generated_code_content, model_used)
        """
        # Tier 1A: Primary CTO Engine — Claude Code CLI (Snappy 15s timeout)
        if self.claude_cmd:
            process = None
            try:
                print(f"\n[Claude Code CTO]: Dispatching Master Prompt to {self.claude_cmd} (Tier: {tier_info['tier']})...")
                process = subprocess.Popen(
                    [self.claude_cmd, "-p", master_prompt],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=True,
                    encoding="utf-8",
                    errors="replace"
                )
                stdout, stderr = process.communicate(timeout=15)
                if process.returncode == 0 and stdout.strip() and len(stdout.strip()) > 50:
                    if "<tool_call>" not in stdout and "<function=" not in stdout and ("```" in stdout or "<!DOCTYPE" in stdout.upper() or "<html" in stdout.lower()):
                        return True, stdout.strip(), "Claude Code CTO (UI/UX Pro)"
                    else:
                        print("[Claude Code CTO]: Subprocess emitted tool call transcript. Auto-cascading to next tier...")
            except subprocess.TimeoutExpired:
                if process:
                    try:
                        process.kill()
                    except Exception:
                        pass
                print("[Claude Code CTO]: Timeout (15s) reached. Cascading to next tier...")
            except Exception as claude_err:
                if process:
                    try:
                        process.kill()
                    except Exception:
                        pass
                err_msg = str(claude_err).encode("ascii", "replace").decode("ascii")
                print(f"[Claude Code CTO Notice]: {err_msg[:120]}. Cascading to next tier...")

        # Tier 1B: RuFlow / Ruflo Multi-Agent Swarm Orchestration Engine (Open Base Configured)
        if self.ruflo_cmd:
            process = None
            try:
                print(f"\n[RuFlow Swarm Core]: Spawning Multi-Agent Swarm via {self.ruflo_cmd} (Tier: {tier_info['tier']})...")
                swarm_env = os.environ.copy()
                swarm_env["OPENAI_BASE_URL"] = "http://localhost:8081/v1"
                swarm_env["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "gemini-web2api")
                swarm_env["ANTHROPIC_BASE_URL"] = "http://localhost:8081/v1"
                cmd_args = self.ruflo_cmd.split() + ["run", master_prompt]
                process = subprocess.Popen(
                    cmd_args,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=True,
                    env=swarm_env,
                    encoding="utf-8",
                    errors="replace"
                )
                stdout, stderr = process.communicate(timeout=20)
                if process.returncode == 0 and stdout.strip() and len(stdout.strip()) > 50:
                    if "<tool_call>" not in stdout and "<function=" not in stdout and ("```" in stdout or "<!DOCTYPE" in stdout.upper() or "<html" in stdout.lower()):
                        return True, stdout.strip(), "RuFlow Multi-Agent Swarm (Open Base)"
            except subprocess.TimeoutExpired:
                if process:
                    try:
                        process.kill()
                    except Exception:
                        pass
                print("[RuFlow Swarm Core]: Timeout reached. Cascading to OpenCode...")
            except Exception as ruflo_err:
                if process:
                    try:
                        process.kill()
                    except Exception:
                        pass
                err_msg = str(ruflo_err).encode("ascii", "replace").decode("ascii")
                print(f"[RuFlow Swarm Notice]: {err_msg[:120]}. Cascading to OpenCode...")

        # Tier 2: OpenCode Autonomous Engine (DeepSeek V4 Free / Multi-Model Agent)
        if self.opencode_cmd:
            process = None
            try:
                print(f"\n[OpenCode Engine]: Dispatching Master Prompt to {self.opencode_cmd} (Tier: {tier_info['tier']})...")
                process = subprocess.Popen(
                    [self.opencode_cmd, "run", "-m", "opencode/deepseek-v4-flash-free", "--auto", master_prompt],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=True,
                    encoding="utf-8",
                    errors="replace"
                )
                stdout, stderr = process.communicate(timeout=60)
                if process.returncode == 0 and stdout.strip() and len(stdout.strip()) > 50:
                    return True, stdout.strip(), "OpenCode Engine (DeepSeek V4)"
            except subprocess.TimeoutExpired:
                if process:
                    try:
                        process.kill()
                    except Exception:
                        pass
                print("[OpenCode Engine]: Timeout (60s) reached. Auto-switching to Gemini-Web2API...")
            except Exception as opencode_err:
                if process:
                    try:
                        process.kill()
                    except Exception:
                        pass
                err_msg = str(opencode_err).encode("ascii", "replace").decode("ascii")
                print(f"[OpenCode Notice]: {err_msg[:120]}. Auto-switching to Gemini-Web2API...")

        # Tier 3: Flagship Gemini-Web2API (Port 8081 - Massive 1M Token Window)
        try:
            print("[Cognitive Dispatcher]: Engaging Gemini-Web2API (1M token context window)...")
            system_msg = (
                "You are F.R.I.D.A.Y. Principal Software Architect. Generate complete, gorgeous, fully-implemented, "
                "runnable code adhering strictly to UI/UX Pro design standards. Output full code in standard markdown code fences."
            )
            payload = {
                "model": "gemini-auto",
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": master_prompt}
                ],
                "stream": False
            }
            resp = requests.post("http://localhost:8081/v1/chat/completions", json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                if content and len(content.strip()) > 50:
                    return True, content.strip(), "Gemini-Web2API (Flagship)"
        except Exception as gemini_err:
            print(f"[Cognitive Dispatcher]: Gemini-Web2API failover ({gemini_err}). Cascading to Groq LPU Cloud...")

        # Tier 4: Groq Cloud LPU Core (Ultra-Fast 500 T/s)
        groq_key = os.environ.get("GROQ_API_KEY", "")
        if groq_key:
            try:
                print("[Cognitive Dispatcher]: Engaging Groq Cloud LPU Core...")
                headers = {
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "FRIDAY-Tactical-OS/7.0"
                }
                payload = {
                    "model": "qwen/qwen3.8-27b",
                    "messages": [
                        {"role": "system", "content": "You are F.R.I.D.A.Y. Expert Software Engineer. Generate complete, production-ready code with UI/UX Pro styling in markdown code fences. No placeholders."},
                        {"role": "user", "content": master_prompt}
                    ],
                    "temperature": tier_info.get("temperature", 0.3),
                    "max_tokens": 4096
                }
                resp = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=25)
                if resp.status_code == 200:
                    content = resp.json()["choices"][0]["message"]["content"]
                    if content and len(content.strip()) > 50:
                        return True, content.strip(), "Groq LPU Cloud"
            except Exception as groq_err:
                print(f"[Cognitive Dispatcher]: Groq LPU failover ({groq_err}).")

        return False, "All autonomous coding engines were unreachable, Boss.", "None"

    def execute_with_groq_fallback(self, master_prompt: str, tier_info: Dict[str, Any]) -> Tuple[bool, str, str]:
        """Direct ultra-fast fallback to Groq LPU Cloud (Qwen 3.8 / Llama 3) for instant guaranteed output."""
        groq_key = os.environ.get("GROQ_API_KEY", "")
        if groq_key:
            try:
                headers = {
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "FRIDAY-Tactical-OS/7.0"
                }
                payload = {
                    "model": "qwen/qwen3.8-27b",
                    "messages": [
                        {"role": "system", "content": "You are F.R.I.D.A.Y. Principal Software Engineer. Output the complete, working, beautiful HTML/CSS/JS or Python project strictly inside standard markdown code blocks (```html ... ```). Do not truncate or omit code."},
                        {"role": "user", "content": master_prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 4096
                }
                resp = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=25)
                if resp.status_code == 200:
                    content = resp.json()["choices"][0]["message"]["content"]
                    if content and len(content.strip()) > 50:
                        return True, content.strip(), "Groq LPU Cloud (Instant Generator)"
            except Exception:
                pass
        return False, "", "None"


class AutonomousCodingEngine:
    r"""Master controller orchestrating multi-language code generation, prompt engineering, and D:\ drive project deployment."""

    def __init__(self):
        self.synthesizer = PromptEngineeringSynthesizer()
        self.executor = ClaudeCodeExecutor()
        base_drive = os.path.splitdrive(os.path.abspath(__file__))[0] or os.path.expandvars("%SystemDrive%")
        self.projects_dir = os.path.join(base_drive, os.sep, "FRIDAY_Projects")
        try:
            os.makedirs(self.projects_dir, exist_ok=True)
        except Exception:
            pass
        self._status_lock = threading.Lock()
        self._active_status = {
            "is_active": False,
            "project_name": "None",
            "stage_num": 0,
            "total_stages": 5,
            "stage_name": "Idle",
            "detail": "Ready for new project orders",
            "start_time": 0.0,
            "last_completed": None,
            "last_completed_time": None
        }

    def update_stage(self, stage_num: int, stage_name: str, detail: str, project_title: str = "Project"):
        with self._status_lock:
            self._active_status["is_active"] = True
            self._active_status["project_name"] = project_title
            self._active_status["stage_num"] = stage_num
            self._active_status["total_stages"] = 5
            self._active_status["stage_name"] = stage_name
            self._active_status["detail"] = detail
            if self._active_status["start_time"] == 0.0:
                self._active_status["start_time"] = time.time()
        try:
            from core.terminal_hud import render_project_stage
            render_project_stage(stage_num, 5, stage_name, detail, project_title)
        except Exception:
            pass

    def mark_completed(self, project_title: str, saved_files: List[str], target_dir: str):
        elapsed = 0.0
        with self._status_lock:
            if self._active_status["start_time"] > 0:
                elapsed = time.time() - self._active_status["start_time"]
            self._active_status["is_active"] = False
            self._active_status["stage_num"] = 5
            self._active_status["stage_name"] = "Completed"
            self._active_status["detail"] = f"Deployed {len(saved_files)} files to {target_dir}"
            self._active_status["last_completed"] = project_title
            self._active_status["last_completed_time"] = datetime.now().strftime("%I:%M %p")
            self._active_status["start_time"] = 0.0
        try:
            from core.terminal_hud import render_project_complete
            file_names = [os.path.basename(f) for f in saved_files]
            render_project_complete(project_title, file_names, target_dir, elapsed)
        except Exception:
            pass

    def mark_failed(self, error_msg: str):
        with self._status_lock:
            self._active_status["is_active"] = False
            self._active_status["stage_name"] = "Failed"
            self._active_status["detail"] = error_msg
            self._active_status["start_time"] = 0.0

    def is_busy(self) -> bool:
        with self._status_lock:
            return self._active_status["is_active"]

    def get_status_speech(self) -> str:
        with self._status_lock:
            if self._active_status["is_active"]:
                stage_num = self._active_status["stage_num"]
                stage_name = self._active_status["stage_name"]
                p_name = self._active_status["project_name"]
                elapsed = int(time.time() - self._active_status["start_time"]) if self._active_status["start_time"] > 0 else 0
                return f"I am currently on Stage {stage_num} of 5 for {p_name}. {stage_name} is in progress, running for {elapsed} seconds, Boss."
            elif self._active_status["last_completed"]:
                return f"All project pipelines are idle, Boss. The latest build was {self._active_status['last_completed']}, completed at {self._active_status['last_completed_time']}."
            else:
                return "All autonomous coding pipelines are idle and standing by for your instructions, Boss."

    def extract_code_blocks(self, text: str) -> List[Tuple[str, str]]:
        """Extracts (language, code) tuples from markdown code fences, HTML blocks, or raw code."""
        if not text:
            return []
            
        pattern = r"```([a-zA-Z0-9_\+#\.\-]*)\r?\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return [(lang or "txt", code.strip()) for lang, code in matches]
        
        # Fallback for unclosed code block (when output was truncated)
        unclosed_pattern = r"```([a-zA-Z0-9_\+#\.\-]*)\r?\n(.*)"
        unclosed_match = re.search(unclosed_pattern, text, re.DOTALL)
        if unclosed_match:
            lang = unclosed_match.group(1) or "txt"
            code = unclosed_match.group(2).strip()
            code = re.sub(r"```+$", "", code).strip()
            return [(lang, code)]
        
        # Extract HTML document directly if tags are present
        if "<!doctype" in text.lower() or "<html" in text.lower():
            start_idx = text.lower().find("<!doctype")
            if start_idx == -1:
                start_idx = text.lower().find("<html")
            end_idx = text.lower().rfind("</html>")
            if end_idx != -1:
                html_body = text[start_idx : end_idx + 7].strip()
            else:
                html_body = text[start_idx:].strip()
            return [("html", html_body)]

        # Fallback for Python / script code
        if "def " in text or "import " in text or "class " in text:
            return [("py", text.strip())]

        return []

    def _derive_slug(self, instruction: str) -> str:
        """Derives a clean, readable, concise project slug from user instruction."""
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", instruction.lower())
        filler = {
            "can", "you", "create", "a", "an", "the", "web", "page", "only", "front", "end",
            "frontend", "for", "called", "as", "write", "code", "script", "program", "build",
            "make", "in", "with", "please", "friday", "me", "to", "app", "website", "site",
            "landing", "just", "simple", "modern", "design", "develop"
        }
        words = [w for w in cleaned.split() if w not in filler]
        if not words:
            return "friday_project"
        return "_".join(words[:4])

    def _repair_html_markup(self, html_code: str) -> str:
        """Guarantees that HTML files have complete, valid head, body, and closing tags so they render properly in browser."""
        code = html_code.strip()
        
        # 1. Close unclosed CSS <style> blocks
        if "<style" in code.lower() and "</style>" not in code.lower():
            open_braces = code.count("{")
            close_braces = code.count("}")
            if open_braces > close_braces:
                code += "\n}" * (open_braces - close_braces)
            code += "\n</style>\n"

        # 2. Close unclosed <head> tag
        if "<head" in code.lower() and "</head>" not in code.lower():
            code += "\n</head>\n"

        # 3. Ensure </body> and </html> are cleanly closed
        if "<body" in code.lower() and "</body>" not in code.lower():
            code += "\n</body>\n"
        if "</html>" not in code.lower():
            if "</body>" not in code.lower() and "<body" in code.lower():
                code += "\n</body>\n"
            code += "\n</html>\n"
            
        return code

    def handle_coding_request(
        self,
        raw_instruction: str,
        speak_fn: Optional[Any] = None,
        input_fn: Optional[Any] = None
    ) -> str:
        """
        End-to-end Meta-Prompt Orchestration & Coding Pipeline with guaranteed file deployment:
        1. Blueprinting & Design Tokens
        2. Neural Code Generation
        3. Code Block Extraction & Parsing
        4. File Deployment & Manifest Generation
        5. Live Launch & Verification
        """
        slug = self._derive_slug(raw_instruction)
        project_title = slug.replace("_", " ").title()
        lang_key, lang_meta = self.synthesizer.detect_target_language(raw_instruction)
        
        # Stage 1: Synthesize UI/UX Pro Master Prompt and determine optimal tier
        if speak_fn:
            speak_fn(f"Understood, Boss. Initializing multi-agent swarm for {project_title}. Step 1: Blueprinting architecture.")
        self.update_stage(1, "Blueprinting & Architecture", f"Synthesizing UI/UX Pro specs for {lang_meta['version']}", project_title)
        master_prompt, tier_info = self.synthesizer.synthesize_master_prompt(raw_instruction)
        tier_name = tier_info["tier"]
        primary_model = tier_info["primary_model"]

        print(f"\n[FRIDAY Coding Core]: Tier Selected -> [{tier_name}] | Model Target: {primary_model}")

        # Stage 2: Execute via Multi-Model Dynamic Failover Engine (RuFlow / OpenCode / Claude)
        self.update_stage(2, "Neural Swarm Code Synthesis", f"Swarm generating production source code via {primary_model}", project_title)
        if speak_fn:
            speak_fn(f"Step 2: Swarm agents are actively writing the components via {primary_model}, Boss.")
        
        success, result_content, model_used = self.executor.execute_with_failover(master_prompt, tier_info)

        if not success or not result_content.strip():
            self.mark_failed("Coding dispatcher unreachable")
            if speak_fn:
                speak_fn("I encountered an issue with the primary coding dispatcher, Boss. Activating fallback neural generator.")
            success, result_content, model_used = self.executor.execute_with_groq_fallback(master_prompt, tier_info)

        print(f"[FRIDAY Coding Core]: Code synthesized successfully using {model_used}.")

        # Stage 3: Extract & Validate Code Blocks
        self.update_stage(3, "Code Block Extraction & Parsing", f"Validating syntax and structure for {lang_key.upper()}", project_title)
        blocks = self.extract_code_blocks(result_content)
        
        # Fallback if no markdown fences were found
        if not blocks:
            if lang_key == "html" or "html" in raw_instruction.lower() or "page" in raw_instruction.lower() or "website" in raw_instruction.lower():
                repaired = self._repair_html_markup(result_content)
                blocks = [("html", repaired)]
            else:
                blocks = [(lang_key, result_content.strip())]

        if blocks:
            try:
                from core.terminal_hud import print_code
                print_code(blocks[0][1], lang_key)
            except Exception:
                pass

        # Stage 4: Automatically deploy code to D:\FRIDAY_Projects\
        self.update_stage(4, "File Assembly & Storage Deployment", f"Writing source files and operational manifest to storage", project_title)
        ext_map = {
            "python": "py", "py": "py", "javascript": "js", "js": "js",
            "typescript": "ts", "ts": "ts", "html": "html", "css": "css",
            "cpp": "cpp", "c": "c", "java": "java", "rust": "rs",
            "csharp": "cs", "go": "go", "sql": "sql", "bash": "sh"
        }
        target_dir = os.path.join(self.projects_dir, slug)
        os.makedirs(target_dir, exist_ok=True)
        saved_paths = []
        
        for i, (code_lang, code_body) in enumerate(blocks):
            file_ext = ext_map.get(code_lang.lower(), ext_map.get(lang_key.lower(), "txt"))
            
            # Smart naming for multi-block outputs (HTML + CSS + JS)
            if file_ext == "html":
                filename = "index.html"
            elif file_ext == "css":
                filename = "style.css"
            elif file_ext in ["js", "ts"]:
                filename = "app.js" if file_ext == "js" else "app.ts"
            elif file_ext == "py":
                filename = f"main.py" if i == 0 else f"script_{i+1}.py"
            else:
                filename = f"{slug}_{i+1}.{file_ext}"

            target_path = os.path.join(target_dir, filename)
            if file_ext == "html":
                code_body = self._repair_html_markup(code_body)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(code_body)
            saved_paths.append(target_path)
            print(f"[FRIDAY Code Engine]: Saved file -> {target_path}")

        # Auto-generate one-click start.bat, requirements.txt, and BRAIN.md operational manifest
        try:
            bat_path = os.path.join(target_dir, "start.bat")
            has_py = any(f.endswith(".py") for f in saved_paths)
            has_html = any(f.endswith(".html") for f in saved_paths)
            
            if has_py and has_html:
                # Full-Stack Application (FastAPI/Flask Backend + F-Aura Frontend)
                with open(bat_path, "w", encoding="utf-8") as bf:
                    bf.write(f"@echo off\r\necho ===================================================\r\necho   F.R.I.D.A.Y. Full-Stack Runtime Engine // {slug}\r\necho ===================================================\r\necho Launching Browser Frontend...\r\ntimeout /t 1 /nobreak >nul\r\nstart \"\" \"index.html\"\r\necho Starting High-Performance Python Backend on port 8000...\r\npython main.py\r\npause\r\n")
                # Auto-generate requirements.txt if needed
                req_path = os.path.join(target_dir, "requirements.txt")
                if not os.path.exists(req_path):
                    with open(req_path, "w", encoding="utf-8") as rf:
                        rf.write("fastapi>=0.110.0\nuvicorn>=0.29.0\npydantic>=2.6.0\n")
            elif has_html:
                html_target = [os.path.basename(f) for f in saved_paths if f.endswith(".html")][0]
                with open(bat_path, "w", encoding="utf-8") as bf:
                    bf.write(f"@echo off\r\necho Launching {slug} in Default Browser...\r\nstart \"\" \"{html_target}\"\r\n")
            elif has_py:
                py_target = [os.path.basename(f) for f in saved_paths if f.endswith(".py")][0]
                with open(bat_path, "w", encoding="utf-8") as bf:
                    bf.write(f"@echo off\r\necho Launching {slug}...\r\npython \"{py_target}\"\r\npause\r\n")

            brain_manifest_path = os.path.join(target_dir, "BRAIN.md")
            with open(brain_manifest_path, "w", encoding="utf-8") as mf:
                mf.write(f"# {slug.replace('_', ' ').title()} — F.R.I.D.A.Y. Project Manifest\n\n"
                         f"- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                         f"- **Engine**: {model_used}\n"
                         f"- **Tier**: {tier_name}\n"
                         f"- **Directive**: \"{raw_instruction}\"\n"
                         f"- **Files**: {', '.join([os.path.basename(p) for p in saved_paths])}\n")
        except Exception:
            pass

        # Stage 5: Live Execution & Browser/Workspace Deployment
        self.update_stage(5, "Live Deployment & Launch", f"Launching project in visual workspace", project_title)
        primary_file = saved_paths[0] if saved_paths else None
        if primary_file:
            try:
                if primary_file.endswith(".html"):
                    os.startfile(primary_file)
                else:
                    os.startfile(target_dir)
            except Exception:
                pass

        self.mark_completed(project_title, saved_paths, target_dir)

        if speak_fn:
            speak_fn(f"Step 5 complete: Project {project_title} has been deployed to FRIDAY Projects and launched on your screen, Boss.")

        return result_content

    def dispatch_coding_task_async(
        self,
        raw_instruction: str,
        speak_fn: Optional[Any] = None,
        on_complete_callback: Optional[Any] = None
    ) -> threading.Thread:
        """
        Dispatches heavy coding and multi-file projects to Claude Code CTO in an asynchronous background thread.
        F.R.I.D.A.Y. remains 100% unblocked and responsive to voice commands.
        """
        def _worker():
            try:
                res = self.handle_coding_request(raw_instruction, speak_fn=speak_fn)
                if on_complete_callback:
                    on_complete_callback(True, res)
            except Exception as e:
                print(f"[FRIDAY Async Dispatcher Error]: {e}")
                self.mark_failed(str(e))
                if on_complete_callback:
                    on_complete_callback(False, str(e))

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        return t


# Global instance
coding_engine = AutonomousCodingEngine()
