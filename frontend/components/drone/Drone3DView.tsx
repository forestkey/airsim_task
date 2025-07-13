import React, { useEffect, useRef } from 'react';
import { Card } from '../ui/Card';
import { TelemetryData } from '@/types/drone';

interface Drone3DViewProps {
  telemetry: TelemetryData | null;
}

export const Drone3DView: React.FC<Drone3DViewProps> = ({ telemetry }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current || !telemetry) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Draw ground grid
    ctx.strokeStyle = '#e5e5e5';
    ctx.lineWidth = 1;
    const gridSize = 20;
    const gridCount = 10;

    for (let i = -gridCount; i <= gridCount; i++) {
      // Vertical lines
      ctx.beginPath();
      ctx.moveTo(centerX + i * gridSize, 0);
      ctx.lineTo(centerX + i * gridSize, canvas.height);
      ctx.stroke();

      // Horizontal lines
      ctx.beginPath();
      ctx.moveTo(0, centerY + i * gridSize);
      ctx.lineTo(canvas.width, centerY + i * gridSize);
      ctx.stroke();
    }

    // Draw drone position
    const scale = 2; // Scale factor for visualization
    const droneX = centerX + telemetry.position.x * scale;
    const droneY = centerY - telemetry.position.y * scale;
    const droneZ = -telemetry.position.z * scale;

    // Draw altitude indicator
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(droneX, centerY);
    ctx.lineTo(droneX, droneY);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw drone shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.beginPath();
    ctx.ellipse(droneX, centerY, 15 + droneZ / 10, 8 + droneZ / 20, 0, 0, Math.PI * 2);
    ctx.fill();

    // Draw drone body
    const droneSize = 20;
    ctx.save();
    ctx.translate(droneX, droneY);
    ctx.rotate(telemetry.attitude.yaw);

    // Draw drone arms
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 4;
    const armLength = droneSize;
    
    // X configuration
    ctx.beginPath();
    ctx.moveTo(-armLength, -armLength);
    ctx.lineTo(armLength, armLength);
    ctx.moveTo(-armLength, armLength);
    ctx.lineTo(armLength, -armLength);
    ctx.stroke();

    // Draw motors
    const motorSize = 8;
    ctx.fillStyle = '#1f2937';
    [-1, 1].forEach(x => {
      [-1, 1].forEach(y => {
        ctx.beginPath();
        ctx.arc(x * armLength, y * armLength, motorSize, 0, Math.PI * 2);
        ctx.fill();
      });
    });

    // Draw drone center
    ctx.fillStyle = telemetry.is_armed ? '#10b981' : '#6b7280';
    ctx.beginPath();
    ctx.arc(0, 0, 6, 0, Math.PI * 2);
    ctx.fill();

    // Draw direction indicator
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, -droneSize);
    ctx.stroke();

    ctx.restore();

    // Draw altitude text
    ctx.fillStyle = '#374151';
    ctx.font = '14px monospace';
    ctx.fillText(`高度: ${(-telemetry.position.z).toFixed(1)}m`, 10, 20);
    ctx.fillText(`航向: ${(telemetry.attitude.yaw * 180 / Math.PI).toFixed(0)}°`, 10, 40);

  }, [telemetry]);

  return (
    <Card title="3D视图" className="h-full">
      <div className="relative h-80">
        <canvas
          ref={canvasRef}
          className="w-full h-full border border-gray-200 rounded"
        />
        
        {/* Legend */}
        <div className="absolute bottom-2 right-2 bg-white/90 p-2 rounded text-xs">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span>已解锁</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-gray-500 rounded-full"></div>
            <span>已锁定</span>
          </div>
        </div>

        {/* Coordinates */}
        {telemetry && (
          <div className="absolute top-2 left-2 bg-white/90 p-2 rounded text-xs font-mono">
            <div>X: {telemetry.position.x.toFixed(2)}m</div>
            <div>Y: {telemetry.position.y.toFixed(2)}m</div>
            <div>Z: {telemetry.position.z.toFixed(2)}m</div>
          </div>
        )}
      </div>
    </Card>
  );
}; 