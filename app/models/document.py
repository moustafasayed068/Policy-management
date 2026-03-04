from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base
from sqlalchemy.orm import relationship
class Document(Base):
    __tablename__ = "documents"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename      = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_size     = Column(Integer)
    status        = Column(String(50), default="processing")
    uploaded_at   = Column(DateTime, server_default=func.now())

    uploaded_by   = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    uploaded_by_user = relationship("User", back_populates="documents")

    chunks        = relationship("Chunk", back_populates="document", cascade="all, delete")
