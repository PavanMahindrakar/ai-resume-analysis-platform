import React from 'react'
import clsx from 'clsx'
import './Card.css'

interface CardProps {
  children: React.ReactNode
  className?: string
  title?: string
  actions?: React.ReactNode
}

export function Card({ children, className, title, actions }: CardProps) {
  return (
    <div className={clsx('card', className)}>
      {(title || actions) && (
        <div className="card-header">
          {title && <h3 className="card-title">{title}</h3>}
          {actions && <div className="card-actions">{actions}</div>}
        </div>
      )}
      <div className="card-content">{children}</div>
    </div>
  )
}
