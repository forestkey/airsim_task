import airsim
import asyncio
import numpy as np
from typing import Optional, Dict, Any
from datetime import datetime
import logging

from app.models.drone import DroneState, DronePosition, DroneAttitude, DroneVelocity, Vector3
from app.core.config import settings

logger = logging.getLogger(__name__)

class DroneClient:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self._state_update_task = None
        self._current_state = None
        
    async def connect(self):
        """连接到AirSim"""
        try:
            self.client = airsim.MultirotorClient(
                ip=settings.AIRSIM_IP,
                port=settings.AIRSIM_PORT
            )
            self.client.confirmConnection()
            self.client.enableApiControl(True)
            self.is_connected = True
            logger.info("Successfully connected to AirSim")
            
            # 启动状态更新任务
            self._state_update_task = asyncio.create_task(self._update_state_loop())
            return True
        except Exception as e:
            logger.error(f"Failed to connect to AirSim: {e}")
            self.is_connected = False
            return False
    
    async def disconnect(self):
        """断开连接"""
        if self._state_update_task:
            self._state_update_task.cancel()
        
        if self.client and self.is_connected:
            self.client.enableApiControl(False)
            self.client.armDisarm(False)
        self.is_connected = False
        logger.info("Disconnected from AirSim")
    
    async def arm(self):
        """解锁无人机"""
        if not self.is_connected:
            raise Exception("Not connected to AirSim")
        
        self.client.armDisarm(True)
        await asyncio.sleep(0.1)
        return True
    
    async def disarm(self):
        """锁定无人机"""
        if not self.is_connected:
            raise Exception("Not connected to AirSim")
        
        self.client.armDisarm(False)
        return True
    
    async def takeoff(self, altitude: float = 10.0):
        """起飞到指定高度"""
        if not self.is_connected:
            raise Exception("Not connected to AirSim")
        
        # 安全检查
        if altitude > settings.MAX_ALTITUDE:
            altitude = settings.MAX_ALTITUDE
            
        await self.arm()
        await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: self.client.takeoffAsync(timeout_sec=10).join()
        )
        
        # 移动到目标高度
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.client.moveToZAsync(-altitude, 3).join()
        )
        return True
    
    async def land(self):
        """降落"""
        if not self.is_connected:
            raise Exception("Not connected to AirSim")
        
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.client.landAsync(timeout_sec=30).join()
        )
        return True
    
    async def move_by_velocity(self, velocity: Vector3, duration: Optional[float] = 1.0):
        """按速度向量移动"""
        if not self.is_connected:
            raise Exception("Not connected to AirSim")
        
        # 速度限制
        speed = np.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2)
        if speed > settings.MAX_SPEED:
            factor = settings.MAX_SPEED / speed
            velocity.x *= factor
            velocity.y *= factor
            velocity.z *= factor
        
        self.client.moveByVelocityAsync(
            velocity.x, velocity.y, velocity.z,
            duration if duration else 1.0
        )
        return True
    
    async def move_to_position(self, position: Vector3, speed: float = 5.0):
        """移动到指定位置"""
        if not self.is_connected:
            raise Exception("Not connected to AirSim")
        
        # 速度限制
        speed = min(speed, settings.MAX_SPEED)
        
        # 地理围栏检查
        distance = np.sqrt(position.x**2 + position.y**2)
        if distance > settings.GEOFENCE_RADIUS:
            raise Exception(f"Position outside geofence radius: {distance:.2f}m")
        
        # 高度限制
        if abs(position.z) > settings.MAX_ALTITUDE:
            position.z = -settings.MAX_ALTITUDE if position.z < 0 else settings.MAX_ALTITUDE
        
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.client.moveToPositionAsync(
                position.x, position.y, position.z, speed
            ).join()
        )
        return True
    
    async def hover(self):
        """悬停"""
        if not self.is_connected:
            raise Exception("Not connected to AirSim")
        
        self.client.hoverAsync()
        return True
    
    async def emergency_stop(self):
        """紧急停止"""
        if not self.is_connected:
            return True
        
        try:
            # 取消所有任务
            self.client.cancelLastTask()
            # 悬停
            await self.hover()
            # 降落
            await self.land()
        except Exception as e:
            logger.error(f"Emergency stop error: {e}")
            # 强制断开
            self.client.reset()
        return True
    
    async def get_state(self) -> DroneState:
        """获取无人机状态"""
        if not self.is_connected or not self._current_state:
            raise Exception("Not connected to AirSim or no state available")
        
        return self._current_state
    
    async def _update_state_loop(self):
        """状态更新循环"""
        while self.is_connected:
            try:
                state = self.client.getMultirotorState()
                
                # 位置
                pos = state.kinematics_estimated.position
                position = DronePosition(
                    x=pos.x_val,
                    y=pos.y_val,
                    z=pos.z_val,
                    timestamp=datetime.now()
                )
                
                # 姿态
                orientation = state.kinematics_estimated.orientation
                pitch, roll, yaw = airsim.to_eularian_angles(orientation)
                attitude = DroneAttitude(
                    roll=np.degrees(roll),
                    pitch=np.degrees(pitch),
                    yaw=np.degrees(yaw),
                    timestamp=datetime.now()
                )
                
                # 速度
                vel = state.kinematics_estimated.linear_velocity
                velocity = DroneVelocity(
                    vx=vel.x_val,
                    vy=vel.y_val,
                    vz=vel.z_val
                )
                
                # GPS位置
                gps_data = None
                if hasattr(state, 'gps_location'):
                    gps = state.gps_location
                    gps_data = {
                        "latitude": gps.latitude,
                        "longitude": gps.longitude,
                        "altitude": gps.altitude
                    }
                
                # 电池（模拟）
                battery = 100.0  # AirSim不提供电池信息，这里模拟
                
                self._current_state = DroneState(
                    position=position,
                    attitude=attitude,
                    velocity=velocity,
                    is_armed=state.landed_state == airsim.LandedState.Flying,
                    is_flying=state.landed_state == airsim.LandedState.Flying,
                    battery_level=battery,
                    gps_location=gps_data
                )
                
                await asyncio.sleep(settings.WS_MESSAGE_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error updating state: {e}")
                await asyncio.sleep(1)

# 全局实例
drone_client = DroneClient() 