'use client'

import { Citation } from '@/types'

interface CitationPillProps {
  citation: Citation
}

export const CitationPill = ({ citation }: CitationPillProps) => {
  const typeColors = {
    pdf: 'bg-red-900/20 text-red-200 border-red-800',
    image: 'bg-green-900/20 text-green-200 border-green-800',
    audio: 'bg-purple-900/20 text-purple-200 border-purple-800',
  }
  
  const color = typeColors[citation.type as keyof typeof typeColors] || typeColors.pdf
  
  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium border ${color}`}>
      <span>{citation.source}</span>
      <span className="opacity-70">({citation.similarity_score.toFixed(2)})</span>
    </div>
  )
}
