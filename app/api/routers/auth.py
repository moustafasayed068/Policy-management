from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, Token
from app.repositories.user import UserRepository
from app.core.security import create_access_token, verify_password
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)): 
    user_repo = UserRepository(db)
    
    user = await user_repo.get_by_email(user_in.email)
    
    if user:
        raise HTTPException(status_code=400, detail="Email is already exsit")
    
    return await user_repo.create(user_in)

@router.post("/get access token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    
    user = await user_repo.get_by_email(form_data.username)
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password incorrect")
    
    access_token = create_access_token(subject=user.id, role=user.role)
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}
#test case for jwt login
@router.get("get data")
async def get(user_id: str = Depends(get_current_user)):
    return {f'user is' :{user_id}}