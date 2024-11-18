from fastapi import APIRouter

from wapang.app.user.views import user_router
from wapang.app.store.views import store_router
from wapang.app.item.views import item_router
from wapang.app.order.views import order_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(store_router, prefix="/stores", tags=["stores"])
api_router.include_router(item_router, prefix="/items", tags=["items"])
api_router.include_router(order_router, prefix="/orders", tags=["orders"])
