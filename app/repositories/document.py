from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.document import Document
from typing import List, Optional
from uuid import UUID

class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Document]:
        result = await self.db.execute(select(Document))
        return result.scalars().all()

    async def get_by_id(self, doc_id: UUID) -> Optional[Document]:
        result = await self.db.execute(select(Document).where(Document.id == doc_id))
        return result.scalar_one_or_none()

    async def add(self, document: Document) -> Document:
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def delete(self, document: Document):
        await self.db.delete(document)
        await self.db.commit()