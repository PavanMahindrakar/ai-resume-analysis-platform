export interface User {
  id: string
  email: string
  is_active: boolean
}

export interface AuthResponse {
  access_token: string
  token_type: string
  expires_in: number
}

export interface Resume {
  id: string
  file_name: string
  content_type: string
  text_length: number
  created_at: string
}

export interface JobDescription {
  id: string
  title: string
  description: string
  created_at: string
}

export interface AnalysisResult {
  id: string
  resume_id: string
  job_description_id: string
  match_score: number
  explanation: string
  matched_keywords: Record<string, {
    resume_keyword: string
    score: number
    match_type: 'exact' | 'partial'
  }>
  missing_keywords: string[]
}

export interface DashboardSummary {
  total_analyses: number
  average_match_score: number
  highest_match_score: number
  lowest_match_score: number
  most_common_missing_skills: Array<{
    skill: string
    count: number
    frequency: number
  }>
}

export interface AnalysisHistoryItem {
  id: string
  resume_id: string
  job_description_id: string
  match_score: number
  created_at: string
}

export interface DashboardHistory {
  analyses: AnalysisHistoryItem[]
  total: number
}
