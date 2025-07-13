import axios from 'axios';
import { Vector3, DroneState, DronePosition, DroneAttitude } from '@/types/drone';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_URL = `${API_BASE_URL}/api/v1`;

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 控制接口
const droneAPI = {
  // 解锁
  arm: async () => {
    const response = await api.post('/control/arm');
    return response.data;
  },

  // 锁定
  disarm: async () => {
    const response = await api.post('/control/disarm');
    return response.data;
  },

  // 起飞
  takeoff: async (altitude: number = 10) => {
    const response = await api.post('/control/takeoff', { altitude });
    return response.data;
  },

  // 降落
  land: async () => {
    const response = await api.post('/control/land');
    return response.data;
  },

  // 移动
  move: async (velocity: Vector3, duration?: number) => {
    const response = await api.post('/control/move', { velocity, duration });
    return response.data;
  },

  // 飞往指定位置
  goto: async (position: Vector3, speed: number = 5) => {
    const response = await api.post('/control/goto', { position, speed });
    return response.data;
  },

  // 悬停
  hover: async () => {
    const response = await api.post('/control/hover');
    return response.data;
  },

  // 紧急停止
  emergency: async () => {
    const response = await api.post('/control/emergency');
    return response.data;
  },

  // 获取状态
  getState: async (): Promise<DroneState> => {
    const response = await api.get('/status/state');
    return response.data;
  },

  // 获取位置
  getPosition: async (): Promise<DronePosition> => {
    const response = await api.get('/status/position');
    return response.data;
  },

  // 获取姿态
  getAttitude: async (): Promise<DroneAttitude> => {
    const response = await api.get('/status/attitude');
    return response.data;
  },
};

export default droneAPI; 