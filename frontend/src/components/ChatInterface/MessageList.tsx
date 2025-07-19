import React from 'react'
import { MessageItem } from './MessageItem'
import { ChatMessage } from '@/src/services/chatService'

interface MessageListProps {
  messages: ChatMessage[]
  isLoading?: boolean
}

export const MessageList: React.FC<MessageListProps> = ({ messages, isLoading }) => {
  // Debug log
  console.log('[MessageList] Rendering with messages:', messages.length, messages)
  
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 && (
        <div className="text-center text-gray-500 py-8">
          <p>开始对话，我可以帮你控制无人机</p>
          <p className="text-sm mt-2">
            例如："让无人机起飞到10米高度" 或 "查看无人机状态"
          </p>
        </div>
      )}
      
      {messages.map((message, index) => (
        <MessageItem key={index} message={message} />
      ))}
      
      {isLoading && (
        <div className="flex items-center gap-2 text-gray-500">
          <div className="flex gap-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
          <span className="text-sm">AI 正在处理...</span>
        </div>
      )}
    </div>
  )
} 