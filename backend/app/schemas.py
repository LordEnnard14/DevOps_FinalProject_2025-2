from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class BookState(str, Enum):
    DISPONIBLE = "Disponible"
    PRESTADO = "Prestado"
    REPARACION = "En reparación"

class BookBase(BaseModel):
    titulo: str
    isbn: str
    author: str
    category: Optional[str] = None
    state: Optional[BookState] = BookState.DISPONIBLE
    genres: Optional[List[str]] = []

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True
