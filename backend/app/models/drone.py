from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Vector3(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

class Quaternion(BaseModel):
    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

class DronePosition(BaseModel):
    x: float
    y: float
    z: float
    timestamp: datetime

class DroneAttitude(BaseModel):
    roll: float
    pitch: float
    yaw: float
    timestamp: datetime

class DroneVelocity(BaseModel):
    vx: float
    vy: float
    vz: float

class DroneState(BaseModel):
    position: DronePosition
    attitude: DroneAttitude
    velocity: DroneVelocity
    is_armed: bool = False
    is_flying: bool = False
    battery_level: float = 100.0
    gps_location: Optional[dict] = None
    
class ControlCommand(BaseModel):
    command: str
    parameters: Optional[dict] = {}

class TakeoffCommand(BaseModel):
    altitude: float = 10.0  # 默认起飞高度10米
    
class MoveCommand(BaseModel):
    velocity: Vector3
    duration: Optional[float] = None
    
class GotoCommand(BaseModel):
    position: Vector3
    speed: float = 5.0 