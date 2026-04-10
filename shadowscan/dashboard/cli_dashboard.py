"""
SHADOWSCAN PRO - Attack Dashboard
Cinematic CLI interface for live attack monitoring
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

"""
SHADOWSCAN PRO - Attack Dashboard
Cinematic CLI interface for live attack monitoring
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import deque

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import (
    Progress, SpinnerColumn, TextColumn, BarColumn,
    TaskProgressColumn, TimeElapsedColumn
)
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich import box
from rich.text import Text

import psutil

console = Console()

# Rest of the file remains the same...

class AttackDashboard:
    """Professional attack dashboard with live updates"""
    
    def __init__(self):
        self.colors = {
            'critical': 'bold red',
            'high': 'red',
            'medium': 'yellow',
            'low': 'green',
            'info': 'cyan',
            'success': 'bold green',
            'warning': 'bold yellow',
        }
        
        self.attack_events = deque(maxlen=10)
        self.current_phase = "INITIALIZING"
        self.phase_description = "Starting attack sequence..."
        self.start_time = datetime.now()
        self.stats = {
            "vulns_found": 0,
            "exploits_attempted": 0,
            "exploits_successful": 0,
            "shells_obtained": 0,
            "creds_found": 0,
            "files_exfiltrated": 0,
            "internal_hosts": 0,
        }
    
    def show_banner(self):
        """Display the epic SHADOWSCAN banner"""
        banner = f"""
[bold red]╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗███████╗ ██████╗ █████╗ ███╗   ██╗  ║
║   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔════╝██╔══██╗████╗  ██║  ║
║   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║███████╗██║     ███████║██╔██╗ ██║  ║
║   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║╚════██║██║     ██╔══██║██║╚██╗██║  ║
║   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝███████║╚██████╗██║  ██║██║ ╚████║  ║
║   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ║
║                                                                              ║
║                    [bold yellow]🔥 SHADOWSCAN PRO - OFFENSIVE SECURITY 🔥[/bold yellow]                  ║
║                                                                              ║
║              [bold cyan]⚡ ROHAIB TECHNICAL ⚡[/bold cyan] | [bold green]📞 +92 306 3844400 📞[/bold green]                 ║
║                                                                              ║
║     [dim]"The tool that doesn't just find vulnerabilities - it EXPLOITS them"[/dim]     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝[/bold red]
        """
        console.print(banner)
    
    def create_layout(self) -> Layout:
        """Create dashboard layout"""
        layout = Layout()
        
        layout.split(
            Layout(name="header", size=5),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        layout["body"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=3)
        )
        
        layout["left"].split(
            Layout(name="stats", size=8),
            Layout(name="progress", size=6),
            Layout(name="phase", size=5)
        )
        
        layout["right"].split(
            Layout(name="exploits", ratio=2),
            Layout(name="events", size=8)
        )
        
        return layout
    
    def create_header(self, target: str) -> Panel:
        """Create header panel"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        header_text = f"""
