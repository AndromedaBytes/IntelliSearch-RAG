'use client'

import { useState, useCallback } from 'react'
import { Message, Toast, FileInfo, ToastType } from '@/types'
import { queryCorpus, ingestFile as ingestFileApi } from '@/lib/api'

const TOAST_DURATION = 4000

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isTyping, setIsTyping] = useState(false)
  const [ingestedFiles, setIngestedFiles] = useState<FileInfo[]>([])
  const [toasts, setToasts] = useState<Toast[]>([])
  
  const addToast = useCallback((message: string, type: ToastType = 'info') => {
    const id = Date.now().toString()
    const toast: Toast = { id, message, type, duration: TOAST_DURATION }
    
    setToasts((prev) => [...prev, toast])
    
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id))
    }, TOAST_DURATION)
  }, [])
  
  const sendMessage = useCallback(
    async (query: string) => {
      // Add user message immediately
      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: query,
        time: new Date(),
      }
      
      setMessages((prev) => [...prev, userMessage])
      setIsTyping(true)
      
      try {
        // Call API with optional client-side similarity threshold override
        let threshold: number | undefined = undefined
        let fullDocumentMode = false
        if (typeof window !== 'undefined') {
          const saved = localStorage.getItem('intellisearch_similarity_threshold')
          if (saved) {
            const parsed = parseFloat(saved)
            if (!Number.isNaN(parsed)) threshold = parsed
          }
          fullDocumentMode = localStorage.getItem('intellisearch_full_document_mode') === 'true'
        }

        const response = await queryCorpus(query, undefined, threshold, fullDocumentMode)
        
        // Create AI message
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'ai',
          content: response.answer,
          citations: response.citations,
          similarity: response.top_similarity,
          time: new Date(),
          gateBlocked: !response.gate_passed,
          analysisMode: fullDocumentMode || response.auto_full_document_enabled ? 'full_document' : 'retrieval',
          autoModeEnabled: response.auto_full_document_enabled,
        }
        
        setMessages((prev) => [...prev, aiMessage])
        
        if (!response.gate_passed) {
          addToast('Similarity gate blocked: insufficient context', 'warning')
        }
      } catch (error: any) {
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'ai',
          content: error.message || 'Failed to process query',
          time: new Date(),
          error: error.message,
        }
        
        setMessages((prev) => [...prev, errorMessage])
        
        if (error.message.includes('Rate limited')) {
          addToast('Rate limited - please try again', 'error')
        } else if (error.message.includes('GitHub token')) {
          addToast('GitHub token invalid', 'error')
        } else {
          addToast(`Error: ${error.message}`, 'error')
        }
      } finally {
        setIsTyping(false)
      }
    },
    [addToast]
  )
  
  const clearChat = useCallback(() => {
    setMessages([])
  }, [])
  
  const addFileToList = useCallback((file: FileInfo) => {
    setIngestedFiles((prev) => [...prev, file])
  }, [])
  
  const ingestFile = useCallback(
    async (file: File) => {
      try {
        await ingestFileApi(file)
      } catch (error: any) {
        throw error
      }
    },
    []
  )
  
  return {
    messages,
    isTyping,
    ingestedFiles,
    toasts,
    sendMessage,
    clearChat,
    addToast,
    addFileToList,
    ingestFile,
  }
}
