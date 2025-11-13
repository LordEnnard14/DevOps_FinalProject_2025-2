import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.crud import create_book, get_book, list_books
from app.db import Base
from app.schemas import BookCreate


@pytest.fixture
def db_session(tmp_path):
    # DB SQLite temporal para pruebas unitarias
    engine = create_engine(
        f"sqlite:///{tmp_path}/test.db", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_and_get_book(db_session):
    payload = BookCreate(
        title="Clean Code",
        author="Robert C. Martin",
        isbn="9780132350884",
        category="Software",
        status="AVAILABLE",
    )
    book = create_book(db_session, payload)
    assert book.id is not None
    fetched = get_book(db_session, book.id)
    assert fetched.title == "Clean Code"


def test_list_books(db_session):
    assert list_books(db_session) == []
