from typing import Annotated, Sequence
from fastapi import Depends
from sqlalchemy.sql import literal, select
from sqlalchemy.orm import Session, joinedload

from wapang.app.item.errors import ItemNotFoundError
from wapang.app.item.models import Item
from wapang.app.store.models import Store
from wapang.database.connection import get_db_session


class ItemStore:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]):
        self.session = session

    def create_item(
        self, store_id: int, item_name: str, price: int, stock: int
    ) -> Item:
        item = Item(store_id=store_id, name=item_name, price=price, stock=stock)
        self.session.add(item)
        self.session.commit()
        return item
    
    def get_item_by_id(self, item_id: int) -> Item | None:
        item = self.session.get(Item, item_id)
        return item

    def update_item(
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
        self.session.commit()
        return item

    def list_items(
        self,
        store_name: str | None = None,
        max_price: int | None = None,
        min_price: int | None = None,
        in_stock: bool | None = None,
    ) -> Sequence[Item]:
        filter_conditions = literal(True)
        if store_name is not None:
            filter_conditions &= Store.name == store_name
        if max_price is not None:
            filter_conditions &= Item.price <= max_price
        if min_price is not None:
            filter_conditions &= Item.price >= min_price
        if in_stock is not None:
            filter_conditions &= Item.stock > 0

        items_list_query = (
            select(Item).where(filter_conditions).options(joinedload((Item.store)))
        )

        return self.session.scalars(items_list_query).all()
