from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.document import DocumentOut
from app.models.document import Document
from app.repositories.document import DocumentRepository
from app.services.document import DocumentService
from app.api.dependencies import get_current_user
from app.services.auth import verify_admin_access
from app.client.supabase import supabase_client

router = APIRouter(prefix="/documents", tags=["Documents Management"])


document_service = DocumentService(supabase_client)


@router.post("/upload", response_model=DocumentOut)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    verify_admin_access(current_user)
    repo = DocumentRepository(db)

    file_content = await file.read()

    # Upload to Supabase
    try:
        await document_service.upload_to_storage("policies", file_content, file.filename, file.content_type)
    except Exception as e:  
        raise HTTPException(status_code=500, detail=f"Error uploading to Supabase: {str(e)}")

    new_doc = Document(
        filename=file.filename,
        original_name=file.filename,
        file_size=len(file_content),
        status="uploaded",
        uploaded_by=current_user.id
    )

    return await repo.add(new_doc)

@router.get("/", response_model=List[DocumentOut])
async def list_documents(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    verify_admin_access(current_user)
    repo = DocumentRepository(db)
    return await repo.get_all()

@router.delete("/{doc_id}")
async def delete_document(doc_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    verify_admin_access(current_user)
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete from storage
    try:
        supabase_client.storage.from_("policies").remove([doc.filename])
    except Exception as e:
        print(f"Storage delete error: {e}")

    await repo.delete(doc)
    return {"message": f"Document {doc.filename} deleted successfully"}