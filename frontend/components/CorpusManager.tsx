'use client'

import { useEffect, useState } from 'react'
import { Trash2, AlertCircle, CheckCircle } from 'lucide-react'
import { CorpusFile } from '@/types'
import { getCorpusInfo, deleteCorpusFile, clearCorpus } from '@/lib/api'

interface CorpusManagerProps {
  onCorpusUpdated?: () => void
}

export const CorpusManager = ({ onCorpusUpdated }: CorpusManagerProps) => {
  const [files, setFiles] = useState<CorpusFile[]>([])
  const [totalDocs, setTotalDocs] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [deletingFile, setDeletingFile] = useState<string | null>(null)
  const [showClearConfirm, setShowClearConfirm] = useState(false)

  const loadCorpus = async () => {
    setLoading(true)
    setError('')
    try {
      const info = await getCorpusInfo()
      setFiles(info.files)
      setTotalDocs(info.total_documents)
    } catch (err: any) {
      setError(err.message || 'Failed to load corpus')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadCorpus()
  }, [])

  const handleDeleteFile = async (filename: string) => {
    setDeletingFile(filename)
    setError('')
    setSuccess('')
    try {
      const result = await deleteCorpusFile(filename)
      setSuccess(`Deleted ${filename} (${result.deleted_count} chunks removed)`)
      setFiles(files.filter(f => f.filename !== filename))
      setTotalDocs(result.remaining_documents)
      onCorpusUpdated?.()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err: any) {
      setError(err.message || 'Failed to delete file')
    } finally {
      setDeletingFile(null)
    }
  }

  const handleClearCorpus = async () => {
    setShowClearConfirm(false)
    setLoading(true)
    setError('')
    setSuccess('')
    try {
      const result = await clearCorpus()
      setSuccess(`Corpus cleared! Deleted ${result.deleted_count} documents`)
      setFiles([])
      setTotalDocs(0)
      onCorpusUpdated?.()
      setTimeout(() => setSuccess(''), 3000)
    } catch (err: any) {
      setError(err.message || 'Failed to clear corpus')
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateStr: string) => {
    if (!dateStr) return 'Unknown'
    try {
      return new Date(dateStr).toLocaleDateString()
    } catch {
      return 'Unknown'
    }
  }

  return (
    <div className="space-y-4">
      {/* Header with reload */}
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-zinc-200">Corpus Contents</h3>
        <button
          onClick={loadCorpus}
          disabled={loading}
          className="text-xs px-2 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-zinc-400 hover:text-zinc-300 disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {/* Total documents */}
      <div className="text-xs text-zinc-400">
        Total documents: <span className="text-zinc-200 font-medium">{totalDocs}</span>
      </div>

      {/* Error message */}
      {error && (
        <div className="flex items-start gap-2 rounded-lg border border-red-500/20 bg-red-500/5 p-3">
          <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-red-300">{error}</p>
        </div>
      )}

      {/* Success message */}
      {success && (
        <div className="flex items-start gap-2 rounded-lg border border-green-500/20 bg-green-500/5 p-3">
          <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-green-300">{success}</p>
        </div>
      )}

      {/* Files list */}
      {loading && !files.length ? (
        <div className="text-center py-6 text-xs text-zinc-400">Loading files...</div>
      ) : files.length === 0 ? (
        <div className="text-center py-6 text-xs text-zinc-500">No files in corpus</div>
      ) : (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {files.map((file) => (
            <div
              key={file.filename}
              className="flex items-center justify-between rounded-lg border border-white/5 bg-white/[0.03] p-3"
            >
              <div className="flex-1 min-w-0">
                <div className="text-xs font-medium text-zinc-200 truncate">
                  {file.filename}
                </div>
                <div className="text-xs text-zinc-500 mt-1">
                  {file.file_type} • {file.chunk_count} chunks • {formatDate(file.upload_date)}
                </div>
              </div>
              <button
                onClick={() => handleDeleteFile(file.filename)}
                disabled={deletingFile === file.filename}
                className="ml-3 flex-shrink-0 p-1 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 hover:text-red-300 disabled:opacity-50 transition"
                title="Delete this file"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Clear All button */}
      {files.length > 0 && (
        <div className="pt-4 border-t border-white/5">
          {!showClearConfirm ? (
            <button
              onClick={() => setShowClearConfirm(true)}
              className="w-full text-xs px-3 py-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 hover:text-red-300 font-medium transition"
            >
              Clear All Documents
            </button>
          ) : (
            <div className="space-y-2">
              <p className="text-xs text-red-300 font-medium">
                This will delete all {totalDocs} documents. This cannot be undone.
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => setShowClearConfirm(false)}
                  className="flex-1 text-xs px-3 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-zinc-300 transition"
                >
                  Cancel
                </button>
                <button
                  onClick={handleClearCorpus}
                  disabled={loading}
                  className="flex-1 text-xs px-3 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-white font-medium disabled:opacity-50 transition"
                >
                  {loading ? 'Clearing...' : 'Confirm Clear'}
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
