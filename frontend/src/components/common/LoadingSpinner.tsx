import React from 'react'
import './LoadingSpinner.css'

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  message?: string
}

export function LoadingSpinner({ size = 'md', message }: LoadingSpinnerProps) {
  return (
    <div className="loading-container">
      <div className={`spinner spinner-${size}`} />
      {message && <p className="loading-message">{message}</p>}
    </div>
  )
}
