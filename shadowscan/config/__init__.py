"""
SHADOWSCAN PRO - Configuration Package
"""

from pathlib import Path

CONFIG_DIR = Path.home() / ".shadowscan"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CONFIG = {
    "stealth": {
        "profile": "shadow",
        "tor_enabled": False,
        "user_agent_rotation": True,
        "fingerprint_randomization": True
    },
    "exploits": {
        "auto_exploit": True,
        "safe_mode": False,
        "max_depth": 3
    },
    "reporting": {
        "format": "html",
        "output_dir": str(CONFIG_DIR / "reports")
    }
}