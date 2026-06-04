"""
Rotas de setores
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_sectors():
    """Listar setores"""
    return {"message": "Lista de setores - em implementação"}
