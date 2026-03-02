from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "MasterChefEC - Ecommerce"
    DEBUG: bool = True

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "masterchefec"

    SECRET_KEY: str = "masterchefec-secret-key-2026-seguro"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
