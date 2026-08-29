"""
F.R.I.D.A.Y. Web Intelligence Utilities
Formats search engine results into clean, prompt-friendly Markdown context.
"""

from typing import List, Dict, Any

def format_search_results(results: List[Dict[str, Any]]) -> str:
    """Formats DuckDuckGo / Bing results into a prompt-friendly string."""
    formatted = ""
    for idx, r in enumerate(results, 1):
        title = r.get('title', 'No Title')
        snippet = r.get('body', '')
        link = r.get('href', '')
        formatted += f"Source {idx}: {title}\n"
        formatted += f"Snippet: {snippet}\n"
        formatted += f"Link: {link}\n\n"
    return formatted
