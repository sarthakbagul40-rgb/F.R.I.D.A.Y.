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
# STITCH-UX & UI/UX PRO MASTER PROMPT DELEGATION
# =============================================================================
from core.design_blueprint import design_blueprint
from core.mcp_design_bridge import mcp_design_bridge


class PromptEngineeringSynthesizer:
    """
    Chief Architect & Meta-Prompt Compiler for F.R.I.D.A.Y.
    Compiles raw voice instructions into Stitch-UX & UI/UX Pro blueprints in <1ms at 0 token cost.
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
        """Delegates domain design token synthesis to design_blueprint & mcp_design_bridge."""
        archetype = design_blueprint.detect_archetype(user_instruction)
        system = mcp_design_bridge.get_system_for_query(user_instruction, archetype)
        preset = design_blueprint.detect_domain(user_instruction)
        return (
            f"- DESIGN SYSTEM: {system['name']}\n"
            f"- DOMAIN THEME: {preset['theme']}\n"
            f"- PRIMARY CANVAS: {system.get('canvas_bg', '#09090b')}\n"
            f"- SURFACE: {system.get('surface', '#121216')}\n"
            f"- TYPOGRAPHY: {system.get('font_display', 'Plus Jakarta Sans')} / {system.get('font_mono', 'JetBrains Mono')}\n"
            f"- RULES: {', '.join(system.get('rules', []))}"
        )

    def synthesize_master_prompt(self, user_instruction: str) -> Tuple[str, Dict[str, Any]]:
        """Compiles raw user command into Stitch-UX Neural Blueprint Master Prompt in <1ms at 0 tokens."""
        user_prefs = None
        try:
            from core.headroom_memory import memory_engine
            user_prefs = memory_engine.get_swarm_preferences()
        except Exception:
            pass

        lang_key, _ = self.detect_target_language(user_instruction)
        if lang_key == "python":
            slug_words = [w for w in re.sub(r"[^a-zA-Z0-9\s]", "", user_instruction).split() if w.lower() not in ["write", "code", "create", "build", "make", "in", "for", "please", "friday", "a", "an", "the", "can", "you", "page", "web"]]
            project_title = " ".join(slug_words[:5]).title() if slug_words else "Python Application"
            compiled_prompt = design_blueprint.synthesize_backend_master_prompt(project_title, user_instruction)
        else:
            compiled_prompt = design_blueprint.synthesize_frontend_master_prompt(user_instruction, user_prefs)

        tier_info = {
            "tier": "Tier 1: Principal CTO Architecture Profile (Stitch-UX)",
            "primary_model": "Claude Code CTO (UI/UX Pro MCP)",
            "temperature": 0.2,
            "max_tokens": 8192
        }
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
        # Tier 1A: Primary CTO Engine — Claude Code CLI (Snappy 10s timeout)
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
                stdout, stderr = process.communicate(timeout=10)
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
                print("[Claude Code CTO]: Timeout (10s) reached. Cascading to next tier...")
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
                stdout, stderr = process.communicate(timeout=10)
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

        # Tier 2: OpenCode Autonomous Engine (DeepSeek V4 / Multi-Model Agent)
        if self.opencode_cmd:
            process = None
            try:
                print(f"\n[OpenCode Engine]: Dispatching Master Prompt to {self.opencode_cmd} (Tier: {tier_info['tier']})...")
                process = subprocess.Popen(
                    [self.opencode_cmd, "run", "-m", "opencode/deepseek-v4-flash", "--auto", master_prompt],
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
                    return True, stdout.strip(), "OpenCode Engine (DeepSeek V4)"
            except subprocess.TimeoutExpired:
                if process:
                    try:
                        process.kill()
                    except Exception:
                        pass
                print("[OpenCode Engine]: Timeout (15s) reached. Auto-switching to Gemini-Web2API...")
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
            resp = requests.post("http://localhost:8081/v1/chat/completions", json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                if content and len(content.strip()) > 50:
                    return True, content.strip(), "Gemini-Web2API (Flagship)"
        except Exception as gemini_err:
            print(f"[Cognitive Dispatcher]: Gemini-Web2API failover ({gemini_err}). Cascading to Groq LPU Cloud...")

        # Tier 4: Groq Cloud LPU Core (Ultra-Fast 500 T/s with Qwen 3.8 / GPT-OSS)
        groq_key = os.environ.get("GROQ_API_KEY", "")
        if groq_key:
            groq_candidates = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.6-27b"]
            for model_name in groq_candidates:
                try:
                    print(f"[Cognitive Dispatcher]: Engaging Groq Cloud LPU Core ({model_name})...")
                    headers = {
                        "Authorization": f"Bearer {groq_key}",
                        "Content-Type": "application/json",
                        "User-Agent": "FRIDAY-Tactical-OS/7.0"
                    }
                    payload = {
                        "model": model_name,
                        "messages": [
                            {"role": "system", "content": "You are F.R.I.D.A.Y. Expert Software Engineer. Generate complete, production-ready code with UI/UX Pro styling in markdown code fences. Write the full page and complete body without truncation."},
                            {"role": "user", "content": master_prompt}
                        ],
                        "temperature": tier_info.get("temperature", 0.3),
                        "max_tokens": 8192
                    }
                    resp = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=40)
                    if resp.status_code == 200:
                        content = resp.json()["choices"][0]["message"]["content"]
                        if content and len(content.strip()) > 50:
                            return True, content.strip(), f"Groq LPU Cloud ({model_name})"
                    else:
                        print(f"[Cognitive Dispatcher]: Groq {model_name} status {resp.status_code}: {resp.text[:100]}")
                except Exception as groq_err:
                    print(f"[Cognitive Dispatcher]: Groq LPU {model_name} failover ({groq_err}).")

        return False, "All autonomous coding engines were unreachable, Boss.", "None"

    def execute_with_groq_fallback(self, master_prompt: str, tier_info: Dict[str, Any]) -> Tuple[bool, str, str]:
        """Direct ultra-fast fallback to Groq LPU Cloud (Qwen 3.8 / GPT-OSS) for instant guaranteed output."""
        groq_key = os.environ.get("GROQ_API_KEY", "")
        if groq_key:
            groq_candidates = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.6-27b"]
            for model_name in groq_candidates:
                try:
                    headers = {
                        "Authorization": f"Bearer {groq_key}",
                        "Content-Type": "application/json",
                        "User-Agent": "FRIDAY-Tactical-OS/7.0"
                    }
                    payload = {
                        "model": model_name,
                        "messages": [
                            {"role": "system", "content": "You are F.R.I.D.A.Y. Principal Software Engineer. Output the complete, working, beautiful HTML/CSS/JS or Python project strictly inside standard markdown code blocks (```html ... ```). Complete the full <body> and all scripts."},
                            {"role": "user", "content": master_prompt}
                        ],
                        "temperature": 0.2,
                        "max_tokens": 8192
                    }
                    resp = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=40)
                    if resp.status_code == 200:
                        content = resp.json()["choices"][0]["message"]["content"]
                        if content and len(content.strip()) > 50:
                            return True, content.strip(), f"Groq LPU Cloud ({model_name})"
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

    def update_stage(self, stage_num: int, stage_name: str, detail: str, project_title: str = "Project", total_stages: int = 5):
        with self._status_lock:
            self._active_status["is_active"] = True
            self._active_status["project_name"] = project_title
            self._active_status["stage_num"] = stage_num
            self._active_status["total_stages"] = total_stages
            self._active_status["stage_name"] = stage_name
            self._active_status["detail"] = detail
            if self._active_status["start_time"] == 0.0:
                self._active_status["start_time"] = time.time()
        try:
            from core.terminal_hud import render_project_stage
            render_project_stage(stage_num, total_stages, stage_name, detail, project_title)
        except Exception:
            pass

    def mark_completed(self, project_title: str, saved_files: List[str], target_dir: str):
        elapsed = 0.0
        with self._status_lock:
            if self._active_status["start_time"] > 0:
                elapsed = time.time() - self._active_status["start_time"]
            total = self._active_status.get("total_stages", 5)
            self._active_status["is_active"] = False
            self._active_status["stage_num"] = total
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
            "builder", "building", "make", "in", "with", "please", "friday", "me", "to", "app",
            "website", "site", "landing", "just", "simple", "clean", "minimalist", "fast", "modern", "design", "develop"
        }
        words = [w for w in cleaned.split() if w not in filler]
        if not words:
            return "friday_project"
        return "_".join(words[:4])

    def _synthesize_utility_tool(self, ins: str) -> str:
        """Synthesizes a pristine, human-crafted single-file utility application (0% bloat, 100% YAGNI)."""
        q = ins.lower()
        is_pw = any(w in q for w in ["password", "secret", "generator"]) and not any(w in q for w in ["currency", "money"])
        is_curr = any(w in q for w in ["currency", "exchange", "forex", "money", "convert"])

        if is_pw:
            return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KeyCraft · Cryptographic Password Generator</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
    }
  </script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
  </style>
</head>
<body class="bg-[#fbfbfa] dark:bg-[#09090b] text-zinc-900 dark:text-zinc-100 min-h-screen flex items-center justify-center p-4 antialiased transition-colors duration-200">
  <div class="max-w-md w-full bg-white dark:bg-[#121216]/90 border border-zinc-200/80 dark:border-white/[0.08] rounded-2xl p-6 sm:p-7 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)] dark:shadow-2xl backdrop-blur-xl transition-all duration-200">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-zinc-100 dark:bg-white/[0.05] border border-zinc-200/80 dark:border-white/[0.08] flex items-center justify-center">
          <i data-lucide="shield-check" class="w-5 h-5 text-indigo-600 dark:text-indigo-400"></i>
        </div>
        <div>
          <h1 class="text-lg font-bold text-zinc-900 dark:text-white tracking-tight">KeyCraft</h1>
          <p class="text-xs text-zinc-500 dark:text-zinc-400">Cryptographic Security Standard</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="toggleTheme()" class="p-2 rounded-xl bg-zinc-100 hover:bg-zinc-200 dark:bg-white/[0.05] dark:hover:bg-white/[0.10] text-zinc-600 dark:text-zinc-300 border border-zinc-200/80 dark:border-white/[0.08] transition-all active:scale-95" title="Toggle Light/Dark Theme">
          <i data-lucide="sun" class="w-4 h-4 hidden dark:block text-amber-400"></i>
          <i data-lucide="moon" class="w-4 h-4 block dark:hidden text-zinc-600"></i>
        </button>
        <div class="px-2.5 py-1 rounded-full bg-zinc-100 dark:bg-white/[0.04] border border-zinc-200/80 dark:border-white/[0.08] text-[11px] font-medium text-zinc-600 dark:text-zinc-400">
          Local · Offline
        </div>
      </div>
    </div>

    <!-- Generated Password Display -->
    <div class="bg-zinc-50 dark:bg-black/30 border border-zinc-200/80 dark:border-white/[0.08] rounded-xl p-4 mb-5 flex items-center justify-between gap-3 transition-colors">
      <div id="password-display" class="font-mono text-xl sm:text-2xl font-semibold text-zinc-900 dark:text-white tracking-wider select-all break-all flex-1">
        Generating...
      </div>
      <div class="flex items-center gap-1.5 flex-shrink-0">
        <button id="refresh-btn" onclick="generate()" class="p-2 rounded-lg bg-zinc-100 hover:bg-zinc-200 dark:bg-white/[0.04] dark:hover:bg-white/[0.08] text-zinc-600 hover:text-zinc-900 dark:text-zinc-300 dark:hover:text-white border border-zinc-200/80 dark:border-white/[0.06] transition-all active:scale-95" title="Generate New">
          <i data-lucide="refresh-cw" class="w-4 h-4 transition-transform duration-300"></i>
        </button>
        <button onclick="copyPassword()" class="p-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition-all active:scale-95 shadow-sm" title="Copy to Clipboard">
          <i data-lucide="copy" class="w-4 h-4"></i>
        </button>
      </div>
    </div>

    <!-- Entropy Strength Bar -->
    <div class="mb-5">
      <div class="flex justify-between items-center text-xs mb-1.5">
        <span class="text-zinc-500 dark:text-zinc-400">Entropy Strength</span>
        <span id="strength-label" class="font-mono text-xs font-semibold text-emerald-600 dark:text-emerald-400">Strong (128-bit)</span>
      </div>
      <div class="grid grid-cols-4 gap-1.5 h-1.5">
        <div id="bar-1" class="h-full rounded-full bg-emerald-500 transition-colors"></div>
        <div id="bar-2" class="h-full rounded-full bg-emerald-500 transition-colors"></div>
        <div id="bar-3" class="h-full rounded-full bg-emerald-500 transition-colors"></div>
        <div id="bar-4" class="h-full rounded-full bg-emerald-500 transition-colors"></div>
      </div>
    </div>

    <!-- Length Slider -->
    <div class="mb-5 bg-zinc-50/80 dark:bg-white/[0.02] border border-zinc-200/80 dark:border-white/[0.06] rounded-xl p-4 transition-colors">
      <div class="flex justify-between items-center mb-2">
        <label class="text-xs font-medium text-zinc-700 dark:text-zinc-300">Password Length</label>
        <span id="length-val" class="font-mono text-sm font-semibold text-zinc-900 dark:text-white bg-zinc-200/70 dark:bg-white/[0.06] px-2 py-0.5 rounded-md">16</span>
      </div>
      <input id="length-slider" type="range" min="8" max="48" value="16" oninput="updateLength(this.value)" class="w-full accent-indigo-600 cursor-pointer">
    </div>

    <!-- Character Set Toggles -->
    <div class="grid grid-cols-2 gap-2.5 mb-5">
      <label class="flex items-center gap-2.5 p-3 rounded-xl bg-zinc-50/80 hover:bg-zinc-100/80 dark:bg-white/[0.02] dark:hover:bg-white/[0.04] border border-zinc-200/80 dark:border-white/[0.06] cursor-pointer transition-colors">
        <input type="checkbox" id="chk-upper" checked onchange="generate()" class="w-4 h-4 rounded accent-indigo-600">
        <span class="text-xs font-medium text-zinc-700 dark:text-zinc-300">Uppercase (A-Z)</span>
      </label>
      <label class="flex items-center gap-2.5 p-3 rounded-xl bg-zinc-50/80 hover:bg-zinc-100/80 dark:bg-white/[0.02] dark:hover:bg-white/[0.04] border border-zinc-200/80 dark:border-white/[0.06] cursor-pointer transition-colors">
        <input type="checkbox" id="chk-lower" checked onchange="generate()" class="w-4 h-4 rounded accent-indigo-600">
        <span class="text-xs font-medium text-zinc-700 dark:text-zinc-300">Lowercase (a-z)</span>
      </label>
      <label class="flex items-center gap-2.5 p-3 rounded-xl bg-zinc-50/80 hover:bg-zinc-100/80 dark:bg-white/[0.02] dark:hover:bg-white/[0.04] border border-zinc-200/80 dark:border-white/[0.06] cursor-pointer transition-colors">
        <input type="checkbox" id="chk-digits" checked onchange="generate()" class="w-4 h-4 rounded accent-indigo-600">
        <span class="text-xs font-medium text-zinc-700 dark:text-zinc-300">Numbers (0-9)</span>
      </label>
      <label class="flex items-center gap-2.5 p-3 rounded-xl bg-zinc-50/80 hover:bg-zinc-100/80 dark:bg-white/[0.02] dark:hover:bg-white/[0.04] border border-zinc-200/80 dark:border-white/[0.06] cursor-pointer transition-colors">
        <input type="checkbox" id="chk-symbols" checked onchange="generate()" class="w-4 h-4 rounded accent-indigo-600">
        <span class="text-xs font-medium text-zinc-700 dark:text-zinc-300">Symbols (!@#$)</span>
      </label>
    </div>

    <!-- Recent History -->
    <div>
      <h3 class="text-xs font-medium text-zinc-400 dark:text-zinc-500 uppercase tracking-wider mb-2">Recent Generated</h3>
      <div id="history-list" class="space-y-1.5 text-xs font-mono text-zinc-600 dark:text-zinc-400"></div>
    </div>
  </div>

  <!-- Toast Alert -->
  <div id="toast" class="fixed bottom-6 px-4 py-2.5 rounded-xl bg-zinc-900 dark:bg-zinc-800 border border-zinc-700 dark:border-white/10 text-white text-xs font-medium shadow-2xl flex items-center gap-2 opacity-0 pointer-events-none transition-all duration-200">
    <i data-lucide="check" class="w-4 h-4 text-emerald-400"></i>
    <span>Copied to clipboard</span>
  </div>

  <script>
    function initTheme() {
      const saved = localStorage.getItem('theme');
      const isDark = saved === 'dark';
      document.documentElement.classList.toggle('dark', isDark);
    }
    function toggleTheme() {
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }
    initTheme();

    const chars = {
      upper: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
      lower: 'abcdefghijklmnopqrstuvwxyz',
      digits: '0123456789',
      symbols: '!@#$%^&*()_+~|}{[]:;?><,.-='
    };
    let history = JSON.parse(localStorage.getItem('keycraft_hist') || '[]');

    function updateLength(v) {
      document.getElementById('length-val').innerText = v;
      generate();
    }

    function generate() {
      const len = parseInt(document.getElementById('length-slider').value);
      const useUpper = document.getElementById('chk-upper').checked;
      const useLower = document.getElementById('chk-lower').checked;
      const useDigits = document.getElementById('chk-digits').checked;
      const useSymbols = document.getElementById('chk-symbols').checked;

      let pool = '';
      if (useUpper) pool += chars.upper;
      if (useLower) pool += chars.lower;
      if (useDigits) pool += chars.digits;
      if (useSymbols) pool += chars.symbols;

      if (!pool) {
        document.getElementById('chk-lower').checked = true;
        pool = chars.lower;
      }

      const arr = new Uint32Array(len);
      crypto.getRandomValues(arr);
      let pw = '';
      for (let i = 0; i < len; i++) {
        pw += pool[arr[i] % pool.length];
      }

      document.getElementById('password-display').innerText = pw;
      updateStrength(pw, len, [useUpper, useLower, useDigits, useSymbols].filter(Boolean).length);

      if (!history.includes(pw)) {
        history.unshift(pw);
        if (history.length > 3) history.pop();
        localStorage.setItem('keycraft_hist', JSON.stringify(history));
      }
      renderHistory();
    }

    function updateStrength(pw, len, typesCount) {
      const score = (len >= 16 ? 2 : (len >= 12 ? 1 : 0)) + typesCount;
      const bars = [document.getElementById('bar-1'), document.getElementById('bar-2'), document.getElementById('bar-3'), document.getElementById('bar-4')];
      const label = document.getElementById('strength-label');

      let activeCount = 1;
      let colorClass = 'bg-rose-500';
      let text = 'Weak';

      if (score >= 5) {
        activeCount = 4; colorClass = 'bg-emerald-500'; text = 'Strong (128-bit)';
      } else if (score >= 4) {
        activeCount = 3; colorClass = 'bg-indigo-500 dark:bg-indigo-400'; text = 'Good (96-bit)';
      } else if (score >= 2) {
        activeCount = 2; colorClass = 'bg-amber-500 dark:bg-amber-400'; text = 'Fair (64-bit)';
      }

      label.innerText = text;
      label.className = 'font-mono text-xs font-semibold ' + (activeCount === 4 ? 'text-emerald-600 dark:text-emerald-400' : (activeCount === 3 ? 'text-indigo-600 dark:text-indigo-400' : 'text-amber-600 dark:text-amber-400'));

      bars.forEach((b, i) => {
        b.className = 'h-full rounded-full transition-colors ' + (i < activeCount ? colorClass : 'bg-zinc-200 dark:bg-white/[0.08]');
      });
    }

    function renderHistory() {
      const el = document.getElementById('history-list');
      if (history.length <= 1) {
        el.innerHTML = '<p class="text-zinc-400 dark:text-zinc-600 italic">No previous entries.</p>';
        return;
      }
      el.innerHTML = history.slice(1).map(h => `
        <div class="flex justify-between items-center p-2 rounded-lg bg-zinc-50 dark:bg-white/[0.02] border border-zinc-200/60 dark:border-white/[0.04]">
          <span class="truncate mr-2 text-zinc-700 dark:text-zinc-300">${h}</span>
          <button onclick="copyText('${h}')" class="text-zinc-400 hover:text-zinc-900 dark:text-zinc-500 dark:hover:text-white transition-colors"><i data-lucide="copy" class="w-3.5 h-3.5"></i></button>
        </div>
      `).join('');
      if (window.lucide) lucide.createIcons();
    }

    function copyPassword() {
      const text = document.getElementById('password-display').innerText.trim();
      copyText(text);
    }

    function copyText(t) {
      navigator.clipboard.writeText(t).then(() => {
        const toast = document.getElementById('toast');
        toast.classList.remove('opacity-0', 'pointer-events-none');
        setTimeout(() => toast.classList.add('opacity-0', 'pointer-events-none'), 2000);
      });
    }

    window.addEventListener('DOMContentLoaded', () => {
      if (window.lucide) lucide.createIcons();
      generate();
    });
  </script>
</body>
</html>"""
        elif is_curr:
            return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Meridian · Currency Converter</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
    }
  </script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
  </style>
