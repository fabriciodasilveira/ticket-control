"""
Rotas de checklists
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_checklists():
    """Listar checklists"""
    return {"message": "Lista de checklists - em implementação"}
