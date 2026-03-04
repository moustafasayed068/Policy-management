from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.message import Message
from uuid import UUID

class MessageRepository:

    async def create(
        self, db: AsyncSession, session_id: UUID, role: str, content: str
    ):
        message = Message(
            session_id=session_id,
            role=role,
            content=content
        )
        db.add(message)
        await db.commit()
        return message

    async def get_by_session(self, db: AsyncSession, session_id: UUID):
        result = await db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at)
        )
        return result.scalars().all()