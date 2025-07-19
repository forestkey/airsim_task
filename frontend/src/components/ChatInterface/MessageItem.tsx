import React from 'react'
import { ChatMessage } from '@/src/services/chatService'
import { Bot, User, AlertCircle, CheckCircle2, XCircle } from 'lucide-react'

interface MessageItemProps {
  message: ChatMessage
}

export const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const isUser = message.role === 'user'
  const isSystem = message.role === 'system'
  
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser ? 'bg-blue-500' : isSystem ? 'bg-yellow-500' : 'bg-gray-700'
      }`}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : isSystem ? (
          <AlertCircle className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex-1 ${isUser ? 'text-right' : ''}`}>
        <div className={`inline-block max-w-[85%] ${isUser ? 'text-left' : ''}`}>
          {/* Message bubble */}
          <div className={`rounded-lg px-4 py-2 ${
            isUser 
              ? 'bg-blue-500 text-white' 
              : isSystem 
              ? 'bg-yellow-100 text-yellow-800 border border-yellow-200'
              : 'bg-gray-100 text-gray-800'
          }`}>
            <p className="whitespace-pre-wrap">{message.content}</p>
          </div>

          {/* Tool calls */}
          {message.tool_calls && message.tool_calls.length > 0 && (
            <div className="mt-2 space-y-1">
              {message.tool_calls.map((tool, index) => (
                <div 
                  key={index} 
                  className="text-xs bg-gray-50 rounded px-2 py-1 flex items-center gap-2"
                >
                  {tool.error ? (
                    <>
                      <XCircle className="w-3 h-3 text-red-500" />
                      <span className="text-red-600">
                        {tool.tool}: {tool.error}
                      </span>
                    </>
                  ) : (
                    <>
                      <CheckCircle2 className="w-3 h-3 text-green-500" />
                      <span className="text-gray-600">
                        执行: {tool.tool}
                        {tool.parameters && Object.keys(tool.parameters).length > 0 && (
                          <span className="ml-1">
                            ({Object.entries(tool.parameters)
                              .map(([k, v]) => `${k}: ${v}`)
                              .join(', ')})
                          </span>
                        )}
                      </span>
                    </>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Timestamp */}
          <div className="text-xs text-gray-500 mt-1">
            {formatTime(message.timestamp)}
          </div>
        </div>
      </div>
    </div>
  )
} 