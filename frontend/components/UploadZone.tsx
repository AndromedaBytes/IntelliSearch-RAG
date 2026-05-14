'use client'

import { useRef, useState } from 'react'
import { motion } from 'framer-motion'
import { Upload, File } from 'lucide-react'
import { FileInfo } from '@/types'

interface UploadZoneProps {
  onFileSelected: (file: File) => void
  isUploading: boolean
  ingestedFiles: FileInfo[]
}

export const UploadZone = ({ onFileSelected, isUploading, ingestedFiles }: UploadZoneProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [isDragOver, setIsDragOver] = useState(false)
  
  const supportedFormats = ['.pdf', '.png', '.jpg', '.jpeg', '.webp', '.mp3', '.wav', '.ogg', '.m4a']
  
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }
  
  const handleDragLeave = () => {
    setIsDragOver(false)
  }
  
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      const file = files[0]
      const ext = '.' + file.name.split('.').pop()?.toLowerCase()
      
      if (supportedFormats.includes(ext)) {
        onFileSelected(file)
      } else {
        alert(`Unsupported format. Supported: ${supportedFormats.join(', ')}`)
      }
    }
  }
  
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files
    if (files?.length) {
      onFileSelected(files[0])
    }
  }
  
  return (
    <div className="w-full">
      <motion.div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        animate={{ scale: isDragOver ? 1.01 : 1 }}
        className={`cursor-pointer rounded-2xl border border-dashed p-7 text-center transition-all ${
          isDragOver
            ? 'border-slate-300 bg-white/[0.06]'
            : 'border-white/10 bg-white/[0.03] hover:bg-white/[0.05]'
        }`}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept={supportedFormats.join(',')}
          onChange={handleFileSelect}
          disabled={isUploading}
        />
        
        <Upload className="w-8 h-8 mx-auto mb-4 text-zinc-400" />
        <h3 className="text-sm font-medium text-zinc-100">
          {isUploading ? 'Uploading...' : 'Drop file or click to upload'}
        </h3>
        <p className="mt-1 text-xs text-zinc-400">
          PDF, images (PNG, JPG, WEBP), or audio (MP3, WAV, OGG, M4A)
        </p>
      </motion.div>
      
      {ingestedFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Files</h4>
          {ingestedFiles.map((file, idx) => (
            <div key={idx} className="flex items-center gap-2 rounded-xl border border-white/5 bg-white/[0.03] px-3 py-2 text-xs">
              <File className="w-3 h-3 text-zinc-400" />
              <span className="text-zinc-300">{file.name}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
