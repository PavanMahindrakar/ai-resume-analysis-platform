import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import { AuthProviderWrapper } from './context/AuthProviderWrapper'
import { ToastProvider } from './context/ToastContext'
import { AnalysisProvider } from './context/AnalysisContext'
import { ThemeProvider } from './context/ThemeContext'
import './assets/styles/index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider>
        <ToastProvider>
          <AuthProviderWrapper>
            <AnalysisProvider>
              <App />
            </AnalysisProvider>
          </AuthProviderWrapper>
        </ToastProvider>
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
