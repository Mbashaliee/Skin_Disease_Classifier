import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { Send, Bot, User } from 'lucide-react'
import './Chatbot.css'

const API_URL = '/api'

function Chatbot() {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content: 'Hello! I\'m your AI assistant. Ask me about skin conditions, symptoms, treatments, or how to use this app.'
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: userMessage
      })

      setMessages(prev => [...prev, {
        role: 'bot',
        content: response.data.response
      }])
    } catch (error) {
      console.error('Chat error:', error)
      setMessages(prev => [...prev, {
        role: 'bot',
        content: 'Sorry, I encountered an error. Please try again.'
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chatbot-container">
      <div className="chatbot-card">
        <div className="chat-header">
          <Bot size={24} />
          <h2>AI Assistant</h2>
        </div>

        <div className="messages-container">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <div className="message-icon">
                {message.role === 'user' ? <User size={20} /> : <Bot size={20} />}
              </div>
              <div className="message-content">
                <p>{message.content}</p>
              </div>
            </div>
          ))}
          {loading && (
            <div className="message bot-message">
              <div className="message-icon">
                <Bot size={20} />
              </div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSubmit} className="chat-input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything about skin conditions..."
            className="chat-input"
            disabled={loading}
          />
          <button type="submit" disabled={!input.trim() || loading} className="send-button">
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  )
}

export default Chatbot
