from sqlalchemy import Column, Integer, String, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship
import enum
from .db import Base

class BookState(str, enum.Enum):
    DISPONIBLE = "Disponible"
    PRESTADO = "Prestado"
    REPARACION = "En reparación"

books_genres = Table(
    "books_genres",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre", String, primary_key=True),
)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    isbn = Column(String, unique=True, index=True)
    author = Column(String, nullable=False)
    category = Column(String, nullable=True)
    state = Column(Enum(BookState), default=BookState.DISPONIBLE)
    genres = relationship("Genre", secondary=books_genres, viewonly=True)