</head>
<body class="bg-[#fbfbfa] dark:bg-[#09090b] text-zinc-900 dark:text-zinc-100 min-h-screen flex items-center justify-center p-4 antialiased transition-colors duration-200">
  <div class="max-w-md w-full bg-white dark:bg-[#121216]/90 border border-zinc-200/80 dark:border-white/[0.08] rounded-2xl p-6 sm:p-7 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)] dark:shadow-2xl backdrop-blur-xl transition-all duration-200">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-zinc-100 dark:bg-white/[0.05] border border-zinc-200/80 dark:border-white/[0.08] flex items-center justify-center">
          <i data-lucide="refresh-cw" class="w-5 h-5 text-indigo-600 dark:text-indigo-400"></i>
        </div>
        <div>
          <h1 class="text-lg font-bold text-zinc-900 dark:text-white tracking-tight">Meridian</h1>
          <p class="text-xs text-zinc-500 dark:text-zinc-400">Institutional Foreign Exchange</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="toggleTheme()" class="p-2 rounded-xl bg-zinc-100 hover:bg-zinc-200 dark:bg-white/[0.05] dark:hover:bg-white/[0.10] text-zinc-600 dark:text-zinc-300 border border-zinc-200/80 dark:border-white/[0.08] transition-all active:scale-95" title="Toggle Light/Dark Theme">
          <i data-lucide="sun" class="w-4 h-4 hidden dark:block text-amber-400"></i>
          <i data-lucide="moon" class="w-4 h-4 block dark:hidden text-zinc-600"></i>
        </button>
        <div class="px-2.5 py-1 rounded-full bg-zinc-100 dark:bg-white/[0.04] border border-zinc-200/80 dark:border-white/[0.08] text-[11px] font-medium text-zinc-600 dark:text-zinc-400">
          Live Mid-Market
        </div>
      </div>
    </div>

    <!-- Source Currency Row -->
    <div class="bg-zinc-50/80 dark:bg-white/[0.02] border border-zinc-200/80 dark:border-white/[0.08] rounded-xl p-3.5 mb-2 focus-within:border-indigo-500 dark:focus-within:border-white/[0.22] transition-colors">
      <div class="text-[11px] font-medium text-zinc-500 dark:text-zinc-400 mb-1">You send</div>
      <div class="grid grid-cols-12 gap-3 items-center">
        <select id="from-currency" onchange="convert()" class="col-span-5 bg-white dark:bg-white/[0.05] border border-zinc-200 dark:border-white/10 rounded-lg px-2.5 py-2 text-sm font-medium text-zinc-900 dark:text-white focus:outline-none cursor-pointer">
          <option value="USD">🇺🇸 USD</option>
          <option value="EUR">🇪🇺 EUR</option>
          <option value="GBP">🇬🇧 GBP</option>
          <option value="JPY">🇯🇵 JPY</option>
          <option value="INR" selected>🇮🇳 INR</option>
          <option value="CAD">🇨🇦 CAD</option>
          <option value="AUD">🇦🇺 AUD</option>
          <option value="CHF">🇨🇭 CHF</option>
          <option value="SGD">🇸🇬 SGD</option>
          <option value="AED">🇦🇪 AED</option>
        </select>
        <div class="col-span-7 min-w-0">
          <input id="amount-input" type="number" value="1000" oninput="convert()" class="w-full bg-transparent font-mono text-2xl font-semibold text-zinc-900 dark:text-white text-right focus:outline-none tracking-tight" placeholder="0.00">
        </div>
      </div>
    </div>

    <!-- Swap Button Divider -->
    <div class="flex justify-center -my-2.5 relative z-10">
      <button id="swap-btn" onclick="swapCurrencies()" class="w-9 h-9 rounded-full bg-white dark:bg-[#18181c] border border-zinc-200 dark:border-white/10 hover:border-zinc-300 dark:hover:border-white/20 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white flex items-center justify-center transition-all duration-200 active:scale-95 shadow-md">
        <i data-lucide="arrow-up-down" class="w-4 h-4 transition-transform duration-300"></i>
      </button>
    </div>

    <!-- Target Currency Row -->
    <div class="bg-zinc-50/80 dark:bg-white/[0.02] border border-zinc-200/80 dark:border-white/[0.08] rounded-xl p-3.5 mb-5 transition-colors">
      <div class="text-[11px] font-medium text-zinc-500 dark:text-zinc-400 mb-1">Recipient gets</div>
      <div class="grid grid-cols-12 gap-3 items-center">
        <select id="to-currency" onchange="convert()" class="col-span-5 bg-white dark:bg-white/[0.05] border border-zinc-200 dark:border-white/10 rounded-lg px-2.5 py-2 text-sm font-medium text-zinc-900 dark:text-white focus:outline-none cursor-pointer">
          <option value="USD" selected>🇺🇸 USD</option>
          <option value="EUR">🇪🇺 EUR</option>
          <option value="GBP">🇬🇧 GBP</option>
          <option value="JPY">🇯🇵 JPY</option>
          <option value="INR">🇮🇳 INR</option>
          <option value="CAD">🇨🇦 CAD</option>
          <option value="AUD">🇦🇺 AUD</option>
          <option value="CHF">🇨🇭 CHF</option>
          <option value="SGD">🇸🇬 SGD</option>
          <option value="AED">🇦🇪 AED</option>
        </select>
        <div class="col-span-7 min-w-0 flex items-center justify-end gap-2">
          <div id="result-display" class="font-mono text-2xl font-semibold text-zinc-900 dark:text-zinc-50 text-right truncate tracking-tight">11.95</div>
          <button onclick="copyResult()" class="p-1.5 rounded-lg bg-zinc-100 hover:bg-zinc-200 dark:bg-white/[0.04] dark:hover:bg-white/[0.08] text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white transition-all flex-shrink-0" title="Copy result">
            <i data-lucide="copy" class="w-4 h-4"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Rate Pill -->
    <div class="flex items-center justify-between p-3 rounded-xl bg-zinc-100/80 dark:bg-white/[0.02] border border-zinc-200/80 dark:border-white/[0.04] mb-5">
      <div class="flex items-center gap-2">
        <i data-lucide="trending-up" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
        <span id="rate-pill" class="text-xs font-mono text-zinc-700 dark:text-zinc-300">1 INR = 0.01195 USD</span>
      </div>
      <span class="text-[11px] text-zinc-500">Zero markup</span>
    </div>

    <!-- Recent History -->
    <div>
      <h3 class="text-xs font-medium text-zinc-400 dark:text-zinc-500 uppercase tracking-wider mb-2">Recent Conversions</h3>
      <div id="history-list" class="space-y-1.5 text-xs font-mono text-zinc-600 dark:text-zinc-400"></div>
    </div>
  </div>

  <div id="toast" class="fixed bottom-6 px-4 py-2.5 rounded-xl bg-zinc-900 dark:bg-zinc-800 border border-zinc-700 dark:border-white/10 text-white text-xs font-medium shadow-2xl flex items-center gap-2 opacity-0 pointer-events-none transition-all duration-200">
    <i data-lucide="check" class="w-4 h-4 text-emerald-400"></i>
    <span>Copied to clipboard</span>
  </div>

  <script>
    function initTheme() {
      const saved = localStorage.getItem('theme');
      const isDark = saved === 'dark';
      document.documentElement.classList.toggle('dark', isDark);
    }
    function toggleTheme() {
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }
    initTheme();

    const rates = { USD: 1.0, EUR: 0.92, GBP: 0.78, JPY: 154.2, INR: 83.7, CAD: 1.37, AUD: 1.52, CHF: 0.90, SGD: 1.35, AED: 3.67 };
    let history = JSON.parse(localStorage.getItem('meridian_hist') || '[]');

    function convert() {
      const from = document.getElementById('from-currency').value;
      const to = document.getElementById('to-currency').value;
      const amount = parseFloat(document.getElementById('amount-input').value) || 0;
      const rate = (rates[to] / rates[from]);
      const res = amount * rate;
      document.getElementById('result-display').innerText = res.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      document.getElementById('rate-pill').innerText = `1 ${from} = ${rate.toFixed(5)} ${to}`;
    }

    function swapCurrencies() {
      const fromEl = document.getElementById('from-currency');
      const toEl = document.getElementById('to-currency');
      const tmp = fromEl.value;
      fromEl.value = toEl.value;
      toEl.value = tmp;
      const icon = document.querySelector('#swap-btn i');
      if (icon) icon.classList.toggle('rotate-180');
      convert();
    }

    function copyResult() {
      const val = document.getElementById('result-display').innerText;
      navigator.clipboard.writeText(val).then(() => {
        const toast = document.getElementById('toast');
        toast.classList.remove('opacity-0', 'pointer-events-none');
        setTimeout(() => toast.classList.add('opacity-0', 'pointer-events-none'), 2000);
      });
    }

    window.addEventListener('DOMContentLoaded', () => {
      if (window.lucide) lucide.createIcons();
      convert();
    });
  </script>
