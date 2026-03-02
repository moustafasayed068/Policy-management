from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
from app.db.base import Base
from sqlalchemy.orm import relationship
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    title       = Column(String(255), nullable=True)
    created_at  = Column(DateTime, server_default=func.now())

    user_id     = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user        = relationship("User", back_populates="chat_sessions")

    messages    = relationship("Message", back_populates="session", cascade="all, delete")