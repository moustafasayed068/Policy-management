from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.documents import Document
from app.schemas.document import DocumentOut
from supabase import create_client, Client
from app.core.config import settings
from typing import List
import os
import fitz  # PyMuPDF

router = APIRouter(prefix="/documents", tags=["Documents Management"])

# إعداد اتصال Supabase
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# دالة مساعدة للتحقق من الصلاحية (عشان منكررش الكود)
def verify_admin_access(user):
    if user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="عفواً، هذه العملية مسموحة فقط للـ HR أو المسؤولين"
        )

# 1. رفع ملف لـ Supabase والداتابيز
@router.post("/upload", response_model=DocumentOut)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    verify_admin_access(current_user)

    file_content = await file.read()
    file_size = len(file_content)
    
    # حساب عدد الصفحات للـ PDF
    total_pages = 0
    if file.filename.lower().endswith(".pdf"):
        try:
            with fitz.open(stream=file_content, filetype="pdf") as doc:
                total_pages = len(doc)
        except Exception as e:
            print(f"Error reading PDF: {e}")

    # رفع الملف لـ Supabase Storage (Bucket: policies)
    bucket_name = "policies"
    # هنحفظ الملف باسمه الأصلي مباشرة في الـ bucket
    file_path = f"{file.filename}"
    
    try:
        # ملاحظة: لو الملف موجود بنفس الاسم، Supabase ممكن يرجع خطأ، الـ Policy اللي عملناها بتسمح بالرفع
        supabase.storage.from_(bucket_name).upload(
            path=file_path,
            file=file_content,
            file_options={"content-type": file.content_type}
        )
    except Exception as e:
        # لو الملف موجود فعلاً ممكن نعدي الخطوة دي أو نحدثه
        if "already exists" not in str(e):
            raise HTTPException(status_code=500, detail=f"خطأ أثناء الرفع لـ Supabase: {str(e)}")

    # حفظ البيانات في قاعدة البيانات
    new_doc = Document(
        filename=file.filename,
        original_name=file.filename,
        file_size=file_size,
        status="uploaded",
        uploaded_by=current_user.id,
        total_pages=total_pages
    )

    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    return new_doc

# 2. عرض كل الملفات المرفوعة
@router.get("/", response_model=List[DocumentOut])
async def list_documents(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    verify_admin_access(current_user)
    result = await db.execute(select(Document))
    return result.scalars().all()

# 3. حذف ملف من السيستم ومن Supabase
@router.delete("/{doc_id}")
async def delete_document(
    doc_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    verify_admin_access(current_user)
    
    # البحث عن الملف في الداتابيز
    query = select(Document).where(Document.id == doc_id)
    result = await db.execute(query)
    doc = result.scalar_one_or_none()
    
    if not doc:
        raise HTTPException(status_code=404, detail="الملف غير موجود")

    # حذف الملف من Supabase Storage
    try:
        supabase.storage.from_("policies").remove([doc.filename])
    except Exception as e:
        print(f"Storage delete error: {e}")

    # حذف السجل من الداتابيز
    await db.delete(doc)
    await db.commit()
    
    return {"message": f"تم حذف الملف {doc.filename} بنجاح من الداتابيز وStorage"}