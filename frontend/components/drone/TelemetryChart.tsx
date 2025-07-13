import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card } from '../ui/Card';
import { TelemetryData } from '@/types/drone';

interface TelemetryChartProps {
  telemetry: TelemetryData | null;
  maxDataPoints?: number;
}

interface ChartData {
  time: string;
  altitude: number;
  velocity: number;
  battery: number;
}

export const TelemetryChart: React.FC<TelemetryChartProps> = ({ 
  telemetry, 
  maxDataPoints = 50 
}) => {
  const [data, setData] = useState<ChartData[]>([]);

  useEffect(() => {
    if (!telemetry) return;

    const newDataPoint: ChartData = {
      time: new Date().toLocaleTimeString(),
      altitude: -telemetry.position.z, // AirSim uses NED coordinates
      velocity: Math.sqrt(
        telemetry.velocity.vx ** 2 + 
        telemetry.velocity.vy ** 2 + 
        telemetry.velocity.vz ** 2
      ),
      battery: telemetry.battery_level
    };

    setData(prevData => {
      const newData = [...prevData, newDataPoint];
      // Keep only the last maxDataPoints
      return newData.slice(-maxDataPoints);
    });
  }, [telemetry, maxDataPoints]);

  return (
    <Card title="遥测数据" className="h-full">
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '1px solid #ccc',
                borderRadius: '4px'
              }}
            />
            <Legend 
              wrapperStyle={{ fontSize: '14px' }}
              iconType="line"
            />
            <Line 
              type="monotone" 
              dataKey="altitude" 
              stroke="#3b82f6" 
              name="高度(m)"
              strokeWidth={2}
              dot={false}
              animationDuration={0}
            />
            <Line 
              type="monotone" 
              dataKey="velocity" 
              stroke="#10b981" 
              name="速度(m/s)"
              strokeWidth={2}
              dot={false}
              animationDuration={0}
            />
            <Line 
              type="monotone" 
              dataKey="battery" 
              stroke="#f59e0b" 
              name="电量(%)"
              strokeWidth={2}
              dot={false}
              animationDuration={0}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      
      {/* 实时数据显示 */}
      {telemetry && (
        <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t">
          <div className="text-center">
            <p className="text-sm text-gray-600">当前高度</p>
            <p className="text-lg font-semibold text-blue-600">
              {(-telemetry.position.z).toFixed(1)} m
            </p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600">当前速度</p>
            <p className="text-lg font-semibold text-green-600">
              {Math.sqrt(
                telemetry.velocity.vx ** 2 + 
                telemetry.velocity.vy ** 2 + 
                telemetry.velocity.vz ** 2
              ).toFixed(1)} m/s
            </p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600">电池电量</p>
            <p className="text-lg font-semibold text-yellow-600">
              {telemetry.battery_level.toFixed(0)}%
            </p>
          </div>
        </div>
      )}
    </Card>
  );
}; 