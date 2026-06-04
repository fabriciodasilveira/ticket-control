import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'TaskManager - Gestão de Tarefas e Checklists',
  description: 'Sistema de gerenciamento de tarefas, checklists e auditorias operacionais para restaurantes',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  )
}
