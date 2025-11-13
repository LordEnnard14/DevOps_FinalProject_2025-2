# tests/conftest.py
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Hace importable el paquete 'app'
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db import Base, get_db
from app.main import app
from app.models import Book


@pytest.fixture(scope="session")
def test_engine(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("data") / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    # Limpieza ordenada
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(
        bind=test_engine, autocommit=False, autoflush=False
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def override_dependency(db_session):
    # Sobrescribe get_db para que TODO el app use esta sesión de prueba
    def _get_db_for_tests():
        try:
            yield db_session
        finally:
            pass  # el fixture cierra

    app.dependency_overrides[get_db] = _get_db_for_tests
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clean_db(db_session):
    db_session.query(Book).delete()
    db_session.commit()
    yield
