from sqlalchemy import insert

from wapang.app.order.enums import OrderStatus
from wapang.app.order.models import Order, OrderItem
from wapang.database.annotation import transactional
from wapang.database.connection import SESSION


class OrderStore:
    @transactional
    async def create_order(
        self, orderer_id: int, items: list[tuple[int, int]]
    ) -> Order:
        order = Order(orderer_id=orderer_id, status=OrderStatus.ORDERED)
        SESSION.add(order)
        # 주문 생성 후, id를 얻기 위해 flush
        await SESSION.flush()

        # bulk insert
        await SESSION.execute(
            insert(OrderItem),
            [
                {"order_id": order.id, "item_id": item_id, "quantity": quantity}
                for item_id, quantity in items
            ],
        )
        return order

    async def get_order_by_id(self, order_id: int) -> Order | None:
        order = await SESSION.get(Order, order_id)
        return order

    @transactional
    async def update_order_status(
        self, order: Order, status: OrderStatus
    ) -> Order | None:
        order.status = status
        await SESSION.flush()
        return order
