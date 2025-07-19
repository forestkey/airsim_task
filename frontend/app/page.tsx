'use client';

import React, { useEffect, useState } from 'react';
import { ControlPanel } from '@/components/drone/ControlPanel';
import { StatusDisplay } from '@/components/drone/StatusDisplay';
import { TelemetryChart } from '@/components/drone/TelemetryChart';
import { Drone3DView } from '@/components/drone/Drone3DView';
import { ChatInterface } from '@/src/components/ChatInterface/ChatInterface';
import { AIAssistantButton } from '@/src/components/ChatInterface/AIAssistantButton';
import { useWebSocket } from '@/lib/hooks/useWebSocket';
import { Plane } from 'lucide-react';

export default function Home() {
  const { telemetry, isConnected } = useWebSocket();
  const [isFlying, setIsFlying] = useState(false);
  const [showAIChat, setShowAIChat] = useState(false);

  useEffect(() => {
    if (telemetry) {
      setIsFlying(telemetry.is_flying);
    }
  }, [telemetry]);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* 顶部导航栏 */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <Plane className="w-8 h-8 text-primary-600" />
              <h1 className="text-xl font-bold text-gray-900">
                AirSim 无人机控制中心
              </h1>
            </div>
            <div className="flex items-center gap-2">
              <div className={`h-3 w-3 rounded-full ${isConnected ? 'bg-success' : 'bg-danger'} animate-pulse`} />
              <span className="text-sm text-gray-600">
                {isConnected ? '系统正常' : '等待连接'}
              </span>
            </div>
          </div>
        </div>
      </nav>

      {/* 主内容区 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 控制面板 - 占据左侧1/3 */}
          <div className="lg:col-span-1">
            <ControlPanel 
              isConnected={isConnected}
              isFlying={isFlying}
              onStatusChange={() => {
                // 刷新状态
              }}
            />
          </div>

          {/* 状态和可视化 - 占据右侧2/3 */}
          <div className="lg:col-span-2 space-y-6">
            <StatusDisplay 
              telemetry={telemetry}
              isConnected={isConnected}
            />
            
            {/* 数据可视化区域 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Drone3DView telemetry={telemetry} />
              <TelemetryChart telemetry={telemetry} />
            </div>
          </div>
        </div>

        {/* 底部信息 */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>请确保AirSim仿真器已启动并正确配置</p>
          <p className="mt-1">
            API服务地址: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
          </p>
        </div>
      </main>

      {/* AI助手浮动按钮 */}
      <AIAssistantButton 
        onClick={() => setShowAIChat(!showAIChat)}
        isOpen={showAIChat}
      />

      {/* AI对话控制 - 条件渲染 */}
      <ChatInterface 
        isVisible={showAIChat}
        onClose={() => setShowAIChat(false)}
      />
    </div>
  );
} 