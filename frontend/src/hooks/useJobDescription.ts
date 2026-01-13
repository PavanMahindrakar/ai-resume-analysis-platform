import { useState, useEffect, useCallback } from 'react'
import { jobService } from '../services/api/jobService'
import { JobDescription } from '../types'
import { useToast } from '../context/ToastContext'
import { useAnalysisContext } from '../context/AnalysisContext'

export function useJobDescription() {
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [jobDescription, setJobDescription] = useState<JobDescription | null>(null)
  const [draft, setDraft] = useState({ title: '', description: '' })
  const [autoSaved, setAutoSaved] = useState(false)
  const { showToast } = useToast()
  const { setSelectedJobDescription } = useAnalysisContext()

  // Auto-save draft to localStorage
  useEffect(() => {
    const savedDraft = localStorage.getItem('job_description_draft')
    if (savedDraft) {
      try {
        const parsed = JSON.parse(savedDraft)
        setDraft(parsed)
        setAutoSaved(true)
      } catch {
        // Ignore parse errors
      }
    }
  }, [])

  // Auto-save with debounce
  useEffect(() => {
    if (!draft.title && !draft.description) return

    const timeoutId = setTimeout(() => {
      localStorage.setItem('job_description_draft', JSON.stringify(draft))
      setAutoSaved(true)
      setTimeout(() => setAutoSaved(false), 2000)
    }, 1000) // Debounce auto-save

    return () => clearTimeout(timeoutId)
  }, [draft])

  const createJobDescription = useCallback(async (title: string, description: string) => {
    setSaving(true)
    setError(null)

    // Optimistic UI: Show saving state
    showToast('Saving job description...', 'info', 2000)

    try {
      const result = await jobService.createJobDescription(title, description)
      setJobDescription(result)
      setSelectedJobDescription(result)
      // Clear draft after successful save
      localStorage.removeItem('job_description_draft')
      setDraft({ title: '', description: '' })
      showToast('Job description saved successfully!', 'success')
      return result
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to create job description'
      setError(errorMessage)
      showToast(errorMessage, 'error')
      throw err
    } finally {
      setSaving(false)
    }
  }, [showToast, setSelectedJobDescription])

  return {
    createJobDescription,
    saving,
    error,
    jobDescription,
    draft,
    setDraft,
    autoSaved,
  }
}
