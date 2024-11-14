from typing import Annotated
from fastapi import APIRouter, Depends
from wapang.app.item.dto.requests import ItemCreateRequest, ItemUpdateRequest
from wapang.app.item.dto.responses import ItemDetailInListResponse, ItemDetailResponse
from wapang.app.item.service import ItemService
from wapang.app.user.models import User
from wapang.app.user.views import login_with_header


item_router = APIRouter()


@item_router.post("/items")
def create_item(
    user: Annotated[User, Depends(login_with_header)],
    item: ItemCreateRequest,
    item_service: Annotated[ItemService, Depends()],
) -> ItemDetailResponse:
    return item_service.create_item(user, item.item_name, item.price, item.stock)


@item_router.patch("/items/{item_id}")
def update_item(
    user: Annotated[User, Depends(login_with_header)],
    item_id: int,
    item: ItemUpdateRequest,
    item_service: Annotated[ItemService, Depends()],
) -> ItemDetailResponse:
    return item_service.update_item(
        user, item_id, item.item_name, item.price, item.stock
    )


@item_router.get("/items")
def get_items(
    item_service: Annotated[ItemService, Depends()],
    store_name: str | None = None,
    max_price: int | None = None,
    min_price: int | None = None,
    in_stock: bool | None = None,
) -> list[ItemDetailInListResponse]:
    return item_service.list_items(store_name, max_price, min_price, in_stock)
