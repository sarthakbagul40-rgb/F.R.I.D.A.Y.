"""
========================================================================================
F.R.I.D.A.Y. OS 10.0: Intent-Adaptive Design Blueprint & Autonomous Tech Stack Engine
Harmonizes Google Stitch UX, UI/UX Pro Design Tokens, and the Ponytail YAGNI Rule
========================================================================================
"""

import os
import re
from typing import Dict, Any, Optional
from core.mcp_design_bridge import mcp_design_bridge

# =====================================================================
# 1. UI/UX PRO DESIGN TOKEN SYSTEM
# =====================================================================
UI_UX_PRO_DESIGN_TOKENS = {
    "fonts": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap",
    "tailwind_cdn": "https://cdn.tailwindcss.com",
    "lucide_cdn": "https://unpkg.com/lucide@latest",
    "theme": {
        "bg_canvas_light": "#fbfbfa",
        "bg_canvas_dark": "#09090b",
        "bg_surface_light": "#ffffff",
        "bg_surface_dark": "#121216",
        "border_subtle_light": "border-zinc-200/80",
        "border_subtle_dark": "border-white/[0.08]",
        "text_primary_light": "text-zinc-900",
        "text_primary_dark": "text-zinc-100",
        "text_secondary_light": "text-zinc-500",
        "text_secondary_dark": "text-zinc-400",
        "accent_stripe": "#6366f1",
        "shadow_apple": "shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)]",
        "glass_blur": "backdrop-blur-xl",
    }
}

# =====================================================================
# 2. INTENT-ADAPTIVE ARCHITECTURAL BLUEPRINTS
# =====================================================================

# Archetype A: Ergonomic Single-Purpose Utility Tool (Apple × Stripe × Notion Architecture)
UTILITY_TOOL_BLUEPRINT = """
UTILITY TOOL BLUEPRINT (Ergonomic Single-Purpose Tool Card):
Design Standard: Inspired by Apple, Stripe, Notion, and Linear.
Structure:
1. [FOCUSED ERGONOMIC CARD CONTAINER]:
   - Centered on screen (`min-h-screen flex items-center justify-center p-4 bg-[#fbfbfa] dark:bg-[#09090b] text-zinc-900 dark:text-zinc-100`).
   - Premium card (`max-w-lg w-full bg-white dark:bg-[#121216]/90 border border-zinc-200/80 dark:border-white/[0.08] rounded-2xl p-6 sm:p-8 backdrop-blur-xl shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)] dark:shadow-2xl`).
   - Minimalist header: Clean icon badge, title with crisp typography, concise purpose subtitle, and a discreet ☀️/🌙 theme toggle button.
2. [INTERACTIVE INPUT & ENGINE]:
   - Laser-focused controls tailored precisely to the requested tool (e.g. length slider, character toggles, entropy meter for password generator; currency selectors with flags and swap button for currency converter; digital countdown and start/pause buttons for timer).
   - Instant reactive feedback on user interaction (updates live without requiring manual page reload).
   - Clean telemetry or status pill with refined styling (`bg-zinc-100 dark:bg-white/[0.04] border border-zinc-200 dark:border-white/[0.08] text-zinc-600 dark:text-zinc-400 text-xs py-1.5 px-3 rounded-full`).
3. [RECENT ACTIVITY & COPY UTILITY]:
   - Compact history list (recent 3-5 actions) stored in `localStorage`.
   - One-click copy result button with toast feedback ("Copied to clipboard").
4. [STRICT PONYTAIL YAGNI RULES — ABSOLUTE PROHIBITION OF BLOAT]:
   - ABSOLUTELY NO shopping carts, NO order drawers, NO checkout modals.
   - ABSOLUTELY NO product catalogs, NO backpacks, drones, clothes, or fake accessories.
   - ABSOLUTELY NO fake 4.9-star ratings or fake testimonials.
   - ABSOLUTELY NO newsletter subscription forms or marketing promotions.
   - Keep the tool laser-focused on its single job in ~100–180 clean lines. Never write unrequested code.
"""

