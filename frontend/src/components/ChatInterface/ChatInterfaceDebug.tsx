import React, { useState, useEffect } from 'react'
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
  
  // Debug state
  const [debugMode] = useState(true)
  const [debugLogs, setDebugLogs] = useState<string[]>([])
  
  const addDebugLog = (log: string) => {
    if (debugMode) {
      const timestamp = new Date().toISOString().split('T')[1].split('.')[0]
      const logEntry = `[${timestamp}] ${log}`
      console.log(logEntry)
      setDebugLogs(prev => [...prev.slice(-9), logEntry])
    }
  }

  useEffect(() => {
    addDebugLog('Component mounted, connecting WebSocket...')
    
    // Connect WebSocket
    chatService.connectWebSocket(
      (data) => {
        addDebugLog(`WebSocket message received: ${data.type}`)
        
        if (data.type === 'connected') {
          setIsConnected(true)
          addDebugLog('WebSocket connected')
        } else if (data.type === 'ai_reply') {
          // Add AI message from WebSocket
          const aiMessage: ChatMessage = {
            role: 'assistant',
            content: data.data.reply,
            timestamp: data.data.timestamp || new Date().toISOString(),
            tool_calls: data.data.tool_calls,
          }
          addDebugLog(`Adding AI message: ${aiMessage.content.substring(0, 50)}...`)
          setMessages(prev => {
            addDebugLog(`Previous messages count: ${prev.length}`)
            return [...prev, aiMessage]
          })
          setIsLoading(false)
        } else if (data.type === 'status_update') {
          addDebugLog(`Status update: ${JSON.stringify(data.data)}`)
        }
      },
      (error) => {
        addDebugLog(`WebSocket error: ${error}`)
        setIsConnected(false)
      },
      () => {
        addDebugLog('WebSocket closed')
        setIsConnected(false)
      }
    )

    // Set connected for now
    setIsConnected(true)

    return () => {
      addDebugLog('Component unmounting, disconnecting WebSocket')
      chatService.disconnectWebSocket()
    }
  }, [])

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return

    addDebugLog(`Sending message: ${content}`)
    
    // Add user message
    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    }
    
    setMessages(prev => {
      addDebugLog(`Adding user message, current count: ${prev.length}`)
      const newMessages = [...prev, userMessage]
      addDebugLog(`New messages count: ${newMessages.length}`)
      return newMessages
    })
    setIsLoading(true)

    try {
      if (chatService.isWebSocketConnected()) {
        addDebugLog('Using WebSocket to send message')
        chatService.sendWebSocketMessage(content)
      } else {
        addDebugLog('Using HTTP API to send message')
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
      addDebugLog(`Error sending message: ${error}`)
      setIsLoading(false)
      const errorMessage: ChatMessage = {
        role: 'system',
        content: '抱歉，发送消息时出现错误。请稍后重试。',
        timestamp: new Date().toISOString(),
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const handleClearChat = async () => {
    addDebugLog('Clearing chat')
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

      {/* Debug Panel */}
      {debugMode && (
        <div className="bg-gray-100 p-2 text-xs font-mono max-h-32 overflow-y-auto border-b">
          <div className="font-bold mb-1">Debug Logs:</div>
          {debugLogs.map((log, index) => (
            <div key={index} className="text-gray-600">{log}</div>
          ))}
          <div className="mt-1 text-gray-700">
            Messages: {messages.length} | Loading: {isLoading.toString()} | Connected: {isConnected.toString()}
          </div>
        </div>
      )}

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
    </div>
  )
} 