'use client'

import { Toast, ToastType } from '@/types'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle, AlertCircle, Info, AlertTriangle, X } from 'lucide-react'

interface ToastNotificationProps {
  toasts: Toast[]
  onRemove: (id: string) => void
}

export const ToastNotification = ({ toasts, onRemove }: ToastNotificationProps) => {
  const icons: Record<ToastType, React.ReactNode> = {
    success: <CheckCircle className="w-4 h-4" />,
    error: <AlertCircle className="w-4 h-4" />,
    info: <Info className="w-4 h-4" />,
    warning: <AlertTriangle className="w-4 h-4" />,
  }
  
  const colors: Record<ToastType, string> = {
    success: 'bg-zinc-900/95 border-white/10 text-zinc-100',
    error: 'bg-zinc-900/95 border-white/10 text-zinc-100',
    info: 'bg-zinc-900/95 border-white/10 text-zinc-100',
    warning: 'bg-zinc-900/95 border-white/10 text-zinc-100',
  }
  
  return (
    <div className="fixed bottom-4 right-4 z-50 flex max-w-md flex-col gap-2">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className={`flex items-center gap-3 rounded-xl border px-4 py-3 shadow-lg shadow-black/20 ${colors[toast.type]}`}
          >
            {icons[toast.type]}
            <span className="flex-1 text-sm">{toast.message}</span>
            <button
              onClick={() => onRemove(toast.id)}
              className="text-current opacity-70 hover:opacity-100 transition"
            >
              <X className="w-4 h-4" />
            </button>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}
