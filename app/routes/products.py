from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.routes.auth import get_current_user, require_auth
from app.repositories.repository import (
    ProductRepository,
    CategoryRepository,
    CartRepository,
    OrderRepository,
)
from app.models.models import Product
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/products", response_class=HTMLResponse)
async def list_products(request: Request, category: Optional[str] = None):
    user_id = get_current_user(request)
    products = await ProductRepository.get_all_products(category_id=category)
    categories = await CategoryRepository.get_all_categories()
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "products": products,
            "categories": categories,
            "selected_category": category,
        },
    )


@router.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: str):
    product = await ProductRepository.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    category = await CategoryRepository.get_category_by_id(product.category_id)
    return templates.TemplateResponse(
        "product_detail.html",
        {"request": request, "product": product, "category": category},
    )


@router.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    cart = await CartRepository.get_cart(user_id)
    cart_items = []
    total = 0

    for item in cart.items:
        product = await ProductRepository.get_product_by_id(item.get("product_id"))
        if product:
            item_total = product.price * item.get("quantity", 1)
            total += item_total
            cart_items.append(
                {
                    "product": product,
                    "quantity": item.get("quantity", 1),
                    "total": item_total,
                }
            )

    return templates.TemplateResponse(
        "cart.html", {"request": request, "cart_items": cart_items, "total": total}
    )


@router.post("/cart/add")
async def add_to_cart(request: Request, product_id: str, quantity: int = 1):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    product = await ProductRepository.get_product_by_id(product_id)
    if not product:
        return {"success": False, "message": "Producto no encontrado"}

    await CartRepository.add_to_cart(user_id, product_id, quantity)
    return {"success": True, "message": "Producto agregado al carrito"}


@router.post("/cart/update")
async def update_cart(request: Request, product_id: str, quantity: int):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    await CartRepository.update_cart_item(user_id, product_id, quantity)
    return {"success": True}


@router.post("/cart/remove")
async def remove_from_cart(request: Request, product_id: str):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    await CartRepository.remove_from_cart(user_id, product_id)
    return {"success": True}


@router.post("/cart/checkout")
async def checkout(request: Request, shipping_address: str = None, notes: str = None):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    cart = await CartRepository.get_cart(user_id)
    if not cart.items:
        return {"success": False, "message": "El carrito está vacío"}

    items = []
    total = 0

    for item in cart.items:
        product = await ProductRepository.get_product_by_id(item.get("product_id"))
        if product:
            qty = item.get("quantity", 1)
            item_total = product.price * qty
            total += item_total
            items.append(
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "quantity": qty,
                    "unit_price": product.price,
                    "total_price": item_total,
                }
            )

            await ProductRepository.update_product(
                product.id, {"stock": product.stock - qty}
            )

    order = await OrderRepository.create_order(
        user_id, items, total, shipping_address, notes
    )
    await CartRepository.clear_cart(user_id)

    return {"success": True, "order_id": order.id}
