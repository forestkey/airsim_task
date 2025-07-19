import React from 'react'
import { MessageItem } from './MessageItem'
import { ChatMessage } from '@/src/services/chatService'

export const TestMessageStyles: React.FC = () => {
  const testMessages: ChatMessage[] = [
    {
      role: 'user',
      content: '测试用户消息 - 这应该显示为浅蓝色背景深蓝色文字',
      timestamp: new Date().toISOString(),
    },
    {
      role: 'assistant',
      content: '测试AI消息 - 这应该显示为灰色背景深灰色文字',
      timestamp: new Date().toISOString(),
    },
    {
      role: 'system',
      content: '测试系统消息 - 这应该显示为黄色背景深黄色文字',
      timestamp: new Date().toISOString(),
    },
  ]

  return (
    <div className="p-8 bg-white space-y-4">
      <h2 className="text-xl font-bold mb-4">消息样式测试</h2>
      
      {/* 测试Tailwind类是否工作 */}
      <div className="space-y-2 mb-6">
        <div className="bg-blue-100 text-blue-900 p-2 rounded">
          测试：bg-blue-100 text-blue-900（用户消息样式）
        </div>
        <div className="bg-gray-100 text-gray-800 p-2 rounded">
          测试：bg-gray-100 text-gray-800（AI消息样式）
        </div>
        <div className="bg-yellow-100 text-yellow-800 p-2 rounded">
          测试：bg-yellow-100 text-yellow-800（系统消息样式）
        </div>
      </div>

      {/* 测试实际的MessageItem组件 */}
      <div className="space-y-4 border-t pt-4">
        <h3 className="font-semibold">MessageItem组件测试：</h3>
        {testMessages.map((message, index) => (
          <MessageItem key={index} message={message} />
        ))}
      </div>
    </div>
  )
} 