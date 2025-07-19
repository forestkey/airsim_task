'use client';

import React, { useState } from 'react';
import { ChatInterface } from '@/src/components/ChatInterface/ChatInterface';
import { AIAssistantButton } from '@/src/components/ChatInterface/AIAssistantButton';

export default function TestAI() {
  const [showAIChat, setShowAIChat] = useState(false);

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f3f4f6', padding: '20px' }}>
      <h1 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '20px' }}>
        AI助手位置测试页面
      </h1>
      
      <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
        <p>点击右下角的蓝色按钮打开AI助手</p>
        <p>当前状态: {showAIChat ? '已打开' : '已关闭'}</p>
      </div>

      {/* AI助手浮动按钮 */}
      <AIAssistantButton 
        onClick={() => setShowAIChat(!showAIChat)}
        isOpen={showAIChat}
      />

      {/* AI对话控制 */}
      <ChatInterface 
        isVisible={showAIChat}
        onClose={() => setShowAIChat(false)}
      />
    </div>
  );
} 