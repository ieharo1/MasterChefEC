from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserRole
from app.services.auth_service import get_password_hash, verify_password


class UserRepository:
    @staticmethod
    async def create_user(
        email: str,
        name: str,
        password: str,
        phone: Optional[str] = None,
        role: UserRole = UserRole.CLIENT,
    ):
        db = get_db()
        hashed_password = get_password_hash(password)
        user_data = {
            "email": email,
            "name": name,
            "hashed_password": hashed_password,
            "phone": phone,
            "role": role.value if isinstance(role, UserRole) else role,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        result = await db.users.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return User.from_dict(user_data)

    @staticmethod
    async def get_user_by_email(email: str):
        db = get_db()
        user_data = await db.users.find_one({"email": email})
        if user_data:
            return User.from_dict(user_data)
        return None

    @staticmethod
    async def get_user_by_id(user_id: str):
        db = get_db()
        try:
            user_data = await db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                return User.from_dict(user_data)
        except:
            pass
        return None

    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100):
        db = get_db()
        users = []
        async for user_data in db.users.find().skip(skip).limit(limit):
            users.append(User.from_dict(user_data))
        return users

    @staticmethod
    async def update_user(user_id: str, update_data: dict):
        db = get_db()
        update_data["updated_at"] = datetime.now()
        await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        return await UserRepository.get_user_by_id(user_id)

    @staticmethod
    async def delete_user(user_id: str):
        db = get_db()
        result = await db.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    @staticmethod
    async def authenticate_user(email: str, password: str):
        user = await UserRepository.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


class CategoryRepository:
    @staticmethod
    async def create_category(
        name: str, description: Optional[str] = None, image: Optional[str] = None
    ):
        db = get_db()
        category_data = {
            "name": name,
            "description": description,
            "image": image,
            "created_at": datetime.now(),
        }
        result = await db.categories.insert_one(category_data)
        category_data["_id"] = result.inserted_id
        from app.models.models import Category

        return Category.from_dict(category_data)

    @staticmethod
    async def get_category_by_id(category_id: str):
        db = get_db()
        try:
            category_data = await db.categories.find_one({"_id": ObjectId(category_id)})
            if category_data:
                from app.models.models import Category

                return Category.from_dict(category_data)
        except:
            pass
        return None

    @staticmethod
    async def get_all_categories():
        db = get_db()
        categories = []
        async for cat_data in db.categories.find():
            from app.models.models import Category

            categories.append(Category.from_dict(cat_data))
        return categories

    @staticmethod
    async def update_category(category_id: str, update_data: dict):
        db = get_db()
        await db.categories.update_one(
            {"_id": ObjectId(category_id)}, {"$set": update_data}
        )
        return await CategoryRepository.get_category_by_id(category_id)

    @staticmethod
    async def delete_category(category_id: str):
        db = get_db()
        result = await db.categories.delete_one({"_id": ObjectId(category_id)})
        return result.deleted_count > 0


