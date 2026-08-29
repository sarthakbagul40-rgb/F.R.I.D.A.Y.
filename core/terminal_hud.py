"""
F.R.I.D.A.Y. Cybernetic Terminal HUD & UI/UX Engine
Sleek, minimalist, high-contrast, and 100% glitch-free across all Windows Terminals.
"""

import os
import sys
import psutil
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax
from rich.align import Align
from rich import box

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Force safe ASCII/UTF-8 rendering so boxes and characters never render as '?'
console = Console(force_terminal=True, legacy_windows=False, safe_box=True)

FRIDAY_ASCII = r"""
  _____ ____  ___ ____    _ __   __
 |  ___|  _ \|_ _|  _ \  / \\ \ / /
 | |_  | |_) || || | | |/ _ \\ V / 
 |  _| |  _ < | || |_| / ___ \| |  
 |_|   |_| \_\___|____/_/   \_\_|  
"""

def render_startup_banner():
    """Renders sleek minimalist HUD startup screen in the local terminal."""
    console.clear()
    
    title_text = Text(FRIDAY_ASCII, style="bold bright_cyan")
    sub_title = Text("F.R.I.D.A.Y. // NEURAL TACTICAL OPERATING SYSTEM (v7.5)", style="bold bright_white")
    full_form = Text("FAST RESPONSIVE INTELLIGENT DIGITAL ASSISTANT YIELD", style="dim cyan")
    status_tag = Text("STATUS: ONLINE & ARMED   |   OPERATOR: BOSS", style="bold gold1")
    
    content = Text.assemble(title_text, "\n\n", sub_title, "\n", full_form, "\n\n", status_tag)
    
    banner_panel = Panel(
        Align.center(content),
        border_style="bright_cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(banner_panel)
    console.print("[dim cyan]>> Audio receptors active. Say 'Friday' or 'Wake up' to command.[/dim cyan]\n")


def print_listening_state():
    """Prints clean, subtle ear sensor state."""
    console.print("[dim cyan]--- [Awaiting 'Friday' / 'Wake Up'] ---[/dim cyan]")


def print_heard(text: str):
    """Prints operator command in sleek amber prompt."""
    console.print(f"\n[bold gold1] [USER] Boss :>[/bold gold1] [bold bright_yellow]{text.strip()}[/bold bright_yellow]")


def print_speaking(text: str, voice_type: str = "FRIDAY"):
    """Prints F.R.I.D.A.Y.'s response in sleek cyan dialogue."""
    console.print(f"[bold bright_cyan] [AI] Friday :>[/bold bright_cyan] [bold bright_white]{text.strip()}[/bold bright_white]\n")


def print_code(code_str: str, language: str = "python"):
    """Renders formatted syntax-highlighted code box."""
    syntax = Syntax(code_str, language, theme="monokai", line_numbers=True, word_wrap=True)
    p = Panel(
        syntax,
        title=f"[bold cyan]AUTONOMOUS CODE ENGINE // {language.upper()}[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 1)
    )
    console.print(p)


def print_guard_request(action_desc: str) -> bool:
    """Renders glowing amber safety gatekeeper alert."""
    alert_text = (
        f"[bold bright_yellow]PERMISSION REQUEST:[/bold bright_yellow]\n"
        f"[bold bright_white] {action_desc}[/bold bright_white]\n\n"
        f"[dim]Confirm with [bold green]yes/y[/bold green] or cancel with [bold red]no/n[/bold red].[/dim]"
    )
    p = Panel(
        alert_text,
        title="[bold red]PERMISSION GATEKEEPER[/bold red]",
        border_style="yellow",
        box=box.ROUNDED,
        padding=(0, 2)
    )
    console.print(p)


def print_status_summary(cpu: float, ram: float, battery: str):
    """Renders clean diagnostic mini-card."""
    msg = f"[cyan]CPU:[/] [bold]{cpu}%[/]  |  [violet]RAM:[/] [bold]{ram}%[/]  |  [green]Power:[/] [bold]{battery}[/]"
    console.print(Panel(msg, title="[bold cyan]SYSTEM HEALTH[/bold cyan]", border_style="cyan", box=box.ROUNDED, padding=(0, 1)))


def render_project_stage(stage_num: int, total_stages: int, stage_name: str, detail: str, project_title: str = "Project"):
    """Renders sleek, clean progress card for autonomous project creation stages with universal ASCII bars."""
    percent = int((stage_num / total_stages) * 100)
    filled = "=" * (stage_num * 6)
    empty = "-" * ((total_stages - stage_num) * 6)
    bar_str = f"[{filled}>{empty}]"

    content = (
        f"[bold white]Project:[/] [bold bright_cyan]{project_title}[/]  |  [bold white]Stage:[/] [bold yellow]{stage_num}/{total_stages} ({stage_name})[/]\n"
        f"[bold white]Progress:[/] [bold cyan]{percent}%[/] [bold bright_cyan]{bar_str}[/]\n"
        f"[bold dim yellow]Action:[/] [white]{detail}[/]"
    )
    
    p = Panel(
        content,
        title=f"[bold cyan]AUTONOMOUS BUILDER // STAGE {stage_num}/{total_stages}[/bold cyan]",
        title_align="left",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 2)
    )
    console.print(p)


def render_project_complete(project_title: str, file_list: list, target_dir: str, duration_sec: float = 0.0):
    """Renders sleek success card upon project deployment."""
    files_str = "\n".join([f"  [green]+[/green] [bold white]{f}[/bold white]" for f in file_list])
    complete_content = (
        f"[bold bright_green]Project Deployed Successfully![/bold bright_green]\n\n"
        f"[bold cyan]Project:[/] [white]{project_title}[/]\n"
        f"[bold cyan]Directory:[/] [green]{target_dir}[/]\n"
        f"[bold cyan]Duration:[/] [yellow]{duration_sec:.1f}s[/]\n\n"
        f"[bold cyan]Artifacts:[/]\n{files_str}"
    )
    p = Panel(
        complete_content,
        title="[bold green]DEPLOYMENT COMPLETE[/bold green]",
        title_align="left",
        border_style="green",
        box=box.ROUNDED,
        padding=(0, 2)
    )
    console.print(p)
