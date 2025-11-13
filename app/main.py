# app/main.py
from __future__ import annotations

from typing import List, Optional

from fastapi import (Depends, FastAPI, Form, HTTPException, Request)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app.auth import login_required
from app.auth import router as auth_router
from app.db import get_db
from app.schemas import BookCreate, BookOut, BookUpdate

app = FastAPI(title="Library Management", version="1.0.0")

# Static & Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# CORS (si conectas un frontend externo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- API ----------
@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok"}


@app.get("/api/books", response_model=List[BookOut], tags=["books"])
def list_books_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_books(db, skip=skip, limit=limit)


@app.get("/api/books/{book_id}", response_model=BookOut, tags=["books"])
def get_book_api(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/api/books", response_model=BookOut, status_code=201, tags=["books"])
def create_book_api(payload: BookCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="ISBN already exists")


@app.put("/api/books/{book_id}", response_model=BookOut, tags=["books"])
def update_book_api(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    try:
        return crud.update_book(db, book, payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="ISBN already exists")


@app.delete("/api/books/{book_id}", status_code=204, tags=["books"])
def delete_book_api(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db, book)
    return None


# ---------- Vistas (Jinja) ----------
app.include_router(auth_router)


@app.get("/")
def root():
    return RedirectResponse(url="/books")


@app.get("/books")
def books_list(
    request: Request, db: Session = Depends(get_db), user=Depends(login_required)
):
    books = crud.list_books(db, limit=100)
    return templates.TemplateResponse(
        "books_list.html", {"request": request, "books": books, "user": user}
    )


@app.get("/books/new")
def books_new(request: Request, user=Depends(login_required)):
    return templates.TemplateResponse(
        "book_form.html", {"request": request, "book": None, "user": user}
    )


@app.post("/books/new")
def books_create(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(...),
    category: Optional[str] = Form(None),
    status: str = Form("AVAILABLE"),
    db: Session = Depends(get_db),
    user=Depends(login_required),
):
    try:
        crud.create_book(
            db,
            BookCreate(
                title=title, author=author, isbn=isbn, category=category, status=status
            ),
        )
        return RedirectResponse(url="/books", status_code=302)
    except IntegrityError:
        return templates.TemplateResponse(
            "book_form.html",
            {"request": request, "book": None, "error": "ISBN duplicado", "user": user},
            status_code=400,
        )


@app.get("/books/{book_id}/edit")
def books_edit(
    book_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(login_required),
):
    book = crud.get_book(db, book_id)
    if not book:
        return RedirectResponse(url="/books", status_code=302)
    return templates.TemplateResponse(
        "book_form.html", {"request": request, "book": book, "user": user}
    )


@app.post("/books/{book_id}/edit")
def books_update(
    book_id: int,
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(...),
    category: Optional[str] = Form(None),
    status: str = Form("AVAILABLE"),
    db: Session = Depends(get_db),
    user=Depends(login_required),
):
    book = crud.get_book(db, book_id)
    if not book:
        return RedirectResponse(url="/books", status_code=302)
    try:
        crud.update_book(
            db,
            book,
            BookUpdate(
                title=title, author=author, isbn=isbn, category=category, status=status
            ),
        )
        return RedirectResponse(url="/books", status_code=302)
    except IntegrityError:
        return templates.TemplateResponse(
            "book_form.html",
            {"request": request, "book": book, "error": "ISBN duplicado", "user": user},
            status_code=400,
        )


@app.post("/books/{book_id}/delete")
def books_delete(
    book_id: int, db: Session = Depends(get_db), user=Depends(login_required)
):
    book = crud.get_book(db, book_id)
    if book:
        crud.delete_book(db, book)
    return RedirectResponse(url="/books", status_code=302)
