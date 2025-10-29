from fastapi import FastAPI, Depends, HTTPException
from typing import List
from . import crud, schemas, models
from .db import engine
from .deps import get_db
from sqlalchemy.orm import Session
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Biblioteca API")

REQUEST_COUNT = Counter("app_requests_total", "Total HTTP requests")

@app.get("/metrics")
def metrics():
    return generate_latest()

@app.get("/books", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    REQUEST_COUNT.inc()
    return crud.get_books(db, skip=skip, limit=limit)

@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    existing = crud.get_book_by_isbn(db, book.isbn)
    if existing:
        raise HTTPException(status_code=400, detail="ISBN already registered")
    return crud.create_book(db, book)
