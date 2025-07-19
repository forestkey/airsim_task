from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.models import ChatMessage, MessageRole
import uuid

class ConversationManager:
    """Manage chat conversations and history"""
    
    def __init__(self, max_history: int = 20, session_timeout: int = 3600):
        self.conversations: Dict[str, List[ChatMessage]] = {}
        self.last_activity: Dict[str, datetime] = {}
        self.max_history = max_history
        self.session_timeout = session_timeout
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> str:
        """Get existing session or create new one"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.last_activity[session_id] = datetime.now()
        self._cleanup_old_sessions()
        
        return session_id
    
    def add_message(self, session_id: str, message: ChatMessage):
        """Add a message to the conversation"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append(message)
        self.last_activity[session_id] = datetime.now()
        
        # Keep only recent messages
        if len(self.conversations[session_id]) > self.max_history:
            self.conversations[session_id] = self.conversations[session_id][-self.max_history:]
    
    def get_messages(self, session_id: str) -> List[ChatMessage]:
        """Get all messages for a session"""
        return self.conversations.get(session_id, [])
    
    def clear_session(self, session_id: str):
        """Clear a specific session"""
        if session_id in self.conversations:
            del self.conversations[session_id]
        if session_id in self.last_activity:
            del self.last_activity[session_id]
    
    def _cleanup_old_sessions(self):
        """Remove sessions that have been inactive for too long"""
        now = datetime.now()
        timeout_delta = timedelta(seconds=self.session_timeout)
        
        expired_sessions = []
        for session_id, last_time in self.last_activity.items():
            if now - last_time > timeout_delta:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.clear_session(session_id)

# Global instance
conversation_manager = ConversationManager() 