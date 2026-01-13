import React from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { Button } from './Button'
import { ThemeToggle } from './ThemeToggle'
import './Layout.css'

export default function Layout() {
  const { user, logout } = useAuth()
  const location = useLocation()

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/resume/upload', label: 'Upload Resume', icon: '📄' },
    { path: '/job/create', label: 'Job Description', icon: '💼' },
    { path: '/analysis', label: 'Run Analysis', icon: '🔍' },
  ]

  return (
    <div className="layout">
      <nav className="sidebar">
        <div className="sidebar-header">
          <h1 className="sidebar-logo">AI Resume Intelligence</h1>
          <p className="sidebar-subtitle">Career Copilot</p>
        </div>

        <div className="sidebar-nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'nav-item-active' : ''}`}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </Link>
          ))}
        </div>

        <div className="sidebar-footer">
          <div className="user-info">
            <span className="user-email" title={user?.email}>{user?.email}</span>
          </div>
          <div className="footer-actions">
            <ThemeToggle />
            <Button variant="outline" size="sm" onClick={logout} aria-label="Logout">
              Logout
            </Button>
          </div>
        </div>
      </nav>

      <main id="main-content" className="main-content" tabIndex={-1}>
        <Outlet />
      </main>
    </div>
  )
}
