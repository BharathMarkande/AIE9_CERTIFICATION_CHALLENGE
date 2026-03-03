import React, { useState, useEffect } from 'react'
import { uploadSession } from '../services/api'

const RISK_STORAGE_KEY = 'riskhalo_risk_per_trade'

export default function UploadPanel({ onUploadSuccess, onUploadError }) {
  const [file, setFile] = useState(null)
  const [riskPerTrade, setRiskPerTrade] = useState(() => {
    try {
      const saved = localStorage.getItem(RISK_STORAGE_KEY)
      return saved !== null ? Number(saved) : 2000
    } catch {
      return 2000
    }
  })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)
  const [isError, setIsError] = useState(false)

  useEffect(() => {
    try {
      localStorage.setItem(RISK_STORAGE_KEY, String(riskPerTrade))
    } catch (_) {}
  }, [riskPerTrade])

  const handleFileChange = (e) => {
    const f = e.target.files?.[0]
    setFile(f || null)
    setMessage(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) {
      setMessage('Please select a weekly trade file (.xlsx)')
      setIsError(true)
      return
    }
    if (riskPerTrade <= 0 || isNaN(riskPerTrade)) {
      setMessage('Please enter a valid risk per trade')
      setIsError(true)
      return
    }
    setLoading(true)
    setMessage(null)
    setIsError(false)
    try {
      const result = await uploadSession(file, riskPerTrade)
      setMessage(result.message || 'Session analyzed successfully.')
      setIsError(false)
      onUploadSuccess?.(result)
    } catch (err) {
      const msg = err.message || 'Upload failed'
      setMessage(msg)
      setIsError(true)
      onUploadError?.(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="glass-card upload-panel">
      <h2 className="panel-title">Upload Session</h2>
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="form-row">
          <label className="label">Weekly trade file (.xlsx)</label>
          <input
            type="file"
            accept=".xlsx,.xls"
            onChange={handleFileChange}
            className="input-file"
            disabled={loading}
          />
        </div>
        <div className="form-row">
          <label className="label">Risk per trade</label>
          <input
            type="number"
            min={1}
            value={riskPerTrade}
            onChange={(e) => setRiskPerTrade(Number(e.target.value) || 0)}
            className="input-number"
            disabled={loading}
          />
        </div>
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? (
            <>
              <span className="spinner" aria-hidden />
              Analyzing...
            </>
          ) : (
            'Analyze Session'
          )}
        </button>
      </form>
      {message && (
        <p className={`upload-message ${isError ? 'error' : 'success'}`}>
          {message}
        </p>
      )}
    </section>
  )
}
