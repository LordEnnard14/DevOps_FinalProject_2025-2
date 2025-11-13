# tests/api/test_api_more.py
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_book_payload(
    title="B1", author="A1", isbn="111", category="C1", status="AVAILABLE"
):
    return {
        "title": title,
        "author": author,
        "isbn": isbn,
        "category": category,
        "status": status,
    }


def test_get_book_not_found():
    r = client.get("/api/books/99999")
    assert r.status_code == 404


def test_update_book_and_conflict():
    # crea dos libros
    r1 = client.post("/api/books", json=create_book_payload(title="L1", isbn="ISBN-L1"))
    r2 = client.post("/api/books", json=create_book_payload(title="L2", isbn="ISBN-L2"))
    assert r1.status_code == 201 and r2.status_code == 201

    b1 = r1.json()
    b2 = r2.json()

    # actualizar OK
    r_ok = client.put(f"/api/books/{b1['id']}", json={"title": "L1-edit"})
    assert r_ok.status_code == 200
    assert r_ok.json()["title"] == "L1-edit"

    # conflicto: intentar poner ISBN de L2 en L1
    r_conflict = client.put(f"/api/books/{b1['id']}", json={"isbn": b2["isbn"]})
    assert r_conflict.status_code == 409


def test_delete_book_and_then_404():
    r = client.post("/api/books", json=create_book_payload(title="L3", isbn="ISBN-L3"))
    assert r.status_code == 201
    book_id = r.json()["id"]

    r_del = client.delete(f"/api/books/{book_id}")
    assert r_del.status_code == 204

    r_again = client.get(f"/api/books/{book_id}")
    assert r_again.status_code == 404
