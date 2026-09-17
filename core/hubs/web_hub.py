"""
F.R.I.D.A.Y. Honeycomb Web Hub
External intelligence: live web scraping, DDG/RSS news, Google Maps navigation, browser automation, WhatsApp messaging, and deep research.
"""

import os
import re
import json
import threading
from core.rate_limiter import api_throttler
from core.browser_agent import browser_agent, open_in_brave
from core.maps_service import maps_engine
from core.github_service import github_engine
from core.whatsapp_service import whatsapp_engine
from core.hubs.base import play_sound, speak
from core.hubs.chat_hub import get_ai_response, handleSuggestion

LOCATIONS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'security_protocol', 'locations.json')

def get_person_location(name: str):
    """Checks if target person is registered in security protocol locations.json."""
    if not os.path.exists(LOCATIONS_FILE):
        return None
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for person, info in data.items():
                if name.lower() in person.lower():
                    return info
    except Exception:
        pass
    return None

def web_search_intelligence(query: str, search_type: str = "text") -> str:
    """Fetches real-time data from the web using DDG or RSS for news."""
    print(f"FRIDAY: Accessing global data streams for '{query}'...")
    try:
        # 1. RSS NEWS PROTOCOL (High-reliability source)
        if search_type == "news" and ("top" in query.lower() or "world" in query.lower()):
            try:
                import requests
                from bs4 import BeautifulSoup
                rss_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
                response = requests.get(rss_url, timeout=10)
                soup = BeautifulSoup(response.content, features="xml")
                items = soup.find_all('item')[:3]
                
                context = "LATEST GLOBAL NEWS (BBC RSS FEED):\n"
                for item in items:
                    t_el = item.find('title')
                    d_el = item.find('description')
                    title = t_el.text if t_el is not None else "Untitled"
                    desc = d_el.text if d_el is not None else ""
                    context += f"- {title}\n  Summary: {desc}\n"
                return context
            except Exception as rss_e:
                print(f"RSS Fallback Error: {rss_e}")

        # 2. DDG SEARCH PROTOCOL (Throttled to avoid 429 IP bans)
        api_throttler.wait("ddg_search")
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            try:
                from ddgs import DDGS  # type: ignore
            except ImportError:
                DDGS = None
        if DDGS is None:
            return "Web search is currently unavailable, Boss."
        with DDGS() as ddgs:
            if search_type == "news":
                results = list(ddgs.news(query, max_results=3))
                context = "LATEST NEWS HEADLINES:\n"
                for r in results:
                    context += f"- {r['title']} (Source: {r['source']})\n  Snippet: {r['body']}\n"
            else:
                results = list(ddgs.text(query, max_results=3))
                context = "SEARCH RESULTS AND SNIPPETS:\n"
                from core.web_utils import format_search_results
                context += format_search_results(results)
                
            return context
    except Exception as e:
        print(f"Web Search Error: {e}")
        if "403" in str(e) or "Ratelimit" in str(e):
            return "Web gateways are currently throttled, Boss. I suggest checking back in a few moments."
        return "I encountered a minor network error connecting to standard information streams, Boss."

def handle_news(cmd: str):
    """Fetches global news and synthesizes an intelligent briefing."""
    play_sound("launch")
    speak("Scanning latest global data streams, Boss.")
    news_context = web_search_intelligence("top world news", search_type="news")
    try:
        from core.background_coprocessor import coprocessor
        distilled_speech = coprocessor.distill_web_research("top world news", news_context)
        speak(distilled_speech)
    except Exception:
        prompt = f"Based on this news data, provide a witty and intelligent news briefing to the Boss:\n\n{news_context}"
        get_ai_response(prompt, speak_stream=True)

def handle_internet_query(cmd: str):
    """Executes live internet search and speaks synthesized response."""
    query = cmd.replace("search and tell me", "").replace("what is", "").replace("on the internet", "").replace("search for", "").strip()
    play_sound("launch")
    speak(f"Reaching out to global telemetry for {query}, Boss.")
    search_context = web_search_intelligence(query)
    try:
        from core.background_coprocessor import coprocessor
        distilled_speech = coprocessor.distill_web_research(query, search_context)
        speak(distilled_speech)
    except Exception:
        prompt = f"The Boss wants to know about '{query}'. Here is some live web data:\n\n{search_context}\n\nSummarize this for him with your personality."
        get_ai_response(prompt, speak_stream=True)

