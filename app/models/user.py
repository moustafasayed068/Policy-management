from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.base import Base

class RoleEnum(str, enum.Enum):
    hr       = "hr"
    employee = "employee"
    admin    = "admin"

class User(Base):
    __tablename__ = "users"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email         = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name     = Column(String(255), nullable=True)
    role          = Column(Enum(RoleEnum), default=RoleEnum.employee, nullable=False)
    is_active     = Column(Boolean, default=True)
    created_at    = Column(DateTime, server_default=func.now())
    updated_at    = Column(DateTime, onupdate=func.now())

    
    documents     = relationship("Document", back_populates="uploaded_by_user")
    chat_sessions = relationship("ChatSession", back_populates="user")