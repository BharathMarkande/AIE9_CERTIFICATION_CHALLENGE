import React, { useState } from 'react'
import Header from './components/Header'
import UploadPanel from './components/UploadPanel'
import SessionSummaryCard from './components/SessionSummaryCard'
import ChatWindow from './components/ChatWindow'

export default function App() {
  const [sessionAnalysis, setSessionAnalysis] = useState(null)

  const handleUploadSuccess = (result) => {
    if (result && (result.behavioral_state != null || result.narrative_summary != null)) {
      setSessionAnalysis({
        behavioral_state: result.behavioral_state,
        severity_score: result.severity_score,
        expectancy_summary: result.expectancy_summary,
        discipline_score: result.discipline_score,
        narrative_summary: result.narrative_summary,
        rule_narrative: result.rule_narrative,
      })
    }
  }

  return (
    <div className="app">
      <div className="app-backdrop" aria-hidden />
      <Header />
      <main className="main">
        <UploadPanel onUploadSuccess={handleUploadSuccess} />
        {sessionAnalysis && (
          <SessionSummaryCard
            analysis={sessionAnalysis}
            onDismiss={() => setSessionAnalysis(null)}
          />
        )}
        <ChatWindow />
      </main>
    </div>
  )
}
