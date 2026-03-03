from fastapi import FastAPI
from app.core.config import settings # تأكد إن المسار صح حسب اسم الفولدر عندك
from app.api.routers import health, auth # ضفنا auth هنا

app = FastAPI(title="Policy Management AI")

# تسجيل الروترز
app.include_router(health.router)
app.include_router(auth.router) # ده السطر اللي هيفتح لك صفحة الـ Login

@app.get("/")
async def root():
    return {"message": "Welcome to Policy Management API", "status": "Running"}