import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useJobDescription } from '../../hooks/useJobDescription'
import { Card } from '../../components/common/Card'
import { Input } from '../../components/common/Input'
import { Textarea } from '../../components/common/Textarea'
import { Button } from '../../components/common/Button'
import { LoadingSpinner } from '../../components/common/LoadingSpinner'
import { ErrorMessage } from '../../components/common/ErrorMessage'
import './JobDescriptionPage.css'

const ROLE_OPTIONS = [
  'Software Engineer',
  'Frontend Developer',
  'Backend Developer',
  'Full Stack Developer',
  'DevOps Engineer',
  'Data Scientist',
  'Product Manager',
  'UX Designer',
  'Other',
]

export default function JobDescriptionPage() {
  const navigate = useNavigate()
  const { createJobDescription, saving, error, draft, setDraft, autoSaved } = useJobDescription()
  const [selectedRole, setSelectedRole] = useState('')

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDraft({ ...draft, title: e.target.value })
  }

  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setDraft({ ...draft, description: e.target.value })
  }

  const handleRoleSelect = (role: string) => {
    setSelectedRole(role)
    if (role !== 'Other') {
      setDraft({ ...draft, title: role })
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!draft.title.trim()) {
      return
    }
    if (!draft.description.trim()) {
      return
    }

    try {
      const result = await createJobDescription(draft.title, draft.description)
      navigate('/analysis', { state: { jobDescriptionId: result.id } })
    } catch {
      // Error handled by hook
    }
  }

  const isFormValid = draft.title.trim() && draft.description.trim()

  return (
    <div className="job-description-page">
      <Card title="Create Job Description">
        {saving && <LoadingSpinner message="Saving job description..." />}

        {error && !saving && <ErrorMessage message={error} />}

        {!saving && (
          <form onSubmit={handleSubmit} className="job-form">
            {autoSaved && (
              <div className="auto-save-indicator">
                💾 Draft auto-saved
              </div>
            )}

            <div className="role-selector">
              <label className="role-label">Quick Select Role:</label>
              <div className="role-buttons">
                {ROLE_OPTIONS.map((role) => (
                  <button
                    key={role}
                    type="button"
                    className={`role-button ${selectedRole === role ? 'role-button-active' : ''}`}
                    onClick={() => handleRoleSelect(role)}
                    disabled={saving}
                  >
                    {role}
                  </button>
                ))}
              </div>
            </div>

            <Input
              label="Job Title"
              value={draft.title}
              onChange={handleTitleChange}
              placeholder="e.g., Senior Software Engineer"
              required
              disabled={saving}
            />

            <Textarea
              label="Job Description"
              value={draft.description}
              onChange={handleDescriptionChange}
              placeholder="Paste the full job description here..."
              showCharCount
              maxLength={10000}
              required
              rows={12}
              disabled={saving}
            />

            <div className="form-actions">
              <Button
                type="submit"
                loading={saving}
                disabled={!isFormValid || saving}
              >
                Save & Continue
              </Button>
            </div>
          </form>
        )}
      </Card>
    </div>
  )
}
