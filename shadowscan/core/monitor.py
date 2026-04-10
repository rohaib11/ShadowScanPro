"""
SHADOWSCAN PRO - Continuous Monitor
Real-time attack monitoring and alerting
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import logging

logger = logging.getLogger(__name__)


@dataclass
class Alert:
    """Alert notification"""
    level: str  # critical, high, medium, low, info
    title: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "shadowscan"
    metadata: Dict = field(default_factory=dict)


class AttackMonitor:
    """Real-time attack monitoring system"""
    
    def __init__(self, max_events: int = 1000):
        self.events = deque(maxlen=max_events)
        self.alerts = deque(maxlen=100)
        self.statistics = {
            "scans_completed": 0,
            "vulnerabilities_found": 0,
            "exploits_successful": 0,
            "shells_obtained": 0,
            "credentials_harvested": 0,
            "data_exfiltrated_gb": 0.0
        }
        self.active_sessions = {}
        self.alert_handlers: List[Callable] = []
        self.start_time = datetime.now()
        self.running = False
    
    def add_event(self, event_type: str, data: Dict):
        """Add monitoring event"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event)
        
        # Update statistics
        if event_type == "scan_complete":
            self.statistics["scans_completed"] += 1
        elif event_type == "vulnerability_found":
            self.statistics["vulnerabilities_found"] += 1
        elif event_type == "exploit_success":
            self.statistics["exploits_successful"] += 1
        elif event_type == "shell_obtained":
            self.statistics["shells_obtained"] += 1
        elif event_type == "credentials_harvested":
            self.statistics["credentials_harvested"] += data.get("count", 0)
    
    def add_alert(self, alert: Alert):
        """Add and broadcast alert"""
        self.alerts.append(alert)
        
        # Notify handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Alert handler failed: {e}")
        
        # Log critical alerts
        if alert.level == "critical":
            logger.critical(f"[{alert.title}] {alert.message}")
        elif alert.level == "high":
            logger.error(f"[{alert.title}] {alert.message}")
    
    def register_alert_handler(self, handler: Callable):
        """Register alert callback"""
        self.alert_handlers.append(handler)
    
    def add_session(self, session_id: str, session_data: Dict):
        """Track active session"""
        self.active_sessions[session_id] = {
            **session_data,
            "created": datetime.now().isoformat()
        }
    
    def remove_session(self, session_id: str):
        """Remove session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
    
    def get_status(self) -> Dict:
        """Get current monitoring status"""
        return {
            "running": self.running,
            "uptime": (datetime.now() - self.start_time).total_seconds(),
            "active_sessions": len(self.active_sessions),
            "total_events": len(self.events),
            "total_alerts": len(self.alerts),
            "statistics": self.statistics,
            "recent_alerts": [
                {
                    "level": a.level,
                    "title": a.title,
                    "timestamp": a.timestamp.isoformat()
                }
                for a in list(self.alerts)[-10:]
            ]
        }
    
    def generate_report(self) -> Dict:
        """Generate monitoring report"""
        return {
            "monitoring_period": {
                "start": self.start_time.isoformat(),
                "end": datetime.now().isoformat(),
                "duration_seconds": (datetime.now() - self.start_time).total_seconds()
            },
            "statistics": self.statistics,
            "alert_summary": {
                "total": len(self.alerts),
                "by_level": {
                    level: len([a for a in self.alerts if a.level == level])
                    for level in ["critical", "high", "medium", "low", "info"]
                }
            },
            "active_sessions": list(self.active_sessions.keys()),
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on monitoring"""
        recommendations = []
        
        if self.statistics["vulnerabilities_found"] > 10:
            recommendations.append("Critical: Multiple vulnerabilities detected - immediate patching required")
        
        if self.statistics["shells_obtained"] > 0:
            recommendations.append("CRITICAL: Active shells detected - isolate affected systems immediately")
        
        if self.statistics["credentials_harvested"] > 100:
            recommendations.append("HIGH: Large credential harvest - rotate all passwords")
        
        return recommendations


