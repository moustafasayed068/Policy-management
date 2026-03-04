from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.repositories.chunk import ChunkRepository
from app.schemas.document import DocumentOut
from app.models.document import Document
from app.repositories.document import DocumentRepository
from app.services.chunk import DocumentService as ChunkDocumentService
from app.services.document import StorageService as StorageDocumentService
from app.api.dependencies import get_current_user
from app.services.auth import verify_admin_access
from app.client.supabase import supabase_client

router = APIRouter(prefix="/documents", tags=["Documents Management"])
storage_service = StorageDocumentService(supabase_client)


@router.post("/upload", response_model=DocumentOut)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_admin_access(current_user)
    repo = DocumentRepository(db)
    chunk_repo = ChunkRepository(db)
    chunk_service = ChunkDocumentService(chunk_repo)

    file_content = await file.read()

    # 1️⃣ Extract text
    try:
        extracted_text = storage_service.extract_text_from_pdf(file_content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2️⃣ Upload to Supabase
    try:
        await storage_service.upload_to_storage(
            bucket_name="policies",
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 3️⃣ Save document
    new_doc = Document(
        filename=file.filename,
        original_name=file.filename,
        file_size=len(file_content),
        status="uploaded",
        uploaded_by=current_user.id,
    )
    saved_doc = await repo.add(new_doc)

    # 4️⃣ Process chunks
    chunks_count = await chunk_service.process_document(saved_doc.id, extracted_text)

    # 5️⃣ Return response
    return DocumentOut(
        id=saved_doc.id,
        filename=saved_doc.filename,
        original_name=saved_doc.original_name,
        file_size=saved_doc.file_size,
        status=saved_doc.status,
        uploaded_at=saved_doc.uploaded_at,
        uploaded_by=saved_doc.uploaded_by,
        extracted_text=f"{chunks_count} chunks created",
    )


@router.get("/", response_model=List[DocumentOut])
async def list_documents(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_admin_access(current_user)
    repo = DocumentRepository(db)
    return await repo.get_all()


@router.delete("/{doc_id}")
async def delete_document(
    doc_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_admin_access(current_user)
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        supabase_client.storage.from_("policies").remove([doc.filename])
    except Exception as e:
        print(f"Storage delete error: {e}")

    await repo.delete(doc)
    return {"message": f"Document {doc.filename} deleted successfully"}