[bold red]🎯 TARGET:[/bold red] {target}                    [bold cyan]⚡ STATUS:[/bold cyan] [green]ATTACKING[/green]
[bold red]🌐 IP:[/bold red] Scanning...                        [bold yellow]📡 VULNS:[/bold yellow] {self.stats['vulns_found']}
[bold red]🏢 HOSTING:[/bold red] Detecting...                  [bold red]💀 EXPLOITS READY:[/bold red] {self.stats['exploits_successful']}
        """
        
        return Panel(
            Align.left(header_text),
            style="bold white on #1a1a2e",
            box=box.DOUBLE,
            border_style="red"
        )
    
    def create_stats_panel(self) -> Panel:
        """Create statistics panel"""
        stats_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        
        stats_table.add_row(
            "[bold cyan]💀 SHELLS OBTAINED[/bold cyan]",
            f"[bold red]{self.stats['shells_obtained']}[/bold red]"
        )
        stats_table.add_row(
            "[bold yellow]🔑 CREDENTIALS FOUND[/bold yellow]",
            f"[bold yellow]{self.stats['creds_found']}[/bold yellow]"
        )
        stats_table.add_row(
            "[bold green]📁 FILES EXFILTRATED[/bold green]",
            f"[bold green]{self.stats['files_exfiltrated']} MB[/bold green]"
        )
        stats_table.add_row(
            "[bold magenta]🌐 INTERNAL HOSTS[/bold magenta]",
            f"[bold magenta]{self.stats['internal_hosts']}[/bold magenta]"
        )
        
        return Panel(
            stats_table,
            title="[bold]📊 ATTACK STATISTICS[/bold]",
            border_style="red",
            box=box.ROUNDED
        )
    
    def create_progress_panel(self) -> Panel:
        """Create progress panel"""
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=30),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console
        )
        
        total_phases = 4
        current = {"RECON": 1, "VULN DETECTION": 2, "EXPLOITATION": 3, "POST-EXPLOIT": 4}.get(self.current_phase, 0)
        
        task = progress.add_task("[red]Attack Progress", total=total_phases)
        progress.update(task, completed=current - 1)
        
        return Panel(
            Align.center(f"{progress}\n[dim]Current: {self.phase_description}[/dim]"),
            title="[bold]⚔️ ATTACK PROGRESS[/bold]",
            border_style="yellow",
            box=box.ROUNDED
        )
    
    def create_phase_panel(self) -> Panel:
        """Create current phase panel"""
        phase_colors = {
            "RECON": "cyan",
            "VULN DETECTION": "yellow",
            "EXPLOITATION": "red",
            "POST-EXPLOIT": "magenta",
            "INITIALIZING": "white"
        }
        
        color = phase_colors.get(self.current_phase, "white")
        
        return Panel(
            Align.center(f"[bold {color}]🔥 {self.current_phase} 🔥[/bold {color}]\n\n{self.phase_description}"),
            title="[bold]🎯 CURRENT PHASE[/bold]",
            border_style=color,
            box=box.HEAVY
        )
    
    def create_exploits_panel(self) -> Panel:
        """Create active exploits panel"""
        exploits_table = Table(show_header=True, box=box.SIMPLE)
        exploits_table.add_column("Exploit", style="cyan", width=30)
        exploits_table.add_column("Status", style="bold", width=15)
        
        # Show recent attack events as exploits
        for event in list(self.attack_events)[-8:]:
            status_color = "green" if "SUCCESS" in event.get("status", "") else "yellow"
            exploits_table.add_row(
                event.get("name", "Unknown")[:28],
                f"[{status_color}]{event.get('status', 'PENDING')}[/{status_color}]"
            )
        
        if not self.attack_events:
            exploits_table.add_row("[dim]Waiting for exploits...[/dim]", "[dim]---[/dim]")
        
        return Panel(
            exploits_table,
            title="[bold]💣 ACTIVE EXPLOITS[/bold]",
            border_style="red",
            box=box.ROUNDED
        )
    
    def create_events_panel(self) -> Panel:
        """Create critical events panel"""
        events_text = ""
        
        for event in list(self.attack_events)[-6:]:
            level = event.get("level", "INFO")
            color = {"CRITICAL": "bold red", "HIGH": "red", "MEDIUM": "yellow", "INFO": "cyan"}.get(level, "white")
            
            events_text += f"[{color}][{level}][/{color}] {event.get('message', '')}\n"
        
        if not events_text:
            events_text = "[dim]No events yet...[/dim]"
        
        return Panel(
            events_text,
            title="[bold]⚠️ CRITICAL EVENTS[/bold]",
            border_style="red",
            box=box.HEAVY
        )
    
    def create_footer(self) -> Panel:
        """Create footer panel"""
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        
        footer_text = f"""
