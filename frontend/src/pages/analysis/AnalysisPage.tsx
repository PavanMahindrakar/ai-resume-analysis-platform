import React, { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAnalysis } from '../../hooks/useAnalysis'
import { useAnalysisContext } from '../../context/AnalysisContext'
import { resumeService } from '../../services/api/resumeService'
import { jobService } from '../../services/api/jobService'
import { Card } from '../../components/common/Card'
import { Button } from '../../components/common/Button'
import { Select } from '../../components/common/Select'
import { LoadingSpinner } from '../../components/common'
import { ErrorMessage } from '../../components/common/ErrorMessage'
import { EmptyState } from '../../components/common/EmptyState'
import { Resume, JobDescription } from '../../types'
import './AnalysisPage.css'

export default function AnalysisPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { runAnalysis, analyzing, error } = useAnalysis()
  const { selectedResume: contextResume, selectedJobDescription: contextJob, setSelectedResume, setSelectedJobDescription } = useAnalysisContext()
  const [resumes, setResumes] = useState<Resume[]>([])
  const [jobDescriptions, setJobDescriptions] = useState<JobDescription[]>([])
  const [selectedResumeId, setSelectedResumeId] = useState<string>(contextResume?.id || '')
  const [selectedJobId, setSelectedJobId] = useState<string>(contextJob?.id || '')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      try {
        const [resumesData, jobsData] = await Promise.all([
          resumeService.getResumes(),
          jobService.getJobDescriptions(),
        ])
        setResumes(resumesData)
        setJobDescriptions(jobsData)

        // Pre-select if coming from job description page
        const jobId = location.state?.jobDescriptionId
        if (jobId && jobsData.find((j) => j.id === jobId)) {
          setSelectedJobId(jobId)
          const job = jobsData.find((j) => j.id === jobId)
          if (job) setSelectedJobDescription(job)
        }
        
        // Pre-select context resume/job if available
        if (contextResume) {
          const foundResume = resumesData.find((r: Resume) => r.id === contextResume.id)
          if (foundResume) {
            setSelectedResumeId(contextResume.id)
          }
        }
        if (contextJob) {
          const foundJob = jobsData.find((j: JobDescription) => j.id === contextJob.id)
          if (foundJob) {
            setSelectedJobId(contextJob.id)
          }
        }
      } catch (error) {
        console.error('Failed to load data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [location.state])

  const handleResumeChange = (resumeId: string) => {
    setSelectedResumeId(resumeId)
    const resume = resumes.find((r: Resume) => r.id === resumeId)
    if (resume) setSelectedResume(resume)
  }

  const handleJobChange = (jobId: string) => {
    setSelectedJobId(jobId)
    const job = jobDescriptions.find((j: JobDescription) => j.id === jobId)
    if (job) setSelectedJobDescription(job)
  }

  const handleRunAnalysis = async () => {
    if (!selectedResumeId || !selectedJobId) {
      return
    }

    try {
      const result = await runAnalysis(selectedResumeId, selectedJobId)
      if (result) {
        navigate(`/analysis/${result.id}`)
      }
    } catch {
      // Error handled by hook
    }
  }

  if (loading) {
    return <LoadingSpinner message="Loading your data..." />
  }

  if (resumes.length === 0) {
    return (
      <EmptyState
        icon="📄"
        title="No Resumes Found"
        message="Upload a resume first to run analysis"
        action={{
          label: 'Upload Resume',
          onClick: () => navigate('/resume/upload'),
        }}
      />
    )
  }

  if (jobDescriptions.length === 0) {
    return (
      <EmptyState
        icon="💼"
        title="No Job Descriptions Found"
        message="Create a job description first to run analysis"
        action={{
          label: 'Create Job Description',
          onClick: () => navigate('/job/create'),
        }}
      />
    )
  }

  return (
    <div className="analysis-page">
      <Card title="Run Resume Analysis">
        {analyzing && <LoadingSpinner message="Analyzing your resume against the job description..." />}

        {error && !analyzing && <ErrorMessage message={error} />}

        {!analyzing && (
          <div className="analysis-form">
            <Select
              label="Select Resume"
              value={selectedResumeId}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => handleResumeChange(e.target.value)}
              disabled={analyzing}
              required
              options={[
                { value: '', label: 'Choose a resume...' },
                ...resumes.map((resume: Resume) => ({
                  value: resume.id,
                  label: resume.file_name,
                })),
              ]}
            />

            <Select
              label="Select Job Description"
              value={selectedJobId}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => handleJobChange(e.target.value)}
              disabled={analyzing}
              required
              options={[
                { value: '', label: 'Choose a job description...' },
                ...jobDescriptions.map((job: JobDescription) => ({
                  value: job.id,
                  label: job.title,
                })),
              ]}
            />

            <Button
              onClick={handleRunAnalysis}
              loading={analyzing}
              disabled={!selectedResumeId || !selectedJobId || analyzing}
              className="analysis-button"
            >
              Run Analysis
            </Button>
          </div>
        )}
      </Card>
    </div>
  )
}
