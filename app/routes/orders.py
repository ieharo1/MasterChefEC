from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.routes.auth import get_current_user
from app.repositories.repository import OrderRepository, UserRepository

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/orders", response_class=HTMLResponse)
async def list_orders(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    orders = await OrderRepository.get_user_orders(user_id)
    return templates.TemplateResponse(
        "orders.html", {"request": request, "orders": orders}
    )


@router.get("/order/{order_id}", response_class=HTMLResponse)
async def order_detail(request: Request, order_id: str):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    order = await OrderRepository.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    return templates.TemplateResponse(
        "order_detail.html", {"request": request, "order": order}
    )


@router.get("/admin/orders", response_class=HTMLResponse)
async def admin_orders(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    orders = await OrderRepository.get_all_orders()
    return templates.TemplateResponse(
        "admin_orders.html", {"request": request, "orders": orders}
    )


@router.post("/admin/orders/{order_id}/status")
async def update_order_status(request: Request, order_id: str, status: str):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        return {"success": False, "message": "Acceso denegado"}

    await OrderRepository.update_order_status(order_id, status)
    return {"success": True}
