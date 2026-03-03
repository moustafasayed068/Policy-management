from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # إعدادات قاعدة البيانات (Supabase)
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_DB_URL: str
    
    # إعدادات الـ Auth
    SECRET_KEY: str  # السر اللي بنشفر بيه التوكن
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # إعدادات الذكاء الاصطناعي
    COHERE_API_KEY: str

    # عشان يقرأ من ملف .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# بناخد نسخة واحدة (Instance) نستخدمها في كل المشروع
settings = Settings()