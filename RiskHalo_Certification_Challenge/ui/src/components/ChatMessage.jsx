import React from 'react'

export default function ChatMessage({ role, content }) {
  const isUser = role === 'user'
  return (
    <div className={`chat-message ${isUser ? 'chat-message-user' : 'chat-message-assistant'}`}>
      <div className="chat-message-bubble">
        {content}
      </div>
    </div>
  )
}
