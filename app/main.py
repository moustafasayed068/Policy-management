from fastapi import FastAPI
from app.core.config import settings 
# 1. ضيف documents هنا في الـ Import
from app.api.routers import health, auth, chat, documents , test

app = FastAPI(title="Policy Management AI")

app.include_router(health.router)
app.include_router(auth.router) 
app.include_router(chat.router)
app.include_router(test.router)
# 2. ضيف الروتر الجديد هنا عشان يظهر في Swagger
app.include_router(documents.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Policy Management API", "status": "Running"}