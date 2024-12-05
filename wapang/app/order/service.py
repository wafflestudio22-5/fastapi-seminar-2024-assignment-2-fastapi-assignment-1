from typing import Annotated

from fastapi import Depends

from wapang.app.item.errors import ItemNotFoundError
from wapang.app.item.store import ItemStore
from wapang.app.order.dto.requests import PlaceOrderRequest
from wapang.app.order.dto.responses import OrderItemResponse, OrderDetailResponse
from wapang.app.order.enums import OrderStatus
from wapang.app.order.errors import (
    AlreadyCanceledError,
    NotEnoughStockError,
    OrderNotFoundError,
)
from wapang.app.order.store import OrderStore
from wapang.app.user.errors import PermissionDeniedError
from wapang.database.annotation import transactional


class OrderService:
    def __init__(
        self,
        order_store: Annotated[OrderStore, Depends()],
        item_store: Annotated[ItemStore, Depends()],
    ):
        self.order_store = order_store
        self.item_store = item_store

    @transactional
    async def place_order(
        self, user_id: int, place_order_request: PlaceOrderRequest
    ) -> OrderDetailResponse:
        # 모든 item의 재고가 충분한지 확인
        # 재고가 충분하다면, 주문 생성 전에 재고 차감
        request_items = [
            (item.item_id, item.quantity) for item in place_order_request.items
        ]
        current_items = await self.item_store.get_items_by_ids(
            [item_id for item_id, _ in request_items]
        )
        current_items = {item.id: item for item in current_items}
        if len(current_items) != len(request_items):
            raise ItemNotFoundError()

        for item_id, quantity in request_items:
            if current_items[item_id].stock < quantity:
                raise NotEnoughStockError()
            else:
                current_items[item_id].stock -= quantity

        order = await self.order_store.create_order(user_id, request_items)
        return OrderDetailResponse(
            order_id=order.id,
            items=[
                OrderItemResponse.model_validate(order_item, from_attributes=True)
                for order_item in await order.awaitable_attrs.order_items
            ],
            status=order.status,
        )

    async def search_order(self, user_id: int, order_id: int) -> OrderDetailResponse:
        order = await self.order_store.get_order_by_id(order_id)
        if order is None:
            raise OrderNotFoundError()
        if order.orderer_id != user_id:
            raise PermissionDeniedError()
        return OrderDetailResponse(
            order_id=order.id,
            items=[
                OrderItemResponse.model_validate(order_item, from_attributes=True)
                for order_item in await order.awaitable_attrs.order_items
            ],
            status=order.status,
        )

    async def cancel_order(self, user_id: int, order_id: int) -> None:
        order = await self.order_store.get_order_by_id(order_id)
        if order is None:
            raise OrderNotFoundError()
        if order.orderer_id != user_id:
            raise PermissionDeniedError()
        if order.status == OrderStatus.CANCELED:
            raise AlreadyCanceledError()
        await self.order_store.update_order_status(order, OrderStatus.CANCELED)

    async def confirm_order(self, user_id: int, order_id: int) -> None:
        order = await self.order_store.get_order_by_id(order_id)
        if order is None:
            raise OrderNotFoundError()
        if order.orderer_id != user_id:
            raise PermissionDeniedError()
        if order.status == OrderStatus.CANCELED:
            raise AlreadyCanceledError()
        await self.order_store.update_order_status(order, OrderStatus.COMPLETE)
