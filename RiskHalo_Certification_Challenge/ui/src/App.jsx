import React from 'react'
import Header from './components/Header'
import UploadPanel from './components/UploadPanel'
import ChatWindow from './components/ChatWindow'

export default function App() {
  return (
    <div className="app">
      <div className="app-backdrop" aria-hidden />
      <Header />
      <main className="main">
        <UploadPanel />
        <ChatWindow />
      </main>
    </div>
  )
}