# Archetype B: E-Commerce & Gastronomy Narrative (Stitch-UX 6-Section Deep Narrative)
COMMERCE_STORE_BLUEPRINT = """
STITCH-UX COMMERCE BLUEPRINT (Mandatory 6-Section UX Narrative for Stores/Restaurants):
1. [NAVIGATION BAR]:
   - Fixed blur-backdrop header (`sticky top-0 z-50 backdrop-blur-xl bg-zinc-950/70 border-b border-zinc-800/80`).
   - Brand logo, nav links with hover indicators, search trigger, and interactive Cart button with live item counter badge.
2. [HERO SHOWCASE SECTION]:
   - Kinetic typography headline, value proposition pill badge, dual CTA action buttons, floating stats/trust indicators.
3. [BENTO GRID FEATURE MATRIX]:
   - Modern asymmetrical grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) with glassmorphic cards and Lucide icons.
4. [DYNAMIC INTERACTIVE CATALOG]:
   - Live search input + multi-category filter pills.
   - Products loaded via JavaScript array `const items = [...]` with real Unsplash images, prices, and 'Add to Cart' actions.
5. [SLIDE-OVER CART DRAWER & CHECKOUT MODAL]:
   - Slide-over drawer with item quantity incrementers (+/-), live subtotal/tax calculation, and animated checkout modal.
6. [FOOTER & SYSTEM STATUS]:
   - Multi-column footer: brand links, newsletter input, and operational status pill (`🟢 All Systems Operational`).
"""

# Archetype C: Data Dashboard & Analytics
DATA_DASHBOARD_BLUEPRINT = """
DATA DASHBOARD BLUEPRINT:
1. [HEADER & TELEMETRY NAV]: Top bar with time range selector, live connection status, and quick export.
2. [KPI METRIC CARDS]: Bento grid of 4 key metric cards with percentage change badges and trend indicators.
3. [PRIMARY VISUALIZATION / CHART AREA]: Clean SVG or Canvas-based interactive telemetry graphs.
4. [LIVE DATA TABLE]: Sortable, filterable table with status badges and pagination controls.
5. [STRICT YAGNI]: Zero unrequested shopping carts or fake commerce items.
"""

# =====================================================================
# 3. DOMAIN-SPECIFIC DESIGN THEMES
# =====================================================================
DOMAIN_PRESETS: Dict[str, Dict[str, Any]] = {
    "food": {
        "theme": "Artisanal Gastronomy & Culinary Elegance",
        "palette": "Warm Saffron Gold (hsl(38, 95%, 52%)), Spicy Terracotta (hsl(14, 88%, 52%)), Deep Charcoal Truffle (hsl(24, 18%, 10%)), Velvet Card Surface (hsl(24, 15%, 15%)), Warm Cream Text (#fff8ee)",
        "typography": "Heading: 'Playfair Display' / 'Cinzel', Body: 'Plus Jakarta Sans'",
        "components": "Interactive Menu Filter, Spice badges, Add to Order drawer, Table Reservation Modal."
    },
    "shop": {
        "theme": "High-Fashion Luxury Boutique & Modern E-Commerce",
        "palette": "Pure Editorial White (#ffffff) / Deep Onyx (#0f1115), Rose Champagne (hsl(35, 75%, 60%)), Cashmere Gray (#f4f4f6), Rich Charcoal Text (#1a1a1a)",
        "typography": "Display: 'Syne' or 'Bodoni Moda', Body: 'Inter' / 'Plus Jakarta Sans'",
        "components": "Product Grid with 3D Spotlight tilt, price discount tags, slide-out Cart Drawer, Free Shipping badges."
    },
    "health": {
        "theme": "Medical Trust, Serene Wellness & Clinical Excellence",
        "palette": "Pure Crisp White (#ffffff), Healing Teal (hsl(172, 80%, 38%)), Oceanic Blue (hsl(210, 85%, 45%)), Soft Slate Surface (#f8fafc), Midnight Navy Text (#0f172a)",
        "typography": "Heading: 'Plus Jakarta Sans', Body: 'Inter'",
        "components": "Instant Appointment Booking Widget, Specialist Doctor Profiles, Service Cards."
    },
    "crypto": {
        "theme": "Next-Gen FinTech & Secure Institutional Finance",
        "palette": "Obsidian Black (#080b11), Emerald Prosperity Glow (hsl(152, 90%, 48%)), Electric Sapphire (hsl(220, 95%, 62%)), Translucent Slate Cards (rgba(255,255,255,0.04)), Crisp Silver Text (#f1f5f9)",
        "typography": "Display: 'Space Grotesk' / 'Outfit', Data/Numbers: 'JetBrains Mono'",
        "components": "Real-Time Conversion Calculator, Currency Ticker, Secure Encryption badges."
    },
    "saas": {
        "theme": "Next-Gen SaaS & Developer Platform",
        "palette": "Obsidian Slate (#0b0f19), Electric Indigo (#6366f1), Cyber Neon Cyan (#38bdf8), Surface Bento (#131b2e), Silver Text (#e2e8f0)",
        "typography": "Display: 'Outfit', Body: 'Plus Jakarta Sans', Code: 'JetBrains Mono'",
        "components": "Hero with live demo, Bento Feature Grid, Pricing Toggle, Interactive FAQ."
    },
    "general": {
        "theme": "Bespoke Modern F-Aura UI/UX Experience",
        "palette": "Deep Charcoal (#0c1017), Vibrant Indigo (#6366f1), Soft Violet (#8b5cf6), Surface Cards: rgba(255,255,255,0.04)",
        "typography": "Primary: 'Plus Jakarta Sans' / 'Outfit' with fluid clamp() scale",
        "components": "Focused responsive card/layout, micro-animations, glassmorphic elevation, zero generic placeholder text."
    }
}


