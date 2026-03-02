from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = None
db = None


async def connect_db():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    await db.users.create_index("email", unique=True)
    await db.products.create_index("sku", unique=True)
    await db.orders.create_index("user_id")
    await db.cart.create_index("user_id")

    return db


async def close_db():
    global client
    if client:
        client.close()


def get_db():
    return db
