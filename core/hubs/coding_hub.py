"""
F.R.I.D.A.Y. Honeycomb Coding Hub
Autonomous Multi-Agent Coding Swarm, Graphify AST analysis, God's Eye orbital view, and CodeRabbit diff reviews.
"""

import os
import re
import threading
from core.claude_bridge import coding_engine
from core.maps_service import maps_engine
from core.graphify_service import graphify_engine
from core.code_reviewer import code_reviewer
from core.hubs.base import play_sound, speak

def handle_project_status(cmd: str):
    """Speaks active coding and project pipeline status with exact stage details."""
    play_sound("launch")
    speech = coding_engine.get_status_speech()
    speak(speech)

def handle_coding_command(cmd: str):
    """Directly dispatches the Multi-Agent Autonomous Coding Swarm (Claude Code CTO -> RuFlow -> OpenCode -> Gemini -> Groq LPU)."""
    try:
        play_sound("launch")
        speak("Right away, Boss. Initializing the autonomous engineering swarm now. Leave the architecture to me.")
        def _run_coding():
            coding_engine.handle_coding_request(cmd, speak_fn=speak, input_fn=input)
        threading.Thread(target=_run_coding, daemon=True).start()
    except Exception as err:
        print(f"[Coding Command Dispatch Error]: {err}")
        play_sound("error")
        speak("I encountered an issue launching the autonomous coding swarm, Boss.")

def handle_gods_eye_recon_cmd(cmd: str):
    """Activates God's Eye 3D Orbital Reconnaissance."""
    try:
        clean_target = re.sub(r"^(?:orbital\s+(?:scan|view)|god'?s\s+eye|satellite\s+view|recon)(?:\s+(?:on|of|over|for))?\s*", "", cmd, flags=re.I).strip()
        clean_target = re.sub(r"^(?:on|over|of|for)\s+", "", clean_target, flags=re.I).strip()
        if not clean_target:
            clean_target = "Tokyo"
        play_sound("launch")
        maps_engine.launch_gods_eye_recon(clean_target, speak_fn=speak)
    except Exception as e:
        speak(f"God's Eye telemetry failure: {e}")

def handle_graphify_cmd(cmd: str):
    """Builds or refreshes F.R.I.D.A.Y.'s deterministic AST code knowledge graph."""
    try:
        play_sound("launch")
        speak("Compiling codebase AST into the spiderweb knowledge graph, Boss.")
        res = graphify_engine.build_graph()
        if res.get("success"):
            stats = graphify_engine.get_summary_stats()
            speak(f"Code knowledge graph compiled, Boss. Mapped {stats.get('nodes_count', 0)} nodes and {stats.get('edges_count', 0)} relationships across {stats.get('communities', 0)} clusters.")
        else:
            speak("Knowledge graph update completed.")
    except Exception as e:
        speak(f"Graph generation notice: {e}")

def handle_graphify_reflex(cmd: str):
    """Answers codebase AST questions (node count, architecture stats, dependencies) via zero-latency AST reflex."""
    try:
        play_sound("launch")
        reflex = graphify_engine.get_codebase_reflex(cmd)
        if reflex:
            speak(reflex)
            return True
        else:
            stats = graphify_engine.get_summary_stats()
            if stats.get("status") == "ready":
                speak(f"Our live AST knowledge graph contains {stats['nodes_count']} nodes and {stats['edges_count']} relationships across {stats['communities']} clusters, Boss.")
                return True
            speak("AST knowledge graph is currently unbuilt or offline, Boss.")
            return True
    except Exception as e:
        speak(f"Codebase query notice: {e}")
        return True

def handle_code_review_cmd(cmd: str):
    """Runs CodeRabbit-style pre-commit diff audit."""
    try:
        play_sound("launch")
        speak("Executing CodeRabbit pre-commit diff safety audit, Boss.")
        diff_res = code_reviewer.audit_git_diff()
        if diff_res["overall_passed"]:
            speak(f"Diff audit passed, Boss. Audited {diff_res['audited_files']} modified files with zero hazards.")
        else:
            speak("Safety warning, Boss. Reviewer detected issues in modified files. Check terminal logs.")
    except Exception as e:
        speak(f"Code review notice: {e}")

