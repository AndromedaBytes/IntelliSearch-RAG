'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Message } from '@/types'
import { motion } from 'framer-motion'
import { CitationPill } from './CitationPill'
import { AlertCircle, Shield } from 'lucide-react'

interface MessageBubbleProps {
  message: Message
}

export const MessageBubble = ({ message }: MessageBubbleProps) => {
  const isUser = message.role === 'user'
  const emptyCorpus = message.content.includes('No documents have been ingested')
  
  const gateBlockedStyle = message.gateBlocked ? 'border-l-4 border-amber-500 bg-amber-900/20' : ''
  const errorStyle = message.error ? 'border-l-4 border-red-500 bg-red-900/20' : ''
  // Strip inline source information and metadata
  const cleanContent = message.content
    .replace(/\s*\[Source:.*?\]\s*/gi, '')
    .replace(/\s*\{[\s\S]*?\}\s*$/g, '')
    .trim()
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`mb-4 flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div
        className={`max-w-3xl px-4 py-3 rounded-lg ${
          isUser
            ? 'rounded-br-none bg-zinc-100 text-zinc-950'
            : `rounded-bl-none border border-white/10 bg-white/[0.03] text-zinc-100 ${gateBlockedStyle} ${errorStyle}`
        }`}
      >
        {message.gateBlocked && (
          <div className="flex items-center gap-2 mb-2 text-amber-200">
            <AlertCircle className="w-4 h-4" />
            <span className="text-xs font-medium">
              {emptyCorpus ? 'No ingested documents' : 'No relevant context found'}
            </span>
          </div>
        )}
        
        {message.error && (
          <div className="flex items-center gap-2 mb-2 text-red-200">
            <AlertCircle className="w-4 h-4" />
            <span className="text-xs font-medium">Error</span>
          </div>
        )}
        
        {!isUser && (
          <div className="mb-2 flex items-center gap-2 text-xs text-zinc-400">
            <Shield className="w-3 h-3" />
            <span>
              {message.analysisMode === 'full_document' 
                ? `Full document mode${message.autoModeEnabled ? ' (auto)' : ''}`
                : 'ChromaDB top-15'
              }
            </span>
            <span>•</span>
            <span>Llama 3.1 405B</span>
          </div>
        )}
        
        <div className="prose prose-invert max-w-none text-sm">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              p: ({ node, ...props }) => <p {...props} className="mb-2" />,
              ul: ({ node, ...props }) => <ul {...props} className="list-disc list-inside mb-2" />,
              ol: ({ node, ...props }) => <ol {...props} className="list-decimal list-inside mb-2" />,
              code: ({ node, inline, ...props }: any) =>
                inline ? (
                  <code {...props} className="bg-zinc-800 px-1 py-0.5 rounded text-xs" />
                ) : (
                  <code {...props} className="block bg-zinc-800 p-2 rounded my-2 text-xs overflow-x-auto" />
                ),
            }}
          >
            {cleanContent}
          </ReactMarkdown>
        </div>
        
        {message.citations && message.citations.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2 border-t border-white/5 pt-2">
            {message.citations.map((citation, idx) => (
              <CitationPill key={idx} citation={citation} />
            ))}
          </div>
        )}
        
        {message.similarity !== undefined && (
          <div className="mt-2 border-t border-white/5 pt-2">
            <div className="text-xs text-zinc-400">
              Similarity: {(message.similarity * 100).toFixed(1)}%
            </div>
            <div className="mt-1 h-1 w-full rounded bg-white/10">
              <div
                className="h-1 rounded bg-zinc-200 transition-all"
                style={{ width: `${Math.min(message.similarity * 100, 100)}%` }}
              />
            </div>
          </div>
        )}
        {/* Consolidated Sources Section */}
        {cleanContent !== message.content && (
          <div className="mt-3 border-t border-white/5 pt-2">
            <div className="text-xs text-zinc-300 font-semibold mb-2">Sources:</div>
            <div className="text-xs text-zinc-400 space-y-1">
              {Array.from(message.content.matchAll(/\[Source:(.*?)\|.*?Type:\s*(.*?)\|.*?Chunk:\s*(\d+)\]/g)).map((match, idx) => (
                <div key={idx} className="ml-2">
                  • {match[1].trim()} ({match[2].trim()}, chunk {match[3]})
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  )
}
