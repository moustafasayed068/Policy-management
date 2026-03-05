from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text # Important for vector search
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
        # 1. Handle or Create Session
        if session_id:
            session = await self.chat_repo.get_by_id_and_user(
                db, session_id, user_id
            )
            if not session:
                raise ValueError("Session not found")
        else:
            session = await self.chat_repo.create(db, user_id)

        # 2. Save user message to database
        await self.message_repo.create(
            db, session.id, "user", message
        )

        # --- START RAG LOGIC (SEARCHING THE FILES) ---
        
        # 3. Get embedding for the current question using our new emb_query
        # We use search_query type for better accuracy in retrieval
        question_embedding = await llm_service.emb_query(message)

        # 4. Semantic Search in the 'chunks' table
        # We fetch the top 5 most relevant pieces of text
        search_stmt = text("""
            SELECT id, content FROM chunks 
            ORDER BY embedding <=> :embedding 
            LIMIT 5
        """)
        
        result = await db.execute(search_stmt, {"embedding": str(question_embedding)})
        rows = result.fetchall()
        
        relevant_context = "\n---\n".join([row.content for row in rows])
        source_chunk_ids = [row.id for row in rows]

        # --- END RAG LOGIC ---

        # 5. Get conversation history to maintain context
        messages_db = await self.message_repo.get_by_session(
            db, session.id
        )

        formatted = [
            {"role": m.role, "content": m.content}
            for m in messages_db
        ]

        # 6. Inject Document Context into the prompt
        # This tells the LLM to answer only from the provided files
        if relevant_context:
            system_instruction = {
                "role": "system",
                "content": (
                    "You are a helpful HR assistant. Use the following document context to answer the user question. "
                    "If the answer is not in the context, say you don't know. Do not hallucinate. "
                    f"\nDocument Context:\n{relevant_context}"
                )
            }
            formatted.insert(0, system_instruction)

        # 7. Generate response using Cohere V2
        reply = await llm_service.chat(formatted)

        # 8. Save assistant reply and link it to the source chunks used
        await self.message_repo.create(
            db, session.id, "assistant", reply, source_chunks=source_chunk_ids
        )

        return session.id, reply