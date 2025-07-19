from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from app.models import ChatRequest, ChatResponse, ChatMessage, MessageRole, WSMessage
from app.gemini import gemini_client
from app.gemini.conversation import conversation_manager
import json
import logging
from typing import Dict
from datetime import datetime
from pydantic.json import pydantic_encoder

logger = logging.getLogger(__name__)
router = APIRouter()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_message(self, session_id: str, message: WSMessage):
        if session_id in self.active_connections:
            # Use custom encoder to handle datetime objects
            message_dict = json.loads(json.dumps(message.dict(), default=str))
            await self.active_connections[session_id].send_json(message_dict)

manager = ConnectionManager()

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Handle chat message and return response"""
    try:
        # Get or create session
        session_id = conversation_manager.get_or_create_session(request.session_id)
        
        # Add user message to history
        user_message = ChatMessage(
            role=MessageRole.USER,
            content=request.message
        )
        conversation_manager.add_message(session_id, user_message)
        
        # Get conversation history
        messages = conversation_manager.get_messages(session_id)
        
        # Send to Gemini
        reply, tool_calls = await gemini_client.chat(messages)
        
        # Add assistant message to history
        assistant_message = ChatMessage(
            role=MessageRole.ASSISTANT,
            content=reply,
            tool_calls=tool_calls
        )
        conversation_manager.add_message(session_id, assistant_message)
        
        # Create response
        response = ChatResponse(
            reply=reply,
            tool_calls=tool_calls,
            session_id=session_id
        )
        
        # Don't send WebSocket update for HTTP requests
        # The WebSocket handler will send updates for WebSocket messages
        
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, session_id)
    
    # Create or get session
    session_id = conversation_manager.get_or_create_session(session_id)
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Send status update
            await manager.send_message(session_id, WSMessage(
                type="status_update",
                data={"status": "processing"}
            ))
            
            # Process chat message
            user_message = ChatMessage(
                role=MessageRole.USER,
                content=message_data["message"]
            )
            conversation_manager.add_message(session_id, user_message)
            
            # Get conversation history
            messages = conversation_manager.get_messages(session_id)
            
            # Send to Gemini
            reply, tool_calls = await gemini_client.chat(messages)
            
            # Add assistant message
            assistant_message = ChatMessage(
                role=MessageRole.ASSISTANT,
                content=reply,
                tool_calls=tool_calls
            )
            conversation_manager.add_message(session_id, assistant_message)
            
            # Send response
            await manager.send_message(session_id, WSMessage(
                type="ai_reply",
                data={
                    "reply": reply,
                    "tool_calls": [tc.dict() for tc in tool_calls],
                    "timestamp": datetime.utcnow().isoformat()
                }
            ))
            
    except WebSocketDisconnect:
        manager.disconnect(session_id)
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(session_id)

@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session"""
    conversation_manager.clear_session(session_id)
    return {"message": "Session cleared"} 