"""
Serviço de Log de Auditoria
"""

from sqlalchemy.orm import Session
from fastapi import Request
from datetime import datetime
import json

from app.models.audit_log import AuditLog, AuditAction
from app.models.user import User


async def log_audit_action(
    db: Session,
    user: User,
    action: str,
    entity_type: str,
    entity_id: str = None,
    old_values: dict = None,
    new_values: dict = None,
    request: Request = None
):
    """
    Registra uma ação no log de auditoria
    
    Args:
        db: Sessão do banco de dados
        user: Usuário que realizou a ação
        action: Tipo de ação (create, update, delete, login, logout, etc)
        entity_type: Tipo de entidade afetada
        entity_id: ID da entidade afetada
        old_values: Valores anteriores (para update)
        new_values: Valores novos (para create/update)
        request: Objeto Request para extrair IP e user agent
    """
    
    # Extrair informações da request
    ip_address = None
    user_agent = None
    device_info = None
    
    if request:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Tentar extrair info do dispositivo
        device_info = {
            "platform": request.headers.get("x-platform"),
            "app_version": request.headers.get("x-app-version"),
        }
    
    # Criar log entry
    audit_log = AuditLog(
        user_id=user.id,
        action=AuditAction(action.upper()),
        entity_type=entity_type,
        entity_id=entity_id,
        old_values=json.dumps(old_values) if old_values else None,
        new_values=json.dumps(new_values) if new_values else None,
        ip_address=ip_address,
        user_agent=user_agent,
        device_info=device_info,
        unit_id=user.unit_id,
    )
    
    db.add(audit_log)
    db.commit()
    
    return audit_log


async def log_mass_action(
    db: Session,
    user: User,
    action: str,
    entity_type: str,
    entity_ids: list,
    request: Request = None
):
    """
    Registra múltiplas ações em lote (mais eficiente)
    """
    
    ip_address = None
    user_agent = None
    
    if request:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
    
    # Criar único log entry com lista de IDs
    audit_log = AuditLog(
        user_id=user.id,
        action=AuditAction(action.upper()),
        entity_type=entity_type,
        entity_id=None,
        old_values=None,
        new_values={"entity_ids": entity_ids},
        ip_address=ip_address,
        user_agent=user_agent,
        unit_id=user.unit_id,
    )
    
    db.add(audit_log)
    db.commit()
    
    return audit_log
