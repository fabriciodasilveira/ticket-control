"""
Modelos SQLAlchemy do banco de dados
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey, DECIMAL, TIME, DATE, JSON, UniqueConstraint, Index, CheckConstraint, Enum as SQLEnum, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import uuid
import enum

from app.db.base import Base, TimestampMixin, SoftDeleteMixin


# Enums do banco de dados
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class TaskFrequency(str, enum.Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    AWAITING_APPROVAL = "awaiting_approval"
    REJECTED = "rejected"
    OVERDUE = "overdue"


class PhotoRequirement(str, enum.Enum):
    NONE = "none"
    OPTIONAL = "optional"
    REQUIRED = "required"
    MULTIPLE = "multiple"


class ChecklistType(str, enum.Enum):
    OPENING = "opening"
    CLOSING = "closing"
    CLEANING = "cleaning"
    SECURITY = "security"
    MAINTENANCE = "maintenance"
    CUSTOM = "custom"


class TemperatureType(str, enum.Enum):
    FREEZER = "freezer"
    REFRIGERATOR = "refrigerator"
    COLD_ROOM = "cold_room"
    OVEN = "oven"
    GRILL = "grill"
    OTHER = "other"


class AlertType(str, enum.Enum):
    TEMPERATURE = "temperature"
    OVERDUE_TASK = "overdue_task"
    PENDING_APPROVAL = "pending_approval"
    CHECKLIST_NOT_DONE = "checklist_not_done"
    REJECTED_TASK = "rejected_task"


class AlertStatus(str, enum.Enum):
    PENDING = "pending"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class NotificationChannel(str, enum.Enum):
    PUSH = "push"
    EMAIL = "email"
    WHATSAPP = "whatsapp"


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"


class AuditAction(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    UPLOAD = "upload"
    APPROVE = "approve"
    REJECT = "reject"
    ASSIGN = "assign"
    REASSIGN = "reassign"


class SyncOperation(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


# Modelos
class Unit(Base, TimestampMixin):
    """Unidade/Loja"""
    
    __tablename__ = "units"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    cnpj = Column(String(18))
    is_active = Column(Boolean, default=True, index=True)
    deleted_at = Column(DateTime)
    
    # Relacionamentos
    sectors = relationship("Sector", back_populates="unit", cascade="all, delete-orphan")
    users = relationship("User", back_populates="unit")
    tasks = relationship("Task", back_populates="unit")
    checklists = relationship("Checklist", back_populates="unit")
    evidences = relationship("Evidence", back_populates="unit")
    alerts = relationship("Alert", back_populates="unit")
    
    __table_args__ = (
        Index('idx_units_code', 'code'),
        Index('idx_units_active', 'is_active'),
    )


class Position(Base, TimestampMixin):
    """Cargo/Função"""
    
    __tablename__ = "positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    permissions = Column(JSONB, default=list)
    is_active = Column(Boolean, default=True)
    
    # Relacionamentos
    user_positions = relationship("UserPosition", back_populates="position")
    tasks = relationship("Task", back_populates="position")
    
    __table_args__ = (
        Index('idx_positions_name', 'name'),
    )


class Sector(Base, TimestampMixin):
    """Setor da unidade"""
    
    __tablename__ = "sectors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    qr_code_data = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Relacionamentos
    unit = relationship("Unit", back_populates="sectors")
    tasks = relationship("Task", back_populates="sector")
    checklists = relationship("Checklist", back_populates="sector")
    temperature_records = relationship("TemperatureRecord", back_populates="sector")
    
    __table_args__ = (
        Index('idx_sectors_unit', 'unit_id'),
        Index('idx_sectors_name', 'name'),
    )


class User(Base, TimestampMixin, SoftDeleteMixin):
    """Usuário do sistema"""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="SET NULL"))
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    avatar_url = Column(Text)
    role = Column(String(20), nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    last_login = Column(DateTime)
    refresh_token = Column(String(255))
    
    # Relacionamentos
    unit = relationship("Unit", back_populates="users")
    user_positions = relationship("UserPosition", back_populates="user", cascade="all, delete-orphan")
    task_assignments = relationship("TaskAssignment", back_populates="user")
    evidences = relationship("Evidence", back_populates="user")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
    created_tasks = relationship("Task", back_populates="creator", foreign_keys="Task.created_by")
    approved_assignments = relationship("TaskAssignment", back_populates="approver", foreign_keys="TaskAssignment.approved_by")
    sync_queue = relationship("SyncQueue", back_populates="user", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'manager', 'employee')", name="check_user_role"),
        Index('idx_users_email', 'email'),
        Index('idx_users_unit', 'unit_id'),
        Index('idx_users_role', 'role'),
        Index('idx_users_active', 'is_active'),
    )


class UserPosition(Base):
    """Relação Usuário-Cargo"""
    
    __tablename__ = "user_positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id", ondelete="CASCADE"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    is_primary = Column(Boolean, default=False)
    
    # Relacionamentos
    user = relationship("User", back_populates="user_positions")
    position = relationship("Position", back_populates="user_positions")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'position_id', name='uq_user_position'),
        Index('idx_user_positions_user', 'user_id'),
        Index('idx_user_positions_position', 'position_id'),
    )


class Task(Base, TimestampMixin, SoftDeleteMixin):
    """Tarefa"""
    
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="CASCADE"), nullable=False)
    sector_id = Column(UUID(as_uuid=True), ForeignKey("sectors.id", ondelete="SET NULL"))
    checklist_id = Column(UUID(as_uuid=True), ForeignKey("checklists.id", ondelete="SET NULL"))
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id", ondelete="SET NULL"))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50))
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM)
    estimated_duration = Column(Integer)  # minutos
    frequency = Column(SQLEnum(TaskFrequency), default=TaskFrequency.ONCE)
    frequency_config = Column(JSONB)
    start_date = Column(DATE)
    due_date = Column(DATE)
    due_time = Column(TIME)
    photo_requirement = Column(SQLEnum(PhotoRequirement), default=PhotoRequirement.NONE)
    max_photos = Column(Integer, default=1)
    requires_temperature = Column(Boolean, default=False)
    temperature_min = Column(Numeric(5, 2))
    temperature_max = Column(Numeric(5, 2))
    requires_signature = Column(Boolean, default=False)
    requires_geolocation = Column(Boolean, default=False)
    instructions = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    is_global = Column(Boolean, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relacionamentos
    unit = relationship("Unit", back_populates="tasks")
    sector = relationship("Sector", back_populates="tasks")
    checklist = relationship("Checklist", back_populates="tasks", foreign_keys=[checklist_id])
    position = relationship("Position", back_populates="tasks")
    assignments = relationship("TaskAssignment", back_populates="task", cascade="all, delete-orphan")
    evidences = relationship("Evidence", back_populates="task")
    creator = relationship("User", back_populates="created_tasks", foreign_keys=[created_by])
    checklist_tasks = relationship("ChecklistTask", back_populates="task", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_tasks_unit', 'unit_id'),
        Index('idx_tasks_sector', 'sector_id'),
        Index('idx_tasks_checklist', 'checklist_id'),
        Index('idx_tasks_due_date', 'due_date'),
        Index('idx_tasks_active', 'is_active'),
    )


class Checklist(Base, TimestampMixin):
    """Checklist"""
    
    __tablename__ = "checklists"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="CASCADE"), nullable=False)
    sector_id = Column(UUID(as_uuid=True), ForeignKey("sectors.id", ondelete="SET NULL"))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    type = Column(SQLEnum(ChecklistType), default=ChecklistType.CUSTOM)
    icon = Column(String(50))
    color = Column(String(7))  # hex color
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relacionamentos
    unit = relationship("Unit", back_populates="checklists")
    sector = relationship("Sector", back_populates="checklists")
    tasks = relationship("Task", back_populates="checklist", foreign_keys=[Task.checklist_id])
    checklist_tasks = relationship("ChecklistTask", back_populates="checklist", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_checklists_unit', 'unit_id'),
        Index('idx_checklists_sector', 'sector_id'),
        Index('idx_checklists_type', 'type'),
    )


class ChecklistTask(Base):
    """Relação Checklist-Tarefa"""
    
    __tablename__ = "checklist_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    checklist_id = Column(UUID(as_uuid=True), ForeignKey("checklists.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    order_index = Column(Integer, nullable=False)
    is_required = Column(Boolean, default=True)
    
    # Relacionamentos
    checklist = relationship("Checklist", back_populates="checklist_tasks")
    task = relationship("Task", back_populates="checklist_tasks")
    
    __table_args__ = (
        UniqueConstraint('checklist_id', 'task_id', name='uq_checklist_task'),
        UniqueConstraint('checklist_id', 'order_index', name='uq_checklist_order'),
        Index('idx_checklist_tasks_checklist', 'checklist_id'),
        Index('idx_checklist_tasks_task', 'task_id'),
    )


class TaskAssignment(Base, TimestampMixin):
    """Atribuição de Tarefa"""
    
    __tablename__ = "task_assignments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id", ondelete="SET NULL"))
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="CASCADE"), nullable=False)
    scheduled_date = Column(DATE, nullable=False, index=True)
    scheduled_time = Column(TIME)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    approved_at = Column(DateTime)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    rejection_reason = Column(Text)
    observations = Column(Text)
    geolocation_lat = Column(Numeric(10, 8))
    geolocation_lng = Column(Numeric(11, 8))
    digital_signature = Column(Text)
    signature_name = Column(String(100))
    execution_time = Column(Integer)  # minutos
    sla_met = Column(Boolean, index=True)
    
    # Relacionamentos
    task = relationship("Task", back_populates="assignments")
    user = relationship("User", back_populates="task_assignments")
    approver = relationship("User", back_populates="approved_assignments", foreign_keys=[approved_by])
    unit = relationship("Unit")
    evidences = relationship("Evidence", back_populates="task_assignment", cascade="all, delete-orphan")
    temperature_records = relationship("TemperatureRecord", back_populates="task_assignment", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_task_assignments_task', 'task_id'),
        Index('idx_task_assignments_user', 'user_id'),
        Index('idx_task_assignments_unit', 'unit_id'),
        Index('idx_task_assignments_status', 'status'),
        Index('idx_task_assignments_date', 'scheduled_date'),
        Index('idx_task_assignments_sla', 'sla_met'),
        Index('idx_task_assignments_user_status_date', 'user_id', 'status', 'scheduled_date'),
        Index('idx_task_assignments_unit_status_date', 'unit_id', 'status', 'scheduled_date'),
    )


class Evidence(Base, TimestampMixin):
    """Evidência/Foto"""
    
    __tablename__ = "evidence"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_assignment_id = Column(UUID(as_uuid=True), ForeignKey("task_assignments.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(50))
    thumbnail_path = Column(String(500))
    width = Column(Integer)
    height = Column(Integer)
    compression_quality = Column(Integer, default=80)
    caption = Column(Text)
    metadata_json = Column('metadata', JSONB)
    is_verified = Column(Boolean, default=False)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    verified_at = Column(DateTime)
    
    # Relacionamentos
    task_assignment = relationship("TaskAssignment", back_populates="evidences")
    task = relationship("Task", back_populates="evidences")
    user = relationship("User", back_populates="evidences")
    unit = relationship("Unit", back_populates="evidences")
    
    __table_args__ = (
        Index('idx_evidence_task_assignment', 'task_assignment_id'),
        Index('idx_evidence_task', 'task_id'),
        Index('idx_evidence_user', 'user_id'),
        Index('idx_evidence_unit', 'unit_id'),
        Index('idx_evidence_created', 'created_at'),
        Index('idx_evidence_unit_created', 'unit_id', 'created_at'),
    )


class TemperatureRecord(Base, TimestampMixin):
    """Registro de Temperatura"""
    
    __tablename__ = "temperature_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_assignment_id = Column(UUID(as_uuid=True), ForeignKey("task_assignments.id", ondelete="CASCADE"))
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="CASCADE"), nullable=False)
    sector_id = Column(UUID(as_uuid=True), ForeignKey("sectors.id", ondelete="SET NULL"))
    temperature_type = Column(SQLEnum(TemperatureType), nullable=False)
    equipment_name = Column(String(100))
    temperature_value = Column(Numeric(5, 2), nullable=False)
    min_allowed = Column(Numeric(5, 2))
    max_allowed = Column(Numeric(5, 2))
    recorded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    notes = Column(Text)
    
    # Relacionamentos
    task_assignment = relationship("TaskAssignment", back_populates="temperature_records")
    sector = relationship("Sector", back_populates="temperature_records")
    
    __table_args__ = (
        Index('idx_temperature_records_assignment', 'task_assignment_id'),
        Index('idx_temperature_records_unit', 'unit_id'),
        Index('idx_temperature_records_type', 'temperature_type'),
        Index('idx_temperature_records_date', 'created_at'),
    )


class Alert(Base, TimestampMixin):
    """Alerta do sistema"""
    
    __tablename__ = "alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="CASCADE"), nullable=False)
    alert_type = Column(SQLEnum(AlertType), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="medium")
    status = Column(SQLEnum(AlertStatus), default=AlertStatus.PENDING, index=True)
    related_entity_type = Column(String(50))
    related_entity_id = Column(UUID(as_uuid=True))
    acknowledged_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    acknowledged_at = Column(DateTime)
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    resolved_at = Column(DateTime)
    
    # Relacionamentos
    unit = relationship("Unit", back_populates="alerts")
    
    __table_args__ = (
        Index('idx_alerts_unit', 'unit_id'),
        Index('idx_alerts_type', 'alert_type'),
        Index('idx_alerts_status', 'status'),
        Index('idx_alerts_severity', 'severity'),
        Index('idx_alerts_created', 'created_at'),
    )


class Notification(Base, TimestampMixin):
    """Notificação"""
    
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("notifications.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    channel = Column(SQLEnum(NotificationChannel), nullable=False)
    status = Column(SQLEnum(NotificationStatus), default=NotificationStatus.PENDING)
    data = Column(JSONB)
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    read_at = Column(DateTime)
    retry_count = Column(Integer, default=0)
    
    # Relacionamentos
    user = relationship("User", back_populates="notifications")
    
    __table_args__ = (
        Index('idx_notifications_user', 'user_id'),
        Index('idx_notifications_status', 'status'),
        Index('idx_notifications_channel', 'channel'),
        Index('idx_notifications_created', 'created_at'),
    )


class AuditLog(Base, TimestampMixin):
    """Log de Auditoria"""
    
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    action = Column(SQLEnum(AuditAction), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True))
    old_values = Column(JSONB)
    new_values = Column(JSONB)
    ip_address = Column(INET)
    user_agent = Column(Text)
    device_info = Column(JSONB)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="SET NULL"))
    
    # Relacionamentos
    user = relationship("User", back_populates="audit_logs")
    
    __table_args__ = (
        Index('idx_audit_logs_user', 'user_id'),
        Index('idx_audit_logs_action', 'action'),
        Index('idx_audit_logs_entity', 'entity_type', 'entity_id'),
        Index('idx_audit_logs_unit', 'unit_id'),
        Index('idx_audit_logs_created', 'created_at'),
        Index('idx_audit_logs_entity_created', 'entity_type', 'entity_id', 'created_at'),
    )


class SyncQueue(Base, TimestampMixin):
    """Fila de Sincronização Offline"""
    
    __tablename__ = "sync_queue"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    device_id = Column(String(100), nullable=False)
    operation = Column(SQLEnum(SyncOperation), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_data = Column(JSONB, nullable=False)
    local_timestamp = Column(DateTime, nullable=False)
    synced = Column(Boolean, default=False, index=True)
    synced_at = Column(DateTime)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # Relacionamentos
    user = relationship("User", back_populates="sync_queue")
    
    __table_args__ = (
        Index('idx_sync_queue_user', 'user_id'),
        Index('idx_sync_queue_device', 'device_id'),
        Index('idx_sync_queue_synced', 'synced'),
        Index('idx_sync_queue_created', 'created_at'),
    )


class DashboardCache(Base, TimestampMixin):
    """Cache para Dashboard"""
    
    __tablename__ = "dashboard_cache"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id", ondelete="CASCADE"), nullable=False)
    cache_key = Column(String(100), nullable=False)
    cache_data = Column(JSONB, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('unit_id', 'cache_key', name='uq_dashboard_cache'),
        Index('idx_dashboard_cache_unit', 'unit_id'),
        Index('idx_dashboard_cache_expires', 'expires_at'),
    )
