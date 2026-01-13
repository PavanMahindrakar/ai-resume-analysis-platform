import React from 'react'
import clsx from 'clsx'
import './Input.css'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
  required?: boolean
}

export function Input({ 
  label, 
  error, 
  helperText, 
  required,
  id,
  className, 
  ...props 
}: InputProps) {
  const inputId = id || `input-${Math.random().toString(36).substring(7)}`
  const errorId = error ? `${inputId}-error` : undefined
  const helperId = helperText && !error ? `${inputId}-helper` : undefined

  return (
    <div className="input-wrapper">
      {label && (
        <label htmlFor={inputId} className="input-label">
          {label}
          {required && <span className="required-indicator" aria-label="required">*</span>}
        </label>
      )}
      <input
        id={inputId}
        className={clsx('input', error && 'input-error', className)}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? errorId : helperId}
        aria-required={required}
        {...props}
      />
      {error && (
        <span id={errorId} className="input-error-text" role="alert">
          {error}
        </span>
      )}
      {helperText && !error && (
        <span id={helperId} className="input-helper">
          {helperText}
        </span>
      )}
    </div>
  )
}
