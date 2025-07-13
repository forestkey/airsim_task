import React from 'react';
import { Card } from '../ui/Card';
import { TelemetryData } from '@/types/drone';
import { 
  Navigation,
  Battery,
  Wifi,
  WifiOff,
  MapPin,
  Activity,
  Compass,
  Gauge
} from 'lucide-react';

interface StatusDisplayProps {
  telemetry: TelemetryData | null;
  isConnected: boolean;
}

export const StatusDisplay: React.FC<StatusDisplayProps> = ({ telemetry, isConnected }) => {
  const formatNumber = (num: number, decimals: number = 2) => {
    return num.toFixed(decimals);
  };

  return (
    <div className="space-y-4">
      {/* 连接状态 */}
      <Card className="p-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700">连接状态</span>
          <div className="flex items-center gap-2">
            {isConnected ? (
              <>
                <Wifi className="w-4 h-4 text-success" />
                <span className="text-sm text-success">已连接</span>
              </>
            ) : (
              <>
                <WifiOff className="w-4 h-4 text-danger" />
                <span className="text-sm text-danger">未连接</span>
              </>
            )}
          </div>
        </div>
      </Card>

      {/* 位置信息 */}
      <Card title="位置信息">
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4 text-gray-500" />
              <span className="text-sm text-gray-600">位置</span>
            </div>
            <div className="text-sm font-mono">
              {telemetry ? (
                <>
                  X: {formatNumber(telemetry.position.x)}m, 
                  Y: {formatNumber(telemetry.position.y)}m, 
                  Z: {formatNumber(telemetry.position.z)}m
                </>
              ) : (
                <span className="text-gray-400">--</span>
              )}
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Gauge className="w-4 h-4 text-gray-500" />
              <span className="text-sm text-gray-600">高度</span>
            </div>
            <div className="text-sm font-mono">
              {telemetry ? `${formatNumber(Math.abs(telemetry.position.z))}m` : '--'}
            </div>
          </div>
        </div>
      </Card>

      {/* 姿态信息 */}
      <Card title="姿态信息">
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Roll</span>
            <span className="text-sm font-mono">
              {telemetry ? `${formatNumber(telemetry.attitude.roll)}°` : '--'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Pitch</span>
            <span className="text-sm font-mono">
              {telemetry ? `${formatNumber(telemetry.attitude.pitch)}°` : '--'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Yaw</span>
            <span className="text-sm font-mono">
              {telemetry ? `${formatNumber(telemetry.attitude.yaw)}°` : '--'}
            </span>
          </div>
        </div>
      </Card>

      {/* 速度信息 */}
      <Card title="速度信息">
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-gray-500" />
              <span className="text-sm text-gray-600">速度</span>
            </div>
            <div className="text-sm font-mono">
              {telemetry ? (
                <>
                  {formatNumber(Math.sqrt(
                    telemetry.velocity.vx ** 2 + 
                    telemetry.velocity.vy ** 2 + 
                    telemetry.velocity.vz ** 2
                  ))} m/s
                </>
              ) : (
                <span className="text-gray-400">--</span>
              )}
            </div>
          </div>

          <div className="text-xs text-gray-500 font-mono">
            {telemetry && (
              <>
                Vx: {formatNumber(telemetry.velocity.vx, 1)} 
                Vy: {formatNumber(telemetry.velocity.vy, 1)} 
                Vz: {formatNumber(telemetry.velocity.vz, 1)}
              </>
            )}
          </div>
        </div>
      </Card>

      {/* 状态信息 */}
      <Card title="飞行状态">
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">解锁状态</span>
            <span className={`text-sm font-medium ${telemetry?.is_armed ? 'text-success' : 'text-gray-400'}`}>
              {telemetry?.is_armed ? '已解锁' : '未解锁'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">飞行状态</span>
            <span className={`text-sm font-medium ${telemetry?.is_flying ? 'text-success' : 'text-gray-400'}`}>
              {telemetry?.is_flying ? '飞行中' : '地面'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Battery className="w-4 h-4 text-gray-500" />
              <span className="text-sm text-gray-600">电池</span>
            </div>
            <span className={`text-sm font-medium ${
              telemetry && telemetry.battery_level < 20 ? 'text-danger' : 
              telemetry && telemetry.battery_level < 50 ? 'text-warning' : 
              'text-success'
            }`}>
              {telemetry ? `${formatNumber(telemetry.battery_level, 0)}%` : '--'}
            </span>
          </div>
        </div>
      </Card>

      {/* GPS信息 */}
      {telemetry?.gps_location && (
        <Card title="GPS信息">
          <div className="space-y-2 text-xs font-mono">
            <div>纬度: {formatNumber(telemetry.gps_location.latitude, 6)}°</div>
            <div>经度: {formatNumber(telemetry.gps_location.longitude, 6)}°</div>
            <div>海拔: {formatNumber(telemetry.gps_location.altitude)}m</div>
          </div>
        </Card>
      )}
    </div>
  );
}; 