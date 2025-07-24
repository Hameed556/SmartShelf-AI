from fastapi import APIRouter
from app.api.v1.endpoints import products, admin, auth, health

api_v1_router = APIRouter()
api_v1_router.include_router(products.router, prefix="/products", tags=["products"])
api_v1_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(health.router, prefix="/health", tags=["health"]) 