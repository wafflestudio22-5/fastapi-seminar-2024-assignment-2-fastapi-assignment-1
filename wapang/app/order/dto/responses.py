from pydantic import BaseModel

from wapang.app.order.models import OrderStatus


class OrderItemResponse(BaseModel):
    item_id: int
    quantity: int


class OrderDetailResponse(BaseModel):
    order_id: int
    items: list[OrderItemResponse]
    status: OrderStatus
