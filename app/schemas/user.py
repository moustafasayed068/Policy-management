from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.user import RoleEnum

# البيانات اللي بنحتاجها لما يوزر جديد يسجل (Register)
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: RoleEnum = RoleEnum.employee  # الديفولت موظف، والمدير بيغيرها لنفسه

# البيانات اللي بنرجعها لما حد يطلب بيانات يوزر (بنشيل الباسورد طبعاً)
class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    role: RoleEnum
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True # عشان Pydantic يعرف يقرأ من الـ SQLAlchemy Model

# بيانات الـ Token اللي هترجع بعد الـ Login
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str # مهمة جداً للـ Frontend عشان يعرف هو مدير ولا موظف

class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None