import { useState, useCallback } from 'react'
import { resumeService } from '../services/api/resumeService'
import { Resume } from '../types'
import { useToast } from '../context/ToastContext'
import { useAnalysisContext } from '../context/AnalysisContext'

export function useResumeUpload() {
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [resume, setResume] = useState<Resume | null>(null)
  const { showToast } = useToast()
  const { setSelectedResume } = useAnalysisContext()

  const uploadResume = useCallback(async (file: File) => {
    setUploading(true)
    setUploadProgress(0)
    setError(null)

    try {
      // Validate file type
      if (file.type !== 'application/pdf') {
        throw new Error('Only PDF files are allowed')
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        throw new Error('File size must be less than 10MB')
      }

      // Simulate progress (in real app, use axios onUploadProgress)
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 200)

      const result = await resumeService.uploadResume(file)
      clearInterval(progressInterval)
      setUploadProgress(100)
      setResume(result)
      setSelectedResume(result)
      showToast('Resume uploaded successfully!', 'success')
      return result
    } catch (err: any) {
      const errorMessage = err.message || 'Upload failed'
      setError(errorMessage)
      showToast(errorMessage, 'error')
      throw err
    } finally {
      setUploading(false)
      setTimeout(() => setUploadProgress(0), 500)
    }
  }, [showToast, setSelectedResume])

  const reset = useCallback(() => {
    setError(null)
    setResume(null)
    setUploadProgress(0)
  }, [])

  return {
    uploadResume,
    uploading,
    uploadProgress,
    error,
    resume,
    reset,
  }
}
