import React from 'react'
import './Skeleton.css'

interface SkeletonProps {
  width?: string | number
  height?: string | number
  variant?: 'text' | 'circular' | 'rectangular'
  className?: string
}

export function Skeleton({ width, height, variant = 'rectangular', className }: SkeletonProps) {
  const style: React.CSSProperties = {
    width: width || '100%',
    height: height || '1rem',
  }

  return (
    <div
      className={`skeleton skeleton-${variant} ${className || ''}`}
      style={style}
    />
  )
}

export function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <Skeleton variant="rectangular" height={200} />
      <div className="skeleton-content">
        <Skeleton variant="text" width="60%" />
        <Skeleton variant="text" width="40%" />
        <Skeleton variant="text" width="80%" />
      </div>
    </div>
  )
}

export function SkeletonList({ count = 3 }: { count?: number }) {
  return (
    <div className="skeleton-list">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="skeleton-list-item">
          <Skeleton variant="circular" width={40} height={40} />
          <div className="skeleton-list-content">
            <Skeleton variant="text" width="60%" />
            <Skeleton variant="text" width="40%" />
          </div>
        </div>
      ))}
    </div>
  )
}
