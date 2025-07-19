from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict, Any, Optional
import json
import asyncio
import logging
from datetime import datetime

from app.core.drone_client import drone_client
from app.models.drone import MoveCommand, Vector3

logger = logging.getLogger(__name__)
router = APIRouter()

# Store chat sessions
chat_sessions: Dict[str, Dict] = {}

@router.websocket("/ws/{session_id}")
async def websocket_chat_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for AI chat"""
    await websocket.accept()
    
    # Send connection confirmation
    await websocket.send_json({
        "type": "connected",
        "data": {"message": "WebSocket connected successfully"}
    })
    
    # Initialize session
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {
            "created_at": datetime.now(),
            "messages": []
        }
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            message = data.get("message", "")
            
            # Store message in session
            chat_sessions[session_id]["messages"].append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Process message and generate response
            response = await process_chat_message(message)
            
            # Send response
            await websocket.send_json({
                "type": "ai_reply",
                "data": {
                    "reply": response["reply"],
                    "tool_calls": response.get("tool_calls", []),
                    "session_id": session_id,
                    "timestamp": datetime.now().isoformat()
                }
            })
            
    except WebSocketDisconnect:
        logger.info(f"Chat WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"Chat WebSocket error: {e}")
        await websocket.close()

async def process_chat_message(message: str) -> Dict[str, Any]:
    """Process chat message and generate response"""
    message_lower = message.lower()
    
    # Simple command parsing (to be replaced with AI service later)
    if "起飞" in message or "takeoff" in message_lower:
        try:
            await drone_client.arm()
            await drone_client.takeoff()
            return {
                "reply": "无人机正在起飞...",
                "tool_calls": [{"tool": "takeoff", "parameters": {}}]
            }
        except Exception as e:
            return {"reply": f"起飞失败：{str(e)}"}
    
    elif "降落" in message or "land" in message_lower:
        try:
            await drone_client.land()
            return {
                "reply": "无人机正在降落...",
                "tool_calls": [{"tool": "land", "parameters": {}}]
            }
        except Exception as e:
            return {"reply": f"降落失败：{str(e)}"}
    
    elif "悬停" in message or "hover" in message_lower:
        try:
            await drone_client.hover()
            return {
                "reply": "无人机已悬停",
                "tool_calls": [{"tool": "hover", "parameters": {}}]
            }
        except Exception as e:
            return {"reply": f"悬停失败：{str(e)}"}
    
    elif "状态" in message or "status" in message_lower:
        try:
            state = await drone_client.get_state()
            return {
                "reply": f"当前位置：X={state.position.x:.2f}, Y={state.position.y:.2f}, Z={state.position.z:.2f}\n" +
                        f"高度：{abs(state.position.z):.2f}米\n" +
                        f"电池：{state.battery_level}%\n" +
                        f"飞行状态：{'飞行中' if state.is_flying else '地面'}"
            }
        except Exception as e:
            return {"reply": f"获取状态失败：{str(e)}"}
    
    elif "向前" in message or "forward" in message_lower:
        # Extract distance (simple parsing)
        try:
            distance = 5.0  # Default distance
            # Try to extract number from message
            import re
            numbers = re.findall(r'\d+', message)
            if numbers:
                distance = float(numbers[0])
            
            await drone_client.move_by_velocity(
                velocity=Vector3(x=distance/3.0, y=0, z=0),
                duration=3.0
            )
            return {
                "reply": f"向前飞行{distance}米...",
                "tool_calls": [{"tool": "move", "parameters": {"x": distance, "y": 0, "z": 0}}]
            }
        except Exception as e:
            return {"reply": f"移动失败：{str(e)}"}
    
    else:
        return {
            "reply": "我理解了您的指令。目前我支持的命令包括：起飞、降落、悬停、查看状态、向前飞行等。请问您想让无人机执行什么操作？"
        }

@router.post("/message")
async def send_chat_message(message: str, session_id: Optional[str] = None):
    """Send a chat message (REST endpoint)"""
    response = await process_chat_message(message)
    return response

@router.delete("/session/{session_id}")
async def clear_chat_session(session_id: str):
    """Clear a chat session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Session not found") 