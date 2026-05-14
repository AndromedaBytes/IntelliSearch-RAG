'use client'

// API Response Types
export interface Citation {
  source: string
  type: string
  chunk_id: number
  similarity_score: number
}

export interface IngestResponse {
  status: 'success' | 'error'
  filename: string
  chunks_stored: number
  file_type: string
}

export interface QueryRequest {
  query: string
  similarity_threshold?: number
  full_document_mode?: boolean
}

export interface QueryResponse {
  answer: string
  citations: Citation[]
  top_similarity: number
  gate_passed: boolean
  model_used: string
  auto_full_document_enabled?: boolean
}

export interface HealthResponse {
  status: string
  chromadb_connected: boolean
  corpus_size: number
  models: {
    gpt4o: string
    llama: string
    github_models: string
  }
}

export interface CorpusFile {
  filename: string
  file_type: string
  chunk_count: number
  upload_date: string
}

export interface CorpusInfo {
  total_documents: number
  files: CorpusFile[]
}

export interface DeleteResponse {
  status: 'success' | 'error'
  deleted_count: number
  remaining_documents: number
}

// UI Types
export interface Message {
  id: string
  role: 'user' | 'ai'
  content: string
  citations?: Citation[]
  similarity?: number
  time: Date
  gateBlocked?: boolean
  error?: string
  analysisMode?: 'retrieval' | 'full_document'
  autoModeEnabled?: boolean
}

export interface FileInfo {
  name: string
  type: 'pdf' | 'image' | 'audio'
  size: number
}

export type ToastType = 'success' | 'error' | 'info' | 'warning'

export interface Toast {
  id: string
  message: string
  type: ToastType
  duration?: number
}
