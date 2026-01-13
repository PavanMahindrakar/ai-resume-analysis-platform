import { useState, useCallback } from 'react'
import { analysisService } from '../services/api/analysisService'
import { AnalysisResult } from '../types'
import { useToast } from '../context/ToastContext'
import { useAnalysisContext } from '../context/AnalysisContext'

export function useAnalysis() {
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const { showToast } = useToast()
  const { setCurrentAnalysis, setIsAnalyzing } = useAnalysisContext()

  const runAnalysis = useCallback(async (resumeId: string, jobDescriptionId: string) => {
    setAnalyzing(true)
    setIsAnalyzing(true)
    setError(null)
    setResult(null)

    // Optimistic UI: Show loading state immediately
    showToast('Starting analysis...', 'info', 2000)

    try {
      const analysisResult = await analysisService.runAnalysis(resumeId, jobDescriptionId)
      setResult(analysisResult)
      setCurrentAnalysis(analysisResult)
      showToast('Analysis completed successfully!', 'success')
      return analysisResult
    } catch (err: any) {
      const errorMessage = err.message || 'Analysis failed'
      setError(errorMessage)
      showToast(errorMessage, 'error')
      throw err
    } finally {
      setAnalyzing(false)
      setIsAnalyzing(false)
    }
  }, [showToast, setCurrentAnalysis, setIsAnalyzing])

  const clearResult = useCallback(() => {
    setResult(null)
    setError(null)
    setCurrentAnalysis(null)
  }, [setCurrentAnalysis])

  return {
    runAnalysis,
    analyzing,
    error,
    result,
    clearResult,
  }
}
