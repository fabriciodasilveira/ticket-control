"""
Módulo core da aplicação
"""

from app.core.config import settings, get_settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
    get_current_manager_or_admin,
)
from app.core.exceptions import (
    APIException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    BadRequestException,
    ConflictException,
    ValidationException,
    StorageException,
)

__all__ = [
    "settings",
    "get_settings",
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "get_current_user",
    "get_current_active_user",
    "get_current_admin_user",
    "get_current_manager_or_admin",
    "APIException",
    "NotFoundException",
    "UnauthorizedException",
    "ForbiddenException",
    "BadRequestException",
    "ConflictException",
    "ValidationException",
    "StorageException",
]
