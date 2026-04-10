"""
SHADOWSCAN PRO - Offensive Security Automation Framework
Developed by ROHAIB TECHNICAL | +92 306 3844400
Military-grade exploitation and OSINT tool
"""

__version__ = "1.0.0"
__author__ = "ROHAIB TECHNICAL"
__contact__ = "+92 306 3844400"
__description__ = "Advanced Offensive Security & Auto-Exploitation Framework"

from .core.engine import ShadowEngine
from .core.exploit_chain import ExploitChain
from .core.payload_generator import PayloadGenerator
from .core.stealth_manager import StealthManager
from .core.session_manager import SessionManager
from .core.monitor import AttackMonitor, AlertManager
from .dashboard.cli_dashboard import AttackDashboard
from .dashboard.attack_monitor import AttackMonitorDashboard

__all__ = [
    "ShadowEngine",
    "ExploitChain", 
    "PayloadGenerator",
    "StealthManager",
    "SessionManager",
    "AttackMonitor",
    "AlertManager",
    "AttackDashboard",
    "AttackMonitorDashboard"
]