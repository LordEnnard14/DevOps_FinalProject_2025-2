# app/crud.py
from __future__ import annotations

from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.schemas import BookCreate, BookUpdate


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_by_isbn(db: Session, isbn: str) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()


def list_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return (
        db.query(models.Book)
        .order_by(models.Book.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_book(db: Session, payload: BookCreate) -> models.Book:
    book = models.Book(
        title=payload.title,
        author=payload.author,
        isbn=payload.isbn,
        category=payload.category,
        status=payload.status or "AVAILABLE",
    )
    db.add(book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # re-raise para que la capa superior decida qué hacer
        raise
    db.refresh(book)
    return book


def update_book(db: Session, db_book: models.Book, payload: BookUpdate) -> models.Book:
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_book, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, db_book: models.Book) -> None:
    db.delete(db_book)
    db.commit()
