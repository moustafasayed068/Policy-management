from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.chat import ChatRepository
from app.repositories.message import MessageRepository
from app.services.llm import llm_service

class ChatService:

    def __init__(self):
        self.chat_repo = ChatRepository()
        self.message_repo = MessageRepository()

    async def chat(
        self,
        db: AsyncSession,
        user_id: UUID,
        message: str,
        session_id: UUID | None = None
    ):
        
        if session_id:
            session = await self.chat_repo.get_by_id_and_user(
                db, session_id, user_id
            )
            if not session:
                raise ValueError("Session not found")
        else:
            session = await self.chat_repo.create(db, user_id)

        
        await self.message_repo.create(
            db, session.id, "user", message
        )

        
        messages = await self.message_repo.get_by_session(
            db, session.id
        )

        formatted = [
            {"role": m.role, "content": m.content}
            for m in messages
        ]

        
        reply = await llm_service.chat(formatted)

        
        await self.message_repo.create(
            db, session.id, "assistant", reply
        )

        return session.id, reply