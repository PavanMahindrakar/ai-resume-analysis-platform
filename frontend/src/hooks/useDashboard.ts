import { useState, useEffect } from 'react'
import { dashboardService } from '../services/api/dashboardService'
import { DashboardSummary, DashboardHistory } from '../types'

export function useDashboard() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [history, setHistory] = useState<DashboardHistory | null>(null)

  const fetchSummary = async (limit: number = 10) => {
    try {
      const data = await dashboardService.getSummary(limit)
      setSummary(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to load summary')
    }
  }

  const fetchHistory = async (skip: number = 0, limit: number = 20) => {
    try {
      const data = await dashboardService.getHistory(skip, limit)
      setHistory(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to load history')
    }
  }

  useEffect(() => {
    const loadData = async () => {
      setLoading(true)
      setError(null)
      try {
        await Promise.all([fetchSummary(), fetchHistory()])
      } catch (err) {
        // Error already set in individual fetch functions
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  return {
    summary,
    history,
    loading,
    error,
    refetch: () => {
      fetchSummary()
      fetchHistory()
    },
  }
}
