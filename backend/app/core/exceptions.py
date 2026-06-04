"""
Exceções personalizadas da aplicação
"""

from fastapi import HTTPException, status
from typing import Optional, Any


class APIException(HTTPException):
    """Exceção base para API"""
    
    def __init__(
        self,
        status_code: int = 500,
        detail: str = "Erro interno do servidor",
        error_code: str = "INTERNAL_ERROR",
        data: Optional[Any] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.data = data


class NotFoundException(APIException):
    """Recurso não encontrado"""
    
    def __init__(self, resource: str = "Recurso", detail: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail or f"{resource} não encontrado",
            error_code="NOT_FOUND"
        )


class UnauthorizedException(APIException):
    """Não autorizado"""
    
    def __init__(self, detail: str = "Não autorizado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="UNAUTHORIZED"
        )


class ForbiddenException(APIException):
    """Proibido"""
    
    def __init__(self, detail: str = "Acesso proibido"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="FORBIDDEN"
        )


class BadRequestException(APIException):
    """Requisição inválida"""
    
    def __init__(self, detail: str = "Requisição inválida"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="BAD_REQUEST"
        )


class ConflictException(APIException):
    """Conflito"""
    
    def __init__(self, detail: str = "Conflito de recursos"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="CONFLICT"
        )


class ValidationException(APIException):
    """Erro de validação"""
    
    def __init__(self, detail: str = "Erro de validação", errors: Optional[list] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR",
            data=errors
        )


class StorageException(APIException):
    """Erro no armazenamento de arquivos"""
    
    def __init__(self, detail: str = "Erro ao armazenar arquivo"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="STORAGE_ERROR"
        )
