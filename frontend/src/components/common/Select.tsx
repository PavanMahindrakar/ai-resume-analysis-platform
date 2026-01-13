import React from 'react'
import clsx from 'clsx'
import './Select.css'

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  helperText?: string
  required?: boolean
  options: Array<{ value: string; label: string }>
}

export function Select({
  label,
  error,
  helperText,
  required,
  id,
  className,
  options,
  ...props
}: SelectProps) {
  const selectId = id || `select-${Math.random().toString(36).substring(7)}`
  const errorId = error ? `${selectId}-error` : undefined
  const helperId = helperText && !error ? `${selectId}-helper` : undefined

  return (
    <div className="select-wrapper">
      {label && (
        <label htmlFor={selectId} className="select-label">
          {label}
          {required && <span className="required-indicator" aria-label="required">*</span>}
        </label>
      )}
      <select
        id={selectId}
        className={clsx('select', error && 'select-error', className)}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? errorId : helperId}
        aria-required={required}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <span id={errorId} className="select-error-text" role="alert">
          {error}
        </span>
      )}
      {helperText && !error && (
        <span id={helperId} className="select-helper">
          {helperText}
        </span>
      )}
    </div>
  )
}
