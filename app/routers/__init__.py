from fastapi import APIRouter

from app.routers import categories, customers, orders, products

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(categories.router)
api_router.include_router(products.router)
api_router.include_router(customers.router)
api_router.include_router(orders.router)
