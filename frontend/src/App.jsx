import { useState } from 'react'
import Classifier from './components/Classifier'
import Chatbot from './components/Chatbot'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('classifier')

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">Skin Disease Classifier</h1>
          <p className="app-subtitle">AI-Powered Dermatology Assistant</p>
        </div>
      </header>

      <div className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'classifier' ? 'active' : ''}`}
          onClick={() => setActiveTab('classifier')}
        >
          <span>Image Classifier</span>
        </button>
        <button
          className={`tab-button ${activeTab === 'chatbot' ? 'active' : ''}`}
          onClick={() => setActiveTab('chatbot')}
        >
          <span>AI Assistant</span>
        </button>
      </div>

      <main className="main-content">
        {activeTab === 'classifier' ? <Classifier /> : <Chatbot />}
      </main>

      <footer className="app-footer">
        <p>Powered by AI for medical education. Always consult a healthcare professional.</p>
      </footer>
    </div>
  )
}

export default App
