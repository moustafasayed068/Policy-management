from fastapi import APIRouter
from app.db.session import  engine
from app.db.base import Base


router = APIRouter(prefix="/health", tags=["health"])


@router.post("/create-tables")
async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return {"status": "ok", "message": "All tables created successfully"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    

@router.get("/tables-seen")
async def tables_seen():
    return {"tables": list(Base.metadata.tables.keys())}


