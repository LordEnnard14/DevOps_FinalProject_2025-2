# tests/ui/test_views_jinja.py
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_view_get():
    r = client.get("/login")
    assert r.status_code == 200
    assert "Iniciar sesión" in r.text


def test_login_bad_credentials():
    r = client.post("/login", data={"username": "x", "password": "y"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Credenciales inválidas"


def test_login_ok_and_access_protected_views():
    # login correcto
    r = client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=False,
    )
    assert r.status_code == 302
    assert r.headers["location"] == "/books"

    # guarda cookie de sesión
    session_cookie = r.cookies.get("session")
    assert session_cookie

    # acceder a /books
    r2 = client.get("/books", cookies={"session": session_cookie})
    assert r2.status_code == 200
    assert "Libros" in r2.text


def test_books_new_and_duplicate_isbn_flow():
    # login
    r = client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=False,
    )
    cookie = r.cookies

    # crear libro por formulario
    form = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "category": "Software",
        "status": "AVAILABLE",
    }
    r_new = client.post("/books/new", data=form, cookies=cookie, follow_redirects=False)
    assert r_new.status_code == 302 and r_new.headers["location"] == "/books"

    # intentar duplicado: vuelve a /books/new
    r_dup = client.post("/books/new", data=form, cookies=cookie)
    # Debe devolver página con error (400)
    assert r_dup.status_code == 400
    assert "ISBN duplicado" in r_dup.text


def test_books_edit_and_delete():
    # login
    r = client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=False,
    )
    cookie = r.cookies

    # crea uno nuevo
    form = {
        "title": "Refactoring",
        "author": "Martin Fowler",
        "isbn": f"9780201485677-{uuid4()}",
        "category": "Software",
        "status": "AVAILABLE",
    }
    r_new = client.post("/books/new", data=form, cookies=cookie, follow_redirects=False)
    assert r_new.status_code == 302

    # lista para hallar el id mostrado en HTML
    r_list = client.get("/books", cookies=cookie)
    assert r_list.status_code == 200
    assert "Refactoring" in r_list.text

    # no necesitamos el id exacto aquí porque ya cubrimos update en API tests;
    # lo importante es cubrir POST /books/{id}/edit y /books/{id}/delete también:
    # Detecta el id a partir del html (opcional). En lugar de parsear, creamos por API:
    # Crea por API para conocer el id:
    r_api = client.post(
        "/api/books",
        json={
            "title": "T",
            "author": "A",
            "isbn": f"I-{uuid4()}",
            "category": "C",
            "status": "AVAILABLE",
        },
    )
    book_id = r_api.json()["id"]

    # GET edit page
    r_edit_get = client.get(f"/books/{book_id}/edit", cookies=cookie)
    assert r_edit_get.status_code == 200
    assert "Editar" in r_edit_get.text

    # POST edit (form)
    r_edit_post = client.post(
        f"/books/{book_id}/edit",
        data={
            "title": "T2",
            "author": "A2",
            "isbn": f"I-{uuid4()}",
            "category": "C",
            "status": "AVAILABLE",
        },
        cookies=cookie,
        follow_redirects=False,
    )
    assert (
        r_edit_post.status_code == 302 and r_edit_post.headers["location"] == "/books"
    )

    # DELETE (form)
    r_del = client.post(
        f"/books/{book_id}/delete", cookies=cookie, follow_redirects=False
    )
    assert r_del.status_code == 302 and r_del.headers["location"] == "/books"
