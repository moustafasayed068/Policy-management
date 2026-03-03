from fastapi import FastAPI
from app.core.config import settings 
from app.api.routers import health, auth 
app = FastAPI(title="Policy Management AI")

app.include_router(health.router)
app.include_router(auth.router) 

@app.get("/")
async def root():
    return {"message": "Welcome to Policy Management API", "status": "Running"}
