"""
Rotas de usuários (CRUD)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse, UserFilter, UserRole
from app.core.security import get_current_user, get_current_admin_user, get_password_hash
from app.services.audit_log_service import log_audit_action

router = APIRouter()


@router.get("/", response_model=UserListResponse)
async def list_users(
    search: str = Query(None),
    role: UserRole = Query(None),
    unit_id: UUID = Query(None),
    is_active: bool = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar usuários com filtros e paginação"""
    
    query = db.query(User)
    
    # Aplicar filtros baseados no papel do usuário atual
    if current_user.role == "manager":
        # Gerente só vê usuários da sua unidade
        query = query.filter(User.unit_id == current_user.unit_id)
    elif current_user.role == "employee":
        # Funcionário só vê a si mesmo
        query = query.filter(User.id == current_user.id)
    
    # Filtros opcionais
    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) | 
            (User.email.ilike(f"%{search}%"))
        )
    
    if role:
        query = query.filter(User.role == role.value)
    
    if unit_id and current_user.role == "admin":
        query = query.filter(User.unit_id == unit_id)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    # Paginação
    total = query.count()
    offset = (page - 1) * page_size
    users = query.offset(offset).limit(page_size).all()
    
    return UserListResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter detalhes de um usuário específico"""
    
    # Verificar permissões
    if current_user.role == "employee" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente"
        )
    
    if current_user.role == "manager":
        user = db.query(User).filter(
            User.id == user_id,
            User.unit_id == current_user.unit_id
        ).first()
    else:
        user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Criar novo usuário (apenas admin)"""
    
    # Verificar se email já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Criar usuário
    user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        phone=user_data.phone,
        role=user_data.role.value,
        unit_id=user_data.unit_id,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Log auditoria
    await log_audit_action(
        db, current_user, "create", "user", 
        str(user.id), new_values=user_data.model_dump(), request=request
    )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualizar usuário"""
    
    # Verificar permissões
    if current_user.role == "employee" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente"
        )
    
    if current_user.role == "manager":
        user = db.query(User).filter(
            User.id == user_id,
            User.unit_id == current_user.unit_id
        ).first()
    else:
        user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Salvar valores antigos para auditoria
    old_values = {
        "full_name": user.full_name,
        "phone": user.phone,
        "role": user.role,
        "unit_id": str(user.unit_id) if user.unit_id else None,
        "is_active": user.is_active,
    }
    
    # Atualizar campos
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    # Log auditoria
    await log_audit_action(
        db, current_user, "update", "user",
        str(user.id), old_values=old_values, new_values=update_data, request=request
    )
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Excluir/desativar usuário (apenas admin)"""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Não permitir exclusão do próprio admin
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir sua própria conta"
        )
    
    # Soft delete
    from datetime import datetime
    user.deleted_at = datetime.utcnow()
    user.is_active = False
    db.commit()
    
    # Log auditoria
    await log_audit_action(
        db, current_user, "delete", "user",
        str(user.id), request=request
    )


@router.post("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager_or_admin)
):
    """Desativar usuário (admin ou manager)"""
    
    # Verificar permissões
    if current_user.role == "manager":
        user = db.query(User).filter(
            User.id == user_id,
            User.unit_id == current_user.unit_id
        ).first()
    else:
        user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    user.is_active = False
    user.refresh_token = None  # Invalidar tokens
    db.commit()
    
    # Log auditoria
    await log_audit_action(
        db, current_user, "update", "user",
        str(user.id), old_values={"is_active": True}, 
        new_values={"is_active": False}, request=request
    )
