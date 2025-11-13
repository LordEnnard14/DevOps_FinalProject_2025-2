from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_protected_without_login():
    r = client.get("/books", follow_redirects=False)
    # 401 por login_required
    assert r.status_code == 401


def test_root_redirects_to_books():
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (302, 307)
    assert r.headers["location"] == "/books"
