import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { Button } from '../../components/common/Button'
import { Input } from '../../components/common/Input'
import './AuthPage.css'

export default function RegisterPage() {
  const navigate = useNavigate()
  const { register } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [errors, setErrors] = useState<{
    email?: string
    password?: string
    confirmPassword?: string
    general?: string
  }>({})
  const [loading, setLoading] = useState(false)

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setEmail(value)
    if (value && !validateEmail(value)) {
      setErrors((prev) => ({ ...prev, email: 'Please enter a valid email address' }))
    } else {
      setErrors((prev) => ({ ...prev, email: undefined }))
    }
  }

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setPassword(value)
    if (value && value.length < 8) {
      setErrors((prev) => ({ ...prev, password: 'Password must be at least 8 characters' }))
    } else {
      setErrors((prev) => ({ ...prev, password: undefined }))
    }
    // Check password match
    if (confirmPassword && value !== confirmPassword) {
      setErrors((prev) => ({ ...prev, confirmPassword: 'Passwords do not match' }))
    } else {
      setErrors((prev) => ({ ...prev, confirmPassword: undefined }))
    }
  }

  const handleConfirmPasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setConfirmPassword(value)
    if (value && value !== password) {
      setErrors((prev) => ({ ...prev, confirmPassword: 'Passwords do not match' }))
    } else {
      setErrors((prev) => ({ ...prev, confirmPassword: undefined }))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrors({})

    // Validation
    if (!email) {
      setErrors((prev) => ({ ...prev, email: 'Email is required' }))
      return
    }
    if (!validateEmail(email)) {
      setErrors((prev) => ({ ...prev, email: 'Please enter a valid email address' }))
      return
    }
    if (!password) {
      setErrors((prev) => ({ ...prev, password: 'Password is required' }))
      return
    }
    if (password.length < 8) {
      setErrors((prev) => ({ ...prev, password: 'Password must be at least 8 characters' }))
      return
    }
    if (password !== confirmPassword) {
      setErrors((prev) => ({ ...prev, confirmPassword: 'Passwords do not match' }))
      return
    }

    setLoading(true)
    try {
      await register(email, password)
      navigate('/dashboard')
    } catch (error: unknown) {
      // Handle error message from axios interceptor or direct error
      let errorMessage = 'Registration failed. Please try again.'
      
      // Log error for debugging
      console.error('Registration error:', error)
      
      if (error && typeof error === 'object') {
        const err = error as { 
          message?: string
          response?: { 
            data?: { 
              detail?: string | string[]
            }
            status?: number
          }
        }
        
        // Check for axios error with response
        if (err.response?.data?.detail) {
          const detail = err.response.data.detail
          // Handle both string and array of errors (validation errors)
          if (Array.isArray(detail)) {
            errorMessage = detail.map((d: { msg?: string } | string) => 
              typeof d === 'string' ? d : d.msg || String(d)
            ).join(', ')
          } else {
            errorMessage = String(detail)
          }
        } else if (err.message) {
          errorMessage = err.message
        }
      } else if (error instanceof Error) {
        errorMessage = error.message
      }
      
      setErrors({
        general: errorMessage,
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <h1>Create Account</h1>
          <p>Get started with AI Resume Intelligence</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {errors.general && (
            <div className="auth-error-banner">{errors.general}</div>
          )}

          <Input
            type="email"
            label="Email"
            value={email}
            onChange={handleEmailChange}
            error={errors.email}
            placeholder="you@example.com"
            disabled={loading}
            autoComplete="email"
          />

          <Input
            type="password"
            label="Password"
            value={password}
            onChange={handlePasswordChange}
            error={errors.password}
            placeholder="At least 8 characters"
            disabled={loading}
            autoComplete="new-password"
            helperText="Must be at least 8 characters"
          />

          <Input
            type="password"
            label="Confirm Password"
            value={confirmPassword}
            onChange={handleConfirmPasswordChange}
            error={errors.confirmPassword}
            placeholder="Confirm your password"
            disabled={loading}
            autoComplete="new-password"
          />

          <Button type="submit" loading={loading} className="auth-submit">
            Create Account
          </Button>
        </form>

        <div className="auth-footer">
          <p>
            Already have an account? <Link to="/login">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
