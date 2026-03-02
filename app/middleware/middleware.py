from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.auth_service import decode_token
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ["/", "/login", "/register", "/products", "/product/", "/static"]

        path = request.url.path
        is_public = any(path.startswith(p) for p in public_paths)

        if not is_public:
            token = request.cookies.get("access_token")
            if not token:
                logger.warning(f"Acceso denegado a {path} - Sin token")

        response = await call_next(request)
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
