import { api } from '../../utils/api'
import { AnalysisResult } from '../../types'

export const analysisService = {
  async runAnalysis(resumeId: string, jobDescriptionId: string): Promise<AnalysisResult> {
    const response = await api.post<AnalysisResult>('/analysis/run', {
      resume_id: resumeId,
      job_description_id: jobDescriptionId,
    })
    return response.data
  },

  async getAnalysis(id: string): Promise<AnalysisResult> {
    const response = await api.get<AnalysisResult>(`/analysis/${id}`)
    return response.data
  },
}
