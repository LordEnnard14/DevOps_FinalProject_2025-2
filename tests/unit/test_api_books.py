from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_book_api():
    payload = {
        "title": "Refactoring",
        "author": "Martin Fowler",
        "isbn": f"9780201485677-{uuid4()}",
        "category": "Software",
        "status": "AVAILABLE",
    }
    r = client.post("/api/books", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["id"] > 0
    assert data["title"] == "Refactoring"
