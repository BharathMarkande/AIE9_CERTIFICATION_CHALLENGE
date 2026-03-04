import React, { useState } from 'react'

const METRIC_INFO = {
  behavioral_state: {
    title: 'Behavioral State',
    body: 'How you trade after a losing trade compared to normal conditions. 1. STABLE — Your performance stays consistent regardless of recent losses. 2. LOSS_ESCALATION — Your losses become larger after losing trades (emotional risk escalation or revenge trading). 3. CONFIDENCE_CONTRACTION — Your winning trades shrink after losses (hesitation or reduced conviction). 4. ADAPTIVE_RECOVERY — Your performance improves after losses, showing resilience.',
  },
  severity: {
    title: 'Severity',
    body: 'This measures how strongly your performance changes after losses — closer to 0 means stable, closer to 1 means highly distorted.',
  },
  expectancy: {
    title: 'Expectancy Impact',
    body: 'Expectancy is the average outcome per trade in "R" (your risk per trade). Normal = expectancy in neutral conditions; Post-loss = after a loss. Delta (Δ) is the change; negative means performance worsens after losses. The rupee impact estimates how much that shift cost over this period.',
  },
  discipline: {
    title: 'Discipline Score',
    body: 'A 0-100 score for how well you followed your rules: risk per trade, daily loss limits, overtrading limits, and minimum risk:reward on winners. Higher is better.',
  },
}

function InfoTooltip({ id, metricKey }) {
  const info = METRIC_INFO[metricKey]
  if (!info) return null
  return (
    <span className="session-summary-info-wrap">
      <button
        type="button"
        className="session-summary-info-icon"
        aria-label={`Information: ${info.title}`}
        aria-describedby={id}
      >
        i
      </button>
      <span id={id} className="session-summary-info-tooltip" role="tooltip">
        <strong>{info.title}</strong>
        <span>{info.body}</span>
      </span>
    </span>
  )
}

/**
 * Session Analysis Card: shows behavioral state, severity, expectancy impact,
 * discipline score, and an expandable "View Full Analysis" with the full narrative.
 */
export default function SessionSummaryCard({ analysis, onDismiss }) {
  const [expanded, setExpanded] = useState(false)

  if (!analysis) return null

  const {
    behavioral_state,
    severity_score,
    expectancy_summary,
    discipline_score,
    narrative_summary,
    rule_narrative,
  } = analysis

  const formatExpectancy = () => {
    if (!expectancy_summary) return '—'
    const { expectancy_normal_R, expectancy_post_R, expectancy_delta_R, economic_impact_rupees } = expectancy_summary
    if ([expectancy_normal_R, expectancy_post_R, expectancy_delta_R, economic_impact_rupees].every((v) => v == null)) {
      return '—'
    }
    const parts = []
    if (expectancy_normal_R != null) parts.push(`Normal: ${expectancy_normal_R}R`)
    if (expectancy_post_R != null) parts.push(`Post-loss: ${expectancy_post_R}R`)
    if (expectancy_delta_R != null) parts.push(`Δ ${expectancy_delta_R}R`)
    if (economic_impact_rupees != null) parts.push(`≈ ₹${Math.round(economic_impact_rupees)} impact`)
    return parts.join(' · ')
  }

  return (
    <section className="glass-card session-summary-card" aria-label="Session analysis">
      <div className="session-summary-header">
        <h2 className="panel-title session-summary-title">Session Analysis</h2>
        {onDismiss && (
          <button
            type="button"
            className="session-summary-dismiss"
            onClick={onDismiss}
            aria-label="Dismiss analysis"
          >
            ×
          </button>
        )}
      </div>

      <div className="session-summary-grid">
        <div className="session-summary-item">
          <span className="session-summary-label">
            Behavioral State
            <InfoTooltip id="info-behavioral-state" metricKey="behavioral_state" />
          </span>
          <span className="session-summary-value session-summary-state">{behavioral_state ?? '—'}</span>
        </div>
        <div className="session-summary-item">
          <span className="session-summary-label">
            Severity
            <InfoTooltip id="info-severity" metricKey="severity" />
          </span>
          <span className="session-summary-value">{severity_score != null ? severity_score : '—'}</span>
        </div>
        <div className="session-summary-item">
          <span className="session-summary-label">
            Expectancy Impact
            <InfoTooltip id="info-expectancy" metricKey="expectancy" />
          </span>
          <span className="session-summary-value session-summary-expectancy">{formatExpectancy()}</span>
        </div>
        <div className="session-summary-item">
          <span className="session-summary-label">
            Discipline Score
            <InfoTooltip id="info-discipline" metricKey="discipline" />
          </span>
          <span className="session-summary-value session-summary-discipline">
            {discipline_score != null ? `${discipline_score}/100` : '—'}
          </span>
        </div>
      </div>

      <div className="session-summary-expand">
        <button
          type="button"
          className="session-summary-expand-btn"
          onClick={() => setExpanded((e) => !e)}
          aria-expanded={expanded}
        >
          {expanded ? 'Hide Full Analysis' : 'View Full Analysis'}
          <span className="session-summary-expand-icon" aria-hidden>{expanded ? ' ▲' : ' ▼'}</span>
        </button>
        {expanded && (
          <div className="session-summary-narrative-wrap">
            {narrative_summary && (
              <div className="session-summary-narrative-block">
                <h3 className="session-summary-narrative-heading">Behavioral & performance</h3>
                <div className="session-summary-narrative">{narrative_summary}</div>
              </div>
            )}
            {rule_narrative && (
              <div className="session-summary-narrative-block">
                <h3 className="session-summary-narrative-heading">Rule compliance</h3>
                <div className="session-summary-narrative">{rule_narrative}</div>
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  )
}
