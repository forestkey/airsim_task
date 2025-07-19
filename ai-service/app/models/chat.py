from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

class ToolCall(BaseModel):
    tool: str
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = datetime.now()
    tool_calls: Optional[List[ToolCall]] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    tool_calls: Optional[List[ToolCall]] = None
    session_id: str
    timestamp: datetime = datetime.now()

class WSMessage(BaseModel):
    type: str  # "user_message", "ai_reply", "tool_execution", "status_update"
    data: Dict[str, Any]
    timestamp: datetime = datetime.now() 