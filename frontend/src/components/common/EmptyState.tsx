import React from 'react'
import './EmptyState.css'

interface EmptyStateProps {
  icon?: string
  title: string
  message: string
  action?: {
    label: string
    onClick: () => void
  }
}

export function EmptyState({ icon = '📭', title, message, action }: EmptyStateProps) {
  return (
    <div className="empty-state" role="status" aria-live="polite">
      <div className="empty-icon" aria-hidden="true">{icon}</div>
      <h3 className="empty-title">{title}</h3>
      <p className="empty-message">{message}</p>
      {action && (
        <button 
          className="empty-action" 
          onClick={action.onClick}
          aria-label={action.label}
        >
          {action.label}
        </button>
      )}
    </div>
  )
}
