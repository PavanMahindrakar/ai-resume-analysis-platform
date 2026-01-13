import { api } from '../../utils/api'
import { AuthResponse, User } from '../../types'

export const authService = {
  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/login', {
      email,
      password,
    })
    return response.data
  },

  async register(email: string, password: string): Promise<User> {
    const response = await api.post<User>('/auth/register', {
      email,
      password,
    })
    return response.data
  },
}
