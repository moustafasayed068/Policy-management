from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.chunk import ChunkRepository
from app.services.chunk import DocumentService
from uuid import UUID
router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/{document_id}/process")
async def process_document(
    document_id: UUID,
    text: str,
    db: AsyncSession = Depends(get_db)
):
    chunk_repo = ChunkRepository(db)
    service = DocumentService(chunk_repo)

    count = await service.process_document(document_id, text)

    return {"chunks_created": count}


@router.post("/search")
async def search_chunks(
    query: str,
    db: AsyncSession = Depends(get_db)
):
    chunk_repo = ChunkRepository(db)
    service = DocumentService(chunk_repo)

    chunks = await service.search(query)

    return [
        {
            "id": str(c.id),
            "content": c.content,
            "chunk_index": c.chunk_index
        }
        for c in chunks
    ]