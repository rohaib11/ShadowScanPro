"""
SHADOWSCAN PRO - Dark Web Crawler
Search .onion sites for leaked data
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import asyncio
import aiohttp
import re
import json
from typing import Dict, List, Optional, Any
from urllib.parse import quote, urljoin
import logging
import hashlib

logger = logging.getLogger(__name__)


class DarkWebCrawler:
    """Dark web search and crawling for leaked data"""
    
    # Dark web search engines
    SEARCH_ENGINES = [
        {
            "name": "Ahmia",
            "url": "https://ahmia.fi/search/",
            "tor_required": False
        },
        {
            "name": "Torch",
            "url": "http://xmh57jrzrnw6insl.onion/search",
            "tor_required": True
        },
        {
            "name": "DarkSearch",
            "url": "https://darksearch.io/api/search",
            "tor_required": False,
            "api": True
        }
    ]
    
    # Known leak sites (onion addresses)
    LEAK_SITES = [
        "http://breachdbsztj7t4.onion",
        "http://leakdbzxc123.onion",
        "http://cryptodb5f3g.onion",
    ]
    
    # Patterns for sensitive data
    SENSITIVE_PATTERNS = {
        "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "password": r'(?:password|passwd|pwd)[\s:=]+[\'"]?([^\'"\s]{6,})',
        "api_key": r'[A-Za-z0-9]{32,}',
        "aws_key": r'AKIA[0-9A-Z]{16}',
        "bitcoin": r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}',
        "ethereum": r'0x[a-fA-F0-9]{40}',
        "credit_card": r'\b(?:\d[ -]*?){13,16}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    }
    
    def __init__(self, use_tor: bool = True):
        self.use_tor = use_tor
        self.results: List[Dict] = []
        self.found_credentials: List[Dict] = []
        self.crawled_pages: set = set()
    
    async def search(self, query: str, deep: bool = False) -> List[Dict]:
        """Search dark web for query"""
        
        results = []
        
        session = await self._get_session()
        
        try:
            for engine in self.SEARCH_ENGINES:
                if engine["tor_required"] and not self.use_tor:
                    continue
                
                try:
                    engine_results = await self._search_engine(session, engine, query)
                    results.extend(engine_results)
                    
                except Exception as e:
                    logger.error(f"Search failed for {engine['name']}: {e}")
            
            if deep:
                # Crawl leak sites
                for site in self.LEAK_SITES:
                    if self.use_tor:
                        site_results = await self._crawl_leak_site(session, site, query)
                        results.extend(site_results)
                        
        finally:
            await session.close()
        
        # Process results for sensitive data
        for result in results:
            await self._analyze_result(result)
        
        self.results = results
        
        return results
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Create HTTP session with optional Tor proxy"""
        
        connector = None
        proxy = None
        
        if self.use_tor:
            proxy = "socks5://127.0.0.1:9050"
        
        timeout = aiohttp.ClientTimeout(total=30)
        
        return aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            proxy=proxy,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"
            }
        )
    
    async def _search_engine(self, session: aiohttp.ClientSession, 
                             engine: Dict, query: str) -> List[Dict]:
        """Search using a specific search engine"""
        
        results = []
        
        if engine.get("api"):
            # API-based search
            url = engine["url"]
            params = {"query": query, "page": 1}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for item in data.get("data", [])[:20]:
                        results.append({
                            "source": engine["name"],
                            "url": item.get("url", ""),
                            "title": item.get("title", ""),
                            "description": item.get("description", ""),
                            "risk": "high"
                        })
        else:
            # HTML-based search
            url = f"{engine['url']}?q={quote(query)}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    
                    # Extract results
                    links = re.findall(r'href="([^"]*\.onion[^"]*)"', html)
                    
                    for link in links[:10]:
                        results.append({
                            "source": engine["name"],
                            "url": link,
                            "title": "",
                            "description": "",
                            "risk": "medium"
                        })
        
        return results
    
    async def _crawl_leak_site(self, session: aiohttp.ClientSession,
                               site: str, query: str) -> List[Dict]:
        """Crawl a known leak site"""
        
        results = []
        
        try:
            async with session.get(site, timeout=20) as response:
                if response.status == 200:
                    html = await response.text()
                    
                    # Search for query in page
                    if query.lower() in html.lower():
                        # Extract data
                        emails = re.findall(self.SENSITIVE_PATTERNS["email"], html)
                        passwords = re.findall(self.SENSITIVE_PATTERNS["password"], html)
                        
                        if emails or passwords:
                            results.append({
                                "source": "leak_site",
                                "url": site,
                                "title": f"Leaked data for {query}",
                                "description": f"Found {len(emails)} emails and {len(passwords)} passwords",
                                "risk": "critical",
                                "emails": emails[:20],
                                "passwords": len(passwords)
                            })
                    
                    # Find links to more pages
                    links = re.findall(r'href="([^"]*)"', html)
                    
                    for link in links[:5]:
                        full_url = urljoin(site, link)
                        
                        if full_url not in self.crawled_pages:
                            self.crawled_pages.add(full_url)
                            
                            try:
                                async with session.get(full_url, timeout=10) as link_response:
                                    if link_response.status == 200:
                                        link_html = await link_response.text()
                                        
                                        if query.lower() in link_html.lower():
                                            results.append({
                                                "source": "leak_site_page",
                                                "url": full_url,
                                                "title": "",
                                                "description": f"Found reference to {query}",
                                                "risk": "high"
                                            })
                            except:
                                pass
                            
                            await asyncio.sleep(0.5)
                            
        except Exception as e:
            logger.error(f"Crawl failed for {site}: {e}")
        
        return results
    
    async def _analyze_result(self, result: Dict):
        """Analyze result for sensitive data"""
        
        url = result.get("url", "")
        description = result.get("description", "")
        
        combined_text = f"{url} {description}"
        
        for pattern_name, pattern in self.SENSITIVE_PATTERNS.items():
            matches = re.findall(pattern, combined_text, re.I)
            
            if matches:
                for match in matches[:5]:
                    credential = {
                        "type": pattern_name,
                        "value": match if isinstance(match, str) else match[0],
                        "source": result.get("source"),
                        "url": url,
                        "risk": "critical" if pattern_name in ["password", "api_key", "aws_key"] else "high"
                    }
                    
                    self.found_credentials.append(credential)
    
    async def search_credential_leaks(self, email: str) -> List[Dict]:
        """Search for leaked credentials by email"""
        
        results = []
        
        # Check common breach databases
        breach_apis = [
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
        ]
        
        session = await self._get_session()
        
        try:
            for api in breach_apis:
                async with session.get(api) as response:
                    if response.status == 200:
                        breaches = await response.json()
                        
                        for breach in breaches:
                            results.append({
                                "email": email,
                                "breach": breach.get("Name"),
                                "date": breach.get("BreachDate"),
                                "data_classes": breach.get("DataClasses", []),
                                "risk": "critical"
                            })
                            
        except Exception as e:
            logger.error(f"Breach check failed: {e}")
        finally:
            await session.close()
        
        return results
    
    async def find_exposed_crypto(self) -> List[Dict]:
        """Find exposed cryptocurrency wallets"""
        
        wallets = []
        
        session = await self._get_session()
        
        try:
            # Search for Bitcoin addresses
            btc_pattern = self.SENSITIVE_PATTERNS["bitcoin"]
            eth_pattern = self.SENSITIVE_PATTERNS["ethereum"]
            
            for engine in self.SEARCH_ENGINES[:1]:
                # Search for common wallet phrases
                queries = ["bitcoin private key", "wallet.dat", "ethereum keystore"]
                
                for query in queries:
                    results = await self._search_engine(session, engine, query)
                    
                    for result in results:
                        url = result.get("url", "")
                        
                        try:
                            async with session.get(url, timeout=10) as response:
                                if response.status == 200:
                                    text = await response.text()
                                    
                                    btc_matches = re.findall(btc_pattern, text)
                                    eth_matches = re.findall(eth_pattern, text)
                                    
                                    for btc in btc_matches[:5]:
                                        wallets.append({
                                            "type": "bitcoin",
                                            "address": btc,
                                            "source": url,
                                            "risk": "critical"
                                        })
                                    
                                    for eth in eth_matches[:5]:
                                        wallets.append({
                                            "type": "ethereum",
                                            "address": eth,
                                            "source": url,
                                            "risk": "critical"
                                        })
                        except:
                            pass
                        
                        await asyncio.sleep(0.3)
                        
        finally:
            await session.close()
        
        return wallets
    
    def generate_report(self) -> Dict:
        """Generate dark web search report"""
        
        risk_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        for cred in self.found_credentials:
            risk_counts[cred.get("risk", "medium")] += 1
        
        return {
            "total_results": len(self.results),
            "credentials_found": len(self.found_credentials),
            "risk_breakdown": risk_counts,
            "credential_types": {
                ctype: len([c for c in self.found_credentials if c["type"] == ctype])
                for ctype in set(c["type"] for c in self.found_credentials)
            },
            "top_findings": self.found_credentials[:20],
            "pages_crawled": len(self.crawled_pages),
            "recommendations": [
                "Change all exposed passwords immediately",
                "Enable 2FA on all accounts",
                "Monitor for identity theft",
                "Consider credit freeze"
            ]
        }