'use client'

import { useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Message } from '@/types'
import { MessageBubble } from './MessageBubble'
import { TypingIndicator } from './TypingIndicator'

interface ChatCanvasProps {
  messages: Message[]
  isTyping: boolean
}

export const ChatCanvas = ({ messages, isTyping }: ChatCanvasProps) => {
  const scrollRef = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages, isTyping])
  
  return (
    <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-6 space-y-4">
      {messages.length === 0 ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex h-full items-center justify-center"
        >
          <div className="max-w-2xl text-center">
            <motion.h2
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="mb-3 text-3xl font-semibold tracking-tight text-zinc-100"
            >
              Search your documents with grounded answers
            </motion.h2>
            
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="mx-auto mb-8 max-w-xl text-sm leading-6 text-zinc-400"
            >
              Upload files, ask a question, and get concise answers with citations. The similarity gate keeps responses grounded in your ingested content.
            </motion.p>
            
            <div className="grid grid-cols-2 gap-3">
              {[
                'Analyze PDFs',
                'Vision Analysis',
                'Audio Intelligence',
                'Cross-doc Synthesis',
              ].map((capability, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.5 + idx * 0.1 }}
                  className="rounded-xl border border-white/10 bg-white/[0.03] p-3 text-xs font-medium text-zinc-200 transition hover:bg-white/5"
                >
                  {capability}
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      ) : (
        <>
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          
          {isTyping && <TypingIndicator />}
        </>
      )}
    </div>
  )
}