[dim]Memory: {memory.percent}% | CPU: {cpu}% | Developed by ROHAIB TECHNICAL | +92 306 3844400[/dim]
[dim]Press [bold]Ctrl+C[/bold] to abort attack[/dim]
        """
        
        return Panel(
            Align.center(footer_text),
            style="dim white",
            box=box.SIMPLE
        )
    
    def update_phase(self, phase: str, description: str):
        """Update current attack phase"""
        self.current_phase = phase
        self.phase_description = description
    
    def add_event(self, level: str, message: str, name: str = "", status: str = ""):
        """Add an attack event"""
        self.attack_events.append({
            "level": level,
            "message": message,
            "name": name,
            "status": status,
            "time": datetime.now().strftime("%H:%M:%S")
        })
    
    def update_stats(self, **kwargs):
        """Update statistics"""
        self.stats.update(kwargs)
    
    async def show_attack_dashboard(self, target: str, scan_data: Dict):
        """Show live attack dashboard"""
        layout = self.create_layout()
        
        with Live(layout, refresh_per_second=10, screen=True) as live:
            while scan_data.get("running", True):
                layout["header"].update(self.create_header(target))
                layout["stats"].update(self.create_stats_panel())
                layout["progress"].update(self.create_progress_panel())
                layout["phase"].update(self.create_phase_panel())
                layout["exploits"].update(self.create_exploits_panel())
                layout["events"].update(self.create_events_panel())
                layout["footer"].update(self.create_footer())
                
                live.update(layout)
                await asyncio.sleep(0.25)
    
    async def start_interactive_console(self):
        """Start interactive attack console"""
        self.show_banner()
        
        console.print("\n[bold green]🔥 SHADOWSCAN PRO INTERACTIVE CONSOLE 🔥[/bold green]")
        console.print("[dim]Type 'help' for commands, 'exit' to quit[/dim]\n")
        
        commands = {
            "help": "Show this help message",
            "scan": "Scan a target - scan <target>",
            "exploit": "Exploit a target - exploit <target>",
            "sessions": "List active sessions",
            "interact": "Interact with session - interact <session_id>",
            "payload": "Generate payload - payload <type> <lhost> <lport>",
            "exit": "Exit console"
        }
        
        while True:
            try:
                cmd = input("\n[shadowscan] #> ").strip().lower()
                
                if cmd == "help":
                    table = Table(title="[bold]Available Commands[/bold]", border_style="cyan")
                    table.add_column("Command", style="cyan")
                    table.add_column("Description", style="white")
                    
                    for cmd_name, desc in commands.items():
                        table.add_row(cmd_name, desc)
                    
                    console.print(table)
                    
                elif cmd == "exit":
                    console.print("[yellow]Exiting ShadowScan Pro...[/yellow]")
                    break
                    
                elif cmd.startswith("scan"):
                    parts = cmd.split()
                    if len(parts) > 1:
                        target = parts[1]
                        console.print(f"[cyan]Scanning {target}...[/cyan]")
                        # Would trigger scan
                    else:
                        console.print("[red]Usage: scan <target>[/red]")
                        
                elif cmd.startswith("exploit"):
                    parts = cmd.split()
                    if len(parts) > 1:
                        target = parts[1]
                        console.print(f"[red]🔥 Launching attack on {target}...[/red]")
                        # Would trigger exploit
                    else:
                        console.print("[red]Usage: exploit <target>[/red]")
                        
                elif cmd == "sessions":
                    console.print("[yellow]Active Sessions:[/yellow]")
                    console.print("  • session_abc123 - target.com (Windows 10)")
                    console.print("  • session_def456 - 192.168.1.100 (Ubuntu 22.04)")
                    
                elif cmd.startswith("payload"):
                    console.print("[cyan]Payload Generator:[/cyan]")
                    console.print("  Available payloads: reverse_shell, bind_shell, meterpreter")
                    
                else:
                    console.print(f"[red]Unknown command: {cmd}[/red]")
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            except EOFError:
                break