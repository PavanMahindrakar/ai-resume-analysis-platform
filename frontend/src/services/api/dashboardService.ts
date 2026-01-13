import { api } from '../../utils/api'
import { DashboardSummary, DashboardHistory } from '../../types'

export const dashboardService = {
  async getSummary(limit: number = 10): Promise<DashboardSummary> {
    const response = await api.get<DashboardSummary>('/dashboard/summary', {
      params: { limit },
    })
    return response.data
  },

  async getHistory(skip: number = 0, limit: number = 20): Promise<DashboardHistory> {
    const response = await api.get<DashboardHistory>('/dashboard/history', {
      params: { skip, limit },
    })
    return response.data
  },
}
