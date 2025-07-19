import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class MCPClient:
    """MCP Client for communicating with the drone control service"""
    
    def __init__(self):
        self.base_url = settings.DRONE_SERVICE_URL
        self.auth_token = settings.MCP_AUTH_TOKEN
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.auth_token}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    async def execute_tool(self, tool: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool through MCP protocol"""
        try:
            url = f"{self.base_url}/api/v1/mcp/execute"
            payload = {
                "tool": tool,
                "parameters": parameters
            }
            
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"MCP execution failed: {e}")
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}: {e.response.text}"
            }
        except Exception as e:
            logger.error(f"MCP execution error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_available_tools(self) -> list:
        """Get list of available tools from the drone service"""
        try:
            url = f"{self.base_url}/api/v1/mcp/tools"
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get tools: {e}")
            return []
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Global instance
mcp_client = MCPClient() 