import { TelemetryData } from '@/types/drone';

/**
 * 创建一个带有默认值的 TelemetryData 对象
 */
export const createDefaultTelemetry = (): TelemetryData => ({
  position: { x: 0, y: 0, z: 0 },
  attitude: { roll: 0, pitch: 0, yaw: 0 },
  velocity: { vx: 0, vy: 0, vz: 0 },
  is_armed: false,
  is_flying: false,
  battery_level: 0,
  gps_location: null,
  timestamp: new Date().toISOString(),
  is_connected: false,
});

/**
 * 安全地获取 telemetry 数据，如果数据不完整则返回默认值
 */
export const safeTelemetry = (telemetry: TelemetryData | null): TelemetryData => {
  if (!telemetry) {
    return createDefaultTelemetry();
  }

  return {
    position: telemetry.position || { x: 0, y: 0, z: 0 },
    attitude: telemetry.attitude || { roll: 0, pitch: 0, yaw: 0 },
    velocity: telemetry.velocity || { vx: 0, vy: 0, vz: 0 },
    is_armed: telemetry.is_armed ?? false,
    is_flying: telemetry.is_flying ?? false,
    battery_level: telemetry.battery_level ?? 0,
    gps_location: telemetry.gps_location || null,
    timestamp: telemetry.timestamp || new Date().toISOString(),
    is_connected: telemetry.is_connected ?? false,
    error: telemetry.error,
  };
};

/**
 * 检查 telemetry 数据是否有效（包含所有必需的嵌套属性）
 */
export const isValidTelemetry = (telemetry: TelemetryData | null): boolean => {
  return !!(
    telemetry &&
    telemetry.position &&
    telemetry.attitude &&
    telemetry.velocity &&
    typeof telemetry.position.x === 'number' &&
    typeof telemetry.position.y === 'number' &&
    typeof telemetry.position.z === 'number'
  );
};

/**
 * 计算速度大小
 */
export const calculateSpeed = (telemetry: TelemetryData | null): number => {
  if (!telemetry?.velocity) return 0;
  
  return Math.sqrt(
    telemetry.velocity.vx ** 2 +
    telemetry.velocity.vy ** 2 +
    telemetry.velocity.vz ** 2
  );
}; 