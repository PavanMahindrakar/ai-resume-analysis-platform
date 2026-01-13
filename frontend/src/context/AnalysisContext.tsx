import React, { createContext, useContext, useState, ReactNode } from 'react'
import { AnalysisResult, Resume, JobDescription } from '../types'

interface AnalysisContextType {
  // Selection state
  selectedResume: Resume | null
  selectedJobDescription: JobDescription | null
  setSelectedResume: (resume: Resume | null) => void
  setSelectedJobDescription: (job: JobDescription | null) => void

  // Analysis state
  currentAnalysis: AnalysisResult | null
  setCurrentAnalysis: (analysis: AnalysisResult | null) => void
  isAnalyzing: boolean
  setIsAnalyzing: (analyzing: boolean) => void

  // Clear all state
  clearSelection: () => void
}

const AnalysisContext = createContext<AnalysisContextType | undefined>(undefined)

export function AnalysisProvider({ children }: { children: ReactNode }) {
  const [selectedResume, setSelectedResume] = useState<Resume | null>(null)
  const [selectedJobDescription, setSelectedJobDescription] = useState<JobDescription | null>(null)
  const [currentAnalysis, setCurrentAnalysis] = useState<AnalysisResult | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const clearSelection = () => {
    setSelectedResume(null)
    setSelectedJobDescription(null)
    setCurrentAnalysis(null)
    setIsAnalyzing(false)
  }

  return (
    <AnalysisContext.Provider
      value={{
        selectedResume,
        selectedJobDescription,
        setSelectedResume,
        setSelectedJobDescription,
        currentAnalysis,
        setCurrentAnalysis,
        isAnalyzing,
        setIsAnalyzing,
        clearSelection,
      }}
    >
      {children}
    </AnalysisContext.Provider>
  )
}

export function useAnalysisContext() {
  const context = useContext(AnalysisContext)
  if (context === undefined) {
    throw new Error('useAnalysisContext must be used within an AnalysisProvider')
  }
  return context
}
