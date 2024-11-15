from typing import Annotated

from fastapi import Depends
from sqlalchemy import insert, update
from sqlalchemy.orm import Session

from wapang.app.item.models import Item
from wapang.app.order.enums import OrderStatus
from wapang.app.order.models import Order, OrderItem
from wapang.database.connection import get_db_session


class OrderStore:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]):
        self.session = session

    def create_order(self, orderer_id: int, items: list[tuple[int, int]]) -> Order:
        # 재고를 먼저 차감하고, 주문을 생성
        for item_id, quantity in items:
            self.session.execute(
                update(Item)
                .where(Item.id == item_id)
                .values(stock=Item.stock - quantity)
            )

        order = Order(orderer_id=orderer_id, status=OrderStatus.ORDERED)
        self.session.add(order)
        # 주문 생성 후, id를 얻기 위해 flush
        self.session.flush()

        # bulk insert
        self.session.execute(
            insert(OrderItem),
            [
                {"order_id": order.id, "item_id": item_id, "quantity": quantity}
                for item_id, quantity in items
            ],
        )
        return order

    def get_order_by_id(self, order_id: int) -> Order | None:
        order = self.session.get(Order, order_id)
        return order

    def update_order_status(self, order: Order, status: OrderStatus) -> Order | None:
        self.session.execute(
            update(Order)
            .where(Order.id == order.id)
            .values({Order.status: status})
        )
        return order
