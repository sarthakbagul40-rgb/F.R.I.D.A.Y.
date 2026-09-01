"""
F.R.I.D.A.Y. OS 8.0: Agency-Agents Swarm & Stitch-UX Neural Blueprint Engine
Encapsulates curated engineering personas, deep sectional UX narratives (Google Stitch),
and elite glassmorphic design token systems (UI/UX Pro).
"""

from typing import Dict, Any, List, Optional

# =====================================================================
# 1. UI/UX PRO DESIGN TOKEN SYSTEM
# =====================================================================
UI_UX_PRO_DESIGN_TOKENS = {
    "fonts": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap",
    "tailwind_cdn": "https://cdn.tailwindcss.com",
    "lucide_cdn": "https://unpkg.com/lucide@latest",
    "theme": {
        "bg_primary": "bg-[#09090b]",
        "bg_surface": "bg-zinc-900/60",
        "bg_surface_elevated": "bg-zinc-800/80",
        "border_subtle": "border-zinc-800/80",
        "border_highlight": "border-zinc-700/50",
        "text_primary": "text-zinc-100",
        "text_secondary": "text-zinc-400",
        "text_muted": "text-zinc-500",
        "accent_glow": "shadow-[0_0_50px_-12px_rgba(99,102,241,0.25)]",
        "glass_blur": "backdrop-blur-xl",
    }
}

# =====================================================================
# 2. STITCH-UX DEEP SECTIONAL ARCHITECTURAL BLUEPRINT
# =====================================================================
STITCH_UX_NARRATIVE_BLUEPRINT = """
STITCH-UX DEEP SECTIONAL BLUEPRINT (Mandatory 6-Section UX Narrative):
Every generated web application MUST include the following 6 rich, interactive sections:

1. [NAVIGATION BAR]:
   - Fixed blur-backdrop header (`sticky top-0 z-50 backdrop-blur-xl bg-zinc-950/70 border-b border-zinc-800/80`).
   - Brand logo with glowing icon badge, desktop nav links with hover indicator lines, global search button, and interactive Shopping Cart trigger with a dynamic item counter badge.

2. [HERO SHOWCASE SECTION]:
   - Kinetic typography header with subtle gradient clip text.
   - Value proposition pill badge (`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs bg-indigo-500/10 text-indigo-400 border border-indigo-500/20`).
   - Dual action CTAs: Primary Glowing Action Button + Secondary Glass Outline Button.
   - Floating stats counters / trust badges (e.g. 4.9★ Rating, 100% Free, Global Shipping).

3. [BENTO GRID FEATURE MATRIX]:
   - Modern asymmetrical grid (`grid grid-cols-1 md:grid-cols-3 gap-6`).
   - Glassmorphic card surfaces with subtle hover elevation and glowing border highlight.
   - Custom Lucide icon indicators for each capability.

4. [DYNAMIC INTERACTIVE DATA CATALOG]:
   - Live Search Input bar + Multi-Category Filter Pills with instant client-side filtering.
   - Product / Item Cards dynamically populated via clean JavaScript Data Arrays (`const items = [...]`).
   - Each card features: high-res Unsplash image, category pill, title, description, price badge, 'Quick View' modal trigger, and 'Add to Cart' button with immediate toast feedback.

5. [INTERACTIVE SLIDE-OVER CART & MODALS]:
   - Slide-Over Cart Drawer (`fixed inset-y-0 right-0 z-50`) with backdrop blur overlay.
   - Live item quantity incrementers (+/-), remove action, real-time Subtotal, Tax, and Grand Total calculation.
   - 'Proceed to Checkout' action triggering an animated confirmation modal with confetti/success state.

6. [FOOTER & SYSTEM STATUS]:
   - Multi-column footer: Brand story, Quick Links, Newsletter subscription input, Live System Status pill (`🟢 All Systems Operational`), and Copyright.
"""

# =====================================================================
# 3. AGENCY-AGENTS ROLE BLUEPRINTS & CONTRACTS
# =====================================================================
AGENCY_ROLE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "frontend_cto": {
        "title": "Principal UI/UX & Frontend Architect",
        "description": "Designs world-class, responsive, glassmorphic interfaces with Tailwind CDN and Lucide Icons.",
        "system_rules": [
            "STRICT ZERO-BLOAT RULE: Never write monolithic, repetitive HTML or massive raw CSS blocks.",
            "DYNAMIC JS ENGINE: Define items as clean JavaScript data arrays (`const catalogItems = [...]`) and render them dynamically in a JS loop.",
            "INTERACTIVE COMPLETENESS: Always include a working slide-over Cart Drawer, Quick-View Modal, Search Filter, and Toast Notification Dispatcher.",
            "TYPOGRAPHY: Import Plus Jakarta Sans and configure Lucide icons (`lucide.createIcons()`) at the end of the script.",
            "NO PLACEHOLDERS: Generate 100% complete, fully implemented DOM trees. Never leave `<!-- TODO -->` or incomplete code."
        ],
        "tech_stack": "HTML5 + Tailwind CSS CDN + Lucide Icons CDN + Vanilla JS"
    },
    "backend_architect": {
        "title": "Senior Backend Systems & Database Specialist",
        "description": "Architects robust, self-contained Python SQLite and FastAPI REST architectures.",
        "system_rules": [
            "ZERO-DEPENDENCY RELIABILITY: Use Python standard library (`sqlite3`, `http.server` or `fastapi` with uvicorn) with automatic self-healing fallback.",
            "AUTO-SEEDING: Ensure the database automatically creates tables and seeds initial mock data on first launch.",
            "SANITIZATION & CORS: Include parameterized SQL queries, CORS headers, and proper error JSON responses.",
            "CLEAN REST API: Provide clean endpoints: GET /api/items, POST /api/cart, POST /api/checkout."
        ],
        "tech_stack": "Python 3.10+ + SQLite3 + FastAPI / Builtin HTTP Server"
    },
    "reality_auditor": {
        "title": "Lead Security & Reality-Check Auditor",
        "description": "Audits synthesized code for tag closures, syntax errors, broken imports, and edge cases.",
        "verification_checklist": [
            "Verify that all `<script>`, `<style>`, `<div>`, and `<body>` tags are properly closed.",
            "Ensure `lucide.createIcons()` is invoked after dynamic DOM elements are rendered.",
            "Verify all event listeners have null-safe checks (e.g. `el && el.addEventListener(...)`).",
            "Ensure zero inline CSS bloat (> 50 lines of raw CSS is strictly forbidden; use Tailwind classes)."
        ]
    }
}

