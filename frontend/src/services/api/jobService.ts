import { api } from '../../utils/api'
import { JobDescription } from '../../types'

export const jobService = {
  async createJobDescription(title: string, description: string): Promise<JobDescription> {
    const response = await api.post<JobDescription>('/job-description/create', {
      title,
      description,
    })
    return response.data
  },

  async getJobDescriptions(): Promise<JobDescription[]> {
    const response = await api.get<JobDescription[]>('/job-descriptions')
    return response.data
  },
}
