from sqlalchemy import Column, String, ARRAY, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
from app.db.base import Base
from sqlalchemy.orm import relationship

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"))
    role = Column(String(20), nullable=False)   # "user" | "assistant"
    content = Column(Text, nullable=False)
    source_chunks = Column(ARRAY(UUID), nullable=True)   # which chunks were used
    created_at = Column(DateTime, server_default=func.now())

    session = relationship("ChatSession", back_populates="messages")