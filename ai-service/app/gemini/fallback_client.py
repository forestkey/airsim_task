"""Fallback chat client for when Gemini API is unavailable"""
from typing import List, Dict, Any
from app.models import ChatMessage, MessageRole, ToolCall
from app.mcp import DRONE_TOOLS, mcp_client
import json
import re
import logging

logger = logging.getLogger(__name__)

class FallbackChatClient:
    """Simple fallback chat client with basic command parsing"""
    
    def __init__(self):
        self.command_patterns = {
            r'起飞|takeoff|飞起来': ('takeoff', {'altitude': 10}),
            r'降落|land|着陆': ('land', {}),
            r'悬停|hover|停': ('hover', {'duration': 5}),
            r'前进|forward|向前': ('move_forward', {'distance': 5}),
            r'后退|backward|向后': ('move_backward', {'distance': 5}),
            r'左移|left|向左': ('move_left', {'distance': 5}),
            r'右移|right|向右': ('move_right', {'distance': 5}),
            r'上升|up|向上': ('move_up', {'distance': 3}),
            r'下降|down|向下': ('move_down', {'distance': 3}),
        }
    
    async def chat(self, messages: List[ChatMessage]) -> tuple[str, List[ToolCall]]:
        """Process chat messages with simple command recognition"""
        if not messages:
            return "你好！我是无人机控制助手。你可以让我帮你控制无人机。", []
        
        # Get last user message
        last_message = None
        for msg in reversed(messages):
            if msg.role == MessageRole.USER:
                last_message = msg.content.lower()
                break
        
        if not last_message:
            return "请告诉我你想让无人机做什么。", []
        
        # Check for commands
        tool_calls = []
        for pattern, (tool_name, default_params) in self.command_patterns.items():
            if re.search(pattern, last_message):
                # Extract numbers from message for parameters
                numbers = re.findall(r'\d+(?:\.\d+)?', last_message)
                params = default_params.copy()
                
                # Update parameters with extracted numbers
                if numbers:
                    if tool_name in ['takeoff', 'move_up', 'move_down']:
                        params['altitude'] = float(numbers[0]) if 'altitude' in params else params.get('distance', float(numbers[0]))
                    elif 'distance' in params:
                        params['distance'] = float(numbers[0])
                    elif 'duration' in params:
                        params['duration'] = float(numbers[0])
                
                # Execute tool
                try:
                    result = await mcp_client.execute_tool(tool_name, params)
                    
                    tool_call = ToolCall(
                        tool=tool_name,
                        parameters=params,
                        result=result if result.get("success") else None,
                        error=result.get("error") if not result.get("success") else None
                    )
                    tool_calls.append(tool_call)
                    
                    if result.get("success"):
                        return f"好的，我已经执行了{self._get_action_name(tool_name)}操作。", tool_calls
                    else:
                        return f"执行{self._get_action_name(tool_name)}时出错：{result.get('error', '未知错误')}", tool_calls
                        
                except Exception as e:
                    logger.error(f"Failed to execute tool {tool_name}: {e}")
                    return f"执行命令时出错：{str(e)}", []
        
        # No command found
        return "我理解你的意思，但我现在只能执行基本的飞行命令。请尝试说：起飞、降落、前进、后退等。", []
    
    def _get_action_name(self, tool_name: str) -> str:
        """Get Chinese name for action"""
        action_names = {
            'takeoff': '起飞',
            'land': '降落',
            'hover': '悬停',
            'move_forward': '前进',
            'move_backward': '后退',
            'move_left': '左移',
            'move_right': '右移',
            'move_up': '上升',
            'move_down': '下降',
        }
        return action_names.get(tool_name, tool_name)
    
    async def simple_chat(self, message: str) -> str:
        """Simple chat without history"""
        messages = [ChatMessage(role=MessageRole.USER, content=message)]
        reply, _ = await self.chat(messages)
        return reply 