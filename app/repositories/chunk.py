from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.chunks import Chunk


class ChunkRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def bulk_create(self, chunks: list[Chunk]) -> None:
        self.db.add_all(chunks)
        await self.db.commit()

    async def get_similar(
        self,
        query_embedding: list[float],
        limit: int = 5
    ) -> list[Chunk]:
        stmt = (
            select(Chunk)
            .order_by(Chunk.embedding.l2_distance(query_embedding))
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()