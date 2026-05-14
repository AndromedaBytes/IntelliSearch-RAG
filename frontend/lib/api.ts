'use client'

import { HealthResponse, IngestResponse, QueryResponse, CorpusInfo, DeleteResponse } from '@/types'

const BASE_URL = 'http://127.0.0.1:8000'

function getHeaders(clientKey?: string) {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }
  
  if (clientKey) {
    headers['X-IntelliSearch-Client-Key'] = clientKey
  }
  
  return headers
}

export async function checkHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch(`${BASE_URL}/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    
    if (!response.ok) throw new Error(`Health check failed: ${response.status}`)
    return await response.json()
  } catch (error) {
    throw error
  }
}

export async function ingestFile(
  file: File,
  clientKey?: string
): Promise<IngestResponse> {
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await fetch(`${BASE_URL}/ingest/`, {
      method: 'POST',
      headers: clientKey ? { 'X-IntelliSearch-Client-Key': clientKey } : undefined,
      body: formData,
    })
    
    if (response.status === 403) {
      throw new Error('Invalid client key')
    }
    if (response.status === 429) {
      throw new Error('Rate limited')
    }
    const data = await response.json().catch(() => null)

    if (!response.ok) {
      const detail = typeof data?.detail === 'string' ? data.detail : `Ingest failed: ${response.status}`
      throw new Error(detail)
    }
    if (!data || data.status !== 'success' || data.chunks_stored <= 0) {
      throw new Error(data?.detail || data?.status || 'Ingest did not store any searchable content')
    }
    
    return data
  } catch (error) {
    throw error
  }
}

export async function queryCorpus(
  query: string,
  clientKey?: string,
  similarityThreshold?: number,
  fullDocumentMode?: boolean
): Promise<QueryResponse> {
  try {
    const response = await fetch(`${BASE_URL}/query/`, {
      method: 'POST',
      headers: getHeaders(clientKey),
      body: JSON.stringify({
        query,
        similarity_threshold: similarityThreshold,
        full_document_mode: fullDocumentMode,
      }),
    })
    
    if (response.status === 403) {
      throw new Error('Invalid client key')
    }
    if (response.status === 429) {
      throw new Error('Rate limited')
    }
    if (response.status === 401) {
      throw new Error('GitHub token invalid')
    }
    if (!response.ok) throw new Error(`Query failed: ${response.status}`)
    
    return await response.json()
  } catch (error) {
    throw error
  }
}

// Re-export types for convenience
export type { HealthResponse } from '@/types'

export async function getCorpusInfo(clientKey?: string): Promise<CorpusInfo> {
  try {
    const response = await fetch(`${BASE_URL}/query/corpus/info`, {
      method: 'GET',
      headers: getHeaders(clientKey),
    })
    
    if (response.status === 403) {
      throw new Error('Invalid client key')
    }
    if (!response.ok) throw new Error(`Failed to get corpus info: ${response.status}`)
    
    return await response.json()
  } catch (error) {
    throw error
  }
}

export async function deleteCorpusFile(filename: string, clientKey?: string): Promise<DeleteResponse> {
  try {
    const response = await fetch(`${BASE_URL}/query/corpus/files/${encodeURIComponent(filename)}`, {
      method: 'DELETE',
      headers: getHeaders(clientKey),
    })
    
    if (response.status === 403) {
      throw new Error('Invalid client key')
    }
    if (!response.ok) throw new Error(`Failed to delete file: ${response.status}`)
    
    return await response.json()
  } catch (error) {
    throw error
  }
}

export async function clearCorpus(clientKey?: string): Promise<DeleteResponse> {
  try {
    const response = await fetch(`${BASE_URL}/query/corpus`, {
      method: 'DELETE',
      headers: getHeaders(clientKey),
    })
    
    if (response.status === 403) {
      throw new Error('Invalid client key')
    }
    if (!response.ok) throw new Error(`Failed to clear corpus: ${response.status}`)
    
    return await response.json()
  } catch (error) {
    throw error
  }
}
