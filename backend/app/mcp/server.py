from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.core.drone_client import drone_client
from app.models.drone import Vector3, DroneState
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# MCP Request/Response models
class MCPRequest(BaseModel):
    tool: str
    parameters: Dict[str, Any]

class MCPResponse(BaseModel):
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Tool definitions (matching AI service)
AVAILABLE_TOOLS = {
    "takeoff": {
        "description": "Take off to specified altitude",
        "handler": "handle_takeoff"
    },
    "land": {
        "description": "Land the drone",
        "handler": "handle_land"
    },
    "move_to_position": {
        "description": "Move to specified position",
        "handler": "handle_move_to_position"
    },
    "hover": {
        "description": "Hover at current position",
        "handler": "handle_hover"
    },
    "get_drone_state": {
        "description": "Get current drone state",
        "handler": "handle_get_state"
    },
    "emergency_stop": {
        "description": "Emergency stop",
        "handler": "handle_emergency_stop"
    }
}

# Simple authentication check
async def verify_mcp_token(authorization: str = Header(...)) -> bool:
    """Verify MCP auth token"""
    # In production, use proper token validation
    expected_token = "Bearer default-dev-token"
    if authorization != expected_token:
        raise HTTPException(status_code=401, detail="Invalid MCP token")
    return True

# Tool handlers
async def handle_takeoff(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle takeoff command"""
    altitude = params.get("altitude", 10)
    if altitude < 1 or altitude > 100:
        raise ValueError("Altitude must be between 1 and 100 meters")
    
    # Use the built-in takeoff method which handles altitude
    await drone_client.takeoff(altitude)
    
    return {"message": f"Takeoff to {altitude}m completed"}

async def handle_land(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle land command"""
    await drone_client.land()
    return {"message": "Landing completed"}

async def handle_move_to_position(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle move to position command"""
    x = params.get("x", 0)
    y = params.get("y", 0)
    z = params.get("z", -10)
    velocity = params.get("velocity", 5)
    
    # Create Vector3 position
    position = Vector3(x=x, y=y, z=z)
    await drone_client.move_to_position(position, velocity)
    
    return {
        "message": f"Moved to position ({x}, {y}, {z})",
        "position": {"x": x, "y": y, "z": z}
    }

async def handle_hover(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle hover command"""
    await drone_client.hover()
    return {"message": "Hovering at current position"}

async def handle_get_state(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get state command"""
    state = await drone_client.get_state()
    return {"state": state}

async def handle_emergency_stop(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle emergency stop command"""
    await drone_client.emergency_stop()
    return {"message": "Emergency stop executed"}

# Main MCP endpoints
@router.post("/execute", response_model=MCPResponse, dependencies=[Depends(verify_mcp_token)])
async def execute_tool(request: MCPRequest):
    """Execute a tool through MCP protocol"""
    try:
        tool_name = request.tool
        parameters = request.parameters
        
        if tool_name not in AVAILABLE_TOOLS:
            return MCPResponse(
                success=False,
                error=f"Unknown tool: {tool_name}"
            )
        
        # Get handler function
        handler_name = AVAILABLE_TOOLS[tool_name]["handler"]
        handler = globals().get(handler_name)
        
        if not handler:
            return MCPResponse(
                success=False,
                error=f"Handler not found for tool: {tool_name}"
            )
        
        # Execute tool
        result = await handler(parameters)
        
        return MCPResponse(
            success=True,
            result=result
        )
        
    except Exception as e:
        logger.error(f"MCP execution error: {e}")
        return MCPResponse(
            success=False,
            error=str(e)
        )

@router.get("/tools", dependencies=[Depends(verify_mcp_token)])
async def get_available_tools():
    """Get list of available tools"""
    tools = []
    for name, info in AVAILABLE_TOOLS.items():
        tools.append({
            "name": name,
            "description": info["description"]
        })
    return tools 