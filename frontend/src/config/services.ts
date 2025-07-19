// Service configuration
export const SERVICES = {
  // Drone control service
  DRONE_API: process.env.NEXT_PUBLIC_DRONE_API || 'http://localhost:8000',
  WS_DRONE: process.env.NEXT_PUBLIC_WS_DRONE || 'ws://localhost:8000/ws',
  
  // AI chat service  
  AI_API: process.env.NEXT_PUBLIC_AI_API || 'http://localhost:8001',
  WS_CHAT: process.env.NEXT_PUBLIC_WS_CHAT || 'ws://localhost:8001',
}

export const API_ENDPOINTS = {
  // Drone control endpoints
  drone: {
    control: {
      arm: '/api/v1/control/arm',
      disarm: '/api/v1/control/disarm',
      takeoff: '/api/v1/control/takeoff',
      land: '/api/v1/control/land',
      move: '/api/v1/control/move',
      hover: '/api/v1/control/hover',
      emergency: '/api/v1/control/emergency_stop',
    },
    status: {
      position: '/api/v1/status/position',
      attitude: '/api/v1/status/attitude',
      state: '/api/v1/status/state',
    }
  },
  
  // AI chat endpoints
  chat: {
    message: '/api/v1/chat/message',
    session: '/api/v1/chat/session',
    ws: '/api/v1/chat/ws',
  }
} 