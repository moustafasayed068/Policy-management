from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.api.dependencies import get_current_user
from app.services.chat import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

chat_service = ChatService()

@router.post("/", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    session_id, reply = await chat_service.chat(
        db=db,
        user_id=current_user.id,
        message=payload.message,
        session_id=payload.session_id
    )

    return ChatResponse(session_id=session_id, reply=reply)