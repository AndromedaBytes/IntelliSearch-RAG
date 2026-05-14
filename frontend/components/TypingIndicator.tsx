'use client'

export const TypingIndicator = () => {
  return (
    <div className="flex items-center gap-2">
      <div className="flex gap-1">
        <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
        <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
        <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
      </div>
      <span className="text-sm text-zinc-400">Thinking...</span>
    </div>
  )
}
