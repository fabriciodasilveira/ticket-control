"""
Rotas de unidades/lojas
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_units():
    """Listar unidades/lojas"""
    return {"message": "Lista de unidades - em implementação"}
