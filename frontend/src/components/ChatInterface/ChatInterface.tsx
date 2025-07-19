'use client'

import React, { useState, useEffect, useRef } from 'react'
import { MessageList } from './MessageList'
import { MessageInput } from './MessageInput'
import { chatService, ChatMessage } from '@/src/services/chatService'
import { Button } from '../../../components/ui/Button'
import { Trash2, Minimize2, Maximize2 } from 'lucide-react'
import '@/src/styles/chat.css'

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [isMinimized, setIsMinimized] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Connect to WebSocket
    chatService.connectWebSocket(
      (data: any) => {
        if (data.type === 'connected') {
          setIsConnected(true)
        } else if (data.type === 'ai_reply') {
          const aiMessage: ChatMessage = {
            role: 'assistant',
            content: data.data.reply,
            timestamp: new Date().toISOString(),
            tool_calls: data.data.tool_calls,
          }
          setMessages(prev => [...prev, aiMessage])
          setIsLoading(false)
        } else if (data.type === 'status_update') {
          // Handle status updates if needed
          console.log('Status update:', data.data)
        }
      },
      (error) => {
        console.error('WebSocket error:', error)
        setIsConnected(false)
      },
      () => {
        setIsConnected(false)
      }
    )

    // 临时解决方案：立即设置连接状态
    // TODO: 等后端实现发送 'connected' 消息后可以移除这行
    setIsConnected(true)

    return () => {
      chatService.disconnectWebSocket()
    }
  }, [])

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return

    // Add user message
    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      if (chatService.isWebSocketConnected()) {
        // Use WebSocket for real-time communication
        chatService.sendWebSocketMessage(content)
      } else {
        // Fallback to HTTP API
        const response = await chatService.sendMessage(content)
        const aiMessage: ChatMessage = {
          role: 'assistant',
          content: response.reply,
          timestamp: response.timestamp,
          tool_calls: response.tool_calls,
        }
        setMessages(prev => [...prev, aiMessage])
        setIsLoading(false)
      }
    } catch (error) {
      console.error('Failed to send message:', error)
      setIsLoading(false)
      // Add error message
      const errorMessage: ChatMessage = {
        role: 'system',
        content: '抱歉，发送消息时出现错误。请稍后重试。',
        timestamp: new Date().toISOString(),
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const handleClearChat = async () => {
    setMessages([])
    await chatService.clearSession()
  }

  if (isMinimized) {
    return (
      <div className="fixed right-0 top-1/2 -translate-y-1/2 bg-white rounded-l-lg shadow-lg p-3 flex flex-col items-center gap-2 border-l border-t border-b border-gray-200">
        <span className="text-sm font-medium writing-mode-vertical">AI 助手</span>
        <Button
          variant="secondary"
          size="sm"
          onClick={() => setIsMinimized(false)}
          className="h-8 w-8 p-1"
        >
          <Maximize2 className="h-4 w-4 rotate-90" />
        </Button>
      </div>
    )
  }

  return (
    <div className="fixed right-0 top-1/2 -translate-y-1/2 w-96 h-[600px] bg-white rounded-l-lg shadow-xl flex flex-col border-l border-t border-b border-gray-200">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-semibold">AI 助手</h3>
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleClearChat}
            className="h-8 w-8 p-1"
            title="清除对话"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={() => setIsMinimized(true)}
            className="h-8 w-8 p-1"
            title="最小化"
          >
            <Minimize2 className="h-4 w-4 -rotate-90" />
          </Button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} isLoading={isLoading} />
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={isLoading || !isConnected}
          placeholder={isConnected ? "输入消息..." : "连接中..."}
        />
      </div>
    </div>
  )
} 