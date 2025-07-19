"""Gemini client with proxy support"""
import os
import google.generativeai as genai
from typing import List, Dict, Any
from app.core.config import settings
from app.models import ChatMessage, MessageRole, ToolCall
from app.mcp import DRONE_TOOLS, mcp_client
import json
import re
import logging

# Import fallback client
from .fallback_client import FallbackChatClient

logger = logging.getLogger(__name__)

# Configure proxy if available
def configure_proxy():
    """Configure proxy settings from environment"""
    http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
    
    if http_proxy or https_proxy:
        # Set proxy for httpx (used by google-generativeai internally)
        proxy_url = https_proxy or http_proxy
        logger.info(f"Using proxy: {proxy_url}")
        
        # Note: google-generativeai doesn't directly support proxy configuration
        # We need to set environment variables that the underlying libraries will use
        if http_proxy:
            os.environ['HTTP_PROXY'] = http_proxy
            os.environ['http_proxy'] = http_proxy
        if https_proxy:
            os.environ['HTTPS_PROXY'] = https_proxy
            os.environ['https_proxy'] = https_proxy
            
        return True
    return False

class GeminiClient:
    """Gemini API client with proxy support and prompt-based tool calling"""
    
    def __init__(self):
        self.fallback_client = FallbackChatClient()
        self.use_fallback = False
        
        # Configure proxy if available
        proxy_configured = configure_proxy()
        if proxy_configured:
            logger.info("Proxy configured for Gemini client")
        
        try:
            # Configure Gemini with API key
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Create enhanced system prompt with tool descriptions
            self.system_prompt = self._create_system_prompt()
            
            # Initialize model - try different models
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            try:
                self.model = genai.GenerativeModel(model_name)
                logger.info(f"Gemini client initialized with model: {model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize {model_name}, trying gemini-1.5-flash")
                self.model = genai.GenerativeModel("gemini-1.5-flash")
                logger.info("Gemini client initialized with gemini-1.5-flash")
                
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            logger.warning("Falling back to simple chat client")
            self.use_fallback = True
    
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
        
        return f"""你是一个专业的无人机控制助手。你可以帮助用户控制无人机执行各种飞行任务。

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
        # Use fallback if Gemini is not available
        if self.use_fallback:
            return await self.fallback_client.chat(messages)
        
        try:
            # Build conversation history with system prompt
            conversation_parts = [self.system_prompt]
            
            for msg in messages:
                if msg.role == MessageRole.USER:
                    conversation_parts.append(f"用户：{msg.content}")
                elif msg.role == MessageRole.ASSISTANT:
                    conversation_parts.append(f"助手：{msg.content}")
            
            # Add prompt for response
            conversation_parts.append("助手：")
            
            # Join all parts
            prompt = "\n\n".join(conversation_parts)
            
            # Generate response with shorter timeout
            response = self.model.generate_content(prompt)
            
            # Extract text from response
            if hasattr(response, 'text'):
                response_text = response.text
            else:
                # Fallback for different response structures
                response_text = str(response)
            
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
                
                try:
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
                except Exception as e:
                    logger.error(f"Failed to execute tool {tool_name}: {e}")
                    tool_calls.append(ToolCall(
                        tool=tool_name,
                        parameters=parameters,
                        result=None,
                        error=str(e)
                    ))
                    tool_results.append(f"工具 {tool_name} 执行失败：{str(e)}")
            
            # If there were tool calls, get final response
            if tool_results:
                # Add tool results to conversation and get final response
                conversation_parts.append(clean_text)
                conversation_parts.append("系统：" + "\n".join(tool_results))
                conversation_parts.append("助手（基于执行结果）：")
                
                final_prompt = "\n\n".join(conversation_parts)
                final_response = self.model.generate_content(final_prompt)
                
                if hasattr(final_response, 'text'):
                    final_text = final_response.text
                else:
                    final_text = str(final_response)
            else:
                final_text = clean_text
            
            return final_text, tool_calls
            
        except Exception as e:
            logger.error(f"Gemini chat error: {e}")
            
            # Check if it's a network/timeout error
            error_str = str(e).lower()
            if any(word in error_str for word in ['timeout', 'connect', 'network', '503', 'failed to connect']):
                logger.warning("Network error detected, using fallback chat client")
                # Switch to fallback for this session
                self.use_fallback = True
                return await self.fallback_client.chat(messages)
            
            error_msg = f"抱歉，我遇到了一个错误：{str(e)}"
            
            # 如果是API key相关的错误，提供更具体的提示
            if "API_KEY" in str(e).upper() or "api key" in str(e).lower():
                error_msg += "\n\n请检查 GEMINI_API_KEY 是否正确设置。"
            
            return error_msg, []
    
    async def simple_chat(self, message: str) -> str:
        """Simple chat without history"""
        try:
            response = self.model.generate_content(message)
            if hasattr(response, 'text'):
                return response.text
            else:
                return str(response)
        except Exception as e:
            logger.error(f"Gemini simple chat error: {e}")
            return f"抱歉，我遇到了一个错误：{str(e)}"

# Global instance - lazy initialization
_gemini_client = None

def get_gemini_client():
    """Get or create the global Gemini client instance"""
    global _gemini_client
    if _gemini_client is None:
        logger.info("Creating new GeminiClient instance...")
        _gemini_client = GeminiClient()
    return _gemini_client 