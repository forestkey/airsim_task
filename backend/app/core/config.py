from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # API配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AirSim Drone Control Service"
    
    # AirSim连接配置
    AIRSIM_IP: str = "127.0.0.1"
    AIRSIM_PORT: int = 41451
    
    # WebSocket配置
    WS_MESSAGE_INTERVAL: float = 0.1  # 100ms
    
    # 安全限制
    MAX_ALTITUDE: float = 100.0  # 最大高度(米)
    MAX_SPEED: float = 20.0      # 最大速度(米/秒)
    GEOFENCE_RADIUS: float = 500.0  # 地理围栏半径(米)
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 