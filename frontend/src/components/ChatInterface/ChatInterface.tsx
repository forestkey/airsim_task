'use client'

import React, { useState, useEffect, useRef } from 'react'
import { MessageList } from './MessageList'
import { MessageInput } from './MessageInput'
import { chatService, ChatMessage } from '@/src/services/chatService'
import { Button } from '../../../components/ui/Button'
import { Trash2, X } from 'lucide-react'
import '@/src/styles/chat.css'

interface ChatInterfaceProps {
  isVisible: boolean
  onClose: () => void
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ isVisible, onClose }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Only connect if visible
    if (!isVisible) return
    
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
          // Use functional update to ensure we have latest state
          setMessages(prevMessages => {
            console.log('[ChatInterface] Adding AI reply, current messages:', prevMessages.length)
            return [...prevMessages, aiMessage]
          })
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
  }, [isVisible])

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return

    // Add user message
    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    }
    console.log('[ChatInterface] Adding user message:', content)
    setMessages(prev => {
      console.log('[ChatInterface] Current messages before adding user:', prev.length)
      const newMessages = [...prev, userMessage]
      console.log('[ChatInterface] Messages after adding user:', newMessages.length)
      return newMessages
    })
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

  return (
    <div 
      style={{
        position: 'fixed',
        right: isVisible ? '0' : '-400px',
        top: '50%',
        transform: 'translateY(-50%)',
        width: '384px',
        height: '600px',
        maxHeight: '80vh',
        backgroundColor: 'white',
        borderRadius: '0.5rem 0 0 0.5rem',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        display: 'flex',
        flexDirection: 'column',
        borderLeft: '1px solid #e5e7eb',
        borderTop: '1px solid #e5e7eb',
        borderBottom: '1px solid #e5e7eb',
        transition: 'right 0.3s ease-in-out',
        zIndex: 9999
      }}
    >
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
            onClick={onClose}
            className="h-8 w-8 p-1"
            title="关闭"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList key={messages.length} messages={messages} isLoading={isLoading} />
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