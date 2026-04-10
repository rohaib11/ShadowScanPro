"""
SHADOWSCAN PRO - Fingerprint Randomizer
Browser fingerprint spoofing for stealth
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import random
import string
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class BrowserFingerprint:
    """Browser fingerprint data"""
    user_agent: str
    platform: str
    languages: List[str]
    timezone: str
    screen_resolution: Tuple[int, int]
    color_depth: int
    pixel_ratio: float
    hardware_concurrency: int
    device_memory: int
    vendor: str
    webgl_vendor: str
    webgl_renderer: str
    canvas_hash: str = ""
    audio_hash: str = ""
    fonts: List[str] = field(default_factory=list)


class FingerprintRandomizer:
    """Generate random browser fingerprints for evasion"""
    
    PLATFORMS = {
        'windows': {
            'platform': 'Win32',
            'vendor': 'Google Inc.',
            'webgl_vendors': ['Google Inc.', 'Intel Inc.', 'NVIDIA Corporation', 'AMD'],
            'renderers': [
                'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)',
                'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0)',
                'ANGLE (AMD, Radeon RX 580 Direct3D11 vs_5_0 ps_5_0)',
            ],
            'screen_resolutions': [(1920, 1080), (1366, 768), (1536, 864), (1440, 900), (2560, 1440)],
            'pixel_ratios': [1.0, 1.25, 1.5],
            'color_depths': [24, 32],
            'hardware_concurrencies': [4, 8, 12, 16],
            'device_memories': [4, 8, 16, 32]
        },
        'macos': {
            'platform': 'MacIntel',
            'vendor': 'Apple Computer, Inc.',
            'webgl_vendors': ['Apple Inc.', 'Intel Inc.', 'AMD'],
            'renderers': ['Apple M1', 'Apple M2', 'Intel Iris Plus Graphics', 'AMD Radeon Pro 5500M'],
            'screen_resolutions': [(1440, 900), (1680, 1050), (2560, 1600), (1920, 1080)],
            'pixel_ratios': [1.0, 2.0],
            'color_depths': [24, 30],
            'hardware_concurrencies': [8, 10, 12],
            'device_memories': [8, 16, 32, 64]
        },
        'linux': {
            'platform': 'Linux x86_64',
            'vendor': 'Google Inc.',
            'webgl_vendors': ['Intel Open Source Technology Center', 'NVIDIA Corporation', 'AMD', 'Mesa'],
            'renderers': [
                'Mesa Intel(R) UHD Graphics 620 (KBL GT2)',
                'Mesa DRI Intel(R) HD Graphics 530 (SKL GT2)',
                'NV134',
            ],
            'screen_resolutions': [(1920, 1080), (1366, 768), (1600, 900), (3840, 2160)],
            'pixel_ratios': [1.0],
            'color_depths': [24],
            'hardware_concurrencies': [2, 4, 8, 16],
            'device_memories': [4, 8, 16, 32]
        }
    }
    
    LANGUAGE_SETS = [
        ['en-US', 'en'],
        ['en-US', 'en', 'es'],
        ['en-GB', 'en'],
        ['en-US', 'en', 'fr'],
        ['en-US', 'en', 'de'],
        ['en-US', 'en', 'zh-CN', 'zh'],
        ['en-US', 'en', 'ja'],
    ]
    
    TIMEZONES = [
        'America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles',
        'Europe/London', 'Europe/Paris', 'Europe/Berlin', 'Asia/Tokyo',
        'Asia/Shanghai', 'Australia/Sydney', 'Pacific/Auckland',
    ]
    
    COMMON_FONTS = [
        'Arial', 'Arial Black', 'Calibri', 'Cambria', 'Comic Sans MS',
        'Consolas', 'Courier New', 'Georgia', 'Helvetica', 'Impact',
        'Segoe UI', 'Tahoma', 'Times New Roman', 'Trebuchet MS', 'Verdana',
        'Webdings', 'Wingdings'
    ]
    
    USER_AGENTS = {
        'windows': [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        ],
        'macos': [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.1 Safari/605.1.15',
        ],
        'linux': [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
        ]
    }
    
    def __init__(self, platform: str = None):
        self.platform = platform or random.choice(['windows', 'macos', 'linux'])
        self._fingerprint: Optional[BrowserFingerprint] = None
    
    def generate(self) -> BrowserFingerprint:
        """Generate random fingerprint"""
        platform_config = self.PLATFORMS[self.platform]
        screen_res = random.choice(platform_config['screen_resolutions'])
        
        fingerprint = BrowserFingerprint(
            user_agent=random.choice(self.USER_AGENTS[self.platform]),
            platform=platform_config['platform'],
            languages=random.choice(self.LANGUAGE_SETS),
            timezone=random.choice(self.TIMEZONES),
            screen_resolution=screen_res,
            color_depth=random.choice(platform_config['color_depths']),
            pixel_ratio=random.choice(platform_config['pixel_ratios']),
            hardware_concurrency=random.choice(platform_config['hardware_concurrencies']),
            device_memory=random.choice(platform_config['device_memories']),
            vendor=platform_config['vendor'],
            webgl_vendor=random.choice(platform_config['webgl_vendors']),
            webgl_renderer=random.choice(platform_config['renderers']),
            canvas_hash=hashlib.md5(str(random.random()).encode()).hexdigest(),
            audio_hash=hashlib.md5(str(random.random()).encode()).hexdigest(),
            fonts=random.sample(self.COMMON_FONTS, random.randint(15, 25))
        )
        
        self._fingerprint = fingerprint
        return fingerprint
    
    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers matching fingerprint"""
        if not self._fingerprint:
            self.generate()
        
        return {
            'User-Agent': self._fingerprint.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': ','.join(f"{lang};q={1.0 - i*0.1}" for i, lang in enumerate(self._fingerprint.languages)),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
    
    def rotate(self):
        """Generate new fingerprint"""
        return self.generate()
    
    def get_current(self) -> BrowserFingerprint:
        """Get current fingerprint"""
        if not self._fingerprint:
            self.generate()
        return self._fingerprint