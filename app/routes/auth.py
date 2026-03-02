from fastapi import APIRouter, Request, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import timedelta
from app.config import settings
from app.services.auth_service import create_access_token, decode_token
from app.repositories.repository import UserRepository
from app.schemas.schemas import UserCreate, Token
from pydantic import EmailStr

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    user_id = decode_token(token)
    return user_id


async def require_auth(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="No autenticado")
    user = await UserRepository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user_id = get_current_user(request)
    if user_id:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    user_id = get_current_user(request)
    if user_id:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(
    request: Request, email: EmailStr, name: str, password: str, phone: str = None
):
    existing = await UserRepository.get_user_by_email(email)
    if existing:
        return {"success": False, "message": "El email ya está registrado"}

    user = await UserRepository.create_user(
        email=email, name=name, password=password, phone=phone
    )

    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(
        key="access_token", value=access_token, httponly=True, max_age=60 * 60
    )
    return response


@router.post("/login")
async def login(request: Request, email: str, password: str):
    user = await UserRepository.authenticate_user(email, password)
    if not user:
        return {"success": False, "message": "Email o contraseña incorrectos"}

    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(
        key="access_token", value=access_token, httponly=True, max_age=60 * 60
    )
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = await UserRepository.get_user_by_id(user_id)
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user}
    )