def dispatch_coding_intent(cmd: str) -> bool:
    """Evaluates project status, graphify codebase queries, or coding imperative intents."""
    # 0. Zero-Latency AST Graphify Reflex Queries (node count, codebase stats, dependencies)
    graph_queries = [
        r'\bhow\s+many\s+nodes\b',
        r'\bgraph\s+nodes\b',
        r'\bgraph\s+stats\b',
        r'\bgraph\s+status\b',
        r'\bcodebase\s+stats\b',
        r'\bcodebase\s+reflex\b',
        r'\bcode\s+graph\s+stats\b',
        r'\bcodebase\s+size\b',
        r'\barchitecture\s+overview\b'
    ]
    if any(re.search(pat, cmd, re.I) for pat in graph_queries):
        handle_graphify_reflex(cmd)
        return True

    # 1. Project & Coding status triggers
    project_status_triggers = [
        r'\bproject\s+status\b', r'\bapp\s+status\b', r'\bcode\s+status\b',
        r'\bkya\s+chal\s+raha\s+hai\b', r'\bkahan\s+tak\s+pahuncha\b',
        r'\bkaam\s+kahan\s+tak\b', r'\bproject\s+bana\b', r'\bprogress\s+update\b',
        r'\bhow\s+is\s+(?:the\s+)?project(?:\s+going)?\b', r'\bhow\s+is\s+(?:the\s+)?app(?:\s+going)?\b',
        r'\bis\s+(?:the\s+)?project\s+ready\b', r'\bis\s+(?:the\s+)?app\s+ready\b',
        r'\bwhere\s+is\s+(?:it|the\s+project|the\s+code|the\s+app)\s+(?:stored|saved|located)\b',
        r'\bopen\s+(?:the\s+)?(?:project|projects|code|app)\s+folder\b',
        r'\bwhat\s+stage\b', r'\bwhich\s+stage\b', r'\bwhat\s+are\s+you\s+working\s+on\b'
    ]
    if any(re.search(trig, cmd, re.I) for trig in project_status_triggers):
        if any(w in cmd.lower() for w in ["where is", "open project folder", "open projects folder", "folder", "stored", "saved"]):
            proj_dir = os.path.realpath(os.path.join(os.path.splitdrive(os.getcwd())[0] + os.sep, "FRIDAY_Projects"))
            os.makedirs(proj_dir, exist_ok=True)
            try:
                os.startfile(proj_dir)
            except Exception:
                pass
            play_sound("launch")
            speak(f"Your project archives are stored in {proj_dir}, Boss. Opening the folder now.")
            return True
        handle_project_status(cmd)
        return True

