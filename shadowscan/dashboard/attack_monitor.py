"""
SHADOWSCAN PRO - Attack Monitor Dashboard
Real-time attack visualization and monitoring
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import deque

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich import box
from rich.text import Text

import psutil

console = Console()


class AttackMonitorDashboard:
    """Real-time attack monitoring dashboard"""
    
    def __init__(self):
        self.events = deque(maxlen=50)
        self.alerts = deque(maxlen=20)
        self.active_sessions = {}
        self.statistics = {
            "scans": 0,
            "vulns": 0,
            "exploits": 0,
            "shells": 0,
            "creds": 0,
            "data_gb": 0.0
        }
        self.start_time = datetime.now()
        self.current_target = "N/A"
        self.current_phase = "IDLE"
        
    def add_event(self, event_type: str, message: str, level: str = "INFO"):
        """Add monitoring event"""
        self.events.appendleft({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "type": event_type,
            "message": message,
            "level": level
        })
        
        # Update statistics
        if event_type == "scan_complete":
            self.statistics["scans"] += 1
        elif event_type == "vuln_found":
            self.statistics["vulns"] += 1
        elif event_type == "exploit_success":
            self.statistics["exploits"] += 1
        elif event_type == "shell_obtained":
            self.statistics["shells"] += 1
        elif event_type == "creds_found":
            self.statistics["creds"] += 1
    
    def add_alert(self, title: str, message: str, level: str = "HIGH"):
        """Add alert"""
        self.alerts.appendleft({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "title": title,
            "message": message,
            "level": level
        })
    
    def update_target(self, target: str):
        """Update current target"""
        self.current_target = target
    
    def update_phase(self, phase: str):
        """Update current attack phase"""
        self.current_phase = phase
    
    def add_session(self, session_id: str, target: str, platform: str):
        """Add active session"""
        self.active_sessions[session_id] = {
            "target": target,
            "platform": platform,
            "connected": datetime.now().strftime("%H:%M:%S")
        }
    
    def remove_session(self, session_id: str):
        """Remove session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
    
    def create_layout(self) -> Layout:
        """Create dashboard layout"""
        layout = Layout()
        
        layout.split(
            Layout(name="header", size=4),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        layout["body"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=2)
        )
        
        layout["left"].split(
            Layout(name="stats", size=8),
            Layout(name="sessions", size=8),
            Layout(name="phase", size=5)
        )
        
        layout["right"].split(
            Layout(name="alerts", size=10),
            Layout(name="events", size=11)
        )
        
        return layout
    
    def create_header(self) -> Panel:
        """Create header panel"""
        duration = (datetime.now() - self.start_time).total_seconds()
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        
        header_text = f"""
[bold red]🎯 TARGET:[/bold red] {self.current_target}
[bold cyan]⏱️ UPTIME:[/bold cyan] {hours:02d}:{minutes:02d}:{seconds:02d}
[bold yellow]⚡ PHASE:[/bold yellow] {self.current_phase}
[bold green]📡 SESSIONS:[/bold green] {len(self.active_sessions)} Active
        """
        
        return Panel(
            Align.center(header_text),
            style="bold white on #1a1a2e",
            box=box.DOUBLE,
            border_style="red"
        )
    
    def create_stats_panel(self) -> Panel:
        """Create statistics panel"""
        stats_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        
        stats_table.add_row(
            "[bold cyan]🔍 Scans Completed[/bold cyan]",
            f"[bold green]{self.statistics['scans']}[/bold green]"
        )
        stats_table.add_row(
            "[bold yellow]⚠️ Vulns Found[/bold yellow]",
            f"[bold yellow]{self.statistics['vulns']}[/bold yellow]"
        )
        stats_table.add_row(
            "[bold red]💀 Exploits Success[/bold red]",
            f"[bold red]{self.statistics['exploits']}[/bold red]"
        )
        stats_table.add_row(
            "[bold magenta]🐚 Shells Obtained[/bold magenta]",
            f"[bold magenta]{self.statistics['shells']}[/bold magenta]"
        )
        stats_table.add_row(
            "[bold blue]🔑 Creds Harvested[/bold blue]",
            f"[bold blue]{self.statistics['creds']}[/bold blue]"
        )
        
        return Panel(
            stats_table,
            title="[bold]📊 STATISTICS[/bold]",
            border_style="cyan",
            box=box.ROUNDED
        )
    
    def create_sessions_panel(self) -> Panel:
        """Create active sessions panel"""
        if not self.active_sessions:
            return Panel(
                "[dim]No active sessions[/dim]",
                title="[bold]🐚 ACTIVE SESSIONS[/bold]",
                border_style="green",
                box=box.ROUNDED
            )
        
        sessions_table = Table(show_header=True, box=box.SIMPLE)
        sessions_table.add_column("ID", style="cyan", width=10)
        sessions_table.add_column("Target", style="white", width=20)
        sessions_table.add_column("Platform", style="yellow", width=12)
        sessions_table.add_column("Connected", style="dim", width=10)
        
        for sid, data in list(self.active_sessions.items())[:5]:
            sessions_table.add_row(
                sid[:8],
                data["target"][:18],
                data["platform"],
                data["connected"]
            )
        
        return Panel(
            sessions_table,
            title=f"[bold]🐚 ACTIVE SESSIONS ({len(self.active_sessions)})[/bold]",
            border_style="green",
            box=box.ROUNDED
        )
    
    def create_phase_panel(self) -> Panel:
        """Create current phase panel"""
        phase_colors = {
            "RECON": "cyan",
            "VULN DETECTION": "yellow",
            "EXPLOITATION": "red",
            "POST-EXPLOIT": "magenta",
            "IDLE": "white"
        }
        
        color = phase_colors.get(self.current_phase, "white")
        
        phase_info = {
            "RECON": "Scanning and enumerating target...",
            "VULN DETECTION": "Identifying vulnerabilities...",
            "EXPLOITATION": "Launching exploits...",
            "POST-EXPLOIT": "Establishing persistence...",
            "IDLE": "Waiting for commands..."
        }
        
        return Panel(
            Align.center(f"[bold {color}]⚡ {self.current_phase} ⚡[/bold {color}]\n\n{phase_info.get(self.current_phase, '')}"),
            title="[bold]🎯 CURRENT PHASE[/bold]",
            border_style=color,
            box=box.HEAVY
        )
    
    def create_alerts_panel(self) -> Panel:
        """Create alerts panel"""
        if not self.alerts:
            return Panel(
                "[dim]No alerts[/dim]",
                title="[bold]🚨 ALERTS[/bold]",
                border_style="red",
                box=box.ROUNDED
            )
        
        alerts_text = ""
        for alert in list(self.alerts)[:8]:
            level_color = {
                "CRITICAL": "bold red",
                "HIGH": "red",
                "MEDIUM": "yellow",
                "LOW": "green",
                "INFO": "cyan"
            }.get(alert["level"], "white")
            
            alerts_text += f"[{level_color}][{alert['level']}][/{level_color}] {alert['title']}\n"
            alerts_text += f"[dim]{alert['message'][:50]}...[/dim]\n\n"
        
        return Panel(
            alerts_text,
            title=f"[bold]🚨 ALERTS ({len(self.alerts)})[/bold]",
            border_style="red",
            box=box.HEAVY
        )
    
    def create_events_panel(self) -> Panel:
        """Create events panel"""
        if not self.events:
            return Panel(
                "[dim]No events[/dim]",
                title="[bold]📡 EVENTS[/bold]",
                border_style="blue",
                box=box.ROUNDED
            )
        
        events_table = Table(show_header=True, box=box.SIMPLE)
        events_table.add_column("Time", style="dim", width=10)
        events_table.add_column("Type", style="cyan", width=12)
        events_table.add_column("Message", style="white", width=35)
        
        for event in list(self.events)[:10]:
            events_table.add_row(
                event["timestamp"],
                event["type"],
                event["message"][:33] + "..." if len(event["message"]) > 35 else event["message"]
            )
        
        return Panel(
            events_table,
            title="[bold]📡 RECENT EVENTS[/bold]",
            border_style="blue",
            box=box.ROUNDED
        )
    
    def create_footer(self) -> Panel:
        """Create footer panel"""
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        
        footer_text = f"""
[dim]Memory: {memory.percent}% | CPU: {cpu}% | Developed by ROHAIB TECHNICAL | +92 306 3844400[/dim]
[dim]Press [bold]Ctrl+C[/bold] to stop[/dim]
        """
        
        return Panel(
            Align.center(footer_text),
            style="dim white",
            box=box.SIMPLE
        )
    
    async def start_monitoring(self, scan_data: Dict):
        """Start live monitoring dashboard"""
        layout = self.create_layout()
        
        with Live(layout, refresh_per_second=10, screen=True) as live:
            while scan_data.get("running", True):
                layout["header"].update(self.create_header())
                layout["stats"].update(self.create_stats_panel())
                layout["sessions"].update(self.create_sessions_panel())
                layout["phase"].update(self.create_phase_panel())
                layout["alerts"].update(self.create_alerts_panel())
                layout["events"].update(self.create_events_panel())
                layout["footer"].update(self.create_footer())
                
                live.update(layout)
                await asyncio.sleep(0.25)
    
    def show_summary(self):
        """Show monitoring summary"""
        console.print("\n" + "=" * 60)
        console.print(Panel.fit(
            f"[bold red]🔥 ATTACK MONITORING SUMMARY 🔥[/bold red]\n\n"
            f"[cyan]Total Scans:[/cyan] {self.statistics['scans']}\n"
            f"[yellow]Vulnerabilities:[/yellow] {self.statistics['vulns']}\n"
            f"[red]Successful Exploits:[/red] {self.statistics['exploits']}\n"
            f"[magenta]Shells Obtained:[/magenta] {self.statistics['shells']}\n"
            f"[blue]Credentials:[/blue] {self.statistics['creds']}\n\n"
            f"[dim]Developed by ROHAIB TECHNICAL | +92 306 3844400[/dim]",
            border_style="red"
        ))