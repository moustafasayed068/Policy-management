from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.message import Message
from uuid import UUID
from typing import List, Optional

class MessageRepository:

    async def create(
        self, 
        db: AsyncSession, 
        session_id: UUID, 
        role: str, 
        content: str,
        source_chunks: Optional[List[UUID]] = None  
    ):
        message = Message(
            session_id=session_id,
            role=role,
            content=content,
            source_chunks=source_chunks 
        )
        db.add(message)
        await db.commit()
        await db.refresh(message) 
        return message

    async def get_by_session(self, db: AsyncSession, session_id: UUID):
        result = await db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at)
        )
        return result.scalars().all()