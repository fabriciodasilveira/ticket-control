'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function Dashboard() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    completed: 0,
    overdue: 0,
  })

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/')
      return
    }

    // Carregar dados do usuário e estatísticas
    fetchDashboardData(token)
  }, [router])

  const fetchDashboardData = async (token: string) => {
    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
      
      // Buscar dados do usuário
      const userResponse = await fetch(`${api_url}/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (userResponse.ok) {
        const userData = await userResponse.json()
        setUser(userData)
      }

      // Buscar estatísticas do dashboard
      const statsResponse = await fetch(`${api_url}/dashboard/stats`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (statsResponse.ok) {
        const statsData = await statsResponse.json()
        setStats(statsData)
      }
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/')
  }

  if (!user) {
    return <div className="min-h-screen flex items-center justify-center">Carregando...</div>
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">{user.full_name} ({user.role})</span>
            <button
              onClick={handleLogout}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
            >
              Sair
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Total de Tarefas</h3>
            <p className="text-3xl font-bold text-gray-900 mt-2">{stats.total}</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Pendentes</h3>
            <p className="text-3xl font-bold text-yellow-600 mt-2">{stats.pending}</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Concluídas</h3>
            <p className="text-3xl font-bold text-green-600 mt-2">{stats.completed}</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Atrasadas</h3>
            <p className="text-3xl font-bold text-red-600 mt-2">{stats.overdue}</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Ações Rápidas</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {user.role === 'admin' && (
              <>
                <button className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition">
                  <p className="font-semibold text-gray-700">Criar Tarefa</p>
                  <p className="text-sm text-gray-500">Nova tarefa operacional</p>
                </button>
                <button className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition">
                  <p className="font-semibold text-gray-700">Criar Checklist</p>
                  <p className="text-sm text-gray-500">Novo checklist de auditoria</p>
                </button>
                <button className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition">
                  <p className="font-semibold text-gray-700">Gerenciar Usuários</p>
                  <p className="text-sm text-gray-500">Cadastrar e editar usuários</p>
                </button>
              </>
            )}
            <button className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition">
              <p className="font-semibold text-gray-700">Minhas Tarefas</p>
              <p className="text-sm text-gray-500">Visualizar tarefas atribuídas</p>
            </button>
            <button className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition">
              <p className="font-semibold text-gray-700">Relatórios</p>
              <p className="text-sm text-gray-500">Exportar dados e métricas</p>
            </button>
            <button className="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition">
              <p className="font-semibold text-gray-700">QR Codes</p>
              <p className="text-sm text-gray-500">Gerar QR Codes por área</p>
            </button>
          </div>
        </div>

        {/* Recent Tasks */}
        <div className="mt-8 bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Tarefas Recentes</h2>
          <div className="text-center py-12 text-gray-500">
            <p>Nenhuma tarefa recente para exibir</p>
            <p className="text-sm mt-2">Comece criando novas tarefas ou checklists</p>
          </div>
        </div>
      </main>
    </div>
  )
}
