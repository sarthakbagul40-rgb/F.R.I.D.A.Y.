"""
F.R.I.D.A.Y. Honeycomb Hubs Registry
Exposes the 6 modular hubs: Chat, Media, System, Coding, Vision, and Web.
"""

import re
from typing import Dict, Any, Callable, List, Tuple

from core.hubs.base import (
    audio_queue,
    raw_audio_queue,
    IS_SPEAKING,
    WEB_REQUEST_ACTIVE,
    latest_web_response,
    play_sound,
    get_speaker,
    speak,
    drain_audio_queues,
    collect_continuous_speech
)

from core.hubs import chat_hub
from core.hubs import media_hub
from core.hubs import system_hub
from core.hubs import coding_hub
from core.hubs import vision_hub
from core.hubs import web_hub

def build_unified_commands() -> Tuple[Dict[str, Callable], List[Tuple[re.Pattern, str]]]:
    """
    Merges command tables from all 6 Honeycomb hubs ordered by length descending
    for maximal pattern specificity in regex word-boundary matching.
    """
    merged: Dict[str, Callable] = {}
    
    # Priority order: Coding -> Media -> Vision -> Web -> System
    merged.update(system_hub.COMMANDS)
    merged.update(web_hub.COMMANDS)
    merged.update(vision_hub.COMMANDS)
    merged.update(media_hub.COMMANDS)
    merged.update(coding_hub.COMMANDS)

    compiled = [
        (re.compile(rf"\b{re.escape(k)}\b", re.I), k)
        for k in sorted(merged.keys(), key=len, reverse=True)
    ]
    return merged, compiled
