'use client'

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X } from 'lucide-react'
import { CorpusManager } from './CorpusManager'

interface SettingsModalProps {
  isOpen: boolean
  onClose: () => void
  onSave: (endpoint: string, similarityThreshold: number, fullDocumentMode: boolean) => void
  initialEndpoint: string
}

export const SettingsModal = ({
  isOpen,
  onClose,
  onSave,
  initialEndpoint,
}: SettingsModalProps) => {
  const [tab, setTab] = useState<'settings' | 'corpus'>('settings')
  const [endpoint, setEndpoint] = useState(initialEndpoint)
  const [similarityThreshold, setSimilarityThreshold] = useState<number>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('intellisearch_similarity_threshold')
      if (saved) {
        const parsed = parseFloat(saved)
        if (!Number.isNaN(parsed)) return parsed
      }
    }
    return 0.7
  })
  const [fullDocumentMode, setFullDocumentMode] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('intellisearch_full_document_mode') === 'true'
    }
    return false
  })

  useEffect(() => {
    if (isOpen) {
      setEndpoint(initialEndpoint)
      setTab('settings')
      if (typeof window !== 'undefined') {
        setFullDocumentMode(localStorage.getItem('intellisearch_full_document_mode') === 'true')
      }
    }
  }, [isOpen, initialEndpoint])
  
  const handleSave = () => {
    onSave(endpoint.trim(), similarityThreshold, fullDocumentMode)
    if (typeof window !== 'undefined') {
      localStorage.setItem('intellisearch_similarity_threshold', String(similarityThreshold))
      localStorage.setItem('intellisearch_full_document_mode', String(fullDocumentMode))
    }
    onClose()
  }
  
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/70 backdrop-blur-md z-40"
          />
          
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="w-full max-w-md rounded-2xl border border-white/10 bg-[#0f1520] p-6 shadow-2xl shadow-black/40"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-zinc-100">Settings</h2>
                <button
                  onClick={onClose}
                  className="text-zinc-400 hover:text-zinc-300"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Tabs */}
              <div className="flex gap-2 mb-6 border-b border-white/5">
                <button
                  onClick={() => setTab('settings')}
                  className={`px-4 py-2 text-sm font-medium border-b-2 transition ${
                    tab === 'settings'
                      ? 'text-zinc-100 border-zinc-400'
                      : 'text-zinc-500 border-transparent hover:text-zinc-400'
                  }`}
                >
                  Configuration
                </button>
                <button
                  onClick={() => setTab('corpus')}
                  className={`px-4 py-2 text-sm font-medium border-b-2 transition ${
                    tab === 'corpus'
                      ? 'text-zinc-100 border-zinc-400'
                      : 'text-zinc-500 border-transparent hover:text-zinc-400'
                  }`}
                >
                  Manage Corpus
                </button>
              </div>
            
              <div className="flex-1 overflow-y-auto space-y-4 max-h-80">
                {tab === 'settings' ? (
                  <>
                    <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-3">
                      <div className="text-xs font-medium text-emerald-200">Client auth</div>
                      <div className="text-xs text-emerald-300/80 mt-1">
                        Uses backend env key automatically. No frontend key input required.
                      </div>
                    </div>

                    <div className="rounded-xl border border-white/5 bg-white/[0.03] p-3">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <div className="text-xs font-medium text-zinc-100">Full document mode</div>
                          <div className="text-xs text-zinc-400 mt-1">
                            Send every chunk in the corpus to Llama instead of only the top-k matches.
                          </div>
                        </div>
                        <button
                          type="button"
                          onClick={() => setFullDocumentMode((value) => !value)}
                          className={`relative h-6 w-11 rounded-full border transition ${
                            fullDocumentMode ? 'border-emerald-400 bg-emerald-500/30' : 'border-white/10 bg-white/10'
                          }`}
                        >
                          <span
                            className={`absolute top-0.5 h-5 w-5 rounded-full bg-white transition ${
                              fullDocumentMode ? 'left-5' : 'left-0.5'
                            }`}
                          />
                        </button>
                      </div>
                    </div>
                    
                    {/* Endpoint */}
                    <div>
                      <label className="block text-sm font-medium text-zinc-300 mb-2">
                        Backend Endpoint
                      </label>
                      <input
                        type="text"
                        value={endpoint}
                        onChange={(e) => setEndpoint(e.target.value)}
                        placeholder="http://127.0.0.1:8000"
                        className="w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-1 focus:ring-slate-400"
                      />
                    </div>
                    
                    {/* Architecture Info */}
                    <div className="space-y-2 pt-4">
                      <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Architecture</h3>
                      
                      <div className="rounded-xl border border-white/5 bg-white/[0.03] p-3">
                        <div className="text-xs font-medium text-zinc-100">GPT-4o</div>
                        <div className="text-xs text-zinc-400">Perception engine, Token A</div>
                      </div>
                      
                      <div className="rounded-xl border border-white/5 bg-white/[0.03] p-3">
                        <div className="text-xs font-medium text-zinc-100">Llama 3.1 405B</div>
                        <div className="text-xs text-zinc-400">Logic engine, 128k context, Token B</div>
                      </div>
                      
                      <div className="rounded-xl border border-white/5 bg-white/[0.03] p-3">
                          <div className="text-xs font-medium text-zinc-100">Similarity gate</div>
                          <div className="flex items-center gap-3">
                            <div className="text-xs text-zinc-400">Threshold:</div>
                            <input
                              type="range"
                              min={0}
                              max={1}
                              step={0.01}
                              value={similarityThreshold}
                              onChange={(e) => setSimilarityThreshold(parseFloat(e.target.value))}
                              className="w-40"
                            />
                            <div className="text-xs text-zinc-200">{similarityThreshold.toFixed(2)}</div>
                          </div>
                      </div>
                    </div>
                  </>
                ) : (
                  <CorpusManager />
                )}
              </div>
            
              {/* Buttons */}
              {tab === 'settings' && (
                <div className="flex gap-3 mt-6">
                  <button
                    onClick={onClose}
                    className="flex-1 rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-zinc-200 transition hover:bg-white/10"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSave}
                    className="flex-1 rounded-xl bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-950 transition hover:bg-white"
                  >
                    Save Changes
                  </button>
                </div>
              )}
              
              {tab === 'corpus' && (
                <div className="flex gap-3 mt-6">
                  <button
                    onClick={onClose}
                    className="w-full rounded-xl bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-950 transition hover:bg-white"
                  >
                    Close
                  </button>
                </div>
              )}
            </motion.div>
            </div>
        </>
      )}
    </AnimatePresence>
  )
}