def is_coding_intent(cmd: str) -> bool:
    """
    F.R.I.D.A.Y. Core DNA Coding Intent Recognizer.
    Recognizes imperatives, builder verbs (including STT artifacts like 'builder'),
    standalone software application names (e.g. 'clean password generator', 'pomodoro timer'),
    and multilingual engineering directives.
    """
    if not cmd or not cmd.strip():
        return False
        
    c = cmd.strip().lower()
    
    # 1. Filter out purely speculative or conversational questions
    is_conversational_statement = any(phrase in c for phrase in [
        "i am going to", "i will", "i'm going to", "i want to", "all nighter", "all-nighter",
        "hours", "going to code", "let me code", "trying to code", "thinking of", "feel like"
    ])
    is_question = any(q in c for q in [
        "how many days", "how long will it take", "what do you think of", "can you tell me what is",
        "what is a", "what are", "rebuild you", "build you", "days will it take"
    ])
    if is_conversational_statement or is_question:
        return False

    # 2. Phonetic & STT normalization
    # Remove leading wake words and greetings if present
    norm = re.sub(r'^(?:friday|jarvis|alexa|hey|yo)\s+', '', c).strip()
    # Normalize common STT mistranscriptions ("builder clean..." -> "build a clean...")
    norm = re.sub(r'\bbuilder\b', 'build a', norm)
    norm = re.sub(r'\bbuilding\s+a\b', 'build a', norm)

    # 3. Direct creation verbs followed by software targets
    creation_verbs = r'(?:create|build|make|generate|write|develop|design|craft|code|program|spin\s+up|launch|setup)'
    software_nouns = (
        r'(?:app|website|web\s+app|webapp|landing\s+page|script|program|code|dashboard|ui|interface|tool|'
        r'portfolio|game|backend|frontend|fullstack|fastapi|flask|react|converter|calculator|timer|tracker|'
        r'counter|clock|bot|extension|plugin|scraper|crawler|generator|clone|store|shop|portal|platform|'
        r'system|utility|widget|simulation|viewer|reader|player|editor|manager|helper|todo|to-do|todo\s+list|'
        r'task\s+list|form|table|page|site|solution|suite|component|service|module|api|database|model)'
    )

    # Pattern A: Verb + optional modifiers + software noun
    # e.g., "build a clean password generator", "create a simple currency converter", "make a pomodoro timer"
    verb_pattern = rf'\b{creation_verbs}\s+(?:me\s+)?(?:an?\s+)?(?:[a-zA-Z0-9_\-\s]{{0,40}}?\s+)?{software_nouns}\b'
    if re.search(verb_pattern, norm, re.I):
        return True

    # Pattern B: Standalone Software Tool Phrases (Zero verb required!)
    # e.g., "clean password generator", "password generator", "currency converter", "pomodoro timer", "todo app", "speed test"
    standalone_tools = [
        r'\b(?:(?:clean|simple|minimalist|modern|secure|fast|quick|dark\s+mode|responsive|offline)\s+)?password\s+generator\b',
        r'\b(?:(?:clean|simple|minimalist|modern|live)\s+)?currency\s+converter\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?pomodoro\s+timer\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?(?:stopwatch|countdown\s+timer|clock\s+widget)\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?(?:calculator|unit\s+converter|exchange\s+rate\s+calculator)\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?(?:todo\s+app|to-do\s+app|todo\s+list|task\s+manager|task\s+list)\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?(?:markdown\s+previewer|markdown\s+editor)\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?(?:color\s+picker|hex\s+color\s+picker)\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?qr\s+(?:code\s+)?generator\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?(?:json\s+formatter|json\s+validator)\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?weather\s+app\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?(?:habit\s+tracker|expense\s+tracker|budget\s+tracker)\b',
        r'\b(?:(?:clean|simple|minimalist|modern)\s+)?(?:typing\s+speed\s+test|speed\s+test\s+app)\b'
    ]
    if any(re.search(pat, norm, re.I) for pat in standalone_tools):
        return True

    # Pattern C: Language/framework specific directives
    # e.g., "write python script for ...", "code this in html/css"
    lang_pattern = r'\b(?:create|build|make|write|code|program)\s+(?:me\s+)?(?:an?\s+)?(?:[a-zA-Z0-9_\-]+\s+){1,4}(?:in\s+(?:python|html|javascript|js|ts|css|react|flask|fastapi|c\+\+|cpp|rust|java|go|c#)|with\s+(?:python|html|javascript|js|ts|css|database|sqlite|gui))\b'
    if re.search(lang_pattern, norm, re.I):
        return True

    # Pattern D: Swarm and Deep Build imperative keywords
    swarm_pattern = r'\b(?:deep\s+build|iron\s+swarm|lightning\s+build|lightning\s+core|claude\s+code|opencode|ruflow|autonomous\s+coder|coding\s+swarm)\b'
    if re.search(swarm_pattern, norm, re.I):
        return True

    # Pattern E: Bilingual Hindi / Hinglish directives
    # e.g., "ek password generator bana do", "currency converter banao", "python script likho"
    hinglish_pattern = r'\b(?:ek\s+)?(?:[a-zA-Z0-9_\-\s]{0,30}?\s+)?(?:app|website|code|script|project|tool|generator|converter|timer)\s+(?:bana\s+do|banao|likh\s+do|likho|develop\s+karo)\b'
    if re.search(hinglish_pattern, norm, re.I):
        return True

    return False

