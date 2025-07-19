import React, { useState, useEffect, useRef, useCallback } from 'react'
import { Send, Trash2, Minimize2, Maximize2, Bot } from 'lucide-react'
import { MessageList } from './MessageList'
import { MessageInput } from './MessageInput'
import { Button } from '../../../components/ui/Button'
import { chatService, ChatMessage } from '@/src/services/chatService'
import '../../styles/chat.css'

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [isMinimized, setIsMinimized] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)
  
  // Use ref to access latest messages in callbacks
  const messagesRef = useRef<ChatMessage[]>([])
  messagesRef.current = messages
  
  const scrollToBottom = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Memoized message handler to prevent closure issues
  const handleWebSocketMessage = useCallback((data: any) => {
    console.log('WebSocket message:', data.type)
    
    if (data.type === 'connected') {
      setIsConnected(true)
    } else if (data.type === 'ai_reply') {
      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: data.data.reply,
        timestamp: data.data.timestamp || new Date().toISOString(),
        tool_calls: data.data.tool_calls,
      }
      
      // Use functional update to ensure we have latest state
      setMessages(prevMessages => {
        console.log('Adding AI message, current messages:', prevMessages.length)
        return [...prevMessages, aiMessage]
      })
      setIsLoading(false)
    } else if (data.type === 'status_update') {
      console.log('Status update:', data.data)
    }
  }, [])

  useEffect(() => {
    console.log('Connecting to WebSocket...')
    
    // Connect to WebSocket
    chatService.connectWebSocket(
      handleWebSocketMessage,
      (error) => {
        console.error('WebSocket error:', error)
        setIsConnected(false)
      },
      () => {
        setIsConnected(false)
      }
    )

    // Set connected state immediately
    setIsConnected(true)

    return () => {
      console.log('Disconnecting WebSocket...')
      chatService.disconnectWebSocket()
    }
  }, [handleWebSocketMessage])

  const handleSendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isLoading) return

    console.log('Sending message:', content)
    
    // Create user message
    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    }
    
    // Add user message to state
    setMessages(prevMessages => {
      const newMessages = [...prevMessages, userMessage]
      console.log('Added user message, total messages:', newMessages.length)
      messagesRef.current = newMessages // Update ref
      return newMessages
    })
    
    setIsLoading(true)

    try {
      if (chatService.isWebSocketConnected()) {
        console.log('Sending via WebSocket')
        chatService.sendWebSocketMessage(content)
      } else {
        console.log('Sending via HTTP')
        const response = await chatService.sendMessage(content)
        const aiMessage: ChatMessage = {
          role: 'assistant',
          content: response.reply,
          timestamp: response.timestamp || new Date().toISOString(),
          tool_calls: response.tool_calls,
        }
        setMessages(prev => [...prev, aiMessage])
        setIsLoading(false)
      }
    } catch (error) {
      console.error('Failed to send message:', error)
      setIsLoading(false)
      const errorMessage: ChatMessage = {
        role: 'system',
        content: '抱歉，发送消息时出现错误。请稍后重试。',
        timestamp: new Date().toISOString(),
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }, [isLoading])

  const handleClearChat = useCallback(async () => {
    console.log('Clearing chat')
    setMessages([])
    messagesRef.current = []
    await chatService.clearSession()
  }, [])

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
          <Bot className="w-5 h-5 text-blue-500" />
          <h3 className="font-semibold">AI 助手</h3>
          {isConnected ? (
            <span className="text-xs text-green-500">● 已连接</span>
          ) : (
            <span className="text-xs text-gray-400">● 连接中...</span>
          )}
        </div>
        <div className="flex items-center gap-1">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleClearChat}
            className="h-8 w-8 p-1 hover:bg-gray-100"
            title="清空对话"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={() => setIsMinimized(true)}
            className="h-8 w-8 p-1 hover:bg-gray-100"
            title="最小化"
          >
            <Minimize2 className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Messages */}
      <MessageList messages={messages} isLoading={isLoading} />

      {/* Input */}
      <div className="p-4 border-t">
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={!isConnected || isLoading}
          placeholder={isConnected ? "输入消息..." : "连接中..."}
        />
      </div>
      
      {/* Scroll anchor */}
      <div ref={scrollRef} />
    </div>
  )
} 