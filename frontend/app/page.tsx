'use client'

import { useState, useRef, useEffect } from 'react'
import { Sidebar } from '@/components/Sidebar'
import { ChatCanvas } from '@/components/ChatCanvas'
import { UploadZone } from '@/components/UploadZone'
import { SettingsModal } from '@/components/SettingsModal'
import { ToastNotification } from '@/components/ToastNotification'
import { useChat } from '@/hooks/useChat'
import { useHealth } from '@/hooks/useHealth'
import { Send, Paperclip } from 'lucide-react'

export default function Page() {
  const {
    messages,
    isTyping,
    toasts,
    ingestedFiles,
    sendMessage,
    clearChat,
    addToast,
    addFileToList,
    ingestFile,
  } = useChat()
  
  const { status: healthStatus, latencyMs } = useHealth()
  
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [queryInput, setQueryInput] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [showUpload, setShowUpload] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  
  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 144) + 'px'
    }
  }, [queryInput])
  
  const handleSendMessage = async () => {
    if (!queryInput.trim() || isTyping) return
    
    const query = queryInput.trim()
    setQueryInput('')
    
    await sendMessage(query)
  }
  
  const handleFileSelected = async (file: File) => {
    setIsUploading(true)
    try {
      await ingestFile(file)
      addFileToList({
        name: file.name,
        type: (file.type.includes('pdf') ? 'pdf' : 
                file.type.includes('audio') ? 'audio' : 'image') as 'pdf' | 'image' | 'audio',
        size: file.size,
      })
      addToast(`${file.name} uploaded successfully`, 'success')
    } catch (error: any) {
      if (error.message.includes('Rate limited')) {
        addToast('GPT-4o rate limit reached - try again shortly', 'error')
      } else {
        addToast(`Failed to ingest ${file.name}: ${error.message}`, 'error')
      }
    } finally {
      setIsUploading(false)
      setShowUpload(false)
    }
  }
  
  const handleRemoveToast = (id: string) => {
    // Toast management handled by hook
  }
  
  return (
    <div className="flex h-screen bg-[#0b0f17] text-zinc-100">
      {/* Sidebar */}
      <Sidebar
        onNewChat={clearChat}
        onOpenSettings={() => setSettingsOpen(true)}
        ingestedFiles={ingestedFiles}
        healthStatus={healthStatus as 'online' | 'offline' | 'checking'}
        latencyMs={latencyMs}
      />
      
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <header className="border-b border-white/5 bg-white/[0.02] px-6 py-4 backdrop-blur-sm">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-sm font-semibold tracking-wide text-zinc-100">IntelliSearch</h2>
              <p className="text-xs text-zinc-400">Private document search with retrieval and citations</p>
            </div>
            <div className="flex items-center gap-3 text-xs text-zinc-400">
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1">Llama 3.1 405B</span>
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1">Gate 0.70</span>
            </div>
          </div>
        </header>

        {/* Chat Canvas */}
        <ChatCanvas messages={messages} isTyping={isTyping} />
        
        {/* Upload & Input Area */}
        <div className="border-t border-white/5 bg-[#0d131d]/90 p-4 space-y-4">
          {/* Upload Zone - Toggle */}
          {showUpload && (
            <div className="animate-in">
              <UploadZone
                onFileSelected={handleFileSelected}
                isUploading={isUploading}
                ingestedFiles={ingestedFiles}
              />
            </div>
          )}
          
          {/* Chat Input */}
          <div className="space-y-2">
            <div className="flex gap-2">
              <textarea
                ref={textareaRef}
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleSendMessage()
                  }
                }}
                placeholder="Ask a question about your documents..."
                disabled={isTyping}
                className="flex-1 min-h-11 max-h-36 resize-none rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-slate-400 disabled:opacity-50"
                rows={1}
              />
              
              <button
                onClick={handleSendMessage}
                disabled={!queryInput.trim() || isTyping}
                className="inline-flex items-center gap-2 rounded-xl bg-zinc-100 px-4 py-3 text-sm font-medium text-zinc-950 transition hover:bg-white disabled:cursor-not-allowed disabled:bg-zinc-700 disabled:text-zinc-400"
              >
                <Send className="w-4 h-4" />
              </button>
              
              <button
                onClick={() => setShowUpload(!showUpload)}
                className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-zinc-300 transition hover:bg-white/10"
              >
                <Paperclip className="w-4 h-4" />
                Attach
              </button>
            </div>
            
            {/* Footer Info */}
            <div className="flex items-center justify-between text-xs text-zinc-400">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-400" />
                <span>top_k=15 • gate&gt;=0.70</span>
              </div>
              <span>{queryInput.length}/2000</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Settings Modal */}
      <SettingsModal
        isOpen={settingsOpen}
        onClose={() => setSettingsOpen(false)}
        onSave={(endpoint, similarityThreshold, fullDocumentMode) => {
          if (typeof window !== 'undefined') {
            localStorage.setItem('intellisearch_similarity_threshold', String(similarityThreshold))
            localStorage.setItem('intellisearch_full_document_mode', String(fullDocumentMode))
          }
          // Endpoint handling could be added to context
        }}
        initialEndpoint="http://127.0.0.1:8000"
      />
      
      {/* Toasts */}
      <ToastNotification toasts={toasts} onRemove={handleRemoveToast} />
    </div>
  )
}

