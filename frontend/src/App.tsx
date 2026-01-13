import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import { LoadingSpinner } from './components/common/LoadingSpinner'
import Layout from './components/common/Layout'
import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import ResumeUploadPage from './pages/resume/ResumeUploadPage'
import JobDescriptionPage from './pages/job/JobDescriptionPage'
import AnalysisPage from './pages/analysis/AnalysisPage'
import AnalysisResultPage from './pages/analysis/AnalysisResultPage'
import './App.css'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { user, loading, isAuthenticated } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="route-loader">
        <LoadingSpinner message="Loading..." />
      </div>
    )
  }

  if (!isAuthenticated || !user) {
    // Preserve the attempted location for redirect after login
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <>{children}</>
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const { user, loading, isAuthenticated } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="route-loader">
        <LoadingSpinner message="Loading..." />
      </div>
    )
  }

  if (isAuthenticated && user) {
    // Redirect to the page they were trying to access, or dashboard
    const from = (location.state as any)?.from?.pathname || '/dashboard'
    return <Navigate to={from} replace />
  }

  return <>{children}</>
}

function App() {
  return (
    <>
      {/* Skip to main content link for screen readers */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <Routes>
        <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
        <Route path="/register" element={<PublicRoute><RegisterPage /></PublicRoute>} />
        
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="resume/upload" element={<ResumeUploadPage />} />
          <Route path="job/create" element={<JobDescriptionPage />} />
          <Route path="analysis" element={<AnalysisPage />} />
          <Route path="analysis/:id" element={<AnalysisResultPage />} />
        </Route>
      </Routes>
    </>
  )
}

export default App
