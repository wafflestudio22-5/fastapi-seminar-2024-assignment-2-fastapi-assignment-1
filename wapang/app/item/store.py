from typing import Sequence
from sqlalchemy.sql import select
from sqlalchemy.orm import joinedload

from wapang.app.item.models import Item
from wapang.app.store.models import Store
from wapang.database.connection import SESSION


class ItemStore:
    async def create_item(
        self, store_id: int, item_name: str, price: int, stock: int
    ) -> Item:
        item = Item(store_id=store_id, name=item_name, price=price, stock=stock)
        SESSION.add(item)
        await SESSION.flush()
        return item

    async def get_item_by_id(self, item_id: int) -> Item | None:
        item = await SESSION.get(Item, item_id)
        return item

    async def update_item(
        self,
        item: Item,
        item_name: str | None = None,
        item_price: int | None = None,
        item_stock: int | None = None,
    ) -> Item:
        if item_name is not None:
            item.name = item_name
        if item_price is not None:
            item.price = item_price
        if item_stock is not None:
            item.stock = item_stock
        await SESSION.flush()
        return item

    async def get_items(
        self,
        store_name: str | None = None,
        max_price: int | None = None,
        min_price: int | None = None,
        in_stock: bool | None = None,
    ) -> Sequence[Item]:
        items_list_query = select(Item).options(joinedload((Item.store)))
        if store_name is not None:
            items_list_query = items_list_query.join(Store).where(
                Store.name == store_name
            )
        if max_price is not None:
            items_list_query = items_list_query.where(Item.price <= max_price)
        if min_price is not None:
            items_list_query = items_list_query.where(Item.price >= min_price)
        if in_stock:
            items_list_query = items_list_query.where(Item.stock > 0)
        return (await SESSION.scalars(items_list_query)).all()

    async def get_items_by_ids(self, item_ids: list[int]) -> Sequence[Item]:
        items_list_query = select(Item).where(Item.id.in_(item_ids))
        return (await SESSION.scalars(items_list_query)).all()
