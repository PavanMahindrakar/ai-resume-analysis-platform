import { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react'
import { User } from '../types'
import { authService } from '../services/auth/authService'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
  showToast?: (message: string, type?: 'success' | 'error' | 'info' | 'warning', duration?: number) => void
}

export function AuthProvider({ children, showToast }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  // Decode JWT to get user info (simple implementation)
  const decodeToken = useCallback((token: string): User | null => {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return {
        id: payload.sub || '',
        email: payload.email || '',
        is_active: true,
      }
    } catch {
      return null
    }
  }, [])

  // Fetch user from token
  const fetchUserFromToken = useCallback(async () => {
    const token = localStorage.getItem('access_token')
    if (token) {
      const decodedUser = decodeToken(token)
      if (decodedUser) {
        setUser(decodedUser)
        return
      }
    }
    setUser(null)
  }, [decodeToken])

  useEffect(() => {
    fetchUserFromToken().finally(() => setLoading(false))
  }, [fetchUserFromToken])

  const login = async (email: string, password: string) => {
    try {
      const response = await authService.login(email, password)
      localStorage.setItem('access_token', response.access_token)
      await fetchUserFromToken()
      showToast?.('Welcome back!', 'success')
    } catch (error) {
      // Extract error message from axios interceptor or Error instance
      let errorMessage = 'Login failed'
      if (error && typeof error === 'object' && 'message' in error) {
        errorMessage = (error as { message: string }).message
      } else if (error instanceof Error) {
        errorMessage = error.message
      }
      showToast?.(errorMessage, 'error')
      throw error
    }
  }

  const register = async (email: string, password: string) => {
    try {
      await authService.register(email, password)
      const response = await authService.login(email, password)
      localStorage.setItem('access_token', response.access_token)
      await fetchUserFromToken()
      showToast?.('Account created successfully!', 'success')
    } catch (error) {
      // Extract error message from axios interceptor or Error instance
      let errorMessage = 'Registration failed'
      if (error && typeof error === 'object' && 'message' in error) {
        errorMessage = (error as { message: string }).message
      } else if (error instanceof Error) {
        errorMessage = error.message
      }
      showToast?.(errorMessage, 'error')
      throw error
    }
  }

  const logout = useCallback(() => {
    localStorage.removeItem('access_token')
    setUser(null)
    showToast?.('Logged out successfully', 'info')
  }, [showToast])

  const refreshUser = useCallback(async () => {
    await fetchUserFromToken()
  }, [fetchUserFromToken])

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        isAuthenticated: !!user,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
