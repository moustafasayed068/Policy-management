from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[UUID] = None

class ChatResponse(BaseModel):
    session_id: UUID
    reply: str