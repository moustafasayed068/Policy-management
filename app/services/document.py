import fitz
from supabase import Client
from app.models.document import Document
from typing import List
from sqlalchemy import select

class DocumentService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    async def upload_to_storage(self, bucket_name: str, file_content: bytes, filename: str, content_type: str):
        try:
            self.supabase.storage.from_(bucket_name).upload(
                path=filename,
                file=file_content,
                file_options={"content-type": content_type}
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise e
            
    async def get_all_documents(self) -> List[Document]:
        result = await self.db.execute(select(Document))
        docs = result.scalars().all()
        for doc in docs:
            if doc.status is None:
                doc.status = "processing"
        return docs