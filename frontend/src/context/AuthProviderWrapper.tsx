import React, { ReactNode } from 'react'
import { AuthProvider } from './AuthContext'
import { useToast } from './ToastContext'

export function AuthProviderWrapper({ children }: { children: ReactNode }) {
  const { showToast } = useToast()
  return <AuthProvider showToast={showToast}>{children}</AuthProvider>
}