class ProductRepository:
    @staticmethod
    async def create_product(
        name: str,
        description: Optional[str],
        price: float,
        category_id: str,
        sku: str,
        stock: int = 0,
        image: Optional[str] = None,
    ):
        db = get_db()
        product_data = {
            "name": name,
            "description": description,
            "price": price,
            "category_id": category_id,
            "sku": sku,
            "stock": stock,
            "image": image,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        result = await db.products.insert_one(product_data)
        product_data["_id"] = result.inserted_id
        from app.models.models import Product

        return Product.from_dict(product_data)

    @staticmethod
    async def get_product_by_id(product_id: str):
        db = get_db()
        try:
            product_data = await db.products.find_one({"_id": ObjectId(product_id)})
            if product_data:
                from app.models.models import Product

                return Product.from_dict(product_data)
        except:
            pass
        return None

    @staticmethod
    async def get_product_by_sku(sku: str):
        db = get_db()
        product_data = await db.products.find_one({"sku": sku})
        if product_data:
            from app.models.models import Product

            return Product.from_dict(product_data)
        return None

    @staticmethod
    async def get_all_products(
        category_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ):
        db = get_db()
        query = {}
        if category_id:
            query["category_id"] = category_id
        products = []
        async for prod_data in db.products.find(query).skip(skip).limit(limit):
            from app.models.models import Product

            products.append(Product.from_dict(prod_data))
        return products

    @staticmethod
    async def update_product(product_id: str, update_data: dict):
        db = get_db()
        update_data["updated_at"] = datetime.now()
        await db.products.update_one(
            {"_id": ObjectId(product_id)}, {"$set": update_data}
        )
        return await ProductRepository.get_product_by_id(product_id)

    @staticmethod
    async def delete_product(product_id: str):
        db = get_db()
        result = await db.products.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0


class CartRepository:
    @staticmethod
    async def get_cart(user_id: str):
        db = get_db()
        cart_data = await db.cart.find_one({"user_id": user_id})
        if cart_data:
            from app.models.models import Cart

            return Cart.from_dict(cart_data)
        return Cart(user_id=user_id)

    @staticmethod
    async def add_to_cart(user_id: str, product_id: str, quantity: int = 1):
        db = get_db()
        cart = await CartRepository.get_cart(user_id)

        found = False
        for item in cart.items:
            if item.get("product_id") == product_id:
                item["quantity"] += quantity
                found = True
                break

        if not found:
            cart.items.append({"product_id": product_id, "quantity": quantity})

        await db.cart.update_one(
            {"user_id": user_id}, {"$set": {"items": cart.items}}, upsert=True
        )
        return cart

    @staticmethod
    async def update_cart_item(user_id: str, product_id: str, quantity: int):
        db = get_db()
        cart = await CartRepository.get_cart(user_id)

        for item in cart.items:
            if item.get("product_id") == product_id:
                if quantity <= 0:
                    cart.items.remove(item)
                else:
                    item["quantity"] = quantity
                break

        await db.cart.update_one({"user_id": user_id}, {"$set": {"items": cart.items}})
        return cart

    @staticmethod
    async def remove_from_cart(user_id: str, product_id: str):
        db = get_db()
        cart = await CartRepository.get_cart(user_id)

        cart.items = [
            item for item in cart.items if item.get("product_id") != product_id
        ]

        await db.cart.update_one({"user_id": user_id}, {"$set": {"items": cart.items}})
        return cart

    @staticmethod
    async def clear_cart(user_id: str):
        db = get_db()
        await db.cart.update_one({"user_id": user_id}, {"$set": {"items": []}})


class OrderRepository:
    @staticmethod
    async def create_order(
        user_id: str,
        items: List[dict],
        total: float,
        shipping_address: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        db = get_db()
        from app.schemas.schemas import OrderStatus

        order_data = {
            "user_id": user_id,
            "items": items,
            "total": total,
            "status": OrderStatus.PENDING.value,
            "shipping_address": shipping_address,
            "notes": notes,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        result = await db.orders.insert_one(order_data)
        order_data["_id"] = result.inserted_id
        from app.models.models import Order

        return Order.from_dict(order_data)

    @staticmethod
    async def get_order_by_id(order_id: str):
        db = get_db()
        try:
            order_data = await db.orders.find_one({"_id": ObjectId(order_id)})
            if order_data:
                from app.models.models import Order

                return Order.from_dict(order_data)
        except:
            pass
        return None

    @staticmethod
    async def get_user_orders(user_id: str):
        db = get_db()
        orders = []
        async for order_data in db.orders.find({"user_id": user_id}).sort(
            "created_at", -1
        ):
            from app.models.models import Order

            orders.append(Order.from_dict(order_data))
        return orders

    @staticmethod
    async def get_all_orders(skip: int = 0, limit: int = 100):
        db = get_db()
        orders = []
        async for order_data in (
            db.orders.find().skip(skip).limit(limit).sort("created_at", -1)
        ):
            from app.models.models import Order

            orders.append(Order.from_dict(order_data))
        return orders

    @staticmethod
    async def update_order_status(order_id: str, status: str):
        db = get_db()
        from app.schemas.schemas import OrderStatus

        await db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": status, "updated_at": datetime.now()}},
        )
        return await OrderRepository.get_order_by_id(order_id)
