"""Tool definitions for Gemini function calling"""

DRONE_TOOLS = [
    {
        "name": "takeoff",
        "description": "让无人机起飞到指定高度",
        "parameters": {
            "type": "object",
            "properties": {
                "altitude": {
                    "type": "number",
                    "description": "目标高度（米），范围 1-100",
                    "minimum": 1,
                    "maximum": 100
                }
            },
            "required": ["altitude"]
        }
    },
    {
        "name": "land",
        "description": "让无人机降落到地面",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "move_to_position",
        "description": "移动无人机到指定的三维坐标位置",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "number",
                    "description": "X坐标（米），相对于起始位置"
                },
                "y": {
                    "type": "number",
                    "description": "Y坐标（米），相对于起始位置"
                },
                "z": {
                    "type": "number",
                    "description": "Z坐标（米），负值表示高度，相对于起始位置"
                },
                "velocity": {
                    "type": "number",
                    "description": "移动速度（米/秒），范围 1-20",
                    "minimum": 1,
                    "maximum": 20,
                    "default": 5
                }
            },
            "required": ["x", "y", "z"]
        }
    },
    {
        "name": "hover",
        "description": "让无人机在当前位置悬停",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_drone_state",
        "description": "获取无人机当前的详细状态信息，包括位置、速度、姿态等",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "emergency_stop",
        "description": "紧急停止无人机的所有动作",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def get_tool_by_name(name: str) -> dict | None:
    """Get tool definition by name"""
    for tool in DRONE_TOOLS:
        if tool["name"] == name:
            return tool
    return None 