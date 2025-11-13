# app/auth.py
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeSerializer

SECRET = "cambia-esto"
serializer = URLSafeSerializer(SECRET, salt="session")
router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


def get_current_user(request: Request):
    token = request.cookies.get("session")
    if not token:
        return None
    try:
        data = serializer.loads(token)
        return data.get("user")
    except Exception:
        return None


def login_required(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


@router.get("/login")
def login_view(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_action(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin":
        token = serializer.dumps({"user": username})
        resp = RedirectResponse(url="/books", status_code=302)
        resp.set_cookie("session", token, httponly=True, samesite="lax")
        return resp
    raise HTTPException(status_code=400, detail="Credenciales inválidas")


@router.get("/logout")
def logout():
    resp = RedirectResponse(url="/login", status_code=302)
    resp.delete_cookie("session")
    return resp
