from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.core.drone_client import drone_client
from app.models.drone import (
    TakeoffCommand, 
    MoveCommand, 
    GotoCommand,
    Vector3
)

router = APIRouter()

@router.post("/arm")
async def arm_drone() -> Dict[str, bool]:
    """解锁无人机"""
    try:
        result = await drone_client.arm()
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/disarm")
async def disarm_drone() -> Dict[str, bool]:
    """锁定无人机"""
    try:
        result = await drone_client.disarm()
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/takeoff")
async def takeoff(command: TakeoffCommand) -> Dict[str, bool]:
    """起飞"""
    try:
        result = await drone_client.takeoff(altitude=command.altitude)
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/land")
async def land() -> Dict[str, bool]:
    """降落"""
    try:
        result = await drone_client.land()
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/move")
async def move(command: MoveCommand) -> Dict[str, bool]:
    """按速度向量移动"""
    try:
        result = await drone_client.move_by_velocity(
            velocity=command.velocity,
            duration=command.duration
        )
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/goto")
async def goto_position(command: GotoCommand) -> Dict[str, bool]:
    """飞往指定位置"""
    try:
        result = await drone_client.move_to_position(
            position=command.position,
            speed=command.speed
        )
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/hover")
async def hover() -> Dict[str, bool]:
    """悬停"""
    try:
        result = await drone_client.hover()
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/emergency")
async def emergency_stop() -> Dict[str, Any]:
    """紧急停止"""
    try:
        result = await drone_client.emergency_stop()
        return {"success": result, "message": "Emergency stop activated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 