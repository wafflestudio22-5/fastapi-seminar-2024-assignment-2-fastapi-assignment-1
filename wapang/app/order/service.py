from typing import Annotated

from fastapi import Depends

from wapang.app.order.dto.requests import PlaceOrderRequest
from wapang.app.order.dto.responses import OrderItemResponse, OrderDetailResponse
from wapang.app.order.enums import OrderStatus
from wapang.app.order.errors import AlreadyCanceledError, OrderNotFoundError
from wapang.app.order.store import OrderStore
from wapang.app.user.errors import PermissionDeniedError


class OrderService:
    def __init__(self, order_store: Annotated[OrderStore, Depends()]):
        self.order_store = order_store

    def place_order(
        self, user_id: int, place_order_request: PlaceOrderRequest
    ) -> OrderDetailResponse:
        items = [(item.item_id, item.quantity) for item in place_order_request.items]
        order = self.order_store.create_order(user_id, items)
        return OrderDetailResponse(
            order_id=order.id,
            items=[
                OrderItemResponse.model_validate(order_item, from_attributes=True)
                for order_item in order.order_items
            ],
            status=order.status,
        )

    def search_order(self, order_id: int) -> OrderDetailResponse:
        order = self.order_store.get_order_by_id(order_id)
        if order is None:
            raise OrderNotFoundError()
        return OrderDetailResponse(
            order_id=order.id,
            items=[
                OrderItemResponse.model_validate(order_item, from_attributes=True)
                for order_item in order.order_items
            ],
            status=order.status,
        )

    def cancel_order(self, user_id: int, order_id: int) -> None:
        order = self.order_store.get_order_by_id(order_id)
        if order is None:
            raise OrderNotFoundError()
        if order.orderer_id != user_id:
            raise PermissionDeniedError()
        if order.status == OrderStatus.CANCELED:
            raise AlreadyCanceledError()
        self.order_store.update_order_status(order, OrderStatus.CANCELED)

    def confirm_order(self, user_id: int, order_id: int) -> None:
        order = self.order_store.get_order_by_id(order_id)
        if order is None:
            raise OrderNotFoundError()
        if order.orderer_id != user_id:
            raise PermissionDeniedError()
        if order.status == OrderStatus.CANCELED:
            raise AlreadyCanceledError()
        self.order_store.update_order_status(order, OrderStatus.COMPLETE)
