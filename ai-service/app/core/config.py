from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AirSim AI Chat Service"
    
    # Gemini Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # Drone Service Configuration
    DRONE_SERVICE_URL: str = "http://localhost:8000"
    MCP_AUTH_TOKEN: str = "default-dev-token"  # Must match backend/app/mcp/server.py
    
    # Service Configuration
    AI_SERVICE_PORT: int = 8001
    AI_SERVICE_HOST: str = "0.0.0.0"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000", "http://localhost:8001"]
    
    # Proxy Configuration (optional)
    HTTP_PROXY: Optional[str] = None
    HTTPS_PROXY: Optional[str] = None
    
    # System Prompt
    SYSTEM_PROMPT: str = """你是一个无人机控制助手，可以帮助用户控制 AirSim 中的无人机。

你可以执行以下操作：
- 起飞（takeoff）：让无人机起飞到指定高度
- 降落（land）：让无人机降落
- 移动（move_to_position）：移动无人机到指定位置
- 悬停（hover）：让无人机在当前位置悬停
- 查询状态（get_drone_state）：获取无人机当前状态
- 紧急停止（emergency_stop）：紧急停止无人机

请根据用户的自然语言指令，合理使用工具控制无人机。在执行操作前，请先说明你要做什么。"""

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 