def handle_route_navigation(cmd: str):
    """Calculates driving route, distance, ETA, and launches Google Maps navigation in Brave."""
    play_sound("launch")
    clean_cmd = cmd.lower()
    origin = ""
    destination = ""
    
    if " from " in clean_cmd and " to " in clean_cmd:
        parts = clean_cmd.split(" from ", 1)[1].split(" to ", 1)
        origin = parts[0].strip()
        destination = parts[1].strip()
    elif " to " in clean_cmd:
        destination = clean_cmd.split(" to ", 1)[1].strip()
        origin = "Current Location"
    else:
        destination = clean_cmd.replace("directions", "").replace("route", "").replace("navigate", "").strip()
        origin = "Current Location"

    if not destination:
        destination = "Mumbai"

    route_data = maps_engine.calculate_route(origin, destination)
    maps_engine.render_and_launch_route(route_data, speak_fn=speak)

def handle_location(cmd: str):
    """Searches maps for a place, city, or locates synced contacts."""
    clean_lower = cmd.lower()

    # 1. Check if user is asking about code or codebase files
    code_terms = ["code", "engine", "service", "class", "function", "module", "script", "file", "symbol", "hub", "repo", "repository", "node", "graph"]
    if any(term in clean_lower for term in code_terms):
        play_sound("launch")
        import glob
        from core.graphify_service import graphify_engine
        reflex = graphify_engine.get_codebase_reflex(cmd)
        if reflex:
            speak(reflex)
            return
        clean_target = re.sub(r'(?i)\b(?:where\s+is|location\s+of|locate|our|the|code|located|file)\b', '', cmd).strip().replace(" ", "_")
        if clean_target:
            matches = [f for f in glob.glob('core/**/*.py', recursive=True) + glob.glob('*.py') if clean_target.lower() in f.lower()]
            if matches:
                speak(f"Located {clean_target} code in {matches[0]}, Boss.")
                return

    # 2. Check if user is asking about project archives
    if any(w in clean_lower for w in ["it stored", "project stored", "code stored", "file stored", "saved", "projects folder", "my code", "my project"]):
        play_sound("launch")
        proj_dir = os.path.realpath(os.path.join(os.path.splitdrive(os.getcwd())[0] + os.sep, "FRIDAY_Projects"))
        os.makedirs(proj_dir, exist_ok=True)
        try:
            os.startfile(proj_dir)
        except Exception:
            pass
        speak(f"All generated code and full-stack projects are archived in your FRIDAY Projects directory at {proj_dir}, Boss. Opening the folder now.")
        return

    play_sound("launch")
    target = cmd.replace("where is", "").replace("location of", "").replace("show on map", "").replace("open map for", "").replace("find on map", "").replace("maps", "").replace("map", "").strip()
    
    if not target or target.lower() in ["it", "this", "that"]:
        target = "Current Location"

    info = get_person_location(target)
    if info:
        speak(f"Active telemetry link found for {target}, Boss. Last updated at {info['last_sync']}.")
        maps_url = f"https://www.google.com/maps?q={info['lat']},{info['lon']}"
        open_in_brave(maps_url)
    else:
        place_data = maps_engine.search_location_or_place(target)
        maps_engine.render_and_launch_place(place_data, speak_fn=speak)

def handle_search(cmd: str):
    """Opens Google Search in Brave browser."""
    query = cmd.replace("search", "").strip()
    speak(f"Opening search stream for {query} in Brave, Boss.")
    open_in_brave(f"https://www.google.com/search?q={query}")
    handleSuggestion(f"Search: {query}")

