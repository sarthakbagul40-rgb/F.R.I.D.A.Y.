"""
F.R.I.D.A.Y. GitHub Intelligence & Repository Discovery Subsystem
Enables real-time searching, star analysis, topic filtering, and architecture extraction across GitHub.
"""

import os
import requests
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console(force_terminal=True, legacy_windows=False)


class GitHubDiscoveryEngine:
    """Searches, ranks, and analyzes repositories directly from GitHub."""

    def __init__(self):
        self.api_url = "https://api.github.com/search/repositories"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "FRIDAY-Autonomous-AI/7.0"
        }
        # Optional user github token from environment
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            self.headers["Authorization"] = f"token {token}"

    def search_repositories(self, query: str, max_results: int = 5, sort: str = "stars") -> List[Dict[str, Any]]:
        """Searches GitHub for top repositories matching the query."""
        params = {
            "q": query,
            "sort": sort,
            "order": "desc",
            "per_page": max_results
        }
        try:
            response = requests.get(self.api_url, headers=self.headers, params=params, timeout=8)
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                results = []
                for item in items:
                    results.append({
                        "name": item.get("full_name"),
                        "stars": item.get("stargazers_count", 0),
                        "description": item.get("description") or "No description provided.",
                        "language": item.get("language") or "General",
                        "url": item.get("html_url"),
                        "forks": item.get("forks_count", 0),
                        "updated_at": item.get("updated_at", "")[:10]
                    })
                return results
            else:
                return []
        except Exception as e:
            print(f"[GitHub Engine Notice]: {e}")
            return []

    def render_and_report(self, query: str, repos: List[Dict[str, Any]], speak_fn=None) -> str:
        """Displays rich terminal table and speaks executive summary."""
        if not repos:
            msg = f"I scanned GitHub for '{query}', but couldn't find active matching repositories, Boss."
            if speak_fn:
                speak_fn(msg)
            return msg

        # 1. Render Rich Table
        table = Table(
            title=f"[bold cyan]🐙 GITHUB INTELLIGENCE // SEARCH: '{query.upper()}'[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan",
            expand=True
        )
        table.add_column("Repository", style="bold bright_white", width=28)
        table.add_column("Stars ⭐", style="bold gold1", width=12)
        table.add_column("Language", style="bold magenta", width=14)
        table.add_column("Description & Highlights", style="cyan", width=45)

        for r in repos:
            stars_formatted = f"{r['stars']:,} ⭐"
            desc = (r['description'][:75] + "...") if len(r['description']) > 75 else r['description']
            table.add_row(r['name'], stars_formatted, r['language'], desc)

        console.print("\n")
        console.print(table)
        console.print("\n")

        # 2. Formulate concise spoken briefing
        top = repos[0]
        summary_speech = (
            f"I searched GitHub for {query}, Boss. The top repository is {top['name'].split('/')[-1]} "
            f"with over {top['stars']:,} stars. It is described as: {top['description']}. "
            f"I found {len(repos)} leading options. Displaying the full comparison grid on your screen."
        )

        if speak_fn:
            speak_fn(summary_speech)

        return summary_speech


# Global singleton instance
github_engine = GitHubDiscoveryEngine()
