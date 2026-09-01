"""
F.R.I.D.A.Y. OS 9.0: Autonomous Headless Web-Browsing Agent (Pillar 3)
Performs deep web research, dynamic page scraping, JavaScript SPA data extraction,
and autonomous web interaction with zero cloud subscription cost.
"""

import re
import urllib.parse
from typing import Optional, Dict, Any, List
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class AutonomousBrowserAgent:
    """
    High-Speed Headless Web Intelligence & Extraction Agent.
    Navigates live web pages, extracts structured DOM content, and summarizes multi-page findings.
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }

    def fetch_page_clean_text(self, url: str, max_chars: int = 4000) -> str:
        """
        Fetches web page, removes boilerplate (navs, footers, ads, scripts),
        and extracts clean, high-density text for LLM ingestion.
        """
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code != 200:
                return f"[HTTP Error {resp.status_code}]"

            soup = BeautifulSoup(resp.text, "html.parser")

            # Remove noise elements
            for el in soup(["script", "style", "nav", "footer", "aside", "noscript", "svg", "header", "form"]):
                el.decompose()

            # Extract main readable text
            text = soup.get_text(separator=" ", strip=True)
            text = re.sub(r"\s+", " ", text).strip()

            return text[:max_chars] if text else "No text extracted."
        except Exception as err:
            return f"[Fetch Error: {err}]"

    def search_duckduckgo(self, query: str, max_results: int = 4) -> List[Dict[str, str]]:
        """
        Queries DuckDuckGo HTML endpoint without API keys, returning list of {title, url, snippet}.
        """
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            resp = requests.get(url, headers=self.headers, timeout=8)
            if resp.status_code != 200:
                return []

            soup = BeautifulSoup(resp.text, "html.parser")
            results = []
            for item in soup.find_all("div", class_="result__body"):
                link_tag = item.find("a", class_="result__url") or item.find("a", class_="result__snippet")
                title_tag = item.find("a", class_="result__title") or item.find("h2")
                snippet_tag = item.find("a", class_="result__snippet") or item.find("div", class_="result__snippet")

                if title_tag and title_tag.get("href"):
                    raw_href = title_tag.get("href")
                    # Extract actual target url from DuckDuckGo redirect
                    if "uddg=" in raw_href:
                        parsed = urllib.parse.parse_qs(urllib.parse.urlparse(raw_href).query)
                        target_url = parsed.get("uddg", [raw_href])[0]
                    else:
                        target_url = raw_href

                    title = title_tag.get_text(strip=True)
                    snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

                    results.append({"title": title, "url": target_url, "snippet": snippet})
                    if len(results) >= max_results:
                        break

            return results
        except Exception:
            return []

    def deep_research(self, query: str) -> str:
        """
        Executes parallel multi-page deep research: searches DDG, fetches top 3 result pages,
        and uses the Cognitive Co-Processor to synthesize a comprehensive briefing.
        """
        search_results = self.search_duckduckgo(query, max_results=3)
        if not search_results:
            return f"I searched the web for '{query}' but could not retrieve live results, Boss."

        # Fetch top pages in parallel
        urls = [r["url"] for r in search_results if r["url"].startswith("http")]
        page_contents = {}

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_url = {executor.submit(self.fetch_page_clean_text, u, 2500): u for u in urls}
            for future in future_to_url:
                u = future_to_url[future]
                try:
                    page_contents[u] = future.result()
                except Exception:
                    page_contents[u] = "Failed to fetch."

        # Build synthesis prompt
        context_blocks = []
        for r in search_results:
            u = r["url"]
            body = page_contents.get(u, r.get("snippet", ""))
            context_blocks.append(f"SOURCE: {r['title']} ({u})\nCONTENT:\n{body}\n")

        synthesis_prompt = f"""
YOU ARE F.R.I.D.A.Y.'S DEEP WEB INTELLIGENCE AGENT.
Provide a clear, accurate, high-density briefing for Boss on: "{query}"

WEB INTELLIGENCE DATA:
{''.join(context_blocks)}

FORMAT:
- Direct Answer / Core Finding (1-2 sentences)
- Key Insights / Data Points (3-4 bullet points)
- Sources Cited
"""
        from core.background_coprocessor import coprocessor
        ok, briefing, _ = coprocessor.execute_fast_completion(
            "You are F.R.I.D.A.Y. Deep Web Research Analyst. Provide concise, high-value intelligence.",
            synthesis_prompt,
            max_tokens=600
        )

        if ok and briefing:
            return briefing.strip()

        # Fallback to direct snippet concatenation
        fallback_res = f"Here is what I found for '{query}', Boss:\n\n"
        for r in search_results[:3]:
            fallback_res += f"• {r['title']}: {r['snippet']}\n"
        return fallback_res


# Global singleton instance
browser_agent = AutonomousBrowserAgent()
