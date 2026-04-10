"""
SHADOWSCAN PRO - Tor Manager
Manage Tor connections for anonymity
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import asyncio
import socket
import subprocess
import os
import signal
import time
from typing import Dict, Optional, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class TorManager:
    """Manages Tor connections and circuit renewal"""
    
    def __init__(
        self,
        socks_port: int = 9050,
        control_port: int = 9051,
        password: Optional[str] = None
    ):
        self.socks_port = socks_port
        self.control_port = control_port
        self.password = password
        self.process: Optional[subprocess.Popen] = None
        self.is_running = False
        self.circuit_count = 0
        self._stem_available = self._check_stem()
    
    def _check_stem(self) -> bool:
        """Check if stem library is available"""
        try:
            import stem
            return True
        except ImportError:
            logger.warning("Stem not installed - circuit renewal limited")
            return False
    
    def is_tor_running(self) -> bool:
        """Check if Tor is already running"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', self.socks_port))
            sock.close()
            return result == 0
        except:
            return False
    
    def start(self) -> bool:
        """Start Tor process"""
        if self.is_tor_running():
            logger.info("Tor is already running")
            self.is_running = True
            return True
        
        try:
            cmd = [
                'tor',
                '--SocksPort', str(self.socks_port),
                '--ControlPort', str(self.control_port),
                '--CookieAuthentication', '1',
                '--RunAsDaemon', '1'
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            # Wait for Tor to start
            for _ in range(30):
                if self.is_tor_running():
                    self.is_running = True
                    logger.info(f"Tor started on port {self.socks_port}")
                    return True
                time.sleep(0.5)
            
            logger.error("Tor failed to start within timeout")
            return False
            
        except FileNotFoundError:
            logger.error("Tor not installed. Install: sudo apt-get install tor")
            return False
        except Exception as e:
            logger.error(f"Failed to start Tor: {e}")
            return False
    
    def stop(self):
        """Stop Tor process"""
        if self.process:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                self.process.wait(timeout=10)
            except:
                try:
                    self.process.kill()
                except:
                    pass
            finally:
                self.process = None
        
        self.is_running = False
        logger.info("Tor stopped")
    
    def get_proxy_url(self) -> str:
        """Get SOCKS proxy URL"""
        return f"socks5://127.0.0.1:{self.socks_port}"
    
    def get_proxy_dict(self) -> Dict[str, str]:
        """Get proxy dict for requests"""
        proxy_url = self.get_proxy_url()
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    async def renew_circuit(self) -> bool:
        """Request new Tor circuit"""
        if not self._stem_available:
            logger.warning("Stem not available - cannot renew circuit")
            return False
        
        try:
            from stem import Signal
            from stem.control import Controller
            
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate(password=self.password)
                controller.signal(Signal.NEWNYM)
                
            self.circuit_count += 1
            logger.info(f"Tor circuit renewed (count: {self.circuit_count})")
            await asyncio.sleep(5)  # Wait for new circuit
            return True
            
        except Exception as e:
            logger.error(f"Failed to renew Tor circuit: {e}")
            return False
    
    async def get_current_ip(self) -> Optional[str]:
        """Get current exit node IP"""
        import aiohttp
        
        proxy = self.get_proxy_url()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://check.torproject.org/api/ip',
                    proxy=proxy,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('IP')
        except Exception as e:
            logger.error(f"Failed to get current IP: {e}")
        
        return None
    
    async def verify_tor_connection(self) -> bool:
        """Verify that we're connected through Tor"""
        import aiohttp
        
        proxy = self.get_proxy_url()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://check.torproject.org/api/ip',
                    proxy=proxy,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('IsTor', False)
        except Exception as e:
            logger.error(f"Tor verification failed: {e}")
        
        return False
    
    async def get_circuit_info(self) -> List[Dict]:
        """Get information about current circuits"""
        if not self._stem_available:
            return []
        
        circuits = []
        
        try:
            from stem.control import Controller
            
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate(password=self.password)
                
                for circ in controller.get_circuits():
                    circuit_info = {
                        'id': circ.id,
                        'status': circ.status,
                        'purpose': circ.purpose,
                        'paths': []
                    }
                    
                    for fingerprint, nickname in circ.path:
                        circuit_info['paths'].append({
                            'fingerprint': fingerprint[:16],
                            'nickname': nickname
                        })
                    
                    circuits.append(circuit_info)
                    
        except Exception as e:
            logger.error(f"Failed to get circuit info: {e}")
        
        return circuits
    
    def get_status(self) -> Dict:
        """Get Tor status"""
        return {
            "running": self.is_running,
            "socks_port": self.socks_port,
            "control_port": self.control_port,
            "circuit_count": self.circuit_count,
            "stem_available": self._stem_available,
            "proxy_url": self.get_proxy_url() if self.is_running else None
        }
    
    def restart(self) -> bool:
        """Restart Tor"""
        self.stop()
        time.sleep(2)
        return self.start()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *args):
        self.stop()
    
    async def __aenter__(self):
        self.start()
        return self
    
    async def __aexit__(self, *args):
        self.stop()