from typing import Annotated
from fastapi import APIRouter, Depends

from wapang.app.store.dto.requests import StoreCreateRequest
from wapang.app.store.dto.responses import StoreDetailResponse
from wapang.app.store.service import StoreService
from wapang.app.user.models import User
from wapang.app.user.views import login_with_header


store_router = APIRouter()


@store_router.post("")
def create_store(
    user: Annotated[User, Depends(login_with_header)],
    store_service: Annotated[StoreService, Depends()],
    store_create_request: StoreCreateRequest,
) -> StoreDetailResponse:
    return store_service.create_store(
        user,
        store_create_request.store_name,
        store_create_request.address,
        store_create_request.email,
        store_create_request.phone_number,
    )

@store_router.get("/{store_id}")
def get_store(
    store_id: int,
    store_service: Annotated[StoreService, Depends()],
) -> StoreDetailResponse:
    return store_service.get_store_by_id(store_id)
