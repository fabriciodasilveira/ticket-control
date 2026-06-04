"""
Rotas de tarefas
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models import User
from app.core.security import get_current_user

router = APIRouter()

@router.get("/")
async def list_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Listar tarefas"""
    return {"message": "Lista de tarefas - em implementação", "user_role": current_user.role}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task():
    """Criar nova tarefa"""
    return {"message": "Tarefa criada - em implementação"}
