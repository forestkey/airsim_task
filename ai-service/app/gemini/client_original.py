import google.generativeai as genai
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.models import ChatMessage, MessageRole, ToolCall
from app.mcp import DRONE_TOOLS, mcp_client
import json
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    """Gemini API client with tool calling support"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Convert tool definitions to Gemini format
        self.functions = self._convert_tools_to_functions()
        
        # Initialize model with tools
        self.model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            tools=self.functions,
            system_instruction=settings.SYSTEM_PROMPT
        )
    
    def _convert_tools_to_functions(self) -> List[Dict[str, Any]]:
        """Convert our tool definitions to Gemini's expected format"""
        functions = []
        
        for tool in DRONE_TOOLS:
            # Create function declaration in the format Gemini expects
            function = {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
            functions.append(function)
        
        return functions
    
    async def chat(self, messages: List[ChatMessage]) -> tuple[str, List[ToolCall]]:
        """Send chat messages to Gemini and handle tool calls"""
        try:
            # Convert messages to Gemini format
            chat_history = []
            for msg in messages[:-1]:  # All except the last message
                if msg.role == MessageRole.USER:
                    chat_history.append({"role": "user", "parts": [msg.content]})
                elif msg.role == MessageRole.ASSISTANT:
                    chat_history.append({"role": "model", "parts": [msg.content]})
            
            # Start chat session
            chat = self.model.start_chat(history=chat_history)
            
            # Send the latest message
            latest_message = messages[-1].content
            response = chat.send_message(latest_message)
            
            # Process response
            tool_calls = []
            final_text = ""
            
            # Check if response contains function calls
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call'):
                        fc = part.function_call
                        tool_name = fc.name
                        
                        # Parse arguments
                        try:
                            # Convert args to dict
                            args = {}
                            for key, value in fc.args.items():
                                args[key] = value
                        except:
                            args = {}
                        
                        # Execute tool through MCP
                        result = await mcp_client.execute_tool(tool_name, args)
                        
                        # Create tool call record
                        tool_call = ToolCall(
                            tool=tool_name,
                            parameters=args,
                            result=result if result.get("success") else None,
                            error=result.get("error") if not result.get("success") else None
                        )
                        tool_calls.append(tool_call)
                        
                        # Send function response back to model
                        response_parts = [{
                            "function_response": {
                                "name": tool_name,
                                "response": result
                            }
                        }]
                        response = chat.send_message(response_parts)
                    
                    if hasattr(part, 'text'):
                        final_text += part.text
            
            # If no function calls, just get the text
            if not tool_calls and response.text:
                final_text = response.text
            
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