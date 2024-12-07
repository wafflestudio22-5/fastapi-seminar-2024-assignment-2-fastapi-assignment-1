from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from wapang.app.order.dto.requests import PlaceOrderRequest
from wapang.app.order.dto.responses import OrderDetailResponse
from wapang.app.order.service import OrderService
from wapang.app.user.models import User
from wapang.app.user.views import login_with_header


order_router = APIRouter()


@order_router.post("", status_code=HTTP_201_CREATED)
async def place_order(
    user: Annotated[User, Depends(login_with_header)],
    order_service: Annotated[OrderService, Depends()],
    place_order_request: PlaceOrderRequest,
) -> OrderDetailResponse:
    return await order_service.place_order(user.id, place_order_request)


@order_router.get("/{order_id}", status_code=HTTP_200_OK)
async def search_order(
    user: Annotated[User, Depends(login_with_header)],
    order_id: int,
    order_service: Annotated[OrderService, Depends()],
) -> OrderDetailResponse:
    return await order_service.search_order(user.id, order_id)


@order_router.delete("/{order_id}", status_code=HTTP_204_NO_CONTENT)
async def cancel_order(
    user: Annotated[User, Depends(login_with_header)],
    order_id: int,
    order_service: Annotated[OrderService, Depends()],
) -> None:
    await order_service.cancel_order(user.id, order_id)


@order_router.post("/{order_id}/complete", status_code=HTTP_204_NO_CONTENT)
async def confirm_order(
    user: Annotated[User, Depends(login_with_header)],
    order_id: int,
    order_service: Annotated[OrderService, Depends()],
) -> None:
    await order_service.confirm_order(user.id, order_id)
