from fastapi import FastAPI
from app.config import settings
from app.api.routers import health

app = FastAPI(title=settings.APP_NAME)

app.include_router(health.router)