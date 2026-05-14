import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'IntelliSearch V2',
  description: 'Cloud-Hybrid Multimodal RAG Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark antialiased">
      <body className="bg-zinc-950 text-zinc-100 font-sans h-screen overflow-hidden">
        {children}
      </body>
    </html>
  )
}
