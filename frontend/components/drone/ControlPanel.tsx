import React, { useState } from 'react';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';
import droneAPI from '@/lib/api/drone';
import { 
  Play, 
  Square, 
  ChevronUp, 
  ChevronDown, 
  RotateCw, 
  RotateCcw,
  MoveUp,
  MoveDown,
  AlertTriangle,
  Pause
} from 'lucide-react';

interface ControlPanelProps {
  isConnected: boolean;
  isFlying: boolean;
  onStatusChange?: () => void;
}

export const ControlPanel: React.FC<ControlPanelProps> = ({ 
  isConnected, 
  isFlying,
  onStatusChange 
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [altitude, setAltitude] = useState(10);
  const [speed, setSpeed] = useState(5);

  const handleCommand = async (command: () => Promise<any>, successMsg?: string) => {
    if (!isConnected) {
      alert('无人机未连接');
      return;
    }

    setIsLoading(true);
    try {
      await command();
      if (successMsg) {
        console.log(successMsg);
      }
      onStatusChange?.();
    } catch (error) {
      console.error('Command failed:', error);
      alert('命令执行失败');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTakeoff = () => {
    handleCommand(
      () => droneAPI.takeoff(altitude),
      '起飞成功'
    );
  };

  const handleLand = () => {
    handleCommand(
      () => droneAPI.land(),
      '降落成功'
    );
  };

  const handleMove = (velocity: { x: number; y: number; z: number }) => {
    handleCommand(
      () => droneAPI.move(velocity, 1),
      '移动命令已发送'
    );
  };

  const handleEmergency = () => {
    if (window.confirm('确定要执行紧急停止吗？')) {
      handleCommand(
        () => droneAPI.emergency(),
        '紧急停止已执行'
      );
    }
  };

  return (
    <Card title="飞行控制" className="w-full">
      <div className="space-y-6">
        {/* 基础控制 */}
        <div className="flex gap-4">
          <Button
            variant={isFlying ? 'secondary' : 'primary'}
            size="lg"
            onClick={handleTakeoff}
            disabled={isLoading || isFlying || !isConnected}
            className="flex-1"
          >
            <Play className="w-5 h-5 mr-2" />
            起飞
          </Button>
          <Button
            variant="secondary"
            size="lg"
            onClick={handleLand}
            disabled={isLoading || !isFlying || !isConnected}
            className="flex-1"
          >
            <Square className="w-5 h-5 mr-2" />
            降落
          </Button>
        </div>

        {/* 高度控制 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            起飞高度: {altitude}米
          </label>
          <input
            type="range"
            min="5"
            max="50"
            value={altitude}
            onChange={(e) => setAltitude(Number(e.target.value))}
            className="w-full"
            disabled={isFlying}
          />
        </div>

        {/* 方向控制 */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">方向控制</h4>
          <div className="grid grid-cols-3 gap-2">
            <div />
            <Button
              variant="secondary"
              onClick={() => handleMove({ x: speed, y: 0, z: 0 })}
              disabled={isLoading || !isFlying}
            >
              <ChevronUp className="w-5 h-5" />
            </Button>
            <div />
            
            <Button
              variant="secondary"
              onClick={() => handleMove({ x: 0, y: -speed, z: 0 })}
              disabled={isLoading || !isFlying}
            >
              <RotateCcw className="w-5 h-5" />
            </Button>
            <Button
              variant="secondary"
              onClick={() => droneAPI.hover()}
              disabled={isLoading || !isFlying}
            >
              <Pause className="w-5 h-5" />
            </Button>
            <Button
              variant="secondary"
              onClick={() => handleMove({ x: 0, y: speed, z: 0 })}
              disabled={isLoading || !isFlying}
            >
              <RotateCw className="w-5 h-5" />
            </Button>
            
            <div />
            <Button
              variant="secondary"
              onClick={() => handleMove({ x: -speed, y: 0, z: 0 })}
              disabled={isLoading || !isFlying}
            >
              <ChevronDown className="w-5 h-5" />
            </Button>
            <div />
          </div>
        </div>

        {/* 高度调整 */}
        <div className="flex gap-4">
          <Button
            variant="secondary"
            onClick={() => handleMove({ x: 0, y: 0, z: -speed })}
            disabled={isLoading || !isFlying}
            className="flex-1"
          >
            <MoveUp className="w-5 h-5 mr-2" />
            上升
          </Button>
          <Button
            variant="secondary"
            onClick={() => handleMove({ x: 0, y: 0, z: speed })}
            disabled={isLoading || !isFlying}
            className="flex-1"
          >
            <MoveDown className="w-5 h-5 mr-2" />
            下降
          </Button>
        </div>

        {/* 速度控制 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            移动速度: {speed}米/秒
          </label>
          <input
            type="range"
            min="1"
            max="20"
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
            className="w-full"
          />
        </div>

        {/* 紧急停止 */}
        <Button
          variant="danger"
          size="lg"
          onClick={handleEmergency}
          disabled={isLoading || !isConnected}
          className="w-full"
        >
          <AlertTriangle className="w-5 h-5 mr-2" />
          紧急停止
        </Button>
      </div>
    </Card>
  );
}; 