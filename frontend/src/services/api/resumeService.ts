import { api } from '../../utils/api'
import { Resume } from '../../types'

export const resumeService = {
  async uploadResume(file: File): Promise<Resume> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post<Resume>('/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async getResumes(): Promise<Resume[]> {
    const response = await api.get<Resume[]>('/resumes')
    return response.data
  },
}