def dispatch_coding_intent(cmd: str) -> bool:
    """Evaluates project status, graphify codebase queries, or coding imperative intents."""
    # 0. Zero-Latency AST Graphify Reflex Queries (node count, codebase stats, dependencies)
    graph_queries = [
        r'\bhow\s+many\s+nodes\b',
        r'\bgraph\s+nodes\b',
        r'\bgraph\s+stats\b',
        r'\bgraph\s+status\b',
        r'\bcodebase\s+stats\b',
        r'\bcodebase\s+reflex\b',
        r'\bcode\s+graph\s+stats\b',
        r'\bcodebase\s+size\b',
        r'\barchitecture\s+overview\b'
    ]
    if any(re.search(pat, cmd, re.I) for pat in graph_queries):
        handle_graphify_reflex(cmd)
        return True

    # 1. Project & Coding status triggers
    project_status_triggers = [
        r'\bproject\s+status\b', r'\bapp\s+status\b', r'\bcode\s+status\b',
        r'\bkya\s+chal\s+raha\s+hai\b', r'\bkahan\s+tak\s+pahuncha\b',
        r'\bkaam\s+kahan\s+tak\b', r'\bproject\s+bana\b', r'\bprogress\s+update\b',
        r'\bhow\s+is\s+(?:the\s+)?project(?:\s+going)?\b', r'\bhow\s+is\s+(?:the\s+)?app(?:\s+going)?\b',
        r'\bis\s+(?:the\s+)?project\s+ready\b', r'\bis\s+(?:the\s+)?app\s+ready\b',
        r'\bwhere\s+is\s+(?:it|the\s+project|the\s+code|the\s+app)\s+(?:stored|saved|located)\b',
        r'\bopen\s+(?:the\s+)?(?:project|projects|code|app)\s+folder\b',
        r'\bwhat\s+stage\b', r'\bwhich\s+stage\b', r'\bwhat\s+are\s+you\s+working\s+on\b'
    ]
    if any(re.search(trig, cmd, re.I) for trig in project_status_triggers):
        if any(w in cmd.lower() for w in ["where is", "open project folder", "open projects folder", "folder", "stored", "saved"]):
            proj_dir = os.path.realpath(os.path.join(os.path.splitdrive(os.getcwd())[0] + os.sep, "FRIDAY_Projects"))
            os.makedirs(proj_dir, exist_ok=True)
            try:
                os.startfile(proj_dir)
            except Exception:
                pass
            play_sound("launch")
            speak(f"Your project archives are stored in {proj_dir}, Boss. Opening the folder now.")
            return True
        handle_project_status(cmd)
        return True

    # 2. Universal Autonomous Coding Swarm Intent DNA
    if is_coding_intent(cmd):
        handle_coding_command(cmd)
        return True

    return False

