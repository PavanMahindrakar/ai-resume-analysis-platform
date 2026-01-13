import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { analysisService } from '../../services/api/analysisService'
import { Card } from '../../components/common/Card'
import { Skeleton } from '../../components/common'
import { ErrorMessage } from '../../components/common/ErrorMessage'
import { handleKeyboardActivation } from '../../utils/keyboard'
import { AnalysisResult } from '../../types'
import './AnalysisResultPage.css'

export default function AnalysisResultPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(['explanation']))
  const [animatedScore, setAnimatedScore] = useState(0)

  useEffect(() => {
    const loadResult = async () => {
      if (!id) {
        setError('Invalid analysis ID')
        setLoading(false)
        return
      }

      try {
        const data = await analysisService.getAnalysis(id)
        setResult(data)
        
        // Animate score from 0 to actual score
        const targetScore = data.match_score
        const duration = 2000 // 2 seconds
        const steps = 60
        const increment = targetScore / steps
        let current = 0
        
        const interval = setInterval(() => {
          current += increment
          if (current >= targetScore) {
            setAnimatedScore(targetScore)
            clearInterval(interval)
          } else {
            setAnimatedScore(current)
          }
        }, duration / steps)
        
        return () => clearInterval(interval)
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to load analysis result'
        setError(errorMessage)
      } finally {
        setLoading(false)
      }
    }

    loadResult()
  }, [id])

  const toggleSection = (section: string) => {
    setExpandedSections((prev: Set<string>) => {
      const newSet = new Set(prev)
      if (newSet.has(section)) {
        newSet.delete(section)
      } else {
        newSet.add(section)
      }
      return newSet
    })
  }

  const getScoreColor = (score: number) => {
    if (score >= 70) return 'var(--success)'
    if (score >= 50) return 'var(--warning)'
    return 'var(--error)'
  }

  if (loading) {
    return (
      <div className="analysis-result-page">
        <Card title="Analysis Results">
          <div className="result-header">
            <Skeleton variant="circular" width={200} height={200} />
          </div>
          <div className="result-sections">
            <Skeleton height={60} />
            <Skeleton height={60} />
            <Skeleton height={60} />
          </div>
        </Card>
      </div>
    )
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={() => navigate('/analysis')} />
  }

  if (!result) {
    return <ErrorMessage message="Analysis result not found" onRetry={() => navigate('/analysis')} />
  }

  const displayScore = loading ? animatedScore : result.match_score

  return (
    <div className="analysis-result-page">
      <Card title="Analysis Results">
        <div className="result-header">
          <div className="score-container">
            <div
              className="score-circle"
              style={{
                background: `conic-gradient(${getScoreColor(result.match_score)} 0deg ${(displayScore / 100) * 360}deg, var(--border) ${(displayScore / 100) * 360}deg 360deg)`,
              }}
            >
              <div className="score-inner">
                <span className="score-value">{displayScore.toFixed(1)}%</span>
                <span className="score-label">Match</span>
              </div>
            </div>
          </div>
        </div>

        <div className="result-sections">
          <div className="result-section">
            <button
              className="section-header"
              onClick={() => toggleSection('explanation')}
              onKeyDown={(e: React.KeyboardEvent) => handleKeyboardActivation(e, () => toggleSection('explanation'))}
              aria-expanded={expandedSections.has('explanation')}
              aria-controls="explanation-section"
            >
              <span>📋 Explanation</span>
              <span aria-hidden="true">{expandedSections.has('explanation') ? '▼' : '▶'}</span>
            </button>
            {expandedSections.has('explanation') && (
              <div id="explanation-section" className="section-content" role="region">
                <pre className="explanation-text">{result.explanation}</pre>
              </div>
            )}
          </div>

          <div className="result-section">
            <button
              className="section-header"
              onClick={() => toggleSection('matched')}
              onKeyDown={(e: React.KeyboardEvent) => handleKeyboardActivation(e, () => toggleSection('matched'))}
              aria-expanded={expandedSections.has('matched')}
              aria-controls="matched-section"
            >
              <span>✅ Matched Skills ({Object.keys(result.matched_keywords).length})</span>
              <span aria-hidden="true">{expandedSections.has('matched') ? '▼' : '▶'}</span>
            </button>
            {expandedSections.has('matched') && (
              <div id="matched-section" className="section-content" role="region">
                <div className="keywords-list">
                  {Object.entries(result.matched_keywords).map(([jobKeyword, details]) => {
                    const keywordDetails = details as { resume_keyword: string; score: number; match_type: 'exact' | 'partial' }
                    return (
                    <div
                      key={jobKeyword}
                      className="keyword-item keyword-matched"
                      style={{ animationDelay: `${Math.random() * 0.3}s` }}
                    >
                      <div className="keyword-name">{jobKeyword}</div>
                      <div className="keyword-details">
                        <span className="keyword-type">{keywordDetails.match_type}</span>
                        <span className="keyword-score">{(keywordDetails.score * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                    )
                  })}
                </div>
              </div>
            )}
          </div>

          <div className="result-section">
            <button
              className="section-header"
              onClick={() => toggleSection('missing')}
              onKeyDown={(e: React.KeyboardEvent) => handleKeyboardActivation(e, () => toggleSection('missing'))}
              aria-expanded={expandedSections.has('missing')}
              aria-controls="missing-section"
            >
              <span>⚠️ Missing Skills ({result.missing_keywords.length})</span>
              <span aria-hidden="true">{expandedSections.has('missing') ? '▼' : '▶'}</span>
            </button>
            {expandedSections.has('missing') && (
              <div id="missing-section" className="section-content" role="region">
                <div className="keywords-list">
                  {result.missing_keywords.map((keyword: string, index: number) => (
                    <div
                      key={keyword}
                      className="keyword-item keyword-missing"
                      style={{ animationDelay: `${index * 0.1}s` }}
                    >
                      {keyword}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="result-actions">
          <button className="action-button" onClick={() => navigate('/analysis')} type="button">
            Run Another Analysis
          </button>
          <button className="action-button" onClick={() => navigate('/dashboard')} type="button">
            View Dashboard
          </button>
        </div>
      </Card>
    </div>
  )
}