class AgencySwarmOrchestrator:
    """
    Coordinates and synthesizes multi-agent blueprints for F.R.I.D.A.Y.'s autonomous coding engine.
    """

    def __init__(self):
        self.roles = AGENCY_ROLE_REGISTRY
        self.tokens = UI_UX_PRO_DESIGN_TOKENS
        self.blueprint = STITCH_UX_NARRATIVE_BLUEPRINT

    def synthesize_frontend_master_prompt(self, user_prompt: str, user_preferences: Optional[str] = None) -> str:
        """
        Synthesizes a master prompt fusing Stitch-UX architectural structure with UI/UX Pro tokens.
        """
        pref_clause = f"\nBOSS ADAPTIVE PREFERENCES (From Neural Memory):\n{user_preferences}\n" if user_preferences else ""

        return f"""
YOU ARE THE PRINCIPAL FRONTEND ARCHITECT & UI/UX PRO LEAD (AGENCY-AGENTS CORE).
Your mission is to generate a world-class, single-file, production-ready web application for the following directive:

USER DIRECTIVE: {user_prompt}
{pref_clause}
{self.blueprint}

MANDATORY TECHNICAL CONSTRAINTS:
1. Single Complete File: Output the entire application inside a single ```html code block.
2. Styling: Use `<script src="https://cdn.tailwindcss.com"></script>` and `<link href="{self.tokens['fonts']}" rel="stylesheet">`.
3. Icons: Use `<script src="{self.tokens['lucide_cdn']}"></script>`. Call `lucide.createIcons()` in JavaScript after DOM rendering.
4. Color Palette: Dark luxury theme (`bg-[#09090b]`, text `zinc-100`, borders `zinc-800/80`, accents `indigo-500/cyan-400`, glassmorphism `backdrop-blur-xl bg-zinc-900/60`).
5. JavaScript Dynamic Engine:
   - Store products/items in a JavaScript array `const items = [...]` with id, title, category, price, rating, desc, image (use working Unsplash URLs).
   - Implement functions: `renderItems(filteredList)`, `filterCategory(cat)`, `searchItems(query)`, `addToCart(id)`, `toggleCart()`, `updateCartUI()`, `checkout()`, `showToast(msg)`.
6. Zero Code Omission: Write the COMPLETE code from `<!DOCTYPE html>` to `</html>`. Do NOT use `// ... rest of code`.
"""

    def synthesize_backend_master_prompt(self, project_name: str, user_prompt: str) -> str:
        """
        Synthesizes a backend database and API prompt for Python/SQLite architectures.
        """
        return f"""
YOU ARE THE SENIOR BACKEND & DATABASE SYSTEMS SPECIALIST (AGENCY-AGENTS CORE).
Your mission is to write a clean, self-contained Python backend server (`app.py`) for:

PROJECT: {project_name}
REQUIREMENTS: {user_prompt}

MANDATORY TECHNICAL CONSTRAINTS:
1. Use Python standard library `sqlite3` for local database storage.
2. Automatically create tables (`items`, `orders`, `users`) and seed sample data on startup.
3. Serve REST API endpoints:
   - GET /api/items
   - GET /api/item/<id>
   - POST /api/cart/add
   - POST /api/checkout
4. Include simple static file serving so `index.html` is served at `http://localhost:8000/`.
5. Output complete runnable code in a single ```python code block.
"""

    def audit_and_repair_markup(self, html_content: str, project_title: str) -> str:
        """
        Reality-Check Auditor: Checks DOM completeness and self-heals any missing tags or broken closures.
        """
        if not html_content or len(html_content.strip()) < 50:
            return ""

        content = html_content.strip()
        
        # Ensure proper HTML5 DOCTYPE
        if not content.lower().startswith("<!doctype html"):
            if "<html" in content.lower():
                idx = content.lower().find("<html")
                content = "<!DOCTYPE html>\n" + content[idx:]
            else:
                content = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n</head>\n<body>\n" + content

        # Ensure closing tags
        if "</body>" not in content.lower():
            content += "\n</body>"
        if "</html>" not in content.lower():
            content += "\n</html>"

        return content


# Global singleton instance
agency_swarm = AgencySwarmOrchestrator()
