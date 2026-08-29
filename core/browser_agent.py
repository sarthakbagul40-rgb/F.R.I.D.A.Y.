"""
F.R.I.D.A.Y. Autonomous Browser Agent (AI Hands)
Powered by browser-use, Playwright, and OmniRoute / Gemini Multi-Provider Intelligence.
Also configures Brave Browser as the primary desktop web engine.
"""

import os
import sys
import asyncio
import subprocess
import webbrowser
from typing import Optional, Tuple, Dict, Any

# Locate Brave Browser on Windows
BRAVE_CANDIDATES = [
    os.path.expandvars(r"%PROGRAMFILES%\BraveSoftware\Brave-Browser\Application\brave.exe"),
    os.path.expandvars(r"%PROGRAMFILES(X86)%\BraveSoftware\Brave-Browser\Application\brave.exe"),
    os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe")
]

BRAVE_EXE = next((p for p in BRAVE_CANDIDATES if os.path.exists(p)), None)

if BRAVE_EXE:
    try:
        webbrowser.register('brave', None, webbrowser.BackgroundBrowser(BRAVE_EXE))
    except Exception:
        pass


def open_in_brave(url: str) -> bool:
    """Opens a URL specifically in Brave Browser with fallback to system default."""
    if BRAVE_EXE and os.path.exists(BRAVE_EXE):
        try:
            subprocess.Popen([BRAVE_EXE, url])
            return True
        except Exception:
            pass
    try:
        webbrowser.open(url)
        return True
    except Exception:
        return False


class AutonomousBrowserManager:
    """Manages AI-driven autonomous web navigation, form interactions, and multi-tab research."""

    def __init__(self):
        self.omniroute_url = "http://localhost:20128/v1"
        self.gemini_url = "http://localhost:8081/v1"

    async def _execute_task_async(self, instruction: str) -> str:
        """Runs browser-use agent asynchronously."""
        try:
            from browser_use import Agent
            from langchain_openai import ChatOpenAI
        except ImportError:
            try:
                from browser_use import Agent
                from openai import OpenAI
            except ImportError:
                return "Browser-use agent components are loading. Please try again in a moment."

        try:
            # 1. Initialize LLM pointing to local OmniRoute Gateway
            try:
                from langchain_openai import ChatOpenAI
                llm = ChatOpenAI(
                    base_url=self.omniroute_url,
                    api_key="omniroute-local",
                    model="auto/best-fast",
                    temperature=0.2
                )
            except Exception:
                from langchain_google_genai import ChatGoogleGenerativeAI
                llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

            agent = Agent(
                task=instruction,
                llm=llm,
            )
            history = await agent.run()
            result = history.final_result()
            return str(result) if result else "Web automation task completed successfully."
        except Exception as e:
            return f"Autonomous browsing error: {e}"

    def execute_task(self, instruction: str, speak_fn=None) -> str:
        """Synchronous wrapper for F.R.I.D.A.Y. main voice loop."""
        if speak_fn:
            speak_fn("Deploying autonomous browser agent, Boss. Navigating now...")
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._execute_task_async(instruction))
            loop.close()
            return result
        except Exception as e:
            return f"Browser Agent error: {e}"


# Global singleton instance
browser_agent = AutonomousBrowserManager()
