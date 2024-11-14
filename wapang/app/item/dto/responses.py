from typing import Self
from pydantic import BaseModel

from wapang.app.item.models import Item


class ItemDetailResponse(BaseModel):
    id: int
    item_name: str
    price: int
    stock: int

    @staticmethod
    def from_item(item: Item) -> "ItemDetailResponse":
        return ItemDetailResponse(
            id=item.id, item_name=item.name, price=item.price, stock=item.stock
        )


class ItemDetailInListResponse(BaseModel):
    id: int
    item_name: str
    price: int
    quantity: int

    @staticmethod
    def from_item(item: Item) -> "ItemDetailInListResponse":
        return ItemDetailInListResponse(
            id=item.id, item_name=item.name, price=item.price, quantity=item.stock
        )
