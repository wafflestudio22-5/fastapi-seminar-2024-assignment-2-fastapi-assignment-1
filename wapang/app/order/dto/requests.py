from pydantic import BaseModel


class OrderItemRequest(BaseModel):
    item_id: int
    quantity: int


class PlaceOrderRequest(BaseModel):
    items: list[OrderItemRequest]
