"""
F.R.I.D.A.Y. Tactical Geospatial Navigation & Maps Subsystem
Provides route planning, distance estimation, travel duration, point-of-interest lookups,
and automatic Brave Browser Google Maps launching.
"""

import os
import urllib.parse
import requests
from typing import Dict, Any, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from core.browser_agent import open_in_brave

console = Console(force_terminal=True, legacy_windows=False)


class GeospatialMapsEngine:
    """Manages map routing, distance computation, and live navigation links."""

    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.osrm_url = "http://router.project-osrm.org/route/v1/driving"
        self.headers = {"User-Agent": "FRIDAY-Tactical-OS/7.0"}

    def geocode(self, place_name: str) -> Optional[Tuple[float, float, str]]:
        """Resolves place name into (lat, lon, display_name)."""
        try:
            params = {"q": place_name, "format": "json", "limit": 1}
            res = requests.get(self.nominatim_url, params=params, headers=self.headers, timeout=5)
            if res.status_code == 200 and res.json():
                data = res.json()[0]
                return float(data["lat"]), float(data["lon"]), data.get("display_name", place_name)
        except Exception:
            pass
        return None

    def calculate_route(self, origin: str, destination: str) -> Dict[str, Any]:
        """Calculates distance, duration, and builds Google Maps navigation link."""
        encoded_origin = urllib.parse.quote(origin)
        encoded_dest = urllib.parse.quote(destination)
        google_maps_url = f"https://www.google.com/maps/dir/?api=1&origin={encoded_origin}&destination={encoded_dest}&travelmode=driving"

        origin_geo = self.geocode(origin)
        dest_geo = self.geocode(destination)

        distance_km = None
        duration_mins = None

        if origin_geo and dest_geo:
            try:
                coords = f"{origin_geo[1]},{origin_geo[0]};{dest_geo[1]},{dest_geo[0]}"
                url = f"{self.osrm_url}/{coords}?overview=false"
                res = requests.get(url, timeout=5)
                if res.status_code == 200 and res.json().get("routes"):
                    route = res.json()["routes"][0]
                    distance_km = round(route["distance"] / 1000.0, 1)
                    duration_mins = round(route["duration"] / 60.0)
            except Exception:
                pass

        return {
            "origin": origin,
            "destination": destination,
            "distance_km": distance_km,
            "duration_mins": duration_mins,
            "maps_url": google_maps_url,
            "origin_display": origin_geo[2] if origin_geo else origin,
            "dest_display": dest_geo[2] if dest_geo else destination
        }

    def search_location_or_place(self, query: str) -> Dict[str, Any]:
        """Searches for a location, place of interest, or nearby spots on Google Maps."""
        encoded_q = urllib.parse.quote(query)
        maps_url = f"https://www.google.com/maps/search/{encoded_q}"
        geo = self.geocode(query)
        return {
            "query": query,
            "maps_url": maps_url,
            "display_name": geo[2] if geo else query,
            "coordinates": (geo[0], geo[1]) if geo else None
        }

    def render_and_launch_route(self, route_data: Dict[str, Any], speak_fn=None, auto_launch: bool = True):
        """Displays route telemetry in terminal, launches in Brave, and speaks summary."""
        orig = route_data["origin"]
        dest = route_data["destination"]
        dist = route_data["distance_km"]
        dur = route_data["duration_mins"]
        url = route_data["maps_url"]

        # 1. Render Rich Route Card
        table = Table(
            title=f"[bold cyan]🗺️ TACTICAL ROUTE // {orig.upper()} ➔ {dest.upper()}[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan",
            expand=True
        )
        table.add_column("Parameter", style="bold bright_white", width=22)
        table.add_column("Telemetry", style="cyan", width=50)

        table.add_row("Origin", str(route_data["origin_display"]))
        table.add_row("Destination", str(route_data["dest_display"]))
        
        if dist:
            hours = dur // 60
            mins = dur % 60
            dur_str = f"{hours} hr {mins} min" if hours > 0 else f"{mins} mins"
            table.add_row("Distance", f"[bold gold1]{dist} km[/bold gold1]")
            table.add_row("Estimated Drive Time", f"[bold green]{dur_str}[/bold green]")
        else:
            table.add_row("Distance / ETA", "Calculating live satellite traffic on launch...")

        table.add_row("Navigation URL", f"[underline bright_blue]{url}[/underline bright_blue]")

        console.print("\n")
        console.print(table)
        console.print("\n")

        # 2. Launch in Brave
        if auto_launch:
            open_in_brave(url)

        # 3. Speak vocal summary
        if speak_fn:
            if dist:
                hours = dur // 60
                mins = dur % 60
                time_speech = f"{hours} hours and {mins} minutes" if hours > 0 else f"{mins} minutes"
                speech = f"Route plotted from {orig} to {dest}, Boss. Total driving distance is approximately {dist} kilometers with an estimated travel time of {time_speech}. Launching live navigation in Brave now."
            else:
                speech = f"Navigation plotted for {orig} to {dest}, Boss. Opening live route stream in Brave."
            speak_fn(speech)

    def render_and_launch_place(self, place_data: Dict[str, Any], speak_fn=None, auto_launch: bool = True):
        """Displays location card, launches in Brave, and speaks summary."""
        q = place_data["query"]
        url = place_data["maps_url"]
        disp = place_data["display_name"]

        console.print(Panel(
            f"[bold cyan]Location / Query:[/bold cyan] [bold bright_white]{q}[/bold bright_white]\n"
            f"[bold cyan]Resolved Region:[/bold cyan] {disp}\n"
            f"[bold cyan]Live Maps Link:[/bold cyan] [underline bright_blue]{url}[/underline bright_blue]",
            title="[bold cyan]🗺️ SATELLITE MAP LOCATION[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        ))

        if auto_launch:
            open_in_brave(url)

        if speak_fn:
            speak_fn(f"Pulling up satellite map telemetry for {q} in Brave, Boss.")


# Global singleton instance
maps_engine = GeospatialMapsEngine()
