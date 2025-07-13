export interface Vector3 {
  x: number;
  y: number;
  z: number;
}

export interface DronePosition {
  x: number;
  y: number;
  z: number;
  timestamp: string;
}

export interface DroneAttitude {
  roll: number;
  pitch: number;
  yaw: number;
  timestamp: string;
}

export interface DroneVelocity {
  vx: number;
  vy: number;
  vz: number;
}

export interface GPSLocation {
  latitude: number;
  longitude: number;
  altitude: number;
}

export interface DroneState {
  position: Omit<DronePosition, 'timestamp'>;
  attitude: Omit<DroneAttitude, 'timestamp'>;
  velocity: DroneVelocity;
  is_armed: boolean;
  is_flying: boolean;
  battery_level: number;
  gps_location: GPSLocation | null;
  timestamp: string;
}

export interface TelemetryData extends DroneState {
  error?: string;
  is_connected?: boolean;
}

export interface ControlCommand {
  command: string;
  parameters?: Record<string, any>;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
} 