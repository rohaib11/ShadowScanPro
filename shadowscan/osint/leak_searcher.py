"""
SHADOWSCAN PRO - Leak Searcher
Search for leaked credentials and data
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import asyncio
import aiohttp
import re
import hashlib
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class LeakSearcher:
    """Search for data leaks and breaches"""
    
    # Leak sources
    SOURCES = [
        {"name": "HaveIBeenPwned", "url": "https://haveibeenpwned.com/api/v3/breachedaccount/"},
        {"name": "Dehashed", "url": "https://api.dehashed.com/search"},
        {"name": "LeakCheck", "url": "https://leakcheck.io/api/public"},
        {"name": "Snusbase", "url": "https://api.snusbase.com/data/search"},
        {"name": "BreachDirectory", "url": "https://breachdirectory.org/api"},
    ]
    
    # Paste sites
    PASTE_SITES = [
        "https://pastebin.com/archive",
        "https://paste.ee/",
        "https://justpaste.it/",
    ]
    
    def __init__(self):
        self.leaks_found = []
        self.credentials_found = []
        self.pastes_found = []
    
    async def search_email(self, email: str) -> Dict:
        """Search for email in breaches"""
        
        result = {
            "email": email,
            "breaches": [],
            "total_breaches": 0,
            "risk_level": "LOW"
        }
        
        session = aiohttp.ClientSession()
        
        try:
            # Check HIBP
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {"hibp-api-key": "free"}
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    breaches = await response.json()
                    result["breaches"] = breaches
                    result["total_breaches"] = len(breaches)
                    
                    for breach in breaches:
                        self.leaks_found.append({
                            "type": "email",
                            "value": email,
                            "breach": breach.get("Name"),
                            "date": breach.get("BreachDate")
                        })
                        
        except Exception as e:
            logger.error(f"Email search failed: {e}")
        finally:
            await session.close()
        
        if result["total_breaches"] > 5:
            result["risk_level"] = "CRITICAL"
        elif result["total_breaches"] > 0:
            result["risk_level"] = "HIGH"
        
        return result
    
    async def search_domain(self, domain: str) -> Dict:
        """Search for domain-related leaks"""
        
        result = {
            "domain": domain,
            "emails_found": [],
            "passwords_found": 0,
            "total_leaks": 0
        }
        
        session = aiohttp.ClientSession()
        
        try:
            # Search common email formats
            common_emails = [
                f"admin@{domain}",
                f"info@{domain}",
                f"contact@{domain}",
                f"support@{domain}",
                f"sales@{domain}",
            ]
            
            for email in common_emails:
                email_result = await self.search_email(email)
                if email_result["total_breaches"] > 0:
                    result["emails_found"].append(email)
                    result["total_leaks"] += email_result["total_breaches"]
                
                await asyncio.sleep(0.5)
                
        finally:
            await session.close()
        
        return result
    
    async def search_password(self, password: str) -> Dict:
        """Check if password appears in leaks"""
        
        result = {
            "password_hash": hashlib.sha1(password.encode()).hexdigest().upper(),
            "found": False,
            "count": 0
        }
        
        session = aiohttp.ClientSession()
        
        try:
            # HIBP password API
            hash_prefix = result["password_hash"][:5]
            url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    suffix = result["password_hash"][5:]
                    
                    for line in text.split('\n'):
                        if line.startswith(suffix):
                            result["found"] = True
                            result["count"] = int(line.split(':')[1])
                            break
                            
        except Exception as e:
            logger.error(f"Password search failed: {e}")
        finally:
            await session.close()
        
        return result
    
    async def search_pastes(self, query: str) -> List[Dict]:
        """Search paste sites for query"""
        
        results = []
        session = aiohttp.ClientSession()
        
        try:
            # Search Pastebin archive
            url = "https://psbdmp.ws/api/v3/search"
            params = {"q": query}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for paste in data.get("data", [])[:20]:
                        paste_info = {
                            "source": "pastebin",
                            "id": paste.get("id"),
                            "title": paste.get("title"),
                            "date": paste.get("date"),
                            "contains_query": True
                        }
                        results.append(paste_info)
                        self.pastes_found.append(paste_info)
                        
        except Exception as e:
            logger.error(f"Paste search failed: {e}")
        finally:
            await session.close()
        
        return results
    
    async def search_username(self, username: str) -> Dict:
        """Search for username across platforms"""
        
        result = {
            "username": username,
            "platforms": {},
            "available": False
        }
        
        platforms = [
            "github", "twitter", "instagram", "reddit", "linkedin",
            "facebook", "youtube", "tiktok", "telegram", "discord"
        ]
        
        session = aiohttp.ClientSession()
        
        try:
            for platform in platforms:
                url = f"https://{platform}.com/{username}"
                
                async with session.get(url, timeout=5) as response:
                    result["platforms"][platform] = {
                        "exists": response.status == 200,
                        "url": url if response.status == 200 else None
                    }
                
                await asyncio.sleep(0.3)
                
        except Exception as e:
            logger.error(f"Username search failed: {e}")
        finally:
            await session.close()
        
        return result
    
    async def search_phone(self, phone: str) -> Dict:
        """Search for phone number leaks"""
        
        result = {
            "phone": phone,
            "leaks": [],
            "carrier": None,
            "location": None
        }
        
        # Simulated phone search
        await asyncio.sleep(0.5)
        
        # Basic validation
        phone_clean = re.sub(r'[^\d]', '', phone)
        
        if len(phone_clean) >= 10:
            result["valid"] = True
            result["carrier"] = "Unknown"
            result["location"] = "Unknown"
        
        return result
    
    async def full_scan(self, target: str, target_type: str = "email") -> Dict:
        """Perform full leak scan"""
        
        results = {
            "target": target,
            "type": target_type,
            "findings": [],
            "risk_score": 0
        }
        
        if target_type == "email":
            email_result = await self.search_email(target)
            results["findings"].append(email_result)
            results["risk_score"] = min(100, email_result["total_breaches"] * 10)
            
        elif target_type == "domain":
            domain_result = await self.search_domain(target)
            results["findings"].append(domain_result)
            results["risk_score"] = min(100, domain_result["total_leaks"] * 5)
            
        elif target_type == "username":
            username_result = await self.search_username(target)
            results["findings"].append(username_result)
        
        # Search pastes
        paste_results = await self.search_pastes(target)
        results["findings"].append({"pastes": len(paste_results)})
        
        return results
    
    def generate_report(self) -> Dict:
        """Generate leak search report"""
        
        return {
            "total_leaks": len(self.leaks_found),
            "credentials_found": len(self.credentials_found),
            "pastes_found": len(self.pastes_found),
            "leaks": self.leaks_found[:20],
            "risk_level": "CRITICAL" if len(self.leaks_found) > 10 else "HIGH",
            "impact": "Credential exposure, identity theft risk",
            "recommendations": [
                "Change all exposed passwords immediately",
                "Enable 2FA on all accounts",
                "Use unique passwords for each service",
                "Monitor accounts for suspicious activity",
                "Consider identity theft protection"
            ]
        }