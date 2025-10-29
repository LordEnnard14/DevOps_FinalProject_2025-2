from sqlalchemy.orm import Session
from . import models, schemas

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_isbn(db: Session, isbn: str):
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        titulo=book.titulo,
        isbn=book.isbn,
        author=book.author,
        category=book.category,
        state=book.state.value if hasattr(book.state, "value") else book.state
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