COMMANDS = {
    "orbital scan": handle_gods_eye_recon_cmd,
    "orbital view": handle_gods_eye_recon_cmd,
    "god's eye": handle_gods_eye_recon_cmd,
    "gods eye": handle_gods_eye_recon_cmd,
    "build code graph": handle_graphify_cmd,
    "refresh code graph": handle_graphify_cmd,
    "code graph": handle_graphify_cmd,
    "graphify": handle_graphify_cmd,
    "how many nodes": handle_graphify_reflex,
    "how many nodes do we have": handle_graphify_reflex,
    "graph nodes": handle_graphify_reflex,
    "graph stats": handle_graphify_reflex,
    "graph status": handle_graphify_reflex,
    "codebase reflex": handle_graphify_reflex,
    "codebase stats": handle_graphify_reflex,
    "codebase size": handle_graphify_reflex,
    "codebase overview": handle_graphify_reflex,
    "architecture overview": handle_graphify_reflex,
    "audit git diff": handle_code_review_cmd,
    "audit code diff": handle_code_review_cmd,
    "code review": handle_code_review_cmd,
    "about the project": handle_project_status,
    "about project": handle_project_status,
    "tell me about the project": handle_project_status,
    "project ke baare mein": handle_project_status,
    "project ka kya hua": handle_project_status,
    "project status": handle_project_status,
    "project update": handle_project_status,
    "coding status": handle_project_status,
    "app status": handle_project_status,
    "kya chal raha hai": handle_project_status,
    "kahan tak pahuncha": handle_project_status,
    "kaam kahan tak pahuncha": handle_project_status,
    "progress update": handle_project_status,
    "how is the project": handle_project_status,
    "how is the app": handle_project_status,
    "is the project ready": handle_project_status,
    "is the app ready": handle_project_status,
    "opencode se code banao": handle_coding_command,
    "opencode se app banao": handle_coding_command,
    "opencode se website banao": handle_coding_command,
    "opencode ko bolo": handle_coding_command,
    "opencode se banao": handle_coding_command,
    "claude ko bolo": handle_coding_command,
    "claude se app banao": handle_coding_command,
    "claude se code karwao": handle_coding_command,
    "ek app bana do": handle_coding_command,
    "ek app banao": handle_coding_command,
    "ek website bana do": handle_coding_command,
    "ek website banao": handle_coding_command,
    "code likh do": handle_coding_command,
    "code likho": handle_coding_command,
    "write a python script": handle_coding_command,
    "write python script": handle_coding_command,
    "write python code": handle_coding_command,
    "write a script": handle_coding_command,
    "write script": handle_coding_command,
    "create a script": handle_coding_command,
    "write code for": handle_coding_command,
    "write code to": handle_coding_command,
    "write code": handle_coding_command,
    "write a program": handle_coding_command,
    "create a program": handle_coding_command,
    "build a script": handle_coding_command,
    "build an app": handle_coding_command,
    "build a website": handle_coding_command,
    "create an app": handle_coding_command,
    "create a website": handle_coding_command,
    "code this": handle_coding_command,
    "code a": handle_coding_command,
    "code for me": handle_coding_command,
    "program a": handle_coding_command,
    "program an": handle_coding_command,
    "write a function": handle_coding_command,
    "write html": handle_coding_command,
    "write javascript": handle_coding_command,
    "write typescript": handle_coding_command,
    "write c++": handle_coding_command,
    "write cpp": handle_coding_command,
    "write java": handle_coding_command,
    "write rust": handle_coding_command,
    "write c#": handle_coding_command,
    "write golang": handle_coding_command,
    "debug this code": handle_coding_command,
    "fix this bug": handle_coding_command,
    "deep build": handle_coding_command,
    "iron swarm": handle_coding_command,
    "lightning build": handle_coding_command,
    "create a converter": handle_coding_command,
    "build a converter": handle_coding_command,
    "currency converter": handle_coding_command,
    "create a currency converter": handle_coding_command,
    "build a currency converter": handle_coding_command,
    "create a timer": handle_coding_command,
    "build a timer": handle_coding_command,
    "pomodoro timer": handle_coding_command,
    "create a calculator": handle_coding_command,
    "build a calculator": handle_coding_command,
    "create a tool": handle_coding_command,
    "build a tool": handle_coding_command,
    "password generator": handle_coding_command,
    "clean password generator": handle_coding_command,
    "create a password generator": handle_coding_command,
    "build a password generator": handle_coding_command,
    "builder clean password generator": handle_coding_command
}