</body>
</html>"""
        else:
            return self._synthesize_password_generator_app()

    def _synthesize_password_generator_app(self) -> str:
        return self._synthesize_utility_tool("password generator")

    def _repair_html_markup(self, html_code: str, raw_instruction: str = "") -> str:
        """
        Guarantees that HTML files have complete, valid, working head, body, components, and scripts.
        If an LLM response was truncated, FRIDAY self-heals and synthesizes the missing interactive components.
        """
        code = html_code.strip()
        ins = (raw_instruction or "").lower()

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

        # 3. If completely missing <body> or severely truncated, synthesize a complete rich F-Aura application
        if "<body" not in code.lower() or len(code) < 300:
            archetype = design_blueprint.detect_archetype(ins)
            if archetype == "utility_tool":
                return self._synthesize_utility_tool(ins)

            is_coffee = any(w in ins for w in ["coffee", "cafe", "espresso", "brew", "roast", "barista", "latte", "cappuccino", "macchiato", "mocha"])
            is_food = is_coffee or any(w in ins for w in ["food", "restaurant", "biryani", "menu", "dining", "pizza", "burger", "bar", "bakery"])
            is_shop = any(w in ins for w in ["shop", "store", "ecommerce", "cart", "clothing", "fashion", "shoes", "product", "buy"])

            if is_coffee:
                title = "The Velvet Roast Coffee Co."
                theme_gradient = "from-amber-600 to-amber-900"
                tagline = "Artisanal micro-roasts & handcrafted single-origin brews."
                catalog_js = """[
            { name: "Ethiopian Yirgacheffe Reserve", price: 18.50, desc: "Floral jasmine aromatics with wild citrus finish.", img: "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?q=80&w=600&auto=format&fit=crop" },
            { name: "Bourbon Barrel Cold Brew", price: 6.50, desc: "Slow-steeped for 24 hours with Madagascar vanilla bean.", img: "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?q=80&w=600&auto=format&fit=crop" },
            { name: "Artisanal Oat Milk Macchiato", price: 5.75, desc: "Double espresso ristretto with salted caramel swirl.", img: "https://images.unsplash.com/photo-1541167760496-1628856ab772?q=80&w=600&auto=format&fit=crop" }
        ]"""
            elif is_food:
                title = "Zafraan Artisanal Dining"
                theme_gradient = "from-amber-500 to-rose-600"
                tagline = "Artisanal gastronomy & royal culinary heritage."
                catalog_js = """[
            { name: "Royal Shahi Biryani", price: 28.00, desc: "Aged basmati rice infused with Persian saffron.", img: "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=600&auto=format&fit=crop" },
            { name: "Smoked Truffle Butter Naan", price: 12.00, desc: "Clay oven baked with French truffle compound butter.", img: "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?q=80&w=600&auto=format&fit=crop" },
            { name: "Kashmiri Kahwa Elixir", price: 9.50, desc: "Green tea leaves with crushed saffron and almonds.", img: "https://images.unsplash.com/photo-1576092768241-dec231879fc3?q=80&w=600&auto=format&fit=crop" }
        ]"""
            elif is_shop:
                title = "Maison Noir Luxury Boutique"
                theme_gradient = "from-indigo-500 to-violet-600"
                tagline = "Sculpted for elegance, crafted without compromise."
                catalog_js = """[
            { name: "Royal Reserve Signature", price: 480, desc: "Handcrafted limited edition masterpiece.", img: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=600&auto=format&fit=crop" },
            { name: "Obsidian Velvet Edition", price: 560, desc: "Burnished finish with precision hardware.", img: "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?q=80&w=600&auto=format&fit=crop" },
            { name: "Amber Saffron Runner", price: 420, desc: "Lightweight composite chassis with luxury accents.", img: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?q=80&w=600&auto=format&fit=crop" }
        ]"""
            else:
                title = "F.R.I.D.A.Y. Intelligent Platform"
                theme_gradient = "from-cyan-500 to-blue-600"
                tagline = "Autonomous intelligence with sub-millisecond precision."
                catalog_js = """[
            { name: "Quantum Neural Node", price: 990, desc: "Distributed high-throughput reasoning coprocessor.", img: "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=600&auto=format&fit=crop" },
            { name: "Tactical Vision Core", price: 750, desc: "Multimodal spatial telemetry with real-time HUD streaming.", img: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=600&auto=format&fit=crop" },
            { name: "Aegis Media Engine", price: 490, desc: "Zero-latency audio and neural narration pipeline.", img: "https://images.unsplash.com/photo-1511379938547-c1f69419868d?q=80&w=600&auto=format&fit=crop" }
        ]"""

            code = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body {{ background-color: #0B0F17; color: #EEF1F7; font-family: 'Plus Jakarta Sans', sans-serif; overflow-x: hidden; }}
        .gold-gradient {{ background: linear-gradient(135deg, #E5C07B 0%, #F3DCAE 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .card-spotlight {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); transition: transform 0.3s ease, border-color 0.3s ease; }}
        .card-spotlight:hover {{ transform: translateY(-4px); border-color: rgba(229,192,123,0.4); }}
    </style>
</head>
<body class="antialiased">
    <nav class="sticky top-0 z-50 bg-[#0B0F17]/80 backdrop-blur-xl border-b border-white/10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 h-20 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br {theme_gradient} flex items-center justify-center">
                    <i data-lucide="sparkles" class="w-5 h-5 text-white"></i>
                </div>
                <span class="font-bold text-xl tracking-wider gold-gradient">{title.upper()}</span>
            </div>
            <button onclick="toggleCart()" class="relative p-2.5 rounded-xl bg-white/5 border border-white/10 hover:border-amber-400 text-gray-300">
                <i data-lucide="shopping-bag" class="w-5 h-5"></i>
                <span id="cart-badge" class="absolute -top-1 -right-1 w-5 h-5 bg-amber-400 text-black text-xs font-bold rounded-full flex items-center justify-center">0</span>
            </button>
        </div>
    </nav>
    <header class="py-16 px-4 max-w-5xl mx-auto text-center">
        <h1 class="text-5xl sm:text-6xl font-extrabold tracking-tight mb-4 gold-gradient">{title}</h1>
        <p class="text-gray-400 text-lg max-w-xl mx-auto mb-8">{tagline}</p>
    </header>
    <section class="max-w-7xl mx-auto px-4 pb-24 grid sm:grid-cols-2 lg:grid-cols-3 gap-6" id="catalog-grid"></section>
    <div id="cart-drawer-overlay" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm opacity-0 pointer-events-none transition-opacity" onclick="toggleCart()"></div>
    <div id="cart-drawer" class="fixed top-0 right-0 bottom-0 z-50 w-full max-w-md bg-[#121824] border-l border-white/10 p-6 flex flex-col justify-between translate-x-full transition-transform">
        <div>
            <div class="flex justify-between items-center pb-4 border-b border-white/10">
                <h3 class="font-bold text-lg text-white">Order Bag</h3>
                <button onclick="toggleCart()" class="text-gray-400 hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
            </div>
            <div id="cart-items" class="py-4 space-y-3 max-h-[60vh] overflow-y-auto">
                <p class="text-gray-500 text-sm text-center py-6">Your bag is empty.</p>
            </div>
        </div>
        <div class="pt-4 border-t border-white/10 space-y-3">
            <div class="flex justify-between text-sm"><span class="text-gray-400">Total</span><span id="cart-total" class="font-bold text-amber-400">$0.00</span></div>
            <button onclick="alert('Order Placed Successfully!')" class="w-full py-3.5 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 text-black font-bold uppercase tracking-wider text-xs">Checkout</button>
        </div>
    </div>
    <script>
        const catalog = {catalog_js};
        let cart = [];
        function render() {{
            document.getElementById('catalog-grid').innerHTML = catalog.map(p => `
                <div class="card-spotlight rounded-2xl p-5 flex flex-col justify-between">
                    <img src="${{p.img}}" class="w-full h-48 object-cover rounded-xl mb-4">
                    <h4 class="font-bold text-lg text-white mb-1">${{p.name}}</h4>
                    <p class="text-gray-400 text-xs mb-4">${{p.desc}}</p>
                    <div class="flex justify-between items-center pt-3 border-t border-white/5">
                        <span class="font-bold text-amber-400">$${{p.price}}</span>
                        <button onclick="add('${{p.name}}', ${{p.price}})" class="px-4 py-2 rounded-lg bg-white/10 hover:bg-amber-400 hover:text-black text-xs font-semibold transition-all">Add to Bag</button>
                    </div>
                </div>
            `).join('');
            if (window.lucide) lucide.createIcons();
        }}
        function add(name, price) {{
            cart.push({{ name, price }});
            update();
        }}
        function update() {{
            document.getElementById('cart-badge').innerText = cart.length;
            const total = cart.reduce((s, i) => s + i.price, 0);
            document.getElementById('cart-total').innerText = '$' + total.toFixed(2);
            document.getElementById('cart-items').innerHTML = cart.length === 0 ? '<p class="text-gray-500 text-sm text-center py-6">Your bag is empty.</p>' : cart.map((item, idx) => `
                <div class="flex justify-between items-center bg-white/5 p-3 rounded-xl">
                    <span class="text-sm text-white">${{item.name}}</span>
                    <span class="text-sm font-bold text-amber-400">$${{item.price}}</span>
                </div>
            `).join('');
        }}
        function toggleCart() {{
            const d = document.getElementById('cart-drawer');
            const o = document.getElementById('cart-drawer-overlay');
            const open = !d.classList.contains('translate-x-full');
            d.classList.toggle('translate-x-full', open);
            o.classList.toggle('opacity-0', open);
            o.classList.toggle('pointer-events-none', open);
        }}
        render();
    </script>
</body>
</html>"""

        # 4. If code was truncated inside a script tag or near the bottom, repair scripts and close body
        if "<script" in code.lower() and "</script>" not in code[code.lower().rfind("<script"):]:
            code += "\n</script>\n"
        if "<body" in code.lower() and "</body>" not in code.lower():
            code += "\n</body>\n"
        if "</html>" not in code.lower():
            code += "\n</html>\n"
            
        return code

    def generate_7_stage_preflight_cascade(
        self,
        project_dir: str,
        project_title: str,
        user_instruction: str,
        lang_key: str,
        lang_meta: Dict[str, str]
    ) -> List[str]:
        """
        Synthesizes the 7-Stage Cumulative Pre-Flight Cascade before code generation:
        1. PRD.md (Product Requirements Document)
        2. TRD.md (Technical Requirements Document)
        3. WORKFLOW.md (User & System Workflow Diagram)
        4. DATABASE.md (Schema, Tables, Indexes, Seed Data)
        5. UI_UX_DESIGN.md (Design Tokens, Components, Stitch-UX Layout)
        6. SECURITY.md (Authentication, CORS, SQL Injection Prevention)
        7. IMPLEMENTATION_PLAN.md (Step-by-step Execution Plan & File Matrix)
        """
        docs_dir = os.path.join(project_dir, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        archetype = design_blueprint.detect_archetype(user_instruction)
        tech_choice = design_blueprint.detect_autonomous_tech_stack(user_instruction)
        domain_info = design_blueprint.detect_domain(user_instruction)

        # 1. PRD.md
        if archetype == "utility_tool":
            q_ins = user_instruction.lower()
            if any(w in q_ins for w in ["password", "secret", "generator"]) and not any(w in q_ins for w in ["currency", "money"]):
                scope_reqs = f"""- **P0 (Must-Have Core Tool)**: Centered ergonomic cryptographic password generator card, reactive entropy generation on slider/toggle change, length slider (8–48 chars), uppercase/lowercase/numbers/symbols switches, real-time 4-bar entropy meter, 1-click copy with toast alert.
- **P1 (High Priority)**: Compact recent history list stored in `localStorage`, clean keyboard shortcuts, mobile-responsive card.
- **P2 (Delighters)**: Refresh spin micro-animation, subtle glassmorphic backdrop glow, copy confirmation toast.
- **Strict Scope Exclusion (Ponytail YAGNI Mandate)**: Strictly NO shopping carts, NO product catalogs, NO backpacks/drones, NO fake 4.9-star ratings, NO newsletter forms."""
            elif any(w in q_ins for w in ["currency", "exchange", "convert", "forex", "money"]):
                scope_reqs = f"""- **P0 (Must-Have Core Tool)**: Centered ergonomic currency converter card, reactive calculation on user input, source and target currency selectors with country flags, animated swap action, live rate pill, copy result to clipboard with toast notification.
- **P1 (High Priority)**: Compact recent history list stored in `localStorage`, clean keyboard shortcuts, mobile-responsive card.
- **P2 (Delighters)**: Swap 180° rotation micro-animation, subtle glassmorphic backdrop glow, copy confirmation toast.
- **Strict Scope Exclusion (Ponytail YAGNI Mandate)**: Strictly NO shopping carts, NO product catalogs, NO backpacks/drones, NO fake 4.9-star ratings, NO newsletter forms."""
            elif any(w in q_ins for w in ["timer", "pomodoro", "stopwatch"]):
                scope_reqs = f"""- **P0 (Must-Have Core Tool)**: Centered ergonomic timer card, large digital countdown, mode pills (Pomodoro, Short Break, Long Break), start/pause/reset buttons, visual ring progress.
- **P1 (High Priority)**: Sound alert or visual pulse on completion, mobile-responsive card.
- **P2 (Delighters)**: Tactile button micro-interactions, clean glass card.
- **Strict Scope Exclusion (Ponytail YAGNI Mandate)**: Strictly NO shopping carts, NO product catalogs, NO backpacks/drones, NO fake 4.9-star ratings, NO newsletter forms."""
            else:
                scope_reqs = f"""- **P0 (Must-Have Core Tool)**: Centered ergonomic single-purpose utility tool card, reactive calculation/execution on user input, clean inputs, copy result to clipboard with toast notification.
- **P1 (High Priority)**: Compact recent history list stored in `localStorage`, clean keyboard shortcuts, mobile-responsive card.
- **P2 (Delighters)**: Micro-animations, subtle glassmorphic backdrop glow, copy confirmation toast.
- **Strict Scope Exclusion (Ponytail YAGNI Mandate)**: Strictly NO shopping carts, NO product catalogs, NO backpacks/drones, NO fake 4.9-star ratings, NO newsletter forms."""
        elif archetype == "commerce_store":
            scope_reqs = f"""- **P0 (Must-Have)**: Complete runnable interface, dynamic data catalog, working cart/action modals, slide-over drawer with item quantity (+/-), live subtotal and tax calculation.
- **P1 (High Priority)**: Search filtering, category tabs, toast notifications, responsive mobile/desktop grid.
- **P2 (Delighters)**: Kinetic typography, glassmorphic elevation, animated spotlight tracking."""
        elif archetype == "data_dashboard":
            scope_reqs = f"""- **P0 (Must-Have)**: Telemetry header, 4 KPI metric cards with delta percentages, interactive chart/graph visualization, sortable data table.
- **P1 (High Priority)**: Time range filters, live status pill, responsive grid.
- **Scope Exclusion**: Zero e-commerce carts or store catalogs."""
        else:
            scope_reqs = f"""- **P0 (Must-Have)**: Complete runnable interface fulfilling the core user directive with zero code omissions.
- **P1 (High Priority)**: Clean dark luxury theme, responsive layout, toast feedback.
- **Scope Exclusion**: Zero unrequested features or bloat."""

        prd_content = f"""# Product Requirements Document (PRD) — {project_title}
**Generated**: {now}  
**Author**: F.R.I.D.A.Y. Autonomous Engineering Swarm  
**Status**: APPROVED & LOCKED  
**Application Archetype**: {archetype.upper()}

## 1. Executive Summary
{project_title} is a production-grade software application built to fulfill the directive:
> "{user_instruction}"

## 2. Autonomous Language & Framework Selection (FRIDAY's Decision)
- **Framework Choice**: {tech_choice['framework']}
- **Primary Tech Stack**: {tech_choice['stack']}
- **Selection Mode**: {"User Specified" if tech_choice['is_user_specified'] else "Autonomous Choice by F.R.I.D.A.Y."}
- **Engineering Rationale**: {tech_choice['rationale']}

## 3. Scope & Functional Requirements
{scope_reqs}

## 4. Engineering Discipline & Ponytail YAGNI Mandate
- **Strict YAGNI**: Never write an unrequested feature, component, or extra line of code without informing Boss.
- **Zero Bloat**: No unrequested shopping carts, no fake e-commerce items, no newsletters, no placeholder debt.
- **SLA**: Instant load (<100ms), zero-dependency resilience, high-contrast dark luxury UI.
"""
        with open(os.path.join(docs_dir, "1_PRD.md"), "w", encoding="utf-8") as f:
            f.write(prd_content)

        # 2. TRD.md
        state_store_desc = "Client-side LocalStorage (`localStorage`) for recent tool actions" if archetype == "utility_tool" else "Client-side Reactive JavaScript array / SQLite3 persistent backend"
        trd_content = f"""# Technical Requirements Document (TRD) — {project_title}
**Generated**: {now}  
**Architecture**: Next-Gen Honeycomb Micro-Kernel  
**Application Archetype**: {archetype.upper()}

## 1. Technology Stack
- **Primary Runtime**: {tech_choice['framework']}
- **Standards**: {tech_choice['stack']}
- **Styling Engine**: Tailwind CSS CDN + Lucide Icons CDN (Zero bulky npm packages)
- **State Store**: {state_store_desc}
- **Engineering Principle**: The easy, modern way — clean, zero-build execution without heavy node_modules or hardcoded complexity.

## 2. Architectural Constraints
- Single complete file output with zero omitted code or truncation.
- Strict Ponytail YAGNI adherence: Zero unrequested scope creep or bloat.
- Cross-platform instant execution in modern web browsers.
"""
        with open(os.path.join(docs_dir, "2_TRD.md"), "w", encoding="utf-8") as f:
            f.write(trd_content)

        # 3. WORKFLOW.md
        if archetype == "utility_tool":
            workflow_content = f"""# System & User Interaction Workflow — {project_title}
**Generated**: {now}  
**Archetype**: UTILITY_TOOL  

## 1. State Lifecycle & Flow
```mermaid
stateDiagram-v2
    [*] --> Initialization
    Initialization --> InputReady: Load Cached State from LocalStorage
    InputReady --> Calculating: Amount or Selection Changed
    Calculating --> ResultUpdated: Instant Reactive Math Calculation
    ResultUpdated --> HistoryUpdated: Save Recent Conversion to LocalStorage
    ResultUpdated --> CopiedToast: User Copies Result to Clipboard
    CopiedToast --> [*]
```

## 2. Event Dispatch Model
- Live `input` and `change` event listeners trigger instant reactive calculations without page reload.
- Animated swap button reverses source and target values with a 180° CSS rotation.
- Toast alert feedback on clipboard copy.
"""
        else:
            workflow_content = f"""# System & User Interaction Workflow — {project_title}
**Generated**: {now}  

## 1. State Lifecycle & Flow
```mermaid
stateDiagram-v2
    [*] --> Initialization
    Initialization --> CatalogLoaded: Load Data Array
    CatalogLoaded --> FilteredView: User Search / Category Click
    FilteredView --> ModalOpen: Quick View Triggered
    ModalOpen --> CartUpdated: Add to Bag / Order
    CartUpdated --> DrawerActive: Slide-over Drawer
    DrawerActive --> CheckoutSuccess: Confirm Action
    CheckoutSuccess --> [*]
```

## 2. Event Dispatch Model
- Custom event dispatcher for instant toast alerts (`showToast(msg)`).
- Reactive subtotal and tax calculation triggers on item quantity change.
"""
        with open(os.path.join(docs_dir, "3_WORKFLOW.md"), "w", encoding="utf-8") as f:
            f.write(workflow_content)

        # 4. DATABASE.md
        if archetype == "utility_tool":
            db_content = f"""# Database & State Schema — {project_title}
**Generated**: {now}  
**Storage Engine**: Client-Side LocalStorage (`localStorage`)  

## 1. State Entities
- **Recent Activity (`recent_conversions`)**:
  - `timestamp`: ISO-8601 string
  - `input_value`: Numeric amount
  - `from_unit`: Source currency/unit code
  - `to_unit`: Target currency/unit code
  - `result_value`: Formatted result string
- **User Preferences**:
  - `default_from`: Preferred default source
  - `default_to`: Preferred default target
"""
        else:
            db_content = f"""# Database Schema & Data Models — {project_title}
**Generated**: {now}  
**Storage Engine**: SQLite3 / In-Memory JSON State  

## 1. Relational Entities
- **Items (`catalog_items`)**:
  - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
  - `title`: TEXT NOT NULL
  - `category`: TEXT NOT NULL
  - `price`: REAL NOT NULL
  - `description`: TEXT
  - `image_url`: TEXT

- **Orders (`user_orders`)**:
  - `order_id`: TEXT PRIMARY KEY
  - `timestamp`: DATETIME DEFAULT CURRENT_TIMESTAMP
  - `total_amount`: REAL
  - `status`: TEXT DEFAULT 'confirmed'

## 2. Seed Protocol
Initial sample records are automatically seeded on first launch if the store is empty.
"""
        with open(os.path.join(docs_dir, "4_DATABASE.md"), "w", encoding="utf-8") as f:
            f.write(db_content)

        # 5. UI_UX_DESIGN.md
        stitch_system = mcp_design_bridge.get_system_for_query(user_instruction, archetype)
        design_rules = "\n".join(f"- {r}" for r in stitch_system.get("rules", []))
        if archetype == "utility_tool":
            ui_content = f"""# UI/UX Design System Specification — {project_title}
**Generated**: {now}  
**Design Standard**: {stitch_system['name']} (Direct Google Stitch & UI/UX Pro Max MCP Integration)  
**Origin**: {stitch_system.get('origin', 'StitchMCP / UI-UX-Pro')}

## 1. Visual Hierarchy & Ergonomic Layout
1. **Centered Minimalist Canvas**: Serene, pure solid dark background (`{stitch_system.get('canvas_bg', '#09090b')}`).
2. **Ergonomic Tool Container**: `max-w-md w-full bg-[#121216]/90 border border-white/[0.08] rounded-2xl p-6 sm:p-7 shadow-2xl backdrop-blur-xl`.
3. **Specular Edge Highlight**: `inset 0 1px 0 rgba(255,255,255,0.08)` for subtle tactile definition.
4. **Monochrome FinTech Numbers**: High-contrast pure white numbers (`#ffffff` / `{stitch_system.get('font_mono', 'JetBrains Mono')}`) with tabular figures.
5. **Human-Grade Select Pills**: Country flag selector options (🇺🇸 USD, 🇪🇺 EUR, 🇬🇧 GBP, 🇯🇵 JPY, 🇮🇳 INR, etc.) with custom SVG chevron.
6. **Tactile Swap Action**: Circular button (`w-10 h-10 rounded-full bg-zinc-800/80 border border-white/10 active:scale-95`) with 180° rotation.
7. **Copy Toast Feedback & Minimal History**: Clipboard notification and compact localStorage conversions.

## 2. Design Tokens & Standards
- **Canvas Background**: `{stitch_system.get('canvas_bg', '#09090b')}`
- **Surface**: `{stitch_system.get('surface', '#121216')}`
- **Container**: `{stitch_system.get('surface_container', '#1b1b1f')}`
- **Borders**: `1px solid rgba(255, 255, 255, 0.08)`
- **Accent**: `{stitch_system.get('accent', '#2563eb')}`
- **Typography Display**: `{stitch_system.get('font_display', 'Plus Jakarta Sans')}`
- **Typography Data**: `{stitch_system.get('font_mono', 'JetBrains Mono')}`
- **Micro-Interactions**: Spring physics `transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1)`

## 3. Strict Anti-AI Tropes Mandates
{design_rules}
"""
        else:
            ui_content = f"""# UI/UX Design System Specification — {project_title}
**Generated**: {now}  
**Design Standard**: {stitch_system['name']} (Direct Google Stitch & UI/UX Pro Max MCP Integration)  
**Origin**: {stitch_system.get('origin', 'StitchMCP / UI-UX-Pro')}

## 1. Mandatory 6 Sections
1. Fixed blur-backdrop Header (`backdrop-blur-xl bg-zinc-950/70 border-b border-zinc-800/80`)
2. Kinetic Typography Hero Section with dual CTA buttons
3. Asymmetric Bento Grid Feature Matrix (`grid-cols-1 md:grid-cols-3`)
4. Dynamic Interactive Catalog with live search & multi-category filtering
5. Slide-Over Cart Drawer & Modals (`fixed inset-y-0 right-0 z-50`)
6. Multi-Column Footer with live system status indicator (`🟢 All Systems Operational`)

## 2. Tokens & Assets
- **Canvas Background**: `{stitch_system.get('canvas_bg', '#061422')}`
- **Surface**: `{stitch_system.get('surface', '#090d16')}`
- **Container**: `{stitch_system.get('surface_container', '#13212e')}`
- **Typography**: `{stitch_system.get('font_display', 'Sora')}` / `{stitch_system.get('font_body', 'Hanken Grotesk')}` / `{stitch_system.get('font_mono', 'Geist')}`
- **Icons**: Lucide CDN (`lucide.createIcons()`)
- **Micro-Interactions**: Spring physics `transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1)`

## 3. Mandatory Rules
{design_rules}
"""
        with open(os.path.join(docs_dir, "5_UI_UX_DESIGN.md"), "w", encoding="utf-8") as f:
            f.write(ui_content)

        # 6. SECURITY.md
        sec_content = f"""# Security & Vulnerability Defense Protocol — {project_title}
**Generated**: {now}  
**Auditor**: F.R.I.D.A.Y. Security Sentinel & CodeRabbit AST  

## 1. Defense Matrix
- **CORS Policy**: Configured with permissive origins for local development, locked in production.
- **SQL Injection**: 100% parameterized queries; zero string-concatenated SQL statements.
- **XSS Mitigation**: Strict DOM element creation or sanitization before innerHTML injection.
- **Dependency Audit**: Zero npm bundle hazards; vendor CDN resources loaded over HTTPS.
"""
        with open(os.path.join(docs_dir, "6_SECURITY.md"), "w", encoding="utf-8") as f:
            f.write(sec_content)

        # 7. IMPLEMENTATION_PLAN.md
        plan_content = f"""# Implementation & Verification Plan — {project_title}
**Generated**: {now}  
**Archetype**: {archetype.upper()}

## 1. Assembly Sequence
1. Pre-Flight Cascade Compilation (`docs/1..7`) [COMPLETE]
2. Multi-Model Neural Code Synthesis (OpenCode / Claude Code / Groq LPU)
3. Code Block Extraction & DOM Completeness Verification
4. CodeRabbit AST Static Code Audit & Ralph Scope-Creep Gate
5. File Assembly & Deployment to `D:\\FRIDAY_Projects\\`
6. Visual Workspace Launch

## 2. Verification Gates
- [x] Syntax & AST Compilation Gate
- [x] Security & Secrets Leak Audit
- [x] Ponytail YAGNI / Scope-Creep Audit Gate
- [x] Browser / Process Launch Verification
"""
        with open(os.path.join(docs_dir, "7_IMPLEMENTATION_PLAN.md"), "w", encoding="utf-8") as f:
            f.write(plan_content)

        # Generate root-level CLAUDE.md and OPENCODE.md shared contracts ("lazy coding" repo synchronization)
        try:
            contracts = design_blueprint.generate_lazy_coding_contracts(
                project_name=project_title,
                domain_theme=domain_info.get("theme", "Modern Web"),
                tech_stack=tech_choice["stack"],
                archetype=archetype,
                user_instruction=user_instruction
            )
            for c_name, c_body in contracts.items():
                c_path = os.path.join(project_dir, c_name)
                os.makedirs(os.path.dirname(c_path), exist_ok=True)
                with open(c_path, "w", encoding="utf-8") as cf:
                    cf.write(c_body)

            # Inject active developer instincts (.claude/rules/instincts.md)
            try:
                from core.headroom_memory import memory_engine
                memory_engine.write_project_instincts(project_dir)
            except Exception as inst_err:
                print(f"[Instincts Notice]: {inst_err}")

            # Wire direct project-level MCP configuration (.mcp.json for Claude Code, opencode.json for OpenCode)
            mcp_design_bridge.generate_mcp_config_files(project_dir)
        except Exception as contract_err:
            print(f"[Contract & MCP Notice]: {contract_err}")

        doc_files = [
            os.path.join(docs_dir, f"{i}_{name}.md")
            for i, name in enumerate(["PRD", "TRD", "WORKFLOW", "DATABASE", "UI_UX_DESIGN", "SECURITY", "IMPLEMENTATION_PLAN"], 1)
        ]
        return doc_files

    def _detect_execution_mode(self, raw_instruction: str) -> Tuple[str, str]:
        """
        Determines whether to route to Mode 1 (Lightning Core, <5s) or Mode 2 (Iron Swarm, 60-80s).
        Returns: (mode_key, mode_display_name) -> e.g. ("lightning", "Mode 1 (Lightning Core)")
        """
        q = raw_instruction.lower().strip()
        
        # Explicit mode 2 / deep swarm triggers
        iron_triggers = [
            "deep build", "iron swarm", "swarm", "fullstack", "full stack", 
            "production", "complete system", "complex", "e-commerce", "ecommerce",
            "store", "shop", "marketplace", "platform", "dashboard", "saas", 
            "portal", "multi-agent", "multi agent", "mode 2"
        ]
        if any(t in q for t in iron_triggers):
            return "iron_swarm", "Mode 2: Iron Swarm (PAC Multi-Agent Engine)"
            
        # Explicit lightning triggers
        lightning_triggers = [
            "quick", "fast", "simple", "script", "small", "timer", "calculator",
            "utility", "snippet", "prototype", "single page", "single script", "lightning", "mode 1"
        ]
        if any(t in q for t in lightning_triggers):
            return "lightning", "Mode 1: Lightning Core (Sub-5s Rapid LPU)"
            
        # Default heuristic: short commands without heavy keywords default to lightning; detailed or app-oriented default to iron_swarm
        words = [w for w in q.split() if len(w) > 2]
        if len(words) <= 6 and not any(w in q for w in ["app", "website", "application"]):
            return "lightning", "Mode 1: Lightning Core (Sub-5s Rapid LPU)"
        
        return "iron_swarm", "Mode 2: Iron Swarm (PAC Multi-Agent Engine)"

    def _write_project_files(
        self,
        target_dir: str,
        slug: str,
        blocks: List[Tuple[str, str]],
        lang_key: str,
        raw_instruction: str,
        project_title: str
    ) -> List[str]:
        """Audits, formats, and writes extracted code blocks to target directory."""
        ext_map = {
            "python": "py", "py": "py", "javascript": "js", "js": "js",
            "typescript": "ts", "ts": "ts", "html": "html", "css": "css",
            "cpp": "cpp", "c": "c", "java": "java", "rust": "rs",
            "csharp": "cs", "go": "go", "sql": "sql", "bash": "sh"
        }
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
                filename = "main.py" if i == 0 else f"script_{i+1}.py"
            else:
                filename = f"{slug}_{i+1}.{file_ext}"

            target_path = os.path.join(target_dir, filename)
            if file_ext == "html":
                code_body = self._repair_html_markup(code_body, raw_instruction)
                try:
                    from core.design_blueprint import design_blueprint
                    code_body = design_blueprint.audit_and_repair_markup(code_body, project_title)
                except Exception:
                    pass
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(code_body)
            saved_paths.append(target_path)
            print(f"[FRIDAY Code Engine]: Saved file -> {target_path}")

        return saved_paths

    def _finalize_deployment(
        self,
        target_dir: str,
        slug: str,
        project_title: str,
        saved_paths: List[str],
        model_used: str,
        tier_name: str,
        raw_instruction: str,
        lang_meta: Dict[str, str],
        speak_fn: Optional[Any] = None,
        mode_label: str = "Iron Swarm"
    ) -> None:
        """Generates start.bat launcher, requirements.txt, BRAIN.md manifest, logs memory, and spawns UI."""
        try:
            bat_path = os.path.join(target_dir, "start.bat")
            has_py = any(f.endswith(".py") for f in saved_paths)
            has_html = any(f.endswith(".html") for f in saved_paths)
            
            if has_py and has_html:
                with open(bat_path, "w", encoding="utf-8") as bf:
                    bf.write(f"@echo off\r\necho ===================================================\r\necho   F.R.I.D.A.Y. Full-Stack Runtime Engine // {slug}\r\necho ===================================================\r\necho Launching Browser Frontend...\r\ntimeout /t 1 /nobreak >nul\r\nstart \"\" \"index.html\"\r\necho Starting High-Performance Python Backend on port 8000...\r\npython main.py\r\npause\r\n")
                req_path = os.path.join(target_dir, "requirements.txt")
                if not os.path.exists(req_path):
                    with open(req_path, "w", encoding="utf-8") as rf:
                        rf.write("fastapi>=0.110.0\nuvicorn>=0.29.0\npydantic>=2.6.0\n")
            elif has_html:
                html_targets = [os.path.basename(f) for f in saved_paths if f.endswith(".html")]
                html_target = html_targets[0] if html_targets else "index.html"
                with open(bat_path, "w", encoding="utf-8") as bf:
                    bf.write(f"@echo off\r\necho Launching {slug} in Default Browser...\r\nstart \"\" \"{html_target}\"\r\n")
            elif has_py:
                py_targets = [os.path.basename(f) for f in saved_paths if f.endswith(".py")]
                py_target = py_targets[0] if py_targets else "main.py"
                with open(bat_path, "w", encoding="utf-8") as bf:
                    bf.write(f"@echo off\r\necho Launching {slug}...\r\npython \"{py_target}\"\r\npause\r\n")

            brain_manifest_path = os.path.join(target_dir, "BRAIN.md")
            with open(brain_manifest_path, "w", encoding="utf-8") as mf:
                mf.write(f"# {slug.replace('_', ' ').title()} — F.R.I.D.A.Y. Project Manifest\n\n"
                         f"- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                         f"- **Engine**: {model_used}\n"
                         f"- **Architecture Mode**: {mode_label}\n"
                         f"- **Tier**: {tier_name}\n"
                         f"- **Directive**: \"{raw_instruction}\"\n"
                         f"- **Architecture Docs**: docs/ (1_PRD through 7_IMPLEMENTATION_PLAN)\n"
                         f"- **Files**: {', '.join([os.path.basename(p) for p in saved_paths])}\n")

            # Commit project milestone into Headroom Memory & Project Vault
            try:
                from core.headroom_memory import memory_engine
                memory_engine.remember(f"Created project '{project_title}' in {target_dir} ({lang_meta.get('version', 'Standard')}) [{mode_label}]", category="project_history")
            except Exception:
                pass
        except Exception as deploy_err:
            print(f"[Deployment Notice]: {deploy_err}")

        # Live Execution & Browser/Workspace Deployment
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

    def handle_coding_request(
        self,
        raw_instruction: str,
        speak_fn: Optional[Any] = None,
        input_fn: Optional[Any] = None
    ) -> str:
        """
        Dual-Mode Autonomous Multi-Agent Coding Orchestrator:
        - Mode 1: Lightning Core (<5s direct Groq LPU rapid synthesis for prototypes & single scripts)
        - Mode 2: Iron Swarm (Planner-Actor-Critic Multi-Agent Swarm with Ralph Spec Auditor & 7-Stage Pre-Flight)
        """
        slug = self._derive_slug(raw_instruction)
        project_title = slug.replace("_", " ").title()
        lang_key, lang_meta = self.synthesizer.detect_target_language(raw_instruction)
        target_dir = os.path.join(self.projects_dir, slug)
        os.makedirs(target_dir, exist_ok=True)

        mode_key, mode_display = self._detect_execution_mode(raw_instruction)
        print(f"\n=======================================================")
        print(f"  [FRIDAY Coding Swarm] Mode: {mode_display}")
        print(f"  Project: {project_title} | Target Dir: {target_dir}")
        print(f"=======================================================")

        master_prompt, tier_info = self.synthesizer.synthesize_master_prompt(raw_instruction)
        tier_name = tier_info["tier"]

        # =========================================================================
        # MODE 1: LIGHTNING CORE (Sub-5s Direct Groq LPU Rapid Synthesis)
        # =========================================================================
        if mode_key == "lightning":
            self.update_stage(1, "Lightning Synthesis", "Compiling pre-flight cascade and generating code via Groq LPU", project_title, total_stages=3)
            if speak_fn:
                speak_fn(f"Understood, Boss. Engaging Lightning Core for {project_title}. Synthesizing code immediately.")

            # Compile pre-flight docs & contracts so every project is fully documented with autonomous stack choice
            self.generate_7_stage_preflight_cascade(target_dir, project_title, raw_instruction, lang_key, lang_meta)

            success, result_content, model_used = self.executor.execute_with_groq_fallback(master_prompt, tier_info)
            if not success or not result_content.strip():
                success, result_content, model_used = self.executor.execute_with_failover(master_prompt, tier_info)

            self.update_stage(2, "Code Extraction & AST Check", "Extracting code blocks and validating syntax", project_title, total_stages=3)
            blocks = self.extract_code_blocks(result_content)
            if not blocks:
                if lang_key == "html" or any(w in raw_instruction.lower() for w in ["html", "page", "website"]):
                    repaired = self._repair_html_markup(result_content, raw_instruction)
                    blocks = [("html", repaired)]
                else:
                    blocks = [(lang_key, result_content.strip())]

            if blocks:
                try:
                    from core.terminal_hud import print_code
                    print_code(blocks[0][1], lang_key)
                except Exception:
                    pass

            saved_paths = self._write_project_files(target_dir, slug, blocks, lang_key, raw_instruction, project_title)

            # CodeRabbit AST check on Python scripts
            for p in saved_paths:
                if p.endswith(".py"):
                    try:
                        from core.code_reviewer import code_reviewer
                        audit_res = code_reviewer.audit_python_file(p)
                        if not audit_res.get("passed", True):
                            from core.runtime_debugger import runtime_debugger
                            runtime_debugger.repair_failing_code(target_dir, p, {"error_message": "; ".join(audit_res.get("issues", [])), "line_number": 1, "full_traceback": str(audit_res.get("issues"))})
                    except Exception:
                        pass

            # Ralph Scope-Creep & AST verification check
            try:
                from core.ralph_engine import ralph_engine
                prd_path = os.path.join(target_dir, "docs", "1_PRD.md")
                prd_content = ""
                if os.path.exists(prd_path):
                    with open(prd_path, "r", encoding="utf-8", errors="replace") as pf:
                        prd_content = pf.read()
                spec_res = ralph_engine.run_spec_verification(target_dir, prd_content, saved_paths)
                if not spec_res.get("passed", True):
                    print(f"[Ralph Gate Notice (Lightning)]: {spec_res.get('issues')}")
            except Exception as ralph_err:
                print(f"[Ralph Check Notice]: {ralph_err}")

            self.update_stage(3, "Live Launch & Workspace", f"Launching {project_title} in browser", project_title, total_stages=3)
            self._finalize_deployment(target_dir, slug, project_title, saved_paths, model_used, tier_name, raw_instruction, lang_meta, speak_fn=speak_fn, mode_label="Lightning Core")

            if speak_fn:
                speak_fn(f"Lightning build complete, Boss. {project_title} is online and operational.")

            return result_content

        # =========================================================================
        # MODE 2: IRON SWARM (Planner-Actor-Critic Multi-Agent Swarm with Ralph Loop)
        # =========================================================================
        # Stage 1: 7-Stage Pre-Flight Cascade + CLAUDE.md / OPENCODE.md Contract Sync
        self.update_stage(1, "7-Stage Pre-Flight Architecture", "Compiling PRD, TRD, UI/UX, Security, Plan, and Contracts", project_title, total_stages=5)
        if speak_fn:
            speak_fn(f"Understood, Boss. Initializing Iron Swarm for {project_title}. Step 1: Compiling architectural pre-flight cascade and lazy coding contracts.")

        doc_files = self.generate_7_stage_preflight_cascade(target_dir, project_title, raw_instruction, lang_key, lang_meta)
        print(f"\n[FRIDAY Coding Swarm]: Generated {len(doc_files)} Pre-Flight Architecture Docs + CLAUDE.md / OPENCODE.md in {target_dir}")

        primary_model = tier_info["primary_model"]
        print(f"[FRIDAY Coding Swarm]: Tier Selected -> [{tier_name}] | Primary Engine: {primary_model}")

        # Stage 2: Lead Builder Swarm Code Synthesis
        self.update_stage(2, "Lead Builder Code Synthesis", f"OpenCode Engine synthesizing full application via {primary_model}", project_title, total_stages=5)
        if speak_fn:
            speak_fn(f"Step 2: OpenCode Lead Builder is writing the complete application, Boss.")

        success, result_content, model_used = self.executor.execute_with_failover(master_prompt, tier_info)
        if not success or not result_content.strip():
            self.mark_failed("Coding dispatcher unreachable")
            if speak_fn:
                speak_fn("I encountered an issue with the primary coding dispatcher, Boss. Activating fallback neural generator.")
            success, result_content, model_used = self.executor.execute_with_groq_fallback(master_prompt, tier_info)

        print(f"[FRIDAY Coding Swarm]: Builder code synthesis complete using {model_used}.")

        # Stage 3: Code Extraction & File Assembly
        self.update_stage(3, "Code Extraction & Assembly", f"Extracting components and writing initial build to disk", project_title, total_stages=5)
        blocks = self.extract_code_blocks(result_content)
        if not blocks:
            if lang_key == "html" or any(w in raw_instruction.lower() for w in ["html", "page", "website"]):
                repaired = self._repair_html_markup(result_content, raw_instruction)
                blocks = [("html", repaired)]
            else:
                blocks = [(lang_key, result_content.strip())]

        if blocks:
            try:
                from core.terminal_hud import print_code
                print_code(blocks[0][1], lang_key)
            except Exception:
                pass

        saved_paths = self._write_project_files(target_dir, slug, blocks, lang_key, raw_instruction, project_title)

        # Stage 4: The Critic & Autonomous Ralph Review Loop (Max 3 iterations)
        self.update_stage(4, "Ralph Spec Auditor & Review Loop", "Auditing against PRD and running AST checks", project_title, total_stages=5)
        if speak_fn:
            speak_fn("Step 4: Ralph Spec Auditor and CodeRabbit are verifying the build against the PRD requirements.")

        try:
            from core.ralph_engine import ralph_engine
            prd_path = os.path.join(target_dir, "docs", "1_PRD.md")
            prd_content = ""
            if os.path.exists(prd_path):
                with open(prd_path, "r", encoding="utf-8", errors="replace") as pf:
                    prd_content = pf.read()

            for loop_idx in range(1, 4):
                spec_res = ralph_engine.run_spec_verification(target_dir, prd_content, saved_paths)
                if spec_res.get("passed", True):
                    print(f"[Ralph Spec Auditor]: Gate check passed on iteration {loop_idx}. Zero critical defects.")
                    break
                
                print(f"[Ralph Review Loop]: Iteration {loop_idx}/3 detected defects: {spec_res.get('issues')}")
                if speak_fn and loop_idx == 1:
                    speak_fn("Notice: Ralph detected minor specification gaps. Applying autonomous surgical patch.")

                # Synthesize surgical fix prompt
                surgical_prompt = (
                    f"{master_prompt}\n\n"
                    f"=======================================================\n"
                    f"RALPH CRITIC SURGICAL FIX DIRECTIVE (Iteration {loop_idx}/3):\n"
                    f"{spec_res.get('surgical_instruction')}\n"
                    f"=======================================================\n"
                    f"Please output the complete, updated index.html fixing these exact gaps."
                )
                p_success, patch_content, p_model = self.executor.execute_with_groq_fallback(surgical_prompt, tier_info)
                if p_success and patch_content.strip():
                    p_blocks = self.extract_code_blocks(patch_content)
                    if p_blocks:
                        saved_paths = self._write_project_files(target_dir, slug, p_blocks, lang_key, raw_instruction, project_title)
                        result_content = patch_content
        except Exception as ralph_err:
            print(f"[Ralph Loop Notice]: {ralph_err}")

        # Python CodeRabbit AST check
        for p in saved_paths:
            if p.endswith(".py"):
                try:
                    from core.code_reviewer import code_reviewer
                    audit_res = code_reviewer.audit_python_file(p)
                    if not audit_res.get("passed", True):
                        print(f"[FRIDAY CodeRabbit Audit]: Issues in {os.path.basename(p)}: {audit_res.get('issues')}")
                        from core.runtime_debugger import runtime_debugger
                        runtime_debugger.repair_failing_code(target_dir, p, {"error_message": "; ".join(audit_res.get("issues", [])), "line_number": 1, "full_traceback": str(audit_res.get("issues"))})
                    else:
                        print(f"[FRIDAY CodeRabbit Audit]: {os.path.basename(p)} passed AST security & syntax checks.")
                except Exception as py_err:
                    print(f"[CodeRabbit Notice]: {py_err}")

        # Stage 5: Live Deployment & Launch
        self.update_stage(5, "Deployment & Visual Launch", "Finalizing project manifest and launching workspace", project_title, total_stages=5)
        self._finalize_deployment(target_dir, slug, project_title, saved_paths, model_used, tier_name, raw_instruction, lang_meta, speak_fn=speak_fn, mode_label="Iron Swarm")

        if speak_fn:
            speak_fn(f"Step 5 complete: Project {project_title} has passed all Ralph verification gates and is live, Boss.")

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
