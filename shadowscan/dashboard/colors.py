"""
SHADOWSCAN PRO - Color Schemes
Professional color theming for CLI
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

from typing import Dict, Optional, List
from rich.style import Style
from rich.theme import Theme
from rich.color import Color


class ColorScheme:
    """Color scheme manager for ShadowScan Pro"""
    
    SCHEMES = {
        "default": {
            "primary": "#ff0000",
            "secondary": "#ff6600",
            "success": "#00ff00",
            "warning": "#ffff00",
            "error": "#ff0000",
            "info": "#00ccff",
            "dim": "#666666",
            "critical": "#ff0000",
            "high": "#ff6600",
            "medium": "#ffcc00",
            "low": "#00ff00",
            "background": "#1a1a2e",
            "border": "#ff0000"
        },
        "dark": {
            "primary": "#ff3333",
            "secondary": "#ff8833",
            "success": "#33ff33",
            "warning": "#ffff33",
            "error": "#ff3333",
            "info": "#33ccff",
            "dim": "#888888",
            "critical": "#ff3333",
            "high": "#ff8833",
            "medium": "#ffdd33",
            "low": "#33ff33",
            "background": "#0d0d1a",
            "border": "#ff3333"
        },
        "neon": {
            "primary": "#ff0066",
            "secondary": "#ff6600",
            "success": "#00ffcc",
            "warning": "#ffcc00",
            "error": "#ff0000",
            "info": "#00ccff",
            "dim": "#444444",
            "critical": "#ff0000",
            "high": "#ff6600",
            "medium": "#ffcc00",
            "low": "#00ff00",
            "background": "#000000",
            "border": "#ff0066"
        },
        "military": {
            "primary": "#2e8b57",
            "secondary": "#556b2f",
            "success": "#228b22",
            "warning": "#daa520",
            "error": "#8b0000",
            "info": "#4682b4",
            "dim": "#696969",
            "critical": "#8b0000",
            "high": "#b22222",
            "medium": "#daa520",
            "low": "#228b22",
            "background": "#1a1a1a",
            "border": "#2e8b57"
        },
        "matrix": {
            "primary": "#00ff00",
            "secondary": "#00cc00",
            "success": "#00ff00",
            "warning": "#ffff00",
            "error": "#ff0000",
            "info": "#00ffff",
            "dim": "#006600",
            "critical": "#ff0000",
            "high": "#ff6600",
            "medium": "#ffff00",
            "low": "#00ff00",
            "background": "#000000",
            "border": "#00ff00"
        }
    }
    
    def __init__(self, scheme_name: str = "default"):
        self.scheme_name = scheme_name
        self.colors = self.SCHEMES.get(scheme_name, self.SCHEMES["default"]).copy()
    
    def get(self, key: str, default: str = "white") -> str:
        """Get color by key"""
        return self.colors.get(key, default)
    
    def set_scheme(self, scheme_name: str):
        """Change color scheme"""
        if scheme_name in self.SCHEMES:
            self.scheme_name = scheme_name
            self.colors = self.SCHEMES[scheme_name].copy()
    
    def get_risk_color(self, risk: str) -> str:
        """Get color for risk level"""
        risk_lower = risk.lower()
        if risk_lower in ["critical", "crit"]:
            return self.get("critical", "#ff0000")
        elif risk_lower in ["high", "h"]:
            return self.get("high", "#ff6600")
        elif risk_lower in ["medium", "med", "m"]:
            return self.get("medium", "#ffcc00")
        elif risk_lower in ["low", "l"]:
            return self.get("low", "#00ff00")
        return self.get("info", "#00ccff")
    
    def get_score_color(self, score: float, max_score: float = 100) -> str:
        """Get color based on score"""
        percentage = (score / max_score) * 100
        
        if percentage >= 80:
            return self.get("critical", "#ff0000")
        elif percentage >= 60:
            return self.get("high", "#ff6600")
        elif percentage >= 40:
            return self.get("medium", "#ffcc00")
        elif percentage >= 20:
            return self.get("info", "#00ccff")
        else:
            return self.get("low", "#00ff00")
    
    def create_rich_theme(self) -> Theme:
        """Create Rich theme from color scheme"""
        styles = {}
        
        for key, value in self.colors.items():
            styles[f"shadowscan.{key}"] = Style(color=value)
        
        return Theme(styles)
    
    def get_all_schemes(self) -> List[str]:
        """Get available scheme names"""
        return list(self.SCHEMES.keys())


class ColorFormatter:
    """Format text with colors"""
    
    def __init__(self, scheme: ColorScheme = None):
        self.scheme = scheme or ColorScheme()
    
    def primary(self, text: str) -> str:
        return f"[{self.scheme.get('primary')}]{text}[/{self.scheme.get('primary')}]"
    
    def secondary(self, text: str) -> str:
        return f"[{self.scheme.get('secondary')}]{text}[/{self.scheme.get('secondary')}]"
    
    def success(self, text: str) -> str:
        return f"[{self.scheme.get('success')}]{text}[/{self.scheme.get('success')}]"
    
    def warning(self, text: str) -> str:
        return f"[{self.scheme.get('warning')}]{text}[/{self.scheme.get('warning')}]"
    
    def error(self, text: str) -> str:
        return f"[{self.scheme.get('error')}]{text}[/{self.scheme.get('error')}]"
    
    def info(self, text: str) -> str:
        return f"[{self.scheme.get('info')}]{text}[/{self.scheme.get('info')}]"
    
    def dim(self, text: str) -> str:
        return f"[{self.scheme.get('dim')}]{text}[/{self.scheme.get('dim')}]"
    
    def critical(self, text: str) -> str:
        return f"[bold {self.scheme.get('critical')}]{text}[/bold {self.scheme.get('critical')}]"
    
    def risk(self, text: str, level: str) -> str:
        color = self.scheme.get_risk_color(level)
        return f"[{color}]{text}[/{color}]"
    
    def score(self, score: float) -> str:
        color = self.scheme.get_score_color(score)
        return f"[{color}]{score:.1f}[/{color}]"
    
    def badge(self, text: str, badge_type: str = "info") -> str:
        colors = {
            "info": ("white", self.scheme.get("info")),
            "success": ("white", self.scheme.get("success")),
            "warning": ("black", self.scheme.get("warning")),
            "error": ("white", self.scheme.get("error")),
            "critical": ("white", self.scheme.get("critical"))
        }
        fg, bg = colors.get(badge_type, colors["info"])
        return f"[{fg} on {bg}] {text} [/]"
    
    def progress_bar(self, value: float, max_value: float = 100, width: int = 20) -> str:
        percentage = value / max_value
        filled = int(width * percentage)
        empty = width - filled
        color = self.scheme.get_score_color(value, max_value)
        return f"[{color}]{'█' * filled}{'░' * empty}[/{color}]"


# Global instances
default_scheme = ColorScheme("default")
default_formatter = ColorFormatter(default_scheme)


def set_color_scheme(scheme_name: str):
    """Change global color scheme"""
    global default_scheme, default_formatter
    default_scheme = ColorScheme(scheme_name)
    default_formatter = ColorFormatter(default_scheme)


def get_available_schemes() -> List[str]:
    """Get available color schemes"""
    return default_scheme.get_all_schemes()
