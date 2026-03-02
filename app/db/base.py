from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models import user, documents, chunks, chat, message