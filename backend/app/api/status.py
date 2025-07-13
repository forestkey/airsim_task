from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict
import asyncio
import json

from app.core.drone_client import drone_client
from app.core.websocket import manager
from app.models.drone import DroneState, DronePosition, DroneAttitude

router = APIRouter()

@router.get("/position")
async def get_position() -> DronePosition:
    """获取无人机位置"""
    try:
        state = await drone_client.get_state()
        return state.position
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/attitude")
async def get_attitude() -> DroneAttitude:
    """获取无人机姿态"""
    try:
        state = await drone_client.get_state()
        return state.attitude
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/state")
async def get_state() -> DroneState:
    """获取无人机完整状态"""
    try:
        state = await drone_client.get_state()
        return state
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket连接端点，用于实时推送无人机状态"""
    await manager.connect(websocket)
    try:
        # 启动状态推送任务
        async def send_telemetry():
            while True:
                try:
                    if drone_client.is_connected:
                        state = await drone_client.get_state()
                        # 转换为可序列化的格式
                        data = {
                            "timestamp": state.position.timestamp.isoformat(),
                            "position": {
                                "x": state.position.x,
                                "y": state.position.y,
                                "z": state.position.z
                            },
                            "attitude": {
                                "roll": state.attitude.roll,
                                "pitch": state.attitude.pitch,
                                "yaw": state.attitude.yaw
                            },
                            "velocity": {
                                "vx": state.velocity.vx,
                                "vy": state.velocity.vy,
                                "vz": state.velocity.vz
                            },
                            "is_armed": state.is_armed,
                            "is_flying": state.is_flying,
                            "battery_level": state.battery_level,
                            "gps_location": state.gps_location
                        }
                        await websocket.send_json(data)
                    else:
                        await websocket.send_json({
                            "error": "Drone not connected",
                            "is_connected": False
                        })
                    
                    await asyncio.sleep(0.1)  # 10Hz更新频率
                except Exception as e:
                    print(f"Error sending telemetry: {e}")
                    break
        
        # 创建任务
        telemetry_task = asyncio.create_task(send_telemetry())
        
        # 保持连接
        while True:
            data = await websocket.receive_text()
            # 可以在这里处理客户端发来的消息
            if data == "ping":
                await websocket.send_text("pong")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        telemetry_task.cancel()
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
        telemetry_task.cancel() 