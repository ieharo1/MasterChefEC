from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.routes.auth import get_current_user
from app.repositories.repository import (
    ProductRepository,
    CategoryRepository,
    UserRepository,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def require_admin(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return None
    return user_id


@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return templates.TemplateResponse("admin.html", {"request": request, "user": user})


@router.get("/admin/products", response_class=HTMLResponse)
async def admin_products(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    products = await ProductRepository.get_all_products()
    categories = await CategoryRepository.get_all_categories()
    return templates.TemplateResponse(
        "admin_products.html",
        {"request": request, "products": products, "categories": categories},
    )


@router.post("/admin/products/create")
async def create_product(
    request: Request,
    name: str,
    description: str,
    price: float,
    category_id: str,
    sku: str,
    stock: int,
    image: str = None,
):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        return {"success": False, "message": "Acceso denegado"}

    product = await ProductRepository.create_product(
        name=name,
        description=description,
        price=price,
        category_id=category_id,
        sku=sku,
        stock=stock,
        image=image,
    )
    return {"success": True, "product_id": product.id}


@router.post("/admin/products/{product_id}/update")
async def update_product(
    request: Request,
    product_id: str,
    name: str = None,
    description: str = None,
    price: float = None,
    category_id: str = None,
    sku: str = None,
    stock: int = None,
    image: str = None,
    is_active: bool = None,
):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        return {"success": False, "message": "Acceso denegado"}

    update_data = {}
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if price is not None:
        update_data["price"] = price
    if category_id is not None:
        update_data["category_id"] = category_id
    if sku is not None:
        update_data["sku"] = sku
    if stock is not None:
        update_data["stock"] = stock
    if image is not None:
        update_data["image"] = image
    if is_active is not None:
        update_data["is_active"] = is_active

    await ProductRepository.update_product(product_id, update_data)
    return {"success": True}


@router.post("/admin/products/{product_id}/delete")
async def delete_product(request: Request, product_id: str):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        return {"success": False, "message": "Acceso denegado"}

    await ProductRepository.delete_product(product_id)
    return {"success": True}


@router.get("/admin/categories", response_class=HTMLResponse)
async def admin_categories(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    categories = await CategoryRepository.get_all_categories()
    return templates.TemplateResponse(
        "admin_categories.html", {"request": request, "categories": categories}
    )


@router.post("/admin/categories/create")
async def create_category(
    request: Request, name: str, description: str = None, image: str = None
):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        return {"success": False, "message": "Acceso denegado"}

    category = await CategoryRepository.create_category(
        name=name, description=description, image=image
    )
    return {"success": True, "category_id": category.id}


@router.post("/admin/categories/{category_id}/update")
async def update_category(
    request: Request,
    category_id: str,
    name: str = None,
    description: str = None,
    image: str = None,
):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        return {"success": False, "message": "Acceso denegado"}

    update_data = {}
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if image is not None:
        update_data["image"] = image

    await CategoryRepository.update_category(category_id, update_data)
    return {"success": True}


@router.post("/admin/categories/{category_id}/delete")
async def delete_category(request: Request, category_id: str):
    user_id = get_current_user(request)
    if not user_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        return {"success": False, "message": "Acceso denegado"}

    await CategoryRepository.delete_category(category_id)
    return {"success": True}


@router.get("/admin/users", response_class=HTMLResponse)
async def admin_users(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = await UserRepository.get_user_by_id(user_id)
    if not user or user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    users = await UserRepository.get_all_users()
    return templates.TemplateResponse(
        "admin_users.html", {"request": request, "users": users}
    )


@router.post("/admin/users/{user_id}/update")
async def update_user(
    request: Request, user_id: str, role: str = None, is_active: bool = None
):
    admin_id = get_current_user(request)
    if not admin_id:
        return {"success": False, "message": "Debe iniciar sesión"}

    admin = await UserRepository.get_user_by_id(admin_id)
    if not admin or admin.role.value != "admin":
        return {"success": False, "message": "Acceso denegado"}

    update_data = {}
    if role is not None:
        update_data["role"] = role
    if is_active is not None:
        update_data["is_active"] = is_active

    await UserRepository.update_user(user_id, update_data)
    return {"success": True}
