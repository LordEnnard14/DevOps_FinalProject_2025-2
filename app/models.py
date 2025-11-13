from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(50), unique=True, nullable=False)
    category = Column(String(50))
    status = Column(String(20), default="AVAILABLE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
