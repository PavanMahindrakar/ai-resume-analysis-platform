import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for global error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Handle network errors
    if (!error.response) {
      return Promise.reject({
        message: 'Network error. Please check your connection.',
        isNetworkError: true,
      })
    }

    const status = error.response.status
    const data = error.response.data as any

    // Handle authentication errors
    if (status === 401) {
      localStorage.removeItem('access_token')
      // Don't redirect immediately - let the component handle it
      // This allows for better UX (showing toast, preserving state, etc.)
      return Promise.reject({
        ...error,
        isAuthError: true,
        message: data?.detail || 'Authentication required',
      })
    }

    // Handle validation errors
    if (status === 422) {
      return Promise.reject({
        ...error,
        isValidationError: true,
        message: data?.detail || 'Validation error',
        errors: data?.detail,
      })
    }

    // Handle server errors
    if (status >= 500) {
      return Promise.reject({
        ...error,
        isServerError: true,
        message: 'Server error. Please try again later.',
      })
    }

    // Handle 400 Bad Request errors (e.g., email already registered)
    if (status === 400) {
      return Promise.reject({
        ...error,
        message: data?.detail || 'Bad request. Please check your input.',
        response: error.response,
      })
    }

    // Handle other errors
    return Promise.reject({
      ...error,
      message: data?.detail || error.message || 'An error occurred',
      response: error.response,
    })
  }
)
