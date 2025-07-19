'use client'

import React from 'react'
import { MessageCircle, X } from 'lucide-react'

interface AIAssistantButtonProps {
  onClick: () => void
  isOpen: boolean
  hasNewMessage?: boolean
}

export const AIAssistantButton: React.FC<AIAssistantButtonProps> = ({
  onClick,
  isOpen,
  hasNewMessage = false
}) => {
  return (
    <button
      onClick={onClick}
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        width: '56px',
        height: '56px',
        backgroundColor: isOpen ? '#1d4ed8' : '#2563eb',
        color: 'white',
        borderRadius: '50%',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: 'none',
        cursor: 'pointer',
        transition: 'all 0.2s',
        transform: isOpen ? 'scale(0.95)' : 'scale(1)',
        zIndex: 9998
      }}
      onMouseEnter={(e) => {
        if (!isOpen) {
          e.currentTarget.style.transform = 'scale(1.05)';
          e.currentTarget.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)';
        }
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = isOpen ? 'scale(0.95)' : 'scale(1)';
        e.currentTarget.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)';
      }}
      aria-label={isOpen ? '关闭AI助手' : '打开AI助手'}
    >
      {isOpen ? (
        <X className="w-6 h-6" />
      ) : (
        <>
          <MessageCircle className="w-6 h-6" />
          {hasNewMessage && (
            <span style={{
              position: 'absolute',
              top: '4px',
              right: '4px',
              width: '12px',
              height: '12px',
              backgroundColor: '#ef4444',
              borderRadius: '50%',
              animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite'
            }} />
          )}
        </>
      )}
    </button>
  )
} 