"""
SHADOWSCAN PRO - Progress Bars
Visual progress indicators for attacks
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import time
from typing import Optional, List, Dict, Any
from rich.progress import (
    Progress, SpinnerColumn, TextColumn, BarColumn,
    TaskProgressColumn, TimeElapsedColumn, TimeRemainingColumn,
    MofNCompleteColumn, TransferSpeedColumn
)
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class AttackProgress:
    """Attack progress visualization"""
    
    def __init__(self, total_phases: int = 4):
        self.total_phases = total_phases
        self.current_phase = 0
        self.phase_name = "INITIALIZING"
        self.start_time = time.time()
        
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold red]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console
        )
        
        self.phases = {
            1: "RECONNAISSANCE",
            2: "VULNERABILITY DETECTION",
            3: "EXPLOITATION",
            4: "POST-EXPLOITATION"
        }
    
    def start(self):
        """Start progress tracking"""
        self.progress.start()
        self.main_task = self.progress.add_task(
            "[red]🔥 ATTACK PROGRESS",
            total=self.total_phases
        )
    
    def advance_phase(self, phase_name: str = None):
        """Advance to next phase"""
        self.current_phase += 1
        if phase_name:
            self.phase_name = phase_name
        elif self.current_phase in self.phases:
            self.phase_name = self.phases[self.current_phase]
        
        self.progress.update(
            self.main_task,
            advance=1,
            description=f"[red]🔥 {self.phase_name}"
        )
    
    def update_description(self, description: str):
        """Update current task description"""
        self.progress.update(
            self.main_task,
            description=f"[yellow]⚡ {description}"
        )
    
    def add_subtask(self, name: str, total: int) -> int:
        """Add a subtask"""
        return self.progress.add_task(f"[cyan]  └─ {name}", total=total)
    
    def update_subtask(self, task_id: int, advance: int = 1):
        """Update subtask progress"""
        self.progress.update(task_id, advance=advance)
    
    def complete_subtask(self, task_id: int):
        """Mark subtask as complete"""
        self.progress.update(task_id, completed=self.progress._tasks[task_id].total)
        self.progress.remove_task(task_id)
    
    def stop(self):
        """Stop progress tracking"""
        self.progress.stop()
    
    def get_elapsed(self) -> float:
        """Get elapsed time"""
        return time.time() - self.start_time


class ExploitProgress:
    """Exploit execution progress"""
    
    def __init__(self):
        self.exploits = {}
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=30),
            MofNCompleteColumn(),
            console=console
        )
    
    def start(self):
        """Start tracking"""
        self.progress.start()
    
    def add_exploit(self, name: str, cve: str = None) -> int:
        """Add exploit to track"""
        display_name = f"{name}"
        if cve:
            display_name += f" ({cve})"
        
        task_id = self.progress.add_task(
            f"[red]💀 {display_name}",
            total=100
        )
        self.exploits[task_id] = {"name": name, "cve": cve}
        return task_id
    
    def update(self, task_id: int, percent: int, status: str = ""):
        """Update exploit progress"""
        name = self.exploits[task_id]["name"]
        desc = f"[red]💀 {name}"
        if status:
            desc += f" - {status}"
        
        self.progress.update(task_id, completed=percent, description=desc)
    
    def complete(self, task_id: int, success: bool = True):
        """Mark exploit as complete"""
        name = self.exploits[task_id]["name"]
        status = "[green]✓ SUCCESS[/green]" if success else "[red]✗ FAILED[/red]"
        self.progress.update(
            task_id,
            completed=100,
            description=f"[red]💀 {name} - {status}"
        )
    
    def stop(self):
        """Stop tracking"""
        self.progress.stop()


class DataExfilProgress:
    """Data exfiltration progress"""
    
    def __init__(self):
        self.progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console
        )
    
    def start(self):
        """Start tracking"""
        self.progress.start()
    
    def add_transfer(self, filename: str, total_size: int) -> int:
        """Add file transfer to track"""
        size_mb = total_size / (1024 * 1024)
        return self.progress.add_task(
            f"[cyan]📁 {filename} ({size_mb:.1f} MB)",
            total=total_size
        )
    
    def update(self, task_id: int, bytes_transferred: int):
        """Update transfer progress"""
        self.progress.update(task_id, advance=bytes_transferred)
    
    def stop(self):
        """Stop tracking"""
        self.progress.stop()


class ScanProgress:
    """Vulnerability scan progress"""
    
    def __init__(self, total_targets: int):
        self.total_targets = total_targets
        self.completed = 0
        self.findings = 0
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            console=console
        )
    
    def start(self):
        """Start scan progress"""
        self.progress.start()
        self.task = self.progress.add_task(
            f"[cyan]🔍 Scanning... (0 findings)",
            total=self.total_targets
        )
    
    def update(self, target: str, findings: int = 0):
        """Update scan progress"""
        self.completed += 1
        self.findings += findings
        
        self.progress.update(
            self.task,
            advance=1,
            description=f"[cyan]🔍 {target[:30]}... ({self.findings} findings)"
        )
    
    def stop(self):
        """Stop scan progress"""
        self.progress.stop()


def create_status_panel(stats: Dict) -> Panel:
    """Create status panel"""
    table = Table(show_header=False, box=None)
    table.add_column(style="cyan")
    table.add_column(style="green")
    
    for key, value in stats.items():
        table.add_row(f"{key}:", str(value))
    
    return Panel(table, title="[bold]STATUS[/bold]", border_style="cyan")


def create_attack_summary(exploit_results: List[Dict]) -> Panel:
    """Create attack summary panel"""
    if not exploit_results:
        return Panel("No exploits executed", title="[bold]ATTACK SUMMARY[/bold]")
    
    table = Table(show_header=True, box=None)
    table.add_column("Exploit", style="cyan")
    table.add_column("Target", style="white")
    table.add_column("Status", style="bold")
    
    for result in exploit_results:
        status = "[green]✓[/green]" if result.get("success") else "[red]✗[/red]"
        table.add_row(
            result.get("name", "Unknown"),
            result.get("target", "N/A")[:30],
            status
        )
    
    return Panel(table, title="[bold red]ATTACK SUMMARY[/bold red]", border_style="red")