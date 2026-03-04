from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.chat import ChatSession
from uuid import UUID

class ChatRepository:

    async def get_by_id_and_user(
        self, db: AsyncSession, session_id: UUID, user_id: UUID 
    ):
        result = await db.execute(
            select(ChatSession).where(
                ChatSession.id == session_id,
                ChatSession.user_id == user_id
            )
        )
        return result.scalars().first()

    async def create(self, db: AsyncSession, user_id: UUID):
        session = ChatSession(user_id=user_id, title="New Chat")
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session