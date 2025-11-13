from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_logout_flow():
    r = client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=False,
    )
    assert r.status_code == 302
    cookie = r.cookies
    r2 = client.get("/logout", cookies=cookie, follow_redirects=False)
    assert r2.status_code == 302
    assert r2.headers["location"] == "/login"
