import React from 'react'
import clsx from 'clsx'
import './Textarea.css'

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  helperText?: string
  showCharCount?: boolean
  maxLength?: number
  required?: boolean
}

export function Textarea({
  label,
  error,
  helperText,
  showCharCount = false,
  maxLength,
  required,
  id,
  className,
  value,
  ...props
}: TextareaProps) {
  const charCount = typeof value === 'string' ? value.length : 0
  const textareaId = id || `textarea-${Math.random().toString(36).substring(7)}`
  const errorId = error ? `${textareaId}-error` : undefined
  const helperId = helperText && !error ? `${textareaId}-helper` : undefined

  return (
    <div className="textarea-wrapper">
      {label && (
        <label htmlFor={textareaId} className="textarea-label">
          {label}
          {required && <span className="required-indicator" aria-label="required">*</span>}
        </label>
      )}
      <textarea
        id={textareaId}
        className={clsx('textarea', error && 'textarea-error', className)}
        maxLength={maxLength}
        value={value}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? errorId : helperId}
        aria-required={required}
        {...props}
      />
      <div className="textarea-footer">
        {error && (
          <span id={errorId} className="textarea-error-text" role="alert">
            {error}
          </span>
        )}
        {helperText && !error && (
          <span id={helperId} className="textarea-helper">
            {helperText}
          </span>
        )}
        {showCharCount && maxLength && (
          <span 
            className={clsx('textarea-count', charCount > maxLength * 0.9 && 'textarea-count-warning')}
            aria-live="polite"
          >
            {charCount} / {maxLength}
          </span>
        )}
      </div>
    </div>
  )
}
