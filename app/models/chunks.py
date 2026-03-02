from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
from app.db.base import Base
from sqlalchemy.orm import relationship
class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    page_number = Column(Integer)
    chunk_index = Column(Integer)        # order within document
    token_count = Column(Integer)        # useful for debugging
    embedding = Column(Vector(1536))     # 1536 for OpenAI, 1024 for Cohere
    created_at = Column(DateTime, server_default=func.now())

    document = relationship("Document", back_populates="chunks")
