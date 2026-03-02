from datetime import datetime
from typing import Optional, List
from app.schemas.schemas import UserRole, OrderStatus


class User:
    def __init__(
        self,
        email: str,
        name: str,
        hashed_password: str,
        phone: Optional[str] = None,
        role: UserRole = UserRole.CLIENT,
        is_active: bool = True,
        created_at: datetime = None,
        updated_at: datetime = None,
        _id: str = None,
    ):
        self.id = str(_id) if _id else None
        self.email = email
        self.name = name
        self.hashed_password = hashed_password
        self.phone = phone
        self.role = role
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            "email": self.email,
            "name": self.name,
            "hashed_password": self.hashed_password,
            "phone": self.phone,
            "role": self.role.value if isinstance(self.role, UserRole) else self.role,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict):
        return User(
            email=data.get("email"),
            name=data.get("name"),
            hashed_password=data.get("hashed_password"),
            phone=data.get("phone"),
            role=data.get("role", UserRole.CLIENT),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            _id=data.get("_id"),
        )


class Category:
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        image: Optional[str] = None,
        created_at: datetime = None,
        _id: str = None,
    ):
        self.id = str(_id) if _id else None
        self.name = name
        self.description = description
        self.image = image
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: dict):
        return Category(
            name=data.get("name"),
            description=data.get("description"),
            image=data.get("image"),
            created_at=data.get("created_at"),
            _id=data.get("_id"),
        )


class Product:
    def __init__(
        self,
        name: str,
        description: Optional[str],
        price: float,
        category_id: str,
        sku: str,
        stock: int = 0,
        image: Optional[str] = None,
        is_active: bool = True,
        created_at: datetime = None,
        updated_at: datetime = None,
        _id: str = None,
    ):
        self.id = str(_id) if _id else None
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.sku = sku
        self.stock = stock
        self.image = image
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category_id": self.category_id,
            "sku": self.sku,
            "stock": self.stock,
            "image": self.image,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict):
        return Product(
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price"),
            category_id=data.get("category_id"),
            sku=data.get("sku"),
            stock=data.get("stock", 0),
            image=data.get("image"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            _id=data.get("_id"),
        )


class Cart:
    def __init__(self, user_id: str, items: List[dict] = None, _id: str = None):
        self.id = str(_id) if _id else None
        self.user_id = user_id
        self.items = items or []

    def to_dict(self):
        return {"user_id": self.user_id, "items": self.items}

    @staticmethod
    def from_dict(data: dict):
        return Cart(
            user_id=data.get("user_id"),
            items=data.get("items", []),
            _id=data.get("_id"),
        )


class Order:
    def __init__(
        self,
        user_id: str,
        items: List[dict],
        total: float,
        status: OrderStatus = OrderStatus.PENDING,
        shipping_address: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        _id: str = None,
    ):
        self.id = str(_id) if _id else None
        self.user_id = user_id
        self.items = items
        self.total = total
        self.status = status if isinstance(status, OrderStatus) else OrderStatus(status)
        self.shipping_address = shipping_address
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "items": self.items,
            "total": self.total,
            "status": self.status.value
            if isinstance(self.status, OrderStatus)
            else self.status,
            "shipping_address": self.shipping_address,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict):
        return Order(
            user_id=data.get("user_id"),
            items=data.get("items", []),
            total=data.get("total"),
            status=data.get("status", OrderStatus.PENDING),
            shipping_address=data.get("shipping_address"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            _id=data.get("_id"),
        )
