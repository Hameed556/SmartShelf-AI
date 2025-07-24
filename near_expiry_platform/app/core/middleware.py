from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        return response 