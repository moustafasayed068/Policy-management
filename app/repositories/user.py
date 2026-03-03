from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

class UserRepository:
    def __init__(self, db: AsyncSession): 
        self.db = db

    async def get_by_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create(self, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        
        db_obj = User(
            email=obj_in.email,
            password_hash=hashed_password,
            full_name=obj_in.full_name,
            role=obj_in.role
        )
        
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
