# app/schemas.py
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: str = Field(..., min_length=4, max_length=50)
    category: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field("AVAILABLE", max_length=20)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=4, max_length=50)
    category: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=20)


class BookOut(BookBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True  # permite crear el schema desde modelos ORM
    }
