'use client'

import { motion } from 'framer-motion'
import { Settings, AlertCircle } from 'lucide-react'
import { FileInfo } from '@/types'

interface SidebarProps {
  onNewChat: () => void
  onOpenSettings: () => void
  ingestedFiles: FileInfo[]
  healthStatus: 'online' | 'offline' | 'checking'
  latencyMs: number | null
}

export const Sidebar = ({
  onNewChat,
  onOpenSettings,
  ingestedFiles,
  healthStatus,
  latencyMs,
}: SidebarProps) => {
  return (
    <motion.div
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className="w-72 flex-shrink-0 border-r border-white/5 bg-[#0a0d14] flex flex-col p-4"
    >
      {/* Brand */}
      <div className="mb-6 rounded-2xl border border-white/5 bg-white/[0.03] p-4">
        <h1 className="text-sm font-semibold tracking-wide text-zinc-100">IntelliSearch</h1>
        <p className="mt-1 text-xs text-zinc-400">Private search workspace</p>
      </div>
      
      {/* New Chat Button */}
      <button
        onClick={onNewChat}
        className="mb-4 w-full rounded-xl border border-white/10 bg-zinc-100 px-4 py-2.5 text-sm font-medium text-zinc-950 transition hover:bg-white"
      >
        New chat
      </button>
      
      {/* Recent Sessions */}
      <div className="mb-6">
        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-zinc-400">Recent sessions</h3>
        <div className="space-y-1">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="cursor-pointer rounded-lg px-3 py-2 text-xs text-zinc-400 transition hover:bg-white/5 hover:text-zinc-200">
              Conversation {i}
            </div>
          ))}
        </div>
      </div>
      
      {/* Ingested Files */}
      {ingestedFiles.length > 0 && (
        <div className="mb-6">
          <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-zinc-400">Files</h3>
          <div className="max-h-44 space-y-1 overflow-y-auto pr-1">
            {ingestedFiles.map((file, idx) => (
              <div key={idx} className="flex items-center gap-2 rounded-lg border border-white/5 bg-white/[0.03] px-3 py-2 text-xs text-zinc-300">
                <div
                  className={`w-2 h-2 rounded-full ${
                    file.type === 'pdf'
                      ? 'bg-red-500'
                      : file.type === 'image'
                      ? 'bg-green-500'
                      : 'bg-purple-500'
                  }`}
                />
                <span className="truncate">{file.name}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Spacer */}
      <div className="flex-1" />
      
      {/* Health Status */}
      <div className="mt-auto border-t border-white/5 pt-4 mb-4">
        <div className="rounded-2xl border border-white/5 bg-white/[0.03] p-3 text-xs">
          <div className="flex items-center gap-2 mb-2">
            <div
              className={`w-2 h-2 rounded-full ${
                healthStatus === 'online' ? 'bg-green-500' : 'bg-red-500'
              }`}
            />
            <span className="text-zinc-300">
              {healthStatus === 'checking' ? 'Checking' : healthStatus === 'online' ? 'Online' : 'Offline'}
            </span>
          </div>
          {latencyMs && (
            <div className="text-zinc-400">
              Latency: {latencyMs}ms
            </div>
          )}
          <div className="mt-1 text-[10px] text-zinc-500">
            GPT-4o and Llama 3.1 405B
          </div>
        </div>
      </div>
      
      {/* Settings */}
      <button
        onClick={onOpenSettings}
        className="flex w-full items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-3 py-2.5 text-sm text-zinc-200 transition hover:bg-white/10"
      >
        <Settings className="w-4 h-4" />
        <span>Settings</span>
      </button>
    </motion.div>
  )
}