def handle_autonomous_browse(cmd: str):
    """Deploys browser-use AI agent to execute web actions autonomously."""
    clean_task = cmd.replace("browse the web and", "").replace("browse the web", "").replace("browse and", "").replace("automate browser", "").replace("browser agent", "").replace("browse", "").strip()
    if not clean_task:
        clean_task = "Search Google and find latest updates"
    play_sound("launch")
    result = browser_agent.execute_task(clean_task, speak_fn=speak)
    if result:
        speak(result)

def handle_github_search(cmd: str):
    """Searches GitHub for top repositories, star counts, and architectures."""
    clean_query = cmd.replace("search on github for", "").replace("search github for", "").replace("search on github", "").replace("search github", "").replace("find on github", "").replace("github search", "").replace("github", "").strip()
    if not clean_query:
        clean_query = "AI agents"
    speak(f"Searching GitHub index for {clean_query}, Boss.")
    play_sound("launch")
    repos = github_engine.search_repositories(clean_query, max_results=5)
    github_engine.render_and_report(clean_query, repos, speak_fn=speak)

def handle_whatsapp(cmd: str):
    """Dispatches WhatsApp messaging using natural language parsing."""
    play_sound("launch")
    whatsapp_engine.send_message(cmd, speak_fn=speak)

def handle_deep_research_command(cmd: str):
    """Activates Autonomous Headless Web Agent for deep multi-page research."""
    try:
        play_sound("launch")
        clean_q = re.sub(r"^(deep research|research|deep search|browse to|browse|scrape)\s*", "", cmd, flags=re.I).strip()
        speak(f"Starting deep web research on {clean_q}, Boss~")
        def _research():
            briefing = browser_agent.deep_research(clean_q)
            speak(briefing)
        threading.Thread(target=_research, daemon=True).start()
    except Exception as err:
        print(f"[Deep Research Error]: {err}")
        speak("I encountered an issue executing deep web research, Boss.")

def dispatch_web_intent(cmd: str) -> bool:
    """Evaluates WhatsApp messaging and navigation intents."""
    cmd_lower = cmd.lower()
    if "whatsapp" in cmd_lower or ("message" in cmd_lower and any(p in cmd_lower for p in ["to", "send"])):
        handle_whatsapp(cmd)
        return True
    return False

COMMANDS = {
    "browse the web and": handle_autonomous_browse,
    "browse the web": handle_autonomous_browse,
    "browse and": handle_autonomous_browse,
    "automate browser": handle_autonomous_browse,
    "browser agent": handle_autonomous_browse,
    "autonomous browser": handle_autonomous_browse,
    "search on github for": handle_github_search,
    "search on github": handle_github_search,
    "search github for": handle_github_search,
    "search github": handle_github_search,
    "find on github": handle_github_search,
    "github search": handle_github_search,
    "message on whatsapp": handle_whatsapp,
    "send message on whatsapp": handle_whatsapp,
    "send whatsapp to": handle_whatsapp,
    "send whatsapp message to": handle_whatsapp,
    "send whatsapp": handle_whatsapp,
    "whatsapp message to": handle_whatsapp,
    "whatsapp message": handle_whatsapp,
    "message to": handle_whatsapp,
    "whatsapp to": handle_whatsapp,
    "whatsapp": handle_whatsapp,
    "news": handle_news,
    "search on google": handle_internet_query,
    "google search for": handle_internet_query,
    "google search": handle_internet_query,
    "search on internet": handle_internet_query,
    "search the internet for": handle_internet_query,
    "search the web for": handle_internet_query,
    "search and tell me": handle_internet_query,
    "directions from": handle_route_navigation,
    "directions to": handle_route_navigation,
    "directions": handle_route_navigation,
    "route from": handle_route_navigation,
    "route to": handle_route_navigation,
    "how far is": handle_route_navigation,
    "distance from": handle_route_navigation,
    "distance to": handle_route_navigation,
    "show on map": handle_location,
    "open map for": handle_location,
    "find on map": handle_location,
    "maps": handle_location,
    "where is": handle_location,
    "location of": handle_location,
    "deep research": handle_deep_research_command,
    "deep search": handle_deep_research_command,
    "research": handle_deep_research_command,
    "search": handle_search
}
