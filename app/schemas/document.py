from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

# ده الموديل اللي السيرفر هيرجعه (Response)
class DocumentOut(BaseModel):
    id: UUID
    filename: str
    original_name: str  # ضفنا ده عشان موجود في الموديل بتاعك
    file_size: Optional[int] = None # ضفنا ده
    total_pages: int # مهم جداً عشان ده اللي بنحسبه بـ fitz
    status: str
    uploaded_at: datetime
    uploaded_by: Optional[UUID] = None # عشان نعرف مين اللي رفع الملف

    # الطريقة الجديدة في Pydantic V2 لربط الـ SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

# لو حبيت تعمل تحديث لبيانات الملف (مثلاً تغير الحالة من processing لـ completed)
class DocumentUpdate(BaseModel):
    status: Optional[str] = None
    total_pages: Optional[int] = None