import React, { useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDropzone } from 'react-dropzone'
import { useResumeUpload } from '../../hooks/useResumeUpload'
import { Card } from '../../components/common/Card'
import { Button } from '../../components/common/Button'
import { LoadingSpinner } from '../../components/common/LoadingSpinner'
import { ErrorMessage } from '../../components/common/ErrorMessage'
import './ResumeUploadPage.css'

export default function ResumeUploadPage() {
  const navigate = useNavigate()
  const { uploadResume, uploading, uploadProgress, error, resume, reset } = useResumeUpload()

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        try {
          await uploadResume(acceptedFiles[0])
        } catch {
          // Error handled by hook
        }
      }
    },
    [uploadResume]
  )

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    disabled: uploading,
  })

  const handleReset = () => {
    reset()
  }

  return (
    <div className="resume-upload-page">
      <Card title="Upload Resume">
        {uploading && (
          <div className="upload-progress">
            <LoadingSpinner message="Uploading and processing your resume..." />
            <div className="progress-bar-container">
              <div
                className="progress-bar"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
            <p className="progress-text">{uploadProgress}%</p>
          </div>
        )}

        {error && !uploading && (
          <ErrorMessage message={error} onRetry={handleReset} />
        )}

        {resume && !uploading && (
          <div className="upload-success">
            <div className="success-icon">✅</div>
            <h3>Resume Uploaded Successfully!</h3>
            <div className="resume-info">
              <p><strong>File:</strong> {resume.file_name}</p>
              <p><strong>Text Extracted:</strong> {resume.text_length.toLocaleString()} characters</p>
            </div>
            <div className="success-actions">
              <Button onClick={() => navigate('/job/create')}>
                Create Job Description
              </Button>
              <Button variant="outline" onClick={handleReset}>
                Upload Another
              </Button>
            </div>
          </div>
        )}

        {!resume && !uploading && !error && (
          <div
            {...getRootProps()}
            className={`dropzone ${isDragActive ? 'dropzone-active' : ''}`}
          >
            <input {...getInputProps()} />
            <div className="dropzone-content">
              <div className="dropzone-icon">📄</div>
              {isDragActive ? (
                <p className="dropzone-text">Drop your PDF resume here...</p>
              ) : (
                <>
                  <p className="dropzone-text">
                    Drag and drop your PDF resume here, or click to select
                  </p>
                  <p className="dropzone-hint">Only PDF files are accepted</p>
                </>
              )}
            </div>
          </div>
        )}

        {fileRejections.length > 0 && (
          <div className="file-rejection">
            <p>⚠️ Invalid file type. Please upload a PDF file.</p>
          </div>
        )}
      </Card>
    </div>
  )
}
