import google.generativeai as genai
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.models import ChatMessage, MessageRole, ToolCall
from app.mcp import DRONE_TOOLS, mcp_client
import json
import re
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    """Gemini API client with prompt-based tool calling"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Create enhanced system prompt with tool descriptions
        self.system_prompt = self._create_system_prompt()
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL
        )
    
    def _create_system_prompt(self) -> str:
        """Create system prompt with tool descriptions"""
        tools_description = "你可以使用以下工具控制无人机：\n\n"
        
        for tool in DRONE_TOOLS:
            tools_description += f"- **{tool['name']}**: {tool['description']}\n"
            if tool['parameters']['properties']:
                tools_description += "  参数：\n"
                for param, details in tool['parameters']['properties'].items():
                    required = param in tool['parameters'].get('required', [])
                    tools_description += f"    - {param}: {details['description']}"
                    if 'default' in details:
                        tools_description += f" (默认: {details['default']})"
                    if required:
                        tools_description += " [必需]"
                    tools_description += "\n"
            tools_description += "\n"
        
        return f"""{settings.SYSTEM_PROMPT}

{tools_description}

当需要调用工具时，请使用以下格式：
[TOOL_CALL]
{{
  "tool": "工具名称",
  "parameters": {{参数}}
}}
[/TOOL_CALL]

例如：
[TOOL_CALL]
{{
  "tool": "takeoff",
  "parameters": {{"altitude": 10}}
}}
[/TOOL_CALL]

在调用工具前，请先说明你要执行的操作。"""
    
    def _extract_tool_calls(self, text: str) -> tuple[str, List[Dict[str, Any]]]:
        """Extract tool calls from response text"""
        tool_calls = []
        clean_text = text
        
        # Find all tool call blocks
        pattern = r'\[TOOL_CALL\](.*?)\[/TOOL_CALL\]'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for match in matches:
            try:
                tool_data = json.loads(match.strip())
                tool_calls.append(tool_data)
                # Remove tool call from text
                clean_text = clean_text.replace(f'[TOOL_CALL]{match}[/TOOL_CALL]', '')
            except json.JSONDecodeError:
                logger.error(f"Failed to parse tool call: {match}")
        
        return clean_text.strip(), tool_calls
    
    async def chat(self, messages: List[ChatMessage]) -> tuple[str, List[ToolCall]]:
        """Send chat messages to Gemini and handle tool calls"""
        try:
            # Build conversation history
            conversation = self.system_prompt + "\n\n"
            
            for msg in messages:
                if msg.role == MessageRole.USER:
                    conversation += f"用户：{msg.content}\n\n"
                elif msg.role == MessageRole.ASSISTANT:
                    conversation += f"助手：{msg.content}\n\n"
            
            # Generate response
            response = self.model.generate_content(conversation)
            response_text = response.text
            
            # Extract tool calls
            clean_text, tool_call_data = self._extract_tool_calls(response_text)
            
            # Execute tool calls
            tool_calls = []
            tool_results = []
            
            for tool_data in tool_call_data:
                tool_name = tool_data.get("tool")
                parameters = tool_data.get("parameters", {})
                
                if not tool_name:
                    logger.error(f"Tool call missing tool name: {tool_data}")
                    continue
                
                # Execute tool through MCP
                result = await mcp_client.execute_tool(tool_name, parameters)
                
                # Create tool call record
                tool_call = ToolCall(
                    tool=tool_name,
                    parameters=parameters,
                    result=result if result.get("success") else None,
                    error=result.get("error") if not result.get("success") else None
                )
                tool_calls.append(tool_call)
                
                # Format result for model
                if result.get("success"):
                    tool_results.append(f"工具 {tool_name} 执行成功：{result.get('result', {}).get('message', '完成')}")
                else:
                    tool_results.append(f"工具 {tool_name} 执行失败：{result.get('error', '未知错误')}")
            
            # If there were tool calls, get final response
            if tool_results:
                # Add tool results to conversation and get final response
                conversation += f"助手：{clean_text}\n\n"
                conversation += "系统：" + "\n".join(tool_results) + "\n\n"
                conversation += "助手（基于执行结果）："
                
                final_response = self.model.generate_content(conversation)
                final_text = final_response.text
            else:
                final_text = clean_text
            
            return final_text, tool_calls
            
        except Exception as e:
            logger.error(f"Gemini chat error: {e}")
            return f"抱歉，我遇到了一个错误：{str(e)}", []
    
    async def simple_chat(self, message: str) -> str:
        """Simple chat without history"""
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            logger.error(f"Gemini simple chat error: {e}")
            return f"抱歉，我遇到了一个错误：{str(e)}"

# Global instance
gemini_client = GeminiClient() 