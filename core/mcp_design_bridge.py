"""
========================================================================================
F.R.I.D.A.Y. OS 10.0: MCP Design System Bridge
Directly interfaces F.R.I.D.A.Y.'s engine with UI/UX Pro Max MCP and Google Stitch Design Systems
Enforces Quiet Luxury, Human Tactile Craftsmanship, and Zero AI Tropes across All Code Swarms
========================================================================================
"""

import os
import json
from typing import Dict, Any

class MCPDesignBridge:
    """
    Direct bridge to Google Stitch Design Systems & UI/UX Pro Max Tokens.
    Ensures F.R.I.D.A.Y., Claude Code, and OpenCode have zero impedance access to:
    1. Google Stitch MCP (https://stitch.googleapis.com/mcp)
    2. UI/UX Pro Max MCP (ui-ux-pro-mcp)
    """

    # 1. Google Stitch Design Systems (extracted directly from StitchMCP designMd registry)
    STITCH_SYSTEMS: Dict[str, Dict[str, Any]] = {
        "apple_stripe_editorial": {
            "name": "Apple × Stripe × Notion · Clean Minimalist Architecture",
            "origin": "Modern Cupertino & Editorial Standard",
            "canvas_bg": "#fbfbfa",
            "canvas_bg_dark": "#09090b",
            "surface": "#ffffff",
            "surface_dark": "#121216",
            "surface_container": "#f4f4f5",
            "surface_border": "border border-zinc-200/80",
            "specular_highlight": "inset 0 1px 0 rgba(255,255,255,1)",
            "input_bg": "bg-zinc-50",
            "input_border": "border border-zinc-200 focus-within:border-indigo-500",
            "text_display": "text-zinc-900 font-semibold",
            "text_muted": "text-zinc-500",
            "text_subtle": "text-zinc-400",
            "accent": "#6366f1",  # Stripe Indigo
            "font_display": "Plus Jakarta Sans",
            "font_body": "Inter",
            "font_mono": "JetBrains Mono",
            "rules": [
                "DEFAULT TO CLEAN LIGHT MODE: Warm linen/porcelain background (#fbfbfa / #ffffff) with deep graphite typography (#09090b / #0f172a).",
                "SEAMLESS ☀️/🌙 THEME SWITCHER: Provide an ergonomic, tactile theme toggle button in the header saving preference in localStorage.",
                "TAILWIND DUAL-THEME ARCHITECTURE: Use Tailwind 'dark' class on <html> with dual classes (e.g. bg-[#fbfbfa] dark:bg-[#09090b], bg-white dark:bg-[#121216], text-zinc-900 dark:text-zinc-50).",
                "APPLE-GRADE REFINEMENT: Soft diffused card drop shadow (0 20px 40px -15px rgba(0,0,0,0.05)), subtle hairline borders (border-zinc-200/80), and frosted glass blur (backdrop-blur-xl).",
                "STRIPE-GRADE TACTILITY: Monospace JetBrains Mono for figures, smooth spring transitions cubic-bezier(0.16, 1, 0.3, 1), tactile button presses.",
                "NOTION-GRADE CLARITY: Distraction-free serene whitespace, readable typography scale, calm aesthetic."
            ]
        },
        "fintech_utility": {
            "name": "Google Stitch · High-Frequency Terminal & Financial Clarity",
            "origin": "StitchMCP / projects/4184006083500341519",
            "canvas_bg": "#09090b",
            "surface": "#121216",
            "surface_container": "#1b1b1f",
            "surface_border": "border border-white/[0.08]",
            "specular_highlight": "inset 0 1px 0 rgba(255,255,255,0.08)",
            "input_bg": "bg-white/[0.03]",
            "input_border": "border border-white/[0.08] focus-within:border-white/[0.22] focus-within:ring-1 focus-within:ring-white/[0.12]",
            "text_display": "text-white font-semibold",
            "text_muted": "text-zinc-400",
            "text_subtle": "text-zinc-500",
            "accent": "#2563eb",  # Refined Royal Sapphire
            "accent_pill": "bg-blue-500/10 text-blue-400 border border-blue-500/20",
            "font_display": "Plus Jakarta Sans",
            "font_body": "Inter",
            "font_mono": "JetBrains Mono",
            "rules": [
                "ABSOLUTELY NO matrix grids (.bg-grid) or cybernetic line work.",
                "ABSOLUTELY NO floating neon blur balls (.glow-a, .glow-b). Serene, pure dark canvas.",
                "ABSOLUTELY NO glowing neon green numbers. All numerical calculations must be crisp, high-contrast white (#ffffff) in JetBrains Mono.",
                "Custom styled currency select pills with real country flags (🇺🇸 USD, 🇪🇺 EUR, 🇬🇧 GBP, 🇯🇵 JPY, 🇮🇳 INR, 🇨🇦 CAD, 🇦🇺 AUD, 🇨🇭 CHF).",
                "Spring timing micro-interactions: cubic-bezier(0.16, 1, 0.3, 1)."
            ]
        },
        "quiet_luxury": {
            "name": "Google Stitch · Quiet Luxury & Minimalist Tactility",
            "origin": "StitchMCP / Modern Architectural Standard",
            "canvas_bg": "#08080a",
            "surface": "#101014",
            "surface_container": "#18181c",
            "surface_border": "border border-white/[0.07]",
            "specular_highlight": "inset 0 1px 0 rgba(255,255,255,0.06)",
            "input_bg": "bg-white/[0.02]",
            "input_border": "border border-white/[0.07] focus-within:border-white/[0.20]",
            "text_display": "text-zinc-50 font-medium",
            "text_muted": "text-zinc-400",
            "text_subtle": "text-zinc-600",
            "accent": "#71717a",
            "font_display": "Plus Jakarta Sans",
            "font_body": "Plus Jakarta Sans",
            "font_mono": "JetBrains Mono",
            "rules": [
                "Zero visual clutter or decorative gimmicks.",
                "Pure focus on typographical precision, generous padding, and tactile response.",
                "Subtle 1px specular highlight at the top border of cards."
            ]
        },
        "stitch_commerce": {
            "name": "Google Stitch · Luminous Ethereal Commerce",
            "origin": "StitchMCP / projects/871340406160357717",
            "canvas_bg": "#061422",
            "surface": "#090d16",
            "surface_container": "#13212e",
            "surface_border": "border border-zinc-800/80",
            "on_surface": "#d6e4f7",
            "primary": "#c3c6d3",
            "secondary": "#ffd700",
            "accent": "#00dbe7",
            "font_display": "Sora",
            "font_body": "Hanken Grotesk",
            "font_mono": "Geist",
            "rules": [
                "Use full 6-section narrative exclusively for actual stores and food menus.",
                "Glassmorphism mid-layer with 20px backdrop-blur and 1px inner stroke.",
                "Kinetic typography with fluid clamping."
            ]
        },
        "institutional_trading": {
            "name": "Google Stitch · Institutional Trading Interface",
            "origin": "StitchMCP / projects/7286204771471037328",
            "canvas_bg": "#111417",
            "surface": "#191c1f",
            "surface_container": "#1d2023",
            "surface_border": "border border-[#2B2F36]",
            "text_display": "text-[#e1e2e7]",
            "font_display": "Inter",
            "font_body": "Inter",
            "font_mono": "IBM Plex Mono",
            "rules": [
                "Zero-depth flat technical chromatic layering.",
                "Tabular numbers with monospace alignment."
            ]
        },
        "tactical_hud": {
            "name": "Google Stitch · Tactical HUD Interface",
            "origin": "StitchMCP / projects/9746355387328727322",
            "canvas_bg": "#131313",
            "surface": "#1f1f1f",
            "surface_container": "#2a2a2a",
            "surface_border": "border border-zinc-700/60",
            "text_display": "text-white font-bold",
            "font_display": "Space Grotesk",
            "font_body": "Geist",
            "font_mono": "JetBrains Mono",
            "rules": [
                "Technical telemetry layout with 4px grid rhythm.",
                "Subtle luminance over shadows."
            ]
        },
        "security_utility": {
            "name": "Google Stitch · Cryptographic Security & Password Craft",
            "origin": "StitchMCP / Quiet Luxury Security Standard",
            "canvas_bg": "#09090b",
            "surface": "#121216",
            "surface_container": "#18181c",
            "surface_border": "border border-white/[0.08]",
            "specular_highlight": "inset 0 1px 0 rgba(255,255,255,0.08)",
            "input_bg": "bg-white/[0.03]",
            "input_border": "border border-white/[0.08] focus-within:border-white/[0.22]",
            "text_display": "text-white font-semibold",
            "text_muted": "text-zinc-400",
            "text_subtle": "text-zinc-500",
            "accent": "#6366f1",
            "font_display": "Plus Jakarta Sans",
            "font_body": "Inter",
            "font_mono": "JetBrains Mono",
            "rules": [
                "ABSOLUTELY NO matrix grids (.bg-grid) or cybernetic line work.",
                "ABSOLUTELY NO floating neon blur balls (.glow-a, .glow-b). Serene, pure dark canvas.",
                "ABSOLUTELY NO radioactive neon green text. High-contrast pure white (#ffffff) typography in JetBrains Mono.",
                "1-click copy action with toast feedback ('Copied to clipboard').",
                "Spring timing micro-interactions: cubic-bezier(0.16, 1, 0.3, 1)."
            ]
        },
    }

    # 2. UI/UX Pro Max Design Intelligence & CSS Tokens
    UI_UX_PRO_TOKENS = {
        "fonts": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=Sora:wght@600;700;800&display=swap",
        "tailwind_cdn": "https://cdn.tailwindcss.com",
        "lucide_cdn": "https://unpkg.com/lucide@latest",
        "spring_transition": "transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
        "button_hover": "transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,0,0,0.25)",
        "button_active": "transform: translateY(0px) scale(0.98)",
        "card_depth": "box-shadow: 0 20px 40px -15px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.08)",
        "trust_badge": "display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px; border-radius: 9999px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);",
        "conversion_focus": "outline: 2px solid #2563eb; outline-offset: 2px;"
    }

    def get_system_for_query(self, query: str, archetype: str) -> Dict[str, Any]:
        """Dynamically matches project query to optimal Google Stitch + UI/UX Pro design system."""
        q = query.lower()
        is_explicit_dark = any(w in q for w in ["dark mode", "dark theme", "in dark", "night mode", "obsidian"])

        # Flagship standard: Apple × Stripe × Notion clean light architecture with built-in dark toggle
        if not is_explicit_dark:
            return self.STITCH_SYSTEMS["apple_stripe_editorial"]

        if archetype == "utility_tool":
            if any(w in q for w in ["password", "secret", "hash", "key", "token", "generator"]):
                return self.STITCH_SYSTEMS["security_utility"]
            elif any(w in q for w in ["currency", "crypto", "convert", "exchange", "money", "forex", "calculator"]):
                return self.STITCH_SYSTEMS["fintech_utility"]
            return self.STITCH_SYSTEMS["quiet_luxury"]
        elif archetype == "commerce_store":
            return self.STITCH_SYSTEMS["stitch_commerce"]
        elif archetype == "data_dashboard":
            if any(w in q for w in ["trade", "crypto", "terminal", "market"]):
                return self.STITCH_SYSTEMS["institutional_trading"]
            return self.STITCH_SYSTEMS["tactical_hud"]
        return self.STITCH_SYSTEMS["quiet_luxury"]

    def generate_human_design_prompt_clause(self, query: str, archetype: str) -> str:
        """
        Synthesizes a direct, comprehensive design directive enforcing Google Stitch + UI/UX Pro Max tokens
        and strictly banning AI tropes (grids, neon blobs, glowing green numbers).
        """
        system = self.get_system_for_query(query, archetype)
        rules_text = "\n".join(f"- {r}" for r in system["rules"])
        q = query.lower()
        is_password = any(w in q for w in ["password", "secret", "generator"]) and not any(w in q for w in ["currency", "money"])
        is_currency = any(w in q for w in ["currency", "exchange", "forex", "money", "convert"])
        is_timer = any(w in q for w in ["timer", "pomodoro", "stopwatch", "clock"])

        if archetype == "utility_tool":
            if is_password:
                tool_specific_controls = """3. High-Contrast Monospace Password Display (Dual Theme):
   - Generated Password Box: Crisp high-contrast characters in JetBrains Mono (`bg-zinc-50 dark:bg-black/30 border border-zinc-200/80 dark:border-white/[0.08] text-zinc-900 dark:text-white font-mono text-xl sm:text-2xl font-semibold tracking-wider select-all break-all`).
   - Integrated action controls: Subtle refresh icon button (regenerates on click with 180° rotation) and copy button with toast alert.
4. Human-Grade Security Controls:
   - Password Length Slider: Smooth slider (range 8 to 48, default 16) with live numeric value badge.
   - Character Set Toggles: Tactile pill switches or checkboxes for:
     - [x] Uppercase (A-Z)
     - [x] Lowercase (a-z)
     - [x] Numbers (0-9)
     - [x] Symbols (!@#$%^&*)
   - Entropy Strength Bar: Minimalist 4-segment meter (Weak, Fair, Good, Strong) showing real-time password security."""
            elif is_currency:
                tool_specific_controls = """3. Human FinTech Typography & Color Hierarchy (Dual Theme):
   - Numerical Inputs: Crisp high-contrast (`text-zinc-900 dark:text-white font-mono text-2xl sm:text-3xl font-semibold tracking-tight`).
   - Calculated Output: Crisp high-contrast (`text-zinc-800 dark:text-zinc-50 font-mono text-2xl sm:text-3xl font-semibold tracking-tight`).
   - Status / Rate Pill: Refined subtle badge (`bg-zinc-100 dark:bg-white/[0.04] border border-zinc-200 dark:border-white/[0.08] text-zinc-600 dark:text-zinc-400 text-xs py-1.5 px-3 rounded-full`).
4. Human-Grade Form Controls & Row Ergonomics:
   - Currency Selectors: Style them with country flags in the options (🇺🇸 USD, 🇪🇺 EUR, 🇬🇧 GBP, 🇯🇵 JPY, 🇮🇳 INR, 🇨🇦 CAD, 🇦🇺 AUD, 🇨🇭 CHF, 🇸🇬 SGD, 🇦🇪 AED).
   - Row Layout: Use rigid grid `grid grid-cols-12 gap-3 items-center` with selector `col-span-5` and amount input `col-span-7 text-right min-w-0`.
   - Swap button: Circular button (`w-10 h-10 rounded-full bg-white dark:bg-zinc-800/80 border border-zinc-200 dark:border-white/10 hover:border-zinc-300 dark:hover:border-white/20 active:scale-95`) with 180° rotation.
   - Recent Conversions: Clean compact list of 3 items."""
            elif is_timer:
                tool_specific_controls = """3. Digital Time Readout (Dual Theme):
   - Large digital countdown (`font-mono text-5xl sm:text-6xl font-bold text-zinc-900 dark:text-white tracking-tight text-center my-6`).
4. Human-Grade Timer Controls:
   - Mode selector pills (Pomodoro 25m, Short Break 5m, Long Break 15m).
   - Tactile Start/Pause and Reset spring action buttons.
   - Circular SVG countdown ring or clean linear progress bar."""
            else:
                tool_specific_controls = """3. High-Contrast Typography:
   - Primary values in crisp JetBrains Mono (`text-zinc-900 dark:text-white font-mono font-semibold`).
4. Ergonomic Controls:
   - Clean inputs and tactile spring action buttons.
   - One-click copy with toast alert feedback."""

            return f"""=======================================================================
GOOGLE STITCH & UI/UX PRO MAX DESIGN SYSTEM SPECIFICATION:
=======================================================================
DESIGN FRAMEWORK: {system['name']} (Engineered via StitchMCP & UI/UX Pro Max)

HUMAN CRAFTSMANSHIP & AESTHETIC DIRECTIVES (APPLE × STRIPE × NOTION HYBRID + DUAL THEME):
1. Dual Theme System (Default Light Mode + Dark Mode Support):
   - Configure Tailwind CDN with class-based dark mode:
     `<script>tailwind.config = {{ darkMode: 'class' }};</script>`
   - Default State: Serene Apple × Stripe × Notion clean light aesthetic:
     - Canvas: Warm linen / porcelain (`bg-[#fbfbfa] dark:bg-[#09090b] text-zinc-900 dark:text-zinc-100 min-h-screen flex items-center justify-center p-4`).
     - Card: Elevated pure white (`max-w-md w-full bg-white dark:bg-[#121216]/90 border border-zinc-200/80 dark:border-white/[0.08] rounded-2xl p-6 sm:p-7 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)] dark:shadow-2xl backdrop-blur-xl`).
   - Tactile ☀️/🌙 Theme Switcher:
     - Include an ergonomic theme toggle button in the card header (`onclick="toggleTheme()"`).
     - Store preference in `localStorage.getItem('theme')` (defaulting to 'light', or 'dark' if dark mode was explicitly requested).
   - ABSOLUTELY NO matrix grid lines (.bg-grid).
   - ABSOLUTELY NO floating neon blur balls (.glow-a, .glow-b).
2. The Focused Ergonomic Tool Card:
   - Centered container with generous whitespace, clean typographic hierarchy, and Apple-grade card radius.
{tool_specific_controls}
5. Micro-Interactions (Apple / Stripe Spring Timing):
   - Interactive buttons: `transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1)`.
   - Copy action: Subtle toast alert with checkmark icon ("Copied to clipboard").

MANDATORY RULES:
{rules_text}
"""
        else:
            return f"""=======================================================================
GOOGLE STITCH & UI/UX PRO MAX DESIGN SYSTEM SPECIFICATION:
=======================================================================
DESIGN FRAMEWORK: {system['name']}
- Primary Palette: Canvas {system.get('canvas_bg')} | Surface {system.get('surface')} | Container {system.get('surface_container')}
- Typography: Display: {system['font_display']}, Body: {system['font_body']}, Data: {system['font_mono']}
- Surface Strategy: Chromatic Layering with specular border highlights (1px solid rgba(255,255,255,0.08)).
- Micro-Interactions: Spring physics `transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1)`.
- Mandatory Rules:
{rules_text}
"""

    def generate_mcp_config_files(self, project_dir: str) -> Dict[str, str]:
        """
        Directly wires project workspace to UI/UX Pro Max MCP and Google Stitch.
        Generates:
        1. .mcp.json (Standard Claude Code / Anthropic MCP contract)
        2. opencode.json (OpenCode Multi-Model Agent MCP schema)
        3. .agents/mcp_config.json (Workspace MCP bridge)
        """
        os.makedirs(project_dir, exist_ok=True)

        stitch_key = os.environ.get("STITCH_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
        stitch_args = ["-y", "mcp-remote", "https://stitch.googleapis.com/mcp"]
        if stitch_key:
            stitch_args.extend(["--header", f"X-Goog-Api-Key: {stitch_key}"])

        claude_mcp = {
            "mcpServers": {
                "ui-ux-pro": {
                    "command": "npx",
                    "args": ["-y", "ui-ux-pro-mcp", "--stdio"]
                },
                "StitchMCP": {
                    "command": "npx",
                    "args": stitch_args
                }
            }
        }

        opencode_mcp = {
            "$schema": "https://opencode.ai/config.json",
            "mcp": {
                "ui-ux-pro": {
                    "type": "stdio",
                    "command": "npx",
                    "args": ["-y", "ui-ux-pro-mcp", "--stdio"]
                },
                "StitchMCP": {
                    "type": "stdio",
                    "command": "npx",
                    "args": stitch_args
                }
            }
        }

        # 1. Write .mcp.json for Claude Code
        mcp_path = os.path.join(project_dir, ".mcp.json")
        try:
            with open(mcp_path, "w", encoding="utf-8") as f:
                json.dump(claude_mcp, f, indent=2)
        except Exception as e:
            print(f"[MCPDesignBridge]: Error writing .mcp.json: {e}")

        # 2. Write opencode.json for OpenCode
        opencode_path = os.path.join(project_dir, "opencode.json")
        try:
            with open(opencode_path, "w", encoding="utf-8") as f:
                json.dump(opencode_mcp, f, indent=2)
        except Exception as e:
            print(f"[MCPDesignBridge]: Error writing opencode.json: {e}")

        # 3. Write .agents/mcp_config.json
        agents_dir = os.path.join(project_dir, ".agents")
        os.makedirs(agents_dir, exist_ok=True)
        try:
            with open(os.path.join(agents_dir, "mcp_config.json"), "w", encoding="utf-8") as f:
                json.dump(claude_mcp, f, indent=2)
        except Exception as e:
            print(f"[MCPDesignBridge]: Error writing .agents/mcp_config.json: {e}")

        return {
            ".mcp.json": mcp_path,
            "opencode.json": opencode_path
        }


# Global singleton instance
mcp_design_bridge = MCPDesignBridge()
