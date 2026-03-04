from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.api.dependencies import get_current_user
from app.services.chat import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

# Initialize the service
chat_service = ChatService()

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Endpoint to handle RAG-based chat. 
    It searches for relevant document chunks and generates an AI response.
    """
    try:
        # Destructuring the tuple returned by the service
        session_id, reply = await chat_service.chat(
            db=db,
            user_id=current_user.id,
            message=payload.message,
            session_id=payload.session_id
        )

        return ChatResponse(session_id=session_id, reply=reply)

    except ValueError as ve:
        # Handle specific errors like "Session not found"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve)
        )
    except Exception as e:
        # Handle any unexpected errors during AI generation or DB operations
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during chat processing: {str(e)}"
        )