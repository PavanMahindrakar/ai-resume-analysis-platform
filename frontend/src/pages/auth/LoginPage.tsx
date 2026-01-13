import React, { useState } from 'react'
import { useNavigate, Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { Button } from '../../components/common/Button'
import { Input } from '../../components/common/Input'
import './AuthPage.css'

export default function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState<{ email?: string; password?: string; general?: string }>({})
  const [loading, setLoading] = useState(false)

  // Get redirect location from state
  interface LocationState {
    from?: {
      pathname: string
    }
  }
  const from = (location.state as LocationState)?.from?.pathname || '/dashboard'

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setEmail(value)
    // Real-time validation
    if (value && !validateEmail(value)) {
      setErrors((prev: { email?: string; password?: string; general?: string }) => ({ ...prev, email: 'Please enter a valid email address' }))
    } else {
      setErrors((prev: { email?: string; password?: string; general?: string }) => ({ ...prev, email: undefined }))
    }
  }

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setPassword(value)
    // Real-time validation
    if (value && value.length < 8) {
      setErrors((prev: { email?: string; password?: string; general?: string }) => ({ ...prev, password: 'Password must be at least 8 characters' }))
    } else {
      setErrors((prev: { email?: string; password?: string; general?: string }) => ({ ...prev, password: undefined }))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrors({})

    // Validation
    if (!email) {
      setErrors((prev: { email?: string; password?: string; general?: string }) => ({ ...prev, email: 'Email is required' }))
      return
    }
    if (!validateEmail(email)) {
      setErrors((prev: { email?: string; password?: string; general?: string }) => ({ ...prev, email: 'Please enter a valid email address' }))
      return
    }
    if (!password) {
      setErrors((prev: { email?: string; password?: string; general?: string }) => ({ ...prev, password: 'Password is required' }))
      return
    }

    setLoading(true)
    try {
      await login(email, password)
      // Navigate to the page they were trying to access, or dashboard
      navigate(from, { replace: true })
    } catch (error: unknown) {
      // Handle error message from axios interceptor or direct error
      let errorMessage = 'Login failed. Please try again.'
      
      // Log error for debugging
      console.error('Login error:', error)
      
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
          <h1>Welcome Back</h1>
          <p>Sign in to your account</p>
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
            placeholder="Enter your password"
            disabled={loading}
            autoComplete="current-password"
          />

          <Button type="submit" loading={loading} className="auth-submit">
            Sign In
          </Button>
        </form>

        <div className="auth-footer">
          <p>
            Don't have an account? <Link to="/register">Sign up</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
