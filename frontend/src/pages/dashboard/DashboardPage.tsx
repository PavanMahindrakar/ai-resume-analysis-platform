import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDashboard } from '../../hooks/useDashboard'
import { Card } from '../../components/common/Card'
import { SkeletonCard, Skeleton } from '../../components/common'
import { ErrorMessage } from '../../components/common/ErrorMessage'
import { EmptyState } from '../../components/common/EmptyState'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'
import { AnalysisHistoryItem } from '../../types'
import './DashboardPage.css'

export default function DashboardPage() {
  const navigate = useNavigate()
  const { summary, history, loading, error, refetch } = useDashboard()
  const [dateFilter, setDateFilter] = useState<'all' | 'week' | 'month'>('all')
  const [roleFilter, setRoleFilter] = useState<string>('all')

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-header">
          <Skeleton width={200} height={40} />
        </div>
        <div className="dashboard-stats">
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
        </div>
        <SkeletonCard />
      </div>
    )
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={refetch} />
  }

  if (!summary || summary.total_analyses === 0) {
    return (
      <EmptyState
        icon="📊"
        title="No Analysis Data"
        message="Run your first analysis to see insights here"
        action={{
          label: 'Run Analysis',
          onClick: () => navigate('/analysis'),
        }}
      />
    )
  }

  // Prepare chart data
  const scoreDistribution = history?.analyses.map((analysis: AnalysisHistoryItem) => ({
    date: new Date(analysis.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    score: analysis.match_score,
  })) || []

  const missingSkillsData = summary.most_common_missing_skills.map((skill) => ({
    skill: skill.skill.length > 20 ? skill.skill.substring(0, 20) + '...' : skill.skill,
    count: skill.count,
    frequency: skill.frequency,
  }))

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <div className="dashboard-filters">
          <select
            className="filter-select"
            value={dateFilter}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setDateFilter(e.target.value as 'all' | 'week' | 'month')}
          >
            <option value="all">All Time</option>
            <option value="week">Last Week</option>
            <option value="month">Last Month</option>
          </select>
          <select
            className="filter-select"
            value={roleFilter}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setRoleFilter(e.target.value)}
          >
            <option value="all">All Roles</option>
            {/* Add role options dynamically */}
          </select>
        </div>
      </div>

      <div className="dashboard-stats">
        <Card className="stat-card">
          <div className="stat-value">{summary.total_analyses}</div>
          <div className="stat-label">Total Analyses</div>
        </Card>
        <Card className="stat-card">
          <div className="stat-value">{summary.average_match_score.toFixed(1)}%</div>
          <div className="stat-label">Average Match</div>
        </Card>
        <Card className="stat-card">
          <div className="stat-value">{summary.highest_match_score.toFixed(1)}%</div>
          <div className="stat-label">Best Score</div>
        </Card>
        <Card className="stat-card">
          <div className="stat-value">{summary.lowest_match_score.toFixed(1)}%</div>
          <div className="stat-label">Lowest Score</div>
        </Card>
      </div>

      <div className="dashboard-charts">
        <Card title="Score Trend" className="chart-card">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={scoreDistribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Line type="monotone" dataKey="score" stroke="var(--primary)" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Most Common Missing Skills" className="chart-card">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={missingSkillsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="skill" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="var(--error)" />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {history && history.analyses.length > 0 && (
        <Card title="Recent Analyses" className="history-card">
          <div className="history-list">
            {history.analyses.map((analysis: AnalysisHistoryItem) => (
              <div
                key={analysis.id}
                className="history-item"
                onClick={() => navigate(`/analysis/${analysis.id}`)}
                onKeyDown={(e: React.KeyboardEvent) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    navigate(`/analysis/${analysis.id}`)
                  }
                }}
                role="button"
                tabIndex={0}
                aria-label={`View analysis from ${new Date(analysis.created_at).toLocaleDateString()}`}
              >
                <div className="history-score">
                  <span className={`score-badge ${analysis.match_score >= 70 ? 'score-high' : analysis.match_score >= 50 ? 'score-medium' : 'score-low'}`}>
                    {analysis.match_score.toFixed(1)}%
                  </span>
                </div>
                <div className="history-info">
                  <div className="history-date">
                    {new Date(analysis.created_at).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </div>
                </div>
                <div className="history-arrow">→</div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  )
}
