"""
Base class para todos os modelos SQLAlchemy
"""

from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import Column, DateTime

Base = declarative_base()


class TimestampMixin:
    """Mixin para adicionar timestamps automáticos"""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin:
    """Mixin para soft delete"""
    
    deleted_at = Column(DateTime, nullable=True)
    
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