class DesignBlueprintEngine:
    """
    Unified Design Intelligence & Intent-Adaptive Blueprint Compiler for F.R.I.D.A.Y.
    Enforces autonomous language selection and strict Ponytail YAGNI principles.
    """

    def __init__(self):
        self.tokens = UI_UX_PRO_DESIGN_TOKENS
        self.presets = DOMAIN_PRESETS

    def detect_archetype(self, instruction: str) -> str:
        """
        Detects application archetype to separate utilities from e-commerce stores.
        Returns: 'utility_tool', 'commerce_store', 'data_dashboard', 'portfolio_showcase', or 'fullstack_app'.
        """
        q = instruction.lower()

        # 1. Utility Tool indicators (Single-purpose focused tools)
        utility_keywords = [
            "converter", "calculator", "timer", "stopwatch", "counter", "todo", "to-do",
            "task list", "color picker", "picker", "generator", "formatter", "diff",
            "widget", "clock", "regex", "qr", "notes", "notes app", "unit converter",
            "currency converter", "password generator", "json formatter", "speed test"
        ]
        # Only treat as utility if not explicitly combined with store/ecommerce
        is_utility = any(w in q for w in utility_keywords)
        is_commerce = any(w in q for w in [
            "shop", "store", "ecommerce", "e-commerce", "bakery", "restaurant", "cafe",
            "boutique", "menu", "dishes", "pizza", "shoes", "clothing", "apparel",
            "order food", "coffee shop", "catalog", "cart"
        ])

        if is_utility and not is_commerce:
            return "utility_tool"
        elif is_commerce:
            return "commerce_store"
        elif any(w in q for w in ["dashboard", "analytics", "metrics", "monitor", "crypto tracker", "crypto monitor", "kpi", "telemetry"]):
            return "data_dashboard"
        elif any(w in q for w in ["portfolio", "resume", "cv", "personal site", "showcase"]):
            return "portfolio_showcase"
        elif any(w in q for w in ["fullstack", "full stack", "backend and frontend", "with database"]):
            return "fullstack_app"

        # Default fallback
        return "utility_tool" if any(w in q for w in ["simple", "tool", "widget", "convert"]) else "general"

    def detect_autonomous_tech_stack(self, instruction: str) -> Dict[str, Any]:
        """
        F.R.I.D.A.Y. autonomously evaluates requirements and chooses the technology stack.
        Rule: If Boss specifies React/Next.js/etc., she honors it.
        Otherwise, she ALWAYS chooses the simplest, latest modern stack (the easy way, not hardcoded/over-engineered).
        """
        q = instruction.lower()

        # Check explicit user specifications
        if "nextjs" in q or "next.js" in q:
            return {
                "framework": "Next.js 15",
                "stack": "Next.js 15 (App Router) + Tailwind CSS + Lucide Icons",
                "is_user_specified": True,
                "easy_way": False,
                "rationale": "Explicitly requested by Boss."
            }
        elif "react" in q:
            return {
                "framework": "React 19",
                "stack": "React 19 + Tailwind CSS + Lucide Icons (Modern ESM standalone / Vite)",
                "is_user_specified": True,
                "easy_way": False,
                "rationale": "Explicitly requested by Boss."
            }
        elif "vue" in q:
            return {
                "framework": "Vue 3",
                "stack": "Vue 3 + Tailwind CSS + Lucide Icons",
                "is_user_specified": True,
                "easy_way": False,
                "rationale": "Explicitly requested by Boss."
            }
        elif "python" in q or "fastapi" in q or "flask" in q:
            return {
                "framework": "Python 3.12",
                "stack": "Python 3.12 Standard Library (or FastAPI if API requested)",
                "is_user_specified": True,
                "easy_way": True,
                "rationale": "Explicitly requested by Boss."
            }

        # Autonomous Selection: Simplest, latest modern stack (The Easy Way)
        archetype = self.detect_archetype(instruction)
        if archetype == "fullstack_app":
            return {
                "framework": "Python FastAPI + Modern ESM HTML5/Tailwind",
                "stack": "FastAPI + SQLite3 + HTML5/Tailwind CDN/ESM JS",
                "is_user_specified": False,
                "easy_way": True,
                "rationale": "Autonomous selection by F.R.I.D.A.Y.: Built with Python FastAPI backend + modern Tailwind/ESM frontend. The simplest, robust fullstack architecture without bulky node_modules."
            }
        else:
            return {
                "framework": "Modern HTML5 + Tailwind CSS CDN + ES Modules (ESM) + Lucide Icons CDN",
                "stack": "HTML5 / Tailwind CDN / Modern Vanilla ESM JS",
                "is_user_specified": False,
                "easy_way": True,
                "rationale": "Autonomous selection by F.R.I.D.A.Y.: Selected the simplest, latest modern stack with zero build-step latency, zero bulky node_modules, and instant browser execution (the easy way, not over-engineered)."
            }

    def detect_domain(self, instruction: str) -> Dict[str, Any]:
        """Detects domain preset from user instruction."""
        q = instruction.lower()
        if any(w in q for w in ["food", "restaurant", "biryani", "cafe", "coffee", "bakery", "dish", "menu", "pizza", "burger", "bar", "dining"]):
            return self.presets["food"]
        elif any(w in q for w in ["shop", "store", "ecommerce", "cart", "clothing", "fashion", "shoes", "product", "buy"]):
            return self.presets["shop"]
        elif any(w in q for w in ["health", "medical", "doctor", "clinic", "hospital", "fitness", "wellness", "dentist"]):
            return self.presets["health"]
        elif any(w in q for w in ["crypto", "fintech", "finance", "bank", "invest", "trading", "wallet", "currency", "converter"]):
            return self.presets["crypto"]
        elif any(w in q for w in ["saas", "dashboard", "developer", "software", "api", "cloud", "ai", "platform"]):
            return self.presets["saas"]
        return self.presets["general"]

    def synthesize_frontend_master_prompt(self, user_prompt: str, user_preferences: Optional[str] = None) -> str:
        """
        Synthesizes an archetype-aware master prompt.
        Enforces focused minimalist tool cards for utilities and rich catalogs only for actual stores.
        """
        domain = self.detect_domain(user_prompt)
        archetype = self.detect_archetype(user_prompt)
        tech_choice = self.detect_autonomous_tech_stack(user_prompt)
        pref_clause = f"\nBOSS ADAPTIVE PREFERENCES (From Neural Memory):\n{user_preferences}\n" if user_preferences else ""
        stitch_design_clause = mcp_design_bridge.generate_human_design_prompt_clause(user_prompt, archetype)

        if archetype == "utility_tool":
            q = user_prompt.lower()
            is_pw = any(w in q for w in ["password", "secret", "generator"]) and not any(w in q for w in ["currency", "money"])
            is_curr = any(w in q for w in ["currency", "exchange", "forex", "money", "convert"])
            is_timer = any(w in q for w in ["timer", "pomodoro", "stopwatch", "clock"])

            if is_pw:
                tool_constraints = """4. High-Contrast Monospace Password Display:
   - Generated Password Box: Crisp pure white characters in JetBrains Mono (`font-mono text-2xl sm:text-3xl font-semibold text-white tracking-wider selection:bg-white/20 select-all break-all`).
   - Integrated action controls: Subtle refresh icon button (regenerates on click with 180° rotation) and copy button with toast alert feedback.
5. Human-Grade Security Controls:
   - Password Length Slider: Smooth slider (range 8 to 48, default 16) with live numeric value badge.
   - Character Set Toggles: Tactile pill switches or checkboxes for:
     - [x] Uppercase (A-Z)
     - [x] Lowercase (a-z)
     - [x] Numbers (0-9)
     - [x] Symbols (!@#$%^&*)
   - Entropy Strength Bar: Minimalist 4-segment meter (Weak, Fair, Good, Strong) showing real-time password security.
   - LocalStorage History: Recent 3-5 generated passwords in compact history list.
   - Call `lucide.createIcons()` in JavaScript after DOM initialization."""
            elif is_curr:
                tool_constraints = """4. Monochrome FinTech Typography (NO NEON GLOWING NUMBERS):
   - Input Amount: Large, crisp pure white numbers (`font-mono text-3xl font-semibold text-white tracking-tight`).
   - Converted Result: Pure crisp white / silver (`font-mono text-3xl font-semibold text-zinc-50 tracking-tight`).
   - NEVER make the numbers radioactive neon green or neon cyan.
5. Human-Grade Form Controls & Row Ergonomics:
   - Currency select options MUST include country flags (🇺🇸 USD, 🇪🇺 EUR, 🇬🇧 GBP, 🇯🇵 JPY, 🇮🇳 INR, 🇨🇦 CAD, 🇦🇺 AUD, 🇨🇭 CHF, 🇸🇬 SGD, 🇦🇪 AED).
   - In each conversion row, use a structured grid or constrained flex (`grid grid-cols-12 gap-3 items-center` with selector `col-span-5` and amount input/result `col-span-7 text-right min-w-0`). The `<input>` must have `w-full text-right outline-none` so it stays strictly within the card boundaries without overflow.
   - Smooth swap button (circular, border border-white/10, rotates 180° on click).
   - Rate pill: `bg-white/[0.04] border border-white/[0.08] text-zinc-400 text-xs py-1.5 px-3 rounded-full`.
   - Copy button with toast alert.
   - LocalStorage recent conversions (clean compact list of 3-4 items).
   - Call `lucide.createIcons()` in JavaScript after DOM initialization."""
            elif is_timer:
                tool_constraints = """4. Digital Time Readout:
   - Large digital countdown (`font-mono text-5xl sm:text-6xl font-bold text-white tracking-tight text-center my-6`).
5. Human-Grade Timer Controls:
   - Mode selector pills (Pomodoro 25m, Short Break 5m, Long Break 15m).
   - Tactile Start/Pause and Reset spring action buttons.
   - Circular SVG countdown ring or clean linear progress bar.
   - Call `lucide.createIcons()` in JavaScript after DOM initialization."""
            else:
                tool_constraints = """4. High-Contrast Typography:
   - Primary values in crisp pure white JetBrains Mono (`text-white font-mono font-semibold`).
5. Ergonomic Controls:
   - Clean inputs and tactile spring action buttons tailored strictly to the requested utility.
   - One-click copy with toast alert feedback.
   - Call `lucide.createIcons()` in JavaScript after DOM initialization."""

            return f"""YOU ARE THE PRINCIPAL FRONTEND ARCHITECT & UI/UX PRO LEAD.
Your mission is to generate a world-class, focused, single-file, production-ready web application for the following directive:

USER DIRECTIVE: {user_prompt}
APPLICATION ARCHETYPE: Focused Ergonomic Utility Tool
AUTONOMOUS TECH STACK: {tech_choice['stack']} (Chosen by F.R.I.D.A.Y. — {tech_choice['rationale']})
{pref_clause}

DOMAIN THEME: {domain['theme']}
COLOR PALETTE: {domain['palette']}
TYPOGRAPHY: {domain['typography']}

{stitch_design_clause}

{UTILITY_TOOL_BLUEPRINT}

MANDATORY TECHNICAL & AESTHETIC CONSTRAINTS:
1. Single Complete File: Output the entire application inside a single ```html code block.
2. Framework & Libraries (The Easy Way):
   - Use `<script src="{self.tokens['tailwind_cdn']}"></script>`
   - Configure Tailwind for Class-Based Dark Mode:
     `<script>tailwind.config = {{ darkMode: 'class' }};</script>`
   - Use `<link href="{self.tokens['fonts']}" rel="stylesheet">`
   - Use `<script src="{self.tokens['lucide_cdn']}"></script>`
3. Human-Crafted Ergonomic Layout (Apple × Stripe × Notion Hybrid + Dual Theme):
   - Clean Dual-Theme Architecture (Default: Clean Light Mode):
     - Canvas: Warm linen / porcelain (`bg-[#fbfbfa] dark:bg-[#09090b] text-zinc-900 dark:text-zinc-100 min-h-screen flex items-center justify-center p-4 antialiased transition-colors duration-200`).
     - Card: Elevated pure white (`max-w-md w-full bg-white dark:bg-[#121216]/90 border border-zinc-200/80 dark:border-white/[0.08] rounded-2xl p-6 sm:p-7 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)] dark:shadow-2xl backdrop-blur-xl transition-all duration-200`).
     - Subtle hairline border: `border-zinc-200/80 dark:border-white/[0.08]`.
   - Tactile ☀️/🌙 Theme Switcher:
     - Header MUST contain an ergonomic theme toggle button:
       `<button onclick="toggleTheme()" class="p-2 rounded-xl bg-zinc-100 hover:bg-zinc-200 dark:bg-white/[0.05] dark:hover:bg-white/[0.10] text-zinc-600 dark:text-zinc-300 border border-zinc-200/80 dark:border-white/[0.08] transition-all active:scale-95" title="Toggle Light/Dark Theme"><i data-lucide="sun" class="w-4 h-4 hidden dark:block text-amber-400"></i><i data-lucide="moon" class="w-4 h-4 block dark:hidden text-zinc-600"></i></button>`
     - Script MUST implement theme management:
       `function initTheme() {{ const saved = localStorage.getItem('theme'); const isDark = saved === 'dark'; document.documentElement.classList.toggle('dark', isDark); }}`
       `function toggleTheme() {{ const isDark = document.documentElement.classList.toggle('dark'); localStorage.setItem('theme', isDark ? 'dark' : 'light'); }}`
       Call `initTheme()` immediately in script!
   - ABSOLUTELY NO background matrix grid lines (.bg-grid).
   - ABSOLUTELY NO floating neon blur spheres (.glow-a, .glow-b). Keep the background serene and clean.
{tool_constraints}
6. STRICT PONYTAIL YAGNI RULE:
   - ZERO shopping carts, ZERO order drawers, ZERO checkout modals.
   - ZERO backpacks, drones, or fake accessories.
   - ZERO newsletter signups or fake 4.9-star ratings.
   - Total code ~130–200 lines of pristine, human-crafted code.
7. Zero Code Omission: Write the COMPLETE code from `<!DOCTYPE html>` to `</html>`.
"""

        elif archetype == "commerce_store":
            return f"""YOU ARE THE PRINCIPAL FRONTEND ARCHITECT & UI/UX PRO LEAD.
Your mission is to generate a world-class, single-file, production-ready e-commerce store for the following directive:

USER DIRECTIVE: {user_prompt}
APPLICATION ARCHETYPE: Full E-Commerce Store & Interactive Catalog
AUTONOMOUS TECH STACK: {tech_choice['stack']}
{pref_clause}

DOMAIN THEME: {domain['theme']}
COLOR PALETTE: {domain['palette']}
TYPOGRAPHY: {domain['typography']}
REQUIRED COMPONENTS: {domain['components']}

{COMMERCE_STORE_BLUEPRINT}

MANDATORY TECHNICAL CONSTRAINTS:
1. Single Complete File: Output the entire application inside a single ```html code block.
2. Styling: Use `<script src="{self.tokens['tailwind_cdn']}"></script>` (configured with `tailwind.config = {{ darkMode: 'class' }};`) and `<link href="{self.tokens['fonts']}" rel="stylesheet">`.
3. Icons: Use `<script src="{self.tokens['lucide_cdn']}"></script>`. Call `lucide.createIcons()` in JavaScript after DOM rendering.
4. Color Palette: Apple × Stripe dual-theme architecture (Default clean light canvas `bg-[#fbfbfa]`, card `bg-white dark:bg-zinc-900/80`, borders `border-zinc-200 dark:border-zinc-800/80`, dark canvas `dark:bg-[#09090b]`, with built-in ☀️/🌙 toggle).
5. JavaScript Dynamic Engine:
   - Store products in `const items = [...]` with id, title, category, price, rating, desc, image (working Unsplash URLs).
   - Implement functions: `renderItems()`, `filterCategory()`, `searchItems()`, `addToCart()`, `toggleCart()`, `updateCartUI()`, `checkout()`, `showToast()`.
6. Zero Code Omission: Write the COMPLETE code from `<!DOCTYPE html>` to `</html>`.
"""

        elif archetype == "data_dashboard":
            return f"""YOU ARE THE PRINCIPAL FRONTEND ARCHITECT & UI/UX PRO LEAD.
Your mission is to generate a world-class, single-file, production-ready data dashboard for the following directive:

USER DIRECTIVE: {user_prompt}
APPLICATION ARCHETYPE: Telemetry & Data Dashboard
AUTONOMOUS TECH STACK: {tech_choice['stack']}
{pref_clause}

DOMAIN THEME: {domain['theme']}
COLOR PALETTE: {domain['palette']}
TYPOGRAPHY: {domain['typography']}

{DATA_DASHBOARD_BLUEPRINT}

MANDATORY TECHNICAL CONSTRAINTS:
1. Single Complete File inside a single ```html code block.
2. Use Tailwind CDN, Lucide CDN, and modern Google Fonts.
3. KPI Bento Grid + Sortable Data Table + Live Status Indicators.
4. STRICT YAGNI: No shopping carts or fake e-commerce items.
5. Zero Code Omission: Write the COMPLETE code from `<!DOCTYPE html>` to `</html>`.
"""

        else:
            return f"""YOU ARE THE PRINCIPAL FRONTEND ARCHITECT & UI/UX PRO LEAD.
Your mission is to generate a world-class, single-file, production-ready web application for:

USER DIRECTIVE: {user_prompt}
AUTONOMOUS TECH STACK: {tech_choice['stack']}
{pref_clause}

DOMAIN THEME: {domain['theme']}
COLOR PALETTE: {domain['palette']}
TYPOGRAPHY: {domain['typography']}

MANDATORY TECHNICAL CONSTRAINTS:
1. Single Complete File: Output the entire application inside a single ```html code block.
2. Use `<script src="{self.tokens['tailwind_cdn']}"></script>` (with `tailwind.config = {{ darkMode: 'class' }};`) and `<script src="{self.tokens['lucide_cdn']}"></script>`.
3. Apple × Stripe × Notion Dual-Theme Architecture (Default clean light mode with ☀️/🌙 toggle, `bg-[#fbfbfa] dark:bg-[#09090b]`, card `bg-white dark:bg-[#121216]/90`, borders `border-zinc-200/80 dark:border-white/[0.08]`).
4. STRICT PONYTAIL YAGNI RULE: Do NOT add unrequested features or bloat. Build exactly what the user commanded with high polish.
5. Zero Code Omission: Write complete, runnable code from `<!DOCTYPE html>` to `</html>`.
"""

    def synthesize_backend_master_prompt(self, project_name: str, user_prompt: str) -> str:
        """Synthesizes backend Python SQLite / FastAPI architecture prompt."""
        return f"""YOU ARE THE SENIOR BACKEND & DATABASE SYSTEMS SPECIALIST.
Your mission is to write a clean, self-contained Python backend server (`main.py`) for:

PROJECT: {project_name}
REQUIREMENTS: {user_prompt}

MANDATORY TECHNICAL CONSTRAINTS:
1. Use Python standard library `sqlite3` for local database storage (zero extra DB servers needed).
2. Automatically create necessary tables and seed sample data on startup.
3. Serve lightweight REST API endpoints matching the project requirements.
4. Include simple static file serving so `index.html` is served at `http://localhost:8000/`.
5. STRICT YAGNI: Only write endpoints and tables that are required for the project. No unnecessary bloat.
6. Output complete runnable code in a single ```python code block.
"""

    def audit_and_repair_markup(self, html_content: str, project_title: str) -> str:
        """Reality-Check Auditor: Checks DOM completeness and self-heals missing tags or broken closures."""
        if not html_content or len(html_content.strip()) < 50:
            return ""

        content = html_content.strip()

        # Ensure proper HTML5 DOCTYPE
        if not content.lower().startswith("<!doctype html"):
            if "<html" in content.lower():
                idx = content.lower().find("<html")
                content = "<!DOCTYPE html>\n" + content[idx:]
            else:
                content = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n<title>" + project_title + "</title>\n</head>\n<body>\n" + content

        # Self-heal missing opening quote on object properties (e.g., desc: RFID-blocking...",)
        content = re.sub(r'(\b[a-zA-Z0-9_]+\s*:\s*)([^\s"\'{}[\]][^"\n\r]*?)",', r'\1"\2",', content)

        # Self-heal inputs and selects in flex/grid to prevent container overflow
        content = re.sub(r'class="([^"]*\bnum-input\b[^"]*)"', lambda m: f'class="{m.group(1)} min-w-0"' if "min-w-0" not in m.group(1) else m.group(0), content)
        content = re.sub(r'class="([^"]*\bcurrency-select\b[^"]*)"', lambda m: f'class="{m.group(1)} w-full"' if "w-full" not in m.group(1) else m.group(0), content)

        # Self-heal AI tropes: radioactive green numbers -> high-contrast pure white
        content = re.sub(r'\b(text-emerald-[0-9]{3}|text-green-[0-9]{3}|text-emerald-glow)\b(?=[^>]*\bfont-mono\b)', 'text-zinc-50', content)
        content = re.sub(r'(?<=\bfont-mono\b[^>]{0,50})\b(text-emerald-[0-9]{3}|text-green-[0-9]{3}|text-emerald-glow)\b', 'text-zinc-50', content)

        # Ensure closing tags
        if "</body>" not in content.lower():
            content += "\n</body>"
        if "</html>" not in content.lower():
            content += "\n</html>"

        return content

    def generate_lazy_coding_contracts(
        self,
        project_name: str,
        domain_theme: str,
        tech_stack: str = "HTML5 + Tailwind CDN + ESM Vanilla JS",
        archetype: str = "utility_tool",
        user_instruction: str = ""
    ) -> Dict[str, str]:
        """
        Generates root-level CLAUDE.md and OPENCODE.md shared contracts ('lazy coding' repo synchronization).
        Directly wires Claude Code and OpenCode to Google Stitch Design Systems & UI/UX Pro Max MCP.
        Ensures all coding agents strictly adhere to the Ponytail Senior Dev Rule (YAGNI, zero bloat, easy way).
        """
        stitch_system = mcp_design_bridge.get_system_for_query(user_instruction, archetype)

        if archetype == "utility_tool":
            scope_rules = f"""## 2. Mandatory Ergonomic Utility Blueprint (Stitch & UI/UX Pro Max)
- **Layout**: Centered ergonomic tool card (Wise / Raycast / Linear design standard).
- **Design System**: {stitch_system['name']}
  - Canvas: `{stitch_system.get('canvas_bg', '#09090b')}` | Surface: `{stitch_system.get('surface', '#121216')}`
  - Typography: {stitch_system.get('font_display', 'Plus Jakarta Sans')} / {stitch_system.get('font_mono', 'JetBrains Mono')}
  - Specular Highlight: `inset 0 1px 0 rgba(255,255,255,0.08)`
- **Core Engine**: Real-time reactive calculation on user input, smooth swap action, copy result toast, localStorage history.
- **ZERO-AI-TROPES MANDATE**:
  - ABSOLUTELY NO matrix grids (`.bg-grid`) or cybernetic line work.
  - ABSOLUTELY NO floating neon blur balls (`.glow-a`, `.glow-b`). Keep canvas serene and solid dark.
  - ABSOLUTELY NO radioactive neon green (`#00ff66` / glowing emerald) for numbers. All amounts must be crisp, high-contrast pure white (`#ffffff`).
  - Style dropdowns with country flags (🇺🇸 USD, 🇪🇺 EUR, 🇬🇧 GBP, 🇯🇵 JPY, 🇮🇳 INR, etc.).
- **STRICT PONYTAIL YAGNI RULE (ZERO BLOAT)**:
  - DO NOT write shopping carts, order drawers, checkout modals, or product catalogs.
  - DO NOT invent backpacks, drones, or fake store merchandise.
  - DO NOT add newsletter subscription inputs or fake 4.9-star ratings.
  - Never write a single extra line of unrequested code without informing the Boss.
  - Keep the tool clean, elegant, and compact (~100–180 lines)."""
        elif archetype == "commerce_store":
            scope_rules = f"""## 2. Mandatory Stitch-UX 6-Section Commerce Blueprint
- **Design System**: {stitch_system['name']}
- **Sticky Navigation**: Fixed blur-backdrop, logo, cart trigger button with live badge counter.
- **Hero Showcase**: Headline gradient, value pill, dual action buttons.
- **Bento Grid**: 3-column card matrix with hover spotlight.
- **Dynamic Catalog**: Live search + category filter pills + JS dataset array.
- **Cart Drawer & Checkout**: Quantity adjustments (+/-), live subtotal/tax calculation, checkout modal.
- **Footer**: Brand links, operational status pill."""
        elif archetype == "data_dashboard":
            scope_rules = f"""## 2. Mandatory Data Dashboard Blueprint
- **Design System**: {stitch_system['name']}
- **Telemetry Header**: Status indicator, range selectors.
- **KPI Bento Grid**: 4 key metric cards with delta percentages.
- **Data Table / Feeds**: Filterable, sortable telemetry table.
- **STRICT YAGNI**: No shopping carts or fake e-commerce items."""
        else:
            scope_rules = f"""## 2. Adaptive Engineering Blueprint
- **Design System**: {stitch_system['name']}
- Build strictly according to user requirements with zero unrequested scope bloat."""

        contract_body = f"""# Project Architecture Contract: {project_name}

## 1. Executive Mission
Build a production-grade, human-like modern application for **{project_name}**.
- **User Directive**: "{user_instruction}"
- **Application Archetype**: {archetype.upper()}
- **Design Framework**: {stitch_system['name']} (Wired to Google Stitch & UI/UX Pro Max MCP)
- **Primary Tech Stack**: {tech_stack}
- **Framework Choice**: The easy, modern way — zero unnecessary build steps or heavy node_modules.
- **Design Standard**: Apple × Stripe × Notion Dual-Theme Architecture (Default clean light mode `#fbfbfa`, ☀️/🌙 theme toggle, dark obsidian support `#09090b`).

{scope_rules}

## 3. MCP Tooling Integration
This repository is wired to:
- **ui-ux-pro-mcp**: For real design tokens, component architecture, and spring physics.
- **StitchMCP**: For Google Stitch design systems, color tokens, and layout guidelines.
Configured in `.mcp.json` (Claude Code) and `opencode.json` (OpenCode).

## 4. Engineering Discipline & The Ponytail Senior Dev Rule
1. **Does this need to exist?** -> If not asked by the user, skip it (YAGNI).
2. **Never write a line extra without informing the Boss.**
3. **Always use the easy way, not the hardcoded way.**
4. **NO PLACEHOLDERS**: Never write `// TODO`, `/* rest of code */`, or incomplete fragments.
5. **LUCIDE HYDRATION**: Always call `lucide.createIcons()` after DOM rendering.
"""
        # 5. Inject Active Developer Instincts (ECC Continuous Learning)
        try:
            from core.headroom_memory import memory_engine
            instincts_md = memory_engine.export_instincts_markdown()
        except Exception:
            instincts_md = ""

        if instincts_md:
            contract_body += f"\n## 5. Active Developer Instincts (ECC Continuous Learning)\n{instincts_md}\n"

        return {
            "CLAUDE.md": contract_body,
            "OPENCODE.md": contract_body,
            os.path.join(".claude", "rules", "instincts.md"): instincts_md
        }


# Global singleton instance
design_blueprint = DesignBlueprintEngine()
