from typing import Annotated
from fastapi import Depends
from wapang.app.item.dto.responses import ItemDetailInListResponse, ItemDetailResponse
from wapang.app.item.errors import ItemNotFoundError
from wapang.app.item.store import ItemStore
from wapang.app.store.errors import StoreNotFoundError
from wapang.app.store.store import StoreStore
from wapang.app.user.errors import PermissionDeniedError
from wapang.app.user.models import User


class ItemService:
    def __init__(
        self,
        item_store: Annotated[ItemStore, Depends()],
        store_store: Annotated[StoreStore, Depends()],
    ):
        self.item_store = item_store
        self.store_store = store_store

    def create_item(
        self, user: User, item_name: str, price: int, stock: int
    ) -> ItemDetailResponse:
        user_store = self.store_store.get_store_of_user(user.id)
        if user_store is None:
            raise StoreNotFoundError()
        new_item = self.item_store.create_item(user_store.id, item_name, price, stock)
        return ItemDetailResponse.from_item(new_item)

    def update_item(
        self,
        user: User,
        item_id: int,
        item_name: str | None = None,
        price: int | None = None,
        stock: int | None = None,
    ) -> ItemDetailResponse:
        user_store = self.store_store.get_store_of_user(user.id)
        if user_store is None:
            raise StoreNotFoundError()

        item = self.item_store.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()

        if item.store_id != user_store.id:
            raise PermissionDeniedError()

        updated_item = self.item_store.update_item(item, item_name, price, stock)
        return ItemDetailResponse.from_item(updated_item)

    def list_items(
        self,
        store_name: str | None = None,
        max_price: int | None = None,
        min_price: int | None = None,
        in_stock: bool | None = None,
    ) -> list[ItemDetailInListResponse]:
        items = self.item_store.list_items(store_name, max_price, min_price, in_stock)
        return [ItemDetailInListResponse.from_item(item) for item in items]
