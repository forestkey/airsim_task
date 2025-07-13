from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.drone_client import drone_client
from app.api import control, status

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("Starting AirSim Drone Control Service...")
    await drone_client.connect()
    yield
    # 关闭时
    logger.info("Shutting down AirSim Drone Control Service...")
    await drone_client.disconnect()

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(
    control.router,
    prefix=f"{settings.API_V1_STR}/control",
    tags=["control"]
)

app.include_router(
    status.router,
    prefix=f"{settings.API_V1_STR}/status",
    tags=["status"]
)

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AirSim Drone Control Service",
        "version": "1.0.0",
        "status": "running",
        "drone_connected": drone_client.is_connected
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "drone_connected": drone_client.is_connected
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 