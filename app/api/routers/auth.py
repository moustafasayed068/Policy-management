from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession # غيرنا دي لـ AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, Token
from app.repositories.user import UserRepository
from app.core.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)): # ضفنا async و AsyncSession
    user_repo = UserRepository(db)
    
    # ضفنا await هنا لأن الدالة بقت async
    user = await user_repo.get_by_email(user_in.email)
    
    if user:
        raise HTTPException(status_code=400, detail="الإيميل ده مسجل عندنا قبل كدة!")
    
    # ضفنا await هنا كمان
    return await user_repo.create(user_in)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    
    # ضفنا await
    user = await user_repo.get_by_email(form_data.username)
    
    # التأكد من اليوزر والباسورد
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="الإيميل أو الباسورد غلط")
    
    # إنشاء التوكن مع الـ Role
    access_token = create_access_token(subject=user.id, role=user.role)
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}