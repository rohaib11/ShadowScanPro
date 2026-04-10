"""
SHADOWSCAN PRO - Session Manager
Manages compromised sessions and shells
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import asyncio
import json
import uuid
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SessionType(Enum):
    """Types of sessions"""
    REVERSE_SHELL = "reverse_shell"
    BIND_SHELL = "bind_shell"
    WEB_SHELL = "web_shell"
    METERPRETER = "meterpreter"
    SSH = "ssh"
    RDP = "rdp"
    C2_BEACON = "c2_beacon"
    API_TOKEN = "api_token"


class SessionStatus(Enum):
    """Session status"""
    ACTIVE = "active"
    IDLE = "idle"
    DISCONNECTED = "disconnected"
    DEAD = "dead"
    UPGRADING = "upgrading"


@dataclass
class Session:
    """Represents a compromised session"""
    session_id: str
    session_type: SessionType
    target: str
    platform: str
    architecture: str
    user: str
    privileges: str
    status: SessionStatus
    created_at: datetime
    last_activity: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    commands_executed: List[str] = field(default_factory=list)
    files_uploaded: List[str] = field(default_factory=list)
    files_downloaded: List[str] = field(default_factory=list)


class SessionManager:
    """Manages all active sessions and shells"""
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.session_callbacks: Dict[str, List[Callable]] = {}
        self.interactive_session: Optional[str] = None
        self.max_sessions = 50
    
    def create_session(
        self,
        session_type: SessionType,
        target: str,
        platform: str = "unknown",
        architecture: str = "unknown",
        user: str = "unknown",
        privileges: str = "user",
        metadata: Dict = None
    ) -> Session:
        """Create a new session"""
        
        if len(self.sessions) >= self.max_sessions:
            # Remove oldest dead session
            dead_sessions = [s for s in self.sessions.values() if s.status == SessionStatus.DEAD]
            if dead_sessions:
                oldest = min(dead_sessions, key=lambda s: s.last_activity)
                del self.sessions[oldest.session_id]
            else:
                # Remove oldest disconnected
                disconnected = [s for s in self.sessions.values() if s.status == SessionStatus.DISCONNECTED]
                if disconnected:
                    oldest = min(disconnected, key=lambda s: s.last_activity)
                    del self.sessions[oldest.session_id]
        
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        session = Session(
            session_id=session_id,
            session_type=session_type,
            target=target,
            platform=platform,
            architecture=architecture,
            user=user,
            privileges=privileges,
            status=SessionStatus.ACTIVE,
            created_at=datetime.now(),
            last_activity=datetime.now(),
            metadata=metadata or {}
        )
        
        self.sessions[session_id] = session
        
        logger.info(f"New session created: {session_id} on {target} ({platform})")
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def list_sessions(self, status: SessionStatus = None) -> List[Session]:
        """List all sessions, optionally filtered by status"""
        sessions = list(self.sessions.values())
        
        if status:
            sessions = [s for s in sessions if s.status == status]
        
        return sorted(sessions, key=lambda s: s.last_activity, reverse=True)
    
    def update_session(self, session_id: str, **kwargs):
        """Update session properties"""
        session = self.sessions.get(session_id)
        
        if session:
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            
            session.last_activity = datetime.now()
            
            # Trigger callbacks
            if session_id in self.session_callbacks:
                for callback in self.session_callbacks[session_id]:
                    try:
                        callback(session)
                    except Exception as e:
                        logger.error(f"Session callback error: {e}")
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            del self.sessions[session_id]
            
            if session_id in self.session_callbacks:
                del self.session_callbacks[session_id]
            
            if self.interactive_session == session_id:
                self.interactive_session = None
            
            logger.info(f"Session deleted: {session_id}")
            return True
        
        return False
    
    def mark_session_dead(self, session_id: str):
        """Mark session as dead"""
        self.update_session(
            session_id,
            status=SessionStatus.DEAD,
            metadata={"death_time": datetime.now().isoformat()}
        )
    
    def mark_session_disconnected(self, session_id: str):
        """Mark session as disconnected"""
        self.update_session(session_id, status=SessionStatus.DISCONNECTED)
    
    def record_command(self, session_id: str, command: str, output: str = ""):
        """Record executed command"""
        session = self.sessions.get(session_id)
        
        if session:
            session.commands_executed.append({
                "command": command,
                "output": output[:1000],  # Truncate long output
                "timestamp": datetime.now().isoformat()
            })
            session.last_activity = datetime.now()
    
    def record_upload(self, session_id: str, local_path: str, remote_path: str):
        """Record file upload"""
        session = self.sessions.get(session_id)
        
        if session:
            session.files_uploaded.append({
                "local": local_path,
                "remote": remote_path,
                "timestamp": datetime.now().isoformat()
            })
            session.last_activity = datetime.now()
    
    def record_download(self, session_id: str, remote_path: str, local_path: str, size: int):
        """Record file download"""
        session = self.sessions.get(session_id)
        
        if session:
            session.files_downloaded.append({
                "remote": remote_path,
                "local": local_path,
                "size": size,
                "timestamp": datetime.now().isoformat()
            })
            session.last_activity = datetime.now()
    
    def set_interactive(self, session_id: str):
        """Set session as interactive"""
        if session_id in self.sessions:
            self.interactive_session = session_id
            logger.info(f"Interactive session set to: {session_id}")
            return True
        return False
    
    def get_interactive(self) -> Optional[Session]:
        """Get current interactive session"""
        if self.interactive_session:
            return self.sessions.get(self.interactive_session)
        return None
    
    def clear_interactive(self):
        """Clear interactive session"""
        self.interactive_session = None
    
    def on_session_update(self, session_id: str, callback: Callable):
        """Register callback for session updates"""
        if session_id not in self.session_callbacks:
            self.session_callbacks[session_id] = []
        self.session_callbacks[session_id].append(callback)
    
    async def execute_command(self, session_id: str, command: str) -> Optional[str]:
        """Execute command on session (simulated)"""
        session = self.sessions.get(session_id)
        
        if not session or session.status != SessionStatus.ACTIVE:
            return None
        
        # Simulate command execution
        await asyncio.sleep(0.5)
        
        # Simulated outputs based on command
        outputs = {
            "whoami": session.user,
            "hostname": session.target,
            "pwd": "/" if session.platform == "linux" else "C:\\",
            "ls": "Documents\nDownloads\nDesktop\n",
            "dir": "Documents\nDownloads\nDesktop\n",
            "id": f"uid={session.user} gid={session.user}",
            "ps": "PID TTY TIME CMD\n1 ? 00:00:00 init\n",
            "ipconfig": "192.168.1.100\n",
            "ifconfig": "eth0: 192.168.1.100\n",
        }
        
        output = outputs.get(command.lower(), f"Command '{command}' executed successfully")
        
        self.record_command(session_id, command, output)
        
        return output
    
    async def upload_file(self, session_id: str, local_path: str, remote_path: str) -> bool:
        """Upload file to session (simulated)"""
        session = self.sessions.get(session_id)
        
        if not session:
            return False
        
        await asyncio.sleep(1.0)
        
        self.record_upload(session_id, local_path, remote_path)
        
        return True
    
    async def download_file(self, session_id: str, remote_path: str, local_path: str) -> Optional[int]:
        """Download file from session (simulated)"""
        session = self.sessions.get(session_id)
        
        if not session:
            return None
        
        await asyncio.sleep(1.0)
        
        # Simulate file size
        size = 1024 * 100  # 100 KB
        
        self.record_download(session_id, remote_path, local_path, size)
        
        return size
    
    async def upgrade_shell(self, session_id: str) -> bool:
        """Upgrade shell to meterpreter or better shell"""
        session = self.sessions.get(session_id)
        
        if not session:
            return False
        
        self.update_session(session_id, status=SessionStatus.UPGRADING)
        
        await asyncio.sleep(2.0)
        
        if session.session_type == SessionType.REVERSE_SHELL:
            session.session_type = SessionType.METERPRETER
            session.metadata["upgraded_from"] = "reverse_shell"
        
        self.update_session(session_id, status=SessionStatus.ACTIVE)
        
        return True
    
    async def spawn_persistence(self, session_id: str, method: str = "scheduled_task") -> bool:
        """Spawn persistence on session"""
        session = self.sessions.get(session_id)
        
        if not session:
            return False
        
        await asyncio.sleep(1.5)
        
        session.metadata["persistence"] = {
            "method": method,
            "installed_at": datetime.now().isoformat()
        }
        
        return True
    
    def get_statistics(self) -> Dict:
        """Get session statistics"""
        total = len(self.sessions)
        active = len([s for s in self.sessions.values() if s.status == SessionStatus.ACTIVE])
        idle = len([s for s in self.sessions.values() if s.status == SessionStatus.IDLE])
        dead = len([s for s in self.sessions.values() if s.status == SessionStatus.DEAD])
        
        platforms = {}
        for session in self.sessions.values():
            platforms[session.platform] = platforms.get(session.platform, 0) + 1
        
        total_commands = sum(len(s.commands_executed) for s in self.sessions.values())
        total_downloads = sum(len(s.files_downloaded) for s in self.sessions.values())
        total_uploads = sum(len(s.files_uploaded) for s in self.sessions.values())
        
        return {
            "total_sessions": total,
            "active": active,
            "idle": idle,
            "dead": dead,
            "platforms": platforms,
            "total_commands": total_commands,
            "total_downloads": total_downloads,
            "total_uploads": total_uploads,
            "interactive_session": self.interactive_session
        }
    
    def export_session(self, session_id: str) -> Optional[Dict]:
        """Export session data"""
        session = self.sessions.get(session_id)
        
        if not session:
            return None
        
        return {
            "session_id": session.session_id,
            "type": session.session_type.value,
            "target": session.target,
            "platform": session.platform,
            "architecture": session.architecture,
            "user": session.user,
            "privileges": session.privileges,
            "status": session.status.value,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "metadata": session.metadata,
            "commands_count": len(session.commands_executed),
            "uploads_count": len(session.files_uploaded),
            "downloads_count": len(session.files_downloaded)
        }
    
    def export_all_sessions(self) -> List[Dict]:
        """Export all sessions"""
        return [self.export_session(s.session_id) for s in self.sessions.values() if s]
    
    def cleanup_dead_sessions(self):
        """Remove dead sessions older than 1 hour"""
        now = datetime.now()
        to_delete = []
        
        for session_id, session in self.sessions.items():
            if session.status == SessionStatus.DEAD:
                if (now - session.last_activity).total_seconds() > 3600:
                    to_delete.append(session_id)
        
        for session_id in to_delete:
            del self.sessions[session_id]
        
        return len(to_delete)