from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_book():
    payload = {
        "titulo": "Libro Test",
        "isbn": "ISBN-1234",
        "author": "Autor Test",
        "category": "Ficción",
        "state": "Disponible",
        "genres": ["Aventura"]
    }
    r = client.post("/books", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["titulo"] == "Libro Test"
    r2 = client.get("/books")
    assert r2.status_code == 200
    assert any(b["isbn"] == "ISBN-1234" for b in r2.json())
