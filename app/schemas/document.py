from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class DocumentOut(BaseModel):
    id: UUID
    filename: str
    original_name: str
    file_size: Optional[int] = 0
    status: Optional[str] = "processing"
    uploaded_at: datetime
    uploaded_by: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)

class DocumentUpdate(BaseModel):
    status: Optional[str] = None