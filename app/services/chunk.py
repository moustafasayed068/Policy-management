from app.repositories.chunk import ChunkRepository
from app.models.chunks import Chunk
from app.services.llm import llm_service


class DocumentService:
    def __init__(self, chunk_repo: ChunkRepository):
        self.chunk_repo = chunk_repo

    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 400,
        overlap: int = 50
    ) -> list[dict]:

        chunks = []
        start = 0
        index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_content = text[start:end]

            chunks.append({
                "content": chunk_content,
                "chunk_index": index,
                "token_count": len(chunk_content.split())
            })

            start += chunk_size - overlap
            index += 1

        return chunks

    async def process_document(
        self,
        document_id,
        text: str
    ) -> int:

        
        chunks_data = self._chunk_text(text)
        contents = [c["content"] for c in chunks_data]

        # embed 
        embeddings = await llm_service.emb(contents)

        db_chunks = []

        for i, chunk_data in enumerate(chunks_data):
            db_chunk = Chunk(
                document_id=document_id,
                content=chunk_data["content"],
                chunk_index=chunk_data["chunk_index"],
                token_count=chunk_data["token_count"],
                embedding=embeddings[i],
            )
            db_chunks.append(db_chunk)

        
        await self.chunk_repo.bulk_create(db_chunks)

        return len(db_chunks)

    async def search(
        self,
        query: str,
        limit: int = 5
    ):

        query_embedding = (await llm_service.emb([query]))[0]

        return await self.chunk_repo.get_similar(
            query_embedding=query_embedding,
            limit=limit
        )