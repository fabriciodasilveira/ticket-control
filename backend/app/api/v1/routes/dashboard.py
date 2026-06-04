"""
Rotas de dashboard
"""

from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter()

@router.get("/metrics")
async def get_dashboard_metrics(current_user: User = Depends(get_current_user)):
    """Obter métricas do dashboard"""
    return {
        "tasks_completed": 0,
        "tasks_pending": 0,
        "tasks_overdue": 0,
        "sla_compliance": 0,
        "user_role": current_user.role
    }

@router.get("/charts/completion-rate")
async def get_completion_rate_chart():
    """Gráfico de taxa de conclusão"""
    return {"chart_type": "line", "data": []}

@router.get("/charts/tasks-by-status")
async def get_tasks_by_status_chart():
    """Gráfico de tarefas por status"""
    return {"chart_type": "pie", "data": []}

@router.get("/ranking/employees")
async def get_employee_ranking():
    """Ranking de colaboradores"""
    return {"ranking": []}

@router.get("/heatmap")
async def get_execution_heatmap():
    """Heatmap de execução"""
    return {"heatmap": []}
