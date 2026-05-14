'use client'

import { useState, useEffect } from 'react'
import { checkHealth, HealthResponse } from '@/lib/api'

export function useHealth() {
  const [status, setStatus] = useState<'checking' | 'online' | 'offline'>('checking')
  const [latencyMs, setLatencyMs] = useState<number | null>(null)
  const [corpusSize, setCorpusSize] = useState(0)
  const [models, setModels] = useState<HealthResponse['models'] | null>(null)
  
  useEffect(() => {
    let intervalId: NodeJS.Timeout | null = null
    
    const performHealthCheck = async () => {
      try {
        const start = Date.now()
        const response = await checkHealth()
        const latency = Date.now() - start
        
        setStatus('online')
        setLatencyMs(latency)
        setCorpusSize(response.corpus_size)
        setModels(response.models)
      } catch (error) {
        setStatus('offline')
        setLatencyMs(null)
      }
    }
    
    // Check immediately on mount
    performHealthCheck()
    
    // Set up polling every 15 seconds
    intervalId = setInterval(performHealthCheck, 15000)
    
    return () => {
      if (intervalId) {
        clearInterval(intervalId)
      }
    }
  }, [])
  
  return { status, latencyMs, corpusSize, models }
}
