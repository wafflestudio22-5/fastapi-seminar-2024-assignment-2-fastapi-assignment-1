from typing import Annotated
from fastapi import APIRouter, Depends

from wapang.app.store.dto.requests import StoreCreateRequest
from wapang.app.store.dto.responses import StoreCreateResponse
from wapang.app.store.service import StoreService
from wapang.app.user.models import User
from wapang.app.user.views import login_with_header


store_router = APIRouter()


@store_router.post("")
def create_store(
    user: Annotated[User, Depends(login_with_header)],
    store_service: Annotated[StoreService, Depends()],
    store_create_request: StoreCreateRequest,
) -> StoreCreateResponse:
    return store_service.create_store(
        user,
        store_create_request.store_name,
        store_create_request.address,
        store_create_request.email,
        store_create_request.phone_number,
    )
