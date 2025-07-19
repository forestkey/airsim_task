import { SERVICES, API_ENDPOINTS } from '@/src/config/services'

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
  tool_calls?: ToolCall[]
}

export interface ToolCall {
  tool: string
  parameters: Record<string, any>
  result?: Record<string, any>
  error?: string
}

export interface ChatRequest {
  message: string
  session_id?: string
}

export interface ChatResponse {
  reply: string
  tool_calls?: ToolCall[]
  session_id: string
  timestamp: string
}

class ChatService {
  private baseUrl: string
  private wsUrl: string
  private ws: WebSocket | null = null
  private sessionId: string | null = null

  constructor() {
    this.baseUrl = SERVICES.AI_API
    this.wsUrl = SERVICES.WS_CHAT
  }

  async sendMessage(message: string): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}${API_ENDPOINTS.chat.message}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: this.sessionId,
      } as ChatRequest),
    })

    if (!response.ok) {
      throw new Error(`Chat API error: ${response.statusText}`)
    }

    const data = await response.json()
    this.sessionId = data.session_id
    return data
  }

  async clearSession(): Promise<void> {
    if (!this.sessionId) return

    await fetch(`${this.baseUrl}${API_ENDPOINTS.chat.session}/${this.sessionId}`, {
      method: 'DELETE',
    })
    
    this.sessionId = null
  }

  connectWebSocket(
    onMessage: (data: any) => void,
    onError?: (error: any) => void,
    onClose?: () => void
  ): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      return
    }

    // Generate session ID if not exists
    if (!this.sessionId) {
      this.sessionId = crypto.randomUUID()
    }

    const wsUrl = `${this.wsUrl}${API_ENDPOINTS.chat.ws}/${this.sessionId}`
    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      console.log('Chat WebSocket connected')
      onMessage({ type: 'connected' })
    }

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onMessage(data)
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    this.ws.onerror = (error) => {
      console.error('Chat WebSocket error:', error)
      onError?.(error)
    }

    this.ws.onclose = () => {
      console.log('Chat WebSocket disconnected')
      onClose?.()
      this.ws = null
    }
  }

  sendWebSocketMessage(message: string): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ message }))
    } else {
      console.error('WebSocket is not connected')
    }
  }

  disconnectWebSocket(): void {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  isWebSocketConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN
  }
}

export const chatService = new ChatService() 