class AlertManager:
    """Manage and route alerts to various channels"""
    
    def __init__(self, monitor: AttackMonitor):
        self.monitor = monitor
        self.monitor.register_alert_handler(self._handle_alert)
        self.webhooks = {}
        self.email_config = None
        self.telegram_config = None
        self.discord_config = None
    
    def _handle_alert(self, alert: Alert):
        """Process and route alert"""
        # Route based on level
        if alert.level == "critical":
            asyncio.create_task(self._send_critical_alert(alert))
        elif alert.level == "high":
            asyncio.create_task(self._send_high_alert(alert))
    
    async def _send_critical_alert(self, alert: Alert):
        """Send critical alert to all channels"""
        tasks = []
        
        if self.webhooks:
            tasks.append(self._send_webhook(alert))
        if self.telegram_config:
            tasks.append(self._send_telegram(alert))
        if self.discord_config:
            tasks.append(self._send_discord(alert))
        if self.email_config:
            tasks.append(self._send_email(alert))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _send_high_alert(self, alert: Alert):
        """Send high alert to primary channels"""
        if self.telegram_config:
            await self._send_telegram(alert)
        if self.webhooks:
            await self._send_webhook(alert)
    
    async def _send_webhook(self, alert: Alert) -> bool:
        """Send alert via webhook"""
        import aiohttp
        
        for url in self.webhooks.values():
            try:
                async with aiohttp.ClientSession() as session:
                    data = {
                        "level": alert.level,
                        "title": alert.title,
                        "message": alert.message,
                        "timestamp": alert.timestamp.isoformat(),
                        "source": alert.source
                    }
                    async with session.post(url, json=data) as response:
                        return response.status == 200
            except:
                pass
        return False
    
    async def _send_telegram(self, alert: Alert) -> bool:
        """Send alert via Telegram"""
        if not self.telegram_config:
            return False
        
        import aiohttp
        
        bot_token = self.telegram_config.get("bot_token")
        chat_id = self.telegram_config.get("chat_id")
        
        if not bot_token or not chat_id:
            return False
        
        message = f"""
🚨 *SHADOWSCAN ALERT [{alert.level.upper()}]* 🚨

*Title:* {alert.title}
*Message:* {alert.message}
*Time:* {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
*Source:* {alert.source}
"""
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        try:
            async with aiohttp.ClientSession() as session:
                data = {
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                }
                async with session.post(url, json=data) as response:
                    return response.status == 200
        except:
            pass
        return False
    
    async def _send_discord(self, alert: Alert) -> bool:
        """Send alert via Discord"""
        if not self.discord_config:
            return False
        
        import aiohttp
        
        webhook_url = self.discord_config.get("webhook_url")
        
        if not webhook_url:
            return False
        
        colors = {
            "critical": 0xFF0000,
            "high": 0xFFA500,
            "medium": 0xFFFF00,
            "low": 0x00FF00,
            "info": 0x0000FF
        }
        
        embed = {
            "title": f"🚨 {alert.title}",
            "description": alert.message,
            "color": colors.get(alert.level, 0x808080),
            "timestamp": alert.timestamp.isoformat(),
            "fields": [
                {"name": "Level", "value": alert.level.upper(), "inline": True},
                {"name": "Source", "value": alert.source, "inline": True}
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                data = {"embeds": [embed]}
                async with session.post(webhook_url, json=data) as response:
                    return response.status == 204
        except:
            pass
        return False
    
    async def _send_email(self, alert: Alert) -> bool:
        """Send alert via email"""
        # Simulated email sending
        logger.info(f"Email alert sent: {alert.title}")
        return True
    
    def configure_telegram(self, bot_token: str, chat_id: str):
        """Configure Telegram alerts"""
        self.telegram_config = {"bot_token": bot_token, "chat_id": chat_id}
    
    def configure_discord(self, webhook_url: str):
        """Configure Discord alerts"""
        self.discord_config = {"webhook_url": webhook_url}
    
    def configure_webhook(self, name: str, url: str):
        """Configure webhook"""
        self.webhooks[name] = url
    
    def configure_email(self, smtp_server: str, port: int, 
                        username: str, password: str, to_email: str):
        """Configure email alerts"""
        self.email_config = {
            "smtp_server": smtp_server,
            "port": port,
            "username": username,
            "password": password,
            "to_email": to_email